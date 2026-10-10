#!/usr/bin/env python3
"""D24 manufactured invariants without importing original repo physics."""
from pathlib import Path
import ast,numpy as np
from scipy.interpolate import PchipInterpolator
p=Path(__file__).with_name('h4f3d24_dense_first_interval_H3_source_transport.py')
s=p.read_text();tree=ast.parse(s)
funcs={n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
need={'projected_initial','original_radau_first_step','transport','source_on_grid','main'}
assert need<=funcs
assert 'D22A_SCIENCE_FAIL_immutable=True' in s
assert 'H4_Z21_solve_performed=False' in s
assert 'q20_B20_recomputed=False' in s
assert '[(14,2),(1,0),(40,2)]' in s
# First 9 sub4 knots exactly cover 2 coarse intervals, and PCHIP interpolates
# the manufactured degree-1 source exactly at the 1/3 Radau stage.
x=np.linspace(-1.,-0.9,9);y=2*x+3+1j*(4*x-1)
v=PchipInterpolator(x,y.real)(x[0]+(x[4]-x[0])/3)+1j*PchipInterpolator(x,y.imag)(x[0]+(x[4]-x[0])/3)
truth=2*(x[0]+(x[4]-x[0])/3)+3+1j*(4*(x[0]+(x[4]-x[0])/3)-1)
assert abs(v-truth)<1e-12
print('GE19_D24_MANUFACTURED_SUB4_STAGE_SOURCE_AND_SCOPE_PASS',flush=True)
# Test the actual D24 one-step function body against a manufactured constant
# eight-state scalar-decay ODE without importing any mutable science modules.
fnode=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='original_radau_first_step')
ns={'np':np};exec(compile(ast.fix_missing_locations(ast.Module(body=[fnode],type_ignores=[])),str(p),'exec'),ns)
class Stub:
    def _canonical_operator_matrices(self,*_):return (-.5*np.eye(8),np.zeros((8,8)),None,None,None,None,None,None,None)
    def _dense_equilibrated_solve(self,K,RHS):
        Y=np.linalg.solve(K,RHS)
        return Y,{'scaled_relative_L2_residual_max':float(np.linalg.norm(K@Y-RHS)/max(np.linalg.norm(RHS),1e-300))}
y0=np.arange(1,9,dtype=complex);y1,err=ns['original_radau_first_step'](Stub(),None,None,None,None,None,0.,.025,y0,lambda _t:np.zeros(8,complex))
assert err<1e-12 and np.linalg.norm(y1-np.exp(-.5*.025)*y0)/np.linalg.norm(y0)<1e-8
print('GE19_D24_ORIGINAL_TWO_STAGE_RADAU_MANUFACTURED_DECAY_PASS',flush=True)
