#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from fullj_weyl import corrected_class_spectral_fringe_bridge_identity as b

ROOT = Path(__file__).resolve().parents[1]
REPAIR_LOCK = "28ec0b77822e932ba0b38a0f22232d7683ece4b3"
FINGERPRINT_GATE = 2.0e-5
FINGERPRINT_ABS_SEPARATION = 1.0e-8
FINGERPRINT_RATIO = 5.0


def fingerprint_match(histories, fingerprint, z):
    vals = [b.eval_at_a(raw, z) for raw in histories]
    dist = np.asarray([b.rel(v, fingerprint) for v in vals], float)
    order = np.argsort(dist)
    j = int(order[0])
    best = float(dist[j])
    second = float(dist[int(order[1])]) if len(order) > 1 else float("inf")
    separated = bool(
        len(order) == 1
        or second - best >= FINGERPRINT_ABS_SEPARATION
        or second >= FINGERPRINT_RATIO * max(best, 1.0e-300)
    )
    ok = bool(best <= FINGERPRINT_GATE and separated)
    return j, vals, {
        "best_index": j,
        "best_relative_L2": best,
        "second_best_relative_L2": second,
        "separated": separated,
        "pass": ok,
        "all_relative_L2": dist.tolist(),
    }


def single_fingerprint(pars, z):
    hs = b.run_histories(pars)
    if len(hs) != 1:
        raise RuntimeError(f"single-k run returned {len(hs)} histories")
    return b.eval_at_a(hs[0], z), hs[0]


