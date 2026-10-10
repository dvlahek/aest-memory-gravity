#!/usr/bin/env python3
"""GE19 D42: preregistered diagnostic of the D41 lapse failures with independent substeps.

Five diagnostic modes only. No changes to the original action, sources, initial
states, boundary conditions or 1e-6 original shift gate. The n=1/8 full clock
cohort is frozen D41, n=2/4/16 trajectories are independently evolved from x0.
No claim of H1 on-shell, Ward, original bitwise Repair18 or certified H3/H4.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d41_full_window_two_constraint_audit as d41
ROOT=Path(__file__).resolve().parents[1]
STEM='ge19_h4f3d42_lapse_substep_convergence'
PRE=ROOT/'ge19/h4f3d42_lapse_substep_convergence_prereg.json'
LOCK=ROOT/'ge19/h4f3d42_lapse_substep_convergence_lock.json'
TINY=1e-300


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def failure_fingerprint(lap,modes,betas,substeps,gate):
    """The exact immutable D41 n1/n8 two-sector 120-failure fingerprint."""
    lap=np.asarray(lap,float)
    modes=np.asarray(modes,int);betas=np.asarray(betas,float);subs=np.asarray(substeps,int)
    if lap.shape!=(128,40,3,2) or not np.array_equal(modes,np.arange(1,41)) or \
       not np.array_equal(betas,[1.,.5,.1]) or not np.array_equal(subs,[1,8]) or \
       not np.isfinite(lap).all() or gate!=1e-6:
        raise RuntimeError('D42 immutable D41 fingerprint cohort/metric invalid')
    off=np.array([1,4,9,14,19,21,22,24,26,27,29,31,32,33,34,36,37,38,39],int)
    support=np.array([m for m in modes if m not in set(off)],int)
    expect=np.zeros(lap.shape,bool)
    expect[1,off-1,:,0]=True
    expect[115,support-1,:,0]=True
    obs=lap>gate
    if not np.array_equal(obs,expect) or int(obs.sum())!=120:
        raise RuntimeError('D42 frozen D41 lapse failure fingerprint changed')
    return {'all_frozen_over_threshold_count':120,'n1_x1_offsupport_count':57,
            'n1_x115_smooth_support_count':63,'n8_over_threshold_count':0,
            'off_support_modes':off.tolist(),'smooth_support_modes':support.tolist()}


def summarize_new(valid,shift,lap,gate):
    """Missing/failed knots never count as successful science endpoints."""
    valid=np.asarray(valid,bool);shift=np.asarray(shift,float);lap=np.asarray(lap,float)
    if valid.ndim!=4 or valid.shape[0]!=128 or valid.shape[1:]!=(5,3,3) or \
       shift.shape!=valid.shape or lap.shape!=valid.shape or not np.all(valid[0]):
        raise RuntimeError('D42 incomplete new trajectory shape/initial states')
    if np.any(valid[1:]&~valid[:-1]) or not np.isfinite(shift[valid]).all() or \
       not np.isfinite(lap[valid]).all() or not np.isnan(shift[~valid]).all() or \
       not np.isnan(lap[~valid]).all():
        raise RuntimeError('D42 invalid new trajectory mask/metrics')
    evaluated=int(np.count_nonzero(valid[1:]));expected=(128-1)*5*3*3
    return {'new_endpoint_expected':expected,'new_endpoint_evaluated':evaluated,
            'new_endpoint_unevaluated':expected-evaluated,
            'observed_new_shift_gate_fail_count':int(np.count_nonzero(valid[1:]&(shift[1:]>gate))),
            'observed_new_lapse_over_reference_count':int(np.count_nonzero(valid[1:]&(lap[1:]>gate))),
            'max_new_lapse_report_only':float(np.max(lap[1:][valid[1:]])) if evaluated else None,
            'max_new_shift':float(np.max(shift[1:][valid[1:]])) if evaluated else None}


def check_inputs(rd,pre,lock):
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!=pre['branch'] or branch=='main':raise RuntimeError('D42 wrong branch/main forbidden')
    if not (pre['classification']=='GE19_D42_PREEXEC_LAPSE_TWO_SECTOR_INDEPENDENT_SUBSTEP_CONVERGENCE'
      and pre['clock_nodes']==128 and pre['modes']==[1,6,14,26,40]
      and pre['betas']==[1.,.5,.1] and pre['frozen_substeps']==[1,8]
      and pre['new_substeps']==[2,4,16] and pre['diagnostic_nodes']==[1,115]
      and pre['original_shift_gate']==pre['lapse_reference_report_only']==1e-6
      and pre['new_endpoint_expected']==5715
      and all(pre[v] for v in ('all_full_41_mode_sources_retained','no_new_projection','independent_x0_start_for_each_new_n',
                                'no_observation_tuning','lapse_fail_is_report_only','stop_on_original_shift_gate_failure',
                                'no_action_or_threshold_changes','no_parent_certification'))):
        raise RuntimeError('D42 preregistration science/scope mismatch')
    for key,want in lock['sha256_local_files'].items():
        if not (ROOT/key).is_file() or sha(ROOT/key)!=want:raise RuntimeError('D42 self SHA mismatch '+key)
    for key,want in pre['frozen_D41_code_sha256'].items():
        if not (ROOT/key).is_file() or sha(ROOT/key)!=want:raise RuntimeError('D42 D41 source changed '+key)
    for key,want in pre['frozen_D41_results_sha256'].items():
        if not (rd/key).is_file() or sha(rd/key)!=want:raise RuntimeError('D42 D41 result changed '+key)
    frozen,*parents=d41.check_inputs(rd,json.loads(d41.PRE.read_text()),json.loads(d41.LOCK.read_text()))
    j41=json.loads((rd/STEM.replace('d42_lapse_substep_convergence','d41_full_window_two_constraint_audit')+'.json').read_text())
    if j41['classification']!='GE19_D41_FULL_CLOCK_NUMERICAL_CONSTRAINT_AUDIT_COMPLETE_PARENTS_UNCERTIFIED' or \
       not j41['all_30720_original_shift_replays_pass'] or \
       j41['lapse_over_original_boundary_threshold_report_only_count']!=120 or \
       not j41['D35_m26_posthoc_momentum_representation_not_original_bitwise'] or \
       any(j41[k] for k in ('H1_on_shell_verified','Noether_ward_verified','H3_full_window_certified',
                           'Z11_certified','Z20_certified','Z21_certified','lensing_licensed')):
        raise RuntimeError('D42 original D41 diagnostic/scope mismatch')
    print('GE19_D42_FROZEN_D41_D40_TO_D22A_AND_SELF_SHA_SCOPE_LOCK_PASS',flush=True)
    return frozen,j41


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--results-dir',required=True)
    ap.add_argument('--json-out',required=True);ap.add_argument('--npz-out',required=True)
    a=ap.parse_args();rd=Path(a.results_dir).resolve();jp=Path(a.json_out).resolve();zp=Path(a.npz_out).resolve()
    if jp.exists() or zp.exists():raise RuntimeError('D42 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text());frozen,j41=check_inputs(rd,pre,lock)
    diagnostic_modes=np.asarray(pre['modes'],int);betas=np.asarray(pre['betas'],float)
    new_subs=np.asarray(pre['new_substeps'],int);sample_subs=np.asarray([1,2,4,8,16],int)
    selected_indices=diagnostic_modes-1;gate=float(pre['original_shift_gate'])
    shp=(128,5,3,5);nshp=(128,5,3,3)
    lap=np.full(shp,np.nan,float);shift=np.full(shp,np.nan,float)
    newvalid=np.zeros(nshp,bool);newstates=np.full(nshp+(8,),np.nan+0j,complex)
    newradau=np.full(nshp,np.nan,float);failures=[]
    def entry_for_sub(n):return int(np.where(sample_subs==n)[0][0])
    with ExitStack() as es:
        z41=es.enter_context(np.load(rd/'ge19_h4f3d41_full_window_two_constraint_audit.npz',allow_pickle=False))
        fullmodes=np.asarray(z41['modes'],int);fullbetas=np.asarray(z41['betas'],float)
        fullsubs=np.asarray(z41['substeps'],int);clock=np.asarray(z41['clock_node_x'],float)
        frozenlap=np.asarray(z41['original_lapse_relative_backward_audit'],float)
        frozenshift=np.asarray(z41['original_shift_relative_backward_replay'],float)
        fingerprint=failure_fingerprint(frozenlap,fullmodes,fullbetas,fullsubs,gate)
        if not (np.array_equal(fullmodes,np.arange(1,41)) and np.array_equal(fullbetas,betas)
                and np.array_equal(fullsubs,[1,8]) and np.array_equal(frozenshift,z41['original_shift_relative_backward_frozen'])
                and np.max(frozenshift)==j41['original_shift_max_relative_backward']):
            raise RuntimeError('D42 D41 archived mode/beta/shift replay mismatch')
        print('GE19_D42_FROZEN_D41_120_LAPSE_FAILURE_TWO_SECTOR_FINGERPRINT_PASS',flush=True)
        for n in [1,8]:
            lap[:,:,:,entry_for_sub(n)]=frozenlap[:,selected_indices,:,0 if n==1 else 1]
            shift[:,:,:,entry_for_sub(n)]=frozenshift[:,selected_indices,:,0 if n==1 else 1]
        j34=json.loads((rd/'ge19_h4f3d34r1_boundary_failure_cohort.json').read_text())
        j35=json.loads((rd/'ge19_h4f3d35_m26_precision_reprojection.json').read_text())
        j36=json.loads((rd/'ge19_h4f3d36_second_interval_continuation.json').read_text())
        z34=es.enter_context(np.load(rd/'ge19_h4f3d34r1_boundary_failure_cohort.npz',allow_pickle=False))
        z35=es.enter_context(np.load(rd/'ge19_h4f3d35_m26_precision_reprojection.npz',allow_pickle=False))
        z36=es.enter_context(np.load(rd/'ge19_h4f3d36_second_interval_continuation.npz',allow_pickle=False))
        seg=[]
        for start,end,ver,stem in ((2,16,'37','prefix_x2_x16_original_action_continuation'),
                (16,32,'38','x16_x32_original_action_continuation'),
                (32,64,'39','x32_x64_original_action_continuation'),
                (64,127,'40','x64_x127_original_action_continuation')):
            seg.append((start,end,es.enter_context(np.load(rd/f'ge19_h4f3d{ver}_{stem}.npz',allow_pickle=False))))
        state,oldshift,_=d41.splice_full_window(z34,z35,z36,seg,j34,j35,j36,fullmodes,fullbetas,fullsubs,clock,gate)
        if not np.array_equal(oldshift,frozenshift):raise RuntimeError('D42 D41 archived shift cohort does not match states')
        z22=es.enter_context(np.load(frozen['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z33=es.enter_context(np.load(rd/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz',allow_pickle=False))
        d25=d41.d25;r7=d25.d20.source.old.r7
        bgs,_,mod6,mod7,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        if not np.array_equal(x,clock) or not np.array_equal(x,np.asarray(z22['x_primary'],float)):
            raise RuntimeError('D42 exact frozen 128 clock mismatch')
        sources={}
        for ib,b in enumerate(betas):
            ma=np.asarray(z33[f'beta{ib}_candidate_C_main_six_by_128_by_41'],complex)
            co=np.asarray(z33[f'beta{ib}_candidate_C_constraint_two_by_128_by_41'],complex)
            if ma.shape!=(6,128,41) or co.shape!=(2,128,41) or not np.isfinite(ma).all() or \
               not np.isfinite(co).all() or not np.any(ma[:,:,0]) or \
               not np.any(ma[3,:,1]) or not np.any(ma[3,:,14]) or \
               not np.array_equal(co[:,:,26],np.zeros((2,128),complex)):
                raise RuntimeError('D42 original action full-mode m0/Y source changed')
            sources[float(b)]={'rhs':ma,'rhs_constraint':co}
        print('GE19_D42_5_DIAGNOSTIC_MODES_FULL_41_MODE_ORIGINAL_ACTION_SOURCES_RETAINED_PASS',flush=True)
        # Diagnostic terms are reported only at x1/x115, plus x0 for provenance.
        diagnostic_nodes=np.asarray(pre['diagnostic_nodes'],int)
        raw=np.full((2,5,3,5,6),np.nan,float) # abs, scale, lhs_abs, target_abs, defect_Re, defect_Im
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            if active['ctx'] is None:raise RuntimeError('D42 original action background unavailable')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            for im,m in enumerate(diagnostic_modes):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                rf,cf=r7._source_interp(x,sources,int(m))
                # Source/operator are independent of beta/substep and never reweighted.
                ops=[d25.shift_at(r7,mod6,mod7,bg,tag,k,float(t),None,rf,cf) for t in x]
                for ib,b in enumerate(betas):
                    def rr(t,fun=rf,index=ib):return np.asarray(fun(t),complex)[:,index:index+1]
                    def cc(t,fun=cf,index=ib):return np.asarray(fun(t),complex)[:,index:index+1]
                    for old_n in [1,8]:
                        which=entry_for_sub(old_n)
                        oi=0 if old_n==1 else 1
                        for ix in diagnostic_nodes:
                            op=ops[int(ix)];_,_,WY,WR,Cmat,main,con=op
                            y=state[int(ix),int(m)-1,ib,oi]
                            source=np.concatenate((main[:,ib],con[:,ib]));w=WY@y+WR@source
                            metric=d41.r18.backward_error(Cmat[4],w,main[0,ib]);lhs=complex(Cmat[4]@w)
                            saved=float(lap[int(ix),im,ib,which])
                            if abs(float(metric['metric'])-saved)>1e-10*max(abs(saved),abs(float(metric['metric'])),TINY):
                                raise RuntimeError('D42 D41 archived lapse source-aware term replay mismatch')
                            defect=lhs-complex(main[0,ib]);raw[int(np.where(diagnostic_nodes==ix)[0][0]),im,ib,which]=[
                                metric['absolute_residual'],metric['scale'],metric['lhs_abs'],metric['target_abs'],
                                defect.real,defect.imag]
                    for i_new,n in enumerate(new_subs):
                        which=entry_for_sub(int(n));y=state[0,int(m)-1,ib,0].copy()
                        newstates[0,im,ib,i_new]=y;newvalid[0,im,ib,i_new]=True
                        init=d41.original_constraint_metrics(ops[0][4],ops[0][2],ops[0][3],ops[0][5],ops[0][6],y,ib)
                        lap[0,im,ib,which]=init[0]
                        shift[0,im,ib,which]=float(d25.metric_from_y(r7,ops[0],y,ib)['relative_backward'])
                        newradau[0,im,ib,i_new]=0.
                        if shift[0,im,ib,which]>gate:
                            raise RuntimeError('D42 frozen D35/34R1 original x0 shift gate not met')
                        for ix in range(1,128):
                            if (not newvalid[ix-1,im,ib,i_new]) or shift[ix-1,im,ib,which]>gate:
                                failures.append({'node_index':ix,'mode':int(m),'beta':float(b),'substeps':int(n),
                                                 'reason':'BLOCKED_BY_EARLIER_SHIFT_OR_NUMERICAL_FAILURE'})
                                continue
                            try:
                                y,rad=d25.integrate(r7,mod6,mod7,bg,tag,k,y,float(x[ix-1]),float(x[ix]),rr,cc,int(n))
                                op=ops[ix];metric=d25.metric_from_y(r7,op,y,ib)
                                lapse=d41.original_constraint_metrics(op[4],op[2],op[3],op[5],op[6],y,ib)[0]
                                if not (np.isfinite(y).all() and np.isfinite((rad,metric['relative_backward'],lapse)).all()):
                                    raise FloatingPointError('D42 nonfinite state/lapse/shift/Radau')
                            except (RuntimeError,ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:
                                failures.append({'node_index':ix,'mode':int(m),'beta':float(b),'substeps':int(n),
                                                 'reason':'NUMERICAL_OR_OPERATOR_EXCEPTION','detail':repr(exc)})
                                continue
                            newstates[ix,im,ib,i_new]=y;newvalid[ix,im,ib,i_new]=True
                            lap[ix,im,ib,which]=float(lapse);shift[ix,im,ib,which]=float(metric['relative_backward'])
                            newradau[ix,im,ib,i_new]=float(rad)
                            if ix in diagnostic_nodes:
                                _,_,WY,WR,Cmat,main,con=op
                                source=np.concatenate((main[:,ib],con[:,ib]));w=WY@y+WR@source
                                lr=d41.r18.backward_error(Cmat[4],w,main[0,ib]);lhs=complex(Cmat[4]@w)
                                defect=lhs-complex(main[0,ib]);raw[int(np.where(diagnostic_nodes==ix)[0][0]),im,ib,which]=[
                                    lr['absolute_residual'],lr['scale'],lr['lhs_abs'],lr['target_abs'],defect.real,defect.imag]
                            if metric['relative_backward']>gate:
                                failures.append({'node_index':ix,'mode':int(m),'beta':float(b),'substeps':int(n),
                                                 'reason':'ORIGINAL_SHIFT_GATE_FAILED','metric':float(metric['relative_backward'])})
                        print(f'GE19_D42_CASE m={m} beta={b} n={n} valid={int(np.count_nonzero(newvalid[:,im,ib,i_new]))}/128 '
                              f'lapse_x1={lap[1,im,ib,which]:.6e} lapse_x115={lap[115,im,ib,which]:.6e} '
                              f'shift_max={np.nanmax(shift[:,im,ib,which]):.6e}',flush=True)
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
        summary=summarize_new(newvalid,shift[:,:,:,1:][:,:,:,[0,1,3]],lap[:,:,:,1:][:,:,:,[0,1,3]],gate)
        if len(failures)!=summary['new_endpoint_unevaluated']+summary['observed_new_shift_gate_fail_count']:
            raise RuntimeError('D42 blocked/failure ledger mismatch')
        # The two diagnostic nodes must retain all five frozen/new substeps in the successful cohort.
        targets=[]
        for ix in diagnostic_nodes:
            for im,m in enumerate(diagnostic_modes):
                for ib,b in enumerate(betas):
                    for j,n in enumerate(sample_subs):
                        val=lap[int(ix),im,ib,j];sh=shift[int(ix),im,ib,j]
                        targets.append({'node_index':int(ix),'mode':int(m),'beta':float(b),'substeps':int(n),
                                        'evaluated':bool(np.isfinite(val) and np.isfinite(sh)),
                                        'lapse_relative_backward_report_only':float(val) if np.isfinite(val) else None,
                                        'shift_relative_backward':float(sh) if np.isfinite(sh) else None})
        res=dict(summary,classification='GE19_D42_TWO_SECTOR_LAPSE_SUBSTEP_CONVERGENCE_DIAGNOSTIC_PARENTS_UNCERTIFIED',
                 preregistration=pre['classification'],source_sha256=sha(__file__),
                 scope='Five preregistered diagnostic modes 1,6,14,26,40, three betas and true x0->x127 independent n2/n4/n16 evolutions. Immutable n1/n8 full-window D41 metrics replayed. Exact original Cstar source/operator, no projection or tuning. Lapse 1e-6 is report-only; original shift 1e-6 remains binding.',
                 claim_boundary='Diagnostic subsampling is not a new full 40-mode cohort, continuum error bound, on-shell H1/Noether or Ward proof, bitwise Repair18 initial momentum, Z11/Z20/Z21 certification or lensing authorization.',
                 frozen_D41_lapse_failure_fingerprint=fingerprint,
                 frozen_D41_original_lapse_above_1e_minus_6=120,
                 original_D41_json_sha256=sha(rd/'ge19_h4f3d41_full_window_two_constraint_audit.json'),
                 original_D41_npz_sha256=sha(rd/'ge19_h4f3d41_full_window_two_constraint_audit.npz'),
                 D22A_original_science_FAIL_immutable=True,D34_D34R1_original_m26_boundary_FAIL_immutable=True,
                 D35_m26_posthoc_momentum_representation_not_original_bitwise=True,
                 original_action_modified=False,production_H3F_source_modified=False,
                 original_shift_gate_unchanged=True,nonanalytic_StageE_Y_retained=True,
                 m0_source_retained_separately=True,all_41_source_modes_retained=True,
                 H1_on_shell_verified=False,Noether_ward_verified=False,H3_full_window_certified=False,
                 Z11_certified=False,Z20_certified=False,Z21_certified=False,lensing_licensed=False,
                 diagnostic_modes=diagnostic_modes.tolist(),betas=betas.tolist(),sample_substeps=sample_subs.tolist(),
                 diagnostic_nodes=diagnostic_nodes.tolist(),target_rows=targets,observed_failure_ledger=failures)
        jp.parent.mkdir(parents=True,exist_ok=True);zp.parent.mkdir(parents=True,exist_ok=True)
        jp.write_text(json.dumps(res,indent=2,sort_keys=True,allow_nan=False)+'\n')
        np.savez_compressed(zp,clock_node_x=x,diagnostic_modes=diagnostic_modes,betas=betas,
                sample_substeps=sample_subs,new_substeps=new_subs,diagnostic_node_indices=diagnostic_nodes,
                lapse_relative_backward_by_node_mode_beta_substep=lap,
                shift_relative_backward_by_node_mode_beta_substep=shift,
                new_states_by_node_mode_beta_substep=newstates,
                new_state_numerically_evaluated=newvalid,new_Radau_backward_report_only=newradau,
                diagnostic_lapse_row_abs_scale_lhs_target_defect=raw)
        print('GE19_D42_NEW_ENDPOINTS evaluated',summary['new_endpoint_evaluated'],'unevaluated',
              summary['new_endpoint_unevaluated'],'shift_fail',summary['observed_new_shift_gate_fail_count'],flush=True)
        print('GE19_D42_CLASSIFICATION '+res['classification'],flush=True)

if __name__=='__main__':main()
