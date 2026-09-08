#!/usr/bin/env python3
"""v0.69 preregistered linear nonlinear-onset memory-shift diagnostic.

This is a result-informed follow-up to the preserved historical v0.67 and
v0.68 FAIL results.  It does not alter either result.  It uses the frozen
eta=0 tangent forcing and direct pk_lin evaluations to ask where the linear
AeST dimensionless matter power first reaches fixed Delta_L^2 thresholds and
how that threshold scale shifts under the memory tangent.

This is NOT a nonlinear simulation.  It diagnoses only the onset implied by
the linear solution.
"""

from pathlib import Path
import argparse
import json
import math
import os
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import v063.theory_response_map as v63

LAMBDAS = np.array([10.0, 5.0, 2.5, 1.25], dtype=float)
Z_GRID = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5], dtype=float)
THRESHOLDS = np.array([0.1, 0.3, 1.0], dtype=float)
KH_MIN = 0.005
KH_MAX = 2.0
N_K = 1201
KH = np.geomspace(KH_MIN, KH_MAX, N_K)
LOG_KH = np.log(KH)
H = v63.START['H0'] / 100.0
K_MPC = KH * H

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
CROSSING_RES_MAX = 5.0e-3
AFFINITY_MAX = 2.0e-2


def compute_run(force_file, lam):
    from classy import Class

    keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA']
    saved = {key: os.environ.get(key) for key in keys}
    try:
        if lam is None:
            for key in keys:
                os.environ.pop(key, None)
        else:
            os.environ['AEST_TANGENT_FORCE_FILE'] = str(force_file)
            os.environ['AEST_TANGENT_LAMBDA'] = str(float(lam))
        os.environ['OMP_NUM_THREADS'] = '1'

        c = Class()
        pars = dict(v63.class_params())
        pars['P_k_max_h/Mpc'] = 2.0
        c.set(pars)
        c.compute()

        pk = np.empty((N_K, Z_GRID.size), dtype=float)
        for iz, z in enumerate(Z_GRID):
            pk[:, iz] = np.array(
                [float(c.pk_lin(float(k), float(z))) for k in K_MPC],
                dtype=float,
            )

        c.struct_cleanup()
        c.empty()
        return pk
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def dimensionless_power(pk):
    arr = np.asarray(pk, dtype=float)
    return (K_MPC[:, None] ** 3) * arr / (2.0 * math.pi**2)


def first_upward_crossing(kh, delta2, threshold):
    """First crossing from below to >= threshold, interpolated in log-log."""
    kk = np.asarray(kh, dtype=float)
    dd = np.asarray(delta2, dtype=float)
    t = float(threshold)
    if not (
        kk.ndim == 1 and dd.ndim == 1 and kk.size == dd.size
        and np.all(np.isfinite(kk)) and np.all(kk > 0.0)
        and np.all(np.isfinite(dd)) and np.all(dd > 0.0)
    ):
        return None
    for i in range(kk.size - 1):
        if dd[i] < t <= dd[i + 1]:
            x0, x1 = math.log(float(kk[i])), math.log(float(kk[i + 1]))
            y0, y1 = math.log(float(dd[i])), math.log(float(dd[i + 1]))
            yt = math.log(t)
            if y1 == y0:
                return math.exp(0.5 * (x0 + x1))
            f = (yt - y0) / (y1 - y0)
            return math.exp(x0 + f * (x1 - x0))
    return None


def crossing_table(delta2, kh=KH):
    d = np.asarray(delta2, dtype=float)
    out = np.full((THRESHOLDS.size, Z_GRID.size), np.nan, dtype=float)
    for it, threshold in enumerate(THRESHOLDS):
        for iz in range(Z_GRID.size):
            x = first_upward_crossing(kh, d[:, iz], threshold)
            if x is not None:
                out[it, iz] = float(x)
    return out


def response_affinity(values):
    """Global RMS lambda-affinity across 3 thresholds x 7 redshifts."""
    arr = np.asarray(values, dtype=float)
    mean = np.mean(arr, axis=0)
    den = float(np.sum(mean * mean))
    eps = np.empty(arr.shape[0], dtype=float)
    for il in range(arr.shape[0]):
        num = float(np.sum((arr[il] - mean) ** 2))
        eps[il] = math.sqrt(max(num, 0.0) / max(den, 1.0e-300))
    return mean, eps


