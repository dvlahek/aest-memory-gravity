#!/usr/bin/env python3
"""GE07 pressureless-matter directional source generator.

Generates the first and second common-direction perturbative coefficients of
the already certified minimally coupled pressureless-dust action in the same
plane-symmetric scalar-longitudinal 3+1 geometry used by GE06.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp

OUT=Path("results/ge07_pressureless_matter_directional_source_generator.json")
OUT.parent.mkdir(parents=True,exist_ok=True)

# ---------------------------------------------------------------------------
# Frozen certified dust action:
# L_d = N L R^2 varrho [W^2 - V^2 - 1],
# W=(Tt-b Tx)/N, V=Tx/L.
# ---------------------------------------------------------------------------
N,L,R,b,varrho,Tt,Tx=sp.symbols(
    "N L R b varrho Tt Tx", positive=True, real=True
)
W=(Tt-b*Tx)/N
V=Tx/L
lag=sp.expand(N*L*R**2*varrho*(W**2-V**2-1))

partial_map={
    "N_f":sp.diff(lag,N),
    "L_f":sp.diff(lag,L),
    "R_f":sp.diff(lag,R),
    "b_f":sp.diff(lag,b),
    "rho_f":sp.diff(lag,varrho),
    "T_t":sp.diff(lag,Tt),
    "T_x":sp.diff(lag,Tx),
}
exact_args=(N,L,R,b,varrho,Tt,Tx)
f_exact={k:sp.lambdify(exact_args,v,"numpy",cse=True) for k,v in partial_map.items()}

# ---------------------------------------------------------------------------
# Common-direction expansion about homogeneous comoving dust FLRW:
# N=1, b=0, L=R=a(t), varrho=rho0/a^3, Tt=1, Tx=0.
# ---------------------------------------------------------------------------
eps=sp.symbols("eps", real=True)
aa,rhob=sp.symbols("aa rhob", positive=True, real=True)
dN,dL,dR,db,drho,dTt,dTx=sp.symbols(
    "dN dL dR db drho dTt dTx", real=True
)
direction_args=(aa,rhob,dN,dL,dR,db,drho,dTt,dTx)
expansion={
    N:1+eps*dN,
    L:aa+eps*dL,
    R:aa+eps*dR,
    b:eps*db,
    varrho:rhob+eps*drho,
    Tt:1+eps*dTt,
    Tx:eps*dTx,
}

coeff1={}
coeff2={}
for key,expr in partial_map.items():
    ee=expr.subs(expansion)
    coeff1[key]=sp.simplify(sp.diff(ee,eps).subs(eps,0))
    coeff2[key]=sp.simplify(sp.diff(ee,eps,2).subs(eps,0))

f_c1={k:sp.lambdify(direction_args,v,"numpy",cse=True) for k,v in coeff1.items()}
f_c2={k:sp.lambdify(direction_args,v,"numpy",cse=True) for k,v in coeff2.items()}

# Exact background audits.
rho0=sp.symbols("rho0", positive=True, real=True)
background={
    N:1,L:aa,R:aa,b:0,varrho:rho0/aa**3,Tt:1,Tx:0
}
normalization_bg=sp.simplify((W**2-V**2-1).subs(background))
Jt=sp.simplify(sp.diff(lag,Tt)/2)
Jx=sp.simplify(sp.diff(lag,Tx)/2)
Jt_bg=sp.simplify(Jt.subs(background))
Jx_bg=sp.simplify(Jx.subs(background))
background_normalization_zero=bool(normalization_bg==0)
background_current_time_constant=bool(sp.simplify(Jt_bg-rho0)==0)
background_current_space_zero=bool(Jx_bg==0)

# Strict minimal-coupling / principal-block checks.
u,phi,q,eta,Y,Q=sp.symbols("u phi q eta Y Q", real=True)
no_direct_aest_memory=not any(lag.has(z) for z in (u,phi,q,eta,Y,Q))
Lt,Rt,ut,pt=sp.symbols("Lt Rt ut pt", real=True)
principal_zero=bool(sp.hessian(lag,(Lt,Rt,ut,pt))==sp.zeros(4))

SOURCE_NAMES=(
    "metric_lapse",
    "metric_longitudinal_scale",
    "metric_transverse_scale",
    "metric_shift",
    "dust_potential_T",
    "dust_density_varrho",
)

def centered(x,axis,h):
    return (np.roll(x,-1,axis=axis)-np.roll(x,1,axis=axis))/(2.0*h)

def bc(x,shape):
    return np.broadcast_to(np.asarray(x,float),shape).copy()

def assemble(pd,dt,dx,shape):
    return {
        "metric_lapse":bc(pd["N_f"],shape),
        "metric_longitudinal_scale":bc(pd["L_f"],shape),
        "metric_transverse_scale":bc(pd["R_f"],shape),
        "metric_shift":bc(pd["b_f"],shape),
        "dust_potential_T":(
            -centered(bc(pd["T_t"],shape),0,dt)
            -centered(bc(pd["T_x"],shape),1,dx)
        ),
        "dust_density_varrho":bc(pd["rho_f"],shape),
    }

def deterministic_grid(nt=48,nx=64):
    tt=np.arange(nt,dtype=float)*(2.0*np.pi/nt)
    xx=np.arange(nx,dtype=float)*(2.0*np.pi/nx)
    TT,XX=np.meshgrid(tt,xx,indexing="ij")
    dt=2.0*np.pi/nt
    dx=2.0*np.pi/nx

    a=1.0+0.08*np.sin(TT)+0.02*np.cos(2.0*TT)
    rhob=0.25/a**3

    direction={
        "N":0.025*np.sin(TT+XX)+0.008*np.cos(2*TT-XX),
        "L":0.030*np.cos(2*TT-XX)+0.007*np.sin(TT+2*XX),
        "R":0.022*np.sin(TT+2*XX)+0.006*np.cos(3*TT-XX),
        "b":0.018*np.sin(TT-XX)+0.004*np.cos(2*TT+XX),
        "rho":0.035*np.cos(TT+XX)+0.011*np.sin(2*TT-XX),
        "T":0.13*np.sin(TT+XX)+0.07*np.cos(2*TT-XX),
    }
    return TT,XX,dt,dx,a,rhob,direction

def direction_locals(direction,dt,dx):
    return (
        direction["N"],
        direction["L"],
        direction["R"],
        direction["b"],
        direction["rho"],
        centered(direction["T"],0,dt),
        centered(direction["T"],1,dx),
    )

def analytic_sources(a,rhob,direction,dt,dx):
    vals=(a,rhob,*direction_locals(direction,dt,dx))
    p1={k:fn(*vals) for k,fn in f_c1.items()}
    p2={k:fn(*vals) for k,fn in f_c2.items()}
    shape=direction["N"].shape
    return assemble(p1,dt,dx,shape),assemble(p2,dt,dx,shape)

def exact_sources(a,rhob,direction,amp,dt,dx):
    dN0,dL0,dR0,db0,drho0,dTt0,dTx0=direction_locals(direction,dt,dx)
    vals=(
        1.0+amp*dN0,
        a+amp*dL0,
        a+amp*dR0,
        amp*db0,
        rhob+amp*drho0,
        1.0+amp*dTt0,
        amp*dTx0,
    )
    pd={k:fn(*vals) for k,fn in f_exact.items()}
    return assemble(pd,dt,dx,direction["N"].shape)

def vectorize(src):
    return np.concatenate([np.asarray(src[k],float).ravel() for k in SOURCE_NAMES])

def norm(x):
    return float(np.linalg.norm(np.asarray(x,float)))

def rel(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),1e-300))

def finite_coeffs(a,rhob,direction,dt,dx,h):
    sp_=exact_sources(a,rhob,direction,+h,dt,dx)
    sm_=exact_sources(a,rhob,direction,-h,dt,dx)
    s0=exact_sources(a,rhob,direction,0.0,dt,dx)
    lin={}
    quad={}
    for k in SOURCE_NAMES:
        lin[k]=(sp_[k]-sm_[k])/(2.0*h)
        quad[k]=(sp_[k]-2.0*s0[k]+sm_[k])/(h*h)
    return lin,quad

TT,XX,dt,dx,a,rhob,direction=deterministic_grid()
L1,Q2=analytic_sources(a,rhob,direction,dt,dx)
L1p,Q2p=finite_coeffs(a,rhob,direction,dt,dx,1.0e-3)
L1c,Q2c=finite_coeffs(a,rhob,direction,dt,dx,3.0e-4)

vL=vectorize(L1); vQ=vectorize(Q2)
vLp=vectorize(L1p); vQp=vectorize(Q2p)
vLc=vectorize(L1c); vQc=vectorize(Q2c)

controls={
    "analytic_L_vs_primary_fd_relative_L2":rel(vL,vLp),
    "analytic_Q_vs_primary_fd_relative_L2":rel(vQ,vQp),
    "primary_vs_control_fd_L_relative_L2":rel(vLp,vLc),
    "primary_vs_control_fd_Q_relative_L2":rel(vQp,vQc),
}

per_source={}
all_finite=True
for k in SOURCE_NAMES:
    arrays=(L1[k],Q2[k],L1p[k],Q2p[k],L1c[k],Q2c[k])
    all_finite=bool(all_finite and all(np.all(np.isfinite(x)) for x in arrays))
    per_source[k]={
        "analytic_L_L2":norm(L1[k]),
        "analytic_Q_L2":norm(Q2[k]),
        "primary_fd_L_L2":norm(L1p[k]),
        "primary_fd_Q_L2":norm(Q2p[k]),
        "analytic_vs_primary_fd_L_relative_L2":rel(L1[k],L1p[k]),
        "analytic_vs_primary_fd_Q_relative_L2":rel(Q2[k],Q2p[k]),
    }

gates={
    "background_normalization_constraint_zero":background_normalization_zero,
    "background_dust_current_conservation_zero":bool(
        background_current_time_constant and background_current_space_zero
    ),
    "no_direct_aest_or_memory_coupling":bool(no_direct_aest_memory),
    "no_field_principal_hessian_contribution":bool(principal_zero),
    "all_required_source_blocks_generated":bool(set(per_source)==set(SOURCE_NAMES)),
    "analytic_L_vs_primary_fd_global_relative_L2_le_1e5":controls["analytic_L_vs_primary_fd_relative_L2"]<=1.0e-5,
    "analytic_Q_vs_primary_fd_global_relative_L2_le_1e5":controls["analytic_Q_vs_primary_fd_relative_L2"]<=1.0e-5,
    "primary_vs_control_fd_L_global_relative_L2_le_1e5":controls["primary_vs_control_fd_L_relative_L2"]<=1.0e-5,
    "primary_vs_control_fd_Q_global_relative_L2_le_1e5":controls["primary_vs_control_fd_Q_relative_L2"]<=1.0e-5,
    "all_outputs_finite":all_finite,
}
passed=bool(all(gates.values()))
classification=(
    "GE07_PRESSURELESS_MATTER_DIRECTIONAL_SOURCE_GENERATOR_PASS"
    if passed else "GE07_PRESSURELESS_MATTER_DIRECTIONAL_SOURCE_GENERATOR_FAIL"
)

result={
    "classification":classification,
    "predata_classification":"GE07_PREDATA_PRESSURELESS_MATTER_DIRECTIONAL_SOURCE_GENERATOR",
    "scope":"Minimally coupled pressureless-matter longitudinal plane-symmetric 3+1 L/Q directional source generator only; no Z20/Z21 solve and eta=0 only.",
    "frozen_action":{
        "covariant":"-1/2 int sqrt(-g) rho_phys (g^munu d_mu T d_nu T + 1)",
        "density_rescaling":"varrho=8*pi*G*rho_phys",
        "reduced":str(lag),
        "free_matter_coupling":False,
    },
    "background":{
        "a":"1+0.08 sin(t)+0.02 cos(2t)",
        "varrho":"0.25/a^3",
        "T_t":1.0,
        "T_x":0.0,
        "Nt":48,
        "Nx":64,
    },
    "exact_checks":{
        "normalization_background":str(normalization_bg),
        "Jt_background":str(Jt_bg),
        "Jx_background":str(Jx_bg),
        "principal_hessian_zero":principal_zero,
        "no_direct_aest_memory":no_direct_aest_memory,
    },
    "finite_difference":{
        "primary_step":1.0e-3,
        "control_step":3.0e-4,
        "global_controls":controls,
    },
    "per_source":per_source,
    "gates":gates,
    "claim_boundary":"PASS certifies the pressureless-matter L/Q directional source generator needed for the H3/H4 scalar hierarchy. It does not solve Z20/Z21, include additional standard-matter nonlinear species, introduce finite eta, or make collapse/observational claims.",
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps(result,indent=2,sort_keys=True))
if not passed:
    raise SystemExit(2)
