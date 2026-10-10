#!/usr/bin/env python3
"""GE19 D40: frozen candidate-C x64->x127 continuation through all C_star clock nodes.

Numerical diagnostic only: SHA-lock actual D39 endpoints and all action/source parents.
No splice reprojection, source retuning, uncertified-parent promotion, or fabricated passes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d39_x32_x64_original_action_continuation as d39
d36=d39.d36

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d40_x64_x127_original_action_continuation_prereg.json'
LOCK=ROOT/'ge19/h4f3d40_x64_x127_original_action_continuation_lock.json'
TINY=1e-300


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def validate_d39_start(z,j,modes,betas,substeps,limit):
    """SHA-locked actual D39 x64 states: 7680 observed x32..x64 gates, no masks."""
    if not (j['classification']=='GE19_D39_X32_X64_ALL_MODE_COHORT_EVALUATED_DIAGNOSTIC_PARENTS_UNCERTIFIED'
            and j['expected_new_endpoint_count']==j['evaluated_new_endpoint_count']==7680
            and j['unevaluated_new_endpoint_count']==j['observed_original_shift_gate_fail_count']==0
            and j['all_new_endpoints_evaluated'] is True and j['all_original_shift_gates_pass'] is True
            and j['D38_3840_prefix_gate_pass_SHA_frozen'] is True
            and j['D37_3360_prefix_gate_pass_SHA_frozen'] is True
            and j['D36_240_second_interval_gate_pass_SHA_frozen'] is True
            and j['D35_m26_posthoc_momentum_representation_not_original_bitwise'] is True
            and j['D22A_original_science_FAIL_immutable'] is True
            and j['D34_D34R1_original_m26_boundary_FAIL_immutable'] is True
            and j['original_shift_gate_unchanged'] is True
            and j['nonanalytic_StageE_Y_retained'] is True
            and j['m0_source_retained_separately'] is True
            and j['no_reprojection_at_x32_or_later_knots'] is True
            and j['no_reprojection_at_x16_or_later_knots'] is True
            and j['no_reprojection_at_x2_or_later_knots'] is True
            and j['original_action_modified'] is False
            and j['production_H3F_source_modified'] is False
            and j['H3_full_window_solve_performed'] is False
            and j['Z11_certified'] is False and j['Z20_certified'] is False
            and j['Z21_certified'] is False and j['lensing_licensed'] is False
            and not j['first_failure_by_case'] and not j['numerical_or_blocked_endpoint_errors']
            and not j['observed_original_shift_gate_failures']):
        raise RuntimeError('D40 frozen D39 x32..x64 science/uncertified scope not reproducible')
    if not (np.array_equal(z['modes'],modes) and np.array_equal(z['betas'],betas)
            and np.array_equal(z['substeps'],substeps)
            and np.array_equal(z['clock_node_indices'],np.arange(32,65))
            and np.asarray(z['clock_node_x']).shape==(33,)):
        raise RuntimeError('D40 frozen D39 clock/cohort indexing mismatch')
    cx=np.asarray(z['clock_node_x'],float)
    y=np.asarray(z['candidate_C_state_8_by_node_mode_beta_substep'],complex)
    valid=np.asarray(z['candidate_C_state_numerically_evaluated'],bool)
    passed=np.asarray(z['candidate_C_shift_original_gate_pass'],bool)
    metrics=np.asarray(z['candidate_C_shift_relative_backward'],float)
    ab=np.asarray(z['candidate_C_shift_absolute_residual'],float)
    rd=np.asarray(z['candidate_C_Radau_backward_report_only'],float)
    shape=(33,40,3,2)
    if (y.shape!=shape+(8,) or valid.shape!=shape or passed.shape!=shape or
            metrics.shape!=shape or ab.shape!=shape or rd.shape!=shape or
            not np.all(np.isfinite(cx)) or not np.all(np.diff(cx)>0) or
            not np.all(valid) or not np.all(passed) or
            not np.all(np.isfinite(y)) or not np.all(np.isfinite(metrics)) or
            not np.all(np.isfinite(ab)) or not np.all(np.isfinite(rd)) or
            not np.all(metrics<=limit)):
        raise RuntimeError('D40 D39 missing/invalid actual x64 state or original gate')
    if not np.array_equal(passed,metrics<=limit):
        raise RuntimeError('D40 parent D39 observed shift labels not original gate')
    if len(j['interval_summaries'])!=32:
        raise RuntimeError('D40 D39 32 interval summaries missing')
    for local,q in enumerate(j['interval_summaries'],start=1):
        if (q['interval_index']!=31+local or q['node_index']!=32+local
                or not (q['evaluated_endpoints']==q['expected_endpoints']==240)
                or q['unevaluated_endpoints']!=0 or q['observed_shift_gate_failures']!=0
                or q['clock_x0_x1']!=[float(cx[local-1]),float(cx[local])]
                or q['max_relative_shift_observed']!=float(np.max(metrics[local]))
                or q['max_absolute_shift_observed']!=float(np.max(ab[local]))
                or q['max_Radau_backward_report_only']!=float(np.max(rd[local]))):
            raise RuntimeError('D40 D39 frozen interval/mask/clock summary mismatch')
    if (j['max_observed_relative_shift_new']!=float(np.max(metrics[1:])) or
            j['max_observed_absolute_shift_new']!=float(np.max(ab[1:])) or
            j['max_observed_Radau_backward_report_only']!=float(np.max(rd[1:]))):
        raise RuntimeError('D40 D39 JSON/NPZ numerical summaries mismatch')
    return y[-1].copy(),metrics[-1].copy(),ab[-1].copy(),rd[-1].copy(),float(cx[-1])

def summarize_prefix(valid,passmask,metric,ab,radau,errors,limit):
    """Only numeric-valid knots count as evaluated; a prior FAIL blocks descendants."""
    valid=np.asarray(valid,bool);passmask=np.asarray(passmask,bool)
    metric=np.asarray(metric,float);ab=np.asarray(ab,float);radau=np.asarray(radau,float)
    if valid.ndim!=4 or valid.shape[1:]!=(40,3,2) or not np.all(valid[0]) or \
       passmask.shape!=valid.shape or metric.shape!=valid.shape or ab.shape!=valid.shape or radau.shape!=valid.shape:
        raise RuntimeError('D40 invalid complete-grid prefix shape')
    if not np.all(np.isfinite(metric[valid])) or not np.all(np.isnan(metric[~valid])) or \
       not np.all(np.isfinite(ab[valid])) or not np.all(np.isnan(ab[~valid])) or \
       not np.all(np.isfinite(radau[valid])) or not np.all(np.isnan(radau[~valid])):
        raise RuntimeError('D40 metric validity mask broken')
    if np.any(passmask&~valid) or not np.all(passmask[0]):
        raise RuntimeError('D40 invalid observed science-pass mask')
    if np.any(valid[1:] & ~(valid[:-1]&passmask[:-1])):
        raise RuntimeError('D40 unevaluated or failed parent illegally propagated to a later knot')
    if not np.array_equal(passmask[valid],metric[valid]<=limit):
        raise RuntimeError('D40 science-pass labels differ from original gate')
    expected=(valid.shape[0]-1)*240
    evaluated=int(valid[1:].sum());missing=expected-evaluated
    if len(errors)!=missing:
        raise RuntimeError('D40 errors/unevaluated ledger mismatch')
    keys=[(q['node_index'],q['mode'],q['beta'],q['substeps']) for q in errors]
    if len(keys)!=len(set(keys)):
        raise RuntimeError('D40 duplicated unobserved endpoint ledger')
    observed_bad=int(np.count_nonzero(valid[1:]&~passmask[1:]))
    all_done=missing==0
    return {
      'expected_new_endpoint_count':expected,
      'evaluated_new_endpoint_count':evaluated,
      'unevaluated_new_endpoint_count':missing,
      'observed_original_shift_gate_fail_count':observed_bad,
      'all_new_endpoints_evaluated':all_done,
      'all_original_shift_gates_pass':(observed_bad==0) if all_done else None,
      'max_observed_relative_shift_new':float(np.max(metric[1:][valid[1:]])) if evaluated else None,
      'max_observed_absolute_shift_new':float(np.max(ab[1:][valid[1:]])) if evaluated else None,
      'max_observed_Radau_backward_report_only':float(np.max(radau[1:][valid[1:]])) if evaluated else None}


def check_inputs(rd,pre,lock):
    if not (pre['classification']=='GE19_D40_PREEXEC_X64_X127_ORIGINAL_ACTION_CONTINUATION'
            and pre['branch']=='physics-first-gravitational-elasticity'
            and pre['source_tag']=='C_star' and pre['source_nt']==128
            and pre['start_node_index']==64 and pre['end_node_index']==127
            and pre['modes']==list(range(1,41)) and pre['betas']==[1.,.5,.1]
            and pre['substeps']==[1,8] and pre['frozen_prefix_endpoint_count']==15360
            and pre['expected_new_endpoint_count']==15120
            and pre['original_shift_gate']==pre['original_boundary_backward_gate']==1e-6
            and all(pre[v] for v in ('no_reprojection_after_x0','no_observational_tuning',
                        'same_original_action_and_beta_Y','original_gate_at_every_new_knot',
                        'stop_case_after_failure_no_silent_pass','no_parent_certification',
                        'no_source_or_threshold_changes'))):
        raise RuntimeError('D40 frozen x64/x127/source/cohort/gate preregistration mismatch')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!=pre['branch'] or branch=='main':
        raise RuntimeError('D40 wrong branch/main forbidden')
    for name,want in lock['sha256_local_files'].items():
        if not (ROOT/name).is_file() or sha(ROOT/name)!=want:
            raise RuntimeError('D40 self SHA lock FAIL '+name)
    for name,want in pre['frozen_D39_code_sha256'].items():
        if not (ROOT/name).is_file() or sha(ROOT/name)!=want:
            raise RuntimeError('D40 immutable D39 source lock FAIL '+name)
    for name,want in pre['frozen_D39_result_sha256'].items():
        if not (rd/name).is_file() or sha(rd/name)!=want:
            raise RuntimeError('D40 immutable D39 result lock FAIL '+name)
    frozen,j35,j33,j36,j37,j38=d39.check_inputs(rd,json.loads(d39.PRE.read_text()),json.loads(d39.LOCK.read_text()))
    j39=json.loads((rd/'ge19_h4f3d39_x32_x64_original_action_continuation.json').read_text())
    print('GE19_D40_D39_D38_D37_D36_D35_D34R1_D33_AND_ORIGINAL_ACTION_ALL_PARENT_SHA_SCOPE_LOCK_PASS',flush=True)
    return frozen,j35,j33,j36,j37,j38,j39

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True);ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    a=ap.parse_args();rd=Path(a.results_dir).resolve();jp=Path(a.json_out).resolve();zp=Path(a.npz_out).resolve()
    if jp.exists() or zp.exists():raise RuntimeError('D40 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    frozen,j35,j33,j36,j37,j38,j39=check_inputs(rd,pre,lock)
    modes=np.asarray(pre['modes'],int);betas=np.asarray(pre['betas'],float);subs=np.asarray(pre['substeps'],int)
    r7=d36.d35.d25.d20.source.old.r7;d25=d36.d35.d25
    start_idx=int(pre['start_node_index']);end_idx=int(pre['end_node_index']);nodes=np.arange(start_idx,end_idx+1)
    shape=(len(nodes),40,3,2)
    data={
      'modes':modes,'betas':betas,'substeps':subs,
      'clock_node_indices':nodes,'clock_node_x':np.zeros(len(nodes),float),
      'candidate_C_state_8_by_node_mode_beta_substep':np.zeros(shape+(8,),complex),
      'candidate_C_state_numerically_evaluated':np.zeros(shape,bool),
      'candidate_C_shift_original_gate_pass':np.zeros(shape,bool),
      'candidate_C_shift_relative_backward':np.full(shape,np.nan,float),
      'candidate_C_shift_absolute_residual':np.full(shape,np.nan,float),
      'candidate_C_Radau_backward_report_only':np.full(shape,np.nan,float)}
    rep={
      'classification':'GE19_D40_X64_X127_INCOMPLETE_DIAGNOSTIC_PARENTS_UNCERTIFIED',
      'preregistration':pre['classification'],'source_sha256':sha(__file__),
      'scope':'All remaining 63 clock intervals x64..x127 of 128-node C_star grid: candidate C, m1..m40, beta 1/0.5/0.1 and separate n1/n8. D39 x64 state reused bitwise, no new projection. Original 1e-6 shift gate at every knot. A failed/blocked case has no silently passed descendants. Numerical full-clock-node scan is not a certified original/full H3 solution.',
      'claim_boundary':'Full 128-clock-node numerical candidate-C shift gate diagnostic only. Not an a priori or a posteriori continuum error bound, a bitwise Repair18 parent, an on-shell H1/Noether proof, certified full-window original H3/H4 Ward, or Z11/Z20/Z21/lensing authorization. Original D22A/D34/D34R1 failures and D35 posthoc m26 momentum representation are immutable.',
      'D22A_original_science_FAIL_immutable':True,
      'D34_D34R1_original_m26_boundary_FAIL_immutable':True,
      'D35_m26_posthoc_momentum_representation_not_original_bitwise':True,
      'D36_240_second_interval_gate_pass_SHA_frozen':True,
      'D37_3360_prefix_gate_pass_SHA_frozen':True,
      'D38_3840_prefix_gate_pass_SHA_frozen':True,
      'D39_7680_prefix_gate_pass_SHA_frozen':True,
      'original_action_modified':False,'production_H3F_source_modified':False,
      'original_shift_gate_unchanged':True,'nonanalytic_StageE_Y_retained':True,
      'm0_source_retained_separately':True,'all_reduced_modes_retained':True,
      'no_reprojection_at_x2_or_later_knots':True,'no_reprojection_at_x16_or_later_knots':True,
      'no_reprojection_at_x32_or_later_knots':True,
      'no_reprojection_at_x64_or_later_knots':True,
      'no_observational_tuning':True,
      'H3_full_window_solve_performed':False,'Z11_certified':False,'Z20_certified':False,
      'Z21_certified':False,'full_H4_Ward_certified':False,'lensing_licensed':False,
      'interval_summaries':[],'numerical_or_blocked_endpoint_errors':[],
      'observed_original_shift_gate_failures':[], 'first_failure_by_case':[],
      'first_interval_transfer_checks':j36['first_interval_transfer_checks'],
      'D36_clock_x1_x2':j36['clock_x1_x2'],
      'D37_clock_x16':float(j37['interval_summaries'][-1]['clock_x0_x1'][-1]),
      'D38_clock_x32':float(j38['interval_summaries'][-1]['clock_x0_x1'][-1]),
      'D39_clock_x64':float(j39['interval_summaries'][-1]['clock_x0_x1'][-1])}
    with ExitStack() as es:
        z39=es.enter_context(np.load(rd/'ge19_h4f3d39_x32_x64_original_action_continuation.npz',allow_pickle=False))
        z33=es.enter_context(np.load(rd/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz',allow_pickle=False))
        z22=es.enter_context(np.load(frozen['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        y64,sh64,ab64,ra64,x64=validate_d39_start(z39,j39,modes,betas,subs,pre['original_shift_gate'])
        data['candidate_C_state_8_by_node_mode_beta_substep'][0]=y64
        data['candidate_C_state_numerically_evaluated'][0]=True
        data['candidate_C_shift_original_gate_pass'][0]=True
        data['candidate_C_shift_relative_backward'][0]=sh64
        data['candidate_C_shift_absolute_residual'][0]=ab64
        data['candidate_C_Radau_backward_report_only'][0]=ra64
        bgs,_,mod6,mod7,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        if x.shape!=(128,) or not np.array_equal(x,np.asarray(z22['x_primary'],float)) or \
           not np.isfinite(x).all() or not np.all(np.diff(x)>0) or \
           not np.array_equal([x[1],x[2]],np.asarray(j36['clock_x1_x2'],float)) or x[16]!=float(j39['D37_clock_x16']) or x[32]!=float(j39['D38_clock_x32']) or x[64]!=x64:
            raise RuntimeError('D40 original action frozen x64 clock mismatch')
        data['clock_node_x'][:]=x[nodes]
        sources={}
        for ib,b in enumerate(betas):
            ma=np.asarray(z33[f'beta{ib}_candidate_C_main_six_by_128_by_41'],complex)
            co=np.asarray(z33[f'beta{ib}_candidate_C_constraint_two_by_128_by_41'],complex)
            if ma.shape!=(6,128,41) or co.shape!=(2,128,41) or \
               not np.isfinite(ma).all() or not np.isfinite(co).all() or \
               not np.any(ma[:,:,0]) or not np.any(ma[3,:,1]) or not np.any(ma[3,:,14]) or \
               not np.array_equal(co[:,:,26],np.zeros((2,128),complex)):
                raise RuntimeError('D40 candidate-C action/m0/m26/Y frozen source mismatch')
            sources[float(b)]={'rhs':ma,'rhs_constraint':co}
        print('GE19_D40_ALL_240_REAL_X64_STATES_AND_BETA_M0_Y_SOURCES_RETAINED_PASS',flush=True)
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            if active['ctx'] is None:raise RuntimeError('D40 action background clock not ready')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        blocked={}
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            for local in range(len(nodes)-1):
                j=int(nodes[local]);next_j=j+1;x0=float(x[j]);x1=float(x[next_j])
                interval_rows=[];interval_errors=[]
                pair_disagreements=[]
                for im,m in enumerate(modes):
                    k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                    rf,cf=r7._source_interp(x,sources,int(m))
                    op0=d25.shift_at(r7,mod6,mod7,bg,tag,k,x0,None,rf,cf)
                    op1=d25.shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rf,cf)
                    for ib,b in enumerate(betas):
                        def rr(t,fun=rf,index=ib):return np.asarray(fun(t),complex)[:,index:index+1]
                        def cc(t,fun=cf,index=ib):return np.asarray(fun(t),complex)[:,index:index+1]
                        for ins,n in enumerate(subs):
                            key=(int(m),float(b),int(n))
                            if key in blocked or not data['candidate_C_state_numerically_evaluated'][local,im,ib,ins] or \
                               not data['candidate_C_shift_original_gate_pass'][local,im,ib,ins]:
                                q={'node_index':next_j,'mode':int(m),'beta':float(b),'substeps':int(n),
                                   'reason':'BLOCKED_BY_PRIOR_UNEVALUATED_OR_SHIFT_GATE_FAIL'}
                                interval_errors.append(q)
                                continue
                            y0=data['candidate_C_state_8_by_node_mode_beta_substep'][local,im,ib,ins]
                            expected=float(data['candidate_C_shift_relative_backward'][local,im,ib,ins])
                            got=d25.metric_from_y(r7,op0,y0,ib)
                            if not np.isfinite(got['relative_backward']) or \
                               abs(got['relative_backward']-expected)>1e-10*max(abs(got['relative_backward']),abs(expected),TINY):
                                raise RuntimeError(f'D40 x{j} transferred state/metric mismatch m={m} beta={b} n={n}')
                            try:
                                yend,rad=d25.integrate(r7,mod6,mod7,bg,tag,k,y0,x0,x1,rr,cc,int(n))
                                met=d25.metric_from_y(r7,op1,yend,ib)
                                if not np.isfinite(yend).all() or not np.isfinite((rad,met['relative_backward'],
                                                                                  met['absolute_residual'])).all():
                                    raise FloatingPointError('nonfinite D40 propagated endpoint/metric')
                            except (RuntimeError,ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:
                                q={'node_index':next_j,'mode':int(m),'beta':float(b),'substeps':int(n),
                                   'reason':'NUMERICAL_OR_OPERATOR_EXCEPTION','exception':type(exc).__name__,
                                   'detail':str(exc)}
                                interval_errors.append(q);blocked[key]=q
                                rep['first_failure_by_case'].append(q)
                                print(f'GE19_D40_UNEVALUATED x{next_j} m={m} beta={b} n={n} reason={exc}',flush=True)
                                continue
                            data['candidate_C_state_8_by_node_mode_beta_substep'][local+1,im,ib,ins]=yend
                            data['candidate_C_state_numerically_evaluated'][local+1,im,ib,ins]=True
                            passed=met['relative_backward']<=pre['original_shift_gate']
                            data['candidate_C_shift_original_gate_pass'][local+1,im,ib,ins]=passed
                            data['candidate_C_shift_relative_backward'][local+1,im,ib,ins]=met['relative_backward']
                            data['candidate_C_shift_absolute_residual'][local+1,im,ib,ins]=met['absolute_residual']
                            data['candidate_C_Radau_backward_report_only'][local+1,im,ib,ins]=float(rad)
                            row={'node_index':next_j,'mode':int(m),'beta':float(b),'substeps':int(n),
                                 'relative_shift':met['relative_backward'],'absolute_shift':met['absolute_residual'],
                                 'Radau_backward_report_only':float(rad),'original_shift_gate_pass':bool(passed)}
                            interval_rows.append(row)
                            if not passed:
                                failure=dict(row,reason='ORIGINAL_SHIFT_GATE_FAIL')
                                rep['observed_original_shift_gate_failures'].append(failure)
                                rep['first_failure_by_case'].append(failure);blocked[key]=failure
                                print(f'GE19_D40_ORIGINAL_SHIFT_GATE_FAIL x{next_j} m={m} beta={b} n={n} shift={met["relative_backward"]:.6e}',flush=True)
                        v=data['candidate_C_state_numerically_evaluated'][local+1,im,ib]
                        if np.all(v):
                            one=data['candidate_C_state_8_by_node_mode_beta_substep'][local+1,im,ib,0]
                            eight=data['candidate_C_state_8_by_node_mode_beta_substep'][local+1,im,ib,1]
                            pair_disagreements.append(d36.rel(one,eight))
                rep['numerical_or_blocked_endpoint_errors'].extend(interval_errors)
                summ={
                  'interval_index':j,'node_index':next_j,'clock_x0_x1':[x0,x1],
                  'expected_endpoints':240,'evaluated_endpoints':len(interval_rows),
                  'unevaluated_endpoints':len(interval_errors),
                  'observed_shift_gate_failures':sum(not q['original_shift_gate_pass'] for q in interval_rows),
                  'max_relative_shift_observed':max((q['relative_shift'] for q in interval_rows),default=None),
                  'max_absolute_shift_observed':max((q['absolute_shift'] for q in interval_rows),default=None),
                  'max_n1_vs_n8_endpoint_state_relative_report_only':max(pair_disagreements,default=None),
                  'max_Radau_backward_report_only':max((q['Radau_backward_report_only'] for q in interval_rows),default=None)}
                if len(interval_rows)+len(interval_errors)!=240:
                    raise RuntimeError('D40 interval ledger lost/duplicated cases')
                rep['interval_summaries'].append(summ)
                print(f'GE19_D40_INTERVAL x{j}->x{next_j} evaluated={len(interval_rows)} '
                      f'unevaluated={len(interval_errors)} shift_gate_fails={summ["observed_shift_gate_failures"]} '
                      f'max_shift={summ["max_relative_shift_observed"]}',flush=True)
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
    result=summarize_prefix(data['candidate_C_state_numerically_evaluated'],
             data['candidate_C_shift_original_gate_pass'],data['candidate_C_shift_relative_backward'],
             data['candidate_C_shift_absolute_residual'],data['candidate_C_Radau_backward_report_only'],
             rep['numerical_or_blocked_endpoint_errors'],pre['original_shift_gate'])
    rep.update(result)
    if not (len(rep['interval_summaries'])==63 and
            len(rep['observed_original_shift_gate_failures'])==result['observed_original_shift_gate_fail_count']):
        raise RuntimeError('D40 final interval/gate ledger inconsistent')
    rep['classification']=('GE19_D40_X64_X127_ALL_MODE_COHORT_EVALUATED_DIAGNOSTIC_PARENTS_UNCERTIFIED'
                           if result['all_new_endpoints_evaluated'] else
                           'GE19_D40_X64_X127_INCOMPLETE_DIAGNOSTIC_PARENTS_UNCERTIFIED')
    jp.parent.mkdir(parents=True,exist_ok=True);zp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps(rep,indent=2,sort_keys=True,allow_nan=False)+'\n')
    np.savez_compressed(zp,**data)
    print('GE19_D40_COHORT evaluated='+str(result['evaluated_new_endpoint_count'])+
          ' unevaluated='+str(result['unevaluated_new_endpoint_count'])+
          ' observed_shift_gate_fails='+str(result['observed_original_shift_gate_fail_count'])+
          ' all_gate_pass='+str(result['all_original_shift_gates_pass']),flush=True)
    print('GE19_D40_CLASSIFICATION '+rep['classification'],flush=True)

if __name__=='__main__':main()
