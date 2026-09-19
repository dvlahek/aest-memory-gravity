#!/usr/bin/env python3
"""GE01 gravitational-viscoelastic tau-crossover map.

Reuses the certified v0.77 additive native-state observable and varies only
the physical memory timescale tauH0 across the analytically predeclared
Maxwell/Drude crossover grid.
"""

from pathlib import Path
import argparse
import json
import math
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import v063.theory_response_map as v63
import v075.fourier_k_resolution_closure as v75
import v076.native_node_power_closure as v76

TAUS = np.array([0.1, 0.3, 0.5, 0.7, 1.0, 3.0, 10.0], dtype=float)
LAMBDAS = np.array([2.5, 1.25], dtype=float)
H = float(v63.START['H0']) / 100.0

R4 = {
    'label': 'r4',
    'k_per_decade_for_pk': 80.0,
    'k_per_decade_for_bao': 560.0,
}

FORCING_L2_MAX = 1.0e-2
FORCING_COS_MIN = 0.9999
BASELINE_REL_L2_MAX = 1.0e-12
TANGENT_REL_L2_MAX = 5.0e-3
TANGENT_COS_MIN = 0.9999
TINY = 1.0e-300


def norm(x):
    return float(np.sqrt(np.sum(np.asarray(x, dtype=float) ** 2)))


def cosine(a, b):
    aa = np.asarray(a, dtype=float).ravel()
    bb = np.asarray(b, dtype=float).ravel()
    return float(np.dot(aa, bb) / max(norm(aa) * norm(bb), TINY))


def rel_l2(a, b):
    return norm(np.asarray(a, dtype=float) - np.asarray(b, dtype=float)) / max(norm(b), TINY)


def tau_tag(tau):
    return str(float(tau)).replace('.', 'p')


