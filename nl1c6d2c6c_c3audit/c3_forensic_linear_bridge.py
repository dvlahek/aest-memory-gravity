#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6c import r3_modewise_full_prehistory as r3

c = r3.c
FIELDS = ("alpha", "E", "chi")
Z = c.m.CHECK_Z.copy()


def rel_l2(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(bb), 1e-300))


def project_modes(fields, design):
    out = np.empty((fields.shape[0], design.shape[1]), float)
    for i, row in enumerate(fields):
        out[i] = np.linalg.lstsq(design, row, rcond=None)[0]
    return out


def point_rel(a, b, trajectory_ref):
    floor = 1e-12 * max(float(np.max(np.abs(trajectory_ref))), 1e-300)
    return float(abs(a - b) / max(abs(b), floor, 1e-300))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", required=True)
    ap.add_argument("--json-out", default="results/c3_forensic_linear_bridge.json")
    args = ap.parse_args()

    ref = np.load(args.reference)
    if not np.allclose(ref["z"], Z, rtol=0.0, atol=1e-12):
        raise RuntimeError("C3 forensic reference checkpoint mismatch")
    if not np.allclose(ref["k_mpc"], c.m.K_MPC, rtol=0.0, atol=1e-13):
        raise RuntimeError("C3 forensic reference k-grid mismatch")

    data = c.m.prepare_class_data()
    run = c.integrate(
        data,
        128,
        4096,
        None,
        orders=(39,),
        nonlinear=False,
        pre_cache=None,
    )
    if not run.get("finite", False):
        raise RuntimeError(f"offline linear control nonfinite: {run.get('fail_reason')}")

    C = c.m.cos_matrix(128)
    design = C.T
    coeff_test = np.asarray([0.71, -0.53, 0.31, -0.17, 0.11, -0.07], float)
    recovered = np.linalg.lstsq(design, design @ coeff_test, rcond=None)[0]
    reconstruction_error = rel_l2(recovered, coeff_test)
    reconstruction_pass = reconstruction_error <= 1e-12
    print(
        f"RECONSTRUCTION_AUDIT relative_L2={reconstruction_error:.12e} "
        f"pass={reconstruction_pass}",
        flush=True,
    )
    if not reconstruction_pass:
        report = {
            "classification": "C3_FORENSIC_LINEAR_BRIDGE_INCOMPLETE",
            "reconstruction_relative_L2": reconstruction_error,
        }
        Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        return 3

    rr = run["orders"][39]
    offline_fields = {
        "alpha": np.asarray(rr["states"][:, 0, :], float),
        "E": np.asarray(rr["E"], float),
        "chi": np.asarray(rr["states"][:, 1, :], float),
    }
    offline = {k: project_modes(v, design) for k, v in offline_fields.items()}

    ref_alpha = np.asarray(ref["alpha"], float)
    ref_E = np.asarray(ref["E"], float)
    ref_theta = np.asarray(ref["theta"], float)
    ref_chi = np.empty_like(ref_alpha)
    for i, tau in enumerate(data["tau_check"]):
        a, _, Q = c.m.bg_eval(data, float(tau))[:3]
        ref_chi[i] = Q * (
            a * ref_theta[i] / (c.m.K_MPC * c.m.K_MPC) + ref_alpha[i]
        )
    refs = {"alpha": ref_alpha, "E": ref_E, "chi": ref_chi}

    checkpoint = []
    for i, z in enumerate(Z):
        row = {"z": float(z)}
        vals = []
        for field in FIELDS:
            err = rel_l2(offline[field][i], refs[field][i])
            row[field] = err
            vals.append(f"{field}={err:.12e}")
        checkpoint.append(row)
        print(f"CHECKPOINT z={z:g} " + " ".join(vals), flush=True)

    mode_rows = []
    field_summary = {}
    field_flags = {}
    for field in FIELDS:
        scales = []
        scaled_resids = []
        for j, k in enumerate(c.m.K_MPC):
            off = offline[field][:, j]
            refj = refs[field][:, j]
            denom = float(np.dot(refj, refj))
            scale = float(np.dot(off, refj) / max(denom, 1e-300))
            scaled_resid = float(
                np.linalg.norm(off - scale * refj) / max(np.linalg.norm(refj), 1e-300)
            )
            full_rel = rel_l2(off, refj)
            z6_rel = point_rel(off[0], refj[0], refj)
            threshold = 1e-12 * max(float(np.max(np.abs(refj))), 1e-300)
            ratio_z6 = float(off[0] / refj[0]) if abs(refj[0]) > threshold else None
            scales.append(scale)
            scaled_resids.append(scaled_resid)
            row = {
                "field": field,
                "mode_index": int(j),
                "k_mpc": float(k),
                "z6_relative_error": z6_rel,
                "full_relative_L2": full_rel,
                "scale": scale,
                "scaled_residual": scaled_resid,
                "ratio_z6": ratio_z6,
                "offline": off.tolist(),
                "reference": refj.tolist(),
            }
            mode_rows.append(row)
            ratio_txt = "nan" if ratio_z6 is None else f"{ratio_z6:.12e}"
            print(
                f"MODE field={field} i={j} k_mpc={k:.12e} "
                f"z6_rel={z6_rel:.12e} full_rel={full_rel:.12e} "
                f"scale={scale:.12e} scaled_resid={scaled_resid:.12e} "
                f"ratio_z6={ratio_txt}",
                flush=True,
            )

        scales = np.asarray(scales, float)
        scaled_resids = np.asarray(scaled_resids, float)
        z6 = checkpoint[0][field]
        z02 = checkpoint[-1][field]
        summary = {
            "scale_median": float(np.median(scales)),
            "scale_spread": float(np.max(scales) - np.min(scales)),
            "max_scaled_residual": float(np.max(scaled_resids)),
            "z6_aggregate_error": float(z6),
            "z02_aggregate_error": float(z02),
        }
        flags = {
            "EARLY_OFFSET": bool(z6 > 0.03),
            "POST_Z6_GROWTH": bool(z6 <= 0.01 and z02 > 0.03),
            "MULTIPLICATIVE_COMPATIBLE": bool(
                summary["max_scaled_residual"] <= 5e-3
                and summary["scale_spread"] <= 1e-2
            ),
        }
        field_summary[field] = summary
        field_flags[field] = flags
        print(
            f"FIELD field={field} scale_median={summary['scale_median']:.12e} "
            f"scale_spread={summary['scale_spread']:.12e} "
            f"max_scaled_resid={summary['max_scaled_residual']:.12e} "
            f"z6={z6:.12e} z0p2={z02:.12e} "
            f"EARLY_OFFSET={flags['EARLY_OFFSET']} "
            f"POST_Z6_GROWTH={flags['POST_Z6_GROWTH']} "
            f"MULTIPLICATIVE_COMPATIBLE={flags['MULTIPLICATIVE_COMPATIBLE']}",
            flush=True,
        )

    medians = [field_summary[f]["scale_median"] for f in FIELDS]
    common_scale = bool(
        all(field_flags[f]["MULTIPLICATIVE_COMPATIBLE"] for f in FIELDS)
        and max(medians) - min(medians) <= 1e-2
    )
    print(f"COMMON_SCALE_COMPATIBLE={common_scale}", flush=True)

    report = {
        "classification": "C3_FORENSIC_LINEAR_BRIDGE_COMPLETE",
        "historical_d2c6c_r3_remains_fail": True,
        "finite_positive_eta_licensed": False,
        "reconstruction_relative_L2": reconstruction_error,
        "checkpoint": checkpoint,
        "modes": mode_rows,
        "field_summary": field_summary,
        "field_flags": field_flags,
        "common_scale_compatible": common_scale,
        "z": Z.tolist(),
        "k_mpc": c.m.K_MPC.tolist(),
    }
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("CLASSIFICATION=C3_FORENSIC_LINEAR_BRIDGE_COMPLETE", flush=True)
    print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
