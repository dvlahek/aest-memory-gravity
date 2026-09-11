#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import LinearOperator, gmres

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nl1c6 import full_j_baryonic_reclosure as base

# Frozen PoC grid from docs/fullj_cosmological_reclosure_poc_predata.md
CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"
ZS = np.asarray([1.0, 0.5], dtype=float)
K_MPC = np.asarray([0.04, 0.10, 0.20, 0.40, 0.80, 1.20], dtype=float)
KFUND = 0.02
MODE_NUM = np.asarray([2, 5, 10, 20, 40, 60], dtype=int)
PHASE = np.asarray([0.13, 0.71, 1.29, 2.03, 2.77, 3.41], dtype=float)
NX = 256
BETAS = (1.0, 0.5, 0.1)
KINDS = ("simple", "exponential", "sharp")
MAX_STEP = 1.0 / 16.0
MIN_STEP = 1.0 / 4096.0
NEWTON_MAX = 80
NEWTON_TOL = 2.0e-10
R2_GATE = 1.0e-8
R1_GATE = 1.0e-10
SAT_GATE = 1.0e-10

START = dict(
    H0=67.3324639084866,
    omega_b=0.022377376877682164,
    omega_cdm=0.12006705327635288,
    tau_reio=0.06174082364515668,
    n_s=0.9666229454895277,
    A_s=2.1308864352626987e-9,
)


def rel_l2(a, b):
    a = np.asarray(a)
    b = np.asarray(b)
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(b), 1e-300))


def configure_periodic_grid():
    # Reuse the already-audited NL1C6 physical operator with only the frozen
    # PoC mode grid / box changed. Physics constants remain exactly NL1C6.
    base.K_MPC = K_MPC.copy()
    base.K_H = K_MPC / base.h
    base.MODE_NUM = MODE_NUM.copy()
    base.PHASE = PHASE.copy()
    base.BOX = 2.0 * np.pi / KFUND
    base.WIDTH = base.weights_log(K_MPC)
    base.PR = base.AS * (K_MPC / base.KPIV) ** (base.NS - 1.0)
    base.MODE_AMP = np.sqrt(2.0 * base.WIDTH * base.PR)

    # Exact-periodicity and 2/3 de-alias checks.
    inferred = np.rint(K_MPC / KFUND).astype(int)
    if not np.array_equal(inferred, MODE_NUM):
        raise RuntimeError(f"mode-number identity failed: {inferred} vs {MODE_NUM}")
    if int(MODE_NUM.max()) > int(np.floor(NX / 3.0)):
        raise RuntimeError("source mode exceeds 2/3 de-alias cutoff")


def class_parameters():
    p = {
        **START,
        "N_ur": 2.046,
        "N_ncdm": 1,
        "m_ncdm": 0.06,
        "T_ncdm": 0.7137658555036082,
        "YHe": 0.2454006,
        "gauge": "newtonian",
        "aest_enabled": "yes",
        "aest_model": "Exp",
        "aest_KB": 0.0665,
        "aest_Q0": 1.0e-4,
        "aest_K2": 9500.0,
        "aest_Z0": 1.0e-17,
        "aest_memory_enabled": "no",
        "aest_memory_order": 39,
        "aest_eta": 0.0,
        "aest_tau_H0": 1.0,
        "output": "mTk",
        "P_k_max_1/Mpc": 1.6,
        "z_pk": ",".join(f"{z:.17g}" for z in ZS),
    }
    return p


def extract_baryon_transfers():
    try:
        from classy import Class
        import classy
    except Exception as exc:
        raise RuntimeError(f"classy import failed: {exc}") from exc

    c = Class()
    params = class_parameters()
    c.set(params)
    c.compute()
    rows = []
    try:
        for z in ZS:
            tr = c.get_transfer(float(z))
            keys = list(tr.keys())
            if "d_b" not in tr:
                raise RuntimeError(f"CLASS transfer has no d_b; keys={keys}")
            if "k (h/Mpc)" in tr:
                knative = np.asarray(tr["k (h/Mpc)"], float) * base.h
                k_units = "h/Mpc"
            elif "k (1/Mpc)" in tr:
                knative = np.asarray(tr["k (1/Mpc)"], float)
                k_units = "1/Mpc"
            else:
                k_candidates = [k for k in keys if k.lower().startswith("k")]
                raise RuntimeError(f"CLASS transfer k key not recognized; candidates={k_candidates}")
            dbnative = np.asarray(tr["d_b"], float)
            good = np.isfinite(knative) & np.isfinite(dbnative) & (knative > 0)
            knative, dbnative = knative[good], dbnative[good]
            order = np.argsort(knative)
            knative, dbnative = knative[order], dbnative[order]
            if len(knative) < 2:
                raise RuntimeError(f"insufficient native transfer points at z={z}")
            if K_MPC.min() < knative.min() or K_MPC.max() > knative.max():
                raise RuntimeError(
                    f"transfer extrapolation forbidden at z={z}: native=[{knative.min()},{knative.max()}], "
                    f"requested=[{K_MPC.min()},{K_MPC.max()}]"
                )
            db = np.interp(np.log(K_MPC), np.log(knative), dbnative)
            if not np.all(np.isfinite(db)):
                raise RuntimeError(f"nonfinite interpolated d_b at z={z}")
            rows.append({
                "z": float(z),
                "d_b": db,
                "native_k_min_Mpc": float(knative.min()),
                "native_k_max_Mpc": float(knative.max()),
                "native_n": int(knative.size),
                "native_k_key_units": k_units,
                "transfer_keys": keys,
            })
    finally:
        try:
            c.struct_cleanup()
            c.empty()
        except Exception:
            pass
    return rows, str(getattr(classy, "__file__", ""))


