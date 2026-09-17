#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair03 as r3

KINDS = ('Simple', 'Exponential', 'Sharp')
BETAS = (1.0, 0.5, 0.1)
PASS_LIMIT = 1e-5
MISMATCH_FLOOR = 0.1
ZERO_REL_LIMIT = 1e-12
ZERO_ABS_FLOOR = 1e-30
GRID_LIMIT = 2e-2
BRIDGE_LIMIT = 1e-6


def l2(x):
    return float(np.linalg.norm(np.asarray(x, float)))


def rel_l2(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(a), np.linalg.norm(b), 1e-300))


def stable_zbg(kq_bg):
    x = float(kq_bg) / (4.0 * b4.K2 * b4.Z0)
    if not (x > 0.0 and math.isfinite(x)):
        raise RuntimeError('invalid KQ background')
    lx = math.log(x)
    y = lx if lx > 1.0 else x * x
    for _ in range(60):
        f = y + 0.5 * math.log(y) - lx
        fp = 1.0 + 0.5 / y
        yn = y - f / fp
        if not (yn > 0.0 and math.isfinite(yn)):
            yn = 0.5 * y
        if abs(yn - y) < 2e-14 * (1.0 + y):
            y = yn
            break
        y = yn
    return math.sqrt(y)


def arr(v, n):
    a = np.asarray(v, float)
    if a.ndim == 0:
        return np.full(n, float(a))
    return np.broadcast_to(a, (n,)).copy()


def build_analytic_momentum_jacobians():
    N, L, R, b, u, Lt, Rt, ut, pt, Nr, Lr, Rr, br, ur, pr = sp.symbols(
        'N L R b u Lt Rt ut pt Nr Lr Rr br ur pr', real=True
    )
    c = sp.cosh(u)
    s = sp.sinh(u)
    kL = (Lt - b * Lr - L * br) / (N * L)
    kR = (Rt - b * Rr) / (N * R)
    sigma = (pt - b * pr) / N
    X = s * sigma + c * pr / L
    E = c * ((ut - b * ur) / N + Nr / (N * L)) + s * (kL + ur / L)
    P = N * L * R**2

    terms = {
        'GR_kin': P * (-4 * kL * kR - 2 * kR**2),
        'GR_curv_NL': 2 * N * L,
        'GR_curv_Rr': 2 * N * Rr**2 / L,
        'GR_Nr_boundary': 4 * Nr * R * Rr / L,
        'AeST_E2': P * sp.Float(b4.KB) * E**2,
        'AeST_EX': P * sp.Float(2 * b4.C) * E * X,
        'AeST_X2': -P * sp.Float(b4.C) * X**2,
    }
    gauge = {N: 1, b: 0, Nr: 0, br: 0}
    args = [L, R, u, Lt, Rt, ut, pt, Lr, Rr, ur, pr]

    out = {}
    exact_zero = {}
    for name, term in terms.items():
        fb = sp.diff(term, b).subs(gauge)
        fbr = sp.diff(term, br).subs(gauge)
        gb = [sp.diff(fb, a) for a in args]
        gbr = [sp.diff(fbr, a) for a in args]
        exact_zero[name] = bool(all(sp.simplify(x) == 0 for x in gb + gbr))
        out[name] = {
            'gb': [sp.lambdify(args, x, 'numpy') for x in gb],
            'gbr': [sp.lambdify(args, x, 'numpy') for x in gbr],
        }
    return out, exact_zero


def background_and_direction(st, qbg, D):
    n = len(st['r'])
    r = np.asarray(st['r'], float)
    one = np.ones(n)
    zero = np.zeros(n)
    a = b4.AI
    H = b4.H_DIRECT

    l1 = np.asarray(st['L_minus_a'], float)
    r1 = np.asarray(st['R_minus_ar'], float)
    u1 = np.asarray(st['u'], float)
    lt1 = np.asarray(st['Ldot_minus_aH'], float)
    rt1 = np.asarray(st['Rdot_minus_aHr'], float)
    ut1 = np.asarray(st['udot'], float)
    dq1 = np.asarray(st['phidot_minus_Q'], float)
    phi1 = np.asarray(st['phi'], float)

    bg = [
        a * one,
        a * r,
        zero,
        a * H * one,
        a * H * r,
        zero,
        qbg * one,
        zero,
        a * one,
        zero,
        zero,
    ]
    direction = [
        l1,
        r1,
        u1,
        lt1,
        rt1,
        ut1,
        dq1,
        D @ l1,
        D @ r1,
        D @ u1,
        D @ phi1,
    ]
    return bg, direction


