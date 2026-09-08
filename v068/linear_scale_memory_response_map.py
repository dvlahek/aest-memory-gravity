#!/usr/bin/env python3
"""v0.68 preregistered low-k matter/Weyl memory-response map.

This is a result-informed follow-up to the historical v0.67 FAIL.  It does not
alter any earlier result and deliberately avoids extending the UV-dominated
sigma8 integral.  Instead it evaluates the eta=0 externally forced tangent on
the exact (k,z) grid that was preregistered in v0.63 before the v0.63 result.
"""

from pathlib import Path
import argparse
import json
import math
import os
import sys

import numpy as np
from scipy.interpolate import RegularGridInterpolator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import v063.theory_response_map as v63

LAMBDAS = np.array([10.0, 5.0, 2.5, 1.25], dtype=float)
K_GRID = np.array([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], dtype=float)
Z_GRID = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5], dtype=float)

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
INTERP_REL_MAX = 5.0e-3
MATTER_AFFINITY_MAX = 5.0e-3
WEYL_AFFINITY_MAX = 5.0e-3

H = v63.START['H0'] / 100.0
K_MPC = K_GRID * H


def _fixed_points():
    return np.array(
        [[math.log(float(k)), float(z)] for k in K_GRID for z in Z_GRID],
        dtype=float,
    )


def interpolate_positive_power_to_fixed_grid(power, k_h, z):
    """Fixed log-power interpolation in (log k,z), as preregistered."""
    p = np.asarray(power, dtype=float)
    k = np.asarray(k_h, dtype=float)
    zz = np.asarray(z, dtype=float)
    if p.shape != (k.size, zz.size):
        raise RuntimeError(f'power/grid shape mismatch: {p.shape}, {k.size}, {zz.size}')
    if not (np.all(np.isfinite(p)) and np.all(p > 0.0)):
        raise RuntimeError('non-positive or non-finite power encountered in log interpolation')
    if not (np.all(np.isfinite(k)) and np.all(k > 0.0) and np.all(np.isfinite(zz))):
        raise RuntimeError('non-finite native k/z grid')

    ik = np.argsort(k)
    iz = np.argsort(zz)
    ks = k[ik]
    zs = zz[iz]
    ps = p[np.ix_(ik, iz)]
    if np.any(np.diff(ks) <= 0.0) or np.any(np.diff(zs) <= 0.0):
        raise RuntimeError('native k/z grid is not strictly monotone after sorting')
    if K_GRID[0] < ks[0] or K_GRID[-1] > ks[-1]:
        raise RuntimeError(f'fixed k grid outside native range: fixed={K_GRID[[0,-1]]}, native={ks[[0,-1]]}')
    if Z_GRID[0] < zs[0] or Z_GRID[-1] > zs[-1]:
        raise RuntimeError(f'fixed z grid outside native range: fixed={Z_GRID[[0,-1]]}, native={zs[[0,-1]]}')

    interp = RegularGridInterpolator(
        (np.log(ks), zs),
        np.log(ps),
        method='linear',
        bounds_error=True,
    )
    vals = np.exp(interp(_fixed_points())).reshape(K_GRID.size, Z_GRID.size)
    return vals


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
        c.set(dict(v63.class_params()))
        c.compute()

        pm_exact = np.empty((K_GRID.size, Z_GRID.size), dtype=float)
        for ik, k_mpc in enumerate(K_MPC):
            for iz, z in enumerate(Z_GRID):
                pm_exact[ik, iz] = float(c.pk_lin(float(k_mpc), float(z)))

        pm_native, k_native, z_native = c.get_pk_and_k_and_z(
            nonlinear=False,
            only_clustering_species=False,
            h_units=True,
        )
        weyl_native, kw_native, zw_native = c.get_Weyl_pk_and_k_and_z(
            nonlinear=False,
            h_units=True,
        )
        k_native = np.asarray(k_native, dtype=float)
        z_native = np.asarray(z_native, dtype=float)
        kw_native = np.asarray(kw_native, dtype=float)
        zw_native = np.asarray(zw_native, dtype=float)
        if not np.allclose(k_native, kw_native, rtol=0.0, atol=1.0e-13):
            raise RuntimeError('native matter/Weyl k grids differ')
        if not np.allclose(z_native, zw_native, rtol=0.0, atol=1.0e-12):
            raise RuntimeError('native matter/Weyl z grids differ')

        pm_interp = interpolate_positive_power_to_fixed_grid(
            np.asarray(pm_native, dtype=float), k_native, z_native
        )
        weyl_fixed = interpolate_positive_power_to_fixed_grid(
            np.asarray(weyl_native, dtype=float), k_native, z_native
        )
        interp_rel = np.abs(pm_interp - pm_exact) / np.maximum(np.abs(pm_exact), 1.0e-300)

        result = {
            'pm': pm_exact,
            'weyl': weyl_fixed,
            'pm_interp': pm_interp,
            'interp_rel': interp_rel,
            'native_k_minmax': [float(np.min(k_native)), float(np.max(k_native))],
            'native_z_minmax': [float(np.min(z_native)), float(np.max(z_native))],
        }
        c.struct_cleanup()
        c.empty()
        return result
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def response(base, plus, minus, lam):
    b = np.asarray(base, dtype=float)
    p = np.asarray(plus, dtype=float)
    m = np.asarray(minus, dtype=float)
    if not (np.all(np.isfinite(b)) and np.all(b > 0.0)):
        raise RuntimeError('baseline power is not finite and strictly positive')
    return (p - m) / (2.0 * float(lam) * b)


