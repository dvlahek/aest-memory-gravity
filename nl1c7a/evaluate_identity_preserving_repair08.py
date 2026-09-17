#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

import nl1c7a.a6_a10_spherical_reconstruction as rec

IDENTITY_LIMIT = 1e-10
REGRESSION_LIMIT = 1e-12
META_LIMIT = 1e-15


def rel_sym(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(a), np.linalg.norm(b), 1e-300))


def interp_at_ai(x, y, method):
    x0 = math.log(rec.AI)
    if not x[0] < x0 < x[-1]:
        raise RuntimeError('a_i not bracketed')
    if method == 'pchip':
        return float(PchipInterpolator(x, y)(x0))
    if method == 'linear':
        return float(np.interp(x0, x, y))
    raise ValueError(method)


def scalar_composites_at_ai(ks, gs, method):
    theta_route = []
    chi_route = []
    native_finite = True
    cancellation = []
    for kval, g in zip(ks, gs):
        names = tuple(g.dtype.names or ())
        if 'theta_A' not in names:
            raise RuntimeError('retained dense trace has no theta_A column')
        a = np.asarray(g['a'], float)
        x = np.log(a)
        Q = np.asarray(g['Q'], float)
        theta = np.asarray(g['theta_A'], float)
        chi = np.asarray(g['chi'], float)
        alpha = np.asarray(g['alpha_A'], float)
        theta_native = a * Q * theta / (float(kval) ** 2)
        chi_native = chi - Q * alpha
        native_finite &= bool(np.all(np.isfinite(theta_native)) and np.all(np.isfinite(chi_native)))
        theta_route.append(interp_at_ai(x, theta_native, method))
        chi_route.append(interp_at_ai(x, chi_native, method))

        chi_i = interp_at_ai(x, chi, method)
        q_i = interp_at_ai(x, Q, method)
        alpha_i = interp_at_ai(x, alpha, method)
        d_i = chi_i - q_i * alpha_i
        cancellation.append((abs(chi_i) + abs(q_i * alpha_i)) / max(abs(d_i), 1e-300))

    theta_route = np.asarray(theta_route, float)
    chi_route = np.asarray(chi_route, float)
    return theta_route, chi_route, bool(native_finite), np.asarray(cancellation, float)


def repaired_state(scale, nq, ks, h, tv, k_method, scalar_ai):
    # Reuse the frozen certified C7A construction for every unchanged quantity.
    st = rec.make_state(scale, nq, ks, h, tv, k_method)

    k = np.geomspace(ks[0], ks[-1], nq)
    target = rec.dtarg(k, scale, h)
    ratio = np.asarray(scalar_ai, float) / np.asarray(tv['delta_b'], float)
    Fphi = rec.ik(ks, ratio, k, k_method) * target
    phi = rec.inv(k, Fphi, np.asarray(st['r'], float))

    st['phi'] = phi
    Q = float(np.median(tv['Q']))
    st['X_from_state'] = Q * np.asarray(st['u'], float) + np.gradient(
        phi, np.asarray(st['r'], float), edge_order=2
    ) / rec.AI
    return st


