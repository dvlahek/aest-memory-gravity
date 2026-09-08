#!/usr/bin/env python3
"""Tolerance-only early-start control for the v0.62 fixed-k ODE diagnostic.

This script is separate from the preregistered v0.62 certification and does not
feed or modify its final classification. It adds one missing diagnostic point:
1e-7 perturbation-integration tolerance using exactly the same early-start
settings and the same ten local k values as the 3e-8, 1e-8, and 3e-9
intermediate convergence diagnostic.

The purpose is to remove the start-time confound present in the earlier
``strong`` runtime probe and provide a clean tolerance-only sequence

    1e-7 -> 3e-8 -> 1e-8 -> 3e-9.

If the three intermediate worker JSON files already exist, the script also
writes a four-tolerance comparison summary. Otherwise it still writes the 1e-7
control result and reports which comparison inputs are missing.
"""

from pathlib import Path
import json
import os
import subprocess
import sys
import time

import run_fixed_k_ode_convergence as core

RESULTS = core.RESULTS

KH_VALUES = [
    0.091950, 0.091975, 0.092000, 0.092025, 0.092050,
    0.126450, 0.126475, 0.126500, 0.126525, 0.126550,
]

COMMON_STARTS = {
    "start_small_k_at_tau_c_over_tau_h": 5e-4,
    "start_large_k_at_tau_h_over_tau_k": 0.03,
}

CONTROL_TOL = 1e-7


def rel_change(a, b):
    return abs(b - a) / max(abs(a), abs(b), 1e-300)


def load_rows(path):
    data = json.loads(path.read_text())
    return {float(r["kh_requested"]): r for r in data["rows"]}


def main():
    variant = "intermediate_conv_tol1e7_early"
    out = RESULTS / f"v062_odeconv_{variant}_batch_0.json"
    trace = RESULTS / f"v062_odeconv_{variant}_batch_0_trace.dat"
    summary_path = RESULTS / "v062_tolerance_only_control.json"
    rows_path = RESULTS / "v062_tolerance_only_control_rows.csv"

    for p in (out, trace, summary_path, rows_path):
        if p.exists():
            p.unlink()

    overrides = dict(COMMON_STARTS)
    overrides["tol_perturbations_integration"] = CONTROL_TOL

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["AEST_OFFLINE_TRACE_FILE"] = str(trace)

    cmd = [
        sys.executable,
        str(Path(core.__file__).resolve()),
        "--worker",
        variant,
        json.dumps(overrides),
        "0",
        json.dumps(KH_VALUES),
    ]

    print(json.dumps({
        "classification_use": "NONE_SEPARATE_TOLERANCE_ONLY_DIAGNOSTIC",
        "stage": "run_1e-7_same_early_starts",
        "tol_perturbations_integration": CONTROL_TOL,
        "kh_values": KH_VALUES,
        "common_early_starts": COMMON_STARTS,
        "physical_model_changed": False,
        "final_certification_changed": False,
    }, indent=2), flush=True)

    t0 = time.perf_counter()
    cp = subprocess.run(cmd, env=env, check=False)
    wall = time.perf_counter() - t0
    if cp.returncode != 0:
        raise RuntimeError(f"{variant} failed with return code {cp.returncode}")

    control_rows = load_rows(out)

    known = {
        "tol1e7": out,
        "tol3e8": RESULTS / "v062_odeconv_intermediate_conv_tol3e8_batch_0.json",
        "tol1e8": RESULTS / "v062_odeconv_intermediate_conv_tol1e8_batch_0.json",
        "tol3e9": RESULTS / "v062_odeconv_intermediate_conv_tol3e9_batch_0.json",
    }
    missing = [name for name, path in known.items() if not path.exists()]

    summary = {
        "classification_use": "NONE_SEPARATE_TOLERANCE_ONLY_DIAGNOSTIC",
        "purpose": "1e-7 same-early-start control; does not feed preregistered v0.62 classification",
        "control_tolerance": CONTROL_TOL,
        "kh_values": KH_VALUES,
        "common_early_starts": COMMON_STARTS,
        "control_wall_seconds": wall,
        "n_control_points": len(control_rows),
        "n_control_negative": sum(float(r["delta_m_gi_final"]) < 0 for r in control_rows.values()),
        "max_abs_direct_over_class_minus_1_control": max(abs(float(r["P_direct_over_class"]) - 1.0) for r in control_rows.values()),
        "comparison_available": not missing,
        "missing_comparison_inputs": missing,
        "physical_model_changed": False,
        "final_certification_changed": False,
    }

    comparison_rows = []
    if not missing:
        maps = {name: load_rows(path) for name, path in known.items()}
        for kh in KH_VALUES:
            vals = {
                name: float(maps[name][kh]["delta_m_gi_final"])
                for name in ("tol1e7", "tol3e8", "tol1e8", "tol3e9")
            }
            row = {
                "kh": kh,
                "delta_gi_1e7": vals["tol1e7"],
                "delta_gi_3e8": vals["tol3e8"],
                "delta_gi_1e8": vals["tol1e8"],
                "delta_gi_3e9": vals["tol3e9"],
                "rel_change_1e7_to_3e8": rel_change(vals["tol1e7"], vals["tol3e8"]),
                "rel_change_3e8_to_1e8": rel_change(vals["tol3e8"], vals["tol1e8"]),
                "rel_change_1e8_to_3e9": rel_change(vals["tol1e8"], vals["tol3e9"]),
                "same_sign_all_four": all(v < 0 for v in vals.values()) or all(v > 0 for v in vals.values()),
            }
            comparison_rows.append(row)

        def med(xs):
            ys = sorted(xs)
            n = len(ys)
            return (ys[n // 2] if n % 2 else 0.5 * (ys[n // 2 - 1] + ys[n // 2]))

        changes = {
            "1e7_to_3e8": [r["rel_change_1e7_to_3e8"] for r in comparison_rows],
            "3e8_to_1e8": [r["rel_change_3e8_to_1e8"] for r in comparison_rows],
            "1e8_to_3e9": [r["rel_change_1e8_to_3e9"] for r in comparison_rows],
        }
        summary.update({
            "n_same_sign_all_four": sum(r["same_sign_all_four"] for r in comparison_rows),
            "max_rel_change_1e7_to_3e8": max(changes["1e7_to_3e8"]),
            "max_rel_change_3e8_to_1e8": max(changes["3e8_to_1e8"]),
            "max_rel_change_1e8_to_3e9": max(changes["1e8_to_3e9"]),
            "median_rel_change_1e7_to_3e8": med(changes["1e7_to_3e8"]),
            "median_rel_change_3e8_to_1e8": med(changes["3e8_to_1e8"]),
            "median_rel_change_1e8_to_3e9": med(changes["1e8_to_3e9"]),
        })

        columns = list(comparison_rows[0].keys())
        with rows_path.open("w") as f:
            f.write(",".join(columns) + "\n")
            for r in comparison_rows:
                f.write(",".join(str(r[c]) for c in columns) + "\n")
        summary["comparison_rows"] = comparison_rows

    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
