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

# The validated repair must be active before the historical power-lattice
# helpers are imported.  It patches only r0.metric_correction.
from fullj_weyl import metric_projection_physical_kmask_repair as kmask
from fullj_weyl import stochastic_tagged_power_lattice as pl

poc = pl.poc
r2 = pl.r2
m = pl.m
static = pl.static

POWER_FAIL_RESULT_LOCK = "b1a66aaa6e1a37919c8287908995ee2aea79eb4e"
KMASK_RESULT_LOCK = "20151ab785e923de20d720f3fdd8890576b6cc05"
HISTORY_LOCK = "c2c275c396dc879d24fa5ca953b484dcc4ab4c03"
PREDATA_LOCK = "bef9e1304ebd838954635e624290696f08d33293"

PASS = "FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_PASS"
FAIL = "FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_FAIL"
INCOMPLETE = "FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_INCOMPLETE"

COEFF_HASH = "9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200"
B2 = (0, 1)
CHECK_Z = np.asarray(pl.CHECK_Z, float)
KFULL = np.asarray(pl.KFULL, float)
K_OVERLAP = np.asarray([0.060, 0.095, 0.160], float)
K_REPAIR = np.asarray([0.165, 0.170, 0.175, 0.180, 0.185, 0.190, 0.195, 0.200], float)
EPS = 0.05
NSTEP = 4096

KF_A, NX_A, BOX_A = pl.KF_A, pl.NX_A, pl.BOX_A
KF_B, NX_B, BOX_B = pl.KF_B, pl.NX_B, pl.BOX_B

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
SAT_GATE = 2.0e-2
ALG_GATE = 1.0e-12
OVERLAP_T_GLOBAL_GATE = 1.0e-6
OVERLAP_T_PERK_GATE = 1.0e-5
OVERLAP_P_GLOBAL_GATE = 2.0e-6
OVERLAP_P_PERK_GATE = 2.0e-5
POWER_L2_MAX_GATE = 5.0e-2
POWER_L2_MED_GATE = 2.5e-2
POWER_PEAK_GATE = 1.0e-1
SPIKE_FACTOR = 2.0

HIST_JSON = ROOT / "results/fullj_stochastic_tagged_power_lattice.json"
HIST_NPZ = ROOT / "results/fullj_stochastic_tagged_power_lattice.npz"
KMASK_JSON = ROOT / "results/fullj_metric_projection_physical_kmask_repair_audit.json"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def health_ok(rec: dict) -> bool:
    return bool(
        rec.get("finite", False)
        and float(rec.get("canonical_max", np.inf)) <= CANONICAL_GATE
        and all(float(v) <= METRIC_GATE for v in rec.get("metric_max", {}).values())
    )


def load_locked_inputs():
    if not HIST_JSON.exists() or not HIST_NPZ.exists():
        raise FileNotFoundError("missing local historical power-lattice JSON/NPZ")
    if not KMASK_JSON.exists():
        raise FileNotFoundError("missing local physical-k repair PASS JSON")

    hist = json.loads(HIST_JSON.read_text())
    if hist.get("classification") != "FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_FAIL":
        raise RuntimeError("historical power-lattice JSON does not preserve FAIL")
    hg = hist.get("gates", {})
    for name in (
        "PL_G1_provenance_and_frozen_identity",
        "PL_G2_stageA_solver_constraint_health",
        "PL_G3_stageA_broadband_saturated_closure",
        "PL_G4_complete_lattice_algebra_background_sanity",
        "PL_G5_stageB_solver_constraint_saturation_health",
    ):
        if hg.get(name) is not True:
            raise RuntimeError(f"historical true power-lattice gate not preserved: {name}")
    for name in (
        "PL_G6_power_half_lattice_interpolation_accuracy",
        "PL_G7_no_unresolved_selected_interval_power_spike",
    ):
        if hg.get(name) is not False:
            raise RuntimeError(f"historical failed power-lattice gate not preserved: {name}")

    q = np.load(HIST_NPZ)
    Kh = np.asarray(q["K_full"], float)
    Ah = np.asarray(q["response_full"], complex)
    if Kh.shape != KFULL.shape or not np.allclose(Kh, KFULL, rtol=0.0, atol=5e-13):
        raise RuntimeError("historical complete lattice does not match frozen KFULL")
    if Ah.shape != (4, len(KFULL), len(CHECK_Z)) or not np.all(np.isfinite(Ah)):
        raise RuntimeError(f"historical response_full shape/nonfinite mismatch {Ah.shape}")

    rep = json.loads(KMASK_JSON.read_text())
    if rep.get("classification") != "FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_PASS":
        raise RuntimeError("local physical-k repair JSON is not PASS")
    if rep.get("METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_VALIDATED") is not True:
        raise RuntimeError("repair validation flag not true")
    if rep.get("STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_REPAIRED") is not True:
        raise RuntimeError("box-doubling repair flag not true")
    if not all(rep.get("gates", {}).values()):
        raise RuntimeError("not all repair gates are true")
    if rep.get("repair", {}).get("original_R2_mask_identity", {}).get("mismatch_count") != 0:
        raise RuntimeError("repair JSON does not preserve original R2 mask identity")

    return hist, Kh, Ah, rep


