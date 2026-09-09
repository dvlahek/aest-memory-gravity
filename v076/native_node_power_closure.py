#!/usr/bin/env python3
"""v0.76 preregistered native-node source-to-Fourier closure audit.

Result-informed follow-up to the locked v0.75 FAIL.  The audit asks whether
CLASS's matter source d_m and its linear Fourier P_m agree on their common
native (k,tau) nodes.  It separately records the already distinct off-node
paths: source interpolation followed by squaring versus CLASS Fourier
log-power interpolation.

No observational data, nonlinear evolution, physical retuning, or science-gate
changes are introduced here.
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
import v072.direct_transfer_tangent_affinity as v72
import v075.fourier_k_resolution_closure as v75

LAMBDAS = np.array([10.0, 5.0, 2.5, 1.25], dtype=float)
K_H = np.array([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], dtype=float)
Z_TARGET = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5], dtype=float)
H = float(v63.START['H0']) / 100.0
K_REQ = K_H * H
AS = float(v63.START['A_s'])
NS = float(v63.START['n_s'])
KPIVOT = 0.05
R4 = {
    'label': 'r4',
    'k_per_decade_for_pk': 80.0,
    'k_per_decade_for_bao': 560.0,
}

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
GRID_K_REL_MAX = 1.0e-12
GRID_Z_ABS_MAX = 1.0e-12
NATIVE_NODE_CLOSURE_MAX = 5.0e-5
NATIVE_SOURCE_AFFINITY_MAX = 5.0e-3
NATIVE_FOURIER_AFFINITY_MAX = 5.0e-3
TARGET_K_REL_MAX = 1.0e-8
TARGET_SOURCE_AFFINITY_MAX = 5.0e-3
HISTORICAL_OFFNODE_SCALE = 5.0e-3


def _pick_key(d, preferred, alternatives=()):
    if preferred in d:
        return preferred
    for key in alternatives:
        if key in d:
            return key
    raise RuntimeError(f'missing key {preferred}; available keys={sorted(d.keys())}')


def _restore_env(saved):
    for key, value in saved.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


def response(base, plus, minus, lam):
    base = np.asarray(base, dtype=float)
    return (np.asarray(plus, dtype=float) - np.asarray(minus, dtype=float)) / (
        2.0 * float(lam) * base
    )


def affinity_by_lambda_mask(arr, mask):
    arr = np.asarray(arr, dtype=float)
    mask = np.asarray(mask, dtype=bool)
    vals = arr[:, mask]
    if vals.ndim != 2 or vals.shape[1] == 0:
        raise RuntimeError('empty affinity mask')
    mean = np.mean(vals, axis=0)
    den = float(np.sum(mean * mean))
    eps = np.empty(vals.shape[0], dtype=float)
    for il in range(vals.shape[0]):
        num = float(np.sum((vals[il] - mean) ** 2))
        eps[il] = math.sqrt(max(num, 0.0) / max(den, 1.0e-300))
    return mean, eps


def affinity_by_lambda(arr):
    arr = np.asarray(arr, dtype=float)
    mean = np.mean(arr, axis=0)
    den = float(np.sum(mean * mean))
    eps = np.empty(arr.shape[0], dtype=float)
    for il in range(arr.shape[0]):
        num = float(np.sum((arr[il] - mean) ** 2))
        eps[il] = math.sqrt(max(num, 0.0) / max(den, 1.0e-300))
    return mean, eps


def primordial_power(k_phys):
    k_phys = np.asarray(k_phys, dtype=float)
    return AS * (k_phys / KPIVOT) ** (NS - 1.0)


def source_power(d_m, k_phys):
    d_m = np.asarray(d_m, dtype=float)
    k_phys = np.asarray(k_phys, dtype=float)
    pref = (2.0 * math.pi**2 / k_phys**3) * primordial_power(k_phys)
    if d_m.ndim == 2:
        return pref[:, None] * d_m**2
    return pref * d_m**2


def compute_run(force_file, lam, label):
    from classy import Class

    env_keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA', 'AEST_OFFLINE_TRACE_FILE']
    saved = {key: os.environ.get(key) for key in env_keys}
    trace_path = ROOT / 'results' / f'v076_{label}_trace.dat'
    if trace_path.exists():
        trace_path.unlink()

    c = None
    try:
        if lam is None:
            os.environ.pop('AEST_TANGENT_FORCE_FILE', None)
            os.environ.pop('AEST_TANGENT_LAMBDA', None)
        else:
            os.environ['AEST_TANGENT_FORCE_FILE'] = str(force_file)
            os.environ['AEST_TANGENT_LAMBDA'] = str(float(lam))
        os.environ['AEST_OFFLINE_TRACE_FILE'] = str(trace_path.resolve())
        os.environ['OMP_NUM_THREADS'] = '1'

        pars = dict(v63.class_params())
        pars['output'] = 'mPk,mTk'
        pars['lensing'] = 'no'
        pars['k_output_values'] = ', '.join(f'{k:.17g}' for k in K_REQ)
        pars['P_k_max_h/Mpc'] = 2.0
        pars['z_max_pk'] = 5.0
        pars['k_per_decade_for_pk'] = 80.0
        pars['k_per_decade_for_bao'] = 560.0

        c = Class()
        c.set(pars)
        c.compute()

        # Common native Fourier/transfer nodes. h_units=False keeps k in 1/Mpc
        # and P in Mpc^3 so the analytic source-power identity is direct.
        pk_native, k_pk, z_pk = c.get_pk_and_k_and_z(
            nonlinear=False,
            only_clustering_species=False,
            h_units=False,
        )
        tk_native, k_tk, z_tk = c.get_transfer_and_k_and_z(
            output_format='class',
            h_units=False,
        )
        dm_key = _pick_key(tk_native, 'd_m', ('delta_m',))
        d_m_native = np.asarray(tk_native[dm_key], dtype=float)
        pk_native = np.asarray(pk_native, dtype=float)
        k_pk = np.asarray(k_pk, dtype=float)
        z_pk = np.asarray(z_pk, dtype=float)
        k_tk = np.asarray(k_tk, dtype=float)
        z_tk = np.asarray(z_tk, dtype=float)

        if pk_native.shape != d_m_native.shape:
            raise RuntimeError(
                f'native shape mismatch: pk={pk_native.shape}, d_m={d_m_native.shape}'
            )
        if pk_native.shape != (k_pk.size, z_pk.size):
            raise RuntimeError(
                f'unexpected native orientation: pk={pk_native.shape}, '
                f'k={k_pk.size}, z={z_pk.size}'
            )
        if k_tk.size != k_pk.size or z_tk.size != z_pk.size:
            raise RuntimeError(
                f'native grid sizes differ: pk=({k_pk.size},{z_pk.size}), '
                f'transfer=({k_tk.size},{z_tk.size})'
            )

        k_grid_rel = float(np.max(np.abs(k_tk - k_pk) / np.maximum(np.abs(k_pk), 1.0e-300)))
        z_grid_abs = float(np.max(np.abs(z_tk - z_pk)))
        p_source_native = source_power(d_m_native, k_tk)

        # Off-node fixed v0.63 target grid: CLASS source interpolation versus
        # CLASS Fourier pk_lin interpolation. These are diagnostic outputs;
        # only target source affinity and exact requested-k recovery are gates.
        target_source = np.empty((K_H.size, Z_TARGET.size), dtype=float)
        target_pk = np.empty_like(target_source)
        target_dm = np.empty_like(target_source)
        target_k_actual_h = np.empty_like(target_source)
        target_k_rel = np.empty_like(target_source)

        for iz, z in enumerate(Z_TARGET):
            tr = c.get_transfer(float(z), output_format='class')
            k_key = _pick_key(tr, 'k (h/Mpc)', ('k [h/Mpc]', 'k'))
            dm_key_target = _pick_key(tr, 'd_m', ('delta_m',))
            kh_native = np.asarray(tr[k_key], dtype=float)
            dm_native_z = np.asarray(tr[dm_key_target], dtype=float)
            for ik, kh_req in enumerate(K_H):
                j = int(np.argmin(np.abs(kh_native - float(kh_req))))
                kh = float(kh_native[j])
                k_phys = kh * H
                rel = abs(kh - float(kh_req)) / max(abs(float(kh_req)), 1.0e-300)
                dm = float(dm_native_z[j])
                target_dm[ik, iz] = dm
                target_source[ik, iz] = float(source_power(np.array([dm]), np.array([k_phys]))[0])
                target_pk[ik, iz] = float(c.pk_lin(k_phys, float(z)))
                target_k_actual_h[ik, iz] = kh
                target_k_rel[ik, iz] = rel

        if not trace_path.exists() or trace_path.stat().st_size == 0:
            raise RuntimeError(f'{label}: accepted-source-grid trace not produced')

        result = {
            'pk_native': pk_native.copy(),
            'd_m_native': d_m_native.copy(),
            'p_source_native': p_source_native.copy(),
            'k_pk': k_pk.copy(),
            'z_pk': z_pk.copy(),
            'k_tk': k_tk.copy(),
            'z_tk': z_tk.copy(),
            'k_grid_rel': k_grid_rel,
            'z_grid_abs': z_grid_abs,
            'target_source': target_source,
            'target_pk': target_pk,
            'target_dm': target_dm,
            'target_k_actual_h': target_k_actual_h,
            'target_k_rel': target_k_rel,
            'transfer_keys': sorted(tk_native.keys()),
        }
        c.struct_cleanup()
        c.empty()
        c = None
        return result
    finally:
        if c is not None:
            try:
                c.struct_cleanup()
                c.empty()
            except Exception:
                pass
        _restore_env(saved)


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

    base = compute_run(force_file, None, 'base')
    plus_runs = []
    minus_runs = []
    g_node_source = np.empty((LAMBDAS.size,) + base['p_source_native'].shape, dtype=float)
    g_node_pk = np.empty_like(g_node_source)
    g_target_source = np.empty((LAMBDAS.size, K_H.size, Z_TARGET.size), dtype=float)
    g_target_pk = np.empty_like(g_target_source)

    all_runs = [base]
    for il, lam in enumerate(LAMBDAS):
        tag = str(float(lam)).replace('.', 'p')
        pr = compute_run(force_file, +float(lam), f'plus_{tag}')
        mr = compute_run(force_file, -float(lam), f'minus_{tag}')
        plus_runs.append(pr)
        minus_runs.append(mr)
        all_runs += [pr, mr]

        # Native grids must be identical across all runs before any tangent is formed.
        for rname, rr in [('plus', pr), ('minus', mr)]:
            if not np.allclose(rr['k_pk'], base['k_pk'], rtol=0.0, atol=1.0e-14):
                raise RuntimeError(f'{rname} lambda={lam}: native Fourier k grid changed')
            if not np.allclose(rr['z_pk'], base['z_pk'], rtol=0.0, atol=1.0e-14):
                raise RuntimeError(f'{rname} lambda={lam}: native Fourier z grid changed')

        g_node_source[il] = response(
            base['p_source_native'], pr['p_source_native'], mr['p_source_native'], lam
        )
        g_node_pk[il] = response(base['pk_native'], pr['pk_native'], mr['pk_native'], lam)
        g_target_source[il] = response(
            base['target_source'], pr['target_source'], mr['target_source'], lam
        )
        g_target_pk[il] = response(base['target_pk'], pr['target_pk'], mr['target_pk'], lam)

    # Primary native-node window is the fixed v0.63 k/z envelope, evaluated on
    # all native common nodes inside it.
    kh_native = base['k_pk'] / H
    mask = (
        (kh_native[:, None] >= 0.03)
        & (kh_native[:, None] <= 0.20)
        & (base['z_pk'][None, :] >= 0.2)
        & (base['z_pk'][None, :] <= 1.5)
    )
    if not np.any(mask):
        raise RuntimeError('v0.76 native-node primary window is empty')

    closure_native_arrays = []
    target_closure_arrays = []
    all_powers_finite_positive = True
    max_k_grid_rel = 0.0
    max_z_grid_abs = 0.0
    max_target_k_rel = 0.0
    for rr in all_runs:
        closure_native_arrays.append(
            np.abs(rr['p_source_native'] - rr['pk_native']) /
            np.maximum(rr['pk_native'], 1.0e-300)
        )
        target_closure_arrays.append(
            np.abs(rr['target_source'] - rr['target_pk']) /
            np.maximum(rr['target_pk'], 1.0e-300)
        )
        for arr in (rr['p_source_native'], rr['pk_native'], rr['target_source'], rr['target_pk']):
            all_powers_finite_positive = bool(
                all_powers_finite_positive
                and np.all(np.isfinite(arr))
                and np.all(arr > 0.0)
            )
        max_k_grid_rel = max(max_k_grid_rel, float(rr['k_grid_rel']))
        max_z_grid_abs = max(max_z_grid_abs, float(rr['z_grid_abs']))
        max_target_k_rel = max(max_target_k_rel, float(np.max(rr['target_k_rel'])))

    native_closure_max = float(max(np.max(x[mask]) for x in closure_native_arrays))
    native_baseline_closure_max = float(np.max(closure_native_arrays[0][mask]))
    target_closure_max = float(max(np.max(x) for x in target_closure_arrays))
    target_baseline_closure_max = float(np.max(target_closure_arrays[0]))

    mean_node_source, eps_node_source = affinity_by_lambda_mask(g_node_source, mask)
    mean_node_pk, eps_node_pk = affinity_by_lambda_mask(g_node_pk, mask)
    mean_target_source, eps_target_source = affinity_by_lambda(g_target_source)
    mean_target_pk, eps_target_pk = affinity_by_lambda(g_target_pk)

    forcing_pass = bool(
        float(forcing['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing['cosine']) >= FORCING_COS_MIN
        and bool(forcing['gate'])
    )
    k_grid_pass = bool(max_k_grid_rel <= GRID_K_REL_MAX)
    z_grid_pass = bool(max_z_grid_abs <= GRID_Z_ABS_MAX)
    native_closure_pass = bool(native_closure_max <= NATIVE_NODE_CLOSURE_MAX)
    native_source_affinity_pass = bool(np.max(eps_node_source) <= NATIVE_SOURCE_AFFINITY_MAX)
    native_fourier_affinity_pass = bool(np.max(eps_node_pk) <= NATIVE_FOURIER_AFFINITY_MAX)
    target_k_pass = bool(max_target_k_rel <= TARGET_K_REL_MAX)
    target_source_affinity_pass = bool(np.max(eps_target_source) <= TARGET_SOURCE_AFFINITY_MAX)

    numerical_pass = bool(
        forcing_pass
        and all_powers_finite_positive
        and k_grid_pass
        and z_grid_pass
        and native_closure_pass
        and native_source_affinity_pass
        and native_fourier_affinity_pass
        and target_k_pass
        and target_source_affinity_pass
    )

    classification = (
        'V076_NATIVE_NODE_POWER_CLOSURE_PASS'
        if numerical_pass
        else 'V076_NATIVE_NODE_POWER_CLOSURE_FAIL'
    )

    target_pk_affinity_max = float(np.max(eps_target_pk))
    if numerical_pass:
        if target_closure_max > HISTORICAL_OFFNODE_SCALE:
            diagnosis = 'V076_TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED'
        else:
            diagnosis = 'V076_NATIVE_AND_OFFNODE_PATHS_CLOSE'
    elif not native_closure_pass:
        diagnosis = 'V076_SOURCE_TO_FOURIER_NATIVE_NODE_MISMATCH'
    else:
        diagnosis = 'V076_PRIMARY_CONTROL_FAILURE'

    result = {
        'classification': classification,
        'diagnosis': diagnosis,
        'predata_classification': 'V076_PREDATA_NATIVE_NODE_POWER_CLOSURE_AUDIT',
        'uses_observational_data': False,
        'result_informed_followup': True,
        'historical_classifications_unchanged': {
            'v074': 'V074_NATIVE_TRANSFER_POWER_CLOSURE_FAIL',
            'v075': 'V075_FOURIER_K_RESOLUTION_CLOSURE_FAIL',
        },
        'scope': 'Theory-only native-node source-to-Fourier closure and off-node interpolation-path localization; no observational likelihood and no nonlinear evolution.',
        'locked_model': {
            'KB': float(v63.KB),
            'tauH0': float(v63.TAUH0),
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': [float(x) for x in LAMBDAS],
        },
        'fixed_numerical_configuration': dict(R4),
        'fixed_target_grid': {
            'k_h_per_Mpc': [float(x) for x in K_H],
            'z': [float(x) for x in Z_TARGET],
        },
        'native_window': {
            'k_h_per_Mpc_min': 0.03,
            'k_h_per_Mpc_max': 0.20,
            'z_min': 0.2,
            'z_max': 1.5,
            'n_common_native_nodes': int(np.sum(mask)),
        },
        'forcing': {
            'relative_L2_control_vs_primary': float(forcing['relative_L2_control_vs_primary']),
            'cosine': float(forcing['cosine']),
            'pass': forcing_pass,
        },
        'native_node': {
            'transfer_vs_fourier_k_relative_error_max_all_runs': float(max_k_grid_rel),
            'transfer_vs_fourier_z_absolute_error_max_all_runs': float(max_z_grid_abs),
            'source_power_vs_fourier_power_relative_error_max_all_runs_in_window': native_closure_max,
            'baseline_source_power_vs_fourier_power_relative_error_max_in_window': native_baseline_closure_max,
            'source_tangent_lambda_affinity_by_lambda': {
                str(float(lam)): float(eps_node_source[i]) for i, lam in enumerate(LAMBDAS)
            },
            'source_tangent_lambda_affinity_max': float(np.max(eps_node_source)),
            'fourier_tangent_lambda_affinity_by_lambda': {
                str(float(lam)): float(eps_node_pk[i]) for i, lam in enumerate(LAMBDAS)
            },
            'fourier_tangent_lambda_affinity_max': float(np.max(eps_node_pk)),
        },
        'off_node_target_diagnostic': {
            'requested_vs_actual_transfer_k_relative_error_max_all_runs': float(max_target_k_rel),
            'source_power_vs_pk_lin_relative_error_max_all_runs': target_closure_max,
            'baseline_source_power_vs_pk_lin_relative_error_max': target_baseline_closure_max,
            'source_tangent_lambda_affinity_by_lambda': {
                str(float(lam)): float(eps_target_source[i]) for i, lam in enumerate(LAMBDAS)
            },
            'source_tangent_lambda_affinity_max': float(np.max(eps_target_source)),
            'pk_lin_tangent_lambda_affinity_by_lambda': {
                str(float(lam)): float(eps_target_pk[i]) for i, lam in enumerate(LAMBDAS)
            },
            'pk_lin_tangent_lambda_affinity_max': target_pk_affinity_max,
            'mean_source_dlnP_deta': mean_target_source.tolist(),
            'mean_pk_lin_dlnP_deta': mean_target_pk.tolist(),
        },
        'gates': {
            'forcing_pass': forcing_pass,
            'all_native_and_target_powers_finite_positive': bool(all_powers_finite_positive),
            'native_transfer_vs_fourier_k_relative_error_max': float(max_k_grid_rel),
            'native_transfer_vs_fourier_k_relative_error_limit': GRID_K_REL_MAX,
            'native_transfer_vs_fourier_k_pass': k_grid_pass,
            'native_transfer_vs_fourier_z_absolute_error_max': float(max_z_grid_abs),
            'native_transfer_vs_fourier_z_absolute_error_limit': GRID_Z_ABS_MAX,
            'native_transfer_vs_fourier_z_pass': z_grid_pass,
            'native_node_source_power_vs_fourier_power_relative_error_max': native_closure_max,
            'native_node_source_power_vs_fourier_power_relative_error_limit': NATIVE_NODE_CLOSURE_MAX,
            'native_node_source_power_vs_fourier_power_pass': native_closure_pass,
            'native_node_source_tangent_lambda_affinity_max': float(np.max(eps_node_source)),
            'native_node_source_tangent_lambda_affinity_limit': NATIVE_SOURCE_AFFINITY_MAX,
            'native_node_source_tangent_lambda_affinity_pass': native_source_affinity_pass,
            'native_node_fourier_tangent_lambda_affinity_max': float(np.max(eps_node_pk)),
            'native_node_fourier_tangent_lambda_affinity_limit': NATIVE_FOURIER_AFFINITY_MAX,
            'native_node_fourier_tangent_lambda_affinity_pass': native_fourier_affinity_pass,
            'target_requested_vs_actual_transfer_k_relative_error_max': float(max_target_k_rel),
            'target_requested_vs_actual_transfer_k_relative_error_limit': TARGET_K_REL_MAX,
            'target_requested_vs_actual_transfer_k_pass': target_k_pass,
            'target_source_tangent_lambda_affinity_max': float(np.max(eps_target_source)),
            'target_source_tangent_lambda_affinity_limit': TARGET_SOURCE_AFFINITY_MAX,
            'target_source_tangent_lambda_affinity_pass': target_source_affinity_pass,
            'numerical_pass': numerical_pass,
        },
        'interpretation_policy': 'A PASS certifies native-node source-to-Fourier closure only. If off-node source-then-square and Fourier-log-power paths still disagree, the diagnosis localizes a numerical interpolation-operator discrepancy; it is not observational evidence and does not certify nonlinear evolution.'
    }

    out_json.write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(
        out_npz,
        lambdas=LAMBDAS,
        k_target_h=K_H,
        z_target=Z_TARGET,
        k_native_1_per_Mpc=base['k_pk'],
        z_native=base['z_pk'],
        native_window_mask=mask,
        base_native_dm=base['d_m_native'],
        base_native_source_power=base['p_source_native'],
        base_native_fourier_power=base['pk_native'],
        native_source_response=g_node_source,
        native_fourier_response=g_node_pk,
        native_source_affinity=eps_node_source,
        native_fourier_affinity=eps_node_pk,
        target_source_response=g_target_source,
        target_pk_response=g_target_pk,
        target_source_affinity=eps_target_source,
        target_pk_affinity=eps_target_pk,
        base_target_source_power=base['target_source'],
        base_target_pk_lin=base['target_pk'],
        base_target_dm=base['target_dm'],
        base_target_k_actual_h=base['target_k_actual_h'],
    )

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
