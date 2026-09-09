#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "v019/patch/source/aest_memory.c"

KB = 0.0665
K2 = 9500.0
Q0 = 1.0e-4
Z0 = 1.0e-17
H0_KM_S_MPC = 67.3324639084866
OMEGA_CDM = 0.12006705327635288
C_KM_S = 299792.458

Z_SMALL = (1e-1, 3e-2, 1e-2, 3e-3, 1e-3)
Z_DERIV = (-4.0, -2.0, -1.0, -0.1, 0.1, 1.0, 2.0, 4.0)
Z_INV = (0.1, 1.0, 2.0, 4.0)
A_GRID = (1.0, 0.8, 0.5, 0.3, 0.2, 1.0 / 7.0)

N1_GATE = 1e-14
N2_GATE = 1e-6
N3_KQ_GATE = 2e-7
N3_KQQ_GATE = 2e-5
N3_PARITY_GATE = 1e-14
N4_GATE = 1e-12
N5_GATE = 1e-12
N6_GATE = 1e-15

CLASS_PASS = "NL1C6D2N_EXP_NORMALIZATION_AUDIT_PASS"
CLASS_FAIL = "NL1C6D2N_EXP_NORMALIZATION_AUDIT_FAIL"


def git_meta():
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        head, branch = "unknown", "unknown"
    return head, branch


def exp_eval(z: float):
    zz = z * z
    ex = math.exp(zz)
    K = K2 * Z0 * Z0 * math.expm1(zz)
    KQ = 2.0 * K2 * Z0 * z * ex
    KQQ = 2.0 * K2 * ex * (1.0 + 2.0 * zz)
    Q = Q0 + Z0 * z
    return Q, K, KQ, KQQ


def cosh_eval(z: float):
    K = 2.0 * K2 * Z0 * Z0 * (math.cosh(z) - 1.0)
    KQ = 2.0 * K2 * Z0 * math.sinh(z)
    KQQ = 2.0 * K2 * math.cosh(z)
    Q = Q0 + Z0 * z
    return Q, K, KQ, KQQ


def exp_inverse_positive(x: float):
    if not x > 0.0:
        raise ValueError("positive branch only")
    L = math.log(x)
    y = x * x if x < 1e-4 else (L if L > 1.0 else x * x)
    y = max(y, 1e-30)
    for _ in range(50):
        f = y + 0.5 * math.log(y) - L
        fp = 1.0 + 0.5 / y
        yn = y - f / fp
        if not (yn > 0.0 and math.isfinite(yn)):
            yn = 0.5 * y
        if abs(yn - y) < 2e-14 * (1.0 + y):
            y = yn
            break
        y = yn
    return math.sqrt(y)


def calibrate(target: float):
    lo, hi = 0.0, 1.0

    def f(z):
        q, k, kq, _ = exp_eval(z)
        return q * kq - k - target

    if not f(lo) < 0.0:
        raise RuntimeError("calibration lower bracket invalid")
    while f(hi) <= 0.0:
        hi *= 2.0
        if hi > 128.0:
            raise RuntimeError("calibration upper bracket failed")
    for _ in range(180):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    z = 0.5 * (lo + hi)
    q, k, kq, kqq = exp_eval(z)
    return z, q, k, kq, kqq


def n1_local_curvature():
    q, k, kq, kqq = exp_eval(0.0)
    curvature_ratio = kqq / (2.0 * K2)
    mu_ref = 2.0 * K2 * Q0 * Q0 / (2.0 - KB)
    mu_from_curvature = kqq * Q0 * Q0 / (2.0 - KB)
    errs = {
        "K_abs_scaled": abs(k) / max(K2 * Z0 * Z0, 1e-300),
        "KQ_abs_scaled": abs(kq) / max(K2 * Z0, 1e-300),
        "KQQ_ratio_error": abs(curvature_ratio - 1.0),
        "mu2_relative_error": abs(mu_from_curvature - mu_ref) / mu_ref,
    }
    worst = max(errs.values())
    return {
        "K_at_Z0": k,
        "KQ_at_Z0": kq,
        "KQQ_at_Z0": kqq,
        "KQQ_over_2K2": curvature_ratio,
        "mu2_reference_Mpc^-2": mu_ref,
        "mu2_from_curvature_Mpc^-2": mu_from_curvature,
        "errors": errs,
        "gate": N1_GATE,
        "max_normalized_error": worst,
        "pass": bool(worst <= N1_GATE),
    }


def n2_small_z():
    rows = {"positive": [], "negative": []}
    endpoints = []
    monotone_all = True
    for sign_name, sign in (("positive", 1.0), ("negative", -1.0)):
        vals = []
        for za in Z_SMALL:
            z = sign * za
            _, k, _, _ = exp_eval(z)
            ref = K2 * (Z0 * z) ** 2
            r = k / ref - 1.0
            vals.append(abs(r))
            rows[sign_name].append({"Z": z, "relative_quadratic_error": r})
        monotone = all(vals[i + 1] <= vals[i] for i in range(len(vals) - 1))
        monotone_all = monotone_all and monotone
        endpoints.append(vals[-1])
    endpoint = max(endpoints)
    return {
        "rows": rows,
        "monotone_to_zero_both_signs": bool(monotone_all),
        "endpoint_abs_error_Z1e-3": endpoint,
        "gate": N2_GATE,
        "pass": bool(monotone_all and endpoint <= N2_GATE),
    }