def blend_operator(chi, a, beta, kind, lam, need_linear_coeff=False):
    n = len(chi)
    kk = base.kgrid(n) / a
    mask = base.dealias_mask(n)
    gh = np.fft.fft(chi)
    g = np.fft.ifft(1j * kk * gh).real
    x = base.ACC_CONV * np.abs(g)
    jf, jp = base.j_and_prime(x, beta, kind, saturated=False)
    j0 = 1.0 / beta
    jb = (1.0 - lam) * j0 + lam * jf
    flux = jb * g
    op = np.fft.ifft(1j * kk * (np.fft.fft(flux) * mask)).real
    if need_linear_coeff:
        aeff = (1.0 - lam) * j0 + lam * (jf + x * jp)
        return op, g, x, jb, aeff
    return op, g, x, jb


def blend_residual_state(chi, rhs, a, beta, kind, lam):
    op, g, x, j = blend_operator(chi, a, beta, kind, lam)
    tilde = base.invlap_phys(op, a)
    phi = tilde + chi
    r = op + base.MU2 * phi - rhs
    return r, op, tilde, phi, g, x, j


def blend_preconditioner(chi, a, beta, kind, lam):
    n = len(chi)
    kk = base.kgrid(n) / a
    _, _, _, _, aeff = blend_operator(chi, a, beta, kind, lam, need_linear_coeff=True)
    abar = max(float(np.mean(aeff)), 1e-12)
    diag = -abar * kk * kk + base.MU2 * (1.0 + abar)
    diag[0] = base.MU2
    scale = np.maximum(np.abs(-abar * kk * kk) + base.MU2 * (1.0 + abar), base.MU2)
    tiny = np.abs(diag) < 1e-8 * scale
    diag[tiny] = np.where(diag[tiny] >= 0, 1.0, -1.0) * 1e-8 * scale[tiny]

    def mv(v):
        vh = np.fft.fft(np.asarray(v, float))
        return np.fft.ifft(vh / diag).real

    return LinearOperator((n, n), matvec=mv, dtype=float)


