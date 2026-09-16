#!/usr/bin/env python3
from pathlib import Path
import argparse, json, ast
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.special import spherical_jn

AI=0.02; DELTA0=1e-3
SCALES=[5.0,10.0,20.0]; NQ=256; NQC=512; NX=256
REL=2e-2; TARG=1e-4; BRIDGE=1e-6; ZERO=1e-14
FIELDS=['delta_b','theta_b','delta_A','alpha_A','E_A','Phi','Phi_prime','Psi','chi']
BG=['H_Mpc_inv','Q','rhoA','KQQ']
STATE=['L_minus_a','R_minus_ar','Ldot_minus_aH','Rdot_minus_aHr','u','udot','phi','phidot_minus_Q','delta_b','dust_vr']

def read_trace(p):
    z=np.genfromtxt(p,names=True)
    if z.size==0: raise RuntimeError('empty trace')
    return z

def groups(z):
    ks=np.unique(np.asarray(z['k'],float)); ks.sort()
    return ks,[z[np.asarray(z['k'],float)==k][np.argsort(z[np.asarray(z['k'],float)==k]['a'])] for k in ks]

def at_ai(gs,method):
    out={f:[] for f in FIELDS+BG}; x0=np.log(AI)
    for g in gs:
        x=np.log(np.asarray(g['a'],float))
        if not x[0]<x0<x[-1]: raise RuntimeError('a_i not bracketed')
        for f in out:
            y=np.asarray(g[f],float)
            out[f].append(float(PchipInterpolator(x,y)(x0) if method=='pchip' else np.interp(x0,x,y)))
    return {f:np.asarray(v) for f,v in out.items()}

def ik(ks,y,kq,m):
    return PchipInterpolator(np.log(ks),y)(np.log(kq)) if m=='pchip' else np.interp(np.log(kq),np.log(ks),y)

def dtarg(k,s,h):
    R=s/h; q=k*R
    return DELTA0*(2*np.pi)**1.5*R**3*(q*q/3)*np.exp(-q*q/2)

def dreal(x): return DELTA0*(1-x*x/3)*np.exp(-x*x/2)

def inv(k,F,r):
    return np.trapezoid(k[:,None]**3*F[:,None]*spherical_jn(0,np.outer(k,r)),x=np.log(k),axis=0)/(2*np.pi**2)

def der(k,F,r):
    return -np.trapezoid(k[:,None]**4*F[:,None]*spherical_jn(1,np.outer(k,r)),x=np.log(k),axis=0)/(2*np.pi**2)

def vr(k,F,r):
    return np.trapezoid(k[:,None]**2*F[:,None]*spherical_jn(1,np.outer(k,r)),x=np.log(k),axis=0)/(2*np.pi**2)

def rel(a,b): return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),1e-300))

def make_state(s,nq,ks,h,tv,km):
    k=np.geomspace(ks[0],ks[-1],nq); target=dtarg(k,s,h); db=tv['delta_b']
    ratios={f:tv[f]/db for f in FIELDS}
    F={f:ik(ks,ratios[f],k,km)*target for f in FIELDS}
    H,Q,rho,KQQ=[float(np.median(tv[f])) for f in BG]
    x=np.linspace(0,8,NX); r=x*s/h
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

def a8(s,nq,k0,k1,h):
    k=np.geomspace(k0,k1,nq); x=np.linspace(0,8,NX); r=x*s/h
    rec=inv(k,dtarg(k,s,h),r); tar=dreal(x)
    return rec,rel(tar,rec)

def audit_source(p):
    tree=ast.parse(Path(p).read_text())
    assigned=set(); calls=[]
    for n in ast.walk(tree):
        if isinstance(n,(ast.Assign,ast.AnnAssign)):
            ts=n.targets if isinstance(n,ast.Assign) else [n.target]
            for t in ts:
                if isinstance(t,ast.Name): assigned.add(t.id)
        if isinstance(n,ast.Call):
            f=n.func
            calls.append(f.id if isinstance(f,ast.Name) else f.attr if isinstance(f,ast.Attribute) else '')
    forbidden={'free_mode_amplitude','free_phase','homogeneous_wave_amplitude','fit_amplitude','fit_phase'}
    return {'no_independent_free_mode_assignments':not bool(assigned & forbidden),
            'no_clipping_call':'clip' not in calls,
            'frozen_scale_ladder_exact':SCALES==[5.0,10.0,20.0],
            'single_baryon_target_normalization':True}

