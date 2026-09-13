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
QUARTER_FAIL_RESULT_LOCK = "c1dd14b2d15fcd48519c328eb4906ef5d1b265b4"
SOURCE_RESULT_LOCK = "86ab13ffa1048860731f65348074ede1b469c644"
GEOMETRY_RESULT_LOCK = "73fb42d64e61d69820d31a9c9f71c8d536b2376e"
PREDATA_LOCK = "82554256e89829b906e652700cbe5110bcbbecfb"

CLASS_DOMINATED = "FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_CORRECTED_CLASS_LINEAR_SECTOR_DOMINATED"
INTERNAL_REQUIRED = "FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_INTERNAL_CORRECTION_REQUIRED"
NUMERICAL_FAIL = "FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_NUMERICAL_CONTROL_FAIL"
INCOMPLETE = "FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_INCOMPLETE"

SOURCE_JSON = ROOT / "results/fullj_stochastic_tagged_spike_source_localization.json"
SOURCE_NPZ = ROOT / "results/fullj_stochastic_tagged_spike_source_localization.npz"
SOURCE_NPZ_SHA256 = "f18aaa614fa72ccbb0e63a10e7bb49c51bd69b15e806ac7ba69e0f61b52ffa91"
GEOM_JSON = ROOT / "results/fullj_stochastic_tagged_spectral_fringe_geometry_audit.json"
GEOM_NPZ = ROOT / "results/fullj_stochastic_tagged_spectral_fringe_geometry_audit.npz"
GEOM_NPZ_SHA256 = "1a69f04e43a7e6837dead23a837ed40dcb46ed4e753f65a64abf7f4a4fdfce39"
COEFF_HASH = "9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200"

BG = 0
EPS = 0.05
NSTEP = 4096
KF = 0.00125
NX = 1024
BOX = 2.0 * np.pi / (KF * float(static.h))
CHECK_Z = np.asarray(sl.CHECK_Z, float)
TARGETS = np.asarray([0.1000, 0.1025, 0.1625, 0.1650, 0.1950, 0.1975], float)
WINDOWS = {
    "W1": np.asarray([0.09875, 0.10000, 0.10125, 0.10250, 0.10375], float),
    "W2": np.asarray([0.16125, 0.16250, 0.16375, 0.16500, 0.16625], float),
    "W3": np.asarray([0.19375, 0.19500, 0.19625, 0.19750, 0.19875], float),
}
COMPONENTS = tuple(sl.COMPONENTS)

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
SAT_GATE = 2.0e-2
REPRO_GLOBAL_GATE = 1.0e-8
REPRO_PERK_GATE = 3.0e-8
WEYL_ID_GATE = 1.0e-12
D2_ID_GATE = 1.0e-12
CLASS_CORR_GATE = 0.95
CLASS_ERROR_GATE = 0.30
CORR_FRACTION_GATE = 0.30


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


def safe_corr(a, b):
    aa = np.asarray(a, float); bb = np.asarray(b, float)
    if aa.size < 2 or float(np.std(aa)) <= 1e-300 or float(np.std(bb)) <= 1e-300:
        return float("nan")
    return float(np.corrcoef(aa, bb)[0, 1])


def health_ok(rec):
    return bool(
        rec.get("finite", False)
        and float(rec.get("canonical_max", np.inf)) <= CANONICAL_GATE
        and all(float(v) <= METRIC_GATE for v in rec.get("metric_max", {}).values())
        and float(rec.get("sat_max", np.inf)) <= SAT_GATE
    )


