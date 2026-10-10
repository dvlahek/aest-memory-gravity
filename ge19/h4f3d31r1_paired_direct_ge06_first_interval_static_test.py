#!/usr/bin/env python3
"""Dependency-free manufactured source-swap tests and D30-array control."""
from __future__ import annotations
import ast,hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d31r1_paired_direct_ge06_first_interval_prereg.json'
LOCK=ROOT/'ge19/h4f3d31r1_paired_direct_ge06_first_interval_lock.json'
SOURCE=ROOT/'ge19/h4f3d31r1_paired_direct_ge06_first_interval.py'
pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
assert pre['classification']=='GE19_D31R1_PREEXEC_REMAINDER_ROUNDOFF_AUDIT'
assert pre['cases']==[[14,0.1],[1,1.0],[40,0.1]] and pre['substeps']==[1,8]
for name,want in lock['sha256_local_files'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==want,name
for name,want in pre['frozen_code_sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==want,name
print('GE19_D31R1_SHA_CODE_PREREG_STATIC_RUNNER_LOCK_PASS',flush=True)
ns={}
tree=ast.parse(SOURCE.read_text())
fun=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='candidate_swap']
assert len(fun)==1
exec(compile(ast.Module(body=fun,type_ignores=[]),str(SOURCE),'exec'),{'np':np,'RuntimeError':RuntimeError},ns)
swap=ns['candidate_swap']
a=np.zeros((6,128,41),complex);b=np.zeros((2,128,41),complex)
c=a.copy();d=b.copy();e=a.copy();f=b.copy()
a[3,0,14]=2.5+1j   # original source = unwanted GE06 + retained Y
c[3,0,14]=2.5;e[3,0,14]=0
b[0,0,14]=1e-18;d[0,0,14]=1e-18;f[0,0,14]=0
a[3,0,1]=-1.2+0.1j;c[3,0,1]=-1.2
c[3,0,40]=12;e[3,0,40]=12.0000000001;a[3,0,40]=12.8+0.3j
out=swap(a,b,c,d,e,f)
assert out['rhs'][3,0,14]==1j and out['rhs'][3,0,1]==0.1j
assert out['rhs_constraint'][0,0,14]==0
assert abs(out['rhs'][3,0,40]-(12.8000000001+0.3j))<1e-12
assert not np.array_equal(out['rhs'],a+c+e)
try:swap(a[:,:1],b,c,d,e,f)
except RuntimeError:pass
else:raise AssertionError('GE19_D31R1_NEGATIVE_SHAPE_CONTROL_FAILED')
print('GE19_D31R1_MANUFACTURED_SIGNED_GE06_ONLY_SWAP_AND_Y_RETENTION_NEGATIVE_CONTROLS_PASS',flush=True)
rd=ROOT/'results';jpath=rd/pre['D30_json'];zpath=rd/pre['D30_npz']
assert hashlib.sha256(jpath.read_bytes()).hexdigest()==pre['frozen_results_sha256'][pre['D30_json']]
assert hashlib.sha256(zpath.read_bytes()).hexdigest()==pre['frozen_results_sha256'][pre['D30_npz']]
j=json.loads(jpath.read_text());support=set(j['exact_support_nonnegative'])
assert support==set(pre['expected_support_all'])
with np.load(zpath,allow_pickle=False) as z:
    om=np.asarray(z['original_GE06_main_six_by_128_by_41'],complex)
    dm=np.asarray(z['direct_GE06_main_six_by_128_by_41'],complex)
    oc=np.asarray(z['original_GE06_constraint_two_by_128_by_41'],complex)
    dc=np.asarray(z['direct_GE06_constraint_two_by_128_by_41'],complex)
    y=np.asarray(z['original_StageE_Y_main_six_by_128_by_41'],complex)
    assert om.shape==dm.shape==(6,128,41) and oc.shape==dc.shape==(2,128,41)
    assert y.shape==om.shape and all(np.isfinite(q).all() for q in (om,dm,oc,dc,y))
    for m in range(41):
        if m not in support:assert not np.any(dm[:,:,m]) and not np.any(dc[:,:,m]),m
    for m in pre['required_nonanalytic_y_modes']: assert np.max(np.abs(y[:,:,m]))>0,m
    def rel(a,b):return np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-300)
    ss=sorted(support)
    assert rel(om[:,:,ss],dm[:,:,ss])<=pre['global_supported_GE06_relative_limit']
    assert rel(oc[:,:,ss],dc[:,:,ss])<=pre['global_supported_GE06_relative_limit']
    assert max(rel(om[:,:,40],dm[:,:,40]),rel(oc[:,:,40],dc[:,:,40]))<=pre['m40_unchanged_action_relative_limit']
