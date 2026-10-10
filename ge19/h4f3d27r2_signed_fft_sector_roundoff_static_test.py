#!/usr/bin/env python3
"""D27R2 implementation-only Nx repair and original-failure negative controls."""
from pathlib import Path
import ast, hashlib
import numpy as np
base=Path(__file__).parent
r1=base/'h4f3d27r1_signed_fft_sector_roundoff_audit.py'
r2=base/'h4f3d27r2_signed_fft_sector_roundoff_audit.py'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r1)=='700abcf1c0123a1f808b50f97ff75b14b450950ef3422558478569a3b545b33a'
old=r1.read_text();new=r2.read_text()
assert 'n0=float(np.sum(np.abs(real3[0,0])+np.abs(real3[1,0]))/nx)' in old
assert 'n1=float(np.sum(np.abs(real3[0,1])+np.abs(real3[1,1]))/nx)' in old
assert 'n0=real_sector_l1_scale(real3,0,len(x),int(pre[\'nx\']))' in new
assert 'n1=real_sector_l1_scale(real3,1,len(x),int(pre[\'nx\']))' in new
assert 'n0=float(np.sum(np.abs(real3[0,0])+np.abs(real3[1,0]))/nx)' not in new
assert 'n1=float(np.sum(np.abs(real3[0,1])+np.abs(real3[1,1]))/nx)' not in new
tr=ast.parse(new)
fn=[n for n in tr.body if isinstance(n,ast.FunctionDef) and n.name=='real_sector_l1_scale']
assert len(fn)==1
ns={'np':np}
exec(compile(ast.Module(body=fn,type_ignores=[]),str(r2),'exec'),ns)
f=ns['real_sector_l1_scale']
g=np.array([[1.,-2.,3.,-4.],[4.,0.,-1.,2.],[0.5,0.,0.,-0.5]])
m=-g+0.25
arr=np.stack((g,m,g+m))
for t in (0,1):
    expected=float(np.sum(np.abs(g[t])+np.abs(m[t]))/4)
    assert f(arr,t,3,4)==expected
for bad,index,nt,nx in [(arr,0,3,5),(arr,0,2,4),(arr,2,3,4),(arr[:2],0,3,4),(arr[:,:,:3],0,3,4),(arr,0,3,0)]:
    try:f(bad,index,nt,nx)
    except RuntimeError:pass
    else:raise AssertionError('D27R2 negative shape/time control failed')
nonfinite=arr.copy();nonfinite[0,0,0]=np.nan
try:f(nonfinite,0,3,4)
except RuntimeError:pass
else:raise AssertionError('D27R2 nonfinite control failed')
print('GE19_D27R2_NX_DEFINED_AND_DIMENSION_NEGATIVE_CONTROLS_PASS',flush=True)
print('GE19_D27R2_ORIGINAL_D27R1_NAMEERROR_REPRODUCTION_AND_IMMUTABLE_SOURCE_PASS',flush=True)
