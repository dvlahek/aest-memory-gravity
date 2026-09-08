#!/usr/bin/env python3
"""v0.67 preregistered growth-kernel closure and tangent-affinity audit.

This is a result-informed follow-up to the historical v0.66 FAIL.  It does not
alter any v0.65/v0.66 result.  The frozen physical model and tangent forcing
construction are unchanged.  Only the numerical k support is extended so the
k-dependent forcing file and P(k) response can be audited beyond the v0.66
boundary at 1.999 h/Mpc.
"""

from pathlib import Path
import argparse
import json
import math
import os
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import v063.theory_response_map as v63

LAMBDAS = np.array([10.0, 5.0, 2.5, 1.25], dtype=float)
PRIMARY_Z = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], dtype=float)
CONTEXT_Z = np.array([1.0, 1.2, 1.5], dtype=float)
ALL_Z = np.concatenate([PRIMARY_Z, CONTEXT_Z])

PKMAX_CLASS = 16.1
KH_MIN = 1.0e-4
KH_MAX = 16.0
N_K = 4096
KH = np.geomspace(KH_MIN, KH_MAX, N_K)
LOG_KH = np.log(KH)
CAPS = np.array([2.0, 4.0, 8.0, 16.0], dtype=float)
BINS = [
    (1.0e-4, 0.03),
    (0.03, 0.08),
    (0.08, 0.20),
    (0.20, 0.50),
    (0.50, 2.0),
    (2.0, 4.0),
    (4.0, 8.0),
    (8.0, 16.0),
]

H0 = v63.START['H0']
H = H0 / 100.0
K_MPC = KH * H
R8_MPC = 8.0 / H

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
FULL_RECON_MAX = 5.0e-3
TAIL_8_16_MAX = 5.0e-3
R_LAMBDA_SPREAD_MAX = 5.0e-3
WEIGHTED_AFFINITY_MAX = 5.0e-3
KERNEL_IDENTITY_MAX = 5.0e-3


def top_hat(x):
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    small = np.abs(x) < 1.0e-3
    xs = x[small]
    out[small] = 1.0 - xs * xs / 10.0 + xs**4 / 280.0
    xb = x[~small]
    out[~small] = 3.0 * (np.sin(xb) - xb * np.cos(xb)) / (xb**3)
    return out


W8 = top_hat(K_MPC * R8_MPC)


def trapz_log(y):
    return float(np.trapezoid(np.asarray(y, dtype=float), LOG_KH))


def integrate_log_interval(y, lo, hi):
    if not (KH_MIN <= lo < hi <= KH_MAX):
        raise ValueError((lo, hi))
    x0 = math.log(lo)
    x1 = math.log(hi)
    mask = (LOG_KH > x0) & (LOG_KH < x1)
    xx = np.concatenate([[x0], LOG_KH[mask], [x1]])
    yy0 = np.asarray(y, dtype=float)
    yy = np.concatenate([
        [np.interp(x0, LOG_KH, yy0)],
        yy0[mask],
        [np.interp(x1, LOG_KH, yy0)],
    ])
    return float(np.trapezoid(yy, xx))


def integrate_log_to_cap(y, cap):
    return integrate_log_interval(y, KH_MIN, float(cap))


def relerr(a, b):
    return abs(float(a) - float(b)) / max(abs(float(b)), 1.0e-300)


def rewrite_ini_extended(text, root):
    old = v63.PKMAX_H
    try:
        v63.PKMAX_H = PKMAX_CLASS
        return v63.rewrite_ini(text, root)
    finally:
        v63.PKMAX_H = old


