#!/usr/bin/env python3
"""Technical execution repair for v0.75 run 34282625854.

The failed run stopped before a v0.75 science classification because the
strict external-force loader encountered a k value present in the classy
science run but absent from the forcing table.  The original forcing trace was
built through the CLASS executable while the science run was built through
classy.Class().  At higher preregistered k resolution those two execution paths
produced non-identical internal k support.

This wrapper changes only the trace-generation path: it rebuilds the same
eta=0 positive-Drude forcing from a baseline classy.Class() instance using the
exact same locked parameters and resolution as the subsequent science runs.
The physical model, resolution sequence, fixed (k,z) grid, tangent amplitudes,
Drude quadrature orders, and all preregistered gates remain unchanged.
"""

from pathlib import Path
import json
import os
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import v063.theory_response_map as v63
import v075.fourier_k_resolution_closure as core

FAILED_RUN_ID = 34282625854
FORCE_K_REL_MAX = 2.0e-10


def _restore_env(saved):
    for key, value in saved.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


def build_forcing_for_resolution(class_root, res):
    """Build the unchanged v0.75 forcing on the exact classy science k grid."""
    from classy import Class

    results = ROOT / 'results'
    results.mkdir(exist_ok=True)
    label = res['label']
    trace = results / f'v075_{label}_forcing_trace.dat'
    log = results / f'v075_{label}_forcing_trace.log'
    if trace.exists():
        trace.unlink()

    env_keys = ['AEST_TANGENT_FORCE_FILE', 'AEST_TANGENT_LAMBDA', 'AEST_OFFLINE_TRACE_FILE']
    saved = {key: os.environ.get(key) for key in env_keys}

    c = None
    try:
        os.environ.pop('AEST_TANGENT_FORCE_FILE', None)
        os.environ.pop('AEST_TANGENT_LAMBDA', None)
        os.environ['AEST_OFFLINE_TRACE_FILE'] = str(trace.resolve())
        os.environ['OMP_NUM_THREADS'] = '1'

        # Intentionally identical to core.compute_run(), except there is no
        # external tangent force.  This guarantees that the baseline trace and
        # the subsequent +/-lambda runs use the same internal CLASS k support.
        pars = dict(v63.class_params())
        pars['output'] = 'mPk,mTk'
        pars['lensing'] = 'no'
        pars['k_output_values'] = ', '.join(f'{k:.17g}' for k in core.K_REQ)
        pars['P_k_max_h/Mpc'] = 2.0
        pars['z_max_pk'] = 5.0
        pars.update(core._resolution_params(res))

        c = Class()
        c.set(pars)
        c.compute()
        c.struct_cleanup()
        c.empty()
        c = None
    finally:
        if c is not None:
            try:
                c.struct_cleanup()
                c.empty()
            except Exception:
                pass
        _restore_env(saved)

    if not trace.exists() or trace.stat().st_size == 0:
        raise RuntimeError(f'{label}: classy baseline forcing trace not produced')

    trace_k = np.loadtxt(trace, comments='#', skiprows=1, usecols=(0,))
    trace_unique = np.unique(np.atleast_1d(trace_k).astype(float))

    log.write_text(json.dumps({
        'classification': 'V075_CLASSY_MATCHED_FORCING_TRACE_TECHNICAL_REPAIR',
        'source_failed_run_id': FAILED_RUN_ID,
        'resolution': dict(res),
        'trace_generation_path': 'patched classy.Class baseline with the exact same parameter dictionary as compute_run',
        'k_histories_in_trace': int(trace_unique.size),
        'physics_modified': False,
        'resolution_sequence_modified': False,
        'fixed_grid_modified': False,
        'tangent_amplitudes_modified': False,
        'science_gates_modified': False,
        'drude_quadrature_orders_modified': False,
    }, indent=2) + '\n')

    prefix = results / f'v075_{label}_forcing'
    summary = results / f'v075_{label}_forcing_summary.json'
    subprocess.run(
        [
            sys.executable,
            str(ROOT / 'v039/build_tau_forcing.py'),
            str(trace),
            '--KB', str(v63.KB),
            '--tauH0', str(v63.TAUH0),
            '--out-prefix', str(prefix),
            '--control-order', '512',
            '--primary-order', '1024',
            '--summary', str(summary),
        ],
        check=True,
    )

    force = Path(str(prefix) + '_force.dat')
    if not force.exists() or force.stat().st_size == 0:
        raise RuntimeError(f'{label}: forcing table not produced')

    force_k = np.loadtxt(force, usecols=(0,))
    force_unique = np.unique(np.atleast_1d(force_k).astype(float))
    support_rel = np.array([
        np.min(np.abs(force_unique - k)) / max(abs(k), 1.0e-300)
        for k in trace_unique
    ])
    support_rel_max = float(np.max(support_rel)) if support_rel.size else 0.0
    if support_rel_max > FORCE_K_REL_MAX:
        raise RuntimeError(
            f'{label}: forcing table does not reproduce its matched classy trace k support; '
            f'max relative k miss={support_rel_max:.3e}'
        )

    d = json.loads(summary.read_text())
    d['v075_resolution'] = dict(res)
    d['technical_execution_repair'] = {
        'source_failed_run_id': FAILED_RUN_ID,
        'failure': 'AEST_TANGENT_FORCE_K_MISS before v0.75 science result',
        'repair': 'generate baseline forcing trace through the same patched classy parameter path used by compute_run',
        'max_trace_to_force_relative_k_miss': support_rel_max,
        'trace_to_force_relative_k_miss_limit': FORCE_K_REL_MAX,
        'physical_model_changed': False,
        'resolution_sequence_changed': False,
        'fixed_k_z_grid_changed': False,
        'tangent_amplitudes_changed': False,
        'science_gates_changed': False,
        'drude_control_order': 512,
        'drude_primary_order': 1024,
    }
    summary.write_text(json.dumps(d, indent=2) + '\n')
    return force.resolve(), summary


# Replace only the technical forcing-trace builder.  All numerical evaluation,
# preregistered gates, and classification logic remain the original v0.75 code.
core.build_forcing_for_resolution = build_forcing_for_resolution

if __name__ == '__main__':
    core.main()
