#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import sys

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6c import r3_modewise_full_prehistory as r3
from nl1c6d2c6c_r4ref import build_dense_fullhistory_reference as r4

c = r3.c
m = c.m
base = r4.base
ORDER = 39
TAUH0 = 1.0
Z_GATE = 5.0e-3
ZP_GATE = 5.0e-3
B_GATE = 5.0e-3
CHI_GATE = 1.0e-8


def rel_l2(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(bb), 1e-300))


def point_rel(a, b, floor):
    return float(abs(float(a) - float(b)) / max(abs(float(b)), float(floor), 1e-300))


def clear_env():
    for key in (
        "AEST_TANGENT_TRACE_FILE",
        "AEST_TANGENT_FORCE_FILE",
        "AEST_TANGENT_LAMBDA",
        "AEST_TANGENT_ALLOW_K_MISS",
    ):
        os.environ.pop(key, None)


def sorted_unique_indices(tau):
    tau = np.asarray(tau, float)
    order = np.argsort(tau)
    ts = tau[order]
    uniq, first = np.unique(ts, return_index=True)
    return uniq, order[first]


def interp_columns(t, tau, arr):
    arr = np.asarray(arr, float)
    return np.asarray([np.interp(t, tau, arr[:, j]) for j in range(arr.shape[1])], float)


def base_chi_mode(data, tau, mode_index):
    a, _, Q = m.bg_eval(data, float(tau))[:3]
    alpha = float(m.mode_values(data, float(tau), "alpha")[mode_index])
    theta = float(m.mode_values(data, float(tau), "theta")[mode_index])
    k = float(m.K_MPC[mode_index])
    return float(Q * (a * theta / (k * k) + alpha))


def advance_to(data, source_spline, current, target, z, zp, hmain):
    t = float(current)
    target = float(target)
    if target < t - 1e-12:
        raise RuntimeError("checkpoint precedes initialized bath state")
    while t < target - 1e-12:
        tn = min(target, t + hmain)
        s0 = np.asarray([float(source_spline(t))], float)
        s1 = np.asarray([float(source_spline(tn))], float)
        z, zp = c.bath_advance(data, t, tn, z, zp, s0, s1, ORDER)
        if not (np.all(np.isfinite(z)) and np.all(np.isfinite(zp))):
            raise FloatingPointError(f"nonfinite offline bath at tau={tn}")
        t = tn
    return t, z, zp


