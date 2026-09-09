#!/usr/bin/env python3
"""v0.77 preregistered native-state tangent-affinity audit.

This result-informed follow-up to the locked v0.76 FAIL tests the additive
eta=0 tangent directly on the CLASS native total-matter transfer source d_m.
The primary metric never divides by a local d_m or P_m value, so transfer
zero/minimum conditioning cannot by itself inflate the response.
"""

from pathlib import Path
import argparse
import json
import math
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import v063.theory_response_map as v63
import v075.fourier_k_resolution_closure as v75
import v076.native_node_power_closure as v76

LAMBDAS = np.array([10.0, 5.0, 2.5, 1.25], dtype=float)
H = float(v63.START['H0']) / 100.0
R4 = {
    'label': 'r4',
    'k_per_decade_for_pk': 80.0,
    'k_per_decade_for_bao': 560.0,
}

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
GRID_K_REL_MAX = 1.0e-12
GRID_Z_ABS_MAX = 1.0e-12
STATE_AFFINITY_MAX = 5.0e-3
EVEN_RESIDUAL_MAX = 5.0e-3


def _norm(x):
    return float(np.sqrt(np.sum(np.asarray(x, dtype=float) ** 2)))


def _affinity(tangents, mask):
    tangents = np.asarray(tangents, dtype=float)
    vals = tangents[:, mask]
    if vals.ndim != 2 or vals.shape[1] == 0:
        raise RuntimeError('empty primary state-tangent mask')
    mean = np.mean(vals, axis=0)
    den = max(_norm(mean), 1.0e-300)
    eps = np.array([_norm(v - mean) / den for v in vals], dtype=float)
    cos = np.array([
        float(np.dot(v, mean) / max(_norm(v) * _norm(mean), 1.0e-300))
        for v in vals
    ], dtype=float)
    return mean, eps, cos