def cmp(a, c):
    pp = b.per_k_rel(a, c)
    return b.rel(a, c), float(max(pp)), pp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_corrected_class_spectral_fringe_bridge_identity.json")
    ap.add_argument("--npz-out", default="results/fullj_corrected_class_spectral_fringe_bridge_identity.npz")
    args = ap.parse_args()

    print("FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_R1_START", flush=True)

    for p in (b.EXTRACTOR_JSON, b.EXTRACTOR_NPZ, b.R3_JSON, b.R3_NPZ):
        if not p.exists():
            out = {"classification": b.INCOMPLETE, "diagnostic_complete": False, "reason": f"missing {p}"}
            Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
            print("FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_R1_CLASSIFICATION=" + b.INCOMPLETE, flush=True)
            return 3

    ej = json.loads(b.EXTRACTOR_JSON.read_text())
    eq = np.load(b.EXTRACTOR_NPZ)
    rj = json.loads(b.R3_JSON.read_text())
    rq = np.load(b.R3_NPZ)
    anchors = np.asarray(b.base.K_ANCHOR, float)
    z = np.asarray(b.base.CHECK_Z, float)
    B0 = np.asarray(rq["aest_sparse_W"], float)
    B5 = np.asarray(eq["E3_bridge_tagged"], complex)

    frozen = bool(
        b.is_ancestor(b.PREDATA_LOCK)
        and b.is_ancestor(REPAIR_LOCK)
        and ej.get("classification") == "FULLJ_CLASS_FRINGE_EXTRACTOR_MISMATCH_CERTIFIED"
        and ej.get("interpretation", {}).get("historical_R3_reclassified") is False
        and rj.get("classification") == "FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_NUMERICAL_CONTROL_FAIL"
        and np.allclose(np.asarray(rq["k_anchor_h_Mpc"], float), anchors, rtol=0, atol=5e-13)
        and np.allclose(np.asarray(rq["redshifts"], float), z, rtol=0, atol=5e-13)
        and B0.shape == (15, 9) and B5.shape == (15, 9)
    )

    B1 = np.full_like(B0, np.nan)
    B2 = np.full_like(B0, np.nan)
    B3 = np.full_like(B0, np.nan)
    B4 = np.full_like(B0, np.nan)
    fingerprint_rows = []
    tau_offsets = []
    a_offsets = []
    param_diffs = {}
    fingerprint_ok = True
    positional_ok = True

    for ik, kh in enumerate(anchors):
        mode_h = np.asarray(b.sd.poc.target_modes(float(kh)), float)
        q = np.where(np.isclose(mode_h, float(kh), rtol=0, atol=5e-13))[0]
        if len(q) != 1:
            raise RuntimeError(f"target {kh} not unique in bridge list {mode_h.tolist()}")
        target_pos = int(q[0])

        # Direct/R3 parameter family: isolated target fingerprint + historical bridge list.
        p1_single, _ = b.r3_params([float(kh)])
        f1, _ = single_fingerprint(p1_single, z)
        p1, serial = b.r3_params(mode_h)
        h1 = b.run_histories(p1)
        j1, vals1, diag1 = fingerprint_match(h1, f1, z)
        B1[ik] = vals1[j1]

        # Historical bridge parameter family: isolated target fingerprint + same bridge list.
        p2_single = b.bridge_params([float(kh)])
        f2, _ = single_fingerprint(p2_single, z)
        p2 = b.bridge_params(mode_h)
        h2 = b.run_histories(p2)
        j2, vals2, diag2 = fingerprint_match(h2, f2, z)
        B2[ik] = vals2[j2]

        if target_pos >= len(h2):
            raise RuntimeError(f"historical positional index {target_pos} outside returned histories {len(h2)}")
        B3[ik] = vals2[target_pos]

        this_fp_ok = bool(diag1["pass"] and diag2["pass"])
        fingerprint_ok = fingerprint_ok and this_fp_ok
        this_pos_ok = bool(j1 == target_pos and j2 == target_pos)
        positional_ok = positional_ok and this_pos_ok

        bridge_tau = b.bridge_tau_from_first_history(h2, z)
        target_tau = b.target_tau_from_history(h2[j2], z)
        B4[ik] = b.eval_at_tau(h2[j2], bridge_tau)
        atarget = 1.0 / (1.0 + z)
        abridge = b.a_at_tau(h2[j2], bridge_tau)
        tau_offsets.append(float(np.max(np.abs(bridge_tau - target_tau))))
        a_offsets.append(float(np.max(np.abs(abridge - atarget))))

        param_diffs[f"{kh:.5f}"] = b.normalized_param_diff(p1, p2)
        fingerprint_rows.append({
            "k_h": float(kh),
            "bridge_list_h": mode_h.tolist(),
            "target_pos": target_pos,
            "direct_match": diag1,
            "bridge_match": diag2,
            "matched_index_direct": int(j1),
            "matched_index_bridge": int(j2),
            "positional_identity": this_pos_ok,
            "serialization_chars": int(serial["string_length"]),
        })
        print(
            f"FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_R1_RUN {ik+1:02d}/15 "
            f"k_h={kh:.5f} n={len(mode_h)} pos={target_pos} "
            f"fp_direct={j1}:{diag1['best_relative_L2']:.3e} "
            f"fp_bridge={j2}:{diag2['best_relative_L2']:.3e} pos_ok={this_pos_ok}",
            flush=True,
        )

    e10, m10, p10 = cmp(B1, B0)
    e21, m21, p21 = cmp(B2, B1)
    e32, m32, p32 = cmp(B3, B2)
    e42, m42, p42 = cmp(B4, B2)
    e54, m54, p54 = cmp(B5, B4)
    e50, m50, p50 = cmp(B5, B0)
    unexpected = {k: v for k, v in param_diffs.items() if v}

    g_repair = bool(fingerprint_ok)
    g1 = bool(frozen and g_repair and all(np.all(np.isfinite(x)) for x in (B0, B1, B2, B3, B4, B5)))
    g2 = bool(e10 <= b.GLOBAL_GATE and m10 <= b.PERK_GATE)
    g3 = bool(e21 <= b.GLOBAL_GATE and m21 <= b.PERK_GATE and len(unexpected) == 0)
    g4 = bool(positional_ok and e32 <= b.GLOBAL_GATE and m32 <= b.PERK_GATE)
    g5 = bool(e42 <= b.GLOBAL_GATE and m42 <= b.PERK_GATE)
    g6 = bool(e54 <= b.GLOBAL_GATE and m54 <= b.PERK_GATE)
    material = bool(e50 > b.MATERIAL_GATE or m50 > b.PERK_GATE)

    if not g_repair:
        classification = b.INCOMPLETE
    elif not g1:
        classification = b.INCOMPLETE
    elif not g2:
        classification = b.KLIST
    elif not g3:
        classification = b.PARAM
    elif not g4:
        classification = b.HISTORY
    elif not g5:
        classification = b.TIME
    elif not g6:
        classification = b.BASIS
    elif material:
        classification = b.NO_TECH
    else:
        classification = b.INCOMPLETE

    gates = {
        "BI_REPAIR_single_k_fingerprint_identity": g_repair,
        "BI_G1_provenance_and_frozen_identity": g1,
        "BI_G2_bridge_list_invariance_direct_params": g2,
        "BI_G3_parameter_construction_identity": g3,
        "BI_G4_history_order_identity": g4,
        "BI_G5_bridge_time_coordinate_identity": g5,
        "BI_G6_basis_fourier_extraction_identity": g6,
    }
    summary = {
        "B1_vs_B0_global_relative_L2": e10,
        "B1_vs_B0_per_k_max": m10,
        "B2_vs_B1_global_relative_L2": e21,
        "B2_vs_B1_per_k_max": m21,
        "B3_vs_B2_global_relative_L2": e32,
        "B3_vs_B2_per_k_max": m32,
        "B4_vs_B2_global_relative_L2": e42,
        "B4_vs_B2_per_k_max": m42,
        "B5_vs_B4_global_relative_L2": e54,
        "B5_vs_B4_per_k_max": m54,
        "B5_vs_B0_global_relative_L2": e50,
        "B5_vs_B0_per_k_max": m50,
        "max_bridge_tau_offset_Mpc": float(max(tau_offsets)),
        "max_bridge_a_offset": float(max(a_offsets)),
        "unexpected_parameter_difference_count": int(len(unexpected)),
        "all_positional_indices_match_fingerprint": bool(positional_ok),
    }
    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "repair_lock": REPAIR_LOCK,
        "historical_first_bridge_identity_run_remains_incomplete": True,
        "gates": gates,
        "summary": summary,
        "fingerprint_rows": fingerprint_rows,
        "unexpected_parameter_differences": unexpected,
        "thresholds": {
            "global": b.GLOBAL_GATE,
            "per_k": b.PERK_GATE,
            "fingerprint": FINGERPRINT_GATE,
            "fingerprint_abs_separation": FINGERPRINT_ABS_SEPARATION,
            "fingerprint_ratio": FINGERPRINT_RATIO,
        },
        "interpretation": {
            "historical_R3_reclassified": False,
            "extractor_equivalence_reclassified": False,
            "new_physics_claim_licensed": False,
            "equation_level_followup_licensed": bool(classification == b.NO_TECH),
        },
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(
        args.npz_out,
        anchors=anchors,
        redshifts=z,
        B0_locked_R3=B0,
        B1_direct_bridge_list=B1,
        B2_bridge_params_fingerprint=B2,
        B3_bridge_positional=B3,
        B4_bridge_common_tau=B4,
        B5_locked_bridge_tagged=B5,
    )
    print("FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_R1_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_R1_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_R1_CLASSIFICATION=" + classification, flush=True)
    return 0 if classification in (b.NO_TECH, b.HISTORY, b.TIME, b.BASIS, b.KLIST, b.PARAM) else 1


if __name__ == "__main__":
    raise SystemExit(main())
