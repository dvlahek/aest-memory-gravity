#!/usr/bin/env python3
"""GE19 D46 controlled *numerical* source-interpolation counterfactual.

Re-evolve the five frozen D42R2 diagnostic modes for three betas with four
Radau substeps per original 128-node interval. Compare the unchanged original
PCHIP baseline from D43 to a DIAGNOSTIC piecewise-linear interpolation of the
SAME frozen D33 41-mode source knots. Keep original action, homogeneous
background, original initial y and shift gate. Do not interpret either
interpolant as an independently recomputed continuous physical source.

The original D22A/D34/D34R1 failures and D35 m26 posthoc momentum remain
immutable. No H1-on-shell, H3, Ward, Z11/Z20/Z21 or lensing certificate.
"""
from __future__ import annotations
import argparse
from contextlib import ExitStack
import hashlib
import json
import math
from pathlib import Path
import subprocess
import numpy as np
from scipy.interpolate import interp1d

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d46_source_interpolation_counterfactual_prereg.json'
TINY=1e-300
STEM='ge19_h4f3d46_source_interpolation_counterfactual'


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):
            h.update(chunk)
    return h.hexdigest()


def require(ok,msg):
    if not ok:raise RuntimeError('GE19_D46_'+msg)


def rel_l2(a,b):
    a=np.asarray(a,complex);b=np.asarray(b,complex)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))


def source_linear(x,main,con,m):
    """Use source knots for *every* original mode; select m only for ODE RHS."""
    x=np.asarray(x,float)
    main=np.asarray(main,complex);con=np.asarray(con,complex)
    require(main.shape==(6,128,41,3) and con.shape==(2,128,41,3),'SOURCE_AXIS_CHANGED')
    require(0<=m<=40 and np.diff(x).min()>0,'SOURCE_GRID_CHANGED')
    r=interp1d(x,main[:,:,m,:],axis=1,kind='linear',bounds_error=True,assume_sorted=True)
    c=interp1d(x,con[:,:,m,:],axis=1,kind='linear',bounds_error=True,assume_sorted=True)
    return r,c


