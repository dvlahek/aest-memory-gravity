#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6c import r3_modewise_full_prehistory as r3
from nl1c6d2c6c_r4ref import build_dense_fullhistory_reference as r4

c = r3.c
m = c.m
base = r4.base
TARGET_INDEX = 5
ZSEL = np.asarray([5.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.5, 0.2], float)


def rel_l2(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(bb), 1.0e-300))


def symrel(a, b):
    a = float(a)
    b = float(b)
    return float(2.0 * abs(a - b) / max(abs(a) + abs(b), 1.0e-300))


def ratio(a, b):
    a = float(a)
    b = float(b)
    return float(a / b) if abs(b) > 1.0e-300 else float("nan")


def unique_history(raw):
    kt = base.pick(raw, ("tau [Mpc]", "tau", "tau[Mpc]"))
    ka = base.pick(raw, ("a", "scale factor"))
    kalpha = base.pick(raw, ("alpha_aest", "alpha"))
    kth = base.pick(raw, ("theta_cdm", "t_cdm"))
    tau = np.asarray(raw[kt], float)
    aa = np.asarray(raw[ka], float)
    alpha = np.asarray(raw[kalpha], float)
    theta = np.asarray(raw[kth], float)
    finite = np.isfinite(tau) & np.isfinite(aa) & np.isfinite(alpha) & np.isfinite(theta)
    tau, aa, alpha, theta = tau[finite], aa[finite], alpha[finite], theta[finite]
    order = np.argsort(tau)
    tau, aa, alpha, theta = tau[order], aa[order], alpha[order], theta[order]
    keep = np.ones(tau.size, dtype=bool)
    if tau.size > 1:
        keep[1:] = np.diff(tau) > 0.0
    tau, aa, alpha, theta = tau[keep], aa[keep], alpha[keep], theta[keep]
    if tau.size < 8:
        raise RuntimeError("insufficient finite unique direct history")
    return tau, aa, alpha, theta