def _even_residual(base, plus, minus, lam, mask, mean_tangent_norm):
    ev = np.asarray(plus, dtype=float)[mask] + np.asarray(minus, dtype=float)[mask] - 2.0 * np.asarray(base, dtype=float)[mask]
    den = max(2.0 * abs(float(lam)) * float(mean_tangent_norm), 1.0e-300)
    return _norm(ev) / den


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--class-root', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--npz-out', required=True)
    args = ap.parse_args()

    out_json = Path(args.json_out)
    out_npz = Path(args.npz_out)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    class_root = Path(args.class_root).resolve()

    force_file, forcing_summary_path = v75.build_forcing_for_resolution(class_root, R4)
    forcing = json.loads(Path(forcing_summary_path).read_text())

    base = v76.compute_run(force_file, None, 'v077_base')
    plus_runs = []
    minus_runs = []
    tangents = np.empty((LAMBDAS.size,) + base['d_m_native'].shape, dtype=float)
    target_tangents = np.empty((LAMBDAS.size,) + base['target_dm'].shape, dtype=float)

    max_k_grid_rel = float(base['k_grid_rel'])
    max_z_grid_abs = float(base['z_grid_abs'])
    all_finite = bool(np.all(np.isfinite(base['d_m_native'])))

    for il, lam in enumerate(LAMBDAS):
        tag = str(float(lam)).replace('.', 'p')
        pr = v76.compute_run(force_file, +float(lam), f'v077_plus_{tag}')
        mr = v76.compute_run(force_file, -float(lam), f'v077_minus_{tag}')
        plus_runs.append(pr)
        minus_runs.append(mr)

        for name, rr in [('plus', pr), ('minus', mr)]:
            if not np.allclose(rr['k_pk'], base['k_pk'], rtol=0.0, atol=1.0e-14):
                raise RuntimeError(f'{name} lambda={lam}: native k grid changed')
            if not np.allclose(rr['z_pk'], base['z_pk'], rtol=0.0, atol=1.0e-14):
                raise RuntimeError(f'{name} lambda={lam}: native z grid changed')
            max_k_grid_rel = max(max_k_grid_rel, float(rr['k_grid_rel']))
            max_z_grid_abs = max(max_z_grid_abs, float(rr['z_grid_abs']))
            all_finite = bool(all_finite and np.all(np.isfinite(rr['d_m_native'])))

        tangents[il] = (pr['d_m_native'] - mr['d_m_native']) / (2.0 * float(lam))
        target_tangents[il] = (pr['target_dm'] - mr['target_dm']) / (2.0 * float(lam))

    kh_native = base['k_pk'] / H
    mask = (
        (kh_native[:, None] >= 0.03)
        & (kh_native[:, None] <= 0.20)
        & (base['z_pk'][None, :] >= 0.2)
        & (base['z_pk'][None, :] <= 1.5)
    )
    if not np.any(mask):
        raise RuntimeError('v0.77 native-state primary window is empty')

    mean_tangent, eps, cos = _affinity(tangents, mask)
    mean_tangent_norm = _norm(mean_tangent)
    even = np.array([
        _even_residual(
            base['d_m_native'],
            plus_runs[il]['d_m_native'],
            minus_runs[il]['d_m_native'],
            LAMBDAS[il],
            mask,
            mean_tangent_norm,
        )
        for il in range(LAMBDAS.size)
    ], dtype=float)

    target_mean = np.mean(target_tangents.reshape(LAMBDAS.size, -1), axis=0)
    target_den = max(_norm(target_mean), 1.0e-300)
    target_eps = np.array([
        _norm(target_tangents[il].ravel() - target_mean) / target_den
        for il in range(LAMBDAS.size)
    ], dtype=float)

    forcing_pass = bool(
        float(forcing['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing['cosine']) >= FORCING_COS_MIN
    )
    grid_pass = bool(max_k_grid_rel <= GRID_K_REL_MAX and max_z_grid_abs <= GRID_Z_ABS_MAX)
    affinity_pass = bool(np.max(eps) <= STATE_AFFINITY_MAX)
    even_pass = bool(np.max(even) <= EVEN_RESIDUAL_MAX)
    numerical_pass = bool(forcing_pass and all_finite and grid_pass and affinity_pass and even_pass)

    classification = (
        'V077_NATIVE_STATE_TANGENT_AFFINITY_PASS'
        if numerical_pass
        else 'V077_NATIVE_STATE_TANGENT_AFFINITY_FAIL'
    )
    diagnosis = (
        'V077_FRACTIONAL_ZERO_CONDITIONING_SUPPORTED'
        if numerical_pass
        else 'V077_NATIVE_STATE_TANGENT_NONAFFINITY_SURVIVES'
    )

    # Descriptive locations only; no local fractional normalization is used in gates.
    mean_full = np.mean(tangents, axis=0)
    masked_abs = np.where(mask, np.abs(mean_full), -np.inf)
    flat = int(np.argmax(masked_abs))
    ik, iz = np.unravel_index(flat, mean_full.shape)

    result = {
        'classification': classification,
        'diagnosis': diagnosis,
        'predata_classification': 'V077_PREDATA_NATIVE_STATE_TANGENT_AFFINITY_AUDIT',
        'uses_observational_data': False,
        'result_informed_followup': True,
        'historical_classifications_unchanged': {
            'v075': 'V075_FOURIER_K_RESOLUTION_CLOSURE_FAIL',
            'v076': 'V076_NATIVE_NODE_POWER_CLOSURE_FAIL',
        },
        'scope': 'Theory-only native total-matter state-tangent audit; no local division by d_m or P_m, no nonlinear evolution, no observational likelihood.',
        'locked_model': {
            'KB': v63.KB,
            'tauH0': v63.TAUH0,
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': [float(x) for x in LAMBDAS],
        },
        'fixed_numerical_configuration': dict(R4),
        'native_window': {
            'k_h_per_Mpc_min': 0.03,
            'k_h_per_Mpc_max': 0.20,
            'z_min': 0.2,
            'z_max': 1.5,
            'n_common_native_nodes': int(np.count_nonzero(mask)),
        },
        'forcing': {
            'relative_L2_control_vs_primary': float(forcing['relative_L2_control_vs_primary']),
            'cosine': float(forcing['cosine']),
            'pass': forcing_pass,
        },
        'native_state': {
            'tangent_definition': '[d_m(+lambda)-d_m(-lambda)]/(2 lambda)',
            'uses_local_fractional_division': False,
            'tangent_lambda_affinity_by_lambda': {
                str(float(lam)): float(eps[i]) for i, lam in enumerate(LAMBDAS)
            },
            'tangent_lambda_affinity_max': float(np.max(eps)),
            'tangent_cosine_to_four_lambda_mean_by_lambda': {
                str(float(lam)): float(cos[i]) for i, lam in enumerate(LAMBDAS)
            },
            'even_residual_by_lambda': {
                str(float(lam)): float(even[i]) for i, lam in enumerate(LAMBDAS)
            },
            'even_residual_max': float(np.max(even)),
            'mean_tangent_L2_norm_in_window': float(mean_tangent_norm),
            'largest_abs_mean_tangent_location': {
                'k_h_per_Mpc': float(kh_native[ik]),
                'z': float(base['z_pk'][iz]),
                'mean_ddm_deta': float(mean_full[ik, iz]),
                'baseline_d_m': float(base['d_m_native'][ik, iz]),
            },
        },
        'fixed_target_context': {
            'state_tangent_lambda_affinity_by_lambda': {
                str(float(lam)): float(target_eps[i]) for i, lam in enumerate(LAMBDAS)
            },
            'state_tangent_lambda_affinity_max': float(np.max(target_eps)),
        },
        'gates': {
            'forcing_pass': forcing_pass,
            'all_native_state_values_finite': all_finite,
            'native_k_grid_relative_mismatch_max': float(max_k_grid_rel),
            'native_k_grid_relative_mismatch_limit': GRID_K_REL_MAX,
            'native_k_grid_pass': bool(max_k_grid_rel <= GRID_K_REL_MAX),
            'native_z_grid_absolute_mismatch_max': float(max_z_grid_abs),
            'native_z_grid_absolute_mismatch_limit': GRID_Z_ABS_MAX,
            'native_z_grid_pass': bool(max_z_grid_abs <= GRID_Z_ABS_MAX),
            'native_state_tangent_lambda_affinity_max': float(np.max(eps)),
            'native_state_tangent_lambda_affinity_limit': STATE_AFFINITY_MAX,
            'native_state_tangent_lambda_affinity_pass': affinity_pass,
            'native_state_even_residual_max': float(np.max(even)),
            'native_state_even_residual_limit': EVEN_RESIDUAL_MAX,
            'native_state_even_residual_pass': even_pass,
            'numerical_pass': numerical_pass,
        },
        'interpretation_policy': 'A PASS certifies numerical lambda-affinity of the additive native d_m state tangent under global L2 normalization and supports conditioning near transfer minima as the source of the v0.76 fractional-affinity excursion. It does not alter historical classifications, simulate nonlinear evolution, or constitute observational evidence.',
    }

    out_json.write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(
        out_npz,
        lambdas=LAMBDAS,
        k_native_h=kh_native,
        z_native=base['z_pk'],
        primary_mask=mask,
        d_m_base=base['d_m_native'],
        d_m_plus=np.stack([r['d_m_native'] for r in plus_runs]),
        d_m_minus=np.stack([r['d_m_native'] for r in minus_runs]),
        state_tangents=tangents,
        state_tangent_mean=mean_full,
        state_tangent_affinity=eps,
        state_tangent_cosine=cos,
        even_residual=even,
        target_state_tangents=target_tangents,
        target_state_tangent_affinity=target_eps,
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
