#!/usr/bin/env python3
"""Offline manufactured controls. Extract D33 pure helpers without importing frozen repo."""
import ast
import hashlib
import json
from pathlib import Path
import numpy as np

root=Path(__file__).resolve().parents[1]
src=root/'ge19/h4f3d33_direct_ge07_paired_first_interval.py'
pre=root/'ge19/h4f3d33_direct_ge07_paired_first_interval_prereg.json'
lock=root/'ge19/h4f3d33_direct_ge07_paired_first_interval_lock.json'
j=json.loads(pre.read_text());lk=json.loads(lock.read_text())
assert j['classification']=='GE19_D33_PREEXEC_DIRECT_GE07_SIGNED_PAIR_AND_PAIRED_FIRST_INTERVAL'
assert tuple(tuple(c) for c in j['cases'])==((14,0.1),(1,1.0),(40,0.1))
assert j['substeps']==[1,8] and j['off_support_modes']==[1,14]
assert j['original_shift_gate']==1e-6 and j['original_boundary_backward_gate']==1e-6
assert j['H3_H4_Z21_lensing_certification'] is False and j['production_source_unchanged']
for filename,want in lk['sha256_local_files'].items():
    assert hashlib.sha256((root/filename).read_bytes()).hexdigest()==want,filename
for want in (*j['frozen_local_code_sha256'].values(),*j['frozen_results_sha256'].values()):
    assert len(want)==64 and all(c in '0123456789abcdef' for c in want)

nodes=ast.parse(src.read_text()).body
names={'rel','signed_ge07_jets','evaluate_c2','direct_ge07_partials'}
subset=[node for node in nodes if isinstance(node,ast.FunctionDef) and node.name in names]
assert len(subset)==len(names)
env={'np':np,'TINY':1e-300}
exec(compile(ast.Module(body=subset,type_ignores=[]),str(src),'exec'),env)

class Toy:
    f_c2={
       'N_f':lambda a,r,N,L,R,b,rho,Tt,Tx:N*Tt,
       'L_f':lambda a,r,N,L,R,b,rho,Tt,Tx:L*rho,
       'R_f':lambda a,r,N,L,R,b,rho,Tt,Tx:R*Tx,
       'b_f':lambda a,r,N,L,R,b,rho,Tt,Tx:Tt*Tx,
       'rho_f':lambda a,r,N,L,R,b,rho,Tt,Tx:N*L,
       'T_t':lambda a,r,N,L,R,b,rho,Tt,Tx:rho*Tt,
       'T_x':lambda a,r,N,L,R,b,rho,Tt,Tx:rho*Tx
    }
nt=5;zero=np.zeros(nt,complex)
v=(np.full(nt,1,dtype=complex), np.full(nt,2,dtype=complex),
   np.full(nt,2,dtype=complex),zero,np.full(nt,3,dtype=complex),
   np.full(nt,4,dtype=complex),np.full(nt,5,dtype=complex))
w=(np.full(nt,7,dtype=complex),np.full(nt,8,dtype=complex),
   np.full(nt,8,dtype=complex),zero,np.full(nt,9,dtype=complex),
   np.full(nt,10,dtype=complex),np.full(nt,11,dtype=complex))
head=(np.ones(nt),2*np.ones(nt))
signed={-5:tuple(z.conj() for z in w),-3:tuple(z.conj() for z in v),3:v,5:w}
part,terms=env['direct_ge07_partials'](8,signed,Toy(),head,nt)
assert terms==[[3,5]],terms
assert np.array_equal(part['N_f'],np.full(nt,1*10+7*4,dtype=complex))
assert np.array_equal(part['b_f'],np.full(nt,4*11+10*5,dtype=complex))
assert not np.array_equal(part['N_f'],np.full(nt,(1*10+7*4)/2,dtype=complex))
diag,terms=env['direct_ge07_partials'](6,signed,Toy(),head,nt)
assert terms==[[3,3]] and np.array_equal(diag['N_f'],np.full(nt,4,dtype=complex))
miss,terms=env['direct_ge07_partials'](1,signed,Toy(),head,nt)
assert terms==[] and all(np.array_equal(a,zero) for a in miss.values())
negative,terms=env['direct_ge07_partials'](2,signed,Toy(),head,nt)
assert terms==[[-3,5]] and np.array_equal(negative['N_f'],np.full(nt,4*7+1*10,dtype=complex))
assert env['rel'](np.ones(nt),np.ones(nt))==0

class FakeG9:
    K_REQ=np.array([0.6,1.,1.6,2.,3.,4.])
class FakeR7:
    FOURIER_N=np.array([3,5,8,10,15,20]);g9=FakeG9();C_VALUES={'C_star':2e-9}
bg={'x':np.arange(nt,dtype=float),'a':np.linspace(.4,.5,nt)}
h1=np.zeros((6,6,nt),complex);dh1=np.zeros((6,4,nt),complex)
h1[0,0]=2;h1[0,1]=3;h1[0,4]=4;h1[0,5]=5;dh1[0,3]=6
s,head=env['signed_ge07_jets'](FakeR7(),bg,h1,dh1)
assert np.array_equal(s[3][0],np.full(nt,2,dtype=complex))
assert np.array_equal(s[3][1],np.full(nt,3,dtype=complex))
assert np.array_equal(s[3][2],np.full(nt,3,dtype=complex))
assert np.array_equal(s[3][3],zero)
assert np.array_equal(s[3][4],np.full(nt,5,dtype=complex))
assert np.array_equal(s[3][5],np.full(nt,6,dtype=complex))
assert np.allclose(s[3][6],np.full(nt,2.4j,dtype=complex),rtol=1e-14,atol=0)
assert all(np.array_equal(a,np.conjugate(b)) for a,b in zip(s[-3],s[3]))
assert np.array_equal(head[0],bg['a'])
print('GE19_D33_MANUFACTURED_GE07_SIGNED_PAIR_DIAGONAL_CROSS_OFFSUPPORT_AND_WRONG_FACTOR_NEGATIVE_CONTROLS_PASS',flush=True)
print('GE19_D33_FROZEN_SHA_PREREG_STATIC_RUNNER_LOCK_PASS',flush=True)
