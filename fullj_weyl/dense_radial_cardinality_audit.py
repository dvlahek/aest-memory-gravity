#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Importing the repaired R2 wrapper also imports the dynamic dense-history
# loader repair used by the completed 41-mode milestone.
from fullj_weyl import dense_radial_class_residual_r2_r1 as repaired

res = repaired.base
dense = res.base
r2 = res.r2
m = res.m
static = res.static

DENSE_FAIL_RESULT_LOCK = "55495cc968082f1cf6638785f7609c787971835c"
RESIDUAL_R2_RESULT_LOCK = "4d87865a8e45985388dfab2b9d8922faa9290f7f"
R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
R1_PHASE_RESULT_LOCK = "20679c5274e936037c226904d40c9d6779b00a49"
PREDATA_LOCK = "76d2b923935278317022ab6ef5d036769b91500b"

PASS = "FULLJ_DENSE_RADIAL_CARDINALITY_AUDIT_PASS"
FAIL = "FULLJ_DENSE_RADIAL_CARDINALITY_AUDIT_FAIL"
INCOMPLETE = "FULLJ_DENSE_RADIAL_CARDINALITY_AUDIT_INCOMPLETE"

K_AUDIT = np.asarray([0.035, 0.040, 0.100, 0.150, 0.1625, 0.175], float)
CHECK_Z = np.asarray(res.CHECK_Z, float)
REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}
N_EMBED = 10
NX = r2.NX
NSTEP = r2.NSTEP

RESIDUAL_JSON = ROOT / "results/fullj_dense_radial_class_residual_r2.json"

CLASS_MED_GATE = 1.0e-8
CLASS_MAX_GATE = 1.0e-5
CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
PHASE_GLOBAL_GATE = 1.0e-8
PHASE_ABS_GATE = 1.0e-8
POWER_PROJ_GATE = 1.0e-12
TRANSFER_GLOBAL_GATE = 1.0e-5
TRANSFER_PER_K_GATE = 5.0e-5
POWER_GLOBAL_GATE = 1.0e-4
POWER_PER_K_GATE = 5.0e-4
SAT_NEW_GATE = 2.0e-2
SAT_ABS_DIFF_GATE = 1.0e-4
SAT_REL_L2_GATE = 1.0e-3


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel_scalar(a: float, b: float) -> float:
    aa = float(a); bb = float(b)
    return float(abs(aa - bb) / max(abs(aa), abs(bb), 1.0e-300))


def rel_l2(a, b) -> float:
    aa = np.asarray(a, float); bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(bb)), 1.0e-300))


def load_residual_fail() -> dict:
    if not RESIDUAL_JSON.exists():
        raise FileNotFoundError(str(RESIDUAL_JSON.relative_to(ROOT)))
    d = json.loads(RESIDUAL_JSON.read_text())
    if d.get("classification") != "FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_FAIL":
        raise RuntimeError("completed residual-R2 JSON does not preserve locked FAIL")
    g = d.get("gates", {})
    want_true = [
        "R2_G1_locked_provenance_setup",
        "R2_G2_completed_K2_state_integrity",
        "R2_G3_CLASS_cross_run_consistency",
        "R2_G4_new_H3_direct_health",
        "R2_G5_new_H3_initial_CLASS_normalization",
        "R2_G6_new_H3_zero_safe_phase",
        "R2_G11_power_sanity",
    ]
    want_false = [
        "R2_G7_new_H3_saturated_closure",
        "R2_G8_independent_K2_residual_holdout_accuracy",
        "R2_G9_residual_refinement_improvement",
        "R2_G10_K2_to_K3_residual_convergence",
    ]
    if not all(g.get(x) is True for x in want_true) or not all(g.get(x) is False for x in want_false):
        raise RuntimeError("completed residual-R2 JSON gate state differs from locked FAIL")
    return d


