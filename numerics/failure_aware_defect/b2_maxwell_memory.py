#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from scipy.integrate import quad
from scipy.optimize import brentq

FD8_WEIGHTS = {
    -4: 1.0 / 280.0,
    -3: -4.0 / 105.0,
    -2: 1.0 / 5.0,
    -1: -4.0 / 5.0,
    0: 0.0,
    1: 4.0 / 5.0,
    2: -1.0 / 5.0,
    3: 4.0 / 105.0,
    4: -1.0 / 280.0,
}
FD8_TAYLOR_C = 1.0 / 630.0
FD8_L1 = sum(abs(w) for w in FD8_WEIGHTS.values())

# For x=h r>=1 and target t0=4h, the constant 1/r contribution to
# q((4+j)h,r) cancels because the derivative-stencil weights sum to zero.
# The remaining exponentials satisfy exp(-(4+j)x)<=exp(-(4+j)).
TAIL_WEIGHTED_EXP_L1 = sum(
    abs(w) * math.exp(-(4 + j)) for j, w in FD8_WEIGHTS.items()
)
TARGET_EXP_TAIL = math.exp(-4.0)


def maxwell_mode(t: float, r: float) -> float:
    """Ramp-driven Maxwell mode q_t + r q = 1, q(0,r)=0."""
    return -math.expm1(-r * t) / r


def m8_antiderivative(r: float) -> float:
    """Integral of r^8/(1+r^2)."""
    return (
        r**7 / 7.0
        - r**5 / 5.0
        + r**3 / 3.0
        - r
        + math.atan(r)
    )


def m8_majorant(rmax: float) -> float:
    return m8_antiderivative(rmax) - m8_antiderivative(1.0)


def i1_antiderivative(r: float) -> float:
    """Integral of 1/[r(1+r^2)]."""
    return math.log(r) - 0.5 * math.log1p(r * r)


def taylor_high_jet_certificate(rmax: float, h: float) -> float:
    """
    Global FD8 Taylor certificate on the stencil interval [0,8h].

    q^(9)(t,r)=r^8 exp(-rt), so the interval supremum is r^8 because
    the stencil touches t=0.
    """
    return FD8_TAYLOR_C * h**8 * m8_majorant(rmax)


def direct_split_certificate(rmax: float, h: float) -> float:
    """
    Failure-aware resolved/unresolved Maxwell certificate.

    Resolved band r<=1/h:
      use the conventional FD8 remainder locally.

    Unresolved band r>=1/h:
      certify the actual stencil values and the exact first derivative:
        |D_h q - q_t(4h,r)| <= A_tail/(h r) + exp(-4),
      where A_tail=sum |w_j| exp(-(4+j)).

    After multiplication by the continuum weight 1/(1+r^2), both
    unresolved-tail integrals converge as rmax -> infinity.
    """
    if rmax < 1.0:
        raise ValueError("rmax must be >= 1")
    if not (0.0 < h <= 1.0):
        raise ValueError("benchmark assumes 0 < h <= 1")

    split = 1.0 / h
    low_hi = min(rmax, split)

    bound = (
        FD8_TAYLOR_C
        * h**8
        * (m8_antiderivative(low_hi) - m8_antiderivative(1.0))
    )

    if rmax > split:
        bound += (
            TAIL_WEIGHTED_EXP_L1
            / h
            * (i1_antiderivative(rmax) - i1_antiderivative(split))
        )
        bound += TARGET_EXP_TAIL * (
            math.atan(rmax) - math.atan(split)
        )

    return bound


def direct_uniform_limit(h: float) -> float:
    """R -> infinity limit of the direct split certificate."""
    if not (0.0 < h <= 1.0):
        raise ValueError("benchmark assumes 0 < h <= 1")

    split = 1.0 / h
    low = (
        FD8_TAYLOR_C
        * h**8
        * (m8_antiderivative(split) - m8_antiderivative(1.0))
    )
    tail_1 = TAIL_WEIGHTED_EXP_L1 / h * (-i1_antiderivative(split))
    tail_2 = TARGET_EXP_TAIL * (0.5 * math.pi - math.atan(split))
    return low + tail_1 + tail_2


