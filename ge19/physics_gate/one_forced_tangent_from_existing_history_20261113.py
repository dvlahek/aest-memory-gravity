#!/usr/bin/env python3
"""GE19 science-first STOP/GO screen: ONE native CLASS eta tangent using
the already completed 141494-sample primordial Bchi0 trace and exact-zero null.

Never reruns baseline or null. No source patch, parameter/eta scan, CLASS build,
cosmology fitting or observational detection claim. Output is only provisional.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
from pathlib import Path

import run_full_class_two_pass_tangent_20261112 as base


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-root", type=Path, required=True)
    parser.add_argument("--original-ini", type=Path, required=True)
    parser.add_argument("--existing-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.class_root.expanduser().resolve()
    original_ini = args.original_ini.expanduser().resolve()
    existing = args.existing_dir.expanduser().resolve()
    out = args.out_dir.expanduser().resolve()

    if not original_ini.is_file():
        raise RuntimeError("GE19_FROZEN_INI_MISSING")
    git_sha = subprocess.check_output(
        ["git", "hash-object", str(original_ini)], text=True
    ).strip()
    if git_sha != "f9a2bde8921a148e063f9657a8ede0a51c6a629d":
        raise RuntimeError("GE19_FROZEN_EXP_INI_CHANGED")

    manifest = base.patched_source_qualification(root)
    if out == existing or existing in out.parents or out in existing.parents:
        raise RuntimeError("GE19_RESULT_DIRECTORY_NOT_SEPARATE")
    if out.exists():
        raise RuntimeError("GE19_OUTPUT_DIRECTORY_ALREADY_EXISTS")
    baseline_path = existing / "baseline_dt010.csv"
    null_path = existing / "null_W1.csv"
    if not (existing / "base010.log").is_file() or not (existing / "null.log").is_file():
        raise RuntimeError("GE19_COMPLETED_NATIVE_CLASS_LOGS_MISSING")
    history = base.read_trace(baseline_path, dense_source=True)
    null = base.read_trace(null_path)
    if len(history) < 100000 or history[0][1] >= 1e-5 or history[-1][1] < 0.99:
        raise RuntimeError("GE19_PRIMORDIAL_HISTORY_NOT_FULLY_COVERED")
    if len(null) < 1:
        raise RuntimeError("GE19_NULL_W_NOT_SAMPLED")
    w0 = base.interpolate_a(history)
    null_max = max(abs(r[2]) for r in null)
    if not math.isfinite(w0) or abs(w0) <= 1e-100:
        raise RuntimeError("GE19_BASELINE_WEYL_MISSING_OR_ZERO")
    if null_max > 1e-12 * abs(w0):
        raise RuntimeError("GE19_NULL_WEYL_NOT_ZERO")
    max_B = max(abs(r[3]) for r in history)
    if max_B == 0.0 or not math.isfinite(max_B):
        raise RuntimeError("GE19_BASELINE_MEMORY_FORCE_ZERO_OR_NONFINITE")

    # The source is directly the successfully completed original Bchi history.
    # Only ONE CLASS process is launched. No derivative from finite differences.
    out.mkdir(parents=True)
    (out / "native").mkdir()
    config = base.make_ini(original_ini, out, "force_single", 2e-7)
    csv_output = out / "forced_single_W1.csv"
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["GE19_TANGENT_MODE"] = "force"
    env["GE19_TANGENT_K_MPC"] = format(base.K_MPC, ".12g")
    env["GE19_TANGENT_TRACE"] = str(baseline_path)
    env["GE19_TANGENT_OUT"] = str(csv_output)
    env.pop("GE19_TANGENT_ZERO_SOURCE", None)
    log = out / "force_single.log"

    print("GE19_EXISTING_HISTORY_ACCEPTED",
          "records", len(history), "null_records", len(null),
          "max_abs_Bchi", format(max_B, ".17g"),
          "null_max_abs_W", format(null_max, ".17g"), flush=True)
    print("GE19_SINGLE_NATIVE_CLASS_FORCE_START", flush=True)
    base.run_class(root, config, log, env)
    print("GE19_SINGLE_NATIVE_CLASS_FORCE_FINISHED", flush=True)
    response = base.read_trace(csv_output)
    w1 = base.interpolate_a(response)
    if not math.isfinite(w1):
        raise RuntimeError("GE19_WEYL_TANGENT_NOT_FINITE")
    ratio = w1 / w0
    report = {
        "classification": "GE19_ONE_FORCED_NATIVE_CLASS_TANGENT_PROVISIONAL_ONLY",
        "fixed_k_Mpc_inverse": base.K_MPC,
        "target_z": 0.5,
        "eta": 0.0,
        "baseline_source_rows": len(history),
        "null_output_rows": len(null),
        "forced_output_rows": len(response),
        "baseline_initial_a": history[0][1],
        "baseline_final_a": history[-1][1],
        "baseline_W0_at_z0p5": w0,
        "baseline_max_abs_Bchi": max_B,
        "null_max_abs_W": null_max,
        "forced_W1_at_z0p5": w1,
        "W1_over_W0_per_unit_eta": ratio,
        "original_history_sha256": digest(baseline_path),
        "original_null_sha256": digest(null_path),
        "class_source_patch_parent_sha256": manifest["parent_source_sha256"],
        "class_source_patch_current_sha256": manifest["modified_source_sha256"],
        "single_native_force_execution_complete": True,
        "independent_numerical_convergence_certified": False,
        "full_Einstein_Ward_constraints_certified": False,
        "primordial_NLO_initial_state_certified": False,
        "full_covariant_action_consistency_certified": False,
        "physical_Weyl_gain_certified": False,
        "DES_detection": False
    }
    report_path = out / "GE19_ONE_FORCED_TANGENT_SCREEN.json"
    report_path.write_text(json.dumps(report, sort_keys=True, indent=2,
                                      allow_nan=False) + "\n")
    print("GE19_PROVISIONAL_FULL_CLASS_WEYL_TANGENT", format(w1, ".17g"),
          "W1_OVER_W0", format(ratio, ".17g"), flush=True)
    print("GE19_REPORT", report_path, flush=True)
    print("GE19_PHYSICS_GO False", flush=True)


if __name__ == "__main__":
    main()