def n3_derivatives_and_parity():
    h = 1e-4
    rows = []
    worst_q = 0.0
    worst_qq = 0.0
    for z in Z_DERIV:
        fm2 = exp_eval(z - 2 * h)[1]
        fm1 = exp_eval(z - h)[1]
        f0 = exp_eval(z)[1]
        fp1 = exp_eval(z + h)[1]
        fp2 = exp_eval(z + 2 * h)[1]
        dK_dz = (fm2 - 8 * fm1 + 8 * fp1 - fp2) / (12 * h)
        d2K_dz2 = (-fp2 + 16 * fp1 - 30 * f0 + 16 * fm1 - fm2) / (12 * h * h)
        kq_num = dK_dz / Z0
        kqq_num = d2K_dz2 / (Z0 * Z0)
        _, _, kq, kqq = exp_eval(z)
        eq = abs(kq_num - kq) / max(abs(kq), 1e-300)
        eqq = abs(kqq_num - kqq) / max(abs(kqq), 1e-300)
        worst_q = max(worst_q, eq)
        worst_qq = max(worst_qq, eqq)
        rows.append({"Z": z, "KQ_relative_error": eq, "KQQ_relative_error": eqq})

    parity_rows = []
    parity_worst = 0.0
    for z in (0.1, 1.0, 2.0, 4.0):
        _, kp, kqp, kqqp = exp_eval(z)
        _, km, kqm, kqqm = exp_eval(-z)
        errs = {
            "K_even": abs(km - kp) / max(abs(kp), 1e-300),
            "KQ_odd": abs(kqm + kqp) / max(abs(kqp), 1e-300),
            "KQQ_even": abs(kqqm - kqqp) / max(abs(kqqp), 1e-300),
        }
        e = max(errs.values())
        parity_worst = max(parity_worst, e)
        parity_rows.append({"abs_Z": z, **errs})
    return {
        "finite_difference_step_Z": h,
        "rows": rows,
        "max_KQ_relative_error": worst_q,
        "max_KQQ_relative_error": worst_qq,
        "KQ_gate": N3_KQ_GATE,
        "KQQ_gate": N3_KQQ_GATE,
        "parity_rows": parity_rows,
        "max_parity_error": parity_worst,
        "parity_gate": N3_PARITY_GATE,
        "pass": bool(worst_q <= N3_KQ_GATE and worst_qq <= N3_KQQ_GATE and parity_worst <= N3_PARITY_GATE),
    }


def n4_inverse():
    rows = []
    worst = 0.0
    for z in Z_INV:
        _, _, kq, _ = exp_eval(z)
        x = kq / (2.0 * K2 * Z0)
        zr = exp_inverse_positive(x)
        e = abs(zr - z) / max(1.0, abs(z))
        worst = max(worst, e)
        rows.append({"Z": z, "x": x, "Z_recovered": zr, "normalized_error": e})
    return {"rows": rows, "max_normalized_error": worst, "gate": N4_GATE, "pass": bool(worst <= N4_GATE)}


def n5_background():
    h = H0_KM_S_MPC / 100.0
    Omega_cdm = OMEGA_CDM / (h * h)
    H0_mpc = H0_KM_S_MPC / C_KM_S
    target = 3.0 * Omega_cdm * H0_mpc * H0_mpc
    z1, q1, k1, I0, _ = calibrate(target)
    rho8 = q1 * I0 - k1
    target_err = abs(rho8 - target) / target
    rows = []
    worst_charge = 0.0
    for a in A_GRID:
        requested_kq = I0 / (a ** 3)
        x = requested_kq / (2.0 * K2 * Z0)
        z = exp_inverse_positive(x)
        q, k, returned_kq, kqq = exp_eval(z)
        e = abs(returned_kq - requested_kq) / requested_kq
        worst_charge = max(worst_charge, e)
        rho = (q * returned_kq - k) / 3.0
        p = k / 3.0
        cad2 = returned_kq / (q * kqq)
        rows.append({
            "a": a, "Z": z, "KQ_requested": requested_kq, "KQ_returned": returned_kq,
            "charge_relative_error": e, "rho_class": rho, "p_class": p, "cad2": cad2,
        })
    worst = max(target_err, worst_charge)
    return {
        "target_rho8": target,
        "calibrated_Z_a1": z1,
        "I0": I0,
        "a1_target_relative_error": target_err,
        "rows": rows,
        "max_charge_relative_error": worst_charge,
        "gate": N5_GATE,
        "max_normalized_error": worst,
        "pass": bool(worst <= N5_GATE),
    }


