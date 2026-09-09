#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

OUT = Path('results/nl1c3b_longitudinal_3plus1_memory_bridge.json')
OUT.parent.mkdir(parents=True, exist_ok=True)

# Exact scalar-longitudinal 3+1 reduction of the frozen NL0B memory action.
# Coframe:
#   theta0=N dt
#   theta1=L (dx+b dt)
#   theta2=R dy
#   theta3=R dz
# A and s span only the (0,1) plane.  For U=q s and X_mu=X s_mu,
# the projected derivative obeys D_A(q s)_mu=A(q)s_mu, so each bath node is
#   Lhat=N L R^2 /4 * [(Aq)^2-(omega q-sqrt(w) X)^2].

N, L, R, b, r = sp.symbols('N L R b r', positive=True, real=True)
pt, px, qt, qx, q = sp.symbols('pt px qt qx q', real=True)
om, sw = sp.symbols('om sw', positive=True, real=True)
ch, sh = sp.cosh(r), sp.sinh(r)
Aq = ch/N * (qt-b*qx) + sh/L * qx
Xphi = sh/N * (pt-b*px) + ch/L * px
lag = N*L*R**2*sp.Rational(1,4) * (Aq**2-(om*q-sw*Xphi)**2)

partial_symbols = [pt, px, qt, qx, q, r, N, b, L, R]
partials = {str(v): sp.diff(lag, v) for v in partial_symbols}
args = (N,L,R,b,r,pt,px,qt,qx,q,om,sw)
f_lag = sp.lambdify(args, lag, 'numpy')
f_partial = {k: sp.lambdify(args,v,'numpy') for k,v in partials.items()}


def centered(a, axis, spacing):
    return (np.roll(a,-1,axis=axis)-np.roll(a,1,axis=axis))/(2.0*spacing)


def deterministic_fields(nt=8,nx=12):
    tt=np.arange(nt)*(2*np.pi/nt)
    xx=np.arange(nx)*(2*np.pi/nx)
    T,X=np.meshgrid(tt,xx,indexing='ij')
    fields=[
        1.0+0.05*np.sin(T+0.3*X),                    # N
        1.0+0.04*np.cos(0.7*T-X),                    # L
        1.0+0.03*np.sin(0.8*T+0.6*X),                # R
        0.03*np.sin(T-1.2*X),                        # b
        0.20*np.sin(0.6*T+X),                        # r
        0.40*np.sin(T+X)+0.30*np.cos(2*T-X),         # phi
        0.15*np.cos(T-2*X)+0.08*np.sin(2*T+X),       # q
    ]
    return fields,2*np.pi/nt,2*np.pi/nx


def eval_action_and_sources(fields,dt,dx,omega=1.7,weight=0.6):
    Nf,Lf,Rf,bf,rf,phif,qf=fields
    vals=(Nf,Lf,Rf,bf,rf,
          centered(phif,0,dt),centered(phif,1,dx),
          centered(qf,0,dt),centered(qf,1,dx),qf,
          omega,math.sqrt(weight))
    lval=np.asarray(f_lag(*vals),float)
    pd={k:np.asarray(fn(*vals),float) for k,fn in f_partial.items()}
    src={
        'scalar_phi':-centered(pd['pt'],0,dt)-centered(pd['px'],1,dx),
        'bath_q':pd['q']-centered(pd['qt'],0,dt)-centered(pd['qx'],1,dx),
        'aether_rapidity':pd['r'],
        'metric_lapse':pd['N'],
        'metric_shift':pd['b'],
        'metric_longitudinal_scale':pd['L'],
        'metric_transverse_scale':pd['R'],
    }
    return float(np.sum(lval)*dt*dx),src


