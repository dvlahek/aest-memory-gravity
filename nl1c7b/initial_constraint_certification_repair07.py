#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.interpolate import PchipInterpolator

import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair05 as r5

ALGEBRA_LIMIT = 1e-10
FOURIER_ENVELOPE = 2e-2
STATE_LIMIT = 1e-12
RADIAL_RESOLUTIONS = (256, 512)


def l2(x):
    return float(np.linalg.norm(np.asarray(x, float)))


def rel_l2(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(a), np.linalg.norm(b), 1e-300))


def symbolic_k_shift_audit():
    N, L, R, b, u, pt, pr = sp.symbols('N L R b u pt pr', real=True)
    Q0, K2, Z0 = sp.symbols('Q0 K2 Z0', positive=True, real=True)
    c = sp.cosh(u)
    s = sp.sinh(u)
    Q = c * (pt - b * pr) / N + s * pr / L
    z = (Q - Q0) / Z0
    K = 2 * K2 * Z0**2 * (sp.exp(z**2) - 1)
    KQ = 4 * K2 * Z0 * z * sp.exp(z**2)
    LK = 2 * N * L * R**2 * K
    source = sp.simplify(sp.diff(LK, b))
    source_target = -2 * L * R**2 * c * pr * KQ
    source_residual = sp.simplify(source - source_target)

    eps = sp.symbols('eps', real=True)
    aa, rr, qbg = sp.symbols('a r qbg', positive=True, real=True)
    l1, r1, u1, dq1, pr1 = sp.symbols('l1 r1 u1 dq1 pr1', real=True)
    bg_path = {
        N: 1,
        b: 0,
        L: aa + eps * l1,
        R: aa * rr + eps * r1,
        u: eps * u1,
        pt: qbg + eps * dq1,
        pr: eps * pr1,
    }
    source_path = sp.simplify(source_target.subs(bg_path))
    first = sp.simplify(sp.diff(source_path, eps).subs(eps, 0))
    zbg = (qbg - Q0) / Z0
    kqbg = 4 * K2 * Z0 * zbg * sp.exp(zbg**2)
    first_target = -2 * aa**3 * rr**2 * kqbg * pr1
    first_residual = sp.simplify(first - first_target)
    return {
        'exact_shift_source_residual': str(source_residual),
        'exact_frechet_residual': str(first_residual),
        'pass': bool(source_residual == 0 and first_residual == 0),
    }


def pchip_at_ai(g, values):
    x = np.log(np.asarray(g['a'], float))
    return float(PchipInterpolator(x, np.asarray(values, float))(math.log(b4.AI)))


def composite_trace_audit(gs, ks, tv):
    native_a = []
    native_b = []
    comp_ai = []
    theta_ai = []
    cancellation = []
    for kval, g in zip(ks, gs):
        aa = np.asarray(g['a'], float)
        Q = np.asarray(g['Q'], float)
        chi = np.asarray(g['chi'], float)
        alpha = np.asarray(g['alpha_A'], float)
        theta = np.asarray(g['theta_A'], float)
        lhs = chi - Q * alpha
        rhs = aa * Q * theta / (float(kval) ** 2)
        native_a.append(lhs)
        native_b.append(rhs)
        comp_ai.append(pchip_at_ai(g, lhs))
        theta_ai.append(pchip_at_ai(g, rhs))

        chi_i = pchip_at_ai(g, chi)
        q_i = pchip_at_ai(g, Q)
        alpha_i = pchip_at_ai(g, alpha)
        diff_i = chi_i - q_i * alpha_i
        cancellation.append((abs(chi_i) + abs(q_i * alpha_i)) / max(abs(diff_i), 1e-300))

    native_a = np.concatenate(native_a)
    native_b = np.concatenate(native_b)
    comp_ai = np.asarray(comp_ai, float)
    theta_ai = np.asarray(theta_ai, float)
    current_ai = np.asarray(tv['chi'] - tv['Q'] * tv['alpha_A'], float)
    cancellation = np.asarray(cancellation, float)
    return {
        'native_identity_relative_L2': rel_l2(native_a, native_b),
        'composite_first_vs_theta_at_ai_relative_L2': rel_l2(comp_ai, theta_ai),
        'current_componentwise_vs_composite_first_at_ai_relative_L2': rel_l2(current_ai, comp_ai),
        'cancellation_condition_min': float(np.min(cancellation)),
        'cancellation_condition_median': float(np.median(cancellation)),
        'cancellation_condition_max': float(np.max(cancellation)),
        'composite_ai': comp_ai,
        'theta_ai': theta_ai,
        'current_ai': current_ai,
    }


