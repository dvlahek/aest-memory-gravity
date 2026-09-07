#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import numpy as np

import run_fixed_k_ode_convergence as core

# Data-blind follow-up declared after the first ODE gate failed.
# We no longer compare to the default NDF15 solution.  The question is whether
# the tightest successive solutions converge to each other.
core.CENTERS = [0.09200, 0.12650]
core.HALF_WINDOW = 0.00015
core.DKH = 0.000025

RESULTS = core.RESULTS
CENTERS = core.CENTERS
DKH = core.DKH

VARIANTS = {
    "ndf15_t3e7_s05": {
        "tol_perturbations_integration": 3e-7,
        "perturbations_integration_stepsize": 0.5,
    },
    "ndf15_t1e7_s05": {
        "tol_perturbations_integration": 1e-7,
        "perturbations_integration_stepsize": 0.5,
    },
    "ndf15_t3e8_s02": {
        "tol_perturbations_integration": 3e-8,
        "perturbations_integration_stepsize": 0.2,
    },
    "ndf15_t1e8_s02": {
        "tol_perturbations_integration": 1e-8,
        "perturbations_integration_stepsize": 0.2,
    },
    "ndf15_t1e8_s01": {
        "tol_perturbations_integration": 1e-8,
        "perturbations_integration_stepsize": 0.1,
    },
    "ndf15_t1e8_s01_early": {
        "tol_perturbations_integration": 1e-8,
        "perturbations_integration_stepsize": 0.1,
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
    # CLASS enum evolver_type is {rk, ndf15}; official pk_ref.pre uses evolver=0 for RK.
    "rk_t1e7_s02_early": {
        "evolver": 0,
        "tol_perturbations_integration": 1e-7,
        "perturbations_integration_stepsize": 0.2,
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
}

PRIMARY_PAIRS = {
    "tolerance_3e8_to_1e8": ("ndf15_t3e8_s02", "ndf15_t1e8_s02"),
    "stepsize_02_to_01_at_1e8": ("ndf15_t1e8_s02", "ndf15_t1e8_s01"),
    "start_time_at_1e8_s01": ("ndf15_t1e8_s01", "ndf15_t1e8_s01_early"),
}

# Predeclared convergence criteria for the tight-solution sequence.
SOURCE_RMS_MAX = 1e-3
MIN_SHIFT_MAX = DKH
DIRECT_CLASS_MAX = 1e-10
ROOT_SHIFT_MAX = 2 * DKH


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
    out = {}
    all_ok = True
    total_final_roots = 0
    for c in CENTERS:
        ra = sorted(core.linear_roots(a_rows, c))
        rb = sorted(core.linear_roots(b_rows, c))
        total_final_roots += len(rb)
        same_count = len(ra) == len(rb)
        if same_count and ra:
            max_shift = max(abs(x-y) for x, y in zip(ra, rb))
        elif same_count:
            max_shift = 0.0
        else:
            max_shift = None
        ok = same_count and (max_shift is not None) and max_shift <= ROOT_SHIFT_MAX + 1e-15
        all_ok = all_ok and ok
        out[f"{c:.5f}"] = {
            "roots_a": ra,
            "roots_b": rb,
            "same_count": same_count,
            "max_paired_root_shift_h_per_Mpc": max_shift,
            "stable": ok,
        }
    return {"windows": out, "pass": all_ok, "n_final_roots": total_final_roots}


def pair_report(a_name, b_name, rows):
    if a_name not in rows or b_name not in rows:
        return {"available": False, "pass": False}
    comp = core.compare_variant(rows[a_name], rows[b_name], b_name)
    shifts = [abs(w["min_k_shift_h_per_Mpc"]) for w in comp["windows"].values()]
    topo = root_topology(rows[a_name], rows[b_name])
    direct = max(
        diagnostics(rows[a_name])["P_direct_vs_CLASS_max_abs_fractional_difference"],
        diagnostics(rows[b_name])["P_direct_vs_CLASS_max_abs_fractional_difference"],
    )
    source_ok = comp["source_rms_normalized_to_baseline_rms"] < SOURCE_RMS_MAX
    min_ok = max(shifts) <= MIN_SHIFT_MAX + 1e-15
    direct_ok = direct < DIRECT_CLASS_MAX
    passed = source_ok and min_ok and direct_ok
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
    for name, overrides in VARIANTS.items():
        print(f"=== {name} ===", flush=True)
        rr, ee = core.run_variant(name, overrides, t)
        errors[name] = ee
        if rr is not None:
            rows[name] = rr

    diags = {name: diagnostics(rr) for name, rr in rows.items()}
    pairs = {label: pair_report(a, b, rows) for label, (a, b) in PRIMARY_PAIRS.items()}
    numerical_converged = all(p["pass"] for p in pairs.values())

    final_name = "ndf15_t1e8_s01_early"
    final_roots = {}
    total_final_roots = 0
    if final_name in rows:
        for c in CENTERS:
            rr = core.linear_roots(rows[final_name], c)
            final_roots[f"{c:.5f}"] = rr
            total_final_roots += len(rr)

    if numerical_converged and total_final_roots > 0:
        classification = "V062_DEEP_ODE_CONVERGED_RAPID_STRUCTURE"
    elif numerical_converged:
        classification = "V062_DEEP_ODE_CONVERGED_SMOOTH_NO_RAPID_ROOTS"
    else:
        classification = "V062_DEEP_ODE_NO_CONVERGENCE"

    rk = {"available": False, "status": "not_available"}
    if final_name in rows and "rk_t1e7_s02_early" in rows:
        rc = core.compare_variant(rows[final_name], rows["rk_t1e7_s02_early"], "rk_t1e7_s02_early")
        shifts = [abs(w["min_k_shift_h_per_Mpc"]) for w in rc["windows"].values()]
        rk_ok = rc["source_rms_normalized_to_baseline_rms"] < 1e-2 and max(shifts) <= DKH + 1e-15
        rk = {
            "available": True,
            "status": "consistent" if rk_ok else "different",
            "source_rms_normalized": rc["source_rms_normalized_to_baseline_rms"],
            "source_sign_agreement_fraction": rc["source_sign_agreement_fraction"],
            "max_abs_minimum_shift_h_per_Mpc": max(shifts),
            "windows": rc["windows"],
        }

    report = {
        "classification": classification,
        "purpose": "decide whether the tightest successive NDF15 solutions converge, rather than comparing them with the already-failed default solution",
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
            "root_topology_is_reported_separately": True,
        },
        "successive_pairs": pairs,
        "numerical_converged": numerical_converged,
        "final_tight_early_roots": final_roots,
        "n_final_tight_early_roots": total_final_roots,
        "rk_crosscheck": rk,
        "interpretation": {
            "converged_rapid": "tight tolerance, step-size and start-time limits agree and retain direct-source roots",
            "converged_smooth": "tight limits agree but the rapid direct-source roots disappear",
            "no_convergence": "even the tightest successive solutions do not agree; rapid-k structure remains numerically uncertified",
        },
    }
    (RESULTS / "v062_fixed_k_ode_deep_convergence.json").write_text(json.dumps(report, indent=2)+"\n")

    fields = [
        "variant","batch","kh_requested","kh_actual","k_relative_offset",
        "delta_m_current_final","theta_m_current_final","delta_m_gi_final",
        "P_direct_Mpc3","P_class_Mpc3","P_direct_over_class","copies",
        "P_direct_relative_spread","source_relative_spread",
    ]
    with (RESULTS / "v062_fixed_k_ode_deep_convergence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for rr in rows.values():
            w.writerows(rr)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
