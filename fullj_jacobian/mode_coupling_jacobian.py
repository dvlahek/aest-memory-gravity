#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import LinearOperator, gmres

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nl1c6 import full_j_baryonic_reclosure as base
from fullj_poc import cosmological_reclosure_poc as poc
from fullj_dense import dense_reclosure_map as dense

ZS = np.asarray([0.25, 0.5, 1.0], dtype=float)
K_MPC = dense.K_MPC.copy()
MODE_NUM = dense.MODE_NUM.copy()
PHASE = dense.PHASE.copy()
NX = int(dense.NX)
KINDS = dense.KINDS
BETAS = dense.BETAS
R2_GATE = dense.R2_GATE
R1_GATE = dense.R1_GATE
TAN_GATE = 1.0e-8
TAN_RTOL = 1.0e-10
UV_KMIN = 0.40
UV_SLOPE_GATE = -1.0
NODE_Z = 0.25
NODE_K = 0.60
NODE_LEFT = 0.40
NODE_RIGHT = 0.80
NODE_RATIO_GATE = 0.25
RAW_BUMP_GATE = 3.0
DIAG_BUMP_GATE = 3.0
COUPLING_GATE = 1.0
ROBUST_BRANCHES = 6


def configure() -> None:
    dense.configure_upstream()
    poc.ZS = ZS.copy()
    poc.K_MPC = K_MPC.copy()
    if int(MODE_NUM.max()) > int(np.floor(NX / 3.0)):
        raise RuntimeError("Jacobian source mode exceeds dense 2/3 cutoff")


def tangent_system(chi, a, beta, kind):
    chi = np.asarray(chi, float)
    n = len(chi)
    kk = base.kgrid(n) / a
    mask = base.dealias_mask(n)
    _, _, _, _, aeff = poc.blend_operator(
        chi, a, beta, kind, 1.0, need_linear_coeff=True
    )

    def pieces(v):
        v = np.asarray(v, float)
        vg = np.fft.ifft(1j * kk * np.fft.fft(v)).real
        dop = np.fft.ifft(1j * kk * (np.fft.fft(aeff * vg) * mask)).real
        dtilde = base.invlap_phys(dop, a)
        dphi = dtilde + v
        return dop, dtilde, dphi

    def jmv(v):
        dop, _, dphi = pieces(v)
        return dop + base.MU2 * dphi

    J = LinearOperator((n, n), matvec=jmv, dtype=float)
    M = poc.blend_preconditioner(chi, a, beta, kind, 1.0)
    return J, M, pieces


def unit_phase_mode(k, phase):
    x = np.arange(NX, dtype=float) * base.BOX / NX
    q = 2.0 * np.cos(k * x + phase)
    q -= np.mean(q)
    return q


def solve_local_jacobian(chi, a, beta, kind):
    J, M, pieces = tangent_system(chi, a, beta, kind)
    Kc = np.zeros((len(K_MPC), len(K_MPC)), dtype=complex)
    tangent_res = np.full(len(K_MPC), np.nan, dtype=float)
    tangent_info = np.full(len(K_MPC), -999, dtype=int)
    iterations_proxy = np.zeros(len(K_MPC), dtype=int)

    for j, (k, m, phase) in enumerate(zip(K_MPC, MODE_NUM, PHASE)):
        q = unit_phase_mode(float(k), float(phase))
        qh = np.fft.fft(q) / NX
        den = qh[int(m)]
        if abs(den) < 0.999999 or abs(den) > 1.000001:
            raise RuntimeError(f"unit tangent Fourier normalization failed at k={k}: |qhat|={abs(den)}")

        callback_count = [0]
        def cb(_):
            callback_count[0] += 1

        dchi, info = gmres(
            J, q, M=M, rtol=TAN_RTOL, atol=0.0,
            restart=min(80, NX), maxiter=360,
            callback=cb, callback_type="pr_norm",
        )
        tangent_info[j] = int(info)
        iterations_proxy[j] = int(callback_count[0])
        if not np.all(np.isfinite(dchi)):
            return {
                "success": False,
                "reason": f"nonfinite_tangent_k_{k:g}",
                "K_complex": Kc,
                "tangent_residual": tangent_res,
                "tangent_info": tangent_info,
                "iterations_proxy": iterations_proxy,
            }
        rr = J.matvec(dchi) - q
        rel = float(np.linalg.norm(rr) / max(np.linalg.norm(q), 1e-300))
        tangent_res[j] = rel
        if info != 0 or not np.isfinite(rel) or rel > TAN_GATE:
            return {
                "success": False,
                "reason": f"tangent_failed_k_{k:g}_info_{info}_res_{rel:.3e}",
                "K_complex": Kc,
                "tangent_residual": tangent_res,
                "tangent_info": tangent_info,
                "iterations_proxy": iterations_proxy,
            }

        dphi = pieces(dchi)[2]
        ch = np.fft.fft(dphi) / NX
        Kc[:, j] = ch[MODE_NUM] / den

    return {
        "success": True,
        "reason": "all_tangent_modes_converged",
        "K_complex": Kc,
        "tangent_residual": tangent_res,
        "tangent_info": tangent_info,
        "iterations_proxy": iterations_proxy,
    }


