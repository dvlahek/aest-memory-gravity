#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6 import full_j_baryonic_reclosure as base
from fullj_poc import cosmological_reclosure_poc as poc
from fullj_dense import dense_reclosure_map as dense
from fullj_jacobian import mode_coupling_jacobian as jac

LOCKED_CLASSIFICATION = "FULLJ_MODE_COUPLING_JACOBIAN_NODE_COUPLING_SUPPORTED"
TARGET_Z = np.asarray([0.25, 0.5, 1.0], float)
K_MPC = dense.K_MPC.copy()
MODE_NUM = dense.MODE_NUM.copy()
NX = int(dense.NX)
KINDS = dense.KINDS
BETAS = dense.BETAS
R1_GATE = dense.R1_GATE
R2_GATE = dense.R2_GATE
TAN_GATE = jac.TAN_GATE
UV_SLOPE_GATE = -1.0
SOURCE_AMP_REL_GATE = 1.0e-12
NODE_Z = 0.25
NODE_K = 0.60
NODE_OFFDIAG_GATE = 0.5
NODE_ROBUST_MIN = 21

PHASE_SETS = {
    "phase_A": np.asarray([
        4.167214657924744, 2.672432702480094, 3.5341498149062374,
        5.077383887606448, 4.573110704763701, 3.4622005659026267,
        4.753835493961269, 1.89751356616761, 1.9121953637074844,
        0.38760824402413774, 5.154893423159532, 3.8118014091722583,
        2.8996246080357104,
    ], float),
    "phase_B": np.asarray([
        1.3870680736241223, 5.8019639397798555, 3.783486433172698,
        6.170369078715129, 0.26412149706240456, 0.16866257796458514,
        0.1985986345216254, 3.7862899814080397, 2.948633738603995,
        5.712223751710549, 4.863919196461439, 4.932350924441611,
        2.5646666361967436,
    ], float),
    "phase_C": np.asarray([
        1.3473795964124813, 2.219831228060226, 1.8723801211612567,
        3.428988935765355, 1.2614275369065642, 3.7339560520169823,
        5.845364428719217, 1.7325476776444173, 3.3708921682007578,
        2.0113011776860024, 4.326327283744503, 0.28834099458887397,
        3.445328907327752,
    ], float),
}


def rel(a, b) -> float:
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(bb), 1.0e-300))


def k_index(target: float) -> int:
    w = np.where(np.isclose(K_MPC, target, rtol=0.0, atol=1.0e-12))[0]
    if len(w) != 1:
        raise RuntimeError(f"missing/nonunique k={target}")
    return int(w[0])


def select_dense_transfers():
    # Exact same orchestration as the corrected locked Jacobian: request the
    # full dense z grid from CLASS first, then select the three target z values.
    dense.configure_upstream()
    transfers, classy_module = poc.extract_baryon_transfers()
    selected = []
    for z in TARGET_Z:
        match = [tr for tr in transfers if abs(float(tr["z"]) - float(z)) < 1.0e-12]
        if len(match) != 1:
            raise RuntimeError(f"expected one dense transfer at z={z:g}, got {len(match)}")
        selected.append(match[0])
    return selected, classy_module, len(transfers)


def set_phase(phases: np.ndarray) -> None:
    p = np.asarray(phases, float)
    if p.shape != (len(K_MPC),):
        raise RuntimeError("phase vector length mismatch")
    poc.PHASE = p.copy()
    jac.PHASE = p.copy()
    base.PHASE = p.copy()
    poc.configure_periodic_grid()


def locked_reference_map(locked: dict):
    refs = {}
    for rec in locked["records"]:
        key = (round(float(rec["z"]), 12), str(rec["kind"]), float(rec["beta0"]))
        refs[key] = np.asarray([m["abs_rhs_mode"] for m in rec["raw_mode_response"]], float)
    return refs


def rhs_mode_abs(rhs: np.ndarray) -> np.ndarray:
    ch = np.fft.fft(np.asarray(rhs, float)) / len(rhs)
    return np.asarray([abs(ch[int(m)]) for m in MODE_NUM], float)


