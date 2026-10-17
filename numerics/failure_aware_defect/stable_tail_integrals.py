#!/usr/bin/env python3
from __future__ import annotations

import math


def _check(a: float, b: float | None) -> None:
    if not (math.isfinite(a) and a > 0.0):
        raise ValueError("a must be finite and positive")
    if b is not None:
        if not (math.isfinite(b) and b >= a):
            raise ValueError("b must be finite and satisfy b >= a")


def integral_inv_r_1pr2(a: float, b: float | None = None) -> float:
    """Stable integral of 1/[r(1+r^2)] from a to b, or a to infinity."""
    _check(a, b)
    ta = 0.5 * math.log1p(1.0 / (a * a))
    if b is None:
        return ta
    tb = 0.5 * math.log1p(1.0 / (b * b))
    return ta - tb


def _j2_tail(r: float) -> float:
    """Integral from r to infinity of 1/[s^2(1+s^2)], evaluated stably."""
    x = 1.0 / r
    # x - atan(x) loses all relative accuracy when x is tiny.
    # Use its alternating Taylor series in that regime.
    if abs(x) < 1e-3:
        x2 = x * x
        return x**3 * (
            1.0 / 3.0
            - x2 / 5.0
            + x2 * x2 / 7.0
            - x2 * x2 * x2 / 9.0
            + x2**4 / 11.0
        )
    return x - math.atan(x)


def integral_inv_r2_1pr2(a: float, b: float | None = None) -> float:
    """Stable integral of 1/[r^2(1+r^2)] from a to b, or a to infinity."""
    _check(a, b)
    ta = _j2_tail(a)
    if b is None:
        return ta
    return ta - _j2_tail(b)


def integral_inv_1pr2(a: float, b: float | None = None) -> float:
    """Stable integral of 1/(1+r^2) from a to b, or a to infinity."""
    _check(a, b)
    ta = math.atan(1.0 / a)
    if b is None:
        return ta
    return ta - math.atan(1.0 / b)
