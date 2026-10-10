#!/usr/bin/env python3
"""D41 manufactured positive/negative controls extracted from exact frozen D41 AST."""
import ast, json
from pathlib import Path
import numpy as np
SRC=Path(__file__).with_name('h4f3d41_full_window_two_constraint_audit.py')
tree=ast.parse(SRC.read_text())
functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
assert {'check_complete_segment','splice_full_window','original_constraint_metrics'}<=functions.keys()
class Backward:
 @staticmethod
 def backward_error(row,w,target):
  lhs=complex(row@w);res=lhs-complex(target)
  s=max(abs(lhs),abs(target),float(np.sum(np.abs(row*w))),1e-300)
  return {'metric':abs(res)/s,'absolute_residual':abs(res),'scale':s}
ns={'np':np,'TINY':1e-300,'r18':Backward}
for name in ('check_complete_segment','splice_full_window','original_constraint_metrics'):
 mod=ast.Module(body=[functions[name]],type_ignores=[])
 exec(compile(ast.fix_missing_locations(mod),str(SRC),'exec'),ns)
check=ns['check_complete_segment'];splice=ns['splice_full_window'];metrics=ns['original_constraint_metrics']
modes=np.arange(1,41);betas=np.array([1.,.5,.1]);subs=np.array([1,8]);x=np.linspace(-.92,-.18,128)
shape=(40,3,2);gate=1e-6
state=np.array([np.full(shape+(8,),j+1,complex) for j in range(128)])
sh=np.full((128,)+shape,1e-7);ab=np.full_like(sh,1e-14)
def segment(a,b):
 return {'modes':modes.copy(),'betas':betas.copy(),'substeps':subs.copy(),
         'clock_node_indices':np.arange(a,b+1),'clock_node_x':x[a:b+1].copy(),
         'candidate_C_state_8_by_node_mode_beta_substep':state[a:b+1].copy(),
         'candidate_C_state_numerically_evaluated':np.ones((b-a+1,)+shape,bool),
         'candidate_C_shift_original_gate_pass':np.ones((b-a+1,)+shape,bool),
         'candidate_C_shift_relative_backward':sh[a:b+1].copy(),
         'candidate_C_shift_absolute_residual':ab[a:b+1].copy()}
for a,b in ((2,16),(16,32),(32,64),(64,127)):
 got=check(segment(a,b),a,b,modes,betas,subs,x,gate)
 assert got[0].shape==(b-a+1,)+shape+(8,)
 for bad in ('wrong_clock','missing_mask','false_gate','overlimit','nonfinite'):
  z=segment(a,b)
  if bad=='wrong_clock':z['clock_node_x'][0]=7.
  if bad=='missing_mask':z['candidate_C_state_numerically_evaluated'][0,25,0,0]=False
  if bad=='false_gate':z['candidate_C_shift_original_gate_pass'][0,25,0,0]=False
  if bad=='overlimit':z['candidate_C_shift_relative_backward'][0,25,0,0]=2e-6
  if bad=='nonfinite':z['candidate_C_state_8_by_node_mode_beta_substep'][0,25,0,0,0]=np.nan
  try:check(z,a,b,modes,betas,subs,x,gate)
  except RuntimeError:pass
  else:raise AssertionError('D41 accepted corrupted segment '+bad)
row={'relative_backward':1e-7,'absolute_residual':1e-14}
z34={'candidate_C_y0_by_mode_beta_8':state[0,:,:,0].copy(),
     'candidate_C_y0_valid_by_mode_beta':np.ones((40,3),bool)}
z34['candidate_C_y0_valid_by_mode_beta'][25]=False
z34['candidate_C_y0_by_mode_beta_8'][25]=0.
z35={'m26_roundoff_candidate_y0_by_beta_8':state[0,25,:,0].copy(),
     'm26_candidate_y0_valid_by_beta':np.ones(3,bool)}