print('GE19_D31R1_FROZEN_D30_SUPPORT_M40_AND_STAGEE_Y_INPUT_TEST_PASS',flush=True)

# Independent manufactured reproduction of the frozen source-aware two-row
# projection shape/sign contract, without importing the historical physics code.
from types import SimpleNamespace
pnode=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='projection']
assert len(pnode)==1
CM=np.zeros((12,10),complex);CM[4,0]=1.;CM[10,1]=1.
WY=np.zeros((10,8),complex);WY[0,4]=1.;WY[1,5]=1.
WR=np.zeros((10,8),complex)
class FakeOperator:
    def _canonical_operator_matrices(self,*_args):
        return (np.zeros((8,8),complex),np.zeros((8,8),complex),None,None,
                WY,WR,CM,None,None)
def fake_project(A,rhs):
    x=np.linalg.lstsq(A,rhs,rcond=None)[0]
    return x,{'rank':2,'augmented_rank':2,'scaled_relative_residual_final':0.0}
def fake_eval(C,WY_,WR_,source,rhs,con,p):
    w=WY_@np.r_[np.zeros(4,complex),p]+WR_@source
    lapse=abs(C[4]@w-rhs[0]);shift=abs((C[10]+C[11])@w-con[0])
    return {'lapse':{'metric':float(lapse)},'shift':{'metric':float(shift)}}
fakemod=SimpleNamespace(r18=SimpleNamespace(projected_momentum_solve=fake_project,
                                         evaluate_candidate=fake_eval))
pglobals={'np':np,'RuntimeError':RuntimeError,'d22a':fakemod}
pns={}
exec(compile(ast.Module(body=pnode,type_ignores=[]),str(SOURCE),'exec'),pglobals,pns)
project=pns['projection']
rf=lambda _:np.array([[0.,0.,2.],[0.,0.,0.],[0.,0.,0.],
                      [0.,0.,0.],[0.,0.,0.],[0.,0.,0.]],complex)
cf=lambda _:np.array([[0.,0.,-3.],[0.,0.,0.]],complex)
y,pr=project(FakeOperator(),None,None,None,'C_star',1.0,0.0,rf,cf,2)
assert y.shape==(8,) and not np.any(y[:4]) and y[4]==2 and y[5]==-3
assert pr['rank']==2 and pr['augmented_rank']==2 and pr['lapse_relative_backward']==0. and pr['shift_relative_backward']==0.
try:project(FakeOperator(),None,None,None,'C_star',1.0,0.0,lambda t:rf(t)[:,2:3],cf,2)
except RuntimeError:pass
else:raise AssertionError('D31 projection beta shape negative control failed')
print('GE19_D31R1_MANUFACTURED_SOURCE_AWARE_TWO_ROW_BOUNDARY_PROJECTION_PASS',flush=True)

# D31R1 manufactured finite-source split: original D31 hard gate fails from
# subtraction of large analytic GE06 despite globally correct original sum.
helpnode=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='finite_source_roundoff_ledger']
assert len(helpnode)==1
helpns={}
exec(compile(ast.Module(body=helpnode,type_ignores=[]),str(SOURCE),'exec'),
     {'np':np,'rel':rel,'RuntimeError':RuntimeError},helpns)
ledger=helpns['finite_source_roundoff_ledger']
ga=np.zeros((6,128,41),complex);ma=np.zeros_like(ga)
ll=np.zeros_like(ga);y=np.zeros_like(ga)
ga[0,0,40]=1e12;y[0,0,40]=1e-3+2e-4j
full=ga+ma+ll+y
r=ledger(full,ga,ma,ll,y,pre['original_D22A_replay_limit'])
assert r['original_full_source_relative']<=pre['original_D22A_replay_limit']
assert r['original_subtractive_remainder_relative_report_only']>pre['non_GE06_remainder_relative_limit']
assert r['original_subtractive_remainder_abs_l2_report_only']>0
# Signed Y/control error must be detected when the full source is on its
# resolvable scale. Do not turn the original full-source check off.
try:ledger(np.zeros_like(full),np.zeros_like(ga),ma,ll,y,pre['original_D22A_replay_limit'])
except RuntimeError:pass
else:raise AssertionError('D31R1 wrong-sign/source full-scale negative control FAIL')
try:ledger(full[:1],ga,ma,ll,y,pre['original_D22A_replay_limit'])
except RuntimeError:pass
else:raise AssertionError('D31R1 sector dimension negative control FAIL')
assert 'D31 original GE07/Lambda/Y remainder identity FAIL' in (ROOT/'ge19/h4f3d31_paired_direct_ge06_first_interval.py').read_text()
print('GE19_D31R1_MANUFACTURED_FINITE_MAIN_SPLIT_AND_PRESERVED_ORIGINAL_FAILURE_PASS',flush=True)
