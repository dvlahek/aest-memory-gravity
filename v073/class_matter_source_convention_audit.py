#!/usr/bin/env python3
"""v0.73 preregistered CLASS matter-source convention audit.

Theory-only result-informed follow-up to v0.72.  The physical model, eta=0
variational forcing, tangent amplitudes and fixed (k,z) grid are unchanged.
The primary observable here is the native CLASS perturbation source `delta_m`
that fourier.c itself uses to construct the linear total-matter spectrum.
"""

from pathlib import Path
import argparse
import json
import math
import os
import sys

import numpy as np
from scipy.interpolate import CubicSpline

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

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
K_REL_MAX = 1.0e-8
SOURCE_PK_REL_MAX = 5.0e-3
SOURCE_AFFINITY_MAX = 5.0e-3


def _find_tau_key(bg):
    candidates = [k for k in bg.keys() if 'conf' in k.lower() and 'time' in k.lower()]
    if not candidates:
        raise RuntimeError(f'no conformal-time background key found; keys={list(bg.keys())}')
    # CLASS normally exposes exactly 'conf. time [Mpc]'.
    exact = [k for k in candidates if k.lower() == 'conf. time [mpc]']
    return exact[0] if exact else candidates[0]


def _interp_sorted(x, y, x0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    order = np.argsort(x)
    xs = x[order]
    ys = y[order]
    if x0 < xs[0] or x0 > xs[-1]:
        raise RuntimeError(f'interpolation target {x0} outside [{xs[0]}, {xs[-1]}]')
    return float(np.interp(float(x0), xs, ys))


def _source_at_tau(tau_array, values, tau0):
    """Smooth source interpolation on the native source grid.

    CLASS late-source tables are spline-interpolated in ln(tau).  We mirror that
    variable here.  The gate is deliberately 0.5%, not machine precision,
    because this Python diagnostic does not reuse CLASS's internal second
    derivatives.
    """
    tau = np.asarray(tau_array, dtype=float)
    val = np.asarray(values, dtype=float)
    good = np.isfinite(tau) & np.isfinite(val) & (tau > 0.0)
    tau = tau[good]
    val = val[good]
    order = np.argsort(tau)
    tau = tau[order]
    val = val[order]
    # remove duplicate tau values if any
    keep = np.r_[True, np.diff(tau) > 0.0]
    tau = tau[keep]
    val = val[keep]
    if tau0 < tau[0] or tau0 > tau[-1]:
        raise RuntimeError(f'tau target {tau0} outside source range [{tau[0]}, {tau[-1]}]')
    if tau.size < 4:
        return float(np.interp(tau0, tau, val))
    cs = CubicSpline(np.log(tau), val)
    return float(cs(math.log(tau0)))


def _raw_manual_Dm(pt_modes, bg, k_actual, z):
    # Same diagnostic reconstruction as v0.72; it is not a v0.73 science gate.
    out = np.empty(len(k_actual), dtype=float)
    for ik, (mode, k) in enumerate(zip(pt_modes, k_actual)):
        b = v72.background_at_z(bg, float(z))
        rho_b = b['(.)rho_b']
        rho_cdm = b['(.)rho_cdm']
        rho_n = b['(.)rho_ncdm[0]']
        p_n = b['(.)p_ncdm[0]']
        H = b['H [1/Mpc]']
        rho_m = rho_b + rho_cdm + rho_n
        rho_plus_p = rho_b + rho_cdm + rho_n + p_n

        db = v72.mode_value(mode, 'delta_b', z)
        tb = v72.mode_value(mode, 'theta_b', z)
        dc = v72.mode_value(mode, 'delta_cdm', z)
        tc = v72.mode_value(mode, 'theta_cdm', z)
        dn = v72.mode_value(mode, 'delta_ncdm[0]', z)
        tn = v72.mode_value(mode, 'theta_ncdm[0]', z)
        a = 1.0 / (1.0 + float(z))

        delta_m = (rho_b * db + rho_cdm * dc + rho_n * dn) / rho_m
        theta_m = (rho_b * tb + rho_cdm * tc + (rho_n + p_n) * tn) / rho_plus_p
        out[ik] = delta_m + 3.0 * a * H * theta_m / (k * k)
    return out


def compute_run(force_file, lam, label):
    from classy import Class

    keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA', 'AEST_OFFLINE_TRACE_FILE']
    saved = {key: os.environ.get(key) for key in keys}
    trace_path = ROOT / 'results' / f'v073_{label}_trace.dat'
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
        bg = c.get_background()
        sources, source_k, source_tau = c.get_sources()
        if 'delta_m' not in sources:
            raise RuntimeError(f'native CLASS delta_m source missing; source keys={sorted(sources.keys())}')
        if len(pt) != len(K_REQ):
            raise RuntimeError(f'expected {len(K_REQ)} requested perturbation modes, got {len(pt)}')

        source_k = np.asarray(source_k, dtype=float)
        source_tau = np.asarray(source_tau, dtype=float)
        delta_src_all = np.asarray(sources['delta_m'], dtype=float)
        if delta_src_all.ndim != 2 or delta_src_all.shape != (source_k.size, source_tau.size):
            raise RuntimeError(
                f'unexpected delta_m source shape {delta_src_all.shape}; '
                f'expected {(source_k.size, source_tau.size)}'
            )

        src_idx = np.array([int(np.argmin(np.abs(source_k - k))) for k in K_REQ], dtype=int)
        k_actual = source_k[src_idx]
        k_rel = np.abs(k_actual - K_REQ) / np.maximum(np.abs(K_REQ), 1.0e-300)

        tau_key = _find_tau_key(bg)
        bg_z = np.asarray(bg['z'], dtype=float)
        bg_tau = np.asarray(bg[tau_key], dtype=float)

        source_delta = np.empty((K_H.size, Z_GRID.size), dtype=float)
        source_power = np.empty_like(source_delta)
        pk_lin = np.empty_like(source_delta)
        manual_Dm = np.empty_like(source_delta)

        for iz, z in enumerate(Z_GRID):
            tau0 = _interp_sorted(bg_z, bg_tau, float(z))
            manual_Dm[:, iz] = _raw_manual_Dm(pt, bg, k_actual, float(z))
            for ik, (isrc, k) in enumerate(zip(src_idx, k_actual)):
                dsrc = _source_at_tau(source_tau, delta_src_all[isrc], tau0)
                PR = AS * (float(k) / KPIVOT) ** (NS - 1.0)
                ps = (2.0 * math.pi**2 / float(k)**3) * dsrc**2 * PR
                pc = float(c.pk_lin(float(k), float(z)))
                source_delta[ik, iz] = dsrc
                source_power[ik, iz] = ps
                pk_lin[ik, iz] = pc

        c.struct_cleanup()
        c.empty()
        return {
            'source_delta': source_delta,
            'source_power': source_power,
            'pk_lin': pk_lin,
            'manual_Dm': manual_Dm,
            'k_actual': k_actual,
            'k_rel': k_rel,
            'tau_key': tau_key,
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


def affinity_by_lambda(arr):
    arr = np.asarray(arr, dtype=float)
    mean = np.mean(arr, axis=0)
    den = float(np.sum(mean * mean))
    eps = []
    for row in arr:
        num = float(np.sum((row - mean) ** 2))
        eps.append(math.sqrt(max(num, 0.0) / max(den, 1.0e-300)))
    return mean, np.asarray(eps, dtype=float)


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
    g_source = np.empty((LAMBDAS.size, K_H.size, Z_GRID.size), dtype=float)
    g_pk = np.empty_like(g_source)

    all_arrays = [base['source_power'], base['pk_lin']]
    all_k_rel = [base['k_rel']]
    source_pk_rel_runs = {
        'base': np.abs(base['source_power'] - base['pk_lin']) / np.maximum(base['pk_lin'], 1.0e-300)
    }

    for il, lam in enumerate(LAMBDAS):
        tag = str(float(lam)).replace('.', 'p')
        pr = compute_run(force_file, +float(lam), f'plus_{tag}')
        mr = compute_run(force_file, -float(lam), f'minus_{tag}')
        plus_runs.append(pr)
        minus_runs.append(mr)
        g_source[il] = response(base['source_power'], pr['source_power'], mr['source_power'], lam)
        g_pk[il] = response(base['pk_lin'], pr['pk_lin'], mr['pk_lin'], lam)
        all_arrays += [pr['source_power'], pr['pk_lin'], mr['source_power'], mr['pk_lin']]
        all_k_rel += [pr['k_rel'], mr['k_rel']]
        source_pk_rel_runs[f'+{float(lam)}'] = np.abs(pr['source_power'] - pr['pk_lin']) / np.maximum(pr['pk_lin'], 1.0e-300)
        source_pk_rel_runs[f'-{float(lam)}'] = np.abs(mr['source_power'] - mr['pk_lin']) / np.maximum(mr['pk_lin'], 1.0e-300)

    mean_source, eps_source = affinity_by_lambda(g_source)
    mean_pk, eps_pk = affinity_by_lambda(g_pk)

    forcing_ok = bool(
        float(forcing['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
        and float(forcing['cosine']) >= FORCING_COS_MIN
        and bool(forcing['gate'])
    )
    finite_positive = bool(all(np.all(np.isfinite(x)) and np.all(x > 0.0) for x in all_arrays))
    k_rel_max = float(max(np.max(x) for x in all_k_rel))
    k_ok = bool(k_rel_max <= K_REL_MAX)
    source_pk_rel_max = float(max(np.max(x) for x in source_pk_rel_runs.values()))
    source_pk_ok = bool(source_pk_rel_max <= SOURCE_PK_REL_MAX)
    source_aff_max = float(np.max(eps_source))
    source_aff_ok = bool(source_aff_max <= SOURCE_AFFINITY_MAX)

    # Diagnostic only: compare v0.72 manual Dm to the native CLASS source.
    src = base['source_delta']
    man = base['manual_Dm']
    manual_norm_rms = normalized_rms(src, man)
    amp_floor = 1.0e-8 * max(float(np.max(np.abs(src))), 1.0e-300)
    mask = np.abs(src) > amp_floor
    if np.any(mask):
        manual_rel_max = float(np.max(np.abs(man[mask] - src[mask]) / np.abs(src[mask])))
    else:
        manual_rel_max = float('nan')

    if forcing_ok and finite_positive and k_ok and source_pk_ok and source_aff_ok:
        classification = 'V073_CLASS_MATTER_SOURCE_CONVENTION_CLOSED'
    elif forcing_ok and finite_positive and k_ok and source_pk_ok and not source_aff_ok:
        classification = 'V073_NATIVE_SOURCE_AFFINITY_FAIL'
    elif forcing_ok and finite_positive and k_ok and not source_pk_ok:
        classification = 'V073_NATIVE_SOURCE_POWER_CLOSURE_FAIL'
    else:
        classification = 'V073_CLASS_MATTER_SOURCE_AUDIT_FAIL'

    report = {
        'classification': classification,
        'predata_classification': 'V073_PREDATA_CLASS_MATTER_SOURCE_CONVENTION_AUDIT',
        'uses_observational_data': False,
        'result_informed_followup': True,
        'historical_classifications_unchanged': {
            'v072': 'V072_DIRECT_TRANSFER_TANGENT_AFFINITY_FAIL'
        },
        'scope': 'Theory-only native CLASS matter-source convention and tangent audit; no observational likelihood or nonlinear evolution.',
        'locked_model': {
            'KB': v63.KB,
            'tauH0': v63.TAUH0,
            'p': 0.0,
            'CLASS_commit': 'e85808324f51fc694d12e3ed7439552a3c3f9540',
            'tangent_amplitudes': LAMBDAS.tolist(),
        },
        'fixed_grid': {
            'k_h_per_Mpc': K_H.tolist(),
            'z': Z_GRID.tolist(),
            'provenance': 'v063 preregistered fixed RSD grid',
        },
        'class_native_definition': {
            'matter_source': 'delta_m',
            'gauge_policy': 'matter_source_in_current_gauge=false (CLASS default): delta_m -> delta_m + 3 a H theta_m/k^2',
            'fourier_source_selection': 'fourier.c selects ppt->index_tp_delta_m for total matter P_m',
            'single_adiabatic_power_identity': 'P_m=(2*pi^2/k^3)*delta_m_source^2*P_R(k)',
            'python_source_time_interpolation': 'cubic spline in ln(tau) over c.get_sources() native source samples',
            'background_tau_key': base['tau_key'],
        },
        'forcing': {
            'relative_L2_control_vs_primary': float(forcing['relative_L2_control_vs_primary']),
            'cosine': float(forcing['cosine']),
        },
        'native_source_affinity_by_lambda': {
            str(float(lam)): float(eps) for lam, eps in zip(LAMBDAS, eps_source)
        },
        'pk_lin_affinity_by_lambda_context_only': {
            str(float(lam)): float(eps) for lam, eps in zip(LAMBDAS, eps_pk)
        },
        'native_source_vs_pk_lin_response_global_normalized_RMS': normalized_rms(mean_source, mean_pk),
        'manual_component_diagnostic': {
            'is_science_gate': False,
            'baseline_manual_Dm_vs_native_delta_m_source_global_normalized_RMS': manual_norm_rms,
            'baseline_manual_Dm_vs_native_delta_m_source_max_relative_difference_above_floor': manual_rel_max,
            'relative_floor': amp_floor,
        },
        'mean_native_source_dlnP_deta': mean_source.tolist(),
        'mean_pk_lin_dlnP_deta': mean_pk.tolist(),
        'gates': {
            'all_native_source_and_pk_lin_powers_finite_positive': finite_positive,
            'forcing_pass': forcing_ok,
            'requested_vs_actual_k_relative_error_max': k_rel_max,
            'requested_vs_actual_k_relative_error_limit': K_REL_MAX,
            'requested_vs_actual_k_pass': k_ok,
            'native_source_power_vs_pk_lin_relative_error_max': source_pk_rel_max,
            'native_source_power_vs_pk_lin_relative_error_limit': SOURCE_PK_REL_MAX,
            'native_source_power_vs_pk_lin_pass': source_pk_ok,
            'native_source_tangent_lambda_affinity_max': source_aff_max,
            'native_source_tangent_lambda_affinity_limit': SOURCE_AFFINITY_MAX,
            'native_source_tangent_lambda_affinity_pass': source_aff_ok,
            'numerical_pass': bool(forcing_ok and finite_positive and k_ok and source_pk_ok and source_aff_ok),
        },
        'interpretation_policy': 'A closure result certifies only the native CLASS matter-source convention and eta=0 tangent consistency on the fixed theory grid. It is not an observational detection and does not itself certify nonlinear-onset physics.'
    }

    out_json.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    np.savez_compressed(
        out_npz,
        lambdas=LAMBDAS,
        k_h=K_H,
        z=Z_GRID,
        source_delta_base=base['source_delta'],
        source_power_base=base['source_power'],
        pk_lin_base=base['pk_lin'],
        manual_Dm_base=base['manual_Dm'],
        g_source=g_source,
        g_pk=g_pk,
        mean_source=mean_source,
        mean_pk=mean_pk,
        eps_source=eps_source,
        eps_pk=eps_pk,
    )
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
