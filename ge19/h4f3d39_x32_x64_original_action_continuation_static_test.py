#!/usr/bin/env python3
"""D39 positive/negative controls from the exact D39 source AST."""
import ast,json
from pathlib import Path
import numpy as np
SOURCE=Path(__file__).with_name('h4f3d39_x32_x64_original_action_continuation.py')
tree=ast.parse(SOURCE.read_text())
functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
assert {'validate_d38_start','summarize_prefix'}<=functions.keys()
ns={'np':np,'TINY':1e-300}
for name in ('validate_d38_start','summarize_prefix'):
    m=ast.Module(body=[functions[name]],type_ignores=[])
    exec(compile(ast.fix_missing_locations(m),str(SOURCE),'exec'),ns)
check=ns['validate_d38_start'];summ=ns['summarize_prefix']
modes=np.arange(1,41);betas=np.array([1.,.5,.1]);subs=np.array([1,8])
shape=(17,40,3,2);cx=np.linspace(-.825,-.731,17)
z={'modes':modes,'betas':betas,'substeps':subs,'clock_node_indices':np.arange(16,33),
   'clock_node_x':cx,'candidate_C_state_8_by_node_mode_beta_substep':np.ones(shape+(8,),complex),
   'candidate_C_state_numerically_evaluated':np.ones(shape,bool),
   'candidate_C_shift_original_gate_pass':np.ones(shape,bool),
   'candidate_C_shift_relative_backward':np.full(shape,1e-8),
   'candidate_C_shift_absolute_residual':np.full(shape,1e-14),
   'candidate_C_Radau_backward_report_only':np.full(shape,1e-16)}
summaries=[{'interval_index':15+i,'node_index':16+i,'expected_endpoints':240,'evaluated_endpoints':240,
   'unevaluated_endpoints':0,'observed_shift_gate_failures':0,'clock_x0_x1':[float(cx[i-1]),float(cx[i])],
   'max_relative_shift_observed':1e-8,'max_absolute_shift_observed':1e-14,
   'max_Radau_backward_report_only':1e-16} for i in range(1,17)]
j={'classification':'GE19_D38_X16_X32_ALL_MODE_COHORT_EVALUATED_DIAGNOSTIC_PARENTS_UNCERTIFIED',
   'expected_new_endpoint_count':3840,'evaluated_new_endpoint_count':3840,
   'unevaluated_new_endpoint_count':0,'observed_original_shift_gate_fail_count':0,
   'all_new_endpoints_evaluated':True,'all_original_shift_gates_pass':True,
   'D37_3360_prefix_gate_pass_SHA_frozen':True,'D36_240_second_interval_gate_pass_SHA_frozen':True,
   'D35_m26_posthoc_momentum_representation_not_original_bitwise':True,
   'D22A_original_science_FAIL_immutable':True,'D34_D34R1_original_m26_boundary_FAIL_immutable':True,
   'original_shift_gate_unchanged':True,'nonanalytic_StageE_Y_retained':True,
   'm0_source_retained_separately':True,'no_reprojection_at_x2_or_later_knots':True,
   'no_reprojection_at_x16_or_later_knots':True,
   'original_action_modified':False,'production_H3F_source_modified':False,
   'H3_full_window_solve_performed':False,'Z11_certified':False,'Z20_certified':False,
   'Z21_certified':False,'lensing_licensed':False,
   'first_failure_by_case':[],'numerical_or_blocked_endpoint_errors':[],
   'observed_original_shift_gate_failures':[],'interval_summaries':summaries,
   'max_observed_relative_shift_new':1e-8,'max_observed_absolute_shift_new':1e-14,
   'max_observed_Radau_backward_report_only':1e-16}
