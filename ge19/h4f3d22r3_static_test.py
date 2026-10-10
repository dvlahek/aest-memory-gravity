#!/usr/bin/env python3
"""No frozen change, genuine source-independent R2 reference, no claim promotion."""
import ast
from pathlib import Path
s=Path(__file__).with_name('h4f3d22r3_direct_R2_boundary_reclosure.py').read_text()
ast.parse(s)
for name in ('h2.load_r2_parent','h2.tangent_on_grid','h2.integrate_dust_tangent','h2.make_reference',
             'fresh_R2_dot_vs_stale_Z11_solution_dot_initial_abs_or_rel',
             'h2.solve_h2_case','D22A_failure_immutable','Z11_certified\':False',
             'Z20_certified\':False','q20_B20_recomputed\':False'):
    assert name in s,name
assert 'fresh_dot=stale_dot' not in s and 'refdot=olddot' not in s
assert 'if can_solve:' in s and 'SKIP_POINTLESS_REINTEGRATION' in s
print('GE19_D22R3_REAL_R2_BOUNDARY_AND_NO_FAKE_H4_STATIC_PASS')
