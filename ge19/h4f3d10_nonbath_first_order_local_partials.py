#!/usr/bin/env python3
"""Source-bound original GE06/GE07/Lambda first-order physical local rows.
No historical generators imported at module import; old is injected only by
the isolated D10 local runner. The original Y first-order flux is zero at X0=0.
"""
from __future__ import annotations
import numpy as np

FIELDS=("N","L","R","b","u","phi","T","rho")
ORIGINAL={"N":"N20","L":"S20","R":"S20",
          "u":"u20","phi":"phi20","T":"T20",
          "rho":"delta_varrho20"}

def evaluate(old,bg,tag,mod6,mod7,state,dot,Dt,nx=128):
    r,dr,dx=old.r7.reduced_state_real(bg,state,nx,dot)
    N=np.asarray(r["N20"],float)
    S=np.asarray(r["S20"],float)
    u=np.asarray(r["u20"],float)
    z=np.zeros_like(N)
    a=np.asarray(bg["a"],float)[:,None]
    adot=(bg["a"]*bg["H"])[:,None]
    Z=bg["Z_action"][:,None]
    kfund=float(old.r7.g9.K_REQ[0]/old.r7.FOURIER_N[0])
    f={n:np.asarray(r[key],float) for n,key in ORIGINAL.items()}
    fx={n:np.asarray(dx[key],float) for n,key in ORIGINAL.items()}
    f["b"]=np.zeros_like(N)
    fx["b"]=np.zeros_like(N)
    # Frozen exact GE06 c1 action partials in original stable-Z variables.
    ge06_args=(a,adot,Z,N,S,S,z,u,
        dr["S20"],dx["S20"],dr["S20"],dx["S20"],z,
        dr["u20"],dx["u20"],dr["phi20"],dx["phi20"],dx["N20"],
        old.r7.KB,old.r7.CV,old.r7.K2,old.r7.Q0,old.r7.Z0)
    p6=old.r7.eval_stable_partials(mod6.f_c1,ge06_args,N.shape,"D10_c1")
    ga=old.r7.assemble_ga_local(p6,Dt,spatial_real=True,kfund=kfund)
    # Exact GE07 frozen dust action: rho0 in frozen GE07 action normalization.
    rhob=(3.0*old.r7.C_VALUES[tag]/bg["a"]**3)[:,None]
    ge07_args=(a,rhob,N,S,S,z,r["delta_varrho20"],
               dr["T20"],dx["T20"])
    p7=old.r7.broadcast_partials(
        {key:fn(*ge07_args) for key,fn in mod7.f_c1.items()},N.shape)
    dust=old.r7.assemble_m_local(p7,Dt,spatial_real=True,kfund=kfund)
    # Original Lambda action -6 rho_lambda N L R^2; no shift or current.
    rl=np.asarray(bg["rho_lambda_action"],float)[:,None]
    lam={"N":-18.0*rl*a*a*S,
         "L":-6.0*rl*(a*a*N+2.0*a*S),
         "R":-12.0*rl*(a*a*N+2.0*a*S)}
    e={n:np.asarray(ga.get(n,0)+dust.get(n,0)+lam.get(n,0),float)
       for n in FIELDS}
    for k,v in list(f.items())+list(fx.items())+list(e.items()):
        if v.shape!=N.shape or not np.isfinite(v).all():
            raise RuntimeError("D10 nonfinite actual first-order field or Euler: "+k)
    return f,fx,e
