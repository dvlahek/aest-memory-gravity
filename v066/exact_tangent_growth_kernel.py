#!/usr/bin/env python3
"""v0.66 exact linear-theory tangent growth kernel.

This is the implementation of the preregistered test in
v066/predata_exact_tangent_growth_kernel.json.

The key identity is deliberately different from the finite-amplitude sigma8
estimator used in v0.65.  In linear perturbation theory the externally forced
eta=0 tangent family is affine in the numerical amplification lambda,

    D(lambda) = D0 + lambda D1.

Therefore sigma8^2 is exactly quadratic in lambda and

    [sigma8^2(+lambda)-sigma8^2(-lambda)] / [4 lambda sigma8^2(0)]

extracts d ln sigma8 / d eta at eta=0 without a lambda->0 fit.  v0.65 remains
historically unchanged; this is a new post-v0.65 theory test.
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
PRIMARY_Z = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], dtype=float)
CONTEXT_Z = np.array([1.0, 1.2, 1.5], dtype=float)
ALL_Z = np.concatenate([PRIMARY_Z, CONTEXT_Z])

KH_MIN = 1.0e-4
KH_MAX = 1.999
N_K = 2048
KH = np.geomspace(KH_MIN, KH_MAX, N_K)
LOG_KH = np.log(KH)
H0 = v63.START['H0']
H = H0 / 100.0
K_MPC = KH * H
R8_MPC = 8.0 / H

BINS = [
    (1.0e-4, 0.03),
    (0.03, 0.08),
    (0.08, 0.20),
    (0.20, 0.50),
    (0.50, 1.999),
]

BASELINE_RECON_MAX = 5.0e-3
LAMBDA_INVARIANCE_MAX = 5.0e-3
KERNEL_IDENTITY_MAX = 5.0e-3


def top_hat(x):
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    small = np.abs(x) < 1.0e-3
    xs = x[small]
    # 3(sin x - x cos x)/x^3 = 1 - x^2/10 + x^4/280 + O(x^6)
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
    yy = np.concatenate([
        [np.interp(x0, LOG_KH, y)],
        np.asarray(y, dtype=float)[mask],
        [np.interp(x1, LOG_KH, y)],
    ])
    return float(np.trapezoid(yy, xx))


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
        # Keep the v0.63/v0.65 frozen physical model. The upper P(k) range is
        # already 2 h/Mpc; the preregistered diagnostic grid stops at 1.999.
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


def baseline_sigma2_from_pk(pk0):
    out = np.empty(ALL_Z.size, dtype=float)
    density = np.empty_like(pk0)
    for iz in range(ALL_Z.size):
        density[:, iz] = (
            (K_MPC**3) * pk0[:, iz] * (W8**2) / (2.0 * math.pi**2)
        )
        out[iz] = trapz_log(density[:, iz])
    return out, density


def relerr(a, b):
    return abs(float(a) - float(b)) / max(abs(float(b)), 1.0e-300)


def bin_summary(kernel, total):
    absolute_total = trapz_log(np.abs(kernel))
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
                abs_part / absolute_total if absolute_total > 1.0e-300 else None
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
    force_file, forcing_summary = v63.build_forcing(class_root)

    base = compute_run(force_file, None)
    sigma2_class = base['sigma8'] ** 2
    sigma2_recon, i0 = baseline_sigma2_from_pk(base['pk'])
    recon_rel = np.abs(sigma2_recon - sigma2_class) / np.maximum(
        np.abs(sigma2_class), 1.0e-300
    )

    r_exact = np.empty((LAMBDAS.size, ALL_Z.size), dtype=float)
    r_v065 = np.empty_like(r_exact)
    kernel_integrals = np.empty_like(r_exact)
    kernel_identity_rel = np.empty_like(r_exact)
    kernels = np.empty((LAMBDAS.size, N_K, ALL_Z.size), dtype=float)
    dlnp = np.empty_like(kernels)
    plus_sigma = np.empty_like(r_exact)
    minus_sigma = np.empty_like(r_exact)
    bin_rows_by_lambda = {}

    for il, lam in enumerate(LAMBDAS):
        plus = compute_run(force_file, +float(lam))
        minus = compute_run(force_file, -float(lam))
        plus_sigma[il, :] = plus['sigma8']
        minus_sigma[il, :] = minus['sigma8']

        # New exact linear-theory estimator.
        r_exact[il, :] = (
            plus['sigma8']**2 - minus['sigma8']**2
        ) / (4.0 * float(lam) * sigma2_class)

        # Historical v0.65 finite-amplitude estimator, reported only to make
        # the distinction transparent. It has no v0.66 classification role.
        r_v065[il, :] = (
            plus['sigma8'] - minus['sigma8']
        ) / (2.0 * float(lam) * base['sigma8'])

        # Exact symmetric derivative of P in a linear transfer family. The
        # lambda^2 contribution cancels here as well.
        dlnp[il, :, :] = (
            plus['pk'] - minus['pk']
        ) / (2.0 * float(lam) * base['pk'])

        rows_for_lambda = []
        for iz, z in enumerate(ALL_Z):
            kernels[il, :, iz] = (
                0.5 * i0[:, iz] * dlnp[il, :, iz] / sigma2_class[iz]
            )
            kval = trapz_log(kernels[il, :, iz])
            kernel_integrals[il, iz] = kval
            kernel_identity_rel[il, iz] = relerr(kval, r_exact[il, iz])
            imax = int(np.argmax(np.abs(kernels[il, :, iz])))
            rows_for_lambda.append({
                'z': float(z),
                'R_exact_dln_sigma8_deta': float(r_exact[il, iz]),
                'R_v065_finite_sigma_estimator_context_only': float(r_v065[il, iz]),
                'kernel_integral': float(kval),
                'kernel_integral_relative_error_vs_R_exact': float(kernel_identity_rel[il, iz]),
                'largest_abs_kernel_density': {
                    'kh_h_per_Mpc': float(KH[imax]),
                    'signed_kernel_density_per_dlnk': float(kernels[il, imax, iz]),
                    'dln_Pm_deta': float(dlnp[il, imax, iz]),
                },
                'fixed_k_bins': bin_summary(kernels[il, :, iz], kval),
            })
        bin_rows_by_lambda[str(float(lam))] = rows_for_lambda

    mean_r = np.mean(r_exact, axis=0)
    lambda_rel_spread = np.max(
        np.abs(r_exact - mean_r[None, :]) /
        np.maximum(np.abs(mean_r[None, :]), 1.0e-300),
        axis=0,
    )

    primary_n = PRIMARY_Z.size
    finite = bool(
        np.all(np.isfinite(base['sigma8']))
        and np.all(np.isfinite(base['pk']))
        and np.all(np.isfinite(r_exact))
        and np.all(np.isfinite(dlnp))
        and np.all(np.isfinite(kernels))
        and np.all(np.isfinite(kernel_integrals))
    )
    recon_ok = bool(float(np.max(recon_rel)) <= BASELINE_RECON_MAX)
    negative_ok = bool(np.all(r_exact[:, :primary_n] < 0.0))
    lambda_ok = bool(
        float(np.max(lambda_rel_spread[:primary_n])) <= LAMBDA_INVARIANCE_MAX
    )
    kernel_ok = bool(
        float(np.max(kernel_identity_rel[:, :primary_n])) <= KERNEL_IDENTITY_MAX
    )
    passed = bool(finite and recon_ok and negative_ok and lambda_ok and kernel_ok)
    classification = (
        'V066_EXACT_TANGENT_GROWTH_KERNEL_PASS'
        if passed else
        'V066_EXACT_TANGENT_GROWTH_KERNEL_FAIL'
    )

    consensus_rows = []
    for iz, z in enumerate(ALL_Z):
        # Signed-bin consensus is the arithmetic mean over the four fixed
        # lambda estimates. No lambda is selected after seeing the result.
        mean_kernel = np.mean(kernels[:, :, iz], axis=0)
        total = trapz_log(mean_kernel)
        imax = int(np.argmax(np.abs(mean_kernel)))
        consensus_rows.append({
            'z': float(z),
            'role': 'primary' if iz < primary_n else 'context',
            'mean_R_exact_over_fixed_lambdas': float(mean_r[iz]),
            'R_exact_by_lambda': {
                str(float(lam)): float(r_exact[il, iz])
                for il, lam in enumerate(LAMBDAS)
            },
            'max_relative_spread_about_lambda_mean': float(lambda_rel_spread[iz]),
            'mean_kernel_integral_over_fixed_lambdas': float(total),
            'largest_abs_mean_kernel_density': {
                'kh_h_per_Mpc': float(KH[imax]),
                'signed_kernel_density_per_dlnk': float(mean_kernel[imax]),
                'mean_dln_Pm_deta': float(np.mean(dlnp[:, imax, iz])),
            },
            'fixed_k_bins_from_mean_kernel': bin_summary(mean_kernel, total),
        })

    result = {
        'classification': classification,
        'predata_classification': 'V066_PREDATA_EXACT_TANGENT_GROWTH_KERNEL',
        'uses_observational_data': False,
        'historical_v065_classification_unchanged': 'V065_SMOOTH_GROWTH_TANGENT_LIMIT_FAIL',
        'locked_model': {
            'KB': v63.KB,
            'tauH0': v63.TAUH0,
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': [float(x) for x in LAMBDAS],
            'lambda_is_numerical_tangent_amplification_not_physical_eta': True,
            'primary_redshifts': [float(x) for x in PRIMARY_Z],
            'context_redshifts': [float(x) for x in CONTEXT_Z],
        },
        'theory_identity': {
            'transfer_affinity': 'D(lambda)=D0+lambda D1 in the linear eta=0 externally forced family',
            'sigma8_squared': 'sigma8^2(lambda)=A+2 lambda B+lambda^2 C',
            'exact_estimator': '[sigma8^2(+lambda)-sigma8^2(-lambda)]/[4 lambda sigma8^2(0)] = d ln sigma8/d eta at eta=0',
            'v065_estimator_role_here': 'context_only; no v0.66 gate uses the finite-amplitude sigma8 estimator',
        },
        'k_grid': {
            'kh_min_h_per_Mpc': KH_MIN,
            'kh_max_h_per_Mpc': KH_MAX,
            'n_log_points': N_K,
            'R8_h_inverse_Mpc': 8.0,
            'fixed_bins_h_per_Mpc': [[float(a), float(b)] for a, b in BINS],
        },
        'baseline_sigma8': [
            {
                'z': float(z),
                'CLASS_sigma8': float(base['sigma8'][iz]),
                'manual_sigma8_from_fixed_k_grid': float(math.sqrt(max(sigma2_recon[iz], 0.0))),
                'sigma8_squared_reconstruction_relative_error': float(recon_rel[iz]),
            }
            for iz, z in enumerate(ALL_Z)
        ],
        'consensus_exact_growth_response': consensus_rows,
        'per_lambda_kernel_reports': bin_rows_by_lambda,
        'gates': {
            'all_values_finite': finite,
            'baseline_sigma8_reconstruction_max_relative_error': float(np.max(recon_rel)),
            'baseline_sigma8_reconstruction_limit': BASELINE_RECON_MAX,
            'baseline_sigma8_reconstruction_pass': recon_ok,
            'all_primary_R_exact_negative_for_all_four_lambdas': negative_ok,
            'lambda_invariance_max_relative_spread_primary': float(np.max(lambda_rel_spread[:primary_n])),
            'lambda_invariance_limit': LAMBDA_INVARIANCE_MAX,
            'lambda_invariance_pass': lambda_ok,
            'kernel_integral_vs_sigma8_squared_estimator_max_relative_error_primary': float(np.max(kernel_identity_rel[:, :primary_n])),
            'kernel_identity_limit': KERNEL_IDENTITY_MAX,
            'kernel_identity_pass': kernel_ok,
            'pass': passed,
        },
        'forcing_summary_file': str(forcing_summary.relative_to(ROOT)),
        'interpretation_policy': (
            'A PASS is a data-blind linear-theory tangent certification. It demonstrates that the exact '
            'sigma8-squared tangent coefficient is negative and identifies its signed k-space support. '
            'It is not an observational detection and does not retroactively alter v0.65.'
        ),
    }

    Path(args.json_out).write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(
        args.npz_out,
        lambdas=LAMBDAS,
        primary_z=PRIMARY_Z,
        context_z=CONTEXT_Z,
        z=ALL_Z,
        kh_h_per_Mpc=KH,
        k_Mpc=K_MPC,
        window_W8=W8,
        sigma8_0=base['sigma8'],
        sigma8_plus=plus_sigma,
        sigma8_minus=minus_sigma,
        sigma2_reconstructed=sigma2_recon,
        sigma2_reconstruction_relative_error=recon_rel,
        R_exact=r_exact,
        R_v065_context_only=r_v065,
        R_exact_mean=mean_r,
        lambda_relative_spread=lambda_rel_spread,
        dln_Pm_deta=dlnp,
        kernel=kernels,
        kernel_integral=kernel_integrals,
        kernel_identity_relative_error=kernel_identity_rel,
    )

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
