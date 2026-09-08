#!/usr/bin/env python3
"""Non-classifying AeST-E conditioning probe for v0.62.

Purpose
-------
Test the numerical hypothesis that the exact-3e-9 NDF15 runtime cliff is tied
to the near-zero AeST E perturbation dominating the solver's relative Newton/LTE
norms.  This diagnostic compares two tolerances, 1e-8 and 3e-9, at the same
requested target kh=0.092, with the same frozen early-start settings and the
same deliberately minimal auxiliary CLASS k grid.

This script changes no physical model parameter and MUST NOT be used for the
preregistered v0.62 scientific classification.  It assumes the local pinned
CLASS build already contains the execution-only runtime profiler, error-
dominator, perturbation-index-map, and early-dynamics instrumentation patches.

Expected diagnostic environment hooks used by the patched CLASS build:
  AEST_NDF15_PROFILE_FILE
  AEST_NDF15_DOMINATOR_FILE
  AEST_PT_INDEX_MAP_FILE
  AEST_EARLY_DYNAMICS_TRACE_FILE

The dominator log stores 1-based NDF15 indices.  Therefore NDF index 8 maps to
CLASS perturbation-vector index 7.  In the full scalar neq=225 layout measured
by the index-map diagnostic, CLASS index 7 is aest_E.
"""

from pathlib import Path
import json
import os
import subprocess
import sys
import time

import run_fixed_k_ode_convergence as core

RESULTS = core.RESULTS
KH_VALUES = [0.09200]
EARLY_STARTS = {
    "start_small_k_at_tau_c_over_tau_h": 5e-4,
    "start_large_k_at_tau_h_over_tau_k": 0.03,
}
MINIMAL_GRID = {
    "P_k_max_h/Mpc": 0.10,
    "k_per_decade_for_pk": 1,
    "k_per_decade_for_bao": 1,
}
TOLERANCES = [1e-8, 3e-9]


def parse_keyvals(path):
    rows = []
    if not path.exists():
        return rows
    for raw in path.read_text(errors="replace").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        row = {}
        for tok in raw.split():
            if "=" not in tok:
                continue
            k, v = tok.split("=", 1)
            row[k] = v
        rows.append(row)
    return rows


def fval(row, key):
    try:
        return float(row[key])
    except Exception:
        return None


def ival(row, key):
    try:
        return int(row[key])
    except Exception:
        return None


def summarize_dominator(path):
    rows = parse_keyvals(path)
    out = {
        "n_rows": len(rows),
        "ndf15_indexing": "1-based",
        "class_index_relation": "class_index = ndf15_index - 1",
        "aest_E_expected_ndf15_index_in_full_neq225_layout": 8,
    }
    if not rows:
        return out

    err_counts = {}
    newton_counts = {}
    e_rows = []
    for r in rows:
        ei = ival(r, "err_idx")
        ni = ival(r, "newton_idx")
        if ei is not None:
            err_counts[str(ei)] = err_counts.get(str(ei), 0) + 1
        if ni is not None:
            newton_counts[str(ni)] = newton_counts.get(str(ni), 0) + 1
        if ei == 8:
            e_rows.append(r)

    out["err_idx_counts"] = err_counts
    out["newton_idx_counts"] = newton_counts
    out["err_idx8_fraction"] = (
        err_counts.get("8", 0) / len(rows) if rows else None
    )
    out["newton_idx8_fraction"] = (
        newton_counts.get("8", 0) / len(rows) if rows else None
    )

    if e_rows:
        ys = [abs(x) for x in (fval(r, "err_y") for r in e_rows) if x is not None]
        invw = [x for x in (fval(r, "err_invwt") for r in e_rows) if x is not None]
        raws = [x for x in (fval(r, "err_raw") for r in e_rows) if x is not None]
        ts = [x for x in (fval(r, "t") for r in e_rows) if x is not None]
        hs = [x for x in (fval(r, "absh") for r in e_rows) if x is not None]
        out["err_idx8_aest_E"] = {
            "n_rows": len(e_rows),
            "abs_y_min": min(ys) if ys else None,
            "abs_y_max": max(ys) if ys else None,
            "invwt_min": min(invw) if invw else None,
            "invwt_max": max(invw) if invw else None,
            "raw_norm_min": min(raws) if raws else None,
            "raw_norm_max": max(raws) if raws else None,
            "tau_min": min(ts) if ts else None,
            "tau_max": max(ts) if ts else None,
            "absh_min": min(hs) if hs else None,
            "absh_max": max(hs) if hs else None,
        }
    return out


