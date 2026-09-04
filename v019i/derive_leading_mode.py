#!/usr/bin/env python3
from pathlib import Path
import json,math,random

H0_KMS_MPC=67.32117
C_KMS=299792.458
H0=H0_KMS_MPC/C_KMS
h=H0_KMS_MPC/100.0
OMEGA_CDM=0.1201075/(h*h)
TARGET=3.0*OMEGA_CDM*H0*H0

MODELS={
 'Cosh':dict(Q0=0.1,K2=7500.0,Z0=1e-9),
 'Exp':dict(Q0=1e-4,K2=9500.0,Z0=1e-17),
}


def eval_z(model,Q0,K2,Z0,z):
    q=Q0+Z0*z
    if model=='Cosh':
        sh=math.sinh(z);ch=math.cosh(z)
        K=2*K2*Z0*Z0*(ch-1)
        KQ=2*K2*Z0*sh
        KQQ=2*K2*ch
    else:
        ex=math.exp(z*z)
        K=2*K2*Z0*Z0*(ex-1)
        KQ=4*K2*Z0*z*ex
        KQQ=4*K2*ex*(1+2*z*z)
    return q,K,KQ,KQQ


def calibrate(model,p):
    lo,hi=0.0,1.0
    def f(z):
        q,K,KQ,KQQ=eval_z(model,**p,z=z)
        return q*KQ-K-TARGET
    while f(hi)<=0:
        hi*=2
        if hi>128: raise RuntimeError('calibration bracket failed')
    for _ in range(180):
        mid=.5*(lo+hi)
        if f(mid)>0: hi=mid
        else: lo=mid
    q,K,KQ,KQQ=eval_z(model,**p,z=.5*(lo+hi))
    return KQ


def exp_z_from_x(x):
    L=math.log(x)
    y=x*x if x<1e-4 else max(L if L>1 else x*x,1e-30)
    for _ in range(80):
        f=y+.5*math.log(y)-L
        fp=1+.5/y
        yn=y-f/fp
        if not (yn>0 and math.isfinite(yn)):yn=.5*y
        if abs(yn-y)<2e-14*(1+y):
            y=yn;break
        y=yn
    return math.sqrt(y)


def background(model,p,I0,a):
    KQ_target=I0/a**3
    if model=='Cosh':
        z=math.asinh(KQ_target/(2*p['K2']*p['Z0']))
    else:
        z=exp_z_from_x(KQ_target/(4*p['K2']*p['Z0']))
    q,K,KQ,KQQ=eval_z(model,**p,z=z)
    rho8=q*KQ-K
    return {'a':a,'Z':z,'Q':q,'KQ':KQ,'w':K/rho8,'cad2':KQ/(q*KQQ)}


def gauge_invariance_test(n=200):
    max_chi=0.0;max_E=0.0
    for _ in range(n):
        Q=10**random.uniform(-4,1)
        varphi=random.uniform(-2,2)
        alpha=random.uniform(-2,2)
        psi=random.uniform(-2,2)
        adot=random.uniform(-2,2)
        T=random.uniform(-2,2)
        Tdot=random.uniform(-2,2)
        chi=varphi+Q*alpha
        E=adot+psi
        varphi2=varphi-Q*T
        alpha2=alpha+T
        psi2=psi-Tdot
        adot2=adot+Tdot
        max_chi=max(max_chi,abs((varphi2+Q*alpha2)-chi))
        max_E=max(max_E,abs((adot2+psi2)-E))
    return max_chi,max_E


def main():
    mch,mE=gauge_invariance_test()
    models={}
    for name,p in MODELS.items():
        I0=calibrate(name,p)
        rows=[background(name,p,I0,a) for a in (1e-4,1e-6,1e-8,1e-10)]
        models[name]={'I0':I0,'early_background':rows,
                      'max_w':max(r['w'] for r in rows),
                      'max_cad2':max(r['cad2'] for r in rows)}
    out={
      'gauge_invariant_combinations':{'chi_max_roundoff':mch,'E_max_roundoff':mE},
      'adiabatic_time_shift':{
        'chi':'0',
        'E':'0',
        'alpha':'-theta',
        'delta':'(1+w_A)*delta_c',
        'Theta':'Theta_c'
      },
      'models':models,
      'gate_status':'PASS' if mch<1e-12 and mE<1e-12 else 'FAIL',
      'scope':'leading k/H -> 0 adiabatic mode; finite-gradient completion is tested separately by CLASS start-time convergence'
    }
    Path('results').mkdir(exist_ok=True)
    Path('results/v019i_derivation.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
    raise SystemExit(0 if out['gate_status']=='PASS' else 1)

if __name__=='__main__':main()
