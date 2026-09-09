#!/usr/bin/env python3
"""Local-only runtime diagnostic for NL1C6R3.

This script does not change equations, tolerances, gates, or the production
solver.  It traces the first production branch (z=max native, simple,
beta=1) and prints entry/exit timing for fixed-theta seed solves and
pseudo-arclength correctors.  Intended to identify where long runs spend time.
"""
import argparse
import time
from pathlib import Path

import numpy as np

from nl1c6 import full_j_baryonic_reclosure as base
from nl1c6r3 import fixed_source_constitutive_homotopy as r3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-npz', required=True)
    ap.add_argument('--route', choices=('screened','mass'), default='screened')
    args = ap.parse_args()

    d = np.load(args.input_npz)
    kh = np.asarray(d['k_native_h'], float)
    z = np.asarray(d['z_native'], float)
    db = np.asarray(d['d_b'], float)
    idx, kmiss = base.mode_indices(kh)
    if kmiss > 1e-12:
        raise RuntimeError(f'k-mode mismatch {kmiss}')
    db6 = db[idx, :]

    it = int(np.argmax(z))
    beta = 1.0
    kind = 'simple'
    _, source, a = base.source_for(db6[:, it], z[it], base.NX_PRIMARY)
    rhs = source / (1.0 + beta)

    print('NL1C6R3_LOCAL_TRACE_START', flush=True)
    print(f'z={z[it]:.16g} a={a:.16g} beta={beta} kind={kind} route={args.route}', flush=True)
    print('theta_seeds=' + ','.join(f'{x:.12e}' for x in r3.THETA_SEEDS), flush=True)

    original_fixed = r3.fixed_theta_solve
    original_corrector = r3.augmented_corrector
    fixed_calls = 0
    corr_calls = 0
    tglobal = time.perf_counter()

    def traced_fixed(rhs_, a_, beta_, kind_, theta_, route_, initial_):
        nonlocal fixed_calls
        fixed_calls += 1
        tc = time.perf_counter()
        print(f'FIXED_ENTER call={fixed_calls} theta={float(theta_):.12e} route={route_} elapsed_total={tc-tglobal:.3f}s', flush=True)
        out = original_fixed(rhs_, a_, beta_, kind_, theta_, route_, initial_)
        te = time.perf_counter()
        hist = out.get('history', [])
        residual = float(hist[-1]) if hist else float('nan')
        print(f'FIXED_EXIT  call={fixed_calls} theta={float(theta_):.12e} success={out.get("success")} reason={out.get("reason")} newton={out.get("iterations")} residual={residual:.12e} dt={te-tc:.3f}s elapsed_total={te-tglobal:.3f}s', flush=True)
        return out

    def traced_corrector(rhs_, a_, beta_, kind_, route_, chi_pred_, theta_pred_, ty_, tt_, chi_scale_):
        nonlocal corr_calls
        corr_calls += 1
        tc = time.perf_counter()
        print(f'ARC_ENTER   call={corr_calls} theta_pred={float(theta_pred_):.12e} tt={float(tt_):.12e} elapsed_total={tc-tglobal:.3f}s', flush=True)
        out = original_corrector(rhs_, a_, beta_, kind_, route_, chi_pred_, theta_pred_, ty_, tt_, chi_scale_)
        te = time.perf_counter()
        print(f'ARC_EXIT    call={corr_calls} theta={float(out.get("theta", float("nan"))):.12e} success={out.get("success")} reason={out.get("reason")} newton={out.get("iterations")} residual={float(out.get("field_relative_residual", float("nan"))):.12e} dt={te-tc:.3f}s elapsed_total={te-tglobal:.3f}s', flush=True)
        return out

    r3.fixed_theta_solve = traced_fixed
    r3.augmented_corrector = traced_corrector
    try:
        out = r3.anchor_route_solve(rhs, a, beta, kind, base.NX_PRIMARY, args.route)
    finally:
        r3.fixed_theta_solve = original_fixed
        r3.augmented_corrector = original_corrector

    total = time.perf_counter() - tglobal
    summary = out.get('route_summary', {})
    print(f'TRACE_RESULT success={out.get("success")} reason={out.get("reason")} total={total:.3f}s', flush=True)
    print('TRACE_SUMMARY', summary, flush=True)
    print('NL1C6R3_LOCAL_TRACE_END', flush=True)


if __name__ == '__main__':
    main()
