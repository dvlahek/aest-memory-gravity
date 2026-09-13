#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.interpolate import CubicSpline

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import corrected_class_spectral_fringe_bridge_identity as b
from fullj_weyl import corrected_class_spectral_fringe_k_ulp_forensics as ulp

PREDATA_LOCK = "429c61c366d5f92073d72d4c963df3ea39f7c48f"
PARENT_JSON = ROOT / "results/fullj_corrected_class_spectral_fringe_k_ulp_forensics.json"
PARENT_NPZ = ROOT / "results/fullj_corrected_class_spectral_fringe_k_ulp_forensics.npz"

PAIRS = {
    "0p10125": (0.10125, 4589576883704929730, 4589576883704929731),
    "0p10250": (0.10250, 4589637531396803372, 4589637531396803373),
    "0p16500": (0.16500, 4592669915990485346, 4592669915990485347),
    "0p19750": (0.19750, 4593959187948552946, 4593959187948552947),
}

INCOMPLETE = "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_LOCALIZATION_INCOMPLETE"
GENERIC = "FULLJ_AEST_ULP_GENERIC_EARLY_HISTORY_DISCONTINUITY"
CERT = "FULLJ_AEST_ULP_AUXILIARY_AMPLITUDE_BRANCH_CERTIFIED"
MIXED = "FULLJ_AEST_ULP_AUXILIARY_EARLY_DIVERGENCE_MIXED"
LATE = "FULLJ_AEST_ULP_LATE_EVOLUTION_DIVERGENCE"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, c) -> float:
    aa = np.asarray(a, float); cc = np.asarray(c, float)
    return float(np.linalg.norm(aa-cc) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(cc)), 1e-300))


def sym_point(a: float, c: float) -> float:
    return float(abs(a-c) / max(abs(a), abs(c), 1e-300))


def tokens(text: str):
    return [q.strip() for q in str(text).split(",") if q.strip()]


def join_tokens(ts):
    return ", ".join(str(x) for x in ts)


def raw_target(pars, pos: int, aest: bool):
    p = dict(pars)
    p["aest_enabled"] = "yes" if aest else "no"
    hs = b.run_histories(p)
    if pos >= len(hs):
        raise RuntimeError(f"target position {pos} outside {len(hs)} histories")
    return hs[pos], len(hs)


def field_key(raw, names, required=True):
    for name in names:
        if name in raw:
            return name
    if required:
        raise RuntimeError(f"missing field among {names}; keys={sorted(raw.keys())}")
    return None


def clean_series(raw, key):
    akey = b.base.d2a.pick(raw, "a", ("scale factor",))
    aa = np.asarray(raw[akey], float)
    yy = np.asarray(raw[key], float)
    ax, vy = b.clean_xy(aa, yy)
    good = np.isfinite(ax) & np.isfinite(vy) & (ax > 0)
    ax = ax[good]; vy = vy[good]
    if len(ax) < 4:
        raise RuntimeError(f"too few finite points for {key}")
    return ax, vy


def common_grid(raw_a, raw_b, n=1024):
    akey_a = b.base.d2a.pick(raw_a, "a", ("scale factor",))
    akey_b = b.base.d2a.pick(raw_b, "a", ("scale factor",))
    aa = np.asarray(raw_a[akey_a], float); ab = np.asarray(raw_b[akey_b], float)
    aa = aa[np.isfinite(aa) & (aa > 0)]; ab = ab[np.isfinite(ab) & (ab > 0)]
    lo = max(float(np.min(aa)), float(np.min(ab)))
    hi = min(float(np.max(aa)), float(np.max(ab)))
    if not (0 < lo < hi):
        raise RuntimeError("no common positive scale-factor range")
    return np.exp(np.linspace(np.log(lo), np.log(hi), n))


def interp(raw, names, grid, required=True):
    key = field_key(raw, names, required=required)
    if key is None:
        return None, None
    aa, yy = clean_series(raw, key)
    sp = CubicSpline(aa, yy, bc_type="not-a-knot")
    out = np.asarray(sp(grid), float)
    if not np.all(np.isfinite(out)):
        raise RuntimeError(f"nonfinite interpolation for {key}")
    return out, key


def scale_fit(xa, xb):
    a = np.asarray(xa, float); bb = np.asarray(xb, float)
    den = float(np.dot(a, a))
    if den <= 1e-300:
        return float("nan"), float("inf")
    c = float(np.dot(a, bb) / den)
    resid = float(np.linalg.norm(bb-c*a) / max(float(np.linalg.norm(bb)), 1e-300))
    return c, resid


def common_numeric_rank(raw_a, raw_b, grid, max_rows=12):
    skip = {"a", "scale factor", "tau", "k"}
    rows = []
    for key in sorted(set(raw_a.keys()) & set(raw_b.keys())):
        if key in skip:
            continue
        try:
            ya, _ = interp(raw_a, (key,), grid)
            yb, _ = interp(raw_b, (key,), grid)
        except Exception:
            continue
        q0 = sym_point(float(ya[0]), float(yb[0]))
        rr = rel(ya, yb)
        c, sr = scale_fit(ya, yb)
        rows.append({"field": key, "first_rel": q0, "full_relL2": rr, "scale": c, "scale_residual": sr})
    rows.sort(key=lambda r: r["first_rel"], reverse=True)
    return rows[:max_rows]


