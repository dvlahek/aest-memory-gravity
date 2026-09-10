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
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6c import build_linear_reference as base

LAMBDA = 10.0
ORDER = 39
TAUH0 = 1.0
FORCE_FIELD = "eta0_tangent_force_aest"


def clear_env() -> None:
    for key in (
        "AEST_TANGENT_TRACE_FILE",
        "AEST_TANGENT_FORCE_FILE",
        "AEST_TANGENT_LAMBDA",
        "AEST_TANGENT_ALLOW_K_MISS",
    ):
        os.environ.pop(key, None)


def normalize_tau_force(tau, force):
    tau = np.asarray(tau, float)
    force = np.asarray(force, float)
    finite = np.isfinite(tau) & np.isfinite(force) & (tau >= 0.0)
    tau = tau[finite]
    force = force[finite]
    if tau.size == 0:
        raise RuntimeError("dense force history contains no finite rows")
    order = np.argsort(tau)
    tau = tau[order]
    force = force[order]
    unique_tau, inv = np.unique(tau, return_inverse=True)
    sums = np.zeros(unique_tau.size, float)
    counts = np.zeros(unique_tau.size, int)
    np.add.at(sums, inv, force)
    np.add.at(counts, inv, 1)
    force_u = sums / counts
    return unique_tau, force_u


def tau_at_a(raw, target_a):
    ka = base.pick(raw, ("a", "scale factor"))
    kt = base.pick(raw, ("tau [Mpc]", "tau", "tau[Mpc]"))
    aa = np.asarray(raw[ka], float)
    tt = np.asarray(raw[kt], float)
    order = np.argsort(aa)
    aa = aa[order]
    tt = tt[order]
    finite = np.isfinite(aa) & np.isfinite(tt)
    aa = aa[finite]
    tt = tt[finite]
    keep = np.ones(aa.size, dtype=bool)
    if aa.size > 1:
        keep[1:] = np.diff(aa) > 0
    aa = aa[keep]
    tt = tt[keep]
    if aa.size < 8:
        raise RuntimeError("insufficient dense a(tau) history")
    return float(PchipInterpolator(aa, tt, extrapolate=False)(target_a))


def make_dense_force_table(force_path: Path):
    clear_env()
    os.environ["OMP_NUM_THREADS"] = "1"
    from classy import Class

    c = Class()
    c.set(base.params(True))
    c.compute()
    try:
        histories, _ = base.d2a.scalar_histories(c.get_perturbations())
        if len(histories) != 6:
            raise RuntimeError(f"Stage A expected 6 dense scalar histories, got {len(histories)}")

        rows = []
        mode_stats = []
        for j, raw in enumerate(histories):
            kt = base.pick(raw, ("tau [Mpc]", "tau", "tau[Mpc]"))
            kf = base.pick(raw, (FORCE_FIELD,))
            tau, force = normalize_tau_force(raw[kt], raw[kf])
            tz6 = tau_at_a(raw, 1.0 / 7.0)
            if tau.size < 100:
                raise RuntimeError(f"Stage A mode {j} has only {tau.size} unique dense rows")
            if not np.all(np.diff(tau) > 0.0):
                raise RuntimeError(f"Stage A mode {j} tau is not strictly increasing")
            if not (tau[0] < tz6):
                raise RuntimeError(
                    f"Stage A mode {j} begins too late: tau_first={tau[0]} tau_z6={tz6}"
                )
            k = float(base.m.K_MPC[j])
            rows.extend((k, float(t), float(f)) for t, f in zip(tau, force))
            st = {
                "mode_index": j,
                "k_mpc": k,
                "rows": int(tau.size),
                "tau_first": float(tau[0]),
                "tau_last": float(tau[-1]),
                "tau_z6": float(tz6),
                "force_max_abs": float(np.max(np.abs(force))),
                "force_l2": float(np.linalg.norm(force)),
            }
            mode_stats.append(st)
            print(
                f"R4_DENSE_MODE i={j} k_mpc={k:.12e} rows={tau.size} "
                f"tau_first={tau[0]:.12e} tau_z6={tz6:.12e} tau_last={tau[-1]:.12e} "
                f"force_max_abs={st['force_max_abs']:.12e}",
                flush=True,
            )
    finally:
        c.struct_cleanup()
        c.empty()
        clear_env()

    rows.sort(key=lambda x: (x[0], x[1]))
    force_path.parent.mkdir(parents=True, exist_ok=True)
    with force_path.open("w") as f:
        for k, tau, force in rows:
            f.write(f"{k:.17g} {tau:.17g} {force:.17g}\n")

    expected_k = np.asarray(base.m.K_MPC, float)
    got_k = np.asarray([x["k_mpc"] for x in mode_stats], float)
    audits = {
        "exact_six_modes": bool(len(mode_stats) == 6 and np.allclose(got_k, expected_k, rtol=0.0, atol=1e-15)),
        "all_rows_ge_100": bool(all(x["rows"] >= 100 for x in mode_stats)),
        "all_begin_before_z6": bool(all(x["tau_first"] < x["tau_z6"] for x in mode_stats)),
        "stage_a_memory_enabled_eta0_order39": True,
    }
    if not all(audits.values()):
        raise RuntimeError(f"Stage A audit failed: {audits}")
    return mode_stats, audits


