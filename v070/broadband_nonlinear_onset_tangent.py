#!/usr/bin/env python3
"""v0.70 preregistered broadband nonlinear-onset tangent diagnostic.

Result-informed follow-up to preserved v0.67--v0.69 results.  The physical
model and eta=0 tangent forcing are unchanged.  v0.70 replaces the grid-
sensitive pointwise first crossing used in v0.69 with fixed log-k top-hat
band averages of the linear dimensionless matter power.  The threshold shift
is then obtained by implicit differentiation at the baseline broadband
crossing, avoiding +lambda/-lambda crossing-branch switching.

This remains a LINEAR-theory diagnostic.  It is not a nonlinear simulation.
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
WIDTHS = np.array([0.1, 0.2], dtype=float)
KH_MIN = 0.005
KH_MAX = 2.0
N_K = 2401
KH = np.geomspace(KH_MIN, KH_MAX, N_K)
LOG_KH = np.log(KH)
H = v63.START['H0'] / 100.0
K_MPC = KH * H

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
CROSSING_RES_MAX = 5.0e-3
SHIFT_RES_RMS_MAX = 5.0e-2
AFFINITY_MAX = 5.0e-2
MIN_ABS_SLOPE = 1.0e-3


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


def dimensionless_power(pk, k_mpc=K_MPC):
    arr = np.asarray(pk, dtype=float)
    kk = np.asarray(k_mpc, dtype=float)
    return (kk[:, None] ** 3) * arr / (2.0 * math.pi**2)


def cumulative_trapezoid(y, x):
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(y, dtype=float)
    dx = np.diff(x)
    out[1:, :] = np.cumsum(
        0.5 * (y[:-1, :] + y[1:, :]) * dx[:, None], axis=0
    )
    return out


def broadband(delta2, logkh, width):
    """Arithmetic top-hat average of Delta^2 over a fixed ln-k width."""
    d = np.asarray(delta2, dtype=float)
    x = np.asarray(logkh, dtype=float)
    w = float(width)
    half = 0.5 * w
    valid = (x >= x[0] + half) & (x <= x[-1] - half)
    xc = x[valid]
    integ = cumulative_trapezoid(d, x)
    out = np.empty((xc.size, d.shape[1]), dtype=float)
    for iz in range(d.shape[1]):
        c = integ[:, iz]
        ca = np.interp(xc - half, x, c)
        cb = np.interp(xc + half, x, c)
        out[:, iz] = (cb - ca) / w
    return xc, out


def first_upward_crossing(x, y, threshold):
    xx = np.asarray(x, dtype=float)
    yy = np.asarray(y, dtype=float)
    t = float(threshold)
    if not (
        xx.ndim == 1 and yy.ndim == 1 and xx.size == yy.size
        and np.all(np.isfinite(xx)) and np.all(np.isfinite(yy))
        and np.all(yy > 0.0)
    ):
        return None
    lt = math.log(t)
    ly = np.log(yy)
    for i in range(xx.size - 1):
        if yy[i] < t <= yy[i + 1]:
            y0, y1 = ly[i], ly[i + 1]
            if y1 == y0:
                return 0.5 * (xx[i] + xx[i + 1])
            f = (lt - y0) / (y1 - y0)
            return float(xx[i] + f * (xx[i + 1] - xx[i]))
    return None


def baseline_crossings(base_delta, logkh):
    result = {}
    for w in WIDTHS:
        xc, db = broadband(base_delta, logkh, w)
        cross = np.full((THRESHOLDS.size, Z_GRID.size), np.nan, dtype=float)
        for it, t in enumerate(THRESHOLDS):
            for iz in range(Z_GRID.size):
                x0 = first_upward_crossing(xc, db[:, iz], t)
                if x0 is not None:
                    cross[it, iz] = x0
        result[float(w)] = (xc, db, cross)
    return result


def log_slope_at_crossing(base_delta, logkh, width, xcross, threshold, iz):
    """Exact moving-top-hat derivative for the interpolated input curve."""
    w = float(width)
    half = 0.5 * w
    d = np.asarray(base_delta[:, iz], dtype=float)
    left = float(np.interp(xcross - half, logkh, d))
    right = float(np.interp(xcross + half, logkh, d))
    dbar = float(threshold)
    return (right - left) / (w * dbar)


def tangent_shift_for_grid(base_delta, plus_delta, minus_delta, logkh):
    """Return baseline crossings and implicit shifts for all lambdas/widths."""
    base_info = baseline_crossings(base_delta, logkh)
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
            xp, pb = broadband(plus_delta[il], logkh, w)
            xm, mb = broadband(minus_delta[il], logkh, w)
            if not (
                np.allclose(xc, xp, rtol=0.0, atol=1.0e-14)
                and np.allclose(xc, xm, rtol=0.0, atol=1.0e-14)
            ):
                raise RuntimeError('broadband center grids differ')
            plus_bars.append(pb)
            minus_bars.append(mb)

        for it, t in enumerate(THRESHOLDS):
            for iz in range(Z_GRID.size):
                x0 = float(cross[it, iz])
                if not np.isfinite(x0):
                    continue
                slope = log_slope_at_crossing(
                    base_delta, logkh, float(w), x0, float(t), iz
                )
                slopes[iw, it, iz] = slope
                for il, lam in enumerate(LAMBDAS):
                    lp = np.log(plus_bars[il][:, iz])
                    lm = np.log(minus_bars[il][:, iz])
                    g = float(np.interp(x0, xc, (lp - lm) / (2.0 * lam)))
                    shifts[il, iw, it, iz] = -g / slope

    return crosses, slopes, shifts


def global_affinity(arr):
    a = np.asarray(arr, dtype=float)
    mean = np.mean(a, axis=0)
    den = float(np.sum(mean * mean))
    eps = np.empty(a.shape[0], dtype=float)
    for il in range(a.shape[0]):
        num = float(np.sum((a[il] - mean) ** 2))
        eps[il] = math.sqrt(max(num, 0.0) / max(den, 1.0e-300))
    return mean, eps


def normalized_rms_difference(a, b):
    aa = np.asarray(a, dtype=float)
    bb = np.asarray(b, dtype=float)
    num = float(np.sum((aa - bb) ** 2))
    den = float(np.sum(aa * aa))
    return math.sqrt(max(num, 0.0) / max(den, 1.0e-300))


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
    plus_pk = np.empty((LAMBDAS.size, N_K, Z_GRID.size), dtype=float)
    minus_pk = np.empty_like(plus_pk)
    for il, lam in enumerate(LAMBDAS):
        plus_pk[il] = compute_run(force_file, +float(lam))
        minus_pk[il] = compute_run(force_file, -float(lam))

    all_pk = [base_pk] + [plus_pk[i] for i in range(LAMBDAS.size)] + [
        minus_pk[i] for i in range(LAMBDAS.size)
    ]
    finite_positive = bool(
        all(np.all(np.isfinite(p)) and np.all(p > 0.0) for p in all_pk)
    )

    base_delta = dimensionless_power(base_pk)
    plus_delta = np.empty_like(plus_pk)
    minus_delta = np.empty_like(minus_pk)
    for il in range(LAMBDAS.size):
        plus_delta[il] = dimensionless_power(plus_pk[il])
        minus_delta[il] = dimensionless_power(minus_pk[il])

    crosses, slopes, shifts = tangent_shift_for_grid(
        base_delta, plus_delta, minus_delta, LOG_KH
    )
    mean_shift, affinity = global_affinity(shifts)

    # Resolution audit from the already-computed direct spectrum: every other k.
    idx = np.arange(0, N_K, 2, dtype=int)
    if idx[-1] != N_K - 1:
        idx = np.append(idx, N_K - 1)
    kh_c = KH[idx]
    logkh_c = np.log(kh_c)
    km_c = kh_c * H
    base_delta_c = dimensionless_power(base_pk[idx, :], k_mpc=km_c)
    plus_delta_c = np.empty((LAMBDAS.size, idx.size, Z_GRID.size), dtype=float)
    minus_delta_c = np.empty_like(plus_delta_c)
    for il in range(LAMBDAS.size):
        plus_delta_c[il] = dimensionless_power(plus_pk[il, idx, :], k_mpc=km_c)
        minus_delta_c[il] = dimensionless_power(minus_pk[il, idx, :], k_mpc=km_c)

    crosses_c, slopes_c, shifts_c = tangent_shift_for_grid(
        base_delta_c, plus_delta_c, minus_delta_c, logkh_c
    )
    mean_shift_c, _ = global_affinity(shifts_c)

    all_crossings = bool(np.all(np.isfinite(crosses)) and np.all(np.isfinite(crosses_c)))
    crossing_rel = np.abs(np.exp(crosses_c) - np.exp(crosses)) / np.maximum(
        np.exp(crosses), 1.0e-300
    )
    crossing_res_max = float(np.nanmax(crossing_rel))
    crossing_res_ok = bool(crossing_res_max <= CROSSING_RES_MAX)

    shift_res_rms = normalized_rms_difference(mean_shift, mean_shift_c)
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
        classification = 'V070_BROADBAND_NONLINEAR_ONSET_TANGENT_FAIL'
    elif np.all(pos_counts >= 5) and width_sign_concordance >= 6:
        classification = 'V070_BROADBAND_MEMORY_DELAY_SUPPORTED'
    elif np.all(neg_counts >= 5) and width_sign_concordance >= 6:
        classification = 'V070_BROADBAND_MEMORY_ADVANCE_SUPPORTED'
    else:
        classification = 'V070_BROADBAND_ONSET_SHIFT_MIXED'

    median_abs_by_width_threshold = np.median(np.abs(mean_shift), axis=2)
    transition_fraction = float(
        np.mean((np.exp(crosses) >= 0.08) & (np.exp(crosses) <= 0.20))
    )

    rows = []
    for iw, w in enumerate(WIDTHS):
        for it, t in enumerate(THRESHOLDS):
            for iz, z in enumerate(Z_GRID):
                rows.append({
                    'width_ln_k': float(w),
                    'DeltaL2_threshold': float(t),
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
                    'baseline_k_in_v068_transition_band_0p08_to_0p20': bool(
                        0.08 <= math.exp(crosses[iw, it, iz]) <= 0.20
                    ),
                })

    result = {
        'classification': classification,
        'predata_classification': 'V070_PREDATA_BROADBAND_NONLINEAR_ONSET_TANGENT',
        'uses_observational_data': False,
        'result_informed_followup': True,
        'historical_classifications_unchanged': {
            'v067': 'V067_GROWTH_KERNEL_CLOSURE_AFFINITY_FAIL',
            'v068': 'V068_LINEAR_SCALE_MEMORY_RESPONSE_MAP_FAIL',
            'v069': 'V069_NONLINEAR_ONSET_DIAGNOSTIC_FAIL',
        },
        'scope': 'Linear-theory broadband threshold diagnostic only; no nonlinear evolution is simulated.',
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
        'broadband_definition': {
            'thresholds_DeltaL2': [float(x) for x in THRESHOLDS],
            'logk_top_hat_widths': [float(x) for x in WIDTHS],
            'average': 'arithmetic mean of Delta_L^2 over the centered ln-k top-hat',
            'implicit_shift': 'd ln k_thr/d eta = -(partial_eta ln Dbar)/(partial_ln_k ln Dbar) at the baseline crossing',
        },
        'forcing': {
            'summary_file': str(Path(forcing_summary_path).relative_to(ROOT)),
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
            'median_abs_dln_k_threshold_deta_by_width_and_threshold': {
                str(float(WIDTHS[iw])): {
                    str(float(THRESHOLDS[it])): float(
                        median_abs_by_width_threshold[iw, it]
                    )
                    for it in range(THRESHOLDS.size)
                }
                for iw in range(WIDTHS.size)
            },
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
            'implicit_shift_lambda_affinity_max': affinity_max,
            'implicit_shift_lambda_affinity_limit': AFFINITY_MAX,
            'implicit_shift_lambda_affinity_pass': affinity_ok,
            'minimum_absolute_baseline_log_slope_at_threshold': min_abs_slope,
            'minimum_absolute_slope_limit': MIN_ABS_SLOPE,
            'minimum_absolute_slope_pass': slope_ok,
            'numerical_pass': numerical_pass,
        },
        'interpretation_policy': (
            'Any delay/advance label refers only to the broadband threshold of the LINEAR dimensionless power. '
            'It does not establish nonlinear saturation, halo behavior, screening, N-body evolution, or an observational detection.'
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
