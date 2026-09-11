#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nl1c6 import full_j_baryonic_reclosure as base
from fullj_poc import cosmological_reclosure_poc as poc

ZS = np.asarray([0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0], dtype=float)
K_MPC = np.asarray([0.025, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30, 0.40,
                    0.60, 0.80, 1.00, 1.20, 1.50], dtype=float)
KFUND = 0.0125
MODE_NUM = np.asarray([2, 4, 6, 8, 12, 16, 24, 32, 48, 64, 80, 96, 120], dtype=int)
PHASE = np.asarray([0.13, 0.71, 1.29, 1.87, 2.45, 3.03, 3.61, 4.19, 4.77,
                    5.35, 5.93, 0.22681469282041355, 0.8068146928204127], dtype=float)
NX = 384
KINDS = ("simple", "exponential", "sharp")
BETAS = (1.0, 0.5, 0.1)
R2_GATE = 1.0e-8
R1_GATE = 1.0e-10
SAT_GATE = 1.0e-10
UV_KMIN = 0.40
UV_SLOPE_GATE = -1.0


def configure_upstream() -> None:
    # Reuse the successful PoC implementation without changing its physical equations.
    poc.ZS = ZS.copy()
    poc.K_MPC = K_MPC.copy()
    poc.KFUND = float(KFUND)
    poc.MODE_NUM = MODE_NUM.copy()
    poc.PHASE = PHASE.copy()
    poc.NX = int(NX)
    poc.KINDS = KINDS
    poc.BETAS = BETAS
    poc.R2_GATE = R2_GATE
    poc.R1_GATE = R1_GATE
    poc.SAT_GATE = SAT_GATE
    poc.configure_periodic_grid()

    inferred = np.rint(K_MPC / KFUND).astype(int)
    if not np.array_equal(inferred, MODE_NUM):
        raise RuntimeError(f"dense mode identity failed: {inferred} vs {MODE_NUM}")
    cutoff = int(np.floor(NX / 3.0))
    if int(MODE_NUM.max()) > cutoff:
        raise RuntimeError(f"dense source mode {MODE_NUM.max()} exceeds 2/3 cutoff {cutoff}")


def dense_mode_response(phi, phi_hg, rhs, a):
    n = len(phi)
    cf = np.fft.fft(phi) / n
    ch = np.fft.fft(phi_hg) / n
    cr = np.fft.fft(rhs) / n
    rows = []
    for k, m in zip(K_MPC, MODE_NUM):
        den = abs(cr[int(m)])
        if den <= 1e-300:
            raise RuntimeError(f"zero rhs Fourier coefficient at dense source mode m={m}")
        tphi = float(abs(cf[int(m)]) / den)
        gphi = float((k / a) ** 2 * tphi)
        rhg = float(abs(cf[int(m)]) / max(abs(ch[int(m)]), 1e-300))
        rows.append({
            "k_Mpc": float(k),
            "mode": int(m),
            "T_phi_Mpc2": tphi,
            "G_phi": gphi,
            "abs_phi_over_abs_phi_saturated": rhg,
            "abs_phi_mode": float(abs(cf[int(m)])),
            "abs_rhs_mode": float(den),
        })
    high = [r for r in rows if r["k_Mpc"] >= UV_KMIN - 1e-12]
    kval = np.asarray([r["k_Mpc"] for r in high], float)
    tval = np.asarray([r["T_phi_Mpc2"] for r in high], float)
    slope = float(np.polyfit(np.log(kval), np.log(np.maximum(tval, 1e-300)), 1)[0])
    mono = bool(np.all(np.diff(tval) < 0.0))
    return rows, slope, mono


