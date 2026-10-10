#!/usr/bin/env python3
"""GE19 D22A: recompute consistent C_star Nt128 B10, Z11 and Z20 candidates.

D17 original-action canonical H1 and D19R1 full-node GE05 bath are numerical
parents. Reuse frozen R2 first-order eta boundary from Repair32B, not an old
source-dependent algebraic initial state. Recompute GE05 M1[Z10,q10] and
stage-E completed H3 source from new H1. Solve independent Z11 and Z20
particular equations in the D17 original-action background, with source-aware
projected Z20 momentum boundary from frozen Repair18.

A single-cohort numerical parent candidate is NOT H2/H3 certification,
q20, original GE05 on-shell, H4 Ward, Z21, or lensing.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from contextlib import ExitStack
import numpy as np

from ge19 import h4f3d20r1_recompute_five_sources_and_bath_ward as d20
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17driver
from ge19 import h4f3d17_original_action_dense_H1_core as d17core
from ge19 import repair32b_factor2_corrected_reduced_h2_z11_reconstruction as h2
from ge19 import repair18_zero_coordinate_constraint_projected_momentum_boundary as r18
from ge19 import repair14_self_consistent_reduced_h3_z20_particular as r14
from ge19 import h3f_corrected_y_source_adapter as h3f

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d22a_predata_original_action_parent_reclosure.json'
TINY=1e-300


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for c in iter(lambda:f.read(1<<20),b''):h.update(c)
    return h.hexdigest()


def rel(a,b):
    a=np.asarray(a); b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))


def aor(a,b):
    a=np.asarray(a); b=np.asarray(b)
    diff=np.abs(a-b)
    return float(np.max(np.minimum(diff,diff/np.maximum(np.maximum(np.abs(a),np.abs(b)),TINY))))


def exact_git(relpath,want):
    head=subprocess.check_output(['git','rev-parse','HEAD:'+relpath],cwd=ROOT,text=True).strip()
    work=subprocess.check_output(['git','hash-object',str(ROOT/relpath)],cwd=ROOT,text=True).strip()
    if head!=want or work!=want:
        raise RuntimeError(f'D22A original git blob changed {relpath}: {head}/{work} != {want}')


def verify(rd,trace,pre):
    if pre['classification']!='GE19_D22A_PREDATA_D17_D19R1_CSTAR_ORIGINAL_ACTION_PARENT_CANDIDATES':
        raise RuntimeError('D22A preregistration changed')
    for relpath,want in pre['frozen_git_blobs'].items():exact_git(relpath,want)
    for relpath,want in pre['local_sha256'].items():
        if sha(ROOT/relpath)!=want:raise RuntimeError('D22A package code modified '+relpath)
    files={}
    for key,(filename,want) in pre['parent_archives'].items():
        p=rd/filename
        if not p.is_file() or sha(p)!=want:raise RuntimeError('D22A parent archive missing/changed '+key)
        files[key]=p
    if not trace.is_file() or sha(trace)!=pre['repair26_trace_sha256'] or trace.stat().st_size!=26643162:
        raise RuntimeError('D22A original Repair26 trace changed')
    # Verify all frozen H3F/H3G/Repair32C/Repair13 inputs without relabelling them.
    d20.source.code_lock()
    source_inputs,source_locks=d20.source.frozen_inputs(rd,trace)
    for key in ('D17_JSON','D19_JSON','D20_JSON','D21_JSON'):
        report=json.loads(files[key].read_text())
        if report.get('Z21_certified') is True or report.get('full_original_H4_Ward_certified') is True:
            raise RuntimeError('D22A parent silently changed H4 science claim '+key)
    if json.loads(files['D19_JSON'].read_text()).get('numerical_tol_pass') is not True:
        raise RuntimeError('D22A D19 bath has no numerical PASS')
    if json.loads(files['D21_JSON'].read_text()).get('classification')!=\
       'GE19_D21R1_EXACT_GE05_PT_CHAIN_RULE_M2_NUMERICAL_REPAIR_PASS_Q20_Z11_FULL_H4_OPEN':
        raise RuntimeError('D22A D21R1 scalar M2 repair not PASS')
    return files,source_inputs,source_locks


def projected_z20(r7,mod6,mod7,bg,tag,sources,progress=5):
    """H3F source-aware Repair18 projected momentum, not old zero-momentum BC."""
    x=np.asarray(bg['x'],float); nt=len(x)
    nbet=len(r7.BETAS);nm=len(r7.M_SOLVE)
    states=np.empty((nbet,nm,6,nt),complex); dots=np.empty((nbet,nm,4,nt),complex)
    p0=np.empty((nbet,nm,4),complex)
    linear=0.;shift=0.;aniso=0.;bscaled=0.;blapse=0.;bshift=0.;initrank=[]
    for jm,m in enumerate(r7.M_SOLVE):
        k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
        rhsfun,confun=r7._source_interp(x,sources,int(m))
        rr=np.asarray(rhsfun(float(x[0])),complex)
        cc=np.asarray(confun(float(x[0])),complex)
        if rr.ndim==1:rr=rr[:,None]
        if cc.ndim==1:cc=cc[:,None]
        M,F,ZY,ZR,WY,WR,Cmat,bp,_=r7._canonical_operator_matrices(
            mod6,mod7,bg,tag,k,float(x[0]))
        y0=np.zeros((8,nbet),complex)
        for ib,_beta in enumerate(r7.BETAS):
            source0=np.concatenate((rr[:,ib],cc[:,ib]))
            offset=WR@source0
            lr=Cmat[4];sr=Cmat[10]+Cmat[11]
            A=np.vstack((lr@WY,sr@WY))[:,4:8]
            rhs=np.array([rr[0,ib]-lr@offset,cc[0,ib]-sr@offset],complex)
            p,sd=r18.projected_momentum_solve(A,rhs)
            ev=r18.evaluate_candidate(Cmat,WY,WR,source0,rr[:,ib],cc[:,ib],p)
            y0[4:8,ib]=p;p0[ib,jm]=p
            bscaled=max(bscaled,float(sd['scaled_relative_residual_final']))
            blapse=max(blapse,float(ev['lapse']['metric']))
            bshift=max(bshift,float(ev['shift']['metric']))
            initrank.append((int(sd['rank']),int(sd['augmented_rank'])))
        Y,steps=r7._radau2_integrate_canonical(mod6,mod7,bg,tag,k,y0,rhsfun,confun)
        st,dt,diag=r7._reconstruct_canonical_solution(mod6,mod7,bg,tag,k,Y,rhsfun,confun)
        states[:,jm]=st; dots[:,jm]=dt
        linear=max(linear,float(steps['radau_block_scaled_relative_L2_residual_max']),
            float(diag['algebraic_scaled_relative_L2_residual_max']),
            float(diag['lapse_noether_row_relative_residual_max']))
        shift=max(shift,float(diag['shift_constraint_relative_L2_max']))
        aniso=max(aniso,float(diag['anisotropy_constraint_relative_L2_max']))
        if jm%progress==0 or jm+1==nm:
            print(f'GE19_D22A_Z20_SOURCE_AWARE_MODE {jm+1}/{nm} '
                  f'linear={linear:.3e} shift={shift:.3e}',flush=True)
    controls=dict(linear_system_relative_max=linear,shift_constraint_relative_max=shift,
        anisotropy_constraint_relative_max=aniso,
        boundary_scaled_relative_max=bscaled,boundary_lapse_backward_max=blapse,
        boundary_shift_backward_max=bshift,
        rank_two_both=all(a==2 and b==2 for a,b in initrank),
        all_states_finite=bool(np.isfinite(states).all() and np.isfinite(dots).all()))
    return states,dots,p0,controls


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--results-dir',required=True)
    p.add_argument('--repair26-trace',required=True)
    p.add_argument('--json-out',required=True)
    p.add_argument('--npz-out',required=True)
    a=p.parse_args();rd=Path(a.results_dir).resolve();trace=Path(a.repair26_trace).resolve()
    oj=Path(a.json_out).resolve();on=Path(a.npz_out).resolve()
    if oj.exists() or on.exists():raise RuntimeError('D22A refuses to overwrite prior results')
    pre=json.loads(PRE.read_text())
    files,inputs,locks=verify(rd,trace,pre)
    print('GE19_D22A_D17_D19_D20_D21_H3F_Z11_R18_FROZEN_SHA_PASS',flush=True)
    old=d20.source.old;r7=old.r7
    with ExitStack() as stack:
        r13=stack.enter_context(np.load(inputs['r13'],allow_pickle=False))
        h3f_parent=stack.enter_context(np.load(inputs['h3fn'],allow_pickle=False))
        z11_parent=stack.enter_context(np.load(inputs['z11'],allow_pickle=False))
        d17=stack.enter_context(np.load(files['D17_NPZ'],allow_pickle=False))
        d19=stack.enter_context(np.load(files['D19_NPZ'],allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,r13)
        tag='C_star';bg=bgs[(128,tag)];x=np.asarray(bg['x'],float)
        xf=np.asarray(d17['primary_C_star_x_dense_sub4'],float)
        if not (np.array_equal(x,np.asarray(d17['x_primary'],float)) and
                np.array_equal(x,np.asarray(d19['original_x_primary'],float)) and
                np.array_equal(x,xf[::4]) and
                np.array_equal(x,np.asarray(z11_parent['x_primary'],float)) and
                np.array_equal(x,np.asarray(h3f_parent['x_primary'],float))):
            raise RuntimeError('D22A exact six-way original action time grid mismatch')
        Y=np.asarray(d17['primary_C_star_H1_canonical_y_dense_sub4'],complex)
        H1,dh1,back,raw,slots=d20.canonical_knots_to_h1(Y,bg,tag,r7,mod6,mod7)
        X=old.r24.first_order_X_modes(r7,bg,H1)
        Xref=np.asarray(d17['primary_C_star_X10_original_action_dense_sub4'],complex)[:,::4]
        if max(back,slots,rel(X,Xref))>1e-9:
            raise RuntimeError('D22A canonical source-action H1/X10 did not reconstruct')
        full_z=np.asarray(d19['physical_Cstar_Nt128_Nq2048_z_sub256'],complex)
        full_v=np.asarray(d19['physical_Cstar_Nt128_Nq2048_v_sub256'],complex)
        if full_z.shape!=(2048,6,128) or full_v.shape!=full_z.shape:
            raise RuntimeError('D22A complete D19 bath missing')
        r,w=old.c4.tan_gl_nodes(2048);r=np.asarray(r,float);w=np.asarray(w,float)
        wz=np.einsum('n,nmt->mt',w,full_z,optimize=True)
        wv=np.einsum('n,nmt->mt',w,full_v,optimize=True)
        if max(rel(wz,np.asarray(d19['sub256_weighted_z'],complex)),
               rel(wv,np.asarray(d19['sub256_weighted_v'],complex)))>1e-11:
            raise RuntimeError('D22A full-node D19 bath did not replay')
        B10=X-wz; rhs11=h2.source_from_B(bg,B10)
        if not (rhs11.shape==(6,6,128) and np.isfinite(rhs11).all()):
            raise RuntimeError('D22A exact GE05 M1 -> GE06 factor-two mapping failed')
        frozen_h1=np.asarray(h3f_parent['C_star_H1_primary'],complex)
        oldref=np.asarray(z11_parent['C_star_Z11_reference_primary'],complex)
        oldstate=np.asarray(z11_parent['C_star_Z11_primary'],complex)
        olddot=np.asarray(z11_parent['C_star_Z11dot_primary'],complex)
        # Original R2 physical tangent boundary remains fixed. The old
        # source-dependent algebraic values MUST NOT be reused as reference.
        ref=oldref.copy(); refdot=olddot.copy()
        boundary_replay=max(aor(oldstate[:,[1,2,3,4],0],ref[:,[1,2,3,4],0]),
                           aor(olddot[:,:,0],refdot[:,:,0]))
        if boundary_replay>1e-8:raise RuntimeError('D22A frozen R2 eta dynamic boundary failed replay')
        # Restore even on exceptions: source files and immutable caches untouched.
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={}
        active={'ctx':None}
        def action_bgpoint(bgarg,xq):
            if active['ctx'] is None:raise RuntimeError('D22A action context missing')
            return active['ctx'](bgarg,xq)
        r7._bg_point=action_bgpoint
        try:
            evalH,_=d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            z11,dz11,c11=h2.solve_h2_case(mod6,mod7,bg,tag,rhs11,ref,refdot)
            print('GE19_D22A_NEW_B10_AND_R2_BOUNDARY_Z11_SOLVED '
                  f'linear={c11["linear_system_relative_L2_max"]:.3e} '
                  f'shift={c11["shift_constraint_relative_L2_max"]:.3e}',flush=True)
            # H3F includes GE06/GE07/Lambda and replaces, not adds to,
            # the historical scalar-only Y contribution.
            print('GE19_D22A_H3F_SOURCE_NX1024_BEGIN',flush=True)
            sources=h3f.source_bundle_reduced_lambda(
                r7,r14,mod6,mod7,bg,np.asarray(bg['rho_lambda_action'],float),
                tag,1024,H1,dh1)
            print('GE19_D22A_H3F_SOURCE_NX2048_CONTROL_BEGIN',flush=True)
            source_hi=h3f.source_bundle_reduced_lambda(
                r7,r14,mod6,mod7,bg,np.asarray(bg['rho_lambda_action'],float),
                tag,2048,H1,dh1)
            srcsp=max(rel(sources[beta]['rhs'][:,:,1:41],source_hi[beta]['rhs'][:,:,1:41])
                      for beta in r7.BETAS)
            z20,dz20,p0,c20=projected_z20(r7,mod6,mod7,bg,tag,sources)
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
        print('GE19_D22A_ACTION_H3F_Z20_PROJECTED_BOUNDARY_SOLVED',flush=True)
        old_B=np.asarray(z11_parent['C_star_B10_primary'],complex)
        old_Z20=np.asarray(h3f_parent['C_star_Z20_primary'],complex)
        old_Z11=np.asarray(z11_parent['C_star_Z11_primary'],complex)
        new_B20=old.r24.X20_modes(r7,bg,z20) # X20 is NOT B20 until q20 recomputed.
        expected={'source_Nx1024_vs_Nx2048':5e-4,'linear':1e-8,'constraint':1e-6,
                  'boundary':1e-8,'initial':1e-8}
        gates={
            'immutable_original_action_and_actual_parent_SHA':True,
            'Cstar_Nt128_original_action_background_knots':True,
            'D17_H1_canonical_reconstruction':max(back,slots,rel(X,Xref))<=1e-9,
            'D19_full_bath_weighted_replay':True,
            'frozen_R2_Z11_dynamic_boundary_replayed':boundary_replay<=expected['initial'],
            'new_Z11_linear_relative':c11['linear_system_relative_L2_max']<=expected['linear'],
            'new_Z11_shift_anisotropy':max(c11['shift_constraint_relative_L2_max'],
                                          c11['anisotropy_constraint_relative_L2_max'])<=expected['constraint'],
            'new_Z11_initial_dynamic_boundary':c11['initial_dynamic_boundary_abs_or_rel_max']<=expected['initial'],
            'H3F_new_source_spatial_Nx1024_Nx2048':srcsp<=expected['source_Nx1024_vs_Nx2048'],
            'new_Z20_linear_relative':c20['linear_system_relative_max']<=expected['linear'],
            'new_Z20_shift_anisotropy':max(c20['shift_constraint_relative_max'],c20['anisotropy_constraint_relative_max'])<=expected['constraint'],
            'new_Z20_projected_boundary_rank_and_error':c20['rank_two_both'] and
                max(c20['boundary_scaled_relative_max'],c20['boundary_lapse_backward_max'],
                    c20['boundary_shift_backward_max'])<=expected['boundary'],
            'new_parent_arrays_finite':all(np.isfinite(v).all() for v in (B10,rhs11,z11,dz11,z20,dz20,p0,new_B20))
        }
        passed=all(gates.values())
        output=dict(
            x_primary=x,D17_H1_action_primary=H1,D17_H1dot_action_primary=dh1,
            D19_weighted_z10_primary=wz,D19_weighted_v10_primary=wv,
            B10_D17_D19_primary=B10,GE05_M1_rhs_for_Z11_primary=rhs11,
            Z11_D17_D19_candidate_primary=z11,Z11dot_D17_D19_candidate_primary=dz11,
            Z11_R2_frozen_reference_primary=ref,
            Z20_D17_H3F_candidate_primary=z20,Z20dot_D17_H3F_candidate_primary=dz20,
            Z20_source_aware_projected_p0_primary=p0,
            X20_D17_Z20_primary_NOT_B20=new_B20)
        for ib,beta in enumerate(r7.BETAS):
            output[f'beta{ib}_H3F_D17_source_rows']=np.asarray(sources[beta]['rhs'],complex)
            output[f'beta{ib}_H3F_D17_source_constraints']=np.asarray(sources[beta]['rhs_constraint'],complex)
        result={
            'classification':('GE19_D22A_CSTAR_D17_D19_B10_Z11_Z20_NUMERICAL_CANDIDATE_PASS_Q20_AND_FULL_H4_OPEN'
                              if passed else 'GE19_D22A_CSTAR_PARENT_NUMERICAL_CANDIDATE_FAIL_Q20_AND_FULL_H4_OPEN'),
            'preregistration':pre['classification'],'gates':{k:bool(v) for k,v in gates.items()},
            'cohort':'C_star, Nt128, all six positive H1 modes, Z20 beta 1/0.5/0.1 and m1..40, Nq2048 D19 bath',
            'input_sha256':{k:sha(v) for k,v in files.items()},
            'frozen_parent_input_sha256':locks,
            'repair26_trace_sha256':sha(trace),
            'D17_H1_vs_frozen_H3F_relative_report_only':rel(H1,frozen_h1),
            'new_B10_vs_frozen_Repair32B_relative_report_only':rel(B10,old_B),
            'new_Z11_vs_frozen_Repair32B_relative_report_only':rel(z11,old_Z11),
            'new_Z20_vs_frozen_H3F_relative_report_only':rel(z20,old_Z20),
            'new_H3F_source_Nx1024_vs_Nx2048_relative_L2_max':srcsp,
            'D17_canonical_backward_relative_max':back,
            'frozen_R2_dynamic_initial_boundary_aor':boundary_replay,
            'Z11_numerical':{k:v for k,v in c11.items() if k!='canonical_march_diagnostics'},
            'Z20_numerical':c20,
            'Z11_recomputed_numerical_candidate':passed,
            'Z20_recomputed_numerical_candidate':passed,
            'q20_and_B20_recomputed':False,'M1_H4_new_q20_closed':False,
            'Z11_certified':False,'Z20_certified_for_new_D17_drive':False,
            'true_continuous_original_H1_certified':False,
            'all_interval_GE05_on_shell_certified':False,
            'full_original_H4_Ward_certified':False,'Z21_certified':False,
            'lensing_licensed':False,'no_observational_tuning':True,
            'frozen_Repair37_SCIENCE_FAIL_immutable':True,
            'claim_boundary':'Numerically rebuilt Cstar Nt128 B10 and source-aware Z11/Z20 candidates from immutable D17 H1 and D19 bath. Old R2 eta boundary is reused. The D17 original-action H1 and D19 bath are not rigorous continuous enclosures, and Cstar time/quadrature control for dependent parents is not complete. X20 is NOT B20 until new q20 projection is computed. No q20, full H4 Ward, Z21 or lensing.'
        }
        oj.parent.mkdir(parents=True,exist_ok=True)
        np.savez_compressed(on,**output)
        oj.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
        print('GE19_D22A_CLASSIFICATION '+result['classification'],flush=True)
        if not passed:raise SystemExit(2)


if __name__=='__main__':main()
