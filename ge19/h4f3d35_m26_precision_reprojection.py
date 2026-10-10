#!/usr/bin/env python3
"""GE19 D35: pre-registered roundoff-only momentum representation, m26 only.

Reproduce immutable D34R1 original boundary FAIL first. On original-action
candidate-C off-support m26 with EXACT zero shift/anisotropy source at all knots,
zero only computed nonzero momenta below 16eps times the largest computed p.
This does not change the original two-row boundary equations, H3 source,
original backward metric, Radau scheme, or any parent. The candidate no longer
claims a bitwise identical Repair18 min-norm momentum. It is an independent
floating-point representation test, not H3/Noether certification.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d34r1_boundary_failure_cohort as d34r1

d34=d34r1.d34;d33=d34r1.d33;d32=d33.d32;d31=d32.d31;d25=d31.d25
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d35_m26_precision_reprojection_prereg.json'
LOCK=ROOT/'ge19/h4f3d35_m26_precision_reprojection_lock.json'
TINY=1e-300


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()


def signed(z):
    q=complex(z);return [float(q.real),float(q.imag)]


def rel(a,b):
    a=np.asarray(a,complex);b=np.asarray(b,complex)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))


def zero_subroundoff_momenta(p, constraint_source, multiplier):
    """Predetermined precision hypothesis. Never infer tolerance from endpoints.

    The shift source must be EXACT zero in the stored original source. This is
    valid ONLY on analytically off-support frozen candidate C. This operation
    is diagnostic and does not reproduce bitwise Repair18 min-norm output.
    """
    p=np.asarray(p,complex)
    c=np.asarray(constraint_source,complex)
    if p.shape!=(4,) or c.shape!=(2,) or not np.all(np.isfinite(p)) or \
       not np.array_equal(c,np.zeros(2,complex)) or not (0<multiplier<=16):
        raise ValueError('D35 precision candidate requires finite 4p and exact 2x zero constraint source')
    largest=float(np.max(np.abs(p)))
    if largest==0.:raise ValueError('D35 no nonzero momentum to diagnose')
    cutoff=float(multiplier*np.finfo(float).eps*largest)
    mask=(np.abs(p)>0)&(np.abs(p)<=cutoff)
    out=p.copy();out[mask]=0.0+0.0j
    return out,mask,cutoff


def check_inputs(rd,pre,lock):
    if pre['classification']!='GE19_D35_PREEXEC_M26_PRECISION_REPROJECTION_AUDIT' or \
       pre['target_mode']!=26 or pre['tiny_component_multiplier_of_float64_epsilon']!=16 or \
       pre['original_shift_gate']!=1e-6 or pre['original_boundary_backward_gate']!=1e-6 or \
       pre['betas']!=[1.0,0.5,0.1] or pre['substeps']!=[1,8] or \
       pre['modes']!=list(range(1,41)):
        raise RuntimeError('D35 preregistered original cohort/threshold/precision method mismatch')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!=pre['branch'] or branch=='main':raise RuntimeError('D35 wrong branch/main forbidden')
    for path,want in lock['sha256_local_files'].items():
        if not (ROOT/path).is_file() or sha(ROOT/path)!=want:
            raise RuntimeError('D35 self SHA lock FAIL '+path)
    for path,want in pre['frozen_original_D34R1_code_sha256'].items():
        if not (ROOT/path).is_file() or sha(ROOT/path)!=want:
            raise RuntimeError('D35 frozen original D34R1 code changed '+path)
    for name,want in pre['frozen_original_D34R1_output_sha256'].items():
        if not (rd/name).is_file() or sha(rd/name)!=want:
            raise RuntimeError('D35 frozen D34R1 diagnostic output changed '+name)
    original=json.loads((rd/'ge19_h4f3d34r1_boundary_failure_cohort.json').read_text())
    if original['classification']!=pre['required_D34R1_classification'] or \
       original['evaluated_shift_case_count']!=234 or original['unevaluated_shift_case_count']!=6 or \
       original['observed_shift_gate_fail_count']!=0 or \
       sorted((q['mode'],q['beta']) for q in original['failed_initial_projections'])!=sorted(map(tuple,pre['required_original_failures'])) or \
       original['all_first_interval_original_shift_gates_pass'] is not None:
        raise RuntimeError('D35 frozen D34R1 original failure ledger mismatch')
    old_pre=json.loads(d34r1.PRE.read_text());old_lock=json.loads(d34r1.LOCK.read_text())
    frozen,j33=d34r1.check_self(rd,old_pre,old_lock)
    if not (original['D34_original_m26_boundary_FAIL_immutable'] and
            original['m0_source_retained_separate_from_reduced_k0_evolution'] and
            original['nonanalytic_StageE_Y_retained']):
        raise RuntimeError('D35 original action/Y/m0 historical boundary mismatch')
    print('GE19_D35_IMMUTABLE_D34R1_234_PLUS_SIX_UNEVALUATED_AND_ALL_PARENT_SHA_PASS',flush=True)
    return original,frozen,j33


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True);ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    a=ap.parse_args();rd=Path(a.results_dir).resolve();jp=Path(a.json_out).resolve();zp=Path(a.npz_out).resolve()
    if jp.exists() or zp.exists():raise RuntimeError('D35 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    original,frozen,j33=check_inputs(rd,pre,lock)
    failed_original={(v['mode'],v['beta']):v for v in original['failed_initial_projections']}
    modes=tuple(pre['modes']);betas=tuple(pre['betas']);substeps=tuple(pre['substeps']);m=26
    r7=d25.d20.source.old.r7
    report={
      'classification':'GE19_D35_M26_PRECISION_REPROJECTION_FIRST_INTERVAL_INCOMPLETE_PARENTS_UNCERTIFIED',
      'preregistration':pre['classification'],'source_sha256':sha(__file__),
      'scope':'Frozen candidate C FIRST INTERVAL only: m26 all three beta values, n1/n8. Frozen other 234 D34R1 endpoints copied by SHA reference only. Precision-zeroed m26 momenta differ by float64-subroundoff components from original Repair18 minimum-norm solution; not bitwise original projection. Original D34/D34R1 FAIL immutable.',
      'claim_boundary':'Posthoc numerical precision representation hypothesis; NOT a rigorous roundoff envelope or a proof of on-shell H1/Noether/H3/H4 Ward, Z20, Z21 or lensing. Any unresolved m26 initial/endpoint remains UNEVALUATED/FAILED, not silently a PASS.',
      'D22A_original_science_FAIL_immutable':True,'D34_original_m26_boundary_FAIL_immutable':True,
      'D34R1_original_m26_three_boundary_FAIL_immutable':True,
      'D34R1_234_observed_endpoints_SHA_frozen':True,
      'H3_full_window_solve_performed':False,'Z11_certified':False,'Z20_certified':False,
      'Z21_certified':False,'full_H4_Ward_certified':False,'lensing_licensed':False,
      'original_action_modified':False,'production_H3F_source_modified':False,
      'original_shift_gate_unchanged':True,'nonanalytic_StageE_Y_retained':True,
      'all_modes_retained':True,'m0_source_retained_separately':True,
      'new_projection_is_roundoff_representation_not_bitwise_repair18':True,
      'source_based_original_boundary_rule_and_shift_metric_retained':True,
      'original_d34r1_counts':{'observed_endpoints':234,'unevaluated_endpoints':6,'failed_initial_projections':3},
      'm26_per_beta':[],'D35_new_endpoint_count':0,'D35_new_endpoint_original_shift_gate_fail_count':0,
      'D35_all_240_endpoint_values_evaluated':False,'D35_all_240_first_interval_shift_gates_pass':None,
      'D35_shift_gate_fail_count':None,'D35_unevaluated_endpoint_count':6,
      'D35_observed_shift_gate_fail_count':0,
      'D35_frozen_and_new_endpoint_no_duplicate':True,
    }
    arrays={'m26_betas':np.asarray(betas,float),'m26_substeps':np.asarray(substeps,int),
      'm26_original_y0_by_beta_8':np.zeros((3,8),complex),
      'm26_roundoff_candidate_y0_by_beta_8':np.zeros((3,8),complex),
      'm26_candidate_y1_by_beta_substep_8':np.zeros((3,2,8),complex),
      'm26_original_y0_valid_by_beta':np.zeros((3,),bool),
      'm26_candidate_y0_valid_by_beta':np.zeros((3,),bool),
      'm26_candidate_y1_valid_by_beta_substep':np.zeros((3,2),bool)}
    new_rows=[];failed_new=[]
    with ExitStack() as es:
        z22=es.enter_context(np.load(frozen['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z33=es.enter_context(np.load(rd/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz',allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        if x.shape!=(128,) or not np.array_equal(x,np.asarray(z22['x_primary'],float)) or tuple(r7.BETAS)!=betas:
            raise RuntimeError('D35 original action background/time/beta mismatch')
        src={}
        for ib,b in enumerate(betas):
            ma=np.asarray(z33[f'beta{ib}_candidate_C_main_six_by_128_by_41'],complex)
            co=np.asarray(z33[f'beta{ib}_candidate_C_constraint_two_by_128_by_41'],complex)
            if ma.shape!=(6,128,41) or co.shape!=(2,128,41) or \
               not np.array_equal(co[:,:,m],np.zeros((2,128),complex)) or not np.any(ma[3,:,m]):
                raise RuntimeError('D35 exact zero original candidate-C constraint source or preserved scalar Y lost')
            src[b]={'rhs':ma,'rhs_constraint':co}
        if next(v for v in j33['GE07_original_vs_direct_modes'] if v['mode']==26)['exact_smooth_GE07_quadratic_supported'] is not False:
            raise RuntimeError('D35 m26 analytic support changed')
        print('GE19_D35_M26_ALL_128_EXACT_ZERO_SHIFT_AND_NONANALYTIC_Y_RETAINED_PASS',flush=True)
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            if active['ctx'] is None:raise RuntimeError('D35 original-action clock not ready')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            x0,x1=float(x[0]),float(x[1]);k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
            rf,cf=r7._source_interp(x,src,m)
            op0=d25.shift_at(r7,mod6,mod7,bg,tag,k,x0,None,rf,cf)
            op1=d25.shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rf,cf)
            for ib,b in enumerate(betas):
                yorig,oproj=d31.projection(r7,mod6,mod7,bg,tag,k,x0,rf,cf,ib)
                initial_orig=d25.metric_from_y(r7,op0,yorig,ib)
                old_record=failed_original[(m,b)]
                old_y=np.array([complex(*q) for q in old_record['initial_state_signed']],complex)
                if rel(yorig,old_y)>1e-13 or \
                   abs(initial_orig['absolute_residual']-old_record['initial_shift']['absolute_residual'])>1e-12*max(abs(initial_orig['absolute_residual']),1e-300) or \
                   initial_orig['relative_backward']<=pre['original_boundary_backward_gate']:
                    raise RuntimeError(f'D35 original D34R1 m26 failure replay mismatch beta={b}')
                arrays['m26_original_y0_by_beta_8'][ib]=yorig;arrays['m26_original_y0_valid_by_beta'][ib]=True
                srcc=np.asarray(cf(x0),complex)[:,ib]
                ynew=yorig.copy()
                pnew,mask,cutoff=zero_subroundoff_momenta(yorig[4:8],srcc,pre['tiny_component_multiplier_of_float64_epsilon'])
                ynew[4:8]=pnew
                delta=rel(ynew,yorig)
                row={'mode':m,'beta':b,'original_initial_shift':initial_orig,
                     'original_min_norm_projection':oproj,
                     'zeroed_momentum_indices':[int(q) for q in np.flatnonzero(mask)],
                     'tiny_component_cutoff_report_only':cutoff,
                     'original_vs_candidate_y0_relative_report_only':delta,
                     'candidate_momentum_representation_is_bitwise_original':bool(np.array_equal(ynew,yorig)),
                     'candidate_initial':None,'candidate_initial_projected_lapse_relative':None,
                     'candidate_initial_projected_shift_relative':None,
                     'candidate_initial_original_boundary_gate_pass':False,
                     'new_evolutions':[], 'unevaluated_n':[1,8]}
                if not mask.any() or delta>32*np.finfo(float).eps:
                    row['classification']='D35_NOT_A_SUBROUNDOFF_MOMENTUM_DIFFERENCE'
                    failed_new.append({'mode':m,'beta':b,'reason':row['classification']})
                    report['m26_per_beta'].append(row)
                    print(f'GE19_D35_M26_CANDIDATE_NOT_LICENSED beta={b} reason={row["classification"]}',flush=True)
                    continue
                rr0=np.asarray(rf(x0),complex)[:,ib];cc0=np.asarray(cf(x0),complex)[:,ib]
                _,_,_,_,WY,WR,Cmat,_,_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,x0)
                evalnew=d31.d22a.r18.evaluate_candidate(Cmat,WY,WR,np.concatenate([rr0,cc0]),rr0,cc0,pnew)
                initial_new=d25.metric_from_y(r7,op0,ynew,ib)
                row.update({'candidate_initial':initial_new,
                      'candidate_initial_projected_lapse_relative':float(evalnew['lapse']['metric']),
                      'candidate_initial_projected_shift_relative':float(evalnew['shift']['metric'])})
                metric=(float(initial_new['relative_backward']),float(evalnew['lapse']['metric']),float(evalnew['shift']['metric']))
                boundary_pass=bool(np.isfinite(metric).all() and max(metric)<=pre['original_boundary_backward_gate'])
                row['candidate_initial_original_boundary_gate_pass']=boundary_pass
                if not boundary_pass:
                    row['classification']='D35_NUMERICAL_REPRESENTATION_BOUNDARY_GATE_FAIL'
                    failed_new.append({'mode':m,'beta':b,'reason':row['classification']})
                    report['m26_per_beta'].append(row)
                    print(f'GE19_D35_M26_BOUNDARY_GATE_FAIL beta={b} initial={initial_new["relative_backward"]:.6e} '
                          f'abs={initial_new["absolute_residual"]:.6e} zeroed={row["zeroed_momentum_indices"]}',flush=True)
                    continue
                arrays['m26_roundoff_candidate_y0_by_beta_8'][ib]=ynew
                arrays['m26_candidate_y0_valid_by_beta'][ib]=True
                row['classification']='D35_ORIGINAL_BOUNDARY_GATE_PASSED_RUN_ENDPOINTS'
                def rr(t,fun=rf,index=ib):return np.asarray(fun(t),complex)[:,index:index+1]
                def cc(t,fun=cf,index=ib):return np.asarray(fun(t),complex)[:,index:index+1]
                for ins,n in enumerate(substeps):
                    y1,er=d25.integrate(r7,mod6,mod7,bg,tag,k,ynew,x0,x1,rr,cc,n)
                    metric=d25.metric_from_y(r7,op1,y1,ib)
                    if not (np.isfinite(y1).all() and np.isfinite(er)):
                        raise RuntimeError(f'D35 nonfinite m26 endpoint beta={b} n={n}')
                    arrays['m26_candidate_y1_by_beta_substep_8'][ib,ins]=y1
                    arrays['m26_candidate_y1_valid_by_beta_substep'][ib,ins]=True
                    passed=bool(metric['relative_backward']<=pre['original_shift_gate'])
                    entry={'mode':m,'beta':b,'substeps':n,'shift':metric,
                         'passes_original_shift_gate':passed,
                         'Radau_block_backward_report_only':float(er),
                         'D35_changed_momentum_representation_only':True}
                    new_rows.append(entry)
                    row['new_evolutions'].append(entry)
                    row['unevaluated_n'].remove(n)
                    print(f'GE19_D35_M26 beta={b} n={n} shift={metric["relative_backward"]:.6e} '
                          f'abs={metric["absolute_residual"]:.6e} original_gate={passed} Radau={er:.3e}',flush=True)
                report['m26_per_beta'].append(row)
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
    combined=list(original['per_case'])+new_rows
    summarized=d34r1.summarize_observed(combined,failed_new,modes,betas,substeps,
                        pre['original_shift_gate'],[tuple(q) for q in original['all_initial_boundary_attempts']])
    report['D35_new_endpoint_count']=len(new_rows)
    report['D35_new_endpoint_original_shift_gate_fail_count']=sum(not q['passes_original_shift_gate'] for q in new_rows)
    report['D35_all_240_endpoint_values_evaluated']=summarized['all_240_shift_cases_evaluated']
    report['D35_all_240_first_interval_shift_gates_pass']=summarized['all_first_interval_original_shift_gates_pass']
    report['D35_shift_gate_fail_count']=summarized['shift_gate_fail_count']
    report['D35_unevaluated_endpoint_count']=summarized['unevaluated_shift_case_count']
    report['D35_observed_shift_gate_fail_count']=summarized['observed_shift_gate_fail_count']
    report['D35_failed_boundary_attempts']=failed_new
    report['D35_original_shift_gate_evaluated_max_relative']=summarized['max_shift_relative_backward']
    if len(new_rows)==6 and summarized['all_240_shift_cases_evaluated']:
        report['classification']='GE19_D35_M26_SUBROUNDOFF_NUMERICAL_REPROJECTION_240_FIRST_INTERVAL_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
    if not all(np.isfinite(v).all() for v in arrays.values()):raise RuntimeError('D35 nonfinite output')
    jp.parent.mkdir(parents=True,exist_ok=True);zp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    np.savez_compressed(zp,**arrays)
    print('GE19_D35_COHORT new_endpoints='+str(len(new_rows))+' evaluated='+str(summarized['evaluated_shift_case_count'])+
          ' unevaluated='+str(summarized['unevaluated_shift_case_count'])+
          ' observed_original_shift_gate_fails='+str(summarized['observed_shift_gate_fail_count']),flush=True)
    print('GE19_D35_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':main()