def aggregate_rows(records):
    out = []
    for z in ZS:
        zr = [r for r in records if r.get("solver_success") and r.get("residual_pass")
              and abs(float(r["z"]) - float(z)) < 1e-12]
        if len(zr) != len(KINDS) * len(BETAS):
            continue
        for ik, k in enumerate(K_MPC):
            tv = np.asarray([r["mode_response"][ik]["T_phi_Mpc2"] for r in zr], float)
            gv = np.asarray([r["mode_response"][ik]["G_phi"] for r in zr], float)
            rv = np.asarray([r["mode_response"][ik]["abs_phi_over_abs_phi_saturated"] for r in zr], float)
            out.append({
                "z": float(z),
                "k_Mpc": float(k),
                "T_phi_median_Mpc2": float(np.median(tv)),
                "T_phi_min_Mpc2": float(np.min(tv)),
                "T_phi_max_Mpc2": float(np.max(tv)),
                "G_phi_median": float(np.median(gv)),
                "G_phi_min": float(np.min(gv)),
                "G_phi_max": float(np.max(gv)),
                "RHG_median": float(np.median(rv)),
                "RHG_min": float(np.min(rv)),
                "RHG_max": float(np.max(rv)),
                "branch_count": int(len(zr)),
                "G_phi_fractional_span": float((np.max(gv) - np.min(gv)) / max(abs(np.median(gv)), 1e-300)),
            })
    return out


def write_long_csv(path: Path, records):
    fields = [
        "z", "a", "kind", "beta0", "k_Mpc", "mode", "T_phi_Mpc2", "G_phi",
        "abs_phi_over_abs_phi_saturated", "abs_phi_mode", "abs_rhs_mode",
        "x_rms", "R1_relative_L2", "R2_relative_L2", "highk_log_slope_T_phi",
        "highk_T_phi_monotone_decreasing", "residual_pass"
    ]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in records:
            if not r.get("solver_success"):
                continue
            d = r["diagnostics"]
            for mr in r["mode_response"]:
                w.writerow({
                    "z": r["z"], "a": r["a"], "kind": r["kind"], "beta0": r["beta0"],
                    "k_Mpc": mr["k_Mpc"], "mode": mr["mode"],
                    "T_phi_Mpc2": mr["T_phi_Mpc2"], "G_phi": mr["G_phi"],
                    "abs_phi_over_abs_phi_saturated": mr["abs_phi_over_abs_phi_saturated"],
                    "abs_phi_mode": mr["abs_phi_mode"], "abs_rhs_mode": mr["abs_rhs_mode"],
                    "x_rms": d["x_rms"], "R1_relative_L2": d["R1_relative_L2"],
                    "R2_relative_L2": d["R2_relative_L2"],
                    "highk_log_slope_T_phi": r["highk_log_slope_T_phi"],
                    "highk_T_phi_monotone_decreasing": r["highk_T_phi_monotone_decreasing"],
                    "residual_pass": r["residual_pass"],
                })