def affinity_by_lambda(values):
    arr = np.asarray(values, dtype=float)
    mean = np.mean(arr, axis=0)
    den = float(np.sum(mean * mean))
    eps = np.empty(arr.shape[0], dtype=float)
    for il in range(arr.shape[0]):
        num = float(np.sum((arr[il] - mean) ** 2))
        eps[il] = math.sqrt(max(num, 0.0) / max(den, 1.0e-300))
    return mean, eps


def sign_topology(matter, weyl):
    m = np.asarray(matter, dtype=float)
    w = np.asarray(weyl, dtype=float)
    if np.any(m == 0.0) or np.any(w == 0.0):
        return 'EXACT_ZERO_PRESENT'
    if np.any(m * w < 0.0):
        return 'MATTER_WEYL_SIGN_SPLIT_PRESENT'
    if np.all(m < 0.0) and np.all(w < 0.0):
        return 'COHERENT_NEGATIVE_BOTH_FIELDS'
    if np.all(m > 0.0) and np.all(w > 0.0):
        return 'COHERENT_POSITIVE_BOTH_FIELDS'
    return 'MIXED_WITHOUT_POINTWISE_SIGN_SPLIT'


def field_stats(x):
    a = np.asarray(x, dtype=float)
    return {
        'rms_abs_response': float(np.sqrt(np.mean(a * a))),
        'mean_abs_response': float(np.mean(np.abs(a))),
        'max_abs_response': float(np.max(np.abs(a))),
        'fraction_negative': float(np.mean(a < 0.0)),
        'fraction_positive': float(np.mean(a > 0.0)),
        'fraction_exact_zero': float(np.mean(a == 0.0)),
    }


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

    base = compute_run(force_file, None)
    gm = np.empty((LAMBDAS.size, K_GRID.size, Z_GRID.size), dtype=float)
    gw = np.empty_like(gm)
    interp_max_by_run = {'baseline': float(np.max(base['interp_rel']))}

    for il, lam in enumerate(LAMBDAS):
        plus = compute_run(force_file, +float(lam))
        minus = compute_run(force_file, -float(lam))
        gm[il] = response(base['pm'], plus['pm'], minus['pm'], lam)
        gw[il] = response(base['weyl'], plus['weyl'], minus['weyl'], lam)
        interp_max_by_run[f'+{float(lam)}'] = float(np.max(plus['interp_rel']))
        interp_max_by_run[f'-{float(lam)}'] = float(np.max(minus['interp_rel']))

    mean_m, eps_m = affinity_by_lambda(gm)
    mean_w, eps_w = affinity_by_lambda(gw)
    delta_wm = mean_w - mean_m

    finite = bool(
        np.all(np.isfinite(base['pm']))
        and np.all(np.isfinite(base['weyl']))
        and np.all(np.isfinite(gm))
        and np.all(np.isfinite(gw))
        and np.all(np.isfinite(eps_m))
        and np.all(np.isfinite(eps_w))
    )
    forcing_ok = bool(
        float(forcing_summary['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing_summary['cosine']) >= FORCING_COS_MIN
        and bool(forcing_summary['gate'])
    )
    interpolation_max = float(max(interp_max_by_run.values()))
    interpolation_ok = bool(interpolation_max <= INTERP_REL_MAX)
    matter_affinity_value = float(np.max(eps_m))
    weyl_affinity_value = float(np.max(eps_w))
    matter_affinity_ok = bool(matter_affinity_value <= MATTER_AFFINITY_MAX)
    weyl_affinity_ok = bool(weyl_affinity_value <= WEYL_AFFINITY_MAX)
    passed = bool(
        finite and forcing_ok and interpolation_ok
        and matter_affinity_ok and weyl_affinity_ok
    )
    classification = (
        'V068_LINEAR_SCALE_MEMORY_RESPONSE_MAP_PASS'
        if passed else
        'V068_LINEAR_SCALE_MEMORY_RESPONSE_MAP_FAIL'
    )

    flat_m = mean_m.ravel()
    flat_w = mean_w.ravel()
    if float(np.std(flat_m)) > 0.0 and float(np.std(flat_w)) > 0.0:
        corr = float(np.corrcoef(flat_m, flat_w)[0, 1])
    else:
        corr = None
    rms_m = float(np.sqrt(np.mean(flat_m * flat_m)))
    rms_w = float(np.sqrt(np.mean(flat_w * flat_w)))
    rms_ratio = rms_w / max(rms_m, 1.0e-300)
    sign_concordance = float(np.mean(np.sign(flat_m) == np.sign(flat_w)))
    idiff = int(np.argmax(np.abs(delta_wm)))
    ik_diff, iz_diff = np.unravel_index(idiff, delta_wm.shape)

    grid_rows = []
    for ik, k in enumerate(K_GRID):
        for iz, z in enumerate(Z_GRID):
            grid_rows.append({
                'k_h_per_Mpc': float(k),
                'z': float(z),
                'mean_dln_Pm_deta': float(mean_m[ik, iz]),
                'mean_dln_PWeyl_deta': float(mean_w[ik, iz]),
                'Delta_Wm': float(delta_wm[ik, iz]),
                'dln_Pm_deta_by_lambda': {
                    str(float(lam)): float(gm[il, ik, iz])
                    for il, lam in enumerate(LAMBDAS)
                },
                'dln_PWeyl_deta_by_lambda': {
                    str(float(lam)): float(gw[il, ik, iz])
                    for il, lam in enumerate(LAMBDAS)
                },
            })

    per_z = []
    for iz, z in enumerate(Z_GRID):
        im = int(np.argmax(np.abs(mean_m[:, iz])))
        iw = int(np.argmax(np.abs(mean_w[:, iz])))
        per_z.append({
            'z': float(z),
            'matter': {
                **field_stats(mean_m[:, iz]),
                'max_abs_k_h_per_Mpc': float(K_GRID[im]),
                'signed_response_at_max': float(mean_m[im, iz]),
            },
            'weyl': {
                **field_stats(mean_w[:, iz]),
                'max_abs_k_h_per_Mpc': float(K_GRID[iw]),
                'signed_response_at_max': float(mean_w[iw, iz]),
            },
        })

    per_k = []
    for ik, k in enumerate(K_GRID):
        im = int(np.argmax(np.abs(mean_m[ik, :])))
        iw = int(np.argmax(np.abs(mean_w[ik, :])))
        per_k.append({
            'k_h_per_Mpc': float(k),
            'matter': {
                **field_stats(mean_m[ik, :]),
                'max_abs_z': float(Z_GRID[im]),
                'signed_response_at_max': float(mean_m[ik, im]),
            },
            'weyl': {
                **field_stats(mean_w[ik, :]),
                'max_abs_z': float(Z_GRID[iw]),
                'signed_response_at_max': float(mean_w[ik, iw]),
            },
        })

    result = {
        'classification': classification,
        'predata_classification': 'V068_PREDATA_LINEAR_SCALE_MEMORY_RESPONSE_MAP',
        'uses_observational_data': False,
        'historical_classifications_unchanged': {
            'v065': 'V065_SMOOTH_GROWTH_TANGENT_LIMIT_FAIL',
            'v066': 'V066_EXACT_TANGENT_GROWTH_KERNEL_FAIL',
            'v067': 'V067_GROWTH_KERNEL_CLOSURE_AFFINITY_FAIL',
        },
        'locked_model': {
            'KB': v63.KB,
            'tauH0': v63.TAUH0,
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': [float(x) for x in LAMBDAS],
            'lambda_is_numerical_tangent_amplification_not_physical_eta': True,
            'linear_theory_only': True,
            'nonlinear_corrections': False,
        },
        'fixed_grid': {
            'provenance': 'v063/predata_theory_target_selection.json',
            'k_h_per_Mpc': [float(x) for x in K_GRID],
            'z': [float(x) for x in Z_GRID],
            'n_points': int(K_GRID.size * Z_GRID.size),
        },
        'forcing': {
            'summary_file': str(Path(forcing_summary_path).relative_to(ROOT)),
            'relative_L2_control_vs_primary': float(forcing_summary['relative_L2_control_vs_primary']),
            'cosine': float(forcing_summary['cosine']),
        },
        'interpolation_audit': {
            'prescription': 'linear interpolation of log power in (log k,z)',
            'matter_native_interpolation_vs_direct_pk_lin_max_relative_error_by_run': interp_max_by_run,
            'max_relative_error_all_runs': interpolation_max,
        },
        'lambda_affinity': {
            'definition': 'equal-weight RMS deviation from four-lambda consensus divided by RMS consensus over all 42 fixed grid points',
            'matter_by_lambda': {
                str(float(lam)): float(eps_m[il]) for il, lam in enumerate(LAMBDAS)
            },
            'weyl_by_lambda': {
                str(float(lam)): float(eps_w[il]) for il, lam in enumerate(LAMBDAS)
            },
        },
        'sign_topology': sign_topology(mean_m, mean_w),
        'consensus_summary': {
            'matter': field_stats(mean_m),
            'weyl': field_stats(mean_w),
            'matter_weyl_sign_concordance_fraction': sign_concordance,
            'matter_weyl_Pearson_correlation': corr,
            'Weyl_to_matter_RMS_response_ratio': float(rms_ratio),
            'largest_abs_matter_weyl_difference': {
                'k_h_per_Mpc': float(K_GRID[ik_diff]),
                'z': float(Z_GRID[iz_diff]),
                'Delta_Wm': float(delta_wm[ik_diff, iz_diff]),
                'matter': float(mean_m[ik_diff, iz_diff]),
                'weyl': float(mean_w[ik_diff, iz_diff]),
            },
        },
        'grid_response': grid_rows,
        'per_redshift_summary': per_z,
        'per_k_summary': per_k,
        'gates': {
            'all_values_finite': finite,
            'forcing_control_vs_primary_relative_L2_limit': FORCING_L2_MAX,
            'forcing_control_vs_primary_cosine_limit': FORCING_COS_MIN,
            'forcing_pass': forcing_ok,
            'native_to_fixed_matter_interpolation_max_relative_error': interpolation_max,
            'native_to_fixed_matter_interpolation_limit': INTERP_REL_MAX,
            'native_to_fixed_matter_interpolation_pass': interpolation_ok,
            'matter_lambda_affinity_max': matter_affinity_value,
            'matter_lambda_affinity_limit': MATTER_AFFINITY_MAX,
            'matter_lambda_affinity_pass': matter_affinity_ok,
            'weyl_lambda_affinity_max': weyl_affinity_value,
            'weyl_lambda_affinity_limit': WEYL_AFFINITY_MAX,
            'weyl_lambda_affinity_pass': weyl_affinity_ok,
            'pass': passed,
        },
        'interpretation_policy': 'PASS certifies numerical stability of the data-blind low-k response map only. Sign and amplitude are reported outcomes, not PASS requirements, and no observational likelihood is used.',
    }

    Path(args.json_out).write_text(json.dumps(result, indent=2))
    np.savez_compressed(
        args.npz_out,
        k_h_per_Mpc=K_GRID,
        z=Z_GRID,
        lambdas=LAMBDAS,
        dln_Pm_deta_by_lambda=gm,
        dln_PWeyl_deta_by_lambda=gw,
        mean_dln_Pm_deta=mean_m,
        mean_dln_PWeyl_deta=mean_w,
        Delta_Wm=delta_wm,
        baseline_Pm=base['pm'],
        baseline_PWeyl=base['weyl'],
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
