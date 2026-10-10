#!/usr/bin/env python3
"""Pure manufactured D26 derivative/finite ledger and wrong-sign controls."""
import ast
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
p=Path(__file__).with_name('h4f3d26_action_shift_source_transport_ledger.py')
tree=ast.parse(p.read_text())
wanted={'signed_ledger','signed_derivative','source_and_derivative','one_sided'}
body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
assert {n.name for n in body}==wanted
ns={'np':np,'PchipInterpolator':PchipInterpolator}
exec(compile(ast.Module(body=body,type_ignores=[]),str(p),'exec'),ns)
# g=(2+3x)(2+x)+(5+x)(3+2x)-(3+2x); g'(0)=19 exactly.
ky0=np.array([2.]);ky1=np.array([2+3*.2]);ks0=np.r_[5.,np.zeros(7)];ks1=ks0.copy();ks1[0]+=.2
# Shift source is s[6], so include a source with equal values at indices 0,6.
s0=np.r_[3.,np.zeros(5),3.,0.];s1=np.r_[3.4,np.zeros(5),3.4,0.]
y0=np.array([2.]);y1=np.array([2.2]);yd=np.array([1.]);sd=np.r_[2.,np.zeros(5),2.,0.]
terms,ds=ns['signed_ledger'](ky0,ky1,ks0,ks1,y0,y1,s0,s1)
g0=ky0@y0+ks0@s0-s0[6];g1=ky1@y1+ks1@s1-s1[6]
assert abs(ds-(g1-g0))<1e-13 and all(np.isfinite(list(terms.values())))
dt,dg=ns['signed_derivative'](ky0,ks0,np.array([3.]),np.r_[1.,np.zeros(7)],y0,yd,s0,sd)
assert abs(dg-19.)<1e-13,(dg,dt)
assert abs((dg+2*sd[6])-19.)>1.0,'wrong-sign negative control failed'
x=np.linspace(0,1,11)
arr=np.zeros((8,len(x)),complex);arr[0]=3+2*x;arr[6]=3+2*x
class Holder:pass
src={1.0:{'rhs':np.zeros((6,len(x),41),complex),'rhs_constraint':np.zeros((2,len(x),41),complex)}}
src[1.0]['rhs'][0,:,14]=arr[0]
src[1.0]['rhs_constraint'][0,:,14]=arr[6]
si,sdot=ns['source_and_derivative'](x,src,14,0)
assert abs(si(0)[6]-3)<1e-13 and abs(sdot(0)[6]-2)<1e-11
assert abs(ns['one_sided'](lambda t:t*t,.1,.0005)-.2)<1e-11
print('GE19_D26_MANUFACTURED_SIGNED_TRANSPORT_SOURCE_DERIVATIVE_NEGATIVE_CONTROLS_PASS',flush=True)
