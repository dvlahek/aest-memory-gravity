#!/usr/bin/env python3
"""GE19 D36: frozen candidate-C FIRST->SECOND interval numerical continuation.

Sources: original-action D33 GE06+GE07 signed pairs, original Lambda and beta-
specific Stage E Y; original D34R1 234 endpoints and D35 m26 six endpoints.
Neither reproject at the x1 splice nor silently promote a missing/failed row.
This is NOT an on-shell, full-window H3, Z20, H4 Ward or lensing certificate.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d35_m26_precision_reprojection as d35

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d36_second_interval_continuation_prereg.json'
LOCK=ROOT/'ge19/h4f3d36_second_interval_continuation_lock.json'
TINY=1e-300


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()


def rel(a,b):
    aa=np.asarray(a,complex);bb=np.asarray(b,complex)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def join_first_endpoints(z34,z35,modes,betas,substeps):
    """Exact slot/mask join; m26 has NO original D34R1 propagated state."""
    modes=np.asarray(modes,int);betas=np.asarray(betas,float);substeps=np.asarray(substeps,int)
    if not (modes.shape==(40,) and np.array_equal(modes,np.arange(1,41)) and
            betas.shape==(3,) and np.array_equal(betas,[1.,.5,.1]) and
            np.array_equal(substeps,[1,8])):
        raise RuntimeError('D36 mode/beta/n cohort changed')
    if not (np.array_equal(z34['modes'],modes) and np.array_equal(z34['betas'],betas) and
            np.array_equal(z34['substeps'],substeps) and
            np.array_equal(z35['m26_betas'],betas) and np.array_equal(z35['m26_substeps'],substeps)):
        raise RuntimeError('D36 frozen cohort indexing mismatch')
    old=np.asarray(z34['candidate_C_y1_by_mode_beta_substep_8'],complex)
    oldmask=np.asarray(z34['candidate_C_y1_valid_by_mode_beta_substep'],bool)
    new=np.asarray(z35['m26_candidate_y1_by_beta_substep_8'],complex)
    newmask=np.asarray(z35['m26_candidate_y1_valid_by_beta_substep'],bool)
    if old.shape!=(40,3,2,8) or oldmask.shape!=(40,3,2) or new.shape!=(3,2,8) or newmask.shape!=(3,2):
        raise RuntimeError('D36 frozen candidate-C first-endpoint shape mismatch')
    slot=25
    expected=oldmask.copy();expected[slot]=True
    if np.any(oldmask[slot]) or not np.all(oldmask[np.arange(40)!=slot]) or not np.all(newmask) or \
       not np.all(np.isfinite(old)) or not np.all(np.isfinite(new)):
        raise RuntimeError('D36 missing, duplicated or nonfinite frozen first-interval endpoints')
    merged=old.copy();merged[slot]=new
    if not np.all(np.isfinite(merged)) or int(np.count_nonzero(expected))!=240:
        raise RuntimeError('D36 frozen first-interval endpoint cohort incomplete')
    return merged,expected


def summarize(rows,errors,modes,betas,substeps,limit):
    planned={(int(m),float(b),int(n)) for m in modes for b in betas for n in substeps}
    keys=[(int(v['mode']),float(v['beta']),int(v['substeps'])) for v in rows]
    badkeys=[(int(v['mode']),float(v['beta']),int(v['substeps'])) for v in errors]
    if len(keys)!=len(set(keys)) or len(badkeys)!=len(set(badkeys)) or \
       set(keys)&set(badkeys) or set(keys)|set(badkeys)!=planned:
        raise RuntimeError('D36 second-interval incomplete or duplicated execution ledger')
    if not all(np.isfinite((q['start_shift']['relative_backward'],q['shift']['relative_backward'],
                            q['shift']['absolute_residual'],q['Radau_block_backward_report_only'])).all() for q in rows):
        raise RuntimeError('D36 nonfinite numerical metrics')
    gatefailed=[{'mode':v['mode'],'beta':v['beta'],'substeps':v['substeps'],
                 'relative_backward':v['shift']['relative_backward']}
                for v in rows if v['shift']['relative_backward']>limit]
    complete=(not errors)
    return {'expected_endpoint_count':len(planned),'evaluated_endpoint_count':len(rows),
            'unevaluated_endpoint_count':len(errors),'numerical_execution_errors':errors,
            'observed_shift_gate_fail_count':len(gatefailed),'observed_shift_gate_failures':gatefailed,
            'all_endpoints_evaluated':complete,
            'all_original_shift_gates_pass':(not gatefailed) if complete else None,
            'shift_gate_fail_count':len(gatefailed) if complete else None,
            'max_observed_shift_relative_backward':max((v['shift']['relative_backward'] for v in rows),default=None),
            'max_observed_shift_absolute_residual':max((v['shift']['absolute_residual'] for v in rows),default=None)}


def check_inputs(rd,pre,lock):
    if (pre['classification']!='GE19_D36_PREEXEC_SECOND_INTERVAL_CANDIDATE_C_CONTINUATION' or
        pre['branch']!='physics-first-gravitational-elasticity' or pre['source_tag']!='C_star' or
        pre['source_nt']!=128 or pre['interval_index']!=1 or
        pre['modes']!=list(range(1,41)) or pre['betas']!=[1.,.5,.1] or
        pre['substeps']!=[1,8] or pre['first_interval_count']!=240 or
        pre['expected_second_interval_count']!=240 or
        pre['original_shift_gate']!=pre['original_boundary_backward_gate'] or
        pre['original_shift_gate']!=1e-6 or
        not all(pre[k] for k in ('no_reprojection_at_x1','original_action_and_beta_Y_retained',
                    'fixed_selection_independent_of_second_interval_results','no_threshold_or_mode_change',
                    'no_parent_certification','no_science_gate_waiver'))):
        raise RuntimeError('D36 original action/clock/cohort/preregistered gate mismatch')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!=pre['branch'] or branch=='main':raise RuntimeError('D36 wrong branch/main forbidden')
    for name,want in lock['sha256_local_files'].items():
        if not (ROOT/name).is_file() or sha(ROOT/name)!=want:
            raise RuntimeError('D36 self SHA lock FAIL '+name)
    for name,want in pre['frozen_D35_code_sha256'].items():
        if not (ROOT/name).is_file() or sha(ROOT/name)!=want:
            raise RuntimeError('D36 immutable D35 source lock FAIL '+name)
    for name,want in pre['frozen_D35_result_sha256'].items():
        if not (rd/name).is_file() or sha(rd/name)!=want:
            raise RuntimeError('D36 immutable D35 output lock FAIL '+name)
    for name,want in pre['frozen_D34R1_result_sha256'].items():
        if not (rd/name).is_file() or sha(rd/name)!=want:
            raise RuntimeError('D36 immutable D34R1 output lock FAIL '+name)
    src=rd/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz'
    if not src.is_file() or sha(src)!=pre['frozen_D33_source_npz_sha256']:
        raise RuntimeError('D36 immutable D33 candidate-C original-action source lock FAIL')
    _original,frozen,j33=d35.check_inputs(rd,json.loads(d35.PRE.read_text()),json.loads(d35.LOCK.read_text()))
    j35=json.loads((rd/'ge19_h4f3d35_m26_precision_reprojection.json').read_text())
    if not (j35['D35_all_240_endpoint_values_evaluated'] is True and
            j35['D35_all_240_first_interval_shift_gates_pass'] is True and
            j35['D35_new_endpoint_count']==6 and j35['D35_unevaluated_endpoint_count']==0 and
            j35['D35_shift_gate_fail_count']==0 and
            j35['original_action_modified'] is False and j35['production_H3F_source_modified'] is False and
            j35['nonanalytic_StageE_Y_retained'] is True and
            j35['m0_source_retained_separately'] is True and
            j35['D34_original_m26_boundary_FAIL_immutable'] is True and
            j35['D34R1_original_m26_three_boundary_FAIL_immutable'] is True):
        raise RuntimeError('D36 D35 first-interval conditional science/parent scope mismatch')
    print('GE19_D36_ALL_D35_D34R1_D33_AND_FROZEN_ORIGINAL_ACTION_SHA_SCOPE_LOCK_PASS',flush=True)
    return frozen,j35,j33


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True);ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    a=ap.parse_args();rd=Path(a.results_dir).resolve();jp=Path(a.json_out).resolve();zp=Path(a.npz_out).resolve()
    if jp.exists() or zp.exists():raise RuntimeError('D36 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    frozen_old,j35,j33=check_inputs(rd,pre,lock)
    modes=tuple(pre['modes']);betas=tuple(pre['betas']);substeps=tuple(pre['substeps'])
    r7=d35.d25.d20.source.old.r7;d25=d35.d25
    d34r1=d35.d34r1
    original_j34=json.loads((rd/'ge19_h4f3d34r1_boundary_failure_cohort.json').read_text())
    original_index={(int(q['mode']),float(q['beta']),int(q['substeps'])):q for q in original_j34['per_case']}
    new_index={(int(q['mode']),float(q['beta']),int(q['substeps'])):q
               for group in j35['m26_per_beta'] for q in group['new_evolutions']}
    if len(original_index)!=234 or len(new_index)!=6 or set(original_index)&set(new_index):
        raise RuntimeError('D36 invalid frozen first-interval endpoint metric ledger')
    allindex={**original_index,**new_index}
    if len(allindex)!=240:raise RuntimeError('D36 archived first-endpoint metrics not complete')
    report={
      'classification':'GE19_D36_SECOND_INTERVAL_INCOMPLETE_DIAGNOSTIC_PARENTS_UNCERTIFIED',
      'preregistration':pre['classification'],'source_sha256':sha(__file__),
      'scope':'Original-action frozen candidate-C first-to-second clock interval x[1]->x[2] with all 40 evolving reduced modes, beta 1/0.5/0.1 and independent n1/n8 paths. First-interval 234 D34R1 and six D35 m26 endpoints joined only if SHA/masks valid. No new momentum projection at x[1]. k0 source remains frozen but k0 reduced evolution is not attempted.',
      'claim_boundary':'Second interval NUMERICAL diagnostic, not original D34 boundary replay or certified first/whole-window H3, Ward, H1 on-shell, Z20, Z21 or lensing. Original D34/D34R1 failures and D35 posthoc m26 momentum representation are retained. Incomplete/failed cases are not successes.',
      'D22A_original_science_FAIL_immutable':True,
      'D34_D34R1_original_m26_boundary_FAIL_immutable':True,
      'D35_m26_posthoc_momentum_representation_not_original_bitwise':True,
      'D35_all_240_first_interval_original_shift_gates_pass':True,
      'D35_first_interval_parent_sha_frozen':True,
      'original_action_modified':False,'production_H3F_source_modified':False,
      'original_shift_gate_unchanged':True,'nonanalytic_StageE_Y_retained':True,
      'm0_source_retained_separately':True,'all_reduced_modes_retained':True,
      'no_reprojection_at_second_interval_start':True,'no_observational_tuning':True,
      'H3_full_window_solve_performed':False,'Z11_certified':False,'Z20_certified':False,
      'Z21_certified':False,'full_H4_Ward_certified':False,'lensing_licensed':False,
      'first_interval_transfer_checks':[],'per_case':[],
      'failed_second_interval_evolutions':[]}
    arrays={'modes':np.asarray(modes,int),'betas':np.asarray(betas,float),
            'substeps':np.asarray(substeps,int),'first_interval_x1_8':np.zeros((40,3,2,8),complex),
            'first_interval_x1_valid':np.zeros((40,3,2),bool),
            'second_interval_x2_8':np.zeros((40,3,2,8),complex),
            'second_interval_x2_valid':np.zeros((40,3,2),bool),
            'second_interval_relative_shift':np.full((40,3,2),np.nan,float),
            'second_interval_absolute_shift':np.full((40,3,2),np.nan,float),
            'second_interval_Radau_backward':np.full((40,3,2),np.nan,float)}
    with ExitStack() as es:
        z34=es.enter_context(np.load(rd/'ge19_h4f3d34r1_boundary_failure_cohort.npz',allow_pickle=False))
        z35=es.enter_context(np.load(rd/'ge19_h4f3d35_m26_precision_reprojection.npz',allow_pickle=False))
        z33=es.enter_context(np.load(rd/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz',allow_pickle=False))
        z22=es.enter_context(np.load(frozen_old['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        y1,mask=join_first_endpoints(z34,z35,modes,betas,substeps)
        arrays['first_interval_x1_8'][:]=y1;arrays['first_interval_x1_valid'][:]=mask
        bgs,_,mod6,mod7,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        if x.shape!=(128,) or not np.array_equal(x,np.asarray(z22['x_primary'],float)) or \
           not np.isfinite(x).all() or not np.all(np.diff(x)>0):
            raise RuntimeError('D36 frozen original-action clock/time-node mismatch')
        x1,x2=float(x[1]),float(x[2]);report['clock_x1_x2']=[x1,x2]
        src={}
        for ib,b in enumerate(betas):
            ma=np.asarray(z33[f'beta{ib}_candidate_C_main_six_by_128_by_41'],complex)
            co=np.asarray(z33[f'beta{ib}_candidate_C_constraint_two_by_128_by_41'],complex)
            if ma.shape!=(6,128,41) or co.shape!=(2,128,41) or \
               not np.isfinite(ma).all() or not np.isfinite(co).all() or \
               not np.any(ma[:,:,0]) or not np.any(ma[3,:,1]) or not np.any(ma[3,:,14]) or \
               not np.array_equal(co[:,:,26],np.zeros((2,128),complex)):
                raise RuntimeError('D36 m0/m26 action constraint source or beta Stage E Y lost')
            src[b]={'rhs':ma,'rhs_constraint':co}
        print('GE19_D36_FROZEN_240_FIRST_ENDPOINT_MASK_AND_ALL_BETA_M0_Y_SOURCE_PASS',flush=True)
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            if active['ctx'] is None:raise RuntimeError('D36 original-action clock not ready')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            failures=[];rows=[]
            for im,m in enumerate(modes):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                # Exact D34R1/D35 original source batching: dict keyed by frozen beta.
                rf,cf=r7._source_interp(x,src,m)
                op1=d25.shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rf,cf)
                op2=d25.shift_at(r7,mod6,mod7,bg,tag,k,x2,None,rf,cf)
                for ib,b in enumerate(betas):
                    def rr(t,fun=rf,index=ib):return np.asarray(fun(t),complex)[:,index:index+1]
                    def cc(t,fun=cf,index=ib):return np.asarray(fun(t),complex)[:,index:index+1]
                    for ins,n in enumerate(substeps):
                        key=(m,b,n);first=y1[im,ib,ins]
                        start=d25.metric_from_y(r7,op1,first,ib)
                        oldmetric=allindex[key]['shift']['relative_backward']
                        if abs(start['relative_backward']-oldmetric)>1e-10*max(abs(oldmetric),abs(start['relative_backward']),TINY) or \
                           start['relative_backward']>pre['original_shift_gate']:
                            raise RuntimeError(f'D36 frozen first-endpoint boundary/state replay FAIL m={m} beta={b} n={n}')
                        if key in [(1,1.,8),(14,.1,8),(26,1.,8),(40,.1,8)]:
                            report['first_interval_transfer_checks'].append({'mode':m,'beta':b,'substeps':n,
                                'frozen_first_interval_shift':oldmetric,'replayed_shift':start['relative_backward'],
                                'first_endpoint_reused_bitwise':True})
                        try:
                            end,er=d25.integrate(r7,mod6,mod7,bg,tag,k,first,x1,x2,rr,cc,n)
                            endmetric=d25.metric_from_y(r7,op2,end,ib)
                            if not np.isfinite(end).all() or not np.isfinite((er,endmetric['relative_backward'],
                                                                            endmetric['absolute_residual'])).all():
                                raise FloatingPointError('nonfinite D36 second-interval endpoint')
                        except (RuntimeError,ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:
                            q={'mode':m,'beta':b,'substeps':n,'reason':'NUMERICAL_OR_OPERATOR_EXCEPTION',
                               'exception':type(exc).__name__,'detail':str(exc)}
                            failures.append(q)
                            print(f'GE19_D36_ENDPOINT_UNEVALUATED m={m} beta={b} n={n} reason={q["exception"]}: {q["detail"]}',flush=True)
                            continue
                        arrays['second_interval_x2_8'][im,ib,ins]=end
                        arrays['second_interval_x2_valid'][im,ib,ins]=True
                        arrays['second_interval_relative_shift'][im,ib,ins]=endmetric['relative_backward']
                        arrays['second_interval_absolute_shift'][im,ib,ins]=endmetric['absolute_residual']
                        arrays['second_interval_Radau_backward'][im,ib,ins]=er
                        row={'mode':m,'beta':b,'substeps':n,'start_shift':start,'shift':endmetric,
                             'Radau_block_backward_report_only':float(er),
                             'passes_original_shift_gate':bool(endmetric['relative_backward']<=pre['original_shift_gate']),
                             'state_transfer_without_reprojection':True}
                        rows.append(row)
                        print(f'GE19_D36_CASE m={m} beta={b} n={n} shift={endmetric["relative_backward"]:.6e} '
                              f'abs={endmetric["absolute_residual"]:.6e} gate={row["passes_original_shift_gate"]} Radau={er:.3e}',flush=True)
            summary=summarize(rows,failures,modes,betas,substeps,pre['original_shift_gate'])
            report.update(summary);report['per_case']=rows;report['failed_second_interval_evolutions']=failures
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
    if report['all_endpoints_evaluated']:
        report['classification']='GE19_D36_SECOND_INTERVAL_ALL_MODE_COHORT_EVALUATED_DIAGNOSTIC_PARENTS_UNCERTIFIED'
    else:
        report['classification']='GE19_D36_SECOND_INTERVAL_INCOMPLETE_DIAGNOSTIC_PARENTS_UNCERTIFIED'
    # Only finite valid results can be used in a later continuation: NaN slots are masked.
    if not all(np.isfinite(v).all() for key,v in arrays.items()
               if key not in ('second_interval_relative_shift','second_interval_absolute_shift','second_interval_Radau_backward')):
        raise RuntimeError('D36 nonfinite saved state/mask')
    valid=arrays['second_interval_x2_valid']
    for key in ('second_interval_relative_shift','second_interval_absolute_shift','second_interval_Radau_backward'):
        if not (np.isfinite(arrays[key][valid]).all() and np.isnan(arrays[key][~valid]).all()):
            raise RuntimeError('D36 invalid/missing endpoint metric mask')
    jp.parent.mkdir(parents=True,exist_ok=True);zp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    np.savez_compressed(zp,**arrays)
    print('GE19_D36_COHORT evaluated='+str(report['evaluated_endpoint_count'])+
          ' unevaluated='+str(report['unevaluated_endpoint_count'])+
          ' observed_shift_gate_fails='+str(report['observed_shift_gate_fail_count'])+
          ' all_gate_pass='+str(report['all_original_shift_gates_pass']),flush=True)
    print('GE19_D36_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':main()
