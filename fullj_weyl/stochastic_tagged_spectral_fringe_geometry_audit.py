#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import metric_projection_physical_kmask_repair as kmask
from fullj_weyl import stochastic_tagged_spike_source_localization as sl

poc = sl.poc
r2 = sl.r2
m = sl.m
static = sl.static

KMASK_RESULT_LOCK = "20151ab785e923de20d720f3fdd8890576b6cc05"
REG_FAIL_RESULT_LOCK = "9f5218629901643574373e32c84d137c9cda2494"
QUARTER_FAIL_RESULT_LOCK = "c1dd14b2d15fcd48519c328eb4906ef5d1b265b4"
SOURCE_RUNNER_LOCK = "a1b7305cef99f5a61a2af49101cc875a5de0fdc3"
FRINGE_NOTE_LOCK = "1dcafa0643fa99e5de527dcb4a66589814ec6301"
SOURCE_RESULT_LOCK = "86ab13ffa1048860731f65348074ede1b469c644"
PREDATA_LOCK = "3039f8378af06c7ceecd1932fa5ec93890d971e7"

PASS = "FULLJ_STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_CERTIFIED"
FAIL = "FULLJ_STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_FAIL"
INCOMPLETE = "FULLJ_STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_INCOMPLETE"

REG_JSON = ROOT / "results/fullj_stochastic_tagged_power_lattice_kmask_regression.json"
REG_NPZ = ROOT / "results/fullj_stochastic_tagged_power_lattice_kmask_regression.npz"
REG_NPZ_SHA256 = "83fb7462ec970bfef953e3804d11a81fd5843745347fe77c318c9e39b8e6e82d"
SOURCE_JSON = ROOT / "results/fullj_stochastic_tagged_spike_source_localization.json"
SOURCE_NPZ = ROOT / "results/fullj_stochastic_tagged_spike_source_localization.npz"
SOURCE_NPZ_SHA256 = "f18aaa614fa72ccbb0e63a10e7bb49c51bd69b15e806ac7ba69e0f61b52ffa91"
COEFF_HASH = "9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200"