def write_aggregate_csv(path: Path, rows):
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_dense_reclosure_map.json")
    ap.add_argument("--npz-out", default="results/fullj_dense_reclosure_map.npz")
    ap.add_argument("--csv-out", default="results/fullj_dense_reclosure_map.csv")
    ap.add_argument("--aggregate-csv-out", default="results/fullj_dense_reclosure_kernel_median.csv")
    args = ap.parse_args()

    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    cout = Path(args.csv_out)
    aout = Path(args.aggregate_csv_out)
    for p in (jout, nout, cout, aout):
        p.parent.mkdir(parents=True, exist_ok=True)

    configure_upstream()
    print("FULLJ_DENSE_START", flush=True)
    print("Z=" + ",".join(f"{x:.6g}" for x in ZS), flush=True)
    print("K_MPC=" + ",".join(f"{x:.6g}" for x in K_MPC), flush=True)
    print(f"NX={NX} kfund={KFUND:.8g}_Mpc^-1 branches={len(KINDS)*len(BETAS)} expected_snapshots={len(ZS)*len(KINDS)*len(BETAS)}", flush=True)

    transfers, classy_module = poc.extract_baryon_transfers()
    print("FULLJ_DENSE_CLASS_TRANSFER_READY classy=" + classy_module, flush=True)
    for tr in transfers:
        print(
            f"FULLJ_DENSE_DB z={tr['z']:.6g} nativeN={tr['native_n']} "
            f"nativeK=[{tr['native_k_min_Mpc']:.6e},{tr['native_k_max_Mpc']:.6e}]",
            flush=True,
        )

    records = []
    any_solver_fail = False
    any_residual_fail = False

    for tr in transfers:
        z = float(tr["z"])
        db = np.asarray(tr["d_b"], float)
        delta, source, a = base.source_for(db, z, NX)
        print(f"FULLJ_DENSE_SNAPSHOT z={z:.6g} a={a:.12e} delta_rms={np.sqrt(np.mean(delta*delta)):.12e}", flush=True)
        for kind in KINDS:
            for beta in BETAS:
                label = f"z{z:g}_{kind}_b{beta:g}"
                print(f"FULLJ_DENSE_SOLVE label={label}", flush=True)
                sol = poc.constitutive_continue(source, a, beta, kind)
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
                    any_solver_fail = True
                    rec["last_lambda"] = float(sol.get("last_lambda", 0.0))
                    rec["failed_lambda"] = float(sol.get("failed_lambda", math.nan))
                    records.append(rec)
                    print(f"FULLJ_DENSE_FAIL label={label} reason={sol['reason']} last_lambda={rec['last_lambda']:.12e}", flush=True)
                    continue

                chi = np.asarray(sol["chi"], float)
                d, tilde, phi = base.diagnostics(chi, sol["rhs"], a, beta, kind)
                residual_pass = bool(d["finite"] and d["R2_relative_L2"] <= R2_GATE and d["R1_relative_L2"] <= R1_GATE)
                if not residual_pass:
                    any_residual_fail = True
                modes, slope, mono = dense_mode_response(phi, sol["phi_hg"], sol["rhs"], a)
                uv_pass = bool(mono and slope <= UV_SLOPE_GATE)
                rec.update({
                    "residual_pass": residual_pass,
                    "uv_persistence_pass": uv_pass,
                    "diagnostics": d,
                    "mode_response": modes,
                    "highk_log_slope_T_phi": slope,
                    "highk_T_phi_monotone_decreasing": mono,
                })
                records.append(rec)
                print(
                    f"FULLJ_DENSE_RESULT label={label} R2={d['R2_relative_L2']:.3e} R1={d['R1_relative_L2']:.3e} "
                    f"x_rms={d['x_rms']:.6e} slope={slope:.6f} monotone={mono} residual_pass={residual_pass} uv_pass={uv_pass}",
                    flush=True,
                )
                print(
                    "FULLJ_DENSE_MODES label=" + label + " " + " ".join(
                        f"k{r['k_Mpc']:.3f}:T={r['T_phi_Mpc2']:.4e},G={r['G_phi']:.4e},RHG={r['abs_phi_over_abs_phi_saturated']:.4e}"
                        for r in modes
                    ),
                    flush=True,
                )

    expected = len(ZS) * len(KINDS) * len(BETAS)
    valid = [r for r in records if r.get("solver_success") and r.get("residual_pass")]
    all_valid = len(valid) == expected and not any_solver_fail and not any_residual_fail
    if not all_valid:
        classification = "FULLJ_DENSE_RECLOSURE_MAP_INCONCLUSIVE_SOLVER"
    else:
        uv_all = all(bool(r.get("uv_persistence_pass")) for r in valid)
        classification = "FULLJ_DENSE_RECLOSURE_MAP_PASS" if uv_all else "FULLJ_DENSE_RECLOSURE_MAP_UV_STRUCTURE_CHANGED"

    agg = aggregate_rows(records)
    write_long_csv(cout, records)
    write_aggregate_csv(aout, agg)

    slopes = np.asarray([float(r["highk_log_slope_T_phi"]) for r in valid], float)
    xrms = np.asarray([float(r["diagnostics"]["x_rms"]) for r in valid], float)
    summary = {
        "expected_snapshots": expected,
        "valid_snapshots": len(valid),
        "uv_pass_snapshots": int(sum(bool(r.get("uv_persistence_pass")) for r in valid)),
        "monotone_highk_snapshots": int(sum(bool(r.get("highk_T_phi_monotone_decreasing")) for r in valid)),
        "slope_min": float(np.min(slopes)) if slopes.size else math.nan,
        "slope_median": float(np.median(slopes)) if slopes.size else math.nan,
        "slope_max": float(np.max(slopes)) if slopes.size else math.nan,
        "x_rms_min": float(np.min(xrms)) if xrms.size else math.nan,
        "x_rms_median": float(np.median(xrms)) if xrms.size else math.nan,
        "x_rms_max": float(np.max(xrms)) if xrms.size else math.nan,
        "aggregate_rows": len(agg),
    }

    result = {
        "classification": classification,
        "diagnostic_complete": True,
        "observational_claim_licensed": False,
        "act_likelihood_used": False,
        "scope": "dense fixed-state periodic physical-coordinate full-J baryonic quasistatic effective response map; no matter re-evolution, memory, finite eta, nonlinear FLRW evolution or likelihood",
        "interpretation_limit": "The aggregate table is an effective response map for the frozen multimode realization, not yet a unique nonlinear transfer function. A PASS licenses a subsequent nonlinear lensing projection experiment only.",
        "grid": {
            "z": ZS.tolist(), "k_Mpc": K_MPC.tolist(), "mode_numbers": MODE_NUM.tolist(),
            "phases": PHASE.tolist(), "Nx": NX, "kfund_Mpc": KFUND,
            "highk_subset_kmin_Mpc": UV_KMIN,
        },
        "branches": {"kind": list(KINDS), "beta0": list(BETAS)},
        "gates": {
            "R2_relative_L2_max": R2_GATE,
            "R1_relative_L2_max": R1_GATE,
            "saturated_control_max": SAT_GATE,
            "highk_slope_max": UV_SLOPE_GATE,
            "highk_T_phi_strictly_decreasing": True,
        },
        "summary": summary,
        "aggregate_kernel": agg,
        "records": records,
    }
    jout.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=True) + "\n")

    # Dense numeric arrays for downstream interpolation/plotting.
    shape = (len(ZS), len(KINDS), len(BETAS), len(K_MPC))
    T = np.full(shape, np.nan)
    G = np.full(shape, np.nan)
    RHG = np.full(shape, np.nan)
    slopes_arr = np.full(shape[:3], np.nan)
    xrms_arr = np.full(shape[:3], np.nan)
    r1_arr = np.full(shape[:3], np.nan)
    r2_arr = np.full(shape[:3], np.nan)
    valid_arr = np.zeros(shape[:3], dtype=bool)
    for r in records:
        iz = int(np.argmin(np.abs(ZS - float(r["z"]))))
        ikind = KINDS.index(r["kind"])
        ib = BETAS.index(float(r["beta0"]))
        if not (r.get("solver_success") and r.get("residual_pass")):
            continue
        valid_arr[iz, ikind, ib] = True
        slopes_arr[iz, ikind, ib] = r["highk_log_slope_T_phi"]
        xrms_arr[iz, ikind, ib] = r["diagnostics"]["x_rms"]
        r1_arr[iz, ikind, ib] = r["diagnostics"]["R1_relative_L2"]
        r2_arr[iz, ikind, ib] = r["diagnostics"]["R2_relative_L2"]
        for ik, mr in enumerate(r["mode_response"]):
            T[iz, ikind, ib, ik] = mr["T_phi_Mpc2"]
            G[iz, ikind, ib, ik] = mr["G_phi"]
            RHG[iz, ikind, ib, ik] = mr["abs_phi_over_abs_phi_saturated"]
    np.savez_compressed(
        nout, z=ZS, k_Mpc=K_MPC, mode_numbers=MODE_NUM, phases=PHASE,
        kinds=np.asarray(KINDS), betas=np.asarray(BETAS),
        T_phi_Mpc2=T, G_phi=G, RHG=RHG, highk_slope=slopes_arr,
        x_rms=xrms_arr, R1=r1_arr, R2=r2_arr, valid=valid_arr,
    )

    print("FULLJ_DENSE_SUMMARY " + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_DENSE_CLASSIFICATION=" + classification, flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_DENSE_JSON=" + str(jout), flush=True)
    print("FULLJ_DENSE_NPZ=" + str(nout), flush=True)
    print("FULLJ_DENSE_CSV=" + str(cout), flush=True)
    print("FULLJ_DENSE_AGGREGATE_CSV=" + str(aout), flush=True)

    # Scientific classifications are encoded in output; nonzero exit is reserved for incomplete solver coverage.
    raise SystemExit(0 if classification != "FULLJ_DENSE_RECLOSURE_MAP_INCONCLUSIVE_SOLVER" else 3)


if __name__ == "__main__":
    main()
