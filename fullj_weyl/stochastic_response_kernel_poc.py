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
from fullj_weyl import stochastic_tagged_radial_convergence as radial

r2 = radial.r2
m = radial.m
static = radial.static

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
GAUSS_RESULT_LOCK = "05e38b273f91eb04b7b4c8753731017d0ed839c1"
SAT_RESULT_LOCK = "f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f"
TAGGED_POC_RESULT_LOCK = "aff670fa8551163f5cde2b5146e0e5840d53b424"
K1_FAIL_RESULT_LOCK = "2531a10772f97958ab221bd1f39ceffc23e964a5"
K2_FAIL_RESULT_LOCK = "a293ff5d02824ba170fcf46251df1e480682386c"
HISTORY_LOCK = "6c57e271ec7e38069870cb479dfc7545798a3dac"
PREDATA_LOCK = "d9814ecfa8e9cccf23dbd4d3ec7139b92b490039"

PASS = "FULLJ_STOCHASTIC_RESPONSE_KERNEL_POC_PASS"
FAIL = "FULLJ_STOCHASTIC_RESPONSE_KERNEL_POC_FAIL"
INCOMPLETE = "FULLJ_STOCHASTIC_RESPONSE_KERNEL_POC_INCOMPLETE"

SEED = 20260912
COEFF_HASH = "9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200"
B4 = (0, 1, 2, 3)
B2 = (0, 1)
INPUTS = np.asarray([0.095, 0.110, 0.135, 0.160, 0.185], float)
EPS = 0.05
EPS_HALF = 0.025
CONTROL_K = 0.160
CONTROL_BG = 0
KF_H = 0.005
NX = 256
NX_HI = 512
NSTEP = 4096
BOX = 2.0 * np.pi / (KF_H * float(static.h))
CHECK_Z = np.asarray(m.CHECK_Z, float)
REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}
NOUT = 127
BOUND_N_MIN = 6
BOUND_N_MAX = 40

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
SAT_GATE = 2.0e-2
CONJ_GATE = 1.0e-12
DIAG_MED_GATE = 1.0e-6
DIAG_MAX_GATE = 1.0e-5
CTRL_GLOBAL_GATE = 1.0e-2
CTRL_PERZ_GATE = 2.0e-2

DIAG_OFFDIAG_DECISION = 5.0e-2
DIAG_LEAKAGE_DECISION = 5.0e-2
DIAG_BG_DECISION = 1.0e-1