def state_control_rows(primary, control, scale):
    rows = []
    ok = True
    for field in rec.STATE:
        n = float(np.linalg.norm(np.asarray(primary[field], float)))
        zero = n <= rec.ZERO
        diff = None if zero else rec.rel(np.asarray(primary[field]), np.asarray(control[field]))
        passed = bool(zero or (np.isfinite(diff) and diff <= rec.REL))
        rows.append({
            'scale': float(scale),
            'field': field,
            'norm': n,
            'zero_norm_excluded': bool(zero),
            'relative_difference': diff,
            'limit': rec.REL,
            'pass': passed,
        })
        ok &= passed
    return rows, bool(ok)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trace', required=True)
    ap.add_argument('--coverage-json', required=True)
    ap.add_argument('--a5-json', required=True)
    ap.add_argument('--official-npz', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--state-npz', required=True)
    args = ap.parse_args()

    out_path = Path(args.out)
    state_path = Path(args.state_npz)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    if state_path.exists():
        state_path.unlink()

    cov = json.loads(Path(args.coverage_json).read_text())
    a5 = json.loads(Path(args.a5_json).read_text())
    official = np.load(args.official_npz)

    repair_meta = cov.get('repair01', {})
    coverage_ok = bool(
        cov.get('classification') == 'NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and all(cov.get('gates', {}).values())
        and cov.get('requested_k_relative_miss_max') == 0
        and cov.get('n_native_times') == 179
        and abs(float(cov.get('a_i')) - rec.AI) <= META_LIMIT
        and repair_meta.get('source_sampling_only') is True
        and repair_meta.get('perturbations_sampling_stepsize') == 0.025
        and repair_meta.get('perturbations_integration_stepsize_overridden') is False
        and repair_meta.get('integration_tolerance_overridden') is False
        and repair_meta.get('interpolation_used') is False
        and repair_meta.get('nearest_neighbour_substitution_used') is False
    )

    z = rec.read_trace(args.trace)
    ks, gs = rec.groups(z)
    h = float(cov['h'])
    exact_grid_ok = bool(len(ks) == 128 and np.all(np.isfinite(ks)) and np.all(np.diff(ks) > 0))

    metadata_ok = bool(
        'a_i' in official.files
        and 'scales_hinv_Mpc' in official.files
        and 'k_grid_Mpc_inv' in official.files
        and 'h' in official.files
        and abs(float(np.asarray(official['a_i'])) - rec.AI) <= META_LIMIT
        and rel_sym(np.asarray(official['scales_hinv_Mpc']), np.asarray(rec.SCALES, float)) <= META_LIMIT
        and rel_sym(np.asarray(official['k_grid_Mpc_inv']), np.asarray(ks, float)) <= META_LIMIT
        and abs(float(np.asarray(official['h'])) - h) <= META_LIMIT
    )
    g1 = bool(coverage_ok and exact_grid_ok and metadata_ok)

    g2 = bool(
        a5.get('classification') == 'NL1C7A_A5_FINITE_GROWING_MODE_DENOMINATOR_PASS'
        and all(a5.get('gates', {}).values())
    )

    tp = rec.at_ai(gs, 'pchip')
    tl = rec.at_ai(gs, 'linear')
    phi_p, phi_chi_p, native_finite_p, cancellation = scalar_composites_at_ai(ks, gs, 'pchip')
    phi_l, phi_chi_l, native_finite_l, _ = scalar_composites_at_ai(ks, gs, 'linear')

    componentwise = np.asarray(tp['chi'], float) - np.asarray(tp['Q'], float) * np.asarray(tp['alpha_A'], float)
    identity_error = rel_sym(phi_p, phi_chi_p)
    identity_linear_error = rel_sym(phi_l, phi_chi_l)
    componentwise_difference = rel_sym(componentwise, phi_p)
    scalar_finite = bool(
        native_finite_p and native_finite_l
        and np.all(np.isfinite(phi_p)) and np.all(np.isfinite(phi_chi_p))
        and np.all(np.isfinite(phi_l)) and np.all(np.isfinite(phi_chi_l))
    )
    g3 = bool(scalar_finite and identity_error <= IDENTITY_LIMIT)

    primary_states = {}
    time_rows = []
    k_rows = []
    a8_rows = []
    a9_rows = []
    g4 = g5 = g6 = g7 = True

    for scale in rec.SCALES:
        primary = repaired_state(scale, rec.NQ, ks, h, tp, 'pchip', phi_p)
        time_control = repaired_state(scale, rec.NQ, ks, h, tl, 'pchip', phi_l)
        k_control = repaired_state(scale, rec.NQ, ks, h, tp, 'linear', phi_p)
        primary_states[scale] = primary

        rows, ok = state_control_rows(primary, time_control, scale)
        time_rows.extend(rows)
        g4 &= ok

        rows, ok = state_control_rows(primary, k_control, scale)
        k_rows.extend(rows)
        g5 &= ok

        x256, e256 = rec.a8(scale, rec.NQ, ks[0], ks[-1], h)
        x512, e512 = rec.a8(scale, rec.NQC, ks[0], ks[-1], h)
        mismatch = rec.rel(x512, x256)
        ok8 = bool(e256 <= rec.TARG and e512 <= rec.TARG and mismatch <= rec.TARG)
        a8_rows.append({
            'scale': float(scale),
            'error_256': e256,
            'error_512': e512,
            'mismatch_256_512': mismatch,
            'limit': rec.TARG,
            'pass': ok8,
        })
        g6 &= ok8

        xerr = rec.rel(np.asarray(primary['X_from_chi']), np.asarray(primary['X_from_state']))
        eerr = rec.rel(np.asarray(primary['E_from_class']), np.asarray(primary['E_from_state']))
        ok9 = bool(np.isfinite(xerr) and np.isfinite(eerr) and xerr <= rec.BRIDGE and eerr <= rec.BRIDGE)
        a9_rows.append({
            'scale': float(scale),
            'X_relative_error': xerr,
            'E_relative_error': eerr,
            'limit': rec.BRIDGE,
            'pass': ok9,
        })
        g7 &= ok9

    source_audit = rec.audit_source(__file__)
    g8 = bool(all(source_audit.values()))

    regression_rows = []
    scalar_change_rows = []
    g9 = True
    for scale in rec.SCALES:
        tag = str(int(scale))
        st = primary_states[scale]
        for key, val in st.items():
            old_key = f's{tag}_{key}'
            if old_key not in official.files:
                regression_rows.append({'scale': float(scale), 'field': key, 'present_in_parent': False, 'pass': False})
                g9 = False
                continue
            err = rel_sym(np.asarray(val), np.asarray(official[old_key]))
            if key in {'phi', 'X_from_state'}:
                scalar_change_rows.append({
                    'scale': float(scale), 'field': key,
                    'relative_L2_vs_historical_C7A': err,
                    'gated_toward_historical_value': False,
                })
            else:
                passed = bool(np.isfinite(err) and err <= REGRESSION_LIMIT)
                regression_rows.append({
                    'scale': float(scale), 'field': key,
                    'present_in_parent': True,
                    'relative_L2': err,
                    'limit': REGRESSION_LIMIT,
                    'pass': passed,
                })
                g9 &= passed

    claim_boundary = {
        'historical_C7A_NPZ_overwritten': False,
        'new_state_NPZ_written_only_if_certified': True,
        'physical_coefficient_changed': False,
        'coefficient_fitted': False,
        'source_fitted_or_inserted': False,
        'sign_flipped': False,
        'clipping_used': False,
        'radial_points_removed': False,
        'historical_threshold_changed': False,
        'nonlinear_evolution_executed': False,
        'finite_eta_executed': False,
        'B4_pass_claimed': False,
        'observational_detection_claimed': False,
    }
    g10 = bool(
        not claim_boundary['historical_C7A_NPZ_overwritten']
        and not claim_boundary['physical_coefficient_changed']
        and not claim_boundary['coefficient_fitted']
        and not claim_boundary['source_fitted_or_inserted']
        and not claim_boundary['sign_flipped']
        and not claim_boundary['clipping_used']
        and not claim_boundary['radial_points_removed']
        and not claim_boundary['historical_threshold_changed']
        and not claim_boundary['nonlinear_evolution_executed']
        and not claim_boundary['finite_eta_executed']
        and not claim_boundary['B4_pass_claimed']
    )

    finite = bool(
        np.isfinite(identity_error)
        and np.isfinite(identity_linear_error)
        and np.isfinite(componentwise_difference)
        and all(np.isfinite(r['relative_difference']) for r in time_rows if r['relative_difference'] is not None)
        and all(np.isfinite(r['relative_difference']) for r in k_rows if r['relative_difference'] is not None)
    )

    if not (g1 and g2 and g10 and finite):
        classification = 'NL1C7A_REPAIR08_IMPLEMENTATION_FAIL'
    elif not g3:
        classification = 'NL1C7A_REPAIR08_SCALAR_IDENTITY_FAIL'
    elif not g4:
        classification = 'NL1C7A_REPAIR08_TIME_INTERPOLATION_CONTROL_FAIL'
    elif not g5:
        classification = 'NL1C7A_REPAIR08_K_INTERPOLATION_CONTROL_FAIL'
    elif not g6:
        classification = 'NL1C7A_REPAIR08_RECONSTRUCTION_FAIL'
    elif not g7:
        classification = 'NL1C7A_REPAIR08_BRIDGE_IDENTITY_FAIL'
    elif not g8:
        classification = 'NL1C7A_REPAIR08_FREE_MODE_INJECTION_FAIL'
    elif not g9:
        classification = 'NL1C7A_REPAIR08_STATE_REGRESSION_FAIL'
    else:
        classification = 'NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED'

    certified = classification == 'NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED'
    if certified:
        arrays = {}
        for scale in rec.SCALES:
            tag = str(int(scale))
            for key, val in primary_states[scale].items():
                arrays[f's{tag}_{key}'] = np.asarray(val)
        arrays['a_i'] = np.asarray(rec.AI)
        arrays['scales_hinv_Mpc'] = np.asarray(rec.SCALES, float)
        arrays['k_grid_Mpc_inv'] = np.asarray(ks, float)
        arrays['h'] = np.asarray(h)
        np.savez_compressed(state_path, **arrays)

    gates = {
        'R8_G1_provenance_and_retained_inputs': g1,
        'R8_G2_A5_denominator_recheck': g2,
        'R8_G3_identity_preserving_scalar_construction': g3,
        'R8_G4_A6_time_interpolation_control': bool(g4),
        'R8_G5_A7_k_interpolation_control': bool(g5),
        'R8_G6_A8_target_profile_reconstruction': bool(g6),
        'R8_G7_A9_bridge_identities': bool(g7),
        'R8_G8_A10_no_free_mode_injection': g8,
        'R8_G9_unchanged_state_regression': bool(g9),
        'R8_G10_claim_boundary': g10,
    }

    active_time = [r for r in time_rows if not r['zero_norm_excluded']]
    active_k = [r for r in k_rows if not r['zero_norm_excluded']]
    reg_active = [r for r in regression_rows if r.get('present_in_parent')]

    result = {
        'classification': classification,
        'scope': 'C7A Repair08 eta=0 identity-preserving scalar initial-state representation only; no B4 certification, nonlinear evolution, finite eta, or observable claim.',
        'parent': {
            'repair07b_freeze_commit': 'c32c77940b5a338fd6ca42f7251b3a1b57927fb7',
            'repair07b_freeze_blob': 'fa0d38dcce6902b224c8d5055a883ad163dab5bd',
            'certified_C7A_artifact': 10481526695,
            'certified_C7A_artifact_sha256': 'c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c',
            'dense_trace_artifact': 10469031693,
            'dense_trace_artifact_sha256': '193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70',
        },
        'settings': {
            'a_i': rec.AI,
            'eta': 0.0,
            'scales_hinv_Mpc': list(rec.SCALES),
            'quadrature_primary': rec.NQ,
            'quadrature_control': rec.NQC,
            'radial_points': rec.NX,
            'A6_A7_limit': rec.REL,
            'A8_limit': rec.TARG,
            'A9_limit': rec.BRIDGE,
            'scalar_identity_limit': IDENTITY_LIMIT,
            'unchanged_state_regression_limit': REGRESSION_LIMIT,
        },
        'scalar_identity': {
            'canonical_route': 'PCHIP(log(a), a*Q*theta_A/k^2 formed on each native k-group)',
            'independent_route': 'PCHIP(log(a), chi-Q*alpha_A formed on each native k-group)',
            'canonical_vs_independent_at_ai_relative_L2': identity_error,
            'linear_time_control_canonical_vs_independent_relative_L2': identity_linear_error,
            'historical_componentwise_vs_canonical_at_ai_relative_L2': componentwise_difference,
            'cancellation_condition_min': float(np.min(cancellation)),
            'cancellation_condition_median': float(np.median(cancellation)),
            'cancellation_condition_max': float(np.max(cancellation)),
            'all_native_and_interpolated_values_finite': scalar_finite,
        },
        'A5': a5,
        'A6': {
            'rows': time_rows,
            'max_active_relative_difference': max(r['relative_difference'] for r in active_time),
            'pass': bool(g4),
        },
        'A7': {
            'rows': k_rows,
            'max_active_relative_difference': max(r['relative_difference'] for r in active_k),
            'pass': bool(g5),
        },
        'A8': {
            'rows': a8_rows,
            'max_error_or_mismatch': max(max(r['error_256'], r['error_512'], r['mismatch_256_512']) for r in a8_rows),
            'pass': bool(g6),
        },
        'A9': {
            'rows': a9_rows,
            'max_bridge_relative_error': max(max(r['X_relative_error'], r['E_relative_error']) for r in a9_rows),
            'pass': bool(g7),
        },
        'A10': {'checks': source_audit, 'pass': g8},
        'unchanged_state_regression': {
            'rows': regression_rows,
            'max_relative_L2': max((r.get('relative_L2', 0.0) for r in reg_active), default=0.0),
            'allowed_scalar_changes': scalar_change_rows,
            'pass': bool(g9),
        },
        'gates': gates,
        'new_state_npz_written': bool(certified and state_path.is_file()),
        'new_state_npz_path': str(state_path),
        'claim_boundary': claim_boundary,
        'continuation': 'Only a CERTIFIED Repair08 artifact may be consumed by a separately preregistered B4 retest under the unchanged historical B4 thresholds.',
    }

    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if certified else 2)


if __name__ == '__main__':
    main()