def build_forcing_extended(class_root):
    """Same v0.39/v0.63 forcing construction, with only k coverage extended."""
    results = ROOT / 'results'
    results.mkdir(exist_ok=True)
    trace = results / 'v067_theory_trace.dat'
    ini = class_root / 'v067_theory_trace.ini'
    ini.write_text(
        rewrite_ini_extended(v63.BASE.read_text(), 'output/v067_theory_trace_')
    )

    env = os.environ.copy()
    env['OMP_NUM_THREADS'] = '1'
    env['AEST_OFFLINE_TRACE_FILE'] = str(trace.resolve())
    log = results / 'v067_theory_trace.log'
    with log.open('w') as f:
        subprocess.run(
            [str(class_root / 'class'), ini.name, str(ROOT / 'v019p/pre/p3.pre')],
            cwd=class_root,
            env=env,
            stdout=f,
            stderr=subprocess.STDOUT,
            check=True,
        )
    if not trace.exists() or trace.stat().st_size == 0:
        raise RuntimeError('v0.67 extended source-grid trace was not produced')

    prefix = results / 'v067_theory'
    summary = results / 'v067_theory_forcing.json'
    subprocess.run(
        [
            sys.executable,
            str(ROOT / 'v039/build_tau_forcing.py'),
            str(trace),
            '--KB', str(v63.KB),
            '--tauH0', str(v63.TAUH0),
            '--out-prefix', str(prefix),
            '--control-order', '512',
            '--primary-order', '1024',
            '--summary', str(summary),
        ],
        check=True,
    )
    force = Path(str(prefix) + '_force.dat')
    if not force.exists() or force.stat().st_size == 0:
        raise RuntimeError('v0.67 extended tangent forcing was not produced')
    with summary.open() as f:
        forcing_summary = json.load(f)
    return force.resolve(), summary.resolve(), forcing_summary