K2_JSON = ROOT / "results/fullj_stochastic_tagged_radial_k2_refinement.json"
K2_NPZ = ROOT / "results/fullj_stochastic_tagged_radial_k2_refinement.npz"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b):
    aa = np.asarray(a, complex)
    bb = np.asarray(b, complex)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def idx(grid, value):
    q = np.where(np.isclose(np.asarray(grid, float), float(value), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"nonunique index for {value}")
    return int(q[0])


def load_locked_k2():
    if not K2_JSON.exists() or not K2_NPZ.exists():
        raise FileNotFoundError("missing locked K2 local JSON/NPZ")
    meta = json.loads(K2_JSON.read_text())
    if meta.get("classification") != "FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_FAIL":
        raise RuntimeError("local K2 JSON does not preserve historical FAIL")
    g = meta.get("gates", {})
    required_true = [
        "K2_G1_provenance_and_locked_K1_identity",
        "K2_G2_all_80_new_runs_finite_constraint_clean",
        "K2_G3_broadband_saturated_closure",
        "K2_G4_tagged_response_power_algebra",
        "K2_G5_new_node_background_convergence_B2_to_B4",
        "K2_G9_refinement_improves_every_redshift",
    ]
    if not all(g.get(x) is True for x in required_true):
        raise RuntimeError("locked K2 required true gates not preserved")
    for x in (
        "K2_G6_direct_K1_to_K2_holdout_accuracy",
        "K2_G7_continuous_K1_to_K2_radial_convergence",
        "K2_G8_direct_radial_smoothness_spike_veto",
    ):
        if g.get(x) is not False:
            raise RuntimeError("locked K2 FAIL gates not preserved")
    q = np.load(K2_NPZ)
    K2 = np.asarray(q["K2"], float)
    A2 = np.asarray(q["response_K2"], complex)
    if A2.shape != (4, len(K2), len(CHECK_Z)) or not np.all(np.isfinite(A2)):
        raise RuntimeError(f"locked K2 response shape/nonfinite mismatch {A2.shape}")
    for kh in INPUTS:
        idx(K2, kh)
    return meta, K2, A2


def fourier_positive(run):
    vals = []
    conj = []
    for cp in run["checkpoints"]:
        w = np.asarray(cp["metric"]["weyl"], float)
        fh = np.fft.fft(w) / float(w.size)
        nmax = w.size // 2 - 1
        pos = fh[1:nmax + 1]
        neg = fh[-np.arange(1, nmax + 1)]
        vals.append(pos)
        conj.append(float(np.linalg.norm(neg - np.conj(pos)) / max(float(np.linalg.norm(pos)), 1e-300)))
    return np.asarray(vals, complex), np.asarray(conj, float)


def run_signed_spectrum(data, mode_h, gvec, bgid, kh, eps, sign, nx):
    make, amp_tag, phase_tag = poc.basis_factory(mode_h, gvec, float(kh), float(eps), int(sign), int(nx), float(BOX))
    old_cos = m.cos_matrix
    old_box = float(static.BOX)
    poc._ACTIVE_DATA = data
    radial.d2b.set_member(REFERENCE_MEMBER)
    m.cos_matrix = make
    static.BOX = float(BOX)
    try:
        run = r2.integrate_combined_r2(data, int(nx), int(NSTEP), True)
        hh = poc.health(run)
        if not hh["finite"]:
            return {
                "finite": False, "background": int(bgid), "k_h": float(kh), "epsilon": float(eps),
                "sign": int(sign), "nx": int(nx), "reason": run.get("fail_reason", "incomplete")
            }, None, None
        sat = poc.saturation(run, int(nx), float(BOX))
        spec, conj = fourier_positive(run)
        rec = {
            "finite": True, "background": int(bgid), "k_h": float(kh), "epsilon": float(eps),
            "sign": int(sign), "nx": int(nx), "box_Mpc": float(BOX), "kF_h": float(KF_H),
            "ntag": int(round(float(kh) / KF_H)), "canonical_max": float(hh["canonical_max"]),
            "metric_max": hh["metric_max"], "sat_max": float(np.max(sat)), "sat_by_z": sat.tolist(),
            "fourier_conjugacy_max": float(np.max(conj)),
        }
        return rec, spec, {"amp_tag": float(amp_tag), "phase_tag": float(phase_tag)}
    finally:
        m.cos_matrix = old_cos
        static.BOX = old_box
        poc._ACTIVE_DATA = None


def normalized_pair(pair, meta, eps, nout=None):
    q = (pair[+1] - pair[-1]) * np.exp(-1j * float(meta["phase_tag"])) / (float(eps) * float(meta["amp_tag"]))
    if nout is not None:
        q = q[:, :int(nout)]
    return np.asarray(q, complex)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_stochastic_response_kernel_poc.json")
    ap.add_argument("--npz-out", default="results/fullj_stochastic_response_kernel_poc.npz")
    ap.add_argument("--csv-out", default="results/fullj_stochastic_response_kernel_poc.csv")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock": bool(poc.gaussian_lock_ok()),
        "saturated_closure_result_lock": is_ancestor(SAT_RESULT_LOCK),
        "tagged_poc_result_lock": is_ancestor(TAGGED_POC_RESULT_LOCK),
        "k1_fail_result_lock": is_ancestor(K1_FAIL_RESULT_LOCK),
        "k2_fail_result_lock": is_ancestor(K2_FAIL_RESULT_LOCK),
        "history_lock": is_ancestor(HISTORY_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    _, gcoef, digest = poc.coeff_draw()
    frozen = bool(
        digest == COEFF_HASH and B4 == (0,1,2,3) and B2 == (0,1)
        and np.allclose(INPUTS, [0.095,0.110,0.135,0.160,0.185], rtol=0, atol=5e-14)
        and EPS == 0.05 and EPS_HALF == 0.025 and CONTROL_K == 0.160 and CONTROL_BG == 0
        and KF_H == 0.005 and NX == 256 and NX_HI == 512 and NSTEP == 4096 and NOUT == 127
        and abs(BOX - 2.0*np.pi/(KF_H*float(static.h))) < 1e-12
        and REFERENCE_MEMBER == {"sigma":0,"kind":"simple","beta0":1.0}
    )

    print("FULLJ_RESPONSE_KERNEL_START", flush=True)
    print("FULLJ_RESPONSE_KERNEL_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_RESPONSE_KERNEL_COEFFICIENT_SHA256=" + digest, flush=True)
    print("FULLJ_RESPONSE_KERNEL_INPUTS=" + json.dumps(INPUTS.tolist()), flush=True)
    print(f"FULLJ_RESPONSE_KERNEL_GEOMETRY kF_h={KF_H:.6f} NX={NX} NX_HI={NX_HI} box_Mpc={BOX:.12e}", flush=True)

    try:
        k2meta, K2grid, A2locked = load_locked_k2()
    except Exception as exc:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "frozen_setup": frozen, "reason": str(exc)}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_RESPONSE_KERNEL_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "frozen_setup": frozen, "coefficient_sha256": digest}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("FULLJ_RESPONSE_KERNEL_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    old_kmpc = np.asarray(m.K_MPC, float).copy()
    old_kh = np.asarray(getattr(m, "K_H", radial.K0), float).copy()
    primary = np.full((len(B4), len(INPUTS), len(CHECK_Z), NOUT), np.nan + 1j*np.nan, complex)
    all_runs = []
    run_index = 0
    eps_control = None
    res_control = None

    try:
        for ii, kh in enumerate(INPUTS):
            mode_h = poc.target_modes(float(kh))
            m.K_H = mode_h.copy(); m.K_MPC = mode_h * float(static.h)
            data = r2.r0.prepare_bridge_data()
            for ib, bgid in enumerate(B4):
                pair = {}; meta = None
                for sign in (+1, -1):
                    run_index += 1
                    rec, spec, mm = run_signed_spectrum(data, mode_h, gcoef[bgid], bgid, kh, EPS, sign, NX)
                    rec["run_index"] = int(run_index); rec["control"] = "primary"
                    all_runs.append(rec)
                    print(
                        f"FULLJ_RESPONSE_KERNEL_RUN {run_index:02d}/44 primary bg={bgid} k_h={kh:.3f} eps={EPS:.3f} sign={sign:+d} "
                        + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get("finite") else f"finite=False reason={rec.get('reason','unknown')}"),
                        flush=True,
                    )
                    if spec is not None:
                        pair[sign] = spec; meta = mm
                if len(pair) == 2:
                    primary[ib, ii] = normalized_pair(pair, meta, EPS, NOUT)

            if abs(float(kh) - CONTROL_K) < 1e-13:
                # Epsilon-halving control at bg0.
                pair = {}; meta = None
                for sign in (+1, -1):
                    run_index += 1
                    rec, spec, mm = run_signed_spectrum(data, mode_h, gcoef[CONTROL_BG], CONTROL_BG, kh, EPS_HALF, sign, NX)
                    rec["run_index"] = int(run_index); rec["control"] = "epsilon_half"
                    all_runs.append(rec)
                    print(
                        f"FULLJ_RESPONSE_KERNEL_RUN {run_index:02d}/44 epshalf bg={CONTROL_BG} k_h={kh:.3f} eps={EPS_HALF:.3f} sign={sign:+d} "
                        + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get("finite") else f"finite=False reason={rec.get('reason','unknown')}"),
                        flush=True,
                    )
                    if spec is not None:
                        pair[sign] = spec; meta = mm
                if len(pair) == 2:
                    eps_control = normalized_pair(pair, meta, EPS_HALF, NOUT)

                # Spatial-resolution control at same physical box.
                pair = {}; meta = None
                for sign in (+1, -1):
                    run_index += 1
                    rec, spec, mm = run_signed_spectrum(data, mode_h, gcoef[CONTROL_BG], CONTROL_BG, kh, EPS, sign, NX_HI)
                    rec["run_index"] = int(run_index); rec["control"] = "nx512"
                    all_runs.append(rec)
                    print(
                        f"FULLJ_RESPONSE_KERNEL_RUN {run_index:02d}/44 nx512 bg={CONTROL_BG} k_h={kh:.3f} eps={EPS:.3f} sign={sign:+d} "
                        + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get("finite") else f"finite=False reason={rec.get('reason','unknown')}"),
                        flush=True,
                    )
                    if spec is not None:
                        pair[sign] = spec; meta = mm
                if len(pair) == 2:
                    res_control = normalized_pair(pair, meta, EPS, NOUT)
    finally:
        m.K_MPC = old_kmpc; m.K_H = old_kh

    all_finite = len(all_runs) == 44 and all(bool(r.get("finite", False)) for r in all_runs)
    health_ok = bool(all_finite and all(
        float(r["canonical_max"]) <= CANONICAL_GATE and all(float(v) <= METRIC_GATE for v in r["metric_max"].values())
        for r in all_runs
    ))
    satmax = float(max([r.get("sat_max", float("inf")) for r in all_runs], default=float("inf")))
    conjmax = float(max([r.get("fourier_conjugacy_max", float("inf")) for r in all_runs], default=float("inf")))
    kernel_finite = bool(np.all(np.isfinite(primary)) and eps_control is not None and res_control is not None
                         and np.all(np.isfinite(eps_control)) and np.all(np.isfinite(res_control)))

    # Diagonal regression against locked K2 scalar response.
    diag_rows = []; diag_err = []
    if kernel_finite:
        for ib, bgid in enumerate(B4):
            for ii, kh in enumerate(INPUTS):
                n = int(round(float(kh) / KF_H))
                diag = primary[ib, ii, :, n-1]
                ref = A2locked[ib, idx(K2grid, kh), :]
                q = rel(diag, ref)
                diag_err.append(q)
                diag_rows.append({"background": int(bgid), "k_in_h_Mpc_inv": float(kh), "relative_L2": float(q)})
    diag_med = float(np.median(diag_err)) if diag_err else float("inf")
    diag_max = float(np.max(diag_err)) if diag_err else float("inf")

    # Epsilon and resolution controls.
    ic = idx(INPUTS, CONTROL_K)
    base_control = primary[CONTROL_BG, ic] if kernel_finite else None
    eps_global = rel(base_control, eps_control) if base_control is not None else float("inf")
    res_global = rel(base_control, res_control) if base_control is not None else float("inf")
    eps_perz = [rel(base_control[iz], eps_control[iz]) for iz in range(len(CHECK_Z))] if base_control is not None else []
    res_perz = [rel(base_control[iz], res_control[iz]) for iz in range(len(CHECK_Z))] if base_control is not None else []
    eps_max = float(np.max(eps_perz)) if eps_perz else float("inf")
    res_max = float(np.max(res_perz)) if res_perz else float("inf")

    # Kernel coupling metrics.
    metric_rows = []
    max_bounded_offdiag = 0.0
    max_total_offdiag = 0.0
    max_leakage = 0.0
    if kernel_finite:
        for ib, bgid in enumerate(B4):
            for ii, kh in enumerate(INPUTS):
                nin = int(round(float(kh) / KF_H))
                for iz, z in enumerate(CHECK_Z):
                    e = np.abs(primary[ib, ii, iz])**2
                    etot = float(np.sum(e))
                    ediag = float(e[nin-1])
                    ebound = float(np.sum(e[BOUND_N_MIN-1:BOUND_N_MAX]))
                    eboff = max(ebound - ediag, 0.0)
                    eoff = max(etot - ediag, 0.0)
                    eleak = max(etot - ebound, 0.0)
                    fbo = float(eboff / max(ebound, 1e-300))
                    fto = float(eoff / max(etot, 1e-300))
                    flk = float(eleak / max(etot, 1e-300))
                    max_bounded_offdiag = max(max_bounded_offdiag, fbo)
                    max_total_offdiag = max(max_total_offdiag, fto)
                    max_leakage = max(max_leakage, flk)
                    metric_rows.append({
                        "background": int(bgid), "k_in_h_Mpc_inv": float(kh), "z": float(z),
                        "diagonal_power": ediag, "bounded_offdiag_fraction": fbo,
                        "total_offdiag_fraction": fto, "out_of_band_leakage_fraction": flk,
                    })

    # Full bounded-kernel background convergence B2->B4.
    bsl = slice(BOUND_N_MIN-1, BOUND_N_MAX)
    mean2 = np.mean(primary[:2, :, :, bsl], axis=0) if kernel_finite else None
    mean4 = np.mean(primary[:, :, :, bsl], axis=0) if kernel_finite else None
    bg_rows = []; bg_diff = []
    if kernel_finite:
        for ii, kh in enumerate(INPUTS):
            q = rel(mean2[ii], mean4[ii])
            bg_diff.append(q)
            bg_rows.append({"k_in_h_Mpc_inv": float(kh), "bounded_kernel_B2_to_B4_relative_L2": float(q)})
    bg_global = rel(mean2, mean4) if kernel_finite else float("inf")
    bg_max = float(np.max(bg_diff)) if bg_diff else float("inf")

    # Dominant off-diagonal modes in the B4 mean at each input/redshift.
    dominant = []
    if kernel_finite:
        km = np.mean(primary, axis=0)
        for ii, kh in enumerate(INPUTS):
            nin = int(round(float(kh) / KF_H))
            for iz, z in enumerate(CHECK_Z):
                e = np.abs(km[ii, iz])**2
                e[nin-1] = -1.0
                inds = np.argsort(e)[-3:][::-1]
                dominant.append({
                    "k_in_h_Mpc_inv": float(kh), "z": float(z),
                    "top_offdiag_k_h_Mpc_inv": [float((j+1)*KF_H) for j in inds],
                    "top_offdiag_power": [float(max(e[j],0.0)) for j in inds],
                })

    gates = {
        "RK_G1_provenance_and_frozen_identity": bool(all(ancestry.values()) and frozen),
        "RK_G2_all_44_runs_finite_constraint_clean": bool(health_ok),
        "RK_G3_broadband_saturated_closure": bool(satmax <= SAT_GATE),
        "RK_G4_full_kernel_fourier_sanity": bool(kernel_finite and conjmax <= CONJ_GATE),
        "RK_G5_diagonal_regression_to_locked_K2": bool(diag_med <= DIAG_MED_GATE and diag_max <= DIAG_MAX_GATE),
        "RK_G6_epsilon_tangent_control": bool(eps_global <= CTRL_GLOBAL_GATE and eps_max <= CTRL_PERZ_GATE),
        "RK_G7_resolution_aliasing_control": bool(res_global <= CTRL_GLOBAL_GATE and res_max <= CTRL_PERZ_GATE),
    }
    classification = PASS if all(gates.values()) else FAIL

    diagonal_supported = bool(
        classification == PASS
        and max_bounded_offdiag <= DIAG_OFFDIAG_DECISION
        and max_leakage <= DIAG_LEAKAGE_DECISION
        and bg_max <= DIAG_BG_DECISION
    )
    kernel_required = bool(classification == PASS and not diagonal_supported)

    summary = {
        "coefficient_sha256": digest,
        "runs_expected": 44,
        "runs_finite": int(sum(bool(r.get("finite", False)) for r in all_runs)),
        "broadband_saturation_max": satmax,
        "fourier_conjugacy_max": conjmax,
        "diagonal_regression_median": diag_med,
        "diagonal_regression_max": diag_max,
        "epsilon_control_global": eps_global,
        "epsilon_control_per_z_max": eps_max,
        "resolution_control_global": res_global,
        "resolution_control_per_z_max": res_max,
        "max_bounded_offdiag_energy_fraction": float(max_bounded_offdiag),
        "max_total_offdiag_energy_fraction": float(max_total_offdiag),
        "max_out_of_band_leakage_fraction": float(max_leakage),
        "bounded_kernel_B2_to_B4_global": float(bg_global),
        "bounded_kernel_B2_to_B4_per_input_max": float(bg_max),
    }

    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "ancestry": ancestry,
        "gates": gates,
        "summary": summary,
        "seed": SEED,
        "coefficient_sha256": digest,
        "background_ids_B4": list(B4),
        "background_ids_B2": list(B2),
        "inputs_h_Mpc_inv": INPUTS.tolist(),
        "epsilon": EPS,
        "epsilon_half": EPS_HALF,
        "kF_h": KF_H,
        "NX": NX,
        "NX_high": NX_HI,
        "box_Mpc": BOX,
        "redshifts": CHECK_Z.tolist(),
        "reference_member": REFERENCE_MEMBER,
        "runs": all_runs,
        "diagonal_regression": diag_rows,
        "background_convergence": bg_rows,
        "kernel_metrics": metric_rows,
        "dominant_offdiagonal_modes": dominant,
        "STOCHASTIC_RESPONSE_KERNEL_POC_TESTED": classification == PASS,
        "STOCHASTIC_SCALAR_DIAGONAL_REDUCTION_SUPPORTED": diagonal_supported,
        "STOCHASTIC_MODE_COUPLING_KERNEL_REQUIRED": kernel_required,
        "STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED": False,
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
        inputs=INPUTS,
        k_out_h=KF_H*np.arange(1,NOUT+1,dtype=float),
        kernel_primary=primary,
        epsilon_control=eps_control,
        resolution_control=res_control,
    )
    with open(args.csv_out, "w", newline="") as f:
        fields = ["background","k_in_h_Mpc_inv","z","diagonal_power","bounded_offdiag_fraction","total_offdiag_fraction","out_of_band_leakage_fraction"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(metric_rows)

    print("FULLJ_RESPONSE_KERNEL_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_RESPONSE_KERNEL_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_RESPONSE_KERNEL_CLASSIFICATION=" + classification, flush=True)
    print("STOCHASTIC_RESPONSE_KERNEL_POC_TESTED=" + str(classification == PASS), flush=True)
    print("STOCHASTIC_SCALAR_DIAGONAL_REDUCTION_SUPPORTED=" + str(diagonal_supported), flush=True)
    print("STOCHASTIC_MODE_COUPLING_KERNEL_REQUIRED=" + str(kernel_required), flush=True)
    print("STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED=False", flush=True)
    print("THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
