#!/usr/bin/env python3
"""Non-scientific reduced-grid target-mode runtime probe for v0.62.

Purpose
-------
Measure the exact 3e-9 AeST NDF15 cost of one preregistered target k value
without evolving the full P(k) grid out to 10 h/Mpc.  This is an execution
isolation diagnostic only.  It MUST NOT be used for the preregistered v0.62
scientific classification.

The AeST equations, physical parameters, perturbation tolerance and frozen
early-start settings are inherited unchanged from run_fixed_k_ode_convergence.
Only P_k_max_h/Mpc is reduced for this diagnostic in order to isolate how much
of the runtime comes from the auxiliary internal CLASS P(k) grid.

Modes
-----
target_092   : kh=0.09200 with diagnostic P_k_max_h/Mpc=0.10
target_1265  : kh=0.12650 with diagnostic P_k_max_h/Mpc=0.14
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=sorted(PROBES), nargs="?", default="target_092")
    args = ap.parse_args()
    cfg = PROBES[args.mode]

    overrides = {
        "tol_perturbations_integration": 3e-9,
        **EARLY_STARTS,
        "P_k_max_h/Mpc": cfg["pkmax_h"],
    }

    variant = f"target_isolation_{args.mode}"
    out = RESULTS / f"v062_odeconv_{variant}_batch_0.json"
    trace = RESULTS / f"v062_odeconv_{variant}_batch_0_trace.dat"
    summary = RESULTS / f"v062_target_isolation_{args.mode}.json"

    for p in (out, trace, summary):
        if p.exists():
            p.unlink()

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["AEST_OFFLINE_TRACE_FILE"] = str(trace)

    # Existing optional diagnostics remain externally controllable.  The early
    # dynamics trace can be enabled by exporting AEST_EARLY_DYNAMICS_TRACE_FILE
    # before invoking this script.
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
        "classification_use": "NONE_NON_SCIENTIFIC_TARGET_GRID_ISOLATION_PROBE",
        "mode": args.mode,
        "description": "Exact frozen 3e-9/early-start AeST target-mode timing with a reduced auxiliary CLASS P(k) grid",
        "kh_values": cfg["kh_values"],
        "diagnostic_P_k_max_h_per_Mpc": cfg["pkmax_h"],
        "frozen_tol_perturbations_integration": 3e-9,
        "frozen_early_starts": EARLY_STARTS,
        "physical_model_changed": False,
        "solver_tolerance_changed": False,
        "scientific_grid_changed_for_classification": False,
        "auxiliary_pk_grid_changed_for_diagnostic": True,
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
