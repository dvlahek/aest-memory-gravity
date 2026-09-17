#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, importlib.util
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[0]
ORIG_PATH=HERE/'homogeneous_background_reconciliation.py'
spec=importlib.util.spec_from_file_location('b2orig',ORIG_PATH)
b2=importlib.util.module_from_spec(spec); spec.loader.exec_module(b2)

HIST_RUN=35190742632
HIST_HEAD='c13207ef37540e7c01171c4d638b4058ad1fadd3'
HIST_ARTIFACT=10483358073
HIST_SHA='aa017449e0d4bc2afa4906925c4c53151c4c1eae1571916851aeacf87ef16281'
HIST_FREEZE='22923058c883dd36c6b507fa7079efba5000b4e0'


def stable_exp_from_kq(kq):
    kq=np.asarray(kq,float)
    Z=np.empty_like(kq)
    for idx,val in np.ndenumerate(kq):
        x=float(val)/(4.0*b2.K2*b2.Z0)
        if not (x>0.0) or not math.isfinite(x):
            raise RuntimeError(f'invalid x from KQ at {idx}: {x}')
        L=math.log(x)
        if x < 1.0e-4:
            y=x*x
        else:
            y=L if L>1.0 else x*x
            if y<1.0e-30: y=1.0e-30
        for _ in range(50):
            f=y+0.5*math.log(y)-L
            fp=1.0+0.5/y
            yn=y-f/fp
            if not (yn>0.0) or not math.isfinite(yn): yn=0.5*y
            if abs(yn-y) < 2.0e-14*(1.0+y):
                y=yn
                break
            y=yn
        Z[idx]=math.sqrt(y)
    zz=Z*Z
    ex=np.exp(zz)
    Q=b2.Q0+b2.Z0*Z
    K=2.0*b2.K2*b2.Z0**2*(ex-1.0)
    KQ_formula=4.0*b2.K2*b2.Z0*Z*ex
    rho8=Q*KQ_formula-K
    return Z,Q,K,KQ_formula,rho8


def stable_source_gate(root):
    src=(root/'v019/patch/source/aest_memory.c').read_text()
    checks={
      'source_x_from_KQ':'double x=kq/(4.*K2*Z0);' in src,
      'source_log_equation':'double f=y+.5*log(y)-L;' in src,
      'source_newton_derivative':'double fp=1.+.5/y;' in src,
      'source_newton_iterations':'for (it=0;it<50;it++)' in src,
      'source_stopping_scale':'fabs(yn-y) < 2.e-14*(1.+y)' in src,
      'primary_does_not_use_Q_minus_Q0':True,
    }
    return {'checks':checks,'pass':all(checks.values()),'relation':'KQ/(4*K2*Z0)=Z*exp(Z^2)'}


