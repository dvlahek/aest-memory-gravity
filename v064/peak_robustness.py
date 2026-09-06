#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import v063.theory_response_map as v63

LAMBDAS = (5.0, 10.0, 20.0)
K_GRID = np.linspace(0.08, 0.15, 141)
Z_GRID = np.linspace(0.20, 0.70, 101)
SIGMA8_Z = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5], dtype=float)
PRIOR_PEAK = (0.10250971366580042, 0.2476197546610166)

GATES = {
    'normalized_l2_difference_max': 0.02,
    'peak_k_shift_h_per_Mpc_max': 0.002,
    'peak_z_shift_max': 0.02,
    'peak_amplitude_relative_difference_max': 0.05,
    'sigma8_normalized_l2_difference_max': 0.02,
}


def compute_dense(force_file, lam):
    from classy import Class

    keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA']
    saved = {k: os.environ.get(k) for k in keys}
    try:
        if lam is None:
            for k in keys:
                os.environ.pop(k, None)
        else:
            os.environ['AEST_TANGENT_FORCE_FILE'] = str(force_file)
            os.environ['AEST_TANGENT_LAMBDA'] = str(float(lam))
        os.environ['OMP_NUM_THREADS'] = '1'

        c = Class()
        c.set(v63.class_params())
        c.compute()

        h = v63.START['H0'] / 100.0
        pm = np.empty((K_GRID.size, Z_GRID.size), dtype=float)
        for ik, kh in enumerate(K_GRID):
            k_mpc = float(kh * h)
            for iz, z in enumerate(Z_GRID):
                pm[ik, iz] = float(c.pk(k_mpc, float(z)))

        sigma8 = np.array([
            float(c.sigma(8.0, float(z), h_units=True)) for z in SIGMA8_Z
        ], dtype=float)

        c.struct_cleanup()
        c.empty()
        return {'pm': pm, 'sigma8': sigma8}
    finally:
        for k, value in saved.items():
            if value is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = value


def fractional_response(base, plus, minus, lam):
    b = np.asarray(base, dtype=float)
    p = np.asarray(plus, dtype=float)
    m = np.asarray(minus, dtype=float)
    if np.any(~np.isfinite(b)) or np.any(b <= 0):
        raise RuntimeError('non-positive or non-finite baseline power encountered')
    return (p - m) / (2.0 * float(lam) * b)


def peak_summary(r):
    a = np.abs(r)
    flat = int(np.argmax(a))
    ik, iz = np.unravel_index(flat, r.shape)
    vals = a[np.isfinite(a)]
    return {
        'k_h_per_Mpc': float(K_GRID[ik]),
        'z': float(Z_GRID[iz]),
        'signed_response_per_eta': float(r[ik, iz]),
        'abs_response_per_eta': float(a[ik, iz]),
        'ik': int(ik),
        'iz': int(iz),
        'quantiles_abs': {
            'q50': float(np.quantile(vals, 0.50)),
            'q90': float(np.quantile(vals, 0.90)),
            'q95': float(np.quantile(vals, 0.95)),
            'q99': float(np.quantile(vals, 0.99)),
        },
        'fractions': {
            'abs_gt_0p1': float(np.mean(vals > 0.1)),
            'abs_gt_1': float(np.mean(vals > 1.0)),
            'abs_gt_5': float(np.mean(vals > 5.0)),
        },
        'rms_abs_response_per_eta': float(np.sqrt(np.mean(vals * vals))),
        'mean_abs_response_per_eta': float(np.mean(vals)),
    }


def contiguous_halfmax_width(axis, values, center_index):
    a = np.abs(np.asarray(values, dtype=float))
    peak = float(a[center_index])
    if not np.isfinite(peak) or peak <= 0:
        return {'width': 0.0, 'lower': float(axis[center_index]), 'upper': float(axis[center_index]), 'n_points': 1}
    threshold = 0.5 * peak
    lo = center_index
    hi = center_index
    while lo > 0 and a[lo - 1] >= threshold:
        lo -= 1
    while hi + 1 < a.size and a[hi + 1] >= threshold:
        hi += 1
    return {
        'width': float(axis[hi] - axis[lo]),
        'lower': float(axis[lo]),
        'upper': float(axis[hi]),
        'n_points': int(hi - lo + 1),
        'threshold_abs_response': float(threshold),
    }


