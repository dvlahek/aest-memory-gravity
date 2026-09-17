#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.special import spherical_jn

AI=0.02; DELTA0=1e-3; SCALES=(5.0,10.0,20.0); NQ=256
KB=0.0665; C=2.0-KB; Q0=1e-4; K2=9500.0; Z0=1e-17; A0_GEO=4.1199352008117163e-5
G3_LIMIT=1e-7
H_DIRECT=math.sqrt(0.006048695270400684/3.0)
VAR_B=0.0009336821113982245
RHO_STD=0.00010529015057211754
FIELDS=['delta_b','theta_b','delta_A','alpha_A','E_A','Phi','Phi_prime','Psi','chi']
BG=['H_Mpc_inv','Q','rhoA','KQQ','KQ']

# Frozen C7A reconstruction ff383c1d..., generalized only in radial point count.
def read_trace(p):
    z=np.genfromtxt(p,names=True)
    if z.size==0: raise RuntimeError('empty trace')
    return z

def groups(z):
    ks=np.unique(np.asarray(z['k'],float)); ks.sort()
    return ks,[z[np.asarray(z['k'],float)==k][np.argsort(z[np.asarray(z['k'],float)==k]['a'])] for k in ks]

def at_ai(gs):
    out={f:[] for f in FIELDS+BG}; x0=np.log(AI)
    for g in gs:
        x=np.log(np.asarray(g['a'],float))
        if not x[0]<x0<x[-1]: raise RuntimeError('a_i not bracketed')
        for f in out:
            out[f].append(float(PchipInterpolator(x,np.asarray(g[f],float))(x0)))
    return {f:np.asarray(v) for f,v in out.items()}

def ik(ks,y,kq): return PchipInterpolator(np.log(ks),y)(np.log(kq))
def dtarg(k,s,h):
    R=s/h; q=k*R
    return DELTA0*(2*np.pi)**1.5*R**3*(q*q/3.0)*np.exp(-q*q/2.0)
def inv(k,F,r): return np.trapezoid(k[:,None]**3*F[:,None]*spherical_jn(0,np.outer(k,r)),x=np.log(k),axis=0)/(2*np.pi**2)
def der(k,F,r): return -np.trapezoid(k[:,None]**4*F[:,None]*spherical_jn(1,np.outer(k,r)),x=np.log(k),axis=0)/(2*np.pi**2)
def vr(k,F,r): return np.trapezoid(k[:,None]**2*F[:,None]*spherical_jn(1,np.outer(k,r)),x=np.log(k),axis=0)/(2*np.pi**2)

def make_state(s,nr,ks,h,tv):
    k=np.geomspace(ks[0],ks[-1],NQ); target=dtarg(k,s,h); db=tv['delta_b']
    ratios={f:tv[f]/db for f in FIELDS}; F={f:ik(ks,ratios[f],k)*target for f in FIELDS}
    H,Q,rho,KQQ=[float(np.median(tv[f])) for f in ['H_Mpc_inv','Q','rhoA','KQQ']]
    x=np.linspace(0,8,nr); r=x*s/h
    S={f:inv(k,F[f],r) for f in FIELDS}
    ar=der(k,F['alpha_A'],r); er=der(k,F['E_A'],r); cr=der(k,F['chi'],r)
    phi=inv(k,F['chi']-Q*F['alpha_A'],r)
    u=ar/AI; udot=er/AI-H*u
    dq=inv(k,(rho/(Q*KQQ))*F['delta_A'],r)
    L=-AI*S['Phi']; R=-AI*r*S['Phi']
    Lt=-AI*H*(S['Phi']+S['Psi'])-S['Phi_prime']; Rt=r*Lt
    out={'x':x,'r':r,'L_minus_a':L,'R_minus_ar':R,'Ldot_minus_aH':Lt,'Rdot_minus_aHr':Rt,
         'u':u,'udot':udot,'phi':phi,'phidot_minus_Q':dq,'delta_b':S['delta_b'],'dust_vr':vr(k,F['theta_b'],r)}
    out['X_from_chi']=cr/AI
    out['X_from_state']=Q*u+np.gradient(phi,r,edge_order=2)/AI
    out['E_from_class']=er/AI; out['E_from_state']=udot+H*u
    return out

def stable_q_from_kq(kq):
    x=float(kq)/(4*K2*Z0)
    if not (x>0.0 and math.isfinite(x)): raise RuntimeError('invalid KQ for stable Exp inversion')
    L=math.log(x); y=L if L>1.0 else x*x
    for _ in range(50):
        f=y+0.5*math.log(y)-L; fp=1.0+0.5/y; yn=y-f/fp
        if not (yn>0.0 and math.isfinite(yn)): yn=0.5*y
        if abs(yn-y)<2e-14*(1+y): y=yn; break
        y=yn
    return Q0+Z0*math.sqrt(y)

def dmat(r):
    r=np.asarray(r,float); n=len(r); D=np.zeros((n,n))
    for i in range(n):
        start=min(max(i-4,0),n-9); ids=np.arange(start,start+9); d=r[ids]-r[i]
        A=np.vstack([d**m for m in range(9)]); b=np.zeros(9); b[1]=1.0
        D[i,ids]=np.linalg.solve(A,b)
    return D