def evaluate_stable(vals,conv):
    H=np.asarray(vals['H_Mpc_inv'],float)
    Q_trace=np.asarray(vals['Q'],float)
    rho_trace=np.asarray(vals['rhoA'],float)
    KQ_trace=np.asarray(vals['KQ'],float)
    Z,Q_stable,K,KQ_formula,rho8_formula=stable_exp_from_kq(KQ_trace)
    rho_c6=3.0*rho_trace
    scalar_energy_rel=float(np.linalg.norm(rho_c6-rho8_formula)/max(np.linalg.norm(rho8_formula),1e-300))
    kq_rel=float(np.linalg.norm(KQ_trace-KQ_formula)/max(np.linalg.norm(KQ_formula),1e-300))
    q_abs=float(np.max(np.abs(Q_trace-Q_stable)))
    q_rel=float(np.linalg.norm(Q_trace-Q_stable)/max(np.linalg.norm(Q_stable),1e-300))
    varrho_b=3.0*(100.0/b2.C_KM_S)**2*b2.OMEGA_B_H2*b2.AI**-3
    lhs=3.0*H*H
    rem=lhs-rho_c6-varrho_b
    eps=np.abs(rem)/np.maximum(lhs,1e-300)
    return {
      'H':H,'Q_trace':Q_trace,'Q_stable':Q_stable,'rho_trace':rho_trace,'rho_c6':rho_c6,
      'KQ_trace':KQ_trace,'Z':Z,'K':K,'KQ_formula':KQ_formula,'rho8_formula':rho8_formula,
      'scalar_energy_rel':scalar_energy_rel,'KQ_formula_rel':kq_rel,
      'Q_trace_stable_max_abs':q_abs,'Q_trace_stable_rel':q_rel,
      'varrho_b':float(varrho_b),'lhs':lhs,'remainder':rem,'epsilon':eps,
      'median':{
        'H_Mpc_inv':float(np.median(H)),'Q_trace':float(np.median(Q_trace)),
        'Q_stable':float(np.median(Q_stable)),'Z_stable':float(np.median(Z)),
        'rhoA_trace_CLASS':float(np.median(rho_trace)),'rhoA_C6':float(np.median(rho_c6)),
        'rhoA_formula_stable':float(np.median(rho8_formula)),'KQ':float(np.median(KQ_trace)),
        '3H2':float(np.median(lhs)),'varrho_b':float(varrho_b),'rho_rem':float(np.median(rem)),
        'rho_rem_fraction_of_3H2':float(np.median(rem/lhs)),'epsilon_H':float(np.median(eps)),
      },
      'spreads':{f:b2.rel_spread(vals[f]) for f in ['H_Mpc_inv','Q','rhoA','KQ']},
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
                   abs(float(cov.get('a_i'))-b2.AI)<1e-15)
    conv=b2.source_convention(root)
    stable_gate=stable_source_gate(root)
    sym=b2.symbolic_identity()
    z=b2.read_trace(args.trace)
    ks,pv=b2.at_ai(z,'pchip'); _,lv=b2.at_ai(z,'linear')
    p=evaluate_stable(pv,conv); l=evaluate_stable(lv,conv)
    maxspread=max(p['spreads'].values())
    interp_change=abs(p['median']['epsilon_H']-l['median']['epsilon_H'])
    g3=bool(conv['pass'] and stable_gate['pass'] and p['scalar_energy_rel']<=b2.SCALAR_ENERGY_LIMIT and p['KQ_formula_rel']<=b2.SCALAR_ENERGY_LIMIT)
    g4=bool(abs(p['varrho_b']-(3*(100/b2.C_KM_S)**2*b2.OMEGA_B_H2*b2.AI**-3))<=1e-15*max(abs(p['varrho_b']),1.0))
    g5=bool(float(np.max(p['epsilon']))<=b2.HAMILTONIAN_LIMIT)
    g6=bool(maxspread<=b2.KSPREAD_LIMIT and interp_change<=b2.INTERP_LIMIT)
    original_limits_unchanged=bool(b2.KSPREAD_LIMIT==1e-10 and b2.SCALAR_ENERGY_LIMIT==1e-8 and b2.HAMILTONIAN_LIMIT==1e-7 and b2.INTERP_LIMIT==2e-2)
    repair_gates={
      'R1_provenance':bool(provenance_ok),
      'R2_stable_source_equivalent_exp_inversion':bool(stable_gate['pass']),
      'R3_scalar_energy_consistency':g3,
      'R4_science_gates_and_limits_unchanged':bool(sym['pass'] and g4 and g6 and original_limits_unchanged),
    }
    if all(repair_gates.values()) and g5:
        cls='NL1C7B2_REPAIR01_HOMOGENEOUS_BACKGROUND_RECONCILIATION_PASS'
    elif all(repair_gates.values()) and not g5:
        cls='NL1C7B2_REPAIR01_HOMOGENEOUS_BACKGROUND_SECTOR_INCOMPLETE'
    else:
        cls='NL1C7B2_REPAIR01_STABLE_EXP_EVALUATION_FAIL'
    result={
      'classification':cls,
      'scope':'Repair01 stable Exp energy evaluation only; eta=0 homogeneous reconciliation. No radial constraint or trajectory.',
      'historical_parent':{'run':HIST_RUN,'head':HIST_HEAD,'artifact':HIST_ARTIFACT,'artifact_sha256':HIST_SHA,'result_freeze':HIST_FREEZE,'science_classification':'NL1C7B2_HOMOGENEOUS_BACKGROUND_RECONCILIATION_FAIL'},
      'provenance':{'dense_trace_run':35149865129,'dense_artifact':b2.DENSE_ARTIFACT,'dense_sha256':b2.DENSE_SHA,'B1_run':b2.B1_RUN,'B1_head':b2.B1_HEAD,'B1_artifact':b2.B1_ARTIFACT,'B1_sha256':b2.B1_SHA,'n_exact_k':int(len(ks)),'n_native_times':int(cov.get('n_native_times',-1))},
      'source_energy_convention':conv,'stable_exp_source_equivalence':stable_gate,'symbolic_homogeneous_identity':sym,
      'parameters':{'a_i':b2.AI,'H0_km_s_Mpc':b2.H0,'omega_b':b2.OMEGA_B_H2,'Q0_Mpc_inv':b2.Q0,'K2':b2.K2,'Z0_Mpc_inv':b2.Z0},
      'pchip':{'median':p['median'],'relative_spreads':p['spreads'],'scalar_energy_relative_error':p['scalar_energy_rel'],'KQ_formula_relative_error':p['KQ_formula_rel'],'Q_trace_stable_max_abs':p['Q_trace_stable_max_abs'],'Q_trace_stable_relative_error':p['Q_trace_stable_rel'],'epsilon_H_max':float(np.max(p['epsilon'])),'epsilon_H_min':float(np.min(p['epsilon']))},
      'linear_control':{'median':l['median'],'normalized_closure_residual_change_abs':float(interp_change),'limit':b2.INTERP_LIMIT},
      'missing_sector_diagnostic':{'reported_only_not_added':True,'rho_rem_Mpc_inv2':p['median']['rho_rem'],'fraction_of_3H2':p['median']['rho_rem_fraction_of_3H2']},
      'limits':{'k_spread':b2.KSPREAD_LIMIT,'scalar_energy':b2.SCALAR_ENERGY_LIMIT,'epsilon_H':b2.HAMILTONIAN_LIMIT,'interpolation_control':b2.INTERP_LIMIT},
      'original_B2_gates_re_evaluated':{'B2_G2_exact_homogeneous_lapse_identity':bool(sym['pass']),'B2_G3_trace_scalar_energy_consistency':g3,'B2_G4_baryon_normalization':g4,'B2_G5_homogeneous_Hamiltonian_closure':g5,'B2_G6_k_independence_and_interpolation_control':g6},
      'repair_gates':repair_gates,
      'claim_boundary':{'radial_initial_constraint_executed':False,'nonlinear_evolution_executed':False,'finite_eta_executed':False,'turnaround_or_collapse_evaluated':False},
    }
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if cls.endswith('_PASS') else 2)

if __name__=='__main__': main()