z36={'first_interval_x1_8':state[1].copy(),'second_interval_x2_8':state[2].copy(),
     'first_interval_x1_valid':np.ones(shape,bool),'second_interval_x2_valid':np.ones(shape,bool),
     'second_interval_relative_shift':sh[2].copy(),'second_interval_absolute_shift':ab[2].copy()}
j34={'per_case':[]};j35={'m26_per_beta':[]};j36={'per_case':[]}
for ib,b in enumerate(betas):
 j35['m26_per_beta'].append({'beta':float(b),'candidate_initial':dict(row),
         'new_evolutions':[{'substeps':int(n),'passes_original_shift_gate':True,'shift':dict(row)} for n in subs]})
 for im,m in enumerate(modes):
  for ins,n in enumerate(subs):
   key={'mode':int(m),'beta':float(b),'substeps':int(n)}
   j36['per_case'].append(dict(key,passes_original_shift_gate=True,start_shift=dict(row),shift=dict(row)))
   if m!=26:j34['per_case'].append(dict(key,passes_original_shift_gate=True,initial_shift=dict(row),shift=dict(row)))
segs=[(a,b,segment(a,b)) for a,b in ((2,16),(16,32),(32,64),(64,127))]
y,s,a=splice(z34,z35,z36,segs,j34,j35,j36,modes,betas,subs,x,gate)
assert np.array_equal(y,state) and np.array_equal(s,sh) and np.array_equal(a,ab)
for bad in ('duplicate_or_missing_first','wrong_initial_m26','broken_x2_x16','broken_x16_x32','wrong_D36_gate'):
 za=dict(z34);zb=dict(z35);zc=dict(z36);ja=dict(j34);jb=dict(j35);jc=dict(j36)
 ss=[(p,q,dict(v)) for p,q,v in segs]
 if bad=='duplicate_or_missing_first':ja['per_case']=ja['per_case'][:-1]
 if bad=='wrong_initial_m26':zb['m26_candidate_y0_valid_by_beta']=np.array([False,True,True])
 if bad=='broken_x2_x16':v=ss[0][2]['candidate_C_state_8_by_node_mode_beta_substep'].copy();v[0,0,0,0,0]=1e12;ss[0][2]['candidate_C_state_8_by_node_mode_beta_substep']=v
 if bad=='broken_x16_x32':v=ss[1][2]['candidate_C_state_8_by_node_mode_beta_substep'].copy();v[0,0,0,0,0]=1e12;ss[1][2]['candidate_C_state_8_by_node_mode_beta_substep']=v
 if bad=='wrong_D36_gate':zc['second_interval_relative_shift']=np.full(shape,2e-7)
 try:splice(za,zb,zc,ss,ja,jb,jc,modes,betas,subs,x,gate)
 except RuntimeError:pass
 else:raise AssertionError('D41 accepted invalid bitwise splice '+bad)
C=np.zeros((14,10),complex);WY=np.zeros((10,8),complex);WR=np.zeros((10,8),complex)
WY[:8]=np.eye(8);C[4,0]=1.;C[10,1]=1.;C[12,2]=1.
for i in range(4):C[i,i+4]=1.
C[5,5]=1.
rr=np.zeros((6,3),complex);cc=np.zeros((2,3),complex);y=np.ones(8,complex)
rr[0,:]=1.;rr[5,:]=1.;cc[0,:]=1.;cc[1,:]=1.
v=metrics(C,WY,WR,rr,cc,y,0)
assert all(np.isfinite(v)) and v[:3]==(0.,0.,0.)
cc[0,0]=-1.
assert metrics(C,WY,WR,rr,cc,y,0)[1]>0.9
pre=json.loads(Path(__file__).with_name('h4f3d41_full_window_two_constraint_audit_prereg.json').read_text())
assert pre['clock_nodes']==128 and pre['expected_case_node_count']==30720 and pre['original_shift_gate']==1e-6
assert pre['no_new_projection'] and pre['no_new_evolution'] and pre['all_other_row_gates_are_report_only']
print('GE19_D41_MANUFACTURED_FULL_WINDOW_SPLICE_SOURCE_ROW_AND_NEGATIVE_CONTROLS_PASS',flush=True)
