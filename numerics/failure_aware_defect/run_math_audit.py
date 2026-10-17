#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

import audited_certificates as ac


def main() -> None:
    ap = argparse.ArgumentParser(description="Recompute audited B1-B3 transition constants with stable tail formulas.")
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()

    hs = np.asarray([0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001], dtype=float)
    scale_power = {"b1": 2, "b2": 1, "b3": 2}
    asym_taylor = {"b1": ac.b1_asym_taylor, "b2": ac.b2_asym_taylor, "b3": ac.b3_asym_taylor}
    direct_limit = {"b1": ac.b1_direct_limit, "b2": ac.b2_direct_limit, "b3": ac.b3_direct_limit}

    payload = {
        "audit": "independent stable-evaluation audit for B1-B3 certificate transitions",
        "fd8": {
            "l1": ac.FD8_L1,
            "symbol_abs": ac.FD8_SYMBOL_ABS,
            "small_xi_C9": ac.FD8_SMALL_XI_C9,
            "tail_weighted_exp_l1": ac.TAIL_WEIGHTED_EXP_L1,
            "moments": {str(k): str(v) for k, v in ac.fd8_exact_moments().items()},
        },
        "benchmarks": {},
    }

    for key in ("b1", "b2", "b3"):
        rho_star = ac.asymptotic_rho_star(key)
        cross = []
        for h in hs:
            R = ac.finite_crossover(key, float(h))
            cross.append({"h": float(h), "R_cross": float(R), "rho_cross_hR": float(h * R)})

        log_h = np.log(hs)
        log_R = np.log(np.asarray([x["R_cross"] for x in cross]))
        slope, intercept = np.polyfit(log_h, log_R, 1)
        p = scale_power[key]
        amplitude = asym_taylor[key](rho_star)

        payload["benchmarks"][key] = {
            "rho_star": float(rho_star),
            "R_cross_law": "R_cross ~ rho_star/h",
            "crossover_certificate_power_h": p,
            "crossover_scaled_amplitude": float(amplitude),
            "finite_h_crossovers": cross,
            "loglog_fit": {"slope": float(slope), "prefactor": float(math.exp(intercept))},
            "direct_uniform_limit_h_0p01": float(direct_limit[key](0.01)),
        }

    print("MATH_AUDIT_FD8_MOMENT9", payload["fd8"]["moments"]["9"])
    for key, q in payload["benchmarks"].items():
        print(
            key.upper(),
            "rho_star", f'{q["rho_star"]:.16e}',
            "fit", f'{q["loglog_fit"]["prefactor"]:.16e}',
            f'h^({q["loglog_fit"]["slope"]:.16e})',
        )
        print("  h=1e-3 rho_cross", f'{q["finite_h_crossovers"][-1]["rho_cross_hR"]:.16e}')

    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print("WROTE", args.json)


if __name__ == "__main__":
    main()
