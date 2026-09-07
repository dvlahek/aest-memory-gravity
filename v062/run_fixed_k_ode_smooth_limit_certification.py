#!/usr/bin/env python3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import json
import numpy as np

import run_fixed_k_ode_convergence as core

# Final data-blind numerical certification after the deep audit showed that
# the default rapid-k zero crossings disappear in all tight NDF15 solutions.
# We test only the tight smooth branch and compare successive limits.
core.CENTERS = [0.09200, 0.12650]
core.HALF_WINDOW = 0.00015
core.DKH = 0.000025

RESULTS = core.RESULTS
CENTERS = core.CENTERS
DKH = core.DKH

VARIANTS = {
    "ndf15_t3e9_s01_early": {
        "tol_perturbations_integration": 3e-9,
        "perturbations_integration_stepsize": 0.1,
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
    "ndf15_t1e9_s01_early": {
        "tol_perturbations_integration": 1e-9,
        "perturbations_integration_stepsize": 0.1,
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
    "ndf15_t1e9_s005_early": {
        "tol_perturbations_integration": 1e-9,
        "perturbations_integration_stepsize": 0.05,
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
    "ndf15_t1e9_s005_earlier": {
        "tol_perturbations_integration": 1e-9,
        "perturbations_integration_stepsize": 0.05,
        "start_small_k_at_tau_c_over_tau_h": 2e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.015,
    },
}

PRIMARY_PAIRS = {
    "tolerance_3e9_to_1e9": ("ndf15_t3e9_s01_early", "ndf15_t1e9_s01_early"),
    "stepsize_01_to_005_at_1e9": ("ndf15_t1e9_s01_early", "ndf15_t1e9_s005_early"),
    "start_time_early_to_earlier_at_1e9_s005": ("ndf15_t1e9_s005_early", "ndf15_t1e9_s005_earlier"),
}

# Locked before seeing this run.
SOURCE_RMS_MAX = 1e-3
MIN_SHIFT_MAX = DKH
DIRECT_CLASS_MAX = 1e-10
ROOT_SHIFT_MAX = DKH


def targets():
    vals = []
    for c in CENTERS:
        vals.extend(np.arange(c-core.HALF_WINDOW, c+core.HALF_WINDOW+0.25*DKH, DKH))
        vals.append(c)
    return sorted(set(round(float(v), 8) for v in vals))


def diagnostics(rows):
    ratios = np.asarray([r["P_direct_over_class"] for r in rows if r["P_direct_over_class"] is not None], float)
    return {
        "n_rows": len(rows),
        "max_requested_to_actual_k_relative_offset": float(max(r["k_relative_offset"] for r in rows)),
        "max_copy_P_spread": float(max(r["P_direct_relative_spread"] for r in rows)),
        "max_copy_source_spread": float(max(r["source_relative_spread"] for r in rows)),
        "P_direct_vs_CLASS_max_abs_fractional_difference": float(np.max(np.abs(ratios-1.0))),
    }


def root_topology(a_rows, b_rows):
    windows = {}
    ok_all = True
    n_final = 0
    for c in CENTERS:
        ra = sorted(core.linear_roots(a_rows, c))
        rb = sorted(core.linear_roots(b_rows, c))
        n_final += len(rb)
        same_count = len(ra) == len(rb)
        if same_count and ra:
            max_shift = max(abs(x-y) for x, y in zip(ra, rb))
        elif same_count:
            max_shift = 0.0
        else:
            max_shift = None
        stable = same_count and max_shift is not None and max_shift <= ROOT_SHIFT_MAX + 1e-15
        ok_all = ok_all and stable
        windows[f"{c:.5f}"] = {
            "roots_a": ra,
            "roots_b": rb,
            "same_count": same_count,
            "max_paired_root_shift_h_per_Mpc": max_shift,
            "stable": stable,
        }
    return {"windows": windows, "pass": ok_all, "n_final_roots": n_final}


def pair_report(a_name, b_name, rows, diags):
    if a_name not in rows or b_name not in rows:
        return {"available": False, "pass": False}
    comp = core.compare_variant(rows[a_name], rows[b_name], b_name)
    shifts = [abs(w["min_k_shift_h_per_Mpc"]) for w in comp["windows"].values()]
    topo = root_topology(rows[a_name], rows[b_name])
    direct = max(
        diags[a_name]["P_direct_vs_CLASS_max_abs_fractional_difference"],
        diags[b_name]["P_direct_vs_CLASS_max_abs_fractional_difference"],
    )
    source_ok = comp["source_rms_normalized_to_baseline_rms"] < SOURCE_RMS_MAX
    min_ok = max(shifts) <= MIN_SHIFT_MAX + 1e-15
    direct_ok = direct < DIRECT_CLASS_MAX
    passed = source_ok and min_ok and direct_ok and topo["pass"]
    return {
        "available": True,
        "a": a_name,
        "b": b_name,
        "source_rms_normalized": comp["source_rms_normalized_to_baseline_rms"],
        "source_sign_agreement_fraction": comp["source_sign_agreement_fraction"],
        "logP_rms_difference": comp["logP_rms_difference"],
        "max_abs_minimum_shift_h_per_Mpc": max(shifts),
        "P_direct_vs_CLASS_max_abs_fractional_difference": direct,
        "root_topology": topo,
        "source_ok": source_ok,
        "minimum_location_ok": min_ok,
        "direct_class_ok": direct_ok,
        "pass": passed,
        "windows": comp["windows"],
    }


def main():
    t = targets()
    rows = {}
    errors = {}

    # The four certification variants are scientifically independent CLASS
    # evaluations. Run them concurrently to reduce wall time only; each call
    # retains exactly the same k grid, solver, tolerances, start times and gates.
    with ThreadPoolExecutor(max_workers=len(VARIANTS)) as pool:
        futures = {}
        for name, overrides in VARIANTS.items():
            print(f"=== {name} ===", flush=True)
            futures[pool.submit(core.run_variant, name, overrides, t)] = name
        for future in as_completed(futures):
            name = futures[future]
            rr, ee = future.result()
            errors[name] = ee
            if rr is not None:
                rows[name] = rr
            print(f"=== {name} complete ===", flush=True)

    diags = {name: diagnostics(rr) for name, rr in rows.items()}
    pairs = {
        label: pair_report(a, b, rows, diags)
        for label, (a, b) in PRIMARY_PAIRS.items()
    }
    numerical_converged = all(p["pass"] for p in pairs.values())

    final_name = "ndf15_t1e9_s005_earlier"
    final_roots = {}
    total_final_roots = 0
    final_minima = {}
    if final_name in rows:
        for c in CENTERS:
            rr = core.linear_roots(rows[final_name], c)
            final_roots[f"{c:.5f}"] = rr
            total_final_roots += len(rr)
            local = [r for r in rows[final_name] if abs(r["kh_requested"]-c) <= core.HALF_WINDOW+1e-12]
            imin = int(np.argmin([r["P_direct_Mpc3"] for r in local]))
            rmin = local[imin]
            final_minima[f"{c:.5f}"] = {
                "kh": rmin["kh_requested"],
                "P_direct_Mpc3": rmin["P_direct_Mpc3"],
                "delta_m_gi_final": rmin["delta_m_gi_final"],
            }

    smooth = numerical_converged and total_final_roots == 0
    rapid = numerical_converged and total_final_roots > 0
    if smooth:
        classification = "V062_SMOOTH_LIMIT_CERTIFIED"
    elif rapid:
        classification = "V062_TIGHT_LIMIT_RETAINS_RAPID_ROOTS"
    else:
        classification = "V062_SMOOTH_LIMIT_NEEDS_FOLLOWUP"

    report = {
        "classification": classification,
        "purpose": "final certification of the tight smooth NDF15 branch after rapid roots disappeared in the deep audit",
        "targets_kh": CENTERS,
        "window_half_width_h_per_Mpc": core.HALF_WINDOW,
        "grid_step_h_per_Mpc": DKH,
        "n_unique_target_k": len(t),
        "variants": VARIANTS,
        "variant_errors": errors,
        "diagnostics": diags,
        "predeclared_gate": {
            "source_rms_normalized": f"<{SOURCE_RMS_MAX}",
            "minimum_location_shift": f"<={MIN_SHIFT_MAX} h/Mpc",
            "direct_vs_CLASS": f"<{DIRECT_CLASS_MAX}",
            "root_topology_shift": f"<={ROOT_SHIFT_MAX} h/Mpc",
            "smooth_certification_requires_zero_final_roots": True,
        },
        "successive_pairs": pairs,
        "numerical_converged": numerical_converged,
        "final_roots": final_roots,
        "n_final_roots": total_final_roots,
        "final_minima": final_minima,
        "interpretation": {
            "V062_SMOOTH_LIMIT_CERTIFIED": "tight tolerance, step-size and earlier-start limits agree and no rapid direct-source roots survive",
            "V062_TIGHT_LIMIT_RETAINS_RAPID_ROOTS": "tight numerical limits agree but rapid roots survive",
            "V062_SMOOTH_LIMIT_NEEDS_FOLLOWUP": "at least one locked tight-limit convergence gate fails",
        },
    }
    (RESULTS / "v062_fixed_k_ode_smooth_limit_certification.json").write_text(json.dumps(report, indent=2)+"\n")

    fields = [
        "variant","batch","kh_requested","kh_actual","k_relative_offset",
        "delta_m_current_final","theta_m_current_final","delta_m_gi_final",
        "P_direct_Mpc3","P_class_Mpc3","P_direct_over_class","copies",
        "P_direct_relative_spread","source_relative_spread",
    ]
    with (RESULTS / "v062_fixed_k_ode_smooth_limit_certification_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for rr in rows.values():
            w.writerows(rr)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