def node_covariance_metrics(Kabs: np.ndarray, rhs_abs: np.ndarray):
    i = k_index(NODE_K)
    variances = np.asarray(rhs_abs, float) ** 2
    pos = variances[variances > 0.0]
    if pos.size == 0:
        raise RuntimeError("zero frozen-shape covariance")
    variances = variances / float(np.median(pos))
    row = np.asarray(Kabs[i, :], float)
    contrib = row * row * variances
    full = float(np.sum(contrib))
    diag = float(contrib[i])
    ratio = full / max(diag, 1.0e-300)
    off = 1.0 - diag / max(full, 1.0e-300)
    return ratio, off


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--locked-json", default="results/fullj_mode_coupling_jacobian.json")
    ap.add_argument("--json-out", default="results/fullj_phase_robustness.json")
    ap.add_argument("--csv-out", default="results/fullj_phase_robustness_summary.csv")
    args = ap.parse_args()

    locked_path = Path(args.locked_json)
    if not locked_path.exists():
        raise FileNotFoundError(locked_path)
    locked = json.loads(locked_path.read_text())
    if locked.get("classification") != LOCKED_CLASSIFICATION or not locked.get("diagnostic_complete", False):
        raise RuntimeError("locked Jacobian input identity failed")
    refs = locked_reference_map(locked)

    transfers, classy_module, full_z_count = select_dense_transfers()
    print("FULLJ_PHASE_START", flush=True)
    print(f"FULLJ_PHASE_CLASS_TRANSFER_READY classy={classy_module} full_z_count={full_z_count}", flush=True)
    print(f"phase_sets={len(PHASE_SETS)} backgrounds={len(PHASE_SETS)*len(TARGET_Z)*len(KINDS)*len(BETAS)} tangent_solves={len(PHASE_SETS)*len(TARGET_Z)*len(KINDS)*len(BETAS)*len(K_MPC)}", flush=True)

    records = []
    incomplete = False
    source_reg_max = 0.0

    for phase_name, phases in PHASE_SETS.items():
        set_phase(phases)
        print("FULLJ_PHASE_SET name=" + phase_name + " phases=" + ",".join(f"{x:.17g}" for x in phases), flush=True)

        for tr in transfers:
            z = float(tr["z"])
            db = np.asarray(tr["d_b"], float)
            delta, source, a = base.source_for(db, z, NX)
            print(f"FULLJ_PHASE_SNAPSHOT phase={phase_name} z={z:g} delta_rms={np.sqrt(np.mean(delta*delta)):.12e}", flush=True)

            for kind in KINDS:
                for beta in BETAS:
                    label = f"{phase_name}_z{z:g}_{kind}_b{beta:g}"
                    sol = poc.constitutive_continue(source, a, beta, kind)
                    rec = {
                        "label": label,
                        "phase_set": phase_name,
                        "z": z,
                        "a": float(a),
                        "kind": kind,
                        "beta0": float(beta),
                        "solver_success": bool(sol["success"]),
                        "solver_reason": sol["reason"],
                    }
                    if not sol["success"]:
                        incomplete = True
                        rec.update({"baseline_valid": False, "jacobian_success": False})
                        records.append(rec)
                        print(f"FULLJ_PHASE_FAIL label={label} reason={sol['reason']}", flush=True)
                        continue

                    chi = np.asarray(sol["chi"], float)
                    d, _, phi = base.diagnostics(chi, sol["rhs"], a, beta, kind)
                    baseline_valid = bool(
                        d["finite"]
                        and d["R2_relative_L2"] <= R2_GATE
                        and d["R1_relative_L2"] <= R1_GATE
                    )
                    rec["baseline_valid"] = baseline_valid
                    rec["R2_relative_L2"] = float(d["R2_relative_L2"])
                    rec["R1_relative_L2"] = float(d["R1_relative_L2"])
                    if not baseline_valid:
                        incomplete = True
                        rec["jacobian_success"] = False
                        records.append(rec)
                        print(f"FULLJ_PHASE_RESIDUAL_FAIL label={label} R2={d['R2_relative_L2']:.3e} R1={d['R1_relative_L2']:.3e}", flush=True)
                        continue

                    raw_modes, raw_slope, raw_mono = dense.dense_mode_response(phi, sol["phi_hg"], sol["rhs"], a)
                    rhs_abs = rhs_mode_abs(sol["rhs"])
                    ref_key = (round(z, 12), str(kind), float(beta))
                    if ref_key not in refs:
                        raise RuntimeError(f"locked source reference missing for {ref_key}")
                    source_rel = rel(rhs_abs, refs[ref_key])
                    source_reg_max = max(source_reg_max, source_rel)
                    source_ok = bool(source_rel <= SOURCE_AMP_REL_GATE)
                    if not source_ok:
                        incomplete = True

                    jres = jac.solve_local_jacobian(chi, a, beta, kind)
                    rec["jacobian_success"] = bool(jres["success"])
                    finite_t = np.asarray(jres["tangent_residual"], float)
                    tanmax = float(np.nanmax(finite_t)) if np.any(np.isfinite(finite_t)) else math.inf
                    rec["tangent_residual_max"] = tanmax
                    if not jres["success"] or not np.isfinite(tanmax) or tanmax > TAN_GATE:
                        incomplete = True
                        records.append(rec)
                        print(f"FULLJ_PHASE_TANGENT_FAIL label={label} reason={jres['reason']} tanmax={tanmax:.3e}", flush=True)
                        continue

                    Kc = np.asarray(jres["K_complex"], complex)
                    Kabs = np.abs(Kc)
                    diag = np.diag(Kabs)
                    hi = K_MPC >= 0.40 - 1.0e-12
                    diag_slope = float(np.polyfit(np.log(K_MPC[hi]), np.log(np.maximum(diag[hi], 1.0e-300)), 1)[0])
                    diag_uv = bool(diag_slope <= UV_SLOPE_GATE)

                    node_ratio = math.nan
                    node_off = math.nan
                    node_majority = False
                    if abs(z - NODE_Z) < 1.0e-12:
                        node_ratio, node_off = node_covariance_metrics(Kabs, rhs_abs)
                        node_majority = bool(node_off > NODE_OFFDIAG_GATE)

                    rec.update({
                        "source_amplitude_regression_rel": source_rel,
                        "source_amplitude_regression_pass": source_ok,
                        "raw_highk_log_slope_T_phi": float(raw_slope),
                        "raw_highk_T_phi_monotone": bool(raw_mono),
                        "diag_highk_log_slope": diag_slope,
                        "diag_uv_stable": diag_uv,
                        "node_frozen_shape_full_to_diag_power_ratio": float(node_ratio),
                        "node_frozen_shape_offdiag_fraction": float(node_off),
                        "node_offdiag_majority": bool(node_majority),
                    })
                    records.append(rec)
                    print(
                        f"FULLJ_PHASE_RESULT label={label} R2={d['R2_relative_L2']:.3e} R1={d['R1_relative_L2']:.3e} "
                        f"tanmax={tanmax:.3e} sourceRel={source_rel:.3e} diagSlope={diag_slope:.6f} "
                        f"diagUV={diag_uv} nodeOff={node_off:.6f} nodeMajority={node_majority}",
                        flush=True,
                    )

    expected_bg = len(PHASE_SETS) * len(TARGET_Z) * len(KINDS) * len(BETAS)
    complete = [r for r in records if r.get("baseline_valid") and r.get("jacobian_success") and r.get("source_amplitude_regression_pass")]
    diag_stable = [r for r in complete if r.get("diag_uv_stable")]
    node = [r for r in complete if abs(float(r["z"]) - NODE_Z) < 1.0e-12]
    node_majority = [r for r in node if r.get("node_offdiag_majority")]

    all_numerical = bool(len(complete) == expected_bg and not incomplete)
    if not all_numerical:
        classification = "FULLJ_PHASE_ROBUSTNESS_INCONCLUSIVE_SOLVER"
    elif len(diag_stable) != expected_bg:
        classification = "FULLJ_PHASE_ROBUSTNESS_LOCAL_UV_STRUCTURE_CHANGED"
    elif len(node_majority) < NODE_ROBUST_MIN:
        classification = "FULLJ_PHASE_ROBUSTNESS_NODE_COUPLING_PHASE_SENSITIVE"
    else:
        classification = "FULLJ_PHASE_ROBUSTNESS_PASS"

    slopes = np.asarray([r["diag_highk_log_slope"] for r in complete], float)
    node_off = np.asarray([r["node_frozen_shape_offdiag_fraction"] for r in node], float)
    node_rat = np.asarray([r["node_frozen_shape_full_to_diag_power_ratio"] for r in node], float)
    summary = {
        "expected_new_backgrounds": expected_bg,
        "complete_new_backgrounds": len(complete),
        "expected_new_tangent_solves": expected_bg * len(K_MPC),
        "diag_uv_stable_new_backgrounds": len(diag_stable),
        "source_amplitude_regression_max_rel": source_reg_max,
        "diag_slope_min": float(np.min(slopes)) if slopes.size else math.nan,
        "diag_slope_median": float(np.median(slopes)) if slopes.size else math.nan,
        "diag_slope_max": float(np.max(slopes)) if slopes.size else math.nan,
        "z0p25_new_node_cases": len(node),
        "z0p25_node_offdiag_majority_cases": len(node_majority),
        "z0p25_node_offdiag_fraction_min": float(np.min(node_off)) if node_off.size else math.nan,
        "z0p25_node_offdiag_fraction_median": float(np.median(node_off)) if node_off.size else math.nan,
        "z0p25_node_offdiag_fraction_max": float(np.max(node_off)) if node_off.size else math.nan,
        "z0p25_node_full_to_diag_ratio_min": float(np.min(node_rat)) if node_rat.size else math.nan,
        "z0p25_node_full_to_diag_ratio_median": float(np.median(node_rat)) if node_rat.size else math.nan,
        "z0p25_node_full_to_diag_ratio_max": float(np.max(node_rat)) if node_rat.size else math.nan,
    }

    out = {
        "classification": classification,
        "diagnostic_complete": bool(all_numerical),
        "locked_input_classification": LOCKED_CLASSIFICATION,
        "phase_sets": {k: v.tolist() for k, v in PHASE_SETS.items()},
        "z": TARGET_Z.tolist(),
        "k_Mpc": K_MPC.tolist(),
        "gates": {
            "R2_relative_L2_max": R2_GATE,
            "R1_relative_L2_max": R1_GATE,
            "tangent_relative_residual_max": TAN_GATE,
            "source_amplitude_regression_rel_max": SOURCE_AMP_REL_GATE,
            "diag_highk_slope_max": UV_SLOPE_GATE,
            "node_offdiag_fraction_strict_min": NODE_OFFDIAG_GATE,
            "node_majority_cases_min": NODE_ROBUST_MIN,
        },
        "summary": summary,
        "records": records,
        "original_locked_phase_not_counted_in_new_gate": True,
        "no_further_phase_count_ladder_preregistered": True,
        "static_snapshot_only": True,
        "evolving_flrw_weyl_power_licensed": False,
        "act_likelihood_used": False,
        "act_likelihood_licensed": False,
        "observational_claim_licensed": False,
    }

    jout = Path(args.json_out)
    cout = Path(args.csv_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    cout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

    fields = [
        "phase_set", "z", "kind", "beta0", "baseline_valid", "jacobian_success",
        "R2_relative_L2", "R1_relative_L2", "tangent_residual_max",
        "source_amplitude_regression_rel", "source_amplitude_regression_pass",
        "diag_highk_log_slope", "diag_uv_stable", "raw_highk_log_slope_T_phi",
        "raw_highk_T_phi_monotone", "node_frozen_shape_full_to_diag_power_ratio",
        "node_frozen_shape_offdiag_fraction", "node_offdiag_majority",
    ]
    with cout.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in records:
            w.writerow({name: r.get(name, math.nan) for name in fields})

    print("FULLJ_PHASE_SUMMARY " + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_PHASE_CLASSIFICATION=" + classification, flush=True)
    print("NO_FURTHER_PHASE_COUNT_LADDER_PREREGISTERED=True", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_PHASE_JSON=" + str(jout), flush=True)
    print("FULLJ_PHASE_CSV=" + str(cout), flush=True)
    return 0 if all_numerical else 1


if __name__ == "__main__":
    raise SystemExit(main())
