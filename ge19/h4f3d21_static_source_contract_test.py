#!/usr/bin/env python3
"""Offline D21 contract test: exact scalar-only patch, physical action and fail-closed science."""
import ast,pathlib
src=pathlib.Path(__file__).with_name('h4f3d21_actual_GE05_phase_safe_M2_reclosure.py').read_text()
core=pathlib.Path(__file__).with_name('h4f3d21_GE05_phase_safe_M2_core.py').read_text()
tr=ast.parse(src); fn={n.name for n in tr.body if isinstance(n,ast.FunctionDef)}
assert {'sha','exact_locks','kahan_add','main'}<=fn
for term in ("ge05.f_c2['pt'](", 'core.current_dot(',
             'old.r24.reconstruct_batched_positive_modes(',
             'd20.canonical_knots_to_h1(',
             "corrected[3]+=fft_delta",'old.GE05_TO_GE06',
             "d20report.get('GE05_M2_FD4_high_phase_temporal_aliasing_closed') is False",
             "'M1_uses_FROZEN_H3G_B20_not_new_q20':True",
             "'new_physical_q20_and_Z11_recomputed':False",
             "'GE05_on_shell_certified':False",
             "'full_original_H4_Ward_certified':False",
             "'Z21_certified':False"):
 assert term in src,term
for term in ('old.r24.evolve_z10(', 'old.reconstruct_m2_source(',
             'np.gradient(', 'def tune(', 'scipy.optimize'):
 assert term not in src,term
assert 'physical_time' in core or 'physical-time' in core
print('GE19_D21_SOURCE_CONTRACT_IMMUTABLE_PARENT_AND_NO_FAKE_H4_PASS',flush=True)
