#!/usr/bin/env python3
"""NL1C6D2A: constraint-consistent baryon matter-sector audit.

This phase augments the frozen NL1C5B density history with the baryon
velocity-divergence transfer and independently checks the Newtonian-gauge
continuity equation on dense CLASS perturbation histories.  It does not evolve
the nonlinear full-J AeST field and does not perform branch selection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.interpolate import CubicSpline

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from v063 import theory_response_map as v63

H0 = 67.3324639084866
h = H0 / 100.0
K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
K_REQ = K_H * h
CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"
INPUT_SHA = "0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590"

K_GRID_GATE = 1.0e-12
Z_GRID_GATE = 1.0e-12
DENSITY_ID_GATE = 1.0e-10
REQUESTED_K_GATE = 1.0e-12
CONTINUITY_GATE = 2.0e-3
DENSE_NATIVE_GATE = 2.0e-4
Z_AUDIT_MIN = 0.2
Z_AUDIT_MAX = 6.0
EDGE_DROP = 2
MIN_INTERIOR = 20

CLASS_PASS = "NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_PASS"
CLASS_FAIL = "NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_FAIL"


def pick(d, key, alts=()):
    if key in d:
        return key
    for alt in alts:
        if alt in d:
            return alt
    raise RuntimeError(f"missing {key}; available={sorted(d.keys())}")


def rel_l2(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(bb), 1.0e-300))


def git_meta():
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        head, branch = "unknown", "unknown"
    return head, branch


def code_sha256():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def unique_sorted_xy(x, *ys):
    x = np.asarray(x, float)
    arrays = [np.asarray(y, float) for y in ys]
    if any(y.shape != x.shape for y in arrays):
        raise RuntimeError("dense-history arrays have inconsistent shapes")
    order = np.argsort(x)
    xs = x[order]
    arrs = [y[order] for y in arrays]
    finite = np.isfinite(xs)
    for y in arrs:
        finite &= np.isfinite(y)
    xs = xs[finite]
    arrs = [y[finite] for y in arrs]
    if xs.size < 4:
        raise RuntimeError("insufficient finite samples for spline")
    keep = np.ones(xs.size, dtype=bool)
    keep[1:] = np.diff(xs) > 0.0
    xs = xs[keep]
    arrs = [y[keep] for y in arrs]
    if xs.size < 4 or np.any(np.diff(xs) <= 0.0):
        raise RuntimeError("could not construct strictly increasing spline grid")
    return (xs, *arrs)


def scalar_histories(pert):
    for key in ("scalar", "scalars"):
        if key in pert:
            out = pert[key]
            if isinstance(out, (list, tuple)):
                return list(out), key
    raise RuntimeError(f"get_perturbations lacks scalar histories; keys={sorted(pert.keys())}")


def dense_keys(d):
    tau_key = pick(d, "tau [Mpc]", ("tau", "tau[Mpc]"))
    a_key = pick(d, "a", ("scale factor",))
    delta_key = pick(d, "delta_b", ("d_b",))
    theta_key = pick(d, "theta_b", ("t_b",))
    phi_key = pick(d, "phi")
    phi_prime_key = "phi_prime" if "phi_prime" in d else None
    return tau_key, a_key, delta_key, theta_key, phi_key, phi_prime_key


def prepare_dense_mode(d, mode_index):
    tau_key, a_key, delta_key, theta_key, phi_key, phi_prime_key = dense_keys(d)
    tau = np.asarray(d[tau_key], float)
    aa = np.asarray(d[a_key], float)
    delta = np.asarray(d[delta_key], float)
    theta = np.asarray(d[theta_key], float)
    phi = np.asarray(d[phi_key], float)
    if phi_prime_key is not None:
        phi_prime = np.asarray(d[phi_prime_key], float)
        tau, aa, delta, theta, phi, phi_prime = unique_sorted_xy(
            tau, aa, delta, theta, phi, phi_prime
        )
        phi_prime_source = "direct_CLASS_phi_prime"
    else:
        tau, aa, delta, theta, phi = unique_sorted_xy(tau, aa, delta, theta, phi)
        phi_prime = CubicSpline(tau, phi, bc_type="not-a-knot")(tau, 1)
        phi_prime_source = "cubic_spline_derivative_of_phi"

    if np.any(aa <= 0.0):
        raise RuntimeError(f"nonpositive scale factor in dense mode {mode_index}")
    z = 1.0 / aa - 1.0
    return {
        "tau": tau,
        "a": aa,
        "z": z,
        "delta_b": delta,
        "theta_b": theta,
        "phi": phi,
        "phi_prime": phi_prime,
        "phi_prime_source": phi_prime_source,
        "available_keys": sorted(d.keys()),
    }


def continuity_regression(modes):
    rows = []
    worst = 0.0
    all_ok = True
    for i, mode in enumerate(modes):
        tau = mode["tau"]
        z = mode["z"]
        delta = mode["delta_b"]
        theta = mode["theta_b"]
        phi_prime = mode["phi_prime"]

        delta_prime = CubicSpline(tau, delta, bc_type="not-a-knot")(tau, 1)
        idx = np.where((z >= Z_AUDIT_MIN) & (z <= Z_AUDIT_MAX))[0]
        if idx.size > 2 * EDGE_DROP:
            idx = idx[EDGE_DROP:-EDGE_DROP]
        if idx.size < MIN_INTERIOR:
            raise RuntimeError(
                f"mode {i} has only {idx.size} interior continuity samples; need {MIN_INTERIOR}"
            )

        dp = delta_prime[idx]
        th = theta[idx]
        pp = phi_prime[idx]
        residual = dp + th - 3.0 * pp
        scale = max(
            float(np.linalg.norm(dp)),
            float(np.linalg.norm(th)),
            float(np.linalg.norm(3.0 * pp)),
            1.0e-300,
        )
        nr = float(np.linalg.norm(residual) / scale)
        ok = bool(np.isfinite(nr) and nr <= CONTINUITY_GATE)
        worst = max(worst, nr if np.isfinite(nr) else float("inf"))
        all_ok = all_ok and ok
        rows.append({
            "mode_index": i,
            "k_h_Mpc": float(K_H[i]),
            "k_Mpc^-1": float(K_REQ[i]),
            "n_interior_samples": int(idx.size),
            "z_min_used": float(np.min(z[idx])),
            "z_max_used": float(np.max(z[idx])),
            "phi_prime_source": mode["phi_prime_source"],
            "normalized_L2_residual": nr,
            "pass": ok,
        })
    return {
        "gate": CONTINUITY_GATE,
        "max_normalized_L2_residual": worst,
        "pass": bool(all_ok),
        "rows": rows,
    }


def dense_native_regression(modes, kh_native, z_native, db_native, tb_native):
    rows = []
    worst_db = 0.0
    worst_tb = 0.0
    all_ok = True

    for i, target in enumerate(K_H):
        j = int(np.argmin(np.abs(kh_native - target)))
        mode = modes[i]
        z_dense = mode["z"]
        delta_dense = mode["delta_b"]
        theta_dense = mode["theta_b"]

        zs, ds, ts = unique_sorted_xy(z_dense, delta_dense, theta_dense)
        lo = max(Z_AUDIT_MIN, float(zs[0]))
        hi = min(Z_AUDIT_MAX, float(zs[-1]))
        mask = (z_native >= lo) & (z_native <= hi)
        if np.count_nonzero(mask) < 4:
            raise RuntimeError(f"insufficient native overlap for k={target:g} h/Mpc")

        zq = np.asarray(z_native[mask], float)
        d_interp = CubicSpline(zs, ds, bc_type="not-a-knot")(zq)
        t_interp = CubicSpline(zs, ts, bc_type="not-a-knot")(zq)
        d_ref = np.asarray(db_native[j, mask], float)
        t_ref = np.asarray(tb_native[j, mask], float)
        ed = rel_l2(d_interp, d_ref)
        et = rel_l2(t_interp, t_ref)
        ok = bool(ed <= DENSE_NATIVE_GATE and et <= DENSE_NATIVE_GATE)
        worst_db = max(worst_db, ed)
        worst_tb = max(worst_tb, et)
        all_ok = all_ok and ok
        rows.append({
            "mode_index": i,
            "requested_k_h_Mpc": float(target),
            "native_k_index": j,
            "actual_k_h_Mpc": float(kh_native[j]),
            "n_native_overlap": int(np.count_nonzero(mask)),
            "z_min": float(np.min(zq)),
            "z_max": float(np.max(zq)),
            "d_b_relative_L2": ed,
            "t_b_relative_L2": et,
            "pass": ok,
        })

    return {
        "gate": DENSE_NATIVE_GATE,
        "max_d_b_relative_L2": worst_db,
        "max_t_b_relative_L2": worst_tb,
        "pass": bool(all_ok),
        "rows": rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-npz", required=True)
    ap.add_argument("--input-zip-sha256", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--npz-out", required=True)
    args = ap.parse_args()

    head, branch = git_meta()
    declared_input_ok = args.input_zip_sha256 == INPUT_SHA

    frozen = np.load(args.input_npz)
    old_kh = np.asarray(frozen["k_native_h"], float)
    old_z = np.asarray(frozen["z_native"], float)
    old_db = np.asarray(frozen["d_b"], float)
    old_dm = np.asarray(frozen["d_m"], float)

    pars = dict(v63.class_params())
    pars["output"] = "mTk,vTk"
    pars["lensing"] = "no"
    pars["k_output_values"] = ", ".join(f"{k:.17g}" for k in K_REQ)
    pars["P_k_max_h/Mpc"] = 2.0
    pars["z_max_pk"] = 5.0
    pars["k_per_decade_for_pk"] = 80.0
    pars["k_per_decade_for_bao"] = 560.0

    print("NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_START", flush=True)
    print(f"git_head={head} branch={branch}", flush=True)
    print(f"code_sha256={code_sha256()}", flush=True)
    print(f"declared_CLASS_commit={CLASS_SHA}", flush=True)

    from classy import Class

    c = Class()
    c.set(pars)
    c.compute()
    try:
        tk, k, z = c.get_transfer_and_k_and_z(output_format="class", h_units=False)
        pert = c.get_perturbations()

        kb = pick(tk, "d_b", ("delta_b",))
        ktb = pick(tk, "t_b", ("theta_b",))
        km = pick(tk, "d_m", ("delta_m",))
        db = np.asarray(tk[kb], float).copy()
        tb = np.asarray(tk[ktb], float).copy()
        dm = np.asarray(tk[km], float).copy()
        kk = np.asarray(k, float).copy()
        zz = np.asarray(z, float).copy()
        transfer_keys = sorted(tk.keys())

        histories_raw, scalar_key = scalar_histories(pert)
        if len(histories_raw) != len(K_H):
            raise RuntimeError(
                f"expected {len(K_H)} dense scalar histories from k_output_values, got {len(histories_raw)}"
            )
        modes = [prepare_dense_mode(d, i) for i, d in enumerate(histories_raw)]
    finally:
        c.struct_cleanup()
        c.empty()

    if db.shape != old_db.shape or dm.shape != old_dm.shape:
        raise RuntimeError(
            f"fresh/frozen transfer shape mismatch db={db.shape}/{old_db.shape} dm={dm.shape}/{old_dm.shape}"
        )
    if tb.shape != db.shape or kk.size != db.shape[0] or zz.size != db.shape[1]:
        raise RuntimeError(f"unexpected fresh transfer dimensions db={db.shape} tb={tb.shape} k={kk.size} z={zz.size}")

    kh = kk / h
    krel = float(np.max(np.abs(kh - old_kh) / np.maximum(np.abs(old_kh), 1.0e-300)))
    zabs = float(np.max(np.abs(zz - old_z)))
    dbrel = rel_l2(db, old_db)
    dmrel = rel_l2(dm, old_dm)
    finite_db = bool(np.all(np.isfinite(db)))
    finite_tb = bool(np.all(np.isfinite(tb)))
    finite_dm = bool(np.all(np.isfinite(dm)))

    requested = []
    reqmax = 0.0
    for target in K_H:
        j = int(np.argmin(np.abs(kh - target)))
        miss = abs(kh[j] - target) / target
        reqmax = max(reqmax, float(miss))
        requested.append({
            "requested_k_h_Mpc": float(target),
            "native_index": j,
            "actual_k_h_Mpc": float(kh[j]),
            "relative_miss": float(miss),
        })

    identity_gates = {
        "declared_input_sha_matches_frozen": bool(declared_input_ok),
        "d_b_finite": finite_db,
        "t_b_finite": finite_tb,
        "d_m_finite": finite_dm,
        "k_grid_match_le_1e-12": bool(krel <= K_GRID_GATE),
        "z_grid_match_le_1e-12": bool(zabs <= Z_GRID_GATE),
        "fresh_d_b_identity_relL2_le_1e-10": bool(dbrel <= DENSITY_ID_GATE),
        "fresh_d_m_identity_relL2_le_1e-10": bool(dmrel <= DENSITY_ID_GATE),
        "requested_k_match_le_1e-12": bool(reqmax <= REQUESTED_K_GATE),
    }
    identity_pass = bool(all(identity_gates.values()))
    print(
        f"A_NATIVE_IDENTITY krel={krel:.12e} zabs={zabs:.12e} "
        f"dbrel={dbrel:.12e} dmrel={dmrel:.12e} t_b_finite={finite_tb} pass={identity_pass}",
        flush=True,
    )

    continuity = continuity_regression(modes)
    print(
        f"B_CONTINUITY max_rel={continuity['max_normalized_L2_residual']:.12e} "
        f"pass={continuity['pass']}",
        flush=True,
    )

    dense_native = dense_native_regression(modes, kh, zz, db, tb)
    print(
        f"C_DENSE_NATIVE d_b_max={dense_native['max_d_b_relative_L2']:.12e} "
        f"t_b_max={dense_native['max_t_b_relative_L2']:.12e} pass={dense_native['pass']}",
        flush=True,
    )

    passed = bool(identity_pass and continuity["pass"] and dense_native["pass"])
    classification = CLASS_PASS if passed else CLASS_FAIL

    dense_key_summary = []
    for i, mode in enumerate(modes):
        dense_key_summary.append({
            "mode_index": i,
            "k_h_Mpc": float(K_H[i]),
            "keys": mode["available_keys"],
            "phi_prime_source": mode["phi_prime_source"],
            "n_samples": int(mode["tau"].size),
            "z_min": float(np.min(mode["z"])),
            "z_max": float(np.max(mode["z"])),
        })

    payload = {
        "label": "NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT",
        "classification": classification,
        "git_head": head,
        "git_branch": branch,
        "code_sha256": code_sha256(),
        "declared_CLASS_commit": CLASS_SHA,
        "declared_frozen_input_sha256": args.input_zip_sha256,
        "expected_frozen_input_sha256": INPUT_SHA,
        "nonlinear_full_j_evolved": False,
        "physical_branch_selection_evaluated": False,
        "causal_memory_eta_evaluated": False,
        "matter_sector_established": bool(passed),
        "gauge": pars.get("gauge"),
        "transfer_keys": transfer_keys,
        "dense_scalar_container_key": scalar_key,
        "dense_history_summary": dense_key_summary,
        "native_identity": {
            "k_relative_mismatch": krel,
            "z_absolute_mismatch": zabs,
            "fresh_d_b_vs_frozen_relative_L2": dbrel,
            "fresh_d_m_vs_frozen_relative_L2": dmrel,
            "requested_k_relative_miss_max": reqmax,
            "requested_k": requested,
            "gates": identity_gates,
            "pass": identity_pass,
        },
        "continuity_regression": continuity,
        "dense_native_identity": dense_native,
        "frozen_gates": {
            "k_grid_relative": K_GRID_GATE,
            "z_grid_absolute": Z_GRID_GATE,
            "density_identity_relative_L2": DENSITY_ID_GATE,
            "requested_k_relative": REQUESTED_K_GATE,
            "continuity_normalized_L2": CONTINUITY_GATE,
            "dense_native_relative_L2": DENSE_NATIVE_GATE,
            "continuity_z_range": [Z_AUDIT_MIN, Z_AUDIT_MAX],
            "continuity_edge_drop": EDGE_DROP,
            "continuity_min_interior_samples": MIN_INTERIOR,
        },
        "interpretation": (
            "PASS establishes that the frozen NL1C5B baryon-density history has a finite, "
            "same-model CLASS baryon velocity-divergence history t_b and that the pair obeys "
            "the Newtonian-gauge baryon continuity equation within the preregistered extraction "
            "tolerance. It is not a nonlinear AeST branch-selection result."
        ),
    }

    jout = Path(args.json_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    save = {
        "k_native_h": kh,
        "z_native": zz,
        "d_b": db,
        "t_b": tb,
        "d_m": dm,
    }
    if "phi" in tk:
        save["phi"] = np.asarray(tk["phi"], float)
    if "psi" in tk:
        save["psi"] = np.asarray(tk["psi"], float)
    npzout = Path(args.npz_out)
    npzout.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(npzout, **save)

    print(f"CLASSIFICATION={classification}", flush=True)
    print(f"MATTER_SECTOR_ESTABLISHED={passed}", flush=True)
    print(f"JSON={jout}", flush=True)
    print(f"NPZ={npzout}", flush=True)
    print("NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_END", flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
