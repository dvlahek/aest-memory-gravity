#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from scipy.integrate import quad

FD8_POSITIVE_WEIGHTS = {
    1: 4.0 / 5.0,
    2: -1.0 / 5.0,
    3: 4.0 / 105.0,
    4: -1.0 / 280.0,
}
FD8_TAYLOR_C = 1.0 / 630.0
FD8_SYMBOL_ABS = 25.0 / 12.0
FD8_SMALL_XI_C9 = 1957.0 / 198450.0


def fd8_symbol(xi: float) -> float:
    """S(xi) with D_h sin(r x)=S(rh) cos(rx)/h."""
    return 2.0 * sum(
        w * math.sin(j * xi) for j, w in FD8_POSITIVE_WEIGHTS.items()
    )


def high_jet_antiderivative(r: float) -> float:
    """Integral of r^7/(1+r^2)."""
    r2 = r * r
    return (
        r**6 / 6.0
        - r**4 / 4.0
        + r2 / 2.0
        - 0.5 * math.log1p(r2)
    )


def high_jet_m9(rmax: float) -> float:
    return high_jet_antiderivative(rmax) - high_jet_antiderivative(1.0)


def i_hi_1_antiderivative(r: float) -> float:
    """Integral of 1/[r(1+r^2)]."""
    return math.log(r) - 0.5 * math.log1p(r * r)


def i_hi_2_antiderivative(r: float) -> float:
    """Integral of 1/[r^2(1+r^2)]."""
    return -1.0 / r - math.atan(r)


def taylor_high_jet_certificate(rmax: float, h: float) -> float:
    return FD8_TAYLOR_C * h**8 * high_jet_m9(rmax)


def direct_analytic_certificate(rmax: float, h: float) -> float:
    """
    Rigorous elementary envelope for the continuum stencil defect.

    Model:
      F_R(x)=int_1^R sin(r x)/[r^2(1+r^2)] dr.

    The exact defect integrand is
      [S(hr)/h-r] cos(rx) / [r^2(1+r^2)].

    For hr<=1:
      |S(hr)/(hr)-1| <= C9 (hr)^8.

    For hr>=1:
      |S(hr)/(hr)-1| <= 1 + A/(hr).

    The resulting bound uses no derivative above first order and is
    uniform in R as R -> infinity.
    """
    if rmax < 1.0:
        raise ValueError("rmax must be >= 1")
    if h <= 0.0:
        raise ValueError("h must be positive")

    split = 1.0 / h
    low_hi = min(rmax, split)

    bound = (
        FD8_SMALL_XI_C9
        * h**8
        * (high_jet_antiderivative(low_hi) - high_jet_antiderivative(1.0))
    )

    if rmax > split:
        bound += (
            i_hi_1_antiderivative(rmax)
            - i_hi_1_antiderivative(split)
        )
        bound += (
            FD8_SYMBOL_ABS
            / h
            * (
                i_hi_2_antiderivative(rmax)
                - i_hi_2_antiderivative(split)
            )
        )

    return bound


def direct_uniform_limit(h: float) -> float:
    """R -> infinity limit of direct_analytic_certificate for 0<h<=1."""
    if not (0.0 < h <= 1.0):
        raise ValueError("closed-form uniform limit is implemented for 0 < h <= 1")

    split = 1.0 / h
    low = (
        FD8_SMALL_XI_C9
        * h**8
        * (high_jet_antiderivative(split) - high_jet_antiderivative(1.0))
    )
    hi1 = -i_hi_1_antiderivative(split)
    hi2 = (
        FD8_SYMBOL_ABS
        / h
        * (-0.5 * math.pi - i_hi_2_antiderivative(split))
    )
    return low + hi1 + hi2


def signed_defect_integrand_amplitude(r: float, h: float) -> float:
    """g(r) such that E_h(F_R)=int_1^R g(r) cos(r x0) dr."""
    return (
        fd8_symbol(h * r) / h - r
    ) / (r * r * (1.0 + r * r))


