#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pickle
import subprocess
from pathlib import Path

import numpy as np
from scipy.integrate import simpson, trapezoid
from scipy.special import spherical_jn

from fullj_weyl import stable_aest_desi_dr1_r9b2k_native_k_density_convergence as k2

ROOT = Path(__file__).resolve().parents[1]
PREFIT_LOCK = "819e40eeea3dec55181fc63233e4002cda005a2e"
R9B2K_POSTDATA_LOCK = "dd3981b2fd838fb24a997af77f913c3d5dd8d07b"
REPAIR02_POSTDATA_LOCK = "d3fd6191d55f4e74aa8666f842dae64bd8aee09b"
R10A_POSTDATA_LOCK = "b7da648f1810ea0c047b6e511e3f87211e830329"
REPAIR02_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair02.json"
REPAIR02_JSON_SHA256 = "eb221160bf64b0905ec0b620fb8441aea2a1e55fc2981f8b3974954917f1cea4"
REPAIR02_CLASS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_CERTIFIED"

TAUS = (10.0, 5.0, 2.5, 1.25)
ETAS = (0.0, 0.025, -0.025, 0.05, -0.05)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
R_MPC_H = np.arange(20.0, 201.0, 10.0)
Z = np.asarray(k2.ZEFF, float)
C_KMS = 299792.458
DEFAULT_NK = 108

BASELINE_E_GATE = 0.01
BASELINE_C_GATE = 0.999
TANGENT_E_GATE = 0.05
TANGENT_C_GATE = 0.995
LINEARITY_E_GATE = 0.10
LINEARITY_C_GATE = 0.99
ETA0_TAU_REL_GATE = 5.0e-3
NORM_GATE = 1.0e-12

CLS_PASS = "STABLE_AEST_KSZ_R11A_PAIRWISE_VELOCITY_RESPONSE_CERTIFIED"
CLS_PROV = "STABLE_AEST_KSZ_R11A_PROVENANCE_FAIL"
CLS_BASE = "STABLE_AEST_KSZ_R11A_BASELINE_FAIL"
CLS_QUAD = "STABLE_AEST_KSZ_R11A_BASELINE_QUADRATURE_FAIL"
CLS_EPS = "STABLE_AEST_KSZ_R11A_EPSILON_FAIL"
CLS_DENS = "STABLE_AEST_KSZ_R11A_NATIVE_DENSITY_FAIL"
CLS_CROSS = "STABLE_AEST_KSZ_R11A_CROSS_QUADRATURE_FAIL"
CLS_LINEAR = "STABLE_AEST_KSZ_R11A_LOCAL_LINEARITY_FAIL"
CLS_RUN = "STABLE_AEST_KSZ_R11A_RUN_FAIL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def metric(a, b) -> dict:
    aa = np.asarray(a, float).ravel(); bb = np.asarray(b, float).ravel()
    na = float(np.linalg.norm(aa)); nb = float(np.linalg.norm(bb))
    den = max(na, nb, 1e-300)
    E = float(np.linalg.norm(aa - bb) / den)
    C = float(np.dot(aa, bb) / max(na * nb, 1e-300))
    return {"E": E, "C": C, "norm_a": na, "norm_b": nb}


def tangent_pass(m: dict) -> bool:
    return bool(
        np.isfinite(m["E"]) and np.isfinite(m["C"])
        and m["E"] <= TANGENT_E_GATE and m["C"] >= TANGENT_C_GATE
        and m["norm_a"] > NORM_GATE and m["norm_b"] > NORM_GATE
    )


def _load_checkpoint(work: Path, tier: str, tau: float, eta: float) -> dict:
    p = work / f"{k2._ckey(tier, tau, eta)}.pkl"
    if not p.is_file():
        raise FileNotFoundError(str(p))
    with p.open("rb") as f:
        case = pickle.load(f)
    if not k2._checkpoint_ok(case, tier, tau, eta):
        raise RuntimeError(f"invalid checkpoint {p}")
    return case


