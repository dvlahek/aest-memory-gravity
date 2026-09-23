#!/usr/bin/env python3
"""GE19 Repair40 — piecewise stage-source decomposition.

Diagnostic only.

Decompose the frozen Repair39 AKIMA(total)-PCHIP(total) dependence into the
six frozen Repair37 H4 source pieces plus the exact nonlinear interpolation-
coupling residual.  No H4 source node is recomputed.
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
SUBSTEPS=4
ACTIVE_COUNT=23850

R39_JSON_SHA="b058d4acb51dd4e0b964fcccb306b7eb105466941b5e0900ae0c84a29374624e"
R39_NPZ_SHA="0bf5b0c2f26cc06b98eab1fb326757ed409cf91c86c23e995251dfd32571c451"
R37_JSON_SHA=r38.R37_JSON_SHA
R37_NPZ_SHA=r38.R37_NPZ_SHA
R13_NPZ_SHA=r38.R13_NPZ_SHA
GE15_DENSE_SHA=r38.GE15_DENSE_SHA

PCHIP_STATE_REPRO_MAX=1e-11
PCHIP_SHIFT_REPRO_MAX=1e-10
AKIMA_STATE_REPRO_MAX=1e-11
AKIMA_SHIFT_REPRO_MAX=1e-10
NODAL_REPRO_MAX=1e-12
STAGE_CLOSURE_MAX=1e-12
STATE_RESPONSE_CLOSURE_MAX=1e-9

PIECES=(
    "2Q_GE06_cross",
    "2Q_GE07_cross",
    "2Q_Lambda_cross",
    "2DY2",
    "2M1_GE05_mapped",
    "2M2_GE05_mapped",
)
COUPLING="INTERPOLATION_COUPLING"
COMPONENTS=PIECES+(COUPLING,)
BASELINE="PCHIP_BASELINE"
FULL="AKIMA_FULL"
VARIANTS=(BASELINE,FULL)+COMPONENTS


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


def complex_alignment(a,b)->float:
    aa=np.asarray(a,complex).ravel()
    bb=np.asarray(b,complex).ravel()
    den=float(np.linalg.norm(aa)*np.linalg.norm(bb))
    if den<=TINY:
        return 0.0
    return float(np.real(np.vdot(aa,bb))/den)


def real_alignment(a,b)->float:
    aa=np.asarray(a,float).ravel()
    bb=np.asarray(b,float).ravel()
    den=float(np.linalg.norm(aa)*np.linalg.norm(bb))
    if den<=TINY:
        return 0.0
    return float(np.dot(aa,bb)/den)


def load_inputs(rd:Path):
    paths={
        "r39j":rd/"ge19_repair39_frozen_source_stage_interpolation_localization.json",
        "r39n":rd/"ge19_repair39_frozen_source_stage_interpolation_localization.npz",
        "r37j":rd/"ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json",
        "r37n":rd/"ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "dense":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "lambda":rd/"ge15_R1_cli_background.dat",
    }
    missing=[str(p) for p in paths.values() if not p.exists()]
    if missing:
        raise RuntimeError("missing Repair40 frozen inputs: "+", ".join(missing))

    expected={
        "r39j":R39_JSON_SHA,
        "r39n":R39_NPZ_SHA,
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

    j39=json.loads(paths["r39j"].read_text())
    if j39.get("classification")!="GE19_REPAIR39_FROZEN_SOURCE_STAGE_INTERPOLATION_LOCALIZATION_COMPLETE":
        raise RuntimeError("Repair39 classification mismatch")
    if j39.get("routing",{}).get("next_route")!="STAGE_SOURCE_REPRESENTATION_DEPENDENCE_CONFIRMED":
        raise RuntimeError("Repair39 route does not license Repair40")
    if not all(j39.get("implementation_gates",{}).values()):
        raise RuntimeError("Repair39 implementation gates are not all true")

    j37=json.loads(paths["r37j"].read_text())
    if j37.get("classification")!="GE19_REPAIR37_CANCELLATION_SAFE_FD8_H4_Z21_RECLOSURE_FAIL":
        raise RuntimeError("Repair37 classification mismatch")

    return (
        paths,hashes,j39,j37,
        np.load(paths["r39n"]),
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


def _sub(a,b):
    def fn(xq):
        return np.asarray(a(xq),complex)-np.asarray(b(xq),complex)
    return fn


def _add(a,b):
    def fn(xq):
        return np.asarray(a(xq),complex)+np.asarray(b(xq),complex)
    return fn


def _sum_funcs(funcs):
    funcs=tuple(funcs)
    def fn(xq):
        vals=[np.asarray(f(xq),complex) for f in funcs]
        out=np.zeros_like(vals[0])
        for v in vals:
            out=out+v
        return out
    return fn


def make_source_bundle(xgrid,total_by_beta,pieces_by_name,m):
    p_rhs,p_con=r39.source_interp(xgrid,total_by_beta,m,"PCHIP")
    a_rhs,a_con=r39.source_interp(xgrid,total_by_beta,m,"AKIMA")

    piece_delta={}
    for piece in PIECES:
        pp_rhs,pp_con=r39.source_interp(
            xgrid,pieces_by_name[piece],m,"PCHIP"
        )
        pa_rhs,pa_con=r39.source_interp(
            xgrid,pieces_by_name[piece],m,"AKIMA"
        )
        piece_delta[piece]=(_sub(pa_rhs,pp_rhs),_sub(pa_con,pp_con))

    sum_piece_rhs=_sum_funcs([piece_delta[p][0] for p in PIECES])
    sum_piece_con=_sum_funcs([piece_delta[p][1] for p in PIECES])
    full_delta_rhs=_sub(a_rhs,p_rhs)
    full_delta_con=_sub(a_con,p_con)
    coupling_rhs=_sub(full_delta_rhs,sum_piece_rhs)
    coupling_con=_sub(full_delta_con,sum_piece_con)
    piece_delta[COUPLING]=(coupling_rhs,coupling_con)

    def funcs(variant):
        if variant==BASELINE:
            return p_rhs,p_con
        if variant==FULL:
            return a_rhs,a_con
        if variant in COMPONENTS:
            dr,dc=piece_delta[variant]
            return _add(p_rhs,dr),_add(p_con,dc)
        raise ValueError(variant)

    return {
        "baseline":(p_rhs,p_con),
        "full":(a_rhs,a_con),
        "deltas":piece_delta,
        "variant":funcs,
    }


def source_total_nodes(total_by_beta,m):
    betas=list(r7.BETAS)
    rr=np.stack([
        np.asarray(total_by_beta[b]["rhs"][:,:,m],complex)
        for b in betas
    ],axis=2)
    cc=np.stack([
        np.asarray(total_by_beta[b]["rhs_constraint"][:,:,m],complex)
        for b in betas
    ],axis=2)
    return rr,cc


def run_variant(variant,bgs,mod6,mod7,r37npz):
    nt=128
    states={}
    metrics={}
    absres={}
    scales={}
    finite=True
    linear_res=0.0
    nodal_rel_max=0.0
    xref=np.asarray(r37npz["x_primary"],float)

    for tag in r7.C_TAGS:
        bg=bgs[(nt,tag)]
        if not np.array_equal(np.asarray(bg["x"],float),xref):
            raise RuntimeError(f"Repair40 x-grid mismatch for {tag}")

        total=r38.frozen_source_by_beta(r37npz,tag)
        pieces={p:frozen_piece_by_beta(r37npz,tag,p) for p in PIECES}
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
            bundle=make_source_bundle(xref,total,pieces,m)
            rhsfun,confun=bundle["variant"](variant)

            # Every component variant must retain the same frozen source nodes.
            rr0,cc0=source_total_nodes(total,m)
            nodal_rel_max=max(
                nodal_rel_max,
                rel_l2(np.asarray(rhsfun(xref),complex),rr0),
                rel_l2(np.asarray(confun(xref),complex),cc0),
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

    return {
        "states":states,
        "metrics":metrics,
        "absres":absres,
        "scales":scales,
        "nodal_source_relative_L2_max":float(nodal_rel_max),
        "canonical_Radau_and_algebraic_linear_residual_max":float(linear_res),
        "all_outputs_finite":bool(finite),
    }


def active_concat(mapping,masks):
    return np.concatenate([
        np.asarray(mapping[tag])[masks[tag]].ravel()
        for tag in r7.C_TAGS
    ])


def concat_states(mapping):
    return np.concatenate([
        np.asarray(mapping[tag],complex).ravel()
        for tag in r7.C_TAGS
    ])


def frozen_r39_mapping(r39npz,method,suffix):
    safe=method.lower()
    return {
        tag:np.asarray(r39npz[f"{tag}_{safe}_{suffix}"])
        for tag in r7.C_TAGS
    }


def active_summary(run,masks):
    v=np.asarray(active_concat(run["metrics"],masks),float)
    return {
        "active_sample_count":int(v.size),
        "Linf":float(np.max(v)),
        "RMS":rms(v),
        "median":float(np.median(v)),
    }


def stage_source_decomposition(r37npz):
    xref=np.asarray(r37npz["x_primary"],float)
    xx=r39.stage_points(xref,SUBSTEPS)

    full2=0.0
    closure2=0.0
    comp2={c:0.0 for c in COMPONENTS}

    for tag in r7.C_TAGS:
        total=r38.frozen_source_by_beta(r37npz,tag)
        pieces={p:frozen_piece_by_beta(r37npz,tag,p) for p in PIECES}
        for m in r7.M_SOLVE:
            bundle=make_source_bundle(xref,total,pieces,m)
            pr,pc=bundle["baseline"]
            ar,ac=bundle["full"]
            fdr=np.asarray(ar(xx)-pr(xx),complex)
            fdc=np.asarray(ac(xx)-pc(xx),complex)
            sumr=np.zeros_like(fdr)
            sumc=np.zeros_like(fdc)
            for comp in COMPONENTS:
                dr,dc=bundle["deltas"][comp]
                vr=np.asarray(dr(xx),complex)
                vc=np.asarray(dc(xx),complex)
                comp2[comp]+=float(np.linalg.norm(vr)**2+np.linalg.norm(vc)**2)
                sumr+=vr
                sumc+=vc
            full2+=float(np.linalg.norm(fdr)**2+np.linalg.norm(fdc)**2)
            closure2+=float(
                np.linalg.norm(fdr-sumr)**2+np.linalg.norm(fdc-sumc)**2
            )

    fullnorm=math.sqrt(full2)
    return {
        "closure_relative_L2":float(math.sqrt(closure2)/max(fullnorm,TINY)),
        "component_stage_source_delta_L2_over_full":{
            c:float(math.sqrt(comp2[c])/max(fullnorm,TINY))
            for c in COMPONENTS
        },
        "full_stage_source_delta_L2":float(fullnorm),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    rd=Path(args.results_dir)
    paths,hashes,j39,j37,r39npz,r37npz,r13npz=load_inputs(rd)
    bgs,mod6,mod7,lambda_diag=r38.build_frozen_operator_context(rd,r13npz)
    sref,null_thr,masks,active_count=r38.frozen_active_masks(r37npz)
    if active_count!=ACTIVE_COUNT:
        raise RuntimeError(f"active count mismatch: {active_count}")

    stage_diag=stage_source_decomposition(r37npz)

    runs={}
    summaries={}
    for variant in VARIANTS:
        runs[variant]=run_variant(variant,bgs,mod6,mod7,r37npz)
        summaries[variant]=active_summary(runs[variant],masks)

    frozen_p_state=frozen_r39_mapping(r39npz,"pchip","Z21")
    frozen_p_metric=frozen_r39_mapping(r39npz,"pchip","shift_metric")
    frozen_a_state=frozen_r39_mapping(r39npz,"akima","Z21")
    frozen_a_metric=frozen_r39_mapping(r39npz,"akima","shift_metric")

    p_state_repro=rel_l2(
        concat_states(runs[BASELINE]["states"]),
        concat_states(frozen_p_state),
    )
    p_shift_repro=rel_l2(
        active_concat(runs[BASELINE]["metrics"],masks),
        active_concat(frozen_p_metric,masks),
    )
    a_state_repro=rel_l2(
        concat_states(runs[FULL]["states"]),
        concat_states(frozen_a_state),
    )
    a_shift_repro=rel_l2(
        active_concat(runs[FULL]["metrics"],masks),
        active_concat(frozen_a_metric,masks),
    )

    s0=concat_states(runs[BASELINE]["states"])
    sf=concat_states(runs[FULL]["states"])
    full_state_delta=sf-s0
    full_state_norm=float(np.linalg.norm(full_state_delta))

    m0=np.asarray(active_concat(runs[BASELINE]["metrics"],masks),float)
    mf=np.asarray(active_concat(runs[FULL]["metrics"],masks),float)
    full_metric_delta=mf-m0
    full_metric_rms=rms(full_metric_delta)

    comp_state_deltas={}
    comp_metric_deltas={}
    component_report={}
    for comp in COMPONENTS:
        sd=concat_states(runs[comp]["states"])-s0
        md=np.asarray(active_concat(runs[comp]["metrics"],masks),float)-m0
        comp_state_deltas[comp]=sd
        comp_metric_deltas[comp]=md
        component_report[comp]={
            "stage_source_delta_L2_over_full_Akima_minus_PCHIP":
                stage_diag["component_stage_source_delta_L2_over_full"][comp],
            "Z21_response_L2_over_full_Akima_minus_PCHIP":
                float(np.linalg.norm(sd)/max(full_state_norm,TINY)),
            "Z21_response_complex_alignment_with_full_response":
                complex_alignment(full_state_delta,sd),
            "active_shift_metric_difference_RMS":
                rms(md),
            "active_shift_metric_difference_RMS_over_full_Akima_minus_PCHIP":
                float(rms(md)/max(full_metric_rms,TINY)),
            "active_shift_metric_difference_alignment_with_full_shift_difference":
                real_alignment(full_metric_delta,md),
            "active_Linf_change_from_PCHIP":
                float(summaries[comp]["Linf"]-summaries[BASELINE]["Linf"]),
            "active_RMS_change_from_PCHIP":
                float(summaries[comp]["RMS"]-summaries[BASELINE]["RMS"]),
        }

    sum_state=np.zeros_like(full_state_delta)
    for comp in COMPONENTS:
        sum_state+=comp_state_deltas[comp]
    state_closure=rel_l2(full_state_delta,sum_state)

    rank_state=sorted(
        COMPONENTS,
        key=lambda c:component_report[c][
            "Z21_response_L2_over_full_Akima_minus_PCHIP"
        ],
        reverse=True,
    )
    rank_shift=sorted(
        COMPONENTS,
        key=lambda c:component_report[c][
            "active_shift_metric_difference_RMS_over_full_Akima_minus_PCHIP"
        ],
        reverse=True,
    )
    top_state=rank_state[0]
    top_shift=rank_shift[0]
    targets=[top_state] if top_state==top_shift else [top_state,top_shift]
    if COUPLING in targets:
        followup_kind="SUM_BEFORE_INTERPOLATION_VS_INTERPOLATION_BEFORE_SUM"
    else:
        followup_kind="DIRECT_FINE_GRID_RECONSTRUCTION_OF_TARGET_PHYSICAL_PIECES"

    nodal_max=max(runs[v]["nodal_source_relative_L2_max"] for v in VARIANTS)
    finite=bool(all(runs[v]["all_outputs_finite"] for v in VARIANTS))
    implementation_gates={
        "Repair39_and_Repair37_hashes_and_routes_exact":True,
        "frozen_active_sample_count_exact":bool(active_count==ACTIVE_COUNT),
        "PCHIP_baseline_Z21_vs_Repair39_relative_L2_le_1e11":
            bool(p_state_repro<=PCHIP_STATE_REPRO_MAX),
        "PCHIP_baseline_shift_metric_vs_Repair39_relative_L2_le_1e10":
            bool(p_shift_repro<=PCHIP_SHIFT_REPRO_MAX),
        "AKIMA_full_Z21_vs_Repair39_relative_L2_le_1e11":
            bool(a_state_repro<=AKIMA_STATE_REPRO_MAX),
        "AKIMA_full_shift_metric_vs_Repair39_relative_L2_le_1e10":
            bool(a_shift_repro<=AKIMA_SHIFT_REPRO_MAX),
        "component_variants_reproduce_frozen_source_nodes_relative_L2_le_1e12":
            bool(nodal_max<=NODAL_REPRO_MAX),
        "stage_source_decomposition_closure_relative_L2_le_1e12":
            bool(stage_diag["closure_relative_L2"]<=STAGE_CLOSURE_MAX),
        "propagated_Z21_response_decomposition_closure_relative_L2_le_1e9":
            bool(state_closure<=STATE_RESPONSE_CLOSURE_MAX),
        "all_outputs_finite":finite,
    }
    impl_ok=bool(all(implementation_gates.values()))

    if impl_ok:
        classification="GE19_REPAIR40_PIECEWISE_STAGE_SOURCE_DECOMPOSITION_COMPLETE"
        route="PIECEWISE_STAGE_SOURCE_DECOMPOSITION_COMPLETE"
    else:
        classification="GE19_REPAIR40_PIECEWISE_STAGE_SOURCE_DECOMPOSITION_IMPLEMENTATION_FAIL"
        route="IMPLEMENTATION_FAIL"

    lrows=list(lambda_diag.values())
    report={
        "classification":classification,
        "predata_classification":"GE19_REPAIR40_PREDATA_PIECEWISE_STAGE_SOURCE_DECOMPOSITION",
        "diagnostic_only":True,
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "provenance":{
            "input_sha256":hashes,
            "Repair39_classification":j39["classification"],
            "Repair39_route":j39["routing"]["next_route"],
            "Repair37_classification":j37["classification"],
            "Repair37_relabelled":False,
            "Repair39_relabelled":False,
        },
        "frozen_contract":{
            "H4_source_nodes_recomputed":False,
            "projected_p0_recomputed":False,
            "internal_Radau_substeps":SUBSTEPS,
            "physical_pieces":list(PIECES),
            "additional_component":COUPLING,
            "science_shift_target_report_only":1e-6,
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
        "baseline_full_reproduction":{
            "PCHIP_Z21_relative_L2":float(p_state_repro),
            "PCHIP_active_shift_metric_relative_L2":float(p_shift_repro),
            "AKIMA_Z21_relative_L2":float(a_state_repro),
            "AKIMA_active_shift_metric_relative_L2":float(a_shift_repro),
        },
        "source_decomposition":{
            "stage_source_closure_relative_L2":
                stage_diag["closure_relative_L2"],
            "full_Akima_minus_PCHIP_stage_source_L2":
                stage_diag["full_stage_source_delta_L2"],
            "component_stage_source_delta_L2_over_full":
                stage_diag["component_stage_source_delta_L2_over_full"],
            "nodal_source_reproduction_relative_L2_max":float(nodal_max),
        },
        "baseline_and_full_results":{
            BASELINE:summaries[BASELINE],
            FULL:summaries[FULL],
            "full_Akima_minus_PCHIP_Z21_response_L2":float(full_state_norm),
            "full_Akima_minus_PCHIP_active_shift_metric_difference_RMS":
                float(full_metric_rms),
        },
        "component_results":{
            comp:{
                **summaries[comp],
                **component_report[comp],
                "canonical_Radau_and_algebraic_linear_residual_max":
                    runs[comp]["canonical_Radau_and_algebraic_linear_residual_max"],
                "all_outputs_finite":runs[comp]["all_outputs_finite"],
            }
            for comp in COMPONENTS
        },
        "propagated_linear_response_closure":{
            "Z21_response_decomposition_relative_L2":float(state_closure),
        },
        "rankings":{
            "descending_Z21_response_L2":list(rank_state),
            "descending_active_shift_metric_difference_RMS":list(rank_shift),
        },
        "deterministic_next_target":{
            "largest_Z21_response_component":top_state,
            "largest_shift_metric_effect_component":top_shift,
            "mandatory_followup_targets":targets,
            "followup_kind":followup_kind,
        },
        "implementation_gates":implementation_gates,
        "routing":{"next_route":route},
        "Z21_window_local_particular_certified":False,
        "lensing_licensed":False,
        "claim_boundary":"Repair40 is a frozen-node piecewise source-representation decomposition only. It changes no H4 physics, source node, projected boundary, threshold, finite-eta assumption or observational input. It cannot relabel prior repairs, select a physically preferred interpolant, certify Z21 or license lensing."
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
    }
    for tag in r7.C_TAGS:
        save[f"{tag}_frozen_active_mask"]=np.asarray(masks[tag],bool)
        save[f"{tag}_pchip_Z21"]=runs[BASELINE]["states"][tag]
        save[f"{tag}_pchip_shift_metric"]=runs[BASELINE]["metrics"][tag]
        save[f"{tag}_akima_Z21"]=runs[FULL]["states"][tag]
        save[f"{tag}_akima_shift_metric"]=runs[FULL]["metrics"][tag]
        for comp in COMPONENTS:
            safe=comp.lower()
            save[f"{tag}_{safe}_Z21_response_delta"]=(
                runs[comp]["states"][tag]-runs[BASELINE]["states"][tag]
            )
            save[f"{tag}_{safe}_shift_metric_delta"]=(
                runs[comp]["metrics"][tag]-runs[BASELINE]["metrics"][tag]
            )
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
            "classification":"GE19_REPAIR40_PIECEWISE_STAGE_SOURCE_DECOMPOSITION_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Z21_window_local_particular_certified":False,
            "lensing_licensed":False,
        },indent=2))
        raise
