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
m = c.m


def fit_scale(ref: np.ndarray, off: np.ndarray) -> dict:
    ref = np.asarray(ref, float).ravel()
    off = np.asarray(off, float).ravel()
    nr = float(np.linalg.norm(ref))
    no = float(np.linalg.norm(off))
    dot = float(np.dot(ref, off))
    s = dot / max(float(np.dot(ref, ref)), 1e-300)
    inv = dot / max(float(np.dot(off, off)), 1e-300)
    resid = float(np.linalg.norm(off - s * ref) / max(no, 1e-300))
    cosine = dot / max(nr * no, 1e-300)
    return {
        "scale_class_to_offline": float(s),
        "scale_offline_to_class": float(inv),
        "cosine": float(cosine),
        "scaled_shape_residual_vs_offline": float(resid),
        "ref_norm": nr,
        "offline_norm": no,
    }


def modal_projection_matrix(nx: int = 128):
    C = m.cos_matrix(nx)
    cols = []
    for j in range(len(m.K_MPC)):
        e = np.zeros(len(m.K_MPC), float)
        e[j] = 1.0
        cols.append(np.asarray(m.to_field(e, C), float))
    B = np.stack(cols, axis=1)
    rank = int(np.linalg.matrix_rank(B))
    cond = float(np.linalg.cond(B))
    if rank != len(m.K_MPC):
        raise RuntimeError(f"six-mode projection basis rank={rank}")
    return B, rank, cond


def project_rows(rows: np.ndarray, B: np.ndarray) -> np.ndarray:
    return np.stack([np.linalg.lstsq(B, np.asarray(row, float), rcond=None)[0] for row in rows])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", default="results/c3_r5_zero_safe_linear_reference.npz")
    ap.add_argument("--json-out", default="results/c3_r5_scale_sign_audit.json")
    args = ap.parse_args()

    try:
        ref = np.load(args.reference)
        data = m.prepare_class_data()
        pre = {39: c.prehistory(data, 128, 4096, 39)}
        linear_member = {"sigma": 0, "kind": "simple", "beta0": 1.0}
        run = c.integrate(
            data,
            128,
            4096,
            linear_member,
            orders=(39,),
            nonlinear=False,
            pre_cache=pre,
        )
        if not run.get("finite", False):
            raise RuntimeError(f"offline linear tangent nonfinite: {run.get('fail_reason')}")

        B, rank, cond = modal_projection_matrix(128)
        rr = run["orders"][39]
        off_alpha = project_rows(rr["states"][:, 0], B)
        off_E = project_rows(rr["E"], B)
        off_chi = project_rows(rr["states"][:, 1], B)

        ref_alpha = np.asarray(ref["alpha"], float)
        ref_E = np.asarray(ref["E"], float)
        ref_theta = np.asarray(ref["theta"], float)
        ref_chi = np.empty_like(ref_alpha)
        for i, tau in enumerate(data["tau_check"]):
            a, _, Q = m.bg_eval(data, float(tau))[:3]
            ref_chi[i] = Q * (a * ref_theta[i] / (m.K_MPC * m.K_MPC) + ref_alpha[i])

        fields = {
            "alpha": (ref_alpha, off_alpha),
            "E": (ref_E, off_E),
            "chi": (ref_chi, off_chi),
        }
        report = {
            "classification": "C3_R5_POSTDATA_SCALE_SIGN_AUDIT_COMPLETE",
            "historical_r5_classification_unchanged": "C3_R5_ZERO_SAFE_TANGENT_FAIL",
            "finite_positive_eta_licensed": False,
            "projection_basis_rank": rank,
            "projection_basis_condition": cond,
            "fields": {},
        }

        for name, (rarr, oarr) in fields.items():
            global_fit = fit_scale(rarr, oarr)
            modes = []
            for j, kh in enumerate(np.asarray(m.K_H, float) if hasattr(m, "K_H") else np.arange(len(m.K_MPC))):
                fit = fit_scale(rarr[:, j], oarr[:, j])
                fit["mode"] = int(j)
                fit["k_mpc"] = float(m.K_MPC[j])
                modes.append(fit)
                print(
                    f"SCALE_MODE field={name} mode={j} k_mpc={m.K_MPC[j]:.12e} "
                    f"s={fit['scale_class_to_offline']:.12e} "
                    f"inv={fit['scale_offline_to_class']:.12e} "
                    f"cos={fit['cosine']:.12e} "
                    f"resid={fit['scaled_shape_residual_vs_offline']:.12e}",
                    flush=True,
                )
            scales = np.asarray([x["scale_class_to_offline"] for x in modes], float)
            report["fields"][name] = {
                "global": global_fit,
                "modes": modes,
                "scale_min": float(np.min(scales)),
                "scale_max": float(np.max(scales)),
                "scale_spread": float(np.max(scales) - np.min(scales)),
            }
            print(
                f"SCALE_GLOBAL field={name} s={global_fit['scale_class_to_offline']:.12e} "
                f"inv={global_fit['scale_offline_to_class']:.12e} "
                f"cos={global_fit['cosine']:.12e} "
                f"resid={global_fit['scaled_shape_residual_vs_offline']:.12e} "
                f"spread={report['fields'][name]['scale_spread']:.12e}",
                flush=True,
            )

        Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print("CLASSIFICATION=C3_R5_POSTDATA_SCALE_SIGN_AUDIT_COMPLETE", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 0
    except Exception as exc:
        print(f"C3_R5_SCALE_SIGN_ERROR {type(exc).__name__}: {exc}", flush=True)
        print("CLASSIFICATION=C3_R5_POSTDATA_SCALE_SIGN_AUDIT_INCOMPLETE", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