def reconstruct_composite_phi(scale, nr, ks, h, tv, composite_ai):
    k = np.geomspace(ks[0], ks[-1], b4.NQ)
    target = b4.dtarg(k, scale, h)
    ratio = np.asarray(composite_ai, float) / np.asarray(tv['delta_b'], float)
    Fphi = b4.ik(ks, ratio, k) * target
    r = np.linspace(0.0, 8.0, nr) * scale / h
    return b4.inv(k, Fphi, r)


def pointwise_metrics(terms):
    names = list(terms)
    arr = np.asarray([np.asarray(terms[k], float) for k in names])
    total = np.sum(arr, axis=0)
    den = np.sum(np.abs(arr), axis=0)
    mask = np.arange(total.size) > 0
    floor = 1e-14 * float(np.max(den[mask]))
    eps = np.abs(total) / (den + floor)
    max_index = int(np.arange(total.size)[mask][np.argmax(eps[mask])])
    return {
        'total': total,
        'global_L2_ratio': float(l2(total[mask]) / max(sum(l2(terms[k][mask]) for k in names), 1e-300)),
        'max_epsilon_M1': float(np.max(eps[mask])),
        'rms_epsilon_M1': float(np.sqrt(np.mean(eps[mask] ** 2))),
        'median_epsilon_M1': float(np.median(eps[mask])),
        'max_epsilon_index': max_index,
        'denominator_at_max_epsilon': float(den[max_index]),
    }


def radial_case(st, phi_composite, scale, nr, qbg, zbg, jac):
    r = np.asarray(st['r'], float)
    D = b4.dmat(r)
    symbolic = r5.symbolic_linear_terms(st, qbg, D, jac)
    gr_r5 = np.zeros_like(r)
    for name, val in symbolic.items():
        if name.startswith('GR_'):
            gr_r5 += np.asarray(val, float)

    l1 = np.asarray(st['L_minus_a'], float)
    lt1 = np.asarray(st['Ldot_minus_aH'], float)
    k1 = (lt1 - b4.H_DIRECT * l1) / b4.AI
    gr_closed = -4.0 * b4.AI**3 * r**2 * (D @ k1)
    mask = np.arange(len(r)) > 0
    gr_rel = rel_l2(gr_r5[mask], gr_closed[mask])

    k_current = r5.analytic_k_linear(st, zbg, D)
    st_comp = dict(st)
    st_comp['phi'] = np.asarray(phi_composite, float)
    k_composite = r5.analytic_k_linear(st_comp, zbg, D)
    dust = r5.analytic_dust_linear(st)

    current_terms = dict(symbolic)
    current_terms['AeST_K'] = k_current
    current_terms['dust'] = dust
    current_terms['AeST_J'] = np.zeros_like(r)
    current_terms['standard_bg'] = np.zeros_like(r)

    composite_terms = dict(symbolic)
    composite_terms['AeST_K'] = k_composite
    composite_terms['dust'] = dust
    composite_terms['AeST_J'] = np.zeros_like(r)
    composite_terms['standard_bg'] = np.zeros_like(r)

    cur = pointwise_metrics(current_terms)
    cmp = pointwise_metrics(composite_terms)
    idxc = cur.pop('max_epsilon_index')
    idxp = cmp.pop('max_epsilon_index')
    cur.pop('total')
    cmp.pop('total')
    cur['max_epsilon_x'] = float(np.asarray(st['x'])[idxc])
    cmp['max_epsilon_x'] = float(np.asarray(st['x'])[idxp])

    return {
        'scale_hinv_Mpc': float(scale),
        'Nr': int(nr),
        'GR_R05_vs_closed_form_relative_L2': gr_rel,
        'phi_current_vs_composite_relative_L2': rel_l2(np.asarray(st['phi'])[mask], np.asarray(phi_composite)[mask]),
        'K_current_vs_composite_relative_L2': rel_l2(k_current[mask], k_composite[mask]),
        'current_route': cur,
        'composite_first_diagnostic_route': cmp,
    }