def actual_defect_reference(
    rmax: float,
    h: float,
    x0: float,
    epsabs: float,
    epsrel: float,
) -> tuple[float, float]:
    """
    High-accuracy numerical reference only, not an interval certificate.

    The rigorous paper claim should rely on direct_analytic_certificate,
    not on this reference value.
    """
    value, err = quad(
        lambda r: signed_defect_integrand_amplitude(r, h),
        1.0,
        rmax,
        weight="cos",
        wvar=x0,
        epsabs=epsabs,
        epsrel=epsrel,
        limit=1000,
    )
    return abs(value), abs(err)


def run_case(
    rmax: float,
    h: float,
    x0: float,
    epsabs: float,
    epsrel: float,
) -> dict:
    taylor = taylor_high_jet_certificate(rmax, h)
    direct = direct_analytic_certificate(rmax, h)
    actual, quad_error = actual_defect_reference(
        rmax, h, x0, epsabs, epsrel
    )

    return {
        "rmax": float(rmax),
        "h": float(h),
        "x0": float(x0),
        "M9_absolute_majorant": float(high_jet_m9(rmax)),
        "taylor_high_jet_certificate": float(taylor),
        "direct_analytic_certificate": float(direct),
        "actual_defect_reference_nonrigorous": float(actual),
        "reference_quad_error_estimate_nonrigorous": float(quad_error),
        "taylor_to_direct_ratio": float(taylor / direct) if direct else math.inf,
        "direct_to_actual_reference_ratio": (
            float(direct / actual) if actual else math.inf
        ),
        "taylor_to_actual_reference_ratio": (
            float(taylor / actual) if actual else math.inf
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "B1 continuum spectral benchmark for high-jet versus direct "
            "stencil-defect certification."
        )
    )
    ap.add_argument("--h", type=float, default=1e-2)
    ap.add_argument("--x0", type=float, default=0.37)
    ap.add_argument(
        "--rmax",
        type=float,
        nargs="*",
        default=[10, 30, 100, 300, 1000, 3000, 10000],
    )
    ap.add_argument("--epsabs", type=float, default=1e-12)
    ap.add_argument("--epsrel", type=float, default=1e-12)
    ap.add_argument("--csv", type=Path, default=None)
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()

    if not (0.0 < args.h <= 1.0):
        raise SystemExit("benchmark currently assumes 0 < h <= 1")
    if any(r < 1.0 for r in args.rmax):
        raise SystemExit("all rmax values must be >= 1")

    rows = [
        run_case(r, args.h, args.x0, args.epsabs, args.epsrel)
        for r in args.rmax
    ]
    uniform = direct_uniform_limit(args.h)

    print(
        "B1_MODEL F_R(x)=int_1^R sin(r x)/[r^2(1+r^2)] dr"
    )
    print(
        "B1_ASYMPTOTICS Taylor~h^8 R^6/3780 -> inf; "
        "direct certificate -> finite cutoff-uniform limit"
    )
    print(f"B1_DIRECT_UNIFORM_LIMIT {uniform:.16e}")
    print(
        "RMAX actual_ref_nonrigorous taylor_high_jet direct_analytic "
        "taylor/direct"
    )
    for row in rows:
        print(
            f'{row["rmax"]:10.1f} '
            f'{row["actual_defect_reference_nonrigorous"]:.6e} '
            f'{row["taylor_high_jet_certificate"]:.6e} '
            f'{row["direct_analytic_certificate"]:.6e} '
            f'{row["taylor_to_direct_ratio"]:.6e}'
        )

    payload = {
        "benchmark": "B1 continuum spectral direct-defect benchmark",
        "model": "F_R(x)=integral_1^R sin(r x)/[r^2(1+r^2)] dr",
        "stencil": "9-point centered FD8 first derivative",
        "rigorous_objects": {
            "M9_absolute_majorant": "closed form integral of r^7/(1+r^2)",
            "taylor_high_jet_certificate": "h^8 M9 / 630",
            "direct_analytic_certificate": (
                "closed-form piecewise envelope using the FD8 symbol; uniform in R"
            ),
            "direct_uniform_limit": float(uniform),
        },
        "nonrigorous_diagnostic_only": (
            "actual_defect_reference_nonrigorous uses scipy QUADPACK and is "
            "reported only for effectivity diagnostics"
        ),
        "rows": rows,
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
