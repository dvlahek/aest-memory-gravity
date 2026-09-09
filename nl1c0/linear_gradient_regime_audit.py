#!/usr/bin/env python3
"""NL1C0 preregistered linear gradient-regime validity audit.

Theory-only. Reconstruct the physical band-limited RMS of the first-order AeST
spatial-gradient variable from the accepted CLASS source-grid chi transfer
function and the frozen primordial curvature spectrum. No nonlinear evolution,
observational data, off-native time interpolation, or physical eta is used.
"""
from pathlib import Path
import argparse
import csv
import json
import math
import os
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import v063.theory_response_map as v63

PRE = json.loads((ROOT / 'nl1c0/predata_linear_gradient_regime_audit.json').read_text())

K_H = np.asarray(PRE['primary_k_grid_h_per_Mpc'], dtype=float)
ZMIN, ZMAX = map(float, PRE['primary_redshift_window'])
HRED = float(PRE['frozen_physical_model']['H0_km_s_Mpc']) / 100.0
K_MPC = K_H * HRED
AS = float(PRE['frozen_physical_model']['A_s'])
NS = float(PRE['frozen_physical_model']['n_s'])
KPIV = float(PRE['frozen_physical_model']['k_pivot_Mpc_inv'])
A0 = float(PRE['frozen_physical_model']['a0_m_s2'])
C = float(PRE['band_integral']['constants']['c_m_s'])
MPC_M = float(PRE['band_integral']['constants']['Mpc_m'])
K_M = K_MPC / MPC_M

K_REL_GATE = float(PRE['primary_numerical_gates']['all_requested_k_modes_found_relative_error_max'])
TIME_REL_GATE = float(PRE['primary_numerical_gates']['common_native_time_grid_relative_mismatch_max'])
MIN_TIMES = int(PRE['primary_numerical_gates']['minimum_common_native_times_inside_redshift_window'])
WIDTH_REL_GATE = float(PRE['primary_numerical_gates']['trapezoid_log_width_sum_relative_error_max'])


def log_trap_weights(k):
    x = np.log(np.asarray(k, dtype=float))
    w = np.empty_like(x)
    w[0] = 0.5 * (x[1] - x[0])
    w[-1] = 0.5 * (x[-1] - x[-2])
    w[1:-1] = 0.5 * (x[2:] - x[:-2])
    return w


def read_trace(path):
    rows = []
    with open(path, newline='') as f:
        for r in csv.DictReader(f, delimiter=' '):
            try:
                rows.append({key: float(value) for key, value in r.items()})
            except Exception:
                continue
    if not rows:
        raise RuntimeError('empty or unreadable accepted-source trace')
    return rows


def cluster_duplicate_times(rows):
    """Collapse repeated source calls at the same accepted tau by medians."""
    rr = sorted(rows, key=lambda r: r['tau'])
    groups = []
    cur = []
    center = None
    for r in rr:
        t = float(r['tau'])
        if center is None or abs(t-center) <= 1e-12 * max(abs(center), abs(t), 1.0):
            cur.append(r)
            center = float(np.median([x['tau'] for x in cur]))
        else:
            groups.append(cur)
            cur = [r]
            center = t
    if cur:
        groups.append(cur)
    out = []
    for g in groups:
        out.append({key: float(np.median([r[key] for r in g])) for key in ['k','tau','a','H_over_H0','chi','Q']})
    return out


def select_mode(rows, target_k):
    rel = np.asarray([abs(r['k']-target_k)/max(abs(target_k), 1e-300) for r in rows])
    m = float(np.min(rel))
    if m > K_REL_GATE:
        raise RuntimeError(f'requested k={target_k:.17g} not found; best relative miss={m:.6g}')
    # Use every row belonging to the exact requested mode, not merely one row.
    selected = [r for r, e in zip(rows, rel) if e <= K_REL_GATE]
    return cluster_duplicate_times(selected), m


def align_modes(modes):
    ref = modes[0]
    if not ref:
        raise RuntimeError('empty reference mode history')
    tau0 = np.asarray([r['tau'] for r in ref], dtype=float)
    aligned = [ref]
    max_rel = 0.0
    for mode in modes[1:]:
        tau = np.asarray([r['tau'] for r in mode], dtype=float)
        if tau.size != tau0.size:
            raise RuntimeError(f'native source time-grid length mismatch: {tau0.size} vs {tau.size}')
        rel = np.abs(tau-tau0) / np.maximum(np.maximum(np.abs(tau0), np.abs(tau)), 1.0)
        max_rel = max(max_rel, float(np.max(rel)))
        if float(np.max(rel)) > TIME_REL_GATE:
            raise RuntimeError(f'native source time-grid mismatch={float(np.max(rel)):.6g}')
        aligned.append(mode)
    # Also require scale factors themselves to be common native output times.
    a0 = np.asarray([r['a'] for r in ref], dtype=float)
    for mode in aligned[1:]:
        aa = np.asarray([r['a'] for r in mode], dtype=float)
        rel = np.abs(aa-a0) / np.maximum(np.maximum(np.abs(a0), np.abs(aa)), 1e-300)
        max_rel = max(max_rel, float(np.max(rel)))
        if float(np.max(rel)) > TIME_REL_GATE:
            raise RuntimeError(f'native source scale-factor mismatch={float(np.max(rel)):.6g}')
    return aligned, max_rel