def synth_test():
    x=np.linspace(-1.,0.,128)
    main=np.zeros((6,128,41,3),complex);con=np.zeros((2,128,41,3),complex)
    main[0,:,1,:]=(1+2j)*np.exp(2*x)[:,None]
    main[3,:,14,:]=(1-1j)*np.sin(x)[:,None]
    con[1,:,1,:]=(3+4j)*x[:,None]
    r,c=source_linear(x,main,con,1)
    require(rel_l2(r(x),main[:,:,1,:])<1e-15 and rel_l2(c(x),con[:,:,1,:])<1e-15,'KNOT_REPLAY_FAIL')
    t=float((x[0]+x[1])/2)
    require(rel_l2(r(t),(main[:,0,1,:]+main[:,1,1,:])/2)<1e-15,'MIDPOINT_LINEAR_FAIL')
    require(np.linalg.norm(r(t)-main[:,0,1,:])>0,'INTERPOLATION_INERT')
    try:
        source_linear(x,main[:,:,:40,:],con,1)
    except RuntimeError as e:
        require('SOURCE_AXIS_CHANGED' in str(e),'NEGATIVE_SHAPE_BAD_ERROR')
    else:
        raise AssertionError('invalid full 41-mode source accepted')
    print('GE19_D46_COMPLEX_LINEAR_SOURCE_KNOT_MIDPOINT_AND_SHAPE_NEGATIVE_PASS',flush=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--preflight-only',action='store_true')
    ap.add_argument('--results-dir',type=Path)
    ap.add_argument('--json-out',type=Path)
    ap.add_argument('--npz-out',type=Path)
    args=ap.parse_args()
    if args.self_test:synth_test()
    if args.results_dir is None:
        require(args.self_test,'MISSING_RESULTS_DIR')
        return
    rd=args.results_dir.resolve()
    pre=json.loads(PRE.read_text())
    require(pre['classification']=='GE19_D46_PREEXEC_FROZEN_D33_PCHIP_VS_LINEAR_SOURCE_INTERPOLATION_COUNTERFACTUAL','WRONG_PREREG')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    require(branch==pre['branch'] and branch!='main','WRONG_BRANCH')
    require(pre['diagnostic_modes']==[1,6,14,26,40] and pre['betas']==[1.0,0.5,0.1] and pre['n_substeps']==4,'COHORT_NOT_PREREGISTERED')
    for name,expected in pre['frozen_original_parent_sha256'].items():
        path=rd/name
        require(path.is_file() and sha(path)==expected,'PARENT_SHA_FAIL_'+name)
    from ge19 import h4f3d41_full_window_two_constraint_audit as d41
    frozen,*_=d41.check_inputs(rd,json.loads(d41.PRE.read_text()),json.loads(d41.LOCK.read_text()))
    require(Path(frozen['D22A_NPZ']).is_file(),'MISSING_D22A')
    require(sha(ROOT/'ge19/h4f3d45_h1_offclock_source_audit.py')==pre['D45_original_driver_sha256'],'D45_CODE_CHANGED')
    require(sha(ROOT/'ge19/h4f3d43_full_40_mode_n2_n4_lapse.py')==pre['D43_original_driver_sha256'],'D43_CODE_CHANGED')
    j45=json.loads((rd/'ge19_h4f3d45_h1_offclock_source_audit.json').read_text())
    d44=rd/'ge19_d44_readonly_archive/ge19_d44_full_cohort_complex_clock_error_budget.json'
    require(d44.is_file() and sha(d44)==j45['original_D44_report_sha256'],'D44_REPORT_CHANGED')
    require(j45['classification']=='GE19_D45_OFFCLOCK_HOMOGENEOUS_BACKGROUND_AND_SOURCE_INTERPOLATION_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
            and not j45['H1_on_shell_verified'] and not j45['lensing_licensed'],'D45_SCOPE_CHANGED')
    print('GE19_D46_ALL_FROZEN_D33_D41_D42R2_D43_D44_D45_AND_ANCESTOR_SHA_PASS',flush=True)
    if args.preflight_only:
        print('GE19_D46_PREFLIGHT_ONLY_NO_EVOLUTION_PASS',flush=True)
        return
    require(args.json_out is not None and args.npz_out is not None,'MISSING_OUTPUT')
    jp=args.json_out.resolve();zp=args.npz_out.resolve()
    require(not jp.exists() and not zp.exists(),'REFUSE_OVERWRITE')
    d25=d41.d25;r7=d25.d20.source.old.r7
    modes=np.asarray(pre['diagnostic_modes'],int);betas=np.asarray(pre['betas'],float)
    gate=float(pre['original_shift_gate'])
    with ExitStack() as stack:
        z13=stack.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z33=stack.enter_context(np.load(rd/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz',allow_pickle=False))
        z43=stack.enter_context(np.load(rd/'ge19_h4f3d43_full_40_mode_n2_n4_lapse.npz',allow_pickle=False))
        z42=stack.enter_context(np.load(rd/'ge19_h4f3d42r2_lapse_substep_convergence.npz',allow_pickle=False))
        z45=stack.enter_context(np.load(rd/'ge19_h4f3d45_h1_offclock_source_audit.npz',allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        require(x.shape==(128,) and np.array_equal(x,z43['clock_node_x']) and np.array_equal(x,z45['clock_node_x']),'CLOCK_CHANGED')
        require(np.array_equal(z43['diagnostic_modes'],np.arange(1,41)) and np.array_equal(z43['betas'],betas) and np.array_equal(z43['new_substeps'],[2,4]),'D43_AXES_CHANGED')
        require(np.array_equal(z42['diagnostic_modes'],modes) and np.array_equal(z42['betas'],betas),'D42R2_PILOT_CHANGED')
        main=np.stack([np.asarray(z33[f'beta{i}_candidate_C_main_six_by_128_by_41'],complex) for i in range(3)],axis=-1)
        con=np.stack([np.asarray(z33[f'beta{i}_candidate_C_constraint_two_by_128_by_41'],complex) for i in range(3)],axis=-1)
        require(main.shape==(6,128,41,3) and con.shape==(2,128,41,3) and np.isfinite(main).all() and np.isfinite(con).all(),'D33_SOURCE_CHANGED')
        require(np.array_equal(con[:,:,26,:],np.zeros((2,128,3),complex)) and np.any(main[3,:,14,:]) and np.any(main[:,:,0,:]),'D33_M26_Y_M0_CHANGED')
        sources={float(b):{'rhs':main[:,:,:,i],'rhs_constraint':con[:,:,:,i]} for i,b in enumerate(betas)}
        for m in modes:
            rlin,clin=source_linear(x,main,con,int(m))
            for it in (0,1,64,115,127):
                orig=np.concatenate((main[:,it,m,:],con[:,it,m,:]),axis=0)
                lin=np.concatenate((rlin(float(x[it])),clin(float(x[it]))),axis=0)
                require(rel_l2(orig,lin)<3e-14,'ALT_KNOT_SOURCE_CHANGED')
            for it in (0,114,126):
                mid=float((x[it]+x[it+1])/2)
                got=np.concatenate((rlin(mid),clin(mid)),axis=0)
                ref=np.asarray(z45['source_linear_mid'][:,it,m,:],complex)
                require(rel_l2(got,ref)<3e-13,'D45_LINEAR_MIDPOINT_REPLAY_FAIL')
            rp,cp=r7._source_interp(x,sources,int(m))
            for it in (0,114,126):
                mid=float((x[it]+x[it+1])/2)
                got=np.concatenate((rp(mid),cp(mid)),axis=0)
                ref=np.asarray(z45['source_PCHIP_mid'][:,it,m,:],complex)
                require(rel_l2(got,ref)<3e-13,'D45_PCHIP_MIDPOINT_REPLAY_FAIL')
        i5=modes-1
        require(np.array_equal(np.take(z43['new_states_by_node_mode_beta_substep'][:,:,:,1,:],i5,axis=1),z42['new_states_by_node_mode_beta_substep'][:,:,:,1,:]),'D43_D42R2_N4_STATES_NOT_BITWISE')
        print('GE19_D46_D45_FULL_SOURCE_MIDPOINT_AND_D43_D42R2_N4_BITWISE_REPLAY_PASS',flush=True)
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            require(active['ctx'] is not None,'ORIGINAL_ACTION_CONTEXT_MISSING')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        nmode=len(modes);n_beta=len(betas);n_clock=len(x)
        alt_state=np.full((n_clock,nmode,n_beta,8),np.nan+1j*np.nan,complex)
        alt_shift=np.full((n_clock,nmode,n_beta),np.nan,float)
        alt_lapse=np.full((n_clock,nmode,n_beta),np.nan,float)
        radau=np.full((n_clock,nmode,n_beta),np.nan,float)
        delta_state=np.full((n_clock,nmode,n_beta),np.nan,float)
        valid=np.zeros((n_clock,nmode,n_beta),bool)
        failures=[];baseline_replay=0.; max_source_at_nodes=0.
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            for im,m in enumerate(modes):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0]);rp,cp=r7._source_interp(x,sources,int(m))
                rlin,clin=source_linear(x,main,con,int(m))
                # Both RHS versions have EXACTLY the same source knots; only off-clock representation changes.
                # Re-evaluate frozen-original PCHIP metrics at the preselected two diagnostic nodes.
                orig_probe={}
                for ix in (0,1,115,127):
                    op_orig=d25.shift_at(r7,mod6,mod7,bg,tag,k,float(x[ix]),None,rp,cp)
                    op_alt=d25.shift_at(r7,mod6,mod7,bg,tag,k,float(x[ix]),None,rlin,clin)
                    max_source_at_nodes=max(max_source_at_nodes,rel_l2(op_orig[5],op_alt[5]),rel_l2(op_orig[6],op_alt[6]))
                    for ib in range(3):
                        yo=z43['new_states_by_node_mode_beta_substep'][ix,m-1,ib,1]
                        ml=d41.original_constraint_metrics(op_orig[4],op_orig[2],op_orig[3],op_orig[5],op_orig[6],yo,ib)
                        sh=d25.metric_from_y(r7,op_orig,yo,ib)['relative_backward']
                        frozen_l=float(z43['lapse_relative_backward_by_node_mode_beta_substep'][ix,m-1,ib,2]);frozen_s=float(z43['shift_relative_backward_by_node_mode_beta_substep'][ix,m-1,ib,2])
                        deviation=max(abs(ml[0]-frozen_l),abs(sh-frozen_s))
                        require(deviation<=5e-11*max(1.,abs(frozen_l),abs(frozen_s)),'FROZEN_ORIGINAL_N4_METRIC_REPLAY_FAIL')
                        baseline_replay=max(baseline_replay,deviation)
                    orig_probe[ix]=op_orig
                for ib,beta in enumerate(betas):
                    def rr(t,fun=rlin,j=ib):return np.asarray(fun(t),complex)[:,j:j+1]
                    def cc(t,fun=clin,j=ib):return np.asarray(fun(t),complex)[:,j:j+1]
                    y=np.asarray(z43['new_states_by_node_mode_beta_substep'][0,m-1,ib,1],complex).copy()
                    alt_state[0,im,ib]=y;valid[0,im,ib]=True;radau[0,im,ib]=0.
                    op=d25.shift_at(r7,mod6,mod7,bg,tag,k,float(x[0]),None,rlin,clin)
                    met=d41.original_constraint_metrics(op[4],op[2],op[3],op[5],op[6],y,ib)
                    alt_lapse[0,im,ib]=met[0];alt_shift[0,im,ib]=d25.metric_from_y(r7,op,y,ib)['relative_backward']
                    delta_state[0,im,ib]=0.
                    if alt_shift[0,im,ib]>gate:
                        failures.append({'mode':int(m),'beta':float(beta),'node':0,'reason':'ALT_INITIAL_SHIFT_GATE'})
                        continue
                    for ix in range(1,n_clock):
                        try:
                            y,rerr=d25.integrate(r7,mod6,mod7,bg,tag,k,y,float(x[ix-1]),float(x[ix]),rr,cc,4)
                            op=d25.shift_at(r7,mod6,mod7,bg,tag,k,float(x[ix]),None,rlin,clin)
                            met=d41.original_constraint_metrics(op[4],op[2],op[3],op[5],op[6],y,ib)
                            sm=d25.metric_from_y(r7,op,y,ib)['relative_backward']
                            orig_y=np.asarray(z43['new_states_by_node_mode_beta_substep'][ix,m-1,ib,1],complex)
                            ds=rel_l2(y,orig_y)
                            require(np.isfinite((rerr,*met,sm,ds)).all() and np.isfinite(y).all(),'NONFINITE_ALTERNATIVE_OUTPUT')
                        except (RuntimeError,ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:
                            failures.append({'mode':int(m),'beta':float(beta),'node':ix,'reason':'ALT_INTEGRATION_OR_METRIC_FAIL','detail':repr(exc)})
                            break
                        valid[ix,im,ib]=True;alt_state[ix,im,ib]=y
                        alt_shift[ix,im,ib]=float(sm);alt_lapse[ix,im,ib]=float(met[0]);radau[ix,im,ib]=float(rerr);delta_state[ix,im,ib]=ds
                        if sm>gate:
                            failures.append({'mode':int(m),'beta':float(beta),'node':ix,'reason':'ALTERNATIVE_SHIFT_EXCEEDS_FROZEN_GATE','value':float(sm)})
                            break
                    print(f'GE19_D46_CASE m={m} beta={beta} n=4 linear_valid={int(np.count_nonzero(valid[:,im,ib]))}/128 '
                          f'x1_alt_lapse={alt_lapse[1,im,ib]:.6e} x115_alt_lapse={alt_lapse[115,im,ib]:.6e}',flush=True)
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
        require(max_source_at_nodes<3e-13,'SOURCE_KNOT_COUNTERFACTUAL_NOT_IDENTICAL')
        evaluated=int(np.count_nonzero(valid[1:]));expected=(128-1)*nmode*n_beta
        completed=bool(evaluated==expected and not failures)
        original_lap=np.take(np.asarray(z43['lapse_relative_backward_by_node_mode_beta_substep'][:,:,:,2],float),i5,axis=1)
        original_shift=np.take(np.asarray(z43['shift_relative_backward_by_node_mode_beta_substep'][:,:,:,2],float),i5,axis=1)
        diff_lapse=alt_lapse-original_lap;diff_shift=alt_shift-original_shift
        def extract_node(ix):
            alt=np.asarray(alt_lapse[ix],float);ref=np.asarray(original_lap[ix],float)
            d=np.abs(alt-ref)
            mask=valid[ix]
            return {'index':int(ix),'evaluated':int(mask.sum()),'expected':int(mask.size),
                    'alt_lapse_max_report_only':float(np.max(alt[mask])) if np.any(mask) else None,
                    'original_lapse_max_report_only':float(np.max(ref[mask])) if np.any(mask) else None,
                    'max_abs_lapse_metric_change_report_only':float(np.max(d[mask])) if np.any(mask) else None,
                    'max_relative_state_change_report_only':float(np.max(delta_state[ix][mask])) if np.any(mask) else None}
        report={'classification':('GE19_D46_FIVE_MODE_SOURCE_INTERPOLATION_COUNTERFACTUAL_COMPLETE_PARENTS_UNCERTIFIED' if completed else
                                  'GE19_D46_ALTERNATIVE_SOURCE_INTERPOLATION_CONTROL_INCOMPLETE_PARENTS_UNCERTIFIED'),
                'preregistration':pre['classification'],'source_sha256':sha(__file__),
                'scope':'Five original D42R2 modes, original three betas, four Radau substeps, full original 128 clock nodes. Original D33 full 41-mode source knots and action preserved, substitute LINEAR for original PCHIP only between knots. Alt numerical sensitivity, not continuous physical source truth.',
                'original_action_modified':False,'original_D33_source_knots_modified':False,'original_PCHIP_production_modified':False,
                'original_D41_D42R2_D43_D44_D45_remain_frozen':True,'original_shift_gate_unchanged':True,
                'H1_on_shell_verified':False,'H3_full_window_certified':False,'Noether_ward_verified':False,
                'Z11_certified':False,'Z20_certified':False,'Z21_certified':False,'lensing_licensed':False,
                'D22A_original_science_FAIL_immutable':True,'D34_D34R1_original_m26_boundary_FAIL_immutable':True,
                'D35_m26_posthoc_momentum_not_original_bitwise':True,
                'frozen_original_parent_sha256':pre['frozen_original_parent_sha256'],
                'all_original_PCHIP_source_knots_replayed':True,
                'D45_linear_and_PCHIP_three_midpoints_per_mode_replayed':True,
                'max_original_source_at_knot_relative_difference':max_source_at_nodes,
                'max_frozen_original_n4_constraint_metric_replay_abs':baseline_replay,
                'alternative_propagated_endpoints_evaluated':evaluated,
                'alternative_propagated_endpoints_expected':expected,
                'alternative_incomplete_case_ledger':failures,
                'alternative_shift_over_original_gate_count':int(np.count_nonzero(valid[1:]&(alt_shift[1:]>gate))),
                'max_alternative_shift':float(np.max(alt_shift[valid])) if np.any(valid) else None,
                'max_alternative_lapse_report_only':float(np.max(alt_lapse[valid])) if np.any(valid) else None,
                'max_abs_lapse_metric_change_report_only':float(np.max(np.abs(diff_lapse[valid]))) if np.any(valid) else None,
                'max_relative_state_change_report_only':float(np.max(delta_state[valid])) if np.any(valid) else None,
                'diagnostic_nodes':[extract_node(i) for i in (1,115,127)],
                'claim_boundary':'Interpolation swap is controlled numerical sensitivity ONLY, not independent true offclock original source, perturbative H1 EOM proof, continuum bound, bitwise Repair18 momentum, full H3/Ward or Z11/Z20/Z21/lensing authorization.',
                'next_step':'Independently evaluate full original GE06/GE07/Lambda perturbative H1 EOM and continuous original 41-mode D33 source between clock nodes, compare to frozen PCHIP and exact original-action lapse without retuning.'}
        require(np.all(np.isfinite(alt_lapse[valid])) and np.all(np.isfinite(alt_shift[valid])) and np.all(np.isfinite(delta_state[valid])),'BAD_VALID_MASK_VALUES')
        jp.parent.mkdir(parents=True,exist_ok=True);zp.parent.mkdir(parents=True,exist_ok=True)
        np.savez_compressed(zp,clock_node_x=x,diagnostic_modes=modes,betas=betas,
            substeps=np.array([4]),alternative_source_method=np.array('linear',dtype='U8'),
            alternative_y_by_node_mode_beta=alt_state,alternative_evaluated=valid,
            original_frozen_n4_lapse=original_lap,original_frozen_n4_shift=original_shift,
            alternative_lapse=alt_lapse,alternative_shift=alt_shift,
            difference_lapse_metric=diff_lapse,difference_shift_metric=diff_shift,
            relative_state_difference=delta_state,alternative_radau_backward=radau)
        jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
        print('GE19_D46_ALT_SOURCE_INTERPOLATION_COMPLETED_ENDPOINTS',evaluated,expected,flush=True)
        print('GE19_D46_NUMERICAL_SENSITIVITY_ONLY_H1_H3_Z21_LENSING_OPEN',flush=True)
        print('GE19_D46_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':main()
