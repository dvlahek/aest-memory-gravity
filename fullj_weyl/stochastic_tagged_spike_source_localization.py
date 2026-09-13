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
from fullj_weyl import stochastic_tagged_power_quarter_lattice as quarter

pl = quarter.pl
poc = pl.poc
r2 = pl.r2
m = pl.m
static = pl.static
d2b = pl.d2b

KMASK_RESULT_LOCK = "20151ab785e923de20d720f3fdd8890576b6cc05"
REG_FAIL_RESULT_LOCK = "9f5218629901643574373e32c84d137c9cda2494"
NPZ_AUDIT_LOCK = "97d72584aa5ed26028e8e60e1e6ef0ccd1919a21"
QUARTER_PREDATA_LOCK = "3d309b51e44eb38569a7be263dbb14963ba4bd17"
QUARTER_FAIL_RESULT_LOCK = "c1dd14b2d15fcd48519c328eb4906ef5d1b265b4"
HISTORY_LOCK = "ce8ef79da695fae7b37793f325678096eb5dc2ac"
PREDATA_LOCK = "a7b63fdaeb501fb01e9ef31e66ba7829b01c5472"

SATURATED_SUPPORTED = "FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_SATURATED_MODE_SUPPORTED"
NONLINEAR_REQUIRED = "FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_NONLINEAR_RESIDUAL_REQUIRED"
NUMERICAL_FAIL = "FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_NUMERICAL_CONTROL_FAIL"
INCOMPLETE = "FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_INCOMPLETE"

PARENT_JSON = ROOT / "results/fullj_stochastic_tagged_power_quarter_lattice.json"
PARENT_NPZ = ROOT / "results/fullj_stochastic_tagged_power_quarter_lattice.npz"
PARENT_NPZ_SHA256 = "468521f4f4c41807659cf4a8a9924149f012aef8f46ad97e91c876a7ffc3886a"
COEFF_HASH = "9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200"

BG = 0
EPS_BASE = 0.05
EPS_HALF = 0.025
NSTEP_BASE = 4096
NSTEP_FINE = 8192
CHECK_Z = np.asarray(pl.CHECK_Z, float)
REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}

WINDOWS = {
    "W1": np.asarray([0.09875, 0.10125, 0.10375], float),
    "W2": np.asarray([0.16125, 0.16375, 0.16625], float),
    "W3": np.asarray([0.19375, 0.19625, 0.19875], float),
}
WINDOW_ORDER = ("W1", "W2", "W3")
K_LOCAL = np.concatenate([WINDOWS[w] for w in WINDOW_ORDER])
CENTERS = np.asarray([WINDOWS[w][1] for w in WINDOW_ORDER], float)

KF_BASE = 0.00125
NX_BASE = 1024
BOX_BASE = 2.0 * np.pi / (KF_BASE * float(static.h))
KF_BOX = 0.000625
NX_BOX = 2048
BOX_BOX = 2.0 * np.pi / (KF_BOX * float(static.h))

