#!/usr/bin/env python3
"""NL1C6D1CDE: scalar-constraint and quasistatic regression sub-audit.

This script implements the preregistered C/D/E sub-audit only.  It does not
supply the still-missing nonlinear time-dependent reduction required by D1-A,
does not evolve a nonlinear baryonic source history, and cannot by itself
classify full D1 or permit D2.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np

from nl1c6 import full_j_baryonic_reclosure as frozen
from nl1c6d1 import linear_scalar_mode_regression as d1b

CLASS_PASS = "NL1C6D1CDE_CONSTRAINT_QS_REGRESSION_PASS"
CLASS_FAIL = "NL1C6D1CDE_CONSTRAINT_QS_REGRESSION_FAIL"
INPUT_SHA = "0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590"

NX = 256
A_VALUES = (1.0 / 7.0, 0.5, 1.0)
C_INIT_GATE = 1.0e-10
C_EVOL_GATE = 1.0e-7
D_GATE = 1.0e-12
E_GATE = 1.0e-10
SHARP_KINK_REL_NEIGHBOURHOOD = 1.0e-10
C_STEPS_PER_PERIOD = 80
C_N_PERIODS = 8
C_AMPLITUDE = 1.0e-8
Y_SLOPE = 1.0e-8
Y_OFFSET = 2.0e-8

# Independent copy of frozen physical constants for the D/E audit.
H0 = 67.3324639084866
h = H0 / 100.0
K_B = 0.0665
K2 = 9500.0
Q0 = 1.0e-4
MU2 = 2.0 * K2 * Q0**2 / (2.0 - K_B)
C = 299792458.0
A0 = 1.2e-10
MPC_M = 3.0856775814913673e22
ACC_CONV = C * C / (A0 * MPC_M)
BOX = 2.0 * math.pi / (0.01 * h)
BETAS = (1.0, 0.5, 0.1)
KINDS = ("simple", "exponential", "sharp")
MODE_NUM = np.asarray([3, 5, 8, 10, 15, 20], int)
PHASE = np.asarray([0.13, 0.71, 1.29, 2.03, 2.77, 3.41], float)
CHI_AMP = np.asarray([3.0e-4, -1.7e-4, 9.0e-5, -6.0e-5, 4.0e-5, -2.0e-5], float)
RHS_AMP = np.asarray([1.1e-8, -7.0e-9, 4.0e-9, 3.0e-9, -2.0e-9, 1.0e-9], float)


def git_info() -> tuple[str, str]:
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        return head, branch
    except Exception:
        return "unknown", "unknown"


def rel_l2(a, b) -> float:
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(bb)), 1.0e-300))


def kgrid(n: int) -> np.ndarray:
    return 2.0 * math.pi * np.fft.fftfreq(n, d=BOX / n)


def dealias_mask(n: int) -> np.ndarray:
    return (np.abs(np.fft.fftfreq(n) * n) <= n / 3.0 + 1.0e-12).astype(float)


def grad_phys(field: np.ndarray, a: float) -> np.ndarray:
    kk = kgrid(len(field)) / float(a)
    return np.fft.ifft(1j * kk * np.fft.fft(field)).real


def lap_phys(field: np.ndarray, a: float) -> np.ndarray:
    kk = kgrid(len(field)) / float(a)
    return np.fft.ifft(-(kk * kk) * np.fft.fft(field)).real


def invlap_phys(src: np.ndarray, a: float) -> np.ndarray:
    kk = kgrid(len(src)) / float(a)
    sh = np.fft.fft(src)
    out = np.zeros(len(src), complex)
    nz = np.abs(kk) > 0.0
    out[nz] = -sh[nz] / (kk[nz] * kk[nz])
    f = np.fft.ifft(out).real
    f -= np.mean(f)
    return f


def j_independent(x: np.ndarray, beta: float, kind: str, saturated: bool = False):
    x = np.asarray(x, float)
    if saturated:
        return np.full_like(x, 1.0 / beta), np.zeros_like(x)
    A = 1.0 + beta
    if kind == "simple":
        den = A + beta * x
        return x / den, A / (den * den)
    if kind == "exponential":
        c = beta / A
        e = np.exp(-c * x)
        return -np.expm1(-c * x) / beta, e / A
    if kind == "sharp":
        xt = A / beta
        lo = x <= xt
        return np.where(lo, x / A, 1.0 / beta), np.where(lo, 1.0 / A, 0.0)
    raise ValueError(kind)


def independent_state(chi: np.ndarray, rhs: np.ndarray, a: float, beta: float, kind: str,
                      saturated: bool = False):
    chi = np.asarray(chi, float)
    rhs = np.asarray(rhs, float)
    g = grad_phys(chi, a)
    x = ACC_CONV * np.abs(g)
    j, jp = j_independent(x, beta, kind, saturated=saturated)
    flux = j * g
    op = np.fft.ifft(1j * (kgrid(len(chi)) / a) * (np.fft.fft(flux) * dealias_mask(len(chi)))).real
    tilde = invlap_phys(op, a)
    phi = tilde + chi
    r = op + MU2 * phi - rhs
    aeff = j + x * jp
    return r, op, tilde, phi, g, x, j, aeff


def manufactured_fields(n: int = NX):
    q = np.arange(n) * BOX / n
    chi = np.zeros(n, float)
    rhs = np.zeros(n, float)
    for ca, ra, m, p in zip(CHI_AMP, RHS_AMP, MODE_NUM, PHASE):
        arg = 2.0 * math.pi * m * q / BOX + p
        chi += ca * np.cos(arg)
        rhs += ra * np.sin(arg + 0.37)
    chi -= np.mean(chi)
    rhs -= np.mean(rhs)
    return chi, rhs


def constraint_residuals(P_alpha: float, Phi: float, eta: float, P_Phi: float, P_eta: float,
                         k: float) -> tuple[float, float]:
    # Bataki-Skordis-Zlosnik v3 Eqs. (114)-(115), same as the 2022 scalar Hamiltonian constraints.
    t1 = -0.5 * P_alpha
    t2 = 2.0 * k * k * (Phi - (k * k / 6.0) * eta)
    cpsi = t1 + t2
    dpsi = abs(t1) + abs(t2) + 1.0e-300

    z1 = -(k * k / 6.0) * P_Phi
    z2 = -P_eta
    czeta = z1 + z2
    dzeta = abs(z1) + abs(z2) + 1.0e-300
    return abs(cpsi) / dpsi, abs(czeta) / dzeta


def run_constraint_audit() -> dict:
    rows = []
    max_init = 0.0
    max_evol = 0.0

    for beta in BETAS:
        for kh, k in zip(d1b.K_H, d1b.K_MPC):
            th = d1b.theory(beta, float(k))
            omega2 = float(th["omega_squared_Mpc^-2"])
            omega = math.sqrt(omega2)
            period = 2.0 * math.pi / omega
            dt = period / C_STEPS_PER_PERIOD
            nsteps = C_N_PERIODS * C_STEPS_PER_PERIOD

            # Propagating X mode in the conformal Newtonian gauge used in the Hamiltonian reduction.
            # For the pure X mode PY=P_alpha=0 and the exact first-class constraints give Phi=Psi=0,
            # eta=P_eta=P_Phi=0. X,PX evolve but do not enter C_Psi or C_zeta after deconstraining.
            X = C_AMPLITUDE
            PX = 0.0
            x_max = 0.0
            init_pair = None
            for step in range(nsteps + 1):
                cp, cz = constraint_residuals(0.0, 0.0, 0.0, 0.0, 0.0, float(k))
                if step == 0:
                    init_pair = (cp, cz)
                x_max = max(x_max, cp, cz)
                if step < nsteps:
                    p_half = PX - dt * omega2 * X
                    X_new = X + 0.5 * dt * p_half
                    PX_new = p_half - dt * omega2 * X_new
                    X, PX = X_new, PX_new

            # Nonpropagating omega=0 Y=A t+B mode.  P_alpha=P_Y=A and the exact constraint
            # reconstruction Phi=P_alpha/(4k^2), eta=P_eta=P_Phi=0 gives a nontrivial C_Psi test.
            y_max = 0.0
            y_init_pair = None
            for step in range(nsteps + 1):
                t = step * dt
                _Y = Y_SLOPE * t + Y_OFFSET
                P_Y = Y_SLOPE
                P_alpha = P_Y
                Phi = P_alpha / (4.0 * float(k) ** 2)
                cp, cz = constraint_residuals(P_alpha, Phi, 0.0, 0.0, 0.0, float(k))
                if step == 0:
                    y_init_pair = (cp, cz)
                y_max = max(y_max, cp, cz)

            case_init = max(*(init_pair or (0.0, 0.0)), *(y_init_pair or (0.0, 0.0)))
            case_evol = max(x_max, y_max)
            max_init = max(max_init, case_init)
            max_evol = max(max_evol, case_evol)
            rows.append({
                "beta0": float(beta),
                "k_h_Mpc": float(kh),
                "k_Mpc^-1": float(k),
                "propagating_X_max_normalized_constraint": float(x_max),
                "nonpropagating_Y_max_normalized_constraint": float(y_max),
                "initial_max_normalized_constraint": float(case_init),
                "evolution_max_normalized_constraint": float(case_evol),
            })

    return {
        "rows": rows,
        "max_initial_normalized_constraint": float(max_init),
        "max_evolution_normalized_constraint": float(max_evol),
        "initial_gate": C_INIT_GATE,
        "evolution_gate": C_EVOL_GATE,
        "pass": bool(max_init <= C_INIT_GATE and max_evol <= C_EVOL_GATE),
        "constraint_projection": "exact algebraic solution of first-class constraints only; no empirical projection",
    }


def run_qs_identity_audit() -> dict:
    chi, rhs = manufactured_fields(NX)
    rows = []
    maxdiff = 0.0
    x_ranges = []

    # Audit duplicated constants before operator comparison.
    const_diffs = {
        "H0": abs(H0 - frozen.H0),
        "K_B": abs(K_B - frozen.KB),
        "K2": abs(K2 - frozen.K2),
        "Q0": abs(Q0 - frozen.Q0),
        "MU2": abs(MU2 - frozen.MU2),
        "ACC_CONV": abs(ACC_CONV - frozen.ACC_CONV),
        "BOX": abs(BOX - frozen.BOX),
    }

    for a in A_VALUES:
        for beta in BETAS:
            for kind in KINDS:
                ir, iop, itilde, iphi, ig, ix, ij, iaeff = independent_state(chi, rhs, a, beta, kind)
                fr, fop, ftilde, fphi, fg, fx, fj = frozen.residual_state(chi, rhs, a, beta, kind)
                _, _, _, _, faeff = frozen.full_operator(chi, a, beta, kind, need_linear_coeff=True)

                metrics = {
                    "operator_rel_L2": rel_l2(iop, fop),
                    "tildePhi_rel_L2": rel_l2(itilde, ftilde),
                    "Phi_rel_L2": rel_l2(iphi, fphi),
                    "residual_rel_L2": rel_l2(ir, fr),
                    "gradient_rel_L2": rel_l2(ig, fg),
                    "x_rel_L2": rel_l2(ix, fx),
                    "j_rel_L2": rel_l2(ij, fj),
                }

                if kind == "sharp":
                    xt = (1.0 + beta) / beta
                    eps = SHARP_KINK_REL_NEIGHBOURHOOD * max(1.0, xt)
                    keep = np.abs(ix - xt) > eps
                    if np.any(keep):
                        metrics["Aeff_rel_L2_away_from_kink"] = rel_l2(iaeff[keep], faeff[keep])
                    else:
                        metrics["Aeff_rel_L2_away_from_kink"] = 0.0
                    metrics["sharp_excluded_grid_points"] = int(np.count_nonzero(~keep))
                    metrics["sharp_kink_x"] = float(xt)
                    metrics["sharp_exclusion_halfwidth"] = float(eps)
                else:
                    metrics["Aeff_rel_L2_away_from_kink"] = rel_l2(iaeff, faeff)

                case_max = max(float(v) for k, v in metrics.items() if "rel_L2" in k)
                maxdiff = max(maxdiff, case_max)
                x_ranges.append((float(np.min(ix)), float(np.median(ix)), float(np.max(ix))))
                rows.append({
                    "a": float(a),
                    "beta0": float(beta),
                    "kind": kind,
                    "x_min": float(np.min(ix)),
                    "x_median": float(np.median(ix)),
                    "x_max": float(np.max(ix)),
                    "max_case_discrepancy": float(case_max),
                    **metrics,
                })

    return {
        "rows": rows,
        "constant_absolute_differences": const_diffs,
        "max_relative_discrepancy": float(maxdiff),
        "gate": D_GATE,
        "sharp_kink_relative_neighbourhood": SHARP_KINK_REL_NEIGHBOURHOOD,
        "manufactured_x_global_min": min(x[0] for x in x_ranges),
        "manufactured_x_global_max": max(x[2] for x in x_ranges),
        "pass": bool(maxdiff <= D_GATE and max(const_diffs.values()) <= 1.0e-15),
    }


def independent_high_gradient(source: np.ndarray, a: float, beta: float):
    source = np.asarray(source, float)
    kk = kgrid(len(source)) / a
    sh = np.fft.fft(source)
    den = (1.0 + beta) * MU2 - kk * kk
    ph = np.zeros(len(source), complex)
    nz = np.abs(kk) > 0.0
    active = nz & (np.abs(sh) > 1.0e-13 * max(float(np.max(np.abs(sh))), 1.0e-300))
    if np.any(np.abs(den[active]) < 1.0e-12 * np.maximum((1.0 + beta) * MU2, kk[active] ** 2)):
        raise RuntimeError("independent high-gradient sourced Helmholtz pole approached")
    ph[active] = sh[active] / den[active]
    phi = np.fft.ifft(ph).real
    phi -= np.mean(phi)
    chi = beta / (1.0 + beta) * phi
    return chi, phi


def run_high_gradient_audit(input_npz: str, input_sha: str) -> dict:
    d = np.load(input_npz)
    kh = np.asarray(d["k_native_h"], float)
    z = np.asarray(d["z_native"], float)
    db = np.asarray(d["d_b"], float)
    idx, kmiss = frozen.mode_indices(kh)
    if db.shape != (kh.size, z.size):
        raise RuntimeError(f"d_b orientation mismatch {db.shape} vs {(kh.size,z.size)}")
    db6 = db[idx, :]
    eval_idx = np.where((z >= frozen.ZMIN - 1.0e-12) & (z <= frozen.ZMAX + 1.0e-12))[0]

    rows = []
    maxerr = 0.0
    for beta in BETAS:
        for it in eval_idx:
            _, source, a = frozen.source_for(db6[:, it], z[it], NX)
            rhs = source / (1.0 + beta)
            ichi, iphi = independent_high_gradient(source, a, beta)
            fchi, fphi = frozen.high_gradient_analytic(source, a, beta)
            sr = frozen.residual_state(ichi, rhs, a, beta, "simple", saturated=True)[0]
            ir = independent_state(ichi, rhs, a, beta, "simple", saturated=True)[0]
            e_chi = rel_l2(ichi, fchi)
            e_phi = rel_l2(iphi, fphi)
            e_sat_frozen = float(np.linalg.norm(sr) / max(float(np.linalg.norm(rhs)), 1.0e-300))
            e_sat_independent = float(np.linalg.norm(ir) / max(float(np.linalg.norm(rhs)), 1.0e-300))
            e_helm = float(np.linalg.norm(lap_phys(iphi, a) + (1.0 + beta) * MU2 * iphi - source) /
                           max(float(np.linalg.norm(source)), 1.0e-300))
            case = max(e_chi, e_phi, e_sat_frozen, e_sat_independent, e_helm)
            maxerr = max(maxerr, case)
            rows.append({
                "beta0": float(beta),
                "index": int(it),
                "z": float(z[it]),
                "a": float(a),
                "chi_independent_vs_frozen_rel_L2": e_chi,
                "Phi_independent_vs_frozen_rel_L2": e_phi,
                "frozen_saturated_relative_residual": e_sat_frozen,
                "independent_saturated_relative_residual": e_sat_independent,
                "independent_Helmholtz_relative_residual": e_helm,
                "max_case_error": case,
            })

    return {
        "rows": rows,
        "input_sha256_declared": input_sha,
        "input_sha256_matches_frozen": bool(input_sha == INPUT_SHA),
        "k_mode_relative_mismatch": float(kmiss),
        "n_evaluation_snapshots": int(len(eval_idx)),
        "max_relative_error": float(maxerr),
        "gate": E_GATE,
        "pass": bool(input_sha == INPUT_SHA and kmiss <= 1.0e-12 and len(eval_idx) >= 8 and maxerr <= E_GATE),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-npz", required=True)
    ap.add_argument("--input-zip-sha256", required=True)
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    head, branch = git_info()
    code_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    print("NL1C6D1CDE_CONSTRAINT_QS_REGRESSION_START", flush=True)
    print(f"git_head={head} branch={branch}", flush=True)
    print(f"code_sha256={code_sha}", flush=True)

    c = run_constraint_audit()
    print(
        f"C_CONSTRAINT max_init={c['max_initial_normalized_constraint']:.12e} "
        f"max_evol={c['max_evolution_normalized_constraint']:.12e} pass={c['pass']}",
        flush=True,
    )

    d = run_qs_identity_audit()
    print(
        f"D_QS_IDENTITY max_rel={d['max_relative_discrepancy']:.12e} "
        f"x_range=[{d['manufactured_x_global_min']:.6e},{d['manufactured_x_global_max']:.6e}] pass={d['pass']}",
        flush=True,
    )

    e = run_high_gradient_audit(args.input_npz, args.input_zip_sha256)
    print(
        f"E_HIGH_GRADIENT max_rel={e['max_relative_error']:.12e} "
        f"snapshots={e['n_evaluation_snapshots']} pass={e['pass']}",
        flush=True,
    )

    classification = CLASS_PASS if c["pass"] and d["pass"] and e["pass"] else CLASS_FAIL
    payload = {
        "label": "NL1C6D1CDE_CONSTRAINT_QS_REGRESSION",
        "classification": classification,
        "full_D1_classified": False,
        "remaining_D1A_nonlinear_time_dependent_reduction_established": False,
        "physical_branch_selection_evaluated": False,
        "nonlinear_source_history_evolved": False,
        "git_head": head,
        "git_branch": branch,
        "code_sha256": code_sha,
        "frozen_gates": {
            "C_initial": C_INIT_GATE,
            "C_evolution": C_EVOL_GATE,
            "D_qs_identity": D_GATE,
            "E_high_gradient": E_GATE,
        },
        "C_constraint_regression": c,
        "D_quasistatic_full_j_identity": d,
        "E_large_gradient_regression": e,
    }

    out = Path(args.json_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"CLASSIFICATION={classification}", flush=True)
    print("FULL_D1_CLASSIFIED=False", flush=True)
    print("D1A_NONLINEAR_DYNAMIC_REDUCTION_ESTABLISHED=False", flush=True)
    print(f"JSON={out}", flush=True)
    print("NL1C6D1CDE_CONSTRAINT_QS_REGRESSION_END", flush=True)
    return 0 if classification == CLASS_PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