y,sh,ab,rad,x32=check(z,j,modes,betas,subs,1e-6)
assert y.shape==(40,3,2,8) and np.array_equal(y,z['candidate_C_state_8_by_node_mode_beta_substep'][-1])
assert x32==cx[-1] and np.array_equal(sh,z['candidate_C_shift_relative_backward'][-1])
for bad in ('missing_mask','false_original_gate','nonfinite_state','overlimit_shift','wrong_clock','bad_parent_classification',
            'missing_summary','wrong_summary_count','wrong_summary_clock','wrong_summary_metric','wrong_global_max','silent_failure',
            'unapproved_source_edit','certified_parent','reprojected_parent'):
    zz=dict(z);jj=dict(j)
    if bad=='missing_mask':
        vv=z['candidate_C_state_numerically_evaluated'].copy();vv[-1,25,0,0]=False;zz['candidate_C_state_numerically_evaluated']=vv
    elif bad=='false_original_gate':
        vv=z['candidate_C_shift_original_gate_pass'].copy();vv[-1,25,0,0]=False;zz['candidate_C_shift_original_gate_pass']=vv
    elif bad=='nonfinite_state':
        vv=z['candidate_C_state_8_by_node_mode_beta_substep'].copy();vv[-1,25,0,0,0]=np.nan;zz['candidate_C_state_8_by_node_mode_beta_substep']=vv
    elif bad=='overlimit_shift':
        vv=z['candidate_C_shift_relative_backward'].copy();vv[-1,25,0,0]=2e-6;zz['candidate_C_shift_relative_backward']=vv
    elif bad=='wrong_clock':
        vv=z['clock_node_indices'].copy();vv[-1]=33;zz['clock_node_indices']=vv
    elif bad=='bad_parent_classification':jj['classification']='INCOMPLETE'
    elif bad=='missing_summary':jj['interval_summaries']=summaries[:-1]
    elif bad in ('wrong_summary_count','wrong_summary_clock','wrong_summary_metric'):
        vv=[dict(q) for q in summaries];vv[-1]['evaluated_endpoints']=239 if bad=='wrong_summary_count' else 240
        if bad=='wrong_summary_clock':vv[-1]['clock_x0_x1']=[-1.,-1.]
        if bad=='wrong_summary_metric':vv[-1]['max_relative_shift_observed']=2e-8
        jj['interval_summaries']=vv
    elif bad=='wrong_global_max':jj['max_observed_relative_shift_new']=2e-8
    elif bad=='silent_failure':jj['observed_original_shift_gate_failures']=[{'mode':26}]
    elif bad=='unapproved_source_edit':jj['production_H3F_source_modified']=True
    elif bad=='certified_parent':jj['Z20_certified']=True
    elif bad=='reprojected_parent':jj['no_reprojection_at_x16_or_later_knots']=False
    try:check(zz,jj,modes,betas,subs,1e-6)
    except RuntimeError:pass
    else:raise AssertionError('D39 accepted corrupt D38 parent: '+bad)
valid=np.ones((33,40,3,2),bool);passed=np.ones_like(valid)
metric=np.full(valid.shape,1e-8);absolute=np.full(valid.shape,1e-14);radau=np.full(valid.shape,1e-16)
out=summ(valid,passed,metric,absolute,radau,[],1e-6)
assert out['expected_new_endpoint_count']==out['evaluated_new_endpoint_count']==7680
assert out['unevaluated_new_endpoint_count']==out['observed_original_shift_gate_fail_count']==0
v=valid.copy();p=passed.copy();r=metric.copy();a=absolute.copy();rd=radau.copy()
p[1,25,0,0]=False;r[1,25,0,0]=2e-6
v[2:,25,0,0]=False;p[2:,25,0,0]=False;r[2:,25,0,0]=np.nan;a[2:,25,0,0]=np.nan;rd[2:,25,0,0]=np.nan
errors=[{'node_index':34+i,'mode':26,'beta':1.0,'substeps':1,'reason':'BLOCKED_BY_PRIOR_UNEVALUATED_OR_SHIFT_GATE_FAIL'} for i in range(31)]
out=summ(v,p,r,a,rd,errors,1e-6)
assert out['unevaluated_new_endpoint_count']==31 and out['observed_original_shift_gate_fail_count']==1
assert out['all_original_shift_gates_pass'] is None
for bad in ('fabricated_pass','missing_error','illegal_downstream_state','silent_metric'):
    vv=v.copy();pp=p.copy();rr=r.copy();aa=a.copy();dd=rd.copy();ee=list(errors)
    if bad=='fabricated_pass':pp[2,25,0,0]=True
    if bad=='missing_error':ee.pop()
    if bad=='illegal_downstream_state':vv[2,25,0,0]=True;rr[2,25,0,0]=0.;aa[2,25,0,0]=0.;dd[2,25,0,0]=0.;ee.pop(0)
    if bad=='silent_metric':rr[2,25,0,0]=0.
    try:summ(vv,pp,rr,aa,dd,ee,1e-6)
    except RuntimeError:pass
    else:raise AssertionError('D39 masked failed knot accepted: '+bad)
pre=json.loads(Path(__file__).with_name('h4f3d39_x32_x64_original_action_continuation_prereg.json').read_text())
assert pre['start_node_index']==32 and pre['end_node_index']==64 and pre['expected_new_endpoint_count']==7680
assert pre['original_shift_gate']==pre['original_boundary_backward_gate']==1e-6
assert pre['no_source_or_threshold_changes'] and pre['no_reprojection_after_x0']
print('GE19_D39_MANUFACTURED_D38_X32_240_AND_X32_X64_7680_GATE_MASK_NEGATIVE_CONTROLS_PASS',flush=True)
