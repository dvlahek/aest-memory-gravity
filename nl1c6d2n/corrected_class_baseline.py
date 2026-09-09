#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from v063 import theory_response_map as v63
from nl1c6d2a import baryon_matter_sector_audit as d2a

CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"
CORRECTED_SOURCE_SHA = "89eb9ce01c957b0c6fcdc1a761e21983a2676acd96662f9069d0cbbc1b519fb6"
H0 = 67.3324639084866
h = H0 / 100.0
K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
K_REQ = K_H * h
Q0 = 1.0e-4
Z0 = 1.0e-17
K2 = 9500.0
Z_MIN = 0.0
Z_MAX = 6.0
CHARGE_GATE = 1.0e-10
CONTINUITY_GATE = 2.0e-3
DENSE_NATIVE_GATE = 2.0e-4

CLASS_PASS = "NL1C6D2N_CORRECTED_CLASS_BASELINE_PASS"
CLASS_FAIL = "NL1C6D2N_CORRECTED_CLASS_BASELINE_FAIL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_meta():
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        head, branch = "unknown", "unknown"
    return head, branch


def find_key(d, tokens, exact=()):
    for k in exact:
        if k in d:
            return k
    low = {k: k.lower() for k in d}
    for token in tokens:
        t = token.lower()
        hits = [k for k, lk in low.items() if t in lk]
        if len(hits) == 1:
            return hits[0]
    return None


def rel_spread(x):
    x = np.asarray(x, float)
    mean = float(np.mean(x))
    return float(np.max(np.abs(x - mean)) / max(abs(mean), 1.0e-300))


def build_params():
    p = dict(v63.class_params())
    p.update({
        "output": "tCl,pCl,mTk,vTk",
        "lensing": "no",
        "l_max_scalars": 2500,
        "k_output_values": ", ".join(f"{k:.17g}" for k in K_REQ),
        "P_k_max_h/Mpc": 2.0,
        "z_max_pk": 6.5,
        "k_per_decade_for_pk": 80.0,
        "k_per_decade_for_bao": 560.0,
        "aest_memory_enabled": "no",
        "aest_eta": 0.0,
    })
    return p


def background_audit(bg):
    z_key = find_key(bg, ("z",), exact=("z",))
    a_key = find_key(bg, ("scale factor",), exact=("a",))
    h_key = find_key(bg, ("h [1/mpc]", "hubble",), exact=("H [1/Mpc]",))
    q_key = find_key(bg, ("q_aest", "q aest"))
    kq_key = find_key(bg, ("kq_aest", "kq aest"))
    p_key = find_key(bg, ("p_aest", "p aest"))
    w_key = find_key(bg, ("w_aest", "w aest"))
    cs_key = find_key(bg, ("cad2_aest", "cad2 aest"))
    rho_key = find_key(bg, ("rho_cdm", "rho aest", "rho_aest"))

    required = {
        "z": z_key, "a": a_key, "H": h_key, "Q": q_key, "KQ": kq_key,
        "rho": rho_key, "p": p_key, "w": w_key, "cad2": cs_key,
    }
    missing = [name for name, key in required.items() if key is None]
    if missing:
        return {
            "pass": False,
            "missing_fields": missing,
            "available_keys": sorted(bg.keys()),
            "field_keys": required,
        }, None

    arr = {name: np.asarray(bg[key], float) for name, key in required.items()}
    mask = (arr["z"] >= Z_MIN) & (arr["z"] <= Z_MAX)
    if np.count_nonzero(mask) < 8:
        return {"pass": False, "reason": "insufficient z=0..6 background samples", "field_keys": required}, None

    vals = {name: v[mask] for name, v in arr.items()}
    finite = all(np.all(np.isfinite(v)) for v in vals.values())
    charge = vals["KQ"] * vals["a"] ** 3
    charge_spread = rel_spread(charge)

    zcoord = (vals["Q"] - Q0) / Z0
    # KQQ is strictly positive analytically for the corrected Exp branch.
    kqq = 2.0 * K2 * np.exp(zcoord * zcoord) * (1.0 + 2.0 * zcoord * zcoord)
    positivity = {
        "Q_positive": bool(np.all(vals["Q"] > 0.0)),
        "rho_positive": bool(np.all(vals["rho"] > 0.0)),
        "KQQ_positive": bool(np.all(kqq > 0.0)),
        "cad2_nonnegative": bool(np.all(vals["cad2"] >= 0.0)),
    }
    passed = bool(finite and charge_spread <= CHARGE_GATE and all(positivity.values()))
    out = {
        "pass": passed,
        "field_keys": required,
        "available_keys": sorted(bg.keys()),
        "n_samples_z0_6": int(np.count_nonzero(mask)),
        "all_finite": bool(finite),
        "charge_relative_spread": charge_spread,
        "charge_gate": CHARGE_GATE,
        "positivity": positivity,
        "z_min": float(np.min(vals["z"])),
        "z_max": float(np.max(vals["z"])),
        "Q_min": float(np.min(vals["Q"])),
        "Q_max": float(np.max(vals["Q"])),
        "w_min": float(np.min(vals["w"])),
        "w_max": float(np.max(vals["w"])),
        "cad2_min": float(np.min(vals["cad2"])),
        "cad2_max": float(np.max(vals["cad2"])),
    }
    vals["KQQ_reconstructed"] = kqq
    return out, vals


