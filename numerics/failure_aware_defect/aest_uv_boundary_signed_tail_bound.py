#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7
from nl1c4 import expanding_memory_source_trajectory as c4

import aest_uv_forced_energy_bound as feb

MODE = 20
NQ = 1024
RSTAR = feb.RSTAR


def cp(z: complex) -> dict:
    return {"real": float(z.real), "imag": float(z.imag), "abs": float(abs(z))}


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Analytic signed-tail enclosure for the AeST earliest-boundary homogeneous transient."
    )
    ap.add_argument("--trace", type=Path, default=None)
    ap.add_argument("--results-dir", type=Path, action="append", default=None)
    ap.add_argument("--nq", type=int, default=NQ)
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()

    results_dirs = list(args.results_dir or [])
    results_dirs.extend([ROOT / "results", Path.home() / "aest-memory-gravity" / "results"])
    seen: set[str] = set()
    dedup: list[Path] = []
    for p in results_dirs:
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            dedup.append(p)

    trace = args.trace.resolve() if args.trace is not None else feb.find_trace(dedup)
    rows = c4.read_trace(trace)
    histories, kmiss, tmiss = c4.select_and_align(rows)
    modes = list(map(int, r7.FOURIER_N))
    im = modes.index(MODE)
    hist = histories[im]
    segs = feb.target_segments(hist)

    amps, _, _ = r7.amplitudes()
    k = float(r7.g9.K_REQ[im])
    fac0 = 0.5 * float(amps[im]) * np.exp(1j * float(r7.PHASES[im]))
    gradfac = complex(fac0 * (1j * k))

    Xs = [gradfac * ((seg["x1"] - seg["x0"]) / seg["ds"]) for seg in segs]
    X0 = gradfac * float(segs[0]["x0"])
    Xs0 = Xs[0]
    u0 = -X0
    us0 = -Xs0

    # Remove the homogeneous damping.  Put d=3h/2 and
    # w=exp(D)u with D'=d.  On each frozen interval
    # w_ss+r^2 w=d^2 w; jumps in d add Delta d delta terms.
    ds = np.asarray([float(seg["ds"]) for seg in segs], float)
    h = np.asarray([float(seg["h"]) for seg in segs], float)
    d = 1.5 * h
    T = float(np.sum(ds))
    D = float(np.sum(d * ds))
    damping = math.exp(-D)

    V_regular = float(np.sum((d * d) * ds))
    V_jump = float(np.sum(np.abs(np.diff(d)))) if len(d) > 1 else 0.0
    V_total_variation = V_regular + V_jump

    w0 = complex(u0)
    wp0 = complex(us0 + d[0] * u0)
    dT = float(d[-1])

    # Volterra-Gronwall bound for r>=RSTAR:
    # |w(s)| <= (|w0|+|wp0|/R) exp(||V||_TV/R).
    M = (abs(w0) + abs(wp0) / RSTAR) * math.exp(V_total_variation / RSTAR)

    # At the target,
    # u_s = exp(-D)[-r w0 sin(rT) + remainder],
    # with the following uniform remainder bound.
    C_remainder = damping * (abs(wp0) + (V_total_variation + dT) * M)

    # Signed leading Drude tail.  With f(r)=r/(1+r^2),
    # int_R^inf f(r) sin(Tr) dr
    # = f(R)cos(TR)/T + err, |err|<=f(R)/T for R>1.
    if not (RSTAR > 1.0 and T > 0.0):
        raise RuntimeError("invalid signed-tail regime")
    fR = RSTAR / (1.0 + RSTAR * RSTAR)
    leading_scalar_center = (2.0 / math.pi) * fR * math.cos(RSTAR * T) / T
    leading_scalar_radius = (2.0 / math.pi) * fR / T
    leading_complex_center = -damping * w0 * leading_scalar_center
    leading_complex_radius = damping * abs(w0) * leading_scalar_radius

    mu_tail = 1.0 - (2.0 / math.pi) * math.atan(RSTAR)
    if abs(mu_tail - 1.0 / 256.0) > 5e-16:
        raise RuntimeError("unexpected RSTAR tail measure")
    remainder_tail_radius = C_remainder * mu_tail
    total_disk_radius = leading_complex_radius + remainder_tail_radius

    # Quadrature sanity check only.  It is not used in the analytic enclosure.
    r, w = c4.tan_gl_nodes(int(args.nq))
    r = np.asarray(r, float)
    w = np.asarray(w, float)
    ub = np.full_like(r, u0, dtype=complex)
    usb = np.full_like(r, us0, dtype=complex)
    for seg in segs:
        ub, usb = c4.step_linear(
            ub,
            usb,
            r,
            float(seg["h"]),
            0.0j,
            0.0j,
            float(seg["ds"]),
        )

    uv = r >= RSTAR
    if not np.any(uv):
        raise RuntimeError("UV_EMPTY")
    quad_signed = complex(np.sum(w[uv] * usb[uv]))
    quad_distance_from_center = float(abs(quad_signed - leading_complex_center))
    quad_inside_disk = bool(quad_distance_from_center <= total_disk_radius * (1.0 + 1e-12) + 1e-18)

    report = {
        "classification": (
            "AEST_UV_BOUNDARY_SIGNED_TAIL_ANALYTIC_ENCLOSURE_ESTABLISHED"
            if quad_inside_disk
            else "AEST_UV_BOUNDARY_SIGNED_TAIL_ANALYTIC_ENCLOSURE_SANITY_CHECK_FAIL"
        ),
        "scope": "target Fourier mode 20; earliest-boundary homogeneous transient through a=0.4",
        "trace": str(trace),
        "trace_sha256": feb.sha256(trace),
        "k_relative_miss": float(kmiss),
        "common_time_mismatch": float(tmiss),
        "target_mode": MODE,
        "continuum_measure": "dmu(r)=2 dr/[pi(1+r^2)]",
        "RSTAR": RSTAR,
        "RSTAR_tail_measure": mu_tail,
        "boundary_initial_data": {"u0": cp(u0), "us0": cp(us0)},
        "damping_transform": {
            "identity": "w=exp(D)u, D'=d=3h/2; w_ss+r^2 w=(d^2+d_s)w",
            "segment_count": int(len(segs)),
            "T_total_s": T,
            "D_total": D,
            "exp_minus_D": damping,
            "d_initial": float(d[0]),
            "d_final": dT,
            "V_regular_integral_d2_ds": V_regular,
            "V_jump_total_variation": V_jump,
            "V_total_variation": V_total_variation,
            "w0": cp(w0),
            "wprime0": cp(wp0),
        },
        "volterra_grownwall_enclosure": {
            "R_min": RSTAR,
            "uniform_abs_w_bound": M,
            "uniform_target_remainder_abs_us_bound": C_remainder,
            "formula": "M=(|w0|+|wprime0|/R) exp(||V||_TV/R); C_R=exp(-D)(|wprime0|+(||V||_TV+d_T)M)",
        },
        "signed_leading_tail": {
            "formula": "I0=(2/pi) int_R^inf [r/(1+r^2)] sin(rT) dr",
            "integration_by_parts_center_scalar": leading_scalar_center,
            "integration_by_parts_radius_scalar": leading_scalar_radius,
            "complex_center": cp(leading_complex_center),
            "complex_radius": leading_complex_radius,
        },
        "analytic_signed_boundary_tail_disk": {
            "center": cp(leading_complex_center),
            "radius": total_disk_radius,
            "remainder_tail_radius": remainder_tail_radius,
            "statement": "The exact signed boundary tail lies in the complex disk |I-center| <= radius.",
        },
        "quadrature_sanity_check_only": {
            "order": int(args.nq),
            "UV_r_min": float(np.min(r[uv])),
            "UV_r_max": float(np.max(r[uv])),
            "signed_boundary_tail": cp(quad_signed),
            "distance_from_analytic_disk_center": quad_distance_from_center,
            "inside_analytic_disk": quad_inside_disk,
        },
        "claim_boundary": (
            "This establishes an analytic signed-tail enclosure for the boundary homogeneous transient of the "
            "frozen piecewise-constant-h numerical representation. The quadrature value is a sanity check only. "
            "This file does not yet combine the boundary disk with the forced L1 bound into B10_x or GE06/GE07."
        ),
        "B10_x_certified": False,
        "GE06_GE07_direct_defect_certified": False,
        "full_AeST_continuum_certified": False,
        "science_threshold_changed": False,
        "observational_tuning": False,
    }

    print("AEST_UV_BOUNDARY_SIGNED_CLASSIFICATION", report["classification"])
    print("T_TOTAL_S", f"{T:.17e}")
    print("EXP_MINUS_D", f"{damping:.17e}")
    print("V_TOTAL_VARIATION", f"{V_total_variation:.17e}")
    print("UNIFORM_W_BOUND", f"{M:.17e}")
    print("UNIFORM_REMAINDER_US_BOUND", f"{C_remainder:.17e}")
    print("LEADING_CENTER_ABS", f"{abs(leading_complex_center):.17e}")
    print("LEADING_RADIUS", f"{leading_complex_radius:.17e}")
    print("REMAINDER_TAIL_RADIUS", f"{remainder_tail_radius:.17e}")
    print("TOTAL_SIGNED_TAIL_DISK_RADIUS", f"{total_disk_radius:.17e}")
    print("QUAD_SIGNED_BOUNDARY_ABS", f"{abs(quad_signed):.17e}")
    print("QUAD_DISTANCE_FROM_CENTER", f"{quad_distance_from_center:.17e}")
    print("QUAD_INSIDE_DISK", quad_inside_disk)

    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print("WROTE", args.json)

    if not quad_inside_disk:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