def fourier_audit(ks, h, tv, qbg, kqbg):
    k = np.asarray(ks, float)
    G = -2.0 * k**2 * (b4.H_DIRECT * np.asarray(tv['Psi'], float) + np.asarray(tv['Phi_prime'], float) / b4.AI)
    represented_density = b4.VAR_B * np.asarray(tv['theta_b'], float) + qbg * kqbg * np.asarray(tv['theta_A'], float)
    M = b4.AI * represented_density
    res = G + M
    den = np.abs(G) + np.abs(M)
    floor = 1e-14 * float(np.max(den))
    eps = np.abs(res) / (den + floor)
    pi_unrepresented = 2.0 * k**2 * (b4.H_DIRECT * np.asarray(tv['Psi'], float) + np.asarray(tv['Phi_prime'], float) / b4.AI) / b4.AI - represented_density

    weighted = []
    for scale in b4.SCALES:
        target = b4.dtarg(k, scale, h)
        A = target / np.asarray(tv['delta_b'], float)
        Gw = G * A
        Mw = M * A
        Rw = res * A
        Piw = pi_unrepresented * A
        Repw = represented_density * A
        weighted.append({
            'scale_hinv_Mpc': float(scale),
            'represented_residual_over_sum_L2': float(l2(Rw) / max(l2(Gw) + l2(Mw), 1e-300)),
            'unrepresented_momentum_over_represented_L2': float(l2(Piw) / max(l2(Repw), 1e-300)),
        })

    return {
        'max_epsilon_0i': float(np.max(eps)),
        'median_epsilon_0i': float(np.median(eps)),
        'min_epsilon_0i': float(np.min(eps)),
        'inherited_limit': FOURIER_ENVELOPE,
        'weighted_scales': weighted,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trace', required=True)
    ap.add_argument('--coverage-json', required=True)
    ap.add_argument('--official-npz', required=True)
    ap.add_argument('--parent-json', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    cov = json.loads(Path(args.coverage_json).read_text())
    parent = json.loads(Path(args.parent_json).read_text())
    official = np.load(args.official_npz)

    parent_ok = bool(
        parent.get('classification') == 'NL1C7B4_REPAIR06_ANALYTIC_LEADING_ORDER_INTERFACE_MISMATCH'
        and parent.get('summary', {}).get('n_cases') == 81
        and parent.get('claim_boundary', {}).get('repair05_primary_evaluator_modified') is False
    )
    ks, gs = b4.groups(b4.read_trace(args.trace))
    tv = b4.at_ai(gs)
    h = float(cov['h'])
    provenance_ok = bool(
        cov.get('classification') == 'NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('n_native_times') == 179
        and len(ks) == 128
        and abs(float(cov.get('a_i')) - b4.AI) < 1e-15
        and parent_ok
    )

    kqbg = float(np.median(tv['KQ']))
    qbg = b4.stable_q_from_kq(kqbg)
    zbg = r5.stable_zbg(kqbg)

    maxrep = 0.0
    states = {}
    for scale in b4.SCALES:
        st = b4.make_state(scale, 256, ks, h, tv)
        states[(scale, 256)] = st
        for key, val in st.items():
            okey = f's{int(scale)}_{key}'
            if okey in official.files:
                maxrep = max(maxrep, b4.rel(np.asarray(val), np.asarray(official[okey])))
        states[(scale, 512)] = b4.make_state(scale, 512, ks, h, tv)
    state_ok = bool(maxrep <= STATE_LIMIT)

    ksym = symbolic_k_shift_audit()
    comp = composite_trace_audit(gs, ks, tv)
    comp_native_ok = bool(
        comp['native_identity_relative_L2'] <= ALGEBRA_LIMIT
        and comp['composite_first_vs_theta_at_ai_relative_L2'] <= ALGEBRA_LIMIT
    )

    jac, _ = r5.build_analytic_momentum_jacobians()
    radial = []
    for scale in b4.SCALES:
        for nr in RADIAL_RESOLUTIONS:
            phi_comp = reconstruct_composite_phi(scale, nr, ks, h, tv, comp['composite_ai'])
            radial.append(radial_case(states[(scale, nr)], phi_comp, scale, nr, qbg, zbg, jac))
    gr_ok = bool(all(row['GR_R05_vs_closed_form_relative_L2'] <= ALGEBRA_LIMIT for row in radial))

    fourier = fourier_audit(ks, h, tv, qbg, kqbg)
    fourier_ok = bool(fourier['max_epsilon_0i'] <= FOURIER_ENVELOPE)
    finite = bool(
        np.isfinite(maxrep)
        and all(np.isfinite(v) for v in [
            comp['native_identity_relative_L2'],
            comp['composite_first_vs_theta_at_ai_relative_L2'],
            comp['current_componentwise_vs_composite_first_at_ai_relative_L2'],
            fourier['max_epsilon_0i'],
        ])
        and all(np.isfinite(row['current_route']['global_L2_ratio']) and np.isfinite(row['composite_first_diagnostic_route']['global_L2_ratio']) for row in radial)
    )

    implementation_ok = bool(provenance_ok and state_ok and ksym['pass'] and comp_native_ok and gr_ok and finite)
    if not implementation_ok:
        classification = 'NL1C7B4_REPAIR07_IMPLEMENTATION_FAIL'
        rc = 2
    elif fourier_ok:
        classification = 'NL1C7B4_REPAIR07_COVARIANT_FOURIER_BRIDGE_DIAGNOSTIC_PASS'
        rc = 0
    else:
        classification = 'NL1C7B4_REPAIR07_COVARIANT_FOURIER_INTERFACE_MISMATCH'
        rc = 0

    comp_public = {k: v for k, v in comp.items() if not isinstance(v, np.ndarray)}
    result = {
        'classification': classification,
        'scope': 'Read-only covariant/Fourier momentum bridge audit of the frozen eta=0 C7A state; composite-first scalar path is diagnostic only and no state artifact is replaced.',
        'parent': {
            'repair06_run': 35227370644,
            'repair06_head': '630023a976d8a6e5aa0eb5a349ae56750dd8a376',
            'repair06_artifact': 10500046102,
            'repair06_artifact_sha256': 'b589d1f595782d793cdcc0f6cde1de1e4df1994b32f27ac64ee253fd665b4b1d',
            'repair05_evaluator_blob': '34fd22c73171fce5e32920a94d71d05de61521f6',
            'b4_evaluator_blob': '8559120dc273be3174eca130ca313ed6ff5acb25',
        },
        'locks': {
            'eta': 0.0,
            'scales_hinv_Mpc': list(b4.SCALES),
            'radial_resolutions': list(RADIAL_RESOLUTIONS),
            'state_reproduction_limit': STATE_LIMIT,
            'algebra_identity_limit': ALGEBRA_LIMIT,
            'inherited_C7A_fourier_envelope': FOURIER_ENVELOPE,
            'B4_raw_constraint_limit_unchanged': 1e-7,
            'Repair05_06_linear_interface_limit_unchanged': 1e-5,
        },
        'state_reproduction': {'max_relative_L2': maxrep, 'limit': STATE_LIMIT, 'pass': state_ok},
        'symbolic_K_shift': ksym,
        'scalar_composite': comp_public,
        'GR_closed_form_pass': gr_ok,
        'radial_diagnostics': radial,
        'fourier_0i': fourier,
        'gates': {
            'R7_G1_provenance_and_immutability': bool(provenance_ok and state_ok),
            'R7_G2_exact_covariant_identities': bool(ksym['pass'] and gr_ok),
            'R7_G3_exact_native_scalar_composite': comp_native_ok,
            'R7_G4_inherited_C7A_fourier_interface_envelope': fourier_ok,
            'R7_G5_no_post_result_repair': True,
        },
        'claim_boundary': {
            'official_C7A_NPZ_modified': False,
            'new_state_NPZ_written': False,
            'composite_first_route_used_as_diagnostic_only': True,
            'coefficient_fitted': False,
            'sign_flipped': False,
            'standard_sector_source_fitted_or_inserted': False,
            'radial_points_removed_from_B4_metric': False,
            'historical_threshold_changed': False,
            'repair05_primary_evaluator_modified': False,
            'nonlinear_evolution_executed': False,
            'finite_eta_executed': False,
            'B4_pass_claimed': False,
        },
        'continuation': 'A diagnostic PASS licenses only a separately preregistered identity-preserving numerical-representation repair of the C7A-to-B4 scalar bridge. The historical C7A artifact remains immutable and B4 must later be re-tested under its original gates.',
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(rc)


if __name__ == '__main__':
    main()
