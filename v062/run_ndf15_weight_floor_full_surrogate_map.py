#!/usr/bin/env python3
"""Fast non-classifying full-grid surrogate map for v0.62 smooth-limit study.

This diagnostic evaluates the complete locked 26-point target k grid for all
four frozen smooth-limit variants, but uses the previously tested diagnostic
NDF15 state-weight floor 1e-13 to avoid the 1e-15 runtime cliff.  The physical
model, requested target k values, perturbation tolerances, nominal stepsizes,
and early-start settings are copied from the frozen v0.62 certification.

IMPORTANT
---------
This is NOT part of the preregistered v0.62 scientific classification and MUST
NOT be used to declare V062_SMOOTH_LIMIT_CERTIFIED.  The 1e-13 floor is only a
fast topology scout.  The auxiliary CLASS internal k grid is minimized per
requested target point, so this script is diagnostic-only even beyond the
weight-floor change.

The script runs one target point per subprocess, checkpointing every completed
worker JSON.  Existing valid point JSONs are reused automatically.  Set
V062_SURROGATE_MAX_WORKERS to limit concurrency; default is min(16,cpu_count).
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import math
import os
import subprocess
import sys
import time

import run_fixed_k_ode_convergence as core

RESULTS = core.RESULTS
CENTERS = [0.09200, 0.12650]
HALF_WINDOW = 0.00015
DKH = 0.000025
SURROGATE_FLOOR = 1e-13

VARIANTS = {
    "ndf15_t3e9_s01_early": {
        "tol_perturbations_integration": 3e-9,
        "perturbations_integration_stepsize": 0.1,
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
    "ndf15_t1e9_s01_early": {
        "tol_perturbations_integration": 1e-9,
        "perturbations_integration_stepsize": 0.1,
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
    "ndf15_t1e9_s005_early": {
        "tol_perturbations_integration": 1e-9,
        "perturbations_integration_stepsize": 0.05,
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
    "ndf15_t1e9_s005_earlier": {
        "tol_perturbations_integration": 1e-9,
        "perturbations_integration_stepsize": 0.05,
        "start_small_k_at_tau_c_over_tau_h": 2e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.015,
    },
}

DEFAULT_MAX_WORKERS = min(16, os.cpu_count() or 1)
MAX_WORKERS = max(1, int(os.environ.get("V062_SURROGATE_MAX_WORKERS", DEFAULT_MAX_WORKERS)))


def grid_for_center(center):
    n = int(round(HALF_WINDOW / DKH))
    return [round(center + j * DKH, 8) for j in range(-n, n + 1)]


def all_targets():
    out = []
    for center in CENTERS:
        pkmax = 0.10 if center < 0.1 else 0.14
        for kh in grid_for_center(center):
            out.append({"center": center, "kh": kh, "pkmax_h": pkmax})
    return out


def tag_k(kh):
    return f"{kh:.8f}".replace(".", "p")


def paths_for(variant_name, kh):
    run_name = f"surrogate_fullmap_{variant_name}_{tag_k(kh)}"
    out = RESULTS / f"v062_odeconv_{run_name}_batch_0.json"
    trace = RESULTS / f"v062_odeconv_{run_name}_batch_0_trace.dat"
    return run_name, out, trace


def valid_single_row(path, kh):
    if not path.exists():
        return None
    try:
        obj = json.loads(path.read_text())
        rows = obj.get("rows", [])
        if len(rows) != 1:
            return None
        row = rows[0]
        if abs(float(row["kh_requested"]) - kh) > 5e-10:
            return None
        return row
    except Exception:
        return None


def run_point(variant_name, variant_overrides, spec):
    kh = spec["kh"]
    run_name, out, trace = paths_for(variant_name, kh)
    cached = valid_single_row(out, kh)
    if cached is not None:
        return {
            "variant": variant_name,
            "center": spec["center"],
            "kh": kh,
            "returncode": 0,
            "wall_seconds": 0.0,
            "reused": True,
            "worker_output_json": str(out),
            "row": cached,
        }

    if out.exists():
        out.unlink()
    if trace.exists():
        trace.unlink()

    overrides = dict(variant_overrides)
    overrides["P_k_max_h/Mpc"] = spec["pkmax_h"]
    overrides["k_per_decade_for_pk"] = 1
    overrides["k_per_decade_for_bao"] = 1

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["AEST_OFFLINE_TRACE_FILE"] = str(trace)
    env["AEST_NDF15_WEIGHT_FLOOR"] = f"{SURROGATE_FLOOR:.17g}"
    # The optional E-state rescaling patch may be present locally from a prior
    # diagnostic. Explicitly force its identity setting for this map.
    env["AEST_E_STATE_SCALE"] = "1"

    cmd = [
        sys.executable,
        str(Path(core.__file__).resolve()),
        "--worker",
        run_name,
        json.dumps(overrides),
        "0",
        json.dumps([kh]),
    ]
    t0 = time.perf_counter()
    cp = subprocess.run(cmd, env=env, check=False)
    wall = time.perf_counter() - t0
    row = valid_single_row(out, kh) if cp.returncode == 0 else None
    return {
        "variant": variant_name,
        "center": spec["center"],
        "kh": kh,
        "returncode": cp.returncode,
        "wall_seconds": wall,
        "reused": False,
        "worker_output_json": str(out),
        "row": row,
    }


def roots(rows, center):
    local = sorted(
        [r for r in rows if abs(float(r["kh_requested"]) - center) <= HALF_WINDOW + 1e-12],
        key=lambda r: float(r["kh_requested"]),
    )
    out = []
    for a, b in zip(local[:-1], local[1:]):
        x0 = float(a["kh_requested"])
        x1 = float(b["kh_requested"])
        y0 = float(a["delta_m_gi_final"])
        y1 = float(b["delta_m_gi_final"])
        if y0 == 0.0:
            out.append(x0)
        elif y0 * y1 < 0.0:
            out.append(x0 + (x1 - x0) * (-y0) / (y1 - y0))
    if local and float(local[-1]["delta_m_gi_final"]) == 0.0:
        out.append(float(local[-1]["kh_requested"]))
    return out


def summarize_variant(results):
    good = [r for r in results if r["row"] is not None and r["returncode"] == 0]
    rows = [r["row"] for r in good]
    windows = {}
    for center in CENTERS:
        local = sorted(
            [r for r in rows if abs(float(r["kh_requested"]) - center) <= HALF_WINDOW + 1e-12],
            key=lambda r: float(r["kh_requested"]),
        )
        if not local:
            windows[f"{center:.5f}"] = {"n_points": 0}
            continue
        dms = [float(r["delta_m_gi_final"]) for r in local]
        abs_idx = min(range(len(local)), key=lambda i: abs(dms[i]))
        p_direct_class = [
            abs(float(r["P_direct_Mpc3"]) - float(r["P_class_Mpc3"])) /
            max(abs(float(r["P_class_Mpc3"])), 1e-300)
            for r in local
        ]
        windows[f"{center:.5f}"] = {
            "n_points": len(local),
            "all_negative": all(x < 0.0 for x in dms),
            "all_positive": all(x > 0.0 for x in dms),
            "n_negative": sum(x < 0.0 for x in dms),
            "n_positive": sum(x > 0.0 for x in dms),
            "n_zero": sum(x == 0.0 for x in dms),
            "linear_roots_h_per_Mpc": roots(local, center),
            "minimum_abs_Dm_kh": float(local[abs_idx]["kh_requested"]),
            "minimum_abs_Dm": dms[abs_idx],
            "max_abs_Dm": max(abs(x) for x in dms),
            "max_direct_vs_class_relative": max(p_direct_class),
            "points": [
                {
                    "kh": float(r["kh_requested"]),
                    "delta_m_gi_final": float(r["delta_m_gi_final"]),
                    "P_class_Mpc3": float(r["P_class_Mpc3"]),
                    "P_direct_over_class": float(r["P_direct_over_class"]),
                }
                for r in local
            ],
        }
    return {
        "n_successful_points": len(good),
        "n_expected_points": len(CENTERS) * len(grid_for_center(CENTERS[0])),
        "windows": windows,
    }


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    targets = all_targets()
    tasks = [(vname, vover, spec) for vname, vover in VARIANTS.items() for spec in targets]
    print(json.dumps({
        "classification_use": "NONE_NON_SCIENTIFIC_FAST_SURROGATE_MAP",
        "surrogate_weight_floor": SURROGATE_FLOOR,
        "frozen_weight_floor": 1e-15,
        "requested_target_grid_matches_frozen_certification": True,
        "physical_model_changed": False,
        "solver_tolerances_changed": False,
        "solver_stepsizes_changed": False,
        "early_start_settings_changed": False,
        "auxiliary_internal_k_grid_changed_for_diagnostic": True,
        "E_state_scale_forced_to_identity": 1,
        "n_target_points_per_variant": len(targets),
        "n_variants": len(VARIANTS),
        "n_tasks": len(tasks),
        "max_parallel_workers": min(MAX_WORKERS, len(tasks)),
    }, indent=2), flush=True)

    collected = {name: [] for name in VARIANTS}
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(tasks))) as pool:
        futs = {
            pool.submit(run_point, vname, vover, spec): (vname, spec)
            for vname, vover, spec in tasks
        }
        for fut in as_completed(futs):
            r = fut.result()
            collected[r["variant"]].append(r)
            state = "reuse" if r["reused"] else "done"
            print(
                f"[{r['variant']}] kh={r['kh']:.8f} {state} "
                f"rc={r['returncode']} wall={r['wall_seconds']:.2f}s",
                flush=True,
            )

    for name in collected:
        collected[name].sort(key=lambda r: (r["center"], r["kh"]))

    summary = {
        "classification_use": "NONE_NON_SCIENTIFIC_FAST_SURROGATE_MAP",
        "purpose": "Fast full locked-target-grid topology scout before selective authoritative 1e-15 runs",
        "surrogate_weight_floor": SURROGATE_FLOOR,
        "frozen_weight_floor": 1e-15,
        "physical_model_changed": False,
        "requested_target_k_changed": False,
        "requested_target_grid_matches_frozen_certification": True,
        "tol_perturbations_integration_changed": False,
        "perturbations_integration_stepsize_changed": False,
        "early_start_settings_changed": False,
        "jacobian_abstol_changed": False,
        "auxiliary_internal_k_grid_changed_for_diagnostic": True,
        "E_state_scale_forced_to_identity": 1,
        "final_certification_changed": False,
        "centers_h_per_Mpc": CENTERS,
        "half_window_h_per_Mpc": HALF_WINDOW,
        "DKH_h_per_Mpc": DKH,
        "variants": VARIANTS,
        "variant_summaries": {name: summarize_variant(rr) for name, rr in collected.items()},
        "runs": collected,
    }
    out = RESULTS / "v062_ndf15_weight_floor_full_surrogate_map_summary.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)
    print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    main()
