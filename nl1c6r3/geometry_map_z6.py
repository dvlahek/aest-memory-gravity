#!/usr/bin/env python3
"""Local-only NL1C6R3 z=6 geometry/runtime map.

Diagnostic only.  This file does not alter the production NL1C6R3 equations,
tolerances, continuation rules, gates, or branch selection.  It runs the
existing anchor_route_solve independently for all 3 interpolation families,
3 beta values, and both constitutive anchors at the first native snapshot.
Each route is isolated in a subprocess with a hard wall-clock timeout.

Outputs:
  results/nl1c6r3_geometry_z6.json
  results/nl1c6r3_geometry_z6.csv
  results/nl1c6r3_geometry_z6_logs/*.log
  results/nl1c6r3_geometry_z6_state/*.json
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np

from nl1c6 import full_j_baryonic_reclosure as base
from nl1c6r3 import fixed_source_constitutive_homotopy as r3

KINDS = ("simple", "exponential", "sharp")
BETAS = (1.0, 0.5, 0.1)
ROUTES = ("screened", "mass")


def atomic_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    tmp.replace(path)


def load_first_snapshot(input_npz: str, beta: float):
    d = np.load(input_npz)
    kh = np.asarray(d["k_native_h"], float)
    z = np.asarray(d["z_native"], float)
    db = np.asarray(d["d_b"], float)
    idx, kmiss = base.mode_indices(kh)
    if kmiss > 1e-12:
        raise RuntimeError(f"k-mode mismatch {kmiss}")
    db6 = db[idx, :]
    it = int(np.argmax(z))
    _, source, a = base.source_for(db6[:, it], z[it], base.NX_PRIMARY)
    rhs = source / (1.0 + beta)
    return float(z[it]), float(a), rhs


def worker(args) -> int:
    z, a, rhs = load_first_snapshot(args.input_npz, args.beta)
    progress_path = Path(args.progress_json)
    result_path = Path(args.result_json)

    metrics = {
        "kind": args.kind,
        "beta": float(args.beta),
        "route": args.route,
        "z": z,
        "a": a,
        "status": "RUNNING",
        "fixed_calls": 0,
        "arc_calls": 0,
        "fixed_seconds": 0.0,
        "arc_seconds": 0.0,
        "augmented_gmres_failed_600": 0,
        "augmented_max_iterations": 0,
        "other_arc_failures": 0,
        "min_abs_tt": None,
        "last_theta_pred": None,
        "last_theta": None,
        "last_event": "start",
    }
    t0 = time.perf_counter()

    def checkpoint(event: str):
        metrics["elapsed_seconds"] = float(time.perf_counter() - t0)
        metrics["last_event"] = event
        atomic_json(progress_path, metrics)

    checkpoint("start")
    original_fixed = r3.fixed_theta_solve
    original_corrector = r3.augmented_corrector

    def traced_fixed(rhs_, a_, beta_, kind_, theta_, route_, initial_):
        metrics["fixed_calls"] += 1
        metrics["last_theta"] = float(theta_)
        checkpoint(f"fixed_enter:{float(theta_):.12e}")
        tc = time.perf_counter()
        out = original_fixed(rhs_, a_, beta_, kind_, theta_, route_, initial_)
        dt = time.perf_counter() - tc
        metrics["fixed_seconds"] += float(dt)
        hist = out.get("history", [])
        metrics["last_fixed_reason"] = str(out.get("reason"))
        metrics["last_fixed_residual"] = float(hist[-1]) if hist else None
        checkpoint(f"fixed_exit:{out.get('reason')}")
        return out

    def traced_corrector(rhs_, a_, beta_, kind_, route_, chi_pred_, theta_pred_, ty_, tt_, chi_scale_):
        metrics["arc_calls"] += 1
        metrics["last_theta_pred"] = float(theta_pred_)
        att = abs(float(tt_))
        if metrics["min_abs_tt"] is None or att < metrics["min_abs_tt"]:
            metrics["min_abs_tt"] = att
        checkpoint(f"arc_enter:{metrics['arc_calls']}:theta_pred={float(theta_pred_):.12e}")
        tc = time.perf_counter()
        out = original_corrector(rhs_, a_, beta_, kind_, route_, chi_pred_, theta_pred_, ty_, tt_, chi_scale_)
        dt = time.perf_counter() - tc
        metrics["arc_seconds"] += float(dt)
        metrics["last_theta"] = float(out.get("theta", float("nan")))
        reason = str(out.get("reason"))
        metrics["last_arc_reason"] = reason
        if reason == "augmented_gmres_failed_600":
            metrics["augmented_gmres_failed_600"] += 1
        elif reason == "augmented_max_iterations":
            metrics["augmented_max_iterations"] += 1
        elif not out.get("success", False):
            metrics["other_arc_failures"] += 1
        checkpoint(f"arc_exit:{metrics['arc_calls']}:{reason}")
        return out

    r3.fixed_theta_solve = traced_fixed
    r3.augmented_corrector = traced_corrector
    try:
        out = r3.anchor_route_solve(rhs, a, args.beta, args.kind, base.NX_PRIMARY, args.route)
        summary = out.get("route_summary", {})
        metrics.update({
            "status": "DONE",
            "success": bool(out.get("success", False)),
            "reason": str(out.get("reason")),
            "total_seconds": float(time.perf_counter() - t0),
            "accepted_points": summary.get("accepted_points"),
            "rejected_points": summary.get("rejected_points"),
            "fold_count": summary.get("fold_count"),
            "theta_min": summary.get("theta_min"),
            "theta_max": summary.get("theta_max"),
            "ds_min_used": summary.get("ds_min_used"),
            "seed_theta": summary.get("seed_theta"),
            "final_reason": summary.get("final_reason"),
        })
        checkpoint("done")
        atomic_json(result_path, metrics)
        print(json.dumps(metrics, sort_keys=True), flush=True)
        return 0
    except Exception as exc:
        metrics.update({
            "status": "ERROR",
            "success": False,
            "reason": f"{type(exc).__name__}: {exc}",
            "total_seconds": float(time.perf_counter() - t0),
        })
        checkpoint("error")
        atomic_json(result_path, metrics)
        raise
    finally:
        r3.fixed_theta_solve = original_fixed
        r3.augmented_corrector = original_corrector


def case_name(kind: str, beta: float, route: str) -> str:
    return f"{kind}_beta{beta:g}_{route}"


def launch_case(script: Path, input_npz: str, outdir: Path, kind: str, beta: float,
                route: str, timeout_s: float) -> dict:
    name = case_name(kind, beta, route)
    logs = outdir / "nl1c6r3_geometry_z6_logs"
    states = outdir / "nl1c6r3_geometry_z6_state"
    logs.mkdir(parents=True, exist_ok=True)
    states.mkdir(parents=True, exist_ok=True)
    log_path = logs / f"{name}.log"
    progress_path = states / f"{name}_progress.json"
    result_path = states / f"{name}_result.json"
    for p in (progress_path, result_path):
        if p.exists():
            p.unlink()

    cmd = [
        sys.executable, "-u", str(script), "--worker",
        "--input-npz", input_npz,
        "--kind", kind,
        "--beta", str(beta),
        "--route", route,
        "--progress-json", str(progress_path),
        "--result-json", str(result_path),
    ]
    env = os.environ.copy()
    env.update({
        "PYTHONPATH": str(ROOT),
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
    })
    started = time.perf_counter()
    with log_path.open("w") as log:
        proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=log, stderr=subprocess.STDOUT, env=env)
        try:
            rc = proc.wait(timeout=timeout_s)
            timed_out = False
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.kill()
            proc.wait()
            rc = proc.returncode
    elapsed = time.perf_counter() - started

    data = None
    if result_path.exists():
        try:
            data = json.loads(result_path.read_text())
        except Exception:
            data = None
    if data is None and progress_path.exists():
        try:
            data = json.loads(progress_path.read_text())
        except Exception:
            data = None
    if data is None:
        data = {"kind": kind, "beta": beta, "route": route}

    if timed_out:
        data.update({
            "status": "TIMEOUT",
            "success": False,
            "reason": f"wall_timeout_{timeout_s:g}s",
            "wall_seconds": float(elapsed),
        })
    else:
        data["wall_seconds"] = float(elapsed)
        data["returncode"] = int(rc)
        if rc != 0 and data.get("status") != "ERROR":
            data["status"] = "ERROR"
            data["success"] = False
            data["reason"] = f"worker_exit_{rc}"
    data["log"] = str(log_path.relative_to(ROOT))
    return data


def parent(args) -> int:
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    script = Path(__file__).resolve()
    cases = [(k, b, r) for k in KINDS for b in BETAS for r in ROUTES]
    workers = max(1, min(int(args.workers), len(cases)))
    print(f"NL1C6R3_GEOMETRY_Z6_START cases={len(cases)} workers={workers} timeout_per_route={args.timeout}s", flush=True)
    t0 = time.perf_counter()
    rows = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {
            ex.submit(launch_case, script, args.input_npz, outdir, k, b, r, float(args.timeout)): (k, b, r)
            for k, b, r in cases
        }
        for fut in as_completed(futs):
            k, b, r = futs[fut]
            try:
                row = fut.result()
            except Exception as exc:
                row = {"kind": k, "beta": b, "route": r, "status": "PARENT_ERROR", "success": False,
                       "reason": f"{type(exc).__name__}: {exc}"}
            rows.append(row)
            print(
                f"CASE {case_name(k,b,r):34s} status={row.get('status')} success={row.get('success')} "
                f"reason={row.get('reason')} theta_max={row.get('theta_max')} min|tt|={row.get('min_abs_tt')} "
                f"gmres600={row.get('augmented_gmres_failed_600')} wall={row.get('wall_seconds',0):.2f}s",
                flush=True,
            )

    order = {(k, b, r): i for i, (k, b, r) in enumerate(cases)}
    rows.sort(key=lambda x: order.get((x.get("kind"), float(x.get("beta", -1)), x.get("route")), 999))
    total = time.perf_counter() - t0
    payload = {
        "label": "NL1C6R3_LOCAL_GEOMETRY_Z6_DIAGNOSTIC_ONLY",
        "production_solver_changed": False,
        "physical_equations_changed": False,
        "physical_gates_changed": False,
        "input_npz": args.input_npz,
        "timeout_per_route_seconds": float(args.timeout),
        "workers": workers,
        "wall_seconds": float(total),
        "rows": rows,
    }
    json_path = outdir / "nl1c6r3_geometry_z6.json"
    atomic_json(json_path, payload)

    csv_path = outdir / "nl1c6r3_geometry_z6.csv"
    fields = [
        "kind", "beta", "route", "status", "success", "reason", "wall_seconds", "total_seconds",
        "seed_theta", "accepted_points", "rejected_points", "fold_count", "theta_min", "theta_max",
        "ds_min_used", "fixed_calls", "arc_calls", "fixed_seconds", "arc_seconds",
        "augmented_gmres_failed_600", "augmented_max_iterations", "other_arc_failures",
        "min_abs_tt", "last_theta_pred", "last_theta", "last_event", "log",
    ]
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)

    print(f"NL1C6R3_GEOMETRY_Z6_END wall={total:.3f}s", flush=True)
    print(f"JSON={json_path}", flush=True)
    print(f"CSV={csv_path}", flush=True)
    return 0


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--input-npz", required=True)
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--workers", type=int, default=min(os.cpu_count() or 4, 9))
    ap.add_argument("--timeout", type=float, default=150.0,
                    help="hard wall-clock timeout per route in seconds")
    ap.add_argument("--kind", choices=KINDS)
    ap.add_argument("--beta", type=float, choices=BETAS)
    ap.add_argument("--route", choices=ROUTES)
    ap.add_argument("--progress-json")
    ap.add_argument("--result-json")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.worker:
        missing = [x for x in (args.kind, args.beta, args.route, args.progress_json, args.result_json) if x is None]
        if missing:
            raise SystemExit("worker mode missing required case arguments")
        raise SystemExit(worker(args))
    raise SystemExit(parent(args))
