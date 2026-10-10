#!/usr/bin/env python3
"""GE19 D32: preregistered independent-sector source-representation diagnostic.

Compare immutable D31R1 candidate A (direct GE06 + original subtractive
non-GE06 remainder) to candidate B (direct GE06 + separately assembled
GE07 + Lambda + Stage E Y) on exactly the frozen first interval.
No production source changes, discarded historical failures or certification.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d31r1_paired_direct_ge06_first_interval as d31

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d32_independent_sector_first_interval_prereg.json'
LOCK=ROOT/'ge19/h4f3d32_independent_sector_first_interval_lock.json'
TINY=1e-300


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):
            h.update(part)
    return h.hexdigest()


def rel(a,b):
    aa=np.asarray(a,complex);bb=np.asarray(b,complex)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def pair(z):
    v=complex(z)
    return [float(v.real),float(v.imag)]


def independent_candidate(direct_ga_main,direct_ga_constraint,ge07_main,
                          ge07_constraint,lambda_main,stage_e_y_main):
    """Add the original independent signed action-source sectors, no subtraction.

    Array layout is original H3F [main 6, constraint 2, time 128, m 0..40].
    Stage E Y is nonanalytic and main-row-only; Lambda is main-row-only.
    This is only an alternative numerical representation of unchanged equations.
    """
    main_shape=(6,128,41);con_shape=(2,128,41)
    raw=(direct_ga_main,direct_ga_constraint,ge07_main,ge07_constraint,
         lambda_main,stage_e_y_main)
    shapes=(main_shape,con_shape,main_shape,con_shape,main_shape,main_shape)
    arrays=tuple(np.asarray(v,complex) for v in raw)
    for v,expect in zip(arrays,shapes):
        if v.shape!=expect or not np.isfinite(v).all():
            raise RuntimeError('D32 independent source sector shape or finite FAIL')
    ga,gc,ma,mc,lam,y=arrays
    base=(ga+ma)+lam
    main=base+y
    con=gc+mc
    if not (np.isfinite(main).all() and np.isfinite(con).all()):
        raise RuntimeError('D32 independent source sum nonfinite')
    return {'rhs':main,'rhs_constraint':con},base


def verify_self(rd,pre,lock):
    if pre['classification']!='GE19_D32_PREEXEC_INDEPENDENT_SIGNED_SECTOR_FIRST_INTERVAL':
        raise RuntimeError('D32 wrong preregistration')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!=pre['branch'] or branch=='main':
        raise RuntimeError('D32 wrong local branch')
    for name,want in lock['sha256_local_files'].items():
        p=ROOT/name
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D32 local source SHA lock FAIL '+name)
    for name,want in pre['frozen_local_code_sha256'].items():
        p=ROOT/name
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D32 immutable D31R1 code SHA lock FAIL '+name)
    for name,want in pre['frozen_results_sha256'].items():
        p=rd/name
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D32 immutable input SHA lock FAIL '+name)
    pre31=json.loads(d31.PRE.read_text());lock31=json.loads(d31.LOCK.read_text())
    frozen,j30,j25=d31.check_inputs(rd,pre31,lock31)
    r31=json.loads((rd/pre['D31R1_json']).read_text())
    j27=json.loads((rd/pre['D27R2_json']).read_text())
    if r31['classification']!=pre['required_D31R1_classification'] or \
       j27['classification']!=pre['required_D27R2_classification']:
        raise RuntimeError('D32 parent classification mismatch')
    if not r31['nonanalytic_StageE_Y_retained'] or \
       any(r31[k] for k in ('Z11_certified','Z20_certified','Z21_certified')):
        raise RuntimeError('D32 immutable D31R1 science scope mismatch')
    if tuple((int(c['mode']),float(c['beta'])) for c in r31['per_case'])!=tuple(
            (int(c[0]),float(c[1])) for c in pre['cases']):
        raise RuntimeError('D32 cases not exact immutable D31R1 cases')
    print('GE19_D32_ALL_D27R2_D31R1_AND_ACTION_PARENT_SHA_LOCK_PASS',flush=True)
    return frozen,j30,j25,r31,j27


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir).resolve()
    jp=Path(args.json_out).resolve();zp=Path(args.npz_out).resolve()
    if jp.exists() or zp.exists():
        raise RuntimeError('D32 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    frozen,j30,j25,r31,j27=verify_self(rd,pre,lock)
    d25=d31.d25;d30=d31.d30
    r7=d25.d20.source.old.r7
    d27=d30.d29.d28.d27
    if d27.d20.source.old.r7 is not r7:
        raise RuntimeError('D32 original action operator source module mismatch')
    if tuple(float(b) for b in r7.BETAS)!=(1.0,0.5,0.1):
        raise RuntimeError('D32 beta cohort changed')
    support=set(j30['exact_support_nonnegative'])
    if any(m in support for m in pre['off_support_modes']):
        raise RuntimeError('D32 analytic GE06 support unexpected')
    output={}
    report={
      'classification':'GE19_D32_INDEPENDENT_SIGNED_GE06_GE07_LAMBDA_STAGEE_FIRST_INTERVAL_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
      'preregistration':pre['classification'],'source_sha256':sha(Path(__file__)),
      'scope':'First interval, frozen Cstar Nt128 original action, unchanged D31R1 cases and n1/n8; candidate B independently assembles direct GE06+original GE07+Lambda+Stage E Y, excluding only the reported finite FFT split remainder. No physical source fit, tolerance or mode deletion.',
      'claim_boundary':'Alternative source arithmetic diagnostic only, no rigorous roundoff envelope or continuum Ward/H1/on-shell proof, no H3 full-window or H4 certification.',
      'D22A_science_FAIL_immutable':True,'D27_original_selected_triplet_FAIL_immutable':True,
      'D31_original_narrow_remainder_FAIL_immutable':True,'D31R1_parent_diagnostic_only':True,
      'original_action_modified':False,'production_H3F_source_modified':False,
      'original_shift_gate_unchanged':True,'boundary_rule_unchanged_candidate_momenta_reprojected':True,
      'all_modes_retained':True,'nonanalytic_StageE_Y_retained':True,'no_observational_tuning':True,
      'Z11_certified':False,'Z20_certified':False,'Z21_certified':False,
      'full_H4_Ward_certified':False,'lensing_licensed':False,'H3_full_window_solve_performed':False,
      'q20_B20_recomputed':False,'per_case':[],'per_beta_ledger':{},
      'candidate_B_original_shift_gate_report_only':{},
    }
    with ExitStack() as es:
        z22=es.enter_context(np.load(frozen['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z30=es.enter_context(np.load(rd/pre['D30_npz'],allow_pickle=False))
        z31=es.enter_context(np.load(rd/pre['D31R1_npz'],allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        if x.shape!=(128,) or not np.array_equal(x,np.asarray(z22['x_primary'],float)):
            raise RuntimeError('D32 original Cstar background grid mismatch')
        def load30(key,shape):
            v=np.asarray(z30[key],complex)
            if v.shape!=shape or not np.isfinite(v).all():
                raise RuntimeError('D32 direct GE06 input shape or finiteness FAIL '+key)
            return v
        direct_main=load30('direct_GE06_main_six_by_128_by_41',(6,128,41))
        direct_con=load30('direct_GE06_constraint_two_by_128_by_41',(2,128,41))
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            if active['ctx'] is None:
                raise RuntimeError('D32 original-action clock not installed')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH)
            active['ctx']=ctx;ctx.knot_check()
            h1=np.asarray(z22['D17_H1_action_primary'],complex)
            dh1=np.asarray(z22['D17_H1dot_action_primary'],complex)
            if h1.shape!=(6,6,128) or dh1.shape!=(6,4,128):
                raise RuntimeError('D32 H1 action parent shape mismatch')
            print('GE19_D32_ORIGINAL_GE06_GE07_LAMBDA_STAGEE_INDEPENDENT_REBUILD_BEGIN',flush=True)
            rebuilt,sectors=d27.audited_rebuild(r7,d27.r14,mod6,mod7,bg,tag,h1,dh1,nx=1024)
            frozen_src=d25.freeze_source(r7,bg,z22)
            A={};B={};beta_details={}
            for ib,beta in enumerate(r7.BETAS):
                orig=rebuilt[beta];sec=sectors[beta]
                original_replay=max(rel(orig['rhs'],frozen_src[beta]['rhs']),
                                    rel(orig['rhs_constraint'],frozen_src[beta]['rhs_constraint']))
                if original_replay>pre['original_source_replay_limit']:
                    raise RuntimeError('D32 original D22A full source replay FAIL '+str(beta))
                A[beta]=d31.candidate_swap(orig['rhs'],orig['rhs_constraint'],
                    sec['GE06_main'],sec['GE06_constraint'],direct_main,direct_con)
                B[beta],base=independent_candidate(direct_main,direct_con,
                    sec['GE07_main'],sec['GE07_constraint'],orig['Q_lambda'],orig['Y_H3'])
                for key,arr in (('rhs',(6,128,41)),('rhs_constraint',(2,128,41))):
                    old_A=np.asarray(z31[f'beta{ib}_candidate_'+('main_six_by_128_by_41' if key=='rhs' else 'constraint_two_by_128_by_41')],complex)
                    if old_A.shape!=arr or rel(old_A,A[beta][key])>pre['archived_candidate_A_replay_limit'] or any(
                            rel(old_A[:,:,m],A[beta][key][:,:,m])>pre['archived_candidate_A_replay_limit']
                            for m in (1,14,40)):
                        raise RuntimeError('D32 archived D31R1 candidate A source replay FAIL beta='+str(beta)+' '+key)
                if rel(sec['GE07_main'],orig['Q_matter'])>pre['independent_GE07_replay_limit']:
                    raise RuntimeError('D32 independent GE07 main vs original matter replay FAIL')
                if max(rel(A[beta]['rhs'][:,:,40],B[beta]['rhs'][:,:,40]),
                       rel(A[beta]['rhs_constraint'][:,:,40],B[beta]['rhs_constraint'][:,:,40]))>pre['m40_source_relative_limit']:
                    raise RuntimeError('D32 in-support original-action m40 source preservation FAIL')
                for m in pre['off_support_modes']:
                    if np.any(direct_main[:,:,m]) or np.any(direct_con[:,:,m]):
                        raise RuntimeError('D32 offsupport GE06 not identically zero')
                    y=np.asarray(orig['Y_H3'][3,:,m],complex)
                    if not np.any(y):
                        raise RuntimeError('D32 nonanalytic Y vanished offsupport')
                    if not np.array_equal(B[beta]['rhs'][3,:,m],y):
                        raise RuntimeError('D32 independently assembled offsupport scalar Y not exactly retained')
                # The signed A-B residual measures floating source assembly. It
                # is not inserted, fitted, or promoted into a physical source.
                difference_main=A[beta]['rhs']-B[beta]['rhs']
                difference_con=A[beta]['rhs_constraint']-B[beta]['rhs_constraint']
                beta_details[str(beta)]={
                  'archived_D31R1_candidate_A_source_replayed':True,
                  'original_D22A_source_replay_relative':original_replay,
                  'candidate_A_minus_B_main_l2_report_only':float(np.linalg.norm(difference_main)),
                  'candidate_A_minus_B_constraint_l2_report_only':float(np.linalg.norm(difference_con)),
                  'candidate_A_minus_B_main_max_abs_report_only':float(np.max(np.abs(difference_main))),
                  'candidate_A_minus_B_constraint_max_abs_report_only':float(np.max(np.abs(difference_con))),
                  'independent_candidate_B_Y_addition_error_relative_report_only':rel(B[beta]['rhs']-base,orig['Y_H3']),
                }
                output[f'beta{ib}_independent_main_six_by_128_by_41']=B[beta]['rhs']
                output[f'beta{ib}_independent_constraint_two_by_128_by_41']=B[beta]['rhs_constraint']
                print('GE19_D32_INDEPENDENT_SOURCE beta='+str(beta)
                      +' AminusBmain='+f'{beta_details[str(beta)]["candidate_A_minus_B_main_l2_report_only"]:.6e}'
                      +' AminusBconstraint='+f'{beta_details[str(beta)]["candidate_A_minus_B_constraint_l2_report_only"]:.6e}',flush=True)
            report['per_beta_ledger']=beta_details
            print('GE19_D32_ALL_THREE_BETA_INDEPENDENT_SECTOR_AND_Y_RETENTION_PASS',flush=True)
            x0,x1=float(x[0]),float(x[1])
            for m,beta in tuple((int(c[0]),float(c[1])) for c in pre['cases']):
                ib=list(r7.BETAS).index(beta)
                key=f'm{m}_beta{str(beta).replace(".","p")}'
                archived=next(c for c in r31['per_case'] if c['mode']==m and c['beta']==beta)
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                rfa,cfa=r7._source_interp(x,A,m)
                rfb,cfb=r7._source_interp(x,B,m)
                op0A=d25.shift_at(r7,mod6,mod7,bg,tag,k,x0,None,rfa,cfa)
                op1A=d25.shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rfa,cfa)
                op0B=d25.shift_at(r7,mod6,mod7,bg,tag,k,x0,None,rfb,cfb)
                op1B=d25.shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rfb,cfb)
                y0A,prA=d31.projection(r7,mod6,mod7,bg,tag,k,x0,rfa,cfa,ib)
                y0B,prB=d31.projection(r7,mod6,mod7,bg,tag,k,x0,rfb,cfb,ib)
                a0ref=np.asarray(z31[key+'_candidate_y0'],complex)
                if rel(y0A,a0ref)>pre['archived_candidate_A_replay_limit']:
                    raise RuntimeError('D32 archived D31R1 candidate A initial state replay FAIL '+key)
                initB=d25.metric_from_y(r7,op0B,y0B,ib)
                prB['passes_original_boundary_gate_report_only']=bool(max(
                   prB['lapse_relative_backward'],prB['shift_relative_backward'],
                   initB['relative_backward'])<=pre['original_boundary_backward_gate'])
                tests=[]
                for n in pre['substeps']:
                    y1A=np.asarray(z31[f'{key}_n{n}_candidate_y1'],complex)
                    opA=d25.metric_from_y(r7,op1A,y1A,ib)
                    archivedA=next(z for z in archived['candidate'] if z['substeps']==n)
                    if abs(opA['relative_backward']-archivedA['shift']['relative_backward'])>pre['archived_A_metric_replay_limit']*max(
                            abs(opA['relative_backward']),abs(archivedA['shift']['relative_backward']),TINY):
                        raise RuntimeError('D32 archived D31R1 candidate A endpoint metric replay FAIL '+key+' n='+str(n))
                    def rr(t,fun=rfb,idx=ib):
                        return np.asarray(fun(t),complex)[:,idx:idx+1]
                    def cc(t,fun=cfb,idx=ib):
                        return np.asarray(fun(t),complex)[:,idx:idx+1]
                    y1B,erB=d25.integrate(r7,mod6,mod7,bg,tag,k,y0B,x0,x1,rr,cc,n)
                    resB=d25.metric_from_y(r7,op1B,y1B,ib)
                    if m==40 and rel(y1B,y1A)>pre['m40_endpoint_state_relative_limit']:
                        raise RuntimeError('D32 in-support original-action m40 endpoint preservation FAIL n='+str(n))
                    tests.append({'substeps':n,'candidate_A_archived_shift':archivedA['shift'],
                        'candidate_B_independent_shift':resB,'candidate_B_Radau_block_backward':float(erB),
                        'candidate_B_vs_A_end_state_relative_report_only':rel(y1B,y1A),
                        'candidate_B_original_shift_gate_report_only':bool(resB['relative_backward']<=pre['original_shift_gate'])})
                    output[f'{key}_n{n}_independent_candidate_B_y1']=y1B
                    print(f'GE19_D32_MODE m={m} beta={beta} n={n} '
                          f'A_abs={opA["absolute_residual"]:.6e} '
                          f'B_abs={resB["absolute_residual"]:.6e} '
                          f'B_relative={resB["relative_backward"]:.6e} '
                          f'B_Radau={erB:.3e}',flush=True)
                source_diff_first=complex(A[beta]['rhs_constraint'][0,0,m]-B[beta]['rhs_constraint'][0,0,m])
                source_diff_last=complex(A[beta]['rhs_constraint'][0,1,m]-B[beta]['rhs_constraint'][0,1,m])
                row27=next((c for c in j27['per_case'] if c['mode']==m and c['beta']==beta),None)
                prior_fft=None
                if row27 is not None:
                    prior_fft={'first':row27['shift_source_fft_signed_remainder']['first'],
                               'last':row27['shift_source_fft_signed_remainder']['last'],
                               'A_minus_B_first_vs_D27_remainder_abs_report_only':abs(source_diff_first-complex(*row27['shift_source_fft_signed_remainder']['first'])),
                               'A_minus_B_last_vs_D27_remainder_abs_report_only':abs(source_diff_last-complex(*row27['shift_source_fft_signed_remainder']['last']))}
                report['per_case'].append({'mode':m,'beta':beta,'candidate_B_initial':initB,
                    'candidate_B_original_rule_momentum_projection':prB,
                    'candidate_A_minus_B_shift_source_first':pair(source_diff_first),
                    'candidate_A_minus_B_shift_source_last':pair(source_diff_last),
                    'candidate_B_shift_source_first':pair(B[beta]['rhs_constraint'][0,0,m]),
                    'candidate_B_shift_source_last':pair(B[beta]['rhs_constraint'][0,1,m]),
                    'candidate_B_scalar_first':pair(B[beta]['rhs'][3,0,m]),
                    'StageE_Y_scalar_first':pair(rebuilt[beta]['Y_H3'][3,0,m]),
                    'prior_D27R2_fft_remnant_comparison_report_only':prior_fft,
                    'original_D31R1_candidate_A_initial_shift':archived['candidate_initial'],
                    'baseline_D31R1_original_n8_shift':archived['baseline'][-1]['shift'],
                    'comparisons':tests})
                output[key+'_independent_candidate_B_y0']=y0B
                report['candidate_B_original_shift_gate_report_only'][key]=[row['candidate_B_original_shift_gate_report_only'] for row in tests]
        finally:
            r7._bg_point=old_bg
            r7._CANONICAL_LOCAL_CACHE=old_cache
    jp.parent.mkdir(parents=True,exist_ok=True)
    zp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    np.savez_compressed(zp,**output)
    print('GE19_D32_CLASSIFICATION '+report['classification'],flush=True)


if __name__=='__main__':
    main()