def normalized_l2(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    den = float(np.linalg.norm(b.ravel()))
    if den == 0:
        return float('inf')
    return float(np.linalg.norm((a - b).ravel()) / den)


def nearest_prior_value(r):
    ik = int(np.argmin(np.abs(K_GRID - PRIOR_PEAK[0])))
    iz = int(np.argmin(np.abs(Z_GRID - PRIOR_PEAK[1])))
    return {
        'requested_k_h_per_Mpc': PRIOR_PEAK[0],
        'requested_z': PRIOR_PEAK[1],
        'grid_k_h_per_Mpc': float(K_GRID[ik]),
        'grid_z': float(Z_GRID[iz]),
        'signed_response_per_eta': float(r[ik, iz]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--class-root', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--npz-out', required=True)
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    force, forcing_summary = v63.build_forcing(class_root)

    base = compute_dense(force, None)
    responses = {}
    sigma8_responses = {}
    summaries = {}

    for lam in LAMBDAS:
        plus = compute_dense(force, +lam)
        minus = compute_dense(force, -lam)
        r = fractional_response(base['pm'], plus['pm'], minus['pm'], lam)
        rs8 = fractional_response(base['sigma8'], plus['sigma8'], minus['sigma8'], lam)
        responses[lam] = r
        sigma8_responses[lam] = rs8
        summaries[lam] = peak_summary(r)

    ref = responses[10.0]
    ref_s8 = sigma8_responses[10.0]
    ref_peak = summaries[10.0]
    ik_ref = ref_peak['ik']
    iz_ref = ref_peak['iz']

    shape = {
        'halfmax_k_at_reference_peak_z': contiguous_halfmax_width(K_GRID, ref[:, iz_ref], ik_ref),
        'halfmax_z_at_reference_peak_k': contiguous_halfmax_width(Z_GRID, ref[ik_ref, :], iz_ref),
        'reference_peak_z': float(Z_GRID[iz_ref]),
        'reference_peak_k_h_per_Mpc': float(K_GRID[ik_ref]),
    }

    comparisons = {}
    all_pass = True
    for lam in (5.0, 20.0):
        s = summaries[lam]
        l2 = normalized_l2(responses[lam], ref)
        s8_l2 = normalized_l2(sigma8_responses[lam], ref_s8)
        kshift = abs(s['k_h_per_Mpc'] - ref_peak['k_h_per_Mpc'])
        zshift = abs(s['z'] - ref_peak['z'])
        ampden = max(ref_peak['abs_response_per_eta'], 1e-300)
        amprel = abs(s['abs_response_per_eta'] - ref_peak['abs_response_per_eta']) / ampden
        gate = {
            'normalized_l2_difference': l2,
            'sigma8_normalized_l2_difference': s8_l2,
            'peak_k_shift_h_per_Mpc': float(kshift),
            'peak_z_shift': float(zshift),
            'peak_amplitude_relative_difference': float(amprel),
            'pass': bool(
                l2 <= GATES['normalized_l2_difference_max']
                and s8_l2 <= GATES['sigma8_normalized_l2_difference_max']
                and kshift <= GATES['peak_k_shift_h_per_Mpc_max']
                and zshift <= GATES['peak_z_shift_max']
                and amprel <= GATES['peak_amplitude_relative_difference_max']
            ),
        }
        comparisons[str(lam)] = gate
        all_pass = all_pass and gate['pass']

    k_width = shape['halfmax_k_at_reference_peak_z']['width']
    z_width = shape['halfmax_z_at_reference_peak_k']['width']
    if not all_pass:
        classification = 'V064_TANGENT_AMPLITUDE_ROBUSTNESS_FAIL'
    elif k_width <= 0.01 or z_width <= 0.10:
        classification = 'V064_ROBUST_NARROW_SCALE_DEPENDENT_CLUSTERING_FEATURE'
    else:
        classification = 'V064_ROBUST_BROAD_SCALE_DEPENDENT_CLUSTERING_FEATURE'

    result = {
        'classification': classification,
        'predata_classification': 'V064_PREDATA_TANGENT_PEAK_ROBUSTNESS',
        'uses_observational_data': False,
        'locked_model': {
            'KB': v63.KB,
            'tauH0': v63.TAUH0,
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': list(LAMBDAS),
        },
        'dense_grid': {
            'k_h_per_Mpc_min': float(K_GRID[0]),
            'k_h_per_Mpc_max': float(K_GRID[-1]),
            'k_h_per_Mpc_step': float(K_GRID[1] - K_GRID[0]),
            'n_k': int(K_GRID.size),
            'z_min': float(Z_GRID[0]),
            'z_max': float(Z_GRID[-1]),
            'z_step': float(Z_GRID[1] - Z_GRID[0]),
            'n_z': int(Z_GRID.size),
            'linear_theory_only': True,
        },
        'response_definition': 'R_lambda=[P_m(+lambda)-P_m(-lambda)]/[2 lambda P_m(0)]',
        'gates': GATES,
        'lambda_summaries': {str(k): v for k, v in summaries.items()},
        'lambda_comparisons_to_10': comparisons,
        'all_lambda_invariance_gates_pass': bool(all_pass),
        'shape_diagnostics_lambda10': shape,
        'prior_v063_peak_checks': {str(lam): nearest_prior_value(responses[lam]) for lam in LAMBDAS},
        'sigma8_response_by_lambda': {
            str(lam): [
                {'z': float(z), 'dln_sigma8_deta': float(x)}
                for z, x in zip(SIGMA8_Z, sigma8_responses[lam])
            ] for lam in LAMBDAS
        },
        'forcing_summary_file': str(forcing_summary.relative_to(ROOT)),
        'interpretation': 'This is a data-blind numerical/tangent robustness test of the v0.63 theory feature. Passing does not constitute an observational detection.',
    }

    Path(args.json_out).write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(
        args.npz_out,
        k_h_per_Mpc=K_GRID,
        z=Z_GRID,
        sigma8_z=SIGMA8_Z,
        pm0=base['pm'],
        sigma8_0=base['sigma8'],
        response_lambda5=responses[5.0],
        response_lambda10=responses[10.0],
        response_lambda20=responses[20.0],
        sigma8_response_lambda5=sigma8_responses[5.0],
        sigma8_response_lambda10=sigma8_responses[10.0],
        sigma8_response_lambda20=sigma8_responses[20.0],
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
