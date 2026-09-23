#!/usr/bin/env python3
"""GE19 Repair42 — direct-target H4 propagation diagnostic.

Diagnostic only.

Use the frozen Repair37 PCHIP total H4 source and projected p0, then replace
only the two mandatory Repair40 target pieces at the original Nt128 factor-1
Radau stages by the resolved Repair41 direct382/direct763 values.

No Z21 certification is permitted here.
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
import ge19.repair38_frozen_source_radau_substep_localization as r38
import ge19.repair39_frozen_source_stage_interpolation_localization as r39

TINY=1e-300
SHIFT_TARGET=1e-6
ACTIVE_COUNT=23850
STAGE_X_MAX=1e-13
TARGET_PCHIP_REPRO_MAX=1e-12
BASELINE_STATE_REPRO_MAX=1e-11
BASELINE_SHIFT_REPRO_MAX=1e-10

R41_JSON_SHA="1b18fede26b021e077ffe5c8b6b7ff0dc727b4defaab48e63491c86d868d1320"
R41_NPZ_SHA="6bfb87ea21d55e2a1d2b16aee9bc8d7246111f91a064a78b74d2ed946ec2ba45"
R37_JSON_SHA=r38.R37_JSON_SHA
R37_NPZ_SHA=r38.R37_NPZ_SHA
R13_NPZ_SHA=r38.R13_NPZ_SHA
GE15_DENSE_SHA=r38.GE15_DENSE_SHA

M1="2M1_GE05_mapped"
Q6="2Q_GE06_cross"
TARGETS=(M1,Q6)

VARIANTS=(
    "PCHIP_BASELINE",
    "DIRECT382_M1_ONLY",
    "DIRECT382_Q_GE06_ONLY",
    "DIRECT382_BOTH",
    "DIRECT763_M1_ONLY",
    "DIRECT763_Q_GE06_ONLY",
    "DIRECT763_BOTH",
)


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


def factor1_stage_x(x):
    xx=np.asarray(x,float)
    out=[]
    for i in range(len(xx)-1):
        h=float(xx[i+1]-xx[i])
        out.extend([float(xx[i]+h/3.0),float(xx[i+1])])
    return np.asarray(out,float)


def load_inputs(rd:Path):
    paths={
        "r41j":rd/"ge19_repair41_direct_fine_grid_target_source_reconstruction.json",
        "r41n":rd/"ge19_repair41_direct_fine_grid_target_source_reconstruction.npz",
        "r37j":rd/"ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json",
        "r37n":rd/"ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "dense":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "lambda":rd/"ge15_R1_cli_background.dat",
    }
    missing=[str(p) for p in paths.values() if not p.exists()]
    if missing:
        raise RuntimeError("missing Repair42 frozen inputs: "+", ".join(missing))

    expected={
        "r41j":R41_JSON_SHA,"r41n":R41_NPZ_SHA,
        "r37j":R37_JSON_SHA,"r37n":R37_NPZ_SHA,
        "r13n":R13_NPZ_SHA,"dense":GE15_DENSE_SHA,
    }
    hashes={}
    for key,want in expected.items():
        got=sha256(paths[key]); hashes[key]=got
        if got!=want:
            raise RuntimeError(f"{key} hash mismatch: {got} != {want}")

    j41=json.loads(paths["r41j"].read_text())
    j37=json.loads(paths["r37j"].read_text())
    if j41.get("classification")!="GE19_REPAIR41_DIRECT_FINE_GRID_TARGET_SOURCE_RECONSTRUCTION_COMPLETE":
        raise RuntimeError("Repair41 classification mismatch")
    if j41.get("routing",{}).get("next_route")!="DIRECT_TARGET_REFERENCE_RESOLVED":
        raise RuntimeError("Repair41 direct target reference not resolved")
    if j37.get("classification")!="GE19_REPAIR37_CANCELLATION_SAFE_FD8_H4_Z21_RECLOSURE_FAIL":
        raise RuntimeError("Repair37 classification mismatch")

    return (
        paths,hashes,j41,j37,
        np.load(paths["r41n"]),
        np.load(paths["r37n"]),
        np.load(paths["r13n"]),
    )


def frozen_piece_by_beta(r37npz,tag,piece):
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


def saved_stage_pair(r41npz,tag,piece,resolution_or_pchip,jm):
    if resolution_or_pchip=="PCHIP":
        stem="pchip"
    elif resolution_or_pchip in (382,763):
        stem=f"direct{resolution_or_pchip}"
    else:
        raise ValueError(resolution_or_pchip)
    main=np.asarray(
        r41npz[f"{tag}_{piece}_{stem}_main"],complex
    )[:,:,:,jm]       # [beta,row,stage]
    con=np.asarray(
        r41npz[f"{tag}_{piece}_{stem}_constraint"],complex
    )[:,:,:,jm]       # [beta,row,stage]
    return main,con


def pchip_target_reproduction(r41npz,r37npz,xref,stage_x):
    num=[]
    ref=[]
    for tag in r7.C_TAGS:
        for piece in TARGETS:
            bybeta=frozen_piece_by_beta(r37npz,tag,piece)
            for jm,m in enumerate(r7.M_SOLVE):
                rf,cf=r39.source_interp(xref,bybeta,m,"PCHIP")
                rr=np.asarray(rf(stage_x),complex)   # [row,stage,beta]
                cc=np.asarray(cf(stage_x),complex)
                sm,sc=saved_stage_pair(r41npz,tag,piece,"PCHIP",jm)
                num.extend([
                    np.transpose(sm,(1,2,0)).ravel(),
                    np.transpose(sc,(1,2,0)).ravel(),
                ])
                ref.extend([rr.ravel(),cc.ravel()])
    return rel_l2(np.concatenate(num),np.concatenate(ref))


def parse_variant(name):
    if name=="PCHIP_BASELINE":
        return None,()
    if name.startswith("DIRECT382_"):
        res=382
    elif name.startswith("DIRECT763_"):
        res=763
    else:
        raise ValueError(name)
    if name.endswith("M1_ONLY"):
        pieces=(M1,)
    elif name.endswith("Q_GE06_ONLY"):
        pieces=(Q6,)
    elif name.endswith("BOTH"):
        pieces=(M1,Q6)
    else:
        raise ValueError(name)
    return res,pieces


def stage_locator(stage_x,x0):
    sx=np.asarray(stage_x,float)
    def locate(xq):
        q=float(xq)
        if abs(q-float(x0))<=STAGE_X_MAX:
            return -1
        j=int(np.searchsorted(sx,q))
        candidates=[]
        if 0<=j<len(sx): candidates.append(j)
        if 0<=j-1<len(sx): candidates.append(j-1)
        if not candidates:
            raise RuntimeError(f"Repair42 stage lookup out of range x={q}")
        k=min(candidates,key=lambda ii:abs(float(sx[ii])-q))
        if abs(float(sx[k])-q)>STAGE_X_MAX:
            raise RuntimeError(
                f"Repair42 source requested away from frozen factor1 stage/node: "
                f"x={q} nearest={sx[k]} err={abs(float(sx[k])-q)}"
            )
        return int(k)
    return locate


def source_functions(
    variant,xref,stage_x,r41npz,r37npz,tag,jm
):
    total=r38.frozen_source_by_beta(r37npz,tag)
    m=int(r7.M_SOLVE[jm])
    base_rhs,base_con=r7._source_interp(xref,total,m)
    res,pieces=parse_variant(variant)

    if res is None:
        return base_rhs,base_con

    locate=stage_locator(stage_x,xref[0])
    deltas=[]
    for piece in pieces:
        dm,dc=saved_stage_pair(r41npz,tag,piece,res,jm)
        pm,pc=saved_stage_pair(r41npz,tag,piece,"PCHIP",jm)
        deltas.append((dm-pm,dc-pc))

    def rhsfun(xq):
        out=np.asarray(base_rhs(float(xq)),complex)
        k=locate(xq)
        if k>=0:
            for dm,dc in deltas:
                out=out+np.asarray(dm[:,:,k],complex).T
        return out

    def confun(xq):
        out=np.asarray(base_con(float(xq)),complex)
        k=locate(xq)
        if k>=0:
            for dm,dc in deltas:
                out=out+np.asarray(dc[:,:,k],complex).T
        return out

    return rhsfun,confun


def delta_source_functions(
    variant,xref,stage_x,r41npz,tag,jm
):
    res,pieces=parse_variant(variant)
    if res is None:
        raise ValueError("baseline has no delta source")
    locate=stage_locator(stage_x,xref[0])
    deltas=[]
    for piece in pieces:
        dm,dc=saved_stage_pair(r41npz,tag,piece,res,jm)
        pm,pc=saved_stage_pair(r41npz,tag,piece,"PCHIP",jm)
        deltas.append((dm-pm,dc-pc))

    def rhsfun(xq):
        k=locate(xq)
        if k<0:
            return np.zeros((6,len(r7.BETAS)),complex)
        out=np.zeros((6,len(r7.BETAS)),complex)
        for dm,dc in deltas:
            out=out+np.asarray(dm[:,:,k],complex).T
        return out

    def confun(xq):
        k=locate(xq)
        if k<0:
            return np.zeros((2,len(r7.BETAS)),complex)
        out=np.zeros((2,len(r7.BETAS)),complex)
        for dm,dc in deltas:
            out=out+np.asarray(dc[:,:,k],complex).T
        return out

    return rhsfun,confun


def run_variant(
    variant,bgs,mod6,mod7,r41npz,r37npz,stage_x
):
    xref=np.asarray(r37npz["x_primary"],float)
    states={}; metrics={}; absres={}; scales={}; p0s={}
    finite=True; linmax=0.0

    for tag in r7.C_TAGS:
        bg=bgs[(128,tag)]
        if not np.array_equal(np.asarray(bg["x"],float),xref):
            raise RuntimeError(f"Repair42 x-grid mismatch for {tag}")
        p0=np.asarray(r37npz[f"{tag}_projected_p0_primary"],complex)
        frozen_state=np.asarray(r37npz[f"{tag}_Z21_primary"],complex)
        nb=len(r7.BETAS); nm=len(r7.M_SOLVE); nt=len(xref)
        st=np.empty_like(frozen_state)
        mt=np.empty((nb,nm,nt),float)
        at=np.empty_like(mt); sc=np.empty_like(mt)

        for jm,m in enumerate(r7.M_SOLVE):
            k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
            rhsfun,confun=source_functions(
                variant,xref,stage_x,r41npz,r37npz,tag,jm
            )
            y0=np.zeros((8,nb),complex)
            y0[4:8,:]=p0[:,jm,:].T

            Y,rdiag=r38.radau2_integrate_substepped(
                mod6,mod7,bg,tag,k,y0,rhsfun,confun,1
            )
            state,dd,odiag=r7._reconstruct_canonical_solution(
                mod6,mod7,bg,tag,k,Y,rhsfun,confun
            )
            mtr,atr,scr=r38.shift_trace_from_canonical(
                mod6,mod7,bg,tag,k,Y,rhsfun,confun
            )
            st[:,jm]=state
            mt[:,jm]=mtr
            at[:,jm]=atr
            sc[:,jm]=scr
            linmax=max(
                linmax,
                float(rdiag["radau_block_scaled_relative_L2_residual_max"]),
                float(odiag["algebraic_scaled_relative_L2_residual_max"]),
                float(odiag["lapse_noether_row_relative_residual_max"]),
            )
            finite=bool(
                finite
                and np.all(np.isfinite(Y))
                and np.all(np.isfinite(state))
                and np.all(np.isfinite(mtr))
                and np.all(np.isfinite(atr))
                and np.all(np.isfinite(scr))
            )
        finite=bool(
            finite
            and np.all(np.isfinite(st))
            and np.all(np.isfinite(mt))
            and np.all(np.isfinite(at))
            and np.all(np.isfinite(sc))
        )
        states[tag]=st; metrics[tag]=mt; absres[tag]=at; scales[tag]=sc
        p0s[tag]=p0

    return {
        "states":states,"metrics":metrics,"absres":absres,"scales":scales,
        "p0":p0s,
        "linear_residual_max":float(linmax),
        "all_outputs_finite":bool(finite),
    }


def run_delta(
    variant,bgs,mod6,mod7,r41npz,r37npz,stage_x
):
    xref=np.asarray(r37npz["x_primary"],float)
    states={}; finite=True; linmax=0.0
    for tag in r7.C_TAGS:
        bg=bgs[(128,tag)]
        frozen_state=np.asarray(r37npz[f"{tag}_Z21_primary"],complex)
        nb=len(r7.BETAS); nm=len(r7.M_SOLVE)
        st=np.empty_like(frozen_state)
        for jm,m in enumerate(r7.M_SOLVE):
            k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
            rhsfun,confun=delta_source_functions(
                variant,xref,stage_x,r41npz,tag,jm
            )
            y0=np.zeros((8,nb),complex)
            Y,rdiag=r38.radau2_integrate_substepped(
                mod6,mod7,bg,tag,k,y0,rhsfun,confun,1
            )
            state,dd,odiag=r7._reconstruct_canonical_solution(
                mod6,mod7,bg,tag,k,Y,rhsfun,confun
            )
            st[:,jm]=state
            linmax=max(
                linmax,
                float(rdiag["radau_block_scaled_relative_L2_residual_max"]),
                float(odiag["algebraic_scaled_relative_L2_residual_max"]),
                float(odiag["lapse_noether_row_relative_residual_max"]),
            )
            finite=bool(
                finite and np.all(np.isfinite(Y)) and np.all(np.isfinite(state))
            )
        finite=bool(finite and np.all(np.isfinite(st)))
        states[tag]=st
    return {
        "states":states,
        "linear_residual_max":float(linmax),
        "all_outputs_finite":bool(finite),
    }


def concat_states(mapping):
    return np.concatenate([
        np.asarray(mapping[tag],complex).ravel()
        for tag in r7.C_TAGS
    ])


def active_concat(mapping,masks):
    return np.concatenate([
        np.asarray(mapping[tag])[masks[tag]].ravel()
        for tag in r7.C_TAGS
    ])


def active_summary(run,masks):
    v=np.asarray(active_concat(run["metrics"],masks),float)
    a=np.asarray(active_concat(run["absres"],masks),float)
    return {
        "active_sample_count":int(v.size),
        "Linf":float(np.max(v)),
        "RMS":float(np.sqrt(np.mean(v*v))),
        "median":float(np.median(v)),
        "max_absolute_residual":float(np.max(a)),
        "canonical_Radau_and_algebraic_linear_residual_max":
            float(run["linear_residual_max"]),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    rd=Path(args.results_dir)
    paths,hashes,j41,j37,r41npz,r37npz,r13npz=load_inputs(rd)
    bgs,mod6,mod7,lambda_diag=r38.build_frozen_operator_context(rd,r13npz)

    xref=np.asarray(r37npz["x_primary"],float)
    sx_generated=factor1_stage_x(xref)
    sx_saved=np.asarray(r41npz["stage_x"],float)
    if sx_generated.shape!=sx_saved.shape:
        raise RuntimeError("Repair41 stage_x shape mismatch")
    stage_x_err=float(np.max(np.abs(sx_generated-sx_saved)))

    target_pchip_repro=pchip_target_reproduction(
        r41npz,r37npz,xref,sx_saved
    )

    sref,null_thr,masks,active_count=r38.frozen_active_masks(r37npz)

    runs={}
    summaries={}
    for variant in VARIANTS:
        runs[variant]=run_variant(
            variant,bgs,mod6,mod7,r41npz,r37npz,sx_saved
        )
        summaries[variant]=active_summary(runs[variant],masks)

    baseline=runs["PCHIP_BASELINE"]
    frozen_states=np.concatenate([
        np.asarray(r37npz[f"{tag}_Z21_primary"],complex).ravel()
        for tag in r7.C_TAGS
    ])
    baseline_states=concat_states(baseline["states"])
    state_repro=rel_l2(baseline_states,frozen_states)

    frozen_metrics=np.concatenate([
        np.asarray(r37npz[f"{tag}_shift_metric_primary"],float).ravel()
        for tag in r7.C_TAGS
    ])
    baseline_metrics=np.concatenate([
        np.asarray(baseline["metrics"][tag],float).ravel()
        for tag in r7.C_TAGS
    ])
    shift_repro=rel_l2(baseline_metrics,frozen_metrics)

    p0_exact=all(
        np.array_equal(
            np.asarray(baseline["p0"][tag],complex),
            np.asarray(r37npz[f"{tag}_projected_p0_primary"],complex)
        )
        for tag in r7.C_TAGS
    )

    # Stable direct delta responses from zero delta p0.
    delta_runs={}
    for variant in VARIANTS[1:]:
        delta_runs[variant]=run_delta(
            variant,bgs,mod6,mod7,r41npz,r37npz,sx_saved
        )

    delta_report={}
    for res in (382,763):
        vm=f"DIRECT{res}_M1_ONLY"
        vq=f"DIRECT{res}_Q_GE06_ONLY"
        vb=f"DIRECT{res}_BOTH"
        dm=concat_states(delta_runs[vm]["states"])
        dq=concat_states(delta_runs[vq]["states"])
        db=concat_states(delta_runs[vb]["states"])
        delta_report[str(res)]={
            "M1_delta_Z21_L2":float(np.linalg.norm(dm)),
            "Q_GE06_delta_Z21_L2":float(np.linalg.norm(dq)),
            "BOTH_delta_Z21_L2":float(np.linalg.norm(db)),
            "M1_alignment_with_BOTH":complex_alignment(dm,db),
            "Q_GE06_alignment_with_BOTH":complex_alignment(dq,db),
            "BOTH_linear_residual_max":
                float(delta_runs[vb]["linear_residual_max"]),
        }

    db382=concat_states(delta_runs["DIRECT382_BOTH"]["states"])
    db763=concat_states(delta_runs["DIRECT763_BOTH"]["states"])
    direct_delta_rel=rel_l2(db382,db763)

    s382=summaries["DIRECT382_BOTH"]
    s763=summaries["DIRECT763_BOTH"]
    side382=bool(s382["Linf"]<=SHIFT_TARGET)
    side763=bool(s763["Linf"]<=SHIFT_TARGET)

    finite=bool(
        all(runs[v]["all_outputs_finite"] for v in VARIANTS)
        and all(delta_runs[v]["all_outputs_finite"] for v in VARIANTS[1:])
    )
    implementation_gates={
        "Repair41_and_Repair37_hashes_and_routes_exact":True,
        "Repair41_stage_x_matches_generated_factor1_stage_x_abs_le_1e13":
            bool(stage_x_err<=STAGE_X_MAX),
        "Repair41_saved_PCHIP_target_stage_values_reproduce_Repair37_target_PCHIP_relative_L2_le_1e12":
            bool(target_pchip_repro<=TARGET_PCHIP_REPRO_MAX),
        "PCHIP_baseline_Z21_vs_Repair37_relative_L2_le_1e11":
            bool(state_repro<=BASELINE_STATE_REPRO_MAX),
        "PCHIP_baseline_shift_metric_vs_Repair37_relative_L2_le_1e10":
            bool(shift_repro<=BASELINE_SHIFT_REPRO_MAX),
        "projected_p0_exact":bool(p0_exact),
        "frozen_active_sample_count_exact":bool(active_count==ACTIVE_COUNT),
        "all_outputs_finite":finite,
    }
    impl_ok=bool(all(implementation_gates.values()))

    if not impl_ok:
        classification="GE19_REPAIR42_DIRECT_TARGET_H4_PROPAGATION_DIAGNOSTIC_IMPLEMENTATION_FAIL"
        route="IMPLEMENTATION_FAIL"
    else:
        classification="GE19_REPAIR42_DIRECT_TARGET_H4_PROPAGATION_DIAGNOSTIC_COMPLETE"
        if side382 and side763:
            route="DIRECT_TARGET_CORRECTION_BELOW_SCIENCE_TARGET"
        elif (not side382) and (not side763):
            route="DIRECT_TARGET_CORRECTION_ABOVE_SCIENCE_TARGET"
        else:
            route="DIRECT_TARGET_CORRECTION_THRESHOLD_SIDE_UNRESOLVED"

    report={
        "classification":classification,
        "predata_classification":"GE19_REPAIR42_PREDATA_DIRECT_TARGET_H4_PROPAGATION_DIAGNOSTIC",
        "diagnostic_only":True,
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "provenance":{
            "input_sha256":hashes,
            "Repair41_classification":j41["classification"],
            "Repair41_route":j41["routing"]["next_route"],
            "Repair37_classification":j37["classification"],
            "Repair37_relabelled":False,
            "Repair41_relabelled":False,
        },
        "frozen_contract":{
            "Nt":128,
            "Radau_substeps_per_interval":1,
            "science_shift_target":SHIFT_TARGET,
            "threshold_relaxed":False,
            "non_target_source_representation":"Repair37 frozen PCHIP total-source baseline",
            "corrected_targets":[M1,Q6],
            "projected_p0_recomputed":False,
        },
        "source_binding_controls":{
            "generated_vs_Repair41_stage_x_abs_max":stage_x_err,
            "Repair41_saved_PCHIP_target_vs_Repair37_PCHIP_relative_L2":
                float(target_pchip_repro),
        },
        "baseline_reproduction":{
            "Z21_relative_L2":float(state_repro),
            "shift_metric_relative_L2":float(shift_repro),
            "projected_p0_exact":bool(p0_exact),
            "active_sample_count":int(active_count),
            "S_ref":float(sref),
            "near_null_threshold":float(null_thr),
        },
        "variant_results":summaries,
        "direct_delta_response_report_only":delta_report,
        "direct382_vs_direct763_report_only":{
            "BOTH_delta_Z21_relative_L2":float(direct_delta_rel),
            "BOTH_active_shift_Linf_abs_difference":
                float(abs(s382["Linf"]-s763["Linf"])),
            "BOTH_active_shift_RMS_abs_difference":
                float(abs(s382["RMS"]-s763["RMS"])),
            "DIRECT382_BOTH_below_or_equal_1e6":bool(side382),
            "DIRECT763_BOTH_below_or_equal_1e6":bool(side763),
        },
        "implementation_gates":implementation_gates,
        "routing":{
            "next_route":route,
            "if_below":"PREREGISTER_DIRECT_TARGET_H4_Z21_SCIENCE_RECLOSURE_WITH_TIME_CONTROL",
            "if_above":"LOCALIZE_RESIDUAL_NON_TARGET_SOURCE_REPRESENTATION",
            "if_threshold_side_unresolved":"INCREASE_DIRECT_TARGET_PARENT_TIME_RESOLUTION",
        },
        "Z21_window_local_particular_certified":False,
        "science_H4_Z21_reclosure_performed":False,
        "lensing_licensed":False,
        "claim_boundary":"Repair42 is a direct-target stage-correction H4 propagation diagnostic on the frozen Repair37 factor-1 grid. It does not certify Z21, alter any science threshold, introduce finite eta, use observational data, or license lensing."
    }

    outj=Path(args.json_out)
    outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")

    save={
        "x_primary":xref,
        "stage_x":sx_saved,
        "frozen_S_ref":np.asarray(sref,float),
        "frozen_near_null_threshold":np.asarray(null_thr,float),
    }
    for tag in r7.C_TAGS:
        save[f"{tag}_frozen_active_mask"]=np.asarray(masks[tag],bool)
        for variant in VARIANTS:
            safe=variant.lower()
            save[f"{tag}_{safe}_Z21"]=runs[variant]["states"][tag]
            save[f"{tag}_{safe}_shift_metric"]=runs[variant]["metrics"][tag]
        for variant in ("DIRECT382_BOTH","DIRECT763_BOTH"):
            safe=variant.lower()
            save[f"{tag}_{safe}_delta_Z21"]=delta_runs[variant]["states"][tag]
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
            "classification":"GE19_REPAIR42_DIRECT_TARGET_H4_PROPAGATION_DIAGNOSTIC_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Z21_window_local_particular_certified":False,
            "science_H4_Z21_reclosure_performed":False,
            "lensing_licensed":False
        },indent=2))
        raise