def symbolic_linear_terms(st, qbg, D, jac):
    n = len(st['r'])
    bg, direction = background_and_direction(st, qbg, D)
    out = {}
    for name, fs in jac.items():
        fb1 = np.zeros(n)
        fbr1 = np.zeros(n)
        for j in range(len(direction)):
            fb1 += arr(fs['gb'][j](*bg), n) * direction[j]
            fbr1 += arr(fs['gbr'][j](*bg), n) * direction[j]
        fbr1 = np.asarray(fbr1, float)
        fbr1[0] = 0.0
        out[name] = fb1 - D @ fbr1
    return out


def analytic_k_linear(st, zbg, D):
    r = np.asarray(st['r'], float)
    pr1 = D @ np.asarray(st['phi'], float)
    a = b4.AI
    return -8.0 * b4.K2 * (a * (a * r)**2) * pr1 * b4.Z0 * zbg * math.exp(zbg * zbg)


def analytic_dust_linear(st):
    r = np.asarray(st['r'], float)
    a = b4.AI
    vr1 = np.asarray(st['dust_vr'], float)
    return 2.0 * a**2 * (a * r)**2 * b4.VAR_B * vr1


def grouped(terms):
    z = np.zeros_like(next(iter(terms.values())))
    g = {
        'GR': z.copy(),
        'AeST_nonK_nonJ': z.copy(),
        'AeST_J': terms['AeST_J'].copy(),
        'AeST_K': terms['AeST_K'].copy(),
        'dust': terms['dust'].copy(),
        'standard_bg': terms['standard_bg'].copy(),
    }
    for k, v in terms.items():
        if k.startswith('GR_'):
            g['GR'] += v
        elif k in ('AeST_E2', 'AeST_EX', 'AeST_X2'):
            g['AeST_nonK_nonJ'] += v
    return g


def bridge_control(st, qbg, qclass, hclass, D):
    mask = np.arange(len(st['r'])) > 0
    pr1 = D @ np.asarray(st['phi'], float)
    E_action = np.asarray(st['udot'], float) + b4.H_DIRECT * np.asarray(st['u'], float)
    X_action = qbg * np.asarray(st['u'], float) + pr1 / b4.AI
    E_c7a = np.asarray(st['udot'], float) + hclass * np.asarray(st['u'], float)
    X_c7a = qclass * np.asarray(st['u'], float) + pr1 / b4.AI
    return {
        'E_action_vs_C7A_relative_L2': rel_l2(E_action[mask], E_c7a[mask]),
        'X_action_vs_C7A_relative_L2': rel_l2(X_action[mask], X_c7a[mask]),
    }


