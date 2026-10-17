#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from b3_volterra_ramp_memory import (
    asymptotic_direct_scaled,
    asymptotic_rho_star,
    asymptotic_taylor_scaled,
    direct_split_certificate,
    taylor_high_jet_certificate,
)


def finite_h_crossover(h: float) -> float:
    """Robustly solve the nontrivial crossover B_T=B_D above rho=hR=1."""
    if not (0.0 < h <= 1.0):
        raise ValueError("requires 0 < h <= 1")

    split = 1.0 / h

    def f(r: float) -> float:
        return taylor_high_jet_certificate(r, h) - direct_split_certificate(r, h)

    # Do not bracket immediately at rho=1+eps: the two formulas coincide at
    # rho=1 and floating-point cancellation can corrupt the sign there for
    # very small h. Scan in rho until the true negative post-split branch is
    # found, then locate the first subsequent sign change.
    rhos = np.geomspace(1.001, 100.0, 800)
    prev_r = split * float(rhos[0])
    prev_f = f(prev_r)
    have_negative = prev_f < 0.0

    for rho in rhos[1:]:
        r = split * float(rho)
        cur_f = f(r)
        if not have_negative and cur_f < 0.0:
            have_negative = True
        if have_negative and prev_f < 0.0 and cur_f > 0.0:
            return float(brentq(f, prev_r, r, xtol=1e-12, rtol=1e-12))
        prev_r = r
        prev_f = cur_f

    raise RuntimeError(f"failed to bracket B3 crossover for h={h}")


def route_row(h: float, rmax: float) -> dict:
    taylor = float(taylor_high_jet_certificate(rmax, h))
    direct = float(direct_split_certificate(rmax, h))
    gamma = taylor / direct if direct > 0.0 else math.inf

    if math.isclose(taylor, direct, rel_tol=1e-13, abs_tol=0.0):
        route = "equal_resolved"
    elif gamma < 1.0:
        route = "high_jet"
    else:
        route = "direct"

    return {
        "h": float(h),
        "rmax": float(rmax),
        "rho_hR": float(h * rmax),
        "taylor_high_jet_certificate": taylor,
        "direct_split_certificate": direct,
        "gamma_taylor_over_direct": float(gamma),
        "preferred_certificate": route,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "B3R1 rigorous h x R route-transition phase diagram for the "
            "manufactured Volterra ramp-memory benchmark."
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

    rho_star = float(asymptotic_rho_star())
    cross = []

    for h in hs:
        h = float(h)
        rc = finite_h_crossover(h)
        bt = float(taylor_high_jet_certificate(rc, h))
        bd = float(direct_split_certificate(rc, h))
        cross.append(
            {
                "h": h,
                "R_cross": rc,
                "rho_cross_hR": h * rc,
                "rho_star_asymptotic": rho_star,
                "relative_rho_error": abs(h * rc - rho_star) / rho_star,
                "certificate_at_crossover": 0.5 * (bt + bd),
                "certificate_at_crossover_over_h2": 0.5 * (bt + bd) / h**2,
                "taylor_at_crossover": bt,
                "direct_at_crossover": bd,
            }
        )

    log_h = np.log(np.asarray([q["h"] for q in cross], dtype=float))
    log_R = np.log(np.asarray([q["R_cross"] for q in cross], dtype=float))
    slope, intercept = np.polyfit(log_h, log_R, 1)
    prefactor = float(math.exp(intercept))

    rgrid = np.geomspace(args.rmin, args.rmax, args.nr)
    rows = [route_row(float(h), float(r)) for h in hs for r in rgrid]

    inconsistencies = 0
    for row in rows:
        g = row["gamma_taylor_over_direct"]
        label = row["preferred_certificate"]
        if label == "equal_resolved":
            ok = math.isclose(g, 1.0, rel_tol=1e-13, abs_tol=0.0)
        elif label == "high_jet":
            ok = g < 1.0
        else:
            ok = g > 1.0
        if not ok:
            inconsistencies += 1

    print("B3R1_ROUTE_TRANSITION gamma=B_T/B_D")
    print("B3R1_PREFERRED equal_resolved for rho<=1; high_jet if gamma<1; direct if gamma>1")
    print(
        "B3R1_ASYMPTOTIC_LAW "
        f"R_cross(h) ~ rho_star/h; rho_star={rho_star:.16e}"
    )
    print(
        "B3R1_CROSSOVER_CERTIFICATE "
        f"B_cross/h^2 -> {asymptotic_taylor_scaled(rho_star):.16e}"
    )
    print(
        "B3R1_LOGLOG_FIT "
        f"R_cross ~ {prefactor:.16e} h^({slope:.16e})"
    )
    print("h R_cross h*R_cross rel_rho_error certificate_over_h2")
    for q in cross:
        print(
            f'{q["h"]:.6e} '
            f'{q["R_cross"]:.12e} '
            f'{q["rho_cross_hR"]:.12e} '
            f'{q["relative_rho_error"]:.6e} '
            f'{q["certificate_at_crossover_over_h2"]:.12e}'
        )

    payload = {
        "benchmark": "B3R1 rigorous Volterra certificate-route transition phase diagram",
        "model": "same B3 manufactured Volterra ramp-memory model",
        "route_metric": "gamma = B_T / B_D",
        "route_rule": {
            "rho_le_1": "certificates coincide on the resolved band",
            "gamma_lt_1": "high_jet certificate narrower",
            "gamma_gt_1": "direct-split certificate narrower",
            "gamma_eq_1_above_split": "nontrivial route transition",
        },
        "claim_boundary": (
            "Uses only the rigorous closed-form B3 certificate formulas. "
            "No actual-error reference and no observationally tuned threshold "
            "enters the route decision."
        ),
        "numerical_bracketing_note": (
            "The finite-h root finder scans away from rho=1 before Brent "
            "bracketing because B_T and B_D coincide exactly at rho=1 and "
            "floating-point subtraction can corrupt the sign arbitrarily "
            "close to that equality. This is an implementation safeguard, "
            "not a change to the certification formulas."
        ),
        "asymptotic_theory": {
            "rho": "rho=hR",
            "direct_scaled_limit": (
                "B_D(rho/h;h)/h^2 -> 1/3780 + "
                "A_tail/3(1-rho^-3) + exp(-4)/2(1-rho^-2)"
            ),
            "taylor_scaled_limit": "B_T(rho/h;h)/h^2 -> rho^6/3780",
            "rho_star": rho_star,
            "crossover_law": "R_cross(h) ~ rho_star / h",
            "certificate_at_crossover_scaled_limit": float(
                asymptotic_taylor_scaled(rho_star)
            ),
        },
        "finite_h_crossover": cross,
        "loglog_fit": {
            "slope": float(slope),
            "prefactor": prefactor,
            "expected_slope": -1.0,
            "expected_prefactor_as_h_to_0": rho_star,
        },
        "grid": {
            "rmin": float(args.rmin),
            "rmax": float(args.rmax),
            "nr": int(args.nr),
            "h_values": [float(x) for x in hs],
            "row_count": len(rows),
            "route_rule_inconsistencies": inconsistencies,
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
