#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
PREDATA_LOCK = "c76075ec27325f525fde70154551c20bf23d0759"
R2_JSON = ROOT / "results/mcmg_r2_self_consistent_growth_weyl.json"

A_INI = 1.0e-3
N_EVAL = 4097
U_VALUES = (0.005, 0.01, 0.02)
ETA_TAN = 0.01
ETA_FINITE = (-0.5, 0.5)
U_FINITE = 0.02
KERNELS = ("exp", "erlang2", "erlang4", "biexp")
BACKGROUNDS = {
    "B0": {"Omega_m0": 0.315, "w": -1.0},
    "B1": {"Omega_m0": 0.270, "w": -1.0},
    "B2": {"Omega_m0": 0.360, "w": -1.0},
    "B3": {"Omega_m0": 0.315, "w": -0.9},
    "B4": {"Omega_m0": 0.315, "w": -1.1},
}

PASS = "MCMG_GROWTH_WEYL_MEMORY_GENERALITY_PASS"
NUM_FAIL = "MCMG_R3_NUMERICAL_CONTROL_FAIL"
TAN_FAIL = "MCMG_R3_TANGENT_CONTROL_FAIL"
CONS_FAIL = "MCMG_R3_GROWTH_WEYL_CONSISTENCY_FAIL"
MOM_FAIL = "MCMG_R3_FIRST_MOMENT_GENERALITY_FAIL"
KERNEL_FAIL = "MCMG_R3_KERNEL_COLLAPSE_FAIL"
FINITE_FAIL = "MCMG_R3_FINITE_AMPLITUDE_GENERALITY_FAIL"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel_l2(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(aa), np.linalg.norm(bb), 1e-300))


def background_quantities(a, om0: float, w: float):
    aa = np.asarray(a, float)
    ode0 = 1.0 - om0
    m = om0 * aa ** -3.0
    de = ode0 * aa ** (-3.0 * (1.0 + w))
    e2 = m + de
    E = np.sqrt(e2)
    om = m / e2
    ode = de / e2
    dlnH = -1.5 * (om + (1.0 + w) * ode)
    return E, om, dlnH


def solve_gr(om0: float, w: float):
    n0 = math.log(A_INI)

    def rhs(n, y):
        a = math.exp(n)
        _, om, dlnh = background_quantities(a, om0, w)
        D, V = y
        return [V, -(2.0 + float(dlnh)) * V + 1.5 * float(om) * D]

    sol = solve_ivp(
        rhs, (n0, 0.0), [A_INI, A_INI], method="DOP853",
        rtol=2e-12, atol=2e-14, dense_output=True, max_step=0.02,
    )
    if not sol.success or sol.sol is None:
        raise RuntimeError(f"GR integration failed om0={om0} w={w}: {sol.message}")
    norm = float(sol.sol(0.0)[0])
    if not np.isfinite(norm) or norm <= 0:
        raise RuntimeError("invalid GR normalization")

    def evaluate(a):
        aa = np.asarray(a, float)
        vals = sol.sol(np.log(aa))
        return np.asarray(vals[0], float) / norm, np.asarray(vals[1], float) / norm

    return evaluate


def kernel_state_count(kind: str) -> int:
    return {"exp": 1, "erlang2": 2, "erlang4": 4, "biexp": 2}[kind]


def memory_output(kind: str, q):
    qq = np.asarray(q, float)
    if kind in ("exp", "erlang2", "erlang4"):
        return float(qq[-1])
    if kind == "biexp":
        return float(0.5 * qq[0] + 0.5 * qq[1])
    raise KeyError(kind)


def memory_derivatives(kind: str, q, source: float, u: float, E: float):
    qq = np.asarray(q, float)
    if kind == "exp":
        return np.asarray([(source - qq[0]) / (u * E)])
    if kind == "erlang2":
        tau = u / 2.0
        return np.asarray([
            (source - qq[0]) / (tau * E),
            (qq[0] - qq[1]) / (tau * E),
        ])
    if kind == "erlang4":
        tau = u / 4.0
        out = np.empty(4, float)
        out[0] = (source - qq[0]) / (tau * E)
        for i in range(1, 4):
            out[i] = (qq[i - 1] - qq[i]) / (tau * E)
        return out
    if kind == "biexp":
        return np.asarray([
            (source - qq[0]) / ((0.5 * u) * E),
            (source - qq[1]) / ((1.5 * u) * E),
        ])
    raise KeyError(kind)