def main() -> int:
    out_json = ROOT / "results" / "c3_direct_bath_bridge.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    try:
        clear_env()
        os.environ["OMP_NUM_THREADS"] = "1"

        # This is the exact base-data path used by the D2C6C offline solver.
        data = m.prepare_class_data()
        hmain = (float(data["t1"]) - float(data["t0"])) / 4096.0

        from classy import Class
        cc = Class()
        params = base.params(True)
        cc.set(params)
        cc.compute()
        try:
            histories, _ = base.d2a.scalar_histories(cc.get_perturbations())
            if len(histories) != 6:
                raise RuntimeError(f"expected six Stage-A scalar histories, got {len(histories)}")

            omega_ratio, weights = c.BATH_DATA[ORDER]
            omega_ratio = np.asarray(omega_ratio, float)
            weights = np.asarray(weights, float)
            if omega_ratio.size != ORDER or weights.size != ORDER:
                raise RuntimeError("order-39 bath definition size mismatch")
            if not np.isclose(np.sum(weights), 1.0, rtol=0.0, atol=1e-12):
                raise RuntimeError(f"order-39 weight sum is {np.sum(weights)}")
            omega = c.H0_MPC * omega_ratio / TAUH0

            mode_reports = []
            all_points = []
            global_max = {"z": 0.0, "zp": 0.0, "B": 0.0, "chi": 0.0}

            for imode, raw in enumerate(histories):
                kt = base.pick(raw, ("tau [Mpc]", "tau", "tau[Mpc]"))
                ka = base.pick(raw, ("a", "scale factor"))
                kalpha = base.pick(raw, ("alpha_aest", "alpha"))
                kth = base.pick(raw, ("theta_cdm", "t_cdm"))
                kforce = base.pick(raw, ("eta0_tangent_force_aest",))

                tau, take = sorted_unique_indices(raw[kt])
                aa = np.asarray(raw[ka], float)[take]
                alpha = np.asarray(raw[kalpha], float)[take]
                theta = np.asarray(raw[kth], float)[take]
                force = np.asarray(raw[kforce], float)[take]
                q = np.column_stack([
                    np.asarray(raw[f"mem_q_aest_{j:02d}"], float)[take]
                    for j in range(ORDER)
                ])
                p = np.column_stack([
                    np.asarray(raw[f"mem_p_aest_{j:02d}"], float)[take]
                    for j in range(ORDER)
                ])
                if tau.size < 100 or not np.all(np.diff(tau) > 0):
                    raise RuntimeError(f"mode {imode} dense history is not usable")
                if not (np.all(np.isfinite(q)) and np.all(np.isfinite(p))):
                    raise RuntimeError(f"mode {imode} has nonfinite CLASS bath states")

                k = float(m.K_MPC[imode])
                Q = np.asarray(data["bg"]["Q"](aa), float)
                chi = Q * (aa * theta / (k * k) + alpha)
                source = chi / aa
                source_spline = PchipInterpolator(tau, source, extrapolate=False)

                factor = omega / (k * np.sqrt(weights))
                z_class_all = q * factor[None, :]
                zp_class_all = p * factor[None, :]

                # Common-state initialization: no prehistory ambiguity remains after tau_first.
                z = z_class_all[0].copy()[:, None]
                zp = zp_class_all[0].copy()[:, None]
                current = float(tau[0])

                cp_rows = []
                for iz, (redshift, target) in enumerate(zip(m.CHECK_Z, data["tau_check"])):
                    target = float(target)
                    if target < tau[0] - 1e-10 or target > tau[-1] + 1e-10:
                        raise RuntimeError(
                            f"mode {imode} checkpoint z={redshift} outside dense CLASS history"
                        )
                    current, z, zp = advance_to(
                        data, source_spline, current, target, z, zp, hmain
                    )
                    qcp = interp_columns(target, tau, q)
                    pcp = interp_columns(target, tau, p)
                    zcp = factor * qcp
                    zpcp = factor * pcp
                    acp = float(np.interp(target, tau, aa))
                    chicp = float(np.interp(target, tau, chi))
                    fcp = float(np.interp(target, tau, force))
                    chibase = base_chi_mode(data, target, imode)

                    zrel = rel_l2(z[:, 0], zcp)
                    zprel = rel_l2(zp[:, 0], zpcp)
                    Bclass = float(
                        np.sum(weights * chicp)
                        - np.sum(np.sqrt(weights) * (acp * omega / k) * qcp)
                    )
                    Boff = float(chicp - acp * np.dot(weights, z[:, 0]))
                    Qcp = float(data["bg"]["Q"](acp))
                    f_from_B = -0.5 * acp * Qcp * Bclass / m.static.KB
                    force_rel = point_rel(fcp, f_from_B, 1e-14 * max(abs(fcp), abs(f_from_B), 1.0))

                    cp_rows.append({
                        "z": float(redshift),
                        "tau": target,
                        "z_state_rel": zrel,
                        "zp_state_rel": zprel,
                        "B_class": Bclass,
                        "B_offline": Boff,
                        "chi_class": chicp,
                        "chi_offline_base": chibase,
                        "force_output": fcp,
                        "force_from_B": f_from_B,
                        "force_B_relative_descriptive": force_rel,
                    })

                bscale = max(max(abs(x["B_class"]) for x in cp_rows), 1e-300)
                chiscale = max(max(abs(x["chi_class"]) for x in cp_rows), 1e-300)
                mode_max = {"z": 0.0, "zp": 0.0, "B": 0.0, "chi": 0.0}
                for row in cp_rows:
                    brel = point_rel(
                        row["B_offline"], row["B_class"], 1e-12 * bscale
                    )
                    chirel = point_rel(
                        row["chi_offline_base"], row["chi_class"], 1e-12 * chiscale
                    )
                    row["B_rel"] = brel
                    row["chi_rel"] = chirel
                    mode_max["z"] = max(mode_max["z"], row["z_state_rel"])
                    mode_max["zp"] = max(mode_max["zp"], row["zp_state_rel"])
                    mode_max["B"] = max(mode_max["B"], brel)
                    mode_max["chi"] = max(mode_max["chi"], chirel)
                    print(
                        f"BATH_POINT mode={imode} k_mpc={k:.12e} z={row['z']:g} "
                        f"Z_STATE_REL={row['z_state_rel']:.12e} "
                        f"ZP_STATE_REL={row['zp_state_rel']:.12e} "
                        f"B_REL={brel:.12e} CHI_REL={chirel:.12e}",
                        flush=True,
                    )
                    all_points.append({"mode": imode, "k_mpc": k, **row})

                for key in global_max:
                    global_max[key] = max(global_max[key], mode_max[key])
                print(
                    f"BATH_MODE mode={imode} k_mpc={k:.12e} rows={tau.size} "
                    f"tau_first={tau[0]:.12e} max_Z={mode_max['z']:.12e} "
                    f"max_ZP={mode_max['zp']:.12e} max_B={mode_max['B']:.12e} "
                    f"max_CHI={mode_max['chi']:.12e}",
                    flush=True,
                )
                mode_reports.append({
                    "mode": imode,
                    "k_mpc": k,
                    "rows": int(tau.size),
                    "tau_first": float(tau[0]),
                    "tau_last": float(tau[-1]),
                    "max": mode_max,
                    "points": cp_rows,
                })
        finally:
            cc.struct_cleanup()
            cc.empty()
            clear_env()

        source_pass = bool(global_max["chi"] <= CHI_GATE)
        state_pass = bool(global_max["z"] <= Z_GATE and global_max["zp"] <= ZP_GATE)
        residual_pass = bool(global_max["B"] <= B_GATE)
        print(
            f"BATH_GLOBAL max_Z={global_max['z']:.12e} max_ZP={global_max['zp']:.12e} "
            f"max_B={global_max['B']:.12e} max_CHI={global_max['chi']:.12e}",
            flush=True,
        )
        print(f"SOURCE_BRIDGE_PASS={source_pass}", flush=True)
        print(f"BATH_STATE_BRIDGE_PASS={state_pass}", flush=True)
        print(f"B_RESIDUAL_BRIDGE_PASS={residual_pass}", flush=True)

        if not source_pass:
            classification = "C3_BATH_BRIDGE_INCOMPLETE"
            code = 3
        elif state_pass and residual_pass:
            classification = "C3_BATH_BRIDGE_PASS"
            code = 0
        else:
            classification = "C3_BATH_BRIDGE_MISMATCH_IDENTIFIED"
            code = 0

        report = {
            "classification": classification,
            "physical_eta": 0.0,
            "tauH0": TAUH0,
            "bath_order": ORDER,
            "mapping": "z_j = omega_j q_j / (k sqrt(w_j))",
            "offline_initialization": "transformed CLASS q_j,p_j at each mode tau_first",
            "offline_step": "existing D2C6C bath_advance with main-step scale Nx128/Nstep4096",
            "global_max": global_max,
            "source_bridge_pass": source_pass,
            "bath_state_bridge_pass": state_pass,
            "B_residual_bridge_pass": residual_pass,
            "thresholds": {
                "Z_STATE_REL": Z_GATE,
                "ZP_STATE_REL": ZP_GATE,
                "B_REL": B_GATE,
                "CHI_REL": CHI_GATE,
            },
            "modes": mode_reports,
            "finite_positive_eta_licensed": False,
        }
        out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"CLASSIFICATION={classification}", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return code

    except Exception as exc:
        report = {
            "classification": "C3_BATH_BRIDGE_INCOMPLETE",
            "error": f"{type(exc).__name__}: {exc}",
            "finite_positive_eta_licensed": False,
        }
        out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"C3_BATH_BRIDGE_ERROR {type(exc).__name__}: {exc}", flush=True)
        print("CLASSIFICATION=C3_BATH_BRIDGE_INCOMPLETE", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
