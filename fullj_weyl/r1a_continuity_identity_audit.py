#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import evolving_flrw_weyl_bridge as r0
from fullj_weyl import evolving_flrw_weyl_bridge_r1 as r1

m = r1.m
static = m.static

R1_PREDATA_LOCK = "e41a11411e517a72e73dcf1290195b420b6ae032"
R1_IMPL_LOCK = "11140f9fd8b24157a87df2b85f18b51f2a9a6f60"
R1A_PREDATA_LOCK = "df9f8d80551c9ce6d115ebdd260ed6c84a229cd5"

PASS_LABEL = "FULLJ_WEYL_R1A_CONTINUITY_IDENTITY_PASS"
FAIL_LABEL = "FULLJ_WEYL_R1A_CONTINUITY_IDENTITY_FAIL"
INCOMPLETE_LABEL = "FULLJ_WEYL_R1A_CONTINUITY_IDENTITY_INCOMPLETE"

GLOBAL_GATE = 5.0e-3
MODE_GATE = 1.0e-2
THETA_MAP_GATE = 1.0e-12
COEFF_MASK_FRAC = 1.0e-8


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel_l2(pred, ref) -> float:
    p = np.asarray(pred, float)
    r = np.asarray(ref, float)
    return float(np.linalg.norm(p - r) / max(float(np.linalg.norm(r)), 1.0e-300))


def coeff_summary(num, den):
    num = np.asarray(num, float)
    den = np.asarray(den, float)
    scale = float(np.max(np.abs(den))) if den.size else 0.0
    if not np.isfinite(scale) or scale <= 0.0:
        return {"n": 0, "median": float("nan"), "p16": float("nan"), "p84": float("nan")}
    mask = np.isfinite(num) & np.isfinite(den) & (np.abs(den) > COEFF_MASK_FRAC * scale)
    if not np.any(mask):
        return {"n": 0, "median": float("nan"), "p16": float("nan"), "p84": float("nan")}
    vals = num[mask] / den[mask]
    return {
        "n": int(vals.size),
        "median": float(np.median(vals)),
        "p16": float(np.percentile(vals, 16.0)),
        "p84": float(np.percentile(vals, 84.0)),
    }


