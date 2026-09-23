#!/usr/bin/env python3
"""GE19 Repair36 — Lambda-complete reduced H4/Z21 reclosure.

Construct

  L_GE06 Z21 =
      -2 Q_total(Z10,Z11)
      -2 DY2[Z10;Z11]
      -2 M1_GE05[Z20,q20]
      -2 M2_GE05[(Z10,q10),(Z10,q10)]

with all GE05 memory residuals mapped into the common GE06 raw-residual
convention by the exact factor two derived in Repair32A.

The solve is a window-local particular state with zero homogeneous H4
boundary at a=0.4. It does not select a primordial Z21 mode.
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
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.repair07_window_retarded_reduced_h3_z20_particular as r7
import ge19.repair11_lambda_inclusive_reduced_h1_reclosure as r11
import ge19.repair13_self_consistent_reduced_background_h1_reclosure as r13
import ge19.repair14_self_consistent_reduced_h3_z20_particular as r14
import ge19.repair24_q20_construction as r24
import ge19.repair27_cancellation_free_parent_q20_reconstruction as r27
import ge19.repair18_zero_coordinate_constraint_projected_momentum_boundary as r18
import nl1c4.expanding_memory_source_trajectory as c4

TINY=1e-300
EPS=float(np.finfo(float).eps)
SQRT_EPS=float(np.sqrt(EPS))
ORDER_MIN=2.5
NEAR_NULL_RATIO_MAX=1000.0*EPS

# Frozen parent hashes.
R13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
R22_JSON_SHA="7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
R22_NPZ_SHA="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
R27_JSON_SHA="99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b"
R27_NPZ_SHA="2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0"
R32B_JSON_SHA="226dd2a2a0e86ddccc39a62d833960bdf9d5a9af038ad3bf225bbbf69d0b95cf"
R32B_NPZ_SHA="5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327"
R32C_JSON_SHA="037314effa33c5bfaf51f6f3c72459de43cb486c6ef5e9a94f5b1984a68611b9"
GE15_DENSE_SHA="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"
REPAIR26_TRACE_SHA=r27.REPAIR26_R1_TRACE_SHA
REPAIR26_TRACE_BYTES=r27.REPAIR26_R1_TRACE_BYTES

# Frozen Repair33 numerics.
NT_PRIMARY=128
NT_CONTROL=64
NX_POLY=128          # exact for polynomial blocks with max generated mode 40
NX_DY_PRIMARY=1024
NX_DY_CONTROL=2048
NQ_PRIMARY=2048
NQ_CONTROL=1024
M_MAX=40
GE05_TO_GE06=2.0

Q_SYMMETRY_MAX=1e-12
DY_SPATIAL_MAX=5e-4
TOTAL_SPATIAL_MAX=5e-4
MEMORY_QUAD_MAX=1e-2
SOURCE_TIME_MAX=5e-3
LINEAR_MAX=1e-8
STATE_TIME_MAX=5e-3
CONSTRAINT_MAX=1e-6
BOUNDARY_MAX=1e-12

COMPONENTS=(
    "2Q_GE06_cross",
    "2Q_GE07_cross",
    "2Q_Lambda_cross",
    "2DY2",
    "2M1_GE05_mapped",
    "2M2_GE05_mapped",
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

def interp_complex_axis(x0,y0,x,axis):
    yy=np.asarray(y0,complex)
    re=PchipInterpolator(x0,yy.real,axis=axis,extrapolate=False)(x)
    im=PchipInterpolator(x0,yy.imag,axis=axis,extrapolate=False)(x)
    return np.asarray(re+1j*im,complex)

def reconstruct_general(coeff,modes,nx):
    """Positive Fourier coeff [...,mode,time] -> real [...,time,x]."""
    cc=np.asarray(coeff,complex)
    modes=np.asarray(modes,int)
    theta=2*np.pi*np.arange(nx,dtype=float)/nx
    basis=np.exp(1j*modes[:,None]*theta[None,:])
    return 2.0*np.real(np.einsum("...mt,mx->...tx",cc,basis,optimize=True))

def fft_low(arr,mmax=M_MAX):
    aa=np.asarray(arr,float)
    hh=np.fft.fft(aa,axis=-1)/aa.shape[-1]
    return np.asarray(hh[...,:mmax+1],complex)

def load_parents(rd:Path,args):
    paths={
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "r22j":rd/"ge19_repair22_on_shell_parent_z20_certification.json",
        "r22n":rd/"ge19_repair22_on_shell_parent_z20_certification.npz",
        "r27j":rd/"ge19_repair27_cancellation_free_parent_q20_reconstruction.json",
        "r27n":rd/"ge19_repair27_cancellation_free_parent_q20_reconstruction.npz",
        "r32bj":rd/"ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.json",
        "r32bn":rd/"ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.npz",
        "r32cj":rd/"ge19_repair32c_artifact_only_reduced_z11_certification.json",
        "dense":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "trace":Path(args.repair26_trace),
    }
    missing=[str(v) for v in paths.values() if not v.exists()]
    if missing:
        raise RuntimeError("missing Repair36 frozen inputs: "+", ".join(missing))
    expected={
        "r13n":R13_NPZ_SHA,"r22j":R22_JSON_SHA,"r22n":R22_NPZ_SHA,
        "r27j":R27_JSON_SHA,"r27n":R27_NPZ_SHA,
        "r32bj":R32B_JSON_SHA,"r32bn":R32B_NPZ_SHA,
        "r32cj":R32C_JSON_SHA,"dense":GE15_DENSE_SHA,"trace":REPAIR26_TRACE_SHA,
    }
    hashes={}
    for k,h in expected.items():
        got=sha256(paths[k]); hashes[k]=got
        if got!=h:
            raise RuntimeError(f"{k} hash mismatch: {got} != {h}")
    if paths["trace"].stat().st_size!=REPAIR26_TRACE_BYTES:
        raise RuntimeError("Repair26 trace byte mismatch")

    j22=json.loads(paths["r22j"].read_text())
    j27=json.loads(paths["r27j"].read_text())
    j32b=json.loads(paths["r32bj"].read_text())
    j32c=json.loads(paths["r32cj"].read_text())
    if j22.get("classification")!="GE19_REPAIR22_ON_SHELL_PARENT_Z20_CERTIFICATION_PASS" or j22.get("Z20_certified") is not True:
        raise RuntimeError("Repair22 Z20 parent not certified")
    if j27.get("classification")!="GE19_REPAIR27_CANCELLATION_FREE_PARENT_Q20_RECONSTRUCTION_PASS" or j27.get("q20_certified_projection") is not True:
        raise RuntimeError("Repair27 q20 parent not certified")
    if j32b.get("classification")!="GE19_REPAIR32B_FACTOR2_CORRECTED_REDUCED_H2_Z11_RECONSTRUCTION_PASS":
        raise RuntimeError("Repair32B parent not PASS")
    if j32c.get("classification")!="GE19_REPAIR32C_ARTIFACT_ONLY_REDUCED_Z11_CERTIFICATION_PASS":
        raise RuntimeError("Repair32C parent not PASS")
    if j32c.get("Z11_certified") is not True or j32c.get("routing",{}).get("H4_Z21_licensed") is not True:
        raise RuntimeError("Repair32C did not license H4/Z21")

    return paths,hashes,np.load(paths["r13n"]),np.load(paths["r22n"]),np.load(paths["r27n"]),np.load(paths["r32bn"])

def build_context(rd,r13npz):
    r24.TRACE_LO_A=r27.REPAIR26_TRACE_LO_A
    r24.TRACE_HI_A=r27.REPAIR26_TRACE_HI_A
    bgs,bgctl=r24.reconstruct_backgrounds(r7,r11,r13,rd,r13npz)

    # Restore the exact frozen Repair11 Lambda-inclusive first-directional
    # operator on every Repair13 background before any canonical H4 solve.
    lambda_by_bg={}
    for key,bg in bgs.items():
        rho=np.asarray(bg["rho_lambda_action"],float)
        if rho.shape!=np.asarray(bg["x"],float).shape or not np.all(np.isfinite(rho)):
            raise RuntimeError(f"invalid Repair13 rho_lambda_action for background {key}")
        lambda_by_bg[id(bg)]=rho
    lambda_diag=r11.install_lambda_operator(r7,lambda_by_bg)

    mod6f=r7.load_frozen_generator(ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r36")
    mod6=r7.build_stable_ge06_generator_v2(mod6f)
    mod7=r7.load_frozen_generator(ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r36")
    ge05=r7.load_frozen_generator(ROOT/"ge05/memory_directional_source_generator.py","ge05r36")
    normf,normdiag=r24.build_normalized_c2_generator(ge05)
    qdirect=build_direct_bilinear_generators(mod6f,mod6,mod7)
    return bgs,bgctl,mod6,mod7,ge05,normf,normdiag,qdirect,lambda_diag

def _bilinear_fnmap(exprs,args,dir_start,dir_count,prefix):
    """Build exact mixed bilinear local-partial evaluators from frozen Q2."""
    args=tuple(args)
    dirs=args[dir_start:dir_start+dir_count]
    es=sp.symbols(f"{prefix}0:{dir_count}",real=True)
    fmap={}
    identities={}
    for key,expr in exprs.items():
        bil=sp.factor_terms(sp.cancel(sp.expand(
            sp.Rational(1,2)*sum(sp.diff(expr,d)*e for d,e in zip(dirs,es))
        )))
        plus=expr.xreplace({d:d+e for d,e in zip(dirs,es)})
        minus=expr.xreplace({d:d-e for d,e in zip(dirs,es)})
        pol=sp.cancel(sp.expand((plus-minus)/4))
        identities[key]=bool(sp.simplify(sp.cancel(sp.expand(bil-pol)))==0)
        fmap[key]=sp.lambdify((*args,*es),bil,"numpy",cse=False)
    return fmap,identities


def build_direct_bilinear_generators(mod6f,mod6,mod7):
    stable_args=(
        mod6f.direction_args[0],
        mod6f.direction_args[1],
        mod6.Zb_symbol,
        *mod6f.direction_args[3:],
    )
    f6,id6=_bilinear_fnmap(
        mod6.coeff2_expr,stable_args,3,15,"ge06e"
    )
    f7,id7=_bilinear_fnmap(
        mod7.coeff2,tuple(mod7.direction_args),2,7,"ge07e"
    )
    exact=bool(all(id6.values()) and all(id7.values()))
    if not exact:
        bad6=[k for k,v in id6.items() if not v]
        bad7=[k for k,v in id7.items() if not v]
        raise RuntimeError(
            f"direct bilinear symbolic polarization identity failed GE06={bad6} GE07={bad7}"
        )
    return {
        "ge06":f6,
        "ge07":f7,
        "GE06_identity_by_partial":id6,
        "GE07_identity_by_partial":id7,
        "all_symbolic_polarization_identities_exact":exact,
    }


def _direct_cross_locals(bg,state,dot,nx):
    real,rdot,spatial=r7.reduced_state_real(bg,state,nx,dot)
    return real,rdot,spatial


def q_cross_direct(qdirect,bg,tag,z10,d10,z11,d11,nx):
    """Exact GE06/GE07 mixed bilinear Q(Z10,Z11), no subtraction."""
    r0,t0,x0=_direct_cross_locals(bg,z10,d10,nx)
    r1,t1,x1=_direct_cross_locals(bg,z11,d11,nx)

    N0=r0["N20"]; S0=r0["S20"]; u0=r0["u20"]; ph0=r0["phi20"]
    T0=r0["T20"]; dr0=r0["delta_varrho20"]
    N1=r1["N20"]; S1=r1["S20"]; u1=r1["u20"]; ph1=r1["phi20"]
    T1=r1["T20"]; dr1=r1["delta_varrho20"]

    z0=np.zeros_like(N0); z1=np.zeros_like(N1)
    aa=bg["a"][:,None]
    adot=(bg["a"]*bg["H"])[:,None]
    Zb=bg["Z_action"][:,None]

    vals6=(
        aa,adot,Zb,
        N0,S0,S0,z0,u0,
        t0["S20"],x0["S20"],
        t0["S20"],x0["S20"],z0,
        t0["u20"],x0["u20"],
        t0["phi20"],x0["phi20"],x0["N20"],
        r7.KB,r7.CV,r7.K2,r7.Q0,r7.Z0,
    )
    e6=(
        N1,S1,S1,z1,u1,
        t1["S20"],x1["S20"],
        t1["S20"],x1["S20"],z1,
        t1["u20"],x1["u20"],
        t1["phi20"],x1["phi20"],x1["N20"],
    )
    p6={}
    for name,fn in qdirect["ge06"].items():
        v=np.broadcast_to(np.asarray(fn(*vals6,*e6)),N0.shape).copy()
        if not np.all(np.isfinite(v)):
            raise RuntimeError(f"nonfinite direct GE06 bilinear partial {name}")
        p6[name]=v

    Dx=r7.fd4_matrix(len(bg["x"]),bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    g=r7.assemble_ga_local(
        p6,Dt,spatial_real=True,
        kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    )

    rhob=(3.0*r7.C_VALUES[tag]/bg["a"]**3)[:,None]
    vals7=(aa,rhob,N0,S0,S0,z0,dr0,t0["T20"],x0["T20"])
    e7=(N1,S1,S1,z1,dr1,t1["T20"],x1["T20"])
    p7={}
    for name,fn in qdirect["ge07"].items():
        v=np.broadcast_to(np.asarray(fn(*vals7,*e7)),N0.shape).copy()
        if not np.all(np.isfinite(v)):
            raise RuntimeError(f"nonfinite direct GE07 bilinear partial {name}")
        p7[name]=v
    m=r7.assemble_m_local(
        p7,Dt,spatial_real=True,
        kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    )

    zma={k:np.zeros_like(v) for k,v in m.items()}
    zga={k:np.zeros_like(v) for k,v in g.items()}
    gm,gc=r7.main_and_constraints(g,zma)
    mm,mc=r7.main_and_constraints(zga,m)
    return gm,gc,mm,mc


def lambda_cross_direct(bg,z10,d10,z11,d11,nx):
    """Exact Repair14 mixed Lambda coefficient B_lambda(Z10,Z11).

    Repair14 froze the common-direction second coefficient
      Q_N   = -36 rho_lambda a S^2
      Q_iso = -72 rho_lambda a N S - 36 rho_lambda S^2.
    This routine evaluates the exact symmetric bilinear coefficient directly
    and audits it against exact quadratic polarization.
    """
    r0,_,_=r7.reduced_state_real(bg,z10,nx,d10)
    r1,_,_=r7.reduced_state_real(bg,z11,nx,d11)
    N0=np.asarray(r0["N20"],float); S0=np.asarray(r0["S20"],float)
    N1=np.asarray(r1["N20"],float); S1=np.asarray(r1["S20"],float)
    aa=np.asarray(bg["a"],float)[:,None]
    rr=np.asarray(bg["rho_lambda_action"],float)[:,None]
    shape=N0.shape
    if any(q.shape!=shape for q in (S0,N1,S1)) or aa.shape[0]!=shape[0]:
        raise RuntimeError("Lambda mixed source shape mismatch")

    main=np.zeros((6,)+shape,float)
    main[0]=-36.0*rr*aa*S0*S1
    main[1]=(
        -36.0*rr*aa*(N0*S1+N1*S0)
        -36.0*rr*S0*S1
    )
    con=np.zeros((2,)+shape,float)

    # Exact frozen Repair14 common-direction source polarization audit.
    rp={"N20":N0+N1,"S20":S0+S1}
    rm={"N20":N0-N1,"S20":S0-S1}
    qp=r14.lambda_c2_equation_source(bg,bg["rho_lambda_action"],rp)
    qm=r14.lambda_c2_equation_source(bg,bg["rho_lambda_action"],rm)
    pol=0.25*(qp-qm)
    polerr=rel_l2(main,pol)

    swap=np.zeros_like(main)
    swap[0]=-36.0*rr*aa*S1*S0
    swap[1]=(
        -36.0*rr*aa*(N1*S0+N0*S1)
        -36.0*rr*S1*S0
    )
    symerr=rel_l2(main,swap)
    return main,con,polerr,symerr


def q2_direction_parts(mod6,mod7,bg,tag,state,dot,nx):
    """Frozen Q2(d,d), retained only for cancellation report diagnostics."""
    nt=len(bg["x"])
    Dx=r7.fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    real,rdot,sp=r7.reduced_state_real(bg,state,nx,dot)

    N=real["N20"]; S=real["S20"]; u=real["u20"]
    dr=real["delta_varrho20"]
    z=np.zeros_like(N)
    aa=bg["a"][:,None]
    adot=(bg["a"]*bg["H"])[:,None]
    Zb=bg["Z_action"][:,None]

    vals6=(
        aa,adot,Zb,N,S,S,z,u,
        rdot["S20"],sp["S20"],
        rdot["S20"],sp["S20"],z,
        rdot["u20"],sp["u20"],
        rdot["phi20"],sp["phi20"],sp["N20"],
        r7.KB,r7.CV,r7.K2,r7.Q0,r7.Z0,
    )
    p6=r7.eval_stable_partials(mod6.f_c2,vals6,N.shape,"c2")
    g=r7.assemble_ga_local(
        p6,Dt,spatial_real=True,
        kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    )

    rhob=(3.0*r7.C_VALUES[tag]/bg["a"]**3)[:,None]
    vals7=(aa,rhob,N,S,S,z,dr,rdot["T20"],sp["T20"])
    p7={name:fn(*vals7) for name,fn in mod7.f_c2.items()}
    p7=r7.broadcast_partials(p7,N.shape)
    m=r7.assemble_m_local(
        p7,Dt,spatial_real=True,
        kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    )
    zma={k:np.zeros_like(v) for k,v in m.items()}
    zga={k:np.zeros_like(v) for k,v in g.items()}
    gm,gc=r7.main_and_constraints(g,zma)
    mm,mc=r7.main_and_constraints(zga,m)
    return gm,gc,mm,mc


def q_cross_balanced_report_only(mod6,mod7,bg,tag,z10,d10,z11,d11,nx,mu=1.0):
    mm=float(mu)
    n10=float(np.sqrt(np.linalg.norm(z10)**2+np.linalg.norm(d10)**2))
    n11=float(np.sqrt(np.linalg.norm(z11)**2+np.linalg.norm(d11)**2))
    a10=np.asarray(z10,complex)/n10
    ad10=np.asarray(d10,complex)/n10
    a11=np.asarray(z11,complex)/n11
    ad11=np.asarray(d11,complex)/n11
    pp=q2_direction_parts(mod6,mod7,bg,tag,a10+mm*a11,ad10+mm*ad11,nx)
    pm=q2_direction_parts(mod6,mod7,bg,tag,a10-mm*a11,ad10-mm*ad11,nx)
    fac=(n10*n11)/(4.0*mm)
    return tuple(fac*(a-b) for a,b in zip(pp,pm))

def dy2_real(bg,z10,d10,z11,d11,beta,nx):
    """Physical directional derivative of the H3 Y2 residual."""
    r0,_,s0=r7.reduced_state_real(bg,z10,nx,d10)
    r1,_,s1=r7.reduced_state_real(bg,z11,nx,d11)
    a=bg["a"][:,None]
    X0=bg["Q_action"][:,None]*r0["u20"]+s0["phi20"]/a
    X1=bg["Q_action"][:,None]*r1["u20"]+s1["phi20"]/a
    directional=2.0*np.abs(X0)*X1

    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    mm=np.fft.fftfreq(nx)*nx
    fh=np.fft.fft(directional,axis=1)*r7.mask23(nx)[None,:]
    div=np.fft.ifft(1j*(kfund*mm)[None,:]*fh,axis=1).real/a
    coef=2.0*(2.0-r7.KB)/((1.0+float(beta))*r7.A0_MPC_INV)
    return coef*div

def m1_mapped_fourier(bg,B20):
    """Return H4 contribution -2*M1_GE05 in GE06 convention.

    B20 shape [beta,40,time]. Output main [beta,6,time,41], constraints zero.
    """
    B=np.asarray(B20,complex)
    nb,nm,nt=B.shape
    main=np.zeros((nb,6,nt,M_MAX+1),complex)
    con=np.zeros((nb,2,nt,M_MAX+1),complex)
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    for jm,m in enumerate(r7.M_SOLVE):
        k=float(m*kfund)
        # raw M1: aether=-Q a^3 B/2, scalar=+a^2 ik B/2.
        # H4 mapped contribution is -2*M1.
        main[:,2,:,m]=bg["Q_action"][None,:]*bg["a"][None,:]**3*B[:,jm,:]
        main[:,3,:,m]=-bg["a"][None,:]**2*(1j*k)*B[:,jm,:]
    return main,con

def grav_real_for_memory(bg,state,modes,nx):
    """N,S,u,phi and phi derivatives for GE05 direction."""
    st=np.asarray(state,complex)
    modes=np.asarray(modes,int)
    nt=st.shape[-1]
    Dx=r7.fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    out={}
    for iv,name in ((0,"N"),(1,"S"),(2,"u"),(3,"phi")):
        c=st[:,iv,:]
        out[name]=reconstruct_general(c,modes,nx)
    phic=st[:,3,:]
    pht=np.asarray([Dt@phic[j] for j in range(len(modes))],complex)
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    ks=modes.astype(float)*kfund
    phix=(1j*ks[:,None])*phic
    out["pt"]=reconstruct_general(pht,modes,nx)
    out["px"]=reconstruct_general(phix,modes,nx)
    return out

def memory_m2_chunk(ge05,bg,grav,z,v,r,w,tau,nx):
    """Sum raw GE05 M2 gravity residual over one q10 node chunk."""
    modes=r7.FOURIER_N
    zr=r24.reconstruct_batched_positive_modes(z,modes,nx)
    zt=r24.reconstruct_batched_positive_modes(v/tau,modes,nx)
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    ks=np.asarray(modes,float)*kfund
    zx=r24.reconstruct_batched_positive_modes((1j*ks[None,:,None])*z,modes,nx)

    rr=np.asarray(r,float)
    ww=np.asarray(w,float)
    om=(rr/tau)[:,None,None]
    sw=np.sqrt(ww)[:,None,None]
    q=sw*zr/om
    qt=sw*zt/om
    qx=sw*zx/om

    shape=q.shape
    aa=np.broadcast_to(bg["a"][None,:,None],shape)
    QQ=np.broadcast_to(bg["Q_action"][None,:,None],shape)
    z0=np.zeros_like(grav["N"])[None,:,:]
    vals=(
        aa,QQ,
        grav["N"][None,:,:],grav["S"][None,:,:],grav["S"][None,:,:],z0,
        grav["u"][None,:,:],grav["pt"][None,:,:],grav["px"][None,:,:],
        qt,qx,q,
        np.broadcast_to(om,shape),np.broadcast_to(sw,shape),
    )
    pd={key:np.broadcast_to(np.asarray(fn(*vals)),shape) for key,fn in ge05.f_c2.items()}

    Dx=r7.fd4_matrix(len(bg["x"]),bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    dtpt=np.einsum("ij,bjk->bik",Dt,pd["pt"],optimize=True)
    dxpx=r24.spectral_dx_batch(pd["px"],kfund)
    scalar=-dtpt-dxpx
    aether=pd["r"]

    # Sum the per-node action residuals; weights are already carried by sw.
    lapse=np.sum(pd["N"],axis=0)
    shift=np.sum(pd["b"],axis=0)
    LL=np.sum(pd["L"],axis=0)
    RR=np.sum(pd["R"],axis=0)
    aeth=np.sum(aether,axis=0)
    scal=np.sum(scalar,axis=0)
    zero=np.zeros_like(lapse)
    main=np.stack([lapse,LL+RR,aeth,scal,zero,zero],axis=0)
    con=np.stack([shift,LL-0.5*RR],axis=0)
    return main,con

def reconstruct_m2_source(ge05,bg,h1,boundary,order,nx=NX_POLY,chunk=16):
    """Raw GE05 M2 source from certified Z10,q10, then map -2 into GE06."""
    r=np.asarray(boundary["r"],float)
    w=np.asarray(boundary["w"],float)
    tau=r24.TAUH0/float(r7.g9.H0_CLASS)
    X10=r24.first_order_X_modes(r7,bg,h1)
    z10,v10=r24.evolve_z10(c4,bg,X10,boundary["z0"],boundary["v0"],r,tau)
    grav=grav_real_for_memory(bg,h1,r7.FOURIER_N,nx)

    raw_main=np.zeros((6,len(bg["x"]),nx),float)
    raw_con=np.zeros((2,len(bg["x"]),nx),float)
    for j0 in range(0,order,chunk):
        j1=min(order,j0+chunk)
        ma,co=memory_m2_chunk(
            ge05,bg,grav,z10[j0:j1],v10[j0:j1],
            r[j0:j1],w[j0:j1],tau,nx
        )
        raw_main += ma
        raw_con += co

    # Exact GE05->GE06 factor two and H4 minus sign.
    return -GE05_TO_GE06*fft_low(raw_main),-GE05_TO_GE06*fft_low(raw_con),z10,v10

def assemble_nonmemory(qdirect,mod6,mod7,bg,tag,z10,d10,z11,d11,nx_dy):
    """Direct GE06/GE07/Lambda Q cross + unchanged DY2."""
    q01=q_cross_direct(qdirect,bg,tag,z10,d10,z11,d11,NX_POLY)
    q10=q_cross_direct(qdirect,bg,tag,z11,d11,z10,d10,NX_POLY)
    symmetry=max(rel_l2(a,b) for a,b in zip(q01,q10))

    qbal=q_cross_balanced_report_only(
        mod6,mod7,bg,tag,z10,d10,z11,d11,NX_POLY,1.0
    )
    cancellation_report=max(rel_l2(a,b) for a,b in zip(q01,qbal))

    lam_m,lam_c,lam_polerr,lam_symerr=lambda_cross_direct(
        bg,z10,d10,z11,d11,NX_POLY
    )

    ga_m,ga_c,ma_m,ma_c=q01
    qga_main=-2.0*fft_low(ga_m); qga_con=-2.0*fft_low(ga_c)
    qm_main=-2.0*fft_low(ma_m); qm_con=-2.0*fft_low(ma_c)
    ql_main=-2.0*fft_low(lam_m); ql_con=-2.0*fft_low(lam_c)

    dy_by_beta={}
    for beta in r7.BETAS:
        dy=dy2_real(bg,z10,d10,z11,d11,beta,nx_dy)
        fm=fft_low(dy)
        main=np.zeros((6,len(bg["x"]),M_MAX+1),complex)
        con=np.zeros((2,len(bg["x"]),M_MAX+1),complex)
        main[3]=-2.0*fm
        dy_by_beta[float(beta)]=(main,con)
    return (
        (qga_main,qga_con),(qm_main,qm_con),(ql_main,ql_con),dy_by_beta,
        symmetry,cancellation_report,lam_polerr,lam_symerr
    )

def build_bath_parent_config(ge05,normf,bgs,r22npz,trace,order,nt,nx_g2):
    boundary=r24.full_history_boundary(c4,r7,trace,order)
    out,diag=r24.construct_configuration(
        ge05,c4,r7,normf,bgs,r22npz,boundary,
        nt,nx_g2,order,spatial_control=False
    )
    return boundary,out,diag

def verify_bath_projection(config,r27npz,kind):
    errs=[]
    for tag in r7.C_TAGS:
        if kind=="primary":
            errs.append(rel_l2(config[tag]["weighted_z10"],r27npz[f"{tag}_weighted_z10_primary"]))
            errs.append(rel_l2(config[tag]["weighted_z20"],r27npz[f"{tag}_weighted_z20_primary"]))
        elif kind=="quadrature":
            errs.append(rel_l2(config[tag]["weighted_z20"],r27npz[f"{tag}_weighted_z20_quadrature_control"]))
        elif kind=="time":
            errs.append(rel_l2(config[tag]["weighted_z10"],r27npz[f"{tag}_weighted_z10_time_control"]))
            errs.append(rel_l2(config[tag]["weighted_z20"],r27npz[f"{tag}_weighted_z20_time_control"]))
        else:
            raise ValueError(kind)
    return max(errs,default=0.0)

def build_source_config(
    qdirect,mod6,mod7,ge05,bgs,r22,r32b,
    bathcfg,boundary,order,nt,nx_dy,
):
    label="primary" if nt==NT_PRIMARY else "control"
    out={}
    qsym=[]; qcancel=[]; qlpol=[]; qlsym=[]
    for tag in r7.C_TAGS:
        bg=bgs[(nt,tag)]
        z10=np.asarray(r22[f"{tag}_H1_{label}"],complex)
        d10=np.asarray(r22[f"{tag}_H1dot_{label}"],complex)
        z11=np.asarray(r32b[f"{tag}_Z11_{label}"],complex)
        d11=np.asarray(r32b[f"{tag}_Z11dot_{label}"],complex)

        qga,qm,ql,dy,qsymerr,qcancelerr,qlpolerr,qlsymerr=assemble_nonmemory(
            qdirect,mod6,mod7,bg,tag,z10,d10,z11,d11,nx_dy
        )
        qsym.append(qsymerr)
        qcancel.append(qcancelerr)
        qlpol.append(qlpolerr)
        qlsym.append(qlsymerr)

        m1_main,m1_con=m1_mapped_fourier(bg,bathcfg[tag]["B20_linear"])
        m2_main0,m2_con0,_,_=reconstruct_m2_source(ge05,bg,z10,boundary,order,NX_POLY)

        bybeta={}
        for ib,beta in enumerate(r7.BETAS):
            qga_m,qga_c=qga; qm_m,qm_c=qm; ql_m,ql_c=ql
            dy_m,dy_c=dy[float(beta)]
            m2_m=m2_main0; m2_c=m2_con0
            pieces={
                "2Q_GE06_cross":(qga_m,qga_c),
                "2Q_GE07_cross":(qm_m,qm_c),
                "2Q_Lambda_cross":(ql_m,ql_c),
                "2DY2":(dy_m,dy_c),
                "2M1_GE05_mapped":(m1_main[ib],m1_con[ib]),
                "2M2_GE05_mapped":(m2_m,m2_c),
            }
            total_m=sum(v[0] for v in pieces.values())
            total_c=sum(v[1] for v in pieces.values())
            bybeta[float(beta)]={
                "rhs":total_m,
                "rhs_constraint":total_c,
                "pieces":pieces,
            }
        out[tag]=bybeta
    return out,max(qsym,default=0.0),max(qcancel,default=0.0),max(qlpol,default=0.0),max(qlsym,default=0.0)

def compare_component(configA,configB,piece=None):
    aa=[]; bb=[]
    for tag in r7.C_TAGS:
        for beta in r7.BETAS:
            A=configA[tag][float(beta)]
            B=configB[tag][float(beta)]
            if piece is None:
                aa.extend([A["rhs"].ravel(),A["rhs_constraint"].ravel()])
                bb.extend([B["rhs"].ravel(),B["rhs_constraint"].ravel()])
            else:
                aa.extend([A["pieces"][piece][0].ravel(),A["pieces"][piece][1].ravel()])
                bb.extend([B["pieces"][piece][0].ravel(),B["pieces"][piece][1].ravel()])
    return rel_l2(np.concatenate(aa),np.concatenate(bb))

def interp_source_config(xp,src,xc):
    out={}
    for tag in r7.C_TAGS:
        out[tag]={}
        for beta in r7.BETAS:
            s=src[tag][float(beta)]
            row={
                "rhs":interp_complex_axis(xp,s["rhs"],xc,axis=1),
                "rhs_constraint":interp_complex_axis(xp,s["rhs_constraint"],xc,axis=1),
                "pieces":{},
            }
            for key,(ma,co) in s["pieces"].items():
                row["pieces"][key]=(
                    interp_complex_axis(xp,ma,xc,axis=1),
                    interp_complex_axis(xp,co,xc,axis=1),
                )
            out[tag][float(beta)]=row
    return out

def shift_trace_from_canonical(mod6,mod7,bg,tag,k,Y,rhsfun,confun):
    ncol,_,nt=Y.shape
    metric=np.empty((ncol,nt),float)
    absres=np.empty((ncol,nt),float)
    scale=np.empty((ncol,nt),float)
    for it,xq in enumerate(bg["x"]):
        rr=np.asarray(rhsfun(float(xq)),complex)
        rc=np.asarray(confun(float(xq)),complex)
        if rr.ndim==1: rr=rr[:,None]
        if rc.ndim==1: rc=rc[:,None]
        M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
            mod6,mod7,bg,tag,k,float(xq)
        )
        for j in range(ncol):
            src=np.concatenate([rr[:,j],rc[:,j]])
            w=WY@Y[j,:,it]+WR@src
            sm=r7._constraint_backward_error(
                Cmat[10]+Cmat[11],w,rc[0,j],Cmat[10]@w,Cmat[11]@w
            )
            metric[j,it]=sm["metric"]
            absres[j,it]=sm["absolute_residual"]
            scale[j,it]=sm["scale"]
    return metric,absres,scale


def solve_config(mod6,mod7,bgs,sources,nt):
    """Certified H3-matched canonical particular-state propagation.

    q0=(S,u,phi,T)=0 exactly. The compatible p0 is the frozen Repair18
    doubly equilibrated minimum-norm lapse+shift projection. Propagation uses
    the Repair07 two-stage Radau IIA canonical march.
    """
    states={}
    p0store={}
    shifttraces={}
    diag={}
    linmax=0.0
    shiftmax=0.0
    anisomax=0.0
    q0max=0.0
    bproj=0.0
    blapse=0.0
    bshift=0.0
    balg=0.0
    finite=True

    for tag in r7.C_TAGS:
        bg=bgs[(nt,tag)]
        x=np.asarray(bg["x"],float)
        nb=len(r7.BETAS); nm=len(r7.M_SOLVE)
        st=np.empty((nb,nm,6,nt),complex)
        p0arr=np.empty((nb,nm,4),complex)
        smetric=np.empty((nb,nm,nt),float)
        sabs=np.empty((nb,nm,nt),float)
        sscale=np.empty((nb,nm,nt),float)
        per_mode=[]

        for jm,m in enumerate(r7.M_SOLVE):
            k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
            rhsfun,confun=r7._source_interp(x,sources[tag],m)
            r0=np.asarray(rhsfun(float(x[0])),complex)
            c0=np.asarray(confun(float(x[0])),complex)
            if r0.ndim==1: r0=r0[:,None]
            if c0.ndim==1: c0=c0[:,None]

            M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
                mod6,mod7,bg,tag,k,float(x[0])
            )
            y0=np.zeros((8,nb),complex)
            initrows=[]

            for ib,beta in enumerate(r7.BETAS):
                source0=np.concatenate([r0[:,ib],c0[:,ib]])
                woff=WR@source0
                lr=Cmat[4]
                sr=Cmat[10]+Cmat[11]
                Afull=np.vstack([lr@WY,sr@WY])
                A=Afull[:,4:8]
                b=np.asarray([
                    r0[0,ib]-lr@woff,
                    c0[0,ib]-sr@woff,
                ],complex)
                p,sd=r18.projected_momentum_solve(A,b)
                y0[4:8,ib]=p
                p0arr[ib,jm]=p

                ev=r18.evaluate_candidate(
                    Cmat,WY,WR,source0,r0[:,ib],c0[:,ib],p
                )
                q0max=max(q0max,float(np.max(np.abs(y0[:4,ib]))))
                bproj=max(bproj,float(sd["scaled_relative_residual_final"]))
                blapse=max(blapse,float(ev["lapse"]["metric"]))
                bshift=max(bshift,float(ev["shift"]["metric"]))
                balg=max(balg,float(ev["algebraic_relative_residual"]))
                finite=bool(finite and ev["all_finite"] and np.all(np.isfinite(p)))
                initrows.append({
                    "beta0":float(beta),
                    "projected_momentum_scaled_relative_residual":float(sd["scaled_relative_residual_final"]),
                    "lapse_backward_error":float(ev["lapse"]["metric"]),
                    "shift_backward_error":float(ev["shift"]["metric"]),
                    "anisotropy_backward_error_report_only":float(ev["anisotropy"]["metric"]),
                    "algebraic_relative_residual":float(ev["algebraic_relative_residual"]),
                    "p_L2":float(np.linalg.norm(p)),
                })

            Y,rdiag=r7._radau2_integrate_canonical(
                mod6,mod7,bg,tag,k,y0,rhsfun,confun
            )
            ss,dd,odiag=r7._reconstruct_canonical_solution(
                mod6,mod7,bg,tag,k,Y,rhsfun,confun
            )
            st[:,jm]=ss
            mt,at,ct=shift_trace_from_canonical(
                mod6,mod7,bg,tag,k,Y,rhsfun,confun
            )
            smetric[:,jm]=mt
            sabs[:,jm]=at
            sscale[:,jm]=ct

            lres=max(
                float(rdiag["radau_block_scaled_relative_L2_residual_max"]),
                float(odiag["algebraic_scaled_relative_L2_residual_max"]),
                float(odiag["lapse_noether_row_relative_residual_max"]),
            )
            linmax=max(linmax,lres)
            shiftmax=max(shiftmax,float(odiag["shift_constraint_relative_L2_max"]))
            anisomax=max(anisomax,float(odiag["anisotropy_constraint_relative_L2_max"]))
            finite=bool(
                finite and odiag["all_outputs_finite"]
                and np.all(np.isfinite(Y)) and np.all(np.isfinite(ss))
            )
            per_mode.append({
                "m":int(m),
                "linear_residual_max":lres,
                "shift_constraint_backward_error_max":float(odiag["shift_constraint_relative_L2_max"]),
                "anisotropy_constraint_backward_error_max":float(odiag["anisotropy_constraint_relative_L2_max"]),
                "radau_block_scaled_relative_L2_residual_max":float(rdiag["radau_block_scaled_relative_L2_residual_max"]),
                "algebraic_scaled_relative_L2_residual_max":float(odiag["algebraic_scaled_relative_L2_residual_max"]),
                "lapse_noether_row_relative_residual_max":float(odiag["lapse_noether_row_relative_residual_max"]),
                "initial_boundary":initrows,
            })

        states[tag]=st
        p0store[tag]=p0arr
        shifttraces[tag]={"metric":smetric,"abs":sabs,"scale":sscale}
        diag[tag]={"per_mode":per_mode}

    boundary={
        "q0_abs_max":float(q0max),
        "projected_momentum_scaled_residual_max":float(bproj),
        "lapse_backward_error_max":float(blapse),
        "shift_backward_error_max":float(bshift),
        "algebraic_relative_residual_max":float(balg),
    }
    controls={
        "linear_residual_max":float(linmax),
        "shift_constraint_backward_error_max":float(shiftmax),
        "anisotropy_constraint_backward_error_max":float(anisomax),
        "boundary":boundary,
        "all_outputs_finite":bool(finite),
    }
    return states,p0store,shifttraces,diag,controls

def observed_order(ec,ef,hc,hf):
    if not (ec>0.0 and ef>0.0 and hc>hf>0.0):
        return float("nan")
    return float(math.log(ec/ef)/math.log(hc/hf))


def matched_shift_control(bgs,primary,control):
    sref=max(
        float(np.max(primary[tag]["scale"])) for tag in r7.C_TAGS
    )
    null_thr=SQRT_EPS*sref
    active_p=[]; active_c=[]; near_abs=[]
    active_count=0; null_count=0
    worst=None; worstv=-1.0

    for tag in r7.C_TAGS:
        mp=primary[tag]["metric"]
        ap=primary[tag]["abs"]
        sp=primary[tag]["scale"]
        mc=control[tag]["metric"]
        xp=np.asarray(bgs[(NT_PRIMARY,tag)]["x"],float)
        xc=np.asarray(bgs[(NT_CONTROL,tag)]["x"],float)
        for ib,beta in enumerate(r7.BETAS):
            for jm,m in enumerate(r7.M_SOLVE):
                ci=PchipInterpolator(xc,mc[ib,jm],extrapolate=False)(xp)
                mask=sp[ib,jm]>null_thr
                nmask=~mask
                if np.any(mask):
                    active_p.extend(np.asarray(mp[ib,jm,mask],float).tolist())
                    active_c.extend(np.asarray(ci[mask],float).tolist())
                    active_count+=int(np.count_nonzero(mask))
                    loc=int(np.argmax(np.where(mask,mp[ib,jm],-np.inf)))
                    vv=float(mp[ib,jm,loc])
                    if vv>worstv:
                        worstv=vv
                        worst={
                            "C":tag,"beta0":float(beta),"m":int(m),
                            "time_index":loc,"ln_a":float(xp[loc]),
                            "metric":vv,
                            "absolute_residual":float(ap[ib,jm,loc]),
                            "scale":float(sp[ib,jm,loc]),
                        }
                if np.any(nmask):
                    near_abs.extend(np.asarray(ap[ib,jm,nmask],float).tolist())
                    null_count+=int(np.count_nonzero(nmask))

    active_p=np.asarray(active_p,float)
    active_c=np.asarray(active_c,float)
    if active_p.size==0 or active_c.size==0:
        raise RuntimeError("no active H4 shift samples under frozen Repair21 rule")
    ep_inf=float(np.max(active_p))
    ec_inf=float(np.max(active_c))
    ep_rms=float(np.sqrt(np.mean(active_p**2)))
    ec_rms=float(np.sqrt(np.mean(active_c**2)))
    xp=np.asarray(bgs[(NT_PRIMARY,r7.C_TAGS[0])]["x"],float)
    xc=np.asarray(bgs[(NT_CONTROL,r7.C_TAGS[0])]["x"],float)
    hp=float(abs(xp[-1]-xp[0])/(len(xp)-1))
    hc=float(abs(xc[-1]-xc[0])/(len(xc)-1))
    return {
        "S_ref":float(sref),
        "near_null_threshold":float(null_thr),
        "active_sample_count":int(active_count),
        "near_null_sample_count":int(null_count),
        "Nt128_active_Linf":ep_inf,
        "Nt64_interpolated_active_Linf":ec_inf,
        "Nt128_active_RMS":ep_rms,
        "Nt64_interpolated_active_RMS":ec_rms,
        "observed_order_Linf":observed_order(ec_inf,ep_inf,hc,hp),
        "observed_order_RMS":observed_order(ec_rms,ep_rms,hc,hp),
        "near_null_absolute_residual_over_Sref_Nt128":float(
            max(near_abs,default=0.0)/max(sref,TINY)
        ),
        "worst_Nt128_active_sample":worst,
    }


def state_time_control(bgs,sp,sc):
    rows=[]; mx=0.0
    xp=np.asarray(bgs[(NT_PRIMARY,"C_star")]["x"],float)
    xc=np.asarray(bgs[(NT_CONTROL,"C_star")]["x"],float)
    for tag in r7.C_TAGS:
        pi=r7.interpolate_state_to(xp,sp[tag],xc)
        e=rel_l2(pi,sc[tag])
        rows.append({"C":tag,"global_relative_L2":e})
        mx=max(mx,e)
    return {"max":float(mx),"per_C":rows}

def source_piece_norms(src):
    out={}
    for key in COMPONENTS:
        vals=[]
        for tag in r7.C_TAGS:
            for beta in r7.BETAS:
                ma,co=src[tag][float(beta)]["pieces"][key]
                vals.extend([ma.ravel(),co.ravel()])
        out[key]=float(np.linalg.norm(np.concatenate(vals)))
    vals=[]
    for tag in r7.C_TAGS:
        for beta in r7.BETAS:
            vals.extend([src[tag][float(beta)]["rhs"].ravel(),src[tag][float(beta)]["rhs_constraint"].ravel()])
    out["total_H4_rhs"]=float(np.linalg.norm(np.concatenate(vals)))
    return out

def all_finite_source(src):
    for tag in r7.C_TAGS:
        for beta in r7.BETAS:
            q=src[tag][float(beta)]
            if not np.all(np.isfinite(q["rhs"])) or not np.all(np.isfinite(q["rhs_constraint"])):
                return False
            for ma,co in q["pieces"].values():
                if not np.all(np.isfinite(ma)) or not np.all(np.isfinite(co)):
                    return False
    return True

def save_config(save,prefix,src):
    for tag in r7.C_TAGS:
        for ib,beta in enumerate(r7.BETAS):
            q=src[tag][float(beta)]
            save[f"{prefix}_{tag}_beta{ib}_total_main"]=q["rhs"]
            save[f"{prefix}_{tag}_beta{ib}_total_constraint"]=q["rhs_constraint"]
            for key,(ma,co) in q["pieces"].items():
                safe=key.replace("/","_")
                save[f"{prefix}_{tag}_beta{ib}_{safe}_main"]=ma
                save[f"{prefix}_{tag}_beta{ib}_{safe}_constraint"]=co

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--repair26-trace",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    rd=Path(args.results_dir)
    paths,hashes,r13npz,r22,r27npz,r32b=load_parents(rd,args)
    bgs,bgctl,mod6,mod7,ge05,normf,normdiag,qdirect,lambda_diag=build_context(rd,r13npz)

    # Exact Repair27 bath reconstruction configurations.
    b2048,pbath,pdiag=build_bath_parent_config(
        ge05,normf,bgs,r22,paths["trace"],NQ_PRIMARY,NT_PRIMARY,r24.NX_PRIMARY
    )
    b1024,qbath,qdiag=build_bath_parent_config(
        ge05,normf,bgs,r22,paths["trace"],NQ_CONTROL,NT_PRIMARY,r24.NX_PRIMARY
    )
    bt2048,tbath,tdiag=build_bath_parent_config(
        ge05,normf,bgs,r22,paths["trace"],NQ_PRIMARY,NT_CONTROL,r24.NX_CONTROL
    )
    bath_repro=max(
        verify_bath_projection(pbath,r27npz,"primary"),
        verify_bath_projection(qbath,r27npz,"quadrature"),
        verify_bath_projection(tbath,r27npz,"time"),
    )
    if bath_repro>1e-10:
        raise RuntimeError(f"Repair27 deterministic bath reconstruction mismatch: {bath_repro}")

    # Primary H4 source, high-resolution spatial control, quadrature control.
    srcP,qsymP,qcancelP,qlpolP,qlsymP=build_source_config(
        qdirect,mod6,mod7,ge05,bgs,r22,r32b,pbath,b2048,NQ_PRIMARY,NT_PRIMARY,NX_DY_PRIMARY
    )
    srcS,qsymS,qcancelS,qlpolS,qlsymS=build_source_config(
        qdirect,mod6,mod7,ge05,bgs,r22,r32b,pbath,b2048,NQ_PRIMARY,NT_PRIMARY,NX_DY_CONTROL
    )
    srcQ,qsymQ,qcancelQ,qlpolQ,qlsymQ=build_source_config(
        qdirect,mod6,mod7,ge05,bgs,r22,r32b,qbath,b1024,NQ_CONTROL,NT_PRIMARY,NX_DY_PRIMARY
    )
    srcT,qsymT,qcancelT,qlpolT,qlsymT=build_source_config(
        qdirect,mod6,mod7,ge05,bgs,r22,r32b,tbath,bt2048,NQ_PRIMARY,NT_CONTROL,NX_DY_PRIMARY
    )

    qsym=max(qsymP,qsymS,qsymQ,qsymT)
    qcancel=max(qcancelP,qcancelS,qcancelQ,qcancelT)
    qlpol=max(qlpolP,qlpolS,qlpolQ,qlpolT)
    qlsym=max(qlsymP,qlsymS,qlsymQ,qlsymT)
    dy_spatial=compare_component(srcP,srcS,"2DY2")
    total_spatial=compare_component(srcP,srcS,None)

    # Memory-only quadrature comparison.
    def memory_concat(src):
        vals=[]
        for tag in r7.C_TAGS:
            for beta in r7.BETAS:
                for key in ("2M1_GE05_mapped","2M2_GE05_mapped"):
                    ma,co=src[tag][float(beta)]["pieces"][key]
                    vals.extend([ma.ravel(),co.ravel()])
        return np.concatenate(vals)
    mem_quad=rel_l2(memory_concat(srcP),memory_concat(srcQ))

    xp=np.asarray(bgs[(NT_PRIMARY,"C_star")]["x"],float)
    xc=np.asarray(bgs[(NT_CONTROL,"C_star")]["x"],float)
    srcPi=interp_source_config(xp,srcP,xc)
    source_time=compare_component(srcPi,srcT,None)

    statesP,p0P,shiftP,solveP,ctlP=solve_config(mod6,mod7,bgs,srcP,NT_PRIMARY)
    statesT,p0T,shiftT,solveT,ctlT=solve_config(mod6,mod7,bgs,srcT,NT_CONTROL)
    linear_max=max(ctlP["linear_residual_max"],ctlT["linear_residual_max"])
    state_time=state_time_control(bgs,statesP,statesT)
    shift_match=matched_shift_control(bgs,shiftP,shiftT)
    raw_shift=max(ctlP["shift_constraint_backward_error_max"],ctlT["shift_constraint_backward_error_max"])
    aniso=max(ctlP["anisotropy_constraint_backward_error_max"],ctlT["anisotropy_constraint_backward_error_max"])
    q0max=max(ctlP["boundary"]["q0_abs_max"],ctlT["boundary"]["q0_abs_max"])
    bproj=max(ctlP["boundary"]["projected_momentum_scaled_residual_max"],ctlT["boundary"]["projected_momentum_scaled_residual_max"])
    blapse=max(ctlP["boundary"]["lapse_backward_error_max"],ctlT["boundary"]["lapse_backward_error_max"])
    bshift=max(ctlP["boundary"]["shift_backward_error_max"],ctlT["boundary"]["shift_backward_error_max"])
    balg=max(ctlP["boundary"]["algebraic_relative_residual_max"],ctlT["boundary"]["algebraic_relative_residual_max"])

    lrows=list(lambda_diag.values())
    lambda_operator_control={
        "stage_evaluation_count":int(len(lrows)),
        "rho_lambda_min":float(min((q["rho_lambda"] for q in lrows),default=math.inf)),
        "rho_lambda_max":float(max((q["rho_lambda"] for q in lrows),default=-math.inf)),
        "lambda_shift_abs_max":float(max((q["lambda_shift_abs_max"] for q in lrows),default=math.inf)),
        "lambda_anisotropy_abs_max":float(max((q["lambda_anisotropy_abs_max"] for q in lrows),default=math.inf)),
        "all_stage_rho_finite":bool(lrows and all(np.isfinite(q["rho_lambda"]) for q in lrows)),
    }

    finite=bool(
        all_finite_source(srcP) and all_finite_source(srcS)
        and all_finite_source(srcQ) and all_finite_source(srcT)
        and all(np.all(np.isfinite(v)) for v in statesP.values())
        and all(np.all(np.isfinite(v)) for v in statesT.values())
    )

    gates={
        "all_parent_hashes_and_classifications_exact":True,
        "Repair32C_Z11_certified_and_H4_licensed":True,
        "GE05_to_GE06_dictionary_scale_exactly_2_no_fit":True,
        "Repair11_Lambda_operator_installed_and_stage_evaluated":bool(
            lambda_operator_control["stage_evaluation_count"]>0
            and lambda_operator_control["all_stage_rho_finite"]
            and lambda_operator_control["lambda_shift_abs_max"]==0.0
            and lambda_operator_control["lambda_anisotropy_abs_max"]==0.0
        ),
        "Q_cross_direct_symbolic_polarization_identity_exact":bool(qdirect["all_symbolic_polarization_identities_exact"]),
        "Q_cross_direct_symmetry_relative_L2_le_1e12":bool(qsym<=Q_SYMMETRY_MAX),
        "Q_lambda_direct_vs_exact_polarization_relative_L2_le_1e12":bool(qlpol<=Q_SYMMETRY_MAX),
        "Q_lambda_direct_symmetry_relative_L2_le_1e12":bool(qlsym<=Q_SYMMETRY_MAX),
        "DY2_Nx1024_vs_Nx2048_low_mode_relative_L2_le_5e4":bool(dy_spatial<=DY_SPATIAL_MAX),
        "total_H4_source_Nx1024_vs_Nx2048_m1_40_relative_L2_le_5e4":bool(total_spatial<=TOTAL_SPATIAL_MAX),
        "memory_source_Nq1024_vs_Nq2048_relative_L2_le_1e2":bool(mem_quad<=MEMORY_QUAD_MAX),
        "total_H4_source_Nt64_vs_Nt128_relative_L2_le_5e3":bool(source_time<=SOURCE_TIME_MAX),
        "canonical_Radau_and_algebraic_linear_residual_le_1e8":bool(linear_max<=LINEAR_MAX),
        "H4_state_Nt64_vs_Nt128_global_relative_L2_le_5e3":bool(state_time["max"]<=STATE_TIME_MAX),
        "H4_active_shift_Nt128_Linf_le_1e6":bool(shift_match["Nt128_active_Linf"]<=CONSTRAINT_MAX),
        "H4_near_null_absolute_residual_over_Sref_le_1000eps":bool(
            shift_match["near_null_absolute_residual_over_Sref_Nt128"]<=NEAR_NULL_RATIO_MAX
        ),
        "H4_matched_active_shift_Linf_order_ge_2p5":bool(
            np.isfinite(shift_match["observed_order_Linf"])
            and shift_match["observed_order_Linf"]>=ORDER_MIN
        ),
        "H4_matched_active_shift_RMS_order_ge_2p5":bool(
            np.isfinite(shift_match["observed_order_RMS"])
            and shift_match["observed_order_RMS"]>=ORDER_MIN
        ),
        "H4_anisotropy_constraint_backward_error_le_1e6":bool(aniso<=CONSTRAINT_MAX),
        "boundary_q0_abs_le_1e12":bool(q0max<=1e-12),
        "boundary_projected_momentum_scaled_residual_le_1e8":bool(bproj<=1e-8),
        "boundary_lapse_backward_error_le_1e6":bool(blapse<=1e-6),
        "boundary_shift_backward_error_le_1e6":bool(bshift<=1e-6),
        "boundary_algebraic_relative_residual_le_1e8":bool(balg<=1e-8),
        "all_source_and_state_outputs_finite":bool(finite and ctlP["all_outputs_finite"] and ctlT["all_outputs_finite"]),
    }
    passed=bool(all(gates.values()))

    report={
        "classification":(
            "GE19_REPAIR36_LAMBDA_COMPLETE_H4_Z21_RECLOSURE_PASS"
            if passed else
            "GE19_REPAIR36_LAMBDA_COMPLETE_H4_Z21_RECLOSURE_FAIL"
        ),
        "predata_classification":"GE19_REPAIR36_PREDATA_LAMBDA_COMPLETE_H4_Z21_RECLOSURE",
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "H4_equation":"L_total(GE06+GE07+Lambda) Z21 = -2 Q_total(GE06+GE07+Lambda; Z10,Z11) - 2 DY2[Z10;Z11] - 2 M1_GE05[Z20,q20] - 2 M2_GE05[(Z10,q10),(Z10,q10)]",
        "provenance":{
            "input_sha256":hashes,
            "Repair26_trace_bytes":paths["trace"].stat().st_size,
            "Repair27_bath_projection_reconstruction_relative_L2_max":bath_repro,
            "GE05_to_GE06_raw_residual_scale":GE05_TO_GE06,
            "fitted_normalization_used":False,
            "Repair11_Lambda_operator_installed":True,
        },
        "construction":{
            "scope":"window-local particular reduced H4/Z21 state",
            "C_tags":list(r7.C_TAGS),
            "beta0":list(r7.BETAS),
            "input_modes":r7.FOURIER_N.tolist(),
            "solved_output_modes":[1,M_MAX],
            "time_primary":NT_PRIMARY,
            "time_control":NT_CONTROL,
            "polynomial_source_grid_exact_bandlimit":NX_POLY,
            "DY2_spatial_primary":NX_DY_PRIMARY,
            "DY2_spatial_control":NX_DY_CONTROL,
            "bath_quadrature_primary":NQ_PRIMARY,
            "bath_quadrature_control":NQ_CONTROL,
            "canonical_particular_boundary":"q0=0 with Repair18 projected p0 from lapse+shift constraints",
        },
        "source_controls":{
            "Q_cross_direct_symbolic_polarization_identity_exact":qdirect["all_symbolic_polarization_identities_exact"],
            "Q_cross_direct_symmetry_relative_L2_max":qsym,
            "Q_cross_balanced_vs_direct_relative_L2_report_only":qcancel,
            "Q_lambda_direct_vs_exact_polarization_relative_L2_max":qlpol,
            "Q_lambda_direct_symmetry_relative_L2_max":qlsym,
            "Q_cross_symbolic_identity_by_partial":{
                "GE06":qdirect["GE06_identity_by_partial"],
                "GE07":qdirect["GE07_identity_by_partial"],
            },
            "DY2_Nx1024_vs_Nx2048_low_mode_relative_L2":dy_spatial,
            "total_H4_source_Nx1024_vs_Nx2048_relative_L2":total_spatial,
            "memory_source_Nq1024_vs_Nq2048_relative_L2":mem_quad,
            "total_H4_source_Nt128_vs_Nt64_relative_L2":source_time,
            "primary_component_L2_norms":source_piece_norms(srcP),
            "normalized_bath_c2_audit":normdiag,
        },
        "solve_controls":{
            "Lambda_operator":lambda_operator_control,
            "canonical_Radau_and_algebraic_linear_residual_max":linear_max,
            "state_Nt128_vs_Nt64_global_relative_L2":state_time,
            "matched_shift":shift_match,
            "raw_all_row_shift_constraint_backward_error_max_report_only":raw_shift,
            "anisotropy_constraint_backward_error_max":aniso,
            "boundary":{
                "q0_abs_max":q0max,
                "projected_momentum_scaled_residual_max":bproj,
                "lapse_backward_error_max":blapse,
                "shift_backward_error_max":bshift,
                "algebraic_relative_residual_max":balg,
            },
            "primary":ctlP,
            "control":ctlT,
            "primary_per_C":solveP,
            "control_per_C":solveT,
        },
        "gates":gates,
        "Z21_window_local_particular_constructed":True,
        "Z21_window_local_particular_certified":passed,
        "primordial_homogeneous_Z21_certified":False,
        "full_species_Z21_certified":False,
        "routing":{
            "next_route":(
                "Z21_WINDOW_LOCAL_PARTICULAR_CERTIFIED_PREREGISTER_LENSING_OBSERVABLE"
                if passed else
                "H4_Z21_FAIL_FREEZE_AND_LOCALIZE"
            )
        },
        "claim_boundary":"Repair36 certifies only the canonical window-local particular reduced H4/Z21 state on the frozen late-time scalar/AeST/pressureless-dust+Lambda scope. It restores the exact Repair11 Lambda first-directional operator and Repair14 mixed Lambda quadratic source while retaining the Repair35 direct GE06/GE07 bilinear Q cross, Repair21/Repair22 shift certification rule, and unchanged Repair18/Repair07 boundary/propagator. It does not choose a primordial homogeneous Z21 mode, certify a full-species nonlinear cosmology, introduce finite eta, or establish an observational signal."
    }

    outj=Path(args.json_out); outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")

    save={
        "x_primary":xp,"x_control":xc,
        "beta0":np.asarray(r7.BETAS,float),
        "modes_output":np.asarray(r7.M_SOLVE,int),
    }
    for tag in r7.C_TAGS:
        save[f"{tag}_Z21_primary"]=statesP[tag]
        save[f"{tag}_Z21_control"]=statesT[tag]
        save[f"{tag}_projected_p0_primary"]=p0P[tag]
        save[f"{tag}_projected_p0_control"]=p0T[tag]
        save[f"{tag}_shift_metric_primary"]=shiftP[tag]["metric"]
        save[f"{tag}_shift_abs_primary"]=shiftP[tag]["abs"]
        save[f"{tag}_shift_scale_primary"]=shiftP[tag]["scale"]
        save[f"{tag}_shift_metric_control"]=shiftT[tag]["metric"]
        save[f"{tag}_shift_abs_control"]=shiftT[tag]["abs"]
        save[f"{tag}_shift_scale_control"]=shiftT[tag]["scale"]
    save_config(save,"primary",srcP)
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
            "classification":"GE19_REPAIR36_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Z21_window_local_particular_certified":False,
            "finite_physical_eta":False,
        },indent=2))
        raise
