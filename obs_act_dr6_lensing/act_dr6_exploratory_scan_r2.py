#!/usr/bin/env python3
from __future__ import annotations

"""Technical R2 wrapper for the frozen ACT DR6 exploratory scan.

R1 fixed the CLASS lensing output contract by requesting scalar tCl+lCl.
The R1 run then stopped before any eta point because two matter-power-output
parameters inherited from the older v0.63 helper were left in the CLASS input
although this lensing-only scan does not request mPk.  CLASS therefore rejected
those parameters as unread.

This wrapper changes only the CLASS input contract:
- modes = s
- output = tCl,lCl
- remove z_max_pk
- remove P_k_max_h/Mpc

The ACT likelihood, eta grid, cosmological parameters, AeST/memory parameters,
likelihood corrections setting, lmax and nonlinear setting remain unchanged.
"""

from obs_act_dr6_lensing import act_dr6_exploratory_scan as base

_original_theory_params = base.theory_params


def theory_params_r2(memory_enabled: bool, eta: float) -> dict:
    p = _original_theory_params(memory_enabled, eta)
    p["modes"] = "s"
    p["output"] = "tCl,lCl"
    p.pop("z_max_pk", None)
    p.pop("P_k_max_h/Mpc", None)
    return p


base.theory_params = theory_params_r2


if __name__ == "__main__":
    raise SystemExit(base.main())
