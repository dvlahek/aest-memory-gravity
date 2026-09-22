#!/usr/bin/env python3
"""GE19 Repair26 — cancellation-free full-history first-order bath boundary.

This diagnostic/certification run generates full-history eta=0 accepted-source
traces with the already certified GE15 exact state s=chi/Q, reconstructs the
retarded normalized first-order bath boundary at a=0.4, and checks R1/R2 plus
quadrature closure. It does not run q20 and does not license H4/Z21 unless a
later separately preregistered step succeeds.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import v063.theory_response_map as v63
import ge09.repair01_dense_accepted_step_local_jet_bridge as g9
import nl1c4.expanding_memory_source_trajectory as c4
import ge19.repair07_window_retarded_reduced_h3_z20_particular as r7

A0 = 0.4
NQ_PRIMARY = 2048
NQ_CONTROL = 1024
TINY = 1.0e-300

LEVELS = {
    "R1": ROOT / "ge11" / "pre" / "R1_repair01.pre",
    "R2": ROOT / "ge11" / "pre" / "R2_repair01.pre",
}

K_REL_MAX = 1.0e-12
TIME_REL_MAX = 1.0e-12
TARGET_A_MAX = 1.0e-15
X0_POINT_MAX = 2.0e-3
BOUNDARY_GL2_MAX = 5.0e-3
QUAD_GL2_MAX = 5.0e-3


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def rel_l2(a, b) -> float:
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(aa), np.linalg.norm(bb), TINY))


def aor(a, b) -> float:
    aa = np.asarray(a)
    bb = np.asarray(b)
    ae = np.abs(aa - bb)
    re = ae / np.maximum(np.maximum(np.abs(aa), np.abs(bb)), TINY)
    return float(np.max(np.minimum(ae, re)))


def run_level(class_root: Path, results: Path, tag: str, pre: Path):
    trace = results / f"ge19_repair26_{tag}_full_history_trace.dat"
    dense = results / f"ge19_repair26_{tag}_dense_accepted_step_trace.dat"
    log = results / f"ge19_repair26_{tag}_class.log"
    prefix = results / f"ge19_repair26_{tag}_cli"

    for p in (trace, dense, log):
        if p.exists():
            p.unlink()

    ini = class_root / f"ge19_repair26_{tag}.ini"
    text = v63.rewrite_ini(v63.BASE.read_text(), str(prefix))
    text = text.replace("lensing = yes", "lensing = no")
    text += "k_output_values = " + ", ".join(f"{k:.17g}" for k in g9.K_REQ) + "\n"
    ini.write_text(text)

    env = os.environ.copy()
    env["AEST_OFFLINE_TRACE_FILE"] = str(trace.resolve())
    env["AEST_DENSE_JET_TRACE_FILE"] = str(dense.resolve())
    env.pop("AEST_FULL_STATE_TRACE_FILE", None)
    env.pop("AEST_TANGENT_FORCE_FILE", None)
    env.pop("AEST_TANGENT_LAMBDA", None)
    env["OMP_NUM_THREADS"] = "1"

    with log.open("w") as fh:
        subprocess.run(
            [str(class_root / "class"), ini.name, str(pre.resolve())],
            cwd=class_root,
            env=env,
            stdout=fh,
            stderr=subprocess.STDOUT,
            check=True,
        )

    if not trace.exists() or trace.stat().st_size == 0:
        raise RuntimeError(f"{tag}: full-history trace not produced")
    if not dense.exists() or dense.stat().st_size == 0:
        raise RuntimeError(f"{tag}: dense accepted-step trace not produced")

    return {
        "trace": trace,
        "dense": dense,
        "log": log,
    }


def grad_factors():
    amps, _, _ = r7.amplitudes()
    return np.asarray([
        0.5 * float(amps[i]) * np.exp(1j * float(r7.PHASES[i])) * (1j * float(g9.K_REQ[i]))
        for i in range(len(g9.K_REQ))
    ], dtype=complex)


def dense_reference(dense: Path):
    rows = g9.read_table(dense)
    modes, kmiss = g9.group_modes(rows)
    interps = [g9.build_interps(m) for m in modes]
    x0 = math.log(A0)
    scalar = np.empty(len(g9.K_REQ), dtype=float)
    q0 = np.empty_like(scalar)

    for i, k in enumerate(g9.K_REQ):
        st = g9.eval_state(interps[i], np.asarray([x0], dtype=float))
        Q = float(st["Q"][0])
        alpha = float(st["alpha_aest"][0])
        theta = float(st["theta_dark"][0])
        chi = Q * (A0 * theta / (float(k) * float(k)) + alpha)
        scalar[i] = chi / A0
        q0[i] = Q

    gf = grad_factors()
    return {
        "scalar": scalar,
        "X": gf * scalar,
        "Q": q0,
        "k_relative_miss": float(kmiss),
        "rows": len(rows),
    }


def trace_boundary(trace: Path, order: int):
    rows = c4.read_trace(trace)
    histories, kmiss, tmiss = c4.select_and_align(rows)
    aa = np.asarray([q["a"] for q in histories[0]], dtype=float)

    lo = max([j for j, a in enumerate(aa) if a <= A0], default=None)
    hi = min([j for j, a in enumerate(aa) if a >= A0], default=None)
    if lo is None or hi is None or lo == hi:
        raise RuntimeError("cancellation-free full-history trace does not bracket a=0.4")

    Nlo = math.log(float(aa[lo]))
    Nhi = math.log(float(aa[hi]))
    Nt = math.log(A0)
    frac = (Nt - Nlo) / (Nhi - Nlo)
    if not 0.0 < frac < 1.0:
        raise RuntimeError("invalid a=0.4 partial-step fraction")

    target_a = math.exp(Nlo + frac * (Nhi - Nlo))
    target_mismatch = abs(target_a - A0)
    if target_mismatch > TARGET_A_MAX:
        raise RuntimeError(f"a=0.4 reconstruction mismatch {target_mismatch}")

    gf = grad_factors()
    z0 = np.empty((order, len(g9.K_REQ)), dtype=complex)
    v0 = np.empty_like(z0)
    trace_X0 = np.empty(len(g9.K_REQ), dtype=complex)
    trace_scalar0 = np.empty(len(g9.K_REQ), dtype=float)
    trace_Q0 = np.empty(len(g9.K_REQ), dtype=float)
    r_ref = w_ref = None

    for im, hist in enumerate(histories):
        rr, ww, qs, vs = c4.integrate_mode(hist[: lo + 1], order)
        rr = np.asarray(rr, dtype=float)
        ww = np.asarray(ww, dtype=float)
        if r_ref is None:
            r_ref = rr
            w_ref = ww
        elif aor(r_ref, rr) > 1.0e-14 or aor(w_ref, ww) > 1.0e-14:
            raise RuntimeError("quadrature nodes changed between modes")

        xlo = float(hist[lo]["chi"] / hist[lo]["a"])
        xhi = float(hist[hi]["chi"] / hist[hi]["a"])
        xt = xlo + frac * (xhi - xlo)

        qlo = float(hist[lo]["Q"])
        qhi = float(hist[hi]["Q"])
        qt_trace = qlo + frac * (qhi - qlo)

        hlo = float(hist[lo]["H_over_H0"]) * c4.TAUH0
        hhi = float(hist[hi]["H_over_H0"]) * c4.TAUH0
        hm = math.sqrt(hlo * hhi)
        dxi = (Nt - Nlo) / hm

        qt, vt = c4.step_linear(
            np.asarray(qs[-1], dtype=float),
            np.asarray(vs[-1], dtype=float),
            rr,
            hm,
            xlo,
            xt,
            dxi,
        )
        z0[:, im] = gf[im] * np.asarray(qt, dtype=float)
        v0[:, im] = gf[im] * np.asarray(vt, dtype=float)
        trace_X0[im] = gf[im] * xt
        trace_scalar0[im] = xt
        trace_Q0[im] = qt_trace

    return {
        "r": r_ref,
        "w": w_ref,
        "z0": z0,
        "v0": v0,
        "trace_X0": trace_X0,
        "trace_scalar0": trace_scalar0,
        "trace_Q0": trace_Q0,
        "k_relative_miss": float(kmiss),
        "common_time_relative_mismatch": float(tmiss),
        "n_history_nodes": len(histories[0]),
        "a_first": float(aa[0]),
        "a_last": float(aa[-1]),
        "trace_lo_a": float(aa[lo]),
        "trace_hi_a": float(aa[hi]),
        "partial_step_fraction_ln_a": float(frac),
        "target_a_abs_mismatch": float(target_mismatch),
    }


def finite_all(*arrs) -> bool:
    return bool(all(np.all(np.isfinite(np.asarray(x))) for x in arrs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--class-root", required=True)
    ap.add_argument("--results-dir", default=str(ROOT / "results"))
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--npz-out", required=True)
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    results = Path(args.results_dir).resolve()
    results.mkdir(parents=True, exist_ok=True)
    out_json = Path(args.json_out)
    out_npz = Path(args.npz_out)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    patch_report = results / "ge15_s_state_patch.json"
    if not patch_report.exists():
        raise RuntimeError("missing GE15 patch report")
    patch = json.loads(patch_report.read_text())
    patch_pass = bool(
        patch.get("classification") == "GE15_CANCELLATION_FREE_S_STATE_PATCH_PASS"
        and patch.get("physics_modified") is False
        and patch.get("state_dimension_modified") is False
        and patch.get("initial_s") == 0.0
        and all(patch.get("checks", {}).values())
    )
    if not patch_pass:
        raise RuntimeError("GE15 cancellation-free state patch audit failed")

    generated = {tag: run_level(class_root, results, tag, pre) for tag, pre in LEVELS.items()}
    dense = {tag: dense_reference(generated[tag]["dense"]) for tag in LEVELS}

    b = {}
    for tag in LEVELS:
        b[(tag, NQ_PRIMARY)] = trace_boundary(generated[tag]["trace"], NQ_PRIMARY)
    b[("R1", NQ_CONTROL)] = trace_boundary(generated["R1"]["trace"], NQ_CONTROL)

    r1 = b[("R1", NQ_PRIMARY)]
    r2 = b[("R2", NQ_PRIMARY)]
    r1c = b[("R1", NQ_CONTROL)]

    x0_r1_dense = aor(r1["trace_X0"], dense["R1"]["X"])
    x0_r2_dense = aor(r2["trace_X0"], dense["R2"]["X"])
    x0_r1_r2 = aor(r1["trace_X0"], r2["trace_X0"])
    dense_r1_r2 = rel_l2(dense["R1"]["X"], dense["R2"]["X"])

    z_r1_r2 = rel_l2(r1["z0"], r2["z0"])
    v_r1_r2 = rel_l2(r1["v0"], r2["v0"])

    wz1 = np.einsum("b,bm->m", r1["w"], r1["z0"], optimize=True)
    wv1 = np.einsum("b,bm->m", r1["w"], r1["v0"], optimize=True)
    wzc = np.einsum("b,bm->m", r1c["w"], r1c["z0"], optimize=True)
    wvc = np.einsum("b,bm->m", r1c["w"], r1c["v0"], optimize=True)
    z_quad = rel_l2(wz1, wzc)
    v_quad = rel_l2(wv1, wvc)

    k_miss = max(
        dense["R1"]["k_relative_miss"],
        dense["R2"]["k_relative_miss"],
        r1["k_relative_miss"],
        r2["k_relative_miss"],
        r1c["k_relative_miss"],
    )
    time_miss = max(
        r1["common_time_relative_mismatch"],
        r2["common_time_relative_mismatch"],
        r1c["common_time_relative_mismatch"],
    )
    target_miss = max(
        r1["target_a_abs_mismatch"],
        r2["target_a_abs_mismatch"],
        r1c["target_a_abs_mismatch"],
    )

    all_finite = finite_all(
        dense["R1"]["X"], dense["R2"]["X"],
        r1["z0"], r1["v0"], r2["z0"], r2["v0"],
        r1c["z0"], r1c["v0"], wz1, wv1, wzc, wvc,
    )

    gates = {
        "GE15_patch_report_pass": patch_pass,
        "requested_k_relative_miss_le_1e12": bool(k_miss <= K_REL_MAX),
        "common_time_relative_mismatch_le_1e12": bool(time_miss <= TIME_REL_MAX),
        "both_R1_R2_full_history_traces_bracket_a0": bool(
            r1["a_first"] < A0 < r1["a_last"] and r2["a_first"] < A0 < r2["a_last"]
        ),
        "trace_a0_target_reconstruction_abs_le_1e15": bool(target_miss <= TARGET_A_MAX),
        "GE15_dense_X0_R1_trace_abs_or_rel_le_2e3": bool(x0_r1_dense <= X0_POINT_MAX),
        "GE15_dense_X0_R2_trace_abs_or_rel_le_2e3": bool(x0_r2_dense <= X0_POINT_MAX),
        "R1_R2_trace_X0_abs_or_rel_le_2e3": bool(x0_r1_r2 <= X0_POINT_MAX),
        "R1_R2_full_z10_boundary_relative_L2_le_5e3": bool(z_r1_r2 <= BOUNDARY_GL2_MAX),
        "R1_R2_full_v10_boundary_relative_L2_le_5e3": bool(v_r1_r2 <= BOUNDARY_GL2_MAX),
        "Nq1024_Nq2048_weighted_z10_boundary_relative_L2_le_5e3": bool(z_quad <= QUAD_GL2_MAX),
        "Nq1024_Nq2048_weighted_v10_boundary_relative_L2_le_5e3": bool(v_quad <= QUAD_GL2_MAX),
        "all_outputs_finite": all_finite,
    }

    trace_keys = [
        "requested_k_relative_miss_le_1e12",
        "common_time_relative_mismatch_le_1e12",
        "both_R1_R2_full_history_traces_bracket_a0",
        "trace_a0_target_reconstruction_abs_le_1e15",
        "GE15_dense_X0_R1_trace_abs_or_rel_le_2e3",
        "GE15_dense_X0_R2_trace_abs_or_rel_le_2e3",
        "R1_R2_trace_X0_abs_or_rel_le_2e3",
    ]
    bath_keys = [
        "R1_R2_full_z10_boundary_relative_L2_le_5e3",
        "R1_R2_full_v10_boundary_relative_L2_le_5e3",
        "Nq1024_Nq2048_weighted_z10_boundary_relative_L2_le_5e3",
        "Nq1024_Nq2048_weighted_v10_boundary_relative_L2_le_5e3",
        "all_outputs_finite",
    ]

    if not all(gates[k] for k in trace_keys):
        route = "CANCELLATION_FREE_TRACE_PRECISION_CLOSURE_FAIL"
    elif not all(gates[k] for k in bath_keys):
        route = "CANCELLATION_FREE_RETARDED_BATH_BOUNDARY_NOT_CLOSED"
    else:
        route = "CANCELLATION_FREE_FULL_HISTORY_BATH_BOUNDARY_CERTIFIED"

    passed = bool(route == "CANCELLATION_FREE_FULL_HISTORY_BATH_BOUNDARY_CERTIFIED")
    classification = (
        "GE19_REPAIR26_CANCELLATION_FREE_FULL_HISTORY_BATH_BOUNDARY_PASS"
        if passed else
        "GE19_REPAIR26_CANCELLATION_FREE_FULL_HISTORY_BATH_BOUNDARY_FAIL"
    )

    file_hashes = {}
    for tag in LEVELS:
        for key in ("trace", "dense", "log"):
            p = generated[tag][key]
            file_hashes[f"{tag}_{key}"] = {
                "sha256": sha256(p),
                "bytes": p.stat().st_size,
                "path": str(p.relative_to(ROOT)),
            }

    result = {
        "classification": classification,
        "predata_classification": "GE19_REPAIR26_PREDATA_CANCELLATION_FREE_FULL_HISTORY_BATH_BOUNDARY_RECONSTRUCTION",
        "route": route,
        "uses_observational_data": False,
        "diagnostic_and_boundary_certification_only": True,
        "physics_modified": False,
        "legacy_v077_rescaled": False,
        "repair25_fitted_normalization_used": False,
        "construction": {
            "internal_state": "s=chi/Q",
            "physical_alpha": "s-a theta/k^2",
            "physical_chi": "Q*s",
            "initial_s": 0.0,
            "trace_grid": "CLASS perturbations_sources accepted source-sampling grid",
            "a_boundary": A0,
            "quadrature_primary": NQ_PRIMARY,
            "quadrature_control": NQ_CONTROL,
            "primary_downstream_trace": "R1",
        },
        "provenance": {
            "generated_files": file_hashes,
            "GE15_patch_report": patch,
        },
        "trace_boundary": {
            "R1": {k: v for k, v in r1.items() if k not in ("r","w","z0","v0","trace_X0","trace_scalar0","trace_Q0")},
            "R2": {k: v for k, v in r2.items() if k not in ("r","w","z0","v0","trace_X0","trace_scalar0","trace_Q0")},
            "R1_trace_X0_vs_GE15_dense_abs_or_rel_max": x0_r1_dense,
            "R2_trace_X0_vs_GE15_dense_abs_or_rel_max": x0_r2_dense,
            "R1_vs_R2_trace_X0_abs_or_rel_max": x0_r1_r2,
            "R1_vs_R2_GE15_dense_X0_relative_L2": dense_r1_r2,
            "R1_trace_scalar_chi_over_a_at_a0": r1["trace_scalar0"].tolist(),
            "R2_trace_scalar_chi_over_a_at_a0": r2["trace_scalar0"].tolist(),
            "R1_GE15_dense_scalar_chi_over_a_at_a0": dense["R1"]["scalar"].tolist(),
            "R2_GE15_dense_scalar_chi_over_a_at_a0": dense["R2"]["scalar"].tolist(),
            "R1_trace_Q_at_a0": r1["trace_Q0"].tolist(),
            "R2_trace_Q_at_a0": r2["trace_Q0"].tolist(),
        },
        "retarded_bath_boundary": {
            "R1_vs_R2_full_z10_relative_L2": z_r1_r2,
            "R1_vs_R2_full_v10_relative_L2": v_r1_r2,
            "R1_Nq1024_vs_Nq2048_weighted_z10_relative_L2": z_quad,
            "R1_Nq1024_vs_Nq2048_weighted_v10_relative_L2": v_quad,
        },
        "gates": gates,
        "next_step": (
            "Separately preregister a q20 reconstruction rerun using only the frozen Repair26 R1 cancellation-free full-history trace/boundary."
            if passed else
            "Do not rerun q20; localize the failing Repair26 trace or retarded-boundary closure first."
        ),
        "q20_rerun_performed": False,
        "q20_certified": False,
        "Z21_licensed": False,
        "claim_boundary": "Repair26 can certify only the cancellation-free full-history first-order bath parent and its retarded z10/v10 boundary. It does not certify q20 or H4/Z21.",
    }

    out_json.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    np.savez_compressed(
        out_npz,
        k_Mpc=g9.K_REQ,
        k_h_Mpc=g9.K_H,
        r_primary=r1["r"],
        w_primary=r1["w"],
        R1_z10_boundary=r1["z0"],
        R1_v10_boundary=r1["v0"],
        R2_z10_boundary=r2["z0"],
        R2_v10_boundary=r2["v0"],
        R1_trace_X0=r1["trace_X0"],
        R2_trace_X0=r2["trace_X0"],
        R1_GE15_dense_X0=dense["R1"]["X"],
        R2_GE15_dense_X0=dense["R2"]["X"],
        R1_weighted_z10=wz1,
        R1_weighted_v10=wv1,
        R1_control_weighted_z10=wzc,
        R1_control_weighted_v10=wvc,
    )

    print(json.dumps(result, indent=2, allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({
            "classification": "GE19_REPAIR26_IMPLEMENTATION_FAIL",
            "error": repr(exc),
            "q20_rerun_performed": False,
            "q20_certified": False,
            "Z21_licensed": False,
        }, indent=2))
        raise
