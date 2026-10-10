#!/usr/bin/env python3
"""GE19 D45: independent off-clock *homogeneous* background and source-interpolation diagnostic.

Original Cstar action/background and original D33 beta-specific 41-mode source are
READ ONLY. No evolution, no source replacement, no constraint reprojection, no
changed gates. Analytic charge/Friedmann reconstruction is independent of
ActionBackground interpolation, but NOT a full first-order H1 EOM/on-shell proof.
PCHIP-vs-linear is a sensitivity comparator, NOT an independent source truth.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.special import lambertw

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d45_h1_offclock_source_audit_prereg.json'
TINY=1e-300
STEM='ge19_h4f3d45_h1_offclock_source_audit'


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def require(condition,message):
    if not condition:raise RuntimeError('GE19_D45_'+message)


def rel_l2(x,y):
    a=np.asarray(x);b=np.asarray(y)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))


def exp_branch_kq(z,k2,z0):
    z=np.asarray(z,float)
    return 4*k2*z0*z*np.exp(z*z)


def stable_exp_k(z,k2,z0):
    z=np.asarray(z,float)
    return 2*k2*z0*z0*np.expm1(z*z)


def invert_exp_charge(kq,k2,z0):
    # Algebraic inversion of the ORIGINAL Exp branch: KQ=4*K2*Z0*z*exp(z**2).
    kq=np.asarray(kq,float);v=kq/(4*k2*z0)
    require(np.isfinite(v).all(),'INVALID_CHARGE_INVERSION_INPUT')
    zz=0.5*np.real(lambertw(2*v*v,0))
    require(np.isfinite(zz).all() and np.all(zz>=0),'EXP_BRANCH_INVERSION_NONFINITE')
    z=np.sign(v)*np.sqrt(zz)
    require(rel_l2(exp_branch_kq(z,k2,z0),kq)<2e-12,'EXP_BRANCH_INVERSION_SELF_TEST_FAIL')
    return z


def friedmann_from_charge(x,charge,lambda_val,c,k2,q0,z0):
    x=np.asarray(x,float);a=np.exp(x); kq=charge/a**3
    z=invert_exp_charge(kq,k2,z0)
    q=q0+z0*z;k=stable_exp_k(z,k2,z0)
    h2=(q*kq-k)/3+c/a**3+lambda_val
    require(np.isfinite(h2).all() and np.all(h2>0),'NONPOSITIVE_FROZEN_FRIEDMANN')
    return dict(a=a,z=z,q=q,kq=kq,k=k,h=np.sqrt(h2),h2=h2)


def source_at_midpoints(x,main,con):
    x=np.asarray(x,float)
    src=np.concatenate((main,con),axis=0)
    require(src.shape==(8,128,41,3) and np.isfinite(src).all(),'BAD_ORIGINAL_SOURCE_AXES')
    mid=(x[:-1]+x[1:])/2
    pc=PchipInterpolator(x,src.real,axis=1,extrapolate=False)(mid)+1j*PchipInterpolator(x,src.imag,axis=1,extrapolate=False)(mid)
    ln=(src[:,:-1]+src[:,1:])/2
    # The original source must replay exactly on all frozen clock knots.
    pc_clock=PchipInterpolator(x,src.real,axis=1,extrapolate=False)(x)+1j*PchipInterpolator(x,src.imag,axis=1,extrapolate=False)(x)
    require(rel_l2(pc_clock,src)<3e-14,'PCHIP_SOURCE_KNOT_REPLAY_FAILED')
    require(np.isfinite(pc).all() and np.isfinite(ln).all(),'NONFINITE_SOURCE_MIDPOINTS')
    return mid,pc,ln,rel_l2(pc_clock,src)


def synth_test():
    z=np.array([-.25,-.01,0,.01,.25]);kq=exp_branch_kq(z,9500,1e-17)
    zr=invert_exp_charge(kq,9500,1e-17)
    require(np.max(np.abs(z-zr))<1e-12,'SYNTHETIC_EXP_BRANCH_FAIL')
    x=np.linspace(-1,0,128);main=np.zeros((6,128,41,3),complex);con=np.zeros((2,128,41,3),complex)
    main[0]=np.exp(2*x)[:,None,None]
    main[3,:,14,:]=(1+1j)*np.sin(x)[:,None]
    mid,pc,lin,err=source_at_midpoints(x,main,con)
    require(mid.shape==(127,) and pc.shape==(8,127,41,3) and err<3e-14,'SYNTHETIC_SOURCE_SHAPE_FAIL')
    require(np.max(np.abs(pc-lin))>0,'SYNTHETIC_INTERPOLATION_NOT_DISTINGUISHED')
    try:require(False,'EXPECTED_NEGATIVE_GUARD')
    except RuntimeError as e:require('EXPECTED_NEGATIVE_GUARD' in str(e),'NEGATIVE_GUARD_WRONG')
    else:raise AssertionError('D45 negative control accepted')
    print('GE19_D45_MANUFACTURED_EXP_BRANCH_SOURCE_INTERPOLATION_AND_NEGATIVE_PASS',flush=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--results-dir',type=Path)
    ap.add_argument('--json-out',type=Path)
    ap.add_argument('--npz-out',type=Path)
    a=ap.parse_args()
    if a.self_test:synth_test()
    if a.results_dir is None:
        require(a.self_test,'MISSING_RESULTS_DIR')
        return
    require(a.json_out is not None and a.npz_out is not None,'MISSING_OUTPUTS')
    rd=a.results_dir.resolve();jp=a.json_out.resolve();npzout=a.npz_out.resolve()
    require(not jp.exists() and not npzout.exists(),'REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());require(pre['classification']=='GE19_D45_PREEXEC_ORIGINAL_ACTION_OFFCLOCK_HOMOGENEOUS_H1_AND_SOURCE_INTERPOLATION_DIAGNOSTIC','WRONG_PREREG')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    require(branch==pre['branch'] and branch!='main','WRONG_BRANCH')
    for name,dig in pre['original_parent_results_sha256'].items():
        require((rd/name).is_file() and sha(rd/name)==dig,'FROZEN_PARENT_HASH_MISMATCH_'+name)
    d44=rd/'ge19_d44_readonly_archive/ge19_d44_full_cohort_complex_clock_error_budget.json'
    require(d44.is_file() and sha(d44)==pre['original_d44_archive_report_sha256'],'FROZEN_D44_HASH_MISMATCH')
    j44=json.loads(d44.read_text());require(j44['classification']=='GE19_D44_FROZEN_D43_COMPLEX_CLOCK_RESIDUAL_DESCRIPTIVE_AUDIT_COMPLETE_PARENTS_UNCERTIFIED','WRONG_D44_PARENT')
    from ge19 import h4f3d41_full_window_two_constraint_audit as d41
    frozen,*_=d41.check_inputs(rd,json.loads(d41.PRE.read_text()),json.loads(d41.LOCK.read_text()))
    require(Path(frozen['D22A_NPZ']).is_file(),'MISSING_D22A')
    print('GE19_D45_ALL_ORIGINAL_D41_D43_D44_AND_D33_PARENT_SHA_SCOPE_LOCK_PASS',flush=True)
    d25=d41.d25; r7=d25.d20.source.old.r7
    with np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False) as z13,\
         np.load(rd/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz',allow_pickle=False) as z33,\
         np.load(rd/'ge19_h4f3d43_full_40_mode_n2_n4_lapse.npz',allow_pickle=False) as z43:
        bgs,_,_,_,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        require(x.shape==(128,) and np.all(np.diff(x)>0) and np.array_equal(x,z43['clock_node_x']),'ORIGINAL_CLOCK_MISMATCH')
        require(np.array_equal(z43['diagnostic_modes'],np.arange(1,41)) and np.array_equal(z43['betas'],[1.,.5,.1]),'D43_COHORT_CHANGED')
        require(j44['numerical']['new_propagated_endpoints']==30480 and not j44['H1_on_shell_verified'],'D44_SCOPE_CHANGED')
        charge_per_knot=np.exp(3*x)*np.asarray(bg['KQ_action'],float)
        charge=float(np.median(charge_per_knot));lam=np.asarray(bg['rho_lambda_action'],float)
        require(charge_per_knot.shape==lam.shape==x.shape and np.isfinite(charge_per_knot).all() and np.isfinite(lam).all(),'BACKGROUND_MISSING_OR_NONFINITE')
        lam_const=float(np.median(lam));k2=float(r7.K2);q0=float(r7.Q0);z0=float(r7.Z0);c=float(r7.C_VALUES[tag])
        mid=(x[:-1]+x[1:])/2
        frozen_exact=friedmann_from_charge(x,charge,lam_const,c,k2,q0,z0)
        mid_exact=friedmann_from_charge(mid,charge,lam_const,c,k2,q0,z0)
        # Original action's actual off-clock implementation, not PCHIP replacement.
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            require(active['ctx'] is not None,'ACTION_CONTEXT_NOT_READY')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            at_knots=[ctx(bg,float(t)) for t in x]
            at_mid=[ctx(bg,float(t)) for t in mid]
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
        def get(points,key):
            return np.asarray([float(point[key]) for point in points],float)
        origk_h=get(at_knots,'H');origm_h=get(at_mid,'H')
        origk_q=get(at_knots,'Q_action');origm_q=get(at_mid,'Q_action')
        origk_z=get(at_knots,'Z_action');origm_z=get(at_mid,'Z_action')
        require(all(np.isfinite(y).all() for y in (origk_h,origm_h,origk_q,origm_q,origk_z,origm_z)),'NONFINITE_ORIGINAL_ACTION_BACKGROUND')
        # Report-only analytic H1 homogeneous scalar-charge/Friedmann comparisons.
        derived_mid_kq=exp_branch_kq(origm_z,k2,z0)
        derived_mid_k=stable_exp_k(origm_z,k2,z0)
        h2_mid_from_action=(origm_q*derived_mid_kq-derived_mid_k)/3+c/np.exp(3*mid)+lam_const
        h2_mid_scale=np.maximum.reduce((np.abs(origm_h**2),np.abs(h2_mid_from_action),np.full_like(mid,TINY)))
        h2_mid_fried_rel=np.abs(origm_h**2-h2_mid_from_action)/h2_mid_scale
        charge_mid_rel=np.abs(np.exp(3*mid)*derived_mid_kq-charge)/max(abs(charge),TINY)
        pchip_H=PchipInterpolator(x,np.asarray(bg['H'],float),extrapolate=False)(mid)
        main=np.stack([np.asarray(z33[f'beta{i}_candidate_C_main_six_by_128_by_41'],complex) for i in range(3)],axis=-1)
        con=np.stack([np.asarray(z33[f'beta{i}_candidate_C_constraint_two_by_128_by_41'],complex) for i in range(3)],axis=-1)
        require(main.shape==(6,128,41,3) and con.shape==(2,128,41,3) and np.any(main[:,:,0]) and np.any(main[3,:,14,:]) and np.array_equal(con[:,:,26,:],np.zeros((2,128,3),complex)),'D33_SOURCE_PROVENANCE_CHANGED')
        mid2,src_pc,src_lin,knot_replay=source_at_midpoints(x,main,con)
        require(np.array_equal(mid,mid2),'MIDPOINT_GRID_CHANGED')
        sources={float(b):{'rhs':main[:,:,:,i],'rhs_constraint':con[:,:,:,i]} for i,b in enumerate([1.,.5,.1])}
        reference_replay=[]
        for m in range(41):
            rf,cf=r7._source_interp(x,sources,int(m))
            for i in [0,114,126]:
                val=np.concatenate((np.asarray(rf(float(mid[i])),complex),np.asarray(cf(float(mid[i])),complex)))
                tar=src_pc[:,i,m,:]
                reference_replay.append(rel_l2(val,tar))
        require(max(reference_replay)<3e-12,'ORIGINAL_PCHIP_IMPLEMENTATION_REPLAY_MISMATCH')
        dif=src_pc-src_lin
        src_rel=np.linalg.norm(dif,axis=0)/np.maximum.reduce((np.linalg.norm(src_pc,axis=0),np.linalg.norm(src_lin,axis=0),np.full((127,41,3),TINY)))
        src_abs=np.linalg.norm(dif,axis=0)
        off=np.array([1,4,9,14,19,21,22,24,26,27,29,31,32,33,34,36,37,38,39])-1
        smooth=np.array([m-1 for m in range(1,41) if m-1 not in set(off)])
        def sector(which,ix):
            w=src_rel[ix,which,:];a=src_abs[ix,which,:]
            return dict(max_normed_PCHIP_vs_linear=float(np.max(w)),median_normed_PCHIP_vs_linear=float(np.median(w)),
                        max_absolute_PCHIP_vs_linear=float(np.max(a)))
        report=dict(classification='GE19_D45_OFFCLOCK_HOMOGENEOUS_BACKGROUND_AND_SOURCE_INTERPOLATION_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
            preregistration=pre['classification'],source_sha256=sha(__file__),
            scope='Read-only original Cstar action homogeneous H1 background at 128 knots + 127 midpoints; independent scalar-charge/Friedmann branch reconstruction; original D33 full 41-mode beta-specific PCHIP source versus linear off-knot comparator. No dynamic first-order H1 EOM or true continuous original source oracle; no new evolution/projection/tuning.',
            original_action_modified=False,production_H3F_source_modified=False,original_gate_unchanged=True,
            D22A_original_science_FAIL_immutable=True,D34_D34R1_original_m26_boundary_FAIL_immutable=True,D35_m26_posthoc_momentum_not_original_bitwise=True,
            original_D41_D42R2_D43_D44_remain_frozen=True,homogeneous_H1_full_EOM_certified=False,H1_on_shell_verified=False,Noether_ward_verified=False,H3_full_window_certified=False,Z11_certified=False,Z20_certified=False,Z21_certified=False,lensing_licensed=False,
            originals_sha256={name:pre['original_parent_results_sha256'][name] for name in sorted(pre['original_parent_results_sha256'])},original_D44_report_sha256=pre['original_d44_archive_report_sha256'],original_repair13_npz_sha256=sha(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz'),
            homogeneous_background=dict(clock_nodes=128,midpoint_count=127,charge_constant_median=charge,
                 max_clock_scalar_charge_relative_deviation=float(np.max(np.abs(charge_per_knot-charge)/max(abs(charge),TINY))),
                 max_lambda_knot_absolute_deviation=float(np.max(np.abs(lam-lam_const))),
                 original_action_knot_H_vs_frozen_background_rel_l2=rel_l2(origk_h,bg['H']),
                 analytic_charge_knot_H_vs_frozen_H_rel_l2=rel_l2(frozen_exact['h'],bg['H']),
                 analytic_charge_knot_Q_vs_frozen_Q_rel_l2=rel_l2(frozen_exact['q'],bg['Q_action']),
                 analytic_charge_knot_Z_vs_frozen_Z_rel_l2=rel_l2(frozen_exact['z'],bg['Z_action']),
                 original_action_mid_H_vs_analytic_charge_H_rel_l2=rel_l2(origm_h,mid_exact['h']),
                 original_action_mid_Q_vs_analytic_charge_Q_rel_l2=rel_l2(origm_q,mid_exact['q']),
                 original_action_mid_Z_vs_analytic_charge_Z_rel_l2=rel_l2(origm_z,mid_exact['z']),
                 original_action_mid_H_vs_PCHIP_frozen_H_rel_l2=rel_l2(origm_h,pchip_H),
                 max_original_action_mid_Friedmann_component_relative_report_only=float(np.max(h2_mid_fried_rel)),
                 max_original_action_mid_charge_relative_report_only=float(np.max(charge_mid_rel))),
            source_interpolation=dict(source_modes=41,reduced_modes=40,beta_count=3,source_rows=8,intervals=127,
                 original_PCHIP_knot_replay_rel_l2=knot_replay,
                 original_PCHIP_implementation_max_offknot_relative_replay=float(max(reference_replay)),
                 PCHIP_vs_linear_midpoint_max_normed=float(np.max(src_rel)),PCHIP_vs_linear_midpoint_median_normed=float(np.median(src_rel)),
                 x0_x1_offsupport_sector=sector(off,0),x114_x115_smooth_support_sector=sector(smooth,114),
                 interpretation='PCHIP-versus-linear is ONLY interpolation choice sensitivity; neither is an independent true continuous original H3 source.'),
            claim_boundary='Neither homogeneous analytic branch agreement nor source-interpolation spread proves full first-order H1 on-shell, full H3/Ward, bitwise Repair18 initial data, Z11/Z20/Z21 or lensing. No observation is opened or fitted.',
            next_step='Use original GE06/GE07/Lambda full H1 first-order EOM at off-clock nodes and independently recomputed continuous D33 source to attribute remaining lapse floor; do not retune or use DES for theory selection.')
        jp.parent.mkdir(parents=True,exist_ok=True);npzout.parent.mkdir(parents=True,exist_ok=True)
        np.savez_compressed(npzout,clock_node_x=x,interval_mid_x=mid,
            analytic_charge_H_mid=mid_exact['h'],original_action_H_mid=origm_h,
            original_action_Q_mid=origm_q,analytic_charge_Q_mid=mid_exact['q'],
            original_action_Z_mid=origm_z,analytic_charge_Z_mid=mid_exact['z'],
            original_action_mid_H_Friedmann_component_rel=h2_mid_fried_rel,
            original_action_mid_scalar_charge_rel=charge_mid_rel,
            source_PCHIP_mid=src_pc,source_linear_mid=src_lin,
            source_PCHIP_linear_normed_mid_by_interval_mode_beta=src_rel,
            source_PCHIP_linear_abs_mid_by_interval_mode_beta=src_abs)
        jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
        print('GE19_D45_HOMOGENEOUS_H1_ORIGINAL_ACTION_OFFCLOCK_AND_ANALYTIC_CHARGE_DIAGNOSTIC_WRITTEN',flush=True)
        print('GE19_D45_ORIGINAL_PCHIP_FULL_41_MODE_SOURCE_AND_LINEAR_SENSITIVITY_WRITTEN',flush=True)
        print('GE19_D45_H1_FULL_ONSHELL_OPEN_SOURCE_TRUE_OFFCLOCK_OPEN_NO_Z21_NO_LENSING',flush=True)
        print('GE19_D45_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':main()
