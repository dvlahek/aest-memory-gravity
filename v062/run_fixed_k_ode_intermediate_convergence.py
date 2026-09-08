#!/usr/bin/env python3
"""Intermediate fixed-k ODE convergence diagnostic for v0.62.

This is a scientific diagnostic of numerical convergence, but it is deliberately
separate from and does NOT replace, modify, or feed the preregistered final
v0.62 smooth-limit certification.  It uses the same patched CLASS worker and
unchanged AeST physical model, while comparing three numerical tolerances on a
compact local k grid with identical early-start settings.

Compared tolerances:
  3e-8, 1e-8, 3e-9

The diagnostic reports sign persistence, direct-vs-CLASS reconstruction, and
pointwise successive-tolerance changes in Delta_m^GI. No preregistered science
gate or final classification is changed by this script.
"""

from pathlib import Path
import json
import math
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

VARIANTS = [
    ("tol3e8", 3e-8),
    ("tol1e8", 1e-8),
    ("tol3e9", 3e-9),
]


def run_variant(name, tol):
    variant = f"intermediate_conv_{name}"
    out = RESULTS / f"v062_odeconv_{variant}_batch_0.json"
    trace = RESULTS / f"v062_odeconv_{variant}_batch_0_trace.dat"

    for p in (out, trace):
        if p.exists():
            p.unlink()

    overrides = dict(COMMON_STARTS)
    overrides["tol_perturbations_integration"] = tol

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
        "stage": "run_variant",
        "variant": variant,
        "tol_perturbations_integration": tol,
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

    data = json.loads(out.read_text())
    return {
        "name": name,
        "tol": tol,
        "wall_seconds": wall,
        "worker_output_json": str(out),
        "trace_file": str(trace),
        "rows": data["rows"],
    }


def rel_change(a, b):
    scale = max(abs(a), abs(b), 1e-300)
    return abs(b - a) / scale


def main():
    summary_path = RESULTS / "v062_intermediate_ode_convergence.json"
    rows_path = RESULTS / "v062_intermediate_ode_convergence_rows.csv"
    for p in (summary_path, rows_path):
        if p.exists():
            p.unlink()

    print(json.dumps({
        "classification_use": "NONE_SEPARATE_INTERMEDIATE_CONVERGENCE_DIAGNOSTIC",
        "purpose": "successive-tolerance convergence check only",
        "tolerances": [v[1] for v in VARIANTS],
        "kh_values": KH_VALUES,
        "common_early_starts": COMMON_STARTS,
        "physical_model_changed": False,
        "final_certification_changed": False,
    }, indent=2), flush=True)

    runs = [run_variant(name, tol) for name, tol in VARIANTS]
    by_name = {r["name"]: r for r in runs}

    row_maps = {}
    for r in runs:
        row_maps[r["name"]] = {float(x["kh_requested"]): x for x in r["rows"]}

    comparison_rows = []
    for kh in KH_VALUES:
        r3e8 = row_maps["tol3e8"][kh]
        r1e8 = row_maps["tol1e8"][kh]
        r3e9 = row_maps["tol3e9"][kh]
        d3e8 = float(r3e8["delta_m_gi_final"])
        d1e8 = float(r1e8["delta_m_gi_final"])
        d3e9 = float(r3e9["delta_m_gi_final"])
        comparison_rows.append({
            "kh": kh,
            "delta_gi_3e8": d3e8,
            "delta_gi_1e8": d1e8,
            "delta_gi_3e9": d3e9,
            "rel_change_3e8_to_1e8": rel_change(d3e8, d1e8),
            "rel_change_1e8_to_3e9": rel_change(d1e8, d3e9),
            "same_sign_all_three": (d3e8 < 0 and d1e8 < 0 and d3e9 < 0) or (d3e8 > 0 and d1e8 > 0 and d3e9 > 0),
            "direct_class_err_3e8": abs(float(r3e8["P_direct_over_class"]) - 1.0),
            "direct_class_err_1e8": abs(float(r1e8["P_direct_over_class"]) - 1.0),
            "direct_class_err_3e9": abs(float(r3e9["P_direct_over_class"]) - 1.0),
        })

    n_same_sign = sum(int(r["same_sign_all_three"]) for r in comparison_rows)
    max_rel_early = max(r["rel_change_3e8_to_1e8"] for r in comparison_rows)
    max_rel_late = max(r["rel_change_1e8_to_3e9"] for r in comparison_rows)
    median_rel_early = sorted(r["rel_change_3e8_to_1e8"] for r in comparison_rows)[len(comparison_rows)//2]
    median_rel_late = sorted(r["rel_change_1e8_to_3e9"] for r in comparison_rows)[len(comparison_rows)//2]
    max_direct_class_err = max(
        max(r["direct_class_err_3e8"], r["direct_class_err_1e8"], r["direct_class_err_3e9"])
        for r in comparison_rows
    )

    # Diagnostic-only convergence trend: does the later successive change shrink?
    trend_improves_max = max_rel_late < max_rel_early
    trend_improves_median = median_rel_late < median_rel_early

    summary = {
        "classification_use": "NONE_SEPARATE_INTERMEDIATE_CONVERGENCE_DIAGNOSTIC",
        "purpose": "successive-tolerance convergence check only; does not feed preregistered v0.62 classification",
        "tolerances": [3e-8, 1e-8, 3e-9],
        "kh_values": KH_VALUES,
        "common_early_starts": COMMON_STARTS,
        "n_points": len(KH_VALUES),
        "n_same_sign_all_three": n_same_sign,
        "max_rel_change_3e8_to_1e8": max_rel_early,
        "max_rel_change_1e8_to_3e9": max_rel_late,
        "median_rel_change_3e8_to_1e8": median_rel_early,
        "median_rel_change_1e8_to_3e9": median_rel_late,
        "later_change_smaller_by_max": trend_improves_max,
        "later_change_smaller_by_median": trend_improves_median,
        "max_abs_direct_over_class_minus_1": max_direct_class_err,
        "wall_seconds_by_variant": {r["name"]: r["wall_seconds"] for r in runs},
        "physical_model_changed": False,
        "final_certification_changed": False,
        "comparison_rows": comparison_rows,
    }

    summary_path.write_text(json.dumps(summary, indent=2) + "\n")

    columns = [
        "kh", "delta_gi_3e8", "delta_gi_1e8", "delta_gi_3e9",
        "rel_change_3e8_to_1e8", "rel_change_1e8_to_3e9",
        "same_sign_all_three", "direct_class_err_3e8", "direct_class_err_1e8", "direct_class_err_3e9",
    ]
    with rows_path.open("w") as f:
        f.write(",".join(columns) + "\n")
        for r in comparison_rows:
            f.write(",".join(str(r[c]) for c in columns) + "\n")

    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