def newton_blend(rhs, a, beta, kind, lam, initial):
    rhs = np.asarray(rhs, float).copy()
    rhs -= np.mean(rhs)
    chi = np.asarray(initial, float).copy()
    chi -= np.mean(chi)
    scale = max(float(np.linalg.norm(rhs)), 1e-300)
    history = []
    accepted_alpha = []

    for it in range(NEWTON_MAX + 1):
        r, op, tilde, phi, g, x, j = blend_residual_state(chi, rhs, a, beta, kind, lam)
        rel = float(np.linalg.norm(r) / scale)
        history.append(rel)
        if not np.isfinite(rel):
            return {"success": False, "reason": "nonfinite_residual", "chi": chi,
                    "iterations": it, "history": history, "accepted_alpha": accepted_alpha}
        if rel <= NEWTON_TOL:
            return {"success": True, "reason": "converged", "chi": chi,
                    "iterations": it, "history": history, "accepted_alpha": accepted_alpha}
        if it == NEWTON_MAX:
            break

        _, _, _, _, aeff = blend_operator(chi, a, beta, kind, lam, need_linear_coeff=True)
        n = len(chi)
        kk = base.kgrid(n) / a
        mask = base.dealias_mask(n)

        def jmv(v):
            v = np.asarray(v, float)
            vg = np.fft.ifft(1j * kk * np.fft.fft(v)).real
            dop = np.fft.ifft(1j * kk * (np.fft.fft(aeff * vg) * mask)).real
            dtilde = base.invlap_phys(dop, a)
            return dop + base.MU2 * (dtilde + v)

        J = LinearOperator((n, n), matvec=jmv, dtype=float)
        M = blend_preconditioner(chi, a, beta, kind, lam)
        delta, info = gmres(J, -r, M=M, rtol=1e-8, atol=0.0,
                            restart=min(80, n), maxiter=360)
        if not np.all(np.isfinite(delta)):
            return {"success": False, "reason": "nonfinite_newton_step", "chi": chi,
                    "iterations": it, "history": history, "accepted_alpha": accepted_alpha}

        norm0 = float(np.linalg.norm(r))
        accepted = False
        for m in range(46):
            alpha = 2.0 ** (-m)
            cand = chi + alpha * delta
            cand -= np.mean(cand)
            rc = blend_residual_state(cand, rhs, a, beta, kind, lam)[0]
            if np.all(np.isfinite(rc)) and float(np.linalg.norm(rc)) < norm0:
                chi = cand
                accepted_alpha.append(float(alpha))
                accepted = True
                break
        if not accepted:
            return {"success": False, "reason": f"line_search_failed_gmres_{info}", "chi": chi,
                    "iterations": it, "history": history, "accepted_alpha": accepted_alpha}

    return {"success": False, "reason": "max_iterations", "chi": chi,
            "iterations": NEWTON_MAX, "history": history, "accepted_alpha": accepted_alpha}


def constitutive_continue(source, a, beta, kind):
    rhs = np.asarray(source, float) / (1.0 + beta)
    chi_hg, phi_hg = base.high_gradient_analytic(source, a, beta)
    r0, _, _, phi0, _, _, _ = blend_residual_state(chi_hg, rhs, a, beta, kind, 0.0)
    sat_res = float(np.linalg.norm(r0) / max(np.linalg.norm(rhs), 1e-300))
    sat_phi = rel_l2(phi0, phi_hg)
    sat_pass = sat_res <= SAT_GATE and sat_phi <= SAT_GATE
    if not sat_pass:
        return {
            "success": False,
            "reason": "saturated_control_failed",
            "chi": chi_hg,
            "phi_hg": phi_hg,
            "rhs": rhs,
            "saturated_residual": sat_res,
            "saturated_phi_rel_l2": sat_phi,
            "continuation": [],
        }

    lam = 0.0
    step = MAX_STEP
    chi = chi_hg.copy()
    steps = []
    attempts = 0
    while lam < 1.0 - 1e-14:
        target = min(1.0, lam + step)
        sol = newton_blend(rhs, a, beta, kind, target, chi)
        attempts += 1
        rec = {
            "from_lambda": float(lam),
            "to_lambda": float(target),
            "step": float(step),
            "success": bool(sol["success"]),
            "reason": sol["reason"],
            "iterations": int(sol["iterations"]),
            "final_relative_residual": float(sol["history"][-1]),
        }
        steps.append(rec)
        if sol["success"]:
            lam = target
            chi = sol["chi"].copy()
            step = min(MAX_STEP, 2.0 * step)
        else:
            step *= 0.5
            if step < MIN_STEP - 1e-16:
                return {
                    "success": False,
                    "reason": "constitutive_continuation_min_step_failed",
                    "failed_lambda": float(target),
                    "last_lambda": float(lam),
                    "chi": chi,
                    "phi_hg": phi_hg,
                    "rhs": rhs,
                    "saturated_residual": sat_res,
                    "saturated_phi_rel_l2": sat_phi,
                    "continuation": steps,
                    "attempts": attempts,
                }
        if attempts > 5000:
            return {
                "success": False,
                "reason": "constitutive_continuation_attempt_limit",
                "last_lambda": float(lam),
                "chi": chi,
                "phi_hg": phi_hg,
                "rhs": rhs,
                "saturated_residual": sat_res,
                "saturated_phi_rel_l2": sat_phi,
                "continuation": steps,
                "attempts": attempts,
            }

    return {
        "success": True,
        "reason": "lambda_1_reached",
        "chi": chi,
        "phi_hg": phi_hg,
        "rhs": rhs,
        "saturated_residual": sat_res,
        "saturated_phi_rel_l2": sat_phi,
        "continuation": steps,
        "attempts": attempts,
    }


