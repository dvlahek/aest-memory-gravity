#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import evolving_flrw_weyl_bridge_r2 as r2
from nl1c6d2c6b import all27_physical_nonlinear_trajectories as d2b

m = r2.m
static = m.static

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
GAUSS1D_RESULT_LOCK = "05e38b273f91eb04b7b4c8753731017d0ed839c1"
GEOM_RESULT_LOCK = "ca6a102196055e27dc2b31379285bfc7aea1a35b"
SAT_RESULT_LOCK = "f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f"
HISTORICAL_TRANSFER_FAIL_LOCK = "b7bb0aef90ec935821f4dc1a63db0d79966a15f8"
R1_PHASE_RESULT_LOCK = "20679c5274e936037c226904d40c9d6779b00a49"
PREDATA_LOCK = "82cfb13a782aea71e0a8e3a7433f9729f47c048a"

PASS = "FULLJ_DENSE_RADIAL_WEYL_EXTENSION_PASS"
FAIL = "FULLJ_DENSE_RADIAL_WEYL_EXTENSION_FAIL"
INCOMPLETE = "FULLJ_DENSE_RADIAL_WEYL_EXTENSION_INCOMPLETE"

REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}
CHECK_Z = np.asarray(m.CHECK_Z, float)
K0_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
N_EMBED = 10
NX = r2.NX
NSTEP = r2.NSTEP

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
INITIAL_CLASS_GATE = 5.0e-3
PHASE_GLOBAL_GATE = 1.0e-8
PHASE_ABS_GATE = 1.0e-8
POWER_PROJ_GATE = 1.0e-12
SAT_GATE = 2.0e-2
ANCHOR_MED_GATE = 5.0e-4
ANCHOR_MAX_GATE = 5.0e-3
HOLD_T_L2_GATE = 3.0e-2
HOLD_P_L2_GATE = 5.0e-2
HOLD_P_PEAK_GATE = 1.0e-1
FINE_T_L2_GATE = 3.0e-2
FINE_P_L2_GATE = 5.0e-2
FINE_P_PEAK_GATE = 1.0e-1
ALG_GATE = 1.0e-12

ORIGINAL_JSON = ROOT / "results/fullj_isotropic_weyl_transfer_nodes.json"
R1_PHASE_JSON = ROOT / "results/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit.json"


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def nested_grids():
    k1 = list(K0_H)
    k2 = list(K0_H)
    for a, b in zip(K0_H[:-1], K0_H[1:]):
        k1.append(0.5 * (a + b))
        k2.extend([a + 0.25 * (b - a), 0.5 * (a + b), a + 0.75 * (b - a)])
    return K0_H.copy(), np.asarray(sorted(set(np.round(k1, 14))), float), np.asarray(sorted(set(np.round(k2, 14))), float)


def interpolation_probe(kh: np.ndarray):
    x0 = np.log(K0_H)
    amp0 = np.asarray(static.MODE_AMP, float)
    ph0 = np.asarray(static.PHASE, float)
    amp = np.exp(np.interp(np.log(kh), x0, np.log(amp0)))
    phase = np.interp(kh, K0_H, ph0)
    return amp, phase


def rel_scalar(a, b) -> float:
    aa = float(a)
    bb = float(b)
    return float(abs(aa - bb) / max(abs(aa), abs(bb), 1.0e-300))


def health(run) -> dict:
    out = {
        "finite": bool(run.get("finite", False)),
        "canonical_max": float("inf"),
        "metric_max": {"hamiltonian": float("inf"), "momentum": float("inf"), "shear": float("inf")},
    }
    cps = run.get("checkpoints", [])
    if not out["finite"] or len(cps) != len(CHECK_Z):
        return out
    out["canonical_max"] = max(float(cp["canonical_constraint"]) for cp in cps)
    mm = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
    for cp in cps:
        cc = cp["metric"]["metric_correction"]["constraint"]
        for key in mm:
            mm[key] = max(mm[key], float(cc[key]))
    out["metric_max"] = mm
    return out


