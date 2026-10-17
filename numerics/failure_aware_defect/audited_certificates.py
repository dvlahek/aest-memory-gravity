#!/usr/bin/env python3
from __future__ import annotations

import math
from fractions import Fraction

from scipy.optimize import brentq

from stable_tail_integrals import (
    integral_inv_1pr2,
    integral_inv_r_1pr2,
    integral_inv_r2_1pr2,
)

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
FD8_POSITIVE_WEIGHTS = {j: FD8_WEIGHTS[j] for j in range(1, 5)}
FD8_TAYLOR_C = 1.0 / 630.0
FD8_L1 = sum(abs(w) for w in FD8_WEIGHTS.values())
FD8_SYMBOL_ABS = 2.0 * sum(abs(FD8_WEIGHTS[j]) for j in range(1, 5))
FD8_SMALL_XI_C9 = 1957.0 / 198450.0
TAIL_WEIGHTED_EXP_L1 = sum(
    abs(w) * math.exp(-(4 + j)) for j, w in FD8_WEIGHTS.items()
)
TARGET_EXP_TAIL = math.exp(-4.0)


def fd8_exact_moments() -> dict[int, Fraction]:
    w = {
        -4: Fraction(1, 280),
        -3: -Fraction(4, 105),
        -2: Fraction(1, 5),
        -1: -Fraction(4, 5),
        0: Fraction(0),
        1: Fraction(4, 5),
        2: -Fraction(1, 5),
        3: Fraction(4, 105),
        4: -Fraction(1, 280),
    }
    return {p: sum(w[j] * (j**p) for j in w) for p in range(10)}


def b1_m7_antiderivative(r: float) -> float:
    r2 = r * r
    return r**6 / 6.0 - r**4 / 4.0 + r2 / 2.0 - 0.5 * math.log1p(r2)


def b2_m8_antiderivative(r: float) -> float:
    return r**7 / 7.0 - r**5 / 5.0 + r**3 / 3.0 - r + math.atan(r)


def b1_taylor(R: float, h: float) -> float:
    return FD8_TAYLOR_C * h**8 * (b1_m7_antiderivative(R) - b1_m7_antiderivative(1.0))


def b1_direct(R: float, h: float) -> float:
    split = 1.0 / h
    low_hi = min(R, split)
    out = FD8_SMALL_XI_C9 * h**8 * (
        b1_m7_antiderivative(low_hi) - b1_m7_antiderivative(1.0)
    )
    if R > split:
        out += integral_inv_r_1pr2(split, R)
        out += FD8_SYMBOL_ABS / h * integral_inv_r2_1pr2(split, R)
    return out


def b1_direct_limit(h: float) -> float:
    split = 1.0 / h
    return (
        FD8_SMALL_XI_C9 * h**8 * (b1_m7_antiderivative(split) - b1_m7_antiderivative(1.0))
        + integral_inv_r_1pr2(split)
        + FD8_SYMBOL_ABS / h * integral_inv_r2_1pr2(split)
    )


def b2_taylor(R: float, h: float) -> float:
    return FD8_TAYLOR_C * h**8 * (b2_m8_antiderivative(R) - b2_m8_antiderivative(1.0))


def b2_direct(R: float, h: float) -> float:
    split = 1.0 / h
    low_hi = min(R, split)
    out = FD8_TAYLOR_C * h**8 * (
        b2_m8_antiderivative(low_hi) - b2_m8_antiderivative(1.0)
    )
    if R > split:
        out += TAIL_WEIGHTED_EXP_L1 / h * integral_inv_r_1pr2(split, R)
        out += TARGET_EXP_TAIL * integral_inv_1pr2(split, R)
    return out


def b2_direct_limit(h: float) -> float:
    split = 1.0 / h
    return (
        FD8_TAYLOR_C * h**8 * (b2_m8_antiderivative(split) - b2_m8_antiderivative(1.0))
        + TAIL_WEIGHTED_EXP_L1 / h * integral_inv_r_1pr2(split)
        + TARGET_EXP_TAIL * integral_inv_1pr2(split)
    )


def b3_taylor(R: float, h: float) -> float:
    return FD8_TAYLOR_C * h**8 * (b1_m7_antiderivative(R) - b1_m7_antiderivative(1.0))


def b3_direct(R: float, h: float) -> float:
    split = 1.0 / h
    low_hi = min(R, split)
    out = FD8_TAYLOR_C * h**8 * (
        b1_m7_antiderivative(low_hi) - b1_m7_antiderivative(1.0)
    )
    if R > split:
        out += TAIL_WEIGHTED_EXP_L1 / h * integral_inv_r2_1pr2(split, R)
        out += TARGET_EXP_TAIL * integral_inv_r_1pr2(split, R)
    return out


def b3_direct_limit(h: float) -> float:
    split = 1.0 / h
    return (
        FD8_TAYLOR_C * h**8 * (b1_m7_antiderivative(split) - b1_m7_antiderivative(1.0))
        + TAIL_WEIGHTED_EXP_L1 / h * integral_inv_r2_1pr2(split)
        + TARGET_EXP_TAIL * integral_inv_r_1pr2(split)
    )


def b1_asym_taylor(rho: float) -> float:
    return rho**6 / 3780.0


def b1_asym_direct(rho: float) -> float:
    return (
        FD8_SMALL_XI_C9 / 6.0
        + 0.5 * (1.0 - rho**-2)
        + FD8_SYMBOL_ABS / 3.0 * (1.0 - rho**-3)
    )


def b2_asym_taylor(rho: float) -> float:
    return rho**7 / 4410.0


def b2_asym_direct(rho: float) -> float:
    return (
        1.0 / 4410.0
        + TAIL_WEIGHTED_EXP_L1 / 2.0 * (1.0 - rho**-2)
        + TARGET_EXP_TAIL * (1.0 - rho**-1)
    )


def b3_asym_taylor(rho: float) -> float:
    return rho**6 / 3780.0


def b3_asym_direct(rho: float) -> float:
    return (
        1.0 / 3780.0
        + TAIL_WEIGHTED_EXP_L1 / 3.0 * (1.0 - rho**-3)
        + TARGET_EXP_TAIL / 2.0 * (1.0 - rho**-2)
    )


def asymptotic_rho_star(which: str) -> float:
    pairs = {
        "b1": (b1_asym_taylor, b1_asym_direct),
        "b2": (b2_asym_taylor, b2_asym_direct),
        "b3": (b3_asym_taylor, b3_asym_direct),
    }
    bt, bd = pairs[which.lower()]
    return brentq(lambda q: bt(q) - bd(q), 1.0 + 1e-8, 10.0, rtol=1e-14)


def finite_crossover(which: str, h: float) -> float:
    pairs = {
        "b1": (b1_taylor, b1_direct),
        "b2": (b2_taylor, b2_direct),
        "b3": (b3_taylor, b3_direct),
    }
    bt, bd = pairs[which.lower()]
    split = 1.0 / h
    # Stay away from the exact equality on the fully resolved band.
    probes = [split * (1.0 + x) for x in (1e-5, 1e-4, 1e-3, 1e-2, 5e-2, 1e-1)]
    lo = None
    for p in probes:
        if bt(p, h) - bd(p, h) < 0.0:
            lo = p
            break
    if lo is None:
        raise RuntimeError("failed to locate negative post-split branch")
    hi = max(2.0 * lo, 2.0 * split)
    while bt(hi, h) - bd(hi, h) <= 0.0:
        hi *= 2.0
    return brentq(lambda R: bt(R, h) - bd(R, h), lo, hi, rtol=1e-13)
