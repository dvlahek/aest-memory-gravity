#!/usr/bin/env python3
"""Non-scientific standard-CLASS control for the v0.62 NDF15 runtime cliff.

Purpose
-------
Test whether the 3e-9 NDF15 microstepping / error-dominator behaviour also
appears when the AeST sector is disabled, while keeping the cosmological
parameters and relevant numerical settings identical to the v0.62 sparse
runtime probe.

This is an execution/conditioning diagnostic only. It MUST NOT be used for the
preregistered v0.62 scientific classification and does not modify the frozen
certification configuration.

Profiler instrumentation is enabled externally through the existing
AEST_NDF15_PROFILE_FILE and AEST_NDF15_DOMINATOR_FILE environment variables.
"""

from pathlib import Path
import json
import os
import time

import run_fixed_k_ode_convergence as core

RESULTS = core.RESULTS
CENTRES2 = [0.092000, 0.126500]
OVERRIDES = {
    "tol_perturbations_integration": 3e-9,
    "start_small_k_at_tau_c_over_tau_h": 5e-4,
    "start_large_k_at_tau_h_over_tau_k": 0.03,
}


def main():
    from classy import Class

    # Start from the exact v0.62 cosmology, then disable only the AeST model.
    # The standard CDM density is already core.BASE['omega_cdm'].
    pars = dict(core.BASE)
    pars.update(OVERRIDES)
    pars["aest_enabled"] = "no"

    k_values = [kh * core.h for kh in CENTRES2]
    pars["k_output_values"] = ", ".join(f"{k:.17g}" for k in k_values)

    trace = RESULTS / "v062_standard_class_ndf15_control_trace.dat"
    summary = RESULTS / "v062_standard_class_ndf15_control.json"
    for p in (trace, summary):
        if p.exists():
            p.unlink()

    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["AEST_OFFLINE_TRACE_FILE"] = str(trace)

    header = {
        "classification_use": "NONE_NON_SCIENTIFIC_STANDARD_CLASS_CONDITIONING_CONTROL",
        "description": "AeST disabled; same cosmology and 3e-9/early-start numerical settings as sparse v0.62 runtime-cliff probe",
        "kh_values": CENTRES2,
        "overrides": OVERRIDES,
        "aest_enabled": False,
        "physical_model_is_control_not_frozen_aest": True,
        "final_certification_changed": False,
    }
    print(json.dumps(header, indent=2), flush=True)

    cosmo = Class()
    cosmo.set(pars)
    t0 = time.perf_counter()
    returncode = 0
    error = None
    try:
        cosmo.compute()
    except Exception as exc:
        returncode = 1
        error = repr(exc)
    wall = time.perf_counter() - t0

    report = dict(header)
    report.update({
        "wall_seconds": wall,
        "returncode": returncode,
        "error": error,
        "trace_file": str(trace),
        "ndf15_profile_file": os.environ.get("AEST_NDF15_PROFILE_FILE"),
        "ndf15_dominator_file": os.environ.get("AEST_NDF15_DOMINATOR_FILE"),
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
