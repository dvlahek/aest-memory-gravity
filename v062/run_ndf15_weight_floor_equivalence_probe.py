#!/usr/bin/env python3
"""Non-classifying NDF15 weight-floor equivalence probe for v0.62.

Runs exact tol_perturbations_integration=3e-9 at kh=0.092 with the same frozen
early starts and minimal auxiliary CLASS k grid, while changing only the NDF15
relative-error weight floor through AEST_NDF15_WEIGHT_FLOOR.

Diagnostic floors: 1e-13 and 1e-12. The default/frozen solver floor is 1e-15.
This script does not alter the physical model, target k, perturbation rtol,
initial conditions, Jacobian abstol, or scientific gates. Results MUST NOT be
used for the preregistered v0.62 classification.

If available, the existing exact-3e-9 reference worker JSON from the AeST-E
conditioning probe is used for numerical comparison:
  results/v062_odeconv_aest_E_conditioning_3e9_batch_0.json
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
KH_VALUES = [0.09200]
EARLY_STARTS = {
    "start_small_k_at_tau_c_over_tau_h": 5e-4,
    "start_large_k_at_tau_h_over_tau_k": 0.03,
}
MINIMAL_GRID = {
    "P_k_max_h/Mpc": 0.10,
    "k_per_decade_for_pk": 1,
    "k_per_decade_for_bao": 1,
}
FLOORS = [1e-13, 1e-12]
REFERENCE = RESULTS / "v062_odeconv_aest_E_conditioning_3e9_batch_0.json"


def load_single_row(path):
    if not path.exists():
        return None
    obj = json.loads(path.read_text())
    rows = obj.get("rows", [])
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def relative(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def compare_rows(row, ref):
    if row is None or ref is None:
        return None
    fields = [
        "kh_actual",
        "delta_m_gi_final",
        "delta_m_current_final",
        "theta_m_current_final",
        "P_direct_Mpc3",
        "P_class_Mpc3",
        "P_direct_over_class",
    ]
    out = {}
    for key in fields:
        if key not in row or key not in ref or row[key] is None or ref[key] is None:
            continue
        a = float(row[key])
        b = float(ref[key])
        out[key] = {
            "value": a,
            "reference": b,
            "absolute_difference": abs(a - b),
            "relative_difference": relative(a, b),
        }
    if "P_direct_Mpc3" in row and "P_class_Mpc3" in row:
        pd = float(row["P_direct_Mpc3"])
        pc = float(row["P_class_Mpc3"])
        out["direct_vs_class_same_run_relative"] = abs(pd - pc) / max(abs(pc), 1e-300)
    return out


def run_floor(floor):
    label = f"floor_{floor:.0e}".replace("-", "m")
    variant = f"ndf15_weight_{label}"
    worker_json = RESULTS / f"v062_odeconv_{variant}_batch_0.json"
    trace = RESULTS / f"v062_odeconv_{variant}_batch_0_trace.dat"
    for p in (worker_json, trace):
        if p.exists():
            p.unlink()

    overrides = {
        "tol_perturbations_integration": 3e-9,
        **EARLY_STARTS,
        **MINIMAL_GRID,
    }
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["AEST_OFFLINE_TRACE_FILE"] = str(trace)
    env["AEST_NDF15_WEIGHT_FLOOR"] = f"{floor:.17g}"

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
        "stage": label,
        "classification_use": "NONE_NON_SCIENTIFIC_NDF15_WEIGHT_FLOOR_EQUIVALENCE_PROBE",
        "weight_floor": floor,
        "tol_perturbations_integration": 3e-9,
        "kh_values": KH_VALUES,
    }, indent=2), flush=True)

    t0 = time.perf_counter()
    cp = subprocess.run(cmd, env=env, check=False)
    wall = time.perf_counter() - t0
    row = load_single_row(worker_json) if cp.returncode == 0 else None
    return {
        "weight_floor": floor,
        "wall_seconds": wall,
        "returncode": cp.returncode,
        "worker_output_json": str(worker_json),
        "offline_trace_file": str(trace),
        "row": row,
    }


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    ref = load_single_row(REFERENCE)
    report = {
        "classification_use": "NONE_NON_SCIENTIFIC_NDF15_WEIGHT_FLOOR_EQUIVALENCE_PROBE",
        "purpose": "Test whether the exact-3e-9 runtime cliff is caused by the near-zero-state weight floor while checking target observables against the unmodified 1e-15-floor reference",
        "physical_model_changed": False,
        "requested_target_k_changed": False,
        "tol_perturbations_integration_changed": False,
        "early_start_settings_changed": False,
        "jacobian_abstol_changed": False,
        "ndf15_weight_floor_varied_for_diagnostic": True,
        "auxiliary_internal_k_grid_changed_for_diagnostic": True,
        "final_certification_changed": False,
        "default_frozen_weight_floor": 1e-15,
        "tested_weight_floors": FLOORS,
        "kh_values": KH_VALUES,
        "early_starts": EARLY_STARTS,
        "minimal_auxiliary_grid": MINIMAL_GRID,
        "reference_worker_json": str(REFERENCE),
        "reference_available": ref is not None,
        "reference_row": ref,
        "runs": [],
    }

    for floor in FLOORS:
        r = run_floor(floor)
        r["comparison_to_unmodified_3e9_reference"] = compare_rows(r["row"], ref)
        report["runs"].append(r)
        print(json.dumps(r, indent=2), flush=True)
        if r["returncode"] != 0:
            break

    # Compact decision-support metrics only; no scientific pass/fail gate.
    for r in report["runs"]:
        cmp = r.get("comparison_to_unmodified_3e9_reference") or {}
        if "P_class_Mpc3" in cmp:
            r["P_class_relative_difference_vs_reference"] = cmp["P_class_Mpc3"]["relative_difference"]
        if "P_direct_Mpc3" in cmp:
            r["P_direct_relative_difference_vs_reference"] = cmp["P_direct_Mpc3"]["relative_difference"]
        if "delta_m_gi_final" in cmp:
            r["Dm_relative_difference_vs_reference"] = cmp["delta_m_gi_final"]["relative_difference"]

    summary = RESULTS / "v062_ndf15_weight_floor_equivalence_probe_summary.json"
    summary.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "summary_file": str(summary),
        "classification_use": report["classification_use"],
        "reference_available": report["reference_available"],
        "runs": [
            {
                "weight_floor": r["weight_floor"],
                "wall_seconds": r["wall_seconds"],
                "returncode": r["returncode"],
                "P_class_relative_difference_vs_reference": r.get("P_class_relative_difference_vs_reference"),
                "P_direct_relative_difference_vs_reference": r.get("P_direct_relative_difference_vs_reference"),
                "Dm_relative_difference_vs_reference": r.get("Dm_relative_difference_vs_reference"),
            }
            for r in report["runs"]
        ],
    }, indent=2), flush=True)

    if report["runs"] and report["runs"][-1]["returncode"] != 0:
        raise SystemExit(report["runs"][-1]["returncode"])


if __name__ == "__main__":
    main()
