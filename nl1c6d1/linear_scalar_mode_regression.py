#!/usr/bin/env python3
"""NL1C6D1B: published AeST scalar normal-mode regression.

This script implements only the preregistered linear propagating normal-mode
regression.  It does not evolve the nonlinear repository field chi and cannot
by itself classify the full NL1C6D1 formulation audit.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

H0 = 67.3324639084866
h = H0 / 100.0
K_B = 0.0665
K2 = 9500.0
Q0 = 1.0e-4  # Mpc^-1
BETAS = (1.0, 0.5, 0.1)
K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
K_MPC = K_H * h

AMPLITUDE = 1.0e-8
PRIMARY_STEPS_PER_PERIOD = 80
CONV_STEPS_PER_PERIOD = (40, 80, 160)
N_CYCLES = 24
OMEGA2_FLOOR = 1.0e-12  # Mpc^-2
PRIMARY_RELERR_GATE = 5.0e-3
CONVERGENCE_ORDER_GATE = 1.8
CONV_MODE_INDICES = (0, len(K_H) - 1)

CLASS_PASS = "NL1C6D1B_LINEAR_SCALAR_MODE_REGRESSION_PASS"
CLASS_FAIL = "NL1C6D1B_LINEAR_SCALAR_MODE_REGRESSION_FAIL"


def theory(beta: float, k_mpc: float) -> dict:
    lambda_s = 1.0 / float(beta)
    cs2 = ((2.0 - K_B) / (K2 * K_B)) * (1.0 + 0.5 * K_B * lambda_s)
    mass2 = ((2.0 - K_B) * (1.0 + lambda_s) * Q0**2) / K_B
    omega2 = cs2 * float(k_mpc) ** 2 + mass2
    return {
        "lambda_s": lambda_s,
        "c_s_squared": cs2,
        "c_s": math.sqrt(cs2),
        "M_squared_Mpc^-2": mass2,
        "M_Mpc^-1": math.sqrt(mass2),
        "omega_squared_Mpc^-2": omega2,
        "omega_Mpc^-1": math.sqrt(omega2),
    }


def static_mu2() -> float:
    return 2.0 * K2 * Q0**2 / (2.0 - K_B)


def evolve_mode(omega2: float, steps_per_period: int) -> dict:
    omega = math.sqrt(float(omega2))
    period = 2.0 * math.pi / omega
    dt = period / int(steps_per_period)
    n_steps = int(N_CYCLES * int(steps_per_period))

    x = AMPLITUDE
    p = 0.0
    t = 0.0
    crossings = []
    e0 = 0.25 * p * p + omega2 * x * x
    max_energy_rel_drift = 0.0

    for _ in range(n_steps):
        # Velocity-Verlet for dX/dt=P/2, dP/dt=-2 omega^2 X.
        p_half = p - dt * omega2 * x
        x_new = x + 0.5 * dt * p_half
        p_new = p_half - dt * omega2 * x_new

        if x > 0.0 and x_new <= 0.0:
            frac = x / (x - x_new)
            crossings.append(t + frac * dt)

        x, p = x_new, p_new
        t += dt
        energy = 0.25 * p * p + omega2 * x * x
        max_energy_rel_drift = max(
            max_energy_rel_drift,
            abs(energy - e0) / max(abs(e0), 1.0e-300),
        )

    crossing_times = np.asarray(crossings, float)
    periods = np.diff(crossing_times)
    if periods.size < 4:
        raise RuntimeError(f"insufficient downward zero crossings: {crossing_times.size}")

    # Frozen estimator: discard first and last complete crossing interval.
    used_periods = periods[1:-1]
    mean_period = float(np.mean(used_periods))
    omega_num = 2.0 * math.pi / mean_period
    omega2_num = omega_num * omega_num
    abs_error = abs(omega2_num - omega2)
    rel_error = abs_error / max(abs(omega2), OMEGA2_FLOOR)

    return {
        "steps_per_period": int(steps_per_period),
        "dt_Mpc": float(dt),
        "n_steps": int(n_steps),
        "downward_crossings": int(crossing_times.size),
        "periods_used": int(used_periods.size),
        "omega_num_Mpc^-1": float(omega_num),
        "omega_squared_num_Mpc^-2": float(omega2_num),
        "omega_squared_abs_error_Mpc^-2": float(abs_error),
        "omega_squared_relative_error": float(rel_error),
        "max_energy_relative_drift": float(max_energy_rel_drift),
    }


def observed_order(e_coarse: float, e_fine: float) -> float:
    if e_fine == 0.0:
        return float("inf")
    if e_coarse == 0.0:
        return float("-inf")
    return math.log(e_coarse / e_fine, 2.0)


def finite_json_value(x):
    if isinstance(x, float) and not math.isfinite(x):
        return "inf" if x > 0 else "-inf"
    return x


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    primary_rows = []
    primary_pass = True
    reference = {}

    print("NL1C6D1B_LINEAR_SCALAR_MODE_REGRESSION_START", flush=True)
    print(f"static_mu2={static_mu2():.16e} Mpc^-2", flush=True)
    print(f"static_mu={math.sqrt(static_mu2()):.16e} Mpc^-1", flush=True)

    for beta in BETAS:
        reference[str(beta)] = {}
        for kh, k in zip(K_H, K_MPC):
            th = theory(beta, k)
            num = evolve_mode(th["omega_squared_Mpc^-2"], PRIMARY_STEPS_PER_PERIOD)
            ok = bool(num["omega_squared_relative_error"] <= PRIMARY_RELERR_GATE)
            primary_pass = primary_pass and ok
            row = {
                "beta0": float(beta),
                "k_h_Mpc": float(kh),
                "k_Mpc^-1": float(k),
                **th,
                **num,
                "pass": ok,
            }
            primary_rows.append(row)
            reference[str(beta)][f"{kh:g}"] = th
            print(
                f"PRIMARY beta={beta:g} k={kh:g}h/Mpc "
                f"omega_ref={th['omega_Mpc^-1']:.12e} "
                f"omega_num={num['omega_num_Mpc^-1']:.12e} "
                f"relerr_omega2={num['omega_squared_relative_error']:.6e} "
                f"pass={ok}",
                flush=True,
            )

    convergence_rows = []
    convergence_pass = True
    for beta in BETAS:
        for idx in CONV_MODE_INDICES:
            kh = float(K_H[idx])
            k = float(K_MPC[idx])
            th = theory(beta, k)
            runs = {
                int(spp): evolve_mode(th["omega_squared_Mpc^-2"], int(spp))
                for spp in CONV_STEPS_PER_PERIOD
            }
            e40 = runs[40]["omega_squared_abs_error_Mpc^-2"]
            e80 = runs[80]["omega_squared_abs_error_Mpc^-2"]
            e160 = runs[160]["omega_squared_abs_error_Mpc^-2"]
            p40_80 = observed_order(e40, e80)
            p80_160 = observed_order(e80, e160)
            ok = bool(p40_80 >= CONVERGENCE_ORDER_GATE and p80_160 >= CONVERGENCE_ORDER_GATE)
            convergence_pass = convergence_pass and ok
            row = {
                "beta0": float(beta),
                "k_h_Mpc": kh,
                "k_Mpc^-1": k,
                "runs": runs,
                "p_40_80": finite_json_value(float(p40_80)),
                "p_80_160": finite_json_value(float(p80_160)),
                "pass": ok,
            }
            convergence_rows.append(row)
            print(
                f"CONVERGENCE beta={beta:g} k={kh:g}h/Mpc "
                f"p40_80={p40_80:.6f} p80_160={p80_160:.6f} pass={ok}",
                flush=True,
            )

    classification = CLASS_PASS if primary_pass and convergence_pass else CLASS_FAIL
    payload = {
        "label": "NL1C6D1B_LINEAR_SCALAR_MODE_REGRESSION",
        "classification": classification,
        "full_D1_classified": False,
        "physical_branch_selection_evaluated": False,
        "nonlinear_chi_evolved": False,
        "constants": {
            "H0_km_s_Mpc": H0,
            "h": h,
            "K_B": K_B,
            "K2": K2,
            "Q0_Mpc^-1": Q0,
            "beta0": list(BETAS),
            "k_h_Mpc": K_H.tolist(),
            "k_Mpc^-1": K_MPC.tolist(),
            "static_mu_squared_Mpc^-2": static_mu2(),
            "static_mu_Mpc^-1": math.sqrt(static_mu2()),
        },
        "frozen_numerics": {
            "amplitude": AMPLITUDE,
            "primary_steps_per_period": PRIMARY_STEPS_PER_PERIOD,
            "convergence_steps_per_period": list(CONV_STEPS_PER_PERIOD),
            "n_cycles": N_CYCLES,
            "omega2_floor_Mpc^-2": OMEGA2_FLOOR,
            "primary_relative_error_gate": PRIMARY_RELERR_GATE,
            "convergence_order_gate": CONVERGENCE_ORDER_GATE,
            "frequency_estimator": "downward_zero_crossings_linear_interpolation_discard_first_last_interval",
            "integrator": "velocity_verlet_canonical_X_P",
        },
        "gates": {
            "all_18_primary_frequency_cases": bool(primary_pass),
            "all_6_convergence_cases_second_order": bool(convergence_pass),
        },
        "reference": reference,
        "primary_rows": primary_rows,
        "convergence_rows": convergence_rows,
    }

    out = Path(args.json_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"CLASSIFICATION={classification}", flush=True)
    print(f"JSON={out}", flush=True)
    print("NL1C6D1B_LINEAR_SCALAR_MODE_REGRESSION_END", flush=True)
    return 0 if classification == CLASS_PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
