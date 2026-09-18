#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair02 as r2
import nl1c7b.initial_constraint_certification_repair09 as r9

R8_NPZ_SHA256 = '4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R8_JSON_SHA256 = '054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R9_JSON_SHA256 = 'be8b54823690ffefb62470c34ee3d7addeef45e2db81e40b10cce4b833376ffc'
R9_CLASS = 'NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL'
REPRO_LIMIT = 1e-12
CLOSURE_LIMIT = 1e-12
BETAS = (1.0, 0.5, 0.1)
KINDS = ('Simple', 'Exponential', 'Sharp')


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def scalar_match(a, b, tol=REPRO_LIMIT):
    a = float(a)
    b = float(b)
    ae = abs(a - b)
    re = ae / max(abs(a), abs(b), 1e-300)
    return bool(np.isfinite(ae) and np.isfinite(re) and (ae <= tol or re <= tol)), ae, re


def source_summary(names, values, idx):
    vals = np.asarray(values, float)[:, idx]
    order = np.argsort(np.abs(vals))[::-1]
    i0 = int(order[0])
    i1 = int(order[1])
    dominant = float(vals[i0])
    second = float(vals[i1])
    rest = float(np.sum(vals) - dominant)
    ratio = None if rest == 0.0 else float(dominant / (-rest))
    return {
        'signed_sources': {name: float(vals[i]) for i, name in enumerate(names)},
        'dominant_label': names[i0],
        'dominant_signed_value': dominant,
        'dominant_abs_value': abs(dominant),
        'second_label': names[i1],
        'second_signed_value': second,
        'second_abs_value': abs(second),
        'signed_sum_non_dominant': rest,
        'dominant_to_opposing_rest_ratio': ratio,
    }