def audit():
    ancestry = {
        "r1_predata_lock": is_ancestor(R1_PREDATA_LOCK),
        "r1_implementation_lock": is_ancestor(R1_IMPL_LOCK),
        "r1a_predata_lock": is_ancestor(R1A_PREDATA_LOCK),
    }
    if not all(ancestry.values()):
        raise m.InputIncomplete(f"R1A ancestry missing: {ancestry}")

    data = r0.prepare_bridge_data()
    taus = np.asarray(data["tau_check"], float)
    zs = np.asarray(m.CHECK_Z, float)
    ks = np.asarray(m.K_MPC, float)
    if taus.size != 9 or ks.size != 6:
        raise m.InputIncomplete(f"expected 9 checkpoints and 6 modes, got {taus.size} and {ks.size}")

    rows = []
    lhs_all = []
    rhs_all = []
    pi_formula_all = []
    pi_required_all = []
    theta_back_all = []
    theta_all = []
    ctheta_num = []
    ctheta_den = []
    cphi_num = []
    cphi_den = []
    cH_num = []
    cH_den = []

    per_mode_lhs = [[] for _ in ks]
    per_mode_rhs = [[] for _ in ks]

    for iz, (tau, z) in enumerate(zip(taus, zs)):
        bg = r1.fluid_quantities(data, float(tau))
        a = float(bg["a"])
        Hconf = a * float(bg["H"])
        w = float(bg["w"])
        cad2 = float(bg["cad2"])
        rho = float(bg["rho"])
        Q = float(bg["Q"])

        for ik, (k, md) in enumerate(zip(ks, data["modes"])):
            sp = md["splines"]
            delta = float(sp["deltaA"](tau))
            delta_p = float(sp["deltaA"](tau, 1))
            theta = float(sp["thetaA"](tau))
            alpha = float(sp["alpha"](tau))
            E = float(sp["E"](tau))
            phi_p = float(sp["phi"](tau, 1))

            chi = Q * (a * theta / (k * k) + alpha)
            combo = static.KB * E + m.A * chi
            Pi = cad2 * delta + cad2 * k * k * combo / (3.0 * a * a * rho)

            T_H = 3.0 * Hconf * (w * delta - Pi)
            T_phi = 3.0 * (1.0 + w) * phi_p
            T_theta = -(1.0 + w) * theta
            rhs = T_H + T_phi + T_theta

            theta_back = (k * k / a) * (chi / Q - alpha)
            Pi_req = w * delta - (
                delta_p - (1.0 + w) * (3.0 * phi_p - theta)
            ) / (3.0 * Hconf)

            den_theta = (1.0 + w) * theta
            num_theta = T_H + T_phi - delta_p
            den_phi = 3.0 * (1.0 + w) * phi_p
            num_phi = delta_p - T_H + (1.0 + w) * theta
            den_H = T_H
            num_H = delta_p - (1.0 + w) * (3.0 * phi_p - theta)

            row = {
                "z": float(z), "tau": float(tau), "k_Mpc": float(k),
                "a": a, "Hconf": Hconf, "w": w, "cad2": cad2, "rho": rho,
                "delta": delta, "delta_prime": delta_p,
                "theta": theta, "theta_back": theta_back,
                "alpha": alpha, "E": E, "phi_prime": phi_p, "chi": chi,
                "Pi_formula": Pi, "Pi_required": Pi_req,
                "T_H": T_H, "T_phi": T_phi, "T_theta": T_theta,
                "rhs": rhs, "residual": delta_p - rhs,
            }
            rows.append(row)

            lhs_all.append(delta_p); rhs_all.append(rhs)
            pi_formula_all.append(Pi); pi_required_all.append(Pi_req)
            theta_back_all.append(theta_back); theta_all.append(theta)
            ctheta_num.append(num_theta); ctheta_den.append(den_theta)
            cphi_num.append(num_phi); cphi_den.append(den_phi)
            cH_num.append(num_H); cH_den.append(den_H)
            per_mode_lhs[ik].append(delta_p); per_mode_rhs[ik].append(rhs)

    global_rel = rel_l2(rhs_all, lhs_all)
    theta_map_rel = rel_l2(theta_back_all, theta_all)
    pi_rel = rel_l2(pi_formula_all, pi_required_all)
    per_mode = []
    for k, rr, ll in zip(ks, per_mode_rhs, per_mode_lhs):
        per_mode.append({"k_Mpc": float(k), "relative_L2": rel_l2(rr, ll)})

    coeffs = {
        "c_theta_expected_1": coeff_summary(ctheta_num, ctheta_den),
        "c_phi_expected_1": coeff_summary(cphi_num, cphi_den),
        "c_H_expected_1": coeff_summary(cH_num, cH_den),
    }
    term_norms = {
        "delta_prime": float(np.linalg.norm(lhs_all)),
        "rhs": float(np.linalg.norm(rhs_all)),
        "T_H": float(np.linalg.norm([r["T_H"] for r in rows])),
        "T_phi": float(np.linalg.norm([r["T_phi"] for r in rows])),
        "T_theta": float(np.linalg.norm([r["T_theta"] for r in rows])),
    }

    gates = {
        "global_continuity_relL2_le_5e-3": bool(global_rel <= GLOBAL_GATE),
        "all_mode_relL2_le_1e-2": bool(all(x["relative_L2"] <= MODE_GATE for x in per_mode)),
        "theta_map_relL2_le_1e-12": bool(theta_map_rel <= THETA_MAP_GATE),
    }
    passed = bool(all(gates.values()))
    classification = PASS_LABEL if passed else FAIL_LABEL

    result = {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": git_head(),
        "ancestry": ancestry,
        "scope": "corrected CLASS linear eta=0 continuity identity only; 6 modes x 9 checkpoints; no nonlinear trajectory rerun",
        "formula": "delta_A' = 3 Hconf (w_A delta_A - Pi_A) + (1+w_A)(3 Phi' - Theta_A)",
        "pressure_closure": "Pi_A = cad2 delta_A + cad2 k^2 [K_B E + (2-K_B) chi]/(3 a^2 rho_A)",
        "global_continuity_relative_L2": float(global_rel),
        "per_mode": per_mode,
        "theta_mapping_relative_L2": float(theta_map_rel),
        "Pi_formula_to_required_relative_L2": float(pi_rel),
        "coefficient_diagnostics": coeffs,
        "term_norms": term_norms,
        "gates": gates,
        "rows": rows,
        "NONLINEAR_TRAJECTORY_RERUN": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
    }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_weyl_r1a_continuity_audit.json")
    ap.add_argument("--csv-out", default="results/fullj_weyl_r1a_continuity_audit.csv")
    args = ap.parse_args()
    jout = Path(args.json_out); cout = Path(args.csv_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        print("FULLJ_WEYL_R1A_CONTINUITY_AUDIT_START", flush=True)
        res = audit()
        jout.write_text(json.dumps(res, indent=2, sort_keys=True, allow_nan=True) + "\n")
        rows = res["rows"]
        if rows:
            with cout.open("w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader(); w.writerows(rows)

        print(
            f"FULLJ_WEYL_R1A_GLOBAL relL2={res['global_continuity_relative_L2']:.12e} "
            f"thetaMap={res['theta_mapping_relative_L2']:.12e} "
            f"PiRel={res['Pi_formula_to_required_relative_L2']:.12e}",
            flush=True,
        )
        for x in res["per_mode"]:
            print(f"FULLJ_WEYL_R1A_MODE k={x['k_Mpc']:.12g} relL2={x['relative_L2']:.12e}", flush=True)
        for name, s in res["coefficient_diagnostics"].items():
            print(
                f"FULLJ_WEYL_R1A_COEFF name={name} n={s['n']} median={s['median']:.12e} "
                f"p16={s['p16']:.12e} p84={s['p84']:.12e}",
                flush=True,
            )
        print("FULLJ_WEYL_R1A_TERMS=" + json.dumps(res["term_norms"], sort_keys=True), flush=True)
        print("FULLJ_WEYL_R1A_GATES=" + json.dumps(res["gates"], sort_keys=True), flush=True)
        print(f"FULLJ_WEYL_R1A_CLASSIFICATION={res['classification']}", flush=True)
        print(f"FULLJ_WEYL_R1A_JSON={jout}", flush=True)
        print(f"FULLJ_WEYL_R1A_CSV={cout}", flush=True)
        return 0 if res["classification"] == PASS_LABEL else 2
    except m.InputIncomplete as exc:
        res = {
            "classification": INCOMPLETE_LABEL,
            "diagnostic_complete": False,
            "reason": str(exc),
            "git_head": git_head(),
            "NONLINEAR_TRAJECTORY_RERUN": False,
            "EVOLVING_WEYL_POWER_LICENSED": False,
            "ACT_LIKELIHOOD_LICENSED": False,
            "OBSERVATIONAL_CLAIM_LICENSED": False,
        }
        jout.write_text(json.dumps(res, indent=2, sort_keys=True) + "\n")
        print(f"FULLJ_WEYL_R1A_CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        print(f"FULLJ_WEYL_R1A_REASON={exc}", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
