#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.signal import fftconvolve

from memory_gravity import mcmg_r1_causal_first_moment as base

QUADRATURE_REPAIR_PARENT = "b03aa592615fefeca1d29978c52595558b65482c"
QUADRATURE_METHOD = "cell_integrated_kernel_weights"


def kernel_cdf(kind: str, s, u: float):
    x = np.maximum(np.asarray(s, float), 0.0)
    if kind == "exp":
        return 1.0 - np.exp(-x / u)
    if kind == "gamma2":
        q = 2.0 * x / u
        return 1.0 - np.exp(-q) * (1.0 + q)
    if kind == "gamma4":
        q = 4.0 * x / u
        return 1.0 - np.exp(-q) * (1.0 + q + 0.5 * q * q + q ** 3 / 6.0)
    if kind == "tophat":
        return np.clip(x / (2.0 * u), 0.0, 1.0)
    raise KeyError(kind)


def repaired_causal_memory(source, dx, kind, u):
    src = np.asarray(source, float)
    j = np.arange(src.size, dtype=float)
    lo = np.maximum(0.0, (j - 0.5) * dx)
    hi = (j + 0.5) * dx
    # Integrate the kernel exactly across each lag cell. This avoids the
    # O(dx/u) normalization bias of point-sampled left-Riemann weights.
    weights = kernel_cdf(kind, hi, u) - kernel_cdf(kind, lo, u)
    dev = src - src[0]
    conv = fftconvolve(dev, weights, mode="full")[: src.size]
    return src[0] + conv


def json_out_from_argv():
    args = sys.argv[1:]
    if "--json-out" in args:
        i = args.index("--json-out")
        if i + 1 < len(args):
            return Path(args[i + 1])
    return Path("results/mcmg_r1_causal_first_moment.json")


def main():
    base.causal_memory_fft = repaired_causal_memory
    rc = int(base.main())
    p = json_out_from_argv()
    if p.exists():
        obj = json.loads(p.read_text())
        obj["numerical_quadrature_repair"] = {
            "method": QUADRATURE_METHOD,
            "parent_implementation_commit": QUADRATURE_REPAIR_PARENT,
            "science_grid_changed": False,
            "kernels_changed": False,
            "u_values_changed": False,
            "gates_or_thresholds_changed": False,
        }
        p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
