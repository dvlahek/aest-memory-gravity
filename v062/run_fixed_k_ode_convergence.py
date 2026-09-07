#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import math
import os
import subprocess
import sys
import numpy as np

RESULTS = Path("results").resolve()
RESULTS.mkdir(parents=True, exist_ok=True)
H0 = 67.3324639084866
h = H0 / 100.0
AS = 2.1308864352626987e-9
NS = 0.9666229454895277
KPIVOT = 0.05
CENTERS = [0.09200, 0.12455, 0.12650, 0.14300]
HALF_WINDOW = 0.00015
DKH = 0.000025

BASE = {
    "H0": H0,
    "omega_b": 0.022377376877682164,
    "N_ur": 2.046,
    "omega_cdm": 0.12006705327635288,
    "N_ncdm": 1,
    "m_ncdm": 0.06,
    "T_ncdm": 0.7137658555036082,
    "YHe": 0.2454006,
    "tau_reio": 0.06174082364515668,
    "n_s": NS,
    "A_s": AS,
    "gauge": "newtonian",
    "aest_enabled": "yes",
    "aest_model": "Exp",
    "aest_KB": 0.0665,
    "aest_Q0": 1e-4,
    "aest_K2": 9500,
    "aest_Z0": 1e-17,
    "aest_memory_enabled": "no",
    "aest_memory_order": 16,
    "aest_eta": 0,
    "aest_tau_H0": 10,
    "output": "mPk",
    "lensing": "no",
    "P_k_max_h/Mpc": 10,
    "z_pk": 0,
    "k_per_decade_for_pk": 40,
    "k_per_decade_for_bao": 70,
}

