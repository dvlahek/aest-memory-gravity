#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from collections import defaultdict

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6a import physical_time_scalar_current_integrator_v6 as v6
from nl1c6d2a import baryon_matter_sector_audit as d2a

m = v6.m
LAMBDA = 10.0
ORDER = 39
TAUH0 = 1.0
CHECK_Z = m.CHECK_Z.copy()
TARGET_A = 1.0 / (1.0 + CHECK_Z)


def params(memory: bool):
    p = dict(m.build_params())
    p.update({
        "aest_memory_enabled": "yes" if memory else "no",
        "aest_memory_order": ORDER,
        "aest_eta": 0.0,
        "aest_tau_H0": TAUH0,
    })
    return p


def clear_force_env():
    for key in (
        "AEST_TANGENT_TRACE_FILE",
        "AEST_TANGENT_FORCE_FILE",
        "AEST_TANGENT_LAMBDA",
    ):
        os.environ.pop(key, None)


def normalize_force(raw: Path, out: Path):
    acc = defaultdict(lambda: [0.0, 0])
    for line in raw.read_text(errors="replace").splitlines():
        p = line.split()
        if len(p) != 3:
            continue
        try:
            k, tau, force = map(float, p)
        except ValueError:
            continue
        if math.isfinite(k) and math.isfinite(tau) and math.isfinite(force) and k > 0 and tau >= 0:
            acc[(k, tau)][0] += force
            acc[(k, tau)][1] += 1
    if not acc:
        raise RuntimeError("eta0 tangent trace produced no valid forcing rows")
    rows = [(k, tau, s / n) for (k, tau), (s, n) in acc.items()]
    rows.sort(key=lambda q: (q[0], q[1]))
    with out.open("w") as f:
        for k, tau, force in rows:
            f.write(f"{k:.17g} {tau:.17g} {force:.17g}\n")
    return {
        "raw_rows": sum(n for _, n in acc.values()),
        "unique_rows": len(rows),
        "k_count": len({q[0] for q in rows}),
        "force_l2": float(np.linalg.norm([q[2] for q in rows])),
        "force_max_abs": float(max(abs(q[2]) for q in rows)),
    }


def make_trace(force_path: Path):
    raw = force_path.with_name(force_path.stem + "_raw.dat")
    raw.parent.mkdir(parents=True, exist_ok=True)
    clear_force_env()
    os.environ["AEST_TANGENT_TRACE_FILE"] = str(raw.resolve())
    os.environ["OMP_NUM_THREADS"] = "1"
    from classy import Class
    c = Class()
    c.set(params(True))
    c.compute()
    try:
        pert = c.get_perturbations()
        histories, _ = d2a.scalar_histories(pert)
        if len(histories) != 6:
            raise RuntimeError(f"trace expected 6 scalar histories, got {len(histories)}")
    finally:
        c.struct_cleanup()
        c.empty()
    clear_force_env()
    return normalize_force(raw, force_path)


def pick(raw, exacts):
    for key in exacts:
        if key in raw:
            return key
    raise RuntimeError(f"missing perturbation field among {exacts}; available={sorted(raw)}")


def interp_on_a(a, y):
    a = np.asarray(a, float)
    y = np.asarray(y, float)
    order = np.argsort(a)
    a = a[order]
    y = y[order]
    finite = np.isfinite(a) & np.isfinite(y)
    a = a[finite]
    y = y[finite]
    keep = np.ones(a.size, dtype=bool)
    if a.size > 1:
        keep[1:] = np.diff(a) > 0
    a = a[keep]
    y = y[keep]
    if a.size < 8:
        raise RuntimeError("insufficient unique perturbation samples")
    if TARGET_A[0] < a[0] - 1e-13 or TARGET_A[-1] > a[-1] + 1e-13:
        raise RuntimeError(f"perturbation history does not cover frozen checkpoints: {a[0]}..{a[-1]}")
    return PchipInterpolator(a, y, extrapolate=False)(TARGET_A)