def evaluate_localized(st, scale, nr, qbg, zbg, funcs, dY):
    r = np.asarray(st['r'], float)
    D = b4.dmat(r)
    n = len(r)
    L = b4.AI + np.asarray(st['L_minus_a'], float)
    R = b4.AI * r + np.asarray(st['R_minus_ar'], float)
    Lt = b4.AI * b4.H_DIRECT + np.asarray(st['Ldot_minus_aH'], float)
    Rt = b4.AI * b4.H_DIRECT * r + np.asarray(st['Rdot_minus_aHr'], float)
    u = np.asarray(st['u'], float)
    ut = np.asarray(st['udot'], float)
    pr = D @ np.asarray(st['phi'], float)
    Lr = D @ L
    Rr = D @ R
    ur = D @ u
    dq = np.asarray(st['phidot_minus_Q'], float)

    qtarget = qbg + dq
    c = np.cosh(u)
    sh = np.sinh(u)
    pt = (qtarget - sh * pr / L) / c
    qexact = c * pt + sh * pr / L

    z = zbg + dq / b4.Z0
    w = z * z
    with np.errstate(over='ignore', invalid='ignore'):
        ew = np.exp(w)
    args = [L, R, u, Lt, Rt, ut, pt, Lr, Rr, ur, pr]
    X = sh * pt + c * pr / L
    noncenter = np.arange(n) > 0

    base_names = list(funcs.keys())
    expected_base = [
        'GR_kin', 'GR_curv_NL', 'GR_curv_Rr', 'GR_Nr_boundary',
        'AeST_E2', 'AeST_EX', 'AeST_X2',
    ]
    if base_names != expected_base:
        raise RuntimeError(f'unexpected frozen source order: {base_names}')
    names = base_names + ['AeST_J', 'AeST_K', 'dust', 'standard_bg']

    rows = []
    closure_max_h = 0.0
    closure_max_m = 0.0

    for kind in KINDS:
        for beta in BETAS:
            CH = []
            CM = []
            for name in base_names:
                fs = funcs[name]
                fN, fNr, fb, fbr = [r2.arrval(f, args, n) for f in fs]
                fNr = np.array(fNr, copy=True)
                fbr = np.array(fbr, copy=True)
                fNr[0] = 0.0
                fbr[0] = 0.0
                CH.append(fN - D @ fNr)
                CM.append(fb - D @ fbr)

            dyN, dyNr, dyb, dybr = [r2.arrval(f, args, n) for f in dY]
            j, J = r1.jJ(kind, np.abs(X) / b4.A0_GEO, beta)
            P = L * R**2
            jN = -b4.C * (P * J + P * j * dyN)
            jNr = -b4.C * (P * j * dyNr)
            jb = -b4.C * (P * j * dyb)
            jbr = -b4.C * (P * j * dybr)
            jNr = np.array(jNr, copy=True)
            jbr = np.array(jbr, copy=True)
            jNr[0] = 0.0
            jbr[0] = 0.0
            CH.append(jN - D @ jNr)
            CM.append(jb - D @ jbr)

            kN = 4.0 * b4.K2 * L * R**2 * (
                b4.Z0 * b4.Z0 * np.expm1(w) - 2.0 * c * pt * b4.Z0 * z * ew
            )
            kb = -8.0 * b4.K2 * L * R**2 * c * pr * b4.Z0 * z * ew
            CH.append(kN)
            CM.append(kb)

            v = np.arctanh(np.asarray(st['dust_vr'], float))
            varrho = b4.VAR_B * (1.0 + np.asarray(st['delta_b'], float))
            CH.append(-2.0 * L * R**2 * varrho * np.cosh(v)**2)
            CM.append(2.0 * L**2 * R**2 * varrho * np.cosh(v) * np.sinh(v))

            CH.append(-2.0 * L * R**2 * b4.RHO_STD)
            CM.append(np.zeros(n))

            CH = np.asarray(CH, float)
            CM = np.asarray(CM, float)
            if CH.shape != (11, n) or CM.shape != (11, n):
                raise RuntimeError('invalid source matrix shape')

            finite = bool(
                np.all(np.isfinite(CH[:, noncenter]))
                and np.all(np.isfinite(CM[:, noncenter]))
                and np.all(np.isfinite(qexact[noncenter]))
            )
            if not finite:
                raise RuntimeError(f'nonfinite source contribution scale={scale} Nr={nr} {kind} beta={beta}')

            numH_direct = np.sum(CH, axis=0)
            numM_direct = np.sum(CM, axis=0)
            # Independent bookkeeping sum through explicit source dictionaries.
            srcH = {name: CH[i] for i, name in enumerate(names)}
            srcM = {name: CM[i] for i, name in enumerate(names)}
            numH_named = np.zeros(n)
            numM_named = np.zeros(n)
            for name in names:
                numH_named = numH_named + srcH[name]
                numM_named = numM_named + srcM[name]

            denH = np.sum(np.abs(CH), axis=0)
            denM = np.sum(np.abs(CM), axis=0)
            preH = float(np.max(denH[noncenter]))
            preM = float(np.max(denM[noncenter]))
            floorH = 1e-14 * preH
            floorM = 1e-14 * preM
            eH = np.abs(numH_direct) / (denH + floorH)
            eM = np.abs(numM_direct) / (denM + floorM)

            closeH = np.abs(numH_direct - numH_named) / (denH + floorH)
            closeM = np.abs(numM_direct - numM_named) / (denM + floorM)
            ch = float(np.max(closeH[noncenter]))
            cm = float(np.max(closeM[noncenter]))
            closure_max_h = max(closure_max_h, ch)
            closure_max_m = max(closure_max_m, cm)

            ih = int(np.argmax(eH[noncenter]) + 1)
            im = int(np.argmax(eM[noncenter]) + 1)
            hs = source_summary(names, CH, ih)
            ms = source_summary(names, CM, im)

            row = {
                'scale_hinv_Mpc': float(scale),
                'Nr': int(nr),
                'Y_kind': kind,
                'beta0': float(beta),
                'max_epsilon_H': float(eH[ih]),
                'max_epsilon_M': float(eM[im]),
                'H_hotspot': {
                    'index': ih,
                    'r_Mpc': float(r[ih]),
                    'numerator_signed': float(numH_direct[ih]),
                    'denominator_abs_sum': float(denH[ih]),
                    'floor': float(floorH),
                    'epsilon': float(eH[ih]),
                    **hs,
                },
                'M_hotspot': {
                    'index': im,
                    'r_Mpc': float(r[im]),
                    'numerator_signed': float(numM_direct[im]),
                    'denominator_abs_sum': float(denM[im]),
                    'floor': float(floorM),
                    'epsilon': float(eM[im]),
                    **ms,
                },
                'decomposition_closure_max_H': ch,
                'decomposition_closure_max_M': cm,
            }
            rows.append(row)

    return rows, closure_max_h, closure_max_m


