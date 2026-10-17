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
    # Integral_r^infinity ds/[s^2(1+s^2)].
    x = 1.0 / r
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