def analytic_K(tauH0, f):
    A = float(tauH0) * math.sqrt(float(f) * (float(f) + 3.0))
    return A / (1.0 + A)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--class-root', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--npz-out', required=True)
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    out_json = Path(args.json_out)
    out_npz = Path(args.npz_out)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    original_tau = float(v63.TAUH0)

    rows = []
    consensus_by_tau = []
    tangent_by_tau = []
    baseline_by_tau = []
    k_native_ref = None
    z_native_ref = None
    mask_ref = None
    baseline_ref = None
    forcing_all_pass = True
    baseline_all_pass = True
    tangent_all_pass = True
    all_finite = True

    try:
        for tau in TAUS:
            v63.TAUH0 = float(tau)

            force_file, forcing_summary_path = v75.build_forcing_for_resolution(class_root, R4)
            forcing = json.loads(Path(forcing_summary_path).read_text())
            forcing_pass = bool(
                float(forcing['relative_L2_control_vs_primary']) <= FORCING_L2_MAX
                and float(forcing['cosine']) >= FORCING_COS_MIN
            )
            forcing_all_pass = bool(forcing_all_pass and forcing_pass)

            tag = tau_tag(tau)
            base = v76.compute_run(force_file, None, f'ge01_tau{tag}_base')
            tangents = []
            for lam in LAMBDAS:
                ltag = str(float(lam)).replace('.', 'p')
                plus = v76.compute_run(
                    force_file, +float(lam), f'ge01_tau{tag}_plus_{ltag}'
                )
                minus = v76.compute_run(
                    force_file, -float(lam), f'ge01_tau{tag}_minus_{ltag}'
                )

                for name, rr in [('plus', plus), ('minus', minus)]:
                    if not np.allclose(rr['k_pk'], base['k_pk'], rtol=0.0, atol=1.0e-14):
                        raise RuntimeError(f'tau={tau} {name}: native k grid changed')
                    if not np.allclose(rr['z_pk'], base['z_pk'], rtol=0.0, atol=1.0e-14):
                        raise RuntimeError(f'tau={tau} {name}: native z grid changed')
                    all_finite = bool(
                        all_finite
                        and np.all(np.isfinite(rr['d_m_native']))
                    )

                tangents.append(
                    (plus['d_m_native'] - minus['d_m_native']) / (2.0 * float(lam))
                )

            tangents = np.asarray(tangents, dtype=float)
            all_finite = bool(
                all_finite
                and np.all(np.isfinite(base['d_m_native']))
                and np.all(np.isfinite(tangents))
            )

            kh_native = np.asarray(base['k_pk'], dtype=float) / H
            z_native = np.asarray(base['z_pk'], dtype=float)
            mask = (
                (kh_native[:, None] >= 0.03)
                & (kh_native[:, None] <= 0.20)
                & (z_native[None, :] >= 0.2)
                & (z_native[None, :] <= 1.5)
            )
            if not np.any(mask):
                raise RuntimeError(f'tau={tau}: empty primary native-state window')

            if k_native_ref is None:
                k_native_ref = kh_native.copy()
                z_native_ref = z_native.copy()
                mask_ref = mask.copy()
                baseline_ref = np.asarray(base['d_m_native'], dtype=float).copy()
            else:
                if not np.allclose(kh_native, k_native_ref, rtol=0.0, atol=1.0e-14):
                    raise RuntimeError(f'tau={tau}: native k grid differs across tau')
                if not np.allclose(z_native, z_native_ref, rtol=0.0, atol=1.0e-14):
                    raise RuntimeError(f'tau={tau}: native z grid differs across tau')
                if not np.array_equal(mask, mask_ref):
                    raise RuntimeError(f'tau={tau}: primary mask differs across tau')

            baseline_rel = rel_l2(base['d_m_native'][mask], baseline_ref[mask])
            baseline_pass = bool(baseline_rel <= BASELINE_REL_L2_MAX)
            baseline_all_pass = bool(baseline_all_pass and baseline_pass)

            vals = tangents[:, mask]
            consensus = np.mean(vals, axis=0)
            consensus_norm = norm(consensus)
            rels = np.array(
                [norm(vals[i] - consensus) / max(consensus_norm, TINY) for i in range(len(LAMBDAS))],
                dtype=float,
            )
            coss = np.array(
                [cosine(vals[i], consensus) for i in range(len(LAMBDAS))],
                dtype=float,
            )
            tangent_pass = bool(
                float(np.max(rels)) <= TANGENT_REL_L2_MAX
                and float(np.min(coss)) >= TANGENT_COS_MIN
            )
            tangent_all_pass = bool(tangent_all_pass and tangent_pass)

            full_consensus = np.mean(tangents, axis=0)
            masked_abs = np.where(mask, np.abs(full_consensus), -np.inf)
            flat = int(np.argmax(masked_abs))
            ik, iz = np.unravel_index(flat, full_consensus.shape)

            rows.append({
                'tauH0': float(tau),
                'forcing_relative_L2_control_vs_primary': float(forcing['relative_L2_control_vs_primary']),
                'forcing_cosine': float(forcing['cosine']),
                'forcing_pass': forcing_pass,
                'baseline_relative_L2_to_tau0p1': float(baseline_rel),
                'baseline_identity_pass': baseline_pass,
                'two_lambda_relative_L2_by_lambda': {
                    str(float(LAMBDAS[i])): float(rels[i])
                    for i in range(len(LAMBDAS))
                },
                'two_lambda_relative_L2_max': float(np.max(rels)),
                'two_lambda_cosine_by_lambda': {
                    str(float(LAMBDAS[i])): float(coss[i])
                    for i in range(len(LAMBDAS))
                },
                'two_lambda_cosine_min': float(np.min(coss)),
                'tangent_linearity_pass': tangent_pass,
                'consensus_tangent_L2_norm': float(consensus_norm),
                'largest_abs_consensus_tangent': {
                    'k_h_per_Mpc': float(kh_native[ik]),
                    'z': float(z_native[iz]),
                    'value': float(full_consensus[ik, iz]),
                    'baseline_d_m': float(base['d_m_native'][ik, iz]),
                },
                'analytic_Maxwell_proxy_at_H_eq_H0': {
                    'f_0p5_K': float(analytic_K(tau, 0.5)),
                    'f_1p0_K': float(analytic_K(tau, 1.0)),
                },
            })

            consensus_by_tau.append(full_consensus)
            tangent_by_tau.append(tangents)
            baseline_by_tau.append(np.asarray(base['d_m_native'], dtype=float).copy())
    finally:
        v63.TAUH0 = original_tau

    consensus_by_tau = np.asarray(consensus_by_tau, dtype=float)
    tangent_by_tau = np.asarray(tangent_by_tau, dtype=float)
    baseline_by_tau = np.asarray(baseline_by_tau, dtype=float)

    ref_idx = int(np.where(np.isclose(TAUS, 10.0))[0][0])
    ref_vec = consensus_by_tau[ref_idx][mask_ref]
    ref_norm = norm(ref_vec)
    norms = []
    cos_to_10 = []
    for i, tau in enumerate(TAUS):
        v = consensus_by_tau[i][mask_ref]
        n = norm(v)
        norms.append(n)
        cos_to_10.append(cosine(v, ref_vec))
        rows[i]['response_norm_relative_to_tauH0_10'] = float(n / max(ref_norm, TINY))
        rows[i]['consensus_cosine_to_tauH0_10'] = float(cos_to_10[-1])

    norms = np.asarray(norms, dtype=float)
    monotone_nondecreasing = bool(np.all(np.diff(norms) >= -1.0e-12 * max(float(np.max(norms)), 1.0)))

    numerical_pass = bool(
        forcing_all_pass
        and baseline_all_pass
        and tangent_all_pass
        and all_finite
    )
    classification = (
        'GE01_GRAVITATIONAL_ELASTIC_TAU_CROSSOVER_PASS'
        if numerical_pass
        else 'GE01_GRAVITATIONAL_ELASTIC_TAU_CROSSOVER_FAIL'
    )

    result = {
        'classification': classification,
        'predata_classification': 'GE01_PREDATA_GRAVITATIONAL_ELASTIC_TAU_CROSSOVER',
        'uses_observational_data': False,
        'scope': 'Theory-only eta=0 additive native matter-state tangent map across the analytic gravitational Maxwell/Drude tau crossover.',
        'canonical_theory': {
            'completion': 'NL0B_COVARIANT_MEMORY_COMPLETION_PASS',
            'interpretation': 'gravitational Maxwell viscoelasticity',
            'K_of_A': 'A/(1+A)',
            'A2': 'tau^2 s(s+3H)',
        },
        'tauH0_values': [float(x) for x in TAUS],
        'tangent_amplitudes': [float(x) for x in LAMBDAS],
        'native_window': {
            'k_h_per_Mpc_min': 0.03,
            'k_h_per_Mpc_max': 0.20,
            'z_min': 0.2,
            'z_max': 1.5,
            'n_common_native_nodes': int(np.count_nonzero(mask_ref)),
        },
        'rows': rows,
        'descriptive': {
            'response_norm_monotone_nondecreasing_with_tau': monotone_nondecreasing,
            'response_norms': [float(x) for x in norms],
            'cosine_to_tauH0_10': [float(x) for x in cos_to_10],
        },
        'gates': {
            'all_forcing_controls_pass': forcing_all_pass,
            'baseline_state_identity_across_tau_pass': baseline_all_pass,
            'two_lambda_tangent_linearity_all_tau_pass': tangent_all_pass,
            'all_values_finite': all_finite,
            'forcing_L2_limit': FORCING_L2_MAX,
            'forcing_cosine_min': FORCING_COS_MIN,
            'baseline_relative_L2_limit': BASELINE_REL_L2_MAX,
            'two_lambda_relative_L2_limit': TANGENT_REL_L2_MAX,
            'two_lambda_cosine_min': TANGENT_COS_MIN,
            'numerical_pass': numerical_pass,
        },
        'claim_boundary': 'PASS certifies the tau-response map of the eta=0 native matter-state tangent. It is not an observational detection, finite-eta validation, or nonlinear evolution.',
    }

    out_json.write_text(json.dumps(result, indent=2) + '\n')
    np.savez_compressed(
        out_npz,
        tauH0=TAUS,
        lambdas=LAMBDAS,
        k_native_h=k_native_ref,
        z_native=z_native_ref,
        primary_mask=mask_ref,
        baselines=baseline_by_tau,
        tangents=tangent_by_tau,
        consensus_tangents=consensus_by_tau,
        consensus_norms=norms,
        cosine_to_tau10=np.asarray(cos_to_10, dtype=float),
    )
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
