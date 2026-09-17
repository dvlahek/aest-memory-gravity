#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair07 as r7


CLASS_MAP = {
    'NL1C7B4_REPAIR07_COVARIANT_FOURIER_BRIDGE_DIAGNOSTIC_PASS':
        'NL1C7B4_REPAIR07A_COVARIANT_FOURIER_BRIDGE_DIAGNOSTIC_PASS',
    'NL1C7B4_REPAIR07_COVARIANT_FOURIER_INTERFACE_MISMATCH':
        'NL1C7B4_REPAIR07A_COVARIANT_FOURIER_INTERFACE_MISMATCH',
    'NL1C7B4_REPAIR07_IMPLEMENTATION_FAIL':
        'NL1C7B4_REPAIR07A_IMPLEMENTATION_FAIL',
}


def output_path(argv: list[str]) -> Path:
    if '--out' not in argv:
        raise RuntimeError('Repair07a requires the inherited --out argument')
    i = argv.index('--out')
    if i + 1 >= len(argv):
        raise RuntimeError('missing value after --out')
    return Path(argv[i + 1])


def main() -> None:
    original_at_ai = b4.at_ai
    bridge_meta: dict[str, object] = {}

    def at_ai_with_native_theta_A(gs):
        tv = original_at_ai(gs)
        if len(gs) != 128:
            raise RuntimeError(f'Repair07a expected 128 native k-groups, got {len(gs)}')

        values = []
        x0 = math.log(b4.AI)
        for i, g in enumerate(gs):
            names = tuple(g.dtype.names or ())
            if 'theta_A' not in names:
                raise RuntimeError(f'native dense trace group {i} has no theta_A column')
            x = np.log(np.asarray(g['a'], float))
            theta = np.asarray(g['theta_A'], float)
            if not (x[0] < x0 < x[-1]):
                raise RuntimeError(f'a_i not bracketed for theta_A in group {i}')
            value = float(PchipInterpolator(x, theta)(x0))
            if not np.isfinite(value):
                raise RuntimeError(f'non-finite theta_A(a_i) in group {i}')
            values.append(value)

        arr = np.asarray(values, float)
        tv['theta_A'] = arr
        bridge_meta.update({
            'source': 'native retained dense trace theta_A column',
            'interpolator': 'PchipInterpolator',
            'independent_variable': 'log(a)',
            'a_i': float(b4.AI),
            'n_k_groups': int(len(gs)),
            'all_finite': bool(np.all(np.isfinite(arr))),
            'theta_A_ai_min': float(np.min(arr)),
            'theta_A_ai_max': float(np.max(arr)),
            'physics_coefficients_changed': False,
            'thresholds_changed': False,
            'state_modified': False,
        })
        return tv

    b4.at_ai = at_ai_with_native_theta_A
    captured = io.StringIO()
    exit_code = None
    try:
        with contextlib.redirect_stdout(captured):
            r7.main()
    except SystemExit as exc:
        exit_code = int(exc.code or 0)
    finally:
        b4.at_ai = original_at_ai

    if exit_code is None:
        raise RuntimeError('Repair07 evaluator returned without terminal SystemExit')

    out = output_path(sys.argv)
    if not out.is_file():
        sys.stdout.write(captured.getvalue())
        raise RuntimeError('Repair07 did not write the expected result JSON')

    result = json.loads(out.read_text())
    old_class = result.get('classification')
    if old_class not in CLASS_MAP:
        raise RuntimeError(f'unexpected Repair07 terminal classification: {old_class!r}')

    result['parent_repair07_terminal_classification'] = old_class
    result['classification'] = CLASS_MAP[old_class]
    result['scope'] = (
        'Repair07a harness-only repair of the frozen eta=0 Repair07 covariant/Fourier '
        'momentum-bridge audit. The sole added operation is native theta_A interpolation '
        'to a_i with the same PCHIP(log(a)) bridge used by frozen B4; no state or physics '
        'quantity is modified.'
    )
    result['repair07a_theta_A_bridge'] = bridge_meta
    result['claim_boundary']['repair07_parent_evaluator_modified'] = False
    result['claim_boundary']['theta_A_bridge_harness_only'] = True
    result['claim_boundary']['physics_equation_changed'] = False
    result['claim_boundary']['threshold_changed_by_repair07a'] = False
    result['claim_boundary']['B4_pass_claimed'] = False

    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(exit_code)


if __name__ == '__main__':
    main()
