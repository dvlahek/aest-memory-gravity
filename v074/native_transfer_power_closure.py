#!/usr/bin/env python3
"""v0.74 preregistered native CLASS transfer-power closure audit.

Result-informed theory-only follow-up to v0.73.  Physics, forcing, tangent
amplitudes and the fixed v0.63 (k,z) grid are unchanged.  Unlike v0.73, this
script does not reimplement CLASS source interpolation in Python.  It obtains
`d_m` through classy.get_transfer(z), whose C path calls
perturbations_output_data_at_z() -> perturbations_sources_at_tau().
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

LAMBDAS = v72.LAMBDAS.copy()
K_H = v72.K_H.copy()
Z_GRID = v72.Z_GRID.copy()
K_REQ = v72.K_REQ.copy()
AS = v72.AS
NS = v72.NS
KPIVOT = v72.KPIVOT
H = float(v63.START['H0']) / 100.0

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
K_REL_MAX = 1.0e-8
TRANSFER_PK_REL_MAX = 5.0e-3
TRANSFER_AFFINITY_MAX = 5.0e-3


def _pick_key(d, preferred, alternatives=()):
    if preferred in d:
        return preferred
    for key in alternatives:
        if key in d:
            return key
    raise RuntimeError(f'missing key {preferred}; available keys={sorted(d.keys())}')


def compute_run(force_file, lam, label):
    from classy import Class

    env_keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA', 'AEST_OFFLINE_TRACE_FILE']
    saved = {key: os.environ.get(key) for key in env_keys}
    trace_path = ROOT / 'results' / f'v074_{label}_trace.dat'
    if trace_path.exists():
        trace_path.unlink()

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

        c = Class()
        c.set(pars)
        c.compute()

        transfer_power = np.empty((K_H.size, Z_GRID.size), dtype=float)
        pk_lin = np.empty_like(transfer_power)
        transfer_dm = np.empty_like(transfer_power)
        k_actual_all = np.empty((K_H.size, Z_GRID.size), dtype=float)
        k_rel_all = np.empty_like(k_actual_all)

        transfer_keys = None
        for iz, z in enumerate(Z_GRID):
            tr = c.get_transfer(float(z), output_format='class')
            if transfer_keys is None:
                transfer_keys = sorted(tr.keys())
            k_key = _pick_key(tr, 'k (h/Mpc)', ('k [h/Mpc]', 'k'))
            dm_key = _pick_key(tr, 'd_m', ('delta_m',))
            kh_native = np.asarray(tr[k_key], dtype=float)
            dm_native = np.asarray(tr[dm_key], dtype=float)
            if kh_native.ndim != 1 or dm_native.shape != kh_native.shape:
                raise RuntimeError(
                    f'unexpected transfer shapes kh={kh_native.shape}, d_m={dm_native.shape}'
                )

            for ik, kh_req in enumerate(K_H):
                j = int(np.argmin(np.abs(kh_native - float(kh_req))))
                kh = float(kh_native[j])
                k = kh * H
                d_m = float(dm_native[j])
                rel = abs(kh - float(kh_req)) / max(abs(float(kh_req)), 1.0e-300)
                PR = AS * (k / KPIVOT) ** (NS - 1.0)
                pt = (2.0 * math.pi**2 / k**3) * d_m**2 * PR
                pc = float(c.pk_lin(k, float(z)))
                transfer_dm[ik, iz] = d_m
                transfer_power[ik, iz] = pt
                pk_lin[ik, iz] = pc
                k_actual_all[ik, iz] = kh
                k_rel_all[ik, iz] = rel

        if not trace_path.exists() or trace_path.stat().st_size == 0:
            raise RuntimeError('v0.74 accepted-source-grid trace not produced')

        c.struct_cleanup()
        c.empty()
        return {
            'transfer_dm': transfer_dm,
            'transfer_power': transfer_power,
            'pk_lin': pk_lin,
            'k_actual_h': k_actual_all,
            'k_rel': k_rel_all,
            'transfer_keys': transfer_keys,
        }
    finally:
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


def affinity_by_lambda(arr):
    arr = np.asarray(arr, dtype=float)
    mean = np.mean(arr, axis=0)
    den = float(np.sum(mean * mean))
    eps = np.empty(arr.shape[0], dtype=float)
    for il in range(arr.shape[0]):
        num = float(np.sum((arr[il] - mean) ** 2))
        eps[il] = math.sqrt(max(num, 0.0) / max(den, 1.0e-300))
    return mean, eps


def normalized_rms(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.sqrt(np.sum((a - b) ** 2) / max(np.sum(a * a), 1.0e-300)))


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
    force_file, forcing_summary_path = v72.build_forcing_with_requested_modes(class_root)
    forcing = json.loads(Path(forcing_summary_path).read_text())

    base = compute_run(force_file, None, 'base')
    plus_runs = []
    minus_runs = []
    gt = np.empty((LAMBDAS.size, K_H.size, Z_GRID.size), dtype=float)
    gp = np.empty_like(gt)

    all_power = [base['transfer_power'], base['pk_lin']]
    all_k_rel = [base['k_rel']]
    closure_runs = {
        'base': np.abs(base['transfer_power'] - base['pk_lin']) / np.maximum(base['pk_lin'], 1.0e-300)
    }

    for il, lam in enumerate(LAMBDAS):
        tag = str(float(lam)).replace('.', 'p')
        pr = compute_run(force_file, +float(lam), f'plus_{tag}')
        mr = compute_run(force_file, -float(lam), f'minus_{tag}')
        plus_runs.append(pr)
        minus_runs.append(mr)
        gt[il] = response(base['transfer_power'], pr['transfer_power'], mr['transfer_power'], lam)
        gp[il] = response(base['pk_lin'], pr['pk_lin'], mr['pk_lin'], lam)
        all_power += [pr['transfer_power'], pr['pk_lin'], mr['transfer_power'], mr['pk_lin']]
        all_k_rel += [pr['k_rel'], mr['k_rel']]
        closure_runs[f'+{float(lam)}'] = np.abs(pr['transfer_power'] - pr['pk_lin']) / np.maximum(pr['pk_lin'], 1.0e-300)
        closure_runs[f'-{float(lam)}'] = np.abs(mr['transfer_power'] - mr['pk_lin']) / np.maximum(mr['pk_lin'], 1.0e-300)

    mean_t, eps_t = affinity_by_lambda(gt)
    mean_p, eps_p = affinity_by_lambda(gp)

    finite_positive = bool(all(np.all(np.isfinite(x)) and np.all(x > 0.0) for x in all_power))
    forcing_ok = bool(
        float(forcing['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing['cosine']) >= FORCING_COS_MIN
        and bool(forcing['gate'])
    )
    k_rel_max = float(max(np.max(x) for x in all_k_rel))
    k_ok = bool(k_rel_max <= K_REL_MAX)
    closure_max = float(max(np.max(x) for x in closure_runs.values()))
    closure_ok = bool(closure_max <= TRANSFER_PK_REL_MAX)
    affinity_max = float(np.max(eps_t))
    affinity_ok = bool(affinity_max <= TRANSFER_AFFINITY_MAX)
    numerical_pass = bool(finite_positive and forcing_ok and k_ok and closure_ok and affinity_ok)

    classification = (
        'V074_NATIVE_TRANSFER_POWER_CLOSURE_PASS'
        if numerical_pass
        else 'V074_NATIVE_TRANSFER_POWER_CLOSURE_FAIL'
    )

    result = {
        'classification': classification,
        'predata_classification': 'V074_PREDATA_NATIVE_TRANSFER_POWER_CLOSURE_AUDIT',
        'uses_observational_data': False,
        'result_informed_followup': True,
        'historical_classifications_unchanged': {
            'v072': 'V072_DIRECT_TRANSFER_TANGENT_AFFINITY_FAIL',
            'v073': 'V073_NATIVE_SOURCE_POWER_CLOSURE_FAIL',
        },
        'scope': 'Theory-only CLASS-native transfer interpolation and power closure audit; no observational likelihood or nonlinear evolution.',
        'locked_model': {
            'KB': float(v63.KB),
            'tauH0': float(v63.TAUH0),
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': [float(x) for x in LAMBDAS],
        },
        'fixed_grid': {
            'k_h_per_Mpc': [float(x) for x in K_H],
            'z': [float(x) for x in Z_GRID],
            'provenance': 'v063 preregistered fixed RSD grid',
        },
        'native_transfer_path': {
            'python_call': "Class.get_transfer(z, output_format='class')",
            'matter_key': 'd_m',
            'k_key': 'k (h/Mpc)',
            'C_path': 'perturbations_output_data_at_z -> perturbations_sources_at_tau',
            'power_identity': 'P=(2*pi^2/k^3)*d_m^2*P_R(k)',
            'transfer_keys_seen': base['transfer_keys'],
        },
        'forcing': {
            'relative_L2_control_vs_primary': float(forcing['relative_L2_control_vs_primary']),
            'cosine': float(forcing['cosine']),
        },
        'transfer_affinity_by_lambda': {
            str(float(lam)): float(eps_t[i]) for i, lam in enumerate(LAMBDAS)
        },
        'pk_lin_affinity_by_lambda_context_only': {
            str(float(lam)): float(eps_p[i]) for i, lam in enumerate(LAMBDAS)
        },
        'transfer_vs_pk_lin_response_global_normalized_RMS_context_only': normalized_rms(mean_t, mean_p),
        'mean_transfer_dlnP_deta': mean_t.tolist(),
        'mean_pk_lin_dlnP_deta': mean_p.tolist(),
        'gates': {
            'all_transfer_and_pk_lin_powers_finite_positive': finite_positive,
            'forcing_pass': forcing_ok,
            'requested_vs_actual_transfer_k_relative_error_max': k_rel_max,
            'requested_vs_actual_transfer_k_relative_error_limit': K_REL_MAX,
            'requested_vs_actual_transfer_k_pass': k_ok,
            'transfer_power_vs_pk_lin_relative_error_max': closure_max,
            'transfer_power_vs_pk_lin_relative_error_limit': TRANSFER_PK_REL_MAX,
            'transfer_power_vs_pk_lin_pass': closure_ok,
            'transfer_tangent_lambda_affinity_max': affinity_max,
            'transfer_tangent_lambda_affinity_limit': TRANSFER_AFFINITY_MAX,
            'transfer_tangent_lambda_affinity_pass': affinity_ok,
            'numerical_pass': numerical_pass,
        },
        'interpretation_policy': 'A PASS certifies only native CLASS transfer-path power closure and eta=0 tangent consistency on the fixed theory grid. It is not an observational detection and does not itself certify nonlinear-onset physics.'
    }

    out_json.write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(
        out_npz,
        lambdas=LAMBDAS,
        k_h=K_H,
        z=Z_GRID,
        base_transfer_dm=base['transfer_dm'],
        base_transfer_power=base['transfer_power'],
        base_pk_lin=base['pk_lin'],
        transfer_response=gt,
        pk_lin_response=gp,
        mean_transfer_response=mean_t,
        mean_pk_lin_response=mean_p,
        transfer_affinity=eps_t,
        pk_lin_affinity=eps_p,
        base_k_actual_h=base['k_actual_h'],
        base_k_rel=base['k_rel'],
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
