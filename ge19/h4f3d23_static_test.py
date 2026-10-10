#!/usr/bin/env python3
"""D23 static scope + independent manufactured nonzero-q projection test."""
from __future__ import annotations
import ast, json, pathlib, types
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
S=ROOT/'ge19/h4f3d23_action_constraint_boundary_transport.py'
T=ast.parse(S.read_text())
code=S.read_text()
for forbidden in ('Z11_certified\':True','Z20_certified\':True','Z21_certified\':True',
                  'full_H4_Ward_certified\':True','lensing_licensed\':True'):
    assert forbidden not in code,forbidden
assert 'r18.projected_momentum_solve(A,b-A@pold)' in code
assert 'offset=WY@base+WR@src8' in code
assert 'H3_40_modes_not_recomputed\':True' in code
namespace={'np':np,'TINY':1e-300}
class MockR18:
    @staticmethod
    def projected_momentum_solve(A,b):
        p,res,rank,s=np.linalg.lstsq(A,b,rcond=None)
        return p,{'rank':rank,'augmented_rank':np.linalg.matrix_rank(np.c_[A,b]),
                  'scaled_relative_residual_final':float(np.linalg.norm(A@p-b)/max(np.linalg.norm(b),1e-300))}
class FakeR7:
    def __init__(self):
        self.C=np.zeros((14,10),complex)
        self.C[4,2]=1.;self.C[4,6]=1.
        self.C[10,3]=2.;self.C[10,7]=1.
        self.C[12,8]=1.
        self.WY=np.zeros((10,8),complex)
        self.WY[2:6,:4]=np.eye(4)
        self.WY[6:10,4:8]=np.eye(4)
        self.WR=np.zeros((10,8),complex)
    def _initial_canonical_state(self,mod6,mod7,bg,tag,k,x,q0,v0,rhs0):
        y=np.r_[q0,v0]
        return y,self.WY@y,{}
    def _canonical_operator_matrices(self,mod6,mod7,bg,tag,k,x):
        return None,None,None,None,self.WY,self.WR,self.C,{},{}
    def _constraint_backward_error(self,row,w,target):
        numerator=abs(row@w-target);scale=max(np.sum(np.abs(row*w)),abs(target),1e-300)
        return {'metric':float(numerator/scale),'absolute_residual':float(numerator),
                'scale':float(scale),'contribution_scale':float(np.sum(np.abs(row*w)))}
namespace.update(r18=MockR18)
for node in T.body:
    if isinstance(node,ast.FunctionDef) and node.name in ('rel','zpair','row_data','project_p','h3_shift_transport'):
        m=ast.Module(body=[node],type_ignores=[])
        exec(compile(ast.fix_missing_locations(m),str(S),'exec'),namespace)
r=FakeR7()
q0=np.array([1+2j,-.4+.2j,.3,-.1],complex)
v0=np.zeros(4,complex)
s=np.zeros(8,complex)
y,diag,vnew=namespace['project_p'](r,None,None,{},'C_star',1.,0.,q0,v0,s)
assert np.array_equal(y[:4],q0)
assert abs(y[4]+q0[0])<1e-12 and abs(y[5]+2*q0[1])<1e-12
assert diag['projection_rank']==2 and diag['projection_augmented_rank']==2
assert diag['projected_initial_rows']['shift']['metric']<1e-12
assert diag['projected_initial_rows']['lapse']['metric']<1e-12
assert diag['initial_R2_dot_absolute_L2_change']>0
# Negative control: forgetting nonzero-q offset produces nonzero constraints.
assert abs(r.C[4]@r.WY@np.r_[q0,np.zeros(4)])>0
# Diagnostic-only contract must survive even for a successful projection.
# Independent H3 source-transport sign test: g(x)=-alpha*x, gprime=-alpha.
class FakeH3(FakeR7):
    BETAS=(1.,.5,.1)
    FOURIER_N=(3,5,8,10,15,20)
    g9=types.SimpleNamespace(K_REQ=np.array([0.03]))
    def __init__(self):
        super().__init__()
        self.C[0:4,6:10]=np.eye(4)
        self.C[10,6]=1.
        self.M=np.zeros((8,8),complex);self.F=np.zeros((8,8),complex)
    def _canonical_operator_matrices(self,mod6,mod7,bg,tag,k,x):
        return self.M,self.F,None,None,self.WY,self.WR,self.C,{},{}
    def _source_interp(self,x,sources,mode):
        def rhs(t):return np.zeros((6,3),complex)
        def con(t):
            c=np.zeros((2,3),complex);c[0]=2.5*t
            return c
        return rhs,con
ff=FakeH3()
try:
    namespace['h3_shift_transport'](ff,None,None,{},'C_star',1,0,
        np.array([0.,.1]),{},np.zeros((3,1,4),complex),
        np.zeros((3,1,6,2),complex),np.zeros((3,1,4,2),complex))
except Exception as e:
    raise AssertionError('manufactured H3 transport did not complete') from e
item=namespace['h3_shift_transport'](ff,None,None,{},'C_star',1,0,
    np.array([0.,.1]),{},np.zeros((3,1,4),complex),
    np.zeros((3,1,6,2),complex),np.zeros((3,1,4,2),complex))
assert abs(item['gprime0_complex'][0]+2.5)<1e-9
assert abs(item['g1_archived_complex'][0]+.25)<1e-9
assert abs(item['linear_first_step_prediction_complex'][0]+.25)<1e-9
assert item['gprime_step_halving_relative_report_only']<1e-8
print('GE19_D23_MANUFACTURED_H3_SOURCE_TRANSPORT_SIGN_AND_FIRST_STEP_PASS')
print('GE19_D23_NONZERO_R2_Q_OFFSET_LAPSE_SHIFT_PROJECTION_AND_NEGATIVE_CONTROL_PASS')
print('GE19_D23_NO_FAKE_H2_H3_H4_CERTIFICATION_STATIC_PASS')
