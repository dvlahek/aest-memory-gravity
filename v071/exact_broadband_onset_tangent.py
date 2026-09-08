#!/usr/bin/env python3
"""v0.71 exact eta=0 broadband onset tangent estimator.

Result-informed follow-up to the preserved v0.70 FAIL. The physical model,
grid, thresholds, broadband widths, lambda values, and sign-classification
rule are unchanged. The only scientific-method change is the eta=0 tangent
estimator: differentiate the broadband power itself with a centered odd
combination, then divide by the baseline broadband power. This removes the
intrinsic finite-lambda O(lambda^2) term produced by taking a centered finite
difference of log broadband power.

This is still a LINEAR-theory onset diagnostic, not nonlinear evolution.
"""

from pathlib import Path
import argparse
import json
import math
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import v070.broadband_nonlinear_onset_tangent as v70

LAMBDAS = v70.LAMBDAS
Z_GRID = v70.Z_GRID
THRESHOLDS = v70.THRESHOLDS
WIDTHS = v70.WIDTHS
KH = v70.KH
LOG_KH = v70.LOG_KH
K_MPC = v70.K_MPC
H = v70.H
N_K = v70.N_K
KH_MIN = v70.KH_MIN
KH_MAX = v70.KH_MAX

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
CROSSING_RES_MAX = 5.0e-3
SHIFT_RES_RMS_MAX = 5.0e-2
AFFINITY_MAX = 5.0e-2
MIN_ABS_SLOPE = 1.0e-3