COMPONENTS = (
    "W_total", "W_CLASS", "W_corr", "delta_A", "Theta_A",
    "alpha", "chi", "P_chi", "S", "E",
)

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
SAT_GATE = 2.0e-2
BASE_GLOBAL_GATE = 1.0e-8
BASE_PERK_GATE = 3.0e-8
WEYL_ID_GATE = 1.0e-12
TIME_T_GLOBAL_GATE = 5.0e-3
TIME_P_GLOBAL_GATE = 1.0e-2
TIME_T_PERK_GATE = 1.0e-2
EPS_T_GLOBAL_GATE = 1.0e-2
EPS_P_GLOBAL_GATE = 2.0e-2
EPS_T_PERK_GATE = 2.0e-2
BOX_T_GLOBAL_GATE = 1.0e-4
BOX_P_GLOBAL_GATE = 2.0e-4
BOX_T_PERK_GATE = 3.0e-4
SURR_T_GLOBAL_GATE = 5.0e-2
SURR_P_GLOBAL_GATE = 1.0e-1
SURR_Z02_CORR_GATE = 0.95
SURR_CENTER_P_GATE = 0.25


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
    aa = np.asarray(a, complex)
    bb = np.asarray(b, complex)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def rel_real(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def safe_corr(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    if aa.size < 2 or float(np.std(aa)) <= 1e-300 or float(np.std(bb)) <= 1e-300:
        return float("nan")
    return float(np.corrcoef(aa, bb)[0, 1])


def load_parent():
    if not PARENT_JSON.exists() or not PARENT_NPZ.exists():
        raise FileNotFoundError("missing quarter-lattice parent JSON/NPZ")
    digest = sha256_file(PARENT_NPZ)
    if digest != PARENT_NPZ_SHA256:
        raise RuntimeError(f"quarter parent NPZ SHA256 mismatch: {digest}")
    meta = json.loads(PARENT_JSON.read_text())
    if meta.get("classification") != "FULLJ_STOCHASTIC_TAGGED_POWER_QUARTER_LATTICE_FAIL":
        raise RuntimeError("quarter parent JSON does not preserve formal FAIL")
    gates = meta.get("gates", {})
    for name in (
        "QL_G1_provenance_and_frozen_identity",
        "QL_G2_solver_constraint_health",
        "QL_G3_broadband_saturated_closure",
        "QL_G4_quarter_stochastic_algebra_sanity",
    ):
        if gates.get(name) is not True:
            raise RuntimeError(f"quarter parent true gate not preserved: {name}")
    for name in (
        "QL_G5_absolute_quarter_power_interpolation_accuracy",
        "QL_G6_no_new_unresolved_quarter_power_spike",
        "QL_G7_refinement_improves_over_005",
    ):
        if gates.get(name) is not False:
            raise RuntimeError(f"quarter parent failed gate not preserved: {name}")

    q = np.load(PARENT_NPZ)
    required = {"redshifts", "quarter_nodes", "response_quarter_B2"}
    if not required.issubset(set(q.files)):
        raise RuntimeError(f"quarter parent NPZ missing keys {sorted(required-set(q.files))}")
    z = np.asarray(q["redshifts"], float)
    kn = np.asarray(q["quarter_nodes"], float)
    ar = np.asarray(q["response_quarter_B2"], complex)
    if not np.allclose(z, CHECK_Z, rtol=0.0, atol=5e-13):
        raise RuntimeError("quarter parent redshift grid mismatch")
    if ar.shape != (2, len(kn), len(CHECK_Z)) or not np.all(np.isfinite(ar)):
        raise RuntimeError(f"quarter parent response shape mismatch {ar.shape}")
    parent = np.stack([ar[BG, idx(kn, k), :] for k in K_LOCAL], axis=0)
    return meta, digest, parent


def saturated_rhs(data, tau, y, ops, C, nonlinear):
    """Exact saturated surrogate: replace only div[(1+j_eff)grad chi] by 2 lap chi."""
    E, b = d2b.r1.derive_E_stable(data, tau, y, ops)
    a, H, Q, KQ, KQQ, Z, Qdot = b
    alpha, chi, pchi, S = y
    grad, lap, _, div = ops

    U = pchi / (2.0 * a**3 * KQQ)
    psi = m.to_field(m.mode_values(data, tau, "psi"), C)
    nl = 2.0 * lap(chi) if nonlinear else lap(chi)

    dalpha = a * (E - psi)
    dchi = a * (U + Q * E + Qdot * alpha)
    dpchi = a * (
        -2.0 * m.A * a * lap(E)
        + 2.0 * m.A * a * nl
        - 2.0 * a * KQ * lap(alpha)
    )
    dS = a * (
        -2.0 * a * KQ * lap(chi)
        - 2.0 * m.A * a * Q * lap(E)
        + 2.0 * m.A * a * Q * nl
    )
    return np.stack([dalpha, dchi, dpchi, dS])


def field_from_checkpoint(cp, name):
    if name == "W_total":
        return np.asarray(cp["metric"]["weyl"], float)
    if name == "W_CLASS":
        return np.asarray(cp["metric"]["class_weyl"], float)
    if name == "W_corr":
        return np.asarray(cp["metric"]["metric_correction"]["weyl"], float)
    if name == "delta_A":
        return np.asarray(cp["delta"], float)
    if name == "Theta_A":
        return np.asarray(cp["theta"], float)
    if name == "alpha":
        return np.asarray(cp["y"][0], float)
    if name == "chi":
        return np.asarray(cp["y"][1], float)
    if name == "P_chi":
        return np.asarray(cp["y"][2], float)
    if name == "S":
        return np.asarray(cp["y"][3], float)
    if name == "E":
        return np.asarray(cp["E"], float)
    raise KeyError(name)


def component_fourier(run, ntag):
    out = {name: [] for name in COMPONENTS}
    for cp in run["checkpoints"]:
        for name in COMPONENTS:
            f = field_from_checkpoint(cp, name)
            fh = np.fft.fft(f) / float(f.size)
            out[name].append(fh[int(ntag)])
    return {name: np.asarray(vals, complex) for name, vals in out.items()}


def run_signed(data, mode_h, gvec, kh, sign, eps, nstep, kf_h, nx, box, variant, surrogate=False):
    ntag = int(round(float(kh) / float(kf_h)))
    if abs(ntag * float(kf_h) - float(kh)) > 5e-13:
        raise RuntimeError(f"target {kh} not exact on kF={kf_h}")
    make, amp_tag, phase_tag = poc.basis_factory(mode_h, gvec, float(kh), float(eps), int(sign), int(nx), float(box))

    old_cos = m.cos_matrix
    old_box = float(static.BOX)
    old_rhs = d2b.rhs_member
    poc._ACTIVE_DATA = data
    d2b.set_member(REFERENCE_MEMBER)
    m.cos_matrix = make
    static.BOX = float(box)
    if surrogate:
        d2b.rhs_member = saturated_rhs
    try:
        run = r2.integrate_combined_r2(data, int(nx), int(nstep), True)
        hh = poc.health(run)
        if not hh["finite"]:
            rec = {
                "finite": False, "variant": variant, "background": int(BG), "k_h": float(kh),
                "epsilon": float(eps), "sign": int(sign), "nstep": int(nstep), "nx": int(nx),
                "kF_h": float(kf_h), "reason": run.get("fail_reason", "incomplete"),
            }
            return rec, None, None
        sat = poc.saturation(run, int(nx), float(box))
        comps = component_fourier(run, ntag)
        rec = {
            "finite": True, "variant": variant, "background": int(BG), "k_h": float(kh),
            "epsilon": float(eps), "sign": int(sign), "nstep": int(nstep), "nx": int(nx),
            "kF_h": float(kf_h), "box_Mpc": float(box), "ntag": int(ntag),
            "canonical_max": float(hh["canonical_max"]), "metric_max": hh["metric_max"],
            "sat_max": float(np.max(sat)), "sat_by_z": np.asarray(sat, float).tolist(),
            "surrogate": bool(surrogate),
        }
        return rec, comps, {"amp_tag": float(amp_tag), "phase_tag": float(phase_tag)}
    finally:
        d2b.rhs_member = old_rhs
        m.cos_matrix = old_cos
        static.BOX = old_box
        poc._ACTIVE_DATA = None


def pair_response(pair, meta, eps):
    phase = np.exp(-1j * float(meta["phase_tag"]))
    amp = float(meta["amp_tag"])
    out = {}
    for name in COMPONENTS:
        out[name] = (pair[+1][name] - pair[-1][name]) * phase / (float(eps) * amp)
    return out


def health_ok(rec):
    return bool(
        rec.get("finite", False)
        and float(rec.get("canonical_max", np.inf)) <= CANONICAL_GATE
        and all(float(v) <= METRIC_GATE for v in rec.get("metric_max", {}).values())
    )


def compare_response(test, base, per_k=False):
    t = np.asarray(test, complex)
    b = np.asarray(base, complex)
    out = {
        "response_global_relative_L2": rel_complex(t, b),
        "power_global_relative_L2": rel_real(np.abs(t)**2, np.abs(b)**2),
    }
    if per_k:
        out["response_per_k"] = [rel_complex(t[i], b[i]) for i in range(t.shape[0])]
        out["response_per_k_max"] = float(max(out["response_per_k"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_stochastic_tagged_spike_source_localization.json")
    ap.add_argument("--npz-out", default="results/fullj_stochastic_tagged_spike_source_localization.npz")
    ap.add_argument("--csv-out", default="results/fullj_stochastic_tagged_spike_source_localization.csv")
    args = ap.parse_args()

    ancestry = {
        "physical_kmask_repair_result_lock": is_ancestor(KMASK_RESULT_LOCK),
        "repaired_regression_fail_result_lock": is_ancestor(REG_FAIL_RESULT_LOCK),
        "npz_audit_lock": is_ancestor(NPZ_AUDIT_LOCK),
        "quarter_predata_lock": is_ancestor(QUARTER_PREDATA_LOCK),
        "quarter_fail_result_lock": is_ancestor(QUARTER_FAIL_RESULT_LOCK),
        "history_lock": is_ancestor(HISTORY_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    _, gcoef, coeff_digest = poc.coeff_draw()
    identity = kmask.original_r2_mask_identity(128)
    exact_base = all(abs(round(float(k)/KF_BASE)*KF_BASE-float(k)) <= 5e-13 for k in K_LOCAL)
    exact_box = all(abs(round(float(k)/KF_BOX)*KF_BOX-float(k)) <= 5e-13 for k in CENTERS)
    frozen = bool(
        coeff_digest == COEFF_HASH
        and BG == 0 and EPS_BASE == 0.05 and EPS_HALF == 0.025
        and NSTEP_BASE == 4096 and NSTEP_FINE == 8192
        and np.allclose(K_LOCAL, [0.09875,0.10125,0.10375,0.16125,0.16375,0.16625,0.19375,0.19625,0.19875], rtol=0.0, atol=5e-14)
        and np.allclose(CENTERS, [0.10125,0.16375,0.19625], rtol=0.0, atol=5e-14)
        and KF_BASE == 0.00125 and NX_BASE == 1024
        and KF_BOX == 0.000625 and NX_BOX == 2048
        and exact_base and exact_box
        and abs(float(kmask.METRIC_KMAX_H)-0.32) < 1e-15
        and identity.get("mismatch_count") == 0
        and REFERENCE_MEMBER == {"sigma":0,"kind":"simple","beta0":1.0}
    )

    print("FULLJ_SPIKE_LOCALIZATION_START", flush=True)
    print("FULLJ_SPIKE_LOCALIZATION_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_SPIKE_LOCALIZATION_COEFFICIENT_SHA256=" + coeff_digest, flush=True)
    print("FULLJ_SPIKE_LOCALIZATION_ORIGINAL_IDENTITY=" + json.dumps(identity, sort_keys=True), flush=True)
    print("FULLJ_SPIKE_LOCALIZATION_LOCAL_NODES=" + json.dumps(K_LOCAL.tolist()), flush=True)
    print("FULLJ_SPIKE_LOCALIZATION_CENTERS=" + json.dumps(CENTERS.tolist()), flush=True)
    print("FULLJ_SPIKE_LOCALIZATION_TOTAL_RUNS=54", flush=True)

    try:
        parent_meta, parent_digest, parent_response = load_parent()
    except Exception as exc:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "frozen_setup": frozen, "reason": str(exc)}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_SPIKE_LOCALIZATION_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "frozen_setup": frozen, "parent_npz_sha256": parent_digest}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_SPIKE_LOCALIZATION_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    responses = {
        "baseline": {name: np.full((len(K_LOCAL), len(CHECK_Z)), np.nan+1j*np.nan, complex) for name in COMPONENTS},
        "saturated": {name: np.full((len(K_LOCAL), len(CHECK_Z)), np.nan+1j*np.nan, complex) for name in COMPONENTS},
        "time8192": {name: np.full((len(CENTERS), len(CHECK_Z)), np.nan+1j*np.nan, complex) for name in COMPONENTS},
        "eps0025": {name: np.full((len(CENTERS), len(CHECK_Z)), np.nan+1j*np.nan, complex) for name in COMPONENTS},
        "box2x": {name: np.full((len(CENTERS), len(CHECK_Z)), np.nan+1j*np.nan, complex) for name in COMPONENTS},
    }
    all_runs = []
    csv_rows = []
    run_index = 0

    old_kmpc = np.asarray(m.K_MPC, float).copy()
    old_kh = np.asarray(getattr(m, "K_H", pl.radial.K0), float).copy()
    try:
        for ik, kh in enumerate(K_LOCAL):
            mode_h = poc.target_modes(float(kh))
            m.K_H = mode_h.copy()
            m.K_MPC = mode_h * float(static.h)
            data = r2.r0.prepare_bridge_data()

            variants = [
                ("baseline", EPS_BASE, NSTEP_BASE, KF_BASE, NX_BASE, BOX_BASE, False, ik),
                ("saturated", EPS_BASE, NSTEP_BASE, KF_BASE, NX_BASE, BOX_BASE, True, ik),
            ]
            if np.any(np.isclose(CENTERS, kh, rtol=0.0, atol=5e-13)):
                ic = idx(CENTERS, kh)
                variants.extend([
                    ("time8192", EPS_BASE, NSTEP_FINE, KF_BASE, NX_BASE, BOX_BASE, False, ic),
                    ("eps0025", EPS_HALF, NSTEP_BASE, KF_BASE, NX_BASE, BOX_BASE, False, ic),
                    ("box2x", EPS_BASE, NSTEP_BASE, KF_BOX, NX_BOX, BOX_BOX, False, ic),
                ])

            for variant, eps, nstep, kf_h, nx, box, surrogate, out_index in variants:
                pair = {}; meta = None
                for sign in (+1, -1):
                    run_index += 1
                    rec, comps, mm = run_signed(
                        data, mode_h, gcoef[BG], float(kh), int(sign), float(eps), int(nstep),
                        float(kf_h), int(nx), float(box), variant, bool(surrogate),
                    )
                    rec["run_index"] = int(run_index)
                    all_runs.append(rec)
                    print(
                        f"FULLJ_SPIKE_LOCALIZATION_RUN {run_index:03d}/54 variant={variant} k_h={kh:.5f} sign={sign:+d} "
                        + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get('finite') else f"finite=False reason={rec.get('reason','unknown')}"),
                        flush=True,
                    )
                    if comps is not None:
                        pair[sign] = comps
                        meta = mm
                if len(pair) == 2:
                    rr = pair_response(pair, meta, eps)
                    for name in COMPONENTS:
                        responses[variant][name][out_index, :] = rr[name]
                        for iz, z in enumerate(CHECK_Z):
                            csv_rows.append({
                                "variant": variant, "component": name, "k_h_Mpc_inv": float(kh), "z": float(z),
                                "T_real": float(np.real(rr[name][iz])), "T_imag": float(np.imag(rr[name][iz])),
                                "P_tag": float(abs(rr[name][iz])**2),
                            })
    finally:
        m.K_MPC = old_kmpc
        m.K_H = old_kh

    all_finite = len(all_runs) == 54 and all(bool(r.get("finite", False)) for r in all_runs)
    health_all = all(health_ok(r) for r in all_runs)
    full_variants = {"baseline", "time8192", "eps0025", "box2x"}
    full_sat_max = max([float(r.get("sat_max", np.inf)) for r in all_runs if r.get("variant") in full_variants] or [np.inf])

    base = responses["baseline"]["W_total"]
    parent_cmp = compare_response(base, parent_response, per_k=True)
    weyl_identity = rel_complex(
        responses["baseline"]["W_total"],
        responses["baseline"]["W_CLASS"] + responses["baseline"]["W_corr"],
    )

    center_idx = [idx(K_LOCAL, k) for k in CENTERS]
    base_centers = base[center_idx, :]
    time_cmp = compare_response(responses["time8192"]["W_total"], base_centers, per_k=True)
    eps_cmp = compare_response(responses["eps0025"]["W_total"], base_centers, per_k=True)
    box_cmp = compare_response(responses["box2x"]["W_total"], base_centers, per_k=True)
    surr = responses["saturated"]["W_total"]
    surr_cmp = compare_response(surr, base, per_k=True)

    iz02 = idx(CHECK_Z, 0.2)
    surr_corr_z02 = safe_corr(np.real(surr[:, iz02]), np.real(base[:, iz02]))
    center_power_rel = []
    for j, ib in enumerate(center_idx):
        pb = float(abs(base[ib, iz02])**2)
        ps = float(abs(surr[ib, iz02])**2)
        center_power_rel.append(abs(ps-pb) / max(pb, ps, 1e-300))

    contrasts = {}
    components_gt2 = {}
    for name in COMPONENTS:
        arr = responses["baseline"][name]
        contrasts[name] = {}
        components_gt2[name] = []
        for iw, w in enumerate(WINDOW_ORDER):
            inds = [idx(K_LOCAL, k) for k in WINDOWS[w]]
            row = {}
            for zval in (0.5, 0.2):
                iz = idx(CHECK_Z, zval)
                p = np.abs(arr[inds, iz])**2
                ratio = float(p[1] / max(float(p[0]), float(p[2]), 1e-300))
                row[str(zval)] = ratio
                if ratio > 2.0:
                    components_gt2[name].append({"window": w, "z": float(zval), "ratio": ratio})
            contrasts[name][w] = row

    g1 = bool(all(ancestry.values()) and frozen and parent_digest == PARENT_NPZ_SHA256)
    g2 = bool(
        all_finite and health_all and full_sat_max <= SAT_GATE
        and parent_cmp["response_global_relative_L2"] <= BASE_GLOBAL_GATE
        and parent_cmp["response_per_k_max"] <= BASE_PERK_GATE
        and weyl_identity <= WEYL_ID_GATE
    )
    g3 = bool(
        time_cmp["response_global_relative_L2"] <= TIME_T_GLOBAL_GATE
        and time_cmp["power_global_relative_L2"] <= TIME_P_GLOBAL_GATE
        and time_cmp["response_per_k_max"] <= TIME_T_PERK_GATE
    )
    g4 = bool(
        eps_cmp["response_global_relative_L2"] <= EPS_T_GLOBAL_GATE
        and eps_cmp["power_global_relative_L2"] <= EPS_P_GLOBAL_GATE
        and eps_cmp["response_per_k_max"] <= EPS_T_PERK_GATE
    )
    g5 = bool(
        box_cmp["response_global_relative_L2"] <= BOX_T_GLOBAL_GATE
        and box_cmp["power_global_relative_L2"] <= BOX_P_GLOBAL_GATE
        and box_cmp["response_per_k_max"] <= BOX_T_PERK_GATE
    )
    g6 = bool(
        surr_cmp["response_global_relative_L2"] <= SURR_T_GLOBAL_GATE
        and surr_cmp["power_global_relative_L2"] <= SURR_P_GLOBAL_GATE
        and np.isfinite(surr_corr_z02) and surr_corr_z02 >= SURR_Z02_CORR_GATE
        and max(center_power_rel) <= SURR_CENTER_P_GATE
    )
    gates = {
        "SL_G1_provenance_and_frozen_identity": g1,
        "SL_G2_baseline_reproduction_and_numerical_health": g2,
        "SL_G3_time_convergence": g3,
        "SL_G4_epsilon_convergence": g4,
        "SL_G5_same_k_box_invariance": g5,
        "SL_G6_saturated_surrogate_mechanism": g6,
    }

    if not g1:
        classification = INCOMPLETE
    elif not all((g2, g3, g4, g5)):
        classification = NUMERICAL_FAIL
    elif g6:
        classification = SATURATED_SUPPORTED
    else:
        classification = NONLINEAR_REQUIRED

    summary = {
        "runs_expected": 54,
        "runs_finite": int(sum(bool(r.get("finite", False)) for r in all_runs)),
        "canonical_max": float(max([float(r.get("canonical_max", np.inf)) for r in all_runs] or [np.inf])),
        "metric_max": {
            key: float(max([float(r.get("metric_max", {}).get(key, np.inf)) for r in all_runs] or [np.inf]))
            for key in ("hamiltonian", "momentum", "shear")
        },
        "full_variant_saturation_max": float(full_sat_max),
        "parent_response_global_relative_L2": float(parent_cmp["response_global_relative_L2"]),
        "parent_response_per_k_max": float(parent_cmp["response_per_k_max"]),
        "weyl_decomposition_relative_residual": float(weyl_identity),
        "time_response_global_relative_L2": float(time_cmp["response_global_relative_L2"]),
        "time_power_global_relative_L2": float(time_cmp["power_global_relative_L2"]),
        "time_response_per_k_max": float(time_cmp["response_per_k_max"]),
        "epsilon_response_global_relative_L2": float(eps_cmp["response_global_relative_L2"]),
        "epsilon_power_global_relative_L2": float(eps_cmp["power_global_relative_L2"]),
        "epsilon_response_per_k_max": float(eps_cmp["response_per_k_max"]),
        "box_response_global_relative_L2": float(box_cmp["response_global_relative_L2"]),
        "box_power_global_relative_L2": float(box_cmp["power_global_relative_L2"]),
        "box_response_per_k_max": float(box_cmp["response_per_k_max"]),
        "saturated_response_global_relative_L2": float(surr_cmp["response_global_relative_L2"]),
        "saturated_power_global_relative_L2": float(surr_cmp["power_global_relative_L2"]),
        "saturated_z02_real_response_correlation": float(surr_corr_z02),
        "saturated_center_z02_power_relative_difference": [float(x) for x in center_power_rel],
    }

    out = {
        "classification": classification,
        "diagnostic_complete": bool(g1 and all_finite),
        "frozen_setup": frozen,
        "ancestry": ancestry,
        "parent_npz_sha256": parent_digest,
        "coefficient_sha256": coeff_digest,
        "metric_kmax_h": float(kmask.METRIC_KMAX_H),
        "original_R2_mask_identity": identity,
        "local_nodes": K_LOCAL.tolist(),
        "centers": CENTERS.tolist(),
        "components": list(COMPONENTS),
        "gates": gates,
        "summary": summary,
        "time_control": time_cmp,
        "epsilon_control": eps_cmp,
        "box_control": box_cmp,
        "saturated_surrogate": {
            **surr_cmp,
            "z02_real_response_correlation": float(surr_corr_z02),
            "center_z02_power_relative_difference": [float(x) for x in center_power_rel],
        },
        "component_center_contrast": contrasts,
        "component_contrast_gt2": components_gt2,
        "thresholds": {
            "canonical": CANONICAL_GATE, "metric": METRIC_GATE, "saturation": SAT_GATE,
            "baseline_global": BASE_GLOBAL_GATE, "baseline_per_k": BASE_PERK_GATE, "weyl_identity": WEYL_ID_GATE,
            "time_T_global": TIME_T_GLOBAL_GATE, "time_P_global": TIME_P_GLOBAL_GATE, "time_T_per_k": TIME_T_PERK_GATE,
            "epsilon_T_global": EPS_T_GLOBAL_GATE, "epsilon_P_global": EPS_P_GLOBAL_GATE, "epsilon_T_per_k": EPS_T_PERK_GATE,
            "box_T_global": BOX_T_GLOBAL_GATE, "box_P_global": BOX_P_GLOBAL_GATE, "box_T_per_k": BOX_T_PERK_GATE,
            "surrogate_T_global": SURR_T_GLOBAL_GATE, "surrogate_P_global": SURR_P_GLOBAL_GATE,
            "surrogate_z02_correlation": SURR_Z02_CORR_GATE, "surrogate_center_power": SURR_CENTER_P_GATE,
        },
        "licenses": {
            "STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_TESTED": classification in (SATURATED_SUPPORTED, NONLINEAR_REQUIRED),
            "STOCHASTIC_TAGGED_SATURATED_MODE_MECHANISM_SUPPORTED": classification == SATURATED_SUPPORTED,
            "STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED": False,
            "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED": False,
            "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED": False,
            "EVOLVING_WEYL_POWER_LICENSED": False,
            "ACT_LIKELIHOOD_LICENSED": False,
            "OBSERVATIONAL_CLAIM_LICENSED": False,
        },
        "runs": all_runs,
    }

    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    with open(args.csv_out, "w", newline="") as f:
        fields = ["variant", "component", "k_h_Mpc_inv", "z", "T_real", "T_imag", "P_tag"]
        wr = csv.DictWriter(f, fieldnames=fields)
        wr.writeheader(); wr.writerows(csv_rows)

    npz_payload = {
        "redshifts": CHECK_Z,
        "local_nodes": K_LOCAL,
        "centers": CENTERS,
        "component_names": np.asarray(COMPONENTS),
        "parent_W_total": parent_response,
    }
    for variant, block in responses.items():
        for name, arr in block.items():
            npz_payload[f"{variant}__{name}"] = arr
    np.savez_compressed(args.npz_out, **npz_payload)

    print("FULLJ_SPIKE_LOCALIZATION_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_SPIKE_LOCALIZATION_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_SPIKE_LOCALIZATION_CLASSIFICATION=" + classification, flush=True)
    print("STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_TESTED=" + str(classification in (SATURATED_SUPPORTED, NONLINEAR_REQUIRED)), flush=True)
    print("STOCHASTIC_TAGGED_SATURATED_MODE_MECHANISM_SUPPORTED=" + str(classification == SATURATED_SUPPORTED), flush=True)

    if classification == INCOMPLETE:
        return 3
    if classification == NUMERICAL_FAIL:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
