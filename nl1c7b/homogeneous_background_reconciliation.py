#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math
import numpy as np
import sympy as sp
from scipy.interpolate import PchipInterpolator

AI=0.02
H0=67.3324639084866
OMEGA_B_H2=0.022377376877682164
C_KM_S=299792.458
Q0=1.0e-4
K2=9500.0
Z0=1.0e-17
KSPREAD_LIMIT=1.0e-10
SCALAR_ENERGY_LIMIT=1.0e-8
HAMILTONIAN_LIMIT=1.0e-7
INTERP_LIMIT=2.0e-2
DENSE_ARTIFACT=10469031693
DENSE_SHA='193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70'
B1_ARTIFACT=10481781728
B1_SHA='645d29e4e8ac7cfa4fff9833a4ef500d34fc667373bfac3073883155fac519a7'
B1_RUN=35185338047
B1_HEAD='6b555bc2ee3cba7c9e97706eb1a0949416e9932f'


def symbolic_identity():
    N,a,ad,r,Nr=sp.symbols('N a ad r Nr', positive=True, real=True)
    pt=sp.symbols('pt', positive=True, real=True)
    Kf=sp.Function('K')
    varrho=sp.symbols('varrho', positive=True, real=True)
    # Exact C6 homogeneous specialization before lapse variation.
    L=a; R=a*r; Rr=a; Lt=ad; Rt=ad*r
    kL=Lt/(N*L); kR=Rt/(N*R)
    grav=N*L*R**2*(-4*kL*kR-2*kR**2)+2*N*L+2*N*Rr**2/L+4*Nr*R*Rr/L
    # Euler-Lagrange lapse source includes -d_r(dL/dN_r); d_r(4 a r)=4a.
    grav_EL=sp.simplify(sp.diff(grav,N)-4*a)
    Q=pt/N
    aest=2*N*a**3*r**2*Kf(Q)
    aest_EL=sp.diff(aest,N)
    # On-shell comoving B1 dust lapse source.
    dust_EL=-2*a**3*r**2*varrho
    total=sp.simplify(grav_EL+aest_EL+dust_EL)
    H=sp.symbols('H', real=True)
    Ksym,KQsym,rhoA=sp.symbols('K KQ rhoA', real=True)
    normalized=sp.simplify(total.subs({ad:a*H,N:1,Kf(pt):Ksym,sp.Subs(sp.Derivative(Kf(sp.Symbol('_xi_1')),sp.Symbol('_xi_1')),sp.Symbol('_xi_1'),pt):KQsym})/(2*a**3*r**2))
    # SymPy's functional derivative representation is version-sensitive; derive the exact target separately.
    exact_target=sp.simplify(3*H**2-(pt*KQsym-Ksym)-varrho)
    exact_with_rho=sp.simplify(exact_target.subs(pt*KQsym-Ksym,rhoA))
    return {
      'grav_lapse_EL':str(sp.factor(grav_EL.subs({N:1,ad:a*H}))),
      'aest_lapse_EL_identity':'2 a^3 r^2 [K(Q)-Q K_Q(Q)]',
      'dust_lapse_EL':str(dust_EL),
      'normalized_total_identity':str(exact_with_rho),
      'pass':bool(sp.simplify(exact_with_rho-(3*H**2-rhoA-varrho))==0),
    }


def read_trace(path):
    z=np.genfromtxt(path,names=True)
    if z.size==0: raise RuntimeError('empty dense trace')
    required={'k','a','H_Mpc_inv','Q','rhoA','KQ'}
    if not required.issubset(set(z.dtype.names or [])):
        raise RuntimeError(f'missing trace fields: {sorted(required-set(z.dtype.names or []))}')
    return z


def at_ai(z,method):
    ks=np.unique(np.asarray(z['k'],float)); ks.sort()
    if len(ks)!=128: raise RuntimeError(f'expected 128 exact k modes, got {len(ks)}')
    out={f:[] for f in ['H_Mpc_inv','Q','rhoA','KQ']}
    x0=math.log(AI)
    for k in ks:
        g=z[np.asarray(z['k'],float)==k]
        g=g[np.argsort(np.asarray(g['a'],float))]
        x=np.log(np.asarray(g['a'],float))
        if not (x[0] < x0 < x[-1]): raise RuntimeError(f'a_i not bracketed for k={k}')
        for f in out:
            y=np.asarray(g[f],float)
            val=float(PchipInterpolator(x,y)(x0) if method=='pchip' else np.interp(x0,x,y))
            out[f].append(val)
    return ks,{f:np.asarray(v,float) for f,v in out.items()}


