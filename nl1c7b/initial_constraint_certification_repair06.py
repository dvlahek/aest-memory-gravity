#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair05 as r5

RESOLUTIONS = (512, 1024, 2048)
GRID_PAIRS = ((512, 1024), (1024, 2048))
EXPECTED_REPAIR05_BLOB = '34fd22c73171fce5e32920a94d71d05de61521f6'
EXPECTED_PARENT_RUN = 35225084320
EXPECTED_PARENT_ARTIFACT = 10498343763
EXPECTED_PARENT_DIGEST = '5798127479d0a359b5805aa7bd846caee035e582b0fdb3a08b7cd7ab2dc2e9ce'
PREdata_COMMIT = 'fac8014a1d8740fc2eb131504be812c8e209db67'


def adjacent_grid_control(rows, lo, hi):
    out = []
    ok_all = True
    for s in b4.SCALES:
        for kind in r5.KINDS:
            for beta in r5.BETAS:
                a = next(
                    x for x in rows
                    if x['scale_hinv_Mpc'] == s and x['Nr'] == lo
                    and x['Y_kind'] == kind and x['beta0'] == beta
                )
                b = next(
                    x for x in rows
                    if x['scale_hinv_Mpc'] == s and x['Nr'] == hi
                    and x['Y_kind'] == kind and x['beta0'] == beta
                )
                p = float(a['rms_epsilon_M1'])
                q = float(b['rms_epsilon_M1'])
                if p < 1e-8 and q < 1e-8:
                    rel = 0.0
                    ok = True
                else:
                    rel = abs(p - q) / max(abs(p), abs(q), 1e-300)
                    ok = bool(rel <= r5.GRID_LIMIT)
                ok_all &= ok
                out.append({
                    'scale_hinv_Mpc': s,
                    'Y_kind': kind,
                    'beta0': beta,
                    'Nr_low': lo,
                    'Nr_high': hi,
                    'rms_low': p,
                    'rms_high': q,
                    'relative_difference': rel,
                    'limit': r5.GRID_LIMIT,
                    'pass': ok,
                })
    return bool(ok_all), out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trace', required=True)
    ap.add_argument('--coverage-json', required=True)
    ap.add_argument('--official-npz', required=True)
    ap.add_argument('--parent-json', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    cov = json.loads(Path(a.coverage_json).read_text())
    parent = json.loads(Path(a.parent_json).read_text())
    off = np.load(a.official_npz)

    parent_grid = parent.get('grid_controls', [])
    parent_20_fail = bool(any(
        float(x.get('scale_hinv_Mpc', -1)) == 20.0 and x.get('pass') is False
        for x in parent_grid
    ))
    parent_ok = bool(
        parent.get('classification') == 'NL1C7B4_REPAIR05_IMPLEMENTATION_FAIL'
        and parent.get('summary', {}).get('n_cases') == 54
        and parent.get('summary', {}).get('grid_control_pass') is False
        and parent.get('state_reproduction', {}).get('pass') is True
        and parent_20_fail
    )

    ks, gs = b4.groups(b4.read_trace(a.trace))
    tv = b4.at_ai(gs)
    h = float(cov['h'])
    provenance_ok = bool(
        cov.get('classification') == 'NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and len(ks) == 128
        and cov.get('n_native_times') == 179
        and abs(float(cov.get('a_i')) - b4.AI) < 1e-15
        and parent_ok
    )

    qclass = float(np.median(tv['Q']))
    hclass = float(np.median(tv['H_Mpc_inv']))
    kqbg = float(np.median(tv['KQ']))
    qbg = b4.stable_q_from_kq(kqbg)
    zbg = r5.stable_zbg(kqbg)
    _, _, kdict = r1.build_nonK()
    jac, exact_zero = r5.build_analytic_momentum_jacobians()

    # Frozen 256-point C7A reproduction remains a provenance control only.
    maxrep = 0.0
    for s in b4.SCALES:
        st = b4.make_state(s, 256, ks, h, tv)
        for k, v in st.items():
            key = f's{int(s)}_{k}'
            if key in off.files:
                maxrep = max(maxrep, b4.rel(np.asarray(v), np.asarray(off[key])))
    rep_ok = bool(maxrep <= 1e-12)

    states = {}
    for s in b4.SCALES:
        for nr in RESOLUTIONS:
            states[(s, nr)] = b4.make_state(s, nr, ks, h, tv)

    bridges = []
    for s in b4.SCALES:
        for nr in RESOLUTIONS:
            st = states[(s, nr)]
            D = b4.dmat(st['r'])
            row = {'scale_hinv_Mpc': s, 'Nr': nr}
            row.update(r5.bridge_control(st, qbg, qclass, hclass, D))
            bridges.append(row)
    bridge_ok = bool(all(
        x['E_action_vs_C7A_relative_L2'] <= r5.BRIDGE_LIMIT
        and x['X_action_vs_C7A_relative_L2'] <= r5.BRIDGE_LIMIT
        for x in bridges
    ))

    # Use the Repair05 case evaluator directly, unchanged, for all 81 rows.
    rows = []
    for s in b4.SCALES:
        for nr in RESOLUTIONS:
            st = states[(s, nr)]
            for kind in r5.KINDS:
                for beta in r5.BETAS:
                    rows.append(
                        r5.case_audit(st, s, nr, kind, beta, qbg, zbg, jac, exact_zero)
                    )

    finite = bool(all(
        np.isfinite(x['max_epsilon_M1'])
        and np.isfinite(x['rms_epsilon_M1'])
        and np.isfinite(x['total_M1_L2'])
        for x in rows
    ))
    zeros_ok = bool(all(
        all(z['pass'] for z in x['analytic_zero_checks'].values())
        for x in rows
    ))

    grid_512_1024_ok, grid_512_1024 = adjacent_grid_control(rows, 512, 1024)
    grid_1024_2048_ok, grid_1024_2048 = adjacent_grid_control(rows, 1024, 2048)
    grid_ok = bool(grid_512_1024_ok and grid_1024_2048_ok)

    implementation_ok = bool(
        provenance_ok
        and rep_ok
        and bool(kdict)
        and finite
        and zeros_ok
        and bridge_ok
        and grid_ok
        and len(rows) == 81
    )
    all_close = bool(
        implementation_ok
        and all(x['max_epsilon_M1'] <= r5.PASS_LIMIT for x in rows)
    )
    all_strong = bool(
        implementation_ok
        and all(x['max_epsilon_M1'] >= r5.MISMATCH_FLOOR for x in rows)
    )

    if not implementation_ok:
        cls = 'NL1C7B4_REPAIR06_IMPLEMENTATION_FAIL'
        rc = 2
    elif all_close:
        cls = 'NL1C7B4_REPAIR06_ANALYTIC_LINEAR_MOMENTUM_INTERFACE_PASS'
        rc = 0
    elif all_strong:
        cls = 'NL1C7B4_REPAIR06_ANALYTIC_LEADING_ORDER_INTERFACE_MISMATCH'
        rc = 0
    else:
        cls = 'NL1C7B4_REPAIR06_ANALYTIC_LINEAR_MOMENTUM_DIAGNOSTIC_COMPLETE'
        rc = 0

    result = {
        'classification': cls,
        'scope': 'High-resolution convergence audit of the frozen Repair05 eta=0 analytic first-order radial momentum identity; no state projection and no evolution.',
        'parent': {
            'run': EXPECTED_PARENT_RUN,
            'head_sha': 'cfb43b99162db1b8cf25621d3de795b42e1e2cf9',
            'artifact': EXPECTED_PARENT_ARTIFACT,
            'artifact_sha256': EXPECTED_PARENT_DIGEST,
            'result_freeze_commit': '56de1b3bf028dfdbbab2684bde652056561074c1',
            'classification_expected': 'NL1C7B4_REPAIR05_IMPLEMENTATION_FAIL',
        },
        'locks': {
            'predata_commit': PREdata_COMMIT,
            'repair05_evaluator_blob': EXPECTED_REPAIR05_BLOB,
            'resolutions': list(RESOLUTIONS),
            'grid_pairs': [list(x) for x in GRID_PAIRS],
            'grid_limit': r5.GRID_LIMIT,
            'pass_limit': r5.PASS_LIMIT,
            'strong_mismatch_floor': r5.MISMATCH_FLOOR,
            'bridge_limit': r5.BRIDGE_LIMIT,
        },
        'state_reproduction': {
            'control_Nr': 256,
            'max_relative_L2': maxrep,
            'limit': 1e-12,
            'pass': rep_ok,
        },
        'symbolic_K_dictionary_identity': bool(kdict),
        'background_interface': {
            'Q_CLASS_Mpc_inv': qclass,
            'Q_action_Mpc_inv': qbg,
            'Q_relative_difference': float(abs(qbg - qclass) / max(abs(qbg), abs(qclass), 1e-300)),
            'H_CLASS_Mpc_inv': hclass,
            'H_action_Mpc_inv': b4.H_DIRECT,
            'H_relative_difference': float(abs(b4.H_DIRECT - hclass) / max(abs(b4.H_DIRECT), abs(hclass), 1e-300)),
            'Exp_Z_background': zbg,
        },
        'symbolic_exact_zero_flags': exact_zero,
        'bridge_controls': bridges,
        'grid_controls': {
            '512_to_1024': grid_512_1024,
            '1024_to_2048': grid_1024_2048,
        },
        'summary': {
            'n_cases': len(rows),
            'all_finite': finite,
            'all_analytic_zero_checks_pass': zeros_ok,
            'bridge_pass': bridge_ok,
            'grid_512_1024_pass': grid_512_1024_ok,
            'grid_1024_2048_pass': grid_1024_2048_ok,
            'grid_control_pass': grid_ok,
            'min_max_epsilon_M1': float(min(x['max_epsilon_M1'] for x in rows)),
            'max_max_epsilon_M1': float(max(x['max_epsilon_M1'] for x in rows)),
            'min_rms_epsilon_M1': float(min(x['rms_epsilon_M1'] for x in rows)),
            'max_rms_epsilon_M1': float(max(x['rms_epsilon_M1'] for x in rows)),
            'all_cases_linear_close': all_close,
            'all_cases_strong_mismatch': all_strong,
            'dominant_group_counts': {
                g: sum(x['dominant_group_at_max_residual'] == g for x in rows)
                for g in ('GR', 'AeST_nonK_nonJ', 'AeST_J', 'AeST_K', 'dust', 'standard_bg')
            },
            'pass_limit': r5.PASS_LIMIT,
            'strong_mismatch_floor': r5.MISMATCH_FLOOR,
        },
        'rows': rows,
        'claim_boundary': {
            'repair05_primary_evaluator_modified': False,
            'finite_difference_tangent_used_for_primary_result': False,
            'state_projected': False,
            'coefficient_fitted': False,
            'dust_sign_changed': False,
            'radial_standard_species_added': False,
            'Y_branch_selected': False,
            'scale_selected': False,
            'nonlinear_evolution_executed': False,
            'finite_eta_executed': False,
        },
    }

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(rc)


if __name__ == '__main__':
    main()