BG = 0
EPS = 0.05
NSTEP = 4096
KF = 0.00125
NX = 1024
BOX = 2.0 * np.pi / (KF * float(static.h))
CHECK_Z = np.asarray(sl.CHECK_Z, float)
TARGETS = np.asarray([0.1000, 0.1025, 0.1625, 0.1650, 0.1950, 0.1975], float)

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
SAT_GATE = 2.0e-2
T_GLOBAL_GATE = 1.0e-4
P_GLOBAL_GATE = 2.0e-4
T_PERK_GATE = 3.0e-4


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def idx(grid, value):
    q = np.where(np.isclose(np.asarray(grid, float), float(value), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"nonunique/missing grid value {value}")
    return int(q[0])


def rel_complex(a, b):
    aa = np.asarray(a, complex); bb = np.asarray(b, complex)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def rel_real(a, b):
    aa = np.asarray(a, float); bb = np.asarray(b, float)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def load_locked_inputs():
    for p in (REG_JSON, REG_NPZ, SOURCE_JSON, SOURCE_NPZ):
        if not p.exists():
            raise FileNotFoundError(f"missing locked local input {p}")
    reg_digest = sha256_file(REG_NPZ)
    src_digest = sha256_file(SOURCE_NPZ)
    if reg_digest != REG_NPZ_SHA256:
        raise RuntimeError(f"repaired-regression NPZ SHA mismatch {reg_digest}")
    if src_digest != SOURCE_NPZ_SHA256:
        raise RuntimeError(f"source-localization NPZ SHA mismatch {src_digest}")

    reg_meta = json.loads(REG_JSON.read_text())
    src_meta = json.loads(SOURCE_JSON.read_text())
    if reg_meta.get("classification") != "FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_FAIL":
        raise RuntimeError("repaired-regression JSON classification mismatch")
    if src_meta.get("classification") != "FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_SATURATED_MODE_SUPPORTED":
        raise RuntimeError("source-localization JSON classification mismatch")

    rq = np.load(REG_NPZ)
    sq = np.load(SOURCE_NPZ)
    req_reg = {"redshifts", "K_full", "selected_half", "response_hybrid_B2", "response_half_new"}
    req_src = {"redshifts", "local_nodes", "baseline__W_total"}
    if not req_reg.issubset(rq.files):
        raise RuntimeError(f"regression NPZ missing {sorted(req_reg-set(rq.files))}")
    if not req_src.issubset(sq.files):
        raise RuntimeError(f"source NPZ missing {sorted(req_src-set(sq.files))}")

    zreg = np.asarray(rq["redshifts"], float)
    zsrc = np.asarray(sq["redshifts"], float)
    if not np.allclose(zreg, CHECK_Z, rtol=0, atol=5e-13) or not np.allclose(zsrc, CHECK_Z, rtol=0, atol=5e-13):
        raise RuntimeError("redshift grid mismatch")

    kfull = np.asarray(rq["K_full"], float)
    khalf = np.asarray(rq["selected_half"], float)
    afull = np.asarray(rq["response_hybrid_B2"], complex)
    ahalf = np.asarray(rq["response_half_new"], complex)
    if afull.shape[0] < 1 or ahalf.shape[0] < 1:
        raise RuntimeError("missing bg0 repaired parent response")

    refs = []
    source_kind = []
    for kh in TARGETS:
        qf = np.where(np.isclose(kfull, kh, rtol=0, atol=5e-13))[0]
        qh = np.where(np.isclose(khalf, kh, rtol=0, atol=5e-13))[0]
        if len(qf) == 1:
            refs.append(np.asarray(afull[BG, int(qf[0]), :], complex)); source_kind.append("K_full")
        elif len(qh) == 1:
            refs.append(np.asarray(ahalf[BG, int(qh[0]), :], complex)); source_kind.append("selected_half")
        else:
            raise RuntimeError(f"target {kh} absent from repaired parent")
    refs = np.stack(refs, axis=0)

    src_nodes = np.asarray(sq["local_nodes"], float)
    src_resp = np.asarray(sq["baseline__W_total"], complex)
    if src_resp.shape != (len(src_nodes), len(CHECK_Z)) or not np.all(np.isfinite(src_resp)):
        raise RuntimeError("bad source-localization baseline profile")
    return reg_digest, src_digest, refs, source_kind, src_nodes, src_resp


def health_ok(rec):
    return bool(
        rec.get("finite", False)
        and float(rec.get("canonical_max", np.inf)) <= CANONICAL_GATE
        and all(float(v) <= METRIC_GATE for v in rec.get("metric_max", {}).values())
        and float(rec.get("sat_max", np.inf)) <= SAT_GATE
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_stochastic_tagged_spectral_fringe_geometry_audit.json")
    ap.add_argument("--npz-out", default="results/fullj_stochastic_tagged_spectral_fringe_geometry_audit.npz")
    ap.add_argument("--csv-out", default="results/fullj_stochastic_tagged_spectral_fringe_geometry_audit.csv")
    args = ap.parse_args()

    ancestry = {
        "physical_kmask_repair_result_lock": is_ancestor(KMASK_RESULT_LOCK),
        "repaired_regression_fail_result_lock": is_ancestor(REG_FAIL_RESULT_LOCK),
        "quarter_fail_result_lock": is_ancestor(QUARTER_FAIL_RESULT_LOCK),
        "source_localization_runner_lock": is_ancestor(SOURCE_RUNNER_LOCK),
        "spectral_fringe_note_lock": is_ancestor(FRINGE_NOTE_LOCK),
        "source_localization_result_lock": is_ancestor(SOURCE_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    _, gcoef, coeff_digest = poc.coeff_draw()
    identity = kmask.original_r2_mask_identity(128)
    exact_modes = all(abs(round(float(k)/KF)*KF-float(k)) <= 5e-13 for k in TARGETS)
    frozen = bool(
        coeff_digest == COEFF_HASH
        and BG == 0 and EPS == 0.05 and NSTEP == 4096
        and abs(KF-0.00125) < 1e-15 and NX == 1024
        and abs(float(kmask.METRIC_KMAX_H)-0.32) < 1e-15
        and identity.get("mismatch_count") == 0
        and np.allclose(TARGETS, [0.1000,0.1025,0.1625,0.1650,0.1950,0.1975], rtol=0, atol=5e-14)
        and exact_modes
    )

    print("FULLJ_FRINGE_GEOMETRY_START", flush=True)
    print("FULLJ_FRINGE_GEOMETRY_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_FRINGE_GEOMETRY_COEFFICIENT_SHA256=" + coeff_digest, flush=True)
    print("FULLJ_FRINGE_GEOMETRY_ORIGINAL_IDENTITY=" + json.dumps(identity, sort_keys=True), flush=True)
    print("FULLJ_FRINGE_GEOMETRY_TARGETS=" + json.dumps(TARGETS.tolist()), flush=True)
    print(f"FULLJ_FRINGE_GEOMETRY_GEOMETRY kF_h={KF:.6f} NX={NX} box_Mpc={BOX:.12e}", flush=True)
    print("FULLJ_FRINGE_GEOMETRY_TOTAL_RUNS=12", flush=True)

    try:
        reg_digest, src_digest, refs, source_kind, src_nodes, src_resp = load_locked_inputs()
    except Exception as exc:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry,
               "frozen_setup": frozen, "reason": str(exc)}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("FULLJ_FRINGE_GEOMETRY_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry,
               "frozen_setup": frozen, "regression_npz_sha256": reg_digest,
               "source_npz_sha256": src_digest}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("FULLJ_FRINGE_GEOMETRY_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    responses = np.full((len(TARGETS), len(CHECK_Z)), np.nan+1j*np.nan, complex)
    runs = []
    rows = []
    run_index = 0
    old_kmpc = np.asarray(m.K_MPC, float).copy()
    old_kh = np.asarray(getattr(m, "K_H", []), float).copy()
    try:
        for ik, kh in enumerate(TARGETS):
            mode_h = poc.target_modes(float(kh))
            m.K_H = mode_h.copy()
            m.K_MPC = mode_h * float(static.h)
            data = r2.r0.prepare_bridge_data()
            pair = {}; meta = None
            for sign in (+1, -1):
                run_index += 1
                rec, comps, mm = sl.run_signed(
                    data, mode_h, gcoef[BG], float(kh), int(sign), EPS, NSTEP,
                    KF, NX, BOX, "interleaved_common_geometry", surrogate=False,
                )
                rec["run_index"] = int(run_index)
                runs.append(rec)
                print(
                    f"FULLJ_FRINGE_GEOMETRY_RUN {run_index:02d}/12 k_h={kh:.5f} sign={sign:+d} "
                    + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get("finite")
                       else f"finite=False reason={rec.get('reason','unknown')}"),
                    flush=True,
                )
                if comps is not None:
                    pair[int(sign)] = comps
                    meta = mm
            if set(pair) == {-1, +1} and meta is not None:
                T = sl.pair_response(pair, meta, EPS)["W_total"]
                responses[ik] = T
                for iz, zz in enumerate(CHECK_Z):
                    rows.append({
                        "k_h_Mpc_inv": float(kh), "z": float(zz),
                        "T_new_real": float(np.real(T[iz])), "T_new_imag": float(np.imag(T[iz])),
                        "T_ref_real": float(np.real(refs[ik,iz])), "T_ref_imag": float(np.imag(refs[ik,iz])),
                        "P_new": float(abs(T[iz])**2), "P_ref": float(abs(refs[ik,iz])**2),
                        "reference_source": source_kind[ik],
                    })
    finally:
        m.K_MPC = old_kmpc
        if old_kh.size:
            m.K_H = old_kh

    all_health = len(runs) == 12 and all(health_ok(r) for r in runs)
    canonical_max = max((float(r.get("canonical_max", np.inf)) for r in runs), default=np.inf)
    sat_max = max((float(r.get("sat_max", np.inf)) for r in runs), default=np.inf)
    metric_max = {name: max((float(r.get("metric_max", {}).get(name, np.inf)) for r in runs), default=np.inf)
                  for name in ("hamiltonian", "momentum", "shear")}

    finite_resp = bool(np.all(np.isfinite(responses)))
    tglob = rel_complex(responses, refs) if finite_resp else float("inf")
    pglob = rel_real(np.abs(responses)**2, np.abs(refs)**2) if finite_resp else float("inf")
    per_k = [rel_complex(responses[i], refs[i]) for i in range(len(TARGETS))] if finite_resp else [float("inf")]*len(TARGETS)
    per_k_max = float(max(per_k))

    merged_k = np.concatenate([src_nodes, TARGETS])
    merged_T = np.concatenate([src_resp, responses], axis=0)
    order = np.argsort(merged_k)
    merged_k = merged_k[order]
    merged_T = merged_T[order]
    unique = bool(len(merged_k) == 15 and np.all(np.diff(merged_k) > 5e-13) and np.all(np.isfinite(merged_T)))

    gates = {
        "IG_G1_provenance_and_exact_setup": bool(all(ancestry.values()) and frozen),
        "IG_G2_numerical_health": bool(all_health),
        "IG_G3_same_k_interleaved_geometry_invariance": bool(
            finite_resp and tglob <= T_GLOBAL_GATE and pglob <= P_GLOBAL_GATE and per_k_max <= T_PERK_GATE
        ),
        "IG_G4_common_geometry_profile_construction": bool(unique),
    }
    classification = PASS if all(gates.values()) else FAIL

    summary = {
        "runs_expected": 12, "runs_finite": int(sum(bool(r.get("finite", False)) for r in runs)),
        "canonical_max": float(canonical_max), "saturation_max": float(sat_max), "metric_max": metric_max,
        "response_global_relative_L2": float(tglob), "power_global_relative_L2": float(pglob),
        "response_per_k": [float(x) for x in per_k], "response_per_k_max": float(per_k_max),
        "merged_profile_nodes": int(len(merged_k)),
    }

    out = {
        "classification": classification, "diagnostic_complete": True, "ancestry": ancestry,
        "frozen_setup": frozen, "coefficient_sha256": coeff_digest,
        "regression_npz_sha256": reg_digest, "source_npz_sha256": src_digest,
        "targets": TARGETS.tolist(), "reference_source": source_kind,
        "summary": summary, "gates": gates, "runs": runs,
        "licenses": {
            "STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_CERTIFIED": bool(classification == PASS),
            "STOCHASTIC_TAGGED_SATURATED_MODE_MECHANISM_SUPPORTED": True,
            "STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED": False,
            "EVOLVING_WEYL_POWER_LICENSED": False,
            "ACT_LIKELIHOOD_LICENSED": False,
            "OBSERVATIONAL_CLAIM_LICENSED": False,
        },
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez(
        args.npz_out, redshifts=CHECK_Z, targets=TARGETS, response_new=responses,
        response_reference=refs, source_local_nodes=src_nodes, source_local_response=src_resp,
        merged_nodes=merged_k, merged_response=merged_T,
    )
    with open(args.csv_out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["k_h_Mpc_inv"])
        w.writeheader(); w.writerows(rows)

    print("FULLJ_FRINGE_GEOMETRY_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_FRINGE_GEOMETRY_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_FRINGE_GEOMETRY_CLASSIFICATION=" + classification, flush=True)
    print("STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_CERTIFIED=" + str(classification == PASS), flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