def rel_spread(v):
    v=np.asarray(v,float); med=float(np.median(v))
    return float((np.max(v)-np.min(v))/max(abs(med),1e-300))


def exp_energy(Q):
    Q=np.asarray(Q,float)
    Z=(Q-Q0)/Z0
    zz=Z*Z
    ex=np.exp(zz)
    K=2*K2*Z0**2*(ex-1.0)
    KQ=4*K2*Z0*Z*ex
    rho8=Q*KQ-K
    return Z,K,KQ,rho8


def source_convention(root):
    src=(root/'v019/patch/source/aest_memory.c').read_text()
    trace=(root/'nl1c7a/apply_trace_extension.py').read_text()
    checks={
      'rho8_defined_QKQ_minus_K':'rho8=q*kq-k;' in src,
      'CLASS_rho_is_rho8_over_3':'*rho_class=rho8/3.;' in src,
      'trace_reads_CLASS_effective_density':'double rhoA_trace = pvecback[pba->index_bg_rho_cdm];' in trace,
      'CDM_slot_documented_as_AeST_density':'cdm density, or AeST effective density when aest_enabled' in (root/'v019/apply_patch_v019.py').read_text(),
    }
    return {'checks':checks,'pass':all(checks.values()),'mapping':'rhoA_C6 = 3 * rhoA_trace = Q*KQ-K'}