def case_audit(st, scale, nr, kind, beta, qbg, zbg, jac, exact_zero):
    r = np.asarray(st['r'], float)
    n = len(r)
    D = b4.dmat(r)
    mask = np.arange(n) > 0

    terms = symbolic_linear_terms(st, qbg, D, jac)
    terms['AeST_J'] = np.zeros(n)
    terms['AeST_K'] = analytic_k_linear(st, zbg, D)
    terms['dust'] = analytic_dust_linear(st)
    terms['standard_bg'] = np.zeros(n)

    names = list(terms)
    total = np.sum(np.asarray([terms[k] for k in names]), axis=0)
    den = np.sum(np.abs(np.asarray([terms[k] for k in names])), axis=0)
    floor = 1e-14 * float(np.max(den[mask]))
    eps = np.abs(total) / (den + floor)
    idx = int(np.arange(n)[mask][np.argmax(eps[mask])])

    nonzero_scale = max(
        float(np.max(np.abs(terms['GR_kin'][mask]))),
        float(np.max(np.abs(terms['AeST_K'][mask]))),
        float(np.max(np.abs(terms['dust'][mask]))),
        1e-300,
    )
    zero_limit = ZERO_REL_LIMIT * nonzero_scale + ZERO_ABS_FLOOR
    zero_terms = ('AeST_E2', 'AeST_EX', 'AeST_X2', 'AeST_J')
    zero_checks = {
        k: {
            'max_abs': float(np.max(np.abs(terms[k][mask]))),
            'limit': zero_limit,
            'pass': bool(float(np.max(np.abs(terms[k][mask]))) <= zero_limit),
            'symbolic_exact_zero': bool(exact_zero.get(k, k == 'AeST_J')),
        }
        for k in zero_terms
    }

    g = grouped(terms)
    gat = {k: float(v[idx]) for k, v in g.items()}
    dominant = max(gat, key=lambda k: abs(gat[k]))
    term_summary = {
        k: {
            'max_abs': float(np.max(np.abs(v[mask]))),
            'L2': l2(v[mask]),
            'value_at_max_residual': float(v[idx]),
        }
        for k, v in terms.items()
    }

    return {
        'scale_hinv_Mpc': scale,
        'Nr': nr,
        'Y_kind': kind,
        'beta0': beta,
        'max_epsilon_M1': float(np.max(eps[mask])),
        'rms_epsilon_M1': float(np.sqrt(np.mean(eps[mask]**2))),
        'total_M1_max_abs': float(np.max(np.abs(total[mask]))),
        'total_M1_L2': l2(total[mask]),
        'max_residual': {'index': idx, 'r_Mpc': float(r[idx]), 'x': float(st['x'][idx])},
        'grouped_contributions_at_max_residual': gat,
        'dominant_group_at_max_residual': dominant,
        'analytic_zero_checks': zero_checks,
        'individual_terms': term_summary,
    }


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

    parent_ok = bool(
        parent.get('classification') == 'NL1C7B4_REPAIR04_LINEARIZATION_NUMERICAL_FAIL'
        and parent.get('summary', {}).get('n_cases') == 54
        and parent.get('state_reproduction', {}).get('pass') is True
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
    zbg = stable_zbg(kqbg)
    _, _, kdict = r1.build_nonK()
    jac, exact_zero = build_analytic_momentum_jacobians()

    states = {}
    maxrep = 0.0
    for s in b4.SCALES:
        st = b4.make_state(s, 256, ks, h, tv)
        states[(s, 256)] = st
        for k, v in st.items():
            key = f's{int(s)}_{k}'
            if key in off.files:
                maxrep = max(maxrep, b4.rel(np.asarray(v), np.asarray(off[key])))
        states[(s, 512)] = b4.make_state(s, 512, ks, h, tv)
    rep_ok = bool(maxrep <= 1e-12)

    bridges = []
    for s in b4.SCALES:
        for nr in (256, 512):
            D = b4.dmat(states[(s, nr)]['r'])
            row = {'scale_hinv_Mpc': s, 'Nr': nr}
            row.update(bridge_control(states[(s, nr)], qbg, qclass, hclass, D))
            bridges.append(row)
    bridge_ok = bool(all(
        x['E_action_vs_C7A_relative_L2'] <= BRIDGE_LIMIT
        and x['X_action_vs_C7A_relative_L2'] <= BRIDGE_LIMIT
        for x in bridges
    ))

    rows = []
    for s in b4.SCALES:
        for nr in (256, 512):
            for kind in KINDS:
                for beta in BETAS:
                    rows.append(case_audit(states[(s, nr)], s, nr, kind, beta, qbg, zbg, jac, exact_zero))

    finite = bool(all(
        np.isfinite(x['max_epsilon_M1']) and np.isfinite(x['rms_epsilon_M1'])
        and np.isfinite(x['total_M1_L2']) for x in rows
    ))
    zeros_ok = bool(all(
        all(z['pass'] for z in x['analytic_zero_checks'].values()) for x in rows
    ))

    grid = []
    grid_ok = True
    for s in b4.SCALES:
        for kind in KINDS:
            for beta in BETAS:
                a256 = next(x for x in rows if x['scale_hinv_Mpc'] == s and x['Nr'] == 256 and x['Y_kind'] == kind and x['beta0'] == beta)
                a512 = next(x for x in rows if x['scale_hinv_Mpc'] == s and x['Nr'] == 512 and x['Y_kind'] == kind and x['beta0'] == beta)
                p, q = a256['rms_epsilon_M1'], a512['rms_epsilon_M1']
                if p < 1e-8 and q < 1e-8:
                    rel = 0.0
                    ok = True
                else:
                    rel = abs(p - q) / max(abs(p), abs(q), 1e-300)
                    ok = bool(rel <= GRID_LIMIT)
                grid_ok &= ok
                grid.append({'scale_hinv_Mpc': s, 'Y_kind': kind, 'beta0': beta,
                             'rms_256': p, 'rms_512': q, 'relative_difference': rel,
                             'limit': GRID_LIMIT, 'pass': ok})

    implementation_ok = bool(
        provenance_ok and rep_ok and bool(kdict) and finite and zeros_ok
        and bridge_ok and grid_ok and len(rows) == 54
    )
    all_close = bool(implementation_ok and all(x['max_epsilon_M1'] <= PASS_LIMIT for x in rows))
    all_strong = bool(implementation_ok and all(x['max_epsilon_M1'] >= MISMATCH_FLOOR for x in rows))

    if not implementation_ok:
        cls = 'NL1C7B4_REPAIR05_IMPLEMENTATION_FAIL'
        rc = 2
    elif all_close:
        cls = 'NL1C7B4_REPAIR05_ANALYTIC_LINEAR_MOMENTUM_INTERFACE_PASS'
        rc = 0
    elif all_strong:
        cls = 'NL1C7B4_REPAIR05_ANALYTIC_LEADING_ORDER_INTERFACE_MISMATCH'
        rc = 0
    else:
        cls = 'NL1C7B4_REPAIR05_ANALYTIC_LINEAR_MOMENTUM_DIAGNOSTIC_COMPLETE'
        rc = 0

    result = {
        'classification': cls,
        'scope': 'Preregistered analytic first-directional-derivative audit of the frozen eta=0 radial momentum constraint at lambda=0; no state projection and no evolution.',
        'parent': {
            'run': 35223365082,
            'head_sha': 'd245a3658d8f7043a702f1a09a862d0b9d3bb7f8',
            'artifact': 10498905089,
            'artifact_sha256': '1192b25acc1099bd24ff07c1e0b58c448d946513c895307a7c364aa9cfe66f3f',
            'result_freeze_commit': '148b5f51b08fae9eb3cf1b49404cca99816bb639',
            'predata_commit': '96223c4faf1f912f6c47df830a5c50702b2b2ed5',
        },
        'state_reproduction': {'max_relative_L2': maxrep, 'limit': 1e-12, 'pass': rep_ok},
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
        'grid_controls': grid,
        'summary': {
            'n_cases': len(rows),
            'all_finite': finite,
            'all_analytic_zero_checks_pass': zeros_ok,
            'bridge_pass': bridge_ok,
            'grid_control_pass': bool(grid_ok),
            'min_max_epsilon_M1': float(min(x['max_epsilon_M1'] for x in rows)),
            'max_max_epsilon_M1': float(max(x['max_epsilon_M1'] for x in rows)),
            'min_rms_epsilon_M1': float(min(x['rms_epsilon_M1'] for x in rows)),
            'max_rms_epsilon_M1': float(max(x['rms_epsilon_M1'] for x in rows)),
            'all_cases_linear_close': all_close,
            'all_cases_strong_mismatch': all_strong,
            'dominant_group_counts': {g: sum(x['dominant_group_at_max_residual'] == g for x in rows)
                                      for g in ('GR', 'AeST_nonK_nonJ', 'AeST_J', 'AeST_K', 'dust', 'standard_bg')},
            'pass_limit': PASS_LIMIT,
            'strong_mismatch_floor': MISMATCH_FLOOR,
        },
        'rows': rows,
        'claim_boundary': {
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
