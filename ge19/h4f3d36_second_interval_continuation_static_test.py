#!/usr/bin/env python3
"""D36 manufactured source-independent cohort, mask and science-gate negatives."""
from __future__ import annotations
import json
import numpy as np
from ge19 import h4f3d36_second_interval_continuation as d

modes=list(range(1,41));betas=[1.,.5,.1];substeps=[1,8]
old=np.ones((40,3,2,8),complex);old[25]=0
oldmask=np.ones((40,3,2),bool);oldmask[25]=False
new=np.ones((3,2,8),complex)*2
newmask=np.ones((3,2),bool)
a={'modes':np.asarray(modes),'betas':np.asarray(betas),'substeps':np.asarray(substeps),
   'candidate_C_y1_by_mode_beta_substep_8':old,
   'candidate_C_y1_valid_by_mode_beta_substep':oldmask}
b={'m26_betas':np.asarray(betas),'m26_substeps':np.asarray(substeps),
   'm26_candidate_y1_by_beta_substep_8':new,
   'm26_candidate_y1_valid_by_beta_substep':newmask}
z,mask=d.join_first_endpoints(a,b,modes,betas,substeps)
assert z.shape==(40,3,2,8) and mask.sum()==240
assert np.array_equal(z[25],new) and np.array_equal(z[0],old[0])
for change in ('overlap','missing','badmode','badbeta','nonfinite'):
    aa=dict(a);bb=dict(b)
    if change=='overlap':
        v=oldmask.copy();v[25]=True;aa['candidate_C_y1_valid_by_mode_beta_substep']=v
    elif change=='missing':
        v=oldmask.copy();v[1,0,0]=False;aa['candidate_C_y1_valid_by_mode_beta_substep']=v
    elif change=='badmode':
        aa['modes']=np.arange(40)
    elif change=='badbeta':
        bb['m26_betas']=np.asarray([1.,.1,.5])
    elif change=='nonfinite':
        v=old.copy();v[0,0,0,0]=np.nan;aa['candidate_C_y1_by_mode_beta_substep_8']=v
    try:d.join_first_endpoints(aa,bb,modes,betas,substeps)
    except RuntimeError:pass
    else:raise AssertionError('D36 invalid frozen splice accepted: '+change)

row=lambda m,n,r:{'mode':m,'beta':1.,'substeps':n,'start_shift':{'relative_backward':0.},
                  'shift':{'relative_backward':r,'absolute_residual':abs(r)},'Radau_block_backward_report_only':0.}
planned=[row(m,n,0.) for m in (1,2) for n in (1,8)]
s=d.summarize(planned,[],(1,2),(1.,),(1,8),1e-6)
assert s['all_endpoints_evaluated'] and s['all_original_shift_gates_pass'] and s['shift_gate_fail_count']==0
s=d.summarize(planned[:-1],[{'mode':2,'beta':1.,'substeps':8,'reason':'manufactured'}],(1,2),(1.,),(1,8),1e-6)
assert s['unevaluated_endpoint_count']==1 and s['all_original_shift_gates_pass'] is None and s['shift_gate_fail_count'] is None
bad=[row(1,1,1.01e-6),row(1,8,0.),row(2,1,0.),row(2,8,0.)]
s=d.summarize(bad,[],(1,2),(1.,),(1,8),1e-6)
assert s['all_original_shift_gates_pass'] is False and s['shift_gate_fail_count']==1
for invalid,errs in ((planned+[planned[0]],[]),(planned, [{'mode':1,'beta':1.,'substeps':1,'reason':'overlap'}])):
    try:d.summarize(invalid,errs,(1,2),(1.,),(1,8),1e-6)
    except RuntimeError:pass
    else:raise AssertionError('D36 duplicate/overlap wrongly accepted')
pre=json.loads(d.PRE.read_text())
assert pre['interval_index']==1 and pre['original_shift_gate']==pre['original_boundary_backward_gate']==1e-6
assert pre['no_reprojection_at_x1'] and pre['first_interval_count']==pre['expected_second_interval_count']==240
assert pre['modes']==modes and pre['betas']==betas and pre['substeps']==substeps
print('GE19_D36_MANUFACTURED_EXACT_SPLICE_ALL_240_MASK_NEGATIVES_AND_UNCHANGED_SHIFT_GATE_PASS',flush=True)