def ix(k):
    w = np.where(np.isclose(K_MPC, k, rtol=0.0, atol=1e-12))[0]
    if len(w) != 1:
        raise RuntimeError(f"k index not unique for {k}")
    return int(w[0])


def geom(a, b):
    return math.sqrt(max(float(a), 0.0) * max(float(b), 0.0))


def branch_metrics(Kabs, raw_modes, z):
    diag = np.diag(Kabs).copy()
    hi = K_MPC >= UV_KMIN - 1e-12
    slope = float(np.polyfit(np.log(K_MPC[hi]), np.log(np.maximum(diag[hi], 1e-300)), 1)[0])

    row_coupling = []
    dominant_input = []
    for i in range(len(K_MPC)):
        d = max(float(Kabs[i, i]), 1e-300)
        off = np.delete(Kabs[i, :], i)
        row_coupling.append(float(np.linalg.norm(off) / d))
        jmax = int(np.argmax(np.where(np.arange(len(K_MPC)) == i, -np.inf, Kabs[i, :])))
        dominant_input.append(float(K_MPC[jmax]))

    out = {
        "diag_abs": diag.tolist(),
        "diag_highk_log_slope": slope,
        "diag_uv_stable": bool(slope <= UV_SLOPE_GATE),
        "row_coupling_l2_over_diag": row_coupling,
        "dominant_offdiag_input_k_Mpc": dominant_input,
    }

    if abs(z - NODE_Z) < 1e-12:
        iL, iN, iR = ix(NODE_LEFT), ix(NODE_K), ix(NODE_RIGHT)
        rhs = np.asarray([r["abs_rhs_mode"] for r in raw_modes], float)
        raw = np.asarray([r["T_phi_Mpc2"] for r in raw_modes], float)
        source_node_ratio = float(rhs[iN] / max(geom(rhs[iL], rhs[iR]), 1e-300))
        raw_bump = float(raw[iN] / max(geom(raw[iL], raw[iR]), 1e-300))
        diag_bump = float(diag[iN] / max(geom(diag[iL], diag[iR]), 1e-300))
        coupling = float(row_coupling[iN])
        support = bool(
            source_node_ratio <= NODE_RATIO_GATE
            and raw_bump >= RAW_BUMP_GATE
            and diag_bump <= DIAG_BUMP_GATE
            and coupling >= COUPLING_GATE
        )
        out["node_test"] = {
            "source_node_ratio": source_node_ratio,
            "raw_transfer_bump": raw_bump,
            "local_diag_bump": diag_bump,
            "row_coupling_ratio": coupling,
            "dominant_offdiag_input_k_Mpc": dominant_input[iN],
            "supports_node_coupling": support,
        }
    return out


