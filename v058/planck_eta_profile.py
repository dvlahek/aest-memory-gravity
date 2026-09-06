#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys
import numpy as np
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import v056.planck_highl_lowl_refit as v


def fit_fixed_eta(eta, cr, packages, out):
    state=dict(v.START)
    state.update(eta=float(eta), A_planck=1.0)
    text=v.BASE.read_text()
    lt=v.LowTT(packages); le=v.LowEE(packages)
    hist=[]
    for it in range(v.NITER):
        hl,B,T,D,fb,ft,FD=v.generate(cr,packages,text,state,it)
        names=v.PARAMS+['A_planck']
        bounds=[]
        for n in names:
            trust=v.STEP[n] if n in v.PARAMS else 0.005
            lo,hi=v.BOUNDS[n]
            bounds.append((max(-trust,lo-state[n]),min(trust,hi-state[n])))
        f=lambda x: v.total_chi2(hl,lt,le,B,T,fb,ft,state,x,D,FD,names)
        before=f(np.zeros(len(names)))
        sol=minimize(f,np.zeros(len(names)),method='Powell',bounds=bounds,
                     options={'maxiter':500,'xtol':1e-6,'ftol':1e-6})
        delta=dict(zip(names,sol.x))
        hist.append({'iteration':it,'chi2_before':float(before),
                     'local_chi2_after':float(sol.fun),'delta':{k:float(x) for k,x in delta.items()},
                     'success':bool(sol.success),'message':str(sol.message)})
        for n,x in delta.items(): state[n]+=float(x)
        state['eta']=float(eta)
    hl,B,T,D,fb,ft,FD=v.generate(cr,packages,text,state,v.NITER)
    final=float(v.total_chi2(hl,lt,le,B,T,fb,ft,state))
    res={
      'classification':'V058_PLANCK_FIXED_ETA_PROFILE_MEMBER_COMPLETE',
      'eta_fixed':float(eta),'iterations':v.NITER,'final_state':state,'final_chi2':final,
      'history':hist,
      'locked_model':{'KB':v.KB,'tauH0':v.TAUH0,'p':0.0,'lambda':v.LAMBDA,
                      'CLASS_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540'},
      'likelihood':'Planck 2018 Plik-lite TTTEEE native high-l + native low-l TT + native low-l EE; common A_planck Gaussian prior sigma=0.0025',
      'profiled_parameters':v.PARAMS+['A_planck'],
      'scope':'Fixed-eta deterministic six-parameter profile member using the same v0.56 iterated CLASS local-linearization machinery. Not an MCMC posterior.',
      'anti_tuning':'Frozen v0.53 physics and predeclared v0.58 eta grid unchanged.'
    }
    Path(out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--class-root',required=True); ap.add_argument('--packages',required=True)
    ap.add_argument('--eta',type=float,required=True); ap.add_argument('--json-out',required=True); z=ap.parse_args()
    fit_fixed_eta(z.eta,Path(z.class_root).resolve(),Path(z.packages).resolve(),z.json_out)

if __name__=='__main__': main()
