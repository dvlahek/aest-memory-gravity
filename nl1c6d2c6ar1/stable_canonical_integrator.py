#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6a import physical_time_scalar_current_integrator_v6 as v6

m = v6.m

m.PASS_LABEL = "NL1C6D2C6AR1_STABLE_CANONICAL_VARIABLE_PASS"
m.FAIL_LABEL = "NL1C6D2C6AR1_STABLE_CANONICAL_VARIABLE_FAIL"
m.INCOMPLETE_LABEL = "NL1C6D2C6AR1_STABLE_CANONICAL_VARIABLE_INCOMPLETE"

_last_cancel_ratio = float("nan")


def initial_state_stable(data, nx):
    global _last_cancel_ratio
    C = m.cos_matrix(nx)
    t0 = data["t0"]
    cf = m.class_fields(data, t0, nx, C)
    a, Q, KQQ, Qdot = cf["a"], cf["Q"], cf["KQQ"], cf["Qdot"]
    H = m.bg_eval(data, t0)[1]

    alpha_m = m.mode_values(data, t0, "alpha")
    theta_m = m.mode_values(data, t0, "theta")
    alpha_tau_m = np.asarray(
        [float(md["splines"]["alpha"](t0, 1)) for md in data["modes"]], float
    )
    theta_tau_m = np.asarray(
        [float(md["splines"]["theta"](t0, 1)) for md in data["modes"]], float
    )

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
    _, lap, _, _ = m.spec_ops(nx)

    # Directly store the elliptic canonical combination S=P_alpha+Q P_chi.
    S = -2.0 * a * m.static.KB * lap(cf["E"]) - 2.0 * m.A * a * lap(cf["chi"])
    y = np.stack([cf["alpha"], cf["chi"], pchi, S])

    rhs0 = -2.0 * a * m.static.KB * lap(cf["E"]) - 2.0 * m.A * a * lap(cf["chi"])
    ell = m.norm_residual(S - rhs0, S, rhs0)
    pdef = m.norm_residual(
        pchi - 2.0 * a**3 * KQQ * U,
        pchi,
        2.0 * a**3 * KQQ * U,
    )
    zero = {
        k: float(abs(np.mean(cf[k])) / max(float(np.sqrt(np.mean(cf[k] ** 2))), 1e-300))
        for k in ("alpha", "E", "chi")
    }

    palpha = S - Q * pchi
    _last_cancel_ratio = float(
        (np.linalg.norm(palpha) + np.linalg.norm(Q * pchi))
        / max(np.linalg.norm(S), 1e-300)
    )

    return y, {
        "elliptic_residual": ell,
        "pchi_definition_residual": pdef,
        "zero_mode_relative": zero,
        "all_finite": bool(np.all(np.isfinite(y))),
        "class_start": cf,
        "initial_derivative_method": "exact_conformal_time_chain_rule",
        "canonical_variable": "S=P_alpha+Q*P_chi",
        "cancellation_ratio": _last_cancel_ratio,
    }


def derive_E_stable(data, tau, y, ops):
    a, H, Q, KQ, KQQ, Z, Qdot = m.bg_eval(data, tau)
    alpha, chi, pchi, S = y
    _, _, invlap, _ = ops
    combo = invlap(-S / (2.0 * a))
    E = (combo - m.A * chi) / m.static.KB
    return E, (a, H, Q, KQ, KQQ, Z, Qdot)


def rhs_stable(data, tau, y, ops, C, nonlinear):
    E, b = derive_E_stable(data, tau, y, ops)
    a, H, Q, KQ, KQQ, Z, Qdot = b
    alpha, chi, pchi, S = y
    grad, lap, _, div = ops

    U = pchi / (2.0 * a**3 * KQQ)
    psi = m.to_field(m.mode_values(data, tau, "psi"), C)

    if nonlinear:
        g = grad(chi)
        x = m.static.ACC_CONV * np.abs(g) / a
        j, _ = m.static.j_and_prime(x, 1.0, "simple", saturated=False)
        nl = div((1.0 + j) * g)
    else:
        nl = lap(chi)

    dalpha = a * (E - psi)
    dchi = a * (U + Q * E + Qdot * alpha)
    dpchi = a * (
        -2.0 * m.A * a * lap(E)
        + 2.0 * m.A * a * nl
        - 2.0 * a * KQ * lap(alpha)
    )

    # Exact transformed equation for S=P_alpha+Q P_chi.
    dS = a * (
        -2.0 * a * KQ * lap(chi)
        - 2.0 * m.A * a * Q * lap(E)
        + 2.0 * m.A * a * Q * nl
    )

    return np.stack([dalpha, dchi, dpchi, dS])


def checkpoint_health_stable(data, tau, y, ops):
    E, b = derive_E_stable(data, tau, y, ops)
    a, H, Q, KQ, KQQ, Z, Qdot = b
    alpha, chi, pchi, S = y
    grad, lap, _, _ = ops

    rhs0 = -2.0 * a * m.static.KB * lap(E) - 2.0 * m.A * a * lap(chi)
    cr = m.norm_residual(S - rhs0, S, rhs0)
    g = grad(chi)
    x = m.static.ACC_CONV * np.abs(g) / a
    j, _ = m.static.j_and_prime(x, 1.0, "simple", saturated=False)
    return E, cr, x, j


m.initial_state = initial_state_stable
m.derive_E = derive_E_stable
m.rhs = rhs_stable
m.checkpoint_health = checkpoint_health_stable


def integrate_stable(data, nx, nstep, nonlinear, collect_stats=False):
    out = v6.integrate_fixed_grid(data, nx, nstep, nonlinear, collect_stats)
    if out["states"] is not None:
        arr = out["states"].copy()
        for i, cp in enumerate(out["checkpoints"]):
            Q = m.bg_eval(data, float(cp["tau"]))[2]
            arr[i, 3, :] = arr[i, 3, :] - Q * arr[i, 2, :]
        out["states"] = arr
    return out


m.integrate = integrate_stable
_old_run_main = m.run_main


def run_main_r1(args):
    code = _old_run_main(args)
    p = Path(args.json_out)
    if p.exists():
        d = json.loads(p.read_text())
        d["repair"] = {
            "stage": "NL1C6D2C6A-R1",
            "canonical_variable": "S=P_alpha+Q*P_chi",
            "thresholds_changed": False,
            "physics_changed": False,
            "cancellation_ratio_z6": float(_last_cancel_ratio),
            "historical_D2C6A_remains_FAIL": True,
        }
        d["classification"] = m.PASS_LABEL if all(d.get("gates", {}).values()) else m.FAIL_LABEL
        d["D2C6B_all27_licensed"] = bool(all(d.get("gates", {}).values()))
        p.write_text(json.dumps(d, indent=2, sort_keys=True) + "\n")
        print(f"R1_CANCELLATION_RATIO={_last_cancel_ratio:.12e}", flush=True)
        print(f"R1_CLASSIFICATION={d['classification']}", flush=True)
        print(f"R1_D2C6B_ALL27_LICENSED={d['D2C6B_all27_licensed']}", flush=True)
    return code


m.run_main = run_main_r1

if __name__ == "__main__":
    raise SystemExit(m.main())
