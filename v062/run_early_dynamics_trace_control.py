#!/usr/bin/env python3
"""Non-classifying early-time dynamics control for the v0.62 NDF15 cliff.

Runs the same pinned v0.62 cosmology and exact 3e-9 / early-start numerical
settings in either AeST or standard-CLASS mode, with one requested centre mode.
The CLASS source must first be instrumented with
apply_early_dynamics_trace_patch.py.

This diagnostic does not alter the frozen v0.62 certification or its gates.
"""
from pathlib import Path
import argparse
import json
import os
import time

import run_fixed_k_ode_convergence as core

RESULTS = core.RESULTS
KH = 0.092000
OVERRIDES = {
    "tol_perturbations_integration": 3e-9,
    "start_small_k_at_tau_c_over_tau_h": 5e-4,
    "start_large_k_at_tau_h_over_tau_k": 0.03,
}


def main():
    from classy import Class

    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["aest", "standard"])
    args = ap.parse_args()

    pars = dict(core.BASE)
    pars.update(OVERRIDES)
    if args.mode == "standard":
        pars["aest_enabled"] = "no"

    k = KH * core.h
    pars["k_output_values"] = f"{k:.17g}"

    trace = RESULTS / f"v062_early_dynamics_{args.mode}.dat"
    summary = RESULTS / f"v062_early_dynamics_{args.mode}.json"
    offline = RESULTS / f"v062_early_dynamics_{args.mode}_offline_trace.dat"
    for p in (trace, summary, offline):
        if p.exists():
            p.unlink()

    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["AEST_EARLY_DYNAMICS_TRACE_FILE"] = str(trace)
    os.environ.setdefault("AEST_EARLY_DYNAMICS_TAU_MIN", "0.03")
    os.environ.setdefault("AEST_EARLY_DYNAMICS_TAU_MAX", "7.0")
    os.environ.setdefault("AEST_EARLY_DYNAMICS_GROWTH", "1.03")
    os.environ["AEST_OFFLINE_TRACE_FILE"] = str(offline)

    header = {
        "classification_use": "NONE_NON_SCIENTIFIC_EARLY_DYNAMICS_TRACE",
        "mode": args.mode,
        "description": "AeST-vs-standard early-time UR/metric/AeST dynamics trace at exact 3e-9 tolerance",
        "kh_requested": KH,
        "k_requested_Mpc_inv": k,
        "overrides": OVERRIDES,
        "aest_enabled": args.mode == "aest",
        "tau_trace_min": float(os.environ["AEST_EARLY_DYNAMICS_TAU_MIN"]),
        "tau_trace_max": float(os.environ["AEST_EARLY_DYNAMICS_TAU_MAX"]),
        "trace_growth": float(os.environ["AEST_EARLY_DYNAMICS_GROWTH"]),
        "trace_file": str(trace),
        "physical_model_is_control": args.mode == "standard",
        "final_certification_changed": False,
    }
    print(json.dumps(header, indent=2), flush=True)

    cosmo = Class()
    cosmo.set(pars)
    t0 = time.perf_counter()
    returncode = 0
    error = None
    interrupted = False
    try:
        cosmo.compute()
    except KeyboardInterrupt:
        interrupted = True
        returncode = 130
        error = "KeyboardInterrupt"
    except Exception as exc:
        returncode = 1
        error = repr(exc)
    wall = time.perf_counter() - t0

    report = dict(header)
    report.update({
        "wall_seconds": wall,
        "returncode": returncode,
        "interrupted": interrupted,
        "error": error,
        "trace_exists": trace.exists(),
        "trace_bytes": trace.stat().st_size if trace.exists() else 0,
    })
    summary.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2), flush=True)

    try:
        cosmo.struct_cleanup()
        cosmo.empty()
    except Exception:
        pass

    raise SystemExit(returncode)


if __name__ == "__main__":
    main()
