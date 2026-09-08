#!/usr/bin/env python3
"""Fast execution-only timing probe for the v0.62 fixed-k ODE path.

This script is deliberately NOT a scientific certification and its outputs must
not be used for the preregistered v0.62 classification.  It exists only to
measure how expensive the patched CLASS path is on the current machine before
launching another long convergence run.

Modes:
  quick   : default NDF15 integration, two locked centre k values.
  medium  : modestly tighter 3e-6 tolerance, six nearby k values.

The physical AeST background/model parameters are inherited unchanged from
run_fixed_k_ode_convergence.py.  The numerical settings below are diagnostic
runtime settings only and are intentionally kept separate from the final
certification script.
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

PROBES = {
    "quick": {
        "overrides": {},
        "kh_values": [0.09200, 0.12650],
        "description": "default NDF15, two centre modes; runtime smoke test only",
    },
    "medium": {
        "overrides": {
            "tol_perturbations_integration": 3e-6,
        },
        "kh_values": [
            0.091975, 0.09200, 0.092025,
            0.126475, 0.12650, 0.126525,
        ],
        "description": "3e-6 NDF15 tolerance, six local modes; runtime probe only",
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=sorted(PROBES), nargs="?", default="quick")
    args = ap.parse_args()

    cfg = PROBES[args.mode]
    variant = f"runtime_probe_{args.mode}"
    out = RESULTS / f"v062_odeconv_{variant}_batch_0.json"
    trace = RESULTS / f"v062_odeconv_{variant}_batch_0_trace.dat"
    summary = RESULTS / f"v062_runtime_probe_{args.mode}.json"

    # Always execute a fresh timing probe.
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
        json.dumps(cfg["overrides"]),
        "0",
        json.dumps(cfg["kh_values"]),
    ]

    print(json.dumps({
        "classification_use": "NONE_NON_SCIENTIFIC_RUNTIME_PROBE",
        "mode": args.mode,
        "description": cfg["description"],
        "kh_values": cfg["kh_values"],
        "overrides": cfg["overrides"],
        "omp_num_threads": 1,
        "physical_model_changed": False,
        "final_certification_changed": False,
    }, indent=2), flush=True)

    t0 = time.perf_counter()
    cp = subprocess.run(cmd, env=env, check=False)
    wall = time.perf_counter() - t0

    report = {
        "classification_use": "NONE_NON_SCIENTIFIC_RUNTIME_PROBE",
        "mode": args.mode,
        "description": cfg["description"],
        "wall_seconds": wall,
        "returncode": cp.returncode,
        "kh_values": cfg["kh_values"],
        "overrides": cfg["overrides"],
        "worker_output_json": str(out),
        "trace_file": str(trace),
        "physical_model_changed": False,
        "final_certification_changed": False,
    }
    summary.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2), flush=True)
    raise SystemExit(cp.returncode)


if __name__ == "__main__":
    main()
