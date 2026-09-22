#!/usr/bin/env python3
"""GE19 Repair30 — reduced H2/Z11 reclosure.

Solve the exact directional H2 equation

    L_total Z11 = -M1[Z10,q10]

on the same frozen reduced AeST+dust+Lambda operator used by Repair22.
Repair22 supplies Z10, Repair27 supplies the certified weighted q10 response,
and the Repair29B-certified R2 full-state tangent supplies only the inherited
finite-window boundary/reference. No H4/Z21 solve is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.repair07_window_retarded_reduced_h3_z20_particular as r7
import ge19.repair11_lambda_inclusive_reduced_h1_reclosure as r11
import ge19.repair13_self_consistent_reduced_background_h1_reclosure as r13
import ge19.repair28_cancellation_free_full_state_eta_tangent as r28

TINY=1e-300

R13_JSON_SHA="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
R13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
R22_JSON_SHA="7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
R22_NPZ_SHA="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
R27_JSON_SHA="99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b"
R27_NPZ_SHA="2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0"
R28_NPZ_SHA="101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705"
GE15_DENSE_SHA="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"

B_TIME_MAX=5e-3
LINEAR_MAX=1e-8
CONSTRAINT_MAX=1e-6
TIME_MAX=5e-3
INIT_MAX=1e-8
CHI_PARENT_MAX=5e-3
CHI_C_MAX=5e-3

DUST_RTOL=1e-11
DUST_ATOL=1e-13

R2_FIELDS=(
    "phi_newtonian","psi_newtonian","phi_prime_conformal",
    "delta_dark","theta_dark","alpha_aest","E_aest","alpha_prime_dy",
    "delta_b","theta_b","delta_m_native","theta_m_native",
    "total_delta_rho","total_rho_plus_p_theta",
    "total_delta_p","total_rho_plus_p_shear",
)


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def rel_l2(a,b)->float:
    aa=np.asarray(a); bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def aor(a,b)->float:
    aa=np.asarray(a); bb=np.asarray(b)
    ae=np.abs(aa-bb)
    re=ae/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),TINY)
    return float(np.max(np.minimum(ae,re)))


def interp_real(x0,y0,x):
    if np.array_equal(np.asarray(x0),np.asarray(x)):
        return np.asarray(y0,float).copy()
    return np.asarray(PchipInterpolator(x0,np.asarray(y0,float),axis=-1,extrapolate=False)(x),float)


def interp_complex(x0,y0,x):
    yy=np.asarray(y0,complex)
    if np.array_equal(np.asarray(x0),np.asarray(x)):
        return yy.copy()
    re=PchipInterpolator(x0,yy.real,axis=-1,extrapolate=False)(x)
    im=PchipInterpolator(x0,yy.imag,axis=-1,extrapolate=False)(x)
    return np.asarray(re+1j*im,complex)


def symbolic_m1_audit():
    N,L,R,b,rr=sp.symbols("N L R b rr", real=True)
    pt,px,qt,qx,q=sp.symbols("pt px qt qx q", real=True)
    om,sw=sp.symbols("om sw", positive=True, real=True)
    ch,sh=sp.cosh(rr),sp.sinh(rr)
    Aq=ch/N*(qt-b*qx)+sh/L*qx
    Xphi=sh/N*(pt-b*px)+ch/L*px
    lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)

    eps=sp.symbols("eps", real=True)
    a,Q,X,z,u=sp.symbols("a Q X z u", real=True)
    dN,dL,dR,db,dpt,dqt,dqx=sp.symbols("dN dL dR db dpt dqt dqx", real=True)
    dpx=a*(X-Q*u)
    dq=sw*z/om
    sub={
        N:1+eps*dN,L:a+eps*dL,R:a+eps*dR,b:eps*db,rr:eps*u,
        pt:Q+eps*dpt,px:eps*dpx,qt:eps*dqt,qx:eps*dqx,q:eps*dq,
    }
    cpx=sp.factor(sp.simplify(sp.diff(sp.expand(sp.diff(lag,px).subs(sub)),eps).subs(eps,0)))
    cr=sp.factor(sp.simplify(sp.diff(sp.expand(sp.diff(lag,rr).subs(sub)),eps).subs(eps,0)))
    exp_px=-a**2*sw**2*(X-z)/2
    exp_r=-Q*a**3*sw**2*(X-z)/2
    return {
        "partial_px_identity":bool(sp.simplify(cpx-exp_px)==0),
        "partial_r_identity":bool(sp.simplify(cr-exp_r)==0),
        "partial_px":str(cpx),
        "partial_r":str(cr),
        "expected_partial_px":str(exp_px),
        "expected_partial_r":str(exp_r),
    }


def build_backgrounds(dense:Path,r13npz):
    base128,state128,_=r7.build_ge15_reference(dense,128)
    base64,state64,_=r7.build_ge15_reference(dense,64)

    x64f=np.asarray(r13npz["x64"],float)
    rho64=np.asarray(r13npz["rho_lambda64"],float)
    if not np.array_equal(x64f,np.asarray(base64["x"],float)):
        raise RuntimeError("Repair13 x64 grid mismatch")
    rho_scale=max(float(np.max(np.abs(rho64))),TINY)
    rho_spread=float(np.max(np.abs(rho64-np.median(rho64)))/rho_scale)
    if rho_spread>1e-12:
        raise RuntimeError(f"rho_lambda is not constant at frozen precision: {rho_spread}")
    rhoL=float(np.median(rho64))

    bgs={}
    lambda_by_bg={}
    repro=0.0
    for nt,base in ((128,base128),(64,base64)):
        rho=np.full(len(base["x"]),rhoL,float)
        for tag in r7.C_TAGS:
            bg,_=r13.reduced_background(r7,base,tag,rho)
            bgs[(nt,tag)]=bg
            lambda_by_bg[id(bg)]=rho
            if nt==64:
                href=np.asarray(r13npz[f"{tag}_H_reduced_primary"],float)
                repro=max(repro,rel_l2(bg["H"],href))
    if repro>1e-12:
        raise RuntimeError(f"Repair13 reduced-background reproduction failed: {repro}")

    return bgs,{128:base128,64:base64},{128:state128,64:state64},lambda_by_bg,{
        "rho_lambda_constant":rhoL,
        "rho_lambda_relative_spread":rho_spread,
        "Repair13_H_Nt64_reproduction_relative_L2_max":repro,
    }


def load_r2_parent(npz:np.lib.npyio.NpzFile):
    x=np.asarray(npz["ln_a"],float)
    if not np.array_equal(x,np.asarray(r28.XGRID,float)):
        raise RuntimeError("Repair28 R2 ln(a) grid mismatch")
    if not np.array_equal(np.asarray(npz["k_Mpc"],float),np.asarray(r7.g9.K_REQ,float)):
        raise RuntimeError("Repair28 R2 k grid mismatch")
    fields={}
    for name in R2_FIELDS:
        key=f"R2_{name}_tangent_consensus"
        if key not in npz:
            raise RuntimeError(f"missing R2 tangent field {key}")
        fields[name]=np.asarray(npz[key],float)
    chi=np.asarray(npz["R2_chi11"],float)
    return x,fields,chi


def tangent_on_grid(x_parent,fields,x):
    return {k:interp_real(x_parent,v,x) for k,v in fields.items()}


def integrate_dust_tangent(bg,base_state,fields):
    """Pressureless reduced standard-sector eta tangent for each k.

    Initial absolute density/momentum tangent is inherited from the full
    standard sector; propagation uses the exact reduced pressureless tangent
    equations on the frozen reduced background.
    """
    x=np.asarray(bg["x"],float)
    a=np.asarray(bg["a"],float)
    H=np.asarray(bg["H"],float)
    calH=a*H
    out=[]

    rho_dark=np.asarray([q["rho_dark"] for q in base_state],float)
    p_dark=np.asarray([q["p_dark"] for q in base_state],float)

    expected=np.asarray(fields["delta_dark"],float).shape
    shape_map={
        "rho_dark":rho_dark.shape,
        "p_dark":p_dark.shape,
        "delta_dark":np.asarray(fields["delta_dark"],float).shape,
        "theta_dark":np.asarray(fields["theta_dark"],float).shape,
        "total_delta_rho":np.asarray(fields["total_delta_rho"],float).shape,
        "total_rho_plus_p_theta":np.asarray(fields["total_rho_plus_p_theta"],float).shape,
    }
    if expected!=(len(r7.FOURIER_N),len(bg["x"])) or any(v!=expected for v in shape_map.values()):
        raise RuntimeError(f"standard-sector tangent shape mismatch: expected={expected} shapes={shape_map}")

    std_dr=fields["total_delta_rho"]-rho_dark*fields["delta_dark"]
    std_mom=fields["total_rho_plus_p_theta"]-(rho_dark+p_dark)*fields["theta_dark"]
    if std_dr.shape!=expected or std_mom.shape!=expected:
        raise RuntimeError(
            f"standard-sector tangent output shape mismatch: dr={std_dr.shape} mom={std_mom.shape} expected={expected}"
        )

    phi_interp=[
        PchipInterpolator(x,fields["phi_newtonian"][ik],extrapolate=False)
        for ik in range(len(r7.FOURIER_N))
    ]
    psi_interp=[
        PchipInterpolator(x,fields["psi_newtonian"][ik],extrapolate=False)
        for ik in range(len(r7.FOURIER_N))
    ]
    H_interp=PchipInterpolator(x,H,extrapolate=False)
    a_interp=lambda xx: math.exp(float(xx))

    C=float(r7.C_VALUES["_PLACEHOLDER_"]) if False else None
    for ik,k in enumerate(r7.g9.K_REQ):
        # bg already carries the frozen dust action density rho_dust_action=C/a^3.
        rho0=float(np.asarray(bg["rho_dust_action"],float)[0])
        d0=float(std_dr[ik,0]/rho0)
        t0=float(std_mom[ik,0]/rho0)

        def rhs(xx,y):
            aa=a_interp(xx)
            hh=float(H_interp(xx))
            hc=aa*hh
            phix=float(phi_interp[ik].derivative()(xx))
            psi=float(psi_interp[ik](xx))
            delta,theta=y
            return np.asarray([
                -theta/hc+3.0*phix,
                -theta+(float(k)*float(k)/hc)*psi,
            ],float)

        sol=solve_ivp(
            rhs,(float(x[0]),float(x[-1])),[d0,t0],
            t_eval=x,method="DOP853",rtol=DUST_RTOL,atol=DUST_ATOL,
        )
        if not sol.success:
            raise RuntimeError(f"dust tangent integration failed k={k}: {sol.message}")
        out.append({
            "delta":np.asarray(sol.y[0],float),
            "theta":np.asarray(sol.y[1],float),
            "std_delta_rho_initial":float(std_dr[ik,0]),
            "std_momentum_initial":float(std_mom[ik,0]),
            "rho0":rho0,
        })
    return out,std_dr,std_mom


def make_reference(bg,base_bg,fields,dust):
    """Map the R2 tangent onto frozen reduced complex +m coefficients."""
    nt=len(bg["x"])
    amps,_,_=r7.amplitudes()
    state=np.zeros((len(r7.FOURIER_N),6,nt),complex)
    dots=np.zeros((len(r7.FOURIER_N),4,nt),complex)
    zero=np.zeros(nt,float)
    x=np.asarray(bg["x"],float)
    a=np.asarray(bg["a"],float)
    H=np.asarray(bg["H"],float)
    Q=np.asarray(bg["Q_action"],float)

    for ik,m in enumerate(r7.FOURIER_N):
        k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
        amp=float(amps[ik]); ph=float(r7.PHASES[ik])

        N=fields["psi_newtonian"][ik]
        S=-a*fields["phi_newtonian"][ik]
        us=-(k/a)*fields["alpha_aest"][ik]
        varphi=Q*a*fields["theta_dark"][ik]/(k*k)
        T=a*dust[ik]["theta"]/(k*k)
        dr=3.0*np.asarray(bg["rho_dust_action"],float)*dust[ik]["delta"]

        raw=(N,S,us,varphi,T,dr)
        state[ik,0]=r7.positive_mode_coeff(N,zero,amp,ph)
        state[ik,1]=r7.positive_mode_coeff(S,zero,amp,ph)
        state[ik,2]=r7.positive_mode_coeff(zero,us,amp,ph)
        state[ik,3]=r7.positive_mode_coeff(varphi,zero,amp,ph)
        state[ik,4]=r7.positive_mode_coeff(T,zero,amp,ph)
        state[ik,5]=r7.positive_mode_coeff(dr,zero,amp,ph)

        # Boundary trajectory derivatives are d/dt_red = H_red d/d ln(a).
        dyn_raw=[S,us,varphi,T]
        for jd,q in enumerate(dyn_raw):
            if jd==3:
                # Exact pressureless identity Tdot=psi for the reduced tangent.
                qdot=N
            else:
                dqdx=np.asarray(PchipInterpolator(x,q,extrapolate=False).derivative()(x),float)
                qdot=H*dqdx
            if jd==1:
                dots[ik,jd]=r7.positive_mode_coeff(zero,qdot,amp,ph)
            else:
                dots[ik,jd]=r7.positive_mode_coeff(qdot,zero,amp,ph)

    return state,dots


def first_order_X(bg,h1):
    st=np.asarray(h1,complex)
    out=np.empty((len(r7.FOURIER_N),st.shape[-1]),complex)
    for im,m in enumerate(r7.FOURIER_N):
        k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
        out[im]=bg["Q_action"]*st[im,2]+(1j*k/bg["a"])*st[im,3]
    return out


def source_from_B(bg,B):
    """Exact -M1 RHS after normalized bath summation.

    main row order: lapse,isotropic,aether,scalar,dust-potential,dust-density.
    """
    B=np.asarray(B,complex)
    rhs=np.zeros((len(r7.FOURIER_N),6,B.shape[-1]),complex)
    for im,m in enumerate(r7.FOURIER_N):
        k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
        rhs[im,2]=0.5*bg["Q_action"]*bg["a"]**3*B[im]
        rhs[im,3]=-0.5*bg["a"]**2*(1j*k)*B[im]
    return rhs


def source_interp(x,rhs_mode):
    arr=np.asarray(rhs_mode,complex)
    re=PchipInterpolator(x,arr.real,axis=-1,extrapolate=False)
    im=PchipInterpolator(x,arr.imag,axis=-1,extrapolate=False)
    def rf(xq):
        return np.asarray(re(xq)+1j*im(xq),complex)[:,None]
    def cf(xq):
        return np.zeros((2,1),complex)
    return rf,cf


def solve_h2_case(mod6,mod7,bg,tag,source,reference,reference_dot):
    nt=len(bg["x"])
    state=np.empty((len(r7.FOURIER_N),6,nt),complex)
    dots=np.empty((len(r7.FOURIER_N),4,nt),complex)
    lin=[]; shift=[]; aniso=[]; init=[]; algebraic_init=[]; march=[]

    for ik,m in enumerate(r7.FOURIER_N):
        k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
        rhsfun,confun=source_interp(np.asarray(bg["x"],float),source[ik])
        rhs0=np.asarray(rhsfun(float(bg["x"][0]))[:,0],complex)
        q0=np.asarray(reference[ik,[1,2,3,4],0],complex)
        v0=np.asarray(reference_dot[ik,:,0],complex)
        y0,w0,idiag=r7._initial_canonical_state(
            mod6,mod7,bg,tag,k,float(bg["x"][0]),q0,v0,rhs0
        )
        Y,rdiag=r7._radau2_integrate_canonical(
            mod6,mod7,bg,tag,k,y0[:,None],rhsfun,confun
        )
        st,dd,odiag=r7._reconstruct_canonical_solution(
            mod6,mod7,bg,tag,k,Y,rhsfun,confun
        )
        state[ik]=st[0]; dots[ik]=dd[0]

        lin.append(max(
            idiag["initial_algebraic_scaled_residual"],
            rdiag["radau_block_scaled_relative_L2_residual_max"],
            odiag["algebraic_scaled_relative_L2_residual_max"],
            odiag["lapse_noether_row_relative_residual_max"],
        ))
        shift.append(odiag["shift_constraint_relative_L2_max"])
        aniso.append(odiag["anisotropy_constraint_relative_L2_max"])
        for j in range(4):
            init.append(aor([state[ik,j+1,0]],[q0[j]]))
            init.append(aor([dots[ik,j,0]],[v0[j]]))
        algebraic_init.append(aor(state[ik,[0,5],0],reference[ik,[0,5],0]))
        march.append({"m":int(m),**idiag,**rdiag,**odiag})

    return state,dots,{
        "linear_system_relative_L2_max":float(max(lin,default=math.inf)),
        "shift_constraint_relative_L2_max":float(max(shift,default=math.inf)),
        "anisotropy_constraint_relative_L2_max":float(max(aniso,default=math.inf)),
        "initial_dynamic_boundary_abs_or_rel_max":float(max(init,default=math.inf)),
        "initial_algebraic_reference_abs_or_rel_max_report_only":float(max(algebraic_init,default=math.inf)),
        "all_outputs_finite":bool(np.all(np.isfinite(state)) and np.all(np.isfinite(dots))),
        "canonical_march_diagnostics":march,
    }


def state_time_control(xp,sp,xc,sc):
    si=interp_complex(xp,sp,xc)
    by={}
    mx=0.0
    for iv,name in enumerate(r7.FIELDS):
        e=rel_l2(si[:,iv,:],sc[:,iv,:])
        by[name]=e; mx=max(mx,e)
    return {"by_field_relative_L2":by,"max":float(mx)}


def chi_from_state(bg,state):
    out=np.empty((len(r7.FOURIER_N),state.shape[-1]),complex)
    for im,m in enumerate(r7.FOURIER_N):
        k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
        out[im]=state[im,3]-1j*(bg["Q_action"]*bg["a"]/k)*state[im,2]
    return out


def full_parent_chi_positive(chi_raw):
    amps,_,_=r7.amplitudes()
    out=np.empty_like(np.asarray(chi_raw,float),dtype=complex)
    z=np.zeros(chi_raw.shape[-1],float)
    for ik in range(len(r7.FOURIER_N)):
        out[ik]=r7.positive_mode_coeff(
            np.asarray(chi_raw[ik],float),z,float(amps[ik]),float(r7.PHASES[ik])
        )
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--repair28-npz",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    rd=Path(args.results_dir)
    paths={
        "dense":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "r13j":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "r22j":rd/"ge19_repair22_on_shell_parent_z20_certification.json",
        "r22n":rd/"ge19_repair22_on_shell_parent_z20_certification.npz",
        "r27j":rd/"ge19_repair27_cancellation_free_parent_q20_reconstruction.json",
        "r27n":rd/"ge19_repair27_cancellation_free_parent_q20_reconstruction.npz",
        "r28n":Path(args.repair28_npz),
    }
    missing=[str(p) for p in paths.values() if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen Repair30 inputs: "+", ".join(missing))

    expected={
        "dense":GE15_DENSE_SHA,
        "r13j":R13_JSON_SHA,"r13n":R13_NPZ_SHA,
        "r22j":R22_JSON_SHA,"r22n":R22_NPZ_SHA,
        "r27j":R27_JSON_SHA,"r27n":R27_NPZ_SHA,
        "r28n":R28_NPZ_SHA,
    }
    hashes={}
    for key,h in expected.items():
        got=sha256(paths[key]); hashes[key]=got
        if got!=h:
            raise RuntimeError(f"{key} hash mismatch: {got} != {h}")

    d13=json.loads(paths["r13j"].read_text())
    d22=json.loads(paths["r22j"].read_text())
    d27=json.loads(paths["r27j"].read_text())
    if d13.get("classification")!="GE19_REPAIR13_SELF_CONSISTENT_REDUCED_BACKGROUND_H1_RECLOSURE_PASS":
        raise RuntimeError("Repair13 parent not PASS")
    if d22.get("classification")!="GE19_REPAIR22_ON_SHELL_PARENT_Z20_CERTIFICATION_PASS" or d22.get("Z20_certified") is not True:
        raise RuntimeError("Repair22 parent not certified")
    if d27.get("classification")!="GE19_REPAIR27_CANCELLATION_FREE_PARENT_Q20_RECONSTRUCTION_PASS":
        raise RuntimeError("Repair27 parent not PASS")

    sym=symbolic_m1_audit()
    if not (sym["partial_px_identity"] and sym["partial_r_identity"]):
        raise RuntimeError(f"GE05 normalized M1 symbolic reduction failed: {sym}")

    z13=np.load(paths["r13n"])
    z22=np.load(paths["r22n"])
    z27=np.load(paths["r27n"])
    z28=np.load(paths["r28n"])

    bgs,bases,base_states,lambda_by_bg,bgdiag=build_backgrounds(paths["dense"],z13)
    r11.install_lambda_operator(r7,lambda_by_bg)

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r30"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r30"
    )

    # Exact grid binding to Repair22.
    if not np.array_equal(np.asarray(z22["x_primary"],float),np.asarray(bases[128]["x"],float)):
        raise RuntimeError("Repair22 primary x grid mismatch")
    if not np.array_equal(np.asarray(z22["x_control"],float),np.asarray(bases[64]["x"],float)):
        raise RuntimeError("Repair22 control x grid mismatch")

    xR2,R2,chiR2=load_r2_parent(z28)
    parent_chi_pos=full_parent_chi_positive(chiR2)

    state={}; dots={}; refs={}; refdots={}; B10={}; source={}
    solve_rows=[]; time_rows=[]; chi_rows=[]; save={}
    btime=0.0; sysmax=0.0; shiftmax=0.0; anisomax=0.0; initmax=0.0; timemax=0.0
    chiparent=0.0; finite=True

    for nt,label,wkey in (
        (128,"primary","weighted_z10_primary"),
        (64,"control","weighted_z10_time_control"),
    ):
        x=np.asarray(bases[nt]["x"],float)
        fields=tangent_on_grid(xR2,R2,x)
        for tag in r7.C_TAGS:
            bg=bgs[(nt,tag)]
            dust,std_dr,std_mom=integrate_dust_tangent(bg,base_states[nt],fields)
            ref,refdot=make_reference(bg,bases[nt],fields,dust)
            refs[(nt,tag)]=ref; refdots[(nt,tag)]=refdot

            h1=np.asarray(z22[f"{tag}_H1_{label}"],complex)
            X=first_order_X(bg,h1)
            wz=np.asarray(z27[f"{tag}_{wkey}"],complex)
            if wz.shape!=X.shape:
                raise RuntimeError(f"weighted z10 shape mismatch Nt={nt} C={tag}: {wz.shape} vs {X.shape}")
            B=X-wz
            B10[(nt,tag)]=B
            source[(nt,tag)]=source_from_B(bg,B)

            st,dd,diag=solve_h2_case(
                mod6,mod7,bg,tag,source[(nt,tag)],ref,refdot
            )
            state[(nt,tag)]=st; dots[(nt,tag)]=dd
            solve_rows.append({"Nt":nt,"C":tag,**diag})
            sysmax=max(sysmax,diag["linear_system_relative_L2_max"])
            shiftmax=max(shiftmax,diag["shift_constraint_relative_L2_max"])
            anisomax=max(anisomax,diag["anisotropy_constraint_relative_L2_max"])
            initmax=max(initmax,diag["initial_dynamic_boundary_abs_or_rel_max"])
            finite=bool(finite and diag["all_outputs_finite"])

            save[f"{tag}_Z11_{label}"]=st
            save[f"{tag}_Z11dot_{label}"]=dd
            save[f"{tag}_B10_{label}"]=B
            save[f"{tag}_M1_rhs_{label}"]=source[(nt,tag)]
            save[f"{tag}_Z11_reference_{label}"]=ref

    # Primary/control source and state convergence.
    x128=np.asarray(bases[128]["x"],float)
    x64=np.asarray(bases[64]["x"],float)
    for tag in r7.C_TAGS:
        bi=interp_complex(x128,B10[(128,tag)],x64)
        eb=rel_l2(bi,B10[(64,tag)])
        btime=max(btime,eb)

        tc=state_time_control(x128,state[(128,tag)],x64,state[(64,tag)])
        time_rows.append({"C":tag,**tc})
        timemax=max(timemax,tc["max"])

        chi=chi_from_state(bgs[(128,tag)],state[(128,tag)])
        ep=rel_l2(chi,parent_chi_pos)
        chiparent=max(chiparent,ep)
        chi_rows.append({"C":tag,"reduced_chi11_vs_R2_parent_relative_L2":ep})
        save[f"{tag}_chi11_primary"]=chi

    # C-envelope spread around C_star.
    chi_star=chi_from_state(bgs[(128,"C_star")],state[(128,"C_star")])
    cspread=0.0
    crows=[]
    for tag in ("C_min","C_max"):
        ch=chi_from_state(bgs[(128,tag)],state[(128,tag)])
        e=rel_l2(ch,chi_star)
        cspread=max(cspread,e)
        crows.append({"C":tag,"relative_L2_vs_C_star":e})

    gates={
        "parent_hashes_exact":True,
        "GE05_normalized_M1_symbolic_identity_exact":bool(sym["partial_px_identity"] and sym["partial_r_identity"]),
        "Repair27_B10_primary_vs_time_control_relative_L2_le_5e3":bool(btime<=B_TIME_MAX),
        "linear_system_relative_L2_residual_le_1e8":bool(sysmax<=LINEAR_MAX),
        "shift_constraint_backward_error_le_1e6":bool(shiftmax<=CONSTRAINT_MAX),
        "anisotropy_constraint_backward_error_le_1e6":bool(anisomax<=CONSTRAINT_MAX),
        "primary128_vs_control64_Z11_state_relative_L2_le_5e3":bool(timemax<=TIME_MAX),
        "initial_dynamic_boundary_abs_or_rel_le_1e8":bool(initmax<=INIT_MAX),
        "reduced_chi11_vs_R2_parent_relative_L2_le_5e3":bool(chiparent<=CHI_PARENT_MAX),
        "reduced_chi11_C_envelope_relative_L2_le_5e3":bool(cspread<=CHI_C_MAX),
        "all_outputs_finite":bool(finite),
    }
    passed=bool(all(gates.values()))

    report={
        "classification":(
            "GE19_REPAIR30_REDUCED_H2_Z11_RECLOSURE_PASS"
            if passed else
            "GE19_REPAIR30_REDUCED_H2_Z11_RECLOSURE_FAIL"
        ),
        "predata_classification":"GE19_REPAIR30_PREDATA_REDUCED_H2_Z11_RECLOSURE",
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "H4_Z21_solve_performed":False,
        "provenance":{
            "input_sha256":hashes,
            "Repair29B_certified_parent":"R2 primary complete eta-tangent representation with targeted R3 numerical control",
            "Repair28_relabelled":False,
        },
        "H2_equation":"L_total Z11 = -M1[Z10,q10]",
        "normalized_M1_symbolic_audit":sym,
        "background_control":bgdiag,
        "memory_source_control":{
            "B10_definition":"X10-weighted_z10",
            "B10_primary_vs_time_control_relative_L2_max":btime,
            "M1_direct_metric_source_zero":True,
            "M1_dust_source_zero":True,
        },
        "solve_controls":{
            "linear_system_relative_L2_max":sysmax,
            "shift_constraint_relative_L2_max":shiftmax,
            "anisotropy_constraint_relative_L2_max":anisomax,
            "initial_dynamic_boundary_abs_or_rel_max":initmax,
            "primary128_vs_control64_state_relative_L2_max":timemax,
            "per_case":solve_rows,
            "time_control":time_rows,
        },
        "chi11_controls":{
            "reduced_vs_Repair29B_R2_parent_relative_L2_max":chiparent,
            "per_C":chi_rows,
            "C_envelope_relative_L2_max":cspread,
            "C_envelope":crows,
        },
        "gates":gates,
        "Z11_constructed":True,
        "Z11_certified":passed,
        "routing":{
            "next_route":(
                "REDUCED_Z11_CERTIFIED_H4_Z21_LICENSED"
                if passed else
                "REDUCED_Z11_RECLOSURE_FAIL_H4_Z21_BLOCKED"
            ),
            "H4_Z21_licensed":passed,
        },
        "claim_boundary":"Repair30 certifies only the reduced first-order eta tangent Z11 on the frozen late-time scalar/AeST/pressureless-dust reduction. It does not solve H4/Z21, introduce finite eta, certify full-species nonlinear evolution, lensing, or observations.",
    }

    outj=Path(args.json_out); outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    save["x_primary"]=x128
    save["x_control"]=x64
    save["R2_parent_chi11_positive"]=parent_chi_pos
    np.savez_compressed(outn,**save)

    print(json.dumps(report,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR30_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Z11_certified":False,
            "H4_Z21_solve_performed":False,
        },indent=2))
        raise