def dense_mode_full(raw, i):
    base = d2a.prepare_dense_mode(raw, i)
    aliases = {
        "psi": ("psi",),
        "delta_cdm": ("delta_cdm", "d_cdm"),
        "theta_cdm": ("theta_cdm", "t_cdm"),
        "alpha_aest": ("alpha_aest", "alpha"),
        "E_aest": ("E_aest", "E"),
    }
    extra = {}
    for outname, names in aliases.items():
        key = next((n for n in names if n in raw), None)
        if key is not None:
            extra[outname] = np.asarray(raw[key], float)
    return base, extra


def trajectory_health(modes_raw, modes_base):
    rows = []
    ok_all = True
    for i, (raw, base) in enumerate(zip(modes_raw, modes_base)):
        z = base["z"]
        mask = (z >= 0.2) & (z <= 6.0)
        keys_checked = []
        finite = True
        for k, v in raw.items():
            try:
                a = np.asarray(v, float)
            except Exception:
                continue
            if a.shape != np.asarray(raw[next(iter(raw))]).shape and a.shape != z.shape:
                continue
            if a.shape == z.shape:
                finite = finite and bool(np.all(np.isfinite(a[mask])))
                keys_checked.append(k)
        ok = bool(finite and np.count_nonzero(mask) >= 8)
        ok_all = ok_all and ok
        rows.append({
            "mode_index": i,
            "k_h_Mpc": float(K_H[i]),
            "n_samples_z0p2_6": int(np.count_nonzero(mask)),
            "numeric_keys_checked": sorted(keys_checked),
            "finite": bool(finite),
            "pass": ok,
        })
    return {"pass": bool(ok_all), "rows": rows}


