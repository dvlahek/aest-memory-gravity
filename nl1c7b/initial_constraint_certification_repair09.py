#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair02 as r2

NPZ_SHA256 = '4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
JSON_SHA256 = '054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
LIMIT = 1e-7
DICT_LIMIT = 1e-12
ANCHOR_LIMIT = 1e-12
GRID_RATIO_LIMIT = 2.0
BETAS = (1.0, 0.5, 0.1)
KINDS = ('Simple', 'Exponential', 'Sharp')


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def rel_sym(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return float(np.linalg.norm(a - b) / max(np.linalg.norm(a), np.linalg.norm(b), 1e-300))


def load_primary_state(npz, scale):
    prefix = f's{int(scale)}_'
    out = {k[len(prefix):]: np.asarray(npz[k], float) for k in npz.files if k.startswith(prefix)}
    required = {
        'x', 'r', 'L_minus_a', 'R_minus_ar', 'Ldot_minus_aH', 'Rdot_minus_aHr',
        'u', 'udot', 'phi', 'phidot_minus_Q', 'delta_b', 'dust_vr',
        'X_from_chi', 'X_from_state', 'E_from_class', 'E_from_state',
    }
    missing = sorted(required - set(out))
    if missing:
        raise RuntimeError(f'Repair08 NPZ missing state arrays for scale={scale}: {missing}')
    n = len(out['r'])
    if n != 256 or any(np.asarray(out[k]).shape != (n,) for k in required):
        raise RuntimeError(f'invalid Repair08 primary state shape for scale={scale}')
    return out


def repaired_state_nr(scale, nr, ks, h, tv_b4, tv_rec, scalar_ai):
    # Frozen generalized C7A constructor for all non-scalar quantities.
    st = b4.make_state(scale, nr, ks, h, tv_b4)

    # Replace only the scalar representation by the certified Repair08 route.
    k = np.geomspace(ks[0], ks[-1], rec.NQ)
    target = rec.dtarg(k, scale, h)
    ratio = np.asarray(scalar_ai, float) / np.asarray(tv_rec['delta_b'], float)
    Fphi = rec.ik(ks, ratio, k, 'pchip') * target
    phi = rec.inv(k, Fphi, np.asarray(st['r'], float))
    st['phi'] = np.asarray(phi, float)
    Q = float(np.median(tv_rec['Q']))
    st['X_from_state'] = Q * np.asarray(st['u'], float) + np.gradient(
        st['phi'], np.asarray(st['r'], float), edge_order=2
    ) / rec.AI
    return st


def stable_zbg(kq_bg):
    x = float(kq_bg) / (4.0 * b4.K2 * b4.Z0)
    if not (x > 0.0 and math.isfinite(x)):
        raise RuntimeError('invalid KQ background')
    lx = math.log(x)
    y = lx if lx > 1.0 else x * x
    for _ in range(50):
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


def evaluate_state(st, scale, nr, qbg, zbg, funcs, dY):
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

    # Frozen Repair02 exact nonlinear dictionary completion.
    qtarget = qbg + dq
    c = np.cosh(u)
    sh = np.sinh(u)
    pt = (qtarget - sh * pr / L) / c
    qexact = c * pt + sh * pr / L
    qscale = np.maximum(np.maximum(np.abs(qtarget), abs(qbg)), 1e-300)
    qerr = float(np.max(np.abs(qexact - qtarget) / qscale))
    corr = pt - qtarget

    # Same stable Exp coordinate used by frozen Repair02.
    z = zbg + dq / b4.Z0
    w = z * z
    with np.errstate(over='ignore', invalid='ignore'):
        ew = np.exp(w)
        K = 2.0 * b4.K2 * b4.Z0 * b4.Z0 * np.expm1(w)
        KQ = 4.0 * b4.K2 * b4.Z0 * z * ew
        KQQ = 4.0 * b4.K2 * ew * (1.0 + 2.0 * w)
    literal_z = (qexact - b4.Q0) / b4.Z0
    finite_exp = bool(
        np.all(np.isfinite(z)) and np.all(np.isfinite(ew)) and np.all(np.isfinite(K))
        and np.all(np.isfinite(KQ)) and np.all(np.isfinite(KQQ))
    )
    dictionary = {
        'scale_hinv_Mpc': float(scale),
        'Nr': int(nr),
        'Q_target_max_normalized_error': qerr,
        'phidot_completion_relative_L2': float(np.linalg.norm(corr) / max(np.linalg.norm(qtarget), 1e-300)),
        'phidot_completion_abs_max_Mpc_inv': float(np.max(np.abs(corr))),
        'stable_Z_abs_max': float(np.max(np.abs(z))),
        'literal_subtraction_Z_abs_max_diagnostic': float(np.max(np.abs(literal_z))),
        'K_abs_max': float(np.max(np.abs(K))) if finite_exp else float('inf'),
        'KQ_abs_max': float(np.max(np.abs(KQ))) if finite_exp else float('inf'),
        'KQQ_abs_max': float(np.max(np.abs(KQQ))) if finite_exp else float('inf'),
        'Exp_sector_finite': finite_exp,
    }

    rows = []
    args = [L, R, u, Lt, Rt, ut, pt, Lr, Rr, ur, pr]
    X = sh * pt + c * pr / L
    noncenter = np.arange(n) > 0

    for kind in KINDS:
        for beta in BETAS:
            CH = []
            CM = []
            for _, fs in funcs.items():
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

            # Exact Exp K(Q) lapse/shift EL terms copied from frozen Repair02.
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
            finite = bool(
                finite_exp and np.all(np.isfinite(CH[:, noncenter])) and np.all(np.isfinite(CM[:, noncenter]))
            )
            if finite:
                denH = np.sum(np.abs(CH), axis=0)
                denM = np.sum(np.abs(CM), axis=0)
                preH = float(np.max(denH[noncenter]))
                preM = float(np.max(denM[noncenter]))
                finite = bool(preH > 0 and preM > 0 and np.isfinite(preH) and np.isfinite(preM))
            else:
                preH = preM = float('nan')

            if finite:
                floorH = 1e-14 * preH
                floorM = 1e-14 * preM
                eH = np.abs(np.sum(CH, axis=0)) / (denH + floorH)
                eM = np.abs(np.sum(CM, axis=0)) / (denM + floorM)
                mh = float(np.max(eH[noncenter]))
                mm = float(np.max(eM[noncenter]))
                rh = r2.rms(eH[noncenter])
                rm = r2.rms(eM[noncenter])
            else:
                floorH = floorM = float('nan')
                mh = mm = rh = rm = float('inf')

            rows.append({
                'scale_hinv_Mpc': float(scale),
                'Nr': int(nr),
                'Y_kind': kind,
                'beta0': float(beta),
                'all_action_terms_finite_noncenter': finite,
                'max_epsilon_H': mh,
                'max_epsilon_M': mm,
                'rms_epsilon_H': rh,
                'rms_epsilon_M': rm,
                'pre_floor_denominator_max_H': preH,
                'pre_floor_denominator_max_M': preM,
                'floor_H': floorH,
                'floor_M': floorM,
                'limit': LIMIT,
                'constraint_pass': bool(finite and mh <= LIMIT and mm <= LIMIT),
            })
    return dictionary, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trace', required=True)
    ap.add_argument('--coverage-json', required=True)
    ap.add_argument('--repair08-json', required=True)
    ap.add_argument('--repair08-npz', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    npz_sha = sha256_file(a.repair08_npz)
    json_sha = sha256_file(a.repair08_json)
    r8_result = json.loads(Path(a.repair08_json).read_text())
    cov = json.loads(Path(a.coverage_json).read_text())
    off = np.load(a.repair08_npz)

    z = rec.read_trace(a.trace)
    ks, gs = rec.groups(z)
    tv_rec = rec.at_ai(gs, 'pchip')
    ks_b4, gs_b4 = b4.groups(b4.read_trace(a.trace))
    tv_b4 = b4.at_ai(gs_b4)
    h = float(cov['h'])

    metadata_ok = bool(
        'a_i' in off.files and 'scales_hinv_Mpc' in off.files and 'k_grid_Mpc_inv' in off.files and 'h' in off.files
        and abs(float(np.asarray(off['a_i'])) - b4.AI) <= 1e-15
        and rel_sym(np.asarray(off['scales_hinv_Mpc']), np.asarray(b4.SCALES, float)) <= 1e-15
        and rel_sym(np.asarray(off['k_grid_Mpc_inv']), np.asarray(ks, float)) <= 1e-15
        and abs(float(np.asarray(off['h'])) - h) <= 1e-15
    )
    r8_gates = r8_result.get('gates', {})
    g1 = bool(
        npz_sha == NPZ_SHA256 and json_sha == JSON_SHA256
        and r8_result.get('classification') == 'NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED'
        and len(r8_gates) == 10 and all(r8_gates.values())
        and r8_result.get('new_state_npz_written') is True
        and cov.get('classification') == 'NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max') == 0
        and cov.get('n_native_times') == 179
        and abs(float(cov.get('a_i')) - b4.AI) <= 1e-15
        and len(ks) == 128 and np.array_equal(ks, ks_b4)
        and metadata_ok
    )

    scalar_ai, scalar_independent, scalar_finite, _ = r8.scalar_composites_at_ai(ks, gs, 'pchip')
    scalar_identity_error = rel_sym(scalar_ai, scalar_independent)

    # Continuous Repair08 representation is reconstructed only for provenance and Nr=512 control.
    reconstructed_256 = {}
    control_512 = {}
    anchor_rows = []
    anchor_max = 0.0
    anchor_finite = True
    for scale in b4.SCALES:
        r256 = r8.repaired_state(scale, rec.NQ, ks, h, tv_rec, 'pchip', scalar_ai)
        reconstructed_256[scale] = r256
        control_512[scale] = repaired_state_nr(scale, 512, ks, h, tv_b4, tv_rec, scalar_ai)
        primary = load_primary_state(off, scale)
        for field, value in r256.items():
            if field not in primary:
                anchor_rows.append({'scale_hinv_Mpc': float(scale), 'field': field, 'present': False, 'pass': False})
                anchor_finite = False
                continue
            err = rel_sym(value, primary[field])
            passed = bool(np.isfinite(err) and err <= ANCHOR_LIMIT)
            anchor_rows.append({
                'scale_hinv_Mpc': float(scale), 'field': field, 'present': True,
                'relative_L2': err, 'limit': ANCHOR_LIMIT, 'pass': passed,
            })
            anchor_max = max(anchor_max, err)
            anchor_finite &= passed
    g2 = bool(anchor_finite and anchor_max <= ANCHOR_LIMIT and scalar_finite and scalar_identity_error <= 1e-10)

    # The actual primary states are read directly from the certified NPZ.
    states = {(scale, 256): load_primary_state(off, scale) for scale in b4.SCALES}
    for scale in b4.SCALES:
        states[(scale, 512)] = control_512[scale]

    kq_bg = float(np.median(tv_b4['KQ']))
    qbg = b4.stable_q_from_kq(kq_bg)
    zbg = stable_zbg(kq_bg)
    funcs, dY, kdict_identity = r1.build_nonK()

    dictionary = []
    rows = []
    for scale in b4.SCALES:
        for nr in (256, 512):
            drow, crows = evaluate_state(states[(scale, nr)], scale, nr, qbg, zbg, funcs, dY)
            dictionary.append(drow)
            rows.extend(crows)

    max_qerr = max(x['Q_target_max_normalized_error'] for x in dictionary)
    exp_finite = all(x['Exp_sector_finite'] for x in dictionary)
    g3 = bool(kdict_identity and exp_finite and np.isfinite(max_qerr) and max_qerr <= DICT_LIMIT)

    g4 = bool(len(rows) == 54 and all(x['constraint_pass'] for x in rows))

    grid = []
    grid_ok = True
    for scale in b4.SCALES:
        for kind in KINDS:
            for beta in BETAS:
                a256 = next(x for x in rows if x['scale_hinv_Mpc'] == scale and x['Nr'] == 256 and x['Y_kind'] == kind and x['beta0'] == beta)
                a512 = next(x for x in rows if x['scale_hinv_Mpc'] == scale and x['Nr'] == 512 and x['Y_kind'] == kind and x['beta0'] == beta)
                qh = r2.ratio2(a256['rms_epsilon_H'], a512['rms_epsilon_H'])
                qm = r2.ratio2(a256['rms_epsilon_M'], a512['rms_epsilon_M'])
                ok = bool(np.isfinite(qh) and np.isfinite(qm) and qh <= GRID_RATIO_LIMIT and qm <= GRID_RATIO_LIMIT)
                grid_ok &= ok
                grid.append({
                    'scale_hinv_Mpc': float(scale), 'Y_kind': kind, 'beta0': float(beta),
                    'rms_ratio_H': qh, 'rms_ratio_M': qm,
                    'limit': GRID_RATIO_LIMIT, 'pass': ok,
                })
    g5 = bool(len(grid) == 27 and grid_ok)

    claim_boundary = {
        'primary_256_loaded_directly_from_certified_Repair08_NPZ': True,
        'state_projection_used': False,
        'coefficient_fitted': False,
        'source_fitted_or_inserted': False,
        'sign_changed': False,
        'K_clipping_used': False,
        'Q_linearized': False,
        'radial_points_removed': False,
        'historical_threshold_changed': False,
        'Y_branch_selected': False,
        'scale_selected': False,
        'nonlinear_evolution_executed': False,
        'finite_eta_executed': False,
        'observational_detection_claimed': False,
    }
    g6 = bool(
        claim_boundary['primary_256_loaded_directly_from_certified_Repair08_NPZ']
        and not claim_boundary['state_projection_used']
        and not claim_boundary['coefficient_fitted']
        and not claim_boundary['source_fitted_or_inserted']
        and not claim_boundary['sign_changed']
        and not claim_boundary['K_clipping_used']
        and not claim_boundary['Q_linearized']
        and not claim_boundary['radial_points_removed']
        and not claim_boundary['historical_threshold_changed']
        and not claim_boundary['Y_branch_selected']
        and not claim_boundary['scale_selected']
        and not claim_boundary['nonlinear_evolution_executed']
        and not claim_boundary['finite_eta_executed']
    )

    gates = {
        'R9_G1_exact_Repair08_provenance': g1,
        'R9_G2_Repair08_state_anchor_reproduction': g2,
        'R9_G3_exact_nonlinear_dictionary': g3,
        'R9_G4_original_raw_B4_constraints': g4,
        'R9_G5_two_grid_control': g5,
        'R9_G6_claim_boundary': g6,
    }

    if not (g1 and g2 and g3 and g6):
        classification = 'NL1C7B4_REPAIR09_IMPLEMENTATION_FAIL'
        rc = 2
    elif not g4:
        classification = 'NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL'
        rc = 2
    elif not g5:
        classification = 'NL1C7B4_REPAIR09_IMPLEMENTATION_FAIL'
        rc = 2
    else:
        classification = 'NL1C7B4_REPAIR09_REPAIR08_EXACT_NONLINEAR_CONSTRAINT_PASS'
        rc = 0

    result = {
        'classification': classification,
        'scope': 'Repair09 exact nonlinear B4 raw eta=0 initial-constraint retest on the certified Repair08 scalar representation; no evolution or finite eta.',
        'provenance': {
            'repair08_npz_sha256_observed': npz_sha,
            'repair08_npz_sha256_expected': NPZ_SHA256,
            'repair08_json_sha256_observed': json_sha,
            'repair08_json_sha256_expected': JSON_SHA256,
            'repair08_freeze_commit': '6a8812f9b8d9f4fa373212376b6c01b4649076aa',
            'repair09_prereg_commit': 'ee97aec3e274f3996c87c622a770f5233666f7f6',
            'dense_trace_artifact': 10469031693,
            'dense_trace_sha256': '193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70',
        },
        'state_anchor': {
            'max_relative_L2': anchor_max,
            'limit': ANCHOR_LIMIT,
            'scalar_canonical_vs_independent_at_ai_relative_L2': scalar_identity_error,
            'pass': g2,
            'rows': anchor_rows,
        },
        'background': {
            'Q_bg_Mpc_inv': qbg,
            'Z_bg_stable': zbg,
            'H_Mpc_inv': b4.H_DIRECT,
            'varrho_b': b4.VAR_B,
            'rho_std_C6': b4.RHO_STD,
        },
        'symbolic_K_dictionary_identity': bool(kdict_identity),
        'dictionary_completion': dictionary,
        'constraint_rows': rows,
        'grid_control': grid,
        'gates': gates,
        'summary': {
            'n_constraint_cases': len(rows),
            'n_constraint_pass': int(sum(x['constraint_pass'] for x in rows)),
            'n_grid_pairs': len(grid),
            'max_Q_target_error': float(max_qerr),
            'max_stable_Z_abs': float(max(x['stable_Z_abs_max'] for x in dictionary)),
            'max_epsilon_H': float(max(x['max_epsilon_H'] for x in rows)),
            'max_epsilon_M': float(max(x['max_epsilon_M'] for x in rows)),
            'min_max_epsilon_H': float(min(x['max_epsilon_H'] for x in rows)),
            'min_max_epsilon_M': float(min(x['max_epsilon_M'] for x in rows)),
            'constraint_limit': LIMIT,
            'grid_ratio_limit': GRID_RATIO_LIMIT,
        },
        'claim_boundary': claim_boundary,
    }
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=True))
    raise SystemExit(rc)


if __name__ == '__main__':
    main()