def run_case(lam: float, force_path: Path, out: Path):
    clear_force_env()
    os.environ["AEST_TANGENT_FORCE_FILE"] = str(force_path.resolve())
    os.environ["AEST_TANGENT_LAMBDA"] = f"{lam:.17g}"
    os.environ["OMP_NUM_THREADS"] = "1"

    from classy import Class
    c = Class()
    c.set(params(False))
    c.compute()
    try:
        histories, _ = d2a.scalar_histories(c.get_perturbations())
        if len(histories) != 6:
            raise RuntimeError(f"forced case expected 6 scalar histories, got {len(histories)}")
        alpha = np.empty((len(CHECK_Z), 6))
        E = np.empty_like(alpha)
        theta = np.empty_like(alpha)
        for j, raw in enumerate(histories):
            ka = pick(raw, ("a", "scale factor"))
            kalpha = pick(raw, ("alpha_aest", "alpha"))
            kE = pick(raw, ("E_aest", "E"))
            kth = pick(raw, ("theta_cdm", "t_cdm"))
            aa = np.asarray(raw[ka], float)
            alpha[:, j] = interp_on_a(aa, raw[kalpha])
            E[:, j] = interp_on_a(aa, raw[kE])
            theta[:, j] = interp_on_a(aa, raw[kth])
    finally:
        c.struct_cleanup()
        c.empty()

    np.savez_compressed(
        out,
        z=CHECK_Z,
        a=TARGET_A,
        k_mpc=m.K_MPC,
        alpha=alpha,
        E=E,
        theta=theta,
        lambda_value=np.asarray([lam]),
    )
    clear_force_env()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/nl1c6d2c6c_linear_tangent_reference.npz")
    ap.add_argument("--force-out", default="results/nl1c6d2c6c_eta0_force39.dat")
    ap.add_argument("--meta-out", default="results/nl1c6d2c6c_linear_tangent_reference.json")
    ap.add_argument("--case", type=float, default=None)
    ap.add_argument("--force", default=None)
    ap.add_argument("--case-out", default=None)
    args = ap.parse_args()

    if args.case is not None:
        if args.force is None or args.case_out is None:
            raise SystemExit("--case requires --force and --case-out")
        run_case(args.case, Path(args.force), Path(args.case_out))
        return 0

    out = Path(args.out)
    force = Path(args.force_out)
    meta = Path(args.meta_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    stats = make_trace(force)

    plus = out.with_name(out.stem + "_plus.npz")
    minus = out.with_name(out.stem + "_minus.npz")
    for lam, target in ((LAMBDA, plus), (-LAMBDA, minus)):
        subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--case", f"{lam:.17g}",
                "--force", str(force.resolve()),
                "--case-out", str(target.resolve()),
            ],
            cwd=ROOT,
            check=True,
            env=os.environ.copy(),
        )

    p = np.load(plus)
    q = np.load(minus)
    dalpha = (p["alpha"] - q["alpha"]) / (2.0 * LAMBDA)
    dE = (p["E"] - q["E"]) / (2.0 * LAMBDA)
    dtheta = (p["theta"] - q["theta"]) / (2.0 * LAMBDA)
    np.savez_compressed(
        out,
        z=CHECK_Z,
        a=TARGET_A,
        k_mpc=m.K_MPC,
        alpha=dalpha,
        E=dE,
        theta=dtheta,
        lambda_value=np.asarray([LAMBDA]),
    )
    plus.unlink(missing_ok=True)
    minus.unlink(missing_ok=True)

    report = {
        "classification": "D2C6C_LINEAR_ETA0_VARIATIONAL_REFERENCE_READY",
        "physical_eta": 0.0,
        "signed_lambda_is_physical_eta": False,
        "lambda": LAMBDA,
        "tauH0": TAUH0,
        "bath_order": ORDER,
        "force_trace": stats,
        "fields": ["alpha", "E", "theta"],
        "z_checkpoints": CHECK_Z.tolist(),
        "method": "central signed-lambda CLASS variational forcing reference",
    }
    meta.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