def variation_audit():
    fields,dt,dx=deterministic_fields()
    _,src=eval_action_and_sources(fields,dt,dx)
    order=[
        ('metric_lapse',0),('metric_longitudinal_scale',1),('metric_transverse_scale',2),
        ('metric_shift',3),('aether_rapidity',4),('scalar_phi',5),('bath_q',6),
    ]
    sites=[(1,2),(3,5),(6,9)]
    rows=[]; max_rel=0.0
    for name,fi in order:
        for ij in sites:
            step=1e-6*max(1.0,abs(float(fields[fi][ij])))
            fp=[a.copy() for a in fields]; fm=[a.copy() for a in fields]
            fp[fi][ij]+=step; fm[fi][ij]-=step
            Sp,_=eval_action_and_sources(fp,dt,dx)
            Sm,_=eval_action_and_sources(fm,dt,dx)
            fd=(Sp-Sm)/(2*step)
            automatic=float(src[name][ij]*dt*dx)
            rel=abs(fd-automatic)/max(1e-12,abs(fd),abs(automatic))
            max_rel=max(max_rel,rel)
            rows.append({'source':name,'site':list(ij),'automatic':automatic,
                         'finite_difference':fd,'relative_error':rel})
    finite=all(np.all(np.isfinite(v)) for v in src.values())
    metric_norms={k:float(np.linalg.norm(src[k])) for k in
                  ['metric_lapse','metric_shift','metric_longitudinal_scale','metric_transverse_scale']}
    metric_retained=all(v>1e-10 for v in metric_norms.values())
    return {'max_relative_error':max_rel,'all_sources_finite':finite,
            'finite_reference_metric_source_l2':metric_norms,
            'finite_reference_direct_metric_stress_retained':metric_retained,
            'rows':rows,'pass':bool(max_rel<=1e-6 and finite and metric_retained)}


def frame_audit():
    fields,_,_=deterministic_fields()
    Nf,Lf,Rf,bf,rf=fields[:5]
    c=np.cosh(rf); s=np.sinh(rf)
    At=c/Nf; Ax=-bf*c/Nf+s/Lf
    st=s/Nf; sx=-bf*s/Nf+c/Lf
    gtt=-Nf**2+(Lf*bf)**2; gtx=Lf**2*bf; gxx=Lf**2
    def dot(vt,vx,wt,wx):
        return gtt*vt*wt+gtx*(vt*wx+vx*wt)+gxx*vx*wx
    eA=float(np.max(np.abs(dot(At,Ax,At,Ax)+1)))
    es=float(np.max(np.abs(dot(st,sx,st,sx)-1)))
    eAs=float(np.max(np.abs(dot(At,Ax,st,sx))))
    return {'max_abs_A2_plus_1':eA,'max_abs_s2_minus_1':es,'max_abs_A_dot_s':eAs,
            'pass':max(eA,es,eAs)<=1e-12}


def flrw_null_audit():
    Q=sp.symbols('Q', real=True)
    subs0={N:1,L:1,R:1,b:0,r:0,pt:Q,px:0,qt:0,qx:0,q:0,
           om:sp.Rational(17,10),sw:sp.sqrt(sp.Rational(3,5))}
    exact_lag=sp.simplify(lag.subs(subs0))
    exact={k:sp.simplify(v.subs(subs0)) for k,v in partials.items()}
    eps=sp.symbols('eps',real=True)
    R1,PX1,QT1,QX1,Q1,PT1=sp.symbols('R1 PX1 QT1 QX1 Q1 PT1',real=True)
    pert={N:1,L:1,R:1,b:0,r:eps*R1,pt:Q+eps*PT1,px:eps*PX1,
          qt:eps*QT1,qx:eps*QX1,q:eps*Q1,om:sp.Rational(17,10),sw:sp.sqrt(sp.Rational(3,5))}
    metric_linear={}
    for key in ['N','b','L','R']:
        metric_linear[key]=sp.simplify(sp.diff(partials[key].subs(pert),eps).subs(eps,0))
    ok=all(v==0 for v in [exact_lag,*exact.values(),*metric_linear.values()])
    return {'background_lagrangian_exact':str(exact_lag),
            'background_partial_sources_exact':{k:str(v) for k,v in exact.items()},
            'linear_metric_source_coefficients_exact':{k:str(v) for k,v in metric_linear.items()},
            'normalized_absolute_error':0.0 if ok else 1.0,'pass':bool(ok)}


