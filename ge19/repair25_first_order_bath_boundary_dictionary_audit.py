#!/usr/bin/env python3
"""GE19 Repair25 — first-order bath boundary dictionary audit.

Diagnostic only. No q20 construction and no H4/Z21 solve.
Compares at the exact a=0.4 surface and on a common overlap window:
  1) legacy v0.77 chi/a,
  2) cancellation-free GE15 chi/a,
  3) Repair22 on-shell GE19 X10 / gradfac.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

A0=0.4
AEND=1.0/(1.0+0.2)
NCOMMON=128
TINY=1e-300

R24_JSON_SHA="71f463524b47f72d2c5082667fe99141d2286ebc2938c4eed6b89a1583339f2a"
R22_JSON_SHA="7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
R22_NPZ_SHA="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
R13_JSON_SHA="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
R13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
V077_TRACE_SHA="98c8468e8ccdf902cad8d6e65f3852e863c6fd19df62ece61353ab725ac5a43e"

Q_MAX=1e-10
ALG_MAX=1e-10
GE19_GL_MAX=1e-8
GE19_POINT_MAX=1e-6
V077_DIRECT_MAX=1e-3
FIT_MAX=1e-3
COS_MIN=0.9999


def sha256(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rel_l2(a,b)->float:
    aa=np.asarray(a)
    bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def aor(a,b)->float:
    aa=np.asarray(a)
    bb=np.asarray(b)
    ae=np.abs(aa-bb)
    re=ae/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),TINY)
    return float(np.max(np.minimum(ae,re)))


def cosine(a,b)->float:
    aa=np.asarray(a,float).ravel()
    bb=np.asarray(b,float).ravel()
    return float(np.dot(aa,bb)/max(np.linalg.norm(aa)*np.linalg.norm(bb),TINY))


def real_ls_scale(x,y)->float:
    xx=np.asarray(x,float).ravel()
    yy=np.asarray(y,float).ravel()
    return float(np.dot(xx,yy)/max(np.dot(xx,xx),TINY))


def complex_json(z):
    z=complex(z)
    return [float(z.real),float(z.imag)]


def complex_record(z):
    z=complex(z)
    return {
        "complex":complex_json(z),
        "magnitude":float(abs(z)),
        "phase_rad":float(np.angle(z)),
    }


def complex_ratio_record(num,den):
    num=complex(num); den=complex(den)
    if abs(den)<=TINY:
        return {"defined":False}
    out={"defined":True}
    out.update(complex_record(num/den))
    return out


def complex_ls_scale(x,y):
    """Least-squares c for y ~= c*x with complex amplitudes."""
    xx=np.asarray(x,complex).ravel()
    yy=np.asarray(y,complex).ravel()
    den=np.vdot(xx,xx)
    if abs(den)<=TINY:
        return 0.0+0.0j
    return complex(np.vdot(xx,yy)/den)


def complex_shape_coherence(x,y):
    xx=np.asarray(x,complex).ravel()
    yy=np.asarray(y,complex).ravel()
    den=np.linalg.norm(xx)*np.linalg.norm(yy)
    if den<=TINY:
        return 0.0
    return float(abs(np.vdot(xx,yy))/den)


def v077_interps(c4,trace):
    rows=c4.read_trace(trace)
    histories,kmiss,tmiss=c4.select_and_align(rows)
    out=[]
    qout=[]
    for hist in histories:
        x=np.log(np.asarray([q["a"] for q in hist],float))
        y=np.asarray([q["chi"]/q["a"] for q in hist],float)
        q=np.asarray([q["Q"] for q in hist],float)
        if np.any(np.diff(x)<=0):
            raise RuntimeError("v0.77 ln(a) grid not increasing")
        out.append(PchipInterpolator(x,y,extrapolate=False))
        qout.append(PchipInterpolator(x,q,extrapolate=False))
    return histories,out,qout,float(kmiss),float(tmiss)


def ge15_modes(g9,dense):
    rows=g9.read_table(dense)
    modes,kmiss=g9.group_modes(rows)
    return modes,[g9.build_interps(m) for m in modes],float(kmiss)


def ge15_scalar_drive(g9,interp,x,k):
    st=g9.eval_state(interp,np.asarray(x,float))
    a=np.exp(np.asarray(x,float))
    Q=np.asarray(st["Q"],float)
    alpha=np.asarray(st["alpha_aest"],float)
    theta=np.asarray(st["theta_dark"],float)
    chi=Q*(a*theta/(k*k)+alpha)
    return chi/a,st


def candidate_factor(name,k,a,Q,H0,c_over_H0):
    a=np.asarray(a,float)
    Q=np.asarray(Q,float)
    one=np.ones(a.shape,dtype=complex)
    if name=="1": return one
    if name=="-1": return -one
    if name=="a": return a.astype(complex)
    if name=="1/a": return (1.0/a).astype(complex)
    if name=="k": return np.full(a.shape,k,dtype=complex)
    if name=="1/k": return np.full(a.shape,1.0/k,dtype=complex)
    if name=="i*k": return np.full(a.shape,1j*k,dtype=complex)
    if name=="-i*k": return np.full(a.shape,-1j*k,dtype=complex)
    if name=="i*k/a": return (1j*k/a).astype(complex)
    if name=="-i*k/a": return (-1j*k/a).astype(complex)
    if name=="a/(i*k)": return (a/(1j*k)).astype(complex)
    if name=="Q": return Q.astype(complex)
    if name=="1/Q": return (1.0/Q).astype(complex)
    if name=="H0": return np.full(a.shape,H0,dtype=complex)
    if name=="c_light/H0": return np.full(a.shape,c_over_H0,dtype=complex)
    if name=="2": return 2.0*one
    if name=="1/2": return 0.5*one
    if name=="i": return 1j*one
    if name=="-i": return -1j*one
    if name=="k/a": return (k/a).astype(complex)
    if name=="a/k": return (a/k).astype(complex)
    raise KeyError(name)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--v077-trace",required=True)
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)
    vtrace=Path(args.v077_trace)

    req={
        "r24":rd/"ge19_repair24_q20_construction.json",
        "r22j":rd/"ge19_repair22_on_shell_parent_z20_certification.json",
        "r22n":rd/"ge19_repair22_on_shell_parent_z20_certification.npz",
        "r13j":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "ge15j":rd/"ge15_cancellation_free_s_state_precision_closure.json",
        "dense":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "lambda":rd/"ge15_R1_cli_background.dat",
        "v077":vtrace,
    }
    missing=[str(p) for p in req.values() if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen input(s): "+", ".join(missing))

    fixed={
        "r24":R24_JSON_SHA,"r22j":R22_JSON_SHA,"r22n":R22_NPZ_SHA,
        "r13j":R13_JSON_SHA,"r13n":R13_NPZ_SHA,"v077":V077_TRACE_SHA,
    }
    hashes={}
    for k,p in req.items():
        hashes[k]=sha256(p)
        if k in fixed and hashes[k]!=fixed[k]:
            raise RuntimeError(f"{k} hash mismatch: {hashes[k]}")

    d24=json.loads(req["r24"].read_text())
    if d24.get("classification")!="GE19_REPAIR24_Q20_CONSTRUCTION_FAIL":
        raise RuntimeError("Repair24 parent classification mismatch")
    false24=[k for k,v in d24.get("gates",{}).items() if not bool(v)]
    if false24!=["H1_X10_initial_match_abs_or_rel_le_1e10"]:
        raise RuntimeError(f"Repair24 failure not uniquely X10 bridge: {false24}")

    ge15j=json.loads(req["ge15j"].read_text())
    if ge15j.get("classification")!="GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS":
        raise RuntimeError("GE15 parent is not PASS")
    expected_dense=ge15j["precision_binding"]["dense_trace_sha256"]["R1"]
    if hashes["dense"]!=expected_dense:
        raise RuntimeError("GE15 R1 dense trace hash mismatch")

    r7=load_module(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py","r7r25")
    r11=load_module(ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py","r11r25")
    r13=load_module(ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py","r13r25")
    g9=load_module(ROOT/"ge09/repair01_dense_accepted_step_local_jet_bridge.py","g9r25")
    c4=load_module(ROOT/"nl1c4/expanding_memory_source_trajectory.py","c4r25")

    modes,g15,km15=ge15_modes(g9,req["dense"])
    vhist,v77,vQ77,km77,tm77=v077_interps(c4,vtrace)
    z22=np.load(req["r22n"])
    z13=np.load(req["r13n"])

    base128,_,_=r7.build_ge15_reference(req["dense"],128)
    rho_l128=r11.interp_lambda(req["lambda"],base128["x"])
    bgs={}
    for tag in r7.C_TAGS:
        bgs[tag],_=r13.reduced_background(r7,base128,tag,rho_l128)

    x0=math.log(A0)
    if abs(float(base128["a"][0])-A0)>1e-14:
        raise RuntimeError("Repair22/GE19 Nt128 grid does not start at a=0.4")

    amps,_,_=r7.amplitudes()
    gradfac=np.asarray([
        0.5*float(amps[i])*np.exp(1j*float(r7.PHASES[i]))*(1j*float(g9.K_REQ[i]))
        for i in range(len(g9.K_REQ))
    ],complex)

    xg0=np.empty(len(g9.K_REQ),float)
    Qg0=np.empty(len(g9.K_REQ),float)
    alpha0=np.empty(len(g9.K_REQ),float)
    theta0=np.empty(len(g9.K_REQ),float)
    xv0=np.empty(len(g9.K_REQ),float)
    Qv0=np.empty(len(g9.K_REQ),float)
    for i,k in enumerate(g9.K_REQ):
        xx,st=ge15_scalar_drive(g9,g15[i],[x0],float(k))
        xg0[i]=float(xx[0])
        Qg0[i]=float(st["Q"][0])
        alpha0[i]=float(st["alpha_aest"][0])
        theta0[i]=float(st["theta_dark"][0])
        xv0[i]=float(v77[i](x0))
        Qv0[i]=float(vQ77[i](x0))

    # Algebraic GE09 -> GE19 reference identity on the exact a=0.4 state.
    refX=np.empty(len(g9.K_REQ),complex)
    for i,k in enumerate(g9.K_REQ):
        amp=float(amps[i]); ph=float(r7.PHASES[i])
        u_sin=-(float(k)/A0)*alpha0[i]
        u=r7.positive_mode_coeff(0.0,u_sin,amp,ph)
        varphi=Qg0[i]*A0*theta0[i]/(float(k)*float(k))
        phi=r7.positive_mode_coeff(varphi,0.0,amp,ph)
        # Use GE15 Q here by construction; Q_action equality is audited separately.
        refX[i]=Qg0[i]*u+(1j*float(k)/A0)*phi
    algebraic_target=gradfac*xg0
    alg_rel=rel_l2(refX,algebraic_target)
    alg_point=aor(refX,algebraic_target)
    v077_X0=gradfac*xv0
    ge15_X0=algebraic_target
    init_complex_scale=complex_ls_scale(ge15_X0,v077_X0)
    init_complex_fit_resid=rel_l2(v077_X0,init_complex_scale*ge15_X0)
    q_trace_ge15_rel=rel_l2(Qv0,Qg0)
    q_trace_ge15_point=aor(Qv0,Qg0)

    # Repair22 on-shell X10 at the first sample for each reduced-C envelope.
    perC=[]
    q_rel_max=0.0
    ge19_gl_max=0.0
    ge19_point_max=0.0
    X22_by_C={}
    for tag in r7.C_TAGS:
        bg=bgs[tag]
        h1=np.asarray(z22[f"{tag}_H1_primary"],complex)
        X=np.empty(len(g9.K_REQ),complex)
        for i,k in enumerate(g9.K_REQ):
            X[i]=bg["Q_action"][0]*h1[i,2,0]+(1j*float(k)/A0)*h1[i,3,0]
        X22_by_C[tag]=X
        scalar=X/gradfac
        qrel=float(np.max(np.abs(bg["Q_action"][0]/Qg0-1.0)))
        gl=rel_l2(X,algebraic_target)
        pp=aor(X,algebraic_target)
        q_rel_max=max(q_rel_max,qrel)
        ge19_gl_max=max(ge19_gl_max,gl)
        ge19_point_max=max(ge19_point_max,pp)
        c_g15_g19=complex_ls_scale(X,ge15_X0)
        c_v77_g19=complex_ls_scale(X,v077_X0)
        complex_modes=[]
        for i,k in enumerate(g9.K_REQ):
            complex_modes.append({
                "mode_index":i,
                "k_Mpc_inv":float(k),
                "v077_transported_X":complex_record(v077_X0[i]),
                "GE15_reference_X":complex_record(ge15_X0[i]),
                "GE19_on_shell_X":complex_record(X[i]),
                "ratio_v077_over_GE15":complex_ratio_record(v077_X0[i],ge15_X0[i]),
                "ratio_GE15_over_GE19":complex_ratio_record(ge15_X0[i],X[i]),
                "ratio_v077_over_GE19":complex_ratio_record(v077_X0[i],X[i]),
            })
        perC.append({
            "C":tag,
            "Q_action_at_a0":float(bg["Q_action"][0]),
            "Q_action_over_GE15_Q_minus_1_abs_max":qrel,
            "Q_action_over_v077_Q_minus_1_abs_max":float(np.max(np.abs(bg["Q_action"][0]/Qv0-1.0))),
            "Repair22_X10_vs_GE15_grad_chi_over_a_relative_L2":gl,
            "Repair22_X10_vs_GE15_grad_chi_over_a_pointwise_abs_or_rel_max":pp,
            "best_complex_scale_GE15_eq_c_GE19":complex_record(c_g15_g19),
            "best_complex_scale_GE15_eq_c_GE19_postfit_relative_L2":rel_l2(ge15_X0,c_g15_g19*X),
            "best_complex_scale_v077_eq_c_GE19":complex_record(c_v77_g19),
            "best_complex_scale_v077_eq_c_GE19_postfit_relative_L2":rel_l2(v077_X0,c_v77_g19*X),
            "per_mode_scalar_X10_over_gradfac":[complex_json(z) for z in scalar],
            "per_mode_scalar_over_GE15":[complex_json(scalar[i]/xg0[i]) for i in range(len(xg0))],
            "per_mode_phase_difference_rad":[float(np.angle(X[i]/algebraic_target[i])) for i in range(len(X))],
            "per_mode_complex_dictionary":complex_modes,
        })

    # Exact-surface v0.77 vs GE15.
    init_rows=[]
    for i,k in enumerate(g9.K_REQ):
        ratio=xv0[i]/xg0[i] if abs(xg0[i])>TINY else math.nan
        init_rows.append({
            "mode_index":i,
            "k_Mpc_inv":float(k),
            "k_h_per_Mpc":float(g9.K_H[i]),
            "v077_chi_over_a":float(xv0[i]),
            "GE15_chi_over_a":float(xg0[i]),
            "v077_over_GE15":float(ratio),
            "Q_trace":float(Qv0[i]),
            "Q_GE15":float(Qg0[i]),
            "Q_trace_over_GE15":float(Qv0[i]/Qg0[i]),
            "v077_transported_X":complex_record(v077_X0[i]),
            "GE15_reference_X":complex_record(ge15_X0[i]),
            "complex_ratio_v077_over_GE15":complex_ratio_record(v077_X0[i],ge15_X0[i]),
            "abs_or_relative_error":float(min(abs(xv0[i]-xg0[i]),abs(xv0[i]-xg0[i])/max(abs(xv0[i]),abs(xg0[i]),TINY))),
        })
    init_v77_rel=rel_l2(xv0,xg0)
    init_v77_point=aor(xv0,xg0)

    # Common overlap, mode by mode.
    lo=x0
    hi=min(
        math.log(AEND),
        min(float(np.log(m[-1]["a"])) for m in modes),
        min(float(np.log(h[-1]["a"])) for h in vhist),
    )
    if not hi>lo:
        raise RuntimeError("no GE15-v0.77 overlap above a=0.4")
    xc=np.linspace(lo,hi,NCOMMON)
    ac=np.exp(xc)

    G=np.empty((len(g9.K_REQ),NCOMMON),float)
    V=np.empty_like(G)
    QG=np.empty_like(G)
    QV=np.empty_like(G)
    per_mode=[]
    fit_scales=[]
    fit_resids=[]
    fit_cos=[]
    for i,k in enumerate(g9.K_REQ):
        G[i],stc=ge15_scalar_drive(g9,g15[i],xc,float(k))
        QG[i]=np.asarray(stc["Q"],float)
        V[i]=np.asarray(v77[i](xc),float)
        QV[i]=np.asarray(vQ77[i](xc),float)
        c=real_ls_scale(G[i],V[i])
        rr=rel_l2(V[i],c*G[i])
        co=cosine(G[i],V[i])
        gx=gradfac[i]*G[i]
        vx=gradfac[i]*V[i]
        ccx=complex_ls_scale(gx,vx)
        fit_scales.append(c); fit_resids.append(rr); fit_cos.append(co)
        per_mode.append({
            "mode_index":i,
            "k_Mpc_inv":float(k),
            "k_h_per_Mpc":float(g9.K_H[i]),
            "direct_relative_L2":rel_l2(V[i],G[i]),
            "direct_pointwise_abs_or_rel_max":aor(V[i],G[i]),
            "best_scale_v077_eq_c_GE15":c,
            "best_scale_postfit_relative_L2":rr,
            "temporal_shape_cosine":co,
            "best_complex_scale_v077_X_eq_c_GE15_X":complex_record(ccx),
            "best_complex_scale_postfit_relative_L2":rel_l2(vx,ccx*gx),
            "complex_shape_coherence":complex_shape_coherence(gx,vx),
            "Q_trace_vs_GE15_relative_L2":rel_l2(QV[i],QG[i]),
            "Q_trace_vs_GE15_pointwise_abs_or_rel_max":aor(QV[i],QG[i]),
        })

    vdirect=rel_l2(V,G)
    vpoint=aor(V,G)
    cglobal=real_ls_scale(G,V)
    global_fit=rel_l2(V,cglobal*G)
    global_cos=cosine(G,V)
    GX=gradfac[:,None]*G
    VX=gradfac[:,None]*V
    cglobal_complex=complex_ls_scale(GX,VX)
    global_complex_fit=rel_l2(VX,cglobal_complex*GX)
    q_window_rel=rel_l2(QV,QG)
    q_window_point=aor(QV,QG)

    # Explicit frozen-convention factor audit. These are diagnostics only:
    # no factor is adopted and routing remains on the original frozen gates.
    candidate={}
    candidate_names=(
        "1","-1","a","1/a","k","1/k","i*k","-i*k",
        "i*k/a","-i*k/a","a/(i*k)","Q","1/Q","H0",
        "c_light/H0","2","1/2","i","-i","k/a","a/k",
    )
    c_over_H0=(float(c4.C_M_S)/1000.0)/float(c4.H0)
    for name in candidate_names:
        F=np.empty(GX.shape,dtype=complex)
        for i,k in enumerate(g9.K_REQ):
            F[i]=candidate_factor(
                name,float(k),ac,QG[i],float(c4.H0),c_over_H0
            )*GX[i]
        cc=complex_ls_scale(F,VX)
        candidate[name]={
            "exact_factor_direct_relative_L2":rel_l2(VX,F),
            "exact_factor_complex_shape_coherence":complex_shape_coherence(F,VX),
            "best_additional_complex_scale":complex_record(cc),
            "postfit_relative_L2_after_additional_scale":rel_l2(VX,cc*F),
        }

    # k-power trend in the per-mode fitted scales.
    kk=np.asarray(g9.K_REQ,float)
    cc=np.asarray(fit_scales,float)
    mask=np.isfinite(cc)&(np.abs(cc)>TINY)
    if np.count_nonzero(mask)>=2:
        pfit=np.polyfit(np.log(kk[mask]),np.log(np.abs(cc[mask])),1)
        k_slope=float(pfit[0])
        k_intercept=float(pfit[1])
    else:
        k_slope=math.nan; k_intercept=math.nan

    qpass=q_rel_max<=Q_MAX
    algpass=alg_rel<=ALG_MAX
    ge19pass=ge19_gl_max<=GE19_GL_MAX and ge19_point_max<=GE19_POINT_MAX
    vcompatible=vdirect<=V077_DIRECT_MAX
    simplefit=global_fit<=FIT_MAX and min(fit_cos)>=COS_MIN

    if not (qpass and algpass):
        route="MIXED_OR_UNRESOLVED"
    elif not ge19pass:
        route="GE19_LOCAL_DICTIONARY_MISMATCH"
    elif vcompatible:
        route="V077_GE15_COMPATIBLE_REPAIR24_ASSEMBLY_BUG"
    elif simplefit:
        route="SIMPLE_LEGACY_NORMALIZATION_CANDIDATE"
    else:
        route="LEGACY_V077_BOUNDARY_TRACE_INCOMPATIBLE_GE15_CERTIFIED"

    result={
        "classification":"GE19_REPAIR25_FIRST_ORDER_BATH_BOUNDARY_DICTIONARY_AUDIT_COMPLETE",
        "predata_classification":"GE19_REPAIR25_PREDATA_FIRST_ORDER_BATH_BOUNDARY_DICTIONARY_AUDIT",
        "diagnostic_only":True,
        "provenance":{
            "hashes":hashes,
            "GE15_R1_dense_expected_sha256":expected_dense,
            "GE15_requested_k_relative_miss_max":km15,
            "v077_requested_k_relative_miss_max":km77,
            "v077_common_time_mismatch":tm77,
            "Repair24_unique_failed_gate":false24[0],
        },
        "exact_surface":{
            "a":A0,
            "GE15_algebraic_reference_X_vs_grad_chi_over_a_relative_L2":alg_rel,
            "GE15_algebraic_reference_X_vs_grad_chi_over_a_pointwise_abs_or_rel_max":alg_point,
            "Q_action_vs_GE15_relative_max":q_rel_max,
            "Repair22_X10_vs_GE15_relative_L2_max":ge19_gl_max,
            "Repair22_X10_vs_GE15_pointwise_abs_or_rel_max":ge19_point_max,
            "v077_vs_GE15_direct_relative_L2":init_v77_rel,
            "v077_vs_GE15_pointwise_abs_or_rel_max":init_v77_point,
            "Q_trace_vs_GE15_relative_L2":q_trace_ge15_rel,
            "Q_trace_vs_GE15_pointwise_abs_or_rel_max":q_trace_ge15_point,
            "best_global_complex_scale_v077_X_eq_c_GE15_X":complex_record(init_complex_scale),
            "best_global_complex_scale_postfit_relative_L2":init_complex_fit_resid,
            "per_mode_v077_GE15":init_rows,
            "per_C_Repair22_GE15":perC,
        },
        "overlap_window":{
            "a_min":float(ac[0]),"a_max":float(ac[-1]),"nodes":NCOMMON,
            "v077_vs_GE15_direct_relative_L2":vdirect,
            "v077_vs_GE15_pointwise_abs_or_rel_max":vpoint,
            "global_shape_cosine":global_cos,
            "best_global_scale_v077_eq_c_GE15":cglobal,
            "best_global_scale_postfit_relative_L2":global_fit,
            "best_global_complex_scale_v077_X_eq_c_GE15_X":complex_record(cglobal_complex),
            "best_global_complex_scale_postfit_relative_L2":global_complex_fit,
            "Q_trace_vs_GE15_relative_L2":q_window_rel,
            "Q_trace_vs_GE15_pointwise_abs_or_rel_max":q_window_point,
            "per_mode":per_mode,
            "per_mode_scale_abs_loglog_k_slope":k_slope,
            "per_mode_scale_abs_loglog_k_intercept":k_intercept,
            "candidate_factor_audits":candidate,
        },
        "frozen_threshold_checks":{
            "Q_action_vs_GE15_pass":qpass,
            "GE15_algebraic_identity_pass":algpass,
            "Repair22_X10_vs_GE15_pass":ge19pass,
            "v077_vs_GE15_direct_compatible":vcompatible,
            "v077_best_global_scale_closes":bool(global_fit<=FIT_MAX),
            "all_per_mode_shape_cosines_ge_0p9999":bool(min(fit_cos)>=COS_MIN),
        },
        "routing":{"next_route":route},
        "diagnostic_amendment01":{
            "expanded_complex_amplitude_ratio_phase_reporting":True,
            "expanded_complex_least_squares_fits":True,
            "explicit_Q_trace_Q_GE15_Q_action_audit":True,
            "expanded_frozen_convention_factor_tests":True,
            "routing_or_threshold_changed":False,
        },
        "next_step_constraint":"No fitted normalization is adopted here. Any replacement of the legacy v0.77 boundary must be derived and preregistered separately before q20 is rerun.",
        "q20_rerun_performed":False,
        "Z21_licensed":False,
    }
    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR25_FIRST_ORDER_BATH_BOUNDARY_DICTIONARY_AUDIT_IMPLEMENTATION_FAIL",
            "error":repr(exc),
        },indent=2))
        raise
