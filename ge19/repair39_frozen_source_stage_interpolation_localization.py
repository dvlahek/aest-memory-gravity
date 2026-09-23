#!/usr/bin/env python3
"""GE19 Repair39 — frozen-source stage-interpolation localization.

Diagnostic only.

Repair39 freezes the Repair37 Nt128 H4 source nodes and projected p0, the
Repair13 reduced background, the Repair07/Repair11 canonical operator and
the Repair38 endpoint-safe two-stage Radau IIA propagation.  It varies only
the off-node source-at-stage interpolation rule at a fixed Radau substep
factor of 4:

  - PCHIP (frozen Repair38 baseline),
  - CubicSpline, not-a-knot,
  - Akima1DInterpolator.

All methods interpolate the same frozen main and constraint source nodes and
must reproduce those nodes within the preregistered tolerance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator, CubicSpline, Akima1DInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.repair07_window_retarded_reduced_h3_z20_particular as r7
import ge19.repair38_frozen_source_radau_substep_localization as r38

TINY=1e-300

R38_JSON_SHA="08dd95c614118c66e37349e2b8d058e85163812fed77c9b048e0ce57e339e5dd"
R38_NPZ_SHA="aff63771c1800b0db236cd020cf0d2772f6d9a0fd0328573d055392f2c60da67"
R37_JSON_SHA=r38.R37_JSON_SHA
R37_NPZ_SHA=r38.R37_NPZ_SHA
R13_NPZ_SHA=r38.R13_NPZ_SHA
GE15_DENSE_SHA=r38.GE15_DENSE_SHA

METHODS=("PCHIP","CUBIC_SPLINE","AKIMA")
SUBSTEPS=4
ACTIVE_COUNT=23850

PCHIP_STATE_REPRO_MAX=1e-11
PCHIP_SHIFT_REPRO_MAX=1e-10
NODAL_SOURCE_REPRO_MAX=1e-12
DEPENDENCE_RATIO_MIN=4.0
INVARIANT_RATIO_MAX=1.0
SCIENCE_TARGET_REPORT_ONLY=1e-6


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
    q=np.asarray(a,float)
    return float(np.sqrt(np.mean(q*q))) if q.size else 0.0


def load_inputs(rd:Path):
    paths={
        "r38j":rd/"ge19_repair38_frozen_source_radau_substep_localization.json",
        "r38n":rd/"ge19_repair38_frozen_source_radau_substep_localization.npz",
        "r37j":rd/"ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json",
        "r37n":rd/"ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "dense":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "lambda":rd/"ge15_R1_cli_background.dat",
    }
    missing=[str(p) for p in paths.values() if not p.exists()]
    if missing:
        raise RuntimeError("missing Repair39 frozen inputs: "+", ".join(missing))

    expected={
        "r38j":R38_JSON_SHA,
        "r38n":R38_NPZ_SHA,
        "r37j":R37_JSON_SHA,
        "r37n":R37_NPZ_SHA,
        "r13n":R13_NPZ_SHA,
        "dense":GE15_DENSE_SHA,
    }
    hashes={}
    for key,want in expected.items():
        got=sha256(paths[key])
        hashes[key]=got
        if got!=want:
            raise RuntimeError(f"{key} hash mismatch: {got} != {want}")

    j38=json.loads(paths["r38j"].read_text())
    if j38.get("classification")!="GE19_REPAIR38_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION_COMPLETE":
        raise RuntimeError("Repair38 classification mismatch")
    if j38.get("routing",{}).get("next_route")!="PCHIP_OR_OTHER_FLOOR_REMAINS":
        raise RuntimeError("Repair38 route does not license Repair39")
    if j38.get("Z21_window_local_particular_certified") is not False:
        raise RuntimeError("Repair38 unexpectedly certified Z21")

    j37=json.loads(paths["r37j"].read_text())
    if j37.get("classification")!="GE19_REPAIR37_CANCELLATION_SAFE_FD8_H4_Z21_RECLOSURE_FAIL":
        raise RuntimeError("Repair37 classification mismatch")

    return (
        paths,hashes,j38,j37,
        np.load(paths["r38n"]),
        np.load(paths["r37n"]),
        np.load(paths["r13n"]),
    )


def _complex_interp(cls,xgrid,arr,axis=1,**kwargs):
    a=np.asarray(arr,complex)
    re=cls(xgrid,a.real,axis=axis,**kwargs)
    im=cls(xgrid,a.imag,axis=axis,**kwargs)
    def fn(xq):
        return np.asarray(re(xq)+1j*im(xq),complex)
    return fn


def source_interp(xgrid,source_by_beta,m,method):
    if method=="PCHIP":
        return r7._source_interp(xgrid,source_by_beta,m)

    betas=list(r7.BETAS)
    rr=np.stack([
        np.asarray(source_by_beta[b]["rhs"][:,:,m],complex)
        for b in betas
    ],axis=2)
    cc=np.stack([
        np.asarray(source_by_beta[b]["rhs_constraint"][:,:,m],complex)
        for b in betas
    ],axis=2)

    if method=="CUBIC_SPLINE":
        rhs=_complex_interp(
            CubicSpline,xgrid,rr,axis=1,
            bc_type="not-a-knot",extrapolate=False,
        )
        con=_complex_interp(
            CubicSpline,xgrid,cc,axis=1,
            bc_type="not-a-knot",extrapolate=False,
        )
    elif method=="AKIMA":
        rhs=_complex_interp(
            Akima1DInterpolator,xgrid,rr,axis=1,
            extrapolate=False,
        )
        con=_complex_interp(
            Akima1DInterpolator,xgrid,cc,axis=1,
            extrapolate=False,
        )
    else:
        raise ValueError(f"unknown interpolation method: {method}")
    return rhs,con


def expected_source_stacks(source_by_beta,m):
    betas=list(r7.BETAS)
    rr=np.stack([
        np.asarray(source_by_beta[b]["rhs"][:,:,m],complex)
        for b in betas
    ],axis=2)
    cc=np.stack([
        np.asarray(source_by_beta[b]["rhs_constraint"][:,:,m],complex)
        for b in betas
    ],axis=2)
    return rr,cc


def nodal_reproduction(xgrid,source_by_beta,m,method):
    rhs,con=source_interp(xgrid,source_by_beta,m,method)
    rr,cc=expected_source_stacks(source_by_beta,m)
    rri=np.asarray(rhs(np.asarray(xgrid,float)),complex)
    cci=np.asarray(con(np.asarray(xgrid,float)),complex)
    return max(rel_l2(rri,rr),rel_l2(cci,cc))


def stage_points(xgrid,substeps=SUBSTEPS):
    x=np.asarray(xgrid,float)
    pts=[]
    c1=1.0/3.0
    for i in range(len(x)-1):
        H=float(x[i+1]-x[i])
        h=H/float(substeps)
        for isub in range(substeps):
            xl=float(x[i]+isub*h)
            xr=float(x[i+1]) if isub==substeps-1 else float(x[i]+(isub+1)*h)
            hs=float(xr-xl)
            pts.append(float(xl+c1*hs))
            pts.append(xr)
    return np.asarray(pts,float)


def stage_source_relative_difference(xgrid,source_by_beta,m,method):
    if method=="PCHIP":
        return 0.0
    p_rhs,p_con=source_interp(xgrid,source_by_beta,m,"PCHIP")
    q_rhs,q_con=source_interp(xgrid,source_by_beta,m,method)
    xx=stage_points(xgrid)
    vals=[
        rel_l2(q_rhs(xx),p_rhs(xx)),
        rel_l2(q_con(xx),p_con(xx)),
    ]
    return float(max(vals))


def run_method(method,bgs,mod6,mod7,r37npz):
    nt=128
    states={}
    metrics={}
    absres={}
    scales={}
    p0_loaded={}
    finite=True
    linear_res=0.0
    nodal_max=0.0
    stage_diff_max=0.0

    xref=np.asarray(r37npz["x_primary"],float)

    for tag in r7.C_TAGS:
        bg=bgs[(nt,tag)]
        if not np.array_equal(np.asarray(bg["x"],float),xref):
            raise RuntimeError(f"x-grid mismatch for {tag}")

        source=r38.frozen_source_by_beta(r37npz,tag)
        p0=np.asarray(r37npz[f"{tag}_projected_p0_primary"],complex)
        frozen_state=np.asarray(r37npz[f"{tag}_Z21_primary"],complex)

        nb=len(r7.BETAS)
        nm=len(r7.M_SOLVE)
        st=np.empty_like(frozen_state)
        mt=np.empty((nb,nm,nt),float)
        at=np.empty_like(mt)
        sc=np.empty_like(mt)

        for jm,m in enumerate(r7.M_SOLVE):
            k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
            rhsfun,confun=source_interp(xref,source,m,method)

            nodal_max=max(
                nodal_max,
                nodal_reproduction(xref,source,m,method),
            )
            stage_diff_max=max(
                stage_diff_max,
                stage_source_relative_difference(xref,source,m,method),
            )

            y0=np.zeros((8,nb),complex)
            y0[4:8,:]=p0[:,jm,:].T

            Y,rdiag=r38.radau2_integrate_substepped(
                mod6,mod7,bg,tag,k,y0,rhsfun,confun,SUBSTEPS
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
        "nodal_source_relative_L2_max":float(nodal_max),
        "stage_source_vs_PCHIP_relative_L2_max":float(stage_diff_max),
        "canonical_Radau_and_algebraic_linear_residual_max":float(linear_res),
        "all_outputs_finite":bool(finite),
    }


def active_concat(mapping,masks):
    vals=[]
    for tag in r7.C_TAGS:
        vals.append(np.asarray(mapping[tag])[masks[tag]].ravel())
    return np.concatenate(vals)


def active_summary(run,masks):
    v=np.asarray(active_concat(run["metrics"],masks),float)
    a=np.asarray(active_concat(run["absres"],masks),float)
    return {
        "active_sample_count":int(v.size),
        "Linf":float(np.max(v)),
        "RMS":float(np.sqrt(np.mean(v*v))),
        "median":float(np.median(v)),
        "max_absolute_residual":float(np.max(a)),
        "below_1e6_report_only":bool(np.max(v)<=SCIENCE_TARGET_REPORT_ONLY),
    }


def frozen_r38_mapping(r38npz,prefix):
    return {
        tag:np.asarray(r38npz[f"{tag}_{prefix}"])
        for tag in r7.C_TAGS
    }


def concat_states(mapping):
    return np.concatenate([
        np.asarray(mapping[tag],complex).ravel()
        for tag in r7.C_TAGS
    ])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    rd=Path(args.results_dir)
    paths,hashes,j38,j37,r38npz,r37npz,r13npz=load_inputs(rd)

    bgs,mod6,mod7,lambda_diag=r38.build_frozen_operator_context(rd,r13npz)
    sref,null_thr,masks,active_count=r38.frozen_active_masks(r37npz)
    if active_count!=ACTIVE_COUNT:
        raise RuntimeError(f"active count mismatch: {active_count}")

    runs={}
    summaries={}
    for method in METHODS:
        runs[method]=run_method(method,bgs,mod6,mod7,r37npz)
        summaries[method]=active_summary(runs[method],masks)

    # Exact baseline reproduction against frozen Repair38 substep4.
    frozen_z4=frozen_r38_mapping(r38npz,"substep4_Z21")
    frozen_m4=frozen_r38_mapping(r38npz,"substep4_shift_metric")
    frozen_m2=frozen_r38_mapping(r38npz,"substep2_shift_metric")

    pchip_state_repro=rel_l2(
        concat_states(runs["PCHIP"]["states"]),
        concat_states(frozen_z4),
    )
    pchip_shift_repro=rel_l2(
        active_concat(runs["PCHIP"]["metrics"],masks),
        active_concat(frozen_m4,masks),
    )

    # Frozen propagation-discretization reference scale from Repair38.
    m4=active_concat(frozen_m4,masks).astype(float)
    m2=active_concat(frozen_m2,masks).astype(float)
    propagation_reference_rms=rms(m4-m2)
    if not np.isfinite(propagation_reference_rms) or propagation_reference_rms<=0.0:
        raise RuntimeError("invalid frozen Repair38 factor2-to-factor4 reference scale")

    representation={}
    for method in ("CUBIC_SPLINE","AKIMA"):
        ma=active_concat(runs[method]["metrics"],masks).astype(float)
        delta=rms(ma-m4)
        ratio=float(delta/propagation_reference_rms)
        representation[method]={
            "active_shift_metric_difference_vs_PCHIP_RMS":float(delta),
            "difference_over_frozen_Radau_factor2_to_factor4_RMS":ratio,
            "active_Linf_difference_vs_PCHIP":float(
                summaries[method]["Linf"]-summaries["PCHIP"]["Linf"]
            ),
            "active_RMS_difference_vs_PCHIP":float(
                summaries[method]["RMS"]-summaries["PCHIP"]["RMS"]
            ),
            "stage_source_vs_PCHIP_relative_L2_max":
                runs[method]["stage_source_vs_PCHIP_relative_L2_max"],
        }

    nodal_max=max(runs[m]["nodal_source_relative_L2_max"] for m in METHODS)
    finite=bool(all(runs[m]["all_outputs_finite"] for m in METHODS))

    implementation_gates={
        "Repair38_and_Repair37_hashes_and_routes_exact":True,
        "frozen_active_sample_count_exact":bool(active_count==ACTIVE_COUNT),
        "PCHIP_factor4_Z21_vs_Repair38_substep4_global_relative_L2_le_1e11":
            bool(pchip_state_repro<=PCHIP_STATE_REPRO_MAX),
        "PCHIP_factor4_shift_metric_vs_Repair38_substep4_global_relative_L2_le_1e10":
            bool(pchip_shift_repro<=PCHIP_SHIFT_REPRO_MAX),
        "all_interpolants_nodal_source_relative_L2_le_1e12":
            bool(nodal_max<=NODAL_SOURCE_REPRO_MAX),
        "all_outputs_finite":finite,
    }
    impl_ok=bool(all(implementation_gates.values()))

    ratios=[
        representation["CUBIC_SPLINE"]["difference_over_frozen_Radau_factor2_to_factor4_RMS"],
        representation["AKIMA"]["difference_over_frozen_Radau_factor2_to_factor4_RMS"],
    ]

    if not impl_ok:
        route="IMPLEMENTATION_FAIL"
        classification="GE19_REPAIR39_FROZEN_SOURCE_STAGE_INTERPOLATION_LOCALIZATION_IMPLEMENTATION_FAIL"
    elif max(ratios)>=DEPENDENCE_RATIO_MIN:
        route="STAGE_SOURCE_REPRESENTATION_DEPENDENCE_CONFIRMED"
        classification="GE19_REPAIR39_FROZEN_SOURCE_STAGE_INTERPOLATION_LOCALIZATION_COMPLETE"
    elif all(q<=INVARIANT_RATIO_MAX for q in ratios):
        route="STAGE_SOURCE_REPRESENTATION_INVARIANT_OTHER_FLOOR"
        classification="GE19_REPAIR39_FROZEN_SOURCE_STAGE_INTERPOLATION_LOCALIZATION_COMPLETE"
    else:
        route="MIXED_STAGE_REPRESENTATION_SENSITIVITY"
        classification="GE19_REPAIR39_FROZEN_SOURCE_STAGE_INTERPOLATION_LOCALIZATION_COMPLETE"

    lrows=list(lambda_diag.values())
    report={
        "classification":classification,
        "predata_classification":"GE19_REPAIR39_PREDATA_FROZEN_SOURCE_STAGE_INTERPOLATION_LOCALIZATION",
        "diagnostic_only":True,
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "provenance":{
            "input_sha256":hashes,
            "Repair38_classification":j38["classification"],
            "Repair38_route":j38["routing"]["next_route"],
            "Repair37_classification":j37["classification"],
            "Repair37_relabelled":False,
            "Repair38_relabelled":False,
        },
        "frozen_contract":{
            "H4_source_nodes_recomputed":False,
            "projected_p0_recomputed":False,
            "internal_Radau_substeps":SUBSTEPS,
            "interpolation_methods":list(METHODS),
            "science_shift_target_report_only":SCIENCE_TARGET_REPORT_ONLY,
            "threshold_relaxed":False,
        },
        "Lambda_operator":{
            "stage_evaluation_count":int(len(lrows)),
            "all_stage_rho_finite":bool(
                lrows and all(np.isfinite(q["rho_lambda"]) for q in lrows)
            ),
            "lambda_shift_abs_max":float(
                max((q["lambda_shift_abs_max"] for q in lrows),default=math.inf)
            ),
            "lambda_anisotropy_abs_max":float(
                max((q["lambda_anisotropy_abs_max"] for q in lrows),default=math.inf)
            ),
        },
        "frozen_active_mask":{
            "S_ref":float(sref),
            "near_null_threshold":float(null_thr),
            "active_sample_count":int(active_count),
        },
        "PCHIP_baseline_reproduction":{
            "Z21_global_relative_L2":float(pchip_state_repro),
            "active_shift_metric_relative_L2":float(pchip_shift_repro),
        },
        "nodal_interpolation_control":{
            "all_methods_nodal_source_relative_L2_max":float(nodal_max),
            "per_method":{
                m:float(runs[m]["nodal_source_relative_L2_max"])
                for m in METHODS
            },
        },
        "method_results":{
            m:{
                **summaries[m],
                "stage_source_vs_PCHIP_relative_L2_max":
                    runs[m]["stage_source_vs_PCHIP_relative_L2_max"],
                "canonical_Radau_and_algebraic_linear_residual_max":
                    runs[m]["canonical_Radau_and_algebraic_linear_residual_max"],
                "all_outputs_finite":runs[m]["all_outputs_finite"],
            }
            for m in METHODS
        },
        "diagnostic_reference_scale":{
            "Repair38_PCHIP_factor2_to_factor4_active_shift_metric_difference_RMS":
                float(propagation_reference_rms),
            "dependence_ratio_min":DEPENDENCE_RATIO_MIN,
            "invariant_ratio_max":INVARIANT_RATIO_MAX,
        },
        "representation_sensitivity":representation,
        "implementation_gates":implementation_gates,
        "routing":{"next_route":route},
        "Z21_window_local_particular_certified":False,
        "lensing_licensed":False,
        "claim_boundary":"Repair39 is a frozen-node stage-source interpolation diagnostic only. It changes no H4 source node, projected boundary, operator, threshold, finite-eta assumption or observational input. It cannot select a physically preferred interpolant, relabel Repair37/Repair38, certify Z21 or license lensing."
    }

    outj=Path(args.json_out)
    outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")

    save={
        "x_primary":np.asarray(r37npz["x_primary"],float),
        "beta0":np.asarray(r7.BETAS,float),
        "modes_output":np.asarray(r7.M_SOLVE,int),
        "frozen_S_ref":np.asarray(sref,float),
        "frozen_near_null_threshold":np.asarray(null_thr,float),
        "Repair38_factor2_to_factor4_active_shift_metric_difference_RMS":
            np.asarray(propagation_reference_rms,float),
    }
    for tag in r7.C_TAGS:
        save[f"{tag}_frozen_active_mask"]=np.asarray(masks[tag],bool)
        for method in METHODS:
            safe=method.lower()
            save[f"{tag}_{safe}_Z21"]=runs[method]["states"][tag]
            save[f"{tag}_{safe}_shift_metric"]=runs[method]["metrics"][tag]
            save[f"{tag}_{safe}_shift_abs"]=runs[method]["absres"][tag]
            save[f"{tag}_{safe}_shift_scale"]=runs[method]["scales"][tag]
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
            "classification":"GE19_REPAIR39_FROZEN_SOURCE_STAGE_INTERPOLATION_LOCALIZATION_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Z21_window_local_particular_certified":False,
            "lensing_licensed":False,
        },indent=2))
        raise