def main() -> int:
    out = ROOT / "results" / "c3_mode5_source_terms.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    for key in (
        "AEST_TANGENT_TRACE_FILE",
        "AEST_TANGENT_FORCE_FILE",
        "AEST_TANGENT_LAMBDA",
        "AEST_TANGENT_ALLOW_K_MISS",
    ):
        os.environ.pop(key, None)
    os.environ["OMP_NUM_THREADS"] = "1"

    data = m.prepare_class_data()
    tau_targets = np.asarray(data["tau_check"][1:], float)
    if tau_targets.size != ZSEL.size:
        raise RuntimeError("frozen checkpoint size mismatch")

    from classy import Class
    cc = Class()
    cc.set(base.params(True))
    cc.compute()
    try:
        histories, _ = base.d2a.scalar_histories(cc.get_perturbations())
        if len(histories) != 6:
            raise RuntimeError(f"expected six direct histories, got {len(histories)}")

        direct = []
        for i, raw in enumerate(histories):
            tau, aa, alpha, theta = unique_history(raw)
            if tau_targets[0] < tau[0] or tau_targets[-1] > tau[-1]:
                raise RuntimeError(f"direct mode {i} does not cover frozen checkpoints")
            direct.append({
                "a": np.interp(tau_targets, tau, aa),
                "alpha": np.interp(tau_targets, tau, alpha),
                "theta": np.interp(tau_targets, tau, theta),
                "tau_first": float(tau[0]),
                "tau_last": float(tau[-1]),
            })

        offline = []
        for j in range(6):
            offline.append({
                "a": np.asarray([float(data["modes"][j]["splines"]["a"](t)) for t in tau_targets]),
                "alpha": np.asarray([float(data["modes"][j]["splines"]["alpha"](t)) for t in tau_targets]),
                "theta": np.asarray([float(data["modes"][j]["splines"]["theta"](t)) for t in tau_targets]),
            })

        matrix = np.zeros((6, 6), float)
        match_rows = []
        for i in range(6):
            for j in range(6):
                ea = rel_l2(direct[i]["alpha"], offline[j]["alpha"])
                et = rel_l2(direct[i]["theta"], offline[j]["theta"])
                cost = math.sqrt(ea * ea + et * et)
                matrix[i, j] = cost
                print(
                    f"MATCH direct={i} offline={j} ALPHA_L2={ea:.12e} "
                    f"THETA_L2={et:.12e} COMBINED={cost:.12e}",
                    flush=True,
                )
                match_rows.append({
                    "direct": i, "offline": j,
                    "alpha_l2": ea, "theta_l2": et, "combined": cost,
                })

        best = []
        for i in range(6):
            j = int(np.argmin(matrix[i]))
            self_cost = float(matrix[i, i])
            best_cost = float(matrix[i, j])
            gain = float(self_cost / max(best_cost, 1.0e-300))
            print(
                f"MATCH_BEST direct={i} offline={j} BEST={best_cost:.12e} "
                f"SELF={self_cost:.12e} SELF_OVER_BEST={gain:.12e}",
                flush=True,
            )
            best.append({
                "direct": i, "best_offline": j, "best_cost": best_cost,
                "self_cost": self_cost, "self_over_best": gain,
            })

        i = TARGET_INDEX
        k = float(m.K_MPC[i])
        points = []
        dchi = []
        ochi = []
        for iz, (zred, tau) in enumerate(zip(ZSEL, tau_targets)):
            ad = float(direct[i]["a"][iz])
            ao = float(offline[i]["a"][iz])
            Qd = float(data["bg"]["Q"](ad))
            # Use the exact offline background path that D2C6C actually uses.
            Qo = float(m.bg_eval(data, float(tau))[2])
            ald = float(direct[i]["alpha"][iz])
            alo = float(offline[i]["alpha"][iz])
            thd = float(direct[i]["theta"][iz])
            tho = float(offline[i]["theta"][iz])

            tad = Qd * ald
            tao = Qo * alo
            ttd = Qd * ad * thd / (k * k)
            tto = Qo * ao * tho / (k * k)
            chid = tad + ttd
            chio = tao + tto
            dchi.append(chid)
            ochi.append(chio)

            vals = {
                "z": float(zred), "tau": float(tau), "k_mpc": k,
                "a_class": ad, "a_offline": ao,
                "Q_class_path": Qd, "Q_offline_path": Qo,
                "alpha_class": ald, "alpha_offline": alo,
                "theta_class": thd, "theta_offline": tho,
                "Talpha_class": tad, "Talpha_offline": tao,
                "Ttheta_class": ttd, "Ttheta_offline": tto,
                "chi_class": chid, "chi_offline": chio,
                "alpha_ratio": ratio(ald, alo),
                "theta_ratio": ratio(thd, tho),
                "Talpha_ratio": ratio(tad, tao),
                "Ttheta_ratio": ratio(ttd, tto),
                "chi_ratio": ratio(chid, chio),
                "alpha_symrel": symrel(ald, alo),
                "theta_symrel": symrel(thd, tho),
                "Talpha_symrel": symrel(tad, tao),
                "Ttheta_symrel": symrel(ttd, tto),
                "chi_symrel": symrel(chid, chio),
            }
            points.append(vals)
            print(
                f"MODE5_POINT z={zred:g} tau={tau:.12e} k={k:.12e} "
                f"aC={ad:.12e} aO={ao:.12e} QC={Qd:.12e} QO={Qo:.12e} "
                f"alphaC={ald:.12e} alphaO={alo:.12e} alphaR={vals['alpha_ratio']:.12e} "
                f"thetaC={thd:.12e} thetaO={tho:.12e} thetaR={vals['theta_ratio']:.12e} "
                f"TaC={tad:.12e} TaO={tao:.12e} TaR={vals['Talpha_ratio']:.12e} "
                f"TtC={ttd:.12e} TtO={tto:.12e} TtR={vals['Ttheta_ratio']:.12e} "
                f"chiC={chid:.12e} chiO={chio:.12e} chiR={vals['chi_ratio']:.12e}",
                flush=True,
            )

        alpha_l2 = rel_l2(direct[i]["alpha"], offline[i]["alpha"])
        theta_l2 = rel_l2(direct[i]["theta"], offline[i]["theta"])
        chi_l2 = rel_l2(dchi, ochi)
        a_l2 = rel_l2(direct[i]["a"], offline[i]["a"])
        best5 = best[i]
        dominant = "alpha" if alpha_l2 >= theta_l2 else "theta"
        print(
            f"MODE5_SUMMARY A_L2={a_l2:.12e} ALPHA_L2={alpha_l2:.12e} "
            f"THETA_L2={theta_l2:.12e} CHI_L2={chi_l2:.12e} "
            f"BEST_OFFLINE_INDEX={best5['best_offline']} DOMINANT_RAW_FIELD={dominant}",
            flush=True,
        )
        print("CLASSIFICATION=C3_MODE5_SOURCE_AUDIT_COMPLETE", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)

        report = {
            "classification": "C3_MODE5_SOURCE_AUDIT_COMPLETE",
            "target_mode": 5,
            "k_mpc": k,
            "z": ZSEL.tolist(),
            "matching_matrix": matrix.tolist(),
            "matching_rows": match_rows,
            "best_matches": best,
            "mode5_summary": {
                "a_l2": a_l2,
                "alpha_l2": alpha_l2,
                "theta_l2": theta_l2,
                "chi_l2": chi_l2,
                "best_offline_index": int(best5["best_offline"]),
                "dominant_raw_field": dominant,
            },
            "points": points,
            "finite_positive_eta_licensed": False,
        }
        out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        return 0
    finally:
        cc.struct_cleanup()
        cc.empty()


if __name__ == "__main__":
    raise SystemExit(main())
