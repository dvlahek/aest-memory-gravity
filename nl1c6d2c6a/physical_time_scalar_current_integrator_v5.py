#!/usr/bin/env python3
from __future__ import annotations

import numpy as np

from nl1c6d2c6a import physical_time_scalar_current_integrator_v4 as v4
from nl1c6d2n import exp_normalization_audit as norm

m = v4.m


def bg_eval_exact(data, tau):
    """Evaluate the preregistered corrected background at exact physical tau.

    This removes only the avoidable endpoint dependence on a truncated native
    background interpolation table. No physics parameters or D2C6A gates are
    changed.
    """
    a_spline = data["modes"][0]["splines"]["a"]
    a = float(a_spline(tau))
    a_tau = float(a_spline(tau, 1))
    if not np.isfinite(a) or not np.isfinite(a_tau) or a <= 0.0:
        raise FloatingPointError("nonfinite/invalid CLASS a(tau) evaluation")

    H = a_tau / (a * a)
    I0 = float(data["background_audit"]["I0"])
    kq_req = I0 / (a ** 3)
    x = kq_req / (2.0 * norm.K2 * norm.Z0)
    Z = float(norm.exp_inverse_positive(float(x)))
    Q, _, KQ, KQQ = norm.exp_eval(Z)
    Qdot = -3.0 * H * KQ / KQQ

    vals = (a, H, Q, KQ, KQQ, Z, Qdot)
    if not np.all(np.isfinite(vals)) or KQQ <= 0.0:
        raise FloatingPointError("nonfinite/invalid exact corrected background evaluation")
    return vals


m.bg_eval = bg_eval_exact

if __name__ == "__main__":
    raise SystemExit(m.main())