def compute_run(force_file, lam):
    from classy import Class

    keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA']
    saved = {k: os.environ.get(k) for k in keys}
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
        pars['P_k_max_h/Mpc'] = PKMAX_CLASS
        c.set(pars)
        c.compute()

        sigma8 = np.array(
            [float(c.sigma(8.0, float(z), h_units=True)) for z in ALL_Z],
            dtype=float,
        )
        pk = np.empty((N_K, ALL_Z.size), dtype=float)
        for iz, z in enumerate(ALL_Z):
            pk[:, iz] = np.array(
                [float(c.pk_lin(float(k), float(z))) for k in K_MPC],
                dtype=float,
            )

        c.struct_cleanup()
        c.empty()
        return {'sigma8': sigma8, 'pk': pk}
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def bin_summary(kernel, total):
    abs_total = trapz_log(np.abs(kernel))
    rows = []
    for lo, hi in BINS:
        signed = integrate_log_interval(kernel, lo, hi)
        abs_part = integrate_log_interval(np.abs(kernel), lo, hi)
        rows.append({
            'kh_range_h_per_Mpc': [float(lo), float(hi)],
            'signed_contribution_to_dln_sigma8_deta': signed,
            'signed_fraction_of_total': (
                signed / total if abs(total) > 1.0e-300 else None
            ),
            'fraction_of_absolute_kernel': (
                abs_part / abs_total if abs_total > 1.0e-300 else None
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
    force_file, forcing_summary_file, forcing_summary = build_forcing_extended(class_root)

    base = compute_run(force_file, None)
    sigma2_class = base['sigma8'] ** 2

    i0 = np.empty_like(base['pk'])
    for iz in range(ALL_Z.size):
        i0[:, iz] = (
            K_MPC**3 * base['pk'][:, iz] * W8**2 / (2.0 * math.pi**2)
        )

    nested_sigma2 = np.empty((CAPS.size, ALL_Z.size), dtype=float)
    nested_recon_rel = np.empty_like(nested_sigma2)
    for ic, cap in enumerate(CAPS):
        for iz in range(ALL_Z.size):
            nested_sigma2[ic, iz] = integrate_log_to_cap(i0[:, iz], cap)
            nested_recon_rel[ic, iz] = relerr(
                nested_sigma2[ic, iz], sigma2_class[iz]
            )

    tail_8_16_fraction = np.array([
        integrate_log_interval(i0[:, iz], 8.0, 16.0)
        / max(nested_sigma2[-1, iz], 1.0e-300)
        for iz in range(ALL_Z.size)
    ], dtype=float)

    r_exact = np.empty((LAMBDAS.size, ALL_Z.size), dtype=float)
    dlnp = np.empty((LAMBDAS.size, N_K, ALL_Z.size), dtype=float)
    kernels = np.empty_like(dlnp)
    kernel_integrals = np.empty_like(r_exact)
    kernel_identity_rel = np.empty_like(r_exact)
    plus_sigma = np.empty_like(r_exact)
    minus_sigma = np.empty_like(r_exact)

    for il, lam in enumerate(LAMBDAS):
        plus = compute_run(force_file, +float(lam))
        minus = compute_run(force_file, -float(lam))
        plus_sigma[il, :] = plus['sigma8']
        minus_sigma[il, :] = minus['sigma8']

        r_exact[il, :] = (
            plus['sigma8']**2 - minus['sigma8']**2
        ) / (4.0 * float(lam) * sigma2_class)

        dlnp[il, :, :] = (
            plus['pk'] - minus['pk']
        ) / (2.0 * float(lam) * base['pk'])

        for iz in range(ALL_Z.size):
            kernels[il, :, iz] = (
                0.5 * i0[:, iz] * dlnp[il, :, iz] / sigma2_class[iz]
            )
            kval = trapz_log(kernels[il, :, iz])
            kernel_integrals[il, iz] = kval
            kernel_identity_rel[il, iz] = relerr(kval, r_exact[il, iz])

    mean_r = np.mean(r_exact, axis=0)
    r_lambda_spread = np.max(
        np.abs(r_exact - mean_r[None, :])
        / np.maximum(np.abs(mean_r[None, :]), 1.0e-300),
        axis=0,
    )

    mean_dlnp = np.mean(dlnp, axis=0)
    weighted_affinity = np.empty((LAMBDAS.size, ALL_Z.size), dtype=float)
    for iz in range(ALL_Z.size):
        den = trapz_log(i0[:, iz] * mean_dlnp[:, iz]**2)
        for il in range(LAMBDAS.size):
            num = trapz_log(
                i0[:, iz] * (dlnp[il, :, iz] - mean_dlnp[:, iz])**2
            )
            weighted_affinity[il, iz] = math.sqrt(
                max(num, 0.0) / max(den, 1.0e-300)
            )

    primary_n = PRIMARY_Z.size
    finite = bool(
        np.all(np.isfinite(base['sigma8']))
        and np.all(np.isfinite(base['pk']))
        and np.all(np.isfinite(i0))
        and np.all(np.isfinite(nested_sigma2))
        and np.all(np.isfinite(tail_8_16_fraction))
        and np.all(np.isfinite(r_exact))
        and np.all(np.isfinite(dlnp))
        and np.all(np.isfinite(kernels))
        and np.all(np.isfinite(weighted_affinity))
    )

    forcing_ok = bool(
        float(forcing_summary['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing_summary['cosine']) >= FORCING_COS_MIN
        and bool(forcing_summary['gate'])
    )
    full_recon_max_primary = float(np.max(nested_recon_rel[-1, :primary_n]))
    full_recon_ok = bool(full_recon_max_primary <= FULL_RECON_MAX)
    tail_max_primary = float(np.max(tail_8_16_fraction[:primary_n]))
    tail_ok = bool(tail_max_primary <= TAIL_8_16_MAX)
    negative_ok = bool(np.all(r_exact[:, :primary_n] < 0.0))
    r_spread_max_primary = float(np.max(r_lambda_spread[:primary_n]))
    r_spread_ok = bool(r_spread_max_primary <= R_LAMBDA_SPREAD_MAX)
    affinity_max_primary = float(np.max(weighted_affinity[:, :primary_n]))
    affinity_ok = bool(affinity_max_primary <= WEIGHTED_AFFINITY_MAX)
    kernel_identity_max_primary = float(
        np.max(kernel_identity_rel[:, :primary_n])
    )
    kernel_ok = bool(kernel_identity_max_primary <= KERNEL_IDENTITY_MAX)

    passed = bool(
        finite and forcing_ok and full_recon_ok and tail_ok and negative_ok
        and r_spread_ok and affinity_ok and kernel_ok
    )
    classification = (
        'V067_GROWTH_KERNEL_CLOSURE_AFFINITY_PASS'
        if passed else
        'V067_GROWTH_KERNEL_CLOSURE_AFFINITY_FAIL'
    )

    baseline_rows = []
    for iz, z in enumerate(ALL_Z):
        baseline_rows.append({
            'z': float(z),
            'role': 'primary' if iz < primary_n else 'context',
            'CLASS_sigma8': float(base['sigma8'][iz]),
            'CLASS_sigma8_squared': float(sigma2_class[iz]),
            'nested_manual_sigma8_squared': {
                str(float(cap)): float(nested_sigma2[ic, iz])
                for ic, cap in enumerate(CAPS)
            },
            'nested_reconstruction_relative_error_vs_CLASS_sigma8_squared': {
                str(float(cap)): float(nested_recon_rel[ic, iz])
                for ic, cap in enumerate(CAPS)
            },
            'fraction_of_manual_sigma8_squared_from_8_to_16_h_per_Mpc': float(
                tail_8_16_fraction[iz]
            ),
        })

    response_rows = []
    for iz, z in enumerate(ALL_Z):
        mean_kernel = np.mean(kernels[:, :, iz], axis=0)
        total = trapz_log(mean_kernel)
        imax = int(np.argmax(np.abs(mean_kernel)))
        response_rows.append({
            'z': float(z),
            'role': 'primary' if iz < primary_n else 'context',
            'mean_R_exact_over_fixed_lambdas': float(mean_r[iz]),
            'R_exact_by_lambda': {
                str(float(lam)): float(r_exact[il, iz])
                for il, lam in enumerate(LAMBDAS)
            },
            'R_exact_max_relative_spread_about_lambda_mean': float(
                r_lambda_spread[iz]
            ),
            'weighted_power_tangent_affinity_by_lambda': {
                str(float(lam)): float(weighted_affinity[il, iz])
                for il, lam in enumerate(LAMBDAS)
            },
            'mean_kernel_integral': float(total),
            'kernel_integral_by_lambda': {
                str(float(lam)): float(kernel_integrals[il, iz])
                for il, lam in enumerate(LAMBDAS)
            },
            'kernel_identity_relative_error_by_lambda': {
                str(float(lam)): float(kernel_identity_rel[il, iz])
                for il, lam in enumerate(LAMBDAS)
            },
            'largest_abs_mean_kernel_density': {
                'kh_h_per_Mpc': float(KH[imax]),
                'signed_kernel_density_per_dlnk': float(mean_kernel[imax]),
                'mean_dln_Pm_deta': float(mean_dlnp[imax, iz]),
            },
            'fixed_k_bins_from_mean_kernel': bin_summary(mean_kernel, total),
        })

    result = {
        'classification': classification,
        'predata_classification': 'V067_PREDATA_GROWTH_KERNEL_CLOSURE_AFFINITY',
        'uses_observational_data': False,
        'historical_v065_classification_unchanged': 'V065_SMOOTH_GROWTH_TANGENT_LIMIT_FAIL',
        'historical_v066_classification_unchanged': 'V066_EXACT_TANGENT_GROWTH_KERNEL_FAIL',
        'locked_physical_model': {
            'KB': v63.KB,
            'tauH0': v63.TAUH0,
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': [float(x) for x in LAMBDAS],
            'lambda_is_numerical_tangent_amplification_not_physical_eta': True,
            'primary_redshifts': [float(x) for x in PRIMARY_Z],
            'context_redshifts': [float(x) for x in CONTEXT_Z],
        },
        'numerical_k_extension': {
            'physical_parameters_changed': False,
            'CLASS_P_k_max_h_per_Mpc': PKMAX_CLASS,
            'kh_min_h_per_Mpc': KH_MIN,
            'kh_max_h_per_Mpc': KH_MAX,
            'n_log_points': N_K,
            'nested_nominal_caps_h_per_Mpc': [float(x) for x in CAPS],
            'fixed_bins_h_per_Mpc': [[float(a), float(b)] for a, b in BINS],
        },
        'forcing': {
            'summary_file': str(forcing_summary_file.relative_to(ROOT)),
            'relative_L2_control_vs_primary': float(
                forcing_summary['relative_L2_control_vs_primary']
            ),
            'cosine': float(forcing_summary['cosine']),
            'k_histories': int(forcing_summary['k_histories']),
            'samples': int(forcing_summary['samples']),
        },
        'baseline_support_closure': baseline_rows,
        'growth_response_and_affinity': response_rows,
        'gates': {
            'all_values_finite': finite,
            'forcing_control_vs_primary_relative_L2': float(
                forcing_summary['relative_L2_control_vs_primary']
            ),
            'forcing_control_vs_primary_relative_L2_limit': FORCING_L2_MAX,
            'forcing_control_vs_primary_cosine': float(forcing_summary['cosine']),
            'forcing_control_vs_primary_cosine_limit': FORCING_COS_MIN,
            'forcing_pass': forcing_ok,
            'baseline_sigma8_squared_reconstruction_at_16_max_relative_error_primary': full_recon_max_primary,
            'baseline_sigma8_squared_reconstruction_limit': FULL_RECON_MAX,
            'baseline_sigma8_squared_reconstruction_pass': full_recon_ok,
            'baseline_8_to_16_shell_fraction_max_primary': tail_max_primary,
            'baseline_8_to_16_shell_fraction_limit': TAIL_8_16_MAX,
            'baseline_high_k_tail_pass': tail_ok,
            'all_primary_R_exact_negative_for_all_four_lambdas': negative_ok,
            'R_exact_lambda_invariance_max_relative_spread_primary': r_spread_max_primary,
            'R_exact_lambda_invariance_limit': R_LAMBDA_SPREAD_MAX,
            'R_exact_lambda_invariance_pass': r_spread_ok,
            'weighted_power_tangent_affinity_max_primary': affinity_max_primary,
            'weighted_power_tangent_affinity_limit': WEIGHTED_AFFINITY_MAX,
            'weighted_power_tangent_affinity_pass': affinity_ok,
            'kernel_integral_vs_R_exact_max_relative_error_primary': kernel_identity_max_primary,
            'kernel_identity_limit': KERNEL_IDENTITY_MAX,
            'kernel_identity_pass': kernel_ok,
            'pass': passed,
        },
        'interpretation_policy': (
            'A PASS is a data-blind numerical/theory certification on the '
            'predeclared extended k range. It is not an observational detection '
            'and does not alter the historical v0.65 or v0.66 FAILs.'
        ),
    }

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(
        args.npz_out,
        kh=KH,
        z=ALL_Z,
        lambdas=LAMBDAS,
        baseline_sigma8=base['sigma8'],
        baseline_pk=base['pk'],
        baseline_sigma8_integrand=i0,
        nested_caps=CAPS,
        nested_sigma8_squared=nested_sigma2,
        tail_8_16_fraction=tail_8_16_fraction,
        plus_sigma8=plus_sigma,
        minus_sigma8=minus_sigma,
        R_exact=r_exact,
        dln_Pm_deta=dlnp,
        weighted_affinity=weighted_affinity,
        kernels=kernels,
        kernel_integrals=kernel_integrals,
        kernel_identity_relative_error=kernel_identity_rel,
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
