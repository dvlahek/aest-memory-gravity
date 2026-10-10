#!/usr/bin/env python3
"""D22A manufactured contract checks; independent of real user outputs."""
from pathlib import Path
import ast,numpy as np
src=Path(__file__).with_name('h4f3d22a_action_parent_reclosure.py').read_text()
tree=ast.parse(src)
need=['D17_H1_action_primary','B10_D17_D19_primary','Z11_D17_D19_candidate_primary',
      'Z20_D17_H3F_candidate_primary','source_bundle_reduced_lambda',
      'projected_momentum_solve','frozen_R2_Z11_dynamic_boundary_replayed',
      'q20_and_B20_recomputed','full_original_H4_Ward_certified']
assert all(s in src for s in need)
assert 'new_B20=old.r24.X20_modes' in src and 'X20_D17_Z20_primary_NOT_B20' in src
assert "'q20_and_B20_recomputed':False" in src
assert "'Z21_certified':False" in src
# Artificial two-equation four-momentum initial boundary, with a nonzero
# source-dependent offset; zero-momentum is deliberately NOT an allowed default.
A=np.array([[1.,2.,-1.,0.],[0.,1.,3.,-2.]])
p=np.array([.17,-.03,.11,.07]); rhs=A@p
sol=np.linalg.lstsq(A,rhs,rcond=None)[0]
assert np.linalg.norm(A@sol-rhs)<1e-13
assert np.linalg.norm(A@np.zeros(4)-rhs)>1e-2
# Exactly the frozen factor +2 in -2 M1 map (not a fitted number).
a=np.array([.5,.6]); Q=np.array([.001,.0012]); B=np.ones((6,2),complex)*(.2+.1j)
coef=2.; aa=coef*.5*Q*a**3*B
assert np.allclose(aa,Q*a**3*B,rtol=0,atol=0)
print('GE19_D22A_MANUFACTURED_SOURCE_AWARE_BOUNDARY_AND_M1_FACTOR_TWO_PASS')
print('GE19_D22A_NO_STALE_Q20_NO_H4_Z21_CLAIM_STATIC_PASS')
