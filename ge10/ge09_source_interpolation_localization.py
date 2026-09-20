#!/usr/bin/env python3
"""GE10: result-informed localization of the frozen GE09 source-grid failure.

Uses only the exact frozen GE09 artifact. No CLASS execution and no physics
or threshold change.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator, interp1d

import ge09.repair01_dense_accepted_step_local_jet_bridge as g9

EXPECTED_ARTIFACT_ID=10600457104
EXPECTED_DIGEST="sha256:494639b2074336e704e06cf18b8875bc88d71c62cebfdb687e8e4c3f5270da38"
EXPECTED_PRIMARY=0.00010032254188771416
REPRO_TOL=1e-15
P_MIN=2.5
STRIDES=(4,2,1)


def decimate_stride(rows,stride):
    if stride==1:
        return list(rows)
    idx=list(range(0,len(rows),stride))
    if idx[-1]!=len(rows)-1:
        idx.append(len(rows)-1)
    return [rows[i] for i in idx]


def scalar_aor(a,b):
    ae=abs(float(a)-float(b))
    re=ae/max(abs(float(a)),abs(float(b)),g9.TINY)
    return min(ae,re)


def artifact_dir(root:Path)->Path:
    hits=list(root.rglob("ge09_dense_accepted_step_trace.dat"))
    if len(hits)!=1:
        raise RuntimeError(f"expected one frozen GE09 dense trace, found {len(hits)}")
    return hits[0].parent


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact-root",required=True)
    ap.add_argument("--artifact-meta-json",required=True)
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    meta=json.loads(Path(args.artifact_meta_json).read_text())
    aid=int(meta.get("id",-1))
    digest=str(meta.get("digest",""))
    provenance_pass=bool(
        aid==EXPECTED_ARTIFACT_ID
        and digest==EXPECTED_DIGEST
        and meta.get("expired") is False
    )

    rd=artifact_dir(Path(args.artifact_root))
    dense=g9.read_table(rd/"ge09_dense_accepted_step_trace.dat")
    source=g9.read_table(rd/"ge09_source_state_trace.dat")
    parent=json.loads((rd/"ge09_repair01_dense_accepted_step_local_jet_bridge.json").read_text())
    if parent.get("classification")!="GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL":
        raise RuntimeError("frozen parent classification mismatch")

    modes,kmiss=g9.group_modes(dense)

    selected=[]
    for r in source:
        if not (g9.AMIN-1e-12<=r["a"]<=g9.AMAX+1e-12):
            continue
        ik,e=g9.nearest_k(r["k"])
        if e<=1e-12:
            selected.append((ik,r))
    if len(selected)!=48:
        raise RuntimeError(f"expected 48 frozen source rows, found {len(selected)}")

    stride_rows={}
    top_primary=[]
    primary_details=[]
    for stride in STRIDES:
        interps=[g9.build_interps(decimate_stride(m,stride)) for m in modes]
        vals=[]
        details=[]
        for ik,r in selected:
            x=math.log(r["a"])
            pred=float(interps[ik]["delta_dark"](x))
            actual=float(r["delta_dark"])
            ae=abs(pred-actual)
            re=ae/max(abs(pred),abs(actual),g9.TINY)
            ao=min(ae,re)
            vals.append(ao)
            details.append({
                "ik":int(ik),"k_Mpc":float(r["k"]),"k_h_Mpc":float(r["k"]/(g9.H0_CLASS*299792.458/100.0)),
                "a":float(r["a"]),"z":float(1.0/r["a"]-1.0),"tau":float(r["tau"]),
                "pred":pred,"actual":actual,
                "absolute_error":ae,"relative_error":re,"abs_or_rel":ao,
            })
        stride_rows[str(stride)]={
            "global_max_abs_or_rel":float(max(vals)),
            "argmax":details[int(np.argmax(vals))],
        }
        if stride==1:
            primary_details=details
            top_primary=sorted(details,key=lambda x:x["abs_or_rel"],reverse=True)[:10]

    worst=stride_rows["1"]["argmax"]
    ik=int(worst["ik"])
    xw=math.log(worst["a"])
    m=modes[ik]
    xx=np.log(np.asarray([r["a"] for r in m],float))
    j=int(np.searchsorted(xx,xw)-1)
    j=max(0,min(j,len(m)-2))
    left,right=m[j],m[j+1]
    frac=float((xw-xx[j])/(xx[j+1]-xx[j]))
    gap=float(xx[j+1]-xx[j])
    swing=max(
        abs(float(right["delta_dark"])-float(left["delta_dark"])),
        abs(float(left["delta_dark"])),
        abs(float(right["delta_dark"])),
        g9.TINY,
    )
    local_swing_norm=float(worst["absolute_error"]/swing)

    y=np.asarray([r["delta_dark"] for r in m],float)
    pchip=PchipInterpolator(xx,y,extrapolate=False)
    linear=interp1d(xx,y,kind="linear",bounds_error=False,fill_value=np.nan)
    actual=float(worst["actual"])
    pchip_pred=float(pchip(xw)); linear_pred=float(linear(xw))
    pchip_aor=scalar_aor(pchip_pred,actual)
    linear_aor=scalar_aor(linear_pred,actual)

    stride_x=np.asarray(STRIDES,float)
    stride_e=np.asarray([stride_rows[str(s)]["global_max_abs_or_rel"] for s in STRIDES],float)
    if not np.all(np.isfinite(stride_e)) or np.any(stride_e<=0):
        fitted_order=float("-inf")
    else:
        slope,_=np.polyfit(np.log(stride_x),np.log(stride_e),1)
        fitted_order=float(slope)

    reproduction_error=abs(stride_rows["1"]["global_max_abs_or_rel"]-EXPECTED_PRIMARY)

    gates={
        "artifact_provenance_exact":provenance_pass,
        "parent_GE09_fail_exact":parent.get("classification")=="GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL",
        "dense_rows_exact_30755":len(dense)==30755,
        "selected_source_rows_exact_48":len(selected)==48,
        "frozen_primary_max_reproduced_within_1e15":reproduction_error<=REPRO_TOL,
        "same_global_worst_field_delta_dark":parent["source_grid_validation"]["abs_or_rel_max_by_field"].get("delta_dark")==parent["source_grid_validation"]["abs_or_rel_max"],
        "stride_errors_strictly_decrease_4_to_2_to_1":bool(stride_e[0]>stride_e[1]>stride_e[2]),
        "fitted_convergence_order_ge_2p5":bool(fitted_order>=P_MIN),
        "primary_error_smaller_than_PCHIP_at_worst":bool(worst["abs_or_rel"]<pchip_aor),
        "primary_error_smaller_than_linear_at_worst":bool(worst["abs_or_rel"]<linear_aor),
        "worst_source_row_strictly_inside_interval":bool(0.0<frac<1.0),
        "all_quantities_finite":bool(np.isfinite([
            *stride_e,fitted_order,frac,gap,local_swing_norm,pchip_aor,linear_aor
        ]).all()),
    }
    passed=bool(all(gates.values()))
    classification=(
        "GE10_GE09_SOURCE_INTERPOLATION_LIMIT_CONFIRMED"
        if passed else
        "GE10_GE09_SOURCE_INTERPOLATION_DIAGNOSTIC_FAIL"
    )

    result={
        "classification":classification,
        "scope":"Result-informed frozen-artifact localization of the historical GE09 source-grid failure; no new CLASS run, physics, interpolation replacement or threshold change.",
        "parent":{
            "classification":parent["classification"],
            "workflow_run":35494446296,
            "artifact_id":EXPECTED_ARTIFACT_ID,
            "artifact_digest":EXPECTED_DIGEST,
            "historical_gate_limit":1e-4,
        },
        "reproduction":{
            "dense_rows":len(dense),
            "selected_source_rows":len(selected),
            "requested_k_relative_miss_max":float(kmiss),
            "frozen_primary_delta_dark_max":float(stride_rows["1"]["global_max_abs_or_rel"]),
            "expected":EXPECTED_PRIMARY,
            "absolute_reproduction_error":float(reproduction_error),
        },
        "stride_convergence":{
            "endpoint_strides":list(STRIDES),
            "global_delta_dark_max_abs_or_rel":{
                str(s):float(stride_rows[str(s)]["global_max_abs_or_rel"]) for s in STRIDES
            },
            "fitted_loglog_order":fitted_order,
            "order_floor":P_MIN,
        },
        "historical_worst_row":{
            **worst,
            "left_endpoint":{
                "a":float(left["a"]),"z":float(1/left["a"]-1),"tau":float(left["tau"]),
                "delta_dark":float(left["delta_dark"]),
                "delta_dark_prime":float(left["delta_dark_prime"]),
            },
            "right_endpoint":{
                "a":float(right["a"]),"z":float(1/right["a"]-1),"tau":float(right["tau"]),
                "delta_dark":float(right["delta_dark"]),
                "delta_dark_prime":float(right["delta_dark_prime"]),
            },
            "ln_a_gap":gap,
            "fraction_in_interval":frac,
            "absolute_error_over_local_endpoint_scale":local_swing_norm,
            "PCHIP_prediction":pchip_pred,
            "PCHIP_abs_or_rel_error":pchip_aor,
            "linear_prediction":linear_pred,
            "linear_abs_or_rel_error":linear_aor,
        },
        "top10_primary_delta_dark_source_mismatches":top_primary,
        "gates":gates,
        "interpretation":{
            "representation":"The frozen cubic-Hermite representation is retained. Its source-grid error decreases strongly with accepted-endpoint density and is substantially smaller than state-only PCHIP or linear interpolation at the historical worst row.",
            "historical_GE09_status":"FAIL remains unchanged.",
            "next_step":"A future representation-refinement track may increase accepted-endpoint density under a separately preregistered precision/convergence design. GE10 itself licenses no threshold change or Z20 solve.",
        },
        "claim_boundary":"GE10 is diagnostic only and cannot relabel GE09, certify the GE06 local jet, close matter, or license Z20/Z21/finite eta.",
    }
    Path(args.json_out).write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