def crossing_rows(base_cross, mean_resp, by_lambda):
    rows = []
    for it, threshold in enumerate(THRESHOLDS):
        for iz, z in enumerate(Z_GRID):
            rows.append({
                'DeltaL2_threshold': float(threshold),
                'z': float(z),
                'baseline_k_h_per_Mpc': float(base_cross[it, iz]),
                'mean_dln_k_threshold_deta': float(mean_resp[it, iz]),
                'dln_k_threshold_deta_by_lambda': {
                    str(float(lam)): float(by_lambda[il, it, iz])
                    for il, lam in enumerate(LAMBDAS)
                },
                'baseline_k_in_previous_v068_transition_band_0p08_to_0p20': bool(
                    0.08 <= base_cross[it, iz] <= 0.20
                ),
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--class-root', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--npz-out', required=True)
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    force_file, forcing_summary_path = v63.build_forcing(class_root)
    with Path(forcing_summary_path).open() as f:
        forcing_summary = json.load(f)

    base_pk = compute_run(force_file, None)
    base_delta = dimensionless_power(base_pk)
    base_cross = crossing_table(base_delta)

    # Resolution audit: same baseline direct spectrum, every other grid point.
    coarse_idx = np.arange(0, N_K, 2, dtype=int)
    if coarse_idx[-1] != N_K - 1:
        coarse_idx = np.append(coarse_idx, N_K - 1)
    coarse_cross = crossing_table(base_delta[coarse_idx, :], kh=KH[coarse_idx])
    crossing_resolution_rel = np.abs(coarse_cross - base_cross) / np.maximum(
        np.abs(base_cross), 1.0e-300
    )

    plus_cross = np.empty((LAMBDAS.size, THRESHOLDS.size, Z_GRID.size), dtype=float)
    minus_cross = np.empty_like(plus_cross)
    onset_response = np.empty_like(plus_cross)
    all_pk = [base_pk]

    for il, lam in enumerate(LAMBDAS):
        plus_pk = compute_run(force_file, +float(lam))
        minus_pk = compute_run(force_file, -float(lam))
        all_pk.extend([plus_pk, minus_pk])

        pc = crossing_table(dimensionless_power(plus_pk))
        mc = crossing_table(dimensionless_power(minus_pk))
        plus_cross[il] = pc
        minus_cross[il] = mc
        onset_response[il] = (np.log(pc) - np.log(mc)) / (2.0 * float(lam))

    mean_response, affinity = response_affinity(onset_response)

    finite_positive = bool(
        all(np.all(np.isfinite(p)) and np.all(p > 0.0) for p in all_pk)
    )
    all_crossings = bool(
        np.all(np.isfinite(base_cross))
        and np.all(np.isfinite(plus_cross))
        and np.all(np.isfinite(minus_cross))
    )
    forcing_ok = bool(
        float(forcing_summary['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing_summary['cosine']) >= FORCING_COS_MIN
        and bool(forcing_summary['gate'])
    )
    resolution_max = float(np.nanmax(crossing_resolution_rel))
    resolution_ok = bool(np.isfinite(resolution_max) and resolution_max <= CROSSING_RES_MAX)
    affinity_max = float(np.nanmax(affinity))
    affinity_ok = bool(np.isfinite(affinity_max) and affinity_max <= AFFINITY_MAX)

    numerical_pass = bool(
        finite_positive and all_crossings and forcing_ok and resolution_ok and affinity_ok
    )

    flat = mean_response.ravel()
    frac_positive = float(np.mean(flat > 0.0))
    frac_negative = float(np.mean(flat < 0.0))
    delta1 = mean_response[2, :]
    delta1_positive_count = int(np.sum(delta1 > 0.0))
    delta1_negative_count = int(np.sum(delta1 < 0.0))

    if not numerical_pass:
        classification = 'V069_NONLINEAR_ONSET_DIAGNOSTIC_FAIL'
    elif frac_positive >= 0.80 and delta1_positive_count >= 5:
        classification = 'V069_MEMORY_DELAYS_LINEAR_NONLINEAR_ONSET'
    elif frac_negative >= 0.80 and delta1_negative_count >= 5:
        classification = 'V069_MEMORY_ADVANCES_LINEAR_NONLINEAR_ONSET'
    else:
        classification = 'V069_MIXED_LINEAR_NONLINEAR_ONSET_SHIFT'

    median_abs_by_threshold = np.median(np.abs(mean_response), axis=1)
    threshold_ordering = bool(
        median_abs_by_threshold[0] <= median_abs_by_threshold[1]
        <= median_abs_by_threshold[2]
    )

    transition_fraction = float(np.mean((base_cross >= 0.08) & (base_cross <= 0.20)))

    result = {
        'classification': classification,
        'predata_classification': 'V069_PREDATA_NONLINEAR_ONSET_MEMORY_SHIFT',
        'uses_observational_data': False,
        'result_informed_followup': True,
        'historical_classifications_unchanged': {
            'v067': 'V067_GROWTH_KERNEL_CLOSURE_AFFINITY_FAIL',
            'v068': 'V068_LINEAR_SCALE_MEMORY_RESPONSE_MAP_FAIL',
        },
        'scope': 'Linear-theory threshold-onset diagnostic only; no nonlinear evolution is simulated.',
        'locked_model': {
            'KB': v63.KB,
            'tauH0': v63.TAUH0,
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': [float(x) for x in LAMBDAS],
            'lambda_is_numerical_tangent_amplification_not_physical_eta': True,
        },
        'direct_grid': {
            'k_h_per_Mpc_min': KH_MIN,
            'k_h_per_Mpc_max': KH_MAX,
            'n_log_points': N_K,
            'z': [float(x) for x in Z_GRID],
            'direct_pk_lin_only': True,
            'native_grid_interpolation_used': False,
        },
        'thresholds_DeltaL2': [float(x) for x in THRESHOLDS],
        'forcing': {
            'summary_file': str(Path(forcing_summary_path).relative_to(ROOT)),
            'relative_L2_control_vs_primary': float(forcing_summary['relative_L2_control_vs_primary']),
            'cosine': float(forcing_summary['cosine']),
        },
        'baseline_k_threshold_h_per_Mpc': base_cross.tolist(),
        'mean_dln_k_threshold_deta': mean_response.tolist(),
        'dln_k_threshold_deta_by_lambda': onset_response.tolist(),
        'lambda_affinity_by_lambda': {
            str(float(lam)): float(affinity[il]) for il, lam in enumerate(LAMBDAS)
        },
        'crossing_rows': crossing_rows(base_cross, mean_response, onset_response),
        'science_summary': {
            'fraction_positive_all_21_threshold_redshift_points': frac_positive,
            'fraction_negative_all_21_threshold_redshift_points': frac_negative,
            'DeltaL2_eq_1_positive_count_of_7': delta1_positive_count,
            'DeltaL2_eq_1_negative_count_of_7': delta1_negative_count,
            'median_abs_dln_k_threshold_deta_by_threshold': {
                str(float(THRESHOLDS[it])): float(median_abs_by_threshold[it])
                for it in range(THRESHOLDS.size)
            },
            'median_abs_response_increases_0p1_to_0p3_to_1': threshold_ordering,
            'fraction_of_baseline_threshold_crossings_in_v068_0p08_to_0p20_band': transition_fraction,
        },
        'gates': {
            'all_spectra_finite_and_positive': finite_positive,
            'all_thresholds_bracketed_all_runs': all_crossings,
            'forcing_pass': forcing_ok,
            'baseline_fine_vs_every_other_grid_crossing_relative_difference_max': resolution_max,
            'baseline_crossing_resolution_limit': CROSSING_RES_MAX,
            'baseline_crossing_resolution_pass': resolution_ok,
            'crossing_response_lambda_affinity_max': affinity_max,
            'crossing_response_lambda_affinity_limit': AFFINITY_MAX,
            'crossing_response_lambda_affinity_pass': affinity_ok,
            'numerical_pass': numerical_pass,
        },
        'interpretation_policy': (
            'A delay/advance classification refers only to where the LINEAR dimensionless power reaches fixed thresholds. '
            'It is not a nonlinear simulation and does not establish nonlinear saturation, halo behavior, or screening.'
        ),
    }

    Path(args.json_out).write_text(json.dumps(result, indent=2))
    np.savez_compressed(
        args.npz_out,
        k_h_per_Mpc=KH,
        z=Z_GRID,
        thresholds=THRESHOLDS,
        baseline_pk=base_pk,
        baseline_DeltaL2=base_delta,
        baseline_k_threshold=base_cross,
        plus_k_threshold=plus_cross,
        minus_k_threshold=minus_cross,
        dln_k_threshold_deta=onset_response,
        mean_dln_k_threshold_deta=mean_response,
        lambda_affinity=affinity,
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
