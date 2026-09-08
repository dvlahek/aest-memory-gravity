#!/usr/bin/env python3
"""Non-classifying minimal-internal-k runtime probe for v0.62.

This diagnostic keeps the AeST model, exact 3e-9 perturbation tolerance,
frozen early-start settings, and requested target k unchanged.  It changes
only the auxiliary CLASS P(k)/BAO sampling density and P(k) extent so we can
measure how much of the runtime cliff comes from the internal k grid.

Outputs from this script MUST NOT be used for the preregistered v0.62
scientific classification.
"""

from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time

import run_fixed_k_ode_convergence as core

RESULTS = core.RESULTS
EARLY_STARTS = {
    "start_small_k_at_tau_c_over_tau_h": 5e-4,
    "start_large_k_at_tau_h_over_tau_k": 0.03,
}

PROBES = {
    "target_092": {
        "kh_values": [0.09200],
        "pkmax_h": 0.10,
    },
    "target_1265": {
        "kh_values": [0.12650],
        "pkmax_h": 0.14,
    },
}

# Deliberately minimal auxiliary sampling for this timing control only.
K_PER_DECADE_PK = 1
K_PER_DECADE_BAO = 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=sorted(PROBES), nargs="?", default="target_092")
    args = ap.parse_args()
    cfg = PROBES[args.mode]

    overrides = {
        "tol_perturbations_integration": 3e-9,
        **EARLY_STARTS,
        "P_k_max_h/Mpc": cfg["pkmax_h"],
        "k_per_decade_for_pk": K_PER_DECADE_PK,
        "k_per_decade_for_bao": K_PER_DECADE_BAO,
    }

    variant = f"minimal_grid_{args.mode}"
    out = RESULTS / f"v062_odeconv_{variant}_batch_0.json"
    trace = RESULTS / f"v062_odeconv_{variant}_batch_0_trace.dat"
    summary = RESULTS / f"v062_minimal_grid_{args.mode}.json"

    for p in (out, trace, summary):
        if p.exists():
            p.unlink()

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
        json.dumps(cfg["kh_values"]),
    ]

    header = {
        "classification_use": "NONE_NON_SCIENTIFIC_MINIMAL_INTERNAL_K_GRID_PROBE",
        "mode": args.mode,
        "description": "Exact 3e-9 AeST target timing with deliberately minimal auxiliary CLASS k sampling",
        "kh_values": cfg["kh_values"],
        "tol_perturbations_integration": 3e-9,
        "early_starts": EARLY_STARTS,
        "diagnostic_P_k_max_h_per_Mpc": cfg["pkmax_h"],
        "diagnostic_k_per_decade_for_pk": K_PER_DECADE_PK,
        "diagnostic_k_per_decade_for_bao": K_PER_DECADE_BAO,
        "physical_model_changed": False,
        "solver_tolerance_changed": False,
        "requested_target_k_changed": False,
        "auxiliary_internal_k_grid_changed_for_diagnostic": True,
        "final_certification_changed": False,
        "omp_num_threads": 1,
    }
    print(json.dumps(header, indent=2), flush=True)

    t0 = time.perf_counter()
    cp = subprocess.run(cmd, env=env, check=False)
    wall = time.perf_counter() - t0

    report = dict(header)
    report.update({
        "wall_seconds": wall,
        "returncode": cp.returncode,
        "worker_output_json": str(out),
        "offline_trace_file": str(trace),
    })
    summary.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2), flush=True)
    raise SystemExit(cp.returncode)


if __name__ == "__main__":
    main()
