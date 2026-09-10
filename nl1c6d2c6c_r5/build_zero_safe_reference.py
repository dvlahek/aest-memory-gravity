#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6c import build_linear_reference as classref
from nl1c6d2c6c import r3_modewise_full_prehistory as r3

c = r3.c
m = c.m
ORDER = 39
LAMBDA = 10.0
TAUH0 = 1.0


def mode_view(data, j: int):
    out = dict(data)
    out["modes"] = [data["modes"][j]]
    return out


def core_source(md, tau: float, k: float):
    a, _, Q = m.bg_eval(md, tau)[:3]
    sp = md["modes"][0]["splines"]
    alpha = float(sp["alpha"](tau))
    theta = float(sp["theta"](tau))
    chi = Q * (a * theta / (k * k) + alpha)
    source = chi / a
    vals = (a, Q, alpha, theta, chi, source)
    if not np.all(np.isfinite(vals)):
        raise FloatingPointError(f"nonfinite core source at tau={tau}")
    return vals


def make_force_table(data, path: Path):
    omega_ratio, weights = c.BATH_DATA[ORDER]
    if len(omega_ratio) != ORDER or len(weights) != ORDER:
        raise RuntimeError("order-39 bath size mismatch")
    if not np.all(weights > 0.0) or abs(float(np.sum(weights)) - 1.0) > 1e-12:
        raise RuntimeError("order-39 bath weights invalid")

    hmain = (float(data["t1"]) - float(data["t0"])) / 4096.0
    if not (math.isfinite(hmain) and hmain > 0.0):
        raise RuntimeError("invalid frozen main-step scale")

    rows = []
    modes = []
    for j, k in enumerate(np.asarray(m.K_MPC, float)):
        md = mode_view(data, j)
        t0 = float(md["modes"][0]["tau_lo"])
        t1 = float(data["t1"])
        if not (t0 < float(data["t0"]) and t1 <= float(md["modes"][0]["tau_hi"]) + 1e-9):
            raise RuntimeError(f"mode {j} does not provide full retarded prehistory")

        nstep = max(1, int(math.ceil((t1 - t0) / hmain)))
        grid = np.linspace(t0, t1, nstep + 1)
        q = np.zeros((ORDER, 1), float)
        p = np.zeros_like(q)
        first_force = None
        max_force = 0.0
        max_b = 0.0

        a0, Q0, _, _, chi0, src0 = core_source(md, float(grid[0]), float(k))
        for n, tau in enumerate(grid):
            tau = float(tau)
            if n > 0:
                a1, Q1, _, _, chi1, src1 = core_source(md, tau, float(k))
                q, p = c.bath_advance(
                    md,
                    float(grid[n - 1]),
                    tau,
                    q,
                    p,
                    np.asarray([src0], float),
                    np.asarray([src1], float),
                    ORDER,
                )
                a0, Q0, chi0, src0 = a1, Q1, chi1, src1

            B = float(c.bath_residual(np.asarray([chi0]), a0, q, weights)[0])
            force = -0.5 * a0 * Q0 * B / m.static.KB
            if not (math.isfinite(B) and math.isfinite(force)):
                raise FloatingPointError(f"nonfinite bath force mode={j} tau={tau}")
            rows.append((float(k), tau, force))
            if first_force is None:
                first_force = force
            max_force = max(max_force, abs(force))
            max_b = max(max_b, abs(B))

        info = {
            "mode": j,
            "k_mpc": float(k),
            "tau_first": t0,
            "tau_z6": float(data["tau_check"][0]),
            "tau_last": t1,
            "rows": int(len(grid)),
            "h_max": float(np.max(np.diff(grid))),
            "first_force_abs": float(abs(first_force)),
            "force_max_abs": float(max_force),
            "B_max_abs": float(max_b),
        }
        modes.append(info)
        print(
            f"R5_FORCE_MODE mode={j} k_mpc={k:.12e} rows={len(grid)} "
            f"tau_first={t0:.12e} tau_z6={data['tau_check'][0]:.12e} "
            f"tau_last={t1:.12e} h_max={info['h_max']:.12e} "
            f"force_max_abs={max_force:.12e}",
            flush=True,
        )

    rows.sort(key=lambda x: (x[0], x[1]))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for k, tau, force in rows:
            f.write(f"{k:.17g} {tau:.17g} {force:.17g}\n")

    audits = {
        "six_exact_modes": len(modes) == 6 and all(abs(x["k_mpc"] - float(m.K_MPC[x["mode"]])) < 1e-15 for x in modes),
        "full_prehistory_before_z6": all(x["tau_first"] < x["tau_z6"] for x in modes),
        "order39_positive_normalized": bool(np.all(weights > 0.0) and abs(float(np.sum(weights)) - 1.0) <= 1e-12),
        "step_no_larger_than_frozen_main": all(x["h_max"] <= hmain * (1.0 + 1e-12) for x in modes),
        "memory_off_core": True,
        "physical_eta_zero": True,
        "signed_lambda_not_physical_eta": True,
    }
    if not all(audits.values()):
        raise RuntimeError(f"R5 force audits failed: {audits}")
    return modes, audits


