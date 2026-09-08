#!/usr/bin/env python3
"""Non-classifying root/topology equivalence probe for the NDF15 weight floor.

Purpose
-------
Compare the frozen/default NDF15 state-weight floor 1e-15 against the fast
1e-13 diagnostic floor on a seven-point local grid around each of the two
v0.62 smooth-limit centers.  The perturbation tolerance, early-start settings,
physical model, requested k values and NDF15 nominal stepsize are unchanged.
Only the diagnostic auxiliary CLASS k sampling is minimized to keep this
control tractable.

This script is NOT part of the preregistered v0.62 scientific classification.
Its role is only to test whether the 1e-13 floor preserves local source signs
and linearized zero-crossing topology relative to the unmodified 1e-15 solver.

The exact/default-floor points are run as independent one-target workers so
that the pathological exact-3e-9 solves can execute in parallel. Completed
worker JSON files are reused automatically.  Set V062_TOPOLOGY_MAX_WORKERS to
limit concurrency; the default is min(14, cpu_count).
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json
import os
import subprocess
import sys
import time

import run_fixed_k_ode_convergence as core

RESULTS = core.RESULTS
CENTERS = [0.09200, 0.12650]
DKH = 0.000025
OFFSETS = [-3, -2, -1, 0, 1, 2, 3]
FROZEN_FLOOR = 1e-15
SURROGATE_FLOOR = 1e-13
ROOT_SHIFT_MAX = DKH
EARLY_STARTS = {
    "start_small_k_at_tau_c_over_tau_h": 5e-4,
    "start_large_k_at_tau_h_over_tau_k": 0.03,
}
COMMON_OVERRIDES = {
    "tol_perturbations_integration": 3e-9,
    "perturbations_integration_stepsize": 0.1,
    **EARLY_STARTS,
    "k_per_decade_for_pk": 1,
    "k_per_decade_for_bao": 1,
}
DEFAULT_MAX_WORKERS = min(14, os.cpu_count() or 1)
MAX_WORKERS = max(1, int(os.environ.get("V062_TOPOLOGY_MAX_WORKERS", DEFAULT_MAX_WORKERS)))


def target_specs():
    specs = []
    for c in CENTERS:
        pkmax = 0.10 if c < 0.1 else 0.14
        for off in OFFSETS:
            kh = round(c + off * DKH, 8)
            specs.append({"center": c, "offset": off, "kh": kh, "pkmax_h": pkmax})
    return specs


def tag_k(kh):
    return f"{kh:.8f}".replace(".", "p")


def paths_for(kind, kh):
    variant = f"ndf15_topology_{kind}_{tag_k(kh)}"
    out = RESULTS / f"v062_odeconv_{variant}_batch_0.json"
    trace = RESULTS / f"v062_odeconv_{variant}_batch_0_trace.dat"
    return variant, out, trace


def valid_single_row(path, kh):
    if not path.exists():
        return None
    try:
        obj = json.loads(path.read_text())
        rows = obj.get("rows", [])
        if len(rows) != 1:
            return None
        row = rows[0]
        if abs(float(row["kh_requested"]) - kh) > 5e-10:
            return None
        return row
    except Exception:
        return None


def run_point(spec, kind, floor):
    kh = spec["kh"]
    variant, out, trace = paths_for(kind, kh)
    cached = valid_single_row(out, kh)
    if cached is not None:
        return {
            "kind": kind,
            "floor": floor,
            "kh": kh,
            "center": spec["center"],
            "offset": spec["offset"],
            "returncode": 0,
            "wall_seconds": 0.0,
            "reused": True,
            "worker_output_json": str(out),
            "row": cached,
        }

    if out.exists():
        out.unlink()
    if trace.exists():
        trace.unlink()

    overrides = dict(COMMON_OVERRIDES)
    overrides["P_k_max_h/Mpc"] = spec["pkmax_h"]

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["AEST_OFFLINE_TRACE_FILE"] = str(trace)
    if floor == FROZEN_FLOOR:
        env.pop("AEST_NDF15_WEIGHT_FLOOR", None)
    else:
        env["AEST_NDF15_WEIGHT_FLOOR"] = f"{floor:.17g}"

    cmd = [
        sys.executable,
        str(Path(core.__file__).resolve()),
        "--worker",
        variant,
        json.dumps(overrides),
        "0",
        json.dumps([kh]),
    ]
    t0 = time.perf_counter()
    cp = subprocess.run(cmd, env=env, check=False)
    wall = time.perf_counter() - t0
    row = valid_single_row(out, kh) if cp.returncode == 0 else None
    return {
        "kind": kind,
        "floor": floor,
        "kh": kh,
        "center": spec["center"],
        "offset": spec["offset"],
        "returncode": cp.returncode,
        "wall_seconds": wall,
        "reused": False,
        "worker_output_json": str(out),
        "row": row,
    }


def run_family(specs, kind, floor):
    results = []
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(specs))) as pool:
        futs = {pool.submit(run_point, s, kind, floor): s for s in specs}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            state = "reuse" if r["reused"] else "done"
            print(
                f"[{kind}] kh={r['kh']:.8f} {state} rc={r['returncode']} "
                f"wall={r['wall_seconds']:.2f}s",
                flush=True,
            )
    return sorted(results, key=lambda r: r["kh"])


def roots(rows, center):
    local = sorted(
        [r for r in rows if abs(float(r["kh_requested"]) - center) <= 3 * DKH + 1e-12],
        key=lambda r: float(r["kh_requested"]),
    )
    out = []
    for a, b in zip(local[:-1], local[1:]):
        x0 = float(a["kh_requested"])
        x1 = float(b["kh_requested"])
        y0 = float(a["delta_m_gi_final"])
        y1 = float(b["delta_m_gi_final"])
        if y0 == 0.0:
            out.append(x0)
        elif y0 * y1 < 0.0:
            out.append(x0 + (x1 - x0) * (-y0) / (y1 - y0))
    return out


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def compare(frozen_results, surrogate_results):
    fmap = {round(r["kh"], 8): r for r in frozen_results if r["row"] is not None}
    smap = {round(r["kh"], 8): r for r in surrogate_results if r["row"] is not None}
    common = sorted(set(fmap) & set(smap))
    points = []
    for kh in common:
        fr = fmap[kh]["row"]
        sr = smap[kh]["row"]
        fd = float(fr["delta_m_gi_final"])
        sd = float(sr["delta_m_gi_final"])
        fp = float(fr["P_class_Mpc3"])
        sp = float(sr["P_class_Mpc3"])
        points.append({
            "kh": kh,
            "center": fmap[kh]["center"],
            "offset": fmap[kh]["offset"],
            "frozen_Dm": fd,
            "surrogate_Dm": sd,
            "same_Dm_sign": (fd == 0.0 and sd == 0.0) or (fd * sd > 0.0),
            "Dm_absolute_difference": abs(sd - fd),
            "Dm_relative_difference": rel(sd, fd),
            "frozen_P_class_Mpc3": fp,
            "surrogate_P_class_Mpc3": sp,
            "P_class_relative_difference": rel(sp, fp),
            "surrogate_direct_vs_class_relative": abs(float(sr["P_direct_Mpc3"]) - sp) / max(abs(sp), 1e-300),
        })

    frows = [fmap[k]["row"] for k in common]
    srows = [smap[k]["row"] for k in common]
    windows = {}
    topology_pass = True
    for c in CENTERS:
        frt = roots(frows, c)
        srt = roots(srows, c)
        same_count = len(frt) == len(srt)
        if same_count and frt:
            shifts = [abs(a - b) for a, b in zip(frt, srt)]
            max_shift = max(shifts)
        elif same_count:
            shifts = []
            max_shift = 0.0
        else:
            shifts = None
            max_shift = None
        sign_ok = all(p["same_Dm_sign"] for p in points if abs(p["center"] - c) < 1e-12)
        root_ok = same_count and max_shift is not None and max_shift <= ROOT_SHIFT_MAX + 1e-15
        passed = sign_ok and root_ok
        topology_pass = topology_pass and passed
        windows[f"{c:.5f}"] = {
            "frozen_roots": frt,
            "surrogate_roots": srt,
            "same_root_count": same_count,
            "paired_root_shifts_h_per_Mpc": shifts,
            "max_root_shift_h_per_Mpc": max_shift,
            "max_root_shift_in_DKH": (max_shift / DKH) if max_shift is not None else None,
            "sign_agreement_all_7_points": sign_ok,
            "root_shift_within_DKH": root_ok,
            "topology_equivalent_on_test_grid": passed,
        }

    all_signs = all(p["same_Dm_sign"] for p in points) if points else False
    return {
        "n_common_points": len(common),
        "expected_points": len(CENTERS) * len(OFFSETS),
        "all_point_signs_agree": all_signs,
        "max_Dm_relative_difference": max((p["Dm_relative_difference"] for p in points), default=None),
        "max_P_class_relative_difference": max((p["P_class_relative_difference"] for p in points), default=None),
        "max_surrogate_direct_vs_class_relative": max((p["surrogate_direct_vs_class_relative"] for p in points), default=None),
        "windows": windows,
        "topology_equivalent_on_test_grid": topology_pass and len(common) == len(CENTERS) * len(OFFSETS),
        "points": points,
    }


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    specs = target_specs()
    header = {
        "classification_use": "NONE_NON_SCIENTIFIC_NDF15_WEIGHT_FLOOR_ROOT_TOPOLOGY_PROBE",
        "purpose": "Compare frozen 1e-15 and fast 1e-13 NDF15 weight floors on seven-point local grids around both v0.62 centers",
        "physical_model_changed": False,
        "tol_perturbations_integration_changed": False,
        "early_start_settings_changed": False,
        "requested_target_k_changed": False,
        "jacobian_abstol_changed": False,
        "ndf15_weight_floor_varied_for_diagnostic": True,
        "auxiliary_internal_k_grid_changed_for_diagnostic": True,
        "final_certification_changed": False,
        "frozen_weight_floor": FROZEN_FLOOR,
        "surrogate_weight_floor": SURROGATE_FLOOR,
        "tol_perturbations_integration": 3e-9,
        "perturbations_integration_stepsize": 0.1,
        "centers_h_per_Mpc": CENTERS,
        "offsets_in_DKH": OFFSETS,
        "DKH_h_per_Mpc": DKH,
        "root_shift_test_limit_h_per_Mpc": ROOT_SHIFT_MAX,
        "root_shift_test_limit_is_existing_frozen_grid_resolution": True,
        "early_starts": EARLY_STARTS,
        "diagnostic_k_per_decade_for_pk": 1,
        "diagnostic_k_per_decade_for_bao": 1,
        "max_parallel_workers": min(MAX_WORKERS, len(specs)),
        "omp_num_threads_per_worker": 1,
    }
    print(json.dumps(header, indent=2), flush=True)

    print("=== frozen/default floor 1e-15 ===", flush=True)
    frozen = run_family(specs, "frozen_1em15", FROZEN_FLOOR)
    if any(r["returncode"] != 0 or r["row"] is None for r in frozen):
        comparison = None
    else:
        print("=== surrogate floor 1e-13 ===", flush=True)
        surrogate = run_family(specs, "surrogate_1em13", SURROGATE_FLOOR)
        comparison = compare(frozen, surrogate)

    if comparison is None:
        surrogate = []

    report = dict(header)
    report.update({
        "frozen_runs": frozen,
        "surrogate_runs": surrogate,
        "comparison": comparison,
    })
    summary = RESULTS / "v062_ndf15_weight_floor_root_topology_probe_summary.json"
    summary.write_text(json.dumps(report, indent=2) + "\n")

    compact = {
        "summary_file": str(summary),
        "classification_use": header["classification_use"],
        "frozen_completed": sum(r["returncode"] == 0 and r["row"] is not None for r in frozen),
        "surrogate_completed": sum(r["returncode"] == 0 and r["row"] is not None for r in surrogate),
        "topology_equivalent_on_test_grid": comparison.get("topology_equivalent_on_test_grid") if comparison else None,
        "all_point_signs_agree": comparison.get("all_point_signs_agree") if comparison else None,
        "max_Dm_relative_difference": comparison.get("max_Dm_relative_difference") if comparison else None,
        "max_P_class_relative_difference": comparison.get("max_P_class_relative_difference") if comparison else None,
        "windows": comparison.get("windows") if comparison else None,
    }
    print(json.dumps(compact, indent=2), flush=True)

    if any(r["returncode"] != 0 or r["row"] is None for r in frozen + surrogate):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