def n6_source_and_cosh():
    text = SOURCE.read_text()
    required_exp = (
        "k=K2*Z0*Z0*(ex-1.);",
        "kq=2.*K2*Z0*Z*ex;",
        "kqq=2.*K2*ex*(1.+2.*zz);",
        "double x=kq/(2.*K2*Z0);",
    )
    forbidden_exp = (
        "k=2.*K2*Z0*Z0*(ex-1.);",
        "kq=4.*K2*Z0*Z*ex;",
        "kqq=4.*K2*ex*(1.+2.*zz);",
        "double x=kq/(4.*K2*Z0);",
    )
    required_cosh = (
        "k=2.*K2*Z0*Z0*(ch-1.);",
        "kq=2.*K2*Z0*sh;",
        "kqq=2.*K2*ch;",
    )
    source_ok = all(s in text for s in required_exp + required_cosh) and all(s not in text for s in forbidden_exp)

    numerical_rows = []
    worst = 0.0
    for z in Z_DERIV:
        _, k, kq, kqq = cosh_eval(z)
        k_ref = 2.0 * K2 * Z0 * Z0 * (math.cosh(z) - 1.0)
        kq_ref = 2.0 * K2 * Z0 * math.sinh(z)
        kqq_ref = 2.0 * K2 * math.cosh(z)
        errs = (
            abs(k - k_ref) / max(abs(k_ref), 1e-300),
            abs(kq - kq_ref) / max(abs(kq_ref), 1e-300),
            abs(kqq - kqq_ref) / max(abs(kqq_ref), 1e-300),
        )
        e = max(errs)
        worst = max(worst, e)
        numerical_rows.append({"Z": z, "max_relative_error": e})
    return {
        "required_corrected_source_snippets_present": source_ok,
        "max_cosh_numerical_error": worst,
        "gate": N6_GATE,
        "rows": numerical_rows,
        "pass": bool(source_ok and worst <= N6_GATE),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    head, branch = git_meta()
    source_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    print("NL1C6D2N_EXP_NORMALIZATION_AUDIT_START", flush=True)
    print(f"git_head={head} branch={branch}", flush=True)
    print(f"source_sha256={source_sha}", flush=True)

    n1 = n1_local_curvature()
    n2 = n2_small_z()
    n3 = n3_derivatives_and_parity()
    n4 = n4_inverse()
    n5 = n5_background()
    n6 = n6_source_and_cosh()

    print(f"N1 max={n1['max_normalized_error']:.12e} pass={n1['pass']}", flush=True)
    print(f"N2 endpoint={n2['endpoint_abs_error_Z1e-3']:.12e} monotone={n2['monotone_to_zero_both_signs']} pass={n2['pass']}", flush=True)
    print(f"N3 KQ={n3['max_KQ_relative_error']:.12e} KQQ={n3['max_KQQ_relative_error']:.12e} parity={n3['max_parity_error']:.12e} pass={n3['pass']}", flush=True)
    print(f"N4 max={n4['max_normalized_error']:.12e} pass={n4['pass']}", flush=True)
    print(f"N5 max={n5['max_normalized_error']:.12e} pass={n5['pass']}", flush=True)
    print(f"N6 cosh={n6['max_cosh_numerical_error']:.12e} source_ok={n6['required_corrected_source_snippets_present']} pass={n6['pass']}", flush=True)

    gates = {
        "N1_local_curvature": n1["pass"],
        "N2_quadratic_small_Z": n2["pass"],
        "N3_derivative_consistency": n3["pass"],
        "N4_forward_inverse_consistency": n4["pass"],
        "N5_background_charge_law": n5["pass"],
        "N6_cosh_non_regression": n6["pass"],
    }
    passed = bool(all(gates.values()))
    classification = CLASS_PASS if passed else CLASS_FAIL
    payload = {
        "classification": classification,
        "git": {"head": head, "branch": branch},
        "source_sha256": source_sha,
        "constants": {
            "K_B": KB, "K2": K2, "Q0_Mpc^-1": Q0, "Z0_Mpc^-1": Z0,
            "H0_km_s_Mpc": H0_KM_S_MPC, "omega_cdm": OMEGA_CDM,
        },
        "corrected_exp": {
            "K": "K2*Z0^2*(exp(Z^2)-1)",
            "KQ": "2*K2*Z0*Z*exp(Z^2)",
            "KQQ": "2*K2*exp(Z^2)*(1+2*Z^2)",
            "inverse_x": "KQ/(2*K2*Z0)",
        },
        "N1": n1, "N2": n2, "N3": n3, "N4": n4, "N5": n5, "N6": n6,
        "gates": gates,
        "historical_v053_results_unchanged": True,
        "corrected_CLASS_cosmological_trajectory_evaluated": False,
        "nonlinear_branch_selection_performed": False,
        "NL1C7_authorized": False,
    }
    Path(args.json_out).write_text(json.dumps(payload, indent=2) + "\n")
    print(f"CLASSIFICATION={classification}", flush=True)
    raise SystemExit(0 if passed else 2)


if __name__ == "__main__":
    main()
