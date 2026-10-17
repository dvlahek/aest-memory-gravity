#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from b2_maxwell_memory import (
    asymptotic_rho_star,
    asymptotic_taylor_scaled,
    direct_split_certificate,
    finite_h_crossover,
    taylor_high_jet_certificate,
)


def route_row(h: float, rmax: float) -> dict:
    taylor = float(taylor_high_jet_certificate(rmax, h))
    direct = float(direct_split_certificate(rmax, h))
    gamma = taylor / direct if direct > 0.0 else math.inf
    rho = h * rmax
    if math.isclose(gamma, 1.0, rel_tol=1e-13, abs_tol=0.0):
        route = "equal_resolved" if rho <= 1.0 + 1e-12 else "tie"
    else:
        route = "high_jet" if gamma < 1.0 else "direct"
    return {
        "h": float(h),
        "rmax": float(rmax),
        "rho_hR": float(rho),
        "taylor_high_jet_certificate": taylor,
        "direct_split_certificate": direct,
        "gamma_taylor_over_direct": float(gamma),
        "preferred_certificate": route,
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "B2R1 rigorous h x R route-transition phase diagram for the "
            "generalized-Maxwell memory benchmark."
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
        rc = float(finite_h_crossover(h))
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
                "certificate_at_crossover_over_h": 0.5 * (bt + bd) / h,
                "taylor_at_crossover": bt,
                "direct_at_crossover": bd,
            }
        )

    log_h = np.log(np.asarray([q["h"] for q in cross], dtype=float))
    log_R = np.log(np.asarray([q["R_cross"] for q in cross], dtype=float))
    slope, intercept = np.polyfit(log_h, log_R, 1)
    fit_prefactor = float(math.exp(intercept))

    rgrid = np.geomspace(args.rmin, args.rmax, args.nr)
    rows = [route_row(float(h), float(r)) for h in hs for r in rgrid]

    inconsistencies = 0
    for q in rows:
        gamma = q["gamma_taylor_over_direct"]
        route = q["preferred_certificate"]
        rho = q["rho_hR"]
        if math.isclose(gamma, 1.0, rel_tol=1e-13, abs_tol=0.0):
            expected = "equal_resolved" if rho <= 1.0 + 1e-12 else "tie"
        else:
            expected = "high_jet" if gamma < 1.0 else "direct"
        if route != expected:
            inconsistencies += 1

    cert_scaled_limit = float(asymptotic_taylor_scaled(rho_star))

    print("B2R1_ROUTE_TRANSITION gamma=B_T/B_D")
    print("B2R1_RESOLVED rho<=1 gives identical high-jet and direct-split bounds")
    print("B2R1_POST_SPLIT high_jet if gamma<1; direct if gamma>1")
    print(
        "B2R1_ASYMPTOTIC_LAW "
        f"R_cross(h) ~ rho_star/h; rho_star={rho_star:.16e}"
    )
    print(
        "B2R1_LOGLOG_FIT "
        f"R_cross ~ {fit_prefactor:.16e} h^({slope:.16e})"
    )
    print(
        "B2R1_CROSS_CERTIFICATE "
        f"B_cross/h -> {cert_scaled_limit:.16e}"
    )
    print("h R_cross h*R_cross rel_rho_error certificate_at_cross cert/h")
    for q in cross:
        print(
            f'{q["h"]:.6e} '
            f'{q["R_cross"]:.12e} '
            f'{q["rho_cross_hR"]:.12e} '
            f'{q["relative_rho_error"]:.6e} '
            f'{q["certificate_at_crossover"]:.12e} '
            f'{q["certificate_at_crossover_over_h"]:.12e}'
        )

    payload = {
        "benchmark": "B2R1 rigorous Maxwell certificate-route transition phase diagram",
        "model": "same B2 generalized-Maxwell ramp-memory continuum",
        "route_metric": "gamma = B_T / B_D",
        "route_rule": {
            "rho_le_1": "high-jet and direct-split certificates coincide",
            "post_split_gamma_lt_1": "high_jet certificate narrower",
            "post_split_gamma_gt_1": "direct certificate narrower",
            "post_split_gamma_eq_1": "nontrivial route transition",
        },
        "claim_boundary": (
            "Uses only the rigorous closed-form B2 certificate formulas. "
            "No actual-error reference and no observationally tuned threshold "
            "enters the route decision."
        ),
        "asymptotic_theory": {
            "rho": "rho=hR",
            "taylor_scaled_limit": "B_T(rho/h;h)/h -> rho^7/4410",
            "direct_scaled_limit": (
                "B_D(rho/h;h)/h -> 1/4410 + A_tail/2(1-rho^-2) "
                "+ exp(-4)(1-rho^-1)"
            ),
            "rho_star": rho_star,
            "crossover_law": "R_cross(h) ~ rho_star / h",
            "certificate_at_crossover_scaled_limit": cert_scaled_limit,
        },
        "finite_h_crossover": cross,
        "loglog_fit": {
            "slope": float(slope),
            "prefactor": fit_prefactor,
            "expected_slope": -1.0,
            "expected_prefactor_as_h_to_0": rho_star,
        },
        "route_rule_inconsistencies": int(inconsistencies),
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
