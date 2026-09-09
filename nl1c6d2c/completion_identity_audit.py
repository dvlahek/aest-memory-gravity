#!/usr/bin/env python3
"""NL1C6D2C completion identity/asymptotic audit.

This implements only the preregistered A1--A5 coefficient-level checks.
It cannot classify full D2C PASS and does not perform nonlinear branch evolution.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

KB = 0.0665
K2 = 9500.0
Q0 = 1.0e-4
Z0 = 1.0e-17
A0_SI = 1.2e-10
C_SI = 299792458.0
MPC_M = 3.085677581491367e22
A0 = A0_SI * MPC_M / (C_SI * C_SI)  # Mpc^-1
EPS_MIX = 0.25

BETAS = (1.0, 0.5, 0.1)
KINDS = ("simple", "exponential", "sharp")
SIGMAS = (-1, 0, 1)
Z_GRID = (-8.0, -4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0, 8.0)
X_TRACK = (0.0, 1e-8, 1e-6, 1e-4, 1e-2, 1.0, 1e2, 1e6, 1e10)
X_DEEP = (1e-2, 3e-3, 1e-3, 3e-4, 1e-4)
X_HIGH = 1e10

A1_GATE = 1e-14
A2_GATE = 6e-9
A3_GATE = 1e-14
A4_GATE = 5e-4
A5_PAD = 1e-12

PASS_LABEL = "NL1C6D2C_COMPLETION_IDENTITY_AUDIT_PASS"
FAIL_LABEL = "NL1C6D2C_COMPLETION_IDENTITY_AUDIT_FAIL"


def git_meta():
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        head, branch = "unknown", "unknown"
    return head, branch


def jfun(x: float, beta: float, kind: str) -> float:
    A = 1.0 + beta
    if kind == "simple":
        return x / (A + beta * x)
    if kind == "exponential":
        return -math.expm1(-beta * x / A) / beta
    if kind == "sharp":
        return min(x / A, 1.0 / beta)
    raise ValueError(kind)


def Jdimless_series(x: float, beta: float, kind: str) -> float:
    """J/a0^2 for small x, evaluated by a stable series."""
    A = 1.0 + beta
    if x == 0.0:
        return 0.0
    if kind == "simple":
        r = beta / A
        s = 0.0
        for n in range(24):
            s += ((-r) ** n) * (x ** (n + 3)) / (n + 3)
        return 2.0 * s / A
    if kind == "exponential":
        c = beta / A
        s = 0.0
        for m in range(1, 24):
            s += ((-1.0) ** (m + 1)) * (c ** m) * (x ** (m + 2)) / (
                math.factorial(m) * (m + 2)
            )
        return 2.0 * s / beta
    if kind == "sharp":
        return 2.0 * x**3 / (3.0 * A)
    raise ValueError(kind)


def Jdimless(x: float, beta: float, kind: str) -> float:
    """Frozen integrated J divided by a0^2, with J(0)=0."""
    if x <= 2.0e-2:
        return Jdimless_series(x, beta, kind)
    A = 1.0 + beta
    if kind == "simple":
        return 2.0 * (
            x * x / (2.0 * beta)
            - A * x / (beta * beta)
            + (A * A / beta**3) * math.log1p(beta * x / A)
        )
    if kind == "exponential":
        c = beta / A
        y = c * x
        one_minus = -math.expm1(-y) - y * math.exp(-y)
        return (2.0 / beta) * (x * x / 2.0 - one_minus / (c * c))
    if kind == "sharp":
        xt = A / beta
        if x <= xt:
            return 2.0 * x**3 / (3.0 * A)
        return x * x / beta - A * A / (3.0 * beta**3)
    raise ValueError(kind)


def Jphys(x: float, beta: float, kind: str) -> float:
    return A0 * A0 * Jdimless(x, beta, kind)


def Kexp(zeta: float) -> float:
    return 2.0 * K2 * Z0 * Z0 * math.expm1(zeta * zeta)


def Hx(x: float) -> float:
    u = x * x
    return u / (1.0 + u)


def mixed_term(x: float, zeta: float, beta: float, sigma: int) -> float:
    Y = A0 * A0 * x * x
    lam = 1.0 / beta
    return (
        sigma
        * EPS_MIX
        * (2.0 - KB)
        * lam
        * Y
        * math.tanh(zeta)
        * Hx(x)
    )


def Fsigma(x: float, zeta: float, beta: float, kind: str, sigma: int) -> float:
    return (
        (2.0 - KB) * Jphys(x, beta, kind)
        - 2.0 * Kexp(zeta)
        + mixed_term(x, zeta, beta, sigma)
    )


def nonincreasing(values, atol=1e-18) -> bool:
    # values are ordered from larger x to smaller x; they must not grow.
    return all(values[i + 1] <= values[i] + atol for i in range(len(values) - 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2c_completion_identity_audit.json",
    )
    args = ap.parse_args()

    # A1: homogeneous slice.
    a1_max = 0.0
    a1_worst = None
    for sigma in SIGMAS:
        for kind in KINDS:
            for beta in BETAS:
                for zeta in Z_GRID:
                    f = Fsigma(0.0, zeta, beta, kind, sigma)
                    r = f + 2.0 * Kexp(zeta)
                    scale = (2.0 - KB) * A0 * A0 + 2.0 * abs(Kexp(zeta))
                    rr = abs(r) / max(scale, 1e-300)
                    if rr > a1_max:
                        a1_max = rr
                        a1_worst = [sigma, kind, beta, zeta]
    a1_pass = a1_max <= A1_GATE

    # A2: coefficient-level mixed linear invisibility.
    a2_by_x = []
    for x in X_DEEP:
        u = x * x
        shape_deriv = u * (2.0 + u) / ((1.0 + u) ** 2)
        worst = 0.0
        for sigma in (-1, 1):
            for zeta in Z_GRID:
                ry = abs(sigma) * EPS_MIX * abs(math.tanh(zeta)) * shape_deriv
                worst = max(worst, ry)
        a2_by_x.append(worst)
    a2_monotone = nonincreasing(a2_by_x)
    a2_endpoint = a2_by_x[-1]
    a2_pass = a2_monotone and a2_endpoint <= A2_GATE

    # A3: exact tracking slice.
    a3_max = 0.0
    a3_worst = None
    for sigma in SIGMAS:
        for kind in KINDS:
            for beta in BETAS:
                for x in X_TRACK:
                    f = Fsigma(x, 0.0, beta, kind, sigma)
                    target = (2.0 - KB) * Jphys(x, beta, kind)
                    r = f - target
                    scale = (2.0 - KB) * (A0 * A0 + abs(Jphys(x, beta, kind)))
                    rr = abs(r) / max(scale, 1e-300)
                    if rr > a3_max:
                        a3_max = rr
                        a3_worst = [sigma, kind, beta, x]
    a3_pass = a3_max <= A3_GATE

    # A4: deep-MOND subleading mixed correction.
    a4_by_x = []
    a4_worst_cases = []
    for x in X_DEEP:
        worst = 0.0
        case = None
        for sigma in (-1, 1):
            for kind in KINDS:
                for beta in BETAS:
                    base = (2.0 - KB) * abs(Jphys(x, beta, kind))
                    for zeta in Z_GRID:
                        rr = abs(mixed_term(x, zeta, beta, sigma)) / max(base, 1e-300)
                        if rr > worst:
                            worst = rr
                            case = [sigma, kind, beta, zeta]
        a4_by_x.append(worst)
        a4_worst_cases.append(case)
    a4_monotone = nonincreasing(a4_by_x)
    a4_endpoint = a4_by_x[-1]
    a4_pass = a4_monotone and a4_endpoint <= A4_GATE

    # A5: high-gradient bounded sign control.
    bvals = []
    a5_worst = []
    for sigma in SIGMAS:
        for zeta in Z_GRID:
            B = 1.0 + sigma * EPS_MIX * math.tanh(zeta) * Hx(X_HIGH)
            bvals.append(B)
            if not (0.75 - A5_PAD <= B <= 1.25 + A5_PAD and B > 0.0):
                a5_worst.append([sigma, zeta, B])
    bmin = min(bvals)
    bmax = max(bvals)
    a5_pass = len(a5_worst) == 0

    gates = {
        "A1_homogeneous_identity": bool(a1_pass),
        "A2_mixed_linear_invisibility_coefficient": bool(a2_pass),
        "A3_tracking_identity": bool(a3_pass),
        "A4_deep_MOND_subleading": bool(a4_pass),
        "A5_high_gradient_bound": bool(a5_pass),
    }
    passed = all(gates.values())
    classification = PASS_LABEL if passed else FAIL_LABEL
    head, branch = git_meta()

    payload = {
        "classification": classification,
        "full_D2C_classified": False,
        "scope": "C1, coefficient-level C2, C3, C4, C5 only; no nonlinear FLRW branch evolution",
        "git": {"head": head, "branch": branch},
        "constants": {
            "K_B": KB,
            "K2": K2,
            "Q0_Mpc^-1": Q0,
            "Z0_Mpc^-1": Z0,
            "a0_SI_m_s^-2": A0_SI,
            "a0_geo_Mpc^-1": A0,
            "epsilon_mix": EPS_MIX,
            "beta0": list(BETAS),
            "kinds": list(KINDS),
            "sigmas": list(SIGMAS),
        },
        "grids": {
            "Z_GRID": list(Z_GRID),
            "X_TRACK": list(X_TRACK),
            "X_DEEP": list(X_DEEP),
            "X_HIGH": X_HIGH,
        },
        "A1": {
            "max_normalized_residual": a1_max,
            "worst_case": a1_worst,
            "gate": A1_GATE,
            "pass": bool(a1_pass),
        },
        "A2": {
            "worst_RY_by_x": dict(zip(map(str, X_DEEP), a2_by_x)),
            "monotone_decreasing_with_decreasing_x": bool(a2_monotone),
            "endpoint_x1e-4": a2_endpoint,
            "endpoint_gate": A2_GATE,
            "pass": bool(a2_pass),
        },
        "A3": {
            "max_normalized_residual": a3_max,
            "worst_case": a3_worst,
            "gate": A3_GATE,
            "pass": bool(a3_pass),
        },
        "A4": {
            "worst_ratio_by_x": dict(zip(map(str, X_DEEP), a4_by_x)),
            "worst_cases_by_x": dict(zip(map(str, X_DEEP), a4_worst_cases)),
            "monotone_decreasing_with_decreasing_x": bool(a4_monotone),
            "endpoint_x1e-4": a4_endpoint,
            "endpoint_gate": A4_GATE,
            "pass": bool(a4_pass),
        },
        "A5": {
            "B_min": bmin,
            "B_max": bmax,
            "allowed_with_pad": [0.75 - A5_PAD, 1.25 + A5_PAD],
            "violations": a5_worst,
            "pass": bool(a5_pass),
        },
        "gates": gates,
        "historical_results_unchanged": True,
        "nonlinear_branch_selection_performed": False,
        "NL1C7_authorized": False,
    }

    out = Path(args.json_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n")

    print(f"a0_geo_Mpc^-1={A0:.17g}")
    print(f"A1 max={a1_max:.6e} gate={A1_GATE:.1e} pass={a1_pass}")
    print(f"A2 endpoint={a2_endpoint:.6e} gate={A2_GATE:.1e} monotone={a2_monotone} pass={a2_pass}")
    print(f"A3 max={a3_max:.6e} gate={A3_GATE:.1e} pass={a3_pass}")
    print(f"A4 endpoint={a4_endpoint:.6e} gate={A4_GATE:.1e} monotone={a4_monotone} pass={a4_pass}")
    print(f"A5 B=[{bmin:.12g},{bmax:.12g}] pass={a5_pass}")
    print(f"CLASSIFICATION={classification}")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
