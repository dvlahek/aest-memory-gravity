#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.special import spherical_jn

AI=0.02
DELTA0=1.0e-3
SCALES=[5.0,10.0,20.0]
NQ_PRIMARY=256
NQ_CONTROL=512
NX=256
REL_LIMIT=2.0e-2
TARGET_LIMIT=1.0e-4
BRIDGE_LIMIT=1.0e-6
ZERO_NORM=1.0e-14
FIELDS=['delta_b','theta_b','delta_A','alpha_A','E_A','Phi','Phi_prime','Psi','chi']
BGFIELDS=['H_Mpc_inv','Q','rhoA','KQQ']
STATE_FIELDS=['L_minus_a','R_minus_ar','Ldot_minus_aH','Rdot_minus_aHr','u','udot','phi','phidot_minus_Q','delta_b','dust_vr']


def read_trace(path):
    z=np.genfromtxt(path,names=True)
    if z.size==0: raise RuntimeError('empty trace')
    return z


def group_trace(z):
    ks=np.unique(np.asarray(z['k'],float)); ks.sort(); groups=[]
    for k in ks:
        g=z[np.asarray(z['k'],float)==k]
        groups.append(g[np.argsort(g['a'])])
    return ks,groups


def time_values(groups,method):
    out={f:[] for f in FIELDS+BGFIELDS}; x0=np.log(AI)
    for g in groups:
        x=np.log(np.asarray(g['a'],float))
        if not (x[0] < x0 < x[-1]): raise RuntimeError('a_i not bracketed')
        for f in out:
            y=np.asarray(g[f],float)
            v=PchipInterpolator(x,y)(x0) if method=='pchip' else np.interp(x0,x,y)
            out[f].append(float(v))
    return {f:np.asarray(v,float) for f,v in out.items()}


def interp_k(ks,y,kq,method):
    x=np.log(ks); xq=np.log(kq)
    return PchipInterpolator(x,y)(xq) if method=='pchip' else np.interp(xq,x,y)


def target_tilde(k,scale,h):
    R=scale/h; q=k*R
    return DELTA0*(2*np.pi)**1.5*R**3*(q*q/3.0)*np.exp(-0.5*q*q)


def target_real(x):
    return DELTA0*(1.0-x*x/3.0)*np.exp(-0.5*x*x)


def scalar_inverse(k,F,r):
    j0=spherical_jn(0,np.outer(k,r))
    return np.trapezoid(k[:,None]**3*F[:,None]*j0,x=np.log(k),axis=0)/(2*np.pi**2)


def radial_derivative(k,F,r):
    j1=spherical_jn(1,np.outer(k,r))
    return -np.trapezoid(k[:,None]**4*F[:,None]*j1,x=np.log(k),axis=0)/(2*np.pi**2)


def radial_velocity(k,theta,r):
    j1=spherical_jn(1,np.outer(k,r))
    return np.trapezoid(k[:,None]**2*theta[:,None]*j1,x=np.log(k),axis=0)/(2*np.pi**2)


def l2rel(primary,control):
    return float(np.linalg.norm(primary-control)/max(np.linalg.norm(primary),1e-300))


def state(scale,nq,ks,h,tv,kmethod):
    kq=np.geomspace(float(ks[0]),float(ks[-1]),nq)
    dt=target_tilde(kq,scale,h)
    db=tv['delta_b']
    ratios={f:tv[f]/db for f in FIELDS}
    F={f:interp_k(ks,ratios[f],kq,kmethod)*dt for f in FIELDS}
    H=float(np.median(tv['H_Mpc_inv'])); Q=float(np.median(tv['Q']))
    rhoA=float(np.median(tv['rhoA'])); KQQ=float(np.median(tv['KQQ']))
    x=np.linspace(0.0,8.0,NX); r=x*scale/h
    scalar={f:scalar_inverse(kq,F[f],r) for f in FIELDS}
    alpha_r=radial_derivative(kq,F['alpha_A'],r)
    E_r=radial_derivative(kq,F['E_A'],r)
    chi_r=radial_derivative(kq,F['chi'],r)
    phiF=F['chi']-Q*F['alpha_A']
    phi=scalar_inverse(kq,phiF,r)
    u=alpha_r/AI
    udot=E_r/AI-H*u
    dqF=(rhoA/(Q*KQQ))*F['delta_A']
    dq=scalar_inverse(kq,dqF,r)
    Lm=-AI*scalar['Phi']
    Rm=-AI*r*scalar['Phi']
    Ldm=-AI*H*(scalar['Phi']+scalar['Psi'])-scalar['Phi_prime']
    Rdm=r*Ldm
    vr=radial_velocity(kq,F['theta_b'],r)
    phi_r_fd=np.gradient(phi,r,edge_order=2)
    X_from_state=Q*u+phi_r_fd/AI
    X_from_chi=chi_r/AI
    E_from_state=udot+H*u
    E_from_class=E_r/AI
    return {
      'x':x,'r':r,'k':kq,
      'L_minus_a':Lm,'R_minus_ar':Rm,'Ldot_minus_aH':Ldm,'Rdot_minus_aHr':Rdm,
      'u':u,'udot':udot,'phi':phi,'phidot_minus_Q':dq,'delta_b':scalar['delta_b'],'dust_vr':vr,
      'X_from_state':X_from_state,'X_from_chi':X_from_chi,
      'E_from_state':E_from_state,'E_from_class':E_from_class,
      'background':{'H_Mpc_inv':H,'Q_Mpc_inv':Q,'rhoA':rhoA,'KQQ':KQQ},
    }