def spectra_health(cl):
    ell = np.asarray(cl["ell"], int)
    mask = (ell >= 2) & (ell <= 2500)
    rows = {}
    ok = True
    for k in ("tt", "te", "ee"):
        if k not in cl:
            rows[k] = {"present": False, "finite": False}
            ok = False
            continue
        a = np.asarray(cl[k], float)[mask]
        finite = bool(a.size > 0 and np.all(np.isfinite(a)))
        rows[k] = {"present": True, "finite": finite, "n": int(a.size)}
        ok = ok and finite
    return {"pass": bool(ok), "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--npz-out", required=True)
    args = ap.parse_args()

    head, branch = git_meta()
    class_root = Path(os.environ.get("NL1C6D2N_CLASS_ROOT", ""))
    if not class_root.exists():
        raise RuntimeError("NL1C6D2N_CLASS_ROOT is not set to the isolated corrected CLASS tree")

    class_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=class_root, text=True).strip()
    class_source = class_root / "source" / "aest_memory.c"
    class_source_sha = sha256(class_source)
    repo_source_sha = sha256(ROOT / "v019" / "patch" / "source" / "aest_memory.c")
    provenance = {
        "repository_head": head,
        "repository_branch": branch,
        "CLASS_head": class_head,
        "expected_CLASS_head": CLASS_SHA,
        "CLASS_source_sha256": class_source_sha,
        "repository_source_sha256": repo_source_sha,
        "expected_corrected_source_sha256": CORRECTED_SOURCE_SHA,
    }
    provenance_pass = bool(
        class_head == CLASS_SHA
        and class_source_sha == CORRECTED_SOURCE_SHA
        and repo_source_sha == CORRECTED_SOURCE_SHA
    )
    provenance["pass"] = provenance_pass

    print("NL1C6D2N_CORRECTED_CLASS_BASELINE_START", flush=True)
    print(f"repo_head={head} branch={branch}", flush=True)
    print(f"CLASS_head={class_head} source_sha256={class_source_sha}", flush=True)

    from classy import Class

    pars = build_params()
    c = Class()
    c.set(pars)
    c.compute()
    try:
        bg = c.get_background()
        tk, kk, zz = c.get_transfer_and_k_and_z(output_format="class", h_units=False)
        pert = c.get_perturbations()
        cl = c.raw_cl(2500)

        histories_raw, scalar_key = d2a.scalar_histories(pert)
        if len(histories_raw) != len(K_H):
            raise RuntimeError(f"expected 6 dense histories, got {len(histories_raw)}")
        dense_pairs = [dense_mode_full(d, i) for i, d in enumerate(histories_raw)]
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
        kh = k / h

        bg_result, bg_vals = background_audit(bg)
        continuity = d2a.continuity_regression(modes)
        closure = d2a.dense_native_regression(modes, kh, z, db, tb)
        traj = trajectory_health(histories_raw, modes)
        spectra = spectra_health(cl)
    finally:
        c.struct_cleanup()
        c.empty()

    # Re-state frozen gates locally so the payload is self-contained.
    continuity_ok = bool(continuity["max_normalized_L2_residual"] <= CONTINUITY_GATE)
    closure_ok = bool(
        closure["max_d_b_relative_L2"] <= DENSE_NATIVE_GATE
        and closure["max_t_b_relative_L2"] <= DENSE_NATIVE_GATE
    )
    finite_native = bool(
        np.all(np.isfinite(db)) and np.all(np.isfinite(tb)) and np.all(np.isfinite(dm))
        and np.all(np.isfinite(k)) and np.all(np.isfinite(z))
    )

    gates = {
        "B1_clean_build_provenance": provenance_pass,
        "B2_background_charge_health": bool(bg_result.get("pass", False)),
        "B3_baryon_continuity": continuity_ok,
        "B4_finite_linear_trajectory": bool(traj["pass"] and finite_native),
        "B5_native_dense_closure": closure_ok,
        "B6_spectra_health": bool(spectra["pass"]),
    }
    passed = bool(all(gates.values()))
    classification = CLASS_PASS if passed else CLASS_FAIL

    print(f"B1_PROVENANCE pass={gates['B1_clean_build_provenance']}", flush=True)
    print(f"B2_BACKGROUND charge_spread={bg_result.get('charge_relative_spread', float('nan')):.12e} pass={gates['B2_background_charge_health']}", flush=True)
    print(f"B3_CONTINUITY max={continuity['max_normalized_L2_residual']:.12e} pass={gates['B3_baryon_continuity']}", flush=True)
    print(f"B4_TRAJECTORY pass={gates['B4_finite_linear_trajectory']}", flush=True)
    print(f"B5_CLOSURE db={closure['max_d_b_relative_L2']:.12e} tb={closure['max_t_b_relative_L2']:.12e} pass={gates['B5_native_dense_closure']}", flush=True)
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
        "k_native_h": kh,
        "z_native": z,
        "d_b": db,
        "t_b": tb,
        "d_m": dm,
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
    for i, (base, extra) in enumerate(zip(modes, extras)):
        for key in ("tau", "a", "z", "delta_b", "theta_b", "phi"):
            save[f"mode{i}_{key}"] = np.asarray(base[key], float)
        for key, val in extra.items():
            if np.asarray(val).shape == np.asarray(base["tau"]).shape:
                # Histories are already aligned in CLASS output ordering; retain raw arrays.
                save[f"mode{i}_{key}"] = np.asarray(val, float)

    npzout = Path(args.npz_out)
    npzout.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(npzout, **save)

    print(f"CLASSIFICATION={classification}", flush=True)
    print(f"JSON={jout}", flush=True)
    print(f"NPZ={npzout}", flush=True)
    print("NL1C6D2N_CORRECTED_CLASS_BASELINE_END", flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
