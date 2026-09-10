#!/usr/bin/env python3
from __future__ import annotations

import numpy as np

from nl1c6d2c6a import physical_time_scalar_current_integrator as m


def initial_state_chain_rule(data, nx):
    C = m.cos_matrix(nx)
    t0 = data["t0"]
    cf = m.class_fields(data, t0, nx, C)
    a, Q, KQQ, Qdot = cf["a"], cf["Q"], cf["KQQ"], cf["Qdot"]
    H = m.bg_eval(data, t0)[1]

    alpha_m = m.mode_values(data, t0, "alpha")
    E_m = m.mode_values(data, t0, "E")
    theta_m = m.mode_values(data, t0, "theta")
    alpha_tau_m = np.asarray(
        [float(md["splines"]["alpha"](t0, 1)) for md in data["modes"]], float
    )
    theta_tau_m = np.asarray(
        [float(md["splines"]["theta"](t0, 1)) for md in data["modes"]], float
    )

    # Exact conformal-time chain rule for chi=Q(a*Theta/k^2+alpha).
    Q_tau = a * Qdot
    a_tau = a * a * H
    theta_pot_m = a * theta_m / (m.K_MPC * m.K_MPC)
    dchi_tau_m = (
        Q_tau * (theta_pot_m + alpha_m)
        + Q * (
            a_tau * theta_m / (m.K_MPC * m.K_MPC)
            + a * theta_tau_m / (m.K_MPC * m.K_MPC)
            + alpha_tau_m
        )
    )
    chi_tau = m.to_field(dchi_tau_m, C)

    U = chi_tau / a - Q * cf["E"] - Qdot * cf["alpha"]
    pchi = 2.0 * a**3 * KQQ * U
    grad, lap, invlap, div = m.spec_ops(nx)
    palpha = -Q * pchi - 2.0 * a * m.static.KB * lap(cf["E"]) - 2.0 * m.A * a * lap(cf["chi"])
    y = np.stack([cf["alpha"], cf["chi"], pchi, palpha])

    lhs = palpha + Q * pchi
    rhs = -2.0 * a * m.static.KB * lap(cf["E"]) - 2.0 * m.A * a * lap(cf["chi"])
    ell = m.norm_residual(lhs - rhs, lhs, rhs)
    pdef = m.norm_residual(
        pchi - 2.0 * a**3 * KQQ * U,
        pchi,
        2.0 * a**3 * KQQ * U,
    )
    zero = {
        k: float(abs(np.mean(cf[k])) / max(float(np.sqrt(np.mean(cf[k] ** 2))), 1e-300))
        for k in ("alpha", "E", "chi")
    }
    return y, {
        "elliptic_residual": ell,
        "pchi_definition_residual": pdef,
        "zero_mode_relative": zero,
        "all_finite": bool(np.all(np.isfinite(y))),
        "class_start": cf,
        "initial_derivative_method": "exact_conformal_time_chain_rule",
    }


m.initial_state = initial_state_chain_rule

if __name__ == "__main__":
    raise SystemExit(m.main())
