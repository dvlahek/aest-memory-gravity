#!/usr/bin/env python3
"""NL1C6D1A: vector-complete 1D longitudinal weak-field reduction audit.

This is an algebraic/numerical formulation audit. It does not evolve a
nonlinear cosmological source history and does not perform branch selection.
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nl1c6 import full_j_baryonic_reclosure as frozen

KB = 0.0665
K2 = 9500.0
Q0 = 1.0e-4
A = 2.0 - KB
BETAS = (1.0, 0.5, 0.1)
K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
H = 0.673324639084866
K_MPC = K_H * H
NX = 256

CANON_GATE = 1.0e-12
CURL_GATE = 1.0e-14
STATIC_GATE = 1.0e-12
TRACKING_GATE = 1.0e-12

CLASS_PASS = "NL1C6D1A_LONGITUDINAL_WEAKFIELD_REDUCTION_AUDIT_PASS"
CLASS_FAIL = "NL1C6D1A_LONGITUDINAL_WEAKFIELD_REDUCTION_AUDIT_FAIL"


def rel(a, b, floor=1e-300):
    return float(np.linalg.norm(np.asarray(a) - np.asarray(b)) / max(np.linalg.norm(np.asarray(b)), floor))


def git_meta():
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        head, branch = "unknown", "unknown"
    return head, branch


def m_cross():
    return math.sqrt((2.0 - KB) / (2.0 * KB)) * Q0


def canonical_regression():
    rows = []
    worst = 0.0
    for ib, beta in enumerate(BETAS):
        for ik, k in enumerate(K_MPC):
            # Deterministic complex amplitudes exercise both quadratures.
            chi = complex(0.17 + 0.03 * ib, -0.11 + 0.01 * ik)
            chidot = complex(-2.0e-4 * (ik + 1), 1.0e-4 * (ib + 1))
            adot = complex(3.0e-4 * (ib + 1), -1.5e-4 * (ik + 1))
            psi = complex(2.5e-5 * (ik + 1), 1.7e-5 * (ib + 1))
            E = adot + psi
            U = chidot - Q0 * E

            pchi_reduced = 4.0 * K2 * U
            pchi_published = 4.0 * K2 * (chidot - Q0 * (adot + psi))

            palpha_reduced = -4.0 * K2 * Q0 * U + 2.0 * KB * k * k * E + 2.0 * A * k * k * chi
            palpha_published = (
                -4.0 * K2 * Q0 * chidot
                + 2.0 * (KB * k * k + 2.0 * K2 * Q0 * Q0) * (adot + psi)
                + 2.0 * A * k * k * chi
            )
            er_chi = abs(pchi_reduced - pchi_published) / max(abs(pchi_published), 1e-300)
            er_alpha = abs(palpha_reduced - palpha_published) / max(abs(palpha_published), 1e-300)
            e = max(er_chi, er_alpha)
            worst = max(worst, e)
            rows.append({
                "beta0": beta, "k_h_Mpc": float(K_H[ik]), "k_Mpc^-1": float(k),
                "Pchi_relative_error": float(er_chi), "Palpha_relative_error": float(er_alpha),
                "max_case_error": float(e),
            })
    return {"gate": CANON_GATE, "max_relative_error": worst, "pass": bool(worst <= CANON_GATE), "rows": rows}


def curl_regression():
    # Repository geometry: chi=chi(x), U=(d_x chi,0,0). All y,z derivatives vanish.
    n = NX
    x = np.arange(n) * frozen.BOX / n
    chi = 2.0e-7 * np.cos(2.0 * np.pi * 3.0 * x / frozen.BOX + 0.13)
    chi += 7.0e-8 * np.sin(2.0 * np.pi * 8.0 * x / frozen.BOX + 0.71)
    ux = frozen.grad_phys(chi, 1.0)
    uy = np.zeros_like(ux)
    uz = np.zeros_like(ux)

    # In a one-coordinate embedding d_y=d_z=0. Evaluate the component formula explicitly.
    d_x_uy = frozen.grad_phys(uy, 1.0)
    d_x_uz = frozen.grad_phys(uz, 1.0)
    curl_x = np.zeros_like(ux)
    curl_y = -d_x_uz
    curl_z = d_x_uy
    curl_norm = float(np.sqrt(np.mean(curl_x**2 + curl_y**2 + curl_z**2)))

    # Double curl of an identically zero curl is identically zero.
    dc_x = np.zeros_like(ux)
    dc_y = -frozen.grad_phys(curl_z, 1.0)
    dc_z = frozen.grad_phys(curl_y, 1.0)
    dc_norm = float(np.sqrt(np.mean(dc_x**2 + dc_y**2 + dc_z**2)))
    scale = max(float(np.sqrt(np.mean(ux**2 + uy**2 + uz**2))), 1e-300)
    nr = max(curl_norm, dc_norm * frozen.BOX) / scale

    mx = m_cross()
    return {
        "gate": CURL_GATE,
        "m_cross_Mpc^-1": mx,
        "m_cross_inverse_Mpc": 1.0 / mx,
        "k_over_m_cross_min": float(np.min(K_MPC / mx)),
        "k_over_m_cross_max": float(np.max(K_MPC / mx)),
        "normalized_curl_doublecurl_residual": float(nr),
        "pass": bool(nr <= CURL_GATE),
        "interpretation": "finite-m_cross curl sector is exactly inactive for chi(x), U=(d_x chi,0,0)",
    }


def j_independent(x, beta, kind):
    x = np.asarray(x, float)
    b = float(beta)
    aa = 1.0 + b
    if kind == "simple":
        return x / (aa + b * x)
    if kind == "exponential":
        return -np.expm1(-b * x / aa) / b
    if kind == "sharp":
        return np.minimum(x / aa, 1.0 / b)
    raise ValueError(kind)


def spectral_grad(field, a):
    n = len(field)
    kk = 2.0 * np.pi * np.fft.fftfreq(n, d=frozen.BOX / n) / a
    return np.fft.ifft(1j * kk * np.fft.fft(field)).real


def spectral_invlap(src, a):
    n = len(src)
    kk = 2.0 * np.pi * np.fft.fftfreq(n, d=frozen.BOX / n) / a
    sh = np.fft.fft(src)
    out = np.zeros(n, complex)
    nz = np.abs(kk) > 0.0
    out[nz] = -sh[nz] / (kk[nz] ** 2)
    f = np.fft.ifft(out).real
    f -= np.mean(f)
    return f


def static_reduction_regression():
    rows = []
    worst = 0.0
    n = NX
    xx = np.arange(n) * frozen.BOX / n
    a_values = (1.0 / 7.0, 0.5, 1.0)
    kinds = ("simple", "exponential", "sharp")

    # Independent source-coupling identity, setting G_tilde=1 since it cancels.
    coupling_rows = []
    coupling_worst = 0.0
    for beta in BETAS:
        Gtilde = 1.0
        GN = 2.0 * (1.0 + beta) * Gtilde / A
        lhs_coeff = 8.0 * math.pi * Gtilde / A
        rhs_coeff = 4.0 * math.pi * GN / (1.0 + beta)
        e = abs(lhs_coeff - rhs_coeff) / abs(rhs_coeff)
        coupling_worst = max(coupling_worst, e)
        coupling_rows.append({"beta0": beta, "relative_error": float(e)})

    for ia, a in enumerate(a_values):
        chi = (1.5e-7 * (1.0 + 0.2 * ia)) * np.cos(2.0 * np.pi * 3.0 * xx / frozen.BOX + 0.13)
        chi += 6.0e-8 * np.sin(2.0 * np.pi * 8.0 * xx / frozen.BOX + 0.71)
        chi -= np.mean(chi)
        for beta in BETAS:
            for kind in kinds:
                g = spectral_grad(chi, a)
                xdim = frozen.ACC_CONV * np.abs(g)
                j = j_independent(xdim, beta, kind)
                flux = j * g
                op = spectral_grad(flux, a)
                # Match the frozen 2/3 spectral de-aliasing convention.
                mask = frozen.dealias_mask(n)
                kk = 2.0 * np.pi * np.fft.fftfreq(n, d=frozen.BOX / n) / a
                op = np.fft.ifft(1j * kk * (np.fft.fft(flux) * mask)).real
                tilde = spectral_invlap(op, a)
                phi = tilde + chi
                rhs = 3.0e-9 * np.cos(2.0 * np.pi * 5.0 * xx / frozen.BOX + 0.29)
                rhs -= np.mean(rhs)
                r_ind = op + frozen.MU2 * phi - rhs

                r_fr, op_fr, tilde_fr, phi_fr, g_fr, x_fr, j_fr = frozen.residual_state(chi, rhs, a, beta, kind)
                errs = {
                    "gradient": rel(g, g_fr), "x": rel(xdim, x_fr), "j": rel(j, j_fr),
                    "operator": rel(op, op_fr), "tildePhi": rel(tilde, tilde_fr),
                    "Phi": rel(phi, phi_fr), "residual": rel(r_ind, r_fr),
                }
                e = max(errs.values())
                worst = max(worst, e)
                rows.append({
                    "a": a, "beta0": beta, "kind": kind, "max_case_error": float(e),
                    **{f"{q}_relative_error": float(v) for q, v in errs.items()},
                })

    total_worst = max(worst, coupling_worst)
    return {
        "gate": STATIC_GATE,
        "max_relative_error": float(total_worst),
        "operator_max_relative_error": float(worst),
        "source_coupling_max_relative_error": float(coupling_worst),
        "pass": bool(total_worst <= STATIC_GATE),
        "source_coupling_rows": coupling_rows,
        "rows": rows,
    }


def tracking_regression():
    rows = []
    worst = 0.0
    for beta in BETAS:
        lam = 1.0 / beta
        cs2 = A / (K2 * KB) * (1.0 + 0.5 * KB * lam)
        mass2 = A * (1.0 + lam) * Q0 * Q0 / KB
        for kh, k in zip(K_H, K_MPC):
            omega2 = cs2 * k * k + mass2
            omega = math.sqrt(omega2)

            # Nonzero-frequency vacuum sector after the exact scalar constraints:
            # variables are v=i*omega*alpha and chi. The determinant must vanish.
            a11 = 2.0 * K2 * Q0 * Q0 + KB * k * k
            a12 = A * k * k - 2.0j * K2 * Q0 * omega
            a21 = -A * k * k - 2.0j * K2 * Q0 * omega
            a22 = A * (1.0 + lam) * k * k - 2.0 * K2 * omega2
            det = a11 * a22 - a12 * a21
            scale = max(abs(a11 * a22), abs(a12 * a21), 1e-300)
            det_rel = abs(det) / scale

            # Independently solve the determinant coefficient for omega^2.
            omega2_from_det = (
                A * (1.0 + lam) * Q0 * Q0 / KB
                + A * (2.0 + KB * lam) * k * k / (2.0 * K2 * KB)
            )
            coeff_rel = abs(omega2_from_det - omega2) / max(abs(omega2), 1e-300)
            e = max(det_rel, coeff_rel)
            worst = max(worst, e)
            rows.append({
                "beta0": beta, "lambda_s": lam, "k_h_Mpc": float(kh), "k_Mpc^-1": float(k),
                "omega_squared_reference": float(omega2), "omega_squared_from_determinant": float(omega2_from_det),
                "determinant_normalized_residual": float(det_rel), "coefficient_relative_error": float(coeff_rel),
                "max_case_error": float(e),
            })
    return {"gate": TRACKING_GATE, "max_relative_error": float(worst), "pass": bool(worst <= TRACKING_GATE), "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    head, branch = git_meta()
    code_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    print("NL1C6D1A_LONGITUDINAL_WEAKFIELD_REDUCTION_AUDIT_START", flush=True)
    print(f"git_head={head} branch={branch}", flush=True)
    print(f"code_sha256={code_sha}", flush=True)

    canon = canonical_regression()
    print(f"A_CANONICAL max_rel={canon['max_relative_error']:.12e} pass={canon['pass']}", flush=True)
    curl = curl_regression()
    print(
        f"A_VECTOR_1D m_cross={curl['m_cross_Mpc^-1']:.12e} Mpc^-1 "
        f"curl_rel={curl['normalized_curl_doublecurl_residual']:.12e} pass={curl['pass']}", flush=True,
    )
    static = static_reduction_regression()
    print(f"A_STATIC_FULLJ max_rel={static['max_relative_error']:.12e} pass={static['pass']}", flush=True)
    track = tracking_regression()
    print(f"A_TRACKING_DISPERSION max_rel={track['max_relative_error']:.12e} pass={track['pass']}", flush=True)

    ok = canon["pass"] and curl["pass"] and static["pass"] and track["pass"]
    classification = CLASS_PASS if ok else CLASS_FAIL
    payload = {
        "label": "NL1C6D1A_LONGITUDINAL_WEAKFIELD_REDUCTION_AUDIT",
        "classification": classification,
        "git_head": head,
        "git_branch": branch,
        "code_sha256": code_sha,
        "physical_branch_selection_evaluated": False,
        "nonlinear_cosmological_source_history_evolved": False,
        "ad_hoc_relaxation_added": False,
        "geometry": "1D periodic longitudinal weak-field",
        "reduced_variables": {
            "E": "dot(alpha)+Psi",
            "U": "dot(chi)-Q0*E",
            "Y": "|grad chi|^2",
            "P_Phi": "-12 dot(Phi)",
            "P_chi": "4 K2 U",
            "P_alpha": "-4 K2 Q0 U - 2 K_B lap(E) - 2(2-K_B) lap(chi)",
            "Psi_constraint": "4 lap(Phi)+P_alpha-16 pi G_tilde rho_b=0",
        },
        "gates": {
            "canonical_published_identity": bool(canon["pass"]),
            "one_dimensional_vector_completeness": bool(curl["pass"]),
            "static_full_j_reduction": bool(static["pass"]),
            "tracking_dispersion_identity": bool(track["pass"]),
        },
        "canonical_regression": canon,
        "vector_curl_regression": curl,
        "static_full_j_regression": static,
        "tracking_regression": track,
        "scope_note": (
            "PASS establishes the gravitational longitudinal weak-field reduction for the repository 1D geometry. "
            "A time-varying baryonic density requires a separately preregistered constraint-consistent matter momentum/continuity sector in D2."
        ),
    }
    out = Path(args.json_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"CLASSIFICATION={classification}", flush=True)
    print("D2_MATTER_SECTOR_ESTABLISHED=False", flush=True)
    print(f"JSON={out}", flush=True)
    print("NL1C6D1A_LONGITUDINAL_WEAKFIELD_REDUCTION_AUDIT_END", flush=True)
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