def single_basis(nx: int, nmode: int, k_mpc: float, amp: float, phase: float, box: float):
    x = np.arange(nx) * box / nx
    C = np.zeros((nmode, nx), float)
    return C, x


def run_single_mode(data, idx: int, k_mpc: float, amp: float, phase: float):
    nmode = len(data["modes"])
    box = 2.0 * np.pi * float(N_EMBED) / float(k_mpc)
    original_cos = m.cos_matrix
    original_box = float(static.BOX)

    def custom_cos_matrix(nx):
        x = np.arange(nx) * box / nx
        C = np.zeros((nmode, nx), float)
        C[idx, :] = float(amp) * np.cos(float(k_mpc) * x + float(phase))
        return C

    d2b.set_member(REFERENCE_MEMBER)
    m.cos_matrix = custom_cos_matrix
    static.BOX = box
    try:
        run = r2.integrate_combined_r2(data, NX, NSTEP, True)
    finally:
        m.cos_matrix = original_cos
        static.BOX = original_box
    return run, box


def transfer_from_run(run, amp: float, phase: float):
    vals = []
    for cp in run["checkpoints"]:
        w = np.asarray(cp["metric"]["weyl"], float)
        wh = np.fft.fft(w) / float(w.size)
        vals.append(2.0 * wh[N_EMBED] * np.exp(-1j * float(phase)) / float(amp))
    return np.asarray(vals, complex)


def saturation_residuals(data, run, box: float):
    original_box = float(static.BOX)
    static.BOX = float(box)
    try:
        ops = m.spec_ops(NX)
        grad, lap, _, div = ops
        vals = []
        for cp in run["checkpoints"]:
            tau = float(cp["tau"])
            a, H, Q, KQ, KQQ, Z, Qdot = m.bg_eval(data, tau)
            chi = np.asarray(cp["y"][1], float)
            g = grad(chi)
            x = static.ACC_CONV * np.abs(g) / a
            je = d2b.j_eff(x, Z)
            lnl = div((1.0 + je) * g)
            lsat = 2.0 * lap(chi)
            scale = max(float(np.linalg.norm(lnl)), float(np.linalg.norm(lsat)), 1.0e-300)
            vals.append(float(np.linalg.norm(lnl - lsat) / scale))
        return np.asarray(vals, float)
    finally:
        static.BOX = original_box


def primordial(k_mpc):
    kk = np.asarray(k_mpc, float)
    return float(static.AS) * (kk / float(static.KPIV)) ** (float(static.NS) - 1.0)


def index_for(grid, value):
    ii = np.where(np.isclose(grid, float(value), rtol=0.0, atol=5.0e-13))[0]
    if len(ii) != 1:
        raise RuntimeError(f"could not resolve nested-grid node {value}")
    return int(ii[0])


def err_metrics(tpred, ttrue, kh):
    tp = np.asarray(tpred, float)
    tt = np.asarray(ttrue, float)
    kh = np.asarray(kh, float)
    km = kh * float(static.h)
    pr = primordial(km)
    pp = 2.0 * np.pi**2 * pr * tp**2 / (km**3)
    pt = 2.0 * np.pi**2 * pr * tt**2 / (km**3)
    et = float(np.linalg.norm(tp - tt) / max(float(np.linalg.norm(tt)), 1.0e-300))
    ep = float(np.linalg.norm(pp - pt) / max(float(np.linalg.norm(pt)), 1.0e-300))
    epeak = float(np.max(np.abs(pp - pt)) / max(float(np.max(pt)), 1.0e-300))
    return {"transfer_L2": et, "power_L2": ep, "power_peak": epeak}


def interp_transfer(k_nodes_h, t_nodes, k_eval_h):
    sp = PchipInterpolator(np.log(np.asarray(k_nodes_h, float)), np.asarray(t_nodes, float), extrapolate=False)
    return np.asarray(sp(np.log(np.asarray(k_eval_h, float))), float)