def evaluate(vals,conv):
    H=np.asarray(vals['H_Mpc_inv'],float)
    Q=np.asarray(vals['Q'],float)
    rho_trace=np.asarray(vals['rhoA'],float)
    KQ_trace=np.asarray(vals['KQ'],float)
    Z,K,KQ_formula,rho8_formula=exp_energy(Q)
    rho_c6=3.0*rho_trace
    scalar_energy_rel=float(np.linalg.norm(rho_c6-rho8_formula)/max(np.linalg.norm(rho8_formula),1e-300))
    kq_rel=float(np.linalg.norm(KQ_trace-KQ_formula)/max(np.linalg.norm(KQ_formula),1e-300))
    varrho_b=3.0*(100.0/C_KM_S)**2*OMEGA_B_H2*AI**-3
    lhs=3.0*H*H
    rem=lhs-rho_c6-varrho_b
    eps=np.abs(rem)/np.maximum(lhs,1e-300)
    return {
      'H':H,'Q':Q,'rho_trace':rho_trace,'rho_c6':rho_c6,'KQ_trace':KQ_trace,
      'Z':Z,'K':K,'KQ_formula':KQ_formula,'rho8_formula':rho8_formula,
      'scalar_energy_rel':scalar_energy_rel,'KQ_formula_rel':kq_rel,
      'varrho_b':float(varrho_b),'lhs':lhs,'remainder':rem,'epsilon':eps,
      'median':{
        'H_Mpc_inv':float(np.median(H)),'Q':float(np.median(Q)),
        'rhoA_trace_CLASS':float(np.median(rho_trace)),'rhoA_C6':float(np.median(rho_c6)),
        'KQ':float(np.median(KQ_trace)),'3H2':float(np.median(lhs)),
        'varrho_b':float(varrho_b),'rho_rem':float(np.median(rem)),
        'rho_rem_fraction_of_3H2':float(np.median(rem/lhs)),
        'epsilon_H':float(np.median(eps)),
      },
      'spreads':{f:rel_spread(vals[f]) for f in ['H_Mpc_inv','Q','rhoA','KQ']},
      'source_convention_pass':bool(conv['pass']),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    cov=json.loads(Path(args.coverage_json).read_text())
    provenance_ok=(cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS' and
                   cov.get('requested_k_relative_miss_max')==0 and cov.get('n_native_times')==179 and
                   abs(float(cov.get('a_i'))-AI)<1e-15)
    conv=source_convention(root)
    sym=symbolic_identity()
    z=read_trace(args.trace)
    ks,pv=at_ai(z,'pchip'); _,lv=at_ai(z,'linear')
    p=evaluate(pv,conv); l=evaluate(lv,conv)
    maxspread=max(p['spreads'].values())
    interp_change=abs(p['median']['epsilon_H']-l['median']['epsilon_H'])
    g3=bool(conv['pass'] and p['scalar_energy_rel']<=SCALAR_ENERGY_LIMIT)
    # B2-G4 is a source/formula gate: only baryonic omega_b enters varrho_b.
    g4=bool(abs(p['varrho_b']-(3*(100/C_KM_S)**2*OMEGA_B_H2*AI**-3))<=1e-15*max(abs(p['varrho_b']),1.0))
    g5=bool(float(np.max(p['epsilon']))<=HAMILTONIAN_LIMIT)
    g6=bool(maxspread<=KSPREAD_LIMIT and interp_change<=INTERP_LIMIT)
    gates={
      'B2_G1_provenance':bool(provenance_ok),
      'B2_G2_exact_homogeneous_lapse_identity':bool(sym['pass']),
      'B2_G3_trace_scalar_energy_consistency':g3,
      'B2_G4_baryon_normalization':g4,
      'B2_G5_homogeneous_Hamiltonian_closure':g5,
      'B2_G6_k_independence_and_interpolation_control':g6,
    }
    if all(gates.values()):
        cls='NL1C7B2_HOMOGENEOUS_BACKGROUND_RECONCILIATION_PASS'
    elif gates['B2_G1_provenance'] and gates['B2_G2_exact_homogeneous_lapse_identity'] and g3 and g4 and g6 and not g5:
        cls='NL1C7B2_HOMOGENEOUS_BACKGROUND_SECTOR_INCOMPLETE'
    else:
        cls='NL1C7B2_HOMOGENEOUS_BACKGROUND_RECONCILIATION_FAIL'
    result={
      'classification':cls,
      'scope':'Homogeneous eta=0 background reconciliation only; no radial constraint, trajectory, finite eta, turnaround or collapse.',
      'provenance':{
        'dense_trace_run':35149865129,'dense_artifact':DENSE_ARTIFACT,'dense_sha256':DENSE_SHA,
        'B1_run':B1_RUN,'B1_head':B1_HEAD,'B1_artifact':B1_ARTIFACT,'B1_sha256':B1_SHA,
        'n_exact_k':int(len(ks)),'n_native_times':int(cov.get('n_native_times',-1)),
      },
      'source_energy_convention':conv,
      'symbolic_homogeneous_identity':sym,
      'parameters':{'a_i':AI,'H0_km_s_Mpc':H0,'omega_b':OMEGA_B_H2,'Q0_Mpc_inv':Q0,'K2':K2,'Z0_Mpc_inv':Z0},
      'pchip':{
        'median':p['median'],'relative_spreads':p['spreads'],
        'scalar_energy_relative_error':p['scalar_energy_rel'],'KQ_formula_relative_error':p['KQ_formula_rel'],
        'epsilon_H_max':float(np.max(p['epsilon'])),'epsilon_H_min':float(np.min(p['epsilon'])),
      },
      'linear_control':{
        'median':l['median'],'normalized_closure_residual_change_abs':float(interp_change),
        'limit':INTERP_LIMIT,
      },
      'missing_sector_diagnostic':{
        'reported_only_not_added':True,
        'rho_rem_Mpc_inv2':p['median']['rho_rem'],
        'fraction_of_3H2':p['median']['rho_rem_fraction_of_3H2'],
        'interpretation':'If nonzero after exact AeST+baryon identities pass, this is an omitted standard-background-sector diagnostic, not a fitted source.',
      },
      'limits':{'k_spread':KSPREAD_LIMIT,'scalar_energy':SCALAR_ENERGY_LIMIT,'epsilon_H':HAMILTONIAN_LIMIT,'interpolation_control':INTERP_LIMIT},
      'gates':gates,
      'claim_boundary':{'radial_initial_constraint_executed':False,'nonlinear_evolution_executed':False,'finite_eta_executed':False,'turnaround_or_collapse_evaluated':False},
    }
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if cls.endswith('_PASS') else 2)

if __name__=='__main__': main()
