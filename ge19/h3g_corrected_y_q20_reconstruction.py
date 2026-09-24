#!/usr/bin/env python3
"""H3G: corrected-Y q20 on certified H3F Z20 and frozen Repair26 R1 history.

Only the second-order Z20 parent differs scientifically from the
historical Repair27 q20. All old Repair24 non-main physics helpers,
R1 first-order bath boundary, science grids, equations and thresholds
are unchanged. A result here is NOT an H4 Noether or Z21 certificate.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import ge19.h3g_corrected_y_q20_core as core

PRE_BLOB="09fc1bd7fc06459d90fc6f6ba37a84adba757d37"
R24_BLOB="fc271987d1bddcd023cc9c057ddcad036b1d72fb"
H3F_JSON_SHA="0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b"
H3F_NPZ_SHA="90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542"
R26_R1_SHA="608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
R26_R1_BYTES=26643162
R26_JSON_SHA="80ba0b5927217be000991c82b4afb5f39b5e0ff369bc9b630a88ec11dabdedb6"
R26_LO_A=0.39953919419256334
R26_HI_A=0.4000388311146992
R26_X0_AOR=3.9819456608594117e-11
OLD_R27_JSON_SHA="99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b"
OLD_R27_NPZ_SHA="2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0"
CONSTANTS={
    "TAUH0":10.0,"NQ_PRIMARY":2048,"NQ_CONTROL":1024,
    "NT_PRIMARY":128,"NT_CONTROL":64,
    "NX_PRIMARY":512,"NX_CONTROL":256,
    "M_MAX":40,"A_INITIAL":0.4,"A_TARGET_MAX":1e-15,
    "X_INITIAL_MAX":1e-10,"SPATIAL_MAX":1e-10,
    "QUAD_MAX":1e-2,"TIME_MAX":5e-3,
}


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def frozen_helper_ast(path:Path):
    tree=ast.parse(path.read_text())
    return {
        n.name:ast.dump(n,include_attributes=False)
        for n in tree.body
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))
        and n.name!="main"
    }


def audit_unchanged_physics():
    frozen=ROOT/"ge19/repair24_q20_construction.py"
    new=ROOT/"ge19/h3g_corrected_y_q20_core.py"
    if frozen_helper_ast(frozen)!=frozen_helper_ast(new):
        raise RuntimeError(
            "H3G helper-function AST mismatch: frozen Repair24 physics changed"
        )
    for rel,expected in (
        ("ge19/h3g_predata_corrected_y_q20_reconstruction.json",PRE_BLOB),
        ("ge19/repair24_q20_construction.py",R24_BLOB),
        ("ge19/h3g_corrected_y_q20_core.py","688920e840a0a13bc85a6f416c2573cf0472eaa3"),
    ):
        observed=subprocess.check_output(
            ["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True
        ).strip()
        if observed!=expected:
            raise RuntimeError(f"frozen tracked blob mismatch {rel}: {observed}")
    bad={
        name:{"expected":expected,"observed":getattr(core,name,None)}
        for name,expected in CONSTANTS.items()
        if getattr(core,name,None)!=expected
    }
    if bad:
        raise RuntimeError(f"frozen q20 science constant mismatch {bad}")


def verify_h3f_parent(rd:Path):
    jf=rd/"ge19_h3f_corrected_y_z20_science_reclosure.json"
    nf=rd/"ge19_h3f_corrected_y_z20_science_reclosure.npz"
    if not jf.is_file() or not nf.is_file():
        raise RuntimeError("missing separately certified H3F Z20 parent JSON/NPZ")
    jh,nh=sha256(jf),sha256(nf)
    if jh!=H3F_JSON_SHA or nh!=H3F_NPZ_SHA:
        raise RuntimeError(f"H3F parent hash mismatch: {jh}, {nh}")
    d=json.loads(jf.read_text())
    if (d.get("classification")!="GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED"
        or d.get("Z20_certified") is not True
        or not d.get("gates")
        or not all(v is True for v in d["gates"].values())
        or d.get("provenance",{}).get("StageE_full_Y_aether_and_scalar_source_used") is not True
        or d.get("provenance",{}).get("historical_scalar_only_Y_replaced_not_added") is not True):
        raise RuntimeError("H3F parent science status/source identity mismatch")
    return d


def optional_old_q20_comparator(rd:Path,new_path:Path):
    oldj=rd/"ge19_repair27_cancellation_free_parent_q20_reconstruction.json"
    oldn=rd/"ge19_repair27_cancellation_free_parent_q20_reconstruction.npz"
    report={"available":False,"report_only":True,"no_required_difference":True}
    if not oldj.is_file() or not oldn.is_file():
        return report
    sj,sn=sha256(oldj),sha256(oldn)
    report.update({"old_json_sha256":sj,"old_npz_sha256":sn})
    if sj!=OLD_R27_JSON_SHA or sn!=OLD_R27_NPZ_SHA or not new_path.is_file():
        report["reason"]="old comparator hash mismatch or new q20 NPZ missing"
        return report
    old=np.load(oldn,allow_pickle=False)
    new=np.load(new_path,allow_pickle=False)
    diffs={}
    for tag in ("C_min","C_star","C_max"):
        name=f"{tag}_weighted_z20_primary"
        a=np.asarray(old[name],complex)
        b=np.asarray(new[name],complex)
        diffs[tag]=float(
            np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-300)
        )
    report.update({
        "available":True,"old_result_verified":True,
        "weighted_z20_relative_L2_per_C":diffs,
        "relative_L2_max":max(diffs.values())
    })
    return report


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--repair26-trace",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir).resolve()
    trace=Path(args.repair26_trace).resolve()
    outj=Path(args.json_out).resolve()
    outn=Path(args.npz_out).resolve()
    outj.parent.mkdir(parents=True,exist_ok=True)

    if not trace.is_file():
        raise RuntimeError("missing frozen Repair26 R1 full-history trace")
    if trace.stat().st_size!=R26_R1_BYTES or sha256(trace)!=R26_R1_SHA:
        raise RuntimeError("Repair26 R1 trace bytes/SHA mismatch")

    audit_unchanged_physics()
    verify_h3f_parent(rd)

    # Exact frozen Repair27 single full-history first-order R1 parent.
    core.TRACE_LO_A=R26_LO_A
    core.TRACE_HI_A=R26_HI_A
    captured=io.StringIO()
    old_argv=list(sys.argv)
    core_rc=0
    try:
        sys.argv=[
            "h3g_corrected_y_q20_core.py",
            "--results-dir",str(rd),
            "--v077-trace",str(trace),  # historical CLI spelling; actual file is pinned R1
            "--json-out",str(outj),
            "--npz-out",str(outn),
        ]
        try:
            with contextlib.redirect_stdout(captured):
                core.main()
        except SystemExit as exc:
            core_rc=int(exc.code or 0)
    finally:
        sys.argv=old_argv

    if not outj.is_file() or not outn.is_file():
        raise RuntimeError("H3G science core missing outputs: "+captured.getvalue()[-2000:])
    d=json.loads(outj.read_text())
    core_pass=(d.get("classification")=="GE19_H3G_CORRECTED_Y_Q20_CORE_PASS")
    if d.get("classification") not in (
        "GE19_H3G_CORRECTED_Y_Q20_CORE_PASS",
        "GE19_H3G_CORRECTED_Y_Q20_CORE_FAIL",
    ):
        raise RuntimeError("unexpected H3G core classification")
    if not d.get("gates") or core_pass!=all(v is True for v in d["gates"].values()):
        raise RuntimeError("H3G q20 core science gate/classification mismatch")
    if (core_pass and core_rc!=0) or (not core_pass and core_rc not in (0,2)):
        raise RuntimeError(f"H3G q20 core exit/classification mismatch: {core_rc}")

    provenance={k:v for k,v in d.get("provenance",{}).items()
                if not k.startswith("v077_artifact_")}
    provenance.update({
        "Repair26_workflow_run_id":35721220889,
        "Repair26_workflow_job_id":106724330805,
        "Repair26_artifact_id":10690709843,
        "Repair26_artifact_digest":"sha256:33faae31aae0ebe3cc52ac2083193ec8ba3dfe284fb07f06ef2568cad8e3938f",
        "Repair26_result_JSON_sha256":R26_JSON_SHA,
        "Repair26_R1_full_history_trace_sha256":R26_R1_SHA,
        "Repair26_R1_full_history_trace_bytes":R26_R1_BYTES,
        "H3F_corrected_Y_Z20_JSON_sha256":H3F_JSON_SHA,
        "H3F_corrected_Y_Z20_NPZ_sha256":H3F_NPZ_SHA,
    })
    d["provenance"]=provenance
    d["classification"]=(
        "GE19_H3G_CORRECTED_Y_Q20_RECONSTRUCTION_PASS"
        if core_pass else "GE19_H3G_CORRECTED_Y_Q20_RECONSTRUCTION_SCIENCE_FAIL"
    )
    d["predata_classification"]="GE19_H3G_PREDATA_CORRECTED_Y_Q20_RECONSTRUCTION"
    d["routing"]={"next_route":(
        "CORRECTED_Y_H3F_PARENT_Q20_CERTIFIED"
        if core_pass else "H3G_CORRECTED_Y_Q20_SCIENCE_FAIL"
    )}
    d["parent_change"]={
        "historical_Repair22_Z20_used":False,
        "H3F_certified_action_completed_Y_Z20_used":True,
        "Repair26_R1_cancellation_free_first_order_trace_used":True,
        "historical_v077_first_order_trace_used":False,
        "Repair25_fitted_normalization_used":False,
        "old_Repair27_q20_not_reused":True,
        "only_scientific_parent_change_relative_to_Repair27":"second-order metric Z20 parent",
    }
    d["inherited_repair24_core"]={
        "core_file":"ge19/h3g_corrected_y_q20_core.py",
        "original_physics_core_file":"ge19/repair24_q20_construction.py",
        "original_physics_core_blob":R24_BLOB,
        "all_non_main_physics_helper_ASTs_identical":True,
        "core_return_code":core_rc,
        "core_stdout_suppressed":True,
        "all_science_constants_and_thresholds_unchanged":True,
    }
    d["old_Repair27_comparator"]=optional_old_q20_comparator(rd,outn)
    d["full_history_boundary"]["source"]="frozen Repair26 R1 cancellation-free full-history trace"
    d["full_history_boundary"]["trace_lo_a"]=R26_LO_A
    d["full_history_boundary"]["trace_hi_a"]=R26_HI_A
    d["q20_constructed"]=core_pass
    d["q20_certified_projection"]=core_pass
    d["full_all_sector_H4_Noether_derived"]=False
    d["H4_Z21_construction_licensed_after_result_freeze"]=False
    d["Z21_licensed_after_freeze"]=False
    d["claim_boundary"]=(
        "PASS certifies only the new window-local particular weighted normalized "
        "q20 projection on the certified H3F corrected-Y Z20 parent, retaining "
        "the unchanged Repair26 R1 first-order bath and Repair24 normalized equations. "
        "Full all-sector H4 Noether and Z21 remain open. No homogeneous bath, "
        "finite eta, lensing or observational claim."
    )
    outj.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n")
    print(json.dumps(d,indent=2,allow_nan=False))
    if not core_pass:
        raise SystemExit(2)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_H3G_CORRECTED_Y_Q20_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "q20_certified_projection":False,
            "H4_Z21_construction_licensed_after_result_freeze":False,
        },indent=2))
        raise
