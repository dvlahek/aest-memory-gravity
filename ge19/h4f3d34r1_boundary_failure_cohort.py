#!/usr/bin/env python3
"""GE19 D34R1: freeze failed D34 and audit all original boundary starts.

This is an independent numerical representation diagnostic, NOT a full-window
H3 solve or a certification. Every reduced evolving m=1..40 is included for
all three original beta values with original n=1 and n=8 Radau schedules.
The m=0 source is retained in the frozen source arrays but the original
reduced evolution excludes k=0; do not silently substitute a k=0 solver.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d34_all_mode_first_interval_gate_scan as d34
d33=d34.d33

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d34r1_boundary_failure_cohort_prereg.json'
LOCK=ROOT/'ge19/h4f3d34r1_boundary_failure_cohort_lock.json'
TINY=1e-300


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for buf in iter(lambda:f.read(1<<20),b''):
            h.update(buf)
    return h.hexdigest()


def rel(a,b):
    a=np.asarray(a,complex);b=np.asarray(b,complex)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))


def complex_pair(z):
    z=complex(z)
    return [float(z.real),float(z.imag)]


def assess(rows, modes, betas, substeps, limit):
    expected={(int(m),float(b),int(n)) for m in modes for b in betas for n in substeps}
    observed=[(int(r['mode']),float(r['beta']),int(r['substeps'])) for r in rows]
    if len(observed)!=len(expected) or set(observed)!=expected or len(observed)!=len(set(observed)):
        raise RuntimeError('D34 incomplete or duplicated mode/beta/substep cohort')
    if not all(np.isfinite([float(r['shift']['relative_backward']),
                            float(r['shift']['absolute_residual'])]).all() for r in rows):
        raise RuntimeError('D34 nonfinite original shift metrics')
    failed=[{'mode':int(r['mode']),'beta':float(r['beta']),'substeps':int(r['substeps']),
             'relative_backward':float(r['shift']['relative_backward'])}
            for r in rows if float(r['shift']['relative_backward'])>limit]
    return {'all_case_count':len(expected),'shift_gate_fail_count':len(failed),
            'all_first_interval_original_shift_gates_pass':not failed,
            'failed_original_shift_gates':failed,
            'max_shift_relative_backward':max(float(r['shift']['relative_backward']) for r in rows),
            'max_shift_absolute_residual':max(float(r['shift']['absolute_residual']) for r in rows)}


def summarize_observed(rows,boundary_failed,modes,betas,substeps,limit,attempts):
    expected_attempts={(int(m),float(b)) for m in modes for b in betas}
    if len(attempts)!=len(expected_attempts) or set(attempts)!=expected_attempts or len(attempts)!=len(set(attempts)):
        raise RuntimeError('D34R1 missing/duplicate original boundary attempts')
    fail_keys={(int(r['mode']),float(r['beta'])) for r in boundary_failed}
    if len(fail_keys)!=len(boundary_failed) or not fail_keys.issubset(expected_attempts):
        raise RuntimeError('D34R1 invalid boundary failure ledger')
    planned={(int(m),float(b),int(n)) for m in modes for b in betas for n in substeps}
    observed=[(int(r['mode']),float(r['beta']),int(r['substeps'])) for r in rows]
    if len(observed)!=len(set(observed)) or not set(observed).issubset(planned):
        raise RuntimeError('D34R1 duplicated/foreign shifted cases')
    omitted=planned-set(observed)
    expected_omitted={(m,b,int(n)) for m,b in fail_keys for n in substeps}
    if omitted!=expected_omitted:
        raise RuntimeError('D34R1 unrecorded missing evolution or failed-boundary evolution')
    failures=[{'mode':int(r['mode']),'beta':float(r['beta']),'substeps':int(r['substeps']),
               'relative_backward':float(r['shift']['relative_backward'])}
              for r in rows if float(r['shift']['relative_backward'])>limit]
    if not all(np.isfinite([float(r['shift']['relative_backward']),float(r['shift']['absolute_residual'])]).all() for r in rows):
        raise RuntimeError('D34R1 nonfinite observed shift metrics')
    complete=(not omitted)
    # The original D34 assessor is applied without modification ONLY if 240 genuine endpoint values exist.
    original=assess(rows,modes,betas,substeps,limit) if complete else None
    return {'all_case_count':len(planned), 'boundary_attempt_count':len(attempts),
            'initial_boundary_failure_count':len(boundary_failed),
            'evaluated_shift_case_count':len(observed),'unevaluated_shift_case_count':len(omitted),
            'all_240_shift_cases_evaluated':complete,
            'all_first_interval_original_shift_gates_pass': original['all_first_interval_original_shift_gates_pass'] if complete else None,
            'shift_gate_fail_count':original['shift_gate_fail_count'] if complete else None,
            'observed_shift_gate_fail_count':len(failures),
            'failed_original_shift_gates':original['failed_original_shift_gates'] if complete else None,
            'failed_original_shift_gates_observed':failures,
            'max_shift_relative_backward':max((float(r['shift']['relative_backward']) for r in rows),default=None),
            'max_shift_absolute_residual':max((float(r['shift']['absolute_residual']) for r in rows),default=None)}


def check_self(rd,pre,lock):
    if pre['classification']!='GE19_D34R1_PREEXEC_FAILED_BOUNDARY_COHORT_LEDGER':
        raise RuntimeError('D34R1 preregistration mismatch')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!=pre['branch'] or branch=='main':
        raise RuntimeError('D34R1 wrong branch/main forbidden')
    for path,want in lock['sha256_local_files'].items():
        if not (ROOT/path).is_file() or sha(ROOT/path)!=want:
            raise RuntimeError('D34R1 self SHA lock FAIL '+path)
    for path,want in pre['original_D34_frozen_code_sha256'].items():
        if not (ROOT/path).is_file() or sha(ROOT/path)!=want:
            raise RuntimeError('D34R1 original D34 frozen code changed '+path)
    if tuple(pre['modes'])!=tuple(range(1,41)) or tuple(pre['betas'])!=(1.0,0.5,0.1) or \
       tuple(pre['substeps'])!=(1,8) or pre['original_shift_gate']!=pre['original_boundary_backward_gate'] or \
       pre['original_shift_gate']!=1e-6:
        raise RuntimeError('D34R1 original cohort or thresholds changed')
    if pre['original_D34_fail_log_sha256']:
        log=rd/pre['original_D34_fail_log_name']
        if not log.is_file() or sha(log)!=pre['original_D34_fail_log_sha256'] or \
           'D34 original two-row boundary projection FAIL m=26 beta=1.0' not in log.read_text():
            raise RuntimeError('D34R1 original D34 FAIL log changed or absent')
    frozen,j33=d34.check_self(rd,json.loads(d34.PRE.read_text()),json.loads(d34.LOCK.read_text()))
    print('GE19_D34R1_IMMUTABLE_D34_FAILURE_AND_ALL_ORIGINAL_ACTION_PARENT_LOCK_PASS',flush=True)
    return frozen,j33


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    a=ap.parse_args()
    rd=Path(a.results_dir).resolve();jp=Path(a.json_out).resolve();zp=Path(a.npz_out).resolve()
    if jp.exists() or zp.exists():
        raise RuntimeError('D34R1 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    frozen,j33=check_self(rd,pre,lock)
    d32=d33.d32;d31=d32.d31;d25=d31.d25
    r7=d25.d20.source.old.r7
    betas=tuple(float(v) for v in pre['betas']);modes=tuple(int(v) for v in pre['modes'])
    substeps=tuple(int(v) for v in pre['substeps'])
    j33_cases={(int(v['mode']),float(v['beta'])):v for v in j33['per_case']}
    support={int(row['mode']) for row in j33['GE07_original_vs_direct_modes']
             if row['exact_smooth_GE07_quadratic_supported']}
    if support!=set(pre['exact_quadratic_support']):
        raise RuntimeError('D34 signed source analytic harmonic support changed')
    report={
        'classification':'GE19_D34R1_BOUNDARY_COHORT_INCOMPLETE_SHIFT_DIAGNOSTIC_PARENTS_UNCERTIFIED',
        'preregistration':pre['classification'],'source_sha256':sha(Path(__file__)),
        'scope':'Frozen D33 candidate C, Cstar Nt128 FIRST INTERVAL m1..40, beta 1/0.5/0.1, n1/n8. No new source construction or full-window evolution. The original reduced H3 k0 mode is not an evolving case; its source stays frozen and is not discarded.',
        'claim_boundary':'First-interval numerical gate scan only; not a continuum error bound, H1 on-shell/Noether or full-window H3/H4 Ward proof. Original D22A failures immutable. No certified Z11/Z20/Z21/lensing.',
        'D22A_original_science_FAIL_immutable':True,'D27_original_triplet_FAIL_immutable':True,
        'D31_original_remainder_FAIL_immutable':True,'D33_diagnostic_only':True,
        'D34_original_m26_boundary_FAIL_immutable':True,
        'original_action_modified':False,'production_H3F_source_modified':False,
        'nonanalytic_StageE_Y_retained':True,'all_reduced_modes_m1_to_m40_retained':True,
        'm0_source_retained_separate_from_reduced_k0_evolution':True,
        'boundary_rule_unchanged_momenta_reprojected':True,
        'original_shift_gate_unchanged':True,'no_observational_tuning':True,
        'H3_full_window_solve_performed':False,'q20_B20_recomputed':False,
        'Z11_certified':False,'Z20_certified':False,'Z21_certified':False,
        'full_H4_Ward_certified':False,'lensing_licensed':False,
        'original_D33_selected_control_replayed':False,
        'per_case':[],'per_beta_summary':{},'source_checks':{},
        'failed_initial_projections':[],'all_initial_boundary_attempts':[],
        'original_D34_failure_log_sha256':pre['original_D34_fail_log_sha256'],
        'missing_endpoint_values_are_not_science_passes':True
    }
    arrays={'modes':np.asarray(modes,int),'betas':np.asarray(betas,float),
            'substeps':np.asarray(substeps,int),
            'candidate_C_y0_by_mode_beta_8':np.zeros((40,3,8),complex),
            'candidate_C_y1_by_mode_beta_substep_8':np.zeros((40,3,2,8),complex),
            'candidate_C_y0_valid_by_mode_beta':np.zeros((40,3),bool),
            'candidate_C_y1_valid_by_mode_beta_substep':np.zeros((40,3,2),bool)}
    with ExitStack() as es:
        z22=es.enter_context(np.load(frozen['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z33=es.enter_context(np.load(rd/pre['D33_npz'],allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        if x.shape!=(128,) or not np.array_equal(x,np.asarray(z22['x_primary'],float)) or \
           tuple(float(v) for v in r7.BETAS)!=betas:
            raise RuntimeError('D34 frozen Cstar/time/beta cohort changed')
        C={}
        for ib,beta in enumerate(betas):
            ma=np.asarray(z33[f'beta{ib}_candidate_C_main_six_by_128_by_41'],complex)
            co=np.asarray(z33[f'beta{ib}_candidate_C_constraint_two_by_128_by_41'],complex)
            if ma.shape!=(6,128,41) or co.shape!=(2,128,41) or \
               not (np.isfinite(ma).all() and np.isfinite(co).all()):
                raise RuntimeError('D34 frozen D33 candidate C array invalid beta='+str(beta))
            C[beta]={'rhs':ma,'rhs_constraint':co}
            if not all(np.array_equal(co[0,:,m],np.zeros(128,complex))
                       for m in range(41) if m not in support):
                raise RuntimeError('D34 offsupport original-action GE06/GE07 shift must vanish')
            if not j33['per_beta_source'][str(beta)]['Y_preserved_main_scalar_m1_m14'] or \
               not all(np.any(ma[3,:,m]) for m in (1,14)):
                raise RuntimeError('D34 original nonanalytic Y retention lost')
            report['source_checks'][str(beta)]={
                'offsupport_shift_zero_all_19':True,
                'm1_m14_beta_specific_Y_scalar_retained':True,
                'm0_source_max_abs_report_only':float(max(np.max(np.abs(ma[:,:,0])),np.max(np.abs(co[:,:,0]))))}
        print('GE19_D34_ALL_BETA_M0_SOURCE_RETAINED_AND_OFFSUPPORT_SHIFT_ZERO_PASS',flush=True)
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            if active['ctx'] is None:
                raise RuntimeError('D34R1 original-action clock not ready')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH)
            active['ctx']=ctx;ctx.knot_check()
            x0,x1=float(x[0]),float(x[1])
            for im,m in enumerate(modes):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                rf,cf=r7._source_interp(x,C,m)
                op0=d25.shift_at(r7,mod6,mod7,bg,tag,k,x0,None,rf,cf)
                op1=d25.shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rf,cf)
                for ib,beta in enumerate(betas):
                    report['all_initial_boundary_attempts'].append([int(m),float(beta)])
                    rank_error=None
                    try:
                        y0,projection=d31.projection(r7,mod6,mod7,bg,tag,k,x0,rf,cf,ib)
                    except RuntimeError as exc:
                        if str(exc)!='D31 candidate original two-row projection rank FAIL':
                            raise
                        rank_error=str(exc);y0=None;projection=None
                    initial=d25.metric_from_y(r7,op0,y0,ib) if y0 is not None else None
                    metrics=([projection['lapse_relative_backward'],projection['shift_relative_backward'],
                              initial['relative_backward']] if rank_error is None else [])
                    projection_pass=(rank_error is None and np.isfinite(metrics).all() and
                                     max(metrics)<=pre['original_boundary_backward_gate'])
                    if not projection_pass:
                        src0=np.asarray(rf(x0),complex)[:,ib]
                        con0=np.asarray(cf(x0),complex)[:,ib]
                        record={'mode':int(m),'beta':float(beta),'support':bool(m in support),
                                'reason':rank_error or 'ORIGINAL_1E_MINUS_6_BOUNDARY_BACKWARD_GATE_FAIL',
                                'projection':projection,'initial_shift':initial,
                                'original_boundary_backward_gate':pre['original_boundary_backward_gate'],
                                'first_main_source_signed':[complex_pair(v) for v in src0],
                                'first_constraint_source_signed':[complex_pair(v) for v in con0],
                                'initial_state_signed':[complex_pair(v) for v in y0] if y0 is not None else None}
                        report['failed_initial_projections'].append(record)
                        print(f'GE19_D34R1_ORIGINAL_BOUNDARY_FAILURE m={m} beta={beta} '
                              f'projection={projection} initial_shift={initial}',flush=True)
                        # The unmodified physical gate is FAILED. No Radau evolution for this
                        # (mode,beta), and its n1/n8 endpoints remain invalid masked slots.
                        continue
                    arrays['candidate_C_y0_by_mode_beta_8'][im,ib]=y0
                    arrays['candidate_C_y0_valid_by_mode_beta'][im,ib]=True
                    sel=j33_cases.get((m,beta))
                    if sel is not None:
                        key=f'm{m}_beta{str(beta).replace(".","p")}'
                        if rel(y0,np.asarray(z33[f'{key}_candidate_C_y0'],complex))>pre['original_D33_state_replay_limit']:
                            raise RuntimeError('D34 frozen D33 selected y0 replay FAIL '+key)
                    def rr(t,fun=rf,index=ib):
                        return np.asarray(fun(t),complex)[:,index:index+1]
                    def cc(t,fun=cf,index=ib):
                        return np.asarray(fun(t),complex)[:,index:index+1]
                    for ins,n in enumerate(substeps):
                        y1,er=d25.integrate(r7,mod6,mod7,bg,tag,k,y0,x0,x1,rr,cc,n)
                        measured=d25.metric_from_y(r7,op1,y1,ib)
                        if not (np.isfinite(y1).all() and np.isfinite(er)):
                            raise RuntimeError(f'D34 nonfinite H3 first interval m={m} beta={beta} n={n}')
                        arrays['candidate_C_y1_by_mode_beta_substep_8'][im,ib,ins]=y1
                        arrays['candidate_C_y1_valid_by_mode_beta_substep'][im,ib,ins]=True
                        if sel is not None:
                            key=f'm{m}_beta{str(beta).replace(".","p")}'
                            archived=np.asarray(z33[f'{key}_n{n}_candidate_C_y1'],complex)
                            old=next(q for q in sel['comparisons'] if q['substeps']==n)
                            om=old['candidate_C_independent_shift']['relative_backward']
                            if rel(y1,archived)>pre['original_D33_state_replay_limit'] or \
                               abs(measured['relative_backward']-om)>pre['original_D33_metric_replay_limit']*max(abs(om),abs(measured['relative_backward']),TINY):
                                raise RuntimeError(f'D34 frozen D33 selected endpoint/metric replay FAIL {key} n={n}')
                        report['per_case'].append({
                            'mode':m,'beta':beta,'substeps':n,
                            'exact_smooth_action_quadratic_support':m in support,
                            'original_two_row_initial_projection':projection,
                            'initial_shift':initial,'shift':measured,
                            'Radau_block_backward_report_only':float(er),
                            'passes_original_shift_gate':bool(measured['relative_backward']<=pre['original_shift_gate'])})
                        print(f'GE19_D34_CASE m={m} beta={beta} n={n} '
                              f'support={m in support} shift={measured["relative_backward"]:.6e} '
                              f'abs={measured["absolute_residual"]:.6e} '
                              f'gate={measured["relative_backward"]<=pre["original_shift_gate"]} '
                              f'Radau={er:.3e}',flush=True)
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
    report['original_D33_selected_control_replayed']=all(
        all(any(r['mode']==m and r['beta']==b and r['substeps']==n for r in report['per_case'])
            for n in substeps) for m,b in pre['original_D33_replay_cases'])
    report.update(summarize_observed(report['per_case'],report['failed_initial_projections'],
                                     modes,betas,substeps,pre['original_shift_gate'],
                                     [tuple(q) for q in report['all_initial_boundary_attempts']]))
    if report['all_240_shift_cases_evaluated'] and report['original_D33_selected_control_replayed']:
        report['classification']='GE19_D34R1_ALL_M1_TO_M40_ALL_BETA_FIRST_INTERVAL_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
    elif not report['original_D33_selected_control_replayed']:
        report['classification']='GE19_D34R1_FROZEN_D33_CONTROL_REPLAY_UNRESOLVED_BOUNDARY_DIAGNOSTIC'
    for beta in betas:
        selected=[r for r in report['per_case'] if r['beta']==beta]
        report['per_beta_summary'][str(beta)]={
            'evaluated_case_count':len(selected),
            'unevaluated_case_count':len(modes)*len(substeps)-len(selected),
            'boundary_failure_count':sum(q['beta']==beta for q in report['failed_initial_projections']),
            'shift_gate_fail_count_observed':sum(not r['passes_original_shift_gate'] for r in selected),
            'max_shift_relative_backward_observed':max((r['shift']['relative_backward'] for r in selected),default=None),
            'max_Radau_block_backward_report_only':max((r['Radau_block_backward_report_only'] for r in selected),default=None)}
    if not all(np.isfinite(v).all() for v in arrays.values()):
        raise RuntimeError('D34 output nonfinite')
    jp.parent.mkdir(parents=True,exist_ok=True);zp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    np.savez_compressed(zp,**arrays)
    print('GE19_D34R1_BOUNDARY_ATTEMPTS '+str(report['boundary_attempt_count'])+
          ' FAILED_INITIAL_PROJECTIONS '+str(report['initial_boundary_failure_count'])+
          ' EVALUATED_ENDPOINTS '+str(report['evaluated_shift_case_count'])+
          ' UNEVALUATED_ENDPOINTS '+str(report['unevaluated_shift_case_count'])+
          ' OBSERVED_SHIFT_GATE_FAILS '+str(report['observed_shift_gate_fail_count']),flush=True)
    print('GE19_D34R1_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':
    main()