def asymptotic_direct_scaled(rho: float) -> float:
    """
    h -> 0 with R=rho/h, rho>1:
      B_D/h -> 1/4410
               + A_tail/2 (1-rho^-2)
               + exp(-4) (1-rho^-1).
    """
    return (
        1.0 / 4410.0
        + 0.5 * TAIL_WEIGHTED_EXP_L1 * (1.0 - rho**-2)
        + TARGET_EXP_TAIL * (1.0 - rho**-1)
    )


def asymptotic_taylor_scaled(rho: float) -> float:
    """h -> 0 with R=rho/h: B_T/h -> rho^7/4410."""
    return rho**7 / 4410.0


def asymptotic_rho_star() -> float:
    return brentq(
        lambda rho: asymptotic_taylor_scaled(rho)
        - asymptotic_direct_scaled(rho),
        1.0 + 1e-10,
        10.0,
        xtol=1e-14,
        rtol=1e-14,
    )


def finite_h_crossover(h: float) -> float:
    """Nontrivial crossover above the resolved-band equality R=1/h."""
    split = 1.0 / h
    lo = split * (1.0 + 1e-8)
    hi = split * 100.0

    def f(r: float) -> float:
        return taylor_high_jet_certificate(r, h) - direct_split_certificate(r, h)

    if f(lo) >= 0.0:
        raise RuntimeError("unexpected post-split sign at lower bracket")
    if f(hi) <= 0.0:
        raise RuntimeError("failed to bracket Maxwell route crossover")

    return brentq(f, lo, hi, xtol=1e-12, rtol=1e-12)


def defect_mode(r: float, h: float) -> float:
    """
    Exact per-mode FD8 defect at t0=4h.

    Used only for a nonrigorous high-accuracy diagnostic reference.
    """
    d_h = sum(
        w * maxwell_mode((4 + j) * h, r)
        for j, w in FD8_WEIGHTS.items()
    ) / h
    exact = math.exp(-4.0 * h * r)
    return d_h - exact


def actual_defect_reference(
    rmax: float,
    h: float,
    epsabs: float,
    epsrel: float,
) -> tuple[float, float]:
    value, err = quad(
        lambda r: defect_mode(r, h) / (1.0 + r * r),
        1.0,
        rmax,
        epsabs=epsabs,
        epsrel=epsrel,
        limit=1000,
    )
    return abs(value), abs(err)


def preferred_route(taylor: float, direct: float) -> str:
    if math.isclose(taylor, direct, rel_tol=1e-13, abs_tol=0.0):
        return "equal_resolved"
    return "high_jet" if taylor < direct else "direct"


