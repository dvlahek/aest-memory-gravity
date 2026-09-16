#!/usr/bin/env python3
"""NL1C4 expanding action-derived memory-source trajectory.

Implements the frozen preregistration in
``docs/nl1c4_predata_expanding_memory_source_trajectory.md``.

Theory-only. It consumes the retained v0.77 memory-off accepted-source trace,
reconstructs the deterministic six-mode real-space representative, evolves the
positive Drude bath over the complete native history, and evaluates the
longitudinal backreaction and direct eta-linear memory-energy source on the
frozen z=0.2..1.5 window. No finite eta, halo model, collapse threshold,
observational data, likelihood, or off-native time interpolation is used.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.special import roots_legendre

ARTIFACT_RUN_ID = 34315590099
ARTIFACT_ID = 10090367181
ARTIFACT_DIGEST = "sha256:24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378"
TRACE_NAME = "v076_v077_base_trace.dat"

H0 = 67.3324639084866
HRED = H0 / 100.0
AS = 2.1308864352626987e-9
NS = 0.9666229454895277
KPIV_MPC = 0.05
A0 = 1.2e-10
C_M_S = 299792458.0
MPC_M = 3.0856775814913673e22
TAUH0 = 10.0

K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], dtype=float)
K_MPC = K_H * HRED
K_M = K_MPC / MPC_M
FOURIER_N = np.asarray([3, 5, 8, 10, 15, 20], dtype=int)
PHASES = np.asarray([0.13, 0.71, 1.29, 2.03, 2.77, 3.41], dtype=float)
ZMIN, ZMAX = 0.2, 1.5

PRIMARY_ORDER = 1024
CONTROL_ORDER = 512
NX_VALUES = (256, 512)
K_REL_MAX = 1.0e-12
MIN_COMMON_TIMES = 8
XRMS_REL_MAX = 1.0e-10
QUAD_REL_MAX = 1.0e-2
NX_REL_MAX = 5.0e-3


def log_trap_weights(k: np.ndarray) -> np.ndarray:
    x = np.log(np.asarray(k, dtype=float))
    w = np.empty_like(x)
    w[0] = 0.5 * (x[1] - x[0])
    w[-1] = 0.5 * (x[-1] - x[-2])
    w[1:-1] = 0.5 * (x[2:] - x[:-2])
    return w


def tan_gl_nodes(n: int) -> tuple[np.ndarray, np.ndarray]:
    z, w = roots_legendre(int(n))
    theta = 0.25 * np.pi * (z + 1.0)
    return np.tan(theta), 0.5 * w


def step_linear(q, v, omega, h, x0, x1, dxi):
    """Cancellation-safe exact interval propagator inherited from v0.22."""
    c = 3.0 * h
    d = 0.5 * c
    slope = (x1 - x0) / dxi
    u0 = q - x0
    vu0 = v - slope
    force = -c * slope
    om2 = omega * omega
    disc = om2 - d * d
    scale = np.maximum(om2 + d * d, 1.0)
    under = disc > 1.0e-12 * scale
    over = disc < -1.0e-12 * scale
    crit = ~(under | over)
    un = np.empty_like(q)
    vn = np.empty_like(v)

    if np.any(under):
        O = np.sqrt(disc[under])
        z = O * dxi
        ed = np.exp(-d * dxi)
        co, si = np.cos(z), np.sin(z)
        uu, vv, oo2 = u0[under], vu0[under], om2[under]
        hu = ed * (uu * co + (vv + d * uu) / O * si)
        hv = ed * (vv * co - (d * vv + oo2 * uu) / O * si)
        one = 1.0 - ed * (co + d / O * si)
        G = ed * si / O
        un[under] = hu + force / oo2 * one
        vn[under] = hv + force * G

    if np.any(over):
        oo2 = om2[over]
        delta = np.sqrt(-disc[over])
        lam1 = -oo2 / (d + delta)
        lam2 = -d - delta
        den = lam1 - lam2
        e1, e2 = np.exp(lam1 * dxi), np.exp(lam2 * dxi)
        uu, vv = u0[over], vu0[over]
        c1 = (vv - lam2 * uu) / den
        c2 = (lam1 * uu - vv) / den
        hu = c1 * e1 + c2 * e2
        hv = lam1 * c1 * e1 + lam2 * c2 * e2
        one = (-lam2 * (-np.expm1(lam1 * dxi)) + lam1 * (-np.expm1(lam2 * dxi))) / den
        G = (e1 - e2) / den
        un[over] = hu + force / oo2 * one
        vn[over] = hv + force * G

    if np.any(crit):
        oo2 = om2[crit]
        zz = d * dxi
        ed = np.exp(-zz)
        uu, vv = u0[crit], vu0[crit]
        hu = ed * (uu + (vv + d * uu) * dxi)
        hv = ed * (vv - (d * vv + oo2 * uu) * dxi)
        one = -np.expm1(-zz) - zz * ed
        G = ed * dxi
        un[crit] = hu + force / oo2 * one
        vn[crit] = hv + force * G

    return x1 + un, vn + slope


def read_trace(path: Path):
    rows = []
    with path.open(newline="") as f:
        reader = csv.DictReader(f, delimiter=" ", skipinitialspace=True)
        required = {"k", "tau", "a", "H_over_H0", "chi", "Q"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise RuntimeError(f"trace header must contain {sorted(required)}")
        for r in reader:
            try:
                row = {key: float(r[key]) for key in required}
            except Exception:
                continue
            if all(math.isfinite(v) for v in row.values()) and row["k"] > 0 and row["a"] > 0 and row["H_over_H0"] > 0:
                rows.append(row)
    if not rows:
        raise RuntimeError("empty or unreadable v0.77 trace")
    return rows


def cluster_duplicate_times(rows):
    rr = sorted(rows, key=lambda r: r["tau"])
    groups, cur, center = [], [], None
    for row in rr:
        t = row["tau"]
        if center is None or abs(t - center) <= 1.0e-12 * max(abs(center), abs(t), 1.0):
            cur.append(row)
            center = float(np.median([x["tau"] for x in cur]))
        else:
            groups.append(cur)
            cur = [row]
            center = t
    if cur:
        groups.append(cur)
    out = []
    for g in groups:
        out.append({key: float(np.median([r[key] for r in g])) for key in ["k", "tau", "a", "H_over_H0", "chi", "Q"]})
    return out


def select_and_align(rows):
    histories, misses = [], []
    allk = np.asarray([r["k"] for r in rows], dtype=float)
    for target in K_MPC:
        rel = np.abs(allk - target) / max(abs(float(target)), 1.0e-300)
        miss = float(np.min(rel))
        misses.append(miss)
        if miss > K_REL_MAX:
            raise RuntimeError(f"requested k={target:.17g} missing; relative miss={miss:.6g}")
        selected = [r for r, e in zip(rows, rel) if e <= K_REL_MAX]
        histories.append(cluster_duplicate_times(selected))

    n = len(histories[0])
    if n == 0 or any(len(h) != n for h in histories):
        raise RuntimeError("selected mode histories do not have a common native length")
    ref_tau = np.asarray([r["tau"] for r in histories[0]])
    ref_a = np.asarray([r["a"] for r in histories[0]])
    ref_H = np.asarray([r["H_over_H0"] for r in histories[0]])
    max_mismatch = 0.0
    for hist in histories[1:]:
        for key, ref in [("tau", ref_tau), ("a", ref_a), ("H_over_H0", ref_H)]:
            cur = np.asarray([r[key] for r in hist])
            rel = np.abs(cur - ref) / np.maximum(np.maximum(np.abs(cur), np.abs(ref)), 1.0)
            max_mismatch = max(max_mismatch, float(np.max(rel)))
            if float(np.max(rel)) > 1.0e-12:
                raise RuntimeError(f"common native {key} mismatch={float(np.max(rel)):.6g}")
    return histories, max(misses), max_mismatch


def integrate_mode(history, order):
    omega, weights = tan_gl_nodes(order)
    q = np.zeros(order, dtype=float)
    v = np.zeros(order, dtype=float)
    nt = len(history)
    qs = np.empty((nt, order), dtype=float)
    vs = np.empty((nt, order), dtype=float)
    qs[0] = q
    vs[0] = v
    N = np.log(np.asarray([r["a"] for r in history], dtype=float))
    H = np.asarray([r["H_over_H0"] for r in history], dtype=float)
    x = np.asarray([r["chi"] / r["a"] for r in history], dtype=float)
    hgrid = H * TAUH0
    for i in range(nt - 1):
        dN = N[i + 1] - N[i]
        if not dN > 0:
            raise RuntimeError("non-increasing native scale-factor history")
        hm = math.sqrt(hgrid[i] * hgrid[i + 1])
        dxi = dN / hm
        q, v = step_linear(q, v, omega, hm, x[i], x[i + 1], dxi)
        qs[i + 1] = q
        vs[i + 1] = v
    return omega, weights, qs, vs


def integrate_all(histories, order):
    q_all, v_all = [], []
    omega_ref = weights_ref = None
    for hist in histories:
        omega, weights, qs, vs = integrate_mode(hist, order)
        if omega_ref is None:
            omega_ref, weights_ref = omega, weights
        q_all.append(qs)
        v_all.append(vs)
    return omega_ref, weights_ref, np.stack(q_all), np.stack(v_all)


def max_pointwise_relative(a, b):
    aa, bb = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    den = np.maximum(np.maximum(np.abs(aa), np.abs(bb)), 1.0e-300)
    return float(np.max(np.abs(aa - bb) / den))


def global_relative_l2(a, b):
    aa, bb = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(aa), np.linalg.norm(bb), 1.0e-300))


def evaluate(histories, order, nx):
    omega, weights, q_all, v_all = integrate_all(histories, order)
    widths = log_trap_weights(K_H)
    PR = AS * (K_MPC / KPIV_MPC) ** (NS - 1.0)
    amplitudes = np.sqrt(2.0 * widths * PR)

    theta = 2.0 * np.pi * np.arange(nx, dtype=float) / nx
    sin_basis = np.sin(FOURIER_N[:, None] * theta[None, :] + PHASES[:, None])

    a = np.asarray([r["a"] for r in histories[0]], dtype=float)
    tau = np.asarray([r["tau"] for r in histories[0]], dtype=float)
    z = 1.0 / a - 1.0
    eval_idx = np.where((z >= ZMIN - 1.0e-12) & (z <= ZMAX + 1.0e-12))[0]
    if eval_idx.size < MIN_COMMON_TIMES:
        raise RuntimeError(f"only {eval_idx.size} native times in frozen redshift window")

    out = []
    for it in eval_idx:
        chi = np.asarray([histories[im][it]["chi"] for im in range(len(histories))], dtype=float)
        xmode = chi / a[it]

        grad_pref = -amplitudes * K_M
        X = (grad_pref * xmode) @ sin_basis
        xrms_real = (C_M_S * C_M_S / A0) * float(np.sqrt(np.mean(X * X)))
        xrms_analytic = float(np.sqrt(np.sum(widths * ((C_M_S * C_M_S / A0) * K_M * np.sqrt(PR) * np.abs(chi) / a[it]) ** 2)))
        xrms_rel = abs(xrms_real - xrms_analytic) / max(abs(xrms_analytic), 1.0e-300)

        q = q_all[:, it, :]
        v = v_all[:, it, :]
        grad_z = ((q.T * grad_pref[None, :]) @ sin_basis)
        grad_v_over_r = (((v.T / omega[:, None]) * grad_pref[None, :]) @ sin_basis)
        weighted_grad_z = weights @ grad_z
        B = X - weighted_grad_z
        B_rms = float(np.sqrt(np.mean(B * B)))
        rho_x = 0.25 * np.sum(weights[:, None] * (grad_v_over_r ** 2 + (grad_z - X[None, :]) ** 2), axis=0)
        rho_mean = float(np.mean(rho_x))

        out.append({
            "native_index": int(it),
            "tau_Mpc": float(tau[it]),
            "a": float(a[it]),
            "z": float(z[it]),
            "x_rms_realspace": xrms_real,
            "x_rms_analytic": xrms_analytic,
            "x_rms_relative_error": float(xrms_rel),
            "B_rms_per_m": B_rms,
            "rhohat_mem_mean_per_m2": rho_mean,
            "B_rms_dimensionless_acceleration_gradient": float((C_M_S * C_M_S / A0) * B_rms),
            "rhohat_mem_mean_dimensionless_gradient2": float((C_M_S * C_M_S / A0) ** 2 * rho_mean),
        })

    return out


def validate_artifact_metadata(path: Path):
    meta = json.loads(path.read_text())
    if "artifacts" in meta:
        art = next((x for x in meta["artifacts"] if int(x.get("id", -1)) == ARTIFACT_ID), None)
    else:
        art = meta
    if art is None:
        return {"checked": True, "pass": False, "reason": "frozen artifact ID absent"}
    got_id = int(art.get("id", art.get("artifact_id", -1)))
    got_digest = str(art.get("digest", ""))
    run = art.get("workflow_run", {}) or {}
    got_run = int(run.get("id", art.get("run_id", -1)))
    ok = got_id == ARTIFACT_ID and got_run == ARTIFACT_RUN_ID and got_digest == ARTIFACT_DIGEST
    return {
        "checked": True,
        "pass": bool(ok),
        "artifact_id": got_id,
        "run_id": got_run,
        "digest": got_digest,
        "expected_artifact_id": ARTIFACT_ID,
        "expected_run_id": ARTIFACT_RUN_ID,
        "expected_digest": ARTIFACT_DIGEST,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace", required=True)
    ap.add_argument("--artifact-meta-json", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--csv-out", required=True)
    args = ap.parse_args()

    trace = Path(args.trace)
    if trace.name != TRACE_NAME:
        raise RuntimeError(f"frozen trace must be named {TRACE_NAME}")
    artifact = validate_artifact_metadata(Path(args.artifact_meta_json))
    if not artifact["pass"]:
        raise RuntimeError(f"frozen artifact provenance mismatch: {artifact}")

    rows = read_trace(trace)
    histories, k_miss, native_mismatch = select_and_align(rows)
    trace_sha = hashlib.sha256(trace.read_bytes()).hexdigest()

    evaluations = {}
    for order in (CONTROL_ORDER, PRIMARY_ORDER):
        for nx in NX_VALUES:
            evaluations[(order, nx)] = evaluate(histories, order, nx)

    base = evaluations[(PRIMARY_ORDER, NX_VALUES[-1])]
    ntime = len(base)
    xrms_errs = []
    for vals in evaluations.values():
        xrms_errs.extend([r["x_rms_relative_error"] for r in vals])

    def vec(order, nx, field):
        return np.asarray([r[field] for r in evaluations[(order, nx)]], dtype=float)

    B_q_c = vec(CONTROL_ORDER, 512, "B_rms_per_m")
    B_q_p = vec(PRIMARY_ORDER, 512, "B_rms_per_m")
    R_q_c = vec(CONTROL_ORDER, 512, "rhohat_mem_mean_per_m2")
    R_q_p = vec(PRIMARY_ORDER, 512, "rhohat_mem_mean_per_m2")
    B_nx_256 = vec(PRIMARY_ORDER, 256, "B_rms_per_m")
    B_nx_512 = vec(PRIMARY_ORDER, 512, "B_rms_per_m")
    R_nx_256 = vec(PRIMARY_ORDER, 256, "rhohat_mem_mean_per_m2")
    R_nx_512 = vec(PRIMARY_ORDER, 512, "rhohat_mem_mean_per_m2")

    controls = {
        "quadrature_B_rms": {
            "max_pointwise_relative_difference": max_pointwise_relative(B_q_c, B_q_p),
            "global_relative_L2": global_relative_l2(B_q_c, B_q_p),
            "limit": QUAD_REL_MAX,
        },
        "quadrature_rhohat_mem_mean": {
            "max_pointwise_relative_difference": max_pointwise_relative(R_q_c, R_q_p),
            "global_relative_L2": global_relative_l2(R_q_c, R_q_p),
            "limit": QUAD_REL_MAX,
        },
        "spatial_B_rms": {
            "max_pointwise_relative_difference": max_pointwise_relative(B_nx_256, B_nx_512),
            "global_relative_L2": global_relative_l2(B_nx_256, B_nx_512),
            "limit": NX_REL_MAX,
        },
        "spatial_rhohat_mem_mean": {
            "max_pointwise_relative_difference": max_pointwise_relative(R_nx_256, R_nx_512),
            "global_relative_L2": global_relative_l2(R_nx_256, R_nx_512),
            "limit": NX_REL_MAX,
        },
    }
    for c in controls.values():
        c["pass"] = bool(c["max_pointwise_relative_difference"] <= c["limit"])

    all_reported = []
    for vals in evaluations.values():
        for r in vals:
            all_reported.extend([r["x_rms_realspace"], r["x_rms_analytic"], r["B_rms_per_m"], r["rhohat_mem_mean_per_m2"]])

    gates = {
        "artifact_digest_exact": bool(artifact["pass"]),
        "all_six_k_modes_relative_error_le_1e-12": bool(k_miss <= K_REL_MAX),
        "common_native_grid_relative_mismatch_le_1e-12": bool(native_mismatch <= 1.0e-12),
        "at_least_8_common_native_times": bool(ntime >= MIN_COMMON_TIMES),
        "realspace_xrms_matches_analytic_le_1e-10": bool(max(xrms_errs) <= XRMS_REL_MAX),
        "quadrature_B_rms_le_1e-2": bool(controls["quadrature_B_rms"]["pass"]),
        "quadrature_rhohat_mem_le_1e-2": bool(controls["quadrature_rhohat_mem_mean"]["pass"]),
        "spatial_B_rms_le_5e-3": bool(controls["spatial_B_rms"]["pass"]),
        "spatial_rhohat_mem_le_5e-3": bool(controls["spatial_rhohat_mem_mean"]["pass"]),
        "all_reported_quantities_finite": bool(np.all(np.isfinite(np.asarray(all_reported, dtype=float)))),
        "B_rms_positive_at_every_evaluation_time": bool(np.all(B_q_p > 0.0)),
        "rhohat_mem_positive_at_every_evaluation_time": bool(np.all(R_q_p > 0.0)),
        "no_finite_eta_observation_likelihood_halo_or_collapse_input": True,
    }
    passed = bool(all(gates.values()))
    classification = "NL1C4_EXPANDING_MEMORY_SOURCE_TRAJECTORY_PASS" if passed else "NL1C4_EXPANDING_MEMORY_SOURCE_TRAJECTORY_FAIL"

    result = {
        "classification": classification,
        "predata_classification": "NL1C4_PREDATA_EXPANDING_MEMORY_SOURCE_TRAJECTORY",
        "scope": "action-derived expanding periodic-box memory-source trajectory only; not a screened-resummed physical-state survival result and not a nonlinear structure-formation or observational result",
        "artifact_provenance": artifact,
        "trace": {
            "file": TRACE_NAME,
            "sha256": trace_sha,
            "requested_k_relative_miss_max": float(k_miss),
            "common_native_grid_relative_mismatch_max": float(native_mismatch),
            "native_history_length": int(len(histories[0])),
            "evaluation_times": int(ntime),
        },
        "frozen_model": {
            "H0_km_s_Mpc": H0,
            "A_s": AS,
            "n_s": NS,
            "k_pivot_Mpc_inv": KPIV_MPC,
            "a0_m_s2": A0,
            "tauH0": TAUH0,
            "eta": None,
            "k_h_per_Mpc": K_H.tolist(),
            "fourier_modes": FOURIER_N.tolist(),
            "phases_rad": PHASES.tolist(),
        },
        "implementation_lock": {
            "quadrature_orders": [CONTROL_ORDER, PRIMARY_ORDER],
            "spatial_resolutions": list(NX_VALUES),
            "relative_difference_gate_definition": "maximum pointwise |A-B|/max(|A|,|B|,1e-300) over the frozen evaluation times; global relative L2 is descriptive only",
            "spatial_derivative": "analytic Fourier derivative on the exact integer modes; no finite-difference derivative",
            "time_evolution": "complete common native history; no off-native time interpolation",
        },
        "controls": controls,
        "x_rms_reconstruction_relative_error_max": float(max(xrms_errs)),
        "primary_time_series": base,
        "gates": gates,
        "historical_results_unchanged": True,
        "interpretation": "PASS certifies that the complete action-derived retarded source is finite, nonzero and numerically stable on the certified physical signal-band reference. It does not establish survival after screened-resummed AeST reclosure and does not justify halo/collapse claims.",
    }

    jout = Path(args.json_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    cout = Path(args.csv_out)
    cout.parent.mkdir(parents=True, exist_ok=True)
    fields = list(base[0].keys())
    with cout.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(base)

    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
