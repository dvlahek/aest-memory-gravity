#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import mpmath as mp

FD8_OFFSETS = (-4, -3, -2, -1, 0, 1, 2, 3, 4)
FD8_WEIGHTS = (
    mp.mpf(1) / 280,
    -mp.mpf(4) / 105,
    mp.mpf(1) / 5,
    -mp.mpf(4) / 5,
    mp.mpf(0),
    mp.mpf(4) / 5,
    -mp.mpf(1) / 5,
    mp.mpf(4) / 105,
    -mp.mpf(1) / 280,
)
FD8_TAYLOR_C = mp.mpf(1) / 630
FD8_L1 = mp.fsum(abs(w) for w in FD8_WEIGHTS)


def fd8_symbol(xi: mp.mpf) -> mp.mpf:
    """Real modified-wavenumber numerator S(xi) for D_h sin(k x)."""
    return mp.fsum(
        w * mp.sin(mp.mpf(j) * xi)
        for j, w in zip(FD8_OFFSETS, FD8_WEIGHTS)
    )


def run_case(kappa: float, h: float, x0: float, beta: float) -> dict:
    k = mp.mpf(kappa)
    hh = mp.mpf(h)
    xx = mp.mpf(x0)
    bb = mp.mpf(beta)

    amp = k ** (-bb)
    xi = k * hh
    symbol = fd8_symbol(xi)

    exact_derivative = k ** (1 - bb) * mp.cos(k * xx)
    fd8_derivative = amp * symbol * mp.cos(k * xx) / hh
    actual_defect = abs(fd8_derivative - exact_derivative)

    # Standard 9-point centered FD8 remainder form:
    # |D_h f - f'| <= h^8 ||f^(9)||_inf / 630.
    taylor_certificate = FD8_TAYLOR_C * hh**8 * k ** (9 - bb)

    # Elementary direct certificate:
    # |D_h f - f'| <= |D_h f| + |f'|
    #                <= ||w||_1 h^-1 k^-beta + k^(1-beta).
    direct_certificate = FD8_L1 / hh * k ** (-bb) + k ** (1 - bb)

    return {
        "kappa": float(k),
        "h": float(hh),
        "x0": float(xx),
        "beta": float(bb),
        "fd8_l1": float(FD8_L1),
        "exact_derivative": float(exact_derivative),
        "fd8_derivative": float(fd8_derivative),
        "actual_defect": float(actual_defect),
        "taylor_high_jet_certificate": float(taylor_certificate),
        "direct_elementary_certificate": float(direct_certificate),
        "taylor_to_direct_ratio": float(taylor_certificate / direct_certificate),
        "taylor_to_actual_ratio": (
            float(taylor_certificate / actual_defect)
            if actual_defect != 0
            else math.inf
        ),
        "direct_to_actual_ratio": (
            float(direct_certificate / actual_defect)
            if actual_defect != 0
            else math.inf
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "B0 analytical separation witness for failure-aware defect certification."
        )
    )
    ap.add_argument("--h", type=float, default=1e-2)
    ap.add_argument("--x0", type=float, default=0.37)
    ap.add_argument("--beta", type=float, default=2.0)
    ap.add_argument("--dps", type=int, default=80)
    ap.add_argument(
        "--kappa",
        type=float,
        nargs="*",
        default=[10, 30, 100, 300, 1000, 3000, 10000],
    )
    ap.add_argument("--csv", type=Path, default=None)
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()

    if not (1.0 < args.beta < 9.0):
        raise SystemExit("B0 separation theorem requires 1 < beta < 9.")
    if args.h <= 0:
        raise SystemExit("h must be positive.")
    if any(k <= 0 for k in args.kappa):
        raise SystemExit("all kappa values must be positive.")

    mp.mp.dps = args.dps
    rows = [run_case(k, args.h, args.x0, args.beta) for k in args.kappa]

    print(
        "B0_THEOREM_REGIME "
        f"beta={args.beta:g} "
        "T_kappa~kappa^(9-beta)->inf "
        "D_kappa<=||w||_1 h^-1 kappa^-beta+kappa^(1-beta)->0"
    )
    print(
        "KAPPA actual_defect taylor_high_jet direct_elementary "
        "taylor/direct"
    )
    for row in rows:
        print(
            f'{row["kappa"]:10.1f} '
            f'{row["actual_defect"]:.6e} '
            f'{row["taylor_high_jet_certificate"]:.6e} '
            f'{row["direct_elementary_certificate"]:.6e} '
            f'{row["taylor_to_direct_ratio"]:.6e}'
        )

    payload = {
        "benchmark": "B0 analytical stiffness-separation witness",
        "family": "f_kappa(x)=kappa^(-beta) sin(kappa x)",
        "stencil": "9-point centered FD8 first derivative",
        "theorem_regime": "1 < beta < 9",
        "asymptotics": {
            "high_jet_certificate": "O(h^8 kappa^(9-beta)) -> infinity",
            "direct_certificate": (
                "O(h^-1 kappa^-beta + kappa^(1-beta)) -> 0"
            ),
            "consequence": (
                "a formally valid high-order derivative certificate can become "
                "arbitrarily non-informative while a direct defect certificate shrinks"
            ),
        },
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
