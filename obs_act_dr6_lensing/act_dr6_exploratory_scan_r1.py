#!/usr/bin/env python3
from __future__ import annotations

"""Technical R1 wrapper for the frozen ACT DR6 exploratory scan.

The original scan stopped before any eta point because CLASS was asked for
`lensing=yes` with only `output=lCl`.  Preserve the original implementation
and change only the CLASS output contract required by the lensed-spectrum
module: scalar modes and a temperature Cl alongside the lensing-potential Cl.
The ACT likelihood remains lens_only=True with primary-CMB corrections off.
"""

from obs_act_dr6_lensing import act_dr6_exploratory_scan as base

_original_theory_params = base.theory_params


def theory_params_r1(memory_enabled: bool, eta: float) -> dict:
    p = _original_theory_params(memory_enabled, eta)
    p["modes"] = "s"
    p["output"] = "tCl,lCl"
    return p


base.theory_params = theory_params_r1


if __name__ == "__main__":
    raise SystemExit(base.main())
