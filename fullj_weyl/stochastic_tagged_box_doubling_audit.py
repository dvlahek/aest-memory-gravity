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

from fullj_weyl import stochastic_tagged_mode_poc as poc
from fullj_weyl import stochastic_tagged_power_lattice as pl

r2 = pl.r2
m = pl.m
static = pl.static

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
GAUSS_RESULT_LOCK = "05e38b273f91eb04b7b4c8753731017d0ed839c1"
SAT_RESULT_LOCK = "f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f"
TAGGED_POC_RESULT_LOCK = "aff670fa8551163f5cde2b5146e0e5840d53b424"
KERNEL_RESULT_LOCK = "2a5f884a50b7b30b90ddff01721914626dbde20f"
POWER_RESULT_LOCK = "b1a66aaa6e1a37919c8287908995ee2aea79eb4e"
HISTORY_ADDENDUM_LOCK = "1edb8309fa978a1a832ca324ff8bf2dc0a6cc59d"
PREDATA_LOCK = "87556935ae310b3e6cd4549fba1f090940ccba7e"

PASS = "FULLJ_STOCHASTIC_TAGGED_BOX_DOUBLING_AUDIT_PASS"
FAIL = "FULLJ_STOCHASTIC_TAGGED_BOX_DOUBLING_AUDIT_FAIL"
INCOMPLETE = "FULLJ_STOCHASTIC_TAGGED_BOX_DOUBLING_AUDIT_INCOMPLETE"

COEFF_HASH = "9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200"
B2 = (0, 1)
AUDIT_K = np.asarray([0.030, 0.060, 0.095, 0.100, 0.120, 0.160, 0.195, 0.200], float)
EPS = 0.05
NSTEP = 4096
CHECK_Z = np.asarray(m.CHECK_Z, float)
REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}

KF_A = 0.005
NX_A = 256
BOX_A = 2.0 * np.pi / (KF_A * float(static.h))
KF_B = 0.0025
NX_B = 512
BOX_B = 2.0 * np.pi / (KF_B * float(static.h))

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
SAT_GATE = 2.0e-2
RESP_GLOBAL_GATE = 1.0e-4
RESP_PERK_GATE = 5.0e-4
RESP_PERZ_GATE = 5.0e-4
RESP_POINT_GATE = 2.0e-3
POWER_GLOBAL_GATE = 2.0e-4
POWER_PERK_GATE = 1.0e-3
POWER_PERZ_GATE = 1.0e-3
POWER_POINT_GATE = 4.0e-3

