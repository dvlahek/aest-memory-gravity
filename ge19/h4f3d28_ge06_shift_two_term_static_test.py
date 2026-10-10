#!/usr/bin/env python3
"""Import-free synthetic test of D28 transparent original GE06 assembler wrapper."""
from __future__ import annotations
import ast,hashlib
from pathlib import Path
import numpy as np
p=Path(__file__).with_name('h4f3d28_ge06_shift_two_term_provenance.py')
source=p.read_text()
ast.parse(source)
fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='capture_ge06_b_terms')
ns={'np':np}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(p),'exec'),ns)
wrap=ns['capture_ge06_b_terms']
class FakeR7:
    def spectral_dx(self,arr,kfund):return np.asarray(arr)*float(kfund)
    def assemble_ga_local(self,pd,Dt,k=None,spatial_real=False,kfund=None):
        return {'b':pd['b_f']-self.spectral_dx(pd['b_x'],kfund)}
orig=FakeR7()
fs=np.array([[1.,-2.,3.,-4.],[4.,0.,-1.,2.],[0.5,0.,0.,-0.5]])
bx=np.array([[0.25,-1.,0.5,-2.],[1.,0.,-0.5,2.],[1.,1.,2.,3.]])
pd={'b_f':fs,'b_x':bx}
captured=[]; f=wrap(orig,(3,4),captured)
r=f(pd,None,kfund=2.,spatial_real=True)
assert np.array_equal(r['b'],fs-2*bx)
assert len(captured)==1 and np.array_equal(captured[0]['minus_b_f']+captured[0]['plus_dx_b_x'],-r['b'])
assert np.array_equal(captured[0]['minus_b_f'],-fs)
assert np.array_equal(captured[0]['plus_dx_b_x'],2*bx)
for bad in ({'b_f':fs[:2],'b_x':bx[:2]}, {'b_f':fs,'b_x':np.ones((3,3))}, {'b_f':np.full_like(fs,np.nan),'b_x':bx}):
    try: f(bad,None,kfund=2.,spatial_real=True)
    except RuntimeError: pass
    else: raise AssertionError('D28 negative shape/nonfinite gate missed')
try:f(pd,None,kfund=2.,spatial_real=False)
except RuntimeError:pass
else:raise AssertionError('D28 wrong representation gate missed')
class WrongSign(FakeR7):
    def assemble_ga_local(self,pd,Dt,k=None,spatial_real=False,kfund=None):
        return {'b':pd['b_f']+self.spectral_dx(pd['b_x'],kfund)}
f2=wrap(WrongSign(),(3,4),[])
try:f2(pd,None,kfund=2.,spatial_real=True)
except RuntimeError:pass
else:raise AssertionError('D28 wrong GE06 sign gate missed')
assert 'return result' in source and 'r7.assemble_ga_local=old_ga' in source
print('GE19_D28_MANUFACTURED_ORIGINAL_GE06_EB_TWO_TERM_AND_WRONG_SIGN_NEGATIVE_CONTROLS_PASS',flush=True)
