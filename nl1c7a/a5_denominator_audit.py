#!/usr/bin/env python3
from pathlib import Path
import argparse, json
import numpy as np
from scipy.interpolate import PchipInterpolator

AI = 0.02
SCALES_HINV_MPC = [5.0, 10.0, 20.0]
QUAD_N = [256, 512]
WEIGHT_REL_CUT = 1.0e-10
DENOM_REL_FLOOR = 1.0e-12
EXPECTED_K_COUNT = 128


def read_trace(path):
    data = np.genfromtxt(path, names=True)
    if data.size == 0:
        raise RuntimeError('empty trace')
    return data


def time_at_ai(trace, field, ks):
    p = []
    l = []
    x0 = np.log(AI)
    for k in ks:
        g = trace[trace['k'] == k]
        order = np.argsort(g['a'])
        a = np.asarray(g['a'][order], float)
        y = np.asarray(g[field][order], float)
        if not (a[0] < AI < a[-1]):
            raise RuntimeError(f'a_i not bracketed at k={k}')
        x = np.log(a)
        p.append(float(PchipInterpolator(x, y)(x0)))
        l.append(float(np.interp(x0, x, y)))
    return np.asarray(p), np.asarray(l)


def target_weight(k_mpc, R_hinv, h):
    R = R_hinv / h
    q = k_mpc * R
    return np.abs((q*q/3.0) * np.exp(-0.5*q*q))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trace', required=True)
    ap.add_argument('--coverage-json', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    coverage = json.loads(Path(args.coverage_json).read_text())
    if coverage.get('classification') != 'NL1C7A_NATIVE_TRACE_COVERAGE_PASS':
        raise RuntimeError('parent A4 classification is not PASS')
    if coverage.get('requested_k_relative_miss_max') != 0.0:
        raise RuntimeError('parent A4 exact-k property lost')
    if coverage.get('repair05', {}).get('interpolation_used') is not False:
        raise RuntimeError('parent A4 used interpolation')

    h = float(coverage['h'])
    trace = read_trace(args.trace)
    ks = np.unique(np.asarray(trace['k'], float))
    if len(ks) != EXPECTED_K_COUNT:
        raise RuntimeError(f'expected {EXPECTED_K_COUNT} k modes, found {len(ks)}')
    ks.sort()
    kh = ks / h

    db_p_time, db_l_time = time_at_ai(trace, 'delta_b', ks)
    if not (np.all(np.isfinite(db_p_time)) and np.all(np.isfinite(db_l_time))):
        raise RuntimeError('non-finite baryon transfer at a_i')

    cases = []
    all_primary_pass = True
    global_min_ratio_primary = np.inf
    global_min_ratio_linear_k = np.inf
    max_time_interp_rel = float(np.max(np.abs(db_p_time-db_l_time) / np.maximum(np.abs(db_p_time), 1e-300)))

    for nq in QUAD_N:
        qh = np.geomspace(float(kh[0]), float(kh[-1]), nq)
        qk = qh * h
        db_p_k = PchipInterpolator(np.log(kh), db_p_time)(np.log(qh))
        db_l_k = np.interp(np.log(qh), np.log(kh), db_p_time)
        maxabs_p = float(np.max(np.abs(db_p_k)))
        maxabs_l = float(np.max(np.abs(db_l_k)))
        for scale in SCALES_HINV_MPC:
            w = target_weight(qk, scale, h)
            active = w > WEIGHT_REL_CUT * float(np.max(w))
            if not np.any(active):
                raise RuntimeError(f'no active target-weight nodes for scale={scale}, nq={nq}')
            ratio_p = float(np.min(np.abs(db_p_k[active])) / maxabs_p)
            ratio_l = float(np.min(np.abs(db_l_k[active])) / maxabs_l)
            finite_p = bool(np.all(np.isfinite(db_p_k[active])))
            primary_pass = finite_p and ratio_p >= DENOM_REL_FLOOR
            all_primary_pass = all_primary_pass and primary_pass
            global_min_ratio_primary = min(global_min_ratio_primary, ratio_p)
            global_min_ratio_linear_k = min(global_min_ratio_linear_k, ratio_l)
            cases.append({
                'quadrature_nodes': nq,
                'R_sigma_hinv_Mpc': scale,
                'active_nodes': int(np.count_nonzero(active)),
                'active_k_h_Mpc_min': float(qh[active][0]),
                'active_k_h_Mpc_max': float(qh[active][-1]),
                'primary_pchip_lnk_minabs_over_maxabs': ratio_p,
                'control_linear_lnk_minabs_over_maxabs': ratio_l,
                'primary_min_abs_T_delta_b': float(np.min(np.abs(db_p_k[active]))),
                'primary_max_abs_T_delta_b': maxabs_p,
                'primary_finite': finite_p,
                'A5_primary_pass': primary_pass,
            })

    gates = {
        'A5_parent_A4_exact_native_coverage': True,
        'A5_T_delta_b_finite_on_all_primary_active_nodes': bool(all(c['primary_finite'] for c in cases)),
        'A5_no_relevant_transfer_zero': bool(global_min_ratio_primary >= DENOM_REL_FLOOR),
        'A5_no_clipping_or_node_deletion': True,
    }
    classification = 'NL1C7A_A5_FINITE_GROWING_MODE_DENOMINATOR_PASS' if all(gates.values()) else 'NL1C7A_TRANSFER_ZERO_FAIL'
    result = {
        'classification': classification,
        'scope': 'NL1C7A A5 only; eta=0 denominator audit on frozen Repair05 trace. No radial reconstruction or spherical evolution.',
        'parent_A4_run': 35104087182,
        'parent_A4_artifact': 10450205501,
        'parent_A4_artifact_sha256': '9b1a4f998af55ce594cbdd6db78b9b99944cd25a3f690c68bab49ffef290ffc6',
        'a_i': AI,
        'scales_hinv_Mpc': SCALES_HINV_MPC,
        'quadrature_nodes': QUAD_N,
        'weight_relative_cut': WEIGHT_REL_CUT,
        'denominator_relative_floor': DENOM_REL_FLOOR,
        'time_interpolation_primary': 'PCHIP in ln a',
        'time_interpolation_control': 'linear in ln a',
        'k_interpolation_primary': 'PCHIP in ln k',
        'k_interpolation_control_reported': 'linear in ln k',
        'max_delta_b_time_interpolation_relative_difference_at_native_k': max_time_interp_rel,
        'global_min_primary_minabs_over_maxabs': float(global_min_ratio_primary),
        'global_min_control_linear_k_minabs_over_maxabs': float(global_min_ratio_linear_k),
        'cases': cases,
        'gates': gates,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if all(gates.values()) else 1)


if __name__ == '__main__':
    main()
