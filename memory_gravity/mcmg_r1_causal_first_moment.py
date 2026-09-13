#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import fftconvolve

ROOT = Path(__file__).resolve().parents[1]
PREDATA_LOCK = "a1f94c9d25152e80960cb1b0af32b1c469136597"

OMEGA_M0 = 0.315
OMEGA_L0 = 0.685
A_INI = 1.0e-3
U_VALUES = (0.005, 0.01, 0.02, 0.04)
U_ZERO = 1.0e-5
N_TIME = 32768
Z_WINDOW_MAX = 2.0

PASS = "MCMG_CAUSAL_FIRST_MOMENT_UNIVERSALITY_PASS"
NUM_FAIL = "MCMG_CAUSAL_FIRST_MOMENT_NUMERICAL_CONTROL_FAIL"
ASYM_FAIL = "MCMG_CAUSAL_FIRST_MOMENT_ASYMPTOTIC_FAIL"
KERNEL_FAIL = "MCMG_CAUSAL_FIRST_MOMENT_KERNEL_UNIVERSALITY_FAIL"
SIGN_FAIL = "MCMG_CAUSAL_FIRST_MOMENT_SIGN_FAIL"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def E_of_a(a):
    a = np.asarray(a, float)
    return np.sqrt(OMEGA_M0 * a ** -3 + OMEGA_L0)


def omega_m(a):
    a = np.asarray(a, float)
    e2 = OMEGA_M0 * a ** -3 + OMEGA_L0
    return OMEGA_M0 * a ** -3 / e2


def x_of_a(a):
    a = np.asarray(a, float)
    return 2.0 / (3.0 * math.sqrt(OMEGA_L0)) * np.arcsinh(
        math.sqrt(OMEGA_L0 / OMEGA_M0) * a ** 1.5
    )


def a_of_x(x):
    x = np.asarray(x, float)
    q = math.sqrt(OMEGA_M0 / OMEGA_L0) * np.sinh(1.5 * math.sqrt(OMEGA_L0) * x)
    return np.maximum(q, 0.0) ** (2.0 / 3.0)


def solve_gr_growth():
    n0 = math.log(A_INI)

    def rhs(n, y):
        a = math.exp(n)
        om = float(omega_m(a))
        dlnh = -1.5 * om
        d, v = y
        return [v, -(2.0 + dlnh) * v + 1.5 * om * d]

    sol = solve_ivp(
        rhs,
        (n0, 0.0),
        [A_INI, A_INI],
        method="DOP853",
        rtol=2e-12,
        atol=2e-14,
        dense_output=True,
        max_step=0.02,
    )
    if not sol.success or sol.sol is None:
        raise RuntimeError(f"GR growth integration failed: {sol.message}")
    d1 = float(sol.sol(0.0)[0])
    if not np.isfinite(d1) or d1 <= 0:
        raise RuntimeError("invalid D(a=1)")

    def eval_at_a(a):
        aa = np.asarray(a, float)
        vals = sol.sol(np.log(aa))
        return np.asarray(vals[0], float) / d1, np.asarray(vals[1], float) / d1

    return eval_at_a


def kernel_values(kind: str, lag: np.ndarray, u: float):
    s = np.asarray(lag, float)
    if kind == "exp":
        return np.exp(-s / u) / u
    if kind == "gamma2":
        return 4.0 * s * np.exp(-2.0 * s / u) / (u * u)
    if kind == "gamma4":
        return (4.0 / u) ** 4 * s ** 3 * np.exp(-4.0 * s / u) / math.factorial(3)
    if kind == "tophat":
        return np.where(s <= 2.0 * u, 1.0 / (2.0 * u), 0.0)
    raise KeyError(kind)


def causal_memory_fft(source, dx, kind, u):
    src = np.asarray(source, float)
    lag = np.arange(src.size, dtype=float) * dx
    kval = kernel_values(kind, lag, u)
    # Frozen prehistory S=S_ini: convolve only deviations from S_ini.
    dev = src - src[0]
    conv = fftconvolve(dev, kval, mode="full")[: src.size] * dx
    return src[0] + conv


