#!/usr/bin/env python3
"""D25R1 synthetic regression + explicit negative control of D25 r0 beta broadcasting.

Loads only AST of two already-present scripts. No physical parents or source import.
"""
import ast, math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
TINY=1e-300

def extract(path):
    tree=ast.parse(path.read_text())
    funcs=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in ('step','integrate','manufactured_test')]
    assert {n.name for n in funcs}=={'step','integrate','manufactured_test'}
    ns={'np':np,'math':math,'TINY':TINY}
    exec(compile(ast.Module(body=funcs,type_ignores=[]),str(path),'exec'),ns)
    return ns

class Dummy:
    def _canonical_operator_matrices(self,*args):
        return np.zeros((8,8),complex),np.eye(8,dtype=complex)
    def _dense_equilibrated_solve(self,K,rhs):
        result=np.linalg.solve(K,rhs)
        defect=K@result-rhs
        scale=max(np.linalg.norm(K@result),np.linalg.norm(rhs),TINY)
        return result,{'scaled_relative_L2_residual_max':float(np.linalg.norm(defect)/scale)}

def main():
    old=extract(ROOT/'ge19/h4f3d25_first_interval_shift_substep_decision.py')
    new=extract(ROOT/'ge19/h4f3d25r1_first_interval_shift_substep_decision.py')
    h=0.4;dummy=Dummy();zero=np.zeros((8,1),complex)
    def full_main(t):return np.tile([11.,22.,33.],(6,1)).astype(complex)
    def full_cons(t):return np.zeros((2,3),complex)
    # Negative control: reproduce the exact silent old array broadcasting.
    old_y,_=old['step'](dummy,None,None,None,'C_star',1.,zero,0.,h,full_main,full_cons)
    assert old_y.shape==(8,3) and np.allclose(old_y[0],h*np.array([11.,22.,33.]))
    old_integ,_=old['integrate'](dummy,None,None,None,'C_star',1.,np.zeros(8,complex),0.,h,full_main,full_cons,1)
    assert old_integ.shape==(8,) and abs(old_integ[0]-11*h)<1e-12
    print('GE19_D25R1_OLD_BROADCAST_BUG_NEGATIVE_CONTROL_PASS',flush=True)
    try:
        new['step'](dummy,None,None,None,'C_star',1.,zero,0.,h,full_main,full_cons)
    except RuntimeError as err:
        assert 'beta column mismatch' in str(err)
    else:raise RuntimeError('D25R1 failed to reject batched source/single-column state')
    for idx,target in ((0,11.),(1,22.),(2,33.)):
        def one_main(t,idx=idx):return full_main(t)[:,idx:idx+1]
        def one_cons(t,idx=idx):return full_cons(t)[:,idx:idx+1]
        for n in (1,2,4,8):
            y,err=new['integrate'](dummy,None,None,None,'C_star',1.,np.zeros(8,complex),0.,h,one_main,one_cons,n)
            assert y.shape==(8,) and np.allclose(y[:6],h*target,rtol=1e-13,atol=1e-13)
            assert np.allclose(y[6:],0) and err<1e-12
    old['manufactured_test']()
    new['manufactured_test']()
    assert 'GE19_D25R1_FIRST_INTERVAL_SHIFT_SUBSTEP_BETA_ALIGNED_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED' in (ROOT/'ge19/h4f3d25r1_first_interval_shift_substep_decision.py').read_text()
    print('GE19_D25R1_STATIC_BETA_ISOLATION_AND_RADAU_REFINEMENT_PASS',flush=True)

if __name__=='__main__':main()
