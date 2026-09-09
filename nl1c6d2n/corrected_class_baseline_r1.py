#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nl1c6d2n import corrected_class_baseline as base
from nl1c6d2n import exp_normalization_audit as norm
from nl1c6d2a import baryon_matter_sector_audit as d2a

CLASS_PASS = "NL1C6D2N_CORRECTED_CLASS_BASELINE_R1_PASS"
CLASS_FAIL = "NL1C6D2N_CORRECTED_CLASS_BASELINE_R1_FAIL"
BACKGROUND_RHO_GATE = 1.0e-10

CORRECTED_ANCHORS = (
    "k=K2*Z0*Z0*(ex-1.);",
    "kq=2.*K2*Z0*Z*ex;",
    "kqq=2.*K2*ex*(1.+2.*zz);",
    "double x=kq/(2.*K2*Z0);",
)
OLD_ANCHORS = (
    "k=2.*K2*Z0*Z0*(ex-1.);",
    "kq=4.*K2*Z0*Z*ex;",
    "kqq=4.*K2*ex*(1.+2.*zz);",
    "double x=kq/(4.*K2*Z0);",
)


def provenance_audit(class_root: Path, head: str, branch: str):
    class_head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=class_root, text=True
    ).strip()
    class_source = class_root / "source" / "aest_memory.c"
    class_text = class_source.read_text()
    class_sha = base.sha256(class_source)
    repo_source = ROOT / "v019" / "patch" / "source" / "aest_memory.c"
    repo_sha = base.sha256(repo_source)

    corrected = {s: (s in class_text) for s in CORRECTED_ANCHORS}
    old_absent = {s: (s not in class_text) for s in OLD_ANCHORS}
    gates = {
        "pinned_CLASS_head": class_head == base.CLASS_SHA,
        "repository_corrected_source_sha": repo_sha == base.CORRECTED_SOURCE_SHA,
        "all_corrected_anchors_in_final_source": all(corrected.values()),
        "all_old_anchors_absent_from_final_source": all(old_absent.values()),
    }
    return {
        "repository_head": head,
        "repository_branch": branch,
        "CLASS_head": class_head,
        "expected_CLASS_head": base.CLASS_SHA,
        "CLASS_final_source_sha256": class_sha,
        "repository_source_sha256": repo_sha,
        "expected_repository_source_sha256": base.CORRECTED_SOURCE_SHA,
        "corrected_anchor_presence": corrected,
        "old_anchor_absence": old_absent,
        "gates": gates,
        "pass": bool(all(gates.values())),
        "note": "Final patched CLASS source is checked by formula anchors because later frozen patches modify the whole-file SHA after v019.",
    }