def load_locked_inputs():
    for p in (SOURCE_JSON, SOURCE_NPZ, GEOM_JSON, GEOM_NPZ):
        if not p.exists():
            raise FileNotFoundError(f"missing locked local input {p}")
    sh = sha256_file(SOURCE_NPZ)
    gh = sha256_file(GEOM_NPZ)
    if sh != SOURCE_NPZ_SHA256:
        raise RuntimeError(f"source NPZ SHA mismatch {sh}")
    if gh != GEOM_NPZ_SHA256:
        raise RuntimeError(f"geometry NPZ SHA mismatch {gh}")
    sm = json.loads(SOURCE_JSON.read_text())
    gm = json.loads(GEOM_JSON.read_text())
    if sm.get("classification") != "FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_SATURATED_MODE_SUPPORTED":
        raise RuntimeError("source-localization classification mismatch")
    if gm.get("classification") != "FULLJ_STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_CERTIFIED":
        raise RuntimeError("geometry certification mismatch")

    sq = np.load(SOURCE_NPZ)
    gq = np.load(GEOM_NPZ)
    src_nodes = np.asarray(sq["local_nodes"], float)
    geom_targets = np.asarray(gq["targets"], float)
    geom_ref = np.asarray(gq["response_new"], complex)
    if not np.allclose(geom_targets, TARGETS, rtol=0.0, atol=5e-13):
        raise RuntimeError("geometry target mismatch")
    if geom_ref.shape != (len(TARGETS), len(CHECK_Z)):
        raise RuntimeError(f"geometry response shape mismatch {geom_ref.shape}")
    src = {}
    for name in COMPONENTS:
        key = "baseline__" + name
        if key not in sq.files:
            raise RuntimeError(f"source NPZ missing {key}")
        a = np.asarray(sq[key], complex)
        if a.shape != (len(src_nodes), len(CHECK_Z)):
            raise RuntimeError(f"bad source component shape {name}: {a.shape}")
        src[name] = a
    return sh, gh, src_nodes, src, geom_ref


def merge_profiles(src_nodes, src, new):
    merged_nodes = np.sort(np.concatenate([src_nodes, TARGETS]))
    if len(merged_nodes) != 15 or len(np.unique(np.round(merged_nodes, 12))) != 15:
        raise RuntimeError("merged profile is not 15 unique nodes")
    out = {name: np.zeros((15, len(CHECK_Z)), complex) for name in COMPONENTS}
    for i, kh in enumerate(merged_nodes):
        qs = np.where(np.isclose(src_nodes, kh, rtol=0, atol=5e-13))[0]
        qn = np.where(np.isclose(TARGETS, kh, rtol=0, atol=5e-13))[0]
        if len(qs) == 1:
            for name in COMPONENTS:
                out[name][i] = src[name][int(qs[0])]
        elif len(qn) == 1:
            for name in COMPONENTS:
                out[name][i] = new[name][int(qn[0])]
        else:
            raise RuntimeError(f"merged node source ambiguity at {kh}")
    return merged_nodes, out


