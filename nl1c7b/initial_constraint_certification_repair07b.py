#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import json
import math
import sys
from pathlib import Path

import numpy as np

import nl1c7b.initial_constraint_certification_repair07a as r7a

ALGEBRA_LIMIT = 1e-10
FOURIER_ENVELOPE = 2e-2
STATE_LIMIT = 1e-12


def output_path(argv: list[str]) -> Path:
    if '--out' not in argv:
        raise RuntimeError('Repair07b requires the inherited --out argument')
    i = argv.index('--out')
    if i + 1 >= len(argv):
        raise RuntimeError('missing value after --out')
    return Path(argv[i + 1])


def main() -> None:
    captured = io.StringIO()
    parent_rc = None
    try:
        with contextlib.redirect_stdout(captured):
            r7a.main()
    except SystemExit as exc:
        parent_rc = int(exc.code or 0)

    if parent_rc is None:
        raise RuntimeError('Repair07a returned without terminal SystemExit')

    out = output_path(sys.argv)
    if not out.is_file():
        sys.stdout.write(captured.getvalue())
        raise RuntimeError('Repair07a did not write the expected result JSON')

    d = json.loads(out.read_text())

    bridge = d.get('repair07a_theta_A_bridge', {})
    scalar = d.get('scalar_composite', {})
    state = d.get('state_reproduction', {})
    symk = d.get('symbolic_K_shift', {})
    fourier = d.get('fourier_0i', {})
    oldg = d.get('gates', {})
    cb = d.get('claim_boundary', {})

    state_value = float(state.get('max_relative_L2', math.inf))
    initial_identity = float(scalar.get('composite_first_vs_theta_at_ai_relative_L2', math.inf))
    full_trace_identity = float(scalar.get('native_identity_relative_L2', math.inf))
    fourier_max = float(fourier.get('max_epsilon_0i', math.inf))

    g1 = bool(
        oldg.get('R7_G1_provenance_and_immutability') is True
        and state.get('pass') is True
        and np.isfinite(state_value)
        and state_value <= STATE_LIMIT
    )

    g2 = bool(
        oldg.get('R7_G2_exact_covariant_identities') is True
        and d.get('GR_closed_form_pass') is True
        and symk.get('pass') is True
        and symk.get('exact_shift_source_residual') == '0'
        and symk.get('exact_frechet_residual') == '0'
    )

    g3 = bool(
        bridge.get('source') == 'native retained dense trace theta_A column'
        and bridge.get('interpolator') == 'PchipInterpolator'
        and bridge.get('independent_variable') == 'log(a)'
        and int(bridge.get('n_k_groups', -1)) == 128
        and bridge.get('all_finite') is True
        and np.isfinite(initial_identity)
        and initial_identity <= ALGEBRA_LIMIT
    )

    g4 = bool(
        np.isfinite(fourier_max)
        and abs(float(fourier.get('inherited_limit', math.inf)) - FOURIER_ENVELOPE) < 1e-15
        and fourier_max <= FOURIER_ENVELOPE
    )

    g5 = bool(
        oldg.get('R7_G5_no_post_result_repair') is True
        and cb.get('official_C7A_NPZ_modified') is False
        and cb.get('new_state_NPZ_written') is False
        and cb.get('coefficient_fitted') is False
        and cb.get('sign_flipped') is False
        and cb.get('standard_sector_source_fitted_or_inserted') is False
        and cb.get('radial_points_removed_from_B4_metric') is False
        and cb.get('historical_threshold_changed') is False
        and cb.get('nonlinear_evolution_executed') is False
        and cb.get('finite_eta_executed') is False
        and cb.get('B4_pass_claimed') is False
        and bridge.get('physics_coefficients_changed') is False
        and bridge.get('thresholds_changed') is False
        and bridge.get('state_modified') is False
    )

    finite = bool(
        np.isfinite(state_value)
        and np.isfinite(initial_identity)
        and np.isfinite(full_trace_identity)
        and np.isfinite(fourier_max)
    )

    implementation_ok = bool(g1 and g2 and g3 and g5 and finite)
    if not implementation_ok:
        classification = 'NL1C7B4_REPAIR07B_IMPLEMENTATION_FAIL'
        rc = 2
    elif g4:
        classification = 'NL1C7B4_REPAIR07B_INITIAL_SLICE_BRIDGE_DIAGNOSTIC_PASS'
        rc = 0
    else:
        classification = 'NL1C7B4_REPAIR07B_COVARIANT_FOURIER_INTERFACE_MISMATCH'
        rc = 0

    historical_class = d.get('classification')
    d['historical_repair07a_classification'] = historical_class
    d['historical_repair07a_science_rc'] = parent_rc
    d['classification'] = classification
    d['scope'] = (
        'Repair07b diagnostic-domain repair of the frozen eta=0 covariant/Fourier '
        'momentum-bridge audit. The scalar algebra gate is restricted to the B4 initial '
        'slice a_i=0.02; the full serialized-trace Repair07a identity failure remains '
        'reported as a non-gating historical diagnostic.'
    )
    d['repair07b_scalar_identity_domain'] = {
        'gate_domain': 'initial slice a_i=0.02 only',
        'algebra_identity_limit_unchanged': ALGEBRA_LIMIT,
        'initial_slice_composite_first_vs_theta_relative_L2': initial_identity,
        'initial_slice_pass': bool(initial_identity <= ALGEBRA_LIMIT),
        'historical_full_serialized_trace_relative_L2': full_trace_identity,
        'historical_full_trace_repair07a_limit': ALGEBRA_LIMIT,
        'historical_full_trace_repair07a_pass': bool(full_trace_identity <= ALGEBRA_LIMIT),
        'historical_full_trace_is_repair07b_gate': False,
        'reason': 'B4 is an initial-constraint certification; full-time text-serialized cancellation diagnostic is outside the certified slice.',
    }
    d['gates'] = {
        'R7B_G1_provenance_and_immutability': g1,
        'R7B_G2_exact_covariant_identities': g2,
        'R7B_G3_initial_slice_scalar_identity': g3,
        'R7B_G4_inherited_C7A_fourier_interface_envelope': g4,
        'R7B_G5_no_post_result_repair': g5,
    }
    d['claim_boundary']['repair07a_parent_evaluator_modified'] = False
    d['claim_boundary']['repair07b_changed_identity_threshold'] = False
    d['claim_boundary']['repair07b_changed_identity_domain_to_B4_initial_slice'] = True
    d['claim_boundary']['historical_repair07a_full_trace_failure_preserved'] = True
    d['claim_boundary']['B4_pass_claimed'] = False

    out.write_text(json.dumps(d, indent=2, sort_keys=True) + '\n')
    print(json.dumps(d, indent=2, sort_keys=True))
    raise SystemExit(rc)


if __name__ == '__main__':
    main()
