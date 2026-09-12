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

R1B_PREDATA_LOCK = "851dc7c6d6bed31f3cd7ff139eaf322e4a192368"
R1A_IMPL_LOCK = "27d4fbeb902a0ef1b6b7fc3b221ccde40b422550"

PASS_LABEL = "FULLJ_WEYL_R1B_EULER_IDENTITY_PASS"
FAIL_LABEL = "FULLJ_WEYL_R1B_EULER_IDENTITY_FAIL"
INCOMPLETE_LABEL = "FULLJ_WEYL_R1B_EULER_IDENTITY_INCOMPLETE"
GLOBAL_GATE = 5.0e-3
MODE_GATE = 1.0e-2


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


def audit():
    ancestry = {
        "r1b_predata_lock": is_ancestor(R1B_PREDATA_LOCK),
        "r1a_implementation_lock": is_ancestor(R1A_IMPL_LOCK),
    }
    if not all(ancestry.values()):
        raise m.InputIncomplete(f"R1B ancestry missing: {ancestry}")

    data = r0.prepare_bridge_data()
    taus = np.asarray(data["tau_check"], float)
    zs = np.asarray(m.CHECK_Z, float)
    ks = np.asarray(m.K_MPC, float)
    if taus.size != 9 or ks.size != 6:
        raise m.InputIncomplete(f"expected 9 checkpoints and 6 modes, got {taus.size} and {ks.size}")

    rows = []
    lhs_all, rhs_all = [], []
    per_lhs = [[] for _ in ks]
    per_rhs = [[] for _ in ks]
    kappas = []

    for tau, z in zip(taus, zs):
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
            theta = float(sp["thetaA"](tau))
            theta_p = float(sp["thetaA"](tau, 1))
            alpha = float(sp["alpha"](tau))
            E = float(sp["E"](tau))
            psi = float(sp["psi_bridge"](tau))

            # Exact linear bridge relation, used only to reconstruct chi for the
            # already frozen pressure closure in this direct CLASS identity audit.
            chi = Q * (a * theta / (k * k) + alpha)
            combo = static.KB * E + m.A * chi
            Pi = cad2 * delta + cad2 * k * k * combo / (3.0 * a * a * rho)

            T_drag = (3.0 * cad2 - 1.0) * Hconf * theta
            T_pi = k * k * Pi / (1.0 + w)
            T_psi = k * k * psi
            rhs = T_drag + T_pi + T_psi

            velpot = chi / Q - alpha
            kappa = (abs(chi / Q) + abs(alpha)) / max(abs(velpot), 1.0e-300)
            finite = bool(np.all(np.isfinite([delta, theta, theta_p, alpha, E, psi, chi, Pi, rhs, kappa])))

            row = {
                "z": float(z), "tau": float(tau), "k_Mpc": float(k),
                "a": a, "Hconf": Hconf, "w": w, "cad2": cad2, "rho": rho,
                "delta": delta, "theta": theta, "theta_prime": theta_p,
                "alpha": alpha, "E": E, "psi": psi, "chi": chi, "Pi": Pi,
                "T_drag": T_drag, "T_pi": T_pi, "T_psi": T_psi,
                "rhs": rhs, "residual": theta_p - rhs,
                "theta_map_condition_number": kappa,
                "finite": finite,
            }
            rows.append(row)
            lhs_all.append(theta_p); rhs_all.append(rhs); kappas.append(kappa)
            per_lhs[ik].append(theta_p); per_rhs[ik].append(rhs)

    global_rel = rel_l2(rhs_all, lhs_all)
    per_mode = [
        {"k_Mpc": float(k), "relative_L2": rel_l2(rr, ll)}
        for k, rr, ll in zip(ks, per_rhs, per_lhs)
    ]
    finite_count = int(sum(bool(r["finite"]) for r in rows))
    condition = {
        "min": float(np.min(kappas)),
        "median": float(np.median(kappas)),
        "max": float(np.max(kappas)),
        "p16": float(np.percentile(kappas, 16.0)),
        "p84": float(np.percentile(kappas, 84.0)),
    }
    term_norms = {
        "theta_prime": float(np.linalg.norm(lhs_all)),
        "rhs": float(np.linalg.norm(rhs_all)),
        "T_drag": float(np.linalg.norm([r["T_drag"] for r in rows])),
        "T_pi": float(np.linalg.norm([r["T_pi"] for r in rows])),
        "T_psi": float(np.linalg.norm([r["T_psi"] for r in rows])),
    }
    gates = {
        "global_euler_relL2_le_5e-3": bool(global_rel <= GLOBAL_GATE),
        "all_mode_relL2_le_1e-2": bool(all(x["relative_L2"] <= MODE_GATE for x in per_mode)),
        "all_54_finite": bool(finite_count == 54),
    }
    classification = PASS_LABEL if all(gates.values()) else FAIL_LABEL
    return {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": git_head(),
        "ancestry": ancestry,
        "scope": "corrected CLASS linear eta=0 Euler identity only; 6 modes x 9 checkpoints; no nonlinear trajectory rerun",
        "formula": "Theta_A' = (3 cad2 - 1) Hconf Theta_A + k^2 Pi_A/(1+w_A) + k^2 Psi",
        "pressure_closure": "Pi_A = cad2 delta_A + cad2 k^2 [K_B E + (2-K_B) chi]/(3 a^2 rho_A)",
        "global_euler_relative_L2": float(global_rel),
        "per_mode": per_mode,
        "finite_points": finite_count,
        "theta_map_condition_number": condition,
        "term_norms": term_norms,
        "gates": gates,
        "rows": rows,
        "NONLINEAR_TRAJECTORY_RERUN": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_weyl_r1b_euler_audit.json")
    ap.add_argument("--csv-out", default="results/fullj_weyl_r1b_euler_audit.csv")
    args = ap.parse_args()
    jout, cout = Path(args.json_out), Path(args.csv_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        print("FULLJ_WEYL_R1B_EULER_AUDIT_START", flush=True)
        res = audit()
        jout.write_text(json.dumps(res, indent=2, sort_keys=True, allow_nan=True) + "\n")
        if res["rows"]:
            with cout.open("w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(res["rows"][0].keys()))
                w.writeheader(); w.writerows(res["rows"])
        print(
            f"FULLJ_WEYL_R1B_GLOBAL relL2={res['global_euler_relative_L2']:.12e} "
            f"finite={res['finite_points']}/54",
            flush=True,
        )
        for x in res["per_mode"]:
            print(f"FULLJ_WEYL_R1B_MODE k={x['k_Mpc']:.12g} relL2={x['relative_L2']:.12e}", flush=True)
        c = res["theta_map_condition_number"]
        print(
            f"FULLJ_WEYL_R1B_CONDITION min={c['min']:.12e} median={c['median']:.12e} "
            f"p84={c['p84']:.12e} max={c['max']:.12e}", flush=True
        )
        print("FULLJ_WEYL_R1B_TERMS=" + json.dumps(res["term_norms"], sort_keys=True), flush=True)
        print("FULLJ_WEYL_R1B_GATES=" + json.dumps(res["gates"], sort_keys=True), flush=True)
        print(f"FULLJ_WEYL_R1B_CLASSIFICATION={res['classification']}", flush=True)
        print(f"FULLJ_WEYL_R1B_JSON={jout}", flush=True)
        print(f"FULLJ_WEYL_R1B_CSV={cout}", flush=True)
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
        print(f"FULLJ_WEYL_R1B_CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        print(f"FULLJ_WEYL_R1B_REASON={exc}", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
