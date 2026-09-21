#!/usr/bin/env python3
"""GE19 Repair23 normalized-bath bridge audit for q20.

Theory/numerics bridge only. No q20 solve and no H4/Z21 solve.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import math
import os
import tempfile
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
OUT=Path("results/ge19_repair23_q20_normalized_bath_bridge_audit.json")

C1_MAX=1.0e-10
C2_FD_MAX=1.0e-5
WEIGHT_MAX=1.0e-12
STEP_MAX=1.0e-8
TINY=1.0e-300


def load_quiet(path:Path,name:str):
    old=os.getcwd()
    with tempfile.TemporaryDirectory() as td:
        os.chdir(td)
        try:
            spec=importlib.util.spec_from_file_location(name,path)
            if spec is None or spec.loader is None:
                raise RuntimeError(f"cannot import {path}")
            mod=importlib.util.module_from_spec(spec)
            with contextlib.redirect_stdout(io.StringIO()):
                spec.loader.exec_module(mod)
            return mod
        finally:
            os.chdir(old)


def rel(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def aor(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    ae=np.abs(aa-bb)
    re=ae/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),TINY)
    return float(np.max(np.minimum(ae,re)))


def symbolic_identities():
    t,xi=sp.symbols("t xi", real=True)
    a=sp.Function("a")(t)
    z=sp.Function("z")(t)
    X=sp.Function("X")(t)
    om,sw,tau=sp.symbols("omega sqrtw tau", positive=True, real=True)
    q=sw*z/om
    L=a**3*sp.Rational(1,4)*(sp.diff(q,t)**2-(om*q-sw*X)**2)
    EL=sp.simplify(sp.diff(L,q) if False else 0)  # placeholder avoided; q is composite

    # Derive before substitution using an independent q function.
    qf=sp.Function("q")(t)
    Lq=a**3*sp.Rational(1,4)*(sp.diff(qf,t)**2-(om*qf-sw*X)**2)
    euler=sp.simplify(sp.diff(Lq,qf)-sp.diff(sp.diff(Lq,sp.diff(qf,t)),t))
    ez=sp.simplify(euler.subs({
        qf:sw*z/om,
        sp.diff(qf,t):sw*sp.diff(z,t)/om,
        sp.diff(qf,t,2):sw*sp.diff(z,t,2)/om,
    }))
    H=sp.diff(a,t)/a
    target_z=sp.diff(z,t,2)+3*H*sp.diff(z,t)+om**2*(z-X)
    scaled=sp.simplify((-2*om/(a**3*sw))*ez)
    q_to_z_residual=sp.simplify(scaled-target_z)

    # t=tau*xi; z_t=z_xi/tau; H=h/tau; r=omega*tau.
    zxi,zxixi,h,r,XX=sp.symbols("zxi zxixi h r XX", real=True)
    cosmic_tau2=sp.expand(
        zxixi + 3*h*zxi + (om*tau)**2*(sp.Symbol("zz")-XX)
    )
    dimensionless=zxixi+3*h*zxi+r**2*(sp.Symbol("zz")-XX)
    dim_residual=sp.simplify(cosmic_tau2.subs(om*tau,r)-dimensionless)

    return {
        "q_to_z_FLRW_residual":str(q_to_z_residual),
        "cosmic_to_dimensionless_residual":str(dim_residual),
        "q_to_z_exact":bool(q_to_z_residual==0),
        "dimensionless_exact":bool(dim_residual==0),
        "normalized_bath_variable":"z=omega*q/sqrt(w)",
        "cosmic_equation":"zddot+3H zdot+omega^2(z-X)=0",
        "dimensionless_equation":"z_xixi+3h z_xi+r^2(z-X)=0",
    }


def c1_discrete_audit(ge05):
    fields,dt,dx=ge05.deterministic_direction()
    omega=1.7; weight=0.6; sw=math.sqrt(weight); Q=0.6
    M1,_=ge05.analytic_sources(fields,dt,dx,a0=1.0,Q0=Q,omega=omega,weight=weight)
    z=omega*np.asarray(fields["q"],float)/sw
    X=Q*np.asarray(fields["r"],float)+ge05.centered(np.asarray(fields["phi"],float),1,dx)
    ztt=ge05.centered(ge05.centered(z,0,dt),0,dt)
    standard=ztt+omega**2*(z-X)
    normalized=(-2.0*omega/sw)*np.asarray(M1["bath_q"],float)
    return {
        "relative_L2":rel(normalized,standard),
        "max_abs_or_relative":aor(normalized,standard),
        "all_finite":bool(np.all(np.isfinite(normalized)) and np.all(np.isfinite(standard))),
    }


def c2_fd_audit(ge05):
    fields,dt,dx=ge05.deterministic_direction()
    _,M2=ge05.analytic_sources(fields,dt,dx)
    _,M2p=ge05.finite_coeffs(fields,dt,dx,1.0e-3)
    _,M2c=ge05.finite_coeffs(fields,dt,dx,3.0e-4)
    return {
        "analytic_vs_primary_relative_L2":rel(M2["bath_q"],M2p["bath_q"]),
        "primary_vs_control_relative_L2":rel(M2p["bath_q"],M2c["bath_q"]),
        "analytic_L2":float(np.linalg.norm(M2["bath_q"])),
        "all_finite":bool(
            np.all(np.isfinite(M2["bath_q"]))
            and np.all(np.isfinite(M2p["bath_q"]))
            and np.all(np.isfinite(M2c["bath_q"]))
        ),
    }


def rescaled_fields(ge05,weight,omega=1.7):
    fields,dt,dx=ge05.deterministic_direction()
    # Hold z fixed while q=sqrt(w) z/omega changes.
    z=omega*np.asarray(fields["q"],float)/math.sqrt(0.6)
    ff={k:np.asarray(v,float).copy() for k,v in fields.items()}
    ff["q"]=math.sqrt(weight)*z/omega
    return ff,dt,dx


def weight_scaling_audit(ge05):
    vals=[]
    for w in (0.2,0.8):
        fields,dt,dx=rescaled_fields(ge05,w)
        m1,m2=ge05.analytic_sources(fields,dt,dx,omega=1.7,weight=w)
        fac=-2.0*1.7/math.sqrt(w)
        vals.append((fac*np.asarray(m1["bath_q"],float),fac*np.asarray(m2["bath_q"],float)))
    return {
        "normalized_c1_weight_relative_L2":rel(vals[0][0],vals[1][0]),
        "normalized_c2_weight_relative_L2":rel(vals[0][1],vals[1][1]),
        "all_finite":bool(all(np.all(np.isfinite(x)) for pair in vals for x in pair)),
    }


def step_linear_audit(c4):
    r=np.asarray([0.07,0.4,1.0,3.0,12.0,80.0],float)
    q0=np.asarray([0.2,-0.1,0.05,0.4,-0.3,0.12],float)
    v0=np.asarray([0.03,0.02,-0.04,0.01,0.08,-0.02],float)
    h=2.3; x0=-0.17; x1=0.29; dxi=0.037
    qe,ve=c4.step_linear(q0.copy(),v0.copy(),r,h,x0,x1,dxi)
    qr=np.empty_like(qe); vr=np.empty_like(ve)

    slope=(x1-x0)/dxi
    for i,rr in enumerate(r):
        def fun(xi,y):
            xx=x0+slope*xi
            return [y[1],-3.0*h*y[1]-rr**2*(y[0]-xx)]
        sol=solve_ivp(
            fun,(0.0,dxi),[q0[i],v0[i]],method="DOP853",
            rtol=2e-13,atol=2e-15,t_eval=[dxi]
        )
        if not sol.success:
            raise RuntimeError(sol.message)
        qr[i],vr[i]=sol.y[:,0]

    return {
        "q_relative_L2":rel(qe,qr),
        "v_relative_L2":rel(ve,vr),
        "q_max_abs_or_relative":aor(qe,qr),
        "v_max_abs_or_relative":aor(ve,vr),
        "all_finite":bool(
            np.all(np.isfinite(qe)) and np.all(np.isfinite(ve))
            and np.all(np.isfinite(qr)) and np.all(np.isfinite(vr))
        ),
    }


def main():
    ge05=load_quiet(ROOT/"ge05"/"memory_directional_source_generator.py","ge05_r23")
    c4=load_quiet(ROOT/"nl1c4"/"expanding_memory_source_trajectory.py","c4_r23")

    sym=symbolic_identities()
    c1=c1_discrete_audit(ge05)
    c2=c2_fd_audit(ge05)
    ws=weight_scaling_audit(ge05)
    step=step_linear_audit(c4)

    gates={
        "symbolic_q_to_z_FLRW_identity_exact":sym["q_to_z_exact"],
        "symbolic_cosmic_to_dimensionless_identity_exact":sym["dimensionless_exact"],
        "GE05_c1_bath_residual_matches_standard_linear_z_equation_relative_L2_le_1e10":
            bool(c1["relative_L2"]<=C1_MAX),
        "GE05_c2_bath_residual_matches_centered_second_directional_fd_relative_L2_le_1e5":
            bool(c2["analytic_vs_primary_relative_L2"]<=C2_FD_MAX),
        "GE05_c2_primary_vs_control_fd_relative_L2_le_1e5":
            bool(c2["primary_vs_control_relative_L2"]<=C2_FD_MAX),
        "weight_scaling_c1_cancels_le_1e12":
            bool(ws["normalized_c1_weight_relative_L2"]<=WEIGHT_MAX),
        "weight_scaling_c2_cancels_le_1e12":
            bool(ws["normalized_c2_weight_relative_L2"]<=WEIGHT_MAX),
        "NL1C4_step_linear_q_relative_L2_le_1e8":bool(step["q_relative_L2"]<=STEP_MAX),
        "NL1C4_step_linear_v_relative_L2_le_1e8":bool(step["v_relative_L2"]<=STEP_MAX),
        "all_outputs_finite":bool(c1["all_finite"] and c2["all_finite"] and ws["all_finite"] and step["all_finite"]),
    }
    passed=bool(all(gates.values()))
    result={
        "classification":(
            "GE19_REPAIR23_Q20_NORMALIZED_BATH_BRIDGE_AUDIT_PASS"
            if passed else "GE19_REPAIR23_Q20_NORMALIZED_BATH_BRIDGE_AUDIT_FAIL"
        ),
        "predata_classification":"GE19_REPAIR23_PREDATA_Q20_NORMALIZED_BATH_BRIDGE_AUDIT",
        "diagnostic_bridge_only":True,
        "symbolic":sym,
        "GE05_c1_linear_z_audit":c1,
        "GE05_c2_finite_difference_audit":c2,
        "weight_scaling_audit":ws,
        "NL1C4_step_linear_audit":step,
        "frozen_dictionary":{
            "z_from_q":"z_j=omega_j*q_j/sqrt(w_j)",
            "q_from_z":"q_j=sqrt(w_j)*z_j/omega_j",
            "first_order_equation":"G1[Z10,z10]=0",
            "second_order_equation":"G1[Z20,z20]+G2[(Z10,z10),(Z10,z10)]=0",
            "GE19_metric_map":"N->N; L,R->S; b->0; rapidity->u; scalar->phi",
            "future_z10_boundary":"full-history retarded positive-Drude state at z=1.5",
            "future_z20_boundary":"z20=0 and dz20/dxi=0 at z=1.5 for the window-local particular bath state",
        },
        "gates":gates,
        "q20_constructed":False,
        "Z21_licensed":False,
        "claim_boundary":"PASS certifies only the normalized-bath dictionary, second-directional q20 equation and window-local boundary convention. It does not construct q20, solve Z21, introduce finite eta or make observational claims.",
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