def background_audit_r1(bg):
    z_key = base.find_key(bg, ("z",), exact=("z",))
    h_key = base.find_key(bg, ("h [1/mpc]", "hubble"), exact=("H [1/Mpc]",))
    rho_key = base.find_key(bg, ("rho_cdm", "rho aest", "rho_aest"))
    required = {"z": z_key, "H": h_key, "rho": rho_key}
    missing = [k for k, v in required.items() if v is None]
    if missing:
        return {
            "pass": False,
            "reason": "public CLASS background lacks required standard fields",
            "missing_fields": missing,
            "available_keys": sorted(bg.keys()),
            "field_keys": required,
        }, None

    z_all = np.asarray(bg[z_key], float)
    H_all = np.asarray(bg[h_key], float)
    rho_all = np.asarray(bg[rho_key], float)
    a_all = 1.0 / (1.0 + z_all)
    mask = (z_all >= base.Z_MIN) & (z_all <= base.Z_MAX)
    if np.count_nonzero(mask) < 8:
        return {"pass": False, "reason": "insufficient z=0..6 background samples"}, None

    i0 = int(np.argmin(np.abs(z_all)))
    z0_sample = float(z_all[i0])
    rho0 = float(rho_all[i0])
    if abs(z0_sample) > 1.0e-10 or not (np.isfinite(rho0) and rho0 > 0.0):
        return {
            "pass": False,
            "reason": "no valid a=1 effective-dark density sample",
            "z_nearest_zero": z0_sample,
            "rho_nearest_zero": rho0,
        }, None

    target_rho8 = 3.0 * rho0
    zcal, qcal, kcal, I0, kqqcal = norm.calibrate(target_rho8)

    aa = a_all[mask]
    zz = z_all[mask]
    HH = H_all[mask]
    rho_class = rho_all[mask]

    Q = np.empty_like(aa)
    K = np.empty_like(aa)
    KQ = np.empty_like(aa)
    KQQ = np.empty_like(aa)
    rho_pred = np.empty_like(aa)
    p_pred = np.empty_like(aa)
    w_pred = np.empty_like(aa)
    cad2_pred = np.empty_like(aa)
    Zcoord = np.empty_like(aa)

    for i, aval in enumerate(aa):
        kq_req = I0 / (aval ** 3)
        x = kq_req / (2.0 * norm.K2 * norm.Z0)
        zc = norm.exp_inverse_positive(float(x))
        q, k, kq, kqq = norm.exp_eval(float(zc))
        rho8 = q * kq - k
        Q[i], K[i], KQ[i], KQQ[i] = q, k, kq, kqq
        Zcoord[i] = zc
        rho_pred[i] = rho8 / 3.0
        p_pred[i] = k / 3.0
        w_pred[i] = k / rho8
        cad2_pred[i] = kq / (q * kqq)

    finite = bool(all(np.all(np.isfinite(x)) for x in (
        zz, aa, HH, rho_class, Q, KQ, KQQ, rho_pred, p_pred, w_pred, cad2_pred
    )))
    charge = KQ * aa**3
    charge_spread = base.rel_spread(charge)
    rho_rel_l2 = float(np.linalg.norm(rho_pred-rho_class) / max(np.linalg.norm(rho_class), 1e-300))
    rho_pointwise = float(np.max(np.abs(rho_pred-rho_class) / np.maximum(np.abs(rho_class), 1e-300)))
    positivity = {
        "Q_positive": bool(np.all(Q > 0.0)),
        "rho_CLASS_positive": bool(np.all(rho_class > 0.0)),
        "rho_reconstructed_positive": bool(np.all(rho_pred > 0.0)),
        "KQQ_positive": bool(np.all(KQQ > 0.0)),
        "cad2_nonnegative": bool(np.all(cad2_pred >= 0.0)),
        "H_finite": bool(np.all(np.isfinite(HH))),
    }
    passed = bool(
        finite
        and charge_spread <= base.CHARGE_GATE
        and rho_rel_l2 <= BACKGROUND_RHO_GATE
        and rho_pointwise <= BACKGROUND_RHO_GATE
        and all(positivity.values())
    )
    out = {
        "pass": passed,
        "method": "public rho_cdm(a) versus independently reconstructed corrected Exp shift-charge background",
        "field_keys": required,
        "available_keys": sorted(bg.keys()),
        "n_samples_z0_6": int(np.count_nonzero(mask)),
        "z_nearest_zero": z0_sample,
        "target_rho8_from_CLASS_a1": target_rho8,
        "calibrated_Z_a1": float(zcal),
        "I0": float(I0),
        "charge_relative_spread": charge_spread,
        "charge_gate": base.CHARGE_GATE,
        "rho_relative_L2": rho_rel_l2,
        "rho_max_pointwise_relative": rho_pointwise,
        "rho_gate": BACKGROUND_RHO_GATE,
        "positivity": positivity,
        "z_min": float(np.min(zz)),
        "z_max": float(np.max(zz)),
        "Q_min": float(np.min(Q)),
        "Q_max": float(np.max(Q)),
        "w_min": float(np.min(w_pred)),
        "w_max": float(np.max(w_pred)),
        "cad2_min": float(np.min(cad2_pred)),
        "cad2_max": float(np.max(cad2_pred)),
    }
    vals = {
        "z": zz, "a": aa, "H": HH, "rho_CLASS": rho_class,
        "rho_reconstructed": rho_pred, "Q": Q, "K": K, "KQ": KQ,
        "KQQ": KQQ, "p": p_pred, "w": w_pred, "cad2": cad2_pred,
        "Zcoord": Zcoord,
    }
    return out, vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--npz-out", required=True)
    args = ap.parse_args()

    head, branch = base.git_meta()
    class_root = Path(os.environ.get("NL1C6D2N_CLASS_ROOT", ""))
    if not class_root.exists():
        raise RuntimeError("NL1C6D2N_CLASS_ROOT is not set to isolated corrected CLASS")

    provenance = provenance_audit(class_root, head, branch)

    print("NL1C6D2N_CORRECTED_CLASS_BASELINE_R1_START", flush=True)
    print(f"repo_head={head} branch={branch}", flush=True)
    print(f"CLASS_head={provenance['CLASS_head']} final_source_sha={provenance['CLASS_final_source_sha256']}", flush=True)

    from classy import Class
    pars = base.build_params()
    c = Class()
    c.set(pars)
    c.compute()
    try:
        bg = c.get_background()
        tk, kk, zz = c.get_transfer_and_k_and_z(output_format="class", h_units=False)
        pert = c.get_perturbations()
        cl = c.raw_cl(2500)

        histories_raw, scalar_key = d2a.scalar_histories(pert)
        if len(histories_raw) != len(base.K_H):
            raise RuntimeError(f"expected 6 dense histories, got {len(histories_raw)}")
        dense_pairs = [base.dense_mode_full(d, i) for i, d in enumerate(histories_raw)]
        modes = [p[0] for p in dense_pairs]
        extras = [p[1] for p in dense_pairs]

        db_key = d2a.pick(tk, "d_b", ("delta_b",))
        tb_key = d2a.pick(tk, "t_b", ("theta_b",))
        dm_key = d2a.pick(tk, "d_m", ("delta_m",))
        db = np.asarray(tk[db_key], float).copy()
        tb = np.asarray(tk[tb_key], float).copy()
        dm = np.asarray(tk[dm_key], float).copy()
        k = np.asarray(kk, float).copy()
        z = np.asarray(zz, float).copy()
        kh = k / base.h

        bg_result, bg_vals = background_audit_r1(bg)
        continuity = d2a.continuity_regression(modes)
        closure = d2a.dense_native_regression(modes, kh, z, db, tb)
        traj = base.trajectory_health(histories_raw, modes)
        spectra = base.spectra_health(cl)
    finally:
        c.struct_cleanup()
        c.empty()

    continuity_ok = bool(continuity["max_normalized_L2_residual"] <= base.CONTINUITY_GATE)
    closure_ok = bool(
        closure["max_d_b_relative_L2"] <= base.DENSE_NATIVE_GATE
        and closure["max_t_b_relative_L2"] <= base.DENSE_NATIVE_GATE
    )
    finite_native = bool(
        np.all(np.isfinite(db)) and np.all(np.isfinite(tb)) and np.all(np.isfinite(dm))
        and np.all(np.isfinite(k)) and np.all(np.isfinite(z))
    )

    gates = {
        "B1_clean_build_provenance_R1": bool(provenance["pass"]),
        "B2_background_charge_health_R1": bool(bg_result.get("pass", False)),
        "B3_baryon_continuity": continuity_ok,
        "B4_finite_linear_trajectory": bool(traj["pass"] and finite_native),
        "B5_native_dense_closure": closure_ok,
        "B6_spectra_health": bool(spectra["pass"]),
    }
    passed = bool(all(gates.values()))
    classification = CLASS_PASS if passed else CLASS_FAIL

    print(f"B1_PROVENANCE_R1 pass={gates['B1_clean_build_provenance_R1']}", flush=True)
    print(
        f"B2_BACKGROUND_R1 charge={bg_result.get('charge_relative_spread', float('nan')):.12e} "
        f"rhoL2={bg_result.get('rho_relative_L2', float('nan')):.12e} "
        f"rhoMax={bg_result.get('rho_max_pointwise_relative', float('nan')):.12e} "
        f"pass={gates['B2_background_charge_health_R1']}", flush=True
    )
    print(f"B3_CONTINUITY max={continuity['max_normalized_L2_residual']:.12e} pass={gates['B3_baryon_continuity']}", flush=True)
    print(f"B4_TRAJECTORY pass={gates['B4_finite_linear_trajectory']}", flush=True)
    print(
        f"B5_CLOSURE db={closure['max_d_b_relative_L2']:.12e} "
        f"tb={closure['max_t_b_relative_L2']:.12e} pass={gates['B5_native_dense_closure']}", flush=True
    )
    print(f"B6_SPECTRA pass={gates['B6_spectra_health']}", flush=True)

    payload = {
        "classification": classification,
        "git": {"head": head, "branch": branch},
        "provenance": provenance,
        "parameters": pars,
        "background": bg_result,
        "continuity": continuity,
        "trajectory_health": traj,
        "native_dense_closure": closure,
        "spectra_health": spectra,
        "transfer_keys": sorted(tk.keys()),
        "dense_scalar_container_key": scalar_key,
        "dense_available_keys": [sorted(d.keys()) for d in histories_raw],
        "gates": gates,
        "technical_remediation_of_first_baseline": True,
        "first_baseline_classification_unchanged": "NL1C6D2N_CORRECTED_CLASS_BASELINE_FAIL",
        "historical_v053_results_unchanged": True,
        "cosmological_refit_performed": False,
        "memory_or_likelihood_evaluated": False,
        "nonlinear_branch_selection_performed": False,
        "NL1C7_authorized": False,
    }

    jout = Path(args.json_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")

    save = {
        "k_native_h": kh, "z_native": z, "d_b": db, "t_b": tb, "d_m": dm,
        "ell": np.asarray(cl["ell"], int),
        "cl_tt": np.asarray(cl["tt"], float),
        "cl_te": np.asarray(cl["te"], float),
        "cl_ee": np.asarray(cl["ee"], float),
    }
    for key in ("phi", "psi"):
        if key in tk:
            save[key] = np.asarray(tk[key], float)
    if bg_vals is not None:
        for key, val in bg_vals.items():
            save[f"bg_{key}"] = np.asarray(val)
    for i, (bmode, extra) in enumerate(zip(modes, extras)):
        for key in ("tau", "a", "z", "delta_b", "theta_b", "phi"):
            save[f"mode{i}_{key}"] = np.asarray(bmode[key], float)
        for key, val in extra.items():
            if np.asarray(val).shape == np.asarray(bmode["tau"]).shape:
                save[f"mode{i}_{key}"] = np.asarray(val, float)

    npzout = Path(args.npz_out)
    npzout.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(npzout, **save)

    print(f"CLASSIFICATION={classification}", flush=True)
    print(f"JSON={jout}", flush=True)
    print(f"NPZ={npzout}", flush=True)
    print("NL1C6D2N_CORRECTED_CLASS_BASELINE_R1_END", flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
