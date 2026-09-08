#!/usr/bin/env python3
"""v0.72 preregistered direct perturbation-mode tangent-affinity audit.

This is a theory-only, result-informed follow-up to v0.68-v0.71. It bypasses
CLASS matter-spectrum interpolation as the primary observable by requesting the
six fixed v0.63 k modes explicitly and reconstructing gauge-invariant total
matter power directly from perturbation variables. The frozen physical model
and eta=0 tangent forcing are unchanged.

Technical repair after run 34277782283: the original v0.63 forcing table was
sampled only on its own CLASS source k grid, while v0.72 asks CLASS to integrate
six additional exact k_output_values. The strict tangent-force loader correctly
aborted when one requested mode was absent from the force table. We therefore
rebuild the *same* eta=0 Drude forcing with those preregistered requested modes
included in the baseline trace. No physical parameter, tangent amplitude,
science gate, or requested (k,z) point is changed.
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
K_H = np.array([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], dtype=float)
Z_GRID = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5], dtype=float)
H0 = float(v63.START['H0'])
h = H0 / 100.0
K_REQ = K_H * h
AS = float(v63.START['A_s'])
NS = float(v63.START['n_s'])
KPIVOT = 0.05

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
K_REL_MAX = 1.0e-8
DIRECT_CLASS_REL_MAX = 1.0e-8
DIRECT_AFFINITY_MAX = 5.0e-3
FORCE_K_REL_MAX = 2.0e-10

REQUIRED = {
    'a', 'delta_b', 'theta_b', 'delta_cdm', 'theta_cdm',
    'delta_ncdm[0]', 'theta_ncdm[0]',
}


def build_forcing_with_requested_modes(class_root):
    """Build the unchanged v0.63 eta=0 forcing with exact v0.72 k support.

    This changes only the trace sampling support. The background/model,
    positive-Drude construction, KB, tauH0, and 512/1024 control/primary
    quadrature orders are identical to v0.63.
    """
    results = ROOT / 'results'
    results.mkdir(exist_ok=True)
    trace = results / 'v072_forcing_trace.dat'
    if trace.exists():
        trace.unlink()

    ini = class_root / 'v072_forcing_trace.ini'
    text = v63.rewrite_ini(v63.BASE.read_text(), 'output/v072_forcing_trace_')
    text += 'k_output_values = ' + ', '.join(f'{k:.17g}' for k in K_REQ) + '\n'
    ini.write_text(text)

    env = os.environ.copy()
    env['OMP_NUM_THREADS'] = '1'
    env['AEST_OFFLINE_TRACE_FILE'] = str(trace.resolve())
    # The baseline trace must not itself be externally forced.
    env.pop('AEST_TANGENT_FORCE_FILE', None)
    env.pop('AEST_TANGENT_LAMBDA', None)

    log = results / 'v072_forcing_trace.log'
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
        raise RuntimeError('v0.72 requested-mode forcing trace was not produced')

    prefix = results / 'v072_forcing'
    summary = results / 'v072_forcing_summary.json'
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
        raise RuntimeError('v0.72 requested-mode forcing table was not produced')

    force_k = np.loadtxt(force, usecols=(0,))
    force_unique = np.unique(np.atleast_1d(force_k).astype(float))
    support_rel = np.array([
        np.min(np.abs(force_unique - k)) / max(abs(k), 1.0e-300)
        for k in K_REQ
    ])
    support_rel_max = float(np.max(support_rel))
    if support_rel_max > FORCE_K_REL_MAX:
        raise RuntimeError(
            f'v0.72 forcing table lacks exact requested-mode support: '
            f'max relative k miss={support_rel_max:.3e}'
        )

    d = json.loads(summary.read_text())
    d['technical_support_repair'] = {
        'source_failed_run_id': 34277782283,
        'reason': 'strict force loader k miss for an exact preregistered k_output_values mode',
        'physical_model_changed': False,
        'science_gates_changed': False,
        'tangent_amplitudes_changed': False,
        'requested_grid_changed': False,
        'max_requested_k_relative_miss_in_force_table': support_rel_max,
        'limit': FORCE_K_REL_MAX,
    }
    summary.write_text(json.dumps(d, indent=2) + '\n')
    return force.resolve(), summary


def interp1_sorted(x, y, x0):
    xx = np.asarray(x, dtype=float)
    yy = np.asarray(y, dtype=float)
    order = np.argsort(xx)
    xs = xx[order]
    ys = yy[order]
    if x0 < xs[0] or x0 > xs[-1]:
        raise RuntimeError(f'interpolation point {x0} outside [{xs[0]}, {xs[-1]}]')
    return float(np.interp(float(x0), xs, ys))


def background_at_z(bg, z):
    if 'z' not in bg:
        raise RuntimeError(f'background z missing; keys={list(bg.keys())}')
    needed = ['(.)rho_b', '(.)rho_cdm', '(.)rho_ncdm[0]', '(.)p_ncdm[0]', 'H [1/Mpc]']
    for key in needed:
        if key not in bg:
            raise RuntimeError(f'missing background key {key}')
    zz = np.asarray(bg['z'], dtype=float)
    return {
        key: interp1_sorted(zz, np.asarray(bg[key], dtype=float), float(z))
        for key in needed
    }


def mode_value(mode, key, z):
    if key not in mode:
        raise RuntimeError(f'missing perturbation key {key}; keys={sorted(mode.keys())}')
    a_target = 1.0 / (1.0 + float(z))
    return interp1_sorted(
        np.asarray(mode['a'], dtype=float),
        np.asarray(mode[key], dtype=float),
        a_target,
    )


def compute_run(force_file, lam, label):
    from classy import Class

    keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA', 'AEST_OFFLINE_TRACE_FILE']
    saved = {key: os.environ.get(key) for key in keys}
    trace_path = ROOT / 'results' / f'v072_{label}_trace.dat'
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
        pars['output'] = 'mPk'
        pars['lensing'] = 'no'
        pars['k_output_values'] = ', '.join(f'{k:.17g}' for k in K_REQ)
        pars['P_k_max_h/Mpc'] = 2.0
        pars['z_max_pk'] = 5.0

        c = Class()
        c.set(pars)
        c.compute()

        pt = c.get_perturbations()['scalar']
        if len(pt) != len(K_REQ):
            raise RuntimeError(f'expected {len(K_REQ)} requested scalar modes, got {len(pt)}')
        bg = c.get_background()
        for mode in pt:
            missing = REQUIRED - set(mode.keys())
            if missing:
                raise RuntimeError(f'missing perturbation keys {sorted(missing)}')

        if not trace_path.exists() or trace_path.stat().st_size == 0:
            raise RuntimeError('requested-mode source-grid trace not produced')
        trace_k = np.loadtxt(trace_path, comments='#', skiprows=1, usecols=(0,))
        trace_unique = np.unique(np.atleast_1d(trace_k).astype(float))
        k_actual = np.array([
            float(trace_unique[np.argmin(np.abs(trace_unique - k))]) for k in K_REQ
        ])
        k_rel = np.abs(k_actual - K_REQ) / np.maximum(np.abs(K_REQ), 1.0e-300)

        p_direct = np.empty((K_H.size, Z_GRID.size), dtype=float)
        p_class = np.empty_like(p_direct)
        dm_store = np.empty_like(p_direct)

        for ik, (mode, k) in enumerate(zip(pt, k_actual)):
            for iz, z in enumerate(Z_GRID):
                b = background_at_z(bg, float(z))
                rho_b = b['(.)rho_b']
                rho_cdm = b['(.)rho_cdm']
                rho_n = b['(.)rho_ncdm[0]']
                p_n = b['(.)p_ncdm[0]']
                H = b['H [1/Mpc]']
                rho_m = rho_b + rho_cdm + rho_n
                rho_plus_p = rho_b + rho_cdm + rho_n + p_n

                db = mode_value(mode, 'delta_b', z)
                tb = mode_value(mode, 'theta_b', z)
                dc = mode_value(mode, 'delta_cdm', z)
                tc = mode_value(mode, 'theta_cdm', z)
                dn = mode_value(mode, 'delta_ncdm[0]', z)
                tn = mode_value(mode, 'theta_ncdm[0]', z)
                a = 1.0 / (1.0 + float(z))

                delta_m = (rho_b * db + rho_cdm * dc + rho_n * dn) / rho_m
                theta_m = (rho_b * tb + rho_cdm * tc + (rho_n + p_n) * tn) / rho_plus_p
                Dm = delta_m + 3.0 * a * H * theta_m / (k * k)
                PR = AS * (k / KPIVOT) ** (NS - 1.0)
                pd = (2.0 * math.pi**2 / k**3) * Dm**2 * PR
                pc = float(c.pk_lin(float(k), float(z)))
                dm_store[ik, iz] = Dm
                p_direct[ik, iz] = pd
                p_class[ik, iz] = pc

        c.struct_cleanup()
        c.empty()
        return {
            'p_direct': p_direct,
            'p_class': p_class,
            'Dm': dm_store,
            'k_actual': k_actual,
            'k_rel': k_rel,
        }
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def response(base, plus, minus, lam):
    return (np.asarray(plus) - np.asarray(minus)) / (
        2.0 * float(lam) * np.asarray(base)
    )


def affinity_by_lambda(values):
    arr = np.asarray(values, dtype=float)
    mean = np.mean(arr, axis=0)
    den = float(np.sum(mean * mean))
    eps = np.empty(arr.shape[0], dtype=float)
    for il in range(arr.shape[0]):
        num = float(np.sum((arr[il] - mean) ** 2))
        eps[il] = math.sqrt(max(num, 0.0) / max(den, 1.0e-300))
    return mean, eps


def normalized_rms(a, b):
    aa = np.asarray(a, dtype=float)
    bb = np.asarray(b, dtype=float)
    return float(np.sqrt(np.sum((aa - bb) ** 2) / max(np.sum(aa * aa), 1.0e-300)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--class-root', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--npz-out', required=True)
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    force_file, forcing_summary_path = build_forcing_with_requested_modes(class_root)
    forcing_summary = json.loads(Path(forcing_summary_path).read_text())

    base = compute_run(force_file, None, 'base')
    plus_runs = []
    minus_runs = []
    gd = np.empty((LAMBDAS.size, K_H.size, Z_GRID.size), dtype=float)
    gc = np.empty_like(gd)

    all_power_arrays = [base['p_direct'], base['p_class']]
    all_k_rel = [base['k_rel']]
    power_rel_by_run = {
        'base': np.abs(base['p_direct'] - base['p_class']) / np.maximum(base['p_class'], 1.0e-300)
    }

    for il, lam in enumerate(LAMBDAS):
        pr = compute_run(force_file, +float(lam), f'plus_{str(float(lam)).replace(".","p")}')
        mr = compute_run(force_file, -float(lam), f'minus_{str(float(lam)).replace(".","p")}')
        plus_runs.append(pr)
        minus_runs.append(mr)
        gd[il] = response(base['p_direct'], pr['p_direct'], mr['p_direct'], lam)
        gc[il] = response(base['p_class'], pr['p_class'], mr['p_class'], lam)
        all_power_arrays += [pr['p_direct'], pr['p_class'], mr['p_direct'], mr['p_class']]
        all_k_rel += [pr['k_rel'], mr['k_rel']]
        power_rel_by_run[f'+{float(lam)}'] = np.abs(pr['p_direct'] - pr['p_class']) / np.maximum(pr['p_class'], 1.0e-300)
        power_rel_by_run[f'-{float(lam)}'] = np.abs(mr['p_direct'] - mr['p_class']) / np.maximum(mr['p_class'], 1.0e-300)

    mean_d, eps_d = affinity_by_lambda(gd)
    mean_c, eps_c = affinity_by_lambda(gc)

    finite_positive = bool(all(np.all(np.isfinite(x)) and np.all(x > 0.0) for x in all_power_arrays))
    forcing_ok = bool(
        float(forcing_summary['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing_summary['cosine']) >= FORCING_COS_MIN
        and bool(forcing_summary['gate'])
    )
    k_rel_max = float(max(np.max(x) for x in all_k_rel))
    k_ok = bool(k_rel_max <= K_REL_MAX)
    direct_class_rel_max = float(max(np.max(x) for x in power_rel_by_run.values()))
    direct_class_ok = bool(direct_class_rel_max <= DIRECT_CLASS_REL_MAX)
    direct_affinity = float(np.max(eps_d))
    class_affinity = float(np.max(eps_c))
    direct_affinity_ok = bool(direct_affinity <= DIRECT_AFFINITY_MAX)

    numerical_pass = bool(
        finite_positive and forcing_ok and k_ok and direct_class_ok and direct_affinity_ok
    )
    classification = (
        'V072_DIRECT_TRANSFER_TANGENT_AFFINITY_PASS'
        if numerical_pass else
        'V072_DIRECT_TRANSFER_TANGENT_AFFINITY_FAIL'
    )
    if direct_affinity_ok and class_affinity > DIRECT_AFFINITY_MAX:
        diagnosis = 'CLASS_PK_LIN_INTERPOLATION_PATH_IMPLICATED'
    elif not direct_affinity_ok:
        diagnosis = 'DIRECT_MODE_TANGENT_NONAFFINITY_SURVIVES'
    else:
        diagnosis = 'DIRECT_AND_PK_LIN_AFFINITY_CONSISTENT'

    rows = []
    for ik, kh in enumerate(K_H):
        for iz, z in enumerate(Z_GRID):
            rows.append({
                'k_h_per_Mpc': float(kh),
                'z': float(z),
                'mean_direct_dlnP_deta': float(mean_d[ik, iz]),
                'mean_pk_lin_dlnP_deta': float(mean_c[ik, iz]),
                'direct_minus_pk_lin_response': float(mean_d[ik, iz] - mean_c[ik, iz]),
                'direct_by_lambda': {str(float(lam)): float(gd[il, ik, iz]) for il, lam in enumerate(LAMBDAS)},
                'pk_lin_by_lambda': {str(float(lam)): float(gc[il, ik, iz]) for il, lam in enumerate(LAMBDAS)},
            })

    result = {
        'classification': classification,
        'predata_classification': 'V072_PREDATA_DIRECT_TRANSFER_TANGENT_AFFINITY_AUDIT',
        'uses_observational_data': False,
        'result_informed_followup': True,
        'historical_classifications_unchanged': {
            'v068': 'V068_LINEAR_SCALE_MEMORY_RESPONSE_MAP_FAIL',
            'v071': 'V071_EXACT_BROADBAND_ONSET_TANGENT_FAIL',
        },
        'technical_history': {
            'run_34277782283': 'TECHNICAL_FAIL_FORCE_K_SUPPORT_MISS_BEFORE_SCIENCE_RESULT',
            'repair': 'same eta=0 forcing rebuilt with the preregistered exact requested modes included in the source-grid trace',
        },
        'scope': 'Theory-only eta=0 tangent numerical audit; no observational likelihood or nonlinear evolution.',
        'locked_model': {
            'KB': v63.KB,
            'tauH0': v63.TAUH0,
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': [float(x) for x in LAMBDAS],
        },
        'fixed_grid': {
            'k_h_per_Mpc': [float(x) for x in K_H],
            'z': [float(x) for x in Z_GRID],
            'provenance': 'v063 preregistered fixed RSD grid',
        },
        'forcing': {
            'relative_L2_control_vs_primary': float(forcing_summary['relative_L2_control_vs_primary']),
            'cosine': float(forcing_summary['cosine']),
            'requested_mode_support_relative_miss_max': float(
                forcing_summary['technical_support_repair']['max_requested_k_relative_miss_in_force_table']
            ),
        },
        'direct_affinity_by_lambda': {str(float(lam)): float(eps_d[il]) for il, lam in enumerate(LAMBDAS)},
        'pk_lin_affinity_by_lambda': {str(float(lam)): float(eps_c[il]) for il, lam in enumerate(LAMBDAS)},
        'mean_direct_response': mean_d.tolist(),
        'mean_pk_lin_response': mean_c.tolist(),
        'response_direct_vs_pk_lin_global_normalized_RMS': normalized_rms(mean_d, mean_c),
        'rows': rows,
        'diagnosis': diagnosis,
        'gates': {
            'all_direct_and_classy_powers_finite_and_positive': finite_positive,
            'forcing_pass': forcing_ok,
            'requested_vs_actual_k_relative_error_max': k_rel_max,
            'requested_vs_actual_k_relative_error_limit': K_REL_MAX,
            'requested_vs_actual_k_pass': k_ok,
            'direct_vs_classy_power_relative_error_max': direct_class_rel_max,
            'direct_vs_classy_power_relative_error_limit': DIRECT_CLASS_REL_MAX,
            'direct_vs_classy_power_pass': direct_class_ok,
            'direct_tangent_lambda_affinity_max': direct_affinity,
            'direct_tangent_lambda_affinity_limit': DIRECT_AFFINITY_MAX,
            'direct_tangent_lambda_affinity_pass': direct_affinity_ok,
            'pk_lin_tangent_lambda_affinity_max_context_only': class_affinity,
            'numerical_pass': numerical_pass,
        },
        'interpretation_policy': 'A PASS certifies only direct linear-theory eta=0 tangent consistency on the fixed v063 grid. It is not an observational detection and does not by itself certify the broadband nonlinear-onset interpretation of v071.'
    }

    Path(args.json_out).write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(
        args.npz_out,
        k_h_per_Mpc=K_H,
        z=Z_GRID,
        lambdas=LAMBDAS,
        base_direct=base['p_direct'],
        base_pk_lin=base['p_class'],
        direct_response=gd,
        pk_lin_response=gc,
        mean_direct_response=mean_d,
        mean_pk_lin_response=mean_c,
        direct_affinity=eps_d,
        pk_lin_affinity=eps_c,
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