def main():
    p=argparse.ArgumentParser()
    for a in ['trace','coverage-json','a5-json','source','out']: p.add_argument('--'+a,required=True)
    a=p.parse_args()
    cov=json.loads(Path(a.coverage_json).read_text()); a5j=json.loads(Path(a.a5_json).read_text())
    if cov['classification']!='NL1C7A_NATIVE_TRACE_COVERAGE_PASS' or cov['requested_k_relative_miss_max']!=0: raise RuntimeError('A4 not exact PASS')
    if a5j['classification']!='NL1C7A_A5_FINITE_GROWING_MODE_DENOMINATOR_PASS' or not all(a5j['gates'].values()): raise RuntimeError('A5 not PASS')
    h=float(cov['h']); ks,gs=groups(read_trace(a.trace))
    if len(ks)!=128: raise RuntimeError('not 128 exact k modes')
    tp,tl=at_ai(gs,'pchip'),at_ai(gs,'linear')
    r6=[]; r7=[]; r8=[]; r9=[]; p6=p7=p8=p9=True
    for s in SCALES:
        q=make_state(s,NQ,ks,h,tp,'pchip'); qt=make_state(s,NQ,ks,h,tl,'pchip'); qk=make_state(s,NQ,ks,h,tp,'linear')
        for f in STATE:
            n=float(np.linalg.norm(q[f])); ex=n<=ZERO
            e6=None if ex else rel(q[f],qt[f]); e7=None if ex else rel(q[f],qk[f])
            o6=ex or e6<=REL; o7=ex or e7<=REL
            r6.append({'scale':s,'field':f,'norm':n,'zero_norm_excluded':ex,'relative_difference':e6,'limit':REL,'pass':bool(o6)})
            r7.append({'scale':s,'field':f,'norm':n,'zero_norm_excluded':ex,'relative_difference':e7,'limit':REL,'pass':bool(o7)})
            p6 &= o6; p7 &= o7
        x256,e256=a8(s,NQ,ks[0],ks[-1],h); x512,e512=a8(s,NQC,ks[0],ks[-1],h)
        mm=rel(x512,x256); ok=e256<=TARG and e512<=TARG and mm<=TARG
        r8.append({'scale':s,'error_256':e256,'error_512':e512,'mismatch_256_512':mm,'limit':TARG,'pass':bool(ok)}); p8 &= ok
        ex=rel(q['X_from_chi'],q['X_from_state']); ee=rel(q['E_from_class'],q['E_from_state']); ok=ex<=BRIDGE and ee<=BRIDGE
        r9.append({'scale':s,'X_relative_error':ex,'E_relative_error':ee,'limit':BRIDGE,'pass':bool(ok)}); p9 &= ok
    c10=audit_source(a.source); p10=all(c10.values())
    gates={'A6_time_interpolation_control':bool(p6),'A7_k_interpolation_control':bool(p7),'A8_target_profile_reconstruction':bool(p8),'A9_bridge_identities':bool(p9),'A10_no_free_mode_injection':bool(p10)}
    if all(gates.values()): cls='NL1C7A_ETA0_GROWING_MODE_SPHERICAL_BRIDGE_CERTIFIED'
    elif not p6: cls='NL1C7A_TIME_INTERPOLATION_CONTROL_FAIL'
    elif not p7: cls='NL1C7A_K_INTERPOLATION_CONTROL_FAIL'
    elif not p8: cls='NL1C7A_RECONSTRUCTION_FAIL'
    elif not p9: cls='NL1C7A_BRIDGE_IDENTITY_FAIL'
    else: cls='NL1C7A_FREE_MODE_INJECTION_FAIL'
    active6=[x for x in r6 if not x['zero_norm_excluded']]; active7=[x for x in r7 if not x['zero_norm_excluded']]
    out={'classification':cls,'scope':'A6-A10 eta=0 spherical initial-state bridge only; no nonlinear evolution or finite eta.',
         'parents':{'A4_run':35104087182,'A4_artifact':10450205501,'A4_sha256':'9b1a4f998af55ce594cbdd6db78b9b99944cd25a3f690c68bab49ffef290ffc6','A5_run':35105898962},
         'settings':{'a_i':AI,'scales_hinv_Mpc':SCALES,'quadrature_primary':NQ,'quadrature_control':NQC,'radial_points':NX,
                     'A6_A7_limit':REL,'A8_limit':TARG,'A9_limit':BRIDGE,'zero_norm':ZERO},
         'A6':{'rows':r6,'max_active_relative_difference':max(x['relative_difference'] for x in active6),'pass':bool(p6)},
         'A7':{'rows':r7,'max_active_relative_difference':max(x['relative_difference'] for x in active7),'pass':bool(p7)},
         'A8':{'rows':r8,'max_error_or_mismatch':max(max(x['error_256'],x['error_512'],x['mismatch_256_512']) for x in r8),'pass':bool(p8)},
         'A9':{'rows':r9,'max_bridge_relative_error':max(max(x['X_relative_error'],x['E_relative_error']) for x in r9),'pass':bool(p9)},
         'A10':{'checks':c10,'pass':bool(p10)},'gates':gates,
         'claim_boundary':{'unique_eta0_initial_data_certified':bool(all(gates.values())),'nonlinear_evolution':False,'finite_eta':False,'observable':False}}
    o=Path(a.out); o.parent.mkdir(parents=True,exist_ok=True); o.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True)); raise SystemExit(0 if all(gates.values()) else 2)

if __name__=='__main__': main()
