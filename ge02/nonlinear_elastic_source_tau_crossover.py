#!/usr/bin/env python3
"""GE02 finite-amplitude nonlinear elastic-source tau crossover.

Reuses the frozen NL1C4 expanding finite-amplitude reference and the exact
NL0B action-derived source diagnostics. Only tauH0 is varied across the
predeclared Maxwell/Drude crossover grid.
"""

from pathlib import Path
import argparse
import json
import math
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import nl1c4.expanding_memory_source_trajectory as c4

TAUS = np.asarray([0.1,0.3,0.5,0.7,1.0,3.0,10.0], dtype=float)
TINY = 1.0e-300


def vec(rows, field):
    return np.asarray([r[field] for r in rows], dtype=float)


def max_pointwise_relative(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    den=np.maximum(np.maximum(np.abs(aa),np.abs(bb)),TINY)
    return float(np.max(np.abs(aa-bb)/den))


def global_rel_l2(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def l2(x):
    return float(np.linalg.norm(np.asarray(x,float)))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--trace",required=True)
    ap.add_argument("--artifact-meta-json",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    trace=Path(args.trace)
    if trace.name != c4.TRACE_NAME:
        raise RuntimeError(f"frozen trace must be named {c4.TRACE_NAME}")

    artifact=c4.validate_artifact_metadata(Path(args.artifact_meta_json))
    if not artifact.get("pass",False):
        raise RuntimeError(f"frozen artifact provenance mismatch: {artifact}")

    rows=c4.read_trace(trace)
    histories,k_miss,native_mismatch=c4.select_and_align(rows)

    original_tau=float(c4.TAUH0)
    result_rows=[]
    B_series=[]
    R_series=[]
    all_tau_pass=True
    all_reported=[]
    try:
        for tau in TAUS:
            c4.TAUH0=float(tau)
            evaluations={}
            for order in (c4.CONTROL_ORDER,c4.PRIMARY_ORDER):
                for nx in c4.NX_VALUES:
                    evaluations[(order,nx)]=c4.evaluate(histories,order,nx)

            primary=evaluations[(c4.PRIMARY_ORDER,c4.NX_VALUES[-1])]
            ntime=len(primary)
            xrms_errs=[]
            for vals in evaluations.values():
                xrms_errs.extend([float(r["x_rms_relative_error"]) for r in vals])

            B_q_c=vec(evaluations[(c4.CONTROL_ORDER,512)],"B_rms_per_m")
            B_q_p=vec(evaluations[(c4.PRIMARY_ORDER,512)],"B_rms_per_m")
            R_q_c=vec(evaluations[(c4.CONTROL_ORDER,512)],"rhohat_mem_mean_per_m2")
            R_q_p=vec(evaluations[(c4.PRIMARY_ORDER,512)],"rhohat_mem_mean_per_m2")
            B_nx_256=vec(evaluations[(c4.PRIMARY_ORDER,256)],"B_rms_per_m")
            B_nx_512=vec(evaluations[(c4.PRIMARY_ORDER,512)],"B_rms_per_m")
            R_nx_256=vec(evaluations[(c4.PRIMARY_ORDER,256)],"rhohat_mem_mean_per_m2")
            R_nx_512=vec(evaluations[(c4.PRIMARY_ORDER,512)],"rhohat_mem_mean_per_m2")

            controls={
                "quadrature_B_rms":max_pointwise_relative(B_q_c,B_q_p),
                "quadrature_rhohat_mem":max_pointwise_relative(R_q_c,R_q_p),
                "spatial_B_rms":max_pointwise_relative(B_nx_256,B_nx_512),
                "spatial_rhohat_mem":max_pointwise_relative(R_nx_256,R_nx_512),
            }

            finite=bool(
                np.isfinite(B_q_p).all()
                and np.isfinite(R_q_p).all()
                and np.isfinite(np.asarray(xrms_errs,float)).all()
            )
            positive_B=bool(np.all(B_q_p>0))
            positive_R=bool(np.all(R_q_p>0))
            tau_pass=bool(
                ntime>=c4.MIN_COMMON_TIMES
                and max(xrms_errs)<=c4.XRMS_REL_MAX
                and controls["quadrature_B_rms"]<=c4.QUAD_REL_MAX
                and controls["quadrature_rhohat_mem"]<=c4.QUAD_REL_MAX
                and controls["spatial_B_rms"]<=c4.NX_REL_MAX
                and controls["spatial_rhohat_mem"]<=c4.NX_REL_MAX
                and finite and positive_B and positive_R
            )
            all_tau_pass=bool(all_tau_pass and tau_pass)

            z=np.asarray([r["z"] for r in primary],float)
            imax=int(np.argmax(R_q_p))
            result_rows.append({
                "tauH0":float(tau),
                "evaluation_times":int(ntime),
                "x_rms_reconstruction_relative_error_max":float(max(xrms_errs)),
                "controls":{
                    "quadrature_B_rms_max_pointwise_relative_difference":controls["quadrature_B_rms"],
                    "quadrature_rhohat_mem_max_pointwise_relative_difference":controls["quadrature_rhohat_mem"],
                    "spatial_B_rms_max_pointwise_relative_difference":controls["spatial_B_rms"],
                    "spatial_rhohat_mem_max_pointwise_relative_difference":controls["spatial_rhohat_mem"],
                },
                "B_rms_time_L2_norm":l2(B_q_p),
                "rhohat_mem_time_L2_norm":l2(R_q_p),
                "rhohat_mem_peak":{
                    "z":float(z[imax]),
                    "value_per_m2":float(R_q_p[imax]),
                },
                "B_rms_min":float(np.min(B_q_p)),
                "B_rms_max":float(np.max(B_q_p)),
                "rhohat_mem_min":float(np.min(R_q_p)),
                "rhohat_mem_max":float(np.max(R_q_p)),
                "all_values_finite":finite,
                "B_rms_positive":positive_B,
                "rhohat_mem_positive":positive_R,
                "pass":tau_pass,
            })

            B_series.append(B_q_p.copy())
            R_series.append(R_q_p.copy())
            all_reported.extend(B_q_p.tolist())
            all_reported.extend(R_q_p.tolist())
    finally:
        c4.TAUH0=original_tau

    B_series=np.asarray(B_series,float)
    R_series=np.asarray(R_series,float)
    B_norm=np.linalg.norm(B_series,axis=1)
    R_norm=np.linalg.norm(R_series,axis=1)
    i10=int(np.where(np.isclose(TAUS,10.0))[0][0])
    for i,row in enumerate(result_rows):
        row["B_rms_norm_relative_to_tauH0_10"]=float(B_norm[i]/max(B_norm[i10],TINY))
        row["rhohat_mem_norm_relative_to_tauH0_10"]=float(R_norm[i]/max(R_norm[i10],TINY))

    gates={
        "artifact_digest_exact":bool(artifact.get("pass",False)),
        "all_six_k_modes_relative_error_le_1e12":bool(k_miss<=c4.K_REL_MAX),
        "common_native_grid_relative_mismatch_le_1e12":bool(native_mismatch<=1.0e-12),
        "all_tau_numerical_action_source_controls_pass":bool(all_tau_pass),
        "all_reported_quantities_finite":bool(np.isfinite(np.asarray(all_reported,float)).all()),
        "no_finite_eta_observation_likelihood_halo_or_collapse_input":True,
    }
    passed=bool(all(gates.values()))
    classification=(
        "GE02_NONLINEAR_ELASTIC_SOURCE_TAU_CROSSOVER_PASS"
        if passed else
        "GE02_NONLINEAR_ELASTIC_SOURCE_TAU_CROSSOVER_FAIL"
    )

    result={
        "classification":classification,
        "predata_classification":"GE02_PREDATA_NONLINEAR_ELASTIC_SOURCE_TAU_CROSSOVER",
        "uses_observational_data":False,
        "scope":"Finite-amplitude action-derived NL0B elastic-source tau map on the frozen expanding v0.77 reference. Nonlinear at source/stress level; not a self-consistent finite-eta nonlinear evolution.",
        "artifact_provenance":artifact,
        "trace":{
            "file":c4.TRACE_NAME,
            "requested_k_relative_miss_max":float(k_miss),
            "common_native_grid_relative_mismatch_max":float(native_mismatch),
            "native_history_length":int(len(histories[0])),
        },
        "tauH0_values":[float(x) for x in TAUS],
        "rows":result_rows,
        "descriptive":{
            "B_rms_norm_monotone_nondecreasing_with_tau":bool(np.all(np.diff(B_norm)>=-1e-12*max(float(np.max(B_norm)),1.0))),
            "rhohat_mem_norm_monotone_nondecreasing_with_tau":bool(np.all(np.diff(R_norm)>=-1e-12*max(float(np.max(R_norm)),1.0))),
            "B_rms_time_L2_norms":[float(x) for x in B_norm],
            "rhohat_mem_time_L2_norms":[float(x) for x in R_norm],
        },
        "gates":gates,
        "claim_boundary":"PASS certifies a controlled nonlinear action-source tau map only. It does not certify finite physical eta, a self-consistent nonlinear trajectory, a halo/collapse observable, or observational evidence.",
    }

    out_json=Path(args.json_out); out_json.parent.mkdir(parents=True,exist_ok=True)
    out_json.write_text(json.dumps(result,indent=2)+"\n")
    np.savez_compressed(
        args.npz_out,
        tauH0=TAUS,
        B_rms_series=B_series,
        rhohat_mem_series=R_series,
        B_rms_time_L2_norm=B_norm,
        rhohat_mem_time_L2_norm=R_norm,
    )
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
