#!/usr/bin/env python3
"""Independent source AST and synthetic canonical Radau / Exp negative tests."""
import ast,math
from pathlib import Path
import numpy as np
import sympy as sp
from ge19 import h4f3d17_original_action_dense_H1_core as core

ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'ge19/repair07_window_retarded_reduced_h3_z20_particular.py').read_text()
tree=ast.parse(source)
def fun(name):
    for q in tree.body:
        if isinstance(q,(ast.FunctionDef,ast.AsyncFunctionDef)) and q.name==name:return ast.get_source_segment(source,q)
    raise RuntimeError('D17 original source missing: '+name)
assert 'PchipInterpolator' in fun('_bg_point')
assert '_bg_point(bg,xq)' in fun('_raw_local_outputs')
assert '_local_linear_matrix' in fun('_canonical_operator_matrices')
assert 'a11=5.0/12.0' in fun('_radau2_integrate_canonical')
assert '_dense_equilibrated_solve' in fun('_radau2_integrate_canonical')
print('GE19_D17_ORIGINAL_H1_CANONICAL_OPERATOR_AND_FROZEN_PCHIP_SOURCE_AST_PASS')
Z,Z0,K2=sp.symbols('Z Z0 K2',positive=True)
KQ=4*K2*Z0*Z*sp.exp(Z**2)
Qx=sp.factor(-3*KQ*Z0/sp.diff(KQ,Z))
assert sp.simplify(Qx-(-3*Z0*Z/(1+2*Z**2)))==0
assert sp.simplify(Qx-(-3*Z0*Z/(1+Z)))!=0
assert np.isclose(core.action_Qx_from_Z(.7,1.2),float(Qx.subs({Z:.7,Z0:1.2})),rtol=1e-14)
print('GE19_D17_ORIGINAL_EXP_SCALAR_CHARGE_ACTION_QX_IDENTITY_PASS_WRONG_BRANCH_NEGATIVE_CONTROL_PASS')
A=np.diag(np.linspace(-.5,-1.4,8)).astype(complex)
y0=np.arange(1,9).astype(complex)/10
M=lambda x:A
solve=lambda a,b:(np.linalg.solve(a,b),{'scaled_relative_L2_residual_max':float(np.linalg.norm(a@np.linalg.solve(a,b)-b)/max(np.linalg.norm(b),1e-300))})
x=np.array([0.,.4,.7,1.])
sol={}
for n in (1,2,4):
    fine,y,diag=core.integrate_original_grid(x,y0,n,M,solve)
    assert np.array_equal(fine[::n],x) and diag<1e-12
    sol[n]=np.linalg.norm(y[:,-1]-np.exp(np.diag(A))*y0)
assert sol[4]<sol[2]<sol[1]
d=core.sampled_hermite_ode_defect(fine,y,M)
assert d['midpoint_canonical_ODE_defect_absolute_L2_max_sampled_not_bound']>0
try:core.integrate_original_grid(x,y0,3,M,solve)
except ValueError:pass
else:raise RuntimeError('D17 wrong nsub negative control escaped')
print('GE19_D17_CANONICAL_RADAU_SUBDIVISION_CONVERGENCE_AND_SAMPLED_DEFECT_PASS_NEGATIVE_CONTROL_PASS')
