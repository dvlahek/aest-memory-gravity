#!/usr/bin/env python3
from __future__ import annotations

import numpy as np
from scipy.interpolate import CubicSpline

from fullj_weyl import stable_aest_desi_dr1_r9b2e_raw_solver_velocity_closure as base

REPAIR_PREFIT_LOCK = "28e98f6490ab02a979461b150af972898156d1fa"
ORIGINAL_PREFIT_LOCK = "756eb268bdc4d0c3ba8dc6bfa94ba74eb11bdab1"
ORIGINAL_IMPLEMENTATION_LOCK = "4fedc11b3d501ea486c9838506b487789203b66c"


def _prepare_history_ordered(raw, target_k_h: float):
    akey = base._pick(raw, ("a", "scale factor"))
    tkey = base._pick(raw, ("tau [Mpc]", "tau", "tau[Mpc]"))
    dbkey = base._pick(raw, ("delta_b", "d_b"))
    tbkey = base._pick(raw, ("theta_b", "t_b"))
    dckey = base._pick(raw, ("delta_cdm", "d_cdm"))
    tckey = base._pick(raw, ("theta_cdm", "t_cdm"))
    phikey = base._pick(raw, ("phi",))
    pprime = "phi_prime" if "phi_prime" in raw else None

    aa = np.asarray(raw[akey], float)
    tau = np.asarray(raw[tkey], float)
    db = np.asarray(raw[dbkey], float)
    tb = np.asarray(raw[tbkey], float)
    dc = np.asarray(raw[dckey], float)
    tc = np.asarray(raw[tckey], float)
    phi = np.asarray(raw[phikey], float)

    if pprime is not None:
        phip = np.asarray(raw[pprime], float)
        tau, aa, db, tb, dc, tc, phi, phip = base._clean_x(
            tau, aa, db, tb, dc, tc, phi, phip
        )
        phip_source = "direct_CLASS_phi_prime"
    else:
        tau, aa, db, tb, dc, tc, phi = base._clean_x(
            tau, aa, db, tb, dc, tc, phi
        )
        phip = CubicSpline(tau, phi, bc_type="not-a-knot")(tau, 1)
        phip_source = "cubic_spline_derivative_of_phi"

    if np.any(aa <= 0.0):
        raise RuntimeError("nonpositive scale factor in raw history")

    return {
        "k_h": float(target_k_h),
        "tau": tau,
        "a": aa,
        "z": 1.0 / aa - 1.0,
        "d_b": db,
        "t_b": tb,
        "d_cdm": dc,
        "t_cdm": tc,
        "phi": phi,
        "phi_prime": phip,
        "phi_prime_source": phip_source,
        "n": int(tau.size),
        "keys": sorted(raw.keys()),
        "mode_mapping": "ordered_k_output_values_response",
    }


def _ordered_histories_repair(c, h: float):
    del h  # mapping is defined by the ordered k_output_values request, not a missing raw k column
    pert = c.get_perturbations()
    raws, key = base.d2a.scalar_histories(pert)
    if len(raws) != len(base.K_H):
        raise RuntimeError(
            f"expected {len(base.K_H)} scalar histories, got {len(raws)}"
        )
    histories = [
        _prepare_history_ordered(raw, float(base.K_H[i]))
        for i, raw in enumerate(raws)
    ]
    return histories, key, 0.0


def main() -> int:
    print(
        "STABLE_AEST_DESI_DR1_R9B2E_REPAIR01_ORDERED_HISTORY_MAPPING_PASS "
        f"repair_prefit={REPAIR_PREFIT_LOCK} original_prefit={ORIGINAL_PREFIT_LOCK} "
        f"original_implementation={ORIGINAL_IMPLEMENTATION_LOCK}",
        flush=True,
    )
    base._ordered_histories = _ordered_histories_repair
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
