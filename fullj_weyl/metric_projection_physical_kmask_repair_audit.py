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

# Activate the geometry-invariant metric projection before importing the tagged
# machinery.  R1/R2 call r0.metric_correction dynamically.
from fullj_weyl import metric_projection_physical_kmask_repair as kmask
from fullj_weyl import stochastic_tagged_mode_poc as poc

r2 = poc.r2
m = poc.m
static = poc.static
d2b = poc.d2b

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
TAGGED_POC_RESULT_LOCK = "aff670fa8551163f5cde2b5146e0e5840d53b424"
KERNEL_RESULT_LOCK = "2a5f884a50b7b30b90ddff01721914626dbde20f"
POWER_FAIL_RESULT_LOCK = "b1a66aaa6e1a37919c8287908995ee2aea79eb4e"
BOX_FAIL_RESULT_LOCK = "f600b7e594e57ffbbd0f3044aa2fbf4da20e942b"
PREDATA_LOCK = "5313c734238363d1c2985446eddd35c2846e7aeb"

PASS = "FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_PASS"
FAIL = "FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_FAIL"
INCOMPLETE = "FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_INCOMPLETE"

COEFF_HASH = "9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200"
AUDIT_K = np.asarray([0.060, 0.095, 0.160, 0.195], float)
BACKGROUNDS = (0, 1)
EPS = 0.05
NSTEP = 4096
REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}
CHECK_Z = np.asarray(m.CHECK_Z, float)

KF_A = 0.005
NX_A = 256
BOX_A = 2.0 * np.pi / (KF_A * float(static.h))
KF_B = 0.0025
NX_B = 512
BOX_B = 2.0 * np.pi / (KF_B * float(static.h))

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
SAT_GATE = 2.0e-2
REPEAT_GATE = 1.0e-10
FIELD_GATE = 1.0e-8
RESP_GLOBAL_GATE = 1.0e-6
RESP_PERK_GATE = 1.0e-5
RESP_PERZ_GATE = 1.0e-5
POWER_GLOBAL_GATE = 1.0e-6
POWER_PERK_GATE = 1.0e-5
POWER_PERZ_GATE = 1.0e-5


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1.0e-300))


def saturation(data, run, nx: int, box: float) -> np.ndarray:
    old_box = float(static.BOX)
    static.BOX = float(box)
    try:
        grad, lap, _, div = m.spec_ops(int(nx))
        out = []
        for cp in run["checkpoints"]:
            tau = float(cp["tau"])
            a, H, Q, KQ, KQQ, Z, Qdot = m.bg_eval(data, tau)
            chi = np.asarray(cp["y"][1], float)
            g = grad(chi)
            x = float(static.ACC_CONV) * np.abs(g) / a
            je = d2b.j_eff(x, Z)
            full = div((1.0 + je) * g)
            sat = 2.0 * lap(chi)
            scale = max(float(np.linalg.norm(full)), float(np.linalg.norm(sat)), 1.0e-300)
            out.append(float(np.linalg.norm(full - sat) / scale))
        return np.asarray(out, float)
    finally:
        static.BOX = old_box


def run_signed(data, mode_h, gvec, bgid: int, kh: float, sign: int, kf_h: float, nx: int, box: float, geom: str):
    ntag = int(round(float(kh) / float(kf_h)))
    if abs(ntag * float(kf_h) - float(kh)) > 5.0e-13:
        raise RuntimeError(f"{kh} not lattice-compatible with kF/h={kf_h}")
    make, amp_tag, phase_tag = poc.basis_factory(mode_h, gvec, float(kh), EPS, int(sign), int(nx), float(box))
    old_cos = m.cos_matrix
    old_box = float(static.BOX)
    d2b.set_member(REFERENCE_MEMBER)
    m.cos_matrix = make
    static.BOX = float(box)
    try:
        run = r2.integrate_combined_r2(data, int(nx), int(NSTEP), True)
        hh = poc.health(run)
        if not hh["finite"]:
            return {
                "finite": False, "geometry": geom, "background": int(bgid), "k_h": float(kh),
                "sign": int(sign), "nx": int(nx), "kF_h": float(kf_h), "box_Mpc": float(box),
                "reason": run.get("fail_reason", "incomplete")
            }, run, None, None
        sat = saturation(data, run, int(nx), float(box))
        wh = poc.tagged_fourier(run, ntag)
        rec = {
            "finite": True, "geometry": geom, "background": int(bgid), "k_h": float(kh),
            "sign": int(sign), "epsilon": float(EPS), "nx": int(nx), "kF_h": float(kf_h),
            "box_Mpc": float(box), "ntag": int(ntag), "canonical_max": float(hh["canonical_max"]),
            "metric_max": hh["metric_max"], "sat_max": float(np.max(sat)), "sat_by_z": sat.tolist(),
        }
        return rec, run, wh, {"amp_tag": float(amp_tag), "phase_tag": float(phase_tag)}
    finally:
        m.cos_matrix = old_cos
        static.BOX = old_box


