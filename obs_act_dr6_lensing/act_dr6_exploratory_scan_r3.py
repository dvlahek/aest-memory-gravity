#!/usr/bin/env python3
from __future__ import annotations

"""Technical R3 wrapper for the frozen ACT DR6 exploratory scan.

R2 reached the first CLASS spectrum but stopped because raw_cl()['pp'] contained
non-finite values. R3 diagnoses their multipole support and permits zeroing only
when all non-finite entries are confined to L=0,1. Any non-finite L>=2 remains
an execution failure. No likelihood/model/eta setting is changed.
"""

import numpy as np

# Importing R2 applies its frozen CLASS input-contract patch to the base module.
from obs_act_dr6_lensing import act_dr6_exploratory_scan_r2 as _r2  # noqa: F401
from obs_act_dr6_lensing import act_dr6_exploratory_scan as base


def compute_clpp_r3(memory_enabled: bool, eta: float):
    from classy import Class

    c = Class()
    c.set(base.theory_params(memory_enabled, eta))
    c.compute()
    try:
        raw = c.raw_cl(base.LMAX)
        if "pp" not in raw:
            raise RuntimeError(f"CLASS raw_cl lacks pp; keys={sorted(raw)}")
        clpp = np.asarray(raw["pp"], float).copy()
        ell = np.arange(clpp.size, dtype=float)
        if clpp.size < base.TRIM_LMAX + 2:
            raise RuntimeError(f"CLASS pp length {clpp.size} is below likelihood requirement")

        bad = np.flatnonzero(~np.isfinite(clpp))
        if bad.size:
            print(
                "CLASS_PP_NONFINITE "
                f"memory_enabled={memory_enabled} eta={eta:.12e} "
                f"count={bad.size} indices={bad.tolist()}",
                flush=True,
            )
            if np.any(bad >= 2):
                raise FloatingPointError(
                    "nonfinite CLASS lensing-potential spectrum at physical multipoles "
                    f"L>=2: {bad[bad >= 2].tolist()}"
                )
            clpp[bad] = 0.0
            print(
                "CLASS_PP_LOWELL_SANITIZED "
                f"memory_enabled={memory_enabled} eta={eta:.12e} "
                f"indices={bad.tolist()}",
                flush=True,
            )

        if not np.all(np.isfinite(clpp[2:])):
            raise FloatingPointError("nonfinite CLASS lensing-potential spectrum remains for L>=2")
        return ell, clpp
    finally:
        c.struct_cleanup()
        c.empty()


base.compute_clpp = compute_clpp_r3


if __name__ == "__main__":
    raise SystemExit(base.main())
