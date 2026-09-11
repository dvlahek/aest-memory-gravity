#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

LOCKED_CLASSIFICATION = "FULLJ_MODE_COUPLING_JACOBIAN_NODE_COUPLING_SUPPORTED"
COMPLETE = "FULLJ_LOCAL_WEYL_COVARIANCE_DERIVED_COMPLETE"
FAIL = "FULLJ_LOCAL_WEYL_COVARIANCE_ALGEBRAIC_FAIL"
EXPECTED_BACKGROUNDS = 27
WEYL_SCALE = 2.0
ALG_GATE = 1.0e-12
NODE_Z = 0.25
NODE_K = 0.60


def rel_norm(a, b) -> float:
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(aa), np.linalg.norm(bb), 1.0e-300))


def covariance_probe(Kw: np.ndarray, variances: np.ndarray):
    v = np.asarray(variances, float)
    pos = v[v > 0.0]
    if pos.size == 0 or np.any(~np.isfinite(v)) or np.any(v < 0.0):
        raise RuntimeError("invalid tangent-coordinate covariance variances")
    v = v / float(np.median(pos))
    Cs = np.diag(v)
    Cw = Kw @ Cs @ Kw.conj().T
    herm = rel_norm(Cw, Cw.conj().T)
    H = 0.5 * (Cw + Cw.conj().T)
    eig = np.linalg.eigvalsh(H)
    eig_scale = max(float(np.max(np.abs(eig))), 1.0e-300)
    min_eig_rel = float(np.min(eig) / eig_scale)
    pw = np.real(np.diag(H))
    pdiag = np.abs(np.diag(Kw)) ** 2 * v
    if np.any(~np.isfinite(pw)) or np.any(~np.isfinite(pdiag)):
        raise RuntimeError("non-finite covariance output")
    ratio = pw / np.maximum(pdiag, 1.0e-300)
    off = 1.0 - pdiag / np.maximum(pw, 1.0e-300)
    return {
        "input_variance_normalized": v,
        "Cw": Cw,
        "hermiticity_relative_residual": herm,
        "min_eigenvalue_relative": min_eig_rel,
        "P_full": pw,
        "P_diag": pdiag,
        "full_to_diag_power_ratio": ratio,
        "offdiag_power_fraction": off,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--jacobian-json",
        default="results/fullj_mode_coupling_jacobian.json",
    )
    ap.add_argument(
        "--json-out",
        default="results/fullj_local_weyl_covariance.json",
    )
    ap.add_argument(
        "--csv-out",
        default="results/fullj_local_weyl_covariance_summary.csv",
    )
    ap.add_argument(
        "--npz-out",
        default="results/fullj_local_weyl_covariance.npz",
    )
    args = ap.parse_args()

    src = Path(args.jacobian_json)
    if not src.exists():
        raise FileNotFoundError(src)
    locked = json.loads(src.read_text())
    if locked.get("classification") != LOCKED_CLASSIFICATION:
        raise RuntimeError("input is not the locked full-J Jacobian result")
    if not bool(locked.get("diagnostic_complete", False)):
        raise RuntimeError("locked Jacobian diagnostic is incomplete")
    records = list(locked.get("records", []))
    if len(records) != EXPECTED_BACKGROUNDS:
        raise RuntimeError(f"expected {EXPECTED_BACKGROUNDS} records, got {len(records)}")

    k = np.asarray(locked["k_Mpc"], float)
    inode = int(np.argmin(np.abs(k - NODE_K)))
    if abs(float(k[inode]) - NODE_K) > 1.0e-12:
        raise RuntimeError("node k missing from locked grid")

    rows = []
    matrices = []
    health = True
    all_unit_ratio = []
    all_unit_off = []
    all_shape_ratio = []
    all_shape_off = []
    node_unit_ratio = []
    node_unit_off = []
    node_shape_ratio = []
    node_shape_off = []
    max_herm = 0.0
    min_eig_rel = math.inf

    for rec in records:
        Kr = np.asarray(rec["K_real"], float)
        Ki = np.asarray(rec["K_imag"], float)
        if Kr.shape != (len(k), len(k)) or Ki.shape != Kr.shape:
            raise RuntimeError(f"bad matrix shape for {rec.get('label')}")
        Kphi = Kr + 1j * Ki
        Kw = WEYL_SCALE * Kphi
        amps = np.asarray([x["abs_rhs_mode"] for x in rec["raw_mode_response"]], float)
        if amps.shape != (len(k),):
            raise RuntimeError(f"bad source-amplitude shape for {rec.get('label')}")

        probes = {
            "unit": covariance_probe(Kw, np.ones(len(k), float)),
            "frozen_shape": covariance_probe(Kw, amps * amps),
        }
        matrices.append([probes["unit"]["Cw"], probes["frozen_shape"]["Cw"]])

        for name, p in probes.items():
            max_herm = max(max_herm, float(p["hermiticity_relative_residual"]))
            min_eig_rel = min(min_eig_rel, float(p["min_eigenvalue_relative"]))
            ok = bool(
                p["hermiticity_relative_residual"] <= ALG_GATE
                and p["min_eigenvalue_relative"] >= -ALG_GATE
                and np.all(p["P_full"] >= -ALG_GATE * max(float(np.max(p["P_full"])), 1.0))
            )
            health = health and ok
            ratio = np.asarray(p["full_to_diag_power_ratio"], float)
            off = np.asarray(p["offdiag_power_fraction"], float)
            if name == "unit":
                all_unit_ratio.extend(ratio.tolist())
                all_unit_off.extend(off.tolist())
            else:
                all_shape_ratio.extend(ratio.tolist())
                all_shape_off.extend(off.tolist())

            z = float(rec["z"])
            if abs(z - NODE_Z) < 1.0e-12:
                if name == "unit":
                    node_unit_ratio.append(float(ratio[inode]))
                    node_unit_off.append(float(off[inode]))
                else:
                    node_shape_ratio.append(float(ratio[inode]))
                    node_shape_off.append(float(off[inode]))

            rows.append({
                "label": rec["label"],
                "z": z,
                "kind": rec["kind"],
                "beta0": float(rec["beta0"]),
                "probe": name,
                "hermiticity_relative_residual": float(p["hermiticity_relative_residual"]),
                "min_eigenvalue_relative": float(p["min_eigenvalue_relative"]),
                "power_ratio_min": float(np.min(ratio)),
                "power_ratio_median": float(np.median(ratio)),
                "power_ratio_max": float(np.max(ratio)),
                "offdiag_fraction_min": float(np.min(off)),
                "offdiag_fraction_median": float(np.median(off)),
                "offdiag_fraction_max": float(np.max(off)),
                "node_k0p6_power_ratio": float(ratio[inode]) if abs(z-NODE_Z) < 1.0e-12 else math.nan,
                "node_k0p6_offdiag_fraction": float(off[inode]) if abs(z-NODE_Z) < 1.0e-12 else math.nan,
            })

    def stats(x):
        a = np.asarray(x, float)
        return {
            "min": float(np.min(a)),
            "median": float(np.median(a)),
            "max": float(np.max(a)),
        }

    classification = COMPLETE if health else FAIL
    summary = {
        "backgrounds": len(records),
        "tangent_coordinates": len(k),
        "algebraic_gate": ALG_GATE,
        "max_hermiticity_relative_residual": max_herm,
        "min_covariance_eigenvalue_relative": min_eig_rel,
        "unit_full_to_diag_power_ratio": stats(all_unit_ratio),
        "unit_offdiag_power_fraction": stats(all_unit_off),
        "frozen_shape_full_to_diag_power_ratio": stats(all_shape_ratio),
        "frozen_shape_offdiag_power_fraction": stats(all_shape_off),
        "z0p25_k0p6_unit_full_to_diag_power_ratio": stats(node_unit_ratio),
        "z0p25_k0p6_unit_offdiag_power_fraction": stats(node_unit_off),
        "z0p25_k0p6_frozen_shape_full_to_diag_power_ratio": stats(node_shape_ratio),
        "z0p25_k0p6_frozen_shape_offdiag_power_fraction": stats(node_shape_off),
    }

    result = {
        "classification": classification,
        "input_classification": LOCKED_CLASSIFICATION,
        "weyl_convention": "W=Phi+Psi; static snapshot Psi=Phi so K_W=2*K_Phi",
        "covariance_basis": "13 certified phase-aligned real tangent directions",
        "probes": {
            "unit": "C_S proportional to identity in tangent coordinates",
            "frozen_shape": "C_S diagonal with variance proportional to locked |S_j|^2; global normalization removed",
        },
        "summary": summary,
        "records": rows,
        "static_snapshot_only": True,
        "phase_aligned_tangent_basis_only": True,
        "cosmological_random_phase_ensemble": False,
        "evolving_flrw_weyl_power_licensed": False,
        "act_likelihood_used": False,
        "act_likelihood_licensed": False,
        "observational_claim_licensed": False,
    }

    jout = Path(args.json_out)
    cout = Path(args.csv_out)
    nout = Path(args.npz_out)
    for p in (jout, cout, nout):
        p.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    with cout.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    marr = np.asarray(matrices, complex)  # background, probe(unit/frozen), kout, kin-cov-index
    np.savez_compressed(
        nout,
        k_Mpc=k,
        labels=np.asarray([r["label"] for r in records], dtype="U64"),
        probe_names=np.asarray(["unit", "frozen_shape"], dtype="U32"),
        C_W_real=marr.real,
        C_W_imag=marr.imag,
    )

    print("FULLJ_LOCAL_WEYL_COV_SUMMARY " + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_LOCAL_WEYL_COV_CLASSIFICATION=" + classification, flush=True)
    print("STATIC_SNAPSHOT_ONLY=True", flush=True)
    print("PHASE_ALIGNED_TANGENT_BASIS_ONLY=True", flush=True)
    print("COSMOLOGICAL_RANDOM_PHASE_ENSEMBLE=False", flush=True)
    print("EVOLVING_FLRW_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_LOCAL_WEYL_COV_JSON=" + str(jout), flush=True)
    print("FULLJ_LOCAL_WEYL_COV_CSV=" + str(cout), flush=True)
    print("FULLJ_LOCAL_WEYL_COV_NPZ=" + str(nout), flush=True)
    return 0 if health else 1


if __name__ == "__main__":
    raise SystemExit(main())