def run_class_trace(class_root, trace_path):
    from classy import Class

    trace_path = Path(trace_path).resolve()
    if trace_path.exists():
        trace_path.unlink()

    saved = {k: os.environ.get(k) for k in ['AEST_OFFLINE_TRACE_FILE','AEST_TANGENT_FORCE_FILE','AEST_TANGENT_LAMBDA','OMP_NUM_THREADS']}
    cobj = None
    try:
        os.environ['AEST_OFFLINE_TRACE_FILE'] = str(trace_path)
        os.environ.pop('AEST_TANGENT_FORCE_FILE', None)
        os.environ.pop('AEST_TANGENT_LAMBDA', None)
        os.environ['OMP_NUM_THREADS'] = '1'

        pars = dict(v63.class_params())
        pars['output'] = 'mPk,mTk'
        pars['lensing'] = 'no'
        pars['aest_memory_enabled'] = 'no'
        pars['aest_eta'] = 0.0
        pars['k_output_values'] = ', '.join(f'{k:.17g}' for k in K_MPC)
        pars['P_k_max_h/Mpc'] = 2.0
        pars['z_max_pk'] = 5.0
        pars['k_per_decade_for_pk'] = 80.0
        pars['k_per_decade_for_bao'] = 560.0

        cobj = Class()
        cobj.set(pars)
        cobj.compute()
        # Force creation of the native transfer table used by the same source grid.
        cobj.get_transfer_and_k_and_z(output_format='class', h_units=False)
        cobj.struct_cleanup()
        cobj.empty()
        cobj = None
    finally:
        if cobj is not None:
            try:
                cobj.struct_cleanup(); cobj.empty()
            except Exception:
                pass
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    if not trace_path.exists() or trace_path.stat().st_size == 0:
        raise RuntimeError('accepted-source-grid trace not produced')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--class-root', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--csv-out', required=True)
    ap.add_argument('--trace-out', required=True)
    args = ap.parse_args()

    out_json = Path(args.json_out); out_json.parent.mkdir(parents=True, exist_ok=True)
    out_csv = Path(args.csv_out); out_csv.parent.mkdir(parents=True, exist_ok=True)
    trace = Path(args.trace_out); trace.parent.mkdir(parents=True, exist_ok=True)

    run_class_trace(Path(args.class_root).resolve(), trace)
    rows = read_trace(trace)

    mode_histories = []
    k_misses = []
    for k in K_MPC:
        hist, miss = select_mode(rows, float(k))
        mode_histories.append(hist)
        k_misses.append(miss)
    mode_histories, time_grid_rel = align_modes(mode_histories)

    widths = log_trap_weights(K_H)
    width_sum = float(np.sum(widths))
    exact_width = float(math.log(K_H[-1]/K_H[0]))
    width_rel = abs(width_sum-exact_width)/abs(exact_width)

    PR = AS * (K_MPC/KPIV)**(NS-1.0)
    pr_ok = bool(np.all(np.isfinite(PR)) and np.all(PR > 0.0))

    ntime = len(mode_histories[0])
    output_rows = []
    all_finite = True
    for it in range(ntime):
        a = float(mode_histories[0][it]['a'])
        tau = float(mode_histories[0][it]['tau'])
        z = 1.0/a - 1.0
        if z < ZMIN-1e-12 or z > ZMAX+1e-12:
            continue
        chi = np.asarray([mode_histories[ik][it]['chi'] for ik in range(K_H.size)], dtype=float)
        qbg = np.asarray([mode_histories[ik][it]['Q'] for ik in range(K_H.size)], dtype=float)
        finite = bool(np.isfinite(a) and np.isfinite(tau) and np.isfinite(z) and np.all(np.isfinite(chi)) and np.all(np.isfinite(qbg)))
        all_finite = all_finite and finite
        if not finite or a <= 0.0:
            continue

        # CLASS scalar perturbations are transfer functions normalized to R=1.
        # X_hat_i = a^-1 partial_i chi, so the physical acceleration is
        # c^2 (k_comoving/a) chi. P_R supplies the stochastic primordial RMS.
        x_mode = (C*C/A0) * (K_M/a) * np.sqrt(PR) * np.abs(chi)
        terms = widths * x_mode*x_mode
        xrms = float(np.sqrt(np.sum(terms)))
        frac = terms / max(float(np.sum(terms)), 1e-300)
        dom = int(np.argmax(frac))
        if xrms <= 0.1:
            regime = 'DEEP_MOND_SAFETY_BAND'
        elif xrms >= 10.0:
            regime = 'HIGH_GRADIENT_SAFETY_BAND'
        else:
            regime = 'TRANSITION_BAND'
        output_rows.append({
            'tau_Mpc': tau,
            'a': a,
            'z': z,
            'x_rms': xrms,
            'regime': regime,
            'dominant_k_h_per_Mpc': float(K_H[dom]),
            'dominant_fraction': float(frac[dom]),
            'chi': chi.tolist(),
            'x_mode': x_mode.tolist(),
            'weighted_fraction': frac.tolist(),
        })

    nwin = len(output_rows)
    numerical = {
        'requested_k_relative_miss_max': float(max(k_misses)),
        'common_native_time_grid_relative_mismatch_max': float(time_grid_rel),
        'common_native_times_inside_window': int(nwin),
        'all_chi_Q_a_z_finite': bool(all_finite),
        'all_primordial_power_positive_finite': pr_ok,
        'trapezoid_log_width_sum': width_sum,
        'expected_log_band_width': exact_width,
        'trapezoid_log_width_sum_relative_error': float(width_rel),
    }
    gates = {
        'requested_k': numerical['requested_k_relative_miss_max'] <= K_REL_GATE,
        'common_time_grid': numerical['common_native_time_grid_relative_mismatch_max'] <= TIME_REL_GATE,
        'minimum_native_times': nwin >= MIN_TIMES,
        'finite_trace': bool(all_finite),
        'primordial_power': pr_ok,
        'log_width': width_rel <= WIDTH_REL_GATE,
    }
    numerical_pass = bool(all(gates.values()))

    if not numerical_pass:
        classification = 'NL1C0_LINEAR_GRADIENT_REGIME_AUDIT_NUMERICAL_FAIL'
    else:
        xvals = np.asarray([r['x_rms'] for r in output_rows], dtype=float)
        if bool(np.all(xvals <= 0.1)):
            classification = 'NL1C0_LINEAR_STATE_DEEP_MOND_REGIME'
        elif bool(np.all(xvals >= 10.0)):
            classification = 'NL1C0_LINEAR_STATE_HIGH_GRADIENT_REGIME'
        else:
            classification = 'NL1C0_LINEAR_STATE_MIXED_OR_TRANSITION_REGIME'

    xvals = np.asarray([r['x_rms'] for r in output_rows], dtype=float) if output_rows else np.asarray([], dtype=float)
    summary = {
        'classification': classification,
        'predata_classification': PRE['classification'],
        'uses_observational_data': False,
        'physical_eta': 0.0,
        'nonlinear_evolution_used': False,
        'primary_window': {'k_h_per_Mpc': K_H.tolist(), 'z_min': ZMIN, 'z_max': ZMAX},
        'log_trapezoid_weights': widths.tolist(),
        'primordial_power': PR.tolist(),
        'numerical_metrics': numerical,
        'numerical_gates': gates,
        'numerical_pass': numerical_pass,
        'x_rms_summary': None if xvals.size == 0 else {
            'min': float(np.min(xvals)),
            'median': float(np.median(xvals)),
            'max': float(np.max(xvals)),
            'count_le_0p1': int(np.sum(xvals <= 0.1)),
            'count_between_0p1_10': int(np.sum((xvals > 0.1) & (xvals < 10.0))),
            'count_ge_10': int(np.sum(xvals >= 10.0)),
        },
        'native_time_results': output_rows,
        'interpretation_rule': PRE['continuation_rule'],
        'historical_results_unchanged': True,
    }
    out_json.write_text(json.dumps(summary, indent=2) + '\n')

    with out_csv.open('w', newline='') as f:
        fieldnames = ['tau_Mpc','a','z','x_rms','regime','dominant_k_h_per_Mpc','dominant_fraction']
        fieldnames += [f'chi_k_{kh:g}' for kh in K_H]
        fieldnames += [f'xmode_k_{kh:g}' for kh in K_H]
        fieldnames += [f'fraction_k_{kh:g}' for kh in K_H]
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
        for r in output_rows:
            row = {key:r[key] for key in ['tau_Mpc','a','z','x_rms','regime','dominant_k_h_per_Mpc','dominant_fraction']}
            for i, kh in enumerate(K_H):
                row[f'chi_k_{kh:g}'] = r['chi'][i]
                row[f'xmode_k_{kh:g}'] = r['x_mode'][i]
                row[f'fraction_k_{kh:g}'] = r['weighted_fraction'][i]
            w.writerow(row)

    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