def target_a8(scale,nq,kmin,kmax,h):
    k=np.geomspace(kmin,kmax,nq); x=np.linspace(0.0,8.0,NX); r=x*scale/h
    rec=scalar_inverse(k,target_tilde(k,scale,h),r)
    tar=target_real(x)
    return rec,tar,l2rel(tar,rec)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--a5-json',required=True)
    ap.add_argument('--source',required=True)
    ap.add_argument('--out',required=True)
    args=ap.parse_args()

    coverage=json.loads(Path(args.coverage_json).read_text())
    a5=json.loads(Path(args.a5_json).read_text())
    if coverage['classification']!='NL1C7A_NATIVE_TRACE_COVERAGE_PASS': raise RuntimeError('A4 not PASS')
    if a5['classification']!='NL1C7A_A5_FINITE_GROWING_MODE_DENOMINATOR_PASS': raise RuntimeError('A5 not PASS')
    if not all(a5['gates'].values()): raise RuntimeError('A5 gates not all true')
    h=float(coverage['h'])
    z=read_trace(args.trace); ks,groups=group_trace(z)
    if len(ks)!=128: raise RuntimeError(f'expected 128 exact modes, got {len(ks)}')
    tp=time_values(groups,'pchip'); tl=time_values(groups,'linear')

    time_rows=[]; a6_pass=True
    k_rows=[]; a7_pass=True
    a8_rows=[]; a8_pass=True
    a9_rows=[]; a9_pass=True

    for scale in SCALES:
        primary=state(scale,NQ_PRIMARY,ks,h,tp,'pchip')
        tcontrol=state(scale,NQ_PRIMARY,ks,h,tl,'pchip')
        kcontrol=state(scale,NQ_PRIMARY,ks,h,tp,'linear')
        for name in STATE_FIELDS:
            norm=float(np.linalg.norm(primary[name]))
            excluded=bool(norm<=ZERO_NORM)
            rr=None if excluded else l2rel(primary[name],tcontrol[name])
            ok=True if excluded else bool(rr<=REL_LIMIT)
            time_rows.append({'R_sigma_hinv_Mpc':scale,'field':name,'primary_norm':norm,'zero_norm_excluded':excluded,'relative_difference':rr,'limit':REL_LIMIT,'pass':ok})
            a6_pass &= ok
            rk=None if excluded else l2rel(primary[name],kcontrol[name])
            okk=True if excluded else bool(rk<=REL_LIMIT)
            k_rows.append({'R_sigma_hinv_Mpc':scale,'field':name,'primary_norm':norm,'zero_norm_excluded':excluded,'relative_difference':rk,'limit':REL_LIMIT,'pass':okk})
            a7_pass &= okk

        rec256,tar,e256=target_a8(scale,NQ_PRIMARY,float(ks[0]),float(ks[-1]),h)
        rec512,_,e512=target_a8(scale,NQ_CONTROL,float(ks[0]),float(ks[-1]),h)
        mismatch=l2rel(rec512,rec256)
        oka=bool(e256<=TARGET_LIMIT and e512<=TARGET_LIMIT and mismatch<=TARGET_LIMIT)
        a8_rows.append({'R_sigma_hinv_Mpc':scale,'error_256':e256,'error_512':e512,'mismatch_256_512':mismatch,'limit':TARGET_LIMIT,'pass':oka})
        a8_pass &= oka

        xr=l2rel(primary['X_from_chi'],primary['X_from_state'])
        er=l2rel(primary['E_from_class'],primary['E_from_state'])
        ok9=bool(xr<=BRIDGE_LIMIT and er<=BRIDGE_LIMIT)
        a9_rows.append({'R_sigma_hinv_Mpc':scale,'X_relative_error':xr,'E_relative_error':er,'limit':BRIDGE_LIMIT,'pass':ok9})
        a9_pass &= ok9

    src=Path(args.source).read_text()
    forbidden=['free_mode_amplitude','free_phase','homogeneous_wave_amplitude','fit_amplitude','fit_phase']
    a10_checks={
      'single_target_normalization_only': 'ratios={f:tv[f]/db for f in FIELDS}' in src and 'target_tilde(kq,scale,h)' in src,
      'no_independent_free_mode_tokens': not any(t in src for t in forbidden),
      'no_postdata_scale_selection': src.count('SCALES=[5.0,10.0,20.0]')==1,
      'no_clipping_call': '.clip(' not in src and 'np.clip(' not in src,
    }
    a10_pass=bool(all(a10_checks.values()))

    gates={'A6_time_interpolation_control':bool(a6_pass),'A7_k_interpolation_control':bool(a7_pass),'A8_target_profile_reconstruction':bool(a8_pass),'A9_bridge_identities':bool(a9_pass),'A10_no_free_mode_injection':bool(a10_pass)}
    if all(gates.values()): classification='NL1C7A_ETA0_GROWING_MODE_SPHERICAL_BRIDGE_CERTIFIED'
    elif not a6_pass: classification='NL1C7A_TIME_INTERPOLATION_CONTROL_FAIL'
    elif not a7_pass: classification='NL1C7A_K_INTERPOLATION_CONTROL_FAIL'
    elif not a8_pass: classification='NL1C7A_RECONSTRUCTION_FAIL'
    elif not a9_pass: classification='NL1C7A_BRIDGE_IDENTITY_FAIL'
    else: classification='NL1C7A_FREE_MODE_INJECTION_FAIL'

    active_time=[r for r in time_rows if not r['zero_norm_excluded']]
    active_k=[r for r in k_rows if not r['zero_norm_excluded']]
    result={
      'classification':classification,
      'scope':'NL1C7A A6-A10 eta=0 spherical initial-state reconstruction only; no nonlinear evolution, finite eta, turnaround, collapse, splashback, or observational claim.',
      'parent_A4_run':35104087182,
      'parent_A4_artifact':10450205501,
      'parent_A4_sha256':'9b1a4f998af55ce594cbdd6db78b9b99944cd25a3f690c68bab49ffef290ffc6',
      'parent_A5_run':35105898962,
      'a_i':AI,'scales_hinv_Mpc':SCALES,'quadrature_primary':NQ_PRIMARY,'quadrature_control':NQ_CONTROL,'radial_points':NX,
      'frozen_limits':{'A6_A7_relative':REL_LIMIT,'A8_target':TARGET_LIMIT,'A9_bridge':BRIDGE_LIMIT,'zero_norm':ZERO_NORM},
      'A6':{'rows':time_rows,'max_active_relative_difference':max(r['relative_difference'] for r in active_time),'pass':bool(a6_pass)},
      'A7':{'rows':k_rows,'max_active_relative_difference':max(r['relative_difference'] for r in active_k),'pass':bool(a7_pass)},
      'A8':{'rows':a8_rows,'max_error_or_mismatch':max(max(r['error_256'],r['error_512'],r['mismatch_256_512']) for r in a8_rows),'pass':bool(a8_pass)},
      'A9':{'rows':a9_rows,'max_bridge_relative_error':max(max(r['X_relative_error'],r['E_relative_error']) for r in a9_rows),'pass':bool(a9_pass)},
      'A10':{'checks':a10_checks,'pass':bool(a10_pass)},
      'gates':gates,
      'claim_boundary':{'unique_eta0_initial_data_certified':bool(all(gates.values())),'nonlinear_evolution':False,'finite_eta':False,'observable':False},
    }
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if all(gates.values()) else 2)

if __name__=='__main__': main()