def _pairwise_row(row: dict, operator: str) -> dict:
    st = row["state"]; bg = row["background"]
    kh = np.asarray(st["kh"], float)
    pdd = np.asarray(st["pdd"], float)
    ptt = np.asarray(st["ptt"], float)
    dcb = np.asarray(st["dcb"], float)
    tcb = np.asarray(st["tcb"], float)
    Hconf = float(st["Hconf"])
    z = float(row["z"])

    if not (kh.ndim == pdd.ndim == ptt.ndim == dcb.ndim == tcb.ndim == 1):
        raise RuntimeError("state arrays must be one-dimensional")
    if not (kh.shape == pdd.shape == ptt.shape == dcb.shape == tcb.shape):
        raise RuntimeError("state array shape mismatch")
    if np.any(~np.isfinite(kh)) or np.any(np.diff(kh) <= 0) or np.any(kh <= 0):
        raise RuntimeError("invalid k grid")
    if np.any(~np.isfinite(pdd)) or np.any(~np.isfinite(ptt)) or np.any(pdd <= 0) or np.any(ptt <= 0):
        raise RuntimeError("invalid source power")
    if not np.isfinite(Hconf) or Hconf == 0.0:
        raise RuntimeError("invalid Hconf")

    vcb = -tcb / Hconf
    sign = np.sign(dcb * vcb)
    pdf = sign * np.sqrt(pdd * ptt)
    if np.any(~np.isfinite(pdf)):
        raise RuntimeError("invalid signed P_deltaf")

    logk = np.log(kh)
    xi = np.empty(R_MPC_H.size, float)
    Idf = np.empty(R_MPC_H.size, float)
    for ir, r in enumerate(R_MPC_H):
        x = kh * float(r)
        fxi = kh**3 * pdd * spherical_jn(0, x) / (2.0 * np.pi**2)
        fi = kh**2 * pdf * spherical_jn(1, x) / (2.0 * np.pi**2)
        if operator == "simpson":
            xi[ir] = float(simpson(fxi, x=logk))
            Idf[ir] = float(simpson(fi, x=logk))
        elif operator == "trapezoid":
            xi[ir] = float(trapezoid(fxi, x=logk))
            Idf[ir] = float(trapezoid(fi, x=logk))
        else:
            raise ValueError(operator)

    h = float(bg["h"])
    H_mpc_inv = float(bg["Hubble_Mpc_inv"])
    if not np.isfinite(h) or h <= 0 or not np.isfinite(H_mpc_inv) or H_mpc_inv <= 0:
        raise RuntimeError("invalid background conversion")
    a = 1.0 / (1.0 + z)
    H_kms_mpc = C_KMS * H_mpc_inv
    denom = 1.0 + xi
    if np.any(~np.isfinite(denom)) or np.any(denom <= 0):
        raise RuntimeError("non-positive pair denominator")
    v12 = -2.0 * a * (H_kms_mpc / h) * Idf / denom
    if np.any(~np.isfinite(v12)):
        raise RuntimeError("non-finite pairwise velocity")
    return {
        "z": z, "kh_n": int(kh.size), "kh_min": float(kh[0]), "kh_max": float(kh[-1]),
        "xi": xi, "Idf_Mpc_over_h": Idf, "v12_kms": v12,
        "H_kms_Mpc": H_kms_mpc, "h": h,
    }


def _pairwise_case(case: dict, operator: str) -> dict:
    rows = [_pairwise_row(row, operator) for row in case["rows"]]
    return {
        "tau_H0": float(case["tau_H0"]), "eta": float(case["eta"]), "tier": case["tier"],
        "operator": operator, "rows": rows,
        "v": np.stack([x["v12_kms"] for x in rows], axis=0),
        "xi": np.stack([x["xi"] for x in rows], axis=0),
        "Idf": np.stack([x["Idf_Mpc_over_h"] for x in rows], axis=0),
    }


def _frac_tangent(v0, vp, vm, eps: float) -> np.ndarray:
    v0 = np.asarray(v0, float); vp = np.asarray(vp, float); vm = np.asarray(vm, float)
    if np.any(np.abs(v0) <= 1e-6):
        raise RuntimeError("baseline pairwise velocity too close to zero")
    return (vp - vm) / (2.0 * float(eps) * v0)


def _abs_tangent(vp, vm, eps: float) -> np.ndarray:
    return (np.asarray(vp, float) - np.asarray(vm, float)) / (2.0 * float(eps))


def _max_point_rel(a, b, floor=1e-6) -> float:
    aa = np.asarray(a, float); bb = np.asarray(b, float)
    return float(np.max(np.abs(aa - bb) / np.maximum(np.maximum(np.abs(aa), np.abs(bb)), floor)))


