#!/usr/bin/env python3
"""D37 manufactured positive/negative tests: D36 parent, every-knot masks, gates."""
import json
import numpy as np
from ge19 import h4f3d37_prefix_x2_x16_original_action_continuation as d

modes=np.arange(1,41);betas=np.asarray([1.,.5,.1]);ns=np.asarray([1,8]);shape=(40,3,2)
y=np.ones(shape+(8,),complex)
shift=np.full(shape,1e-8);absr=np.full(shape,1e-14);rad=np.full(shape,1e-16)
z={'modes':modes,'betas':betas,'substeps':ns,'second_interval_x2_8':y,
   'second_interval_x2_valid':np.ones(shape,bool),'second_interval_relative_shift':shift,
   'second_interval_absolute_shift':absr,'second_interval_Radau_backward':rad}
j={'classification':'GE19_D36_SECOND_INTERVAL_ALL_MODE_COHORT_EVALUATED_DIAGNOSTIC_PARENTS_UNCERTIFIED',
   'expected_endpoint_count':240,'evaluated_endpoint_count':240,'unevaluated_endpoint_count':0,
   'observed_shift_gate_fail_count':0,'all_endpoints_evaluated':True,'all_original_shift_gates_pass':True,
   'no_reprojection_at_second_interval_start':True,'D35_m26_posthoc_momentum_representation_not_original_bitwise':True,
   'D22A_original_science_FAIL_immutable':True,'D34_D34R1_original_m26_boundary_FAIL_immutable':True,
   'original_shift_gate_unchanged':True,'nonanalytic_StageE_Y_retained':True,'m0_source_retained_separately':True,
   'per_case':[{'mode':int(m),'beta':float(b),'substeps':int(n),
                'state_transfer_without_reprojection':True,'passes_original_shift_gate':True,
                'shift':{'relative_backward':1e-8}}
               for m in modes for b in betas for n in ns]}
a,b,c,e=d.validate_d36_start(z,j,modes,betas,ns,1e-6)
assert a.shape==shape+(8,) and np.array_equal(b,shift)
for variant in ('missing_mask','nonfinite_state','changed_metric','bad_status','missing_json_case','duplicate_json_case','excess_shift'):
    zz=dict(z);jj=dict(j)
    if variant=='missing_mask':
        vv=z['second_interval_x2_valid'].copy();vv[0,0,0]=False;zz['second_interval_x2_valid']=vv
    elif variant=='nonfinite_state':
        vv=y.copy();vv[0,0,0,0]=np.nan;zz['second_interval_x2_8']=vv
    elif variant=='changed_metric':
        vv=shift.copy();vv[0,0,0]=1.01e-8;zz['second_interval_relative_shift']=vv
    elif variant=='bad_status':jj['all_original_shift_gates_pass']=False
    elif variant=='missing_json_case':jj['per_case']=j['per_case'][:-1]
    elif variant=='duplicate_json_case':jj['per_case']=j['per_case']+[j['per_case'][0]]
    elif variant=='excess_shift':
        vv=shift.copy();vv[0,0,0]=1.01e-6;zz['second_interval_relative_shift']=vv
    try:d.validate_d36_start(zz,jj,modes,betas,ns,1e-6)
    except RuntimeError:pass
    else:raise AssertionError('D37 invalid D36 parent accepted: '+variant)

valid=np.ones((3,)+shape,bool);passes=np.ones_like(valid)
rel=np.zeros_like(valid,dtype=float);ar=np.zeros_like(valid,dtype=float);ra=np.zeros_like(valid,dtype=float)
s=d.summarize_prefix(valid,passes,rel,ar,ra,[],1e-6)
assert s['expected_new_endpoint_count']==480 and s['evaluated_new_endpoint_count']==480
assert s['all_original_shift_gates_pass'] is True and s['observed_original_shift_gate_fail_count']==0
# A real failing knot is observed; its later endpoint is masked and not promoted.
vv=valid.copy();vv[2,0,0,0]=False
pp=passes.copy();pp[1,0,0,0]=False;pp[2,0,0,0]=False
rr=rel.copy();rr[1,0,0,0]=1.01e-6;rr[2,0,0,0]=np.nan
aa=ar.copy();aa[2,0,0,0]=np.nan
bb=ra.copy();bb[2,0,0,0]=np.nan
error=[{'node_index':4,'mode':1,'beta':1.,'substeps':1,'reason':'BLOCKED_BY_PRIOR_UNEVALUATED_OR_SHIFT_GATE_FAIL'}]
s=d.summarize_prefix(vv,pp,rr,aa,bb,error,1e-6)
assert s['evaluated_new_endpoint_count']==479 and s['unevaluated_new_endpoint_count']==1
assert s['observed_original_shift_gate_fail_count']==1 and s['all_original_shift_gates_pass'] is None
# No observed FAIL may be silently relabeled as PASS.
for variant in ('false_pass_label','missing_error','invalid_metric_mask','duplicate_error','pass_without_observation','illegal_future_propagation'):
    v=vv.copy();p=pp.copy();r=rr.copy();ab=aa.copy();rad=bb.copy();err=list(error)
    if variant=='false_pass_label':p[1,0,0,0]=True
    if variant=='missing_error':err=[]
    if variant=='invalid_metric_mask':r[2,0,0,0]=0.
    if variant=='duplicate_error':err=err+err
    if variant=='pass_without_observation':p[2,0,0,0]=True
    if variant=='illegal_future_propagation':
        v[2,0,0,0]=True;r[2,0,0,0]=0.;ab[2,0,0,0]=0.;rad[2,0,0,0]=0.;err=[]
    try:d.summarize_prefix(v,p,r,ab,rad,err,1e-6)
    except RuntimeError:pass
    else:raise AssertionError('D37 failed/unevaluated case mislabeled: '+variant)
pre=json.loads(d.PRE.read_text())
assert pre['start_node_index']==2 and pre['end_node_index']==16
assert pre['expected_new_endpoint_count']==3360 and pre['original_shift_gate']==1e-6
assert pre['no_reprojection_after_x0'] and pre['original_gate_at_every_new_knot']
print('GE19_D37_MANUFACTURED_FROZEN_D36_ALL_240_AND_X2_X16_MASK_GATE_NEGATIVE_CONTROLS_PASS',flush=True)
