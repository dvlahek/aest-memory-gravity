#!/usr/bin/env python3
"""Offline source-contract and manufactured canonical extraction tests for D20."""
import ast, pathlib, types, numpy as np
SRC=pathlib.Path(__file__).with_name('h4f3d20r1_recompute_five_sources_and_bath_ward.py')
s=SRC.read_text();tree=ast.parse(s)
functions={x.name:x for x in tree.body if isinstance(x,ast.FunctionDef)}
assert {'canonical_knots_to_h1','actual_m2','main','rel','sha'}<=functions.keys()
assert 'old.memory_m2_chunk(' in s and 'old.q_cross_direct(' in s
assert 'old.r24.evolve_z10(' not in s and 'old.reconstruct_m2_source(' not in s
assert "'new_physical_q20_and_Z11_recomputed':False" in s
assert "'full_original_H4_Ward_certified':False" in s
assert "'M1_uses_FROZEN_H3G_B20_not_new_q20':True" in s
assert "'GE05_M2_FD4_high_phase_temporal_aliasing_closed':False" in s
small=ast.Module(body=[functions['canonical_knots_to_h1']],type_ignores=[])
ns={'np':np,'TINY':1e-300,'rel':lambda a,b: float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-300))};exec(compile(ast.fix_missing_locations(small),str(SRC),'exec'),ns)
class R:
 def _constraint_backward_error(self,row,w,source):
  lhs=row@w; contribution=np.sum(np.abs(row*w));scale=max(abs(lhs),abs(source),contribution,1e-300)
  return {"metric":float(abs(lhs-source)/scale)}
 FOURIER_N=np.asarray([3,5,8,10,15,20]);g9=types.SimpleNamespace(K_REQ=np.asarray([.03]))
 def _canonical_operator_matrices(self,mod6,mod7,bg,tag,k,x):
  WY=np.zeros((10,8),complex)
  for dest,j in [(2,0),(3,1),(4,2),(5,3),(0,4),(1,5),(6,6),(7,7)]:WY[dest,j]=1
  C=np.zeros((14,10),complex)
  for j,dest in enumerate([0,1,6,7]):C[j,dest]=1
  return np.zeros((8,8)),None,None,None,WY,None,C,None,{}
bg={'x':np.asarray([0.,1.])}
y=np.empty((6,8,5),complex)
for i in range(6):
 for j in range(8):y[i,j]=1+100*i+10*j+np.arange(5)
st,dt,alg,oldraw,qslot=ns['canonical_knots_to_h1'](y,bg,'C_star',R(),None,None)
assert st.shape==(6,6,2) and dt.shape==(6,4,2) and alg<=1e-15 and qslot<=1e-15
assert st[0,1,0]==y[0,0,0] and st[0,0,1]==y[0,4,4]
assert dt[1,0,1]==y[1,6,4]
try:ns['canonical_knots_to_h1'](y[:,:,:4],bg,'C_star',R(),None,None)
except ValueError:pass
else:raise AssertionError('invalid fine grid allowed')
small2=ast.Module(body=[functions['actual_m2']],type_ignores=[])
ns2={'np':np,'TINY':1e-300};exec(compile(ast.fix_missing_locations(small2),str(SRC),'exec'),ns2)
class Old:
 GE05_TO_GE06=2.0;M_MAX=40;r7=types.SimpleNamespace(FOURIER_N=np.asarray([3,5,8,10,15,20]))
 def grav_real_for_memory(self,bg,h1,modes,nx):return {}
 def memory_m2_chunk(self,ge05,bg,grav,z,v,r,w,tau,nx):
  assert len(r)==len(w)==z.shape[0]==v.shape[0]
  return (np.ones((6,len(bg['x']),nx))*len(r),
          np.ones((2,len(bg['x']),nx))*len(r))
 def fft_low(self,x):return np.fft.fft(x,axis=-1)[...,:41]/x.shape[-1]
nq=17; z=np.zeros((nq,6,2),complex);w=np.ones(nq)
result=ns2['actual_m2'](None,Old(),bg,np.zeros((6,6,2)),z,z,np.arange(nq)+1,w,1,nx=128,chunk=8)
assert result.shape==(8,2,41) and np.max(np.abs(result[:,:,0]+34))<1e-14
assert not np.any(result[:,:,1:])
print('GE19_D20_ORIGINAL_M2_NEGATIVE_TWO_AND_COMPLETE_CHUNK_MANUFACTURED_PASS')
print('GE19_D20_CANONICAL_GE06_GE07_EXTRACTION_MANUFACTURED_PASS')
print('GE19_D20_NO_R1_REPROPAGATION_AND_STALE_M1_NEGATIVE_SCOPE_PASS')

# Original Repair07-style contribution-scaled backward error is meaningful
# when a near-null target is built from cancelling large local terms.
row=np.array([1e10,-1e10],complex);wv=np.array([1,1+2e-16],complex)
metric=R()._constraint_backward_error(row,wv,0.)['metric']
assert metric<1e-14,metric
wrong=wv.copy();wrong[1]=1.1
assert R()._constraint_backward_error(row,wrong,0.)['metric']>1e-3
print('GE19_D20R1_CANCELLATION_SAFE_ROW_BACKWARD_AND_NEGATIVE_CONTROL_PASS')
