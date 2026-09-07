#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
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
RSD_K = np.array([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], dtype=float)


def compute_growth(force_file, lam):
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
        c.set(v63.class_params())
        c.compute()

        sigma8 = np.array(
            [float(c.sigma(8.0, float(z), h_units=True)) for z in ALL_Z],
            dtype=float,
        )
        growth_f = np.empty((RSD_K.size, ALL_Z.size), dtype=float)
        for ik, k in enumerate(RSD_K):
            for iz, z in enumerate(ALL_Z):
                growth_f[ik, iz] = float(
                    c.scale_dependent_growth_factor_f(
                        float(k), float(z), h_units=True, nonlinear=False
                    )
                )
        fs8 = growth_f * sigma8[None, :]

        c.struct_cleanup()
        c.empty()
        return {'sigma8': sigma8, 'growth_f': growth_f, 'fs8': fs8}
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def fractional_response(base, plus, minus, lam, label):
    b = np.asarray(base, dtype=float)
    p = np.asarray(plus, dtype=float)
    m = np.asarray(minus, dtype=float)
    if np.any(~np.isfinite(b)) or np.any(~np.isfinite(p)) or np.any(~np.isfinite(m)):
        raise RuntimeError(f'non-finite values in {label}')
    if np.any(np.abs(b) <= 1e-300):
        raise RuntimeError(f'zero baseline encountered in {label}')
    r = (p - m) / (2.0 * float(lam) * b)
    if np.any(~np.isfinite(r)):
        raise RuntimeError(f'non-finite fractional response in {label}')
    return r


def fit_lambda_squared(values):
    y = np.asarray(values, dtype=float)
    x = LAMBDAS * LAMBDAS
    A = np.column_stack([np.ones_like(x), x])
    beta, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    intercept = float(beta[0])
    slope = float(beta[1])
    pred = A @ beta
    resid = y - pred
    ss_res = float(np.dot(resid, resid))
    centered = y - float(np.mean(y))
    ss_tot = float(np.dot(centered, centered))
    r2 = 1.0 if ss_tot == 0.0 and ss_res == 0.0 else (
        float(1.0 - ss_res / ss_tot) if ss_tot > 0.0 else float('nan')
    )
    return {
        'R0_dln_sigma8_deta': intercept,
        'lambda2_coefficient': slope,
        'residual_rms': float(np.sqrt(np.mean(resid * resid))),
        'residual_max_abs': float(np.max(np.abs(resid))),
        'r_squared': r2,
        'predicted_at_lambdas': [float(v) for v in pred],
    }