def load_locked_results():
    if not ORIGINAL_JSON.exists() or not R1_PHASE_JSON.exists():
        missing = [str(p.relative_to(ROOT)) for p in (ORIGINAL_JSON, R1_PHASE_JSON) if not p.exists()]
        raise FileNotFoundError(", ".join(missing))
    orig = json.loads(ORIGINAL_JSON.read_text())
    phase = json.loads(R1_PHASE_JSON.read_text())
    if orig.get("classification") != "FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_FAIL":
        raise RuntimeError("historical six-node JSON no longer has locked FAIL classification")
    if phase.get("classification") != "FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_R1_PHASE_AUDIT_PASS":
        raise RuntimeError("R1 zero-safe phase JSON is not locked PASS")
    return orig, phase


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_dense_radial_weyl_extension.json")
    ap.add_argument("--npz-out", default="results/fullj_dense_radial_weyl_extension.npz")
    ap.add_argument("--csv-out", default="results/fullj_dense_radial_weyl_extension.csv")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock": is_ancestor(GAUSS1D_RESULT_LOCK),
        "geometry_result_lock": is_ancestor(GEOM_RESULT_LOCK),
        "saturated_closure_result_lock": is_ancestor(SAT_RESULT_LOCK),
        "historical_transfer_fail_lock": is_ancestor(HISTORICAL_TRANSFER_FAIL_LOCK),
        "r1_phase_result_lock": is_ancestor(R1_PHASE_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }

    k0, k1, k2 = nested_grids()
    amp2, phase2 = interpolation_probe(k2)
    frozen_setup = bool(
        np.array_equal(CHECK_Z, np.asarray([6.0,5.0,4.0,3.0,2.0,1.5,1.0,0.5,0.2]))
        and np.array_equal(k0, K0_H)
        and len(k1) == 11 and len(k2) == 21
        and N_EMBED == 10 and NX == 128 and NSTEP == 4096
        and REFERENCE_MEMBER == {"sigma": 0, "kind": "simple", "beta0": 1.0}
    )

    try:
        orig, phase_audit = load_locked_results()
    except Exception as exc:
        result = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "reason": str(exc)}
        Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_DENSE_RADIAL_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen_setup:
        result = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "frozen_setup": frozen_setup, "reason": "missing locked ancestry or frozen setup mismatch"}
        Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_DENSE_RADIAL_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    print("FULLJ_DENSE_RADIAL_START", flush=True)
    print("FULLJ_DENSE_RADIAL_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_DENSE_RADIAL_GRIDS=" + json.dumps({"K0": k0.tolist(), "K1": k1.tolist(), "K2": k2.tolist()}), flush=True)

    original_kmpc = np.asarray(m.K_MPC, float).copy()
    original_kh = np.asarray(getattr(m, "K_H", K0_H), float).copy()
    k2_mpc = k2 * float(static.h)
    m.K_MPC = k2_mpc.copy()
    m.K_H = k2.copy()
    try:
        data = r2.r0.prepare_bridge_data()
    finally:
        # Keep the dense globals through integrations; restore only after all runs.
        pass

    T = np.full((len(CHECK_Z), len(k2)), np.nan + 1j*np.nan, complex)
    Tc = np.full((len(CHECK_Z), len(k2)), np.nan, float)
    sat = np.full((len(CHECK_Z), len(k2)), np.nan, float)
    health_rows = []
    boxes = []

    try:
        for j, kh in enumerate(k2):
            run, box = run_single_mode(data, j, float(k2_mpc[j]), float(amp2[j]), float(phase2[j]))
            hh = health(run)
            health_rows.append({"k_h_Mpc_inv": float(kh), "box_Mpc": float(box), **hh})
            boxes.append(float(box))
            if not hh["finite"]:
                raise RuntimeError(f"dense single-mode run k/h={kh:g} incomplete")
            T[:, j] = transfer_from_run(run, float(amp2[j]), float(phase2[j]))
            sat[:, j] = saturation_residuals(data, run, box)
            for iz, tau in enumerate(np.asarray(data["tau_check"], float)):
                Tc[iz, j] = float(m.mode_values(data, float(tau), "phi")[j] + m.mode_values(data, float(tau), "psi_bridge")[j])
            print(
                f"FULLJ_DENSE_RADIAL_NODE {j+1:02d}/{len(k2)} k_h={kh:.8f} "
                f"canonical={hh['canonical_max']:.3e} satMax={float(np.max(sat[:,j])):.3e}",
                flush=True,
            )
    finally:
        m.K_MPC = original_kmpc
        m.K_H = original_kh

    realT = np.real(T)
    imagT = np.imag(T)
    pr2 = primordial(k2_mpc)
    delta2 = pr2[None, :] * realT**2
    p3d = 2.0 * np.pi**2 * delta2 / (k2_mpc[None, :]**3)
    delta2_back = p3d * (k2_mpc[None, :]**3) / (2.0 * np.pi**2)
    alg_res = float(np.linalg.norm(delta2 - delta2_back) / max(float(np.linalg.norm(delta2)), 1.0e-300))

    all_health = all(
        bool(q["finite"])
        and float(q["canonical_max"]) <= CANONICAL_GATE
        and all(float(v) <= METRIC_GATE for v in q["metric_max"].values())
        for q in health_rows
    )

    initial_rel = np.abs(T[0, :] - Tc[0, :]) / np.maximum(np.abs(Tc[0, :]), 1.0e-300)
    phase_global = float(np.linalg.norm(imagT) / max(float(np.linalg.norm(T)), 1.0e-300))
    phase_abs = float(np.max(np.abs(imagT)))
    p_complex = pr2[None, :] * np.abs(T)**2
    proj_change = np.abs(p_complex - delta2) / np.maximum(p_complex, delta2, 1.0e-300)
    proj_change_max = float(np.max(proj_change))
    sat_max = float(np.max(sat))

    locked_map = {}
    for row in orig.get("transfer_nodes", []):
        locked_map[(round(float(row["k_h_Mpc_inv"]), 12), round(float(row["z"]), 12))] = float(row["T_W_R2_real"])
    anchor_diffs = []
    anchor_rows = []
    for kh in k0:
        j = index_for(k2, kh)
        for iz, z in enumerate(CHECK_Z):
            key = (round(float(kh), 12), round(float(z), 12))
            if key not in locked_map:
                raise RuntimeError(f"locked original JSON missing anchor {key}")
            old = locked_map[key]
            q = rel_scalar(realT[iz, j], old)
            anchor_diffs.append(q)
            anchor_rows.append({"k_h_Mpc_inv": float(kh), "z": float(z), "new_T": float(realT[iz,j]), "locked_T": old, "relative_difference": q})
    anchor_med = float(np.median(anchor_diffs))
    anchor_max = float(np.max(anchor_diffs))

    idx0 = np.asarray([index_for(k2, q) for q in k0], int)
    idx1 = np.asarray([index_for(k2, q) for q in k1], int)
    hold_idx = np.asarray([j for j, q in enumerate(k2) if not np.any(np.isclose(k1, q, rtol=0.0, atol=5.0e-13))], int)
    hold_k = k2[hold_idx]
    hold_rows = []
    e0_t, e1_t, e0_p, e1_p, e1_peak = [], [], [], [], []
    improve_t = 0
    improve_p = 0
    for iz, z in enumerate(CHECK_Z):
        true = realT[iz, hold_idx]
        pred0 = interp_transfer(k0, realT[iz, idx0], hold_k)
        pred1 = interp_transfer(k1, realT[iz, idx1], hold_k)
        q0 = err_metrics(pred0, true, hold_k)
        q1 = err_metrics(pred1, true, hold_k)
        e0_t.append(q0["transfer_L2"]); e1_t.append(q1["transfer_L2"])
        e0_p.append(q0["power_L2"]); e1_p.append(q1["power_L2"]); e1_peak.append(q1["power_peak"])
        improve_t += int(q1["transfer_L2"] < q0["transfer_L2"])
        improve_p += int(q1["power_L2"] < q0["power_L2"])
        hold_rows.append({"z": float(z), "level0": q0, "level1": q1})

    logfine = np.linspace(np.log(float(k2[0])), np.log(float(k2[-1])), 401)
    kfine = np.exp(logfine)
    fine_rows = []
    f01_t, f12_t, f01_p, f12_p, f12_peak = [], [], [], [], []
    final_T = np.empty((len(CHECK_Z), len(kfine)), float)
    final_P = np.empty_like(final_T)
    for iz, z in enumerate(CHECK_Z):
        t0 = interp_transfer(k0, realT[iz, idx0], kfine)
        t1 = interp_transfer(k1, realT[iz, idx1], kfine)
        t2 = interp_transfer(k2, realT[iz, :], kfine)
        q01 = err_metrics(t0, t1, kfine)
        q12 = err_metrics(t1, t2, kfine)
        f01_t.append(q01["transfer_L2"]); f12_t.append(q12["transfer_L2"])
        f01_p.append(q01["power_L2"]); f12_p.append(q12["power_L2"]); f12_peak.append(q12["power_peak"])
        final_T[iz, :] = t2
        kmfine = kfine * float(static.h)
        final_P[iz, :] = 2.0 * np.pi**2 * primordial(kmfine) * t2**2 / (kmfine**3)
        fine_rows.append({"z": float(z), "K0_to_K1": q01, "K1_to_K2": q12})

    all_power_finite = bool(
        np.all(np.isfinite(delta2)) and np.all(np.isfinite(p3d)) and np.all(np.isfinite(final_P))
        and np.all(delta2 >= 0.0) and np.all(p3d >= 0.0) and np.all(final_P >= 0.0)
    )

    gates = {
        "G1_locked_provenance_setup": bool(all(ancestry.values()) and frozen_setup),
        "G2_finite_constraint_health": bool(all_health),
        "G3_initial_CLASS_normalization": bool(float(np.max(initial_rel)) <= INITIAL_CLASS_GATE),
        "G4_zero_safe_phase_consistency": bool(phase_global <= PHASE_GLOBAL_GATE and phase_abs <= PHASE_ABS_GATE and proj_change_max <= POWER_PROJ_GATE),
        "G5_dense_saturated_closure": bool(sat_max <= SAT_GATE),
        "G6_anchor_recovery": bool(anchor_med <= ANCHOR_MED_GATE and anchor_max <= ANCHOR_MAX_GATE),
        "G7_level1_direct_holdout_accuracy": bool(max(e1_t) <= HOLD_T_L2_GATE and max(e1_p) <= HOLD_P_L2_GATE and max(e1_peak) <= HOLD_P_PEAK_GATE),
        "G8_refinement_improvement": bool(improve_t >= 7 and improve_p >= 7 and np.median(e1_t) < np.median(e0_t) and np.median(e1_p) < np.median(e0_p)),
        "G9_fine_grid_K1_to_K2_convergence": bool(max(f12_t) <= FINE_T_L2_GATE and max(f12_p) <= FINE_P_L2_GATE and max(f12_peak) <= FINE_P_PEAK_GATE and np.median(f12_t) < np.median(f01_t) and np.median(f12_p) < np.median(f01_p)),
        "G10_power_sanity": bool(all_power_finite and alg_res <= ALG_GATE),
    }
    classification = PASS if all(gates.values()) else FAIL

    summary = {
        "initial_CLASS_max_relative_error": float(np.max(initial_rel)),
        "global_quadrature_relL2": phase_global,
        "absolute_imaginary_max": phase_abs,
        "real_projection_power_change_max": proj_change_max,
        "dense_saturation_max": sat_max,
        "anchor_recovery_median": anchor_med,
        "anchor_recovery_max": anchor_max,
        "holdout_level0_transfer_L2_median": float(np.median(e0_t)),
        "holdout_level1_transfer_L2_median": float(np.median(e1_t)),
        "holdout_level1_transfer_L2_max": float(np.max(e1_t)),
        "holdout_level0_power_L2_median": float(np.median(e0_p)),
        "holdout_level1_power_L2_median": float(np.median(e1_p)),
        "holdout_level1_power_L2_max": float(np.max(e1_p)),
        "holdout_level1_power_peak_max": float(np.max(e1_peak)),
        "holdout_improved_redshifts_transfer": int(improve_t),
        "holdout_improved_redshifts_power": int(improve_p),
        "fine_K0_to_K1_transfer_L2_median": float(np.median(f01_t)),
        "fine_K1_to_K2_transfer_L2_median": float(np.median(f12_t)),
        "fine_K1_to_K2_transfer_L2_max": float(np.max(f12_t)),
        "fine_K0_to_K1_power_L2_median": float(np.median(f01_p)),
        "fine_K1_to_K2_power_L2_median": float(np.median(f12_p)),
        "fine_K1_to_K2_power_L2_max": float(np.max(f12_p)),
        "fine_K1_to_K2_power_peak_max": float(np.max(f12_peak)),
        "power_identity_relative_residual": alg_res,
    }

    rows = []
    for iz, z in enumerate(CHECK_Z):
        for j, kh in enumerate(k2):
            rows.append({
                "z": float(z),
                "k_h_Mpc_inv": float(kh),
                "k_Mpc_inv": float(k2_mpc[j]),
                "probe_amp": float(amp2[j]),
                "phase": float(phase2[j]),
                "T_real": float(realT[iz,j]),
                "T_imag": float(imagT[iz,j]),
                "T_CLASS": float(Tc[iz,j]),
                "eps_sat": float(sat[iz,j]),
                "Delta_W2": float(delta2[iz,j]),
                "P_W_Mpc3": float(p3d[iz,j]),
            })

    result = {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": git_head(),
        "ancestry": ancestry,
        "reference_member": REFERENCE_MEMBER,
        "redshifts": CHECK_Z.tolist(),
        "K0_h_Mpc_inv": k0.tolist(),
        "K1_h_Mpc_inv": k1.tolist(),
        "K2_h_Mpc_inv": k2.tolist(),
        "n_embed": N_EMBED,
        "NX": NX,
        "NSTEP": NSTEP,
        "health": health_rows,
        "anchor_recovery": anchor_rows,
        "holdout_rows": hold_rows,
        "fine_convergence_rows": fine_rows,
        "summary": summary,
        "gates": gates,
        "rows": rows,
        "THREE_D_DENSE_RADIAL_WEYL_NODES_LICENSED": bool(classification == PASS),
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED": bool(classification == PASS),
        "BOUNDED_K_H_MPC_MIN": 0.03,
        "BOUNDED_K_H_MPC_MAX": 0.20,
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
        "scope": "direct 21-node nested radial extension and PCHIP convergence audit on 0.03<=k/h<=0.20 Mpc^-1; no k-range extrapolation or lensing",
    }

    jout = Path(args.json_out); jout.parent.mkdir(parents=True, exist_ok=True)
    nout = Path(args.npz_out); cout = Path(args.csv_out)
    jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(
        nout,
        redshifts=CHECK_Z,
        K0_h_Mpc_inv=k0,
        K1_h_Mpc_inv=k1,
        K2_h_Mpc_inv=k2,
        T_real=realT,
        T_imag=imagT,
        T_CLASS=Tc,
        eps_sat=sat,
        Delta_W2=delta2,
        P_W_Mpc3=p3d,
        fine_k_h_Mpc_inv=kfine,
        fine_T=final_T,
        fine_P_W_Mpc3=final_P,
    )
    with cout.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wr.writeheader(); wr.writerows(rows)

    print("FULLJ_DENSE_RADIAL_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_DENSE_RADIAL_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_DENSE_RADIAL_CLASSIFICATION=" + classification, flush=True)
    print("THREE_D_DENSE_RADIAL_WEYL_NODES_LICENSED=" + str(bool(classification == PASS)), flush=True)
    print("THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=" + str(bool(classification == PASS)), flush=True)
    print("THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_DENSE_RADIAL_JSON=" + str(jout), flush=True)
    print("FULLJ_DENSE_RADIAL_NPZ=" + str(nout), flush=True)
    print("FULLJ_DENSE_RADIAL_CSV=" + str(cout), flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
