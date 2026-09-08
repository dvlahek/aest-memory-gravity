#!/usr/bin/env python3
"""v0.75 preregistered CLASS k-resolution closure audit.

Theory-only, result-informed follow-up to v0.74. The physical model, fixed
(k,z) grid and tangent amplitudes are unchanged. The only scanned numerical
quantity is the preregistered CLASS scalar/Fourier k sampling density. Both
k_per_decade_for_pk and k_per_decade_for_bao are scaled together by factors
1,2,4,8 relative to their CLASS defaults.
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
import v072.direct_transfer_tangent_affinity as v72

LAMBDAS = v72.LAMBDAS.copy()
K_H = v72.K_H.copy()
Z_GRID = v72.Z_GRID.copy()
K_REQ = v72.K_REQ.copy()
AS = v72.AS
NS = v72.NS
KPIVOT = v72.KPIVOT
H = float(v63.START['H0']) / 100.0

RESOLUTIONS = [
    {'label': 'r1', 'k_per_decade_for_pk': 10.0, 'k_per_decade_for_bao': 70.0},
    {'label': 'r2', 'k_per_decade_for_pk': 20.0, 'k_per_decade_for_bao': 140.0},
    {'label': 'r3', 'k_per_decade_for_pk': 40.0, 'k_per_decade_for_bao': 280.0},
    {'label': 'r4', 'k_per_decade_for_pk': 80.0, 'k_per_decade_for_bao': 560.0},
]

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
K_REL_MAX = 1.0e-8
TRANSFER_AFFINITY_MAX = 5.0e-3
HIGHRES_CLOSURE_MAX = 5.0e-3
HIGHRES_PK_AFFINITY_MAX = 5.0e-3
R4_R3_PK_RMS_MAX = 5.0e-3


def _pick_key(d, preferred, alternatives=()):
    if preferred in d:
        return preferred
    for key in alternatives:
        if key in d:
            return key
    raise RuntimeError(f'missing key {preferred}; available keys={sorted(d.keys())}')


def normalized_rms(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.sqrt(np.sum((a - b) ** 2) / max(np.sum(a * a), 1.0e-300)))


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


def _resolution_params(res):
    return {
        'k_per_decade_for_pk': float(res['k_per_decade_for_pk']),
        'k_per_decade_for_bao': float(res['k_per_decade_for_bao']),
    }


def build_forcing_for_resolution(class_root, res):
    """Rebuild the unchanged eta=0 Drude forcing on this locked CLASS k grid."""
    results = ROOT / 'results'
    results.mkdir(exist_ok=True)
    label = res['label']
    trace = results / f'v075_{label}_forcing_trace.dat'
    log = results / f'v075_{label}_forcing_trace.log'
    if trace.exists():
        trace.unlink()

    ini = class_root / f'v075_{label}_forcing_trace.ini'
    text = v63.rewrite_ini(v63.BASE.read_text(), f'output/v075_{label}_forcing_trace_')
    text += 'k_output_values = ' + ', '.join(f'{k:.17g}' for k in K_REQ) + '\n'
    text += f"k_per_decade_for_pk = {float(res['k_per_decade_for_pk']):.17g}\n"
    text += f"k_per_decade_for_bao = {float(res['k_per_decade_for_bao']):.17g}\n"
    ini.write_text(text)

    env = os.environ.copy()
    env['OMP_NUM_THREADS'] = '1'
    env['AEST_OFFLINE_TRACE_FILE'] = str(trace.resolve())
    env.pop('AEST_TANGENT_FORCE_FILE', None)
    env.pop('AEST_TANGENT_LAMBDA', None)

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
        raise RuntimeError(f'{label}: forcing trace not produced')

    prefix = results / f'v075_{label}_forcing'
    summary = results / f'v075_{label}_forcing_summary.json'
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
        raise RuntimeError(f'{label}: forcing table not produced')

    d = json.loads(summary.read_text())
    d['v075_resolution'] = dict(res)
    d['physical_model_changed'] = False
    d['science_grid_changed'] = False
    summary.write_text(json.dumps(d, indent=2) + '\n')
    return force.resolve(), summary


def compute_run(force_file, lam, res, label):
    from classy import Class

    env_keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA', 'AEST_OFFLINE_TRACE_FILE']
    saved = {key: os.environ.get(key) for key in env_keys}
    trace_path = ROOT / 'results' / f"v075_{res['label']}_{label}_trace.dat"
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
        pars.update(_resolution_params(res))

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
                    f"{res['label']}: unexpected transfer shapes kh={kh_native.shape}, d_m={dm_native.shape}"
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
            raise RuntimeError(f"{res['label']} {label}: accepted-source-grid trace not produced")

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


def evaluate_resolution(class_root, res):
    force_file, summary_path = build_forcing_for_resolution(class_root, res)
    forcing = json.loads(Path(summary_path).read_text())

    base = compute_run(force_file, None, res, 'base')
    gt = np.empty((LAMBDAS.size, K_H.size, Z_GRID.size), dtype=float)
    gp = np.empty_like(gt)
    plus_runs = []
    minus_runs = []
    closure_arrays = [
        np.abs(base['transfer_power'] - base['pk_lin']) / np.maximum(base['pk_lin'], 1.0e-300)
    ]
    all_powers = [base['transfer_power'], base['pk_lin']]
    all_k_rel = [base['k_rel']]
    pk_all_runs = [base['pk_lin']]

    for il, lam in enumerate(LAMBDAS):
        tag = str(float(lam)).replace('.', 'p')
        pr = compute_run(force_file, +float(lam), res, f'plus_{tag}')
        mr = compute_run(force_file, -float(lam), res, f'minus_{tag}')
        plus_runs.append(pr)
        minus_runs.append(mr)
        gt[il] = response(base['transfer_power'], pr['transfer_power'], mr['transfer_power'], lam)
        gp[il] = response(base['pk_lin'], pr['pk_lin'], mr['pk_lin'], lam)
        closure_arrays += [
            np.abs(pr['transfer_power'] - pr['pk_lin']) / np.maximum(pr['pk_lin'], 1.0e-300),
            np.abs(mr['transfer_power'] - mr['pk_lin']) / np.maximum(mr['pk_lin'], 1.0e-300),
        ]
        all_powers += [pr['transfer_power'], pr['pk_lin'], mr['transfer_power'], mr['pk_lin']]
        all_k_rel += [pr['k_rel'], mr['k_rel']]
        pk_all_runs += [pr['pk_lin'], mr['pk_lin']]

    mean_t, eps_t = affinity_by_lambda(gt)
    mean_p, eps_p = affinity_by_lambda(gp)
    forcing_ok = bool(
        float(forcing['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing['cosine']) >= FORCING_COS_MIN
        and bool(forcing['gate'])
    )
    finite_positive = bool(all(np.all(np.isfinite(x)) and np.all(x > 0.0) for x in all_powers))
    k_rel_max = float(max(np.max(x) for x in all_k_rel))
    transfer_affinity_max = float(np.max(eps_t))
    closure_max = float(max(np.max(x) for x in closure_arrays))
    baseline_closure_max = float(np.max(closure_arrays[0]))

    return {
        'resolution': dict(res),
        'forcing': forcing,
        'forcing_pass': forcing_ok,
        'finite_positive': finite_positive,
        'k_rel_max': k_rel_max,
        'transfer_affinity': eps_t,
        'transfer_affinity_max': transfer_affinity_max,
        'pk_affinity': eps_p,
        'pk_affinity_max': float(np.max(eps_p)),
        'closure_max': closure_max,
        'baseline_closure_max': baseline_closure_max,
        'mean_transfer_response': mean_t,
        'mean_pk_response': mean_p,
        'response_rms': normalized_rms(mean_t, mean_p),
        'base_transfer_dm': base['transfer_dm'],
        'base_transfer_power': base['transfer_power'],
        'base_pk_lin': base['pk_lin'],
        'pk_all_runs': np.stack(pk_all_runs, axis=0),
        'transfer_response': gt,
        'pk_response': gp,
        'base_k_actual_h': base['k_actual_h'],
        'base_k_rel': base['k_rel'],
        'transfer_keys': base['transfer_keys'],
    }


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

    levels = [evaluate_resolution(class_root, res) for res in RESOLUTIONS]
    hi = levels[-1]
    prev = levels[-2]

    controls_each = []
    for lev in levels:
        controls_each.append(bool(
            lev['forcing_pass']
            and lev['finite_positive']
            and lev['k_rel_max'] <= K_REL_MAX
            and lev['transfer_affinity_max'] <= TRANSFER_AFFINITY_MAX
        ))

    r4_r3_pk_rms = normalized_rms(hi['pk_all_runs'], prev['pk_all_runs'])
    highres_closure_ok = bool(hi['closure_max'] <= HIGHRES_CLOSURE_MAX)
    highres_pk_affinity_ok = bool(hi['pk_affinity_max'] <= HIGHRES_PK_AFFINITY_MAX)
    r4_r3_ok = bool(r4_r3_pk_rms <= R4_R3_PK_RMS_MAX)
    numerical_pass = bool(
        all(controls_each)
        and highres_closure_ok
        and highres_pk_affinity_ok
        and r4_r3_ok
    )

    classification = (
        'V075_FOURIER_K_RESOLUTION_CLOSURE_PASS'
        if numerical_pass
        else 'V075_FOURIER_K_RESOLUTION_CLOSURE_FAIL'
    )

    closure_seq = [float(lev['closure_max']) for lev in levels]
    baseline_closure_seq = [float(lev['baseline_closure_max']) for lev in levels]
    monotone_closure = bool(all(closure_seq[i + 1] <= closure_seq[i] for i in range(len(closure_seq) - 1)))
    monotone_baseline = bool(all(baseline_closure_seq[i + 1] <= baseline_closure_seq[i] for i in range(len(baseline_closure_seq) - 1)))

    result = {
        'classification': classification,
        'predata_classification': 'V075_PREDATA_FOURIER_K_RESOLUTION_CLOSURE_AUDIT',
        'uses_observational_data': False,
        'result_informed_followup': True,
        'historical_classifications_unchanged': {
            'v072': 'V072_DIRECT_TRANSFER_TANGENT_AFFINITY_FAIL',
            'v073': 'V073_NATIVE_SOURCE_POWER_CLOSURE_FAIL',
            'v074': 'V074_NATIVE_TRANSFER_POWER_CLOSURE_FAIL',
        },
        'scope': 'Theory-only CLASS scalar/Fourier k-resolution convergence audit; no observational likelihood and no nonlinear evolution.',
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
        'resolution_sequence': [dict(x) for x in RESOLUTIONS],
        'per_resolution': {},
        'r4_vs_r3_pk_lin_all_runs_global_normalized_RMS': float(r4_r3_pk_rms),
        'descriptive_closure_monotone_nonincreasing': monotone_closure,
        'descriptive_baseline_closure_monotone_nonincreasing': monotone_baseline,
        'gates': {
            'controls_pass_each_resolution': controls_each,
            'all_controls_pass': bool(all(controls_each)),
            'highest_resolution_transfer_power_vs_pk_lin_relative_error_max': float(hi['closure_max']),
            'highest_resolution_transfer_power_vs_pk_lin_relative_error_limit': HIGHRES_CLOSURE_MAX,
            'highest_resolution_transfer_power_vs_pk_lin_pass': highres_closure_ok,
            'highest_resolution_pk_lin_tangent_lambda_affinity_max': float(hi['pk_affinity_max']),
            'highest_resolution_pk_lin_tangent_lambda_affinity_limit': HIGHRES_PK_AFFINITY_MAX,
            'highest_resolution_pk_lin_tangent_lambda_affinity_pass': highres_pk_affinity_ok,
            'r4_vs_r3_pk_lin_all_runs_global_normalized_RMS': float(r4_r3_pk_rms),
            'r4_vs_r3_pk_lin_all_runs_global_normalized_RMS_limit': R4_R3_PK_RMS_MAX,
            'r4_vs_r3_pk_lin_convergence_pass': r4_r3_ok,
            'numerical_pass': numerical_pass,
        },
        'interpretation_policy': 'A PASS certifies only k-resolution convergence/closure of CLASS pk_lin against the CLASS-native transfer observable on the fixed theory grid. It is not observational evidence and does not certify nonlinear evolution.'
    }

    for lev in levels:
        label = lev['resolution']['label']
        result['per_resolution'][label] = {
            'k_per_decade_for_pk': float(lev['resolution']['k_per_decade_for_pk']),
            'k_per_decade_for_bao': float(lev['resolution']['k_per_decade_for_bao']),
            'forcing_relative_L2_control_vs_primary': float(lev['forcing']['relative_L2_control_vs_primary']),
            'forcing_cosine': float(lev['forcing']['cosine']),
            'forcing_pass': bool(lev['forcing_pass']),
            'all_transfer_and_pk_lin_powers_finite_positive': bool(lev['finite_positive']),
            'requested_vs_actual_transfer_k_relative_error_max': float(lev['k_rel_max']),
            'transfer_tangent_lambda_affinity_by_lambda': {
                str(float(lam)): float(lev['transfer_affinity'][i]) for i, lam in enumerate(LAMBDAS)
            },
            'transfer_tangent_lambda_affinity_max': float(lev['transfer_affinity_max']),
            'pk_lin_tangent_lambda_affinity_by_lambda': {
                str(float(lam)): float(lev['pk_affinity'][i]) for i, lam in enumerate(LAMBDAS)
            },
            'pk_lin_tangent_lambda_affinity_max': float(lev['pk_affinity_max']),
            'transfer_power_vs_pk_lin_relative_error_max_all_runs': float(lev['closure_max']),
            'baseline_transfer_power_vs_pk_lin_relative_error_max': float(lev['baseline_closure_max']),
            'pk_lin_vs_transfer_mean_response_global_normalized_RMS': float(lev['response_rms']),
            'mean_transfer_dlnP_deta': lev['mean_transfer_response'].tolist(),
            'mean_pk_lin_dlnP_deta': lev['mean_pk_response'].tolist(),
        }

    out_json.write_text(json.dumps(result, indent=2) + '\n')

    arrays = {
        'lambdas': LAMBDAS,
        'k_h': K_H,
        'z': Z_GRID,
    }
    for lev in levels:
        label = lev['resolution']['label']
        arrays[f'{label}_base_transfer_dm'] = lev['base_transfer_dm']
        arrays[f'{label}_base_transfer_power'] = lev['base_transfer_power']
        arrays[f'{label}_base_pk_lin'] = lev['base_pk_lin']
        arrays[f'{label}_pk_all_runs'] = lev['pk_all_runs']
        arrays[f'{label}_transfer_response'] = lev['transfer_response']
        arrays[f'{label}_pk_response'] = lev['pk_response']
        arrays[f'{label}_mean_transfer_response'] = lev['mean_transfer_response']
        arrays[f'{label}_mean_pk_response'] = lev['mean_pk_response']
        arrays[f'{label}_transfer_affinity'] = lev['transfer_affinity']
        arrays[f'{label}_pk_affinity'] = lev['pk_affinity']
        arrays[f'{label}_base_k_actual_h'] = lev['base_k_actual_h']
        arrays[f'{label}_base_k_rel'] = lev['base_k_rel']
    np.savez_compressed(out_npz, **arrays)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