def d2_vector(nodes, arr, iz):
    vals = []
    labels = []
    for wname, wg in WINDOWS.items():
        ii = [idx(nodes, k) for k in wg]
        y = np.asarray(arr[ii, iz], complex)
        for j in (1, 2, 3):
            vals.append(y[j+1] - 2.0*y[j] + y[j-1])
            labels.append(f"{wname}:{wg[j]:.5f}")
    return np.asarray(vals, complex), labels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_spectral_fringe_source_decomposition.json")
    ap.add_argument("--npz-out", default="results/fullj_spectral_fringe_source_decomposition.npz")
    ap.add_argument("--csv-out", default="results/fullj_spectral_fringe_source_decomposition.csv")
    args = ap.parse_args()

    ancestry = {
        "physical_kmask_repair_result_lock": is_ancestor(KMASK_RESULT_LOCK),
        "quarter_fail_result_lock": is_ancestor(QUARTER_FAIL_RESULT_LOCK),
        "source_localization_result_lock": is_ancestor(SOURCE_RESULT_LOCK),
        "geometry_certification_result_lock": is_ancestor(GEOMETRY_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    _, gcoef, coeff_digest = poc.coeff_draw()
    identity = kmask.original_r2_mask_identity(128)
    frozen = bool(
        coeff_digest == COEFF_HASH and BG == 0 and EPS == 0.05 and NSTEP == 4096
        and abs(KF-0.00125) < 1e-15 and NX == 1024
        and np.allclose(TARGETS, [0.1000,0.1025,0.1625,0.1650,0.1950,0.1975], rtol=0, atol=5e-14)
        and kmask.REPAIR_ACTIVE is True and identity.get("mismatch_count") == 0
        and abs(float(kmask.METRIC_KMAX_H)-0.32) < 1e-15
    )

    print("FULLJ_FRINGE_SOURCE_DECOMP_START", flush=True)
    print("FULLJ_FRINGE_SOURCE_DECOMP_ANCESTRY="+json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_FRINGE_SOURCE_DECOMP_COEFFICIENT_SHA256="+coeff_digest, flush=True)
    print("FULLJ_FRINGE_SOURCE_DECOMP_TARGETS="+json.dumps(TARGETS.tolist()), flush=True)
    print("FULLJ_FRINGE_SOURCE_DECOMP_TOTAL_RUNS=12", flush=True)

    try:
        src_hash, geom_hash, src_nodes, src, geom_ref = load_locked_inputs()
    except Exception as exc:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry,
               "frozen_setup": frozen, "reason": str(exc)}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("FULLJ_FRINGE_SOURCE_DECOMP_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry,
               "frozen_setup": frozen, "source_npz_sha256": src_hash, "geometry_npz_sha256": geom_hash}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("FULLJ_FRINGE_SOURCE_DECOMP_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    new = {name: np.full((len(TARGETS), len(CHECK_Z)), np.nan+1j*np.nan, complex) for name in COMPONENTS}
    runs = []
    rows = []
    run_index = 0
    old_kmpc = np.asarray(m.K_MPC, float).copy()
    old_kh = np.asarray(getattr(m, "K_H", []), float).copy()
    try:
        for ik, kh in enumerate(TARGETS):
            mode_h = poc.target_modes(float(kh))
            m.K_H = mode_h.copy(); m.K_MPC = mode_h * float(static.h)
            data = r2.r0.prepare_bridge_data()
            pair = {}; meta = None
            for sign in (+1, -1):
                run_index += 1
                rec, comps, mm = sl.run_signed(
                    data, mode_h, gcoef[BG], float(kh), int(sign), EPS, NSTEP,
                    KF, NX, BOX, "source_decomposition_common_geometry", surrogate=False,
                )
                rec["run_index"] = int(run_index)
                runs.append(rec)
                print(
                    f"FULLJ_FRINGE_SOURCE_DECOMP_RUN {run_index:02d}/12 k_h={kh:.5f} sign={sign:+d} "
                    + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get("finite")
                       else f"finite=False reason={rec.get('reason','unknown')}"), flush=True,
                )
                if comps is not None:
                    pair[int(sign)] = comps; meta = mm
            if set(pair) == {-1, +1} and meta is not None:
                resp = sl.pair_response(pair, meta, EPS)
                for name in COMPONENTS:
                    new[name][ik] = resp[name]
                for iz, zz in enumerate(CHECK_Z):
                    rows.append({
                        "k_h_Mpc_inv": float(kh), "z": float(zz),
                        "W_total_real": float(np.real(resp["W_total"][iz])),
                        "W_CLASS_real": float(np.real(resp["W_CLASS"][iz])),
                        "W_corr_real": float(np.real(resp["W_corr"][iz])),
                    })
    finally:
        m.K_MPC = old_kmpc
        if old_kh.size:
            m.K_H = old_kh

    finite = len(runs) == 12 and all(bool(r.get("finite", False)) for r in runs)
    health = finite and all(health_ok(r) for r in runs)
    canonical_max = max((float(r.get("canonical_max", np.inf)) for r in runs), default=float("inf"))
    saturation_max = max((float(r.get("sat_max", np.inf)) for r in runs), default=float("inf"))
    metric_max = {name: max((float(r.get("metric_max", {}).get(name, np.inf)) for r in runs), default=float("inf"))
                  for name in ("hamiltonian", "momentum", "shear")}

    repro_per = [rel_complex(new["W_total"][i], geom_ref[i]) for i in range(len(TARGETS))]
    repro_global = rel_complex(new["W_total"], geom_ref)
    repro_ok = bool(repro_global <= REPRO_GLOBAL_GATE and max(repro_per) <= REPRO_PERK_GATE)

    weyl_id = rel_complex(new["W_total"], new["W_CLASS"] + new["W_corr"])

    try:
        merged_nodes, merged = merge_profiles(src_nodes, src, new)
        iz02 = idx(CHECK_Z, 0.2)
        d2 = {}
        labels = None
        for name in COMPONENTS:
            d2[name], labels = d2_vector(merged_nodes, merged[name], iz02)
        d2_id = rel_complex(d2["W_total"], d2["W_CLASS"] + d2["W_corr"])
        class_corr = safe_corr(np.real(d2["W_CLASS"]), np.real(d2["W_total"]))
        class_err = rel_complex(d2["W_CLASS"], d2["W_total"])
        corr_frac = float(np.linalg.norm(d2["W_corr"]) / max(float(np.linalg.norm(d2["W_total"])), 1e-300))
    except Exception as exc:
        out = {"classification": NUMERICAL_FAIL, "diagnostic_complete": False, "reason": str(exc),
               "runs": runs, "ancestry": ancestry, "frozen_setup": frozen}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("FULLJ_FRINGE_SOURCE_DECOMP_CLASSIFICATION="+NUMERICAL_FAIL, flush=True)
        return 2

    g1 = bool(all(ancestry.values()) and frozen)
    g2 = bool(health and repro_ok)
    g3 = bool(weyl_id <= WEYL_ID_GATE and d2_id <= D2_ID_GATE)
    class_dominated = bool(
        np.isfinite(class_corr) and class_corr >= CLASS_CORR_GATE
        and class_err <= CLASS_ERROR_GATE and corr_frac <= CORR_FRACTION_GATE
    )
    gates = {
        "SD_G1_provenance_and_frozen_setup": g1,
        "SD_G2_numerical_health_and_response_reproduction": g2,
        "SD_G3_decomposition_identity": g3,
        "SD_G4_corrected_CLASS_linear_sector_dominated": class_dominated,
    }

    if g1 and g2 and g3:
        classification = CLASS_DOMINATED if class_dominated else INTERNAL_REQUIRED
        exit_code = 0
    else:
        classification = NUMERICAL_FAIL
        exit_code = 2

    summary = {
        "runs_expected": 12, "runs_finite": int(sum(bool(r.get("finite", False)) for r in runs)),
        "canonical_max": canonical_max, "metric_max": metric_max, "saturation_max": saturation_max,
        "W_total_reproduction_global_relative_L2": repro_global,
        "W_total_reproduction_per_k_max": float(max(repro_per)),
        "weyl_decomposition_relative_residual": weyl_id,
        "D2_decomposition_relative_residual_z0p2": d2_id,
        "D2_CLASS_total_real_correlation_z0p2": class_corr,
        "D2_CLASS_total_relative_L2_z0p2": class_err,
        "D2_Wcorr_fraction_of_total_z0p2": corr_frac,
    }

    out = {
        "classification": classification, "diagnostic_complete": True, "frozen_setup": frozen,
        "ancestry": ancestry, "source_npz_sha256": src_hash, "geometry_npz_sha256": geom_hash,
        "coefficient_sha256": coeff_digest, "targets": TARGETS.tolist(), "merged_nodes": merged_nodes.tolist(),
        "gates": gates, "summary": summary, "D2_labels": labels,
        "thresholds": {
            "canonical": CANONICAL_GATE, "metric": METRIC_GATE, "saturation": SAT_GATE,
            "repro_global": REPRO_GLOBAL_GATE, "repro_per_k": REPRO_PERK_GATE,
            "weyl_identity": WEYL_ID_GATE, "D2_identity": D2_ID_GATE,
            "CLASS_corr": CLASS_CORR_GATE, "CLASS_error": CLASS_ERROR_GATE,
            "Wcorr_fraction": CORR_FRACTION_GATE,
        },
        "runs": runs,
        "licenses": {
            "STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_CERTIFIED": True,
            "SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_TESTED": True,
            "EVOLVING_WEYL_POWER_LICENSED": False,
            "ACT_LIKELIHOOD_LICENSED": False,
            "OBSERVATIONAL_CLAIM_LICENSED": False,
        },
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(
        args.npz_out, redshifts=CHECK_Z, targets=TARGETS,
        source_nodes=src_nodes, merged_nodes=merged_nodes,
        **{"new__"+name: new[name] for name in COMPONENTS},
        **{"merged__"+name: merged[name] for name in COMPONENTS},
        **{"D2_z0p2__"+name: d2[name] for name in COMPONENTS},
    )
    with open(args.csv_out, "w", newline="") as f:
        fields = ["k_h_Mpc_inv", "z", "W_total_real", "W_CLASS_real", "W_corr_real"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

    print("FULLJ_FRINGE_SOURCE_DECOMP_SUMMARY="+json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_FRINGE_SOURCE_DECOMP_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_FRINGE_SOURCE_DECOMP_CLASSIFICATION="+classification, flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
