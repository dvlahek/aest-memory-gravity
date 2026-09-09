#!/usr/bin/env python3
"""v0.78 preregistered time-interpolation operator closure audit.

This result-informed follow-up to the locked v0.77 PASS compares two CLASS
paths at exactly the same native Fourier k nodes:

  source path:  get_transfer(z) -> d_m(z,k) -> (2 pi^2/k^3) d_m^2 P_R
  Fourier path: pk_lin(k,z), evaluated at that exact native k.

The same run also rechecks source-to-Fourier power closure on common native
(k,tau) nodes. If native closure is exact while an off-native-time discrepancy
survives at exact native k, k interpolation is eliminated and the discrepancy
is localized to the different time-interpolation operators.
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
import v075.fourier_k_resolution_closure as v75

LAMBDAS = np.array([10.0, 5.0, 2.5, 1.25], dtype=float)
Z_TARGET = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5], dtype=float)
H = float(v63.START['H0']) / 100.0
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
K_GRID_REL_MAX = 1.0e-12
NATIVE_CLOSURE_MAX = 5.0e-5
OFFNODE_DISCREPANCY_MIN = 1.0e-2
OFFNODE_POINT_THRESHOLD = 5.0e-3
OFFNODE_POINT_COUNT_MIN = 1


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


def _pick_key(d, preferred, alternatives=()):
    if preferred in d:
        return preferred
    for key in alternatives:
        if key in d:
            return key
    raise RuntimeError(f'missing key {preferred}; available={sorted(d.keys())}')


def _restore_env(saved):
    for key, value in saved.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


def compute_run(force_file, lam, label):
    from classy import Class

    env_keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA', 'AEST_OFFLINE_TRACE_FILE']
    saved = {key: os.environ.get(key) for key in env_keys}
    trace = ROOT / 'results' / f'v078_{label}_trace.dat'
    if trace.exists():
        trace.unlink()

    c = None
    try:
        if lam is None:
            os.environ.pop('AEST_TANGENT_FORCE_FILE', None)
            os.environ.pop('AEST_TANGENT_LAMBDA', None)
        else:
            os.environ['AEST_TANGENT_FORCE_FILE'] = str(force_file)
            os.environ['AEST_TANGENT_LAMBDA'] = str(float(lam))
        os.environ['AEST_OFFLINE_TRACE_FILE'] = str(trace.resolve())
        os.environ['OMP_NUM_THREADS'] = '1'

        pars = dict(v63.class_params())
        pars['output'] = 'mPk,mTk'
        pars['lensing'] = 'no'
        pars['P_k_max_h/Mpc'] = 2.0
        pars['z_max_pk'] = 5.0
        pars['k_per_decade_for_pk'] = 80.0
        pars['k_per_decade_for_bao'] = 560.0

        c = Class()
        c.set(pars)
        c.compute()

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
            raise RuntimeError(f'native shape mismatch pk={pk_native.shape}, dm={d_m_native.shape}')
        if pk_native.shape != (k_pk.size, z_pk.size):
            raise RuntimeError(f'unexpected native orientation {pk_native.shape} vs {(k_pk.size,z_pk.size)}')

        k_native_rel = float(np.max(np.abs(k_tk-k_pk) / np.maximum(np.abs(k_pk),1e-300)))
        z_native_abs = float(np.max(np.abs(z_tk-z_pk)))
        p_source_native = source_power(d_m_native, k_tk)

        kh_native = k_tk / H
        window = (kh_native >= 0.03) & (kh_native <= 0.20)
        if not np.any(window):
            raise RuntimeError('empty native k window')
        k_win = k_tk[window]
        kh_win = kh_native[window]

        source_off = np.empty((k_win.size, Z_TARGET.size), dtype=float)
        pk_off = np.empty_like(source_off)
        k_match_rel = np.empty(Z_TARGET.size, dtype=float)

        for iz, z in enumerate(Z_TARGET):
            tr = c.get_transfer(float(z), output_format='class')
            kkey = _pick_key(tr, 'k (h/Mpc)', ('k [h/Mpc]', 'k'))
            dmkey = _pick_key(tr, 'd_m', ('delta_m',))
            kh_tr = np.asarray(tr[kkey], dtype=float)
            dm_tr = np.asarray(tr[dmkey], dtype=float)
            if kh_tr.size != kh_native.size:
                raise RuntimeError(f'z={z}: transfer k size changed {kh_tr.size} vs {kh_native.size}')
            rel_all = np.abs(kh_tr-kh_native)/np.maximum(np.abs(kh_native),1e-300)
            k_match_rel[iz] = float(np.max(rel_all))
            dm_win = dm_tr[window]
            source_off[:, iz] = source_power(dm_win, k_win)
            pk_off[:, iz] = np.array([float(c.pk_lin(float(k), float(z))) for k in k_win], dtype=float)

        if not trace.exists() or trace.stat().st_size == 0:
            raise RuntimeError(f'{label}: accepted source-grid trace not produced')

        out = {
            'pk_native': pk_native.copy(),
            'p_source_native': p_source_native.copy(),
            'd_m_native': d_m_native.copy(),
            'k_native': k_tk.copy(),
            'z_native': z_tk.copy(),
            'k_native_rel': k_native_rel,
            'z_native_abs': z_native_abs,
            'kh_window': kh_win.copy(),
            'source_off': source_off.copy(),
            'pk_off': pk_off.copy(),
            'k_match_rel': k_match_rel.copy(),
        }
        c.struct_cleanup()
        c.empty()
        c = None
        return out
    finally:
        if c is not None:
            try:
                c.struct_cleanup()
                c.empty()
            except Exception:
                pass
        _restore_env(saved)


def relerr(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return np.abs(a-b)/np.maximum(np.abs(b), 1.0e-300)


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

    runs = [('base', None)]
    for lam in LAMBDAS:
        tag = str(float(lam)).replace('.', 'p')
        runs += [(f'plus_{tag}', +float(lam)), (f'minus_{tag}', -float(lam))]

    data = {}
    native_closure_max = 0.0
    k_grid_rel_max = 0.0
    z_grid_abs_max = 0.0
    offnode_max_by_run = {}
    offnode_count_by_run = {}
    all_finite_positive = True

    for label, lam in runs:
        rr = compute_run(force_file, lam, label)
        data[label] = rr

        nc = relerr(rr['p_source_native'], rr['pk_native'])
        native_closure_max = max(native_closure_max, float(np.max(nc)))
        k_grid_rel_max = max(k_grid_rel_max, float(rr['k_native_rel']), float(np.max(rr['k_match_rel'])))
        z_grid_abs_max = max(z_grid_abs_max, float(rr['z_native_abs']))

        oe = relerr(rr['source_off'], rr['pk_off'])
        offnode_max_by_run[label] = float(np.max(oe))
        offnode_count_by_run[label] = int(np.count_nonzero(oe > OFFNODE_POINT_THRESHOLD))

        for arr in (rr['p_source_native'], rr['pk_native'], rr['source_off'], rr['pk_off']):
            all_finite_positive = bool(
                all_finite_positive and np.all(np.isfinite(arr)) and np.all(arr > 0.0)
            )

    base_off_max = offnode_max_by_run['base']
    base_off_count = offnode_count_by_run['base']

    forcing_pass = bool(
        float(forcing['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing['cosine']) >= FORCING_COS_MIN
    )
    k_pass = bool(k_grid_rel_max <= K_GRID_REL_MAX)
    native_pass = bool(native_closure_max <= NATIVE_CLOSURE_MAX)
    offnode_pass = bool(
        base_off_max >= OFFNODE_DISCREPANCY_MIN
        and base_off_count >= OFFNODE_POINT_COUNT_MIN
    )
    numerical_pass = bool(forcing_pass and k_pass and native_pass and all_finite_positive and offnode_pass)

    classification = (
        'V078_TIME_INTERPOLATION_OPERATOR_CLOSURE_PASS'
        if numerical_pass
        else 'V078_TIME_INTERPOLATION_OPERATOR_CLOSURE_FAIL'
    )
    diagnosis = (
        'V078_TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED'
        if numerical_pass
        else 'V078_TIME_INTERPOLATION_LOCALIZATION_NOT_CERTIFIED'
    )

    base_oe = relerr(data['base']['source_off'], data['base']['pk_off'])
    flat = int(np.argmax(base_oe))
    ik, iz = np.unravel_index(flat, base_oe.shape)

    result = {
        'classification': classification,
        'diagnosis': diagnosis,
        'predata_classification': 'V078_PREDATA_TIME_INTERPOLATION_OPERATOR_CLOSURE_AUDIT',
        'uses_observational_data': False,
        'result_informed_followup': True,
        'historical_classifications_unchanged': {
            'v075': 'V075_FOURIER_K_RESOLUTION_CLOSURE_FAIL',
            'v076': 'V076_NATIVE_NODE_POWER_CLOSURE_FAIL',
            'v077': 'V077_NATIVE_STATE_TANGENT_AFFINITY_PASS',
        },
        'scope': 'Theory-only CLASS operator audit at exact native Fourier k. No nonlinear evolution and no observational likelihood.',
        'locked_model': {
            'KB': v63.KB,
            'tauH0': v63.TAUH0,
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': [float(x) for x in LAMBDAS],
        },
        'fixed_numerical_configuration': dict(R4),
        'forcing': {
            'relative_L2_control_vs_primary': float(forcing['relative_L2_control_vs_primary']),
            'cosine': float(forcing['cosine']),
            'pass': forcing_pass,
        },
        'native_node_closure': {
            'max_relative_error_all_base_and_forced_runs': native_closure_max,
            'limit': NATIVE_CLOSURE_MAX,
            'pass': native_pass,
        },
        'exact_native_k_control': {
            'max_relative_k_mismatch': k_grid_rel_max,
            'limit': K_GRID_REL_MAX,
            'pass': k_pass,
            'max_native_z_grid_mismatch': z_grid_abs_max,
        },
        'off_native_time_exact_native_k': {
            'z_grid': [float(x) for x in Z_TARGET],
            'k_h_per_Mpc_min': 0.03,
            'k_h_per_Mpc_max': 0.20,
            'baseline_max_relative_source_vs_pk_lin_discrepancy': base_off_max,
            'baseline_number_points_above_0p5_percent': base_off_count,
            'diagnostic_floor_for_max_discrepancy': OFFNODE_DISCREPANCY_MIN,
            'minimum_point_count_above_0p5_percent': OFFNODE_POINT_COUNT_MIN,
            'max_relative_discrepancy_by_run': offnode_max_by_run,
            'number_points_above_0p5_percent_by_run': offnode_count_by_run,
            'baseline_largest_discrepancy_location': {
                'k_h_per_Mpc': float(data['base']['kh_window'][ik]),
                'z': float(Z_TARGET[iz]),
                'source_power': float(data['base']['source_off'][ik, iz]),
                'pk_lin': float(data['base']['pk_off'][ik, iz]),
                'relative_discrepancy': float(base_oe[ik, iz]),
            },
            'pass': offnode_pass,
        },
        'gates': {
            'forcing_pass': forcing_pass,
            'all_compared_powers_finite_positive': all_finite_positive,
            'exact_native_k_control_pass': k_pass,
            'native_node_closure_pass': native_pass,
            'off_native_time_discrepancy_survives_at_exact_native_k': offnode_pass,
            'numerical_pass': numerical_pass,
        },
        'interpretation_policy': 'A PASS certifies that source and Fourier matter power agree on common native nodes but diverge at off-native times even when evaluated at exactly the same native Fourier k nodes. Under the frozen CLASS implementation this localizes the discrepancy to the distinct time-interpolation operators, not k interpolation, source-to-power normalization, or native perturbation evolution. A PASS closes the linear numerical-chain debugging and motivates transition to nonlinear AeST+memory physics using the certified state/native-source representation.',
    }

    out_json.write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(
        out_npz,
        z_target=Z_TARGET,
        lambdas=LAMBDAS,
        kh_window=data['base']['kh_window'],
        base_source_off=data['base']['source_off'],
        base_pk_off=data['base']['pk_off'],
        base_off_relerr=base_oe,
        base_p_source_native=data['base']['p_source_native'],
        base_pk_native=data['base']['pk_native'],
        base_k_native=data['base']['k_native'],
        base_z_native=data['base']['z_native'],
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
