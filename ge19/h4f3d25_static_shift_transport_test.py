#!/usr/bin/env python3
"""Manufactured D25 sign, derivative, and non-certification checks without repo imports."""
import ast
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator

root=Path(__file__).resolve().parent
script=root/'h4f3d25_H3_first_step_shift_transport_decomposition.py'
src=script.read_text()
tr=ast.parse(src)
wanted={'scalar_interp','operator_coefficients','derivative_onesided'}
body=[node for node in tr.body if isinstance(node,ast.FunctionDef) and node.name in wanted]
assert {n.name for n in body}==wanted
ns={'np':np,'PchipInterpolator':PchipInterpolator}
exec(compile(ast.Module(body=body,type_ignores=[]),str(script),'exec'),ns)

class R7:
 def _canonical_operator_matrices(self,*args):
  C=np.zeros((16,10),complex);C[10,0]=2.;C[11,1]=-3.
  WY=np.zeros((10,8),complex);WY[0,0]=1.;WY[1,1]=1.
  WR=np.zeros((10,8),complex);WR[0,0]=1.;WR[1,1]=1.
  M=np.zeros((8,8),complex);F=np.zeros((8,8),complex)
  return M,F,None,None,WY,WR,C,None,None
m,f,ky,ks,*_=ns['operator_coefficients'](R7(),None,None,None,1.,0.)
assert np.array_equal(ky[:2],[2.,-3.])
assert np.array_equal(ks[[0,1,6]],[2.,-3.,-1.])
y=np.zeros(8,complex);s=np.zeros(8,complex);s[6]=4.
g=ky@y+ks@s
assert g==-4. and g!=4.

x=np.linspace(-1,1,11);arr=np.stack((2*x+3,3*x-1),axis=0).astype(complex)
p,pd=ns['scalar_interp'](x,arr)
assert np.max(np.abs(pd(x[0])-[2,3]))<1e-12
assert np.max(np.abs(p(x[4])-arr[:,4]))<1e-12
assert abs(ns['derivative_onesided'](lambda q:q*q,0.2,0.003)-0.4)<1e-12
assert 'D22A_SCIENCE_FAIL_immutable' in src
assert "'Z11_certified':False" in src and "'Z20_certified':False" in src
assert "'new_H3_integration':False" in src and "'q20_B20_recomputed':False" in src
assert 'source_changes' in src and 'allow_nan=False' in src
print('GE19_D25_SIGN_DERIVATIVE_AND_IMMUTABLE_PARENT_NEGATIVE_CONTROLS_PASS',flush=True)
