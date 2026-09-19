#!/usr/bin/env python3
"""GE05 action-derived directional NL0B memory source generator."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

OUT=Path("results/ge05_memory_directional_source_generator.json")
OUT.parent.mkdir(parents=True,exist_ok=True)

# Frozen NL1C3B longitudinal 3+1 per-node memory action.
N,L,R,b,r=sp.symbols("N L R b r", real=True)
pt,px,qt,qx,q=sp.symbols("pt px qt qx q", real=True)
om,sw=sp.symbols("om sw", positive=True, real=True)
ch,sh=sp.cosh(r),sp.sinh(r)
Aq=ch/N*(qt-b*qx)+sh/L*qx
Xphi=sh/N*(pt-b*px)+ch/L*px
lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)

partial_symbols=[pt,px,qt,qx,q,r,N,b,L,R]
partials={str(v):sp.diff(lag,v) for v in partial_symbols}
args=(N,L,R,b,r,pt,px,qt,qx,q,om,sw)
f_partial={k:sp.lambdify(args,v,"numpy") for k,v in partials.items()}

# Directional expansion about an FLRW point.
eps=sp.symbols("eps", real=True)
a,Q=sp.symbols("a Q", positive=True, real=True)
dN,dL,dR,db,dr,dpt,dpx,dqt,dqx,dq=sp.symbols(
    "dN dL dR db dr dpt dpx dqt dqx dq", real=True
)
direction_args=(a,Q,dN,dL,dR,db,dr,dpt,dpx,dqt,dqx,dq,om,sw)
expansion={
    N:1+eps*dN,
    L:a+eps*dL,
    R:a+eps*dR,
    b:eps*db,
    r:eps*dr,
    pt:Q+eps*dpt,
    px:eps*dpx,
    qt:eps*dqt,
    qx:eps*dqx,
    q:eps*dq,
}
coeff1={}
coeff2={}
for key,expr in partials.items():
    ee=sp.expand(expr.subs(expansion))
    coeff1[key]=sp.simplify(sp.diff(ee,eps).subs(eps,0))
    coeff2[key]=sp.simplify(sp.diff(ee,eps,2).subs(eps,0))

metric_keys=("N","b","L","R")
metric_M1_exact_zero=bool(all(sp.simplify(coeff1[k])==0 for k in metric_keys))

f_c1={k:sp.lambdify(direction_args,v,"numpy") for k,v in coeff1.items()}
f_c2={k:sp.lambdify(direction_args,v,"numpy") for k,v in coeff2.items()}

SOURCE_NAMES=(
    "scalar_phi","bath_q","aether_rapidity",
    "metric_lapse","metric_shift",
    "metric_longitudinal_scale","metric_transverse_scale",
)

def centered(x,axis,h):
    return (np.roll(x,-1,axis=axis)-np.roll(x,1,axis=axis))/(2.0*h)

def bc(x,shape):
    return np.broadcast_to(np.asarray(x,float),shape).copy()

def assemble(pd,dt,dx,shape):
    return {
        "scalar_phi":-centered(bc(pd["pt"],shape),0,dt)-centered(bc(pd["px"],shape),1,dx),
        "bath_q":bc(pd["q"],shape)-centered(bc(pd["qt"],shape),0,dt)-centered(bc(pd["qx"],shape),1,dx),
        "aether_rapidity":bc(pd["r"],shape),
        "metric_lapse":bc(pd["N"],shape),
        "metric_shift":bc(pd["b"],shape),
        "metric_longitudinal_scale":bc(pd["L"],shape),
        "metric_transverse_scale":bc(pd["R"],shape),
    }

def deterministic_direction(nt=48,nx=64):
    tt=np.arange(nt)*2.0*np.pi/nt
    xx=np.arange(nx)*2.0*np.pi/nx
    T,X=np.meshgrid(tt,xx,indexing="ij")
    fields={
        "N":0.03*np.sin(T+0.2*X)+0.01*np.cos(2*T-X),
        "L":0.04*np.cos(2*T-X)+0.008*np.sin(T+2*X),
        "R":0.025*np.sin(0.7*T+1.3*X)+0.006*np.cos(2*T+X),
        "b":0.02*np.sin(T-X)+0.005*np.cos(2*T+2*X),
        "r":0.15*np.cos(0.6*T+X)+0.03*np.sin(2*T-X),
        "phi":0.30*np.sin(T+X)+0.20*np.cos(2*T-X),
        "q":0.10*np.cos(T-2*X)+0.05*np.sin(2*T+X),
    }
    return fields,2.0*np.pi/nt,2.0*np.pi/nx

def direction_locals(fields,dt,dx):
    return (
        fields["N"],fields["L"],fields["R"],fields["b"],fields["r"],
        centered(fields["phi"],0,dt),centered(fields["phi"],1,dx),
        centered(fields["q"],0,dt),centered(fields["q"],1,dx),fields["q"],
    )

def analytic_sources(fields,dt,dx,a0=1.0,Q0=0.6,omega=1.7,weight=0.6):
    loc=direction_locals(fields,dt,dx)
    vals=(a0,Q0,*loc,omega,math.sqrt(weight))
    pd1={k:fn(*vals) for k,fn in f_c1.items()}
    pd2={k:fn(*vals) for k,fn in f_c2.items()}
    shape=fields["N"].shape
    return assemble(pd1,dt,dx,shape),assemble(pd2,dt,dx,shape)

def exact_sources(fields,amp,dt,dx,a0=1.0,Q0=0.6,omega=1.7,weight=0.6):
    d=direction_locals(fields,dt,dx)
    dN0,dL0,dR0,db0,dr0,dpt0,dpx0,dqt0,dqx0,dq0=d
    vals=(
        1.0+amp*dN0,
        a0+amp*dL0,
        a0+amp*dR0,
        amp*db0,
        amp*dr0,
        Q0+amp*dpt0,
        amp*dpx0,
        amp*dqt0,
        amp*dqx0,
        amp*dq0,
        omega,math.sqrt(weight),
    )
    pd={k:fn(*vals) for k,fn in f_partial.items()}
    return assemble(pd,dt,dx,fields["N"].shape)

def vectorize(src):
    return np.concatenate([np.asarray(src[k],float).ravel() for k in SOURCE_NAMES])

def norm(x):
    return float(np.linalg.norm(np.asarray(x,float)))

def rel(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),1e-300))

def finite_coeffs(fields,dt,dx,h):
    sp_=exact_sources(fields,+h,dt,dx)
    sm_=exact_sources(fields,-h,dt,dx)
    s0=exact_sources(fields,0.0,dt,dx)
    m1={}
    m2={}
    for k in SOURCE_NAMES:
        m1[k]=(sp_[k]-sm_[k])/(2.0*h)
        m2[k]=(sp_[k]-2.0*s0[k]+sm_[k])/(h*h)
    return m1,m2

fields,dt,dx=deterministic_direction()
M1,M2=analytic_sources(fields,dt,dx)
M1p,M2p=finite_coeffs(fields,dt,dx,1.0e-3)
M1c,M2c=finite_coeffs(fields,dt,dx,3.0e-4)

v1=vectorize(M1); v2=vectorize(M2)
v1p=vectorize(M1p); v2p=vectorize(M2p)
v1c=vectorize(M1c); v2c=vectorize(M2c)

global_controls={
    "analytic_M1_vs_primary_fd_relative_L2":rel(v1,v1p),
    "analytic_M2_vs_primary_fd_relative_L2":rel(v2,v2p),
    "primary_vs_control_fd_M1_relative_L2":rel(v1p,v1c),
    "primary_vs_control_fd_M2_relative_L2":rel(v2p,v2c),
}

per_source={}
all_finite=True
for k in SOURCE_NAMES:
    arrays=(M1[k],M2[k],M1p[k],M2p[k],M1c[k],M2c[k])
    all_finite=bool(all_finite and all(np.all(np.isfinite(x)) for x in arrays))
    per_source[k]={
        "analytic_M1_L2":norm(M1[k]),
        "analytic_M2_L2":norm(M2[k]),
        "primary_fd_M1_L2":norm(M1p[k]),
        "primary_fd_M2_L2":norm(M2p[k]),
        "analytic_vs_primary_fd_M1_relative_L2":rel(M1[k],M1p[k]),
        "analytic_vs_primary_fd_M2_relative_L2":rel(M2[k],M2p[k]),
    }

metric_M2_norm=float(math.sqrt(sum(norm(M2[k])**2 for k in (
    "metric_lapse","metric_shift","metric_longitudinal_scale","metric_transverse_scale"
))))
metric_M2_ok=bool(np.isfinite(metric_M2_norm) and metric_M2_norm>1.0e-10)

gates={
    "all_required_source_blocks_generated":bool(set(per_source)==set(SOURCE_NAMES)),
    "symbolic_direct_metric_M1_exact_zero":metric_M1_exact_zero,
    "analytic_M1_vs_primary_fd_global_relative_L2_le_1e5":global_controls["analytic_M1_vs_primary_fd_relative_L2"]<=1.0e-5,
    "analytic_M2_vs_primary_fd_global_relative_L2_le_1e5":global_controls["analytic_M2_vs_primary_fd_relative_L2"]<=1.0e-5,
    "primary_vs_control_fd_M1_global_relative_L2_le_1e5":global_controls["primary_vs_control_fd_M1_relative_L2"]<=1.0e-5,
    "primary_vs_control_fd_M2_global_relative_L2_le_1e5":global_controls["primary_vs_control_fd_M2_relative_L2"]<=1.0e-5,
    "direct_metric_M2_finite_and_nonzero":metric_M2_ok,
    "all_outputs_finite":all_finite,
}
passed=bool(all(gates.values()))
classification=(
    "GE05_MEMORY_DIRECTIONAL_SOURCE_GENERATOR_PASS"
    if passed else "GE05_MEMORY_DIRECTIONAL_SOURCE_GENERATOR_FAIL"
)

result={
    "classification":classification,
    "predata_classification":"GE05_PREDATA_MEMORY_DIRECTIONAL_SOURCE_GENERATOR",
    "scope":"Action-derived first and second directional coefficients M1/M2 of the frozen NL0B longitudinal 3+1 memory source system around an FLRW point; no memory-off Q block and no Z20/Z21 solve.",
    "frozen_action":{
        "per_node":"N L R^2/4 * [(Aq)^2-(omega q-sqrt(w) X)^2]",
        "background":{"a":1.0,"Q":0.6},
        "omega":1.7,"weight":0.6,
    },
    "symbolic":{
        "direct_metric_M1_exact_zero":metric_M1_exact_zero,
        "generated_partial_blocks":sorted(coeff1.keys()),
    },
    "finite_difference":{
        "primary_step":1.0e-3,
        "control_step":3.0e-4,
        "global_controls":global_controls,
    },
    "direct_metric_M2_combined_L2":metric_M2_norm,
    "per_source":per_source,
    "gates":gates,
    "claim_boundary":"PASS certifies the explicit NL0B memory directional source coefficients M1 and M2 needed by the NL1B2 H4 hierarchy. It does not generate the memory-off analytic Q block, solve Z20/Z21, introduce finite eta, or make collapse/observational claims.",
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps(result,indent=2,sort_keys=True))
if not passed:
    raise SystemExit(2)
