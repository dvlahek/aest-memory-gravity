#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import sys

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6a import physical_time_scalar_current_integrator_v6 as v6
from nl1c6d2a import baryon_matter_sector_audit as d2a

m = v6.m
CHECK_Z = np.asarray([6.0, 5.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.5, 0.2], float)
TARGET_A = 1.0 / (1.0 + CHECK_Z)
GATE = 5.0e-3
ORDER = 39
TAUH0 = 1.0
FIELDS = {
    "alpha": ("alpha_aest", "alpha"),
    "E": ("E_aest", "E"),
    "theta": ("theta_cdm", "t_cdm"),
}


def clear_force_env() -> None:
    for key in (
        "AEST_TANGENT_TRACE_FILE",
        "AEST_TANGENT_FORCE_FILE",
        "AEST_TANGENT_LAMBDA",
        "AEST_TANGENT_ALLOW_K_MISS",
    ):
        os.environ.pop(key, None)


def pick(raw, names):
    for name in names:
        if name in raw:
            return name
    raise RuntimeError(f"missing field among {names}; available={sorted(raw.keys())}")


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
        keep[1:] = np.diff(a) > 0.0
    a = a[keep]
    y = y[keep]
    if a.size < 8:
        raise RuntimeError("insufficient unique finite perturbation samples")
    if TARGET_A[0] < a[0] - 1e-13 or TARGET_A[-1] > a[-1] + 1e-13:
        raise RuntimeError(f"history does not cover frozen checkpoints: {a[0]}..{a[-1]}")
    out = PchipInterpolator(a, y, extrapolate=False)(TARGET_A)
    if not np.all(np.isfinite(out)):
        raise RuntimeError("nonfinite checkpoint interpolation")
    return np.asarray(out, float)


def params(memory_enabled: bool):
    p = dict(m.build_params())
    p.update({
        "output": "mTk,vTk",
        "lensing": "no",
        "k_output_values": ", ".join(f"{k:.17g}" for k in m.K_MPC),
        "P_k_max_h/Mpc": 2.0,
        "z_max_pk": 6.5,
        "aest_memory_enabled": "yes" if memory_enabled else "no",
        "aest_eta": 0.0,
        "aest_tau_H0": TAUH0,
        "aest_memory_order": ORDER,
    })
    return p


def run_case(memory_enabled: bool):
    clear_force_env()
    os.environ["OMP_NUM_THREADS"] = "1"
    from classy import Class

    c = Class()
    c.set(params(memory_enabled))
    c.compute()
    try:
        histories, scalar_key = d2a.scalar_histories(c.get_perturbations())
        if len(histories) != 6:
            raise RuntimeError(f"expected 6 scalar histories, got {len(histories)}")
        out = {name: np.empty((len(CHECK_Z), 6), float) for name in FIELDS}
        for j, raw in enumerate(histories):
            ka = pick(raw, ("a", "scale factor"))
            aa = np.asarray(raw[ka], float)
            for name, aliases in FIELDS.items():
                kf = pick(raw, aliases)
                out[name][:, j] = interp_on_a(aa, raw[kf])
        return out, scalar_key
    finally:
        c.struct_cleanup()
        c.empty()
        clear_force_env()


def rel_l2(test, ref):
    test = np.asarray(test, float)
    ref = np.asarray(ref, float)
    return float(np.linalg.norm(test - ref) / max(np.linalg.norm(ref), 1e-300))


def max_symmetric_rel(test, ref):
    test = np.asarray(test, float)
    ref = np.asarray(ref, float)
    scale = np.maximum(np.maximum(np.abs(test), np.abs(ref)), 1e-300)
    usable = np.maximum(np.abs(test), np.abs(ref)) > 1e-12 * max(
        float(np.max(np.abs(test))), float(np.max(np.abs(ref))), 1e-300
    )
    if not np.any(usable):
        return 0.0
    return float(np.max(np.abs(test[usable] - ref[usable]) / scale[usable]))


def main() -> int:
    out_json = ROOT / "results" / "c3_eta0_zero_coupling.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    try:
        off, scalar_off = run_case(False)
        on, scalar_on = run_case(True)
        if scalar_off != scalar_on:
            raise RuntimeError(f"scalar history key changed: off={scalar_off} on={scalar_on}")

        rows = []
        all_ok = True
        worst = (-1.0, None, None)
        for j, kh in enumerate(np.asarray(m.K_H, float)):
            k = float(m.K_MPC[j])
            for field in ("alpha", "E", "theta"):
                ref = off[field][:, j]
                test = on[field][:, j]
                err = rel_l2(test, ref)
                pmax = max_symmetric_rel(test, ref)
                ok = bool(np.isfinite(err) and err <= GATE)
                all_ok = all_ok and ok
                if err > worst[0]:
                    worst = (err, j, field)
                rows.append({
                    "mode": j,
                    "k_h_Mpc": float(kh),
                    "k_Mpc^-1": k,
                    "field": field,
                    "relative_L2": err,
                    "max_point_relative": pmax,
                    "pass": ok,
                })
                print(
                    f"ZERO_MODE mode={j} k_h={kh:.12e} k_mpc={k:.12e} field={field} "
                    f"REL_L2={err:.12e} MAX_POINT_REL={pmax:.12e} PASS={ok}",
                    flush=True,
                )
                denom_scale = max(float(np.max(np.abs(ref))), 1e-300)
                for iz, z in enumerate(CHECK_Z):
                    ratio = float(test[iz] / ref[iz]) if abs(ref[iz]) > 1e-12 * denom_scale else float("nan")
                    print(
                        f"ZERO_POINT mode={j} field={field} z={z:g} "
                        f"OFF={ref[iz]:.12e} ON={test[iz]:.12e} RATIO={ratio:.12e}",
                        flush=True,
                    )

        report = {
            "classification": "C3_CLASS_ETA0_ZERO_COUPLING_PASS" if all_ok else "C3_CLASS_ETA0_ZERO_COUPLING_FAIL",
            "gate": GATE,
            "memory_off": {"aest_memory_enabled": False, "aest_eta": 0.0, "aest_tau_H0": TAUH0, "aest_memory_order": ORDER},
            "memory_on": {"aest_memory_enabled": True, "aest_eta": 0.0, "aest_tau_H0": TAUH0, "aest_memory_order": ORDER},
            "z_checkpoints": CHECK_Z.tolist(),
            "rows": rows,
            "global_max_relative_L2": float(worst[0]),
            "worst_mode": int(worst[1]),
            "worst_field": str(worst[2]),
            "ZERO_COUPLING_PASS": bool(all_ok),
            "FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED": False,
        }
        out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"ZERO_GLOBAL MAX_REL_L2={worst[0]:.12e} WORST_MODE={worst[1]} WORST_FIELD={worst[2]}", flush=True)
        print(f"ZERO_COUPLING_PASS={all_ok}", flush=True)
        print(f"CLASSIFICATION={report['classification']}", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 0 if all_ok else 1
    except Exception as exc:
        print(f"C3_ZERO_COUPLING_ERROR {type(exc).__name__}: {exc}", flush=True)
        print("CLASSIFICATION=C3_CLASS_ETA0_ZERO_COUPLING_INCOMPLETE", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