def flrw_bath_equation_audit():
    t=sp.symbols('t', real=True)
    af=sp.Function('a')(t); qf=sp.Function('q')(t); Xf=sp.Function('X')(t)
    oms,sws=sp.symbols('omega sqrtw', positive=True, real=True)
    Lflrw=af**3*sp.Rational(1,4)*(sp.diff(qf,t)**2-(oms*qf-sws*Xf)**2)
    EL=sp.simplify(sp.diff(sp.diff(Lflrw,sp.diff(qf,t)),t)-sp.diff(Lflrw,qf))
    normalized=sp.simplify(2*EL/af**3)
    Hf=sp.diff(af,t)/af
    target=sp.diff(qf,t,2)+3*Hf*sp.diff(qf,t)+oms**2*qf-oms*sws*Xf
    residual=sp.simplify(normalized-target)

    # Conformal conversion: dot q=q'/a, ddot q=(q''-Hc q')/a^2,
    # H=Hc/a. Therefore cosmic equation times a^2 gives
    # q''+2 Hc q'+a^2 omega^2 q=a^2 omega sqrt(w) X.
    qp,qpp,Hc,aa,qq,XX=sp.symbols('qp qpp Hc aa qq XX', real=True)
    cosmic_times_a2=sp.expand((qpp-Hc*qp)+3*Hc*qp+aa**2*oms**2*qq-aa**2*oms*sws*XX)
    conformal_target=qpp+2*Hc*qp+aa**2*oms**2*qq-aa**2*oms*sws*XX
    conformal_residual=sp.simplify(cosmic_times_a2-conformal_target)

    k,chi=sp.symbols('k chi', real=True)
    drive=sp.simplify((aa**2*oms*sws*XX).subs(XX,k*chi/aa))
    drive_target=aa*k*oms*sws*chi
    drive_residual=sp.simplify(drive-drive_target)
    ok=(residual==0 and conformal_residual==0 and drive_residual==0)
    return {'cosmic_EL_normalized':str(normalized),
            'cosmic_target':str(target),'cosmic_residual':str(residual),
            'conformal_residual':str(conformal_residual),
            'frozen_linear_drive_residual':str(drive_residual),
            'pass':bool(ok)}

variation=variation_audit()
frame=frame_audit()
flrw=flrw_null_audit()
bath=flrw_bath_equation_audit()

gates={
    'variation_relative_error_le_1e-6':variation['pass'],
    'unit_frame_absolute_error_le_1e-12':frame['pass'],
    'flrw_null_and_no_linear_direct_stress':flrw['pass'],
    'exact_3H_cosmic_bath_equation':bath['pass'],
    'all_sources_finite':variation['all_sources_finite'],
}
classification=('NL1C3B_LONGITUDINAL_3PLUS1_MEMORY_BRIDGE_PASS' if all(gates.values())
                else 'NL1C3B_LONGITUDINAL_3PLUS1_MEMORY_BRIDGE_FAIL')
result={
    'classification':classification,
    'scope':'exact longitudinal 3+1 component reduction of the frozen NL0B memory action; no memory-survival observable, finite physical eta, collapse statistic, likelihood or observational data',
    'component_reduction':{
        'coframe':'theta0=N dt; theta1=L(dx+b dt); theta2=R dy; theta3=R dz',
        'aether':'A=cosh(r)e0+sinh(r)e1',
        'spatial_unit':'s=sinh(r)e0+cosh(r)e1',
        'per_node_Lhat':'N L R^2/4 * [(Aq)^2-(omega q-sqrt(w) X)^2]',
    },
    'variation_audit':variation,
    'frame_constraint_audit':frame,
    'flrw_null_audit':flrw,
    'flrw_bath_equation_audit':bath,
    'locked_gates':gates,
    'historical_results_unchanged':True,
    'interpretation':'PASS closes the expanding-volume component bridge and reproduces the exact 3H cosmic-time / 2H conformal-time frozen bath dynamics. It permits an action-derived expanding periodic-box source trajectory but is not itself a structure-growth result.'
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
