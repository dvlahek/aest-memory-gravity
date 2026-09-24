#!/usr/bin/env python3
"""GE19 Repair43: frozen Q_GE06 main-versus-constraint stage-source split.

Diagnostic only. The frozen Repair37 PCHIP total H4 source is the baseline.
Only the Repair41 direct Q_GE06 source-stage correction is split into its
six-row main and two-row constraint components on the original factor-1
Nt128 Radau grid. Baseline and full Q_GE06 variants must reproduce Repair42.
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

TINY=1e-300
R42_JSON_SHA="4a211581a77c1ad00e14cc398ca7a19b12642f3f3e35b416314d6721f5f81e25"
R42_NPZ_SHA="a60515f3d92bbd388fd2fadae6cf2dd07f3ee68e8690b07632bbe5091e9013c5"
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
    "DIRECT382_Q_GE06_MAIN_ONLY",
    "DIRECT382_Q_GE06_CONSTRAINT_ONLY",
    "DIRECT382_Q_GE06_BOTH",
    "DIRECT763_Q_GE06_MAIN_ONLY",
    "DIRECT763_Q_GE06_CONSTRAINT_ONLY",
    "DIRECT763_Q_GE06_BOTH",
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


def load_inputs(rd:Path):
    paths,hashes,j41,j37,r41npz,r37npz,r13npz=r42.load_inputs(rd)
    extra={
        "r42j":rd/"ge19_repair42_direct_target_h4_propagation_diagnostic.json",
        "r42n":rd/"ge19_repair42_direct_target_h4_propagation_diagnostic.npz",
    }
    for key,p in extra.items():
        if not p.is_file():
            raise RuntimeError(f"missing frozen Repair42 artifact: {p}")
        got=sha256(p)
        want={"r42j":R42_JSON_SHA,"r42n":R42_NPZ_SHA}[key]
        if got!=want:
            raise RuntimeError(f"{key} hash mismatch: {got} != {want}")
        paths[key]=p
        hashes[key]=got
    j42=json.loads(extra["r42j"].read_text())
    if j42.get("classification")!="GE19_REPAIR42_DIRECT_TARGET_H4_PROPAGATION_DIAGNOSTIC_COMPLETE":
        raise RuntimeError("Repair42 classification mismatch")
    if j42.get("routing",{}).get("next_route")!="DIRECT_TARGET_CORRECTION_ABOVE_SCIENCE_TARGET":
        raise RuntimeError("Repair42 route mismatch")
    if not all(j42.get("implementation_gates",{}).values()):
        raise RuntimeError("Repair42 implementation gates not all true")
    if j42.get("Z21_window_local_particular_certified") is not False:
        raise RuntimeError("Repair42 incorrectly certified Z21")
    return paths,hashes,j42,j41,j37,np.load(extra["r42n"]),r41npz,r37npz,r13npz


def parse_variant(variant):
    if variant=="PCHIP_BASELINE":
        return None,None
    if variant.startswith("DIRECT382_"):
        resolution=382
    elif variant.startswith("DIRECT763_"):
        resolution=763
    else:
        raise ValueError(variant)
    if variant.endswith("_MAIN_ONLY"):
        row_family="MAIN_ONLY"
    elif variant.endswith("_CONSTRAINT_ONLY"):
        row_family="CONSTRAINT_ONLY"
    elif variant.endswith("_BOTH"):
        row_family="BOTH"
    else:
        raise ValueError(variant)
    return resolution,row_family


def source_functions(
    variant,xref,stage_x,r41npz,r37npz,tag,jm
):
    # Exactly the Repair42/Repair37 PCHIP total H4 source is used for baseline.
    base_rhs,base_con=r42.source_functions(
        "PCHIP_BASELINE",xref,stage_x,r41npz,r37npz,tag,jm
    )
    resolution,row_family=parse_variant(variant)
    if resolution is None:
        return base_rhs,base_con

    dm,dc=r42.saved_stage_pair(r41npz,tag,r42.Q6,resolution,jm)
    pm,pc=r42.saved_stage_pair(r41npz,tag,r42.Q6,"PCHIP",jm)
    delta_main=dm-pm
    delta_con=dc-pc
    locate=r42.stage_locator(stage_x,float(xref[0]))

    def rhsfun(xq):
        out=np.asarray(base_rhs(float(xq)),complex)
        k=locate(xq)
        if k>=0 and row_family in ("MAIN_ONLY","BOTH"):
            out=out+np.asarray(delta_main[:,:,k],complex).T
        return out

    def confun(xq):
        out=np.asarray(base_con(float(xq)),complex)
        k=locate(xq)
        if k>=0 and row_family in ("CONSTRAINT_ONLY","BOTH"):
            out=out+np.asarray(delta_con[:,:,k],complex).T
        return out

    return rhsfun,confun


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


def frozen_r42_variant(r42npz,name,suffix):
    safe=name.lower()
    return {
        tag:np.asarray(r42npz[f"{tag}_{safe}_{suffix}"])
        for tag in r7.C_TAGS
    }


def hotspot_report(
    runs,r41npz,r37npz,stage_x,xref
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
        raise RuntimeError("hotspot not a frozen stage")
    frozen_scale=float(
        r37npz[f"{HOTSPOT_TAG}_shift_scale_primary"][beta,mode_index,it]
    )
    if frozen_scale<=0.0:
        raise RuntimeError("invalid frozen hotspot shift scale")

    sources={}
    for res in (382,763):
        dm,dc=r42.saved_stage_pair(
            r41npz,HOTSPOT_TAG,r42.Q6,res,mode_index
        )
        pm,pc=r42.saved_stage_pair(
            r41npz,HOTSPOT_TAG,r42.Q6,"PCHIP",mode_index
        )
        dmain=np.asarray(dm[beta,:,si]-pm[beta,:,si],complex)
        dcon=np.asarray(dc[beta,:,si]-pc[beta,:,si],complex)
        sources[str(res)]={
            "GE06_main_delta_L2":float(np.linalg.norm(dmain)),
            "GE06_constraint_delta_row0_abs":float(abs(dcon[0])),
            "GE06_constraint_delta_row1_abs":float(abs(dcon[1])),
            "GE06_constraint_delta_row0_abs_over_frozen_shift_scale":
                float(abs(dcon[0])/frozen_scale),
        }

    per_variant={}
    for v in VARIANTS:
        metric=float(runs[v]["metrics"][HOTSPOT_TAG][beta,mode_index,it])
        ab=float(runs[v]["absres"][HOTSPOT_TAG][beta,mode_index,it])
        scale=float(runs[v]["scales"][HOTSPOT_TAG][beta,mode_index,it])
        per_variant[v]={
            "shift_metric":metric,
            "absolute_shift_residual":ab,
            "backward_error_scale":scale,
            "absolute_residual_over_scale":float(ab/max(scale,TINY)),
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
        "GE06_direct_source_deltas":sources,
        "per_variant":per_variant,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    rd=Path(args.results_dir)
    paths,hashes,j42,j41,j37,r42npz,r41npz,r37npz,r13npz=load_inputs(rd)
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
    frozen_baseline=frozen_r42_variant(
        r42npz,"PCHIP_BASELINE","Z21"
    )
    frozen_baseline_metric=frozen_r42_variant(
        r42npz,"PCHIP_BASELINE","shift_metric"
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
        v=f"DIRECT{res}_Q_GE06_BOTH"
        frozen_v=f"DIRECT{res}_Q_GE06_ONLY"
        repro[f"DIRECT{res}_Q_GE06_BOTH_Z21_relative_L2"]=rel_l2(
            concat_states(runs[v]["states"]),
            concat_states(frozen_r42_variant(r42npz,frozen_v,"Z21")),
        )
        repro[f"DIRECT{res}_Q_GE06_BOTH_shift_metric_relative_L2"]=rel_l2(
            concat_active(runs[v]["metrics"],masks),
            concat_active(frozen_r42_variant(r42npz,frozen_v,"shift_metric"),masks),
        )

    p0_exact=all(
        np.array_equal(
            runs["PCHIP_BASELINE"]["p0"][tag],
            np.asarray(r37npz[f"{tag}_projected_p0_primary"],complex)
        )
        for tag in r7.C_TAGS
    )
    finite=bool(all(runs[v]["all_outputs_finite"] for v in VARIANTS))
    impl={
        "frozen_parents_hashes_and_routes_exact":True,
        "stage_coordinate_abs_le_1e13":bool(stage_error<=STAGE_X_MAX),
        "PCHIP_target_reproduction_relative_L2_le_1e12":
            bool(target_pchip_repro<=PCHIP_TARGET_REPRO_MAX),
        "PCHIP_baseline_Z21_relative_L2_le_1e11":
            bool(repro["PCHIP_Z21_relative_L2"]<=STATE_REPRO_MAX),
        "PCHIP_baseline_shift_relative_L2_le_1e10":
            bool(repro["PCHIP_shift_metric_relative_L2"]<=METRIC_REPRO_MAX),
        "DIRECT382_Q_GE06_BOTH_Z21_relative_L2_le_1e11":
            bool(repro["DIRECT382_Q_GE06_BOTH_Z21_relative_L2"]<=STATE_REPRO_MAX),
        "DIRECT382_Q_GE06_BOTH_shift_relative_L2_le_1e10":
            bool(repro["DIRECT382_Q_GE06_BOTH_shift_metric_relative_L2"]<=METRIC_REPRO_MAX),
        "DIRECT763_Q_GE06_BOTH_Z21_relative_L2_le_1e11":
            bool(repro["DIRECT763_Q_GE06_BOTH_Z21_relative_L2"]<=STATE_REPRO_MAX),
        "DIRECT763_Q_GE06_BOTH_shift_relative_L2_le_1e10":
            bool(repro["DIRECT763_Q_GE06_BOTH_shift_metric_relative_L2"]<=METRIC_REPRO_MAX),
        "projected_p0_exact":bool(p0_exact),
        "frozen_active_count_exact":bool(active_count==ACTIVE_COUNT),
        "all_outputs_finite":finite,
    }
    implementation_ok=bool(all(impl.values()))

    attribution={}
    for res in (382,763):
        full=np.asarray(concat_active(
            runs[f"DIRECT{res}_Q_GE06_BOTH"]["metrics"],masks
        ),float)
        main=np.asarray(concat_active(
            runs[f"DIRECT{res}_Q_GE06_MAIN_ONLY"]["metrics"],masks
        ),float)
        con=np.asarray(concat_active(
            runs[f"DIRECT{res}_Q_GE06_CONSTRAINT_ONLY"]["metrics"],masks
        ),float)
        dmain=rms(main-full)
        dcon=rms(con-full)
        attribution[str(res)]={
            "MAIN_ONLY_vs_frozen_Repair42_Q_GE06_ONLY_active_field_difference_RMS":
                float(dmain),
            "CONSTRAINT_ONLY_vs_frozen_Repair42_Q_GE06_ONLY_active_field_difference_RMS":
                float(dcon),
            "closer_row_family":(
                "CONSTRAINT_ONLY" if dcon<dmain
                else "MAIN_ONLY" if dmain<dcon
                else "TIE"
            ),
        }

    hotspot=hotspot_report(runs,r41npz,r37npz,stage_x,xref)
    if not implementation_ok:
        route="IMPLEMENTATION_FAIL"
        classification="GE19_REPAIR43_QGE06_MAIN_CONSTRAINT_STAGE_SPLIT_IMPLEMENTATION_FAIL"
    elif all(attribution[str(res)]["closer_row_family"]=="CONSTRAINT_ONLY"
             for res in (382,763)):
        route="QGE06_CONSTRAINT_ROW_FIELD_CLOSER_TO_FULL"
        classification="GE19_REPAIR43_QGE06_MAIN_CONSTRAINT_STAGE_SPLIT_COMPLETE"
    elif all(attribution[str(res)]["closer_row_family"]=="MAIN_ONLY"
             for res in (382,763)):
        route="QGE06_MAIN_ROW_FIELD_CLOSER_TO_FULL"
        classification="GE19_REPAIR43_QGE06_MAIN_CONSTRAINT_STAGE_SPLIT_COMPLETE"
    else:
        route="QGE06_MIXED_ROW_SENSITIVITY"
        classification="GE19_REPAIR43_QGE06_MAIN_CONSTRAINT_STAGE_SPLIT_COMPLETE"

    report={
        "classification":classification,
        "predata_classification":"GE19_REPAIR43_PREDATA_QGE06_MAIN_CONSTRAINT_STAGE_SPLIT",
        "diagnostic_only":True,
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "provenance":{
            "input_sha256":hashes,
            "Repair42_classification":j42["classification"],
            "Repair42_route":j42["routing"]["next_route"],
            "Repair41_route":j41["routing"]["next_route"],
            "Repair37_classification":j37["classification"],
            "previous_repairs_relabelled":False,
        },
        "frozen_contract":{
            "Nt":128,
            "Radau_substeps_per_interval":1,
            "target_piece":r42.Q6,
            "direct_source_interpolated":False,
            "science_shift_target_report_only":SCIENCE_TARGET_REPORT_ONLY,
            "threshold_relaxed":False,
            "projected_p0_recomputed":False,
        },
        "stage_and_source_binding":{
            "generated_vs_Repair41_stage_x_abs_max":stage_error,
            "Repair41_PCHIP_target_vs_Repair37_target_relative_L2":target_pchip_repro,
        },
        "frozen_active_mask":{
            "active_count":active_count,
            "S_ref":float(sref),
            "near_null_threshold":float(null_thr),
        },
        "Repair42_reproduction":repro,
        "variant_results":summaries,
        "row_family_active_field_attribution":attribution,
        "registered_hotspot":hotspot,
        "implementation_gates":impl,
        "routing":{"next_route":route},
        "Z21_window_local_particular_certified":False,
        "science_H4_Z21_reclosure_performed":False,
        "lensing_licensed":False,
        "claim_boundary":"Repair43 is a frozen GE06 main-versus-constraint stage-correction diagnostic. The frozen source physics, operator, projected boundary, active mask and 1e-6 science target are unchanged. Repair43 cannot select a physically correct interpolant, relabel prior repairs, certify Z21 or license lensing.",
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
            "classification":"GE19_REPAIR43_QGE06_MAIN_CONSTRAINT_STAGE_SPLIT_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Z21_window_local_particular_certified":False,
            "lensing_licensed":False,
        },indent=2))
        raise