def exact_tangent_shift_for_grid(base_delta, plus_delta, minus_delta, logkh):
    """Fixed-baseline crossings and exact odd broadband-power tangent shifts."""
    base_info = v70.baseline_crossings(base_delta, logkh)
    shifts = np.full(
        (LAMBDAS.size, WIDTHS.size, THRESHOLDS.size, Z_GRID.size),
        np.nan,
        dtype=float,
    )
    slopes = np.full((WIDTHS.size, THRESHOLDS.size, Z_GRID.size), np.nan)
    crosses = np.full_like(slopes, np.nan)

    for iw, w in enumerate(WIDTHS):
        xc, base_bar, cross = base_info[float(w)]
        crosses[iw, :, :] = cross

        plus_bars = []
        minus_bars = []
        for il in range(LAMBDAS.size):
            xp, pb = v70.broadband(plus_delta[il], logkh, w)
            xm, mb = v70.broadband(minus_delta[il], logkh, w)
            if not (
                np.allclose(xc, xp, rtol=0.0, atol=1.0e-14)
                and np.allclose(xc, xm, rtol=0.0, atol=1.0e-14)
            ):
                raise RuntimeError('broadband center grids differ')
            plus_bars.append(pb)
            minus_bars.append(mb)

        for it, threshold in enumerate(THRESHOLDS):
            for iz in range(Z_GRID.size):
                x0 = float(cross[it, iz])
                if not np.isfinite(x0):
                    continue
                slope = v70.log_slope_at_crossing(
                    base_delta, logkh, float(w), x0, float(threshold), iz
                )
                slopes[iw, it, iz] = slope

                # At the baseline crossing Dbar(0)=threshold by construction.
                # For an affine perturbation state, Dbar(lambda) is at most
                # quadratic, so this odd combination recovers dDbar/deta|0
                # exactly for any numerical tangent amplification lambda.
                b0 = float(threshold)
                for il, lam in enumerate(LAMBDAS):
                    odd_grid = (
                        plus_bars[il][:, iz] - minus_bars[il][:, iz]
                    ) / (2.0 * float(lam))
                    dbar_deta = float(np.interp(x0, xc, odd_grid))
                    g_ln = dbar_deta / b0
                    shifts[il, iw, it, iz] = -g_ln / slope

    return crosses, slopes, shifts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--class-root', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--npz-out', required=True)
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    force_file, forcing_summary_path = v70.v63.build_forcing(class_root)
    with Path(forcing_summary_path).open() as f:
        forcing_summary = json.load(f)

    base_pk = v70.compute_run(force_file, None)
    plus_pk = np.empty((LAMBDAS.size, N_K, Z_GRID.size), dtype=float)
    minus_pk = np.empty_like(plus_pk)
    for il, lam in enumerate(LAMBDAS):
        plus_pk[il] = v70.compute_run(force_file, +float(lam))
        minus_pk[il] = v70.compute_run(force_file, -float(lam))

    all_pk = [base_pk] + [plus_pk[i] for i in range(LAMBDAS.size)] + [
        minus_pk[i] for i in range(LAMBDAS.size)
    ]
    finite_positive = bool(
        all(np.all(np.isfinite(p)) and np.all(p > 0.0) for p in all_pk)
    )

    base_delta = v70.dimensionless_power(base_pk)
    plus_delta = np.empty_like(plus_pk)
    minus_delta = np.empty_like(minus_pk)
    for il in range(LAMBDAS.size):
        plus_delta[il] = v70.dimensionless_power(plus_pk[il])
        minus_delta[il] = v70.dimensionless_power(minus_pk[il])

    crosses, slopes, shifts = exact_tangent_shift_for_grid(
        base_delta, plus_delta, minus_delta, LOG_KH
    )
    mean_shift, affinity = v70.global_affinity(shifts)

    # Same every-other-grid resolution audit as v0.70.
    idx = np.arange(0, N_K, 2, dtype=int)
    if idx[-1] != N_K - 1:
        idx = np.append(idx, N_K - 1)
    kh_c = KH[idx]
    logkh_c = np.log(kh_c)
    km_c = kh_c * H
    base_delta_c = v70.dimensionless_power(base_pk[idx, :], k_mpc=km_c)
    plus_delta_c = np.empty((LAMBDAS.size, idx.size, Z_GRID.size), dtype=float)
    minus_delta_c = np.empty_like(plus_delta_c)
    for il in range(LAMBDAS.size):
        plus_delta_c[il] = v70.dimensionless_power(
            plus_pk[il, idx, :], k_mpc=km_c
        )
        minus_delta_c[il] = v70.dimensionless_power(
            minus_pk[il, idx, :], k_mpc=km_c
        )

    crosses_c, slopes_c, shifts_c = exact_tangent_shift_for_grid(
        base_delta_c, plus_delta_c, minus_delta_c, logkh_c
    )
    mean_shift_c, _ = v70.global_affinity(shifts_c)

    all_crossings = bool(
        np.all(np.isfinite(crosses)) and np.all(np.isfinite(crosses_c))
    )
    crossing_rel = np.abs(np.exp(crosses_c) - np.exp(crosses)) / np.maximum(
        np.exp(crosses), 1.0e-300
    )
    crossing_res_max = float(np.nanmax(crossing_rel))
    crossing_res_ok = bool(crossing_res_max <= CROSSING_RES_MAX)

    shift_res_rms = v70.normalized_rms_difference(mean_shift, mean_shift_c)
    shift_res_ok = bool(shift_res_rms <= SHIFT_RES_RMS_MAX)

    affinity_max = float(np.nanmax(affinity))
    affinity_ok = bool(affinity_max <= AFFINITY_MAX)

    min_abs_slope = float(np.nanmin(np.abs(slopes)))
    slope_ok = bool(np.isfinite(min_abs_slope) and min_abs_slope >= MIN_ABS_SLOPE)

    forcing_ok = bool(
        float(forcing_summary['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing_summary['cosine']) >= FORCING_COS_MIN
        and bool(forcing_summary['gate'])
    )

    numerical_pass = bool(
        finite_positive and all_crossings and forcing_ok and crossing_res_ok
        and shift_res_ok and affinity_ok and slope_ok
    )

    delta1 = mean_shift[:, 2, :]
    pos_counts = np.sum(delta1 > 0.0, axis=1)
    neg_counts = np.sum(delta1 < 0.0, axis=1)
    width_sign_concordance = int(
        np.sum(np.sign(delta1[0, :]) == np.sign(delta1[1, :]))
    )

    if not numerical_pass:
        classification = 'V071_EXACT_BROADBAND_ONSET_TANGENT_FAIL'
    elif np.all(pos_counts >= 5) and width_sign_concordance >= 6:
        classification = 'V071_EXACT_BROADBAND_MEMORY_DELAY_SUPPORTED'
    elif np.all(neg_counts >= 5) and width_sign_concordance >= 6:
        classification = 'V071_EXACT_BROADBAND_MEMORY_ADVANCE_SUPPORTED'
    else:
        classification = 'V071_EXACT_BROADBAND_ONSET_SHIFT_MIXED'

    transition_fraction = float(
        np.mean((np.exp(crosses) >= 0.08) & (np.exp(crosses) <= 0.20))
    )

    rows = []
    for iw, w in enumerate(WIDTHS):
        for it, threshold in enumerate(THRESHOLDS):
            for iz, z in enumerate(Z_GRID):
                rows.append({
                    'width_ln_k': float(w),
                    'DeltaL2_threshold': float(threshold),
                    'z': float(z),
                    'baseline_k_h_per_Mpc': float(math.exp(crosses[iw, it, iz])),
                    'baseline_log_slope': float(slopes[iw, it, iz]),
                    'mean_dln_k_threshold_deta': float(mean_shift[iw, it, iz]),
                    'dln_k_threshold_deta_by_lambda': {
                        str(float(lam)): float(shifts[il, iw, it, iz])
                        for il, lam in enumerate(LAMBDAS)
                    },
                    'coarse_grid_mean_dln_k_threshold_deta': float(
                        mean_shift_c[iw, it, iz]
                    ),
                })

    result = {
        'classification': classification,
        'predata_classification': 'V071_PREDATA_EXACT_BROADBAND_ONSET_TANGENT',
        'uses_observational_data': False,
        'result_informed_followup': True,
        'historical_classifications_unchanged': {
            'v067': 'V067_GROWTH_KERNEL_CLOSURE_AFFINITY_FAIL',
            'v068': 'V068_LINEAR_SCALE_MEMORY_RESPONSE_MAP_FAIL',
            'v069': 'V069_NONLINEAR_ONSET_DIAGNOSTIC_FAIL',
            'v070': 'V070_BROADBAND_NONLINEAR_ONSET_TANGENT_FAIL',
        },
        'scope': 'Linear-theory broadband threshold diagnostic only; no nonlinear evolution is simulated.',
        'estimator': {
            'partial_eta_Dbar': '[Dbar(+lambda)-Dbar(-lambda)]/(2 lambda)',
            'partial_eta_ln_Dbar': 'partial_eta_Dbar / Dbar(0)',
            'baseline_Dbar_at_crossing': 'threshold',
            'implicit_shift': '-(partial_eta ln Dbar)/(partial_ln_k ln Dbar)',
            'v070_log_finite_difference_not_reused': True,
        },
        'locked_model': {
            'KB': v70.v63.KB,
            'tauH0': v70.v63.TAUH0,
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
        },
        'broadband_definition': {
            'thresholds_DeltaL2': [float(x) for x in THRESHOLDS],
            'logk_top_hat_widths': [float(x) for x in WIDTHS],
        },
        'forcing': {
            'relative_L2_control_vs_primary': float(
                forcing_summary['relative_L2_control_vs_primary']
            ),
            'cosine': float(forcing_summary['cosine']),
        },
        'baseline_k_threshold_h_per_Mpc': np.exp(crosses).tolist(),
        'baseline_log_slope_at_threshold': slopes.tolist(),
        'mean_dln_k_threshold_deta': mean_shift.tolist(),
        'dln_k_threshold_deta_by_lambda': shifts.tolist(),
        'lambda_affinity_by_lambda': {
            str(float(lam)): float(affinity[il]) for il, lam in enumerate(LAMBDAS)
        },
        'rows': rows,
        'science_summary': {
            'DeltaL2_eq_1_positive_count_of_7_by_width': {
                str(float(WIDTHS[iw])): int(pos_counts[iw])
                for iw in range(WIDTHS.size)
            },
            'DeltaL2_eq_1_negative_count_of_7_by_width': {
                str(float(WIDTHS[iw])): int(neg_counts[iw])
                for iw in range(WIDTHS.size)
            },
            'DeltaL2_eq_1_width_sign_concordance_count_of_7': width_sign_concordance,
            'fraction_of_baseline_broadband_threshold_crossings_in_v068_0p08_to_0p20_band': transition_fraction,
        },
        'gates': {
            'all_spectra_finite_and_positive': finite_positive,
            'all_broadband_thresholds_bracketed_full_and_coarse': all_crossings,
            'forcing_pass': forcing_ok,
            'baseline_fine_vs_every_other_grid_crossing_relative_difference_max': crossing_res_max,
            'baseline_crossing_resolution_limit': CROSSING_RES_MAX,
            'baseline_crossing_resolution_pass': crossing_res_ok,
            'implicit_shift_fine_vs_every_other_grid_global_normalized_RMS': shift_res_rms,
            'implicit_shift_resolution_limit': SHIFT_RES_RMS_MAX,
            'implicit_shift_resolution_pass': shift_res_ok,
            'exact_odd_tangent_shift_lambda_affinity_max': affinity_max,
            'exact_odd_tangent_shift_lambda_affinity_limit': AFFINITY_MAX,
            'exact_odd_tangent_shift_lambda_affinity_pass': affinity_ok,
            'minimum_absolute_baseline_log_slope_at_threshold': min_abs_slope,
            'minimum_absolute_slope_limit': MIN_ABS_SLOPE,
            'minimum_absolute_slope_pass': slope_ok,
            'numerical_pass': numerical_pass,
        },
        'interpretation_policy': (
            'Any delay/advance label refers only to the broadband threshold of the LINEAR dimensionless power. '
            'It does not establish nonlinear saturation, halo behavior, screening, N-body evolution, or observational detection.'
        ),
    }

    Path(args.json_out).write_text(json.dumps(result, indent=2))
    np.savez_compressed(
        args.npz_out,
        k_h_per_Mpc=KH,
        z=Z_GRID,
        thresholds=THRESHOLDS,
        widths=WIDTHS,
        baseline_pk=base_pk,
        plus_pk=plus_pk,
        minus_pk=minus_pk,
        baseline_DeltaL2=base_delta,
        baseline_k_threshold=np.exp(crosses),
        baseline_log_slope=slopes,
        dln_k_threshold_deta=shifts,
        mean_dln_k_threshold_deta=mean_shift,
        coarse_mean_dln_k_threshold_deta=mean_shift_c,
        lambda_affinity=affinity,
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