def solve_system(eval_gr, om0: float, w: float, kind: str, u: float, eta: float, N):
    d0, v0 = eval_gr(np.asarray([A_INI], float))
    s0 = float(d0[0] / A_INI)
    nq = kernel_state_count(kind)
    y0 = np.asarray([float(d0[0]), float(v0[0])] + [s0] * nq, float)

    def rhs(n, y):
        a = math.exp(n)
        E, om, dlnh = background_quantities(a, om0, w)
        E = float(E); om = float(om); dlnh = float(dlnh)
        D, V = float(y[0]), float(y[1])
        q = y[2:]
        M = memory_output(kind, q)
        source = D / a
        drive = (1.0 - eta) * D + eta * a * M
        dq = memory_derivatives(kind, q, source, u, E)
        return np.concatenate((
            np.asarray([V, -(2.0 + dlnh) * V + 1.5 * om * drive]), dq
        ))

    sol = solve_ivp(
        rhs, (float(N[0]), float(N[-1])), y0, t_eval=N, method="Radau",
        rtol=2e-10, atol=2e-12, max_step=0.02,
    )
    if not sol.success:
        raise RuntimeError(f"integration failed bg=({om0},{w}) kernel={kind} u={u} eta={eta}: {sol.message}")
    Y = np.asarray(sol.y, float)
    D, V = Y[0], Y[1]
    if kind in ("exp", "erlang2", "erlang4"):
        M = Y[-1]
    else:
        M = 0.5 * Y[2] + 0.5 * Y[3]
    P = (1.0 - eta) * D / np.exp(N) + eta * M
    return {"Y": Y, "D": D, "V": V, "M": M, "P": P}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/mcmg_r3_heldout_generality.json")
    ap.add_argument("--npz-out", default="results/mcmg_r3_heldout_generality.npz")
    args = ap.parse_args()

    if not is_ancestor(PREDATA_LOCK):
        raise SystemExit("MCMG_R3_PREDATA_LOCK_FAIL")
    if not R2_JSON.exists():
        raise SystemExit("MCMG_R3_R2_RESULT_MISSING")
    r2j = json.loads(R2_JSON.read_text())
    if r2j.get("classification") != "MCMG_SELF_CONSISTENT_GROWTH_WEYL_MEMORY_PASS":
        raise SystemExit("MCMG_R3_R2_PARENT_NOT_PASS")

    print("MCMG_R3_START", flush=True)
    N = np.linspace(math.log(A_INI), 0.0, N_EVAL)
    a = np.exp(N)
    z = 1.0 / a - 1.0
    win = z <= 2.0 + 1e-12

    all_finite = True
    all_positive = True
    nested_errors = {}
    tangent_symmetry = {}
    tangent_consistency = {}
    first_moment_errors = {}
    kernel_collapse = {}
    finite_amplitude = {}
    arrays = {"N": N, "a": a, "z": z}

    C_store = {}
    L_store = {}
    T_store = {}

    for bname, bg in BACKGROUNDS.items():
        om0 = float(bg["Omega_m0"]); w = float(bg["w"])
        eval_gr = solve_gr(om0, w)
        D0, V0 = eval_gr(a)
        P0 = D0 / a
        E, _, _ = background_quantities(a, om0, w)
        dPdx = E * (V0 - D0) / a
        T = -dPdx / P0
        T_store[bname] = T
        arrays[f"D_GR_{bname}"] = D0
        arrays[f"P_GR_{bname}"] = P0
        arrays[f"T_{bname}"] = T

        nested_errors[bname] = {}
        tangent_symmetry[bname] = {}
        tangent_consistency[bname] = {}
        first_moment_errors[bname] = {}
        finite_amplitude[bname] = {}

        for kind in KERNELS:
            nested_errors[bname][kind] = {}
            tangent_symmetry[bname][kind] = {}
            tangent_consistency[bname][kind] = {}
            first_moment_errors[bname][kind] = {}
            finite_amplitude[bname][kind] = {}

            for u in U_VALUES:
                rz = solve_system(eval_gr, om0, w, kind, u, 0.0, N)
                rp = solve_system(eval_gr, om0, w, kind, u, +ETA_TAN, N)
                rm = solve_system(eval_gr, om0, w, kind, u, -ETA_TAN, N)
                for rr in (rz, rp, rm):
                    all_finite &= bool(np.all(np.isfinite(rr["Y"])) and np.all(np.isfinite(rr["P"])))
                    all_positive &= bool(np.all(rr["D"] > 0))

                de = rel_l2(rz["D"][win], D0[win])
                pe = rel_l2(rz["P"][win], P0[win])
                nested_errors[bname][kind][str(u)] = {"D": de, "P": pe}

                gp = rp["D"] / D0 - 1.0; gm = rm["D"] / D0 - 1.0
                wp = rp["P"] / P0 - 1.0; wm = rm["P"] / P0 - 1.0
                eg = float(np.linalg.norm((gp + gm)[win]) / max(np.linalg.norm((gp - gm)[win]), 1e-300))
                ew = float(np.linalg.norm((wp + wm)[win]) / max(np.linalg.norm((wp - wm)[win]), 1e-300))
                tangent_symmetry[bname][kind][str(u)] = {"growth_even_to_odd": eg, "weyl_even_to_odd": ew}

                C = ((wp - gp) - (wm - gm)) / (2.0 * ETA_TAN)
                L = (rz["M"] - P0) / P0
                C_store[(bname, kind, u)] = C
                L_store[(bname, kind, u)] = L
                ce = rel_l2(C[win], L[win])
                me = rel_l2((C / u)[win], T[win])
                tangent_consistency[bname][kind][str(u)] = ce
                first_moment_errors[bname][kind][str(u)] = me

                print(
                    f"MCMG_R3_TANGENT bg={bname} kernel={kind} u={u:.6f} "
                    f"memory_cons={ce:.6e} first_moment={me:.6e} odd={max(eg,ew):.6e}",
                    flush=True,
                )

                utag = str(u).replace('.', 'p')
                arrays[f"C_{bname}_{kind}_u{utag}"] = C
                arrays[f"L_{bname}_{kind}_u{utag}"] = L

            # Finite-amplitude held-out control at u=0.02.
            rz = solve_system(eval_gr, om0, w, kind, U_FINITE, 0.0, N)
            Lf = (rz["M"] - P0) / P0
            for eta in ETA_FINITE:
                rr = solve_system(eval_gr, om0, w, kind, U_FINITE, eta, N)
                all_finite &= bool(np.all(np.isfinite(rr["Y"])) and np.all(np.isfinite(rr["P"])))
                all_positive &= bool(np.all(rr["D"] > 0))
                g = rr["D"] / D0 - 1.0
                ww = rr["P"] / P0 - 1.0
                h = ww - g
                rec = {
                    "growth_today": float(g[-1]),
                    "weyl_today": float(ww[-1]),
                    "max_abs_growth": float(np.max(np.abs(g[win]))),
                    "max_abs_weyl": float(np.max(np.abs(ww[win]))),
                    "finite_relation_relL2": rel_l2((h / eta)[win], Lf[win]),
                }
                finite_amplitude[bname][kind][str(eta)] = rec

    # G1 finite positive evolution.
    g1 = bool(all_finite and all_positive)

    # G2 nested GR.
    max_nested = 0.0
    for b in nested_errors.values():
        for k in b.values():
            for urec in k.values():
                max_nested = max(max_nested, max(urec.values()))
    g2 = bool(max_nested <= 1e-8)

    # G3 tangent odd symmetry.
    max_odd = 0.0
    for b in tangent_symmetry.values():
        for k in b.values():
            for urec in k.values():
                max_odd = max(max_odd, max(urec.values()))
    g3 = bool(max_odd <= 0.02)

    # G4 exact growth-Weyl memory consistency.
    max_cons = max(
        val for b in tangent_consistency.values() for k in b.values() for val in k.values()
    )
    g4 = bool(max_cons <= 0.005)

    # G5 first-moment universality and convergence.
    max_m005 = 0.0
    convergence_all = True
    for b in first_moment_errors.values():
        for k in b.values():
            e005 = k[str(0.005)]; e02 = k[str(0.02)]
            max_m005 = max(max_m005, e005)
            convergence_all &= bool(e005 < e02)
    g5 = bool(max_m005 <= 0.03 and convergence_all)

    # G6 kernel-shape collapse at fixed first moment u=0.005.
    max_collapse = 0.0
    for bname in BACKGROUNDS:
        pair = []
        for i, ka in enumerate(KERNELS):
            qa = C_store[(bname, ka, 0.005)] / 0.005
            for kb in KERNELS[i + 1:]:
                qb = C_store[(bname, kb, 0.005)] / 0.005
                pair.append(rel_l2(qa[win], qb[win]))
        kernel_collapse[bname] = {"pairwise": pair, "max": float(max(pair))}
        max_collapse = max(max_collapse, max(pair))
    g6 = bool(max_collapse <= 0.02)

    # G7 finite-amplitude relation and stability.
    max_finite_relation = 0.0
    g7 = True
    for b in finite_amplitude.values():
        for k in b.values():
            for eta_s, rec in k.items():
                eta = float(eta_s)
                max_finite_relation = max(max_finite_relation, rec["finite_relation_relL2"])
                if not (
                    np.sign(rec["growth_today"]) == np.sign(eta)
                    and np.sign(rec["weyl_today"]) == np.sign(eta)
                    and rec["max_abs_growth"] < 0.05
                    and rec["max_abs_weyl"] < 0.05
                    and rec["finite_relation_relL2"] <= 0.01
                ):
                    g7 = False
    g7 = bool(g7 and g1)

    gates = {
        "R3_G1_finite_positive_evolution": g1,
        "R3_G2_nested_GR_all_kernel_background": g2,
        "R3_G3_tangent_odd_symmetry": g3,
        "R3_G4_growth_weyl_memory_consistency": g4,
        "R3_G5_first_moment_universality": g5,
        "R3_G6_kernel_shape_collapse": g6,
        "R3_G7_finite_amplitude_relation_and_stability": g7,
    }

    if not all((g1, g2)):
        classification = NUM_FAIL
    elif not g3:
        classification = TAN_FAIL
    elif not g4:
        classification = CONS_FAIL
    elif not g5:
        classification = MOM_FAIL
    elif not g6:
        classification = KERNEL_FAIL
    elif not g7:
        classification = FINITE_FAIL
    else:
        classification = PASS

    summary = {
        "classification": classification,
        "background_count": len(BACKGROUNDS),
        "kernel_count": len(KERNELS),
        "max_nested_GR_relative_L2": float(max_nested),
        "max_tangent_even_to_odd": float(max_odd),
        "max_tangent_vs_passive_lag_relative_L2": float(max_cons),
        "max_first_moment_error_u0p005": float(max_m005),
        "all_first_moment_u0p005_better_than_u0p02": bool(convergence_all),
        "max_kernel_collapse_u0p005": float(max_collapse),
        "max_finite_amplitude_relation_relL2": float(max_finite_relation),
    }

    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "predata_lock": PREDATA_LOCK,
        "parent_R2_classification": r2j.get("classification"),
        "backgrounds": BACKGROUNDS,
        "kernels": list(KERNELS),
        "u_values": list(U_VALUES),
        "eta_tangent": ETA_TAN,
        "finite_amplitude_eta": list(ETA_FINITE),
        "finite_amplitude_u": U_FINITE,
        "gates": gates,
        "summary": summary,
        "nested_GR_errors": nested_errors,
        "tangent_symmetry": tangent_symmetry,
        "tangent_consistency": tangent_consistency,
        "first_moment_errors": first_moment_errors,
        "kernel_collapse": kernel_collapse,
        "finite_amplitude": finite_amplitude,
        "interpretation": {
            "licenses_memory_consistency_derivation_or_projection": bool(classification == PASS),
            "new_physics_claim_licensed": False,
            "observational_claim_licensed": False,
            "Nature_claim_licensed": False,
            "AeST_reclassified": False,
        },
    }

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(args.npz_out, **arrays)

    print("MCMG_R3_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("MCMG_R3_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("MCMG_R3_CLASSIFICATION=" + classification, flush=True)
    return 0 if classification == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