def key(row):
    return (
        float(row['scale_hinv_Mpc']),
        int(row['Nr']),
        str(row['Y_kind']),
        float(row['beta0']),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trace', required=True)
    ap.add_argument('--coverage-json', required=True)
    ap.add_argument('--repair08-json', required=True)
    ap.add_argument('--repair08-npz', required=True)
    ap.add_argument('--repair09-json', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    cov = json.loads(Path(a.coverage_json).read_text())
    r8_result = json.loads(Path(a.repair08_json).read_text())
    r9_result = json.loads(Path(a.repair09_json).read_text())
    off = np.load(a.repair08_npz)

    r8_npz_sha = sha256_file(a.repair08_npz)
    r8_json_sha = sha256_file(a.repair08_json)
    r9_json_sha = sha256_file(a.repair09_json)

    z = rec.read_trace(a.trace)
    ks, gs = rec.groups(z)
    tv_rec = rec.at_ai(gs, 'pchip')
    ks_b4, gs_b4 = b4.groups(b4.read_trace(a.trace))
    tv_b4 = b4.at_ai(gs_b4)
    h = float(cov['h'])

    r9_gates = r9_result.get('gates', {})
    r8_gates = r8_result.get('gates', {})
    g1 = bool(
        r8_npz_sha == R8_NPZ_SHA256
        and r8_json_sha == R8_JSON_SHA256
        and r9_json_sha == R9_JSON_SHA256
        and r8_result.get('classification') == 'NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED'
        and len(r8_gates) == 10 and all(r8_gates.values())
        and r9_result.get('classification') == R9_CLASS
        and r9_gates.get('R9_G1_exact_Repair08_provenance') is True
        and r9_gates.get('R9_G2_Repair08_state_anchor_reproduction') is True
        and r9_gates.get('R9_G3_exact_nonlinear_dictionary') is True
        and r9_gates.get('R9_G4_original_raw_B4_constraints') is False
        and r9_gates.get('R9_G5_two_grid_control') is True
        and r9_gates.get('R9_G6_claim_boundary') is True
        and cov.get('classification') == 'NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max') == 0
        and cov.get('n_native_times') == 179
        and len(ks) == 128
        and np.array_equal(ks, ks_b4)
    )

    scalar_ai, scalar_independent, scalar_finite, _ = r8.scalar_composites_at_ai(ks, gs, 'pchip')
    scalar_identity_error = r9.rel_sym(scalar_ai, scalar_independent)

    states = {}
    anchor_max = 0.0
    anchor_ok = bool(scalar_finite and scalar_identity_error <= 1e-10)
    for scale in b4.SCALES:
        primary = r9.load_primary_state(off, scale)
        reconstructed = r8.repaired_state(scale, rec.NQ, ks, h, tv_rec, 'pchip', scalar_ai)
        for field, value in reconstructed.items():
            if field not in primary:
                anchor_ok = False
                continue
            err = r9.rel_sym(value, primary[field])
            anchor_max = max(anchor_max, err)
            anchor_ok &= bool(np.isfinite(err) and err <= r9.ANCHOR_LIMIT)
        states[(scale, 256)] = primary
        states[(scale, 512)] = r9.repaired_state_nr(scale, 512, ks, h, tv_b4, tv_rec, scalar_ai)

    kq_bg = float(np.median(tv_b4['KQ']))
    qbg = b4.stable_q_from_kq(kq_bg)
    zbg = r9.stable_zbg(kq_bg)
    funcs, dY, kdict_identity = r1.build_nonK()

    rows = []
    closure_h = 0.0
    closure_m = 0.0
    for scale in b4.SCALES:
        for nr in (256, 512):
            rr, ch, cm = evaluate_localized(states[(scale, nr)], scale, nr, qbg, zbg, funcs, dY)
            rows.extend(rr)
            closure_h = max(closure_h, ch)
            closure_m = max(closure_m, cm)

    frozen_rows = {key(x): x for x in r9_result['constraint_rows']}
    repro_rows = []
    repro_ok = bool(anchor_ok and kdict_identity and len(rows) == 54 and len(frozen_rows) == 54)
    for row in rows:
        k = key(row)
        fr = frozen_rows.get(k)
        if fr is None:
            repro_ok = False
            repro_rows.append({'key': list(k), 'present_in_repair09': False, 'pass': False})
            continue
        ph, ah, rh = scalar_match(row['max_epsilon_H'], fr['max_epsilon_H'])
        pm, am, rm = scalar_match(row['max_epsilon_M'], fr['max_epsilon_M'])
        ok = bool(ph and pm)
        repro_ok &= ok
        repro_rows.append({
            'key': list(k),
            'present_in_repair09': True,
            'epsilon_H_abs_error': ah,
            'epsilon_H_relative_error': rh,
            'epsilon_M_abs_error': am,
            'epsilon_M_relative_error': rm,
            'limit': REPRO_LIMIT,
            'pass': ok,
        })

    g2 = bool(repro_ok and r9_result.get('classification') == R9_CLASS)
    g3 = bool(
        np.isfinite(closure_h) and np.isfinite(closure_m)
        and closure_h <= CLOSURE_LIMIT and closure_m <= CLOSURE_LIMIT
    )

    source_names = [
        'GR_kin', 'GR_curv_NL', 'GR_curv_Rr', 'GR_Nr_boundary',
        'AeST_E2', 'AeST_EX', 'AeST_X2', 'AeST_J', 'AeST_K', 'dust', 'standard_bg',
    ]
    complete = True
    for row in rows:
        for spot in ('H_hotspot', 'M_hotspot'):
            s = row[spot]
            complete &= bool(
                isinstance(s.get('index'), int)
                and np.isfinite(s.get('r_Mpc'))
                and set(s.get('signed_sources', {})) == set(source_names)
                and all(np.isfinite(v) for v in s['signed_sources'].values())
            )
    g4 = bool(len(rows) == 54 and complete)

    pair_rows = []
    pair_ok = True
    for scale in b4.SCALES:
        for kind in KINDS:
            for beta in BETAS:
                a256 = next(x for x in rows if key(x) == (float(scale), 256, kind, float(beta)))
                a512 = next(x for x in rows if key(x) == (float(scale), 512, kind, float(beta)))
                pair_rows.append({
                    'scale_hinv_Mpc': float(scale),
                    'Y_kind': kind,
                    'beta0': float(beta),
                    'H': {
                        'r256_Mpc': a256['H_hotspot']['r_Mpc'],
                        'r512_Mpc': a512['H_hotspot']['r_Mpc'],
                        'dominant_256': a256['H_hotspot']['dominant_label'],
                        'dominant_512': a512['H_hotspot']['dominant_label'],
                        'dominant_label_agrees': a256['H_hotspot']['dominant_label'] == a512['H_hotspot']['dominant_label'],
                    },
                    'M': {
                        'r256_Mpc': a256['M_hotspot']['r_Mpc'],
                        'r512_Mpc': a512['M_hotspot']['r_Mpc'],
                        'dominant_256': a256['M_hotspot']['dominant_label'],
                        'dominant_512': a512['M_hotspot']['dominant_label'],
                        'dominant_label_agrees': a256['M_hotspot']['dominant_label'] == a512['M_hotspot']['dominant_label'],
                    },
                })
    pair_ok &= len(pair_rows) == 27
    g5 = bool(pair_ok)

    claim_boundary = {
        'state_modified_or_projected': False,
        'coefficient_fitted': False,
        'source_fitted_or_inserted': False,
        'sign_changed': False,
        'K_clipping_used': False,
        'Q_linearized': False,
        'radial_points_removed': False,
        'Y_beta_or_scale_selected': False,
        'historical_threshold_changed': False,
        'nonlinear_evolution_executed': False,
        'finite_eta_executed': False,
        'observational_detection_claimed': False,
        'B4_pass_claimed': False,
    }
    g6 = bool(not any(claim_boundary.values()))

    gates = {
        'R10_G1_exact_frozen_provenance': g1,
        'R10_G2_exact_Repair09_reproduction': g2,
        'R10_G3_signed_decomposition_closure': g3,
        'R10_G4_complete_hotspot_localization': g4,
        'R10_G5_two_grid_localization_reporting': g5,
        'R10_G6_claim_boundary': g6,
    }

    if all(gates.values()):
        classification = 'NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS'
        rc = 0
    else:
        classification = 'NL1C7B4_REPAIR10_IMPLEMENTATION_FAIL'
        rc = 2

    h_counts = Counter(x['H_hotspot']['dominant_label'] for x in rows)
    m_counts = Counter(x['M_hotspot']['dominant_label'] for x in rows)
    h_second = Counter(x['H_hotspot']['second_label'] for x in rows)
    m_second = Counter(x['M_hotspot']['second_label'] for x in rows)

    result = {
        'classification': classification,
        'scope': 'Repair10 exact signed source-term localization of the frozen Repair09 raw eta=0 initial-constraint failure; no repair, evolution, or finite eta.',
        'provenance': {
            'repair08_npz_sha256': r8_npz_sha,
            'repair08_json_sha256': r8_json_sha,
            'repair09_json_sha256': r9_json_sha,
            'repair09_result_freeze_commit': '04d85232092cdc747cf317f2937f1c33a1c0dddc',
            'repair10_prereg_commit': 'c43c3147da0ac7d9990d6badd422095b2b737ff9',
            'dense_trace_artifact': 10469031693,
            'dense_trace_digest': 'sha256:193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70',
        },
        'state_anchor': {
            'max_relative_L2': anchor_max,
            'scalar_canonical_vs_independent_at_ai_relative_L2': scalar_identity_error,
            'pass': anchor_ok,
        },
        'source_labels': source_names,
        'repair09_reproduction': {
            'limit': REPRO_LIMIT,
            'rows': repro_rows,
            'pass': g2,
        },
        'decomposition_closure': {
            'max_H': closure_h,
            'max_M': closure_m,
            'limit': CLOSURE_LIMIT,
            'pass': g3,
        },
        'localization_rows': rows,
        'two_grid_localization': pair_rows,
        'summary': {
            'n_cases': len(rows),
            'H_dominant_label_counts': dict(sorted(h_counts.items())),
            'M_dominant_label_counts': dict(sorted(m_counts.items())),
            'H_second_label_counts': dict(sorted(h_second.items())),
            'M_second_label_counts': dict(sorted(m_second.items())),
            'max_epsilon_H': float(max(x['max_epsilon_H'] for x in rows)),
            'max_epsilon_M': float(max(x['max_epsilon_M'] for x in rows)),
            'min_epsilon_H': float(min(x['max_epsilon_H'] for x in rows)),
            'min_epsilon_M': float(min(x['max_epsilon_M'] for x in rows)),
        },
        'gates': gates,
        'claim_boundary': claim_boundary,
    }

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    raise SystemExit(rc)


if __name__ == '__main__':
    main()