def field_pair_metrics(run_a, run_b):
    if len(run_a["checkpoints"]) != len(CHECK_Z) or len(run_b["checkpoints"]) != len(CHECK_Z):
        raise RuntimeError("checkpoint count mismatch")
    cross = {"alpha": 0.0, "chi": 0.0, "Pchi": 0.0, "S": 0.0, "delta_A": 0.0, "Theta_A": 0.0, "Weyl": 0.0}
    repeat = dict(cross)
    for ca, cb in zip(run_a["checkpoints"], run_b["checkpoints"]):
        fa = {
            "alpha": np.asarray(ca["y"][0], float),
            "chi": np.asarray(ca["y"][1], float),
            "Pchi": np.asarray(ca["y"][2], float),
            "S": np.asarray(ca["y"][3], float),
            "delta_A": np.asarray(ca["delta"], float),
            "Theta_A": np.asarray(ca["theta"], float),
            "Weyl": np.asarray(ca["metric"]["weyl"], float),
        }
        fb = {
            "alpha": np.asarray(cb["y"][0], float),
            "chi": np.asarray(cb["y"][1], float),
            "Pchi": np.asarray(cb["y"][2], float),
            "S": np.asarray(cb["y"][3], float),
            "delta_A": np.asarray(cb["delta"], float),
            "Theta_A": np.asarray(cb["theta"], float),
            "Weyl": np.asarray(cb["metric"]["weyl"], float),
        }
        for name in cross:
            if fa[name].size != NX_A or fb[name].size != NX_B:
                raise RuntimeError(f"unexpected field size {name}: {fa[name].size}, {fb[name].size}")
            b0 = fb[name][:NX_A]
            b1 = fb[name][NX_A:]
            cross[name] = max(cross[name], rel(fa[name], b0))
            repeat[name] = max(repeat[name], rel(b0, b1))
    return cross, repeat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_metric_projection_physical_kmask_repair_audit.json")
    ap.add_argument("--npz-out", default="results/fullj_metric_projection_physical_kmask_repair_audit.npz")
    ap.add_argument("--csv-out", default="results/fullj_metric_projection_physical_kmask_repair_audit.csv")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock": bool(poc.gaussian_lock_ok()),
        "tagged_poc_result_lock": is_ancestor(TAGGED_POC_RESULT_LOCK),
        "kernel_result_lock": is_ancestor(KERNEL_RESULT_LOCK),
        "power_lattice_fail_result_lock": is_ancestor(POWER_FAIL_RESULT_LOCK),
        "box_doubling_fail_result_lock": is_ancestor(BOX_FAIL_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    _, gcoef, digest = poc.coeff_draw()
    original_identity = kmask.original_r2_mask_identity(128)
    frozen = bool(
        kmask.REPAIR_ACTIVE
        and abs(kmask.ORIGINAL_KF_H - 0.01) < 1e-15
        and abs(kmask.METRIC_KMAX_H - 0.32) < 1e-15
        and digest == COEFF_HASH
        and np.allclose(AUDIT_K, [0.060, 0.095, 0.160, 0.195], rtol=0, atol=5e-14)
        and BACKGROUNDS == (0, 1) and EPS == 0.05 and NSTEP == 4096
        and KF_A == 0.005 and NX_A == 256 and KF_B == 0.0025 and NX_B == 512
        and REFERENCE_MEMBER == {"sigma":0,"kind":"simple","beta0":1.0}
    )

    print("FULLJ_KMASK_REPAIR_START", flush=True)
    print("FULLJ_KMASK_REPAIR_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_KMASK_REPAIR_COEFFICIENT_SHA256=" + digest, flush=True)
    print("FULLJ_KMASK_REPAIR_ORIGINAL_IDENTITY=" + json.dumps(original_identity, sort_keys=True), flush=True)
    print(f"FULLJ_KMASK_REPAIR_CUTOFF kmax_h={kmask.METRIC_KMAX_H:.6f}", flush=True)
    print("FULLJ_KMASK_REPAIR_K=" + json.dumps(AUDIT_K.tolist()), flush=True)

    if not all(ancestry.values()) or not frozen or not original_identity["identical"]:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry,
               "frozen_setup": frozen, "original_r2_mask_identity": original_identity}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_KMASK_REPAIR_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    responses_a = np.full((len(BACKGROUNDS), len(AUDIT_K), len(CHECK_Z)), np.nan + 1j*np.nan, complex)
    responses_b = np.full_like(responses_a, np.nan + 1j*np.nan)
    runs = []
    field_cross_max = {"alpha": 0.0, "chi": 0.0, "Pchi": 0.0, "S": 0.0, "delta_A": 0.0, "Theta_A": 0.0, "Weyl": 0.0}
    repeat_max = dict(field_cross_max)
    per_pair_fields = []
    run_index = 0

    old_kmpc = np.asarray(m.K_MPC, float).copy()
    old_kh = np.asarray(getattr(m, "K_H", poc.K0), float).copy()
    try:
        for ik, kh in enumerate(AUDIT_K):
            mode_h = poc.target_modes(float(kh))
            m.K_H = mode_h.copy()
            m.K_MPC = mode_h * float(static.h)
            data = r2.r0.prepare_bridge_data()
            for ib, bgid in enumerate(BACKGROUNDS):
                geom_runs = {"A": {}, "B": {}}
                geom_wh = {"A": {}, "B": {}}
                geom_meta = {"A": None, "B": None}
                for geom, kf, nx, box in (("A", KF_A, NX_A, BOX_A), ("B", KF_B, NX_B, BOX_B)):
                    for sign in (+1, -1):
                        run_index += 1
                        rec, run, wh, meta = run_signed(data, mode_h, gcoef[bgid], bgid, float(kh), sign, kf, nx, box, geom)
                        rec["run_index"] = int(run_index)
                        runs.append(rec)
                        print(
                            f"FULLJ_KMASK_REPAIR_RUN {run_index:02d}/32 geom={geom} bg={bgid} k_h={kh:.4f} sign={sign:+d} "
                            f"canonical={rec.get('canonical_max', float('nan')):.3e} satMax={rec.get('sat_max', float('nan')):.3e}",
                            flush=True,
                        )
                        if not rec.get("finite", False):
                            continue
                        geom_runs[geom][sign] = run
                        geom_wh[geom][sign] = wh
                        geom_meta[geom] = meta
                if all(sign in geom_runs["A"] and sign in geom_runs["B"] for sign in (+1, -1)):
                    for sign in (+1, -1):
                        cross, rep = field_pair_metrics(geom_runs["A"][sign], geom_runs["B"][sign])
                        per_pair_fields.append({"k_h": float(kh), "background": int(bgid), "sign": int(sign),
                                                "cross_geometry": cross, "B_repeat": rep})
                        for name in field_cross_max:
                            field_cross_max[name] = max(field_cross_max[name], float(cross[name]))
                            repeat_max[name] = max(repeat_max[name], float(rep[name]))
                    ma = geom_meta["A"]
                    mb = geom_meta["B"]
                    ta = (geom_wh["A"][+1] - geom_wh["A"][-1]) * np.exp(-1j * ma["phase_tag"]) / (EPS * ma["amp_tag"])
                    tb = (geom_wh["B"][+1] - geom_wh["B"][-1]) * np.exp(-1j * mb["phase_tag"]) / (EPS * mb["amp_tag"])
                    responses_a[ib, ik, :] = ta
                    responses_b[ib, ik, :] = tb
    finally:
        m.K_MPC = old_kmpc
        m.K_H = old_kh

    all_finite = len(runs) == 32 and all(r.get("finite", False) for r in runs)
    canonical_max = max((float(r.get("canonical_max", np.inf)) for r in runs), default=np.inf)
    metric_max = {name: max((float(r.get("metric_max", {}).get(name, np.inf)) for r in runs), default=np.inf)
                  for name in ("hamiltonian", "momentum", "shear")}
    sat_max = max((float(r.get("sat_max", np.inf)) for r in runs), default=np.inf)

    response_global = rel(responses_a, responses_b) if np.all(np.isfinite(responses_a)) and np.all(np.isfinite(responses_b)) else np.inf
    response_per_k = [rel(responses_a[:, i, :], responses_b[:, i, :]) for i in range(len(AUDIT_K))]
    response_per_z = [rel(responses_a[:, :, iz], responses_b[:, :, iz]) for iz in range(len(CHECK_Z))]
    pa = np.abs(responses_a) ** 2
    pb = np.abs(responses_b) ** 2
    power_global = rel(pa, pb) if np.all(np.isfinite(pa)) and np.all(np.isfinite(pb)) else np.inf
    power_per_k = [rel(pa[:, i, :], pb[:, i, :]) for i in range(len(AUDIT_K))]
    power_per_z = [rel(pa[:, :, iz], pb[:, :, iz]) for iz in range(len(CHECK_Z))]

    max_repeat = max(repeat_max.values())
    max_field_cross = max(field_cross_max.values())

    gates = {
        "KM_G1_provenance_and_frozen_identity": bool(all(ancestry.values()) and frozen),
        "KM_G2_original_R2_mask_identity": bool(original_identity["mismatch_count"] == 0),
        "KM_G3_all_32_repaired_runs_finite_constraint_clean": bool(
            all_finite and canonical_max <= CANONICAL_GATE and all(metric_max[k] <= METRIC_GATE for k in metric_max)
        ),
        "KM_G4_broadband_saturated_closure": bool(sat_max <= SAT_GATE),
        "KM_G5_doubled_box_repeat_symmetry": bool(max_repeat <= REPEAT_GATE),
        "KM_G6_direct_AB_field_invariance": bool(max_field_cross <= FIELD_GATE),
        "KM_G7_tagged_response_box_invariance": bool(
            response_global <= RESP_GLOBAL_GATE and max(response_per_k) <= RESP_PERK_GATE and max(response_per_z) <= RESP_PERZ_GATE
        ),
        "KM_G8_tagged_power_box_invariance": bool(
            power_global <= POWER_GLOBAL_GATE and max(power_per_k) <= POWER_PERK_GATE and max(power_per_z) <= POWER_PERZ_GATE
        ),
    }
    classification = PASS if all(gates.values()) else FAIL

    summary = {
        "runs_expected": 32, "runs_finite": int(sum(bool(r.get("finite", False)) for r in runs)),
        "canonical_max": float(canonical_max), "metric_max": metric_max, "broadband_saturation_max": float(sat_max),
        "B_repeat_field_max": float(max_repeat), "AB_field_relative_L2_max": float(max_field_cross),
        "response_global_relative_L2": float(response_global), "response_per_k_max": float(max(response_per_k)),
        "response_per_z_max": float(max(response_per_z)), "power_global_relative_L2": float(power_global),
        "power_per_k_max": float(max(power_per_k)), "power_per_z_max": float(max(power_per_z)),
    }

    out = {
        "classification": classification, "diagnostic_complete": True, "ancestry": ancestry, "frozen_setup": frozen,
        "coefficient_sha256": digest, "repair": {"original_kF_h": kmask.ORIGINAL_KF_H,
        "metric_kmax_h": kmask.METRIC_KMAX_H, "original_R2_mask_identity": original_identity},
        "audit_k_h_Mpc_inv": AUDIT_K.tolist(), "background_ids": list(BACKGROUNDS), "epsilon": EPS,
        "geometry_A": {"kF_h": KF_A, "NX": NX_A, "box_Mpc": BOX_A},
        "geometry_B": {"kF_h": KF_B, "NX": NX_B, "box_Mpc": BOX_B},
        "field_cross_geometry_max": field_cross_max, "field_B_repeat_max": repeat_max,
        "per_pair_fields": per_pair_fields,
        "per_k": [{"k_h_Mpc_inv": float(k), "response_relative_L2": float(response_per_k[i]),
                   "power_relative_L2": float(power_per_k[i])} for i, k in enumerate(AUDIT_K)],
        "per_z": [{"z": float(z), "response_relative_L2": float(response_per_z[i]),
                   "power_relative_L2": float(power_per_z[i])} for i, z in enumerate(CHECK_Z)],
        "summary": summary, "gates": gates, "runs": runs,
        "METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_VALIDATED": bool(classification == PASS),
        "STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_REPAIRED": bool(classification == PASS),
        "STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED": False,
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(args.npz_out, K=AUDIT_K, z=CHECK_Z, response_A=responses_a, response_B=responses_b,
                        power_A=pa, power_B=pb)
    with Path(args.csv_out).open("w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["background", "k_h_Mpc_inv", "z", "T_A_real", "T_A_imag", "T_B_real", "T_B_imag", "P_A", "P_B"])
        for ib, bgid in enumerate(BACKGROUNDS):
            for ik, kh in enumerate(AUDIT_K):
                for iz, z in enumerate(CHECK_Z):
                    wr.writerow([bgid, float(kh), float(z), float(responses_a[ib,ik,iz].real), float(responses_a[ib,ik,iz].imag),
                                 float(responses_b[ib,ik,iz].real), float(responses_b[ib,ik,iz].imag),
                                 float(pa[ib,ik,iz]), float(pb[ib,ik,iz])])

    print("FULLJ_KMASK_REPAIR_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_KMASK_REPAIR_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_KMASK_REPAIR_CLASSIFICATION=" + classification, flush=True)
    print("METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_VALIDATED=" + str(classification == PASS), flush=True)
    print("STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_REPAIRED=" + str(classification == PASS), flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