def rel(a,b): return float(np.linalg.norm(a-b)/max(np.linalg.norm(b),1e-300))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True); ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--official-npz',required=True); ap.add_argument('--out',required=True)
    a=ap.parse_args(); cov=json.loads(Path(a.coverage_json).read_text()); off=np.load(a.official_npz)
    provenance_ok=(cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS' and
                   cov.get('requested_k_relative_miss_max')==0 and cov.get('n_native_times')==179 and
                   abs(float(cov.get('a_i'))-AI)<1e-15)
    ks,gs=groups(read_trace(a.trace)); tv=at_ai(gs); h=float(cov['h'])
    if len(ks)!=128: raise RuntimeError('not 128 exact k modes')
    qbg=stable_q_from_kq(float(np.median(tv['KQ'])))

    reproduction={}; states={}; maxrep=0.0
    for s in SCALES:
        tag=str(int(s)); st=make_state(s,256,ks,h,tv); states[(s,256)]=st; rows={}
        for k,v in st.items():
            key=f's{tag}_{k}'
            if key not in off.files: continue
            e=rel(np.asarray(v),np.asarray(off[key])); rows[k]=e; maxrep=max(maxrep,e)
        reproduction[tag]=rows; states[(s,512)]=make_state(s,512,ks,h,tv)
    rep_ok=bool(maxrep<=1e-12)

    # Exact nonlinear C6 scalar is Q=cosh(u)*sigma+sinh(u)*phi_r/L.  B4 must not
    # replace this by the linearized phidot perturbation.  This guard checks if
    # the frozen Exp action can even be evaluated without clipping/linearizing K.
    domain=[]; representable=True; logmax=math.log(np.finfo(float).max)
    for s in SCALES:
      for nr in (256,512):
        st=states[(s,nr)]; D=dmat(st['r']); L=AI+st['L_minus_a']; u=st['u']; pr=D@st['phi']
        sigma=qbg+st['phidot_minus_Q']; qfull=np.cosh(u)*sigma+np.sinh(u)*pr/L
        z=(qfull-Q0)/Z0; z2=z*z
        ok=bool(np.all(np.isfinite(z2)) and np.max(z2)<=logmax)
        domain.append({'scale_hinv_Mpc':s,'Nr':nr,'u_abs_max':float(np.max(np.abs(u))),
          'Q_background_Mpc_inv':qbg,'Q_full_min_Mpc_inv':float(np.min(qfull)),'Q_full_max_Mpc_inv':float(np.max(qfull)),
          'deltaQ_full_abs_max_Mpc_inv':float(np.max(np.abs(qfull-qbg))),
          'Z_abs_max':float(np.max(np.abs(z))),'Z2_max':float(np.max(z2)),
          'float64_log_max':float(logmax),'Exp_K_float64_representable':ok})
        representable &= ok

    no_state_modification=True
    if not provenance_ok or not rep_ok:
        cls='NL1C7B4_CONSTRAINT_IMPLEMENTATION_INCOMPLETE'; reason='provenance_or_official_state_reproduction_failed'
    elif not representable:
        cls='NL1C7B4_CONSTRAINT_IMPLEMENTATION_INCOMPLETE'; reason='full_Exp_Q_sector_not_representable_in_unmodified_float64_action_evaluator'
    else:
        cls='NL1C7B4_CONSTRAINT_IMPLEMENTATION_INCOMPLETE'; reason='guard_passed_but_full_constraint_evaluator_requires_separate_locked_completion'

    result={'classification':cls,'reason':reason,
      'scope':'B4 raw eta=0 initial-constraint certification domain guard; no state projection and no evolution.',
      'provenance':{'C7A_run':35183893359,'C7A_artifact':10481526695,
                    'C7A_artifact_sha256':'c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c',
                    'B3_repair01_run':35196289353,'B3_repair01_artifact':10486515383,
                    'B3_repair01_artifact_sha256':'12f3157fa05e7c0c4fc431005a506cbfa6347aa78dafd1a1dedf4328b193d3ec'},
      'background':{'a_i':AI,'H_direct_Mpc_inv':H_DIRECT,'Q_stable_Mpc_inv':qbg,
                    'varrho_b':VAR_B,'rho_std_C6':RHO_STD},
      'state_reproduction':{'max_relative_L2':maxrep,'limit':1e-12,'pass':rep_ok,'rows':reproduction},
      'nonlinear_Q_domain':domain,
      'gates':{'B4_G1_provenance_and_state_reproduction':bool(provenance_ok and rep_ok),
               'B4_G2_exact_action_source_structure':False,
               'B4_G3_initial_constraints':False,'B4_G4_grid_control':False,
               'B4_G5_no_state_modification':no_state_modification},
      'claim_boundary':{'constraint_projection_used':False,'linearized_Q_used':False,'K_clipping_used':False,
                        'nonlinear_evolution_executed':False,'finite_eta_executed':False}}
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True)); raise SystemExit(2)
if __name__=='__main__': main()
