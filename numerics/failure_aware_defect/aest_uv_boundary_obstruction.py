#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7
from ge19 import repair27_cancellation_free_parent_q20_reconstruction as r27
from nl1c4 import expanding_memory_source_trajectory as c4

A_TARGET = 0.4
TAUH0 = 10.0
MODE = 20


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def find_trace(results_dirs: list[Path]) -> Path:
    target_bytes = int(r27.REPAIR26_R1_TRACE_BYTES)
    target_sha = str(r27.REPAIR26_R1_TRACE_SHA)
    for rd in results_dirs:
        if not rd.exists():
            continue
        for p in rd.rglob("ge19_repair26_R1_full_history_trace.dat"):
            if p.is_file() and p.stat().st_size == target_bytes and sha256(p) == target_sha:
                return p
        for p in rd.rglob("*repair26*trace*.dat"):
            if p.is_file() and p.stat().st_size == target_bytes and sha256(p) == target_sha:
                return p
    raise RuntimeError("FROZEN_REPAIR26_TRACE_NOT_FOUND")


def complex_payload(z: complex) -> dict:
    return {"real": float(z.real), "imag": float(z.imag), "abs": float(abs(z))}


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "Audit the earliest frozen AeST bath boundary for the continuum-UV "
            "absolute-envelope obstruction."
        )
    )
    ap.add_argument("--trace", type=Path, default=None)
    ap.add_argument("--results-dir", type=Path, action="append", default=None)
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()

    results_dirs = list(args.results_dir or [])
    results_dirs.extend([ROOT / "results", Path.home() / "aest-memory-gravity" / "results"])
    # Preserve order while removing duplicates.
    seen = set()
    results_dirs = [p for p in results_dirs if not (str(p.resolve()) in seen or seen.add(str(p.resolve())))]

    trace = args.trace.resolve() if args.trace is not None else find_trace(results_dirs)
    rows = c4.read_trace(trace)
    histories, kmiss, tmiss = c4.select_and_align(rows)
    amps, _, _ = r7.amplitudes()

    modes = list(map(int, r7.FOURIER_N))
    per_mode = []
    for im, hist in enumerate(histories):
        if len(hist) < 2:
            raise RuntimeError("history too short")
        a0 = float(hist[0]["a"])
        a1 = float(hist[1]["a"])
        if not (a0 > 0.0 and a1 > a0):
            raise RuntimeError("unexpected initial scale-factor ordering")

        N0 = math.log(a0)
        N1 = math.log(a1)
        h0 = float(hist[0]["H_over_H0"]) * TAUH0
        h1 = float(hist[1]["H_over_H0"]) * TAUH0
        hm = math.sqrt(h0 * h1)
        dxi = (N1 - N0) / hm

        x0 = float(hist[0]["chi"] / hist[0]["a"])
        x1 = float(hist[1]["chi"] / hist[1]["a"])
        xs0_piecewise = (x1 - x0) / dxi

        k = float(r7.g9.K_REQ[im])
        fac0 = 0.5 * float(amps[im]) * np.exp(1j * float(r7.PHASES[im]))
        gradfac = complex(fac0 * (1j * k))
        X0 = gradfac * x0
        Xs0 = gradfac * xs0_piecewise

        # Large-r homogeneous displacement mismatch produces
        # |u_s| ~ r |X0| exp[-3/2 int h ds].  With ds=dN/h on the
        # frozen interval convention, the leading damping from a0 to
        # A_TARGET is (a0/A_TARGET)^(3/2).
        damping_to_target = (a0 / A_TARGET) ** 1.5
        leading_us_over_r_amplitude = abs(X0) * damping_to_target

        per_mode.append(
            {
                "fourier_mode": int(r7.FOURIER_N[im]),
                "k_req": k,
                "history_a0": a0,
                "history_a1": a1,
                "trace_x0_chi_over_a": x0,
                "trace_first_interval_xs": xs0_piecewise,
                "X0": complex_payload(X0),
                "Xs0_piecewise": complex_payload(Xs0),
                "large_r_homogeneous_damping_to_a0p4": damping_to_target,
                "leading_abs_us_over_r_amplitude_at_a0p4": leading_us_over_r_amplitude,
                "position_mismatch_obstruction_present": bool(abs(X0) > 0.0),
            }
        )

    target = per_mode[modes.index(MODE)]
    obstruction = bool(target["position_mismatch_obstruction_present"])

    report = {
        "classification": (
            "AEST_UV_ABSOLUTE_ENVELOPE_POSITION_MISMATCH_OBSTRUCTION_PRESENT"
            if obstruction
            else "AEST_UV_NO_POSITION_MISMATCH_OBSTRUCTION_FROM_EARLIEST_BOUNDARY"
        ),
        "scope": "frozen Repair26 full-history trace; earliest bath boundary only",
        "trace": str(trace),
        "trace_sha256": sha256(trace),
        "k_relative_miss": float(kmiss),
        "common_time_mismatch": float(tmiss),
        "bath_initial_condition": "z(s0,r)=0, v(s0,r)=0 for every Drude mode",
        "regularized_variables": {
            "u": "z-X",
            "u_s": "v-X_s",
            "q": "u_s/r^2",
        },
        "continuum_measure": "dmu(r)=2 dr/[pi(1+r^2)]",
        "criterion": (
            "If X(s0) != 0, then the large-r homogeneous component generically has "
            "|u_s|=O(r |X(s0)|) up to r-independent damping. Its absolute Drude tail "
            "scales as integral dr/r and is not L1. If X(s0)=0, this specific O(r) "
            "obstruction is absent; the velocity mismatch is O(1) and is L1 under dmu."
        ),
        "target_mode": MODE,
        "target_mode_result": target,
        "per_mode": per_mode,
        "claim_boundary": (
            "This diagnostic tests only the earliest-boundary obstruction. It does not "
            "by itself certify the forced UV remainder, a signed oscillatory transient, "
            "B10_x, GE06/GE07, or the full AeST continuum problem."
        ),
    }

    print("AEST_UV_BOUNDARY_CLASSIFICATION", report["classification"])
    print("TARGET_MODE", MODE)
    print("A0", f"{target['history_a0']:.17e}")
    print("TRACE_X0", f"{target['trace_x0_chi_over_a']:.17e}")
    print("ABS_X0", f"{target['X0']['abs']:.17e}")
    print("ABS_XS0", f"{target['Xs0_piecewise']['abs']:.17e}")
    print("DAMPING_TO_A0P4", f"{target['large_r_homogeneous_damping_to_a0p4']:.17e}")
    print("LEADING_ABS_US_OVER_R_AMPLITUDE", f"{target['leading_abs_us_over_r_amplitude_at_a0p4']:.17e}")

    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print("WROTE", args.json)


if __name__ == "__main__":
    main()
