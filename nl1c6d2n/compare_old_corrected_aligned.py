#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator

FIELDS = ("d_b", "t_b", "d_m", "phi", "psi")
ZMIN = 0.2
ZMAX = 6.0


def rel_l2(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(b), 1e-300))


def orient(field, k, z, name):
    a = np.asarray(field, float)
    nk, nz = len(k), len(z)
    if a.shape == (nk, nz):
        return a
    if a.shape == (nz, nk):
        return a.T
    raise RuntimeError(f"{name}: cannot infer transfer orientation from shape={a.shape}, nk={nk}, nz={nz}")


def sorted_axes(k, z, a):
    ik = np.argsort(k)
    iz = np.argsort(z)
    return np.asarray(k)[ik], np.asarray(z)[iz], a[np.ix_(ik, iz)]


def directional(src_k, src_z, src_a, dst_k, dst_z, dst_a):
    klo = max(float(np.min(src_k)), float(np.min(dst_k)))
    khi = min(float(np.max(src_k)), float(np.max(dst_k)))
    zlo = max(ZMIN, float(np.min(src_z)), float(np.min(dst_z)))
    zhi = min(ZMAX, float(np.max(src_z)), float(np.max(dst_z)))
    km = (dst_k >= klo) & (dst_k <= khi)
    zm = (dst_z >= zlo) & (dst_z <= zhi)
    if np.count_nonzero(km) < 8 or np.count_nonzero(zm) < 8:
        raise RuntimeError(f"insufficient common grid: nk={np.count_nonzero(km)} nz={np.count_nonzero(zm)}")

    kt = dst_k[km]
    zt = dst_z[zm]
    ref = dst_a[np.ix_(km, zm)]
    interp = RegularGridInterpolator((src_k, src_z), src_a, method="linear", bounds_error=True)
    kk, zz = np.meshgrid(kt, zt, indexing="ij")
    pts = np.column_stack([kk.ravel(), zz.ravel()])
    pred = interp(pts).reshape(ref.shape)
    return {
        "relative_L2": rel_l2(pred, ref),
        "n_k": int(len(kt)),
        "n_z": int(len(zt)),
        "k_min_h_Mpc": float(np.min(kt)),
        "k_max_h_Mpc": float(np.max(kt)),
        "z_min": float(np.min(zt)),
        "z_max": float(np.max(zt)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--historical", required=True)
    ap.add_argument("--corrected", required=True)
    ap.add_argument("--raw-json", required=True)
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    old = np.load(args.historical)
    cor = np.load(args.corrected)
    raw = json.load(open(args.raw_json))

    ok = np.asarray(old["k_native_h"], float)
    oz = np.asarray(old["z_native"], float)
    ck = np.asarray(cor["k_native_h"], float)
    cz = np.asarray(cor["z_native"], float)

    fields = {}
    for key in FIELDS:
        if key not in old.files or key not in cor.files:
            fields[key] = {"present": False}
            continue
        oa = orient(old[key], ok, oz, f"historical:{key}")
        ca = orient(cor[key], ck, cz, f"corrected:{key}")
        oks, ozs, oas = sorted_axes(ok, oz, oa)
        cks, czs, cas = sorted_axes(ck, cz, ca)
        old_to_corrected = directional(oks, ozs, oas, cks, czs, cas)
        corrected_to_old = directional(cks, czs, cas, oks, ozs, oas)
        fields[key] = {
            "present": True,
            "historical_to_corrected": old_to_corrected,
            "corrected_to_historical": corrected_to_old,
            "symmetric_conservative_relative_L2": float(max(old_to_corrected["relative_L2"], corrected_to_old["relative_L2"])),
        }

    vals = [v["symmetric_conservative_relative_L2"] for v in fields.values() if v.get("present")]
    out = {
        "label": "NL1C6D2N_OLD_VS_CORRECTED_GRID_ALIGNED_DIAGNOSTIC",
        "historical_npz": args.historical,
        "corrected_npz": args.corrected,
        "alignment": {
            "method": "bilinear RegularGridInterpolator in native (k_h,z)",
            "z_range": [ZMIN, ZMAX],
            "two_directional_interpolations": True,
            "reported_metric": "max of two directional relative L2 values",
            "no_extrapolation": True,
        },
        "transfer_metric_fields": fields,
        "max_grid_aligned_transfer_relative_L2": float(max(vals)) if vals else None,
        "direct_controls_from_raw_diagnostic": {
            "background": raw.get("background"),
            "spectra": raw.get("spectra"),
            "raw_grid_mismatch": raw.get("grids"),
            "raw_elementwise_transfer_metrics_not_used_for_rerun_decision": True,
        },
        "descriptive_only_no_similarity_pass_fail": True,
        "cosmological_refit_performed": False,
        "memory_or_likelihood_evaluated": False,
        "historical_results_unchanged": True,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("OLD_VS_CORRECTED_GRID_ALIGNED_DIAGNOSTIC")
    print(json.dumps(out, indent=2, sort_keys=True))
    print(f"JSON={args.json_out}")


if __name__ == "__main__":
    raise SystemExit(main())
