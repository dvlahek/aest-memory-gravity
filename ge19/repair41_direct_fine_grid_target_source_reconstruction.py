#!/usr/bin/env python3
"""GE19 Repair41 — direct fine-grid reconstruction of Repair40 target sources.

Diagnostic only.

Reconstructs the two mandatory Repair40 physical target pieces
  2M1_GE05_mapped
  2Q_GE06_cross
on Nt=382 and Nt=763 direct parent grids.  Both grids contain every original
Nt128 factor-1 two-stage Radau stage coordinate exactly, so target source
values are read by exact node lookup, with no target-source interpolation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.repair07_window_retarded_reduced_h3_z20_particular as r7
import ge19.repair11_lambda_inclusive_reduced_h1_reclosure as r11
import ge19.repair13_self_consistent_reduced_background_h1_reclosure as r13
import ge19.repair14_self_consistent_reduced_h3_z20_particular as r14
import ge19.repair18_zero_coordinate_constraint_projected_momentum_boundary as r18
import ge19.repair24_q20_construction as r24
import ge19.repair27_cancellation_free_parent_q20_reconstruction as r27
import ge19.repair32b_factor2_corrected_reduced_h2_z11_reconstruction as r32
import ge19.repair37_cancellation_safe_fd8_h4_z21_reclosure as r37
import ge19.repair39_frozen_source_stage_interpolation_localization as r39

TINY=1e-300
NT_COARSE=128
NT_FINE3=382
NT_FINE6=763
NQ=2048
NX=512
TIME_MAX=5e-3
ADAPTER_MAX=1e-12
STAGE_COORD_MAX=1e-13

R40_JSON_SHA="f5618344db31328dc4e680eb41bb6a715da3fbe7e54ddff3cb53bc027386bf44"
R40_NPZ_SHA="06c7799787abcc510259c626bcb9ca925f96efce13c7949a89690f243fbf01b5"
R37_JSON_SHA="da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a"
R37_NPZ_SHA="572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f"
R13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
R18_JSON_SHA="d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc"
R22_JSON_SHA="7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
R22_NPZ_SHA="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
R27_JSON_SHA="99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b"
R27_NPZ_SHA="2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0"
R28_NPZ_SHA="101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705"
R32A_JSON_SHA="adef8fad50233c7fa5df3d57e7f21df80ed99228402831b2861ad06256519725"
R32B_JSON_SHA="226dd2a2a0e86ddccc39a62d833960bdf9d5a9af038ad3bf225bbbf69d0b95cf"
R32B_NPZ_SHA="5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327"
R32C_JSON_SHA="037314effa33c5bfaf51f6f3c72459de43cb486c6ef5e9a94f5b1984a68611b9"
GE18_NPZ_SHA=r7.GE18_NPZ_SHA
GE15_DENSE_SHA="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"
REPAIR26_TRACE_SHA=r27.REPAIR26_R1_TRACE_SHA
REPAIR26_TRACE_BYTES=r27.REPAIR26_R1_TRACE_BYTES

TARGET_M1="2M1_GE05_mapped"
TARGET_Q6="2Q_GE06_cross"
TARGETS=(TARGET_M1,TARGET_Q6)


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def rel_l2(a,b)->float:
    aa=np.asarray(a)
    bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def complex_alignment(a,b)->float:
    aa=np.asarray(a,complex).ravel()
    bb=np.asarray(b,complex).ravel()
    den=float(np.linalg.norm(aa)*np.linalg.norm(bb))
    if den<=TINY:
        return 0.0
    return float(np.real(np.vdot(aa,bb))/den)


def load_inputs(rd:Path,repair26_trace:Path,repair28_npz:Path):
    paths={
        "r40j":rd/"ge19_repair40_piecewise_stage_source_decomposition.json",
        "r40n":rd/"ge19_repair40_piecewise_stage_source_decomposition.npz",
        "r37j":rd/"ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json",
        "r37n":rd/"ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "r18j":rd/"ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json",
        "r22j":rd/"ge19_repair22_on_shell_parent_z20_certification.json",
        "r22n":rd/"ge19_repair22_on_shell_parent_z20_certification.npz",
        "r27j":rd/"ge19_repair27_cancellation_free_parent_q20_reconstruction.json",
        "r27n":rd/"ge19_repair27_cancellation_free_parent_q20_reconstruction.npz",
        "r32aj":rd/"ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_audit.json",
        "r32bj":rd/"ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.json",
        "r32bn":rd/"ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.npz",
        "r32cj":rd/"ge19_repair32c_artifact_only_reduced_z11_certification.json",
        "ge18n":rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz",
        "dense":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "lambda":rd/"ge15_R1_cli_background.dat",
        "trace":Path(repair26_trace),
        "r28n":Path(repair28_npz),
    }
    missing=[str(v) for v in paths.values() if not v.exists()]
    if missing:
        raise RuntimeError("missing Repair41 frozen inputs: "+", ".join(missing))

    expected={
        "r40j":R40_JSON_SHA,"r40n":R40_NPZ_SHA,
        "r37j":R37_JSON_SHA,"r37n":R37_NPZ_SHA,
        "r13n":R13_NPZ_SHA,"r18j":R18_JSON_SHA,
        "r22j":R22_JSON_SHA,"r22n":R22_NPZ_SHA,
        "r27j":R27_JSON_SHA,"r27n":R27_NPZ_SHA,
        "r32aj":R32A_JSON_SHA,
        "r32bj":R32B_JSON_SHA,"r32bn":R32B_NPZ_SHA,
        "r32cj":R32C_JSON_SHA,
        "ge18n":GE18_NPZ_SHA,"dense":GE15_DENSE_SHA,
        "trace":REPAIR26_TRACE_SHA,"r28n":R28_NPZ_SHA,
    }
    hashes={}
    for key,want in expected.items():
        got=sha256(paths[key])
        hashes[key]=got
        if got!=want:
            raise RuntimeError(f"{key} hash mismatch: {got} != {want}")
    if paths["trace"].stat().st_size!=REPAIR26_TRACE_BYTES:
        raise RuntimeError("Repair26 trace byte mismatch")

    j40=json.loads(paths["r40j"].read_text())
    if j40.get("classification")!="GE19_REPAIR40_PIECEWISE_STAGE_SOURCE_DECOMPOSITION_COMPLETE":
        raise RuntimeError("Repair40 classification mismatch")
    if j40.get("routing",{}).get("next_route")!="PIECEWISE_STAGE_SOURCE_DECOMPOSITION_COMPLETE":
        raise RuntimeError("Repair40 route mismatch")
    tgt=j40.get("deterministic_next_target",{}).get("mandatory_followup_targets")
    if tgt!=[TARGET_M1,TARGET_Q6]:
        raise RuntimeError(f"Repair40 target mismatch: {tgt}")

    j22=json.loads(paths["r22j"].read_text())
    j27=json.loads(paths["r27j"].read_text())
    j32a=json.loads(paths["r32aj"].read_text())
    j32b=json.loads(paths["r32bj"].read_text())
    j32c=json.loads(paths["r32cj"].read_text())
    if j22.get("Z20_certified") is not True:
        raise RuntimeError("Repair22 Z20 not certified")
    if j27.get("q20_certified_projection") is not True:
        raise RuntimeError("Repair27 q20 not certified")
    if j32a.get("classification")!="GE19_REPAIR32A_GE06_GE05_RAW_RESIDUAL_NORMALIZATION_DICTIONARY_PASS":
        raise RuntimeError("Repair32A dictionary not PASS")
    if j32b.get("classification")!="GE19_REPAIR32B_FACTOR2_CORRECTED_REDUCED_H2_Z11_RECONSTRUCTION_PASS":
        raise RuntimeError("Repair32B not PASS")
    if j32c.get("Z11_certified") is not True:
        raise RuntimeError("Repair32C Z11 not certified")

    return (
        paths,hashes,
        np.load(paths["r40n"]),
        np.load(paths["r37n"]),
        np.load(paths["r13n"]),
        np.load(paths["r22n"]),
        np.load(paths["r27n"]),
        np.load(paths["r32bn"]),
        np.load(paths["ge18n"]),
        np.load(paths["r28n"]),
    )


def build_generators():
    mod6f=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r41"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6f)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r41"
    )
    ge05=r24.load_quiet(
        ROOT/"ge05/memory_directional_source_generator.py","ge05r41"
    )
    normf,normdiag=r24.build_normalized_c2_generator(ge05)
    qdirect=r37.build_direct_bilinear_generators(mod6f,mod6,mod7)
    return mod6,mod7,ge05,normf,normdiag,qdirect


def build_grid_context(rd:Path,nt:int,z13):
    base,base_state,jets=r7.build_ge15_reference(
        rd/"ge15_R1_dense_accepted_step_trace.dat",nt
    )
    rho=r11.interp_lambda(
        rd/"ge15_R1_cli_background.dat",np.asarray(base["x"],float)
    )
    bgs={}
    for tag in r7.C_TAGS:
        bgs[tag],_=r13.reduced_background(r7,base,tag,rho)
    return base,base_state,jets,rho,bgs


def solve_h1(mod6,mod7,bg,jets,ge18,tag):
    ref,refdot=r7.reference_reduced_mode_state(bg,jets,ge18,tag)
    return r7.solve_reduced_h1_case_canonical(mod6,mod7,bg,tag,ref,refdot)


def solve_z20(mod6,mod7,bg,rho,tag,h1,h1dot):
    source=r14.source_bundle_reduced_lambda(
        r7,mod6,mod7,bg,rho,tag,r7.NX_PRIMARY,h1,h1dot
    )
    x=np.asarray(bg["x"],float)
    nb=len(r7.BETAS)
    nm=len(r7.M_SOLVE)
    nt=len(x)
    states=np.empty((nb,nm,6,nt),complex)
    finite=True
    linmax=0.0

    for jm,m in enumerate(r7.M_SOLVE):
        k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
        rhsfun,confun=r7._source_interp(x,source,m)
        r0=np.asarray(rhsfun(float(x[0])),complex)
        c0=np.asarray(confun(float(x[0])),complex)
        if r0.ndim==1: r0=r0[:,None]
        if c0.ndim==1: c0=c0[:,None]

        M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
            mod6,mod7,bg,tag,k,float(x[0])
        )
        y0=np.zeros((8,nb),complex)
        for ib,beta in enumerate(r7.BETAS):
            source0=np.concatenate([r0[:,ib],c0[:,ib]])
            woff=WR@source0
            lr=Cmat[4]
            sr=Cmat[10]+Cmat[11]
            A=np.vstack([lr@WY,sr@WY])[:,4:8]
            b=np.asarray([
                r0[0,ib]-lr@woff,
                c0[0,ib]-sr@woff,
            ],complex)
            p,sd=r18.projected_momentum_solve(A,b)
            y0[4:8,ib]=p
            linmax=max(linmax,float(sd["scaled_relative_residual_final"]))

        Y,rdiag=r7._radau2_integrate_canonical(
            mod6,mod7,bg,tag,k,y0,rhsfun,confun
        )
        st,dd,odiag=r7._reconstruct_canonical_solution(
            mod6,mod7,bg,tag,k,Y,rhsfun,confun
        )
        states[:,jm]=st
        linmax=max(
            linmax,
            float(rdiag["radau_block_scaled_relative_L2_residual_max"]),
            float(odiag["algebraic_scaled_relative_L2_residual_max"]),
            float(odiag["lapse_noether_row_relative_residual_max"]),
        )
        finite=bool(
            finite and np.all(np.isfinite(Y)) and np.all(np.isfinite(st))
        )
    return states,{"linear_residual_max":float(linmax),"all_outputs_finite":finite}


def construct_q20_direct(normf,bg,h1,h1dot,z20,boundary):
    r=np.asarray(boundary["r"],float)
    w=np.asarray(boundary["w"],float)
    if len(r)!=NQ:
        raise RuntimeError("Repair41 q20 quadrature mismatch")
    tau=r24.TAUH0/float(r7.g9.H0_CLASS)

    X10=r24.first_order_X_modes(r7,bg,h1)
    z10,v10=r24.evolve_z10(
        r7.c4,bg,X10,boundary["z0"],boundary["v0"],r,tau
    )
    wz10=np.einsum("b,bmt->mt",w,z10,optimize=True)
    X20=r24.X20_modes(r7,bg,z20)
    metric=r24.metric_real_fields(r7,bg,h1,h1dot,NX)

    wz20=np.zeros_like(X20)
    finite=True
    max_xeff=0.0
    for j0 in range(0,NQ,r24.CHUNK):
        j1=min(NQ,j0+r24.CHUNK)
        rc=r[j0:j1]
        wc=w[j0:j1]
        zc=z10[j0:j1]
        vc=v10[j0:j1]
        g2=r24.normalized_g2_chunk(
            normf,r7,bg,metric,zc,vc,rc,tau,NX
        )
        zs,vs,xeff=r24.solve_z20_chunk(bg,X20,g2,rc,tau)
        wz20 += np.einsum("b,bcmt->cmt",wc,zs,optimize=True)
        max_xeff=max(max_xeff,float(np.max(np.abs(xeff))))
        finite=bool(
            finite and np.all(np.isfinite(g2))
            and np.all(np.isfinite(zs)) and np.all(np.isfinite(vs))
        )

    return {
        "weighted_z10":wz10,
        "weighted_z20":wz20,
        "X20":X20,
        "B20_linear":X20-wz20,
        "effective_drive_abs_max":float(max_xeff),
        "all_outputs_finite":bool(finite),
    }


def solve_z11(mod6,mod7,bg,base,base_state,fields,h1,wz10,tag):
    dust,std_dr,std_mom=r32.integrate_dust_tangent(bg,base_state,fields)
    ref,refdot=r32.make_reference(bg,base,fields,dust)
    X=r32.first_order_X(bg,h1)
    B10=X-wz10
    source=r32.source_from_B(bg,B10)
    st,dd,diag=r32.solve_h2_case(
        mod6,mod7,bg,tag,source,ref,refdot
    )
    return st,dd,diag,B10


def target_q6(qdirect,bg,tag,h1,h1dot,z11,z11dot):
    ga_m,ga_c,ma_m,ma_c=r37.q_cross_direct(
        qdirect,bg,tag,h1,h1dot,z11,z11dot,r37.NX_POLY
    )
    main=-2.0*r37.fft_low(ga_m)
    con=-2.0*r37.fft_low(ga_c)
    nb=len(r7.BETAS)
    return (
        np.repeat(main[None,...],nb,axis=0),
        np.repeat(con[None,...],nb,axis=0),
    )


def target_m1(bg,B20):
    return r37.m1_mapped_fourier(bg,B20)


def frozen_target_by_beta(r37npz,tag,piece):
    out={}
    for ib,beta in enumerate(r7.BETAS):
        out[float(beta)]={
            "rhs":np.asarray(
                r37npz[f"primary_{tag}_beta{ib}_{piece}_main"],complex
            ),
            "rhs_constraint":np.asarray(
                r37npz[f"primary_{tag}_beta{ib}_{piece}_constraint"],complex
            ),
        }
    return out


def stack_target_from_frozen(r37npz,tag,piece):
    rows=[]
    cons=[]
    for ib,beta in enumerate(r7.BETAS):
        rows.append(np.asarray(
            r37npz[f"primary_{tag}_beta{ib}_{piece}_main"],complex
        ))
        cons.append(np.asarray(
            r37npz[f"primary_{tag}_beta{ib}_{piece}_constraint"],complex
        ))
    return np.stack(rows,axis=0),np.stack(cons,axis=0)


def formula_adapter_controls(rd,z22,z27,z32b,z37,qdirect):
    base,_,_=r7.build_ge15_reference(
        rd/"ge15_R1_dense_accepted_step_trace.dat",NT_COARSE
    )
    rho=r11.interp_lambda(
        rd/"ge15_R1_cli_background.dat",np.asarray(base["x"],float)
    )
    m1_num=[]; m1_ref=[]; q6_num=[]; q6_ref=[]
    for tag in r7.C_TAGS:
        bg,_=r13.reduced_background(r7,base,tag,rho)
        m1=target_m1(bg,np.asarray(z27[f"{tag}_B20_linear_primary"],complex))
        q6=target_q6(
            qdirect,bg,tag,
            np.asarray(z22[f"{tag}_H1_primary"],complex),
            np.asarray(z22[f"{tag}_H1dot_primary"],complex),
            np.asarray(z32b[f"{tag}_Z11_primary"],complex),
            np.asarray(z32b[f"{tag}_Z11dot_primary"],complex),
        )
        for piece,val,aa,bb in (
            (TARGET_M1,m1,m1_num,m1_ref),
            (TARGET_Q6,q6,q6_num,q6_ref),
        ):
            ref=stack_target_from_frozen(z37,tag,piece)
            aa.extend([val[0].ravel(),val[1].ravel()])
            bb.extend([ref[0].ravel(),ref[1].ravel()])
    return {
        TARGET_M1:rel_l2(np.concatenate(m1_num),np.concatenate(m1_ref)),
        TARGET_Q6:rel_l2(np.concatenate(q6_num),np.concatenate(q6_ref)),
    }


def coarse_stage_coordinates(x128):
    x=np.asarray(x128,float)
    out=[]
    for i in range(len(x)-1):
        h=float(x[i+1]-x[i])
        out.extend([float(x[i]+h/3.0),float(x[i+1])])
    return np.asarray(out,float)


def stage_indices(xfine,x128,mult):
    xfine=np.asarray(xfine,float)
    x128=np.asarray(x128,float)
    idx=[]
    coords=[]
    for i in range(len(x128)-1):
        idx.extend([mult*i+mult//3,mult*(i+1)])
        h=float(x128[i+1]-x128[i])
        coords.extend([float(x128[i]+h/3.0),float(x128[i+1])])
    idx=np.asarray(idx,int)
    coords=np.asarray(coords,float)
    if np.any(idx<0) or np.any(idx>=len(xfine)):
        raise RuntimeError("Repair41 stage index out of range")
    err=float(np.max(np.abs(xfine[idx]-coords)))
    return idx,coords,err


def extract_time(arr,idx):
    a=np.asarray(arr)
    return np.take(a,idx,axis=-1)


def extract_target_stage(pair,idx):
    main,con=pair
    # target arrays: [beta,row,time,mode]
    return (
        np.take(np.asarray(main),idx,axis=2)[...,1:41],
        np.take(np.asarray(con),idx,axis=2)[...,1:41],
    )


def concat_pair(pair):
    return np.concatenate([
        np.asarray(pair[0],complex).ravel(),
        np.asarray(pair[1],complex).ravel(),
    ])


def frozen_stage_representation(x128,z37,tag,piece,method,xx):
    bybeta=frozen_target_by_beta(z37,tag,piece)
    nb=len(r7.BETAS)
    ns=len(xx)
    nm=len(r7.M_SOLVE)
    main=np.empty((nb,6,ns,nm),complex)
    con=np.empty((nb,2,ns,nm),complex)
    for jm,m in enumerate(r7.M_SOLVE):
        rf,cf=r39.source_interp(x128,bybeta,m,method)
        rr=np.asarray(rf(xx),complex) # [row,stage,beta]
        cc=np.asarray(cf(xx),complex)
        main[:,:,:,jm]=np.transpose(rr,(2,0,1))
        con[:,:,:,jm]=np.transpose(cc,(2,0,1))
    return main,con


def build_direct_grid(
    rd,nt,mod6,mod7,normf,qdirect,ge18,z28,boundary
):
    base,base_state,jets,rho,bgs=build_grid_context(rd,nt,None)
    x=np.asarray(base["x"],float)
    xR2,R2,chiR2=r32.load_r2_parent(z28)
    fields=r32.tangent_on_grid(xR2,R2,x)

    out={}
    finite=True
    diagnostics={}
    for tag in r7.C_TAGS:
        bg=bgs[tag]
        h1,h1dot,h1diag=solve_h1(mod6,mod7,bg,jets,ge18,tag)
        z20,z20diag=solve_z20(mod6,mod7,bg,rho,tag,h1,h1dot)
        q20=construct_q20_direct(normf,bg,h1,h1dot,z20,boundary)
        z11,z11dot,z11diag,B10=solve_z11(
            mod6,mod7,bg,base,base_state,fields,h1,q20["weighted_z10"],tag
        )
        q6=target_q6(qdirect,bg,tag,h1,h1dot,z11,z11dot)
        m1=target_m1(bg,q20["B20_linear"])

        finite=bool(
            finite and h1diag["all_outputs_finite"]
            and z20diag["all_outputs_finite"]
            and q20["all_outputs_finite"]
            and z11diag["all_outputs_finite"]
            and np.all(np.isfinite(q6[0])) and np.all(np.isfinite(q6[1]))
            and np.all(np.isfinite(m1[0])) and np.all(np.isfinite(m1[1]))
        )
        out[tag]={
            "h1":h1,"h1dot":h1dot,
            "z20":z20,
            "weighted_z10":q20["weighted_z10"],
            "weighted_z20":q20["weighted_z20"],
            "B20_linear":q20["B20_linear"],
            "z11":z11,"z11dot":z11dot,
            TARGET_Q6:q6,
            TARGET_M1:m1,
        }
        diagnostics[tag]={
            "H1_linear_residual_max":float(h1diag["linear_system_relative_L2_max"]),
            "Z20_linear_residual_max":float(z20diag["linear_residual_max"]),
            "Z11_linear_residual_max":float(z11diag["linear_system_relative_L2_max"]),
            "q20_effective_drive_abs_max":float(q20["effective_drive_abs_max"]),
        }
    return {
        "nt":nt,"x":x,"base":base,"out":out,
        "all_outputs_finite":finite,"diagnostics":diagnostics,
    }


def paired_stage_rel(g3,g6,idx3,idx6,key):
    a=[]; b=[]
    for tag in r7.C_TAGS:
        if key in (TARGET_M1,TARGET_Q6):
            p3=extract_target_stage(g3["out"][tag][key],idx3)
            p6=extract_target_stage(g6["out"][tag][key],idx6)
            a.append(concat_pair(p3)); b.append(concat_pair(p6))
        else:
            a.append(extract_time(g3["out"][tag][key],idx3).ravel())
            b.append(extract_time(g6["out"][tag][key],idx6).ravel())
    return rel_l2(np.concatenate(a),np.concatenate(b))


def target_comparison(g6,idx6,x128,z37,xx,piece):
    direct=[]
    pchip=[]
    akima=[]
    for tag in r7.C_TAGS:
        d=extract_target_stage(g6["out"][tag][piece],idx6)
        p=frozen_stage_representation(x128,z37,tag,piece,"PCHIP",xx)
        a=frozen_stage_representation(x128,z37,tag,piece,"AKIMA",xx)
        direct.append(concat_pair(d))
        pchip.append(concat_pair(p))
        akima.append(concat_pair(a))
    dd=np.concatenate(direct)
    pp=np.concatenate(pchip)
    aa=np.concatenate(akima)
    dp=dd-pp
    ap=aa-pp
    ep=rel_l2(pp,dd)
    ea=rel_l2(aa,dd)
    return {
        "PCHIP_vs_direct763_relative_L2":float(ep),
        "AKIMA_vs_direct763_relative_L2":float(ea),
        "closer_frozen_representation":"PCHIP" if ep<ea else ("AKIMA" if ea<ep else "TIE"),
        "PCHIP_to_AKIMA_delta_alignment_with_PCHIP_to_direct_delta":
            complex_alignment(ap,dp),
        "PCHIP_to_direct_delta_L2":float(np.linalg.norm(dp)),
        "PCHIP_to_AKIMA_delta_L2":float(np.linalg.norm(ap)),
        "direct763_L2":float(np.linalg.norm(dd)),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--repair26-trace",required=True)
    ap.add_argument("--repair28-npz",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    rd=Path(args.results_dir)
    (
        paths,hashes,z40,z37,z13,z22,z27,z32b,ge18,z28
    )=load_inputs(rd,Path(args.repair26_trace),Path(args.repair28_npz))

    mod6,mod7,ge05,normf,normdiag,qdirect=build_generators()
    adapters=formula_adapter_controls(rd,z22,z27,z32b,z37,qdirect)

    # Build all fine backgrounds first, then install one Lambda wrapper over
    # the exact fine-grid rho arrays used by those backgrounds.
    contexts={}
    lambda_by_bg={}
    for nt in (NT_FINE3,NT_FINE6):
        base,base_state,jets,rho,bgs=build_grid_context(rd,nt,z13)
        contexts[nt]=(base,base_state,jets,rho,bgs)
        for tag in r7.C_TAGS:
            lambda_by_bg[id(bgs[tag])]=rho
    r11.install_lambda_operator(r7,lambda_by_bg)
    if r32.r7 is not r7:
        raise RuntimeError("Repair32B and Repair41 do not share Repair07 module object")

    r24.TRACE_LO_A=r27.REPAIR26_TRACE_LO_A
    r24.TRACE_HI_A=r27.REPAIR26_TRACE_HI_A
    boundary=r24.full_history_boundary(
        r7.c4,r7,Path(args.repair26_trace),NQ
    )

    # build_direct_grid reconstructs its context; bind its new backgrounds to
    # the already-installed Lambda wrapper by using a local builder below.
    def build_bound(nt):
        base,base_state,jets,rho,bgs=contexts[nt]
        x=np.asarray(base["x"],float)
        xR2,R2,chiR2=r32.load_r2_parent(z28)
        fields=r32.tangent_on_grid(xR2,R2,x)
        out={}; finite=True; diagnostics={}
        for tag in r7.C_TAGS:
            bg=bgs[tag]
            h1,h1dot,h1diag=solve_h1(mod6,mod7,bg,jets,ge18,tag)
            z20,z20diag=solve_z20(mod6,mod7,bg,rho,tag,h1,h1dot)
            q20=construct_q20_direct(normf,bg,h1,h1dot,z20,boundary)
            z11,z11dot,z11diag,B10=solve_z11(
                mod6,mod7,bg,base,base_state,fields,h1,q20["weighted_z10"],tag
            )
            q6=target_q6(qdirect,bg,tag,h1,h1dot,z11,z11dot)
            m1=target_m1(bg,q20["B20_linear"])
            finite=bool(
                finite and h1diag["all_outputs_finite"]
                and z20diag["all_outputs_finite"]
                and q20["all_outputs_finite"]
                and z11diag["all_outputs_finite"]
                and np.all(np.isfinite(q6[0])) and np.all(np.isfinite(q6[1]))
                and np.all(np.isfinite(m1[0])) and np.all(np.isfinite(m1[1]))
            )
            out[tag]={
                "h1":h1,"h1dot":h1dot,
                "z20":z20,
                "weighted_z10":q20["weighted_z10"],
                "weighted_z20":q20["weighted_z20"],
                "B20_linear":q20["B20_linear"],
                "z11":z11,"z11dot":z11dot,
                TARGET_Q6:q6,TARGET_M1:m1,
            }
            diagnostics[tag]={
                "H1_linear_residual_max":float(h1diag["linear_system_relative_L2_max"]),
                "Z20_linear_residual_max":float(z20diag["linear_residual_max"]),
                "Z11_linear_residual_max":float(z11diag["linear_system_relative_L2_max"]),
                "q20_effective_drive_abs_max":float(q20["effective_drive_abs_max"]),
            }
        return {"nt":nt,"x":x,"out":out,"all_outputs_finite":finite,"diagnostics":diagnostics}

    g3=build_bound(NT_FINE3)
    g6=build_bound(NT_FINE6)

    x128=np.asarray(z37["x_primary"],float)
    idx3,xx3,err3=stage_indices(g3["x"],x128,3)
    idx6,xx6,err6=stage_indices(g6["x"],x128,6)
    stage_err=max(err3,err6,float(np.max(np.abs(xx3-xx6))))

    resolution={
        "Z10_stage_relative_L2":paired_stage_rel(g3,g6,idx3,idx6,"h1"),
        "Z20_stage_relative_L2":paired_stage_rel(g3,g6,idx3,idx6,"z20"),
        "weighted_z20_stage_relative_L2":paired_stage_rel(g3,g6,idx3,idx6,"weighted_z20"),
        "Z11_stage_relative_L2":paired_stage_rel(g3,g6,idx3,idx6,"z11"),
        TARGET_M1+"_stage_source_relative_L2":paired_stage_rel(g3,g6,idx3,idx6,TARGET_M1),
        TARGET_Q6+"_stage_source_relative_L2":paired_stage_rel(g3,g6,idx3,idx6,TARGET_Q6),
    }

    comparisons={
        TARGET_M1:target_comparison(g6,idx6,x128,z37,xx6,TARGET_M1),
        TARGET_Q6:target_comparison(g6,idx6,x128,z37,xx6,TARGET_Q6),
    }

    implementation_gates={
        "frozen_parent_hashes_exact":True,
        "Nt128_formula_adapter_2M1_vs_Repair37_target_relative_L2_le_1e12":
            bool(adapters[TARGET_M1]<=ADAPTER_MAX),
        "Nt128_formula_adapter_2Q_GE06_vs_Repair37_target_relative_L2_le_1e12":
            bool(adapters[TARGET_Q6]<=ADAPTER_MAX),
        "fine_stage_coordinate_exact_abs_le_1e13":bool(stage_err<=STAGE_COORD_MAX),
        "all_outputs_finite":bool(g3["all_outputs_finite"] and g6["all_outputs_finite"]),
    }
    resolution_gates={
        "fine382_vs_fine763_Z10_stage_relative_L2_le_5e3":
            bool(resolution["Z10_stage_relative_L2"]<=TIME_MAX),
        "fine382_vs_fine763_Z20_stage_relative_L2_le_5e3":
            bool(resolution["Z20_stage_relative_L2"]<=TIME_MAX),
        "fine382_vs_fine763_weighted_z20_stage_relative_L2_le_5e3":
            bool(resolution["weighted_z20_stage_relative_L2"]<=TIME_MAX),
        "fine382_vs_fine763_Z11_stage_relative_L2_le_5e3":
            bool(resolution["Z11_stage_relative_L2"]<=TIME_MAX),
        "fine382_vs_fine763_2M1_stage_source_relative_L2_le_5e3":
            bool(resolution[TARGET_M1+"_stage_source_relative_L2"]<=TIME_MAX),
        "fine382_vs_fine763_2Q_GE06_stage_source_relative_L2_le_5e3":
            bool(resolution[TARGET_Q6+"_stage_source_relative_L2"]<=TIME_MAX),
    }

    impl_ok=bool(all(implementation_gates.values()))
    res_ok=bool(all(resolution_gates.values()))
    if not impl_ok:
        classification="GE19_REPAIR41_DIRECT_FINE_GRID_TARGET_SOURCE_RECONSTRUCTION_IMPLEMENTATION_FAIL"
        route="IMPLEMENTATION_FAIL"
    elif res_ok:
        classification="GE19_REPAIR41_DIRECT_FINE_GRID_TARGET_SOURCE_RECONSTRUCTION_COMPLETE"
        route="DIRECT_TARGET_REFERENCE_RESOLVED"
    else:
        classification="GE19_REPAIR41_DIRECT_FINE_GRID_TARGET_SOURCE_RECONSTRUCTION_COMPLETE"
        route="DIRECT_TARGET_REFERENCE_UNRESOLVED"

    report={
        "classification":classification,
        "predata_classification":"GE19_REPAIR41_PREDATA_DIRECT_FINE_GRID_TARGET_SOURCE_RECONSTRUCTION",
        "diagnostic_only":True,
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "provenance":{"input_sha256":hashes},
        "direct_time_grids":{
            "coarse_reference_Nt":NT_COARSE,
            "fine_primary_Nt":NT_FINE3,
            "fine_control_Nt":NT_FINE6,
            "factor1_stage_coordinate_abs_error_max":float(stage_err),
            "stage_count":int(len(xx6)),
        },
        "formula_adapter_reproduction":{
            TARGET_M1+"_relative_L2":float(adapters[TARGET_M1]),
            TARGET_Q6+"_relative_L2":float(adapters[TARGET_Q6]),
        },
        "direct_parent_and_target_resolution":resolution,
        "direct763_vs_frozen_stage_representations":comparisons,
        "fine_grid_diagnostics":{
            "Nt382":g3["diagnostics"],
            "Nt763":g6["diagnostics"],
            "normalized_GE05_generator":normdiag,
        },
        "implementation_gates":implementation_gates,
        "resolution_gates":resolution_gates,
        "routing":{
            "next_route":route,
            "if_resolved":"PREREGISTER_REPAIR42_DIRECT_TARGET_H4_PROPAGATION_DIAGNOSTIC",
        },
        "Z21_window_local_particular_certified":False,
        "H4_Z21_reclosure_performed":False,
        "lensing_licensed":False,
        "claim_boundary":"Repair41 directly reconstructs only the two mandatory Repair40 target source pieces on finer parent grids and compares them at exact original factor-1 Radau stage nodes. It does not solve H4/Z21, change any science threshold, introduce finite eta, use observations, or license lensing."
    }

    outj=Path(args.json_out)
    outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")

    save={
        "x128":x128,
        "stage_x":xx6,
        "fine382_stage_indices":idx3,
        "fine763_stage_indices":idx6,
    }
    for tag in r7.C_TAGS:
        for piece in TARGETS:
            p3=extract_target_stage(g3["out"][tag][piece],idx3)
            p6=extract_target_stage(g6["out"][tag][piece],idx6)
            save[f"{tag}_{piece}_direct382_main"]=p3[0]
            save[f"{tag}_{piece}_direct382_constraint"]=p3[1]
            save[f"{tag}_{piece}_direct763_main"]=p6[0]
            save[f"{tag}_{piece}_direct763_constraint"]=p6[1]
            for method in ("PCHIP","AKIMA"):
                fp=frozen_stage_representation(x128,z37,tag,piece,method,xx6)
                save[f"{tag}_{piece}_{method.lower()}_main"]=fp[0]
                save[f"{tag}_{piece}_{method.lower()}_constraint"]=fp[1]
    np.savez_compressed(outn,**save)

    print(json.dumps(report,indent=2,allow_nan=False))
    if not impl_ok:
        raise SystemExit(3)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR41_DIRECT_FINE_GRID_TARGET_SOURCE_RECONSTRUCTION_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Z21_window_local_particular_certified":False,
            "H4_Z21_reclosure_performed":False,
            "lensing_licensed":False
        },indent=2))
        raise
