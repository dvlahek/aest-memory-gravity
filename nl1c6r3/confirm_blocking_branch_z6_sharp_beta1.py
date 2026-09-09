#!/usr/bin/env python3
"""Local-only formal confirmation of the NL1C6R3 blocking branch.

This script reuses the unchanged production NL1C6R3 solver on the first native
snapshot only, with kind='sharp' and beta=1.0, and runs both preregistered
constitutive anchor routes without a wall-clock timeout.

It does not alter equations, tolerances, continuation rules, endpoint gates,
or branch selection.  It writes a compact JSON result suitable for preserving
an explicit numerical blocking result before deciding the next scientific step.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from nl1c6 import full_j_baryonic_reclosure as base
from nl1c6r3 import fixed_source_constitutive_homotopy as r3


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def git_head() -> str:
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    except Exception:
        return 'UNKNOWN'


def git_branch() -> str:
    try:
        return subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    except Exception:
        return 'UNKNOWN'


def first_snapshot(input_npz: str):
    d = np.load(input_npz)
    kh = np.asarray(d['k_native_h'], float)
    z = np.asarray(d['z_native'], float)
    db = np.asarray(d['d_b'], float)
    idx, kmiss = base.mode_indices(kh)
    if kmiss > 1e-12:
        raise RuntimeError(f'k-mode mismatch {kmiss}')
    db6 = db[idx, :]
    it = int(np.argmax(z))
    beta = 1.0
    kind = 'sharp'
    _, source, a = base.source_for(db6[:, it], z[it], base.NX_PRIMARY)
    rhs = source / (1.0 + beta)
    return int(it), float(z[it]), float(a), beta, kind, rhs


def summarize_route(route: str, rhs, a: float, beta: float, kind: str) -> dict:
    print(f'ROUTE_START route={route}', flush=True)
    t0 = time.perf_counter()
    out = r3.anchor_route_solve(rhs, a, beta, kind, base.NX_PRIMARY, route)
    dt = time.perf_counter() - t0
    summary = dict(out.get('route_summary', {}))
    result = {
        'route': route,
        'success': bool(out.get('success', False)),
        'reason': str(out.get('reason')),
        'wall_seconds': float(dt),
        'iterations': int(out.get('iterations', 0)),
        'final_solver_relative_residual': float(out.get('history', [float('nan')])[-1]),
        'route_summary': summary,
        'endpoint_valid': False,
        'endpoint_diagnostics': None,
    }
    if out.get('success', False):
        ok, diag = r3.endpoint_valid(out['chi'], rhs, a, beta, kind)
        result['endpoint_valid'] = bool(ok)
        result['endpoint_diagnostics'] = diag
    print(
        f"ROUTE_END route={route} success={result['success']} reason={result['reason']} "
        f"endpoint_valid={result['endpoint_valid']} wall={dt:.3f}s",
        flush=True,
    )
    print('ROUTE_SUMMARY ' + json.dumps(result, sort_keys=True), flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-npz', required=True)
    ap.add_argument('--input-zip-sha256', default='')
    ap.add_argument('--json-out', default='results/nl1c6r3_blocking_branch_z6_sharp_beta1.json')
    args = ap.parse_args()

    input_path = Path(args.input_npz)
    if not input_path.is_file():
        raise FileNotFoundError(input_path)

    it, z, a, beta, kind, rhs = first_snapshot(args.input_npz)
    print('NL1C6R3_BLOCKING_BRANCH_CONFIRMATION_START', flush=True)
    print(f'index={it} z={z:.16g} a={a:.16g} beta={beta} kind={kind}', flush=True)
    print(f'git_head={git_head()} branch={git_branch()}', flush=True)

    t0 = time.perf_counter()
    screened = summarize_route('screened', rhs, a, beta, kind)
    mass = summarize_route('mass', rhs, a, beta, kind)
    total = time.perf_counter() - t0

    neither_valid = not screened['endpoint_valid'] and not mass['endpoint_valid']
    blocking_snapshot = bool(neither_valid)

    payload = {
        'label': 'NL1C6R3_LOCAL_BLOCKING_BRANCH_CONFIRMATION',
        'diagnostic_only': True,
        'production_solver_changed': False,
        'physical_equations_changed': False,
        'physical_gates_changed': False,
        'historical_results_unchanged': True,
        'input_npz': str(input_path),
        'input_npz_sha256': sha256_file(input_path),
        'input_zip_sha256_declared': args.input_zip_sha256,
        'git_head': git_head(),
        'git_branch': git_branch(),
        'python': sys.version,
        'platform': platform.platform(),
        'numpy': np.__version__,
        'scipy': __import__('scipy').__version__,
        'snapshot': {'index': it, 'z': z, 'a': a},
        'kind': kind,
        'beta': beta,
        'screened': screened,
        'mass': mass,
        'neither_route_residual_valid_at_theta1': blocking_snapshot,
        'blocking_interpretation': (
            'This snapshot blocks a full NL1C6R3 PASS under the existing preregistered rule if reproduced: '
            'neither constitutive anchor produced a residual-valid theta=1 endpoint.'
            if blocking_snapshot else
            'At least one route produced a residual-valid theta=1 endpoint; this snapshot is not a blocker.'
        ),
        'full_NL1C6R3_classification_assigned_here': False,
        'total_wall_seconds': float(total),
    }

    outpath = Path(args.json_out)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')
    print(f'BLOCKING_SNAPSHOT={blocking_snapshot}', flush=True)
    print(f'JSON={outpath}', flush=True)
    print(f'TOTAL_WALL={total:.3f}s', flush=True)
    print('NL1C6R3_BLOCKING_BRANCH_CONFIRMATION_END', flush=True)


if __name__ == '__main__':
    main()