def mode_response(phi, phi_hg, rhs, a):
    n = len(phi)
    cf = np.fft.fft(phi) / n
    ch = np.fft.fft(phi_hg) / n
    cr = np.fft.fft(rhs) / n
    rows = []
    for k, m in zip(K_MPC, MODE_NUM):
        den = abs(cr[int(m)])
        if den <= 1e-300:
            raise RuntimeError(f"zero rhs Fourier coefficient at source mode m={m}")
        tphi = float(abs(cf[int(m)]) / den)
        gphi = float((k / a) ** 2 * tphi)
        ratio_hg = float(abs(cf[int(m)]) / max(abs(ch[int(m)]), 1e-300))
        rows.append({
            "k_Mpc": float(k),
            "mode": int(m),
            "T_phi_Mpc2": tphi,
            "G_phi": gphi,
            "abs_phi_over_abs_phi_saturated": ratio_hg,
            "abs_phi_mode": float(abs(cf[int(m)])),
            "abs_rhs_mode": float(den),
        })
    high = [r for r in rows if r["k_Mpc"] >= 0.4 - 1e-12]
    kval = np.asarray([r["k_Mpc"] for r in high], float)
    tval = np.asarray([r["T_phi_Mpc2"] for r in high], float)
    slope = float(np.polyfit(np.log(kval), np.log(np.maximum(tval, 1e-300)), 1)[0])
    mono = bool(tval[0] > tval[1] > tval[2])
    return rows, slope, mono


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_cosmological_reclosure_poc.json")
    ap.add_argument("--npz-out", default="results/fullj_cosmological_reclosure_poc.npz")
    args = ap.parse_args()
    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    configure_periodic_grid()
    print("FULLJ_POC_START", flush=True)
    print("K_MPC=" + ",".join(f"{x:.6g}" for x in K_MPC), flush=True)
    print("Z=" + ",".join(f"{x:.6g}" for x in ZS), flush=True)
    print("BRANCHES=9 co-primary", flush=True)
    print("NX=256 kfund=0.02_Mpc^-1", flush=True)

    try:
        transfers, classy_module = extract_baryon_transfers()
        print("FULLJ_POC_CLASS_TRANSFER_READY classy=" + classy_module, flush=True)
        for tr in transfers:
            print(
                f"FULLJ_POC_DB z={tr['z']:.6g} nativeN={tr['native_n']} "
                f"nativeK=[{tr['native_k_min_Mpc']:.6e},{tr['native_k_max_Mpc']:.6e}] "
                + " d_b=" + ",".join(f"{x:.6e}" for x in tr["d_b"]),
                flush=True,
            )

        records = []
        field_phi = []
        field_chi = []
        field_keys = []
        any_fail = False

        for tr in transfers:
            z = float(tr["z"])
            db = np.asarray(tr["d_b"], float)
            delta, source, a = base.source_for(db, z, NX)
            print(f"FULLJ_POC_SNAPSHOT z={z:.6g} a={a:.12e} delta_rms={np.sqrt(np.mean(delta*delta)):.12e}", flush=True)

            for kind in KINDS:
                for beta in BETAS:
                    label = f"z{z:g}_{kind}_b{beta:g}"
                    print(f"FULLJ_POC_SOLVE label={label}", flush=True)
                    sol = constitutive_continue(source, a, beta, kind)
                    rec = {
                        "label": label,
                        "z": z,
                        "a": float(a),
                        "kind": kind,
                        "beta0": float(beta),
                        "solver_success": bool(sol["success"]),
                        "solver_reason": sol["reason"],
                        "saturated_residual": float(sol["saturated_residual"]),
                        "saturated_phi_rel_l2": float(sol["saturated_phi_rel_l2"]),
                        "continuation_attempts": int(sol.get("attempts", len(sol["continuation"]))),
                        "continuation": sol["continuation"],
                    }
                    if not sol["success"]:
                        any_fail = True
                        rec["last_lambda"] = float(sol.get("last_lambda", 0.0))
                        rec["failed_lambda"] = float(sol.get("failed_lambda", math.nan))
                        records.append(rec)
                        print(
                            f"FULLJ_POC_FAIL label={label} reason={sol['reason']} "
                            f"last_lambda={rec['last_lambda']:.12e}",
                            flush=True,
                        )
                        continue

                    chi = np.asarray(sol["chi"], float)
                    d, tilde, phi = base.diagnostics(chi, sol["rhs"], a, beta, kind)
                    residual_pass = bool(
                        d["finite"] and d["R2_relative_L2"] <= R2_GATE and d["R1_relative_L2"] <= R1_GATE
                    )
                    if not residual_pass:
                        any_fail = True
                    modes, slope, mono = mode_response(phi, sol["phi_hg"], sol["rhs"], a)
                    rec.update({
                        "residual_pass": residual_pass,
                        "diagnostics": d,
                        "mode_response": modes,
                        "highk_log_slope_T_phi": slope,
                        "highk_T_phi_monotone_decreasing": mono,
                    })
                    records.append(rec)
                    field_keys.append(label)
                    field_phi.append(phi)
                    field_chi.append(chi)
                    print(
                        f"FULLJ_POC_RESULT label={label} R2={d['R2_relative_L2']:.3e} "
                        f"R1={d['R1_relative_L2']:.3e} x_rms={d['x_rms']:.6e} "
                        f"slope={slope:.6f} monotone={mono} residual_pass={residual_pass}",
                        flush=True,
                    )
                    print(
                        "FULLJ_POC_MODES label=" + label + " " + " ".join(
                            f"k{r['k_Mpc']:.2f}:T={r['T_phi_Mpc2']:.4e},G={r['G_phi']:.4e},RHG={r['abs_phi_over_abs_phi_saturated']:.4e}"
                            for r in modes
                        ),
                        flush=True,
                    )

        valid = [r for r in records if r.get("solver_success") and r.get("residual_pass")]
        expected = len(ZS) * len(KINDS) * len(BETAS)
        all_valid = (len(valid) == expected) and not any_fail
        if not all_valid:
            classification = "FULLJ_COSMO_RECLOSURE_POC_INCONCLUSIVE_SOLVER"
        else:
            robust = all(
                bool(r["highk_T_phi_monotone_decreasing"]) and float(r["highk_log_slope_T_phi"]) <= -1.0
                for r in valid
            )
            classification = (
                "FULLJ_COSMO_RECLOSURE_POC_UV_SUPPRESSION_ROBUST"
                if robust else "FULLJ_COSMO_RECLOSURE_POC_UV_SUPPRESSION_NOT_ROBUST"
            )

        slopes = [float(r["highk_log_slope_T_phi"]) for r in valid]
        monotone_count = sum(bool(r["highk_T_phi_monotone_decreasing"]) for r in valid)
        result = {
            "classification": classification,
            "diagnostic_complete": True,
            "observational_claim_licensed": False,
            "act_likelihood_used": False,
            "scope": "fixed-state periodic physical-coordinate full-J baryonic quasistatic cosmological snapshot reclosure PoC; no matter re-evolution, memory, finite eta or likelihood",
            "class_upstream_sha": CLASS_SHA,
            "source_model": {
                "aest_model": "Exp",
                "KB": 0.0665,
                "eta": 0.0,
                "memory_enabled": False,
                "z": ZS.tolist(),
                "k_Mpc": K_MPC.tolist(),
                "Nx": NX,
                "kfund_Mpc": KFUND,
            },
            "continuation": {
                "type": "constitutive_full_source",
                "j_lambda": "(1-lambda)/beta0 + lambda*j(x)",
                "max_step": MAX_STEP,
                "min_step": MIN_STEP,
                "Newton_max": NEWTON_MAX,
                "physical_source_scaled": False,
            },
            "transfers": [
                {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in tr.items()}
                for tr in transfers
            ],
            "records": records,
            "summary": {
                "expected_cases": expected,
                "valid_cases": len(valid),
                "monotone_highk_cases": int(monotone_count),
                "slope_min": float(min(slopes)) if slopes else math.nan,
                "slope_median": float(np.median(slopes)) if slopes else math.nan,
                "slope_max": float(max(slopes)) if slopes else math.nan,
            },
            "interpretation_limit": "A positive UV-suppression label licenses only a larger controlled nonlinear calculation. It is not a CMB-lensing prediction or ACT test.",
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=True) + "\n")

        arrays = {
            "k_Mpc": K_MPC,
            "z": ZS,
            "mode_num": MODE_NUM,
            "phase": PHASE,
            "field_keys": np.asarray(field_keys, dtype="U64"),
        }
        for i, tr in enumerate(transfers):
            arrays[f"d_b_z{i}"] = np.asarray(tr["d_b"], float)
        if field_phi:
            arrays["phi"] = np.stack(field_phi)
            arrays["chi"] = np.stack(field_chi)
        np.savez_compressed(nout, **arrays)

        print("FULLJ_POC_SUMMARY " + json.dumps(result["summary"], sort_keys=True), flush=True)
        print("FULLJ_POC_CLASSIFICATION=" + classification, flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        return 0 if all_valid else 2

    except Exception as exc:
        result = {
            "classification": "FULLJ_COSMO_RECLOSURE_POC_INCOMPLETE",
            "diagnostic_complete": False,
            "observational_claim_licensed": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_POC_ERROR=" + result["error"], flush=True)
        print("FULLJ_POC_CLASSIFICATION=" + result["classification"], flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