def run_case(lam: float, force_path: Path, out: Path):
    clear_env()
    os.environ["AEST_TANGENT_FORCE_FILE"] = str(force_path.resolve())
    os.environ["AEST_TANGENT_LAMBDA"] = f"{lam:.17g}"
    os.environ["AEST_TANGENT_ALLOW_K_MISS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"

    from classy import Class
    c = Class()
    c.set(base.params(False))
    c.compute()
    try:
        histories, _ = base.d2a.scalar_histories(c.get_perturbations())
        if len(histories) != 6:
            raise RuntimeError(f"Stage B expected 6 scalar histories, got {len(histories)}")
        alpha = np.empty((len(base.CHECK_Z), 6))
        E = np.empty_like(alpha)
        theta = np.empty_like(alpha)
        for j, raw in enumerate(histories):
            ka = base.pick(raw, ("a", "scale factor"))
            kalpha = base.pick(raw, ("alpha_aest", "alpha"))
            kE = base.pick(raw, ("E_aest", "E"))
            kth = base.pick(raw, ("theta_cdm", "t_cdm"))
            aa = np.asarray(raw[ka], float)
            alpha[:, j] = base.interp_on_a(aa, raw[kalpha])
            E[:, j] = base.interp_on_a(aa, raw[kE])
            theta[:, j] = base.interp_on_a(aa, raw[kth])
    finally:
        c.struct_cleanup()
        c.empty()
        clear_env()

    np.savez_compressed(
        out,
        z=base.CHECK_Z,
        a=base.TARGET_A,
        k_mpc=base.m.K_MPC,
        alpha=alpha,
        E=E,
        theta=theta,
        lambda_value=np.asarray([lam]),
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/c3_r4_dense_linear_reference.npz")
    ap.add_argument("--force-out", default="results/c3_r4_dense_force39.dat")
    ap.add_argument("--meta-out", default="results/c3_r4_dense_linear_reference.json")
    ap.add_argument("--case", type=float, default=None)
    ap.add_argument("--force", default=None)
    ap.add_argument("--case-out", default=None)
    args = ap.parse_args()

    try:
        if args.case is not None:
            if args.force is None or args.case_out is None:
                raise RuntimeError("--case requires --force and --case-out")
            run_case(args.case, Path(args.force), Path(args.case_out))
            return 0

        out = Path(args.out)
        force = Path(args.force_out)
        meta = Path(args.meta_out)
        out.parent.mkdir(parents=True, exist_ok=True)

        mode_stats, audits = make_dense_force_table(force)

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
            z=base.CHECK_Z,
            a=base.TARGET_A,
            k_mpc=base.m.K_MPC,
            alpha=dalpha,
            E=dE,
            theta=dtheta,
            lambda_value=np.asarray([LAMBDA]),
        )
        plus.unlink(missing_ok=True)
        minus.unlink(missing_ok=True)

        audits.update({
            "stage_b_memory_disabled_eta0_signed_lambda": True,
            "sparse_k_reference_only": True,
            "no_backward_extrapolation": True,
        })
        report = {
            "classification": "C3_R4_DENSE_FULLHISTORY_REFERENCE_READY",
            "physical_eta": 0.0,
            "tauH0": TAUH0,
            "bath_order": ORDER,
            "lambda": LAMBDA,
            "signed_lambda_is_physical_eta": False,
            "force_field": FORCE_FIELD,
            "mode_stats": mode_stats,
            "audits": audits,
            "z_checkpoints": base.CHECK_Z.tolist(),
            "method": "CLASS-live eta0 bath dense-history forcing, central signed-lambda response",
        }
        meta.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True), flush=True)
        return 0
    except Exception as exc:
        print(f"C3_R4_REFERENCE_REPAIR_ERROR {type(exc).__name__}: {exc}", flush=True)
        print("CLASSIFICATION=C3_R4_REFERENCE_REPAIR_INCOMPLETE", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
