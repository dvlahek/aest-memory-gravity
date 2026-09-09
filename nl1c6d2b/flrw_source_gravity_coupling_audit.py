#!/usr/bin/env python3
"""NL1C6D2B: FLRW source/gravity coupling formulation audit.

This audit deliberately separates:
  * hard numerical contradictions with already frozen identities/conventions;
  * linear CLASS consistency checks that can be evaluated now; and
  * the still-missing action-derived nonlinear FLRW longitudinal reduction.

It does not perform nonlinear branch selection and it does not introduce a
phenomenological Hubble/friction term.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any

import numpy as np
from scipy.interpolate import CubicSpline

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nl1c6d1 import longitudinal_weakfield_reduction_audit as d1a
from nl1c6d2a import baryon_matter_sector_audit as d2a
from v063 import theory_response_map as v63

H0 = 67.3324639084866
h = H0 / 100.0
K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
K_REQ = K_H * h

CLASS_PASS = "NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT_PASS"
CLASS_FAIL = "NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT_FAIL"
CLASS_INCOMPLETE = "NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT_INCOMPLETE"
PREDATA = "NL1C6D2B_PREDATA_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT"

STATIC_GATE = 1.0e-12
CONTINUITY_GATE = 2.0e-3
CONSTRAINT_GATE = 2.0e-3
DENSE_NATIVE_GATE = 2.0e-4
Z_MIN = 0.2
Z_MAX = 6.0
EDGE_DROP = 2
MIN_INTERIOR = 20


def git_meta():
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        head, branch = "unknown", "unknown"
    return head, branch


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel_l2(residual, *terms):
    rr = np.asarray(residual, float)
    scale = 1.0e-300
    for t in terms:
        scale = max(scale, float(np.linalg.norm(np.asarray(t, float))))
    return float(np.linalg.norm(rr) / scale)


def pick(d: dict[str, Any], key: str, alts=()):
    if key in d:
        return key
    for alt in alts:
        if alt in d:
            return alt
    raise KeyError(f"missing {key}; available={sorted(d.keys())}")


def optional_pick(d: dict[str, Any], names):
    for name in names:
        if name in d:
            return name
    return None


def unique_sorted_xy(x, *ys):
    x = np.asarray(x, float)
    arrays = [np.asarray(y, float) for y in ys]
    order = np.argsort(x)
    xs = x[order]
    arrs = [y[order] for y in arrays]
    finite = np.isfinite(xs)
    for y in arrs:
        finite &= np.isfinite(y)
    xs = xs[finite]
    arrs = [y[finite] for y in arrs]
    keep = np.ones(xs.size, dtype=bool)
    if xs.size > 1:
        keep[1:] = np.diff(xs) > 0.0
    xs = xs[keep]
    arrs = [y[keep] for y in arrs]
    if xs.size < 4 or np.any(np.diff(xs) <= 0.0):
        raise RuntimeError("could not construct strictly increasing interpolation grid")
    return (xs, *arrs)


def mode_arrays(raw):
    tau_key = pick(raw, "tau [Mpc]", ("tau", "tau[Mpc]"))
    a_key = pick(raw, "a", ("scale factor",))
    phi_key = pick(raw, "phi")
    psi_key = pick(raw, "psi")
    db_key = pick(raw, "delta_b", ("d_b",))
    tb_key = pick(raw, "theta_b", ("t_b",))

    fields = {
        "tau": np.asarray(raw[tau_key], float),
        "a": np.asarray(raw[a_key], float),
        "phi": np.asarray(raw[phi_key], float),
        "psi": np.asarray(raw[psi_key], float),
        "delta_b": np.asarray(raw[db_key], float),
        "theta_b": np.asarray(raw[tb_key], float),
    }
    optional = (
        "delta_g", "theta_g", "shear_g",
        "delta_ur", "theta_ur", "shear_ur",
        "delta_cdm", "theta_cdm",
        "delta_ncdm[0]", "theta_ncdm[0]", "shear_ncdm[0]",
    )
    for name in optional:
        if name in raw:
            fields[name] = np.asarray(raw[name], float)

    keys = list(fields)
    arrays = [fields[k] for k in keys]
    tau, *sorted_arrays = unique_sorted_xy(fields["tau"], *arrays[1:])
    out = {"tau": tau}
    for k, arr in zip(keys[1:], sorted_arrays):
        out[k] = arr
    out["z"] = 1.0 / out["a"] - 1.0
    out["available_keys"] = sorted(raw.keys())
    return out


def scalar_histories(pert):
    for key in ("scalar", "scalars"):
        if key in pert and isinstance(pert[key], (list, tuple)):
            return list(pert[key]), key
    raise RuntimeError(f"get_perturbations lacks scalar histories; keys={sorted(pert.keys())}")


def bg_key(bg, candidates):
    for key in candidates:
        if key in bg:
            return key
    raise KeyError(f"none of background keys {candidates} found")


def bg_spline(bg, candidates):
    key = bg_key(bg, candidates)
    zkey = bg_key(bg, ("z",))
    aa = 1.0 / (1.0 + np.asarray(bg[zkey], float))
    vv = np.asarray(bg[key], float)
    aa, vv = unique_sorted_xy(aa, vv)
    return key, CubicSpline(aa, vv, bc_type="not-a-knot")


def run_class():
    pars = dict(v63.class_params())
    pars["output"] = "mTk,vTk"
    pars["lensing"] = "no"
    pars["k_output_values"] = ", ".join(f"{k:.17g}" for k in K_REQ)
    pars["P_k_max_h/Mpc"] = 2.0
    pars["z_max_pk"] = 6.5
    pars["k_per_decade_for_pk"] = 80.0
    pars["k_per_decade_for_bao"] = 560.0

    from classy import Class

    c = Class()
    c.set(pars)
    c.compute()
    try:
        pert = c.get_perturbations()
        bg = c.get_background()
        histories_raw, scalar_key = scalar_histories(pert)
        if len(histories_raw) != len(K_REQ):
            raise RuntimeError(
                f"expected {len(K_REQ)} scalar histories, got {len(histories_raw)}"
            )
        modes = [mode_arrays(m) for m in histories_raw]
        bg_copy = {k: np.asarray(v).copy() for k, v in bg.items()}
    finally:
        c.struct_cleanup()
        c.empty()
    return modes, bg_copy, scalar_key, pars


def b1_status():
    return {
        "status": "INCOMPLETE",
        "pass": False,
        "hard_fail": False,
        "reason": (
            "The repository has a certified nonlinear-spatial 1D weak-field reduction "
            "(D1A) and a frozen linear FLRW AeST CLASS bridge, but no explicit "
            "action-derived nonlinear FLRW longitudinal reduction retaining J(Y) "
            "with all temporal/canonical and matter-momentum terms. Splicing the two "
            "would be an additional theory choice prohibited by the preregistration."
        ),
        "established": [
            "full nonperturbative AeST 3+1/Hamiltonian framework exists in the literature",
            "D1A certifies the 1D nonlinear-spatial weak-field static/full-J reduction",
            "frozen CLASS implements the linear FLRW AeST background and perturbation system",
            "1D longitudinal curl sector is exactly inactive",
        ],
        "missing": [
            "explicit nonlinear-in-spatial-gradient FLRW longitudinal reduced equations from the same action",
            "action-derived FLRW canonical/first-order coefficients for the nonlinear J(Y) sector",
            "action-derived nonlinear matter momentum source in the reduced variables",
        ],
    }


def b2_zero_expansion_support():
    canon = d1a.canonical_regression()
    track = d1a.tracking_regression()
    support_ok = bool(canon["pass"] and track["pass"])
    return {
        "status": "INCOMPLETE",
        "pass": False,
        "hard_fail": not support_ok,
        "gate": STATIC_GATE,
        "supporting_D1A_canonical_max_relative_error": canon["max_relative_error"],
        "supporting_D1A_tracking_max_relative_error": track["max_relative_error"],
        "supporting_checks_pass": support_ok,
        "reason": (
            "D1A zero-expansion identities remain certified, but an FLRW-to-D1A "
            "limit cannot be evaluated as a derived-system regression until B1 exists."
        ),
    }


def b3_fixed_a_support():
    static = d1a.static_reduction_regression()
    support_ok = bool(static["pass"] and static["max_relative_error"] <= STATIC_GATE)
    return {
        "status": "SUPPORTING_PASS" if support_ok else "FAIL",
        "pass": support_ok,
        "hard_fail": not support_ok,
        "gate": STATIC_GATE,
        "max_relative_error": float(static["max_relative_error"]),
        "operator_max_relative_error": float(static["operator_max_relative_error"]),
        "source_coupling_max_relative_error": float(
            static["source_coupling_max_relative_error"]
        ),
        "qualification": (
            "This independently confirms the exact fixed-a physical-gradient/full-J "
            "R3 identity, but it is not promoted to proof of the missing B1 FLRW "
            "dynamical reduction."
        ),
    }


def continuity_support(modes):
    rows = []
    worst = 0.0
    ok_all = True
    for i, mode in enumerate(modes):
        tau = mode["tau"]
        z = mode["z"]
        db = mode["delta_b"]
        tb = mode["theta_b"]
        phi = mode["phi"]
        dbp = CubicSpline(tau, db, bc_type="not-a-knot")(tau, 1)
        phip = CubicSpline(tau, phi, bc_type="not-a-knot")(tau, 1)
        idx = np.where((z >= Z_MIN) & (z <= Z_MAX))[0]
        if idx.size > 2 * EDGE_DROP:
            idx = idx[EDGE_DROP:-EDGE_DROP]
        if idx.size < MIN_INTERIOR:
            raise RuntimeError(f"k={K_H[i]} has insufficient continuity samples")
        r = dbp[idx] + tb[idx] - 3.0 * phip[idx]
        nr = rel_l2(r, dbp[idx], tb[idx], 3.0 * phip[idx])
        passed = bool(np.isfinite(nr) and nr <= CONTINUITY_GATE)
        worst = max(worst, nr if np.isfinite(nr) else float("inf"))
        ok_all = ok_all and passed
        rows.append(
            {
                "k_h_Mpc": float(K_H[i]),
                "n": int(idx.size),
                "normalized_L2_residual": nr,
                "pass": passed,
            }
        )
    return {
        "status": "PASS" if ok_all else "FAIL",
        "pass": bool(ok_all),
        "hard_fail": not ok_all,
        "gate": CONTINUITY_GATE,
        "max_normalized_L2_residual": worst,
        "theta_convention": (
            "CLASS theta_b is the Newtonian-gauge velocity divergence entering "
            "delta_b' + theta_b - 3 phi' = 0; no factor-of-a redefinition is applied."
        ),
        "rows": rows,
    }


def b4_status(modes):
    avail = [set(m["available_keys"]) for m in modes]
    common = sorted(set.intersection(*avail)) if avail else []
    has_effective_fluid = all(
        ("delta_cdm" in m and "theta_cdm" in m) for m in modes
    )
    return {
        "status": "INCOMPLETE",
        "pass": False,
        "hard_fail": False,
        "target_gate": 2.0e-3,
        "dense_native_target": DENSE_NATIVE_GATE,
        "frozen_CLASS_trajectory_available": True,
        "effective_AeST_delta_theta_available": has_effective_fluid,
        "common_dense_keys": common,
        "reason": (
            "B4 requires linearizing the B1-derived nonlinear FLRW system. "
            "The frozen CLASS trajectory can test a proposed reduction, but cannot "
            "replace the missing derivation by testing CLASS against its own equations."
        ),
    }


def constraint_support(modes, bg):
    """Reconstruct CLASS Newtonian-gauge momentum and shear constraints."""
    try:
        _, rho_g = bg_spline(bg, ("(.)rho_g", "rho_g"))
        _, rho_b = bg_spline(bg, ("(.)rho_b", "rho_b"))
        _, rho_ur = bg_spline(bg, ("(.)rho_ur", "rho_ur"))
        _, rho_dark = bg_spline(bg, ("(.)rho_cdm", "rho_cdm"))
        _, H_phys = bg_spline(bg, ("H [1/Mpc]", "H"))
        try:
            _, p_dark = bg_spline(bg, ("(.)p_aest", "p_aest"))
        except KeyError:
            p_dark = None
        try:
            _, rho_n = bg_spline(bg, ("(.)rho_ncdm[0]", "rho_ncdm[0]"))
            _, p_n = bg_spline(bg, ("(.)p_ncdm[0]", "p_ncdm[0]"))
            has_n = True
        except KeyError:
            rho_n = p_n = None
            has_n = False
    except KeyError as exc:
        return {
            "status": "INCOMPLETE",
            "pass": False,
            "hard_fail": False,
            "reason": f"required background column unavailable: {exc}",
        }

    if p_dark is None:
        return {
            "status": "INCOMPLETE",
            "pass": False,
            "hard_fail": False,
            "reason": (
                "AeST effective pressure background column is unavailable from "
                "get_background(); cannot independently reconstruct (rho+p) theta."
            ),
        }

    rows = []
    worst_m = 0.0
    worst_s = 0.0
    all_ok = True
    for i, mode in enumerate(modes):
        required = ("theta_g", "shear_g", "theta_ur", "shear_ur", "theta_cdm")
        missing = [q for q in required if q not in mode]
        if has_n:
            missing += [
                q for q in ("theta_ncdm[0]", "shear_ncdm[0]") if q not in mode
            ]
        if missing:
            return {
                "status": "INCOMPLETE",
                "pass": False,
                "hard_fail": False,
                "reason": f"dense mode lacks fields required for independent stress sum: {missing}",
                "available_keys": mode["available_keys"],
            }

        tau = mode["tau"]
        a = mode["a"]
        z = mode["z"]
        phi = mode["phi"]
        psi = mode["psi"]
        phip = CubicSpline(tau, phi, bc_type="not-a-knot")(tau, 1)
        Hc = a * H_phys(a)

        rp_theta = (
            (4.0 / 3.0) * rho_g(a) * mode["theta_g"]
            + rho_b(a) * mode["theta_b"]
            + (4.0 / 3.0) * rho_ur(a) * mode["theta_ur"]
            + (rho_dark(a) + p_dark(a)) * mode["theta_cdm"]
        )
        rp_shear = (
            (4.0 / 3.0) * rho_g(a) * mode["shear_g"]
            + (4.0 / 3.0) * rho_ur(a) * mode["shear_ur"]
        )
        if has_n:
            rp_theta = rp_theta + (rho_n(a) + p_n(a)) * mode["theta_ncdm[0]"]
            rp_shear = rp_shear + (rho_n(a) + p_n(a)) * mode["shear_ncdm[0]"]

        k2 = K_REQ[i] ** 2
        mom_rhs = -Hc * psi + 1.5 * a * a * rp_theta / k2
        shear_rhs = phi - 4.5 * a * a * rp_shear / k2

        idx = np.where((z >= Z_MIN) & (z <= Z_MAX))[0]
        if idx.size > 2 * EDGE_DROP:
            idx = idx[EDGE_DROP:-EDGE_DROP]
        if idx.size < MIN_INTERIOR:
            raise RuntimeError(f"k={K_H[i]} has insufficient constraint samples")

        rm = phip[idx] - mom_rhs[idx]
        rs = psi[idx] - shear_rhs[idx]
        nm = rel_l2(
            rm,
            phip[idx],
            Hc[idx] * psi[idx],
            1.5 * a[idx] * a[idx] * rp_theta[idx] / k2,
        )
        ns = rel_l2(
            rs,
            psi[idx],
            phi[idx],
            4.5 * a[idx] * a[idx] * rp_shear[idx] / k2,
        )
        passed = bool(
            np.isfinite(nm)
            and np.isfinite(ns)
            and nm <= CONSTRAINT_GATE
            and ns <= CONSTRAINT_GATE
        )
        worst_m = max(worst_m, nm if np.isfinite(nm) else float("inf"))
        worst_s = max(worst_s, ns if np.isfinite(ns) else float("inf"))
        all_ok = all_ok and passed
        rows.append(
            {
                "k_h_Mpc": float(K_H[i]),
                "n": int(idx.size),
                "momentum_normalized_L2": nm,
                "shear_normalized_L2": ns,
                "pass": passed,
            }
        )

    return {
        "status": "PASS" if all_ok else "FAIL",
        "pass": bool(all_ok),
        "hard_fail": not all_ok,
        "gate": CONSTRAINT_GATE,
        "max_momentum_normalized_L2": worst_m,
        "max_shear_normalized_L2": worst_s,
        "equations": {
            "momentum": "phi' = -Hconf psi + (3/2) a^2/k^2 sum[(rho+p) theta]",
            "shear": "psi = phi - (9/2) a^2/k^2 sum[(rho+p) shear]",
        },
        "projection_used": False,
        "rows": rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--d2a-json",
        default="results/nl1c6d2a_baryon_matter_sector_audit.json",
    )
    ap.add_argument(
        "--d2a-npz",
        default="results/nl1c6d2a_baryon_matter_sector.npz",
    )
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2b_flrw_source_gravity_coupling_audit.json",
    )
    args = ap.parse_args()

    head, branch = git_meta()
    out = Path(args.json_out)
    out.parent.mkdir(parents=True, exist_ok=True)

    d2a_path = Path(args.d2a_json)
    d2a_npz_path = Path(args.d2a_npz)
    prior = json.loads(d2a_path.read_text())
    prior_ok = (
        prior.get("classification")
        == "NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_PASS"
    )
    npz = np.load(d2a_npz_path)
    prior_arrays_ok = all(
        key in npz for key in ("d_b", "t_b", "d_m", "phi", "psi")
    )

    print("NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT_START", flush=True)
    print(f"git_head={head} branch={branch}", flush=True)
    print(f"code_sha256={sha256(Path(__file__))}", flush=True)
    print(f"D2A_PASS={prior_ok} D2A_ARRAYS={prior_arrays_ok}", flush=True)

    b1 = b1_status()
    print(f"B1_FLRW_NONLINEAR_DERIVATION status={b1['status']}", flush=True)

    b2 = b2_zero_expansion_support()
    print(
        "B2_ZERO_EXPANSION "
        f"status={b2['status']} support_pass={b2['supporting_checks_pass']}",
        flush=True,
    )

    b3 = b3_fixed_a_support()
    print(
        "B3_FIXED_A_FULLJ "
        f"status={b3['status']} max_rel={b3['max_relative_error']:.12e}",
        flush=True,
    )

    modes = bg = None
    class_error = None
    try:
        modes, bg, scalar_key, pars = run_class()
        b4 = b4_status(modes)
        b5 = continuity_support(modes)
        b6 = constraint_support(modes, bg)
    except Exception as exc:
        class_error = f"{type(exc).__name__}: {exc}"
        b4 = {
            "status": "INCOMPLETE",
            "pass": False,
            "hard_fail": False,
            "reason": f"CLASS support regression could not be evaluated: {class_error}",
        }
        b5 = {
            "status": "INCOMPLETE",
            "pass": False,
            "hard_fail": False,
            "reason": f"CLASS support regression could not be evaluated: {class_error}",
        }
        b6 = {
            "status": "INCOMPLETE",
            "pass": False,
            "hard_fail": False,
            "reason": f"CLASS support regression could not be evaluated: {class_error}",
        }
        scalar_key = None
        pars = None

    print(f"B4_LINEAR_FLRW status={b4['status']}", flush=True)
    if "max_normalized_L2_residual" in b5:
        print(
            "B5_MATTER "
            f"status={b5['status']} max_rel={b5['max_normalized_L2_residual']:.12e}",
            flush=True,
        )
    else:
        print(f"B5_MATTER status={b5['status']}", flush=True)
    if "max_momentum_normalized_L2" in b6:
        print(
            "B6_CONSTRAINTS "
            f"status={b6['status']} mom={b6['max_momentum_normalized_L2']:.12e} "
            f"shear={b6['max_shear_normalized_L2']:.12e}",
            flush=True,
        )
    else:
        print(f"B6_CONSTRAINTS status={b6['status']}", flush=True)

    b7 = {
        "status": "PASS",
        "pass": True,
        "hard_fail": False,
        "nonlinear_full_source_evolved": False,
        "branch_selection_performed": False,
        "finite_eta_used": False,
        "observational_likelihood_used": False,
    }
    print("B7_NO_BRANCH_SELECTION status=PASS", flush=True)

    hard_fail = bool(
        (not prior_ok)
        or (not prior_arrays_ok)
        or any(x.get("hard_fail", False) for x in (b1, b2, b3, b4, b5, b6, b7))
    )
    required_incomplete = any(
        x.get("status") == "INCOMPLETE" for x in (b1, b2, b4, b5, b6)
    )

    if hard_fail:
        classification = CLASS_FAIL
    elif required_incomplete:
        classification = CLASS_INCOMPLETE
    else:
        classification = CLASS_PASS

    payload = {
        "label": "NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT",
        "predata_classification": PREDATA,
        "classification": classification,
        "git_head": head,
        "git_branch": branch,
        "code_sha256": sha256(Path(__file__)),
        "inputs": {
            "D2A_json": str(d2a_path),
            "D2A_json_sha256": sha256(d2a_path),
            "D2A_npz": str(d2a_npz_path),
            "D2A_npz_sha256": sha256(d2a_npz_path),
            "D2A_classification_pass": prior_ok,
            "D2A_required_arrays_present": prior_arrays_ok,
        },
        "B1": b1,
        "B2": b2,
        "B3": b3,
        "B4": b4,
        "B5": b5,
        "B6": b6,
        "B7": b7,
        "class_support_run": {
            "error": class_error,
            "scalar_history_key": scalar_key,
            "k_h_Mpc": [float(x) for x in K_H],
            "parameters": None
            if pars is None
            else {
                "H0": pars.get("H0"),
                "omega_b": pars.get("omega_b"),
                "aest_enabled": pars.get("aest_enabled"),
                "aest_model": pars.get("aest_model"),
                "aest_KB": pars.get("aest_KB"),
                "aest_Q0": pars.get("aest_Q0"),
                "aest_K2": pars.get("aest_K2"),
                "aest_memory_enabled": pars.get("aest_memory_enabled"),
                "gauge": pars.get("gauge"),
            },
        },
        "decision": {
            "hard_contradiction": hard_fail,
            "required_requirement_incomplete": required_incomplete,
            "D2_nonlinear_branch_evolution_permitted": classification == CLASS_PASS,
            "NL1C7_permitted": False,
        },
        "interpretation": (
            "FAIL means a frozen identity or evaluated regression is contradicted. "
            "INCOMPLETE means the covariant theory is not rejected, but the required "
            "nonlinear FLRW longitudinal reduction/mapping has not been established "
            "without an additional theory choice. Neither outcome is a physical "
            "exclusion of full-J AeST."
        ),
    }

    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"CLASSIFICATION={classification}", flush=True)
    print(f"JSON={out}", flush=True)
    print("NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT_END", flush=True)


if __name__ == "__main__":
    main()