def write_matrix_csv(path, records):
    fields = ["z", "kind", "beta0", "k_out_Mpc", "k_in_Mpc", "K_abs", "K_real", "K_imag"]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in records:
            if not r.get("jacobian_success"):
                continue
            kr = np.asarray(r["K_real"], float)
            ki = np.asarray(r["K_imag"], float)
            ka = np.hypot(kr, ki)
            for io, ko in enumerate(K_MPC):
                for ji, kj in enumerate(K_MPC):
                    w.writerow({
                        "z": r["z"], "kind": r["kind"], "beta0": r["beta0"],
                        "k_out_Mpc": float(ko), "k_in_Mpc": float(kj),
                        "K_abs": float(ka[io, ji]), "K_real": float(kr[io, ji]), "K_imag": float(ki[io, ji]),
                    })


def write_summary_csv(path, records):
    fields = [
        "z", "kind", "beta0", "baseline_valid", "jacobian_success", "diag_highk_log_slope",
        "diag_uv_stable", "tangent_residual_max", "node_source_ratio", "node_raw_bump",
        "node_diag_bump", "node_row_coupling_ratio", "node_dominant_input_k_Mpc", "node_support"
    ]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in records:
            nt = r.get("node_test", {})
            w.writerow({
                "z": r["z"], "kind": r["kind"], "beta0": r["beta0"],
                "baseline_valid": r.get("baseline_valid", False),
                "jacobian_success": r.get("jacobian_success", False),
                "diag_highk_log_slope": r.get("diag_highk_log_slope", math.nan),
                "diag_uv_stable": r.get("diag_uv_stable", False),
                "tangent_residual_max": r.get("tangent_residual_max", math.nan),
                "node_source_ratio": nt.get("source_node_ratio", math.nan),
                "node_raw_bump": nt.get("raw_transfer_bump", math.nan),
                "node_diag_bump": nt.get("local_diag_bump", math.nan),
                "node_row_coupling_ratio": nt.get("row_coupling_ratio", math.nan),
                "node_dominant_input_k_Mpc": nt.get("dominant_offdiag_input_k_Mpc", math.nan),
                "node_support": nt.get("supports_node_coupling", False),
            })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_mode_coupling_jacobian.json")
    ap.add_argument("--npz-out", default="results/fullj_mode_coupling_jacobian.npz")
    ap.add_argument("--matrix-csv-out", default="results/fullj_mode_coupling_jacobian_matrix.csv")
    ap.add_argument("--summary-csv-out", default="results/fullj_mode_coupling_jacobian_summary.csv")
    args = ap.parse_args()

    paths = [Path(args.json_out), Path(args.npz_out), Path(args.matrix_csv_out), Path(args.summary_csv_out)]
    for p in paths:
        p.parent.mkdir(parents=True, exist_ok=True)

    configure()
    print("FULLJ_JAC_START", flush=True)
    print("Z=" + ",".join(f"{z:g}" for z in ZS), flush=True)
    print("K_MPC=" + ",".join(f"{k:g}" for k in K_MPC), flush=True)
    print(f"backgrounds={len(ZS)*len(KINDS)*len(BETAS)} tangent_solves={len(ZS)*len(KINDS)*len(BETAS)*len(K_MPC)}", flush=True)

    transfers, classy_module = poc.extract_baryon_transfers()
    print("FULLJ_JAC_CLASS_TRANSFER_READY classy=" + classy_module, flush=True)

    records = []
    all_mats = []
    incomplete = False

    for tr in transfers:
        z = float(tr["z"])
        db = np.asarray(tr["d_b"], float)
        delta, source, a = base.source_for(db, z, NX)
        print(f"FULLJ_JAC_SNAPSHOT z={z:g} a={a:.12e} delta_rms={np.sqrt(np.mean(delta*delta)):.12e}", flush=True)
        for kind in KINDS:
            for beta in BETAS:
                label = f"z{z:g}_{kind}_b{beta:g}"
                print(f"FULLJ_JAC_BASELINE_SOLVE label={label}", flush=True)
                sol = poc.constitutive_continue(source, a, beta, kind)
                rec = {
                    "label": label, "z": z, "a": float(a), "kind": kind, "beta0": float(beta),
                    "baseline_solver_success": bool(sol["success"]), "baseline_solver_reason": sol["reason"],
                }
                if not sol["success"]:
                    incomplete = True
                    rec.update({"baseline_valid": False, "jacobian_success": False})
                    records.append(rec)
                    print(f"FULLJ_JAC_BASELINE_FAIL label={label} reason={sol['reason']}", flush=True)
                    continue

                chi = np.asarray(sol["chi"], float)
                d, _, phi = base.diagnostics(chi, sol["rhs"], a, beta, kind)
                baseline_valid = bool(
                    d["finite"] and d["R2_relative_L2"] <= R2_GATE and d["R1_relative_L2"] <= R1_GATE
                )
                rec["baseline_valid"] = baseline_valid
                rec["baseline_diagnostics"] = d
                if not baseline_valid:
                    incomplete = True
                    rec["jacobian_success"] = False
                    records.append(rec)
                    print(f"FULLJ_JAC_BASELINE_RESIDUAL_FAIL label={label} R2={d['R2_relative_L2']:.3e} R1={d['R1_relative_L2']:.3e}", flush=True)
                    continue

                raw_modes, raw_slope, raw_mono = dense.dense_mode_response(phi, sol["phi_hg"], sol["rhs"], a)
                jac = solve_local_jacobian(chi, a, beta, kind)
                rec["jacobian_success"] = bool(jac["success"])
                rec["jacobian_reason"] = jac["reason"]
                rec["tangent_residuals"] = np.asarray(jac["tangent_residual"], float).tolist()
                rec["tangent_gmres_info"] = np.asarray(jac["tangent_info"], int).tolist()
                rec["tangent_iterations_proxy"] = np.asarray(jac["iterations_proxy"], int).tolist()
                finite_tres = np.asarray(jac["tangent_residual"], float)
                rec["tangent_residual_max"] = float(np.nanmax(finite_tres)) if np.any(np.isfinite(finite_tres)) else math.nan
                rec["raw_highk_log_slope_T_phi"] = float(raw_slope)
                rec["raw_highk_T_phi_monotone"] = bool(raw_mono)
                rec["raw_mode_response"] = raw_modes

                if not jac["success"]:
                    incomplete = True
                    records.append(rec)
                    print(f"FULLJ_JAC_TANGENT_FAIL label={label} reason={jac['reason']}", flush=True)
                    continue

                Kc = np.asarray(jac["K_complex"], complex)
                Kabs = np.abs(Kc)
                metrics = branch_metrics(Kabs, raw_modes, z)
                rec.update(metrics)
                rec["K_real"] = Kc.real.tolist()
                rec["K_imag"] = Kc.imag.tolist()
                records.append(rec)
                all_mats.append(Kc)

                node_txt = ""
                if "node_test" in metrics:
                    nt = metrics["node_test"]
                    node_txt = (
                        f" nodeN={nt['source_node_ratio']:.3e} Braw={nt['raw_transfer_bump']:.3e} "
                        f"Bdiag={nt['local_diag_bump']:.3e} C06={nt['row_coupling_ratio']:.3e} "
                        f"support={nt['supports_node_coupling']}"
                    )
                print(
                    f"FULLJ_JAC_RESULT label={label} R2={d['R2_relative_L2']:.3e} R1={d['R1_relative_L2']:.3e} "
                    f"tanmax={rec['tangent_residual_max']:.3e} diag_slope={metrics['diag_highk_log_slope']:.6f} "
                    f"diag_uv={metrics['diag_uv_stable']}" + node_txt,
                    flush=True,
                )
                if abs(z - NODE_Z) < 1e-12:
                    iN = ix(NODE_K)
                    row = Kabs[iN, :]
                    print(
                        "FULLJ_JAC_NODE_ROW label=" + label + " " + " ".join(
                            f"kin{k:.3f}:K={v:.4e}" for k, v in zip(K_MPC, row)
                        ), flush=True,
                    )

    expected_bg = len(ZS) * len(KINDS) * len(BETAS)
    complete = [r for r in records if r.get("baseline_valid") and r.get("jacobian_success")]
    diag_stable = [r for r in complete if r.get("diag_uv_stable")]
    node_records = [r for r in complete if abs(float(r["z"]) - NODE_Z) < 1e-12 and "node_test" in r]
    node_support = [r for r in node_records if r["node_test"]["supports_node_coupling"]]

    all_complete = (len(complete) == expected_bg and not incomplete)
    if not all_complete:
        classification = "FULLJ_MODE_COUPLING_JACOBIAN_INCONCLUSIVE_SOLVER"
    elif len(diag_stable) != expected_bg:
        classification = "FULLJ_MODE_COUPLING_JACOBIAN_LOCAL_UV_STRUCTURE_CHANGED"
    elif len(node_support) >= ROBUST_BRANCHES:
        classification = "FULLJ_MODE_COUPLING_JACOBIAN_NODE_COUPLING_SUPPORTED"
    else:
        classification = "FULLJ_MODE_COUPLING_JACOBIAN_DIAGONAL_UV_STABLE_NODE_UNRESOLVED"

    slopes = np.asarray([r["diag_highk_log_slope"] for r in complete], float)
    tanmax = np.asarray([r["tangent_residual_max"] for r in complete], float)
    coupling06 = np.asarray([
        r["node_test"]["row_coupling_ratio"] for r in node_records
    ], float) if node_records else np.asarray([], float)
    diagbump = np.asarray([
        r["node_test"]["local_diag_bump"] for r in node_records
    ], float) if node_records else np.asarray([], float)

    summary = {
        "expected_backgrounds": expected_bg,
        "complete_backgrounds": len(complete),
        "expected_tangent_solves": expected_bg * len(K_MPC),
        "diag_uv_stable_backgrounds": len(diag_stable),
        "z0p25_node_support_branches": len(node_support),
        "diag_slope_min": float(np.min(slopes)) if slopes.size else math.nan,
        "diag_slope_median": float(np.median(slopes)) if slopes.size else math.nan,
        "diag_slope_max": float(np.max(slopes)) if slopes.size else math.nan,
        "tangent_residual_max": float(np.max(tanmax)) if tanmax.size else math.nan,
        "z0p25_coupling_ratio_median": float(np.median(coupling06)) if coupling06.size else math.nan,
        "z0p25_diag_bump_median": float(np.median(diagbump)) if diagbump.size else math.nan,
    }

    result = {
        "classification": classification,
        "diagnostic_complete": bool(all_complete),
        "observational_claim_licensed": False,
        "act_likelihood_used": False,
        "scope": "phase-aligned local full-J mode-coupling Jacobian around three frozen nonlinear cosmological snapshots; no matter re-evolution, memory, finite eta, full quadrature operator or likelihood",
        "z": ZS.tolist(),
        "k_Mpc": K_MPC.tolist(),
        "mode_num": MODE_NUM.tolist(),
        "phase": PHASE.tolist(),
        "gates": {
            "R2_relative_L2_max": R2_GATE,
            "R1_relative_L2_max": R1_GATE,
            "tangent_relative_residual_max": TAN_GATE,
            "diag_highk_slope_max": UV_SLOPE_GATE,
            "node_source_ratio_max": NODE_RATIO_GATE,
            "raw_bump_min": RAW_BUMP_GATE,
            "diag_bump_max": DIAG_BUMP_GATE,
            "coupling_ratio_min": COUPLING_GATE,
            "robust_node_branches_min": ROBUST_BRANCHES,
        },
        "summary": summary,
        "records": records,
    }

    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    write_matrix_csv(Path(args.matrix_csv_out), records)
    write_summary_csv(Path(args.summary_csv_out), records)

    if all_mats:
        arr = np.asarray(all_mats, complex)
    else:
        arr = np.empty((0, len(K_MPC), len(K_MPC)), complex)
    np.savez_compressed(
        args.npz_out,
        z=ZS, k_Mpc=K_MPC, mode_num=MODE_NUM, phase=PHASE,
        K_real=arr.real, K_imag=arr.imag,
        labels=np.asarray([r["label"] for r in complete], dtype="U64"),
    )

    print("FULLJ_JAC_SUMMARY " + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_JAC_CLASSIFICATION=" + classification, flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_JAC_JSON=" + args.json_out, flush=True)
    print("FULLJ_JAC_NPZ=" + args.npz_out, flush=True)
    print("FULLJ_JAC_MATRIX_CSV=" + args.matrix_csv_out, flush=True)
    print("FULLJ_JAC_SUMMARY_CSV=" + args.summary_csv_out, flush=True)
    return 0 if all_complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
