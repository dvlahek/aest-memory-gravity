#!/usr/bin/env python3
"""Non-classifying AeST E state-coordinate rescaling equivalence probe.

Tests the exact tol_perturbations_integration=3e-9 AeST solution at kh=0.092
using an invertible numerical coordinate transform E_stored=S*E_physical.
The physical equations are decoded/encoded by the companion patch. NDF15's
weight floor remains the frozen 1e-15 and Jacobian abstol is unchanged.

Diagnostic scales: 1e4 and 1e6. These values were selected from the prior
conditioning trace: |E| can reach ~1e-19, so they lift the stored coordinate
near/above the 1e-15 solver floor without modifying the physical variable.

Results MUST NOT be used for the preregistered v0.62 classification.
"""

from pathlib import Path
import json
import os
import subprocess
import sys
import time

import run_fixed_k_ode_convergence as core

RESULTS = core.RESULTS
KH_VALUES = [0.09200]
SCALES = [1e4, 1e6]
REFERENCE = RESULTS / "v062_odeconv_aest_E_conditioning_3e9_batch_0.json"
EARLY_STARTS = {
    "start_small_k_at_tau_c_over_tau_h": 5e-4,
    "start_large_k_at_tau_h_over_tau_k": 0.03,
}
MINIMAL_GRID = {
    "P_k_max_h/Mpc": 0.10,
    "k_per_decade_for_pk": 1,
    "k_per_decade_for_bao": 1,
}


def load_single_row(path):
    if not path.exists():
        return None
    obj = json.loads(path.read_text())
    rows = obj.get("rows", [])
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def rel(a, b):
    return abs(float(a)-float(b))/max(abs(float(b)), 1e-300)


def compare(row, ref):
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
        if key in row and key in ref and row[key] is not None and ref[key] is not None:
            out[key] = {
                "value": row[key],
                "reference": ref[key],
                "absolute_difference": abs(float(row[key])-float(ref[key])),
                "relative_difference": rel(row[key], ref[key]),
            }
    if row.get("P_direct_Mpc3") is not None and row.get("P_class_Mpc3") is not None:
        out["direct_vs_class_same_run_relative"] = rel(row["P_direct_Mpc3"], row["P_class_Mpc3"])
    return out


def label_scale(scale):
    return f"{scale:.0e}".replace("+", "").replace("-", "m")


def run_scale(scale):
    label = label_scale(scale)
    variant = f"aest_E_state_scale_{label}"
    out = RESULTS / f"v062_odeconv_{variant}_batch_0.json"
    trace = RESULTS / f"v062_odeconv_{variant}_batch_0_trace.dat"
    for p in (out, trace):
        if p.exists():
            p.unlink()

    overrides = {
        "tol_perturbations_integration": 3e-9,
        "perturbations_integration_stepsize": 0.1,
        **EARLY_STARTS,
        **MINIMAL_GRID,
    }
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["AEST_OFFLINE_TRACE_FILE"] = str(trace)
    env["AEST_E_STATE_SCALE"] = f"{scale:.17g}"
    # Explicitly remove the prior weight-floor diagnostic override if inherited.
    env.pop("AEST_NDF15_WEIGHT_FLOOR", None)

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
        "stage": variant,
        "classification_use": "NONE_NON_SCIENTIFIC_AEST_E_STATE_RESCALING_EQUIVALENCE_PROBE",
        "E_state_scale": scale,
        "frozen_ndf15_weight_floor": 1e-15,
        "tol_perturbations_integration": 3e-9,
        "kh_values": KH_VALUES,
    }, indent=2), flush=True)

    t0 = time.perf_counter()
    cp = subprocess.run(cmd, env=env, check=False)
    wall = time.perf_counter()-t0
    row = load_single_row(out) if cp.returncode == 0 else None
    return {
        "E_state_scale": scale,
        "wall_seconds": wall,
        "returncode": cp.returncode,
        "worker_output_json": str(out),
        "offline_trace_file": str(trace),
        "row": row,
    }


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    ref = load_single_row(REFERENCE)
    report = {
        "classification_use": "NONE_NON_SCIENTIFIC_AEST_E_STATE_RESCALING_EQUIVALENCE_PROBE",
        "purpose": "Test an invertible E_stored=S*E_physical coordinate transform as a conditioning fix for the exact-3e-9 NDF15 runtime cliff",
        "physical_equations_changed": False,
        "state_coordinate_changed_for_diagnostic": True,
        "ndf15_weight_floor_changed": False,
        "frozen_ndf15_weight_floor": 1e-15,
        "jacobian_abstol_changed": False,
        "tol_perturbations_integration_changed": False,
        "requested_target_k_changed": False,
        "early_start_settings_changed": False,
        "auxiliary_internal_k_grid_changed_for_diagnostic": True,
        "final_certification_changed": False,
        "kh_values": KH_VALUES,
        "tested_E_state_scales": SCALES,
        "early_starts": EARLY_STARTS,
        "minimal_auxiliary_grid": MINIMAL_GRID,
        "reference_worker_json": str(REFERENCE),
        "reference_available": ref is not None,
        "reference_row": ref,
        "runs": [],
    }

    for scale in SCALES:
        r = run_scale(scale)
        r["comparison_to_unmodified_3e9_reference"] = compare(r["row"], ref)
        cmp = r["comparison_to_unmodified_3e9_reference"] or {}
        if "delta_m_gi_final" in cmp:
            r["Dm_relative_difference_vs_reference"] = cmp["delta_m_gi_final"]["relative_difference"]
        if "P_class_Mpc3" in cmp:
            r["P_class_relative_difference_vs_reference"] = cmp["P_class_Mpc3"]["relative_difference"]
        if "P_direct_Mpc3" in cmp:
            r["P_direct_relative_difference_vs_reference"] = cmp["P_direct_Mpc3"]["relative_difference"]
        report["runs"].append(r)
        print(json.dumps(r, indent=2), flush=True)
        if r["returncode"] != 0:
            break

    summary = RESULTS / "v062_aest_E_state_rescaling_equivalence_probe_summary.json"
    summary.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({
        "summary_file": str(summary),
        "classification_use": report["classification_use"],
        "reference_available": report["reference_available"],
        "runs": [{
            "E_state_scale": r["E_state_scale"],
            "wall_seconds": r["wall_seconds"],
            "returncode": r["returncode"],
            "Dm_relative_difference_vs_reference": r.get("Dm_relative_difference_vs_reference"),
            "P_class_relative_difference_vs_reference": r.get("P_class_relative_difference_vs_reference"),
            "P_direct_relative_difference_vs_reference": r.get("P_direct_relative_difference_vs_reference"),
        } for r in report["runs"]],
    }, indent=2), flush=True)

    if report["runs"] and report["runs"][-1]["returncode"] != 0:
        raise SystemExit(report["runs"][-1]["returncode"])


if __name__ == "__main__":
    main()