def run_case(
    rmax: float,
    h: float,
    epsabs: float,
    epsrel: float,
) -> dict:
    taylor = taylor_high_jet_certificate(rmax, h)
    direct = direct_split_certificate(rmax, h)
    actual, quad_err = actual_defect_reference(rmax, h, epsabs, epsrel)

    return {
        "rmax": float(rmax),
        "h": float(h),
        "rho_hR": float(h * rmax),
        "M8_global_absolute_majorant": float(m8_majorant(rmax)),
        "taylor_high_jet_certificate": float(taylor),
        "direct_split_certificate": float(direct),
        "gamma_taylor_over_direct": (
            float(taylor / direct) if direct else math.inf
        ),
        "preferred_certificate": preferred_route(taylor, direct),
        "actual_defect_reference_nonrigorous": float(actual),
        "reference_quad_error_estimate_nonrigorous": float(quad_err),
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
            "B2 generalized-Maxwell continuum-memory benchmark for "
            "failure-aware high-jet versus direct-tail certification."
        )
    )
    ap.add_argument("--h", type=float, default=1e-2)
    ap.add_argument(
        "--rmax",
        type=float,
        nargs="*",
        default=[10, 30, 100, 200, 300, 1000, 3000, 10000],
    )
    ap.add_argument("--epsabs", type=float, default=1e-12)
    ap.add_argument("--epsrel", type=float, default=1e-12)
    ap.add_argument("--csv", type=Path, default=None)
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()

    if not (0.0 < args.h <= 1.0):
        raise SystemExit("benchmark assumes 0 < h <= 1")
    if any(r < 1.0 for r in args.rmax):
        raise SystemExit("all rmax values must be >= 1")

    rows = [
        run_case(r, args.h, args.epsabs, args.epsrel)
        for r in args.rmax
    ]

    rho_star = asymptotic_rho_star()
    r_cross = finite_h_crossover(args.h)
    cert_cross = taylor_high_jet_certificate(r_cross, args.h)

    payload = {
        "benchmark": "B2 generalized Maxwell ramp-memory benchmark",
        "model": {
            "mode_equation": "q_t + r q = 1, q(0,r)=0",
            "mode_solution": "q(t,r)=(1-exp(-rt))/r",
            "continuum_memory": "M_R(t)=integral_1^R q(t,r)/(1+r^2) dr",
            "target": "t0=4h with FD8 stencil nodes [0,8h]",
        },
        "rigorous_objects": {
            "global_high_jet_certificate": (
                "h^8/630 * integral_1^R r^8/(1+r^2) dr"
            ),
            "direct_split_certificate": (
                "resolved r<=1/h high-jet remainder plus unresolved-tail "
                "source-value/first-derivative enclosure"
            ),
            "direct_uniform_limit": float(direct_uniform_limit(args.h)),
            "unresolved_tail_weighted_exp_l1": float(TAIL_WEIGHTED_EXP_L1),
        },
        "asymptotic_theory": {
            "rho": "rho=hR",
            "taylor_scaled_limit": "B_T(rho/h;h)/h -> rho^7/4410",
            "direct_scaled_limit": (
                "B_D(rho/h;h)/h -> 1/4410 + "
                "A_tail/2(1-rho^-2) + exp(-4)(1-rho^-1)"
            ),
            "rho_star": float(rho_star),
            "crossover_law": "R_cross(h) ~ rho_star/h",
            "certificate_at_crossover_scaled_limit": float(
                asymptotic_taylor_scaled(rho_star)
            ),
        },
        "finite_h_crossover": {
            "h": float(args.h),
            "R_cross": float(r_cross),
            "rho_cross_hR": float(args.h * r_cross),
            "certificate_at_crossover": float(cert_cross),
            "certificate_at_crossover_over_h": float(cert_cross / args.h),
        },
        "claim_boundary": (
            "Rigorous claims use only the closed-form high-jet and direct-split "
            "certificates. QUADPACK actual-defect values are diagnostics only. "
            "The unresolved-tail direct route uses mode values and the first "
            "derivative; it does not require a global ninth-derivative "
            "majorant over the unresolved relaxation spectrum."
        ),
        "nonrigorous_diagnostic_only": (
            "actual_defect_reference_nonrigorous uses scipy QUADPACK"
        ),
        "rows": rows,
    }

    print("B2_MODEL generalized Maxwell ramp memory")
    print("B2_MODE q_t+r q=1, q(0,r)=0")
    print(
        "B2_MEMORY M_R(t)=int_1^R q(t,r)/(1+r^2) dr; target t0=4h"
    )
    print(
        "B2_ASYMPTOTICS Taylor~h^8 R^7/4410 -> inf; "
        "direct split -> finite cutoff-uniform limit"
    )
    print(f"B2_TAIL_WEIGHTED_EXP_L1 {TAIL_WEIGHTED_EXP_L1:.16e}")
    print(f"B2_DIRECT_UNIFORM_LIMIT {direct_uniform_limit(args.h):.16e}")
    print(f"B2_RHO_STAR {rho_star:.16e}")
    print(f"B2_R_CROSS {r_cross:.16e}")
    print(f"B2_HR_CROSS {args.h*r_cross:.16e}")
    print(
        "RMAX actual_ref_nonrigorous taylor_high_jet direct_split "
        "taylor/direct preferred"
    )
    for row in rows:
        print(
            f'{row["rmax"]:10.1f} '
            f'{row["actual_defect_reference_nonrigorous"]:.6e} '
            f'{row["taylor_high_jet_certificate"]:.6e} '
            f'{row["direct_split_certificate"]:.6e} '
            f'{row["gamma_taylor_over_direct"]:.6e} '
            f'{row["preferred_certificate"]}'
        )

    if args.csv is not None:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0]))
            wr.writeheader()
            wr.writerows(rows)
        print("WROTE", args.csv)

    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n"
        )
        print("WROTE", args.json)


if __name__ == "__main__":
    main()