POWER_JSON = ROOT / "results/fullj_stochastic_tagged_power_lattice.json"
POWER_NPZ = ROOT / "results/fullj_stochastic_tagged_power_lattice.npz"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def idx(grid, value):
    q = np.where(np.isclose(np.asarray(grid, float), float(value), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"nonunique index for {value}")
    return int(q[0])


def rel_complex(a, b):
    aa = np.asarray(a, complex)
    bb = np.asarray(b, complex)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def rel_real(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def pointwise_complex(a, b):
    aa = np.asarray(a, complex)
    bb = np.asarray(b, complex)
    scale = max(float(np.max(np.abs(aa))), float(np.max(np.abs(bb))), 1e-300)
    floor = 1e-12 * scale
    den = np.maximum(np.maximum(np.abs(aa), np.abs(bb)), floor)
    return np.abs(aa - bb) / den


def pointwise_real(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    scale = max(float(np.max(np.abs(aa))), float(np.max(np.abs(bb))), 1e-300)
    floor = 1e-12 * scale
    den = np.maximum(np.maximum(np.abs(aa), np.abs(bb)), floor)
    return np.abs(aa - bb) / den


def load_locked_power():
    if not POWER_JSON.exists() or not POWER_NPZ.exists():
        raise FileNotFoundError("missing locked/local power-lattice JSON/NPZ")
    meta = json.loads(POWER_JSON.read_text())
    if meta.get("classification") != "FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_FAIL":
        raise RuntimeError("local power-lattice JSON does not preserve historical FAIL")
    g = meta.get("gates", {})
    for name in (
        "PL_G1_provenance_and_frozen_identity",
        "PL_G2_stageA_solver_constraint_health",
        "PL_G3_stageA_broadband_saturated_closure",
        "PL_G4_complete_lattice_algebra_background_sanity",
        "PL_G5_stageB_solver_constraint_saturation_health",
    ):
        if g.get(name) is not True:
            raise RuntimeError(f"locked power-lattice true gate not preserved: {name}")
    for name in (
        "PL_G6_power_half_lattice_interpolation_accuracy",
        "PL_G7_no_unresolved_selected_interval_power_spike",
    ):
        if g.get(name) is not False:
            raise RuntimeError(f"locked power-lattice FAIL gate not preserved: {name}")
    q = np.load(POWER_NPZ)
    K = np.asarray(q["K_full"], float)
    A = np.asarray(q["response_full"], complex)
    if A.shape != (4, len(K), len(CHECK_Z)) or not np.all(np.isfinite(A)):
        raise RuntimeError(f"locked full response shape/nonfinite mismatch {A.shape}")
    for kh in AUDIT_K:
        idx(K, kh)
    return meta, K, A


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_stochastic_tagged_box_doubling_audit.json")
    ap.add_argument("--npz-out", default="results/fullj_stochastic_tagged_box_doubling_audit.npz")
    ap.add_argument("--csv-out", default="results/fullj_stochastic_tagged_box_doubling_audit.csv")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock": bool(poc.gaussian_lock_ok()),
        "saturated_closure_result_lock": is_ancestor(SAT_RESULT_LOCK),
        "tagged_poc_result_lock": is_ancestor(TAGGED_POC_RESULT_LOCK),
        "kernel_result_lock": is_ancestor(KERNEL_RESULT_LOCK),
        "power_lattice_fail_result_lock": is_ancestor(POWER_RESULT_LOCK),
        "history_addendum_lock": is_ancestor(HISTORY_ADDENDUM_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    _, gcoef, digest = poc.coeff_draw()
    frozen = bool(
        digest == COEFF_HASH
        and B2 == (0, 1)
        and np.allclose(AUDIT_K, [0.030,0.060,0.095,0.100,0.120,0.160,0.195,0.200], rtol=0, atol=5e-14)
        and EPS == 0.05 and NSTEP == 4096
        and KF_A == 0.005 and NX_A == 256 and KF_B == 0.0025 and NX_B == 512
        and abs(BOX_A - 2.0*np.pi/(KF_A*float(static.h))) < 1e-12
        and abs(BOX_B - 2.0*np.pi/(KF_B*float(static.h))) < 1e-12
        and REFERENCE_MEMBER == {"sigma":0,"kind":"simple","beta0":1.0}
    )

    print("FULLJ_BOX_AUDIT_START", flush=True)
    print("FULLJ_BOX_AUDIT_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_BOX_AUDIT_COEFFICIENT_SHA256=" + digest, flush=True)
    print("FULLJ_BOX_AUDIT_K=" + json.dumps(AUDIT_K.tolist()), flush=True)
    print(f"FULLJ_BOX_AUDIT_GEOM_A kF_h={KF_A:.6f} NX={NX_A} box_Mpc={BOX_A:.12e}", flush=True)
    print(f"FULLJ_BOX_AUDIT_GEOM_B kF_h={KF_B:.6f} NX={NX_B} box_Mpc={BOX_B:.12e}", flush=True)

    try:
        power_meta, Kfull, A_full = load_locked_power()
    except Exception as exc:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "frozen_setup": frozen, "reason": str(exc)}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_BOX_AUDIT_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "frozen_setup": frozen, "coefficient_sha256": digest}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_BOX_AUDIT_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    A_ref = np.empty((len(B2), len(AUDIT_K), len(CHECK_Z)), complex)
    for ia, kh in enumerate(AUDIT_K):
        A_ref[:, ia, :] = A_full[:2, idx(Kfull, kh), :]

    A_new = np.full_like(A_ref, np.nan + 1j*np.nan)
    runs = []
    rows = []
    run_index = 0
    old_kmpc = np.asarray(m.K_MPC, float).copy()
    old_kh = np.asarray(getattr(m, "K_H", pl.KFULL), float).copy()
    try:
        for ia, kh in enumerate(AUDIT_K):
            mode_h = poc.target_modes(float(kh))
            m.K_H = mode_h.copy()
            m.K_MPC = mode_h * float(static.h)
            data = r2.r0.prepare_bridge_data()
            for ib, bgid in enumerate(B2):
                pair = {}
                mm = None
                for sign in (+1, -1):
                    run_index += 1
                    rec, wh, meta = pl.run_signed_geom(
                        data, mode_h, gcoef[bgid], bgid, float(kh), sign,
                        KF_B, NX_B, BOX_B, "box0025_audit"
                    )
                    rec["run_index"] = int(run_index)
                    runs.append(rec)
                    print(
                        f"FULLJ_BOX_AUDIT_RUN {run_index:02d}/32 bg={bgid} k_h={kh:.4f} sign={sign:+d} "
                        + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get("finite") else f"finite=False reason={rec.get('reason','unknown')}"),
                        flush=True,
                    )
                    if wh is not None:
                        pair[sign] = wh
                        mm = meta
                if len(pair) == 2:
                    T = pl.pair_response(pair, mm)
                    A_new[ib, ia, :] = T
                    for iz, zz in enumerate(CHECK_Z):
                        rows.append({
                            "background": int(bgid), "k_h_Mpc_inv": float(kh), "z": float(zz),
                            "T_A_real": float(np.real(A_ref[ib, ia, iz])),
                            "T_A_imag": float(np.imag(A_ref[ib, ia, iz])),
                            "T_B_real": float(np.real(T[iz])),
                            "T_B_imag": float(np.imag(T[iz])),
                            "P_A": float(abs(A_ref[ib, ia, iz])**2),
                            "P_B": float(abs(T[iz])**2),
                        })
    finally:
        m.K_MPC = old_kmpc
        m.K_H = old_kh

    finite_runs = [r for r in runs if r.get("finite")]
    all_finite = len(finite_runs) == 32 and np.all(np.isfinite(A_new))
    canonical_max = max((float(r.get("canonical_max", np.inf)) for r in finite_runs), default=np.inf)
    metric_max = {name: max((float(r.get("metric_max", {}).get(name, np.inf)) for r in finite_runs), default=np.inf) for name in ("hamiltonian", "momentum", "shear")}
    sat_max = max((float(r.get("sat_max", np.inf)) for r in finite_runs), default=np.inf)

    P_ref = np.abs(A_ref)**2
    P_new = np.abs(A_new)**2

    resp_global = rel_complex(A_ref, A_new)
    power_global = rel_real(P_ref, P_new)
    resp_per_k = [rel_complex(A_ref[:, i, :], A_new[:, i, :]) for i in range(len(AUDIT_K))]
    power_per_k = [rel_real(P_ref[:, i, :], P_new[:, i, :]) for i in range(len(AUDIT_K))]
    resp_per_z = [rel_complex(A_ref[:, :, i], A_new[:, :, i]) for i in range(len(CHECK_Z))]
    power_per_z = [rel_real(P_ref[:, :, i], P_new[:, :, i]) for i in range(len(CHECK_Z))]
    resp_point = pointwise_complex(A_ref, A_new)
    power_point = pointwise_real(P_ref, P_new)

    summary = {
        "runs_expected": 32,
        "runs_finite": len(finite_runs),
        "canonical_max": float(canonical_max),
        "metric_hamiltonian_max": float(metric_max["hamiltonian"]),
        "metric_momentum_max": float(metric_max["momentum"]),
        "metric_shear_max": float(metric_max["shear"]),
        "broadband_saturation_max": float(sat_max),
        "response_global_relative_L2": float(resp_global),
        "response_per_k_max": float(max(resp_per_k)),
        "response_per_z_max": float(max(resp_per_z)),
        "response_pointwise_zero_safe_max": float(np.max(resp_point)),
        "power_global_relative_L2": float(power_global),
        "power_per_k_max": float(max(power_per_k)),
        "power_per_z_max": float(max(power_per_z)),
        "power_pointwise_zero_safe_max": float(np.max(power_point)),
        "coefficient_sha256": digest,
    }

    g1 = bool(all(ancestry.values()) and frozen)
    g2 = bool(all_finite and canonical_max <= CANONICAL_GATE and all(metric_max[x] <= METRIC_GATE for x in metric_max))
    g3 = bool(sat_max <= SAT_GATE)
    g4 = bool(resp_global <= RESP_GLOBAL_GATE and max(resp_per_k) <= RESP_PERK_GATE and max(resp_per_z) <= RESP_PERZ_GATE and np.max(resp_point) <= RESP_POINT_GATE)
    g5 = bool(power_global <= POWER_GLOBAL_GATE and max(power_per_k) <= POWER_PERK_GATE and max(power_per_z) <= POWER_PERZ_GATE and np.max(power_point) <= POWER_POINT_GATE)
    gates = {
        "BD_G1_provenance_and_frozen_identity": g1,
        "BD_G2_all_32_runs_finite_constraint_clean": g2,
        "BD_G3_broadband_saturated_closure": g3,
        "BD_G4_same_k_response_box_doubling_invariance": g4,
        "BD_G5_same_k_power_box_doubling_invariance": g5,
    }
    classification = PASS if all(gates.values()) else FAIL

    git_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    per_k = [{
        "k_h_Mpc_inv": float(kh),
        "response_relative_L2": float(resp_per_k[i]),
        "power_relative_L2": float(power_per_k[i]),
    } for i, kh in enumerate(AUDIT_K)]
    per_z = [{
        "z": float(zz),
        "response_relative_L2": float(resp_per_z[i]),
        "power_relative_L2": float(power_per_z[i]),
    } for i, zz in enumerate(CHECK_Z)]

    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": git_head,
        "ancestry": ancestry,
        "frozen_setup": frozen,
        "coefficient_sha256": digest,
        "audit_k_h_Mpc_inv": AUDIT_K.tolist(),
        "background_ids": list(B2),
        "epsilon": EPS,
        "NSTEP": NSTEP,
        "geometry_A": {"kF_h": KF_A, "NX": NX_A, "box_Mpc": float(BOX_A)},
        "geometry_B": {"kF_h": KF_B, "NX": NX_B, "box_Mpc": float(BOX_B)},
        "summary": summary,
        "per_k": per_k,
        "per_z": per_z,
        "gates": gates,
        "STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_TESTED": bool(classification == PASS),
        "STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED": False,
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
        "runs": runs,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(
        args.npz_out,
        redshifts=CHECK_Z,
        audit_k=AUDIT_K,
        response_A=A_ref,
        response_B=A_new,
        power_A=P_ref,
        power_B=P_new,
        response_pointwise=resp_point,
        power_pointwise=power_point,
    )
    with Path(args.csv_out).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["background","k_h_Mpc_inv","z","T_A_real","T_A_imag","T_B_real","T_B_imag","P_A","P_B"])
        writer.writeheader()
        writer.writerows(rows)

    print("FULLJ_BOX_AUDIT_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_BOX_AUDIT_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_BOX_AUDIT_CLASSIFICATION=" + classification, flush=True)
    print("STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_TESTED=" + str(classification == PASS), flush=True)
    print("STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED=False", flush=True)
    print("THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
