#!/usr/bin/env python3
"""GE19 Repair44 — split GE06 shift source row0 from anisotropy source row1.

Diagnostic only. No parent source, operator, threshold, boundary, time grid
or observational input is changed. The full two-row constraint correction
must reproduce frozen Repair43 before row-level interpretation.
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
import ge19.repair42_direct_target_h4_propagation_diagnostic as r42
import ge19.repair43_qge06_main_constraint_stage_split as r43

TINY=1e-300
R43_JSON_SHA="559ae65ffc5d21433799e4e33aa6d91237a9aa41b9799463971bc45dabecae44"
R43_NPZ_SHA="d5c8c02c7f8272dc390ce9e4d2374a35b2ce1b14da5b60e69dc8366499bfe71c"
STAGE_X_MAX=1e-13
PCHIP_TARGET_REPRO_MAX=1e-12
STATE_REPRO_MAX=1e-11
METRIC_REPRO_MAX=1e-10
ACTIVE_COUNT=23850
SCIENCE_TARGET_REPORT_ONLY=1e-6
HOTSPOT_TAG="C_max"
HOTSPOT_BETA_INDEX=0
HOTSPOT_MODE=8
HOTSPOT_TIME_INDEX=3
HOTSPOT_X=-0.8989528773447014

VARIANTS=(
    "PCHIP_BASELINE",
    "DIRECT382_Q_GE06_SHIFT_ROW0_ONLY",
    "DIRECT382_Q_GE06_ANISOTROPY_ROW1_ONLY",
    "DIRECT382_Q_GE06_BOTH_CONSTRAINT_ROWS",
    "DIRECT763_Q_GE06_SHIFT_ROW0_ONLY",
    "DIRECT763_Q_GE06_ANISOTROPY_ROW1_ONLY",
    "DIRECT763_Q_GE06_BOTH_CONSTRAINT_ROWS",
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


def rms(a)->float:
    arr=np.asarray(a,float)
    return float(np.sqrt(np.mean(arr*arr))) if arr.size else 0.0


def complex_parts(z):
    z=complex(z)
    return {"real":float(z.real),"imag":float(z.imag),"abs":float(abs(z))}


def load_inputs(rd:Path):
    paths,hashes,j42,j41,j37,r42npz,r41npz,r37npz,r13npz=r43.load_inputs(rd)
    extra={
        "r43j":rd/"ge19_repair43_qge06_main_constraint_stage_split.json",
        "r43n":rd/"ge19_repair43_qge06_main_constraint_stage_split.npz",
    }
    for key,p in extra.items():
        if not p.is_file():
            raise RuntimeError(f"missing frozen Repair43 artifact: {p}")
        got=sha256(p)
        want={"r43j":R43_JSON_SHA,"r43n":R43_NPZ_SHA}[key]
        if got!=want:
            raise RuntimeError(f"{key} hash mismatch: {got} != {want}")
        paths[key]=p
        hashes[key]=got
    j43=json.loads(extra["r43j"].read_text())
    if j43.get("classification")!="GE19_REPAIR43_QGE06_MAIN_CONSTRAINT_STAGE_SPLIT_COMPLETE":
        raise RuntimeError("Repair43 classification mismatch")
    if j43.get("routing",{}).get("next_route")!="QGE06_CONSTRAINT_ROW_FIELD_CLOSER_TO_FULL":
        raise RuntimeError("Repair43 route does not license Repair44")
    if not all(j43.get("implementation_gates",{}).values()):
        raise RuntimeError("Repair43 implementation gates not all true")
    if j43.get("Z21_window_local_particular_certified") is not False:
        raise RuntimeError("Repair43 incorrectly certified Z21")
    return paths,hashes,j43,j42,j41,j37,np.load(extra["r43n"]),r42npz,r41npz,r37npz,r13npz


def parse_variant(variant):
    if variant=="PCHIP_BASELINE":
        return None,None
    if variant.startswith("DIRECT382_"):
        resolution=382
    elif variant.startswith("DIRECT763_"):
        resolution=763
    else:
        raise ValueError(variant)
    if variant.endswith("_SHIFT_ROW0_ONLY"):
        row="SHIFT_ROW0_ONLY"
    elif variant.endswith("_ANISOTROPY_ROW1_ONLY"):
        row="ANISOTROPY_ROW1_ONLY"
    elif variant.endswith("_BOTH_CONSTRAINT_ROWS"):
        row="BOTH_CONSTRAINT_ROWS"
    else:
        raise ValueError(variant)
    return resolution,row


def source_functions(
    variant,xref,stage_x,r41npz,r37npz,tag,jm
):
    # Baseline is the frozen Repair37 PCHIP total source.
    base_rhs,base_con=r42.source_functions(
        "PCHIP_BASELINE",xref,stage_x,r41npz,r37npz,tag,jm
    )
    resolution,row=parse_variant(variant)
    if resolution is None:
        return base_rhs,base_con

    dm,dc=r42.saved_stage_pair(r41npz,tag,r42.Q6,resolution,jm)
    pm,pc=r42.saved_stage_pair(r41npz,tag,r42.Q6,"PCHIP",jm)
    delta_con=np.asarray(dc-pc,complex)
    locate=r42.stage_locator(stage_x,float(xref[0]))

    def confun(xq):
        out=np.asarray(base_con(float(xq)),complex).copy()
        k=locate(xq)
        if k>=0:
            if row in ("SHIFT_ROW0_ONLY","BOTH_CONSTRAINT_ROWS"):
                out[0,:]+=delta_con[:,0,k]
            if row in ("ANISOTROPY_ROW1_ONLY","BOTH_CONSTRAINT_ROWS"):
                out[1,:]+=delta_con[:,1,k]
        return out

    return base_rhs,confun


def run_variant(
    variant,bgs,mod6,mod7,r41npz,r37npz,stage_x
):
    xref=np.asarray(r37npz["x_primary"],float)
    states={}
    metrics={}
    absres={}
    scales={}
    p0_loaded={}
    finite=True
    linear_res=0.0
    hotspot_y=None

    for tag in r7.C_TAGS:
        bg=bgs[(128,tag)]
        if not np.array_equal(np.asarray(bg["x"],float),xref):
            raise RuntimeError(f"Repair43 x-grid mismatch for {tag}")
        p0=np.asarray(r37npz[f"{tag}_projected_p0_primary"],complex)
        frozen_state=np.asarray(r37npz[f"{tag}_Z21_primary"],complex)
        nb=len(r7.BETAS)
        nm=len(r7.M_SOLVE)
        nt=len(xref)
        st=np.empty_like(frozen_state)
        mt=np.empty((nb,nm,nt),float)
        at=np.empty_like(mt)
        sc=np.empty_like(mt)

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
            sm,sa,ss=r38.shift_trace_from_canonical(
                mod6,mod7,bg,tag,k,Y,rhsfun,confun
            )
            if tag==HOTSPOT_TAG and int(m)==HOTSPOT_MODE:
                hotspot_y=np.asarray(Y[HOTSPOT_BETA_INDEX,:,HOTSPOT_TIME_INDEX],complex).copy()
            st[:,jm]=state
            mt[:,jm]=sm
            at[:,jm]=sa
            sc[:,jm]=ss
            linear_res=max(
                linear_res,
                float(rdiag["radau_block_scaled_relative_L2_residual_max"]),
                float(odiag["algebraic_scaled_relative_L2_residual_max"]),
                float(odiag["lapse_noether_row_relative_residual_max"]),
            )
            finite=bool(
                finite
                and np.all(np.isfinite(Y))
                and np.all(np.isfinite(state))
                and np.all(np.isfinite(sm))
                and np.all(np.isfinite(sa))
                and np.all(np.isfinite(ss))
            )

        # Check completed fields only, not future np.empty mode slots.
        finite=bool(
            finite and np.all(np.isfinite(st))
            and np.all(np.isfinite(mt))
            and np.all(np.isfinite(at))
            and np.all(np.isfinite(sc))
        )
        states[tag]=st
        metrics[tag]=mt
        absres[tag]=at
        scales[tag]=sc
        p0_loaded[tag]=p0

    return {
        "states":states,
        "metrics":metrics,
        "absres":absres,
        "scales":scales,
        "p0":p0_loaded,
        "hotspot_canonical_y":hotspot_y,
        "linear_residual_max":float(linear_res),
        "all_outputs_finite":bool(finite),
    }




def concat_states(mapping):
    return np.concatenate([
        np.asarray(mapping[tag],complex).ravel()
        for tag in r7.C_TAGS
    ])




def concat_active(mapping,masks):
    return np.concatenate([
        np.asarray(mapping[tag])[masks[tag]].ravel()
        for tag in r7.C_TAGS
    ])




def active_summary(run,masks):
    v=np.asarray(concat_active(run["metrics"],masks),float)
    a=np.asarray(concat_active(run["absres"],masks),float)
    s=np.asarray(concat_active(run["scales"],masks),float)
    return {
        "active_sample_count":int(v.size),
        "Linf":float(np.max(v)),
        "RMS":rms(v),
        "median":float(np.median(v)),
        "active_absolute_shift_residual_max":float(np.max(a)),
        "active_shift_scale_min":float(np.min(s)),
        "canonical_Radau_and_algebraic_linear_residual_max":
            float(run["linear_residual_max"]),
        "below_or_equal_1e6_report_only":bool(np.max(v)<=SCIENCE_TARGET_REPORT_ONLY),
    }





def frozen_r43_variant(r43npz,name,suffix):
    safe=name.lower()
    return {
        tag:np.asarray(r43npz[f"{tag}_{safe}_{suffix}"])
        for tag in r7.C_TAGS
    }


def hotspot_report(
    runs,bgs,mod6,mod7,r41npz,r37npz,stage_x,xref
):
    beta=HOTSPOT_BETA_INDEX
    mode_index=int(np.where(np.asarray(r37npz["modes_output"],int)==HOTSPOT_MODE)[0][0])
    it=HOTSPOT_TIME_INDEX
    if not np.isclose(float(np.asarray(r37npz["beta0"])[beta]),1.0,rtol=0,atol=0):
        raise RuntimeError("hotspot beta0 is not 1.0")
    x=float(xref[it])
    if abs(x-HOTSPOT_X)>STAGE_X_MAX:
        raise RuntimeError("frozen hotspot time mismatch")
    si=r42.stage_locator(stage_x,float(xref[0]))(x)
    if si<0:
        raise RuntimeError("hotspot not a frozen factor1 stage")

    frozen_scale=float(
        r37npz[f"{HOTSPOT_TAG}_shift_scale_primary"][beta,mode_index,it]
    )
    if not frozen_scale>0.0:
        raise RuntimeError("invalid frozen hotspot shift denominator")

    source_deltas={}
    for res in (382,763):
        dm,dc=r42.saved_stage_pair(
            r41npz,HOTSPOT_TAG,r42.Q6,res,mode_index
        )
        pm,pc=r42.saved_stage_pair(
            r41npz,HOTSPOT_TAG,r42.Q6,"PCHIP",mode_index
        )
        delta=np.asarray(dc[beta,:,si]-pc[beta,:,si],complex)
        source_deltas[str(res)]={
            "shift_row0_delta":complex_parts(delta[0]),
            "anisotropy_row1_delta":complex_parts(delta[1]),
            "shift_row0_delta_abs_over_frozen_shift_scale":
                float(abs(delta[0])/frozen_scale),
            "anisotropy_row1_delta_abs_over_frozen_shift_scale":
                float(abs(delta[1])/frozen_scale),
        }

    bg=bgs[(128,HOTSPOT_TAG)]
    kval=float(HOTSPOT_MODE*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
        mod6,mod7,bg,HOTSPOT_TAG,kval,x
    )
    per_variant={}
    complex_residuals={}
    for v in VARIANTS:
        y=runs[v]["hotspot_canonical_y"]
        if y is None:
            raise RuntimeError(f"missing canonical hotspot state for {v}")
        rhsfun,confun=source_functions(
            v,xref,stage_x,r41npz,r37npz,HOTSPOT_TAG,mode_index
        )
        rr=np.asarray(rhsfun(x),complex)
        cc=np.asarray(confun(x),complex)
        src=np.concatenate([rr[:,beta],cc[:,beta]])
        w=WY@y+WR@src
        residual=complex((Cmat[10]+Cmat[11])@w-cc[0,beta])
        complex_residuals[v]=residual
        metric=float(runs[v]["metrics"][HOTSPOT_TAG][beta,mode_index,it])
        absres=float(runs[v]["absres"][HOTSPOT_TAG][beta,mode_index,it])
        scale=float(runs[v]["scales"][HOTSPOT_TAG][beta,mode_index,it])
        per_variant[v]={
            "shift_metric":metric,
            "complex_shift_residual":complex_parts(residual),
            "absolute_shift_residual":absres,
            "backward_error_scale":scale,
            "absolute_residual_over_scale":float(absres/max(scale,TINY)),
            "complex_vs_saved_absolute_residual_abs_difference":
                float(abs(abs(residual)-absres)),
        }

    baseline=complex_residuals["PCHIP_BASELINE"]
    identity_report={}
    for res in (382,763):
        v=f"DIRECT{res}_Q_GE06_SHIFT_ROW0_ONLY"
        delta=complex(source_deltas[str(res)]["shift_row0_delta"]["real"],
                      source_deltas[str(res)]["shift_row0_delta"]["imag"])
        measured=complex_residuals[v]-baseline
        identity_report[str(res)]={
            "observed_row0_only_shift_residual_delta":complex_parts(measured),
            "predicted_negative_shift_source_delta":complex_parts(-delta),
            "complex_identity_absolute_defect":float(abs(measured+delta)),
            "complex_identity_defect_over_frozen_shift_scale":
                float(abs(measured+delta)/frozen_scale),
        }

    return {
        "tag":HOTSPOT_TAG,
        "beta_index":beta,
        "beta0":1.0,
        "mode":HOTSPOT_MODE,
        "mode_index":mode_index,
        "time_index":it,
        "ln_a":x,
        "stage_index":si,
        "frozen_Repair37_backward_error_scale":frozen_scale,
        "direct_source_row_deltas":source_deltas,
        "per_variant":per_variant,
        "row0_independent_constraint_identity_report_only":identity_report,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    rd=Path(args.results_dir)
    (
        paths,hashes,j43,j42,j41,j37,r43npz,r42npz,r41npz,r37npz,r13npz
    )=load_inputs(rd)
    bgs,mod6,mod7,lambda_diag=r38.build_frozen_operator_context(rd,r13npz)

    xref=np.asarray(r37npz["x_primary"],float)
    stage_x=np.asarray(r41npz["stage_x"],float)
    xgen=r42.factor1_stage_x(xref)
    if stage_x.shape!=xgen.shape:
        raise RuntimeError("Repair41 stage grid shape mismatch")
    stage_error=float(np.max(np.abs(stage_x-xgen)))
    target_pchip_repro=r42.pchip_target_reproduction(
        r41npz,r37npz,xref,stage_x
    )
    sref,null_thr,masks,active_count=r38.frozen_active_masks(r37npz)

    runs={}
    summaries={}
    for variant in VARIANTS:
        runs[variant]=run_variant(
            variant,bgs,mod6,mod7,r41npz,r37npz,stage_x
        )
        summaries[variant]=active_summary(runs[variant],masks)

    baseline=runs["PCHIP_BASELINE"]
    frozen_baseline=frozen_r43_variant(
        r43npz,"PCHIP_BASELINE","Z21"
    )
    frozen_baseline_metric=frozen_r43_variant(
        r43npz,"PCHIP_BASELINE","shift_metric"
    )
    repro={
        "PCHIP_Z21_relative_L2":
            rel_l2(concat_states(baseline["states"]),
                   concat_states(frozen_baseline)),
        "PCHIP_shift_metric_relative_L2":
            rel_l2(concat_active(baseline["metrics"],masks),
                   concat_active(frozen_baseline_metric,masks)),
    }
    for res in (382,763):
        v=f"DIRECT{res}_Q_GE06_BOTH_CONSTRAINT_ROWS"
        fv=f"DIRECT{res}_Q_GE06_CONSTRAINT_ONLY"
        repro[f"DIRECT{res}_BOTH_CONSTRAINT_ROWS_Z21_relative_L2"]=rel_l2(
            concat_states(runs[v]["states"]),
            concat_states(frozen_r43_variant(r43npz,fv,"Z21")),
        )
        repro[f"DIRECT{res}_BOTH_CONSTRAINT_ROWS_shift_metric_relative_L2"]=rel_l2(
            concat_active(runs[v]["metrics"],masks),
            concat_active(frozen_r43_variant(r43npz,fv,"shift_metric"),masks),
        )

    row0_exact={
        str(res):bool(all(np.array_equal(
            np.asarray(runs[f"DIRECT{res}_Q_GE06_SHIFT_ROW0_ONLY"]["states"][tag],complex),
            np.asarray(baseline["states"][tag],complex)
        ) for tag in r7.C_TAGS))
        for res in (382,763)
    }
    row0_state_max={
        str(res):float(max(
            np.max(np.abs(
                runs[f"DIRECT{res}_Q_GE06_SHIFT_ROW0_ONLY"]["states"][tag]
                -baseline["states"][tag]
            ))
            for tag in r7.C_TAGS
        ))
        for res in (382,763)
    }

    p0_exact=all(
        np.array_equal(
            runs["PCHIP_BASELINE"]["p0"][tag],
            np.asarray(r37npz[f"{tag}_projected_p0_primary"],complex)
        )
        for tag in r7.C_TAGS
    )
    finite=bool(all(runs[v]["all_outputs_finite"] for v in VARIANTS))

    gates={
        "frozen_parents_hashes_and_routes_exact":True,
        "stage_coordinate_abs_le_1e13":bool(stage_error<=STAGE_X_MAX),
        "PCHIP_target_reproduction_relative_L2_le_1e12":
            bool(target_pchip_repro<=PCHIP_TARGET_REPRO_MAX),
        "PCHIP_baseline_Z21_relative_L2_le_1e11":
            bool(repro["PCHIP_Z21_relative_L2"]<=STATE_REPRO_MAX),
        "PCHIP_baseline_shift_relative_L2_le_1e10":
            bool(repro["PCHIP_shift_metric_relative_L2"]<=METRIC_REPRO_MAX),
        "DIRECT382_BOTH_CONSTRAINT_ROWS_Z21_relative_L2_le_1e11":
            bool(repro["DIRECT382_BOTH_CONSTRAINT_ROWS_Z21_relative_L2"]<=STATE_REPRO_MAX),
        "DIRECT382_BOTH_CONSTRAINT_ROWS_shift_relative_L2_le_1e10":
            bool(repro["DIRECT382_BOTH_CONSTRAINT_ROWS_shift_metric_relative_L2"]<=METRIC_REPRO_MAX),
        "DIRECT763_BOTH_CONSTRAINT_ROWS_Z21_relative_L2_le_1e11":
            bool(repro["DIRECT763_BOTH_CONSTRAINT_ROWS_Z21_relative_L2"]<=STATE_REPRO_MAX),
        "DIRECT763_BOTH_CONSTRAINT_ROWS_shift_relative_L2_le_1e10":
            bool(repro["DIRECT763_BOTH_CONSTRAINT_ROWS_shift_metric_relative_L2"]<=METRIC_REPRO_MAX),
        "shift_row0_only_Z21_equal_baseline_exact":
            bool(all(row0_exact.values())),
        "projected_p0_exact":bool(p0_exact),
        "frozen_active_count_exact":bool(active_count==ACTIVE_COUNT),
        "all_outputs_finite":finite,
    }
    implementation_ok=bool(all(gates.values()))

    attribution={}
    for res in (382,763):
        full=np.asarray(concat_active(
            runs[f"DIRECT{res}_Q_GE06_BOTH_CONSTRAINT_ROWS"]["metrics"],masks
        ),float)
        shift=np.asarray(concat_active(
            runs[f"DIRECT{res}_Q_GE06_SHIFT_ROW0_ONLY"]["metrics"],masks
        ),float)
        anis=np.asarray(concat_active(
            runs[f"DIRECT{res}_Q_GE06_ANISOTROPY_ROW1_ONLY"]["metrics"],masks
        ),float)
        dshift=rms(shift-full)
        danis=rms(anis-full)
        attribution[str(res)]={
            "SHIFT_ROW0_ONLY_vs_Repair43_constraint_only_active_field_difference_RMS":
                float(dshift),
            "ANISOTROPY_ROW1_ONLY_vs_Repair43_constraint_only_active_field_difference_RMS":
                float(danis),
            "closer_row":(
                "SHIFT_ROW0_ONLY" if dshift<danis
                else "ANISOTROPY_ROW1_ONLY" if danis<dshift
                else "TIE"
            ),
            "anisotropy_row1_only_Z21_response_relative_L2":
                rel_l2(
                    concat_states(runs[f"DIRECT{res}_Q_GE06_ANISOTROPY_ROW1_ONLY"]["states"]),
                    concat_states(baseline["states"])
                ),
        }

    hotspot=hotspot_report(
        runs,bgs,mod6,mod7,r41npz,r37npz,stage_x,xref
    )
    if not implementation_ok:
        classification="GE19_REPAIR44_QGE06_SHIFT_ANISOTROPY_ROW_SPLIT_IMPLEMENTATION_FAIL"
        route="IMPLEMENTATION_FAIL"
    elif all(attribution[str(res)]["closer_row"]=="SHIFT_ROW0_ONLY"
             for res in (382,763)):
        classification="GE19_REPAIR44_QGE06_SHIFT_ANISOTROPY_ROW_SPLIT_COMPLETE"
        route="QGE06_SHIFT_ROW0_FIELD_CLOSER_TO_FULL"
    elif all(attribution[str(res)]["closer_row"]=="ANISOTROPY_ROW1_ONLY"
             for res in (382,763)):
        classification="GE19_REPAIR44_QGE06_SHIFT_ANISOTROPY_ROW_SPLIT_COMPLETE"
        route="QGE06_ANISOTROPY_ROW1_FIELD_CLOSER_TO_FULL"
    else:
        classification="GE19_REPAIR44_QGE06_SHIFT_ANISOTROPY_ROW_SPLIT_COMPLETE"
        route="QGE06_MIXED_CONSTRAINT_ROW_SENSITIVITY"

    report={
        "classification":classification,
        "predata_classification":"GE19_REPAIR44_PREDATA_QGE06_SHIFT_ANISOTROPY_ROW_SPLIT",
        "diagnostic_only":True,
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "provenance":{
            "input_sha256":hashes,
            "Repair43_classification":j43["classification"],
            "Repair43_route":j43["routing"]["next_route"],
            "Repair42_classification":j42["classification"],
            "Repair41_route":j41["routing"]["next_route"],
            "Repair37_classification":j37["classification"],
            "previous_repairs_relabelled":False,
        },
        "frozen_contract":{
            "Nt":128,
            "Radau_substeps_per_interval":1,
            "target_piece":r42.Q6,
            "source_target_rows":["shift constraint row0","anisotropy row1"],
            "direct_source_interpolated":False,
            "projected_p0_recomputed":False,
            "science_shift_target_report_only":SCIENCE_TARGET_REPORT_ONLY,
            "threshold_relaxed":False,
        },
        "stage_and_source_binding":{
            "generated_vs_Repair41_stage_x_abs_max":stage_error,
            "Repair41_PCHIP_target_vs_Repair37_target_relative_L2":
                target_pchip_repro,
        },
        "frozen_active_mask":{
            "active_count":active_count,
            "S_ref":float(sref),
            "near_null_threshold":float(null_thr),
        },
        "Repair43_reproduction":repro,
        "shift_row0_only_Z21_exact_baseline":row0_exact,
        "shift_row0_only_Z21_max_absolute_difference":row0_state_max,
        "variant_results":summaries,
        "row_level_active_field_attribution":attribution,
        "registered_hotspot":hotspot,
        "implementation_gates":gates,
        "routing":{"next_route":route},
        "Z21_window_local_particular_certified":False,
        "science_H4_Z21_reclosure_performed":False,
        "lensing_licensed":False,
        "claim_boundary":"Repair44 is a frozen GE06 shift-row0 versus anisotropy-row1 source-stage diagnostic. The source physics, operator, projected boundary, active mask and 1e-6 target are unchanged. It cannot relabel prior repairs, certify Z21 or license lensing."
    }

    outj=Path(args.json_out)
    outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")

    saved={
        "x_primary":xref,
        "stage_x":stage_x,
        "frozen_S_ref":np.asarray(sref,float),
        "frozen_near_null_threshold":np.asarray(null_thr,float),
    }
    for tag in r7.C_TAGS:
        saved[f"{tag}_frozen_active_mask"]=np.asarray(masks[tag],bool)
        for v in VARIANTS:
            safe=v.lower()
            saved[f"{tag}_{safe}_Z21"]=runs[v]["states"][tag]
            saved[f"{tag}_{safe}_shift_metric"]=runs[v]["metrics"][tag]
            saved[f"{tag}_{safe}_shift_abs"]=runs[v]["absres"][tag]
            saved[f"{tag}_{safe}_shift_scale"]=runs[v]["scales"][tag]
    np.savez_compressed(outn,**saved)

    print(json.dumps(report,indent=2,allow_nan=False))
    if not implementation_ok:
        raise SystemExit(3)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR44_QGE06_SHIFT_ANISOTROPY_ROW_SPLIT_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Z21_window_local_particular_certified":False,
            "lensing_licensed":False,
        },indent=2))
        raise
