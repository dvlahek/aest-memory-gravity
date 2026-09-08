#!/usr/bin/env python3
"""Targeted non-classifying frozen-floor sign confirmation for v0.62.

This is the last narrow diagnostic after the fast 1e-13 full-grid surrogate map.
The selected k values were chosen *after* seeing that surrogate map, so this
script is explicitly NOT part of the preregistered v0.62 classification and
must never be used to turn a preregistered FAIL/unresolved result into a PASS.

What is frozen here
-------------------
- AeST physical model and cosmology from run_fixed_k_ode_convergence.py.
- NDF15 state-weight floor remains the original/default 1e-15: the diagnostic
  AEST_NDF15_WEIGHT_FLOOR environment override is explicitly removed.
- The two tested solver endpoints use exactly the frozen tolerance, NDF15
  nominal stepsize, and early-start values from the smooth-limit certification.
- AEST_E_STATE_SCALE is forced to 1, so the abandoned E-rescaling diagnostic is
  the identity transformation.

What is diagnostic-only
-----------------------
- Only eight requested target-mode solves are run: for each of two endpoint
  solver variants, the two locked window centres plus that variant's two
  smallest-|Dm| locations from the 1e-13 surrogate scout.
- The auxiliary CLASS mPk grid is minimized (k_per_decade=1 and a small Pkmax)
  to avoid re-solving the full internal k grid. Requested target k values are
  unchanged.

The purpose is only to ask a narrow question: at the exact/default NDF15
weight floor, do the most root-favourable surrogate locations and the two
window centres remain on the negative branch?  A positive answer is supporting
numerical evidence, not the formal V062_SMOOTH_LIMIT_CERTIFIED gate.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import os
import subprocess
import sys
import time

import run_fixed_k_ode_convergence as core

RESULTS = core.RESULTS
FROZEN_WEIGHT_FLOOR = 1e-15
CENTERS = [0.09200, 0.12650]

# Endpoint variants from the locked v0.62 smooth-limit certification.
# We intentionally do not run the two intermediate 1e-9 controls here because
# this is a minimal post-surrogate sign confirmation, not a replacement for the
# full preregistered convergence grid.
VARIANTS = {
    "ndf15_t3e9_s01_early": {
        "tol_perturbations_integration": 3e-9,
        "perturbations_integration_stepsize": 0.1,
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

# Chosen after the completed 1e-13 full surrogate map:
# - t3e9 minima:     0.091900 and 0.126350
# - t1e9/earlier minima: 0.092025 and 0.126450
# Each variant also checks both locked window centres.
TARGETS = {
    "ndf15_t3e9_s01_early": [0.091900, 0.092000, 0.126350, 0.126500],
    "ndf15_t1e9_s005_earlier": [0.092000, 0.092025, 0.126450, 0.126500],
}

DEFAULT_MAX_WORKERS = min(8, os.cpu_count() or 1)
MAX_WORKERS = max(1, int(os.environ.get("V062_FINAL_EXACT_MAX_WORKERS", DEFAULT_MAX_WORKERS)))


def tag_k(kh):
    return f"{kh:.8f}".replace(".", "p")


def output_paths(variant, kh):
    worker_variant = f"targeted_frozenfloor_{variant}_{tag_k(kh)}"
    out = RESULTS / f"v062_odeconv_{worker_variant}_batch_0.json"
    trace = RESULTS / f"v062_odeconv_{worker_variant}_batch_0_trace.dat"
    return worker_variant, out, trace


def valid_single_row(path, kh):
    if not path.exists():
        return None
    try:
        obj = json.loads(path.read_text())
        rows = obj.get("rows", [])
        if len(rows) != 1:
            return None
        row = rows[0]
        if abs(float(row["kh_requested"]) - float(kh)) > 5e-10:
            return None
        return row
    except Exception:
        return None


def pkmax_for(kh):
    return 0.10 if kh < 0.1 else 0.14


def run_point(variant, kh):
    worker_variant, out, trace = output_paths(variant, kh)
    cached = valid_single_row(out, kh)
    if cached is not None:
        return {
            "variant": variant,
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

    overrides = dict(VARIANTS[variant])
    # Diagnostic-only auxiliary grid reduction.  The requested mode itself and
    # all physical/solver settings listed above remain unchanged.
    overrides["P_k_max_h/Mpc"] = pkmax_for(kh)
    overrides["k_per_decade_for_pk"] = 1
    overrides["k_per_decade_for_bao"] = 1

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["AEST_OFFLINE_TRACE_FILE"] = str(trace)

    # Exact/default frozen NDF15 floor: no diagnostic floor override.
    env.pop("AEST_NDF15_WEIGHT_FLOOR", None)

    # The abandoned source-coordinate rescaling patch may be compiled into the
    # local CLASS tree.  Force its identity setting explicitly.
    env["AEST_E_STATE_SCALE"] = "1"

    # Avoid accidental runtime-profiler instrumentation inherited from a shell.
    for name in (
        "AEST_NDF15_PROFILE_FILE",
        "AEST_NDF15_DOMINATOR_FILE",
        "AEST_PERTURBATION_INDEX_MAP_FILE",
        "AEST_EARLY_DYNAMICS_TRACE_FILE",
    ):
        env.pop(name, None)

    cmd = [
        sys.executable,
        str(Path(core.__file__).resolve()),
        "--worker",
        worker_variant,
        json.dumps(overrides),
        "0",
        json.dumps([kh]),
    ]

    t0 = time.perf_counter()
    cp = subprocess.run(cmd, env=env, check=False)
    wall = time.perf_counter() - t0
    row = valid_single_row(out, kh) if cp.returncode == 0 else None
    return {
        "variant": variant,
        "kh": kh,
        "returncode": cp.returncode,
        "wall_seconds": wall,
        "reused": False,
        "worker_output_json": str(out),
        "row": row,
    }


def main():
    specs = [(variant, kh) for variant in VARIANTS for kh in TARGETS[variant]]

    print(json.dumps({
        "classification_use": "NONE_NON_SCIENTIFIC_TARGETED_FROZEN_FLOOR_SIGN_CONFIRMATION",
        "selected_after_surrogate_map": True,
        "may_be_used_for_preregistered_pass": False,
        "frozen_ndf15_weight_floor": FROZEN_WEIGHT_FLOOR,
        "weight_floor_environment_override": None,
        "physical_model_changed": False,
        "requested_target_k_changed": False,
        "solver_tolerances_changed_relative_to_selected_frozen_variants": False,
        "solver_stepsizes_changed_relative_to_selected_frozen_variants": False,
        "early_start_settings_changed_relative_to_selected_frozen_variants": False,
        "auxiliary_internal_k_grid_changed_for_diagnostic": True,
        "E_state_scale_forced_to_identity": 1,
        "variants": VARIANTS,
        "targets_h_per_Mpc": TARGETS,
        "n_tasks": len(specs),
        "max_parallel_workers": min(MAX_WORKERS, len(specs)),
    }, indent=2), flush=True)

    results = []
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(specs))) as pool:
        futs = {pool.submit(run_point, variant, kh): (variant, kh) for variant, kh in specs}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            row = r["row"]
            if row is None:
                sign = "NO_ROW"
                dm = None
            else:
                dm = float(row["delta_m_gi_final"])
                sign = "NEG" if dm < 0 else ("POS" if dm > 0 else "ZERO")
            state = "reuse" if r["reused"] else "done"
            print(
                f"[{r['variant']}] kh={r['kh']:.8f} {state} rc={r['returncode']} "
                f"wall={r['wall_seconds']:.2f}s sign={sign} Dm={dm}",
                flush=True,
            )

    results.sort(key=lambda r: (r["variant"], r["kh"]))

    variant_summaries = {}
    all_success = True
    all_negative = True
    max_direct_class = 0.0
    min_abs_dm = None

    for variant in VARIANTS:
        rr = [r for r in results if r["variant"] == variant]
        good = [r for r in rr if r["returncode"] == 0 and r["row"] is not None]
        dms = [float(r["row"]["delta_m_gi_final"]) for r in good]
        direct = [
            abs(float(r["row"]["P_direct_over_class"]) - 1.0)
            for r in good
            if r["row"].get("P_direct_over_class") is not None
        ]
        v_all_success = len(good) == len(TARGETS[variant])
        v_all_negative = v_all_success and all(x < 0.0 for x in dms)
        v_min_abs = min((abs(x) for x in dms), default=None)
        v_max_direct = max(direct, default=None)

        all_success = all_success and v_all_success
        all_negative = all_negative and v_all_negative
        if v_max_direct is not None:
            max_direct_class = max(max_direct_class, v_max_direct)
        if v_min_abs is not None:
            min_abs_dm = v_min_abs if min_abs_dm is None else min(min_abs_dm, v_min_abs)

        variant_summaries[variant] = {
            "n_successful_points": len(good),
            "n_expected_points": len(TARGETS[variant]),
            "all_negative": v_all_negative,
            "n_negative": sum(x < 0.0 for x in dms),
            "n_positive": sum(x > 0.0 for x in dms),
            "n_zero": sum(x == 0.0 for x in dms),
            "minimum_abs_Dm_on_selected_points": v_min_abs,
            "max_direct_vs_class_relative": v_max_direct,
            "points": [
                {
                    "kh": r["kh"],
                    "wall_seconds": r["wall_seconds"],
                    "reused": r["reused"],
                    "delta_m_gi_final": (float(r["row"]["delta_m_gi_final"]) if r["row"] else None),
                    "P_class_Mpc3": (float(r["row"]["P_class_Mpc3"]) if r["row"] else None),
                    "P_direct_over_class": (float(r["row"]["P_direct_over_class"]) if r["row"] and r["row"].get("P_direct_over_class") is not None else None),
                }
                for r in rr
            ],
        }

    summary = {
        "classification_use": "NONE_NON_SCIENTIFIC_TARGETED_FROZEN_FLOOR_SIGN_CONFIRMATION",
        "selected_after_surrogate_map": True,
        "may_be_used_for_preregistered_pass": False,
        "purpose": "Exact/default-floor sign check at surrogate-selected root-favourable points and locked centres",
        "frozen_ndf15_weight_floor": FROZEN_WEIGHT_FLOOR,
        "weight_floor_environment_override": None,
        "physical_model_changed": False,
        "requested_target_k_changed": False,
        "solver_tolerances_changed_relative_to_selected_frozen_variants": False,
        "solver_stepsizes_changed_relative_to_selected_frozen_variants": False,
        "early_start_settings_changed_relative_to_selected_frozen_variants": False,
        "auxiliary_internal_k_grid_changed_for_diagnostic": True,
        "E_state_scale_forced_to_identity": 1,
        "formal_v062_certification_changed": False,
        "variants": VARIANTS,
        "targets_h_per_Mpc": TARGETS,
        "all_tasks_successful": all_success,
        "all_selected_exact_floor_Dm_negative": all_negative,
        "minimum_abs_Dm_across_selected_points": min_abs_dm,
        "max_direct_vs_class_relative": max_direct_class if all_success else None,
        "variant_summaries": variant_summaries,
        "runs": results,
        "interpretation_rule": (
            "If all selected exact-floor points remain negative, this supports the surrogate no-root topology at the tested high-risk locations. "
            "It does not replace the locked full-grid smooth-limit certification."
        ),
    }

    out = RESULTS / "v062_targeted_frozen_floor_sign_confirmation_summary.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)
    print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    main()
