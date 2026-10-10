#!/usr/bin/env python3
"""D30 side-effect-free manufactured test of the exact D30 production pair code."""
from __future__ import annotations
import ast,hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'ge19/h4f3d30_direct_ge06_mode_pair_audit.py'
PRE=ROOT/'ge19/h4f3d30_direct_ge06_mode_pair_audit_prereg.json'
LOCK=ROOT/'ge19/h4f3d30_direct_ge06_mode_pair_audit_lock.json'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
assert pre['classification']=='GE19_D30_PREEXEC_ORIGINAL_GE06_DIRECT_SIGNED_PAIR_DIAGNOSTIC'
assert tuple(pre['first_order_modes'])==(3,5,8,10,15,20)
assert pre['expected_support']=={'1':False,'14':False,'23':True,'30':True,'35':True,'40':True}
assert not pre['allow_production_source_replacement']
for key,expected in lock['sha256_local_files'].items():
    p=ROOT/key
    if not p.is_file() or sha(p)!=expected:raise RuntimeError('D30 source lock FAIL '+key)
for collection in ('frozen_outputs_sha256','frozen_source_sha256'):
    for name,val in pre[collection].items():
        if len(val)!=64 or any(c not in '0123456789abcdef' for c in val):
            raise RuntimeError('D30 malformed prereg SHA '+name)

# Extract the ACTUAL two production functions without importing the project
# (the project imports symbolic generators and/or requires user-local archives).
tree=ast.parse(SRC.read_text())
names=('action_eval','mode_pair_partials')
nodes=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in names]
assert {x.name for x in nodes}==set(names)
ns={'np':np}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SRC),'exec'),ns)
fn=ns['mode_pair_partials']
nt=3
head=(np.ones(nt),np.ones(nt),np.ones(nt))
tail=(0.1,1.9,1.0,0.2,0.7)
def quad(*a):
    v=np.asarray(a[3],complex);w=np.asarray(a[4],complex)
    return v*v+3*v*w+2*w*w
class Fake:
    f_c2={'b_f':quad,'b_x':lambda *a:2*quad(*a)}
def jets(z,w):
    return (np.full(nt,z,complex),np.full(nt,w,complex),*(np.zeros(nt,complex) for _ in range(13)))
v3=jets(1+2j,2-1j)
v5=jets(-3+1j,1+0.5j)
v20=jets(0.5-0.4j,-1+0.2j)
signed={3:v3,-3:tuple(np.conjugate(a) for a in v3),
        5:v5,-5:tuple(np.conjugate(a) for a in v5),
        20:v20,-20:tuple(np.conjugate(a) for a in v20)}
val0,pairs=fn(1,signed,Fake(),head,tail,nt)
assert pairs==[] and all(not np.any(z) for z in val0.values())
val0,pairs=fn(14,signed,Fake(),head,tail,nt)
assert pairs==[] and all(not np.any(z) for z in val0.values())
val8,pairs=fn(8,signed,Fake(),head,tail,nt)
want8=quad(*(head+tuple(x+y for x,y in zip(v3,v5))+tail))-quad(*(head+v3+tail))-quad(*(head+v5+tail))
assert pairs==[[3,5]] and np.allclose(val8['b_f'],want8,rtol=1e-13,atol=1e-13)
val6,pairs=fn(6,signed,Fake(),head,tail,nt)
assert pairs==[[3,3]] and np.allclose(val6['b_f'],quad(*(head+v3+tail)))
val40,pairs=fn(40,signed,Fake(),head,tail,nt)
assert pairs==[[20,20]] and np.allclose(val40['b_f'],quad(*(head+v20+tail)))
val2,pairs=fn(2,signed,Fake(),head,tail,nt)
want2=quad(*(head+tuple(x+y for x,y in zip(signed[-3],v5))+tail))-quad(*(head+signed[-3]+tail))-quad(*(head+v5+tail))
assert pairs==[[-3,5]] and np.allclose(val2['b_f'],want2,rtol=1e-13,atol=1e-13)
# Negative controls: adding a new first-order mode really turns on a formerly
# forbidden pair, and the wrong cross-factor does not reproduce the source.
signed11={**signed,11:jets(1+0.2j,-0.3+0.8j)}
signed11[-11]=tuple(np.conjugate(a) for a in signed11[11])
_,m14pairs=fn(14,signed11,Fake(),head,tail,nt)
assert [3,11] in m14pairs
signed4={**signed,4:jets(0.2+0.4j,0.5+0.7j)}
signed4[-4]=tuple(np.conjugate(a) for a in signed4[4])
_,m1pairs=fn(1,signed4,Fake(),head,tail,nt)
assert [-4,5] in m1pairs
assert np.linalg.norm(val8['b_f']-want8/2)>1e-12
code=SRC.read_text()
assert "'original_StageE_Y_main_six_by_128_by_41':sources[0.1]['Y_H3']" in code
assert "'production_GE06_source_modified':False" in code
assert "'no_mode_exclusion':True" in code
print('GE19_D30_MANUFACTURED_EXACT_PAIR_DIAGONAL_CROSS_NEGATIVE_CONTROLS_PASS',flush=True)
print('GE19_D30_SOURCE_SHA_AND_NONANALYTIC_Y_RETENTION_STATIC_PASS',flush=True)
