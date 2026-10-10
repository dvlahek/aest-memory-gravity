#!/usr/bin/env python3
"""GE19 D41: frozen 128-node candidate-C lapse/shift/anisotropy and canonical-algebraic audit.

NO new evolution, NO reprojection, NO source/threshold changes. Original D35 m26
subroundoff candidate is NOT bitwise Repair18. H1 on-shell, Noether, Ward and
full H3/H4 parent certification remain UNPROVEN irrespective of numeric gates.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d40_x64_x127_original_action_continuation as d40

d36=d40.d36;d35=d36.d35;d25=d35.d25;r18=d35.d31.d22a.r18
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d41_full_window_two_constraint_audit_prereg.json'
LOCK=ROOT/'ge19/h4f3d41_full_window_two_constraint_audit_lock.json'
TINY=1e-300
STEM='ge19_h4f3d41_full_window_two_constraint_audit'


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def check_complete_segment(z, start, end, modes, betas, subs, x, gate):
    """Reject corrupted or fabricated endpoint cohorts, and wrong/missing clocks."""
    n=end-start+1;shape=(n,40,3,2)
    if not (np.array_equal(z['clock_node_indices'],np.arange(start,end+1))
            and np.array_equal(z['clock_node_x'],x[start:end+1])
            and np.array_equal(z['modes'],modes) and np.array_equal(z['betas'],betas)
            and np.array_equal(z['substeps'],subs)):
        raise RuntimeError(f'D41 invalid frozen x{start}..x{end} cohort/clock')
    y=np.asarray(z['candidate_C_state_8_by_node_mode_beta_substep'],complex)
    v=np.asarray(z['candidate_C_state_numerically_evaluated'],bool)
    p=np.asarray(z['candidate_C_shift_original_gate_pass'],bool)
    met=np.asarray(z['candidate_C_shift_relative_backward'],float)
    ab=np.asarray(z['candidate_C_shift_absolute_residual'],float)
    if y.shape!=shape+(8,) or any(a.shape!=shape for a in (v,p,met,ab)) or \
       not np.all(v) or not np.all(p) or not np.array_equal(p,met<=gate) or \
       not np.isfinite(y).all() or not np.isfinite(met).all() or not np.isfinite(ab).all():
        raise RuntimeError(f'D41 incomplete/corrupt frozen x{start}..x{end} endpoints')
    return y,met,ab


def splice_full_window(z34,z35,z36,segments,j34,j35,j36,modes,betas,subs,x,gate):
    """Bitwise complete x0..x127 state/shift join; never fill unevaluated with zero."""
    if not (np.array_equal(modes,np.arange(1,41)) and np.array_equal(betas,[1.,.5,.1])
            and np.array_equal(subs,[1,8]) and x.shape==(128,) and np.all(np.diff(x)>0)):
        raise RuntimeError('D41 frozen clock/cohort changed')
    shp=(128,40,3,2);states=np.empty(shp+(8,),complex);shift=np.full(shp,np.nan)
    ab=np.full(shp,np.nan)
    old=np.asarray(z34['candidate_C_y0_by_mode_beta_8'],complex)
    oldv=np.asarray(z34['candidate_C_y0_valid_by_mode_beta'],bool)
    new=np.asarray(z35['m26_roundoff_candidate_y0_by_beta_8'],complex)
    newv=np.asarray(z35['m26_candidate_y0_valid_by_beta'],bool)
    if old.shape!=(40,3,8) or oldv.shape!=(40,3) or new.shape!=(3,8) or newv.shape!=(3,) or \
       np.any(oldv[25]) or not np.all(oldv[np.arange(40)!=25]) or not np.all(newv) or \
       not np.isfinite(old).all() or not np.isfinite(new).all():
        raise RuntimeError('D41 first-node D34R1/D35 provenance fail')
    old=old.copy();old[25]=new
    states[0]=np.repeat(old[:,: ,None,:],2,axis=2)
    j36rows={(q['mode'],q['beta'],q['substeps']):q for q in j36['per_case']}
    j34rows={(q['mode'],q['beta'],q['substeps']):q for q in j34['per_case']}
    j35rows={q['beta']:q for q in j35['m26_per_beta']}
    if len(j36rows)!=240 or len(j34rows)!=234 or len(j35rows)!=3:
        raise RuntimeError('D41 original x0/x1 JSON ledgers incomplete')
    for im,m in enumerate(modes):
        for ib,b in enumerate(betas):
            for ins,n in enumerate(subs):
                key=(int(m),float(b),int(n));q=j36rows.get(key)
                if q is None or not q['passes_original_shift_gate']:
                    raise RuntimeError('D41 first-two-interval parent missing '+str(key))
                if m!=26:
                    oldrow=j34rows.get(key)
                    if oldrow is None or not oldrow['passes_original_shift_gate'] or \
                       q['start_shift']!=oldrow['shift']:
                        raise RuntimeError('D41 original D34R1 first-endpoint gate mismatch '+str(key))
                    start=oldrow['initial_shift']
                else:
                    oldrow=j35rows[float(b)]
                    fresh=next((v for v in oldrow['new_evolutions'] if v['substeps']==n),None)
                    if fresh is None or not fresh['passes_original_shift_gate'] or \
                       fresh['shift']!=q['start_shift']:
                        raise RuntimeError('D41 original D35 m26 first-endpoint gate mismatch '+str(key))
                    start=oldrow['candidate_initial']
                shift[0,im,ib,ins]=start['relative_backward']
                ab[0,im,ib,ins]=start['absolute_residual']
                shift[1,im,ib,ins]=q['start_shift']['relative_backward']
                ab[1,im,ib,ins]=q['start_shift']['absolute_residual']
                if q['shift']['relative_backward']>gate:
                    raise RuntimeError('D41 original x2 gate not passed')
    for key,idx in (('first_interval_x1_8',1),('second_interval_x2_8',2)):
        a=np.asarray(z36[key],complex)
        v=np.asarray(z36['first_interval_x1_valid' if idx==1 else 'second_interval_x2_valid'],bool)
        if a.shape!=(40,3,2,8) or v.shape!=(40,3,2) or not np.all(v) or not np.isfinite(a).all():
            raise RuntimeError('D41 original D36 first/second states incomplete')
        states[idx]=a
    # x2 source-of-record D36 (including absolute endpoint metrics in JSON).
    for im,m in enumerate(modes):
        for ib,b in enumerate(betas):
            for ins,n in enumerate(subs):
                q=j36rows[int(m),float(b),int(n)]['shift']
                shift[2,im,ib,ins]=q['relative_backward']
                ab[2,im,ib,ins]=q['absolute_residual']
    if not np.array_equal(shift[2],np.asarray(z36['second_interval_relative_shift'],float)) or \
       not np.array_equal(ab[2],np.asarray(z36['second_interval_absolute_shift'],float)):
        raise RuntimeError('D41 original D36 JSON/NPZ x2 metric mismatch')
    joins=[]
    for start,end,z in segments:
        y,s,a=check_complete_segment(z,start,end,modes,betas,subs,x,gate)
        if not (np.array_equal(states[start],y[0]) and np.array_equal(shift[start],s[0])
                and np.array_equal(ab[start],a[0])):
            raise RuntimeError(f'D41 x{start} bitwise provenance/shift splice FAIL')
        states[start+1:end+1]=y[1:]
        shift[start+1:end+1]=s[1:]
        ab[start+1:end+1]=a[1:]
        joins.append(int(start))
    if joins!=[2,16,32,64] or not np.isfinite(states).all() or not np.isfinite(shift).all() or \
       not np.isfinite(ab).all() or np.max(shift)>gate:
        raise RuntimeError('D41 full-window state/clock/mask/gate incomplete')
    return states,shift,ab


def original_constraint_metrics(Cmat,WY,WR,rr,cc,y,ib):
    """Frozen Repair18 row geometry, applied to ACTUAL evolved y (not p-only q=0)."""
    rr=np.asarray(rr,complex);cc=np.asarray(cc,complex);y=np.asarray(y,complex)
    if rr.shape!=(6,3) or cc.shape!=(2,3) or y.shape!=(8,):
        raise RuntimeError('D41 invalid exact original source/state shape')
    ss=np.concatenate((rr[:,ib],cc[:,ib]));w=WY@y+WR@ss
    lapse=r18.backward_error(Cmat[4],w,rr[0,ib])
    shift=r18.backward_error(Cmat[10]+Cmat[11],w,cc[0,ib])
    aniso=r18.backward_error(Cmat[12]+Cmat[13],w,cc[1,ib])
    alg=np.vstack((Cmat[0:4],Cmat[5:6],Cmat[12:13]+Cmat[13:14]))
    targ=np.concatenate((y[4:8],[rr[5,ib],cc[1,ib]]))
    lhs=alg@w;rownorm=np.maximum(np.max(np.abs(alg),axis=1),TINY)
    a=(lhs-targ)/rownorm;ls=lhs/rownorm;ts=targ/rownorm
    rel=float(np.linalg.norm(a)/max(np.linalg.norm(ls),np.linalg.norm(ts),TINY))
    if not np.isfinite((lapse['metric'],shift['metric'],aniso['metric'],rel)).all():
        raise FloatingPointError('D41 nonfinite original-action constraint/algebraic audit')
    return float(lapse['metric']),float(shift['metric']),float(aniso['metric']),rel


def check_inputs(rd,pre,lock):
    if not (pre['classification']=='GE19_D41_PREEXEC_FULL_WINDOW_TWO_CONSTRAINT_AND_ANISOTROPY_AUDIT'
       and pre['branch']=='physics-first-gravitational-elasticity'
       and pre['clock_nodes']==128 and pre['expected_case_node_count']==30720
       and pre['original_boundary_backward_gate']==pre['original_shift_gate']==1e-6
       and pre['modes']==list(range(1,41)) and pre['betas']==[1.,.5,.1]
       and pre['substeps']==[1,8] and pre['no_new_evolution'] and pre['no_new_projection']
       and pre['no_science_cut_or_fitted_floor'] and pre['all_other_row_gates_are_report_only']):
        raise RuntimeError('D41 preregistered science/scope mismatch')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!=pre['branch'] or branch=='main':raise RuntimeError('D41 wrong branch/main forbidden')
    for key,want in lock['sha256_local_files'].items():
        if not (ROOT/key).is_file() or sha(ROOT/key)!=want:
            raise RuntimeError('D41 self SHA mismatch '+key)
    for key,want in pre['frozen_D40_code_sha256'].items():
        if not (ROOT/key).is_file() or sha(ROOT/key)!=want:
            raise RuntimeError('D41 frozen D40 code mismatch '+key)
    for key,want in pre['frozen_D40_result_sha256'].items():
        if not (rd/key).is_file() or sha(rd/key)!=want:
            raise RuntimeError('D41 frozen D40 result mismatch '+key)
    frozen,j35,j33,j36,j37,j38,j39=d40.check_inputs(rd,json.loads(d40.PRE.read_text()),json.loads(d40.LOCK.read_text()))
    j40=json.loads((rd/'ge19_h4f3d40_x64_x127_original_action_continuation.json').read_text())
    if not (j40['classification']=='GE19_D40_X64_X127_ALL_MODE_COHORT_EVALUATED_DIAGNOSTIC_PARENTS_UNCERTIFIED'
            and j40['expected_new_endpoint_count']==j40['evaluated_new_endpoint_count']==15120
            and j40['unevaluated_new_endpoint_count']==j40['observed_original_shift_gate_fail_count']==0
            and j40['all_new_endpoints_evaluated'] and j40['all_original_shift_gates_pass']
            and j40['D35_m26_posthoc_momentum_representation_not_original_bitwise']
            and j40['D22A_original_science_FAIL_immutable']
            and j40['D34_D34R1_original_m26_boundary_FAIL_immutable']
            and not any(j40[k] for k in ('H3_full_window_solve_performed','Z11_certified','Z20_certified','Z21_certified','lensing_licensed'))):
        raise RuntimeError('D41 D40 scope/immutable parents changed')
    print('GE19_D41_D40_ALL_FROZEN_ANCESTOR_AND_SELF_SHA_SCOPE_LOCK_PASS',flush=True)
    return frozen,j35,j33,j36,j37,j38,j39,j40


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--results-dir',required=True)
    ap.add_argument('--json-out',required=True);ap.add_argument('--npz-out',required=True)
    args=ap.parse_args();rd=Path(args.results_dir).resolve()
    jp=Path(args.json_out).resolve();zp=Path(args.npz_out).resolve()
    if jp.exists() or zp.exists():raise RuntimeError('D41 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    frozen,j35,j33,j36,j37,j38,j39,j40=check_inputs(rd,pre,lock)
    j34=json.loads((rd/'ge19_h4f3d34r1_boundary_failure_cohort.json').read_text())
    modes=np.asarray(pre['modes'],int);betas=np.asarray(pre['betas'],float);subs=np.asarray(pre['substeps'],int)
    r7=d25.d20.source.old.r7
    with ExitStack() as es:
        z34=es.enter_context(np.load(rd/'ge19_h4f3d34r1_boundary_failure_cohort.npz',allow_pickle=False))
        z35=es.enter_context(np.load(rd/'ge19_h4f3d35_m26_precision_reprojection.npz',allow_pickle=False))
        z36=es.enter_context(np.load(rd/'ge19_h4f3d36_second_interval_continuation.npz',allow_pickle=False))
        seg=[]
        for start,end,ver,stem in ((2,16,'37','prefix_x2_x16_original_action_continuation'),
                (16,32,'38','x16_x32_original_action_continuation'),
                (32,64,'39','x32_x64_original_action_continuation'),
                (64,127,'40','x64_x127_original_action_continuation')):
            seg.append((start,end,es.enter_context(np.load(rd/f'ge19_h4f3d{ver}_{stem}.npz',allow_pickle=False))))
        z22=es.enter_context(np.load(frozen['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z33=es.enter_context(np.load(rd/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz',allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        if not np.array_equal(x,np.asarray(z22['x_primary'],float)):
            raise RuntimeError('D41 D17 original-action clock parent changed')
        state,frozen_shift,ab=splice_full_window(z34,z35,z36,seg,j34,j35,j36,modes,betas,subs,x,pre['original_shift_gate'])
        print('GE19_D41_FULL_128_CLOCK_NODE_240_CASES_EXACT_PROVENANCE_SPLICE_PASS',flush=True)
        sources={}
        for ib,b in enumerate(betas):
            ma=np.asarray(z33[f'beta{ib}_candidate_C_main_six_by_128_by_41'],complex)
            co=np.asarray(z33[f'beta{ib}_candidate_C_constraint_two_by_128_by_41'],complex)
            if ma.shape!=(6,128,41) or co.shape!=(2,128,41) or \
               not np.isfinite(ma).all() or not np.isfinite(co).all() or \
               not np.any(ma[:,:,0]) or not np.any(ma[3,:,1]) or not np.any(ma[3,:,14]) or \
               not np.array_equal(co[:,:,26],np.zeros((2,128),complex)):
                raise RuntimeError('D41 source/m0/StageE-Y/m26 provenance mismatch')
            sources[float(b)]={'rhs':ma,'rhs_constraint':co}
        shp=(128,40,3,2);lap=np.full(shp,np.nan);sh=np.full(shp,np.nan)
        an=np.full(shp,np.nan);al=np.full(shp,np.nan)
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            if active['ctx'] is None:raise RuntimeError('D41 original action context missing')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            for im,m in enumerate(modes):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0]);rf,cf=r7._source_interp(x,sources,int(m))
                for ix,t in enumerate(x):
                    M,F,ZY,ZR,WY,WR,Cmat,bp,_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,float(t))
                    rr=np.asarray(rf(float(t)),complex);cc=np.asarray(cf(float(t)),complex)
                    if rr.shape!=(6,3) or cc.shape!=(2,3):raise RuntimeError('D41 beta batch source shape')
                    op=(M,F,WY,WR,Cmat,rr,cc)
                    for ib,b in enumerate(betas):
                        for ins,n in enumerate(subs):
                            y=state[ix,im,ib,ins]
                            lapse,shift,aniso,algebraic=original_constraint_metrics(Cmat,WY,WR,rr,cc,y,ib)
                            oldmetric=d25.metric_from_y(r7,op,y,ib)
                            saved=float(frozen_shift[ix,im,ib,ins]);savedab=float(ab[ix,im,ib,ins])
                            if abs(oldmetric['relative_backward']-saved)>pre['shift_metric_replay_relative']*max(abs(saved),abs(oldmetric['relative_backward']),TINY) or \
                               abs(oldmetric['absolute_residual']-savedab)>pre['shift_metric_replay_relative']*max(abs(savedab),abs(oldmetric['absolute_residual']),TINY):
                                raise RuntimeError(f'D41 archived shift replay FAIL x{ix} m{m} beta{b} n{n}')
                            lap[ix,im,ib,ins]=lapse;sh[ix,im,ib,ins]=oldmetric['relative_backward']
                            an[ix,im,ib,ins]=aniso;al[ix,im,ib,ins]=algebraic
                print(f'GE19_D41_MODE m={m} lapse_max={np.max(lap[:,im]):.6e} shift_max={np.max(sh[:,im]):.6e} anisotropy_max={np.max(an[:,im]):.6e} algebraic_max={np.max(al[:,im]):.6e}',flush=True)
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
        if any(not np.isfinite(a).all() or a.shape!=shp for a in (lap,sh,an,al)):
            raise RuntimeError('D41 incomplete original-action constraint rows')
        def worst(metric,n=8):
            inds=np.argpartition(metric.ravel(),-n)[-n:]
            return [{'node_index':int(np.unravel_index(i,shp)[0]),
                     'mode':int(modes[np.unravel_index(i,shp)[1]]),
                     'beta':float(betas[np.unravel_index(i,shp)[2]]),
                     'substeps':int(subs[np.unravel_index(i,shp)[3]]),
                     'relative_backward':float(metric.ravel()[i])} for i in inds[np.argsort(metric.ravel()[inds])[::-1]]]
        gate=float(pre['original_boundary_backward_gate'])
        res={'classification':'GE19_D41_FULL_CLOCK_NUMERICAL_CONSTRAINT_AUDIT_COMPLETE_PARENTS_UNCERTIFIED',
             'preregistration':pre['classification'],'source_sha256':sha(__file__),
             'scope':'Independent source-aware ORIGINAL action lapse/shift/anisotropy and canonical-algebraic numerical audit of actual candidate-C evolved y at all 128 Cstar clock nodes, all 40 reduced modes, beta 1/.5/.1, n1/n8. No new evolution/projection/retuning; 30720 case-node samples, 30480 propagated endpoints plus 240 initial states. Lapse/anisotropy/algebraic tolerance 1e-6 report-only, no promotion to original full H3.',
             'claim_boundary':'Numerical exact-clock-node constraint diagnostic, NOT continuum bound, independent H1 on-shell or Noether proof, Ward identity, original bitwise Repair18 initial state or Z11/Z20/Z21/lensing certification. Original D22A/D34/D34R1 failures and D35 posthoc m26 momentum representation immutable.',
             'original_action_modified':False,'production_H3F_source_modified':False,
             'D22A_original_science_FAIL_immutable':True,
             'D34_D34R1_original_m26_boundary_FAIL_immutable':True,
             'D35_m26_posthoc_momentum_representation_not_original_bitwise':True,
             'all_30720_original_shift_replays_pass':True,
             'all_128_nodes_present':True,'all_240_cases_per_node':True,
             'source_beta_specific_Y_and_m0_retained':True,
             'no_new_evolution_or_projection':True,
             'H1_on_shell_verified':False,'Noether_ward_verified':False,
             'Z11_certified':False,'Z20_certified':False,'Z21_certified':False,
             'H3_full_window_certified':False,'full_H4_Ward_certified':False,'lensing_licensed':False,
             'original_gate_unchanged':True,'numeric_candidate_complete':True,
             'evaluated_case_node_count':30720,'evaluated_propagated_endpoint_count':30480,
             'original_shift_max_relative_backward':float(np.max(sh)),
             'lapse_max_relative_backward':float(np.max(lap)),
             'anisotropy_max_relative_backward':float(np.max(an)),
             'canonical_algebraic_max_relative_report_only':float(np.max(al)),
             'lapse_over_original_boundary_threshold_report_only_count':int(np.count_nonzero(lap>gate)),
             'anisotropy_over_original_boundary_threshold_report_only_count':int(np.count_nonzero(an>gate)),
             'algebraic_over_original_boundary_threshold_report_only_count':int(np.count_nonzero(al>gate)),
             'lapse_worst_case_report_only':worst(lap),
             'anisotropy_worst_case_report_only':worst(an),
             'algebraic_worst_case_report_only':worst(al),
             'lapse_and_shift_at_all_clock_nodes_satisfy_report_only_1e_minus_6':bool(np.max(lap)<=gate and np.max(sh)<=gate),
             'original_D40_json_sha256':sha(rd/'ge19_h4f3d40_x64_x127_original_action_continuation.json'),
             'original_D40_npz_sha256':sha(rd/'ge19_h4f3d40_x64_x127_original_action_continuation.npz')}
        jp.parent.mkdir(parents=True,exist_ok=True);zp.parent.mkdir(parents=True,exist_ok=True)
        jp.write_text(json.dumps(res,indent=2,sort_keys=True,allow_nan=False)+'\n')
        np.savez_compressed(zp,clock_node_x=x,modes=modes,betas=betas,substeps=subs,
              original_shift_relative_backward_replay=sh,
              original_lapse_relative_backward_audit=lap,
              original_anisotropy_relative_backward_audit=an,
              original_canonical_algebraic_relative_audit=al,
              original_shift_relative_backward_frozen=frozen_shift)
        print('GE19_D41_FULL_WINDOW_30720_ORIGINAL_SHIFT_REPLAY_PASS',flush=True)
        print('GE19_D41_LAPSE_MAX',res['lapse_max_relative_backward'],'OVER_1E6',res['lapse_over_original_boundary_threshold_report_only_count'],flush=True)
        print('GE19_D41_ANISO_MAX',res['anisotropy_max_relative_backward'],'OVER_1E6',res['anisotropy_over_original_boundary_threshold_report_only_count'],flush=True)
        print('GE19_D41_CLASSIFICATION '+res['classification'],flush=True)

if __name__=='__main__':main()
