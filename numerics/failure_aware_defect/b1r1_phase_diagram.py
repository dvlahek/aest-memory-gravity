#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from b1_continuum_symbol_defect import (
    FD8_SMALL_XI_C9,
    FD8_SYMBOL_ABS,
    direct_analytic_certificate,
    taylor_high_jet_certificate,
)


def asymptotic_direct_scaled(rho: float) -> float:
    """Limit of B_D(rho/h;h)/h^2 as h -> 0 for fixed rho >= 1."""
    if rho < 1.0:
        raise ValueError("rho must be >= 1")
    return (
        FD8_SMALL_XI_C9 / 6.0
        + 0.5 * (1.0 - rho**-2)
        + (FD8_SYMBOL_ABS / 3.0) * (1.0 - rho**-3)
    )


def asymptotic_taylor_scaled(rho: float) -> float:
    """Limit of B_T(rho/h;h)/h^2 as h -> 0."""
    return rho**6 / 3780.0


def asymptotic_crossover_rho() -> float:
    """Unique nontrivial rho > 1 solving the small-h route transition law."""
    f = lambda rho: asymptotic_taylor_scaled(rho) - asymptotic_direct_scaled(rho)
    return float(brentq(f, 1.0 + 1e-10, 16.0, rtol=1e-14, maxiter=1000))


def finite_h_crossover(h: float) -> float:
    """Solve B_T(R;h)=B_D(R;h) for the crossover R > 1/h."""
    if not (0.0 < h <= 1.0):
        raise ValueError("requires 0 < h <= 1")

    lo = (1.0 / h) * (1.0 + 1e-10)

    def f(r: float) -> float:
        return taylor_high_jet_certificate(r, h) - direct_analytic_certificate(r, h)

    hi = 2.0 * lo
    while f(hi) <= 0.0:
        hi *= 2.0
        if not math.isfinite(hi) or hi > 1e300:
            raise RuntimeError(f"failed to bracket crossover for h={h}")

    return float(brentq(f, lo, hi, rtol=1e-13, maxiter=1000))


def route_row(h: float, rmax: float) -> dict:
    taylor = float(taylor_high_jet_certificate(rmax, h))
    direct = float(direct_analytic_certificate(rmax, h))
    gamma = taylor / direct if direct > 0.0 else math.inf
    if gamma < 1.0:
        route = "high_jet"
    elif gamma > 1.0:
        route = "direct"
    else:
        route = "tie"

    return {
        "h": float(h),
        "rmax": float(rmax),
        "rho_hR": float(h * rmax),
        "taylor_high_jet_certificate": taylor,
        "direct_analytic_certificate": direct,
        "gamma_taylor_over_direct": float(gamma),
        "preferred_certificate": route,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "B1R1 rigorous h x R route-transition phase diagram using only "
            "the two B1 certificate formulas."
        )
    )
    ap.add_argument(
        "--h",
        type=float,
        nargs="*",
        default=[0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001],
    )
    ap.add_argument("--rmin", type=float, default=3.0)
    ap.add_argument("--rmax", type=float, default=1e5)
    ap.add_argument("--nr", type=int, default=181)
    ap.add_argument("--csv", type=Path, default=None)
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()

    hs = np.asarray(args.h, dtype=float)
    if np.any(~np.isfinite(hs)) or np.any(hs <= 0.0) or np.any(hs > 1.0):
        raise SystemExit("all h values must satisfy 0 < h <= 1")
    if not (math.isfinite(args.rmin) and math.isfinite(args.rmax)):
        raise SystemExit("rmin and rmax must be finite")
    if args.rmin < 1.0 or args.rmax <= args.rmin:
        raise SystemExit("require 1 <= rmin < rmax")
    if args.nr < 3:
        raise SystemExit("nr must be >= 3")

    rho_star = asymptotic_crossover_rho()

    cross = []
    for h in hs:
        rc = finite_h_crossover(float(h))
        bt = taylor_high_jet_certificate(rc, float(h))
        bd = direct_analytic_certificate(rc, float(h))
        cross.append(
            {
                "h": float(h),
                "R_cross": float(rc),
                "rho_cross_hR": float(h * rc),
                "rho_star_asymptotic": float(rho_star),
                "relative_rho_error": float(abs(h * rc - rho_star) / rho_star),
                "certificate_at_crossover": float(0.5 * (bt + bd)),
                "taylor_at_crossover": float(bt),
                "direct_at_crossover": float(bd),
            }
        )

    log_h = np.log(np.asarray([q["h"] for q in cross], dtype=float))
    log_R = np.log(np.asarray([q["R_cross"] for q in cross], dtype=float))
    slope, intercept = np.polyfit(log_h, log_R, 1)
    fit_prefactor = float(math.exp(intercept))

    rgrid = np.geomspace(args.rmin, args.rmax, args.nr)
    rows = [route_row(float(h), float(r)) for h in hs for r in rgrid]

    print("B1R1_ROUTE_TRANSITION gamma=B_T/B_D")
    print("B1R1_PREFERRED high_jet if gamma<1; direct if gamma>1")
    print(
        "B1R1_ASYMPTOTIC_LAW "
        f"R_cross(h) ~ rho_star/h; rho_star={rho_star:.16e}"
    )
    print(
        "B1R1_LOGLOG_FIT "
        f"R_cross ~ {fit_prefactor:.16e} h^({slope:.16e})"
    )
    print("h R_cross h*R_cross rel_rho_error certificate_at_cross")
    for q in cross:
        print(
            f'{q["h"]:.6e} '
            f'{q["R_cross"]:.12e} '
            f'{q["rho_cross_hR"]:.12e} '
            f'{q["relative_rho_error"]:.6e} '
            f'{q["certificate_at_crossover"]:.12e}'
        )

    payload = {
        "benchmark": "B1R1 rigorous certificate-route transition phase diagram",
        "model": "same B1 continuum spectral model",
        "route_metric": "gamma = B_T / B_D",
        "route_rule": {
            "gamma_lt_1": "high_jet certificate narrower",
            "gamma_gt_1": "direct certificate narrower",
            "gamma_eq_1": "route transition",
        },
        "claim_boundary": (
            "Uses only rigorous closed-form certificate formulas. "
            "No actual-error reference and no observationally tuned threshold "
            "enters the route decision."
        ),
        "asymptotic_theory": {
            "rho": "rho=hR",
            "direct_scaled_limit": (
                "B_D(rho/h;h)/h^2 -> C9/6 + "
                "1/2(1-rho^-2) + A/3(1-rho^-3)"
            ),
            "taylor_scaled_limit": "B_T(rho/h;h)/h^2 -> rho^6/3780",
            "rho_star": float(rho_star),
            "crossover_law": "R_cross(h) ~ rho_star / h",
        },
        "finite_h_crossover": cross,
        "loglog_fit": {
            "slope": float(slope),
            "prefactor": fit_prefactor,
            "expected_slope": -1.0,
            "expected_prefactor_as_h_to_0": float(rho_star),
        },
        "grid": {
            "rmin": float(args.rmin),
            "rmax": float(args.rmax),
            "nr": int(args.nr),
            "h_values": [float(x) for x in hs],
            "rows": rows,
        },
    }

    if args.csv is not None:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0]))
            wr.writeheader()
            wr.writerows(rows)
        print("WROTE", args.csv)

    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print("WROTE", args.json)


if __name__ == "__main__":
    main()