def fs8_summary(response):
    response = np.asarray(response, dtype=float)
    rows = []
    for iz, z in enumerate(ALL_Z):
        vals = response[:, iz]
        rows.append({
            'z': float(z),
            'median_dln_fsigma8_deta': float(np.median(vals)),
            'q10_dln_fsigma8_deta': float(np.quantile(vals, 0.10)),
            'q90_dln_fsigma8_deta': float(np.quantile(vals, 0.90)),
            'negative_fraction_over_fixed_k_grid': float(np.mean(vals < 0.0)),
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--class-root', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--npz-out', required=True)
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    force, forcing_summary = v63.build_forcing(class_root)

    base = compute_growth(force, None)
    sigma8_response = {}
    fs8_response = {}

    for lam in LAMBDAS:
        plus = compute_growth(force, +float(lam))
        minus = compute_growth(force, -float(lam))
        sigma8_response[float(lam)] = fractional_response(
            base['sigma8'], plus['sigma8'], minus['sigma8'], lam, f'sigma8 lambda={lam}'
        )
        fs8_response[float(lam)] = fractional_response(
            base['fs8'], plus['fs8'], minus['fs8'], lam, f'fsigma8 lambda={lam}'
        )

    sigma_matrix = np.vstack([sigma8_response[float(l)] for l in LAMBDAS])
    fits = [fit_lambda_squared(sigma_matrix[:, iz]) for iz in range(ALL_Z.size)]

    primary_n = PRIMARY_Z.size
    primary_matrix = sigma_matrix[:, :primary_n]
    all_primary_lambda_negative = bool(np.all(primary_matrix < 0.0))
    all_primary_R0_negative = bool(all(fits[iz]['R0_dln_sigma8_deta'] < 0.0 for iz in range(primary_n)))

    idx = {float(l): i for i, l in enumerate(LAMBDAS)}
    large_pair = np.abs(
        sigma_matrix[idx[5.0], :primary_n] - sigma_matrix[idx[10.0], :primary_n]
    )
    small_pair = np.abs(
        sigma_matrix[idx[1.25], :primary_n] - sigma_matrix[idx[2.5], :primary_n]
    )
    stabilizing = small_pair < large_pair
    n_stabilizing = int(np.sum(stabilizing))

    fit_finite = bool(all(
        np.isfinite(f['R0_dln_sigma8_deta'])
        and np.isfinite(f['lambda2_coefficient'])
        and np.isfinite(f['residual_rms'])
        and np.isfinite(f['residual_max_abs'])
        for f in fits[:primary_n]
    ))

    passed = bool(
        all_primary_lambda_negative
        and all_primary_R0_negative
        and n_stabilizing >= 6
        and fit_finite
    )
    classification = (
        'V065_SMOOTH_GROWTH_TANGENT_LIMIT_PASS'
        if passed else
        'V065_SMOOTH_GROWTH_TANGENT_LIMIT_FAIL'
    )

    response_rows = []
    for iz, z in enumerate(ALL_Z):
        response_rows.append({
            'z': float(z),
            'role': 'primary' if iz < primary_n else 'context',
            'responses_by_lambda': {
                str(float(lam)): float(sigma_matrix[i, iz])
                for i, lam in enumerate(LAMBDAS)
            },
            'zero_amplitude_fit': fits[iz],
            'stabilization_gate': (
                {
                    'large_pair_abs_difference_lambda5_vs10': float(large_pair[iz]),
                    'small_pair_abs_difference_lambda1p25_vs2p5': float(small_pair[iz]),
                    'pass': bool(stabilizing[iz]),
                }
                if iz < primary_n else None
            ),
        })

    result = {
        'classification': classification,
        'predata_classification': 'V065_PREDATA_SMOOTH_GROWTH_CONVERGENCE',
        'uses_observational_data': False,
        'locked_model': {
            'KB': v63.KB,
            'tauH0': v63.TAUH0,
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': [float(x) for x in LAMBDAS],
            'lambda_is_numerical_tangent_amplification_not_physical_eta': True,
        },
        'primary_observable': 'sigma8(z)',
        'response_definition': 'R_sigma(lambda,z)=[sigma8(+lambda,z)-sigma8(-lambda,z)]/[2 lambda sigma8(0,z)]',
        'zero_amplitude_fit': 'R_sigma(lambda,z)=R0(z)+c(z) lambda^2',
        'sigma8_response': response_rows,
        'gates': {
            'all_primary_lambda_responses_negative': all_primary_lambda_negative,
            'all_primary_extrapolated_R0_negative': all_primary_R0_negative,
            'fit_finite_on_all_primary_redshifts': fit_finite,
            'n_primary_redshifts_stabilizing': n_stabilizing,
            'minimum_primary_redshifts_stabilizing': 6,
            'number_primary_redshifts': int(primary_n),
            'pass': passed,
        },
        'secondary_fsigma8': {
            'classification_role': 'context_only',
            'k_h_per_Mpc': [float(x) for x in RSD_K],
            'summary_by_lambda': {
                str(float(lam)): fs8_summary(fs8_response[float(lam)])
                for lam in LAMBDAS
            },
        },
        's8_identity': 'At fixed Omega_m, d ln S8 / d eta = d ln sigma8 / d eta; no observational S8 likelihood is used here.',
        'forcing_summary_file': str(forcing_summary.relative_to(ROOT)),
        'interpretation': 'A PASS certifies only a data-blind smooth negative late-time growth tangent response at eta=0. It is not an observational detection and does not rehabilitate the v0.64 rejected narrow P_m feature.',
    }

    Path(args.json_out).write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(
        args.npz_out,
        lambdas=LAMBDAS,
        z=ALL_Z,
        primary_z=PRIMARY_Z,
        context_z=CONTEXT_Z,
        rsd_k_h_per_Mpc=RSD_K,
        sigma8_0=base['sigma8'],
        sigma8_response=sigma_matrix,
        extrapolated_R0=np.array([f['R0_dln_sigma8_deta'] for f in fits], dtype=float),
        lambda2_coefficient=np.array([f['lambda2_coefficient'] for f in fits], dtype=float),
        fit_residual_rms=np.array([f['residual_rms'] for f in fits], dtype=float),
        fs8_0=base['fs8'],
        fs8_response_lambda10=fs8_response[10.0],
        fs8_response_lambda5=fs8_response[5.0],
        fs8_response_lambda2p5=fs8_response[2.5],
        fs8_response_lambda1p25=fs8_response[1.25],
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