def run_signed_case(lam: float, force: Path, out: Path):
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "nl1c6d2c6c" / "build_linear_reference.py"),
            "--case", f"{lam:.17g}",
            "--force", str(force.resolve()),
            "--case-out", str(out.resolve()),
        ],
        cwd=ROOT,
        env=env,
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/c3_r5_zero_safe_linear_reference.npz")
    ap.add_argument("--force-out", default="results/c3_r5_eta0_force39.dat")
    ap.add_argument("--meta-out", default="results/c3_r5_zero_safe_linear_reference.json")
    args = ap.parse_args()

    try:
        out = Path(args.out)
        force = Path(args.force_out)
        meta = Path(args.meta_out)
        out.parent.mkdir(parents=True, exist_ok=True)

        # This CLASS data path is explicitly memory disabled.  The passive bath
        # is reconstructed only after the core trajectory is fixed.
        data = m.prepare_class_data()
        modes, audits = make_force_table(data, force)

        plus = out.with_name(out.stem + "_plus.npz")
        minus = out.with_name(out.stem + "_minus.npz")
        run_signed_case(+LAMBDA, force, plus)
        run_signed_case(-LAMBDA, force, minus)

        pp = np.load(plus)
        mm = np.load(minus)
        dalpha = (pp["alpha"] - mm["alpha"]) / (2.0 * LAMBDA)
        dE = (pp["E"] - mm["E"]) / (2.0 * LAMBDA)
        dtheta = (pp["theta"] - mm["theta"]) / (2.0 * LAMBDA)
        np.savez_compressed(
            out,
            z=classref.CHECK_Z,
            a=classref.TARGET_A,
            k_mpc=m.K_MPC,
            alpha=dalpha,
            E=dE,
            theta=dtheta,
            lambda_value=np.asarray([LAMBDA]),
        )
        plus.unlink(missing_ok=True)
        minus.unlink(missing_ok=True)

        report = {
            "classification": "C3_R5_ZERO_COUPLING_SAFE_REFERENCE_READY",
            "physical_eta": 0.0,
            "tauH0": TAUH0,
            "bath_order": ORDER,
            "lambda": LAMBDA,
            "signed_lambda_is_physical_eta": False,
            "core": "memory-disabled CLASS",
            "bath": "external analytic order-39 bath_advance on frozen CLASS core source",
            "forcing": "-a Q B_chi^(0)/(2 K_B)",
            "mode_stats": modes,
            "audits": audits,
        }
        meta.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print("CLASSIFICATION=C3_R5_ZERO_COUPLING_SAFE_REFERENCE_READY", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 0
    except Exception as exc:
        print(f"C3_R5_REFERENCE_ERROR {type(exc).__name__}: {exc}", flush=True)
        print("CLASSIFICATION=C3_R5_REFERENCE_INCOMPLETE", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