def summarize_early(path):
    rows = parse_keyvals(path)
    out = {"n_rows": len(rows)}
    if not rows:
        return out

    vals = []
    ders = []
    taus = []
    for r in rows:
        # Support current logger naming and harmless future variants.
        for key in ("aest_E", "E_aest", "E"):
            x = fval(r, key)
            if x is not None:
                vals.append(x)
                break
        for key in ("aest_E_prime", "aest_E_deriv", "E_prime", "dE"):
            x = fval(r, key)
            if x is not None:
                ders.append(x)
                break
        x = fval(r, "tau")
        if x is None:
            x = fval(r, "t")
        if x is not None:
            taus.append(x)

    if vals:
        out["aest_E_abs_min"] = min(abs(x) for x in vals)
        out["aest_E_abs_max"] = max(abs(x) for x in vals)
        out["aest_E_sign_changes_in_logged_sequence"] = sum(
            1 for a, b in zip(vals, vals[1:]) if a != 0 and b != 0 and a * b < 0
        )
    if ders:
        out["aest_E_deriv_abs_max"] = max(abs(x) for x in ders)
    if taus:
        out["tau_min"] = min(taus)
        out["tau_max"] = max(taus)
    return out


def run_one(tol):
    label = "1e8" if tol == 1e-8 else "3e9"
    variant = f"aest_E_conditioning_{label}"
    worker_json = RESULTS / f"v062_odeconv_{variant}_batch_0.json"
    offline_trace = RESULTS / f"v062_odeconv_{variant}_batch_0_trace.dat"
    profile = RESULTS / f"v062_aest_E_conditioning_{label}_ndf15_profile.dat"
    dominator = RESULTS / f"v062_aest_E_conditioning_{label}_dominator.dat"
    index_map = RESULTS / f"v062_aest_E_conditioning_{label}_index_map.dat"
    early = RESULTS / f"v062_aest_E_conditioning_{label}_early_dynamics.dat"

    for p in (worker_json, offline_trace, profile, dominator, index_map, early):
        if p.exists():
            p.unlink()

    overrides = {
        "tol_perturbations_integration": tol,
        **EARLY_STARTS,
        **MINIMAL_GRID,
    }

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["AEST_OFFLINE_TRACE_FILE"] = str(offline_trace)
    env["AEST_NDF15_PROFILE_FILE"] = str(profile)
    env["AEST_NDF15_DOMINATOR_FILE"] = str(dominator)
    env["AEST_PT_INDEX_MAP_FILE"] = str(index_map)
    env["AEST_EARLY_DYNAMICS_TRACE_FILE"] = str(early)

    cmd = [
        sys.executable,
        str(Path(core.__file__).resolve()),
        "--worker",
        variant,
        json.dumps(overrides),
        "0",
        json.dumps(KH_VALUES),
    ]

    print(json.dumps({
        "stage": label,
        "tolerance": tol,
        "kh_values": KH_VALUES,
        "minimal_auxiliary_grid": MINIMAL_GRID,
        "classification_use": "NONE_NON_SCIENTIFIC_AEST_E_CONDITIONING_PROBE",
    }, indent=2), flush=True)

    t0 = time.perf_counter()
    cp = subprocess.run(cmd, env=env, check=False)
    wall = time.perf_counter() - t0

    return {
        "label": label,
        "tolerance": tol,
        "wall_seconds": wall,
        "returncode": cp.returncode,
        "worker_output_json": str(worker_json),
        "offline_trace_file": str(offline_trace),
        "ndf15_profile_file": str(profile),
        "dominator_file": str(dominator),
        "index_map_file": str(index_map),
        "early_dynamics_file": str(early),
        "dominator_summary": summarize_dominator(dominator),
        "early_dynamics_summary": summarize_early(early),
    }


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    report = {
        "classification_use": "NONE_NON_SCIENTIFIC_AEST_E_CONDITIONING_PROBE",
        "purpose": "Compare 1e-8 versus exact 3e-9 at fixed target and fixed minimal auxiliary k grid, with AeST-E/NDF15 instrumentation enabled",
        "physical_model_changed": False,
        "requested_target_k_changed": False,
        "early_start_settings_changed": False,
        "auxiliary_internal_k_grid_changed_for_diagnostic": True,
        "solver_tolerance_varied_for_diagnostic": True,
        "final_certification_changed": False,
        "kh_values": KH_VALUES,
        "early_starts": EARLY_STARTS,
        "minimal_auxiliary_grid": MINIMAL_GRID,
        "indexing_note": "NDF15 arrays are 1-based; NDF index j maps to CLASS perturbation index j-1. In measured full neq=225 layout, NDF 8 = CLASS 7 = aest_E.",
        "runs": [],
    }

    for tol in TOLERANCES:
        r = run_one(tol)
        report["runs"].append(r)
        print(json.dumps(r, indent=2), flush=True)
        if r["returncode"] != 0:
            break

    if len(report["runs"]) == 2 and all(r["returncode"] == 0 for r in report["runs"]):
        w1 = report["runs"][0]["wall_seconds"]
        w3 = report["runs"][1]["wall_seconds"]
        report["runtime_ratio_3e9_over_1e8"] = w3 / w1 if w1 > 0 else None

    summary = RESULTS / "v062_aest_E_conditioning_probe_summary.json"
    summary.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "summary_file": str(summary),
        "classification_use": report["classification_use"],
        "runtime_ratio_3e9_over_1e8": report.get("runtime_ratio_3e9_over_1e8"),
    }, indent=2), flush=True)

    if report["runs"] and report["runs"][-1]["returncode"] != 0:
        raise SystemExit(report["runs"][-1]["returncode"])


if __name__ == "__main__":
    main()