def exponential_memory_ode(eval_growth, u, x_eval):
    x0 = float(x_of_a(A_INI))

    def source_x(x):
        a = float(a_of_x(x))
        d, _ = eval_growth(np.asarray([a]))
        return float(d[0] / a)

    s0 = source_x(x0)

    def rhs(x, y):
        return [(source_x(x) - y[0]) / u]

    sol = solve_ivp(
        rhs,
        (x0, float(x_eval[-1])),
        [s0],
        method="Radau",
        rtol=2e-10,
        atol=2e-12,
        dense_output=True,
        max_step=0.002,
    )
    if not sol.success or sol.sol is None:
        raise RuntimeError(f"zero-memory exponential solve failed: {sol.message}")
    return np.asarray(sol.sol(x_eval)[0], float)


def rel_l2(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    den = max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300)
    return float(np.linalg.norm(aa - bb) / den)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/mcmg_r1_causal_first_moment.json")
    ap.add_argument("--npz-out", default="results/mcmg_r1_causal_first_moment.npz")
    args = ap.parse_args()

    if not is_ancestor(PREDATA_LOCK):
        raise SystemExit("MCMG_R1_PREDATA_LOCK_FAIL")

    print("MCMG_R1_START", flush=True)
    eval_growth = solve_gr_growth()

    x_ini = float(x_of_a(A_INI))
    x_end = float(x_of_a(1.0))
    x = np.linspace(x_ini, x_end, N_TIME)
    dx = float(x[1] - x[0])
    a = a_of_x(x)
    d, dn = eval_growth(a)
    source = d / a
    dsource_dx = E_of_a(a) * (dn - d) / a
    z = 1.0 / a - 1.0
    win = z <= Z_WINDOW_MAX + 1e-12

    all_finite = bool(
        np.all(np.isfinite(x))
        and np.all(np.isfinite(a))
        and np.all(np.isfinite(d))
        and np.all(np.isfinite(dn))
        and np.all(np.isfinite(source))
        and np.all(np.isfinite(dsource_dx))
    )
    growth_positive = bool(np.all(d > 0))
    early_ratio = float(dn[0] / d[0])
    g1 = bool(all_finite and growth_positive and abs(early_ratio - 1.0) <= 1e-5)

    kernels = ("exp", "gamma2", "gamma4", "tophat")
    delta = {}
    errors = {k: {} for k in kernels}
    memories = {}

    for kind in kernels:
        for u in U_VALUES:
            m = causal_memory_fft(source, dx, kind, u)
            memories[(kind, u)] = m
            dd = m - source
            delta[(kind, u)] = dd
            err = float(
                np.linalg.norm(dd[win] / u + dsource_dx[win])
                / max(np.linalg.norm(dsource_dx[win]), 1e-300)
            )
            errors[kind][u] = err
            print(f"MCMG_R1_KERNEL kind={kind} u={u:.6f} first_moment_error={err:.8e}", flush=True)

    # G2: exact static-source control using the same convolution implementation.
    static = np.ones_like(source) * 1.23456789
    static_errs = {}
    for kind in kernels:
        ms = causal_memory_fft(static, dx, kind, 0.04)
        e = float(np.max(np.abs(ms - static)) / np.max(np.abs(static)))
        static_errs[kind] = e
    g2 = bool(max(static_errs.values()) <= 1e-10)

    # G3: actual stiff exponential relaxation at u=1e-5.
    xw = x[win]
    sw = source[win]
    mz = exponential_memory_ode(eval_growth, U_ZERO, xw)
    zero_err = float(np.max(np.abs(mz - sw)) / max(np.max(np.abs(sw)), 1e-300))
    g3 = bool(zero_err <= 2e-5)

    # G4: alter only future source (z<0.5), then verify no effect at z>=0.5.
    zcut = 0.5
    xcut = float(x_of_a(1.0 / (1.0 + zcut)))
    sf = source.copy()
    sf[x > xcut] *= 1.1
    causal_errs = {}
    past = x <= xcut + 1e-15
    for kind in kernels:
        m0 = memories[(kind, 0.04)]
        mf = causal_memory_fft(sf, dx, kind, 0.04)
        e = float(np.max(np.abs(mf[past] - m0[past])) / max(np.max(np.abs(m0[past])), 1e-300))
        causal_errs[kind] = e
    g4 = bool(max(causal_errs.values()) <= 1e-12)

    # G5: first-moment convergence.
    g5a = all(errors[k][0.005] < 0.15 for k in kernels)
    g5b = all(errors[k][0.005] < errors[k][0.02] for k in kernels)
    strict_count = sum(
        errors[k][0.005] < errors[k][0.01] < errors[k][0.02]
        for k in kernels
    )
    g5 = bool(g5a and g5b and strict_count >= 3)

    # G6: shape collapse at fixed first moment.
    def collapse(u):
        vals = []
        for i, ka in enumerate(kernels):
            qa = delta[(ka, u)][win] / u
            for kb in kernels[i + 1 :]:
                qb = delta[(kb, u)][win] / u
                vals.append(rel_l2(qa, qb))
        return float(max(vals)), vals

    c005, pair005 = collapse(0.005)
    c02, pair02 = collapse(0.02)
    g6 = bool(c005 < 0.10 and c005 < c02)

    # G7: sign consistency where the derivative is non-negligible.
    dw = dsource_dx[win]
    active = np.abs(dw) > 1e-6 * max(float(np.max(np.abs(dw))), 1e-300)
    sign_fractions = {}
    for kind in kernels:
        q = delta[(kind, 0.01)][win]
        same = np.sign(q[active]) == np.sign(-dw[active])
        sign_fractions[kind] = float(np.mean(same)) if same.size else 0.0
    g7 = bool(min(sign_fractions.values()) >= 0.99)

    gates = {
        "R1_G1_GR_source_and_finite_control": g1,
        "R1_G2_static_source_limit": g2,
        "R1_G3_zero_memory_limit": g3,
        "R1_G4_explicit_causality": g4,
        "R1_G5_first_moment_convergence": g5,
        "R1_G6_kernel_shape_collapse": g6,
        "R1_G7_lag_sign_consistency": g7,
    }

    if not all((g1, g2, g3, g4)):
        classification = NUM_FAIL
    elif not g5:
        classification = ASYM_FAIL
    elif not g6:
        classification = KERNEL_FAIL
    elif not g7:
        classification = SIGN_FAIL
    else:
        classification = PASS

    summary = {
        "classification": classification,
        "early_Dprime_over_D": early_ratio,
        "zero_memory_max_relative": zero_err,
        "static_max_relative": float(max(static_errs.values())),
        "causality_max_relative": float(max(causal_errs.values())),
        "strict_first_moment_monotonic_kernel_count": int(strict_count),
        "kernel_collapse_u0p005": c005,
        "kernel_collapse_u0p02": c02,
        "min_lag_sign_fraction_u0p01": float(min(sign_fractions.values())),
        "dx_H0t": dx,
        "x_ini": x_ini,
        "x_today": x_end,
    }

    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "predata_lock": PREDATA_LOCK,
        "cosmology": {"Omega_m0": OMEGA_M0, "Omega_Lambda0": OMEGA_L0, "a_ini": A_INI},
        "u_values": list(U_VALUES),
        "zero_memory_u": U_ZERO,
        "gates": gates,
        "summary": summary,
        "first_moment_errors": {k: {str(u): float(v) for u, v in errors[k].items()} for k in kernels},
        "static_errors": static_errs,
        "causality_errors": causal_errs,
        "lag_sign_fractions": sign_fractions,
        "collapse_pairwise": {"u0p005": pair005, "u0p02": pair02},
        "interpretation": {
            "licenses_R2_self_consistent_growth_memory": bool(classification == PASS),
            "new_physics_claim_licensed": False,
            "observational_claim_licensed": False,
            "AeST_reclassified": False,
        },
    }

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

    npz = {
        "x_H0t": x,
        "a": a,
        "z": z,
        "D_GR": d,
        "Dprime_ln_a_GR": dn,
        "source_D_over_a": source,
        "dsource_dx": dsource_dx,
    }
    for kind in kernels:
        for u in U_VALUES:
            tag = str(u).replace(".", "p")
            npz[f"memory_{kind}_u{tag}"] = memories[(kind, u)]
            npz[f"delta_{kind}_u{tag}"] = delta[(kind, u)]
    np.savez_compressed(args.npz_out, **npz)

    print("MCMG_R1_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("MCMG_R1_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("MCMG_R1_CLASSIFICATION=" + classification, flush=True)
    return 0 if classification == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
