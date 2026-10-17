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
NQ = 1024
TSTAR = 255.0 / 256.0
RSTAR = math.tan(0.5 * math.pi * TSTAR)


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
        for pattern in ("ge19_repair26_R1_full_history_trace.dat", "*repair26*trace*.dat"):
            for p in rd.rglob(pattern):
                if p.is_file() and p.stat().st_size == target_bytes and sha256(p) == target_sha:
                    return p
    raise RuntimeError("FROZEN_REPAIR26_TRACE_NOT_FOUND")


def cp(z: complex) -> dict:
    return {"real": float(z.real), "imag": float(z.imag), "abs": float(abs(z))}


def target_segments(hist: list[dict]) -> list[dict]:
    aa = np.asarray([row["a"] for row in hist], float)
    lo = max([i for i, a in enumerate(aa) if a <= A_TARGET], default=None)
    hi = min([i for i, a in enumerate(aa) if a >= A_TARGET], default=None)
    if lo is None or hi is None or lo == hi:
        raise RuntimeError("frozen trace does not bracket a=0.4")

    segs: list[dict] = []
    for i in range(lo):
        a0 = float(hist[i]["a"])
        a1 = float(hist[i + 1]["a"])
        N0, N1 = math.log(a0), math.log(a1)
        h0 = float(hist[i]["H_over_H0"]) * TAUH0
        h1 = float(hist[i + 1]["H_over_H0"]) * TAUH0
        hm = math.sqrt(h0 * h1)
        ds = (N1 - N0) / hm
        x0 = float(hist[i]["chi"] / hist[i]["a"])
        x1 = float(hist[i + 1]["chi"] / hist[i + 1]["a"])
        segs.append({"h": hm, "ds": ds, "x0": x0, "x1": x1, "a0": a0, "a1": a1})

    # Final partial interval lo -> a=0.4, exactly as the frozen boundary construction.
    a0 = float(hist[lo]["a"])
    a1 = float(hist[hi]["a"])
    N0, N1, Nt = math.log(a0), math.log(a1), math.log(A_TARGET)
    frac = (Nt - N0) / (N1 - N0)
    h0 = float(hist[lo]["H_over_H0"]) * TAUH0
    h1 = float(hist[hi]["H_over_H0"]) * TAUH0
    hm = math.sqrt(h0 * h1)
    ds = (Nt - N0) / hm
    x0 = float(hist[lo]["chi"] / hist[lo]["a"])
    xhi = float(hist[hi]["chi"] / hist[hi]["a"])
    xt = x0 + frac * (xhi - x0)
    segs.append({"h": hm, "ds": ds, "x0": x0, "x1": xt, "a0": a0, "a1": A_TARGET})
    return segs


def loglog_slope(r: np.ndarray, y: np.ndarray, n: int = 64) -> float:
    rr = np.asarray(r[-n:], float)
    yy = np.asarray(y[-n:], float)
    mask = np.isfinite(rr) & (rr > 0) & np.isfinite(yy) & (yy > 0)
    if np.sum(mask) < 4:
        return math.nan
    return float(np.polyfit(np.log(rr[mask]), np.log(yy[mask]), 1)[0])


