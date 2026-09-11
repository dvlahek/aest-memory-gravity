#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

LOCKED_CLASSIFICATION = "FULLJ_MODE_COUPLING_JACOBIAN_NODE_COUPLING_SUPPORTED"
EXPECTED_BACKGROUNDS = 27
EXPECTED_K = np.asarray(
    [0.025, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30, 0.40, 0.60, 0.80, 1.00, 1.20, 1.50],
    dtype=float,
)
UV_KMIN = 0.40
SCALE = 2.0
REG_GATE = 1.0e-12


def slope(k: np.ndarray, y: np.ndarray) -> float:
    hi = k >= UV_KMIN - 1.0e-12
    return float(
        np.polyfit(
            np.log(k[hi]),
            np.log(np.maximum(np.asarray(y, float)[hi], 1.0e-300)),
            1,
        )[0]
    )


def row_coupling(Kabs: np.ndarray) -> np.ndarray:
    out = np.zeros(Kabs.shape[0], dtype=float)
    for i in range(Kabs.shape[0]):
        d = max(float(Kabs[i, i]), 1.0e-300)
        out[i] = float(np.linalg.norm(np.delete(Kabs[i, :], i)) / d)
    return out


def rel(a, b) -> float:
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(aa), np.linalg.norm(bb), 1.0e-300))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--jacobian-npz",
        default="results/fullj_mode_coupling_jacobian.npz",
    )
    ap.add_argument(
        "--jacobian-json",
        default="results/fullj_mode_coupling_jacobian.json",
    )
    ap.add_argument(
        "--npz-out",
        default="results/fullj_static_snapshot_weyl_operator.npz",
    )
    ap.add_argument(
        "--json-out",
        default="results/fullj_static_snapshot_weyl_operator.json",
    )
    ap.add_argument(
        "--csv-out",
        default="results/fullj_static_snapshot_weyl_operator_summary.csv",
    )
    args = ap.parse_args()

    inp = Path(args.jacobian_npz)
    meta_path = Path(args.jacobian_json)
    if not inp.exists():
        raise FileNotFoundError(inp)
    if not meta_path.exists():
        raise FileNotFoundError(meta_path)

    meta = json.loads(meta_path.read_text())
    if meta.get("classification") != LOCKED_CLASSIFICATION:
        raise RuntimeError(
            "input Jacobian is not the locked node-coupling-supported result: "
            + str(meta.get("classification"))
        )
    if not bool(meta.get("diagnostic_complete", False)):
        raise RuntimeError("input Jacobian diagnostic is not complete")
    if bool(meta.get("observational_claim_licensed", True)):
        raise RuntimeError("locked input unexpectedly licenses observational claims")

    dat = np.load(inp, allow_pickle=False)
    k = np.asarray(dat["k_Mpc"], float)
    Kr = np.asarray(dat["K_real"], float)
    Ki = np.asarray(dat["K_imag"], float)
    labels = np.asarray(dat["labels"]).astype(str)

    if len(labels) != EXPECTED_BACKGROUNDS:
        raise RuntimeError(f"expected {EXPECTED_BACKGROUNDS} backgrounds, got {len(labels)}")
    if k.shape != EXPECTED_K.shape or not np.allclose(k, EXPECTED_K, rtol=0.0, atol=1.0e-14):
        raise RuntimeError("locked k grid mismatch")
    if Kr.shape != (EXPECTED_BACKGROUNDS, len(k), len(k)) or Ki.shape != Kr.shape:
        raise RuntimeError(f"unexpected Jacobian matrix shape {Kr.shape}")
    if not np.all(np.isfinite(Kr)) or not np.all(np.isfinite(Ki)):
        raise RuntimeError("non-finite locked Jacobian matrix")

    Kphi = Kr + 1j * Ki
    Kweyl = SCALE * Kphi

    scale_residual = rel(Kweyl, SCALE * Kphi)
    rows = []
    slope_diffs = []
    coupling_diffs = []
    amplitude_scale_errors = []

    for ib, label in enumerate(labels):
        Aphi = np.abs(Kphi[ib])
        Aw = np.abs(Kweyl[ib])
        dphi = np.diag(Aphi)
        dw = np.diag(Aw)
        sphi = slope(k, dphi)
        sw = slope(k, dw)
        cphi = row_coupling(Aphi)
        cw = row_coupling(Aw)

        sd = abs(sw - sphi)
        cd = float(np.max(np.abs(cw - cphi)))
        ase = rel(Aw, SCALE * Aphi)
        slope_diffs.append(sd)
        coupling_diffs.append(cd)
        amplitude_scale_errors.append(ase)
        rows.append(
            {
                "label": label,
                "phi_diag_highk_slope": sphi,
                "weyl_diag_highk_slope": sw,
                "abs_slope_difference": sd,
                "max_abs_row_coupling_difference": cd,
                "amplitude_scale_relative_error": ase,
            }
        )

    max_slope_diff = float(max(slope_diffs))
    max_coupling_diff = float(max(coupling_diffs))
    max_amp_error = float(max(amplitude_scale_errors))
    regression_pass = bool(
        scale_residual <= REG_GATE
        and max_slope_diff <= REG_GATE
        and max_coupling_diff <= REG_GATE
        and max_amp_error <= REG_GATE
    )

    phi_slopes = np.asarray([r["phi_diag_highk_slope"] for r in rows], float)
    weyl_slopes = np.asarray([r["weyl_diag_highk_slope"] for r in rows], float)

    classification = (
        "FULLJ_STATIC_SNAPSHOT_WEYL_OPERATOR_IDENTITY_PASS"
        if regression_pass
        else "FULLJ_STATIC_SNAPSHOT_WEYL_OPERATOR_IDENTITY_FAIL"
    )

    result = {
        "classification": classification,
        "input_classification": LOCKED_CLASSIFICATION,
        "backgrounds": int(len(labels)),
        "k_Mpc": k.tolist(),
        "weyl_convention": "W=Phi+Psi",
        "static_dust_identity": "Psi=Phi",
        "operator_identity": "K_W=2*K_Phi",
        "scale_factor": SCALE,
        "regression_gate": REG_GATE,
        "scale_residual": scale_residual,
        "max_abs_slope_difference": max_slope_diff,
        "max_abs_row_coupling_difference": max_coupling_diff,
        "max_amplitude_scale_relative_error": max_amp_error,
        "phi_diag_slope_min": float(np.min(phi_slopes)),
        "phi_diag_slope_median": float(np.median(phi_slopes)),
        "phi_diag_slope_max": float(np.max(phi_slopes)),
        "weyl_diag_slope_min": float(np.min(weyl_slopes)),
        "weyl_diag_slope_median": float(np.median(weyl_slopes)),
        "weyl_diag_slope_max": float(np.max(weyl_slopes)),
        "static_snapshot_weyl_mapping_licensed": bool(regression_pass),
        "evolving_flrw_weyl_power_licensed": False,
        "act_likelihood_used": False,
        "act_likelihood_licensed": False,
        "observational_claim_licensed": False,
        "scope": (
            "deterministic zero-parameter W=2 Phi mapping of the locked static/fixed-a full-J "
            "mode-coupling Jacobian; not an evolving FLRW Weyl power spectrum or lensing prediction"
        ),
        "records": rows,
    }

    out_npz = Path(args.npz_out)
    out_json = Path(args.json_out)
    out_csv = Path(args.csv_out)
    for p in (out_npz, out_json, out_csv):
        p.parent.mkdir(parents=True, exist_ok=True)

    np.savez_compressed(
        out_npz,
        k_Mpc=k,
        labels=labels,
        K_Phi_real=Kphi.real,
        K_Phi_imag=Kphi.imag,
        K_Weyl_real=Kweyl.real,
        K_Weyl_imag=Kweyl.imag,
        scale_factor=np.asarray([SCALE], float),
    )
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("FULLJ_STATIC_WEYL_SUMMARY " + json.dumps({
        "backgrounds": len(labels),
        "scale_residual": scale_residual,
        "max_abs_slope_difference": max_slope_diff,
        "max_abs_row_coupling_difference": max_coupling_diff,
        "weyl_diag_slope_min": float(np.min(weyl_slopes)),
        "weyl_diag_slope_median": float(np.median(weyl_slopes)),
        "weyl_diag_slope_max": float(np.max(weyl_slopes)),
    }, sort_keys=True), flush=True)
    print("FULLJ_STATIC_WEYL_CLASSIFICATION=" + classification, flush=True)
    print("STATIC_SNAPSHOT_WEYL_MAPPING_LICENSED=" + str(regression_pass), flush=True)
    print("EVOLVING_FLRW_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_STATIC_WEYL_NPZ=" + str(out_npz), flush=True)
    print("FULLJ_STATIC_WEYL_JSON=" + str(out_json), flush=True)
    print("FULLJ_STATIC_WEYL_CSV=" + str(out_csv), flush=True)

    return 0 if regression_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