def run_pair(data, mode_h, gcoef, bgid, kh, kf_h, nx, box, stage, run_index, total_runs):
    pair = {}
    meta = None
    records = []
    for sign in (+1, -1):
        run_index += 1
        rec, wh, mm = pl.run_signed_geom(
            data, mode_h, gcoef[bgid], bgid, float(kh), sign,
            float(kf_h), int(nx), float(box), stage,
        )
        rec["run_index"] = int(run_index)
        records.append(rec)
        print(
            f"FULLJ_POWER_KMASK_REG_RUN {run_index:03d}/{total_runs} "
            f"stage={stage} bg={bgid} k_h={kh:.4f} sign={sign:+d} "
            + (
                f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}"
                if rec.get("finite") else f"finite=False reason={rec.get('reason','unknown')}"
            ),
            flush=True,
        )
        if wh is not None:
            pair[sign] = wh
            meta = mm
    T = pl.pair_response(pair, meta) if len(pair) == 2 else None
    return run_index, records, T


def append_response_rows(rows, stage, bgid, kh, T):
    if T is None:
        return
    for iz, z in enumerate(CHECK_Z):
        rows.append({
            "stage": stage,
            "background": int(bgid),
            "k_h_Mpc_inv": float(kh),
            "z": float(z),
            "T_real": float(np.real(T[iz])),
            "T_imag": float(np.imag(T[iz])),
            "P_tag": float(abs(T[iz])**2),
        })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_stochastic_tagged_power_lattice_kmask_regression.json")
    ap.add_argument("--npz-out", default="results/fullj_stochastic_tagged_power_lattice_kmask_regression.npz")
    ap.add_argument("--csv-out", default="results/fullj_stochastic_tagged_power_lattice_kmask_regression.csv")
    args = ap.parse_args()

    ancestry = {
        "historical_power_lattice_fail_result_lock": is_ancestor(POWER_FAIL_RESULT_LOCK),
        "physical_kmask_repair_result_lock": is_ancestor(KMASK_RESULT_LOCK),
        "history_lock": is_ancestor(HISTORY_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    _, gcoef, digest = poc.coeff_draw()
    identity = kmask.original_r2_mask_identity(128)
    frozen = bool(
        digest == COEFF_HASH
        and B2 == (0, 1)
        and pl.B2 == (0, 1)
        and EPS == pl.EPS == 0.05
        and NSTEP == pl.NSTEP == 4096
        and abs(float(kmask.METRIC_KMAX_H) - 0.32) < 1e-15
        and identity.get("mismatch_count") == 0
        and np.allclose(K_OVERLAP, [0.060, 0.095, 0.160], rtol=0.0, atol=5e-14)
        and np.allclose(K_REPAIR, [0.165,0.170,0.175,0.180,0.185,0.190,0.195,0.200], rtol=0.0, atol=5e-14)
        and pl.N_HALF == 16
        and pl.CURV_Z == (1.0, 0.5, 0.2)
        and abs(KF_A - 0.005) < 1e-15 and NX_A == 256
        and abs(KF_B - 0.0025) < 1e-15 and NX_B == 512
    )

    print("FULLJ_POWER_KMASK_REG_START", flush=True)
    print("FULLJ_POWER_KMASK_REG_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_POWER_KMASK_REG_COEFFICIENT_SHA256=" + digest, flush=True)
    print("FULLJ_POWER_KMASK_REG_ORIGINAL_IDENTITY=" + json.dumps(identity, sort_keys=True), flush=True)
    print("FULLJ_POWER_KMASK_REG_OVERLAP=" + json.dumps(K_OVERLAP.tolist()), flush=True)
    print("FULLJ_POWER_KMASK_REG_REPAIR=" + json.dumps(K_REPAIR.tolist()), flush=True)
    print("FULLJ_POWER_KMASK_REG_TOTAL_RUNS=108", flush=True)

    try:
        hist_meta, Khist, Ahist, repair_meta = load_locked_inputs()
    except Exception as exc:
        out = {
            "classification": INCOMPLETE, "diagnostic_complete": False,
            "ancestry": ancestry, "frozen_setup": frozen, "reason": str(exc),
        }
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_POWER_KMASK_REG_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out = {
            "classification": INCOMPLETE, "diagnostic_complete": False,
            "ancestry": ancestry, "frozen_setup": frozen,
            "coefficient_sha256": digest, "original_R2_mask_identity": identity,
        }
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_POWER_KMASK_REG_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    A_overlap = np.full((len(B2), len(K_OVERLAP), len(CHECK_Z)), np.nan + 1j*np.nan, complex)
    A_repair = np.full((len(B2), len(K_REPAIR), len(CHECK_Z)), np.nan + 1j*np.nan, complex)
    all_runs = []
    response_rows = []
    run_index = 0
    total_runs = 108

    old_kmpc = np.asarray(m.K_MPC, float).copy()
    old_kh = np.asarray(getattr(m, "K_H", pl.radial.K0), float).copy()
    try:
        for stage, grid, target in (("A_overlap", K_OVERLAP, A_overlap), ("A_repair", K_REPAIR, A_repair)):
            for ik, kh in enumerate(grid):
                mode_h = poc.target_modes(float(kh))
                m.K_H = mode_h.copy()
                m.K_MPC = mode_h * float(static.h)
                data = r2.r0.prepare_bridge_data()
                for ib, bgid in enumerate(B2):
                    run_index, recs, T = run_pair(
                        data, mode_h, gcoef, bgid, float(kh),
                        KF_A, NX_A, BOX_A, stage, run_index, total_runs,
                    )
                    all_runs.extend(recs)
                    if T is not None:
                        target[ib, ik, :] = T
                    append_response_rows(response_rows, stage, bgid, kh, T)
    finally:
        m.K_MPC = old_kmpc
        m.K_H = old_kh

    stageA_runs = list(all_runs)

    # Certify reuse below/equal to k/h=0.16 against the historical Stage-A lattice.
    A_overlap_ref = np.empty_like(A_overlap)
    for ik, kh in enumerate(K_OVERLAP):
        A_overlap_ref[:, ik, :] = Ahist[:2, pl.idx(Khist, kh), :]
    overlap_t_global = pl.rel(A_overlap, A_overlap_ref)
    overlap_p_global = pl.rel_real(np.abs(A_overlap)**2, np.abs(A_overlap_ref)**2)
    overlap_rows = []
    overlap_t_pk = []
    overlap_p_pk = []
    for ik, kh in enumerate(K_OVERLAP):
        et = pl.rel(A_overlap[:, ik, :], A_overlap_ref[:, ik, :])
        ep = pl.rel_real(np.abs(A_overlap[:, ik, :])**2, np.abs(A_overlap_ref[:, ik, :])**2)
        overlap_t_pk.append(et)
        overlap_p_pk.append(ep)
        overlap_rows.append({"k_h_Mpc_inv": float(kh), "response_relative_L2": et, "power_relative_L2": ep})
    overlap_t_max = float(np.max(overlap_t_pk))
    overlap_p_max = float(np.max(overlap_p_pk))

    # Hybrid B2 regression lattice: historical A data where physical membership was
    # already correct, fresh repaired data at every node above k/h=0.16.
    Ahybrid = np.asarray(Ahist[:2], complex).copy()
    for ik, kh in enumerate(K_REPAIR):
        Ahybrid[:, pl.idx(KFULL, kh), :] = A_repair[:, ik, :]
    Phybrid = np.abs(Ahybrid)**2
    Pb2 = np.mean(Phybrid, axis=0)
    Tb2 = np.mean(Ahybrid, axis=0)
    back = np.real(Ahybrid)**2 + np.imag(Ahybrid)**2
    alg = float(np.linalg.norm(Phybrid - back) / max(float(np.linalg.norm(Phybrid)), 1e-300))

    selected, selection_rows, node_curv, interval_curv = pl.adaptive_half_selection(Pb2)
    print("FULLJ_POWER_KMASK_REG_SELECTED_HALF=" + json.dumps(selected.tolist()), flush=True)
    print("FULLJ_POWER_KMASK_REG_SELECTION=" + json.dumps(selection_rows, sort_keys=True), flush=True)

    Amid = np.full((len(B2), len(selected), len(CHECK_Z)), np.nan + 1j*np.nan, complex)
    old_kmpc = np.asarray(m.K_MPC, float).copy()
    old_kh = np.asarray(getattr(m, "K_H", pl.radial.K0), float).copy()
    try:
        for ih, kh in enumerate(selected):
            mode_h = poc.target_modes(float(kh))
            m.K_H = mode_h.copy()
            m.K_MPC = mode_h * float(static.h)
            data = r2.r0.prepare_bridge_data()
            for ib, bgid in enumerate(B2):
                run_index, recs, T = run_pair(
                    data, mode_h, gcoef, bgid, float(kh),
                    KF_B, NX_B, BOX_B, "B_half", run_index, total_runs,
                )
                all_runs.extend(recs)
                if T is not None:
                    Amid[ib, ih, :] = T
                append_response_rows(response_rows, "B_half", bgid, kh, T)
    finally:
        m.K_MPC = old_kmpc
        m.K_H = old_kh

    stageB_runs = all_runs[len(stageA_runs):]
    Pmid = np.mean(np.abs(Amid)**2, axis=0)
    Tmid = np.mean(Amid, axis=0)

    power_rows = []
    transfer_desc = []
    power_l2 = []
    power_peak = []
    pinterp_all = []
    spike_ok = True
    spike_max_ratio = 0.0
    spike_failures = []
    for iz, z in enumerate(CHECK_Z):
        pred = pl.power_interp(KFULL, Pb2[:, iz], selected)
        direct = Pmid[:, iz]
        ep = pl.rel_real(pred, direct)
        epeak = float(np.max(np.abs(pred - direct)) / max(float(np.max(direct)), 1e-300))
        power_l2.append(ep)
        power_peak.append(epeak)
        pinterp_all.append(pred)
        power_rows.append({"z": float(z), "power_L2": float(ep), "power_peak": float(epeak)})
        tpred = pl.complex_interp(KFULL, Tb2[:, iz], selected)
        transfer_desc.append({"z": float(z), "transfer_L2_descriptive": float(pl.rel(tpred, Tmid[:, iz]))})
        pmax = float(np.max(Pb2[:, iz]))
        floor = 1e-14 * pmax
        for ih, kh in enumerate(selected):
            right = int(np.searchsorted(KFULL, kh))
            left = right - 1
            den = max(float(Pb2[left, iz]), float(Pb2[right, iz]), floor, 1e-300)
            ratio = float(direct[ih] / den)
            spike_max_ratio = max(spike_max_ratio, ratio)
            limit = SPIKE_FACTOR * max(float(Pb2[left, iz]), float(Pb2[right, iz])) + floor
            if float(direct[ih]) > limit:
                spike_ok = False
                spike_failures.append({
                    "z": float(z), "k_h_Mpc_inv": float(kh), "ratio": ratio,
                    "direct_power": float(direct[ih]), "left_power": float(Pb2[left, iz]),
                    "right_power": float(Pb2[right, iz]),
                })
    pinterp_all = np.asarray(pinterp_all, float).T
    interp_nonneg = bool(np.all(np.isfinite(pinterp_all)) and np.all(pinterp_all >= 0.0))

    stageA_health = bool(
        len(stageA_runs) == 44
        and all(health_ok(r) for r in stageA_runs)
    )
    stageA_sat = float(max([r.get("sat_max", np.inf) for r in stageA_runs], default=np.inf))
    stageB_health = bool(
        len(stageB_runs) == 64
        and all(health_ok(r) for r in stageB_runs)
        and np.all(np.isfinite(Amid))
    )
    stageB_sat = float(max([r.get("sat_max", np.inf) for r in stageB_runs], default=np.inf))

    overlap_pass = bool(
        np.all(np.isfinite(A_overlap))
        and overlap_t_global <= OVERLAP_T_GLOBAL_GATE
        and overlap_t_max <= OVERLAP_T_PERK_GATE
        and overlap_p_global <= OVERLAP_P_GLOBAL_GATE
        and overlap_p_max <= OVERLAP_P_PERK_GATE
    )
    hybrid_sanity = bool(
        np.all(np.isfinite(Ahybrid)) and np.all(np.isfinite(Phybrid))
        and np.all(Phybrid >= 0.0) and alg <= ALG_GATE
    )

    gates = {
        "KR_G1_provenance_and_frozen_identity": bool(all(ancestry.values()) and frozen),
        "KR_G2_overlap_reuse_certification": overlap_pass,
        "KR_G3_stageA_repaired_health_and_saturation": bool(stageA_health and stageA_sat <= SAT_GATE),
        "KR_G4_repaired_hybrid_power_sanity": hybrid_sanity,
        "KR_G5_stageB_repaired_health_and_saturation": bool(stageB_health and stageB_sat <= SAT_GATE),
        "KR_G6_repaired_half_lattice_power_interpolation_accuracy": bool(
            interp_nonneg
            and max(power_l2) <= POWER_L2_MAX_GATE
            and float(np.median(power_l2)) <= POWER_L2_MED_GATE
            and max(power_peak) <= POWER_PEAK_GATE
        ),
        "KR_G7_no_unresolved_repaired_half_lattice_power_spike": bool(spike_ok),
    }
    classification = PASS if all(gates.values()) else FAIL

    summary = {
        "runs_expected": 108,
        "runs_finite": int(sum(bool(r.get("finite", False)) for r in all_runs)),
        "canonical_max": float(max([r.get("canonical_max", np.inf) for r in all_runs], default=np.inf)),
        "metric_max": {
            key: float(max([r.get("metric_max", {}).get(key, np.inf) for r in all_runs], default=np.inf))
            for key in ("hamiltonian", "momentum", "shear")
        },
        "broadband_saturation_max": float(max(stageA_sat, stageB_sat)),
        "overlap_response_global_relative_L2": float(overlap_t_global),
        "overlap_response_per_k_max": float(overlap_t_max),
        "overlap_power_global_relative_L2": float(overlap_p_global),
        "overlap_power_per_k_max": float(overlap_p_max),
        "power_half_L2_max": float(max(power_l2)),
        "power_half_L2_median": float(np.median(power_l2)),
        "power_half_peak_max": float(max(power_peak)),
        "spike_max_ratio": float(spike_max_ratio),
        "power_identity_relative_L2": float(alg),
        "selected_half": selected.tolist(),
    }

    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "ancestry": ancestry,
        "frozen_setup": frozen,
        "coefficient_sha256": digest,
        "original_R2_mask_identity": identity,
        "metric_kmax_h": float(kmask.METRIC_KMAX_H),
        "K_overlap": K_OVERLAP.tolist(),
        "K_repair": K_REPAIR.tolist(),
        "selected_half": selected.tolist(),
        "selection": selection_rows,
        "overlap_regression": {
            "global": {"response_relative_L2": float(overlap_t_global), "power_relative_L2": float(overlap_p_global)},
            "per_k": overlap_rows,
            "response_per_k_max": float(overlap_t_max),
            "power_per_k_max": float(overlap_p_max),
        },
        "power_half_by_z": power_rows,
        "transfer_half_descriptive_by_z": transfer_desc,
        "spike_failures": spike_failures,
        "summary": summary,
        "gates": gates,
        "historical_power_lattice_classification": hist_meta.get("classification"),
        "historical_power_lattice_summary": hist_meta.get("summary", {}),
        "repair_classification": repair_meta.get("classification"),
        "STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_TESTED": bool(classification == PASS),
        "STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED": False,
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
    }

    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(
        args.npz_out,
        redshifts=CHECK_Z,
        K_full=KFULL,
        K_overlap=K_OVERLAP,
        K_repair=K_REPAIR,
        selected_half=selected,
        response_hybrid_B2=Ahybrid,
        power_hybrid_B2=Phybrid,
        response_overlap_new=A_overlap,
        response_overlap_historical=A_overlap_ref,
        response_repair_new=A_repair,
        response_half_new=Amid,
        power_half_new=np.abs(Amid)**2,
        power_interp_half=pinterp_all,
        node_curvature=node_curv,
        interval_curvature=interval_curv,
    )
    with open(args.csv_out, "w", newline="") as f:
        fields = ["stage", "background", "k_h_Mpc_inv", "z", "T_real", "T_imag", "P_tag"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(response_rows)

    print("FULLJ_POWER_KMASK_REG_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_POWER_KMASK_REG_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_POWER_KMASK_REG_CLASSIFICATION=" + classification, flush=True)
    print("STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_TESTED=" + str(classification == PASS), flush=True)
    return 0 if classification == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