def old_saturation(old: dict, k2: np.ndarray) -> np.ndarray:
    out = np.full((len(CHECK_Z), len(k2)), np.nan, float)
    for row in old.get("rows", []):
        z = float(row["z"]); kh = float(row["k_h_Mpc_inv"])
        if not np.any(np.isclose(kh, k2, rtol=0.0, atol=5.0e-13)):
            continue
        out[res.ix(CHECK_Z, z), res.ix(k2, kh)] = float(row["eps_sat"])
    if not np.all(np.isfinite(out)):
        raise RuntimeError("stored K2 saturation grid incomplete")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_dense_radial_cardinality_audit.json")
    ap.add_argument("--npz-out", default="results/fullj_dense_radial_cardinality_audit.npz")
    ap.add_argument("--csv-out", default="results/fullj_dense_radial_cardinality_audit.csv")
    args = ap.parse_args()

    ancestry = {
        "dense_fail_result_lock": is_ancestor(DENSE_FAIL_RESULT_LOCK),
        "residual_r2_result_lock": is_ancestor(RESIDUAL_R2_RESULT_LOCK),
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "r1_phase_result_lock": is_ancestor(R1_PHASE_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }

    k1, k2, k3, h3 = res.grids()
    frozen = bool(
        np.array_equal(K_AUDIT, np.asarray([0.035,0.040,0.100,0.150,0.1625,0.175], float))
        and len(k3) == 41 and len(k2) == 21 and len(h3) == 20
        and N_EMBED == 10 and NX == 128 and NSTEP == 4096
        and REFERENCE_MEMBER == {"sigma":0,"kind":"simple","beta0":1.0}
        and np.array_equal(CHECK_Z, np.asarray([6.0,5.0,4.0,3.0,2.0,1.5,1.0,0.5,0.2], float))
    )

    try:
        residual_fail = load_residual_fail()
        old, T21, Tc21 = res.load_old(k2)
        S21 = old_saturation(old, k2)
    except Exception as exc:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "reason": str(exc)}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_CARDINALITY_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "frozen_setup": frozen}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_CARDINALITY_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    print("FULLJ_CARDINALITY_START", flush=True)
    print("FULLJ_CARDINALITY_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_CARDINALITY_K_AUDIT=" + json.dumps(K_AUDIT.tolist()), flush=True)

    amp3, phase3 = dense.interpolation_probe(k3)
    k3_mpc = k3 * float(static.h)
    old_kmpc = np.asarray(m.K_MPC, float).copy()
    old_kh = np.asarray(getattr(m, "K_H", res.K0), float).copy()

    T41 = np.full((len(CHECK_Z), len(K_AUDIT)), np.nan + 1j*np.nan, complex)
    Tc41 = np.full((len(CHECK_Z), len(K_AUDIT)), np.nan, float)
    S41 = np.full((len(CHECK_Z), len(K_AUDIT)), np.nan, float)
    health_rows = []

    try:
        m.K_MPC = k3_mpc.copy(); m.K_H = k3.copy()
        data = r2.r0.prepare_bridge_data()

        for ia, kh in enumerate(K_AUDIT):
            j3 = res.ix(k3, kh)
            j2 = res.ix(k2, kh)
            for iz, tau in enumerate(np.asarray(data["tau_check"], float)):
                Tc41[iz, ia] = float(
                    m.mode_values(data, float(tau), "phi")[j3]
                    + m.mode_values(data, float(tau), "psi_bridge")[j3]
                )

            run, box = dense.run_single_mode(
                data, j3, float(k3_mpc[j3]), float(amp3[j3]), float(phase3[j3])
            )
            hh = dense.health(run)
            health_rows.append({"k_h_Mpc_inv": float(kh), "box_Mpc": float(box), **hh})
            if not hh["finite"]:
                raise RuntimeError(f"audit rerun incomplete at k/h={kh:g}")
            T41[:, ia] = dense.transfer_from_run(run, float(amp3[j3]), float(phase3[j3]))
            S41[:, ia] = dense.saturation_residuals(data, run, box)

            tr = rel_l2(np.real(T41[:, ia]), T21[:, j2])
            sr = rel_l2(S41[:, ia], S21[:, j2])
            print(
                f"FULLJ_CARDINALITY_NODE {ia+1:02d}/{len(K_AUDIT)} k_h={kh:.8f} "
                f"transferRelL2={tr:.3e} satRelL2={sr:.3e} "
                f"satOldMax={np.max(S21[:,j2]):.3e} satNewMax={np.max(S41[:,ia]):.3e}",
                flush=True,
            )
    finally:
        m.K_MPC = old_kmpc; m.K_H = old_kh

    idx2 = np.asarray([res.ix(k2, kh) for kh in K_AUDIT], int)
    T21s = T21[:, idx2]
    Tc21s = Tc21[:, idx2]
    S21s = S21[:, idx2]
    real41 = np.real(T41)
    imag41 = np.imag(T41)

    class_diff = np.asarray(
        [rel_scalar(Tc41[iz, ia], Tc21s[iz, ia]) for iz in range(len(CHECK_Z)) for ia in range(len(K_AUDIT))],
        float,
    )

    all_health = all(
        bool(q["finite"]) and float(q["canonical_max"]) <= CANONICAL_GATE
        and all(float(v) <= METRIC_GATE for v in q["metric_max"].values())
        for q in health_rows
    )

    phase_global = float(np.linalg.norm(imag41) / max(float(np.linalg.norm(T41)), 1.0e-300))
    phase_abs = float(np.max(np.abs(imag41)))
    pcomplex = np.abs(T41)**2
    preal = real41**2
    proj = float(np.max(np.abs(pcomplex - preal) / np.maximum(np.maximum(pcomplex, preal), 1.0e-300)))

    transfer_global = rel_l2(real41, T21s)
    transfer_per_k = np.asarray([rel_l2(real41[:, j], T21s[:, j]) for j in range(len(K_AUDIT))], float)

    P41 = res.power_from_T(K_AUDIT, real41)
    P21 = res.power_from_T(K_AUDIT, T21s)
    power_global = rel_l2(P41, P21)
    power_per_k = np.asarray([rel_l2(P41[:, j], P21[:, j]) for j in range(len(K_AUDIT))], float)

    sat_abs_diff = float(np.max(np.abs(S41 - S21s)))
    sat_rel = rel_l2(S41, S21s)
    sat_new_max = float(np.max(S41))

    gates = {
        "C_G1_provenance_setup": bool(all(ancestry.values()) and frozen),
        "C_G2_41mode_CLASS_reference_consistency": bool(np.median(class_diff) <= CLASS_MED_GATE and np.max(class_diff) <= CLASS_MAX_GATE),
        "C_G3_rerun_solver_metric_health": bool(all_health),
        "C_G4_rerun_phase_health": bool(phase_global <= PHASE_GLOBAL_GATE and phase_abs <= PHASE_ABS_GATE and proj <= POWER_PROJ_GATE),
        "C_G5_transfer_cardinality_invariance": bool(transfer_global <= TRANSFER_GLOBAL_GATE and np.max(transfer_per_k) <= TRANSFER_PER_K_GATE),
        "C_G6_power_cardinality_invariance": bool(power_global <= POWER_GLOBAL_GATE and np.max(power_per_k) <= POWER_PER_K_GATE),
        "C_G7_saturation_cardinality_invariance": bool(sat_new_max <= SAT_NEW_GATE and sat_abs_diff <= SAT_ABS_DIFF_GATE and sat_rel <= SAT_REL_L2_GATE),
    }
    classification = PASS if all(gates.values()) else FAIL

    node_rows = []
    for ia, kh in enumerate(K_AUDIT):
        j2 = idx2[ia]
        for iz, z in enumerate(CHECK_Z):
            node_rows.append({
                "z": float(z),
                "k_h_Mpc_inv": float(kh),
                "T21_real": float(T21s[iz, ia]),
                "T41_real": float(real41[iz, ia]),
                "T41_imag": float(imag41[iz, ia]),
                "T_abs_diff": float(abs(real41[iz, ia] - T21s[iz, ia])),
                "CLASS21": float(Tc21s[iz, ia]),
                "CLASS41": float(Tc41[iz, ia]),
                "eps_sat_21": float(S21s[iz, ia]),
                "eps_sat_41": float(S41[iz, ia]),
                "P21": float(P21[iz, ia]),
                "P41": float(P41[iz, ia]),
            })

    summary = {
        "class_median_relative_difference": float(np.median(class_diff)),
        "class_max_relative_difference": float(np.max(class_diff)),
        "phase_global": phase_global,
        "phase_abs_max": phase_abs,
        "real_projection_power_change_max": proj,
        "transfer_global_relL2": transfer_global,
        "transfer_per_k_relL2_max": float(np.max(transfer_per_k)),
        "power_global_relL2": power_global,
        "power_per_k_relL2_max": float(np.max(power_per_k)),
        "saturation_new_max": sat_new_max,
        "saturation_abs_difference_max": sat_abs_diff,
        "saturation_global_relL2": sat_rel,
    }

    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "ancestry": ancestry,
        "reference_member": REFERENCE_MEMBER,
        "redshifts": CHECK_Z.tolist(),
        "K_audit_h_Mpc_inv": K_AUDIT.tolist(),
        "K3_h_Mpc_inv": k3.tolist(),
        "NX": NX,
        "NSTEP": NSTEP,
        "n_embed": N_EMBED,
        "health": health_rows,
        "summary": summary,
        "gates": gates,
        "rows": node_rows,
        "HISTORICAL_DENSE_FAIL_PRESERVED": True,
        "HISTORICAL_RESIDUAL_R2_FAIL_PRESERVED": True,
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
    }

    jout = Path(args.json_out); jout.parent.mkdir(parents=True, exist_ok=True)
    nout = Path(args.npz_out); cout = Path(args.csv_out)
    jout.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(
        nout,
        redshifts=CHECK_Z,
        K_audit_h_Mpc_inv=K_AUDIT,
        T21=T21s,
        T41=T41,
        CLASS21=Tc21s,
        CLASS41=Tc41,
        eps_sat_21=S21s,
        eps_sat_41=S41,
        P21=P21,
        P41=P41,
    )
    with cout.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(node_rows[0].keys()))
        wr.writeheader(); wr.writerows(node_rows)

    print("FULLJ_CARDINALITY_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_CARDINALITY_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_CARDINALITY_CLASSIFICATION=" + classification, flush=True)
    print("THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