VARIANTS = {
    "baseline_ndf15": {},
    "ndf15_tol_3e6": {
        "tol_perturbations_integration": 3e-6,
    },
    "ndf15_tol_1e6": {
        "tol_perturbations_integration": 1e-6,
    },
    "ndf15_tol_3e7": {
        "tol_perturbations_integration": 3e-7,
    },
    "ndf15_early": {
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
    "ndf15_tight_early": {
        "tol_perturbations_integration": 1e-6,
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
    "rk_tight_early": {
        "evolver": "rk",
        "tol_perturbations_integration": 1e-7,
        "perturbations_integration_stepsize": 0.05,
        "start_small_k_at_tau_c_over_tau_h": 5e-4,
        "start_large_k_at_tau_h_over_tau_k": 0.03,
    },
}

REQUIRED = {
    "a", "delta_b", "theta_b", "delta_cdm", "theta_cdm",
    "delta_ncdm[0]", "theta_ncdm[0]",
}


def bg_value(bg, iz, key):
    if key not in bg:
        raise RuntimeError(f"missing background key {key}; available={list(bg.keys())}")
    return float(np.asarray(bg[key], float)[iz])


def worker(variant_name, overrides, batch_id, kh_values):
    from classy import Class

    k_values = [x * h for x in kh_values]
    pars = dict(BASE)
    pars.update(overrides)
    pars["k_output_values"] = ", ".join(f"{x:.17g}" for x in k_values)

    cosmo = Class()
    cosmo.set(pars)
    cosmo.compute()
    pt = cosmo.get_perturbations()["scalar"]
    if len(pt) != len(k_values):
        raise RuntimeError(f"expected {len(k_values)} scalar modes, got {len(pt)}")

    bg = cosmo.get_background()
    if "z" not in bg:
        raise RuntimeError(f"background has no z column; keys={list(bg.keys())}")
    iz = int(np.argmin(np.abs(np.asarray(bg["z"], float))))
    rho_b = bg_value(bg, iz, "(.)rho_b")
    rho_cdm = bg_value(bg, iz, "(.)rho_cdm")
    rho_ncdm = bg_value(bg, iz, "(.)rho_ncdm[0]")
    p_ncdm = bg_value(bg, iz, "(.)p_ncdm[0]")
    H = bg_value(bg, iz, "H [1/Mpc]")
    rho_m = rho_b + rho_cdm + rho_ncdm
    rho_plus_p_m = rho_b + rho_cdm + rho_ncdm + p_ncdm

    trace_path = Path(os.environ["AEST_OFFLINE_TRACE_FILE"])
    trace_k = np.loadtxt(trace_path, comments="#", skiprows=1, usecols=(0,))
    unique_trace_k = np.unique(np.atleast_1d(trace_k).astype(float))

    rows = []
    for mode_index, (kh_i, k_req, mode) in enumerate(zip(kh_values, k_values, pt)):
        missing = REQUIRED - set(mode.keys())
        if missing:
            raise RuntimeError(f"missing component keys {sorted(missing)}; available={sorted(mode.keys())}")
        a = float(np.asarray(mode["a"], float)[-1])
        db = float(np.asarray(mode["delta_b"], float)[-1])
        tb = float(np.asarray(mode["theta_b"], float)[-1])
        dc = float(np.asarray(mode["delta_cdm"], float)[-1])
        tc = float(np.asarray(mode["theta_cdm"], float)[-1])
        dn = float(np.asarray(mode["delta_ncdm[0]"], float)[-1])
        tn = float(np.asarray(mode["theta_ncdm[0]"], float)[-1])
        k_actual = float(unique_trace_k[np.argmin(np.abs(unique_trace_k - k_req))])

        delta_m = (rho_b * db + rho_cdm * dc + rho_ncdm * dn) / rho_m
        theta_m = (rho_b * tb + rho_cdm * tc + (rho_ncdm + p_ncdm) * tn) / rho_plus_p_m
        Dm = delta_m + 3.0 * a * H * theta_m / (k_actual * k_actual)
        PR = AS * (k_actual / KPIVOT) ** (NS - 1.0)
        P_direct = (2.0 * math.pi**2 / k_actual**3) * Dm**2 * PR
        P_class = float(cosmo.pk_lin(k_actual, 0.0))
        rows.append({
            "variant": variant_name,
            "batch": batch_id,
            "mode_index": mode_index,
            "kh_requested": kh_i,
            "kh_actual": k_actual / h,
            "k_relative_offset": abs(k_actual - k_req) / max(abs(k_req), 1e-300),
            "a_final": a,
            "delta_b_final": db,
            "theta_b_final": tb,
            "delta_cdm_final": dc,
            "theta_cdm_final": tc,
            "delta_ncdm_final": dn,
            "theta_ncdm_final": tn,
            "delta_m_current_final": delta_m,
            "theta_m_current_final": theta_m,
            "delta_m_gi_final": Dm,
            "P_direct_Mpc3": P_direct,
            "P_class_Mpc3": P_class,
            "P_direct_over_class": P_direct / P_class if P_class > 0 else None,
        })

    out = RESULTS / f"v062_odeconv_{variant_name}_batch_{batch_id}.json"
    out.write_text(json.dumps({"variant": variant_name, "batch": batch_id, "rows": rows}, indent=2) + "\n")
    cosmo.struct_cleanup()
    cosmo.empty()
    print(json.dumps({"variant": variant_name, "batch": batch_id, "n": len(rows)}, indent=2))


def make_targets():
    vals = []
    for c in CENTERS:
        vals.extend(np.arange(c - HALF_WINDOW, c + HALF_WINDOW + 0.25 * DKH, DKH))
        vals.append(c)
    return sorted(set(round(float(v), 8) for v in vals))


def linear_roots(rows, center):
    local = sorted(
        [r for r in rows if abs(r["kh_requested"] - center) <= HALF_WINDOW + 1e-12],
        key=lambda r: r["kh_requested"],
    )
    roots = []
    for a, b in zip(local[:-1], local[1:]):
        x0, x1 = a["kh_requested"], b["kh_requested"]
        y0, y1 = a["delta_m_gi_final"], b["delta_m_gi_final"]
        if y0 == 0.0:
            roots.append(float(x0))
        elif y0 * y1 < 0.0:
            roots.append(float(x0 + (x1 - x0) * (-y0) / (y1 - y0)))
    return roots


def run_variant(variant_name, overrides, targets):
    anchors = list(CENTERS)
    payload = [x for x in targets if all(abs(x - a) > 1e-10 for a in anchors)]
    chunks = [payload[i:i + 26] for i in range(0, len(payload), 26)]
    raw_rows = []
    errors = []
    for batch_id, chunk in enumerate(chunks):
        vals = sorted(set(chunk + anchors))
        env = os.environ.copy()
        env["OMP_NUM_THREADS"] = "1"
        env["AEST_OFFLINE_TRACE_FILE"] = str(RESULTS / f"v062_odeconv_{variant_name}_batch_{batch_id}_trace.dat")
        cp = subprocess.run(
            [sys.executable, __file__, "--worker", variant_name, json.dumps(overrides), str(batch_id), json.dumps(vals)],
            env=env,
            check=False,
        )
        if cp.returncode != 0:
            errors.append({"batch": batch_id, "returncode": cp.returncode})
            continue
        path = RESULTS / f"v062_odeconv_{variant_name}_batch_{batch_id}.json"
        raw_rows.extend(json.loads(path.read_text())["rows"])

    if not raw_rows:
        return None, errors

    by_k = {}
    for row in raw_rows:
        by_k.setdefault(round(row["kh_requested"], 8), []).append(row)
    merged = []
    for _, copies in sorted(by_k.items()):
        base = dict(copies[0])
        base["copies"] = len(copies)
        pp = np.asarray([r["P_direct_Mpc3"] for r in copies], float)
        ss = np.asarray([r["delta_m_gi_final"] for r in copies], float)
        base["P_direct_relative_spread"] = float((pp.max() - pp.min()) / max(np.mean(np.abs(pp)), 1e-300))
        base["source_relative_spread"] = float((ss.max() - ss.min()) / max(np.mean(np.abs(ss)), 1e-300))
        merged.append(base)
    return merged, errors


def compare_variant(base_rows, rows, variant_name):
    bmap = {round(r["kh_requested"], 8): r for r in base_rows}
    vmap = {round(r["kh_requested"], 8): r for r in rows}
    common = sorted(set(bmap) & set(vmap))
    bd = np.asarray([bmap[k]["delta_m_gi_final"] for k in common], float)
    vd = np.asarray([vmap[k]["delta_m_gi_final"] for k in common], float)
    bp = np.asarray([bmap[k]["P_direct_Mpc3"] for k in common], float)
    vp = np.asarray([vmap[k]["P_direct_Mpc3"] for k in common], float)
    rms_scale = max(float(np.sqrt(np.mean(bd**2))), 1e-300)
    max_scale = max(float(np.max(np.abs(bd))), 1e-300)
    result = {
        "variant": variant_name,
        "n_common": len(common),
        "source_rms_normalized_to_baseline_rms": float(np.sqrt(np.mean((vd - bd)**2)) / rms_scale),
        "source_maxabs_normalized_to_baseline_maxabs": float(np.max(np.abs(vd - bd)) / max_scale),
        "source_sign_agreement_fraction": float(np.mean(np.sign(vd) == np.sign(bd))),
        "logP_rms_difference": float(np.sqrt(np.mean((np.log(np.maximum(vp, 1e-300)) - np.log(np.maximum(bp, 1e-300)))**2))),
        "windows": {},
    }
    for c in CENTERS:
        bk = [k for k in common if abs(k - c) <= HALF_WINDOW + 1e-12]
        b_local = [bmap[k] for k in bk]
        v_local = [vmap[k] for k in bk]
        ib = int(np.argmin([r["P_direct_Mpc3"] for r in b_local]))
        iv = int(np.argmin([r["P_direct_Mpc3"] for r in v_local]))
        bmin = b_local[ib]
        vmin = v_local[iv]
        broots = linear_roots(base_rows, c)
        vroots = linear_roots(rows, c)
        nearest_b = min(broots, key=lambda x: abs(x - c)) if broots else None
        nearest_v = min(vroots, key=lambda x: abs(x - c)) if vroots else None
        bsrc = np.asarray([r["delta_m_gi_final"] for r in b_local], float)
        vsrc = np.asarray([r["delta_m_gi_final"] for r in v_local], float)
        local_scale = max(float(np.sqrt(np.mean(bsrc**2))), 1e-300)
        result["windows"][f"{c:.5f}"] = {
            "baseline_min_kh": bmin["kh_requested"],
            "variant_min_kh": vmin["kh_requested"],
            "min_k_shift_h_per_Mpc": float(vmin["kh_requested"] - bmin["kh_requested"]),
            "baseline_Pmin_Mpc3": bmin["P_direct_Mpc3"],
            "variant_Pmin_Mpc3": vmin["P_direct_Mpc3"],
            "Pmin_ratio_to_baseline": float(vmin["P_direct_Mpc3"] / max(bmin["P_direct_Mpc3"], 1e-300)),
            "local_source_rms_normalized": float(np.sqrt(np.mean((vsrc - bsrc)**2)) / local_scale),
            "baseline_zero_crossings": broots,
            "variant_zero_crossings": vroots,
            "baseline_nearest_root": nearest_b,
            "variant_nearest_root": nearest_v,
            "nearest_root_shift_h_per_Mpc": None if nearest_b is None or nearest_v is None else float(nearest_v - nearest_b),
        }
    return result


def main():
    targets = make_targets()
    variant_rows = {}
    variant_errors = {}
    for name, overrides in VARIANTS.items():
        print(f"=== {name} ===", flush=True)
        rows, errors = run_variant(name, overrides, targets)
        variant_errors[name] = errors
        if rows is not None:
            variant_rows[name] = rows

    if "baseline_ndf15" not in variant_rows:
        raise RuntimeError("baseline_ndf15 produced no usable rows")

    baseline = variant_rows["baseline_ndf15"]
    comparisons = {}
    for name, rows in variant_rows.items():
        if name == "baseline_ndf15":
            continue
        comparisons[name] = compare_variant(baseline, rows, name)

    diagnostics = {}
    for name, rows in variant_rows.items():
        ratios = np.asarray([r["P_direct_over_class"] for r in rows if r["P_direct_over_class"] is not None], float)
        diagnostics[name] = {
            "n_rows": len(rows),
            "max_requested_to_actual_k_relative_offset": float(max(r["k_relative_offset"] for r in rows)),
            "max_anchor_P_spread": float(max(r["P_direct_relative_spread"] for r in rows)),
            "max_anchor_source_spread": float(max(r["source_relative_spread"] for r in rows)),
            "P_direct_vs_CLASS_max_abs_fractional_difference": float(np.max(np.abs(ratios - 1.0))),
        }

    required_ndf = ["ndf15_tol_1e6", "ndf15_tol_3e7", "ndf15_early", "ndf15_tight_early"]
    missing_ndf = [x for x in required_ndf if x not in comparisons]
    numerical_pass = not missing_ndf
    gate_details = {}
    if numerical_pass:
        for name in required_ndf:
            comp = comparisons[name]
            source_ok = comp["source_rms_normalized_to_baseline_rms"] < 1e-4
            shifts = [abs(w["min_k_shift_h_per_Mpc"]) for w in comp["windows"].values()]
            minloc_ok = max(shifts) <= DKH + 1e-12
            direct_ok = diagnostics[name]["P_direct_vs_CLASS_max_abs_fractional_difference"] < 1e-10
            gate_details[name] = {
                "source_rms_lt_1e-4": source_ok,
                "all_minimum_shifts_le_one_grid_step": minloc_ok,
                "P_direct_vs_CLASS_lt_1e-10": direct_ok,
                "max_abs_minimum_shift": max(shifts),
            }
            numerical_pass = numerical_pass and source_ok and minloc_ok and direct_ok

    rk_status = "not_available"
    if "rk_tight_early" in comparisons:
        rk = comparisons["rk_tight_early"]
        rk_source_ok = rk["source_rms_normalized_to_baseline_rms"] < 1e-3
        rk_shift_ok = max(abs(w["min_k_shift_h_per_Mpc"]) for w in rk["windows"].values()) <= DKH + 1e-12
        rk_status = "consistent" if rk_source_ok and rk_shift_ok else "different"

    classification = "V062_FIXED_K_ODE_CONVERGENCE_PASS" if numerical_pass else "V062_FIXED_K_ODE_CONVERGENCE_NEEDS_FOLLOWUP"
    report = {
        "classification": classification,
        "targets_kh": CENTERS,
        "window_half_width_h_per_Mpc": HALF_WINDOW,
        "grid_step_h_per_Mpc": DKH,
        "n_unique_target_k": len(targets),
        "variants": VARIANTS,
        "variant_errors": variant_errors,
        "diagnostics": diagnostics,
        "comparisons_to_baseline": comparisons,
        "formal_ndf15_gate": {
            "required_variants": required_ndf,
            "missing_variants": missing_ndf,
            "criteria": {
                "source_rms_normalized": "<1e-4",
                "minimum_location_shift": f"<= {DKH} h/Mpc (one grid step)",
                "P_direct_vs_CLASS_max_abs_fractional_difference": "<1e-10",
            },
            "details": gate_details,
            "pass": numerical_pass,
        },
        "rk_crosscheck_status": rk_status,
        "interpretation": (
            "PASS means the targeted rapid-k matter-source structure is stable to tighter NDF15 ODE tolerances and earlier integration starts on the declared local grid. "
            "The RK result is reported as an independent solver cross-check but is not required for the formal NDF15 gate."
        ),
    }
    (RESULTS / "v062_fixed_k_ode_convergence.json").write_text(json.dumps(report, indent=2) + "\n")

    all_rows = []
    for rows in variant_rows.values():
        all_rows.extend(rows)
    fields = [
        "variant", "batch", "kh_requested", "kh_actual", "k_relative_offset",
        "delta_m_current_final", "theta_m_current_final", "delta_m_gi_final",
        "P_direct_Mpc3", "P_class_Mpc3", "P_direct_over_class", "copies",
        "P_direct_relative_spread", "source_relative_spread",
    ]
    with (RESULTS / "v062_fixed_k_ode_convergence_rows.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(all_rows)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        worker(sys.argv[2], json.loads(sys.argv[3]), int(sys.argv[4]), [float(x) for x in json.loads(sys.argv[5])])
    else:
        main()
