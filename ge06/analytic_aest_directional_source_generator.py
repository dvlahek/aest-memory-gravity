#!/usr/bin/env python3
"""GE06 memory-off analytic Einstein+AeST directional source generator.

Generates the first and second perturbative directional coefficients of the
plane-symmetric scalar-longitudinal 3+1 Euler-Lagrange source system from the
frozen analytic action.  The nonanalytic Y sector is deliberately excluded:
its Y2/DY2 operators are handled separately by NL1B2/GE04.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

OUT=Path("results/ge06_analytic_aest_directional_source_generator.json")
OUT.parent.mkdir(parents=True,exist_ok=True)

# ---------------------------------------------------------------------------
# Frozen representative audit parameters.  These condition the generator
# test only; the action structure and functional Exp K(Q) dependence are the
# scientific object being audited.
# ---------------------------------------------------------------------------
KBV=0.1
CV=2.0-KBV
K2V=0.4
Q0V=0.2
Z0V=0.7

# ---------------------------------------------------------------------------
# Exact longitudinal plane-symmetric 3+1 analytic Einstein+AeST action.
# theta0=N dt, theta1=L(dx+b dt), theta2=R dy, theta3=R dz.
#
# The GR spatial-curvature term is the plane-symmetric counterpart of the
# spherical NL1C6 reduction, after one radial integration by parts:
#   2 N Rx^2/L + 4 Nx R Rx/L.
# There is no +2 N L unit-sphere curvature term.
# ---------------------------------------------------------------------------
N,L,R,b,u,phi=sp.symbols("N L R b u phi", real=True)
Lt,Lx,Rt,Rx,bx,ut,ux,pt,px,Nx=sp.symbols(
    "Lt Lx Rt Rx bx ut ux pt px Nx", real=True
)

KB,C,K2,Q0,Z0=sp.symbols("KB C K2 Q0 Z0", positive=True, real=True)
ch,sh=sp.cosh(u),sp.sinh(u)

kL=(Lt-b*Lx-L*bx)/(N*L)
kR=(Rt-b*Rx)/(N*R)
sigma=(pt-b*px)/N
Qinv=ch*sigma+sh*px/L
Xinv=sh*sigma+ch*px/L
E=ch*((ut-b*ux)/N+Nx/(N*L))+sh*(kL+ux/L)

z=(Qinv-Q0)/Z0
Kfun=2*K2*Z0**2*(sp.exp(z**2)-1)

grav=N*L*R**2*(-4*kL*kR-2*kR**2) + 2*N*Rx**2/L + 4*Nx*R*Rx/L
aest=N*L*R**2*(KB*E**2 + 2*C*E*Xinv - C*Xinv**2 + 2*Kfun)
lag=sp.expand(grav+aest)

# Local partials required for Euler-Lagrange assembly.
partial_map={
    "N_f":sp.diff(lag,N),
    "N_x":sp.diff(lag,Nx),
    "L_f":sp.diff(lag,L),
    "L_t":sp.diff(lag,Lt),
    "L_x":sp.diff(lag,Lx),
    "R_f":sp.diff(lag,R),
    "R_t":sp.diff(lag,Rt),
    "R_x":sp.diff(lag,Rx),
    "b_f":sp.diff(lag,b),
    "b_x":sp.diff(lag,bx),
    "u_f":sp.diff(lag,u),
    "u_t":sp.diff(lag,ut),
    "u_x":sp.diff(lag,ux),
    "phi_t":sp.diff(lag,pt),
    "phi_x":sp.diff(lag,px),
}

exact_args=(
    N,L,R,b,u,Lt,Lx,Rt,Rx,bx,ut,ux,pt,px,Nx,
    KB,C,K2,Q0,Z0,
)
f_exact={k:sp.lambdify(exact_args,v,"numpy",cse=True) for k,v in partial_map.items()}

# ---------------------------------------------------------------------------
# Symbolic common-direction expansion about a homogeneous FLRW point.
# Local background inputs a, adot, Qb are supplied pointwise.
# ---------------------------------------------------------------------------
eps=sp.symbols("eps", real=True)
aa,adot,Qb=sp.symbols("aa adot Qb", positive=True, real=True)
dN,dL,dR,db,du,dLt,dLx,dRt,dRx,dbx,dut,dux,dpt,dpx,dNx=sp.symbols(
    "dN dL dR db du dLt dLx dRt dRx dbx dut dux dpt dpx dNx",
    real=True,
)

direction_args=(
    aa,adot,Qb,
    dN,dL,dR,db,du,dLt,dLx,dRt,dRx,dbx,dut,dux,dpt,dpx,dNx,
    KB,C,K2,Q0,Z0,
)

expansion={
    N:1+eps*dN,
    L:aa+eps*dL,
    R:aa+eps*dR,
    b:eps*db,
    u:eps*du,
    Lt:adot+eps*dLt,
    Lx:eps*dLx,
    Rt:adot+eps*dRt,
    Rx:eps*dRx,
    bx:eps*dbx,
    ut:eps*dut,
    ux:eps*dux,
    pt:Qb+eps*dpt,
    px:eps*dpx,
    Nx:eps*dNx,
}

coeff1={}
coeff2={}
for key,expr in partial_map.items():
    ee=expr.subs(expansion)
    coeff1[key]=sp.simplify(sp.diff(ee,eps).subs(eps,0))
    coeff2[key]=sp.simplify(sp.diff(ee,eps,2).subs(eps,0))

f_c1={k:sp.lambdify(direction_args,v,"numpy",cse=True) for k,v in coeff1.items()}
f_c2={k:sp.lambdify(direction_args,v,"numpy",cse=True) for k,v in coeff2.items()}

# Exact Exp KQQ identity audit.
qq=sp.symbols("qq", real=True)
zz=(qq-Q0)/Z0
Kqq_expr=sp.diff(2*K2*Z0**2*(sp.exp(zz**2)-1),qq,2)
Kqq_expected=4*K2*sp.exp(zz**2)*(1+2*zz**2)
Kqq_identity=bool(sp.simplify(Kqq_expr-Kqq_expected)==0)

SOURCE_NAMES=(
    "metric_lapse",
    "metric_longitudinal_scale",
    "metric_transverse_scale",
    "metric_shift",
    "aether_rapidity",
    "scalar_phi",
)

def centered(x,axis,h):
    return (np.roll(x,-1,axis=axis)-np.roll(x,1,axis=axis))/(2.0*h)

def bc(x,shape):
    return np.broadcast_to(np.asarray(x,float),shape).copy()

def assemble(pd,dt,dx,shape):
    return {
        "metric_lapse":bc(pd["N_f"],shape)-centered(bc(pd["N_x"],shape),1,dx),
        "metric_longitudinal_scale":(
            bc(pd["L_f"],shape)
            -centered(bc(pd["L_t"],shape),0,dt)
            -centered(bc(pd["L_x"],shape),1,dx)
        ),
        "metric_transverse_scale":(
            bc(pd["R_f"],shape)
            -centered(bc(pd["R_t"],shape),0,dt)
            -centered(bc(pd["R_x"],shape),1,dx)
        ),
        "metric_shift":bc(pd["b_f"],shape)-centered(bc(pd["b_x"],shape),1,dx),
        "aether_rapidity":(
            bc(pd["u_f"],shape)
            -centered(bc(pd["u_t"],shape),0,dt)
            -centered(bc(pd["u_x"],shape),1,dx)
        ),
        "scalar_phi":(
            -centered(bc(pd["phi_t"],shape),0,dt)
            -centered(bc(pd["phi_x"],shape),1,dx)
        ),
    }

def deterministic_grid(nt=48,nx=64):
    tt=np.arange(nt,dtype=float)*(2.0*np.pi/nt)
    xx=np.arange(nx,dtype=float)*(2.0*np.pi/nx)
    T,X=np.meshgrid(tt,xx,indexing="ij")
    dt=2.0*np.pi/nt
    dx=2.0*np.pi/nx

    a=1.0+0.08*np.sin(T)+0.02*np.cos(2.0*T)
    adot=0.08*np.cos(T)-0.04*np.sin(2.0*T)
    qb=0.2+0.03*np.cos(T)

    direction={
        "N":0.025*np.sin(T+X)+0.008*np.cos(2*T-X),
        "L":0.030*np.cos(2*T-X)+0.007*np.sin(T+2*X),
        "R":0.022*np.sin(T+2*X)+0.006*np.cos(3*T-X),
        "b":0.018*np.sin(T-X)+0.004*np.cos(2*T+X),
        "u":0.11*np.cos(T+X)+0.025*np.sin(2*T-X),
        "phi":0.20*np.sin(T+X)+0.13*np.cos(2*T-X),
    }
    return T,X,dt,dx,a,adot,qb,direction

def direction_locals(direction,dt,dx):
    return (
        direction["N"],
        direction["L"],
        direction["R"],
        direction["b"],
        direction["u"],
        centered(direction["L"],0,dt),
        centered(direction["L"],1,dx),
        centered(direction["R"],0,dt),
        centered(direction["R"],1,dx),
        centered(direction["b"],1,dx),
        centered(direction["u"],0,dt),
        centered(direction["u"],1,dx),
        centered(direction["phi"],0,dt),
        centered(direction["phi"],1,dx),
        centered(direction["N"],1,dx),
    )

def analytic_sources(a,adot,qb,direction,dt,dx):
    loc=direction_locals(direction,dt,dx)
    vals=(a,adot,qb,*loc,KBV,CV,K2V,Q0V,Z0V)
    p1={k:fn(*vals) for k,fn in f_c1.items()}
    p2={k:fn(*vals) for k,fn in f_c2.items()}
    shape=direction["N"].shape
    return assemble(p1,dt,dx,shape),assemble(p2,dt,dx,shape)

def exact_sources(a,adot,qb,direction,amp,dt,dx):
    d=direction_locals(direction,dt,dx)
    (
        dN0,dL0,dR0,db0,du0,dLt0,dLx0,dRt0,dRx0,
        dbx0,dut0,dux0,dpt0,dpx0,dNx0
    )=d
    vals=(
        1.0+amp*dN0,
        a+amp*dL0,
        a+amp*dR0,
        amp*db0,
        amp*du0,
        adot+amp*dLt0,
        amp*dLx0,
        adot+amp*dRt0,
        amp*dRx0,
        amp*dbx0,
        amp*dut0,
        amp*dux0,
        qb+amp*dpt0,
        amp*dpx0,
        amp*dNx0,
        KBV,CV,K2V,Q0V,Z0V,
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

def finite_coeffs(a,adot,qb,direction,dt,dx,h):
    sp_=exact_sources(a,adot,qb,direction,+h,dt,dx)
    sm_=exact_sources(a,adot,qb,direction,-h,dt,dx)
    s0=exact_sources(a,adot,qb,direction,0.0,dt,dx)
    lin={}
    quad={}
    for k in SOURCE_NAMES:
        lin[k]=(sp_[k]-sm_[k])/(2.0*h)
        quad[k]=(sp_[k]-2.0*s0[k]+sm_[k])/(h*h)
    return lin,quad

T,X,dt,dx,a,adot,qb,direction=deterministic_grid()
L1,Q2=analytic_sources(a,adot,qb,direction,dt,dx)
L1p,Q2p=finite_coeffs(a,adot,qb,direction,dt,dx,1.0e-3)
L1c,Q2c=finite_coeffs(a,adot,qb,direction,dt,dx,3.0e-4)

vL=vectorize(L1)
vQ=vectorize(Q2)
vLp=vectorize(L1p)
vQp=vectorize(Q2p)
vLc=vectorize(L1c)
vQc=vectorize(Q2c)

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
    "exact_exp_KQQ_identity":Kqq_identity,
    "all_required_source_blocks_generated":bool(set(per_source)==set(SOURCE_NAMES)),
    "analytic_L_vs_primary_fd_global_relative_L2_le_1e5":controls["analytic_L_vs_primary_fd_relative_L2"]<=1.0e-5,
    "analytic_Q_vs_primary_fd_global_relative_L2_le_1e5":controls["analytic_Q_vs_primary_fd_relative_L2"]<=1.0e-5,
    "primary_vs_control_fd_L_global_relative_L2_le_1e5":controls["primary_vs_control_fd_L_relative_L2"]<=1.0e-5,
    "primary_vs_control_fd_Q_global_relative_L2_le_1e5":controls["primary_vs_control_fd_Q_relative_L2"]<=1.0e-5,
    "all_outputs_finite":all_finite,
}
passed=bool(all(gates.values()))
classification=(
    "GE06_ANALYTIC_AEST_DIRECTIONAL_SOURCE_GENERATOR_PASS"
    if passed else "GE06_ANALYTIC_AEST_DIRECTIONAL_SOURCE_GENERATOR_FAIL"
)

result={
    "classification":classification,
    "predata_classification":"GE06_PREDATA_ANALYTIC_AEST_DIRECTIONAL_SOURCE_GENERATOR",
    "scope":"Memory-off analytic Einstein+AeST longitudinal plane-symmetric 3+1 L/Q directional source generator. The nonanalytic Y sector and matter nonlinearities are excluded by construction.",
    "frozen_action":{
        "GR_kinetic":"N L R^2[-4 kL kR-2 kR^2]",
        "GR_plane_curvature":"2 N Rx^2/L + 4 Nx R Rx/L",
        "AeST_analytic":"N L R^2[KB E^2+2 C E X-C X^2+2 K(Q)]",
        "Y_sector_included":False,
        "audit_parameters":{"KB":KBV,"C":CV,"K2":K2V,"Q0":Q0V,"Z0":Z0V},
    },
    "symbolic":{
        "Exp_KQQ_identity_exact":Kqq_identity,
        "generated_local_partial_count":len(partial_map),
    },
    "background":{
        "a":"1+0.08 sin(t)+0.02 cos(2t)",
        "Q":"0.2+0.03 cos(t)",
        "Nt":48,"Nx":64,
    },
    "finite_difference":{
        "primary_step":1.0e-3,
        "control_step":3.0e-4,
        "global_controls":controls,
    },
    "per_source":per_source,
    "gates":gates,
    "claim_boundary":"PASS certifies the memory-off analytic Einstein+AeST L/Q directional source generator in the controlled scalar-longitudinal plane-symmetric sector. It excludes the separately certified Y operator and matter nonlinearities, does not solve Z20/Z21, introduce finite eta, or establish collapse/observational claims.",
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps(result,indent=2,sort_keys=True))
if not passed:
    raise SystemExit(2)