def main() -> None:
    ap = argparse.ArgumentParser(description="AeST UV boundary/forced split and forced energy certificate.")
    ap.add_argument("--trace", type=Path, default=None)
    ap.add_argument("--results-dir", type=Path, action="append", default=None)
    ap.add_argument("--nq", type=int, default=NQ)
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()

    results_dirs = list(args.results_dir or [])
    results_dirs.extend([ROOT / "results", Path.home() / "aest-memory-gravity" / "results"])
    seen: set[str] = set()
    dedup = []
    for p in results_dirs:
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            dedup.append(p)
    trace = args.trace.resolve() if args.trace is not None else find_trace(dedup)

    rows = c4.read_trace(trace)
    histories, kmiss, tmiss = c4.select_and_align(rows)
    modes = list(map(int, r7.FOURIER_N))
    im = modes.index(MODE)
    hist = histories[im]
    segs = target_segments(hist)

    amps, _, _ = r7.amplitudes()
    k = float(r7.g9.K_REQ[im])
    fac0 = 0.5 * float(amps[im]) * np.exp(1j * float(r7.PHASES[im]))
    gradfac = complex(fac0 * (1j * k))

    # Piecewise-constant X_s values for the frozen linear driver.
    Xs = [gradfac * ((seg["x1"] - seg["x0"]) / seg["ds"]) for seg in segs]
    regular_forcing_variation = float(
        sum(3.0 * seg["h"] * abs(xs) * seg["ds"] for seg, xs in zip(segs, Xs))
    )
    slope_jump_variation = float(sum(abs(Xs[i] - Xs[i - 1]) for i in range(1, len(Xs))))
    C_forced = regular_forcing_variation + slope_jump_variation

    # This UV split was frozen in the earlier D55/B2C2A diagnostic.
    mu_tail_exact = 1.0 - (2.0 / math.pi) * math.atan(RSTAR)
    mu_tail_identity = 1.0 / 256.0
    if abs(mu_tail_exact - mu_tail_identity) > 5e-16:
        raise RuntimeError("unexpected RSTAR tail measure")
    forced_absolute_tail_bound = C_forced * mu_tail_exact

    # Quadrature-node verification of the exact algebraic split. This is a sanity
    # check only; C_forced and the L1 tail bound above do not depend on quadrature.
    r, w = c4.tan_gl_nodes(int(args.nq))
    r = np.asarray(r, float)
    w = np.asarray(w, float)

    z = np.zeros_like(r, dtype=complex)
    v = np.zeros_like(r, dtype=complex)

    X0 = gradfac * float(segs[0]["x0"])
    Xs0 = Xs[0]
    ub = np.full_like(r, -X0, dtype=complex)
    usb = np.full_like(r, -Xs0, dtype=complex)

    for seg in segs:
        X_left = gradfac * float(seg["x0"])
        X_right = gradfac * float(seg["x1"])
        z, v = c4.step_linear(z, v, r, float(seg["h"]), X_left, X_right, float(seg["ds"]))
        ub, usb = c4.step_linear(ub, usb, r, float(seg["h"]), 0.0j, 0.0j, float(seg["ds"]))

    Xt = gradfac * float(segs[-1]["x1"])
    Xst = Xs[-1]
    u_total = z - Xt
    us_total = v - Xst
    u_forced = u_total - ub
    us_forced = us_total - usb

    max_forced_us = float(np.max(np.abs(us_forced)))
    energy_bound_node_check = bool(max_forced_us <= C_forced * (1.0 + 2e-11) + 1e-14)

    uv = r >= RSTAR
    if not np.any(uv):
        raise RuntimeError("UV_EMPTY")
    ruv = r[uv]
    wuv = w[uv]
    usb_uv = usb[uv]
    usf_uv = us_forced[uv]

    signed_boundary_tail = complex(np.sum(wuv * usb_uv))
    absolute_boundary_tail_proxy = float(np.sum(wuv * np.abs(usb_uv)))
    signed_forced_tail = complex(np.sum(wuv * usf_uv))
    absolute_forced_tail_proxy = float(np.sum(wuv * np.abs(usf_uv)))

    report = {
        "classification": (
            "AEST_UV_FORCED_REMAINDER_ABSOLUTE_ENERGY_BOUND_ESTABLISHED_BOUNDARY_SIGNED_TAIL_OPEN"
            if energy_bound_node_check
            else "AEST_UV_FORCED_REMAINDER_ENERGY_BOUND_NODE_CHECK_FAIL"
        ),
        "scope": "target Fourier mode 20; frozen Repair26 piecewise-linear full-history driver through a=0.4",
        "trace": str(trace),
        "trace_sha256": sha256(trace),
        "k_relative_miss": float(kmiss),
        "common_time_mismatch": float(tmiss),
        "target_mode": MODE,
        "quadrature_order_diagnostic_only": int(args.nq),
        "continuum_measure": "dmu(r)=2 dr/[pi(1+r^2)]",
        "RSTAR": RSTAR,
        "RSTAR_tail_measure": mu_tail_exact,
        "RSTAR_tail_measure_identity": "1/256",
        "boundary_initial_data": {"u0": cp(-X0), "us0": cp(-Xs0)},
        "forced_initial_data": "u_forced(s0,r)=0, us_forced(s0,r)=0",
        "piecewise_driver": {
            "segment_count": len(segs),
            "regular_integral_sum_3h_abs_Xs_ds": regular_forcing_variation,
            "slope_jump_total_variation": slope_jump_variation,
            "C_forced": C_forced,
            "identity": "sqrt(E_forced)(s) <= integral |3 h X_s| ds + sum |Delta X_s| = C_forced",
        },
        "rigorous_for_frozen_piecewise_linear_driver": {
            "uniform_in_r_abs_us_forced_bound": C_forced,
            "absolute_Drude_tail_bound_r_ge_RSTAR": forced_absolute_tail_bound,
            "forced_continuum_L1_bound_established": True,
        },
        "quadrature_sanity_check_only": {
            "max_abs_us_forced": max_forced_us,
            "max_abs_us_forced_over_C_forced": float(max_forced_us / C_forced) if C_forced else 0.0,
            "energy_bound_node_check": energy_bound_node_check,
            "UV_r_min": float(np.min(ruv)),
            "UV_r_max": float(np.max(ruv)),
            "boundary_raw_loglog_slope_abs_us": loglog_slope(ruv, np.abs(usb_uv)),
            "forced_raw_loglog_slope_abs_us": loglog_slope(ruv, np.abs(usf_uv)),
            "signed_boundary_tail": cp(signed_boundary_tail),
            "absolute_boundary_tail_proxy": absolute_boundary_tail_proxy,
            "signed_forced_tail": cp(signed_forced_tail),
            "absolute_forced_tail_proxy": absolute_forced_tail_proxy,
        },
        "open_problem": (
            "The boundary homogeneous transient is not absolutely L1 because of the nonzero position mismatch. "
            "Its signed continuum Drude tail still requires a rigorous oscillatory enclosure."
        ),
        "B10_x_certified": False,
        "GE06_GE07_direct_defect_certified": False,
        "full_AeST_continuum_certified": False,
        "science_threshold_changed": False,
        "observational_tuning": False,
    }

    print("AEST_UV_FORCED_CLASSIFICATION", report["classification"])
    print("SEGMENT_COUNT", len(segs))
    print("C_FORCED", f"{C_forced:.17e}")
    print("FORCED_ABS_TAIL_BOUND", f"{forced_absolute_tail_bound:.17e}")
    print("MAX_NODE_ABS_US_FORCED", f"{max_forced_us:.17e}")
    print("MAX_NODE_OVER_C_FORCED", f"{report['quadrature_sanity_check_only']['max_abs_us_forced_over_C_forced']:.17e}")
    print("BOUNDARY_RAW_SLOPE", f"{report['quadrature_sanity_check_only']['boundary_raw_loglog_slope_abs_us']:.17e}")
    print("FORCED_RAW_SLOPE", f"{report['quadrature_sanity_check_only']['forced_raw_loglog_slope_abs_us']:.17e}")
    print("BOUNDARY_SIGNED_TAIL_ABS", f"{report['quadrature_sanity_check_only']['signed_boundary_tail']['abs']:.17e}")
    print("BOUNDARY_ABS_TAIL_PROXY", f"{absolute_boundary_tail_proxy:.17e}")

    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print("WROTE", args.json)

    if not energy_bound_node_check:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