def _write(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", default="results/stable_aest_desi_dr1_r9b2k_work")
    ap.add_argument("--json-out", default="results/stable_aest_ksz_r11a_pairwise_velocity_response.json")
    ap.add_argument("--npz-out", default="results/stable_aest_ksz_r11a_pairwise_velocity_response.npz")
    args = ap.parse_args()

    out = Path(args.json_out); work = Path(args.workdir)
    print("STABLE_AEST_KSZ_R11A_START", flush=True)

    # G1: immutable parent chain and all existing checkpoints.
    prov = {
        "prefit_lock": PREFIT_LOCK,
        "r9b2k_postdata_lock": R9B2K_POSTDATA_LOCK,
        "repair02_postdata_lock": REPAIR02_POSTDATA_LOCK,
        "r10a_postdata_lock": R10A_POSTDATA_LOCK,
        "repair02_json_sha256_expected": REPAIR02_JSON_SHA256,
    }
    try:
        locks = (PREFIT_LOCK, R9B2K_POSTDATA_LOCK, REPAIR02_POSTDATA_LOCK, R10A_POSTDATA_LOCK)
        prov["ancestor_locks"] = {x: ancestor(x) for x in locks}
        rj = json.loads(REPAIR02_JSON.read_text())
        prov["repair02_json_sha256"] = sha256(REPAIR02_JSON)
        prov["repair02_classification"] = rj.get("classification")
        g1 = bool(
            all(prov["ancestor_locks"].values())
            and prov["repair02_json_sha256"] == REPAIR02_JSON_SHA256
            and rj.get("classification") == REPAIR02_CLASS
            and rj.get("diagnostic_complete") is True
            and all(rj.get("gates", {}).values())
        )
    except Exception as exc:
        prov["error"] = repr(exc); g1 = False

    cases = {}
    checkpoint_meta = []
    if g1:
        try:
            specs = [("D1", 10.0, eta) for eta in ETAS]
            specs += [("D2", tau, eta) for tau in TAUS for eta in ETAS]
            for tier, tau, eta in specs:
                case = _load_checkpoint(work, tier, tau, eta)
                cases[(tier, tau, eta)] = case
                nk = [len(x["state"]["kh"]) for x in case["rows"]]
                checkpoint_meta.append({
                    "tier": tier, "tau_H0": tau, "eta": eta,
                    "n_k_min": int(min(nk)), "n_k_max": int(max(nk)),
                })
        except Exception as exc:
            prov["checkpoint_error"] = repr(exc); g1 = False

    if not g1:
        result = {"classification": CLS_PROV, "diagnostic_complete": False, "gates": {"R11A_G1_provenance_checkpoints": False}, "provenance": prov}
        _write(out, result)
        print("STABLE_AEST_KSZ_R11A_CLASSIFICATION=" + CLS_PROV, flush=True)
        return 3

    print(f"STABLE_AEST_KSZ_R11A_CHECKPOINT_PASS count={len(checkpoint_meta)}", flush=True)

    # Build all pairwise curves with both operators.
    pw = {}
    try:
        for key, case in cases.items():
            for op in ("simpson", "trapezoid"):
                pw[key + (op,)] = _pairwise_case(case, op)
    except Exception as exc:
        result = {"classification": CLS_RUN, "diagnostic_complete": False, "gates": {"R11A_G1_provenance_checkpoints": True}, "error": repr(exc), "provenance": prov}
        _write(out, result)
        print(f"STABLE_AEST_KSZ_R11A_RUN_FAIL error={exc!r}", flush=True)
        return 2

    def V(tier, tau, eta, op):
        return pw[(tier, float(tau), float(eta), op)]["v"]

    # G2: baseline physicality, actual native refinement, eta0 tau invariance.
    g2 = True
    physicality = []
    for tau in TAUS:
        for op in ("simpson", "trapezoid"):
            q = pw[("D2", tau, 0.0, op)]
            ok = bool(
                np.all(np.isfinite(q["v"])) and np.all(np.isfinite(q["xi"])) and np.all(np.isfinite(q["Idf"]))
                and np.all(1.0 + q["xi"] > 0.0) and np.all(np.abs(q["v"]) > 1e-6)
            )
            g2 &= ok
            physicality.append({
                "tau_H0": tau, "operator": op, "pass": ok,
                "v_min_kms": float(np.min(q["v"])), "v_max_kms": float(np.max(q["v"])),
                "xi_min": float(np.min(q["xi"])), "xi_max": float(np.max(q["xi"])),
            })
    refine = []
    for iz, z in enumerate(Z):
        n1 = len(cases[("D1", 10.0, 0.0)]["rows"][iz]["state"]["kh"])
        n2 = len(cases[("D2", 10.0, 0.0)]["rows"][iz]["state"]["kh"])
        ok = bool(n2 > n1 > DEFAULT_NK); g2 &= ok
        refine.append({"z": float(z), "n_default": DEFAULT_NK, "n_D1": int(n1), "n_D2": int(n2), "pass": ok})
    eta0_tau_max_rel = 0.0
    vref = V("D2", 10.0, 0.0, "simpson")
    for tau in TAUS[1:]:
        eta0_tau_max_rel = max(eta0_tau_max_rel, _max_point_rel(vref, V("D2", tau, 0.0, "simpson")))
    g2 &= bool(eta0_tau_max_rel <= ETA0_TAU_REL_GATE)

    # G3: baseline quadrature agreement.
    baseline_quad = {}; g3 = True
    for tau in TAUS:
        m = metric(V("D2", tau, 0.0, "simpson"), V("D2", tau, 0.0, "trapezoid"))
        baseline_quad[str(tau)] = m
        g3 &= bool(m["E"] <= BASELINE_E_GATE and m["C"] >= BASELINE_C_GATE)

    # Tangents for all needed cases.
    tang = {}
    abs_tang = {}
    for tier, taus in (("D1", (10.0,)), ("D2", TAUS)):
        for tau in taus:
            for op in ("simpson", "trapezoid"):
                v0 = V(tier, tau, 0.0, op)
                for eps in (EPS_PRIMARY, EPS_CONTROL):
                    vp = V(tier, tau, +eps, op); vm = V(tier, tau, -eps, op)
                    tang[(tier, tau, op, eps)] = _frac_tangent(v0, vp, vm, eps)
                    abs_tang[(tier, tau, op, eps)] = _abs_tangent(vp, vm, eps)

    # G4 epsilon consistency.
    eps_metrics = {}; g4 = True
    for tau in TAUS:
        eps_metrics[str(tau)] = {}
        for op in ("simpson", "trapezoid"):
            m = metric(tang[("D2", tau, op, EPS_PRIMARY)], tang[("D2", tau, op, EPS_CONTROL)])
            eps_metrics[str(tau)][op] = m; g4 &= tangent_pass(m)

    # G5 D1 -> D2 convergence at tau10.
    density_metrics = {}; g5 = True
    for op in ("simpson", "trapezoid"):
        density_metrics[op] = {}
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            m = metric(tang[("D1", 10.0, op, eps)], tang[("D2", 10.0, op, eps)])
            density_metrics[op][str(eps)] = m; g5 &= tangent_pass(m)

    # G6 Simpson <-> trapezoid tangent agreement on D2.
    cross_quad = {}; g6 = True
    for tau in TAUS:
        cross_quad[str(tau)] = {}
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            m = metric(tang[("D2", tau, "simpson", eps)], tang[("D2", tau, "trapezoid", eps)])
            cross_quad[str(tau)][str(eps)] = m; g6 &= tangent_pass(m)

    # G7 direct eta=0.05 physical shift vs local linear prediction.
    linearity = {}; g7 = True
    physical = {}
    for tau in TAUS:
        v0 = V("D2", tau, 0.0, "simpson")
        vp = V("D2", tau, 0.05, "simpson")
        direct_frac = (vp - v0) / v0
        linear_frac = 0.05 * tang[("D2", tau, "simpson", EPS_PRIMARY)]
        m = metric(direct_frac, linear_frac)
        ok = bool(m["E"] <= LINEARITY_E_GATE and m["C"] >= LINEARITY_C_GATE)
        g7 &= ok
        linearity[str(tau)] = {**m, "pass": ok}

        dv = vp - v0
        T = tang[("D2", tau, "simpson", EPS_PRIMARY)]
        flat = int(np.argmax(np.abs(direct_frac)))
        iz, ir = np.unravel_index(flat, direct_frac.shape)
        physical[str(tau)] = {
            "max_abs_T_per_eta": float(np.max(np.abs(T))),
            "rms_T_per_eta": float(np.sqrt(np.mean(T**2))),
            "max_abs_fractional_shift_eta005": float(np.max(np.abs(direct_frac))),
            "rms_fractional_shift_eta005": float(np.sqrt(np.mean(direct_frac**2))),
            "max_abs_velocity_shift_kms_eta005": float(np.max(np.abs(dv))),
            "rms_velocity_shift_kms_eta005": float(np.sqrt(np.mean(dv**2))),
            "largest_fractional_shift": {
                "z": float(Z[iz]), "r_Mpc_h": float(R_MPC_H[ir]),
                "baseline_v12_kms": float(v0[iz, ir]),
                "delta_v12_kms": float(dv[iz, ir]),
                "fractional_shift": float(direct_frac[iz, ir]),
                "T_per_eta": float(T[iz, ir]),
            },
        }

    # Descriptive tau coherence; intentionally not a gate.
    tau_coherence = {}
    tref = tang[("D2", 10.0, "simpson", EPS_PRIMARY)]
    for tau in TAUS:
        m = metric(tref, tang[("D2", tau, "simpson", EPS_PRIMARY)])
        tau_coherence[str(tau)] = {
            "cosine_to_tau10": m["C"],
            "norm_ratio_to_tau10": float(m["norm_b"] / max(m["norm_a"], 1e-300)),
        }

    gates = {
        "R11A_G1_provenance_checkpoints": True,
        "R11A_G2_baseline_physicality_tau_invariance": bool(g2),
        "R11A_G3_baseline_quadrature": bool(g3),
        "R11A_G4_epsilon_consistency": bool(g4),
        "R11A_G5_native_density_convergence": bool(g5),
        "R11A_G6_cross_quadrature_tangent": bool(g6),
        "R11A_G7_local_eta005_linearity": bool(g7),
    }
    if not g2: classification = CLS_BASE
    elif not g3: classification = CLS_QUAD
    elif not g4: classification = CLS_EPS
    elif not g5: classification = CLS_DENS
    elif not g6: classification = CLS_CROSS
    elif not g7: classification = CLS_LINEAR
    else: classification = CLS_PASS

    result = {
        "classification": classification,
        "diagnostic_complete": True,
        "science_evaluated": classification == CLS_PASS,
        "gates": gates,
        "provenance": prov,
        "checkpoints": checkpoint_meta,
        "settings": {
            "tau_H0": list(TAUS), "eta_values": list(ETAS),
            "epsilon_primary": EPS_PRIMARY, "epsilon_control": EPS_CONTROL,
            "r_Mpc_h": R_MPC_H.tolist(), "z": Z.tolist(),
            "primary_operator": "native Simpson in ln k",
            "control_operator": "native trapezoid in ln k",
            "pairwise_field": "unbiased linear cb matter",
            "no_extrapolation": True, "no_smoothing": True,
            "baseline_E_gate": BASELINE_E_GATE, "baseline_C_gate": BASELINE_C_GATE,
            "tangent_E_gate": TANGENT_E_GATE, "tangent_C_gate": TANGENT_C_GATE,
            "linearity_E_gate": LINEARITY_E_GATE, "linearity_C_gate": LINEARITY_C_GATE,
        },
        "baseline": {
            "physicality": physicality, "native_refinement": refine,
            "eta0_tau_max_point_relative": eta0_tau_max_rel,
            "quadrature_metrics": baseline_quad,
        },
        "robustness": {
            "epsilon_metrics": eps_metrics,
            "density_metrics_tau10": density_metrics,
            "cross_quadrature_metrics": cross_quad,
            "eta005_linearity": linearity,
        },
        "physical_response": physical,
        "tau_coherence": tau_coherence,
        "claim_scope": {
            "theory_only_pairwise_velocity_response": classification == CLS_PASS,
            "ksz_detection": False,
            "ksz_likelihood": False,
            "optical_depth_inference": False,
            "galaxy_halo_prediction": False,
            "nonlinear_small_scale_claim": False,
            "eta_bound": False,
            "tau_bound": False,
        },
    }
    _write(out, result)

    arrays = {"z": Z, "r_Mpc_h": R_MPC_H}
    for tau in TAUS:
        tag = str(tau).replace(".", "p")
        v0 = V("D2", tau, 0.0, "simpson")
        vp = V("D2", tau, 0.05, "simpson")
        arrays[f"v12_tau{tag}_eta0_kms"] = v0
        arrays[f"T_v12_tau{tag}_eps025"] = tang[("D2", tau, "simpson", EPS_PRIMARY)]
        arrays[f"T_v12_tau{tag}_eps05"] = tang[("D2", tau, "simpson", EPS_CONTROL)]
        arrays[f"physical_frac_tau{tag}_eta005"] = (vp - v0) / v0
        arrays[f"physical_dv_tau{tag}_eta005_kms"] = vp - v0
    np.savez_compressed(args.npz_out, **arrays)

    print("STABLE_AEST_KSZ_R11A_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_KSZ_R11A_PHYSICAL=" + json.dumps(physical, sort_keys=True), flush=True)
    print("STABLE_AEST_KSZ_R11A_TAU=" + json.dumps(tau_coherence, sort_keys=True), flush=True)
    print("STABLE_AEST_KSZ_R11A_CLASSIFICATION=" + classification, flush=True)
    return 0 if classification == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
