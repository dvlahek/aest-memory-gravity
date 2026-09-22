#!/usr/bin/env python3
"""GE19 Repair27 — q20 reconstruction with the certified Repair26 parent.

The frozen Repair24 q20 science core is reused unchanged. The only permitted
scientific-parent change is the full-history first-order bath trace:
historical v0.77 -> frozen Repair26 R1 cancellation-free trace.

No fitted normalization is applied.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.repair24_q20_construction as r24

REPAIR26_RUN_ID=35721220889
REPAIR26_JOB_ID=106724330805
REPAIR26_ARTIFACT_ID=10690709843
REPAIR26_ARTIFACT_DIGEST="sha256:33faae31aae0ebe3cc52ac2083193ec8ba3dfe284fb07f06ef2568cad8e3938f"
REPAIR26_RESULT_JSON_SHA="80ba0b5927217be000991c82b4afb5f39b5e0ff369bc9b630a88ec11dabdedb6"
REPAIR26_R1_TRACE_SHA="608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
REPAIR26_R1_TRACE_BYTES=26643162
REPAIR26_TRACE_LO_A=0.39953919419256334
REPAIR26_TRACE_HI_A=0.4000388311146992
REPAIR26_X0_VS_GE15_AOR=3.9819456608594117e-11

EXPECTED_CORE_CONSTANTS={
    "TAUH0":10.0,
    "NQ_PRIMARY":2048,
    "NQ_CONTROL":1024,
    "NT_PRIMARY":128,
    "NT_CONTROL":64,
    "NX_PRIMARY":512,
    "NX_CONTROL":256,
    "M_MAX":40,
    "A_INITIAL":0.4,
    "A_TARGET_MAX":1e-15,
    "X_INITIAL_MAX":1e-10,
    "SPATIAL_MAX":1e-10,
    "QUAD_MAX":1e-2,
    "TIME_MAX":5e-3,
}


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def audit_core():
    bad={}
    for name,expected in EXPECTED_CORE_CONSTANTS.items():
        got=getattr(r24,name)
        if got!=expected:
            bad[name]={"expected":expected,"got":got}
    if bad:
        raise RuntimeError(f"Repair24 core constants changed: {bad}")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--repair26-trace",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    trace=Path(args.repair26_trace).resolve()
    outj=Path(args.json_out)
    outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)

    if not trace.exists():
        raise RuntimeError(f"missing frozen Repair26 R1 trace: {trace}")
    if trace.stat().st_size!=REPAIR26_R1_TRACE_BYTES:
        raise RuntimeError(
            f"Repair26 R1 trace byte mismatch: {trace.stat().st_size} != {REPAIR26_R1_TRACE_BYTES}"
        )
    tsha=sha256(trace)
    if tsha!=REPAIR26_R1_TRACE_SHA:
        raise RuntimeError(f"Repair26 R1 trace hash mismatch: {tsha}")

    audit_core()

    # Only allowed core modification: bind the full-history initial-surface
    # bracket to the already frozen Repair26 R1 trace. All equations, grids,
    # controls and science thresholds remain the Repair24 values audited above.
    r24.TRACE_LO_A=REPAIR26_TRACE_LO_A
    r24.TRACE_HI_A=REPAIR26_TRACE_HI_A

    old_argv=sys.argv[:]
    core_stdout=io.StringIO()
    core_rc=0
    try:
        sys.argv=[
            "repair24_q20_construction.py",
            "--results-dir",str(Path(args.results_dir).resolve()),
            "--v077-trace",str(trace),
            "--json-out",str(outj),
            "--npz-out",str(outn),
        ]
        try:
            with contextlib.redirect_stdout(core_stdout):
                r24.main()
        except SystemExit as exc:
            core_rc=int(exc.code or 0)
    finally:
        sys.argv=old_argv

    if not outj.exists():
        raise RuntimeError(
            "frozen Repair24 core produced no JSON; captured stdout="+core_stdout.getvalue()[-2000:]
        )

    d=json.loads(outj.read_text())
    if d.get("classification") not in (
        "GE19_REPAIR24_Q20_CONSTRUCTION_PASS",
        "GE19_REPAIR24_Q20_CONSTRUCTION_FAIL",
    ):
        raise RuntimeError(f"unexpected inherited core classification: {d.get('classification')}")

    # Core science validity is defined by its unchanged frozen gates.
    core_pass=bool(all(bool(v) for v in d.get("gates",{}).values()))
    if core_pass!=(d.get("classification")=="GE19_REPAIR24_Q20_CONSTRUCTION_PASS"):
        raise RuntimeError("inherited Repair24 classification/gate inconsistency")
    if core_pass and core_rc!=0:
        raise RuntimeError(f"inherited Repair24 PASS returned nonzero rc={core_rc}")
    if (not core_pass) and core_rc not in (0,2):
        raise RuntimeError(f"inherited Repair24 FAIL returned unexpected rc={core_rc}")

    # The hard-coded legacy artifact labels in Repair24 are report metadata only.
    # Remove them and replace them with the actually verified Repair26 parent.
    parent_hashes={
        k:v for k,v in d.get("provenance",{}).items()
        if not k.startswith("v077_artifact_")
    }
    parent_hashes.update({
        "Repair26_workflow_run_id":REPAIR26_RUN_ID,
        "Repair26_workflow_job_id":REPAIR26_JOB_ID,
        "Repair26_artifact_id":REPAIR26_ARTIFACT_ID,
        "Repair26_artifact_digest":REPAIR26_ARTIFACT_DIGEST,
        "Repair26_result_JSON_sha256":REPAIR26_RESULT_JSON_SHA,
        "Repair26_R1_full_history_trace_sha256":REPAIR26_R1_TRACE_SHA,
        "Repair26_R1_full_history_trace_bytes":REPAIR26_R1_TRACE_BYTES,
    })

    d["classification"]=(
        "GE19_REPAIR27_CANCELLATION_FREE_PARENT_Q20_RECONSTRUCTION_PASS"
        if core_pass else
        "GE19_REPAIR27_CANCELLATION_FREE_PARENT_Q20_RECONSTRUCTION_FAIL"
    )
    d["predata_classification"]="GE19_REPAIR27_PREDATA_CANCELLATION_FREE_PARENT_Q20_RECONSTRUCTION"
    d["routing"]={
        "next_route":(
            "CANCELLATION_FREE_PARENT_Q20_CERTIFIED"
            if core_pass else
            "Q20_CONSTRUCTION_OR_CONVERGENCE_FAIL_AFTER_BOUNDARY_REPAIR"
        )
    }
    d["provenance"]=parent_hashes
    d["parent_change"]={
        "historical_v077_trace_used":False,
        "Repair26_R1_cancellation_free_trace_used":True,
        "Repair25_fitted_normalization_used":False,
        "Repair26_R1_trace_X0_vs_GE15_dense_abs_or_rel_max":REPAIR26_X0_VS_GE15_AOR,
        "only_scientific_parent_change":"full-history first-order bath trace",
    }
    d["inherited_repair24_core"]={
        "core_file":"ge19/repair24_q20_construction.py",
        "core_blob":"fc271987d1bddcd023cc9c057ddcad036b1d72fb",
        "core_stdout_suppressed":True,
        "core_return_code":core_rc,
        "all_science_constants_and_thresholds_unchanged":True,
        "historical_Repair24_relabelled":False,
    }
    d["full_history_boundary"]["source"]="frozen Repair26 R1 cancellation-free full-history trace"
    d["full_history_boundary"]["trace_lo_a"]=REPAIR26_TRACE_LO_A
    d["full_history_boundary"]["trace_hi_a"]=REPAIR26_TRACE_HI_A
    d["q20_constructed"]=core_pass
    d["q20_certified_projection"]=core_pass
    d["H4_Z21_construction_licensed_after_result_freeze"]=core_pass
    d["Z21_licensed_after_freeze"]=core_pass
    d["q20_rerun_performed"]=True
    d["claim_boundary"]=(
        "PASS certifies the same window-local particular baseline second-order normalized-bath "
        "projection as Repair24, but with the certified Repair26 cancellation-free full-history "
        "first-order parent. It does not choose a primordial/homogeneous q20 mode, solve H4/Z21, "
        "introduce finite eta, or make observational claims."
    )

    outj.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n")
    print(json.dumps(d,indent=2,allow_nan=False))
    if not core_pass:
        raise SystemExit(2)


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR27_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "q20_rerun_performed":False,
            "q20_certified_projection":False,
            "H4_Z21_construction_licensed_after_result_freeze":False,
        },indent=2))
        raise