def make_params(kh, bits):
    mode_h = np.asarray(b.sd.poc.target_modes(float(kh)), float)
    q = np.where(np.isclose(mode_h, float(kh), rtol=0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"target {kh} not unique")
    pos = int(q[0])
    p00, _ = b.r3_params(mode_h)
    tt = tokens(p00["k_output_values"])
    tt[pos] = format(ulp.bits_float(int(bits)), ".17g")
    p = dict(p00); p["k_output_values"] = join_tokens(tt)
    return p, pos


def parent_has_pair(pq, tag, ba, bb):
    key = f"bits_{tag}"
    if key not in pq.files:
        return False
    vals = set(int(x) for x in np.asarray(pq[key]).tolist())
    return int(ba) in vals and int(bb) in vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_aest_ulp_initial_amplitude_localization.json")
    ap.add_argument("--npz-out", default="results/fullj_aest_ulp_initial_amplitude_localization.npz")
    args = ap.parse_args()

    print("FULLJ_AEST_ULP_INITIAL_AMPLITUDE_START", flush=True)
    if not PARENT_JSON.exists() or not PARENT_NPZ.exists():
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "reason": "missing parent ULP result"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("FULLJ_AEST_ULP_INITIAL_AMPLITUDE_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    pj = json.loads(PARENT_JSON.read_text())
    pq = np.load(PARENT_NPZ)
    g1 = bool(
        is_ancestor(PREDATA_LOCK)
        and pj.get("classification") == "FULLJ_CLASS_FRINGE_AEST_ULP_SENSITIVITY_CERTIFIED"
        and pj.get("diagnostic_complete") is True
        and all(bool(v) for v in pj.get("gates", {}).values())
        and all(parent_has_pair(pq, tag, ba, bb) for tag, (_, ba, bb) in PAIRS.items())
    )

    rows = []
    arrays = {}
    gr_ok = True
    auxiliary_start_count = 0
    multiplicative_count = 0
    delayed_metric_count = 0

    for tag, (kh, ba, bb) in PAIRS.items():
        pA, posA = make_params(kh, ba)
        pB, posB = make_params(kh, bb)
        if posA != posB:
            raise RuntimeError("pair target positions differ")
        pos = posA

        aeA, nha = raw_target(pA, pos, True)
        aeB, nhb = raw_target(pB, pos, True)
        grA, nga = raw_target(pA, pos, False)
        grB, ngb = raw_target(pB, pos, False)

        grid = common_grid(aeA, aeB, 1024)
        ggrid = common_grid(grA, grB, 1024)

        alphaA, alpha_key = interp(aeA, ("alpha_aest", "alpha"), grid)
        alphaB, _ = interp(aeB, (alpha_key,), grid)
        EA, E_key = interp(aeA, ("E_aest", "E"), grid)
        EB, _ = interp(aeB, (E_key,), grid)
        phiA, _ = interp(aeA, ("phi",), grid)
        phiB, _ = interp(aeB, ("phi",), grid)
        psiA, _ = interp(aeA, ("psi",), grid)
        psiB, _ = interp(aeB, ("psi",), grid)
        WA = phiA + psiA; WB = phiB + psiB

        gphiA, _ = interp(grA, ("phi",), ggrid)
        gphiB, _ = interp(grB, ("phi",), ggrid)
        gpsiA, _ = interp(grA, ("psi",), ggrid)
        gpsiB, _ = interp(grB, ("psi",), ggrid)
        gWA = gphiA + gpsiA; gWB = gphiB + gpsiB

        ca, ra = scale_fit(alphaA, alphaB)
        ce, re = scale_fit(EA, EB)
        da = sym_point(float(alphaA[0]), float(alphaB[0]))
        de = sym_point(float(EA[0]), float(EB[0]))
        dw = sym_point(float(WA[0]), float(WB[0]))
        dscale = float(abs(ca-ce) / max(abs(ca), abs(ce), 1e-300))

        gr_phi_first = sym_point(float(gphiA[0]), float(gphiB[0]))
        gr_psi_first = sym_point(float(gpsiA[0]), float(gpsiB[0]))
        gr_W_first = sym_point(float(gWA[0]), float(gWB[0]))
        gr_W_full = rel(gWA, gWB)
        this_gr = bool(max(gr_phi_first, gr_psi_first, gr_W_first) <= 1e-4 and gr_W_full <= 1e-5)
        gr_ok &= this_gr

        aux_start = bool(da >= 1e-2 and de >= 1e-2)
        mult = bool(ra <= 1e-3 and re <= 1e-3 and dscale <= 1e-3 and (abs(ca-1.0) >= 1e-2 or abs(ce-1.0) >= 1e-2))
        delayed = bool(dw < min(da, de)/10.0)
        auxiliary_start_count += int(aux_start)
        multiplicative_count += int(mult)
        delayed_metric_count += int(delayed)

        rank = common_numeric_rank(aeA, aeB, grid)
        row = {
            "tag": tag, "k_h": float(kh), "bits_A": int(ba), "bits_B": int(bb), "target_pos": int(pos),
            "a_start": float(grid[0]), "a_end": float(grid[-1]),
            "alpha_key": alpha_key, "E_key": E_key,
            "alpha_first_rel": da, "E_first_rel": de, "W_first_rel": dw,
            "alpha_scale_B_over_A": ca, "E_scale_B_over_A": ce,
            "alpha_scale_residual": ra, "E_scale_residual": re, "alpha_E_scale_disagreement": dscale,
            "aest_W_full_relL2": rel(WA, WB),
            "gr_phi_first_rel": gr_phi_first, "gr_psi_first_rel": gr_psi_first,
            "gr_W_first_rel": gr_W_first, "gr_W_full_relL2": gr_W_full,
            "GR_continuous": this_gr, "auxiliary_material_at_start": aux_start,
            "common_multiplicative_auxiliary_branch": mult, "metric_delayed_relative_to_auxiliary": delayed,
            "n_histories": {"aest_A": nha, "aest_B": nhb, "gr_A": nga, "gr_B": ngb},
            "top_common_field_discontinuities": rank,
        }
        rows.append(row)

        arrays[f"a_{tag}"] = grid
        arrays[f"alpha_A_{tag}"] = alphaA; arrays[f"alpha_B_{tag}"] = alphaB
        arrays[f"E_A_{tag}"] = EA; arrays[f"E_B_{tag}"] = EB
        arrays[f"W_A_{tag}"] = WA; arrays[f"W_B_{tag}"] = WB
        arrays[f"gr_a_{tag}"] = ggrid
        arrays[f"gr_W_A_{tag}"] = gWA; arrays[f"gr_W_B_{tag}"] = gWB

        print(
            f"FULLJ_AEST_ULP_INITIAL_PAIR k_h={kh:.5f} bits={ba}/{bb} "
            f"alpha_first={da:.6e} E_first={de:.6e} W_first={dw:.6e} "
            f"c_alpha={ca:.9g} c_E={ce:.9g} r_alpha={ra:.3e} r_E={re:.3e} "
            f"grW_first={gr_W_first:.3e} grW_full={gr_W_full:.3e}", flush=True
        )

    g2 = bool(gr_ok)
    g3 = bool(auxiliary_start_count >= 3)
    g4 = bool(multiplicative_count >= 3)
    g5 = bool(delayed_metric_count >= 3)
    gates = {
        "IA_G1_provenance_and_parent_lock": g1,
        "IA_G2_matched_GR_early_continuity": g2,
        "IA_G3_AeST_auxiliary_material_difference_at_history_start": g3,
        "IA_G4_common_multiplicative_auxiliary_branch": g4,
        "IA_G5_metric_response_delayed_relative_to_auxiliary_branch": g5,
    }

    if not g1:
        classification = INCOMPLETE
    elif not g2:
        classification = GENERIC
    elif g3 and g4 and g5:
        classification = CERT
    elif g3:
        classification = MIXED
    else:
        classification = LATE

    summary = {
        "classification": classification,
        "pair_count": len(rows),
        "auxiliary_start_pass_count": int(auxiliary_start_count),
        "multiplicative_branch_pass_count": int(multiplicative_count),
        "delayed_metric_pass_count": int(delayed_metric_count),
        "max_GR_W_first_rel": float(max(r["gr_W_first_rel"] for r in rows)),
        "max_GR_W_full_relL2": float(max(r["gr_W_full_relL2"] for r in rows)),
        "max_alpha_scale_residual": float(max(r["alpha_scale_residual"] for r in rows)),
        "max_E_scale_residual": float(max(r["E_scale_residual"] for r in rows)),
        "max_alpha_E_scale_disagreement": float(max(r["alpha_E_scale_disagreement"] for r in rows)),
    }
    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "predata_lock": PREDATA_LOCK,
        "parent_classification": pj.get("classification"),
        "gates": gates,
        "summary": summary,
        "pairs": rows,
        "interpretation": {
            "historical_R3_reclassified": False,
            "new_physics_claim_licensed": False,
            "physical_instability_claim_licensed": False,
            "source_level_initialization_index_audit_licensed": bool(classification == CERT),
        },
    }
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out, **arrays)
    print("FULLJ_AEST_ULP_INITIAL_AMPLITUDE_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_AEST_ULP_INITIAL_AMPLITUDE_SUMMARY="+json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_AEST_ULP_INITIAL_AMPLITUDE_CLASSIFICATION="+classification, flush=True)
    return 0 if classification == CERT else 1


if __name__ == "__main__":
    raise SystemExit(main())
