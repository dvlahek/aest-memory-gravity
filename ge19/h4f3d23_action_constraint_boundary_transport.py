#!/usr/bin/env python3
"""D23: action-compatible initial H2 momentum diagnostic and H3 first-interval transport.

Immutable D22A FAIL and D22R3 R2 equality are inputs, never reclassified.
The R2 dynamic tangent is an independent comparator, NOT exact reduced-action BC.
Projected Z11 is a numerical diagnostic only, and Z20 is not reintegrated.
"""
from __future__ import annotations
import argparse, hashlib, json
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d22a_action_parent_reclosure as d22
from ge19 import h4f3d20r1_recompute_five_sources_and_bath_ward as d20
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17driver
from ge19 import h4f3d17_original_action_dense_H1_core as d17core
from ge19 import repair18_zero_coordinate_constraint_projected_momentum_boundary as r18

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d23_predata_action_constraint_boundary_transport.json'
TINY=1e-300

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def rel(a,b):
    a=np.asarray(a);b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))

def zpair(v):return [float(np.real(v)),float(np.imag(v))]

def row_data(r7,C,w,src):
    out={}
    for key,row,target in (
        ('lapse',C[4],src[0]),
        ('shift',C[10]+C[11],src[6]),
        ('anisotropy',C[12]+C[13],src[7]),
    ):
        v=r7._constraint_backward_error(row,w,target)
        out[key]={q:float(v[q]) for q in ('metric','absolute_residual','scale','contribution_scale')}
    return out

def project_p(r7,mod6,mod7,bg,tag,k,x0,q0,v0,src8):
    """Reproduce the R2 canonical datum, then project lapse+shift in p only.

    Explicit q0 offset matters: Repair18's zero-q projector cannot be used
    unchanged for a nonzero R2 eta tangent. Never modify the frozen R2 datum.
    """
    q0=np.asarray(q0,complex);v0=np.asarray(v0,complex);src8=np.asarray(src8,complex)
    if q0.shape!=(4,) or v0.shape!=(4,) or src8.shape!=(8,):
        raise ValueError('D23 q,v,source shapes')
    yold,wold,idiag=r7._initial_canonical_state(
        mod6,mod7,bg,tag,k,float(x0),q0,v0,src8[:6])
    _,_,_,_,WY,WR,C,bp,_=r7._canonical_operator_matrices(
        mod6,mod7,bg,tag,k,float(x0))
    if not np.array_equal(yold[:4],q0):
        raise RuntimeError('frozen R2 canonical q boundary not reproduced')
    base=np.r_[q0,np.zeros(4,complex)]
    offset=WY@base+WR@src8
    lapse=C[4];shift=C[10]+C[11]
    A=np.stack([lapse@WY[:,4:8],shift@WY[:,4:8]])
    b=np.asarray([src8[0]-lapse@offset,src8[6]-shift@offset],complex)
    pold=yold[4:8]
    # Frozen Repair18 algorithm, now used on the exact *delta* from R2.
    dp,diag=r18.projected_momentum_solve(A,b-A@pold)
    ynew=yold.copy();ynew[4:8]+=dp
    wnew=WY@ynew+WR@src8
    residual=A@ynew[4:8]-b
    oldrows=row_data(r7,C,wold,src8)
    newrows=row_data(r7,C,wnew,src8)
    vnew=wnew[6:10]
    source_l2=max(float(np.linalg.norm(b)),TINY)
    output={
        'projection_rank':int(diag['rank']),
        'projection_augmented_rank':int(diag['augmented_rank']),
        'projection_scaled_relative_residual':float(diag['scaled_relative_residual_final']),
        'constraint_equations_residual_over_rhs':float(np.linalg.norm(residual)/source_l2),
        'initial_R2_dot_relative_change':rel(vnew,v0),
        'initial_R2_dot_absolute_L2_change':float(np.linalg.norm(vnew-v0)),
        'initial_R2_dot_absolute_max_change':float(np.max(np.abs(vnew-v0))),
        'canonical_R2_momentum_relative_change':rel(ynew[4:8],pold),
        'canonical_R2_momentum_absolute_L2_change':float(np.linalg.norm(dp)),
        'old_initial_rows':oldrows,'projected_initial_rows':newrows,
        'frozen_R2_reference_not_modified':True,
    }
    return ynew,output,vnew

def h3_shift_transport(r7,mod6,mod7,bg,tag,mode,beta_idx,x,sources,p0,arch_st,arch_dot):
    """Exact action operator plus archived H3F PCHIP source: g_x at x0.

    Constraint g(x)=C_shift(x)[WY(x)y+WR(x)S(x)]-S_shift(x).
    Differentiation is of the canonical operator/source; not an FD4 bath jet.
    g_x is a diagnostic necessary transport test, not a full Noether proof.
    """
    k=float(mode*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    rhsfun,confun=r7._source_interp(x,sources,int(mode))
    ib=int(beta_idx);i=int(mode-1)
    y0=np.r_[np.zeros(4,complex),np.asarray(p0[ib,i],complex)]
    def src(xx):
        main=np.asarray(rhsfun(float(xx)),complex)
        con=np.asarray(confun(float(xx)),complex)
        return np.r_[main[:,ib],con[:,ib]]
    def maps(xx):
        M,F,_,_,WY,WR,C,_,_=r7._canonical_operator_matrices(
            mod6,mod7,bg,tag,k,float(xx))
        row=C[10]+C[11]
        gs=row@WR
        gs[6]-=1.0
        return M,F,row@WY,gs,C,WY,WR
    x0=float(x[0]);dx=float(x[1]-x[0]);x1=float(x[1]);
    M,F,gy,gs,C,WY,WR=maps(x0)
    s0=src(x0);ydot=M@y0+F@s0
    g0=gy@y0+gs@s0
    eps=dx/1024.0
    def gd(e):
        _,_,gym,gsm,_,_,_=maps(x0+e)
        # Includes explicit derivative of the *actual frozen source interpolation*.
        return ((gym-gy)@y0+(gsm@src(x0+e)-gs@s0))/e+gy@ydot
    gprime=gd(eps);gprime_half=gd(eps/2)
    _,_,gy1,gs1,C1,WY1,WR1=maps(x1)
    state=np.asarray(arch_st[ib,i],complex);dots=np.asarray(arch_dot[ib,i],complex)
    w1=np.r_[state[[0,5],1],state[[1,2,3,4],1],dots[:,1]]
    s1=src(x1)
    # Independent direct archived-state shift residual, not an H3 re-solve.
    g1=(C1[10]+C1[11])@w1-s1[6]
    g1_can=gy1@np.r_[state[[1,2,3,4],1],C1[0:4]@w1]+gs1@s1
    # Test reconstructed canonical row consistency to detect an indexing bug.
    archive_consistency=float(abs(g1-g1_can)/max(abs(g1),abs(g1_can),TINY))
    deriv_stability=float(abs(gprime-gprime_half)/max(abs(gprime),abs(gprime_half),TINY))
    rows0=row_data(r7,C,WY@y0+WR@s0,s0)
    rows1=row_data(r7,C1,w1,s1)
    out={
        'beta':float(r7.BETAS[ib]),'mode':int(mode),
        'x0':x0,'x1':x1,'dx':dx,
        'source_shift_x0':zpair(s0[6]),'source_shift_x1':zpair(s1[6]),
        'g0_complex':zpair(g0),'g1_archived_complex':zpair(g1),
        'gprime0_complex':zpair(gprime),
        'linear_first_step_prediction_complex':zpair(dx*gprime),
        'gprime_step_halving_relative_report_only':deriv_stability,
        'first_step_archived_vs_canonical_reconstruction_relative':archive_consistency,
        'first_step_absolute_shift_defect':float(abs(g1)),
        'first_step_shift_backward':rows1['shift']['metric'],
        'initial_shift_backward':rows0['shift']['metric'],
        'initial_lapse_backward':rows0['lapse']['metric'],
        'first_step_projection_predictor_report_only':float(abs(dx*gprime)/max(abs(g1),TINY)),
        'no_H3_reintegration':True,
    }
    return out

def main():
    ap=argparse.ArgumentParser()
    for key in ('results-dir','repair26-trace','json-out','npz-out'):
        ap.add_argument('--'+key,required=True)
    args=ap.parse_args();rd=Path(args.results_dir).resolve()
    trace=Path(args.repair26_trace).resolve();oj=Path(args.json_out).resolve();on=Path(args.npz_out).resolve()
    if oj.exists() or on.exists():raise RuntimeError('D23 no overwrite')
    pre=json.loads(PRE.read_text())
    if pre.get('classification')!='GE19_D23_PREDATA_ACTION_CONSTRAINT_BOUNDARY_AND_H3_TRANSPORT_DIAGNOSTIC':
        raise RuntimeError('D23 preregistration changed')
    for key,(name,want) in pre['archived_files'].items():
        p=rd/name
        if not p.is_file() or sha(p)!=want:raise RuntimeError(f'D23 original parent mismatch {key}')
    files,inputs,locks=d22.verify(rd,trace,json.loads(d22.PRE.read_text()))
    report22=json.loads((rd/pre['archived_files']['D22A_JSON'][0]).read_text())
    report3=json.loads((rd/pre['archived_files']['D22R3_JSON'][0]).read_text())
    if report22['classification']!='GE19_D22A_CSTAR_PARENT_NUMERICAL_CANDIDATE_FAIL_Q20_AND_FULL_H4_OPEN':
        raise RuntimeError('D23 D22A SCIENCE FAIL mutated')
    if report3['classification']!='GE19_D22R3_FRESH_R2_BOUNDARY_EQUIVALENT_D22A_FAIL_RETAINS':
        raise RuntimeError('D23 R2 provenance changed')
    if report3['source_hashes']['R28']!='101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705':
        raise RuntimeError('D23 original R2 SHA changed')
    print('GE19_D23_ALL_D17_D19_D22A_D22R3_PARENT_SHA_AND_R2_GENUINE_PASS',flush=True)
    old=d20.source.old;r7=old.r7
    states=np.full((len(r7.FOURIER_N),6,128),np.nan+0j,complex)
    dots=np.full((len(r7.FOURIER_N),4,128),np.nan+0j,complex)
    out={};solved=[]
    with ExitStack() as stack:
        r13=stack.enter_context(np.load(inputs['r13'],allow_pickle=False))
        archive=stack.enter_context(np.load(rd/pre['archived_files']['D22A_NPZ'][0],allow_pickle=False))
        r3=stack.enter_context(np.load(rd/pre['archived_files']['D22R3_NPZ'][0],allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,r13)
        tag='C_star';bg=bgs[(128,tag)];x=np.asarray(bg['x'],float)
        if x.size!=128 or not (np.array_equal(x,archive['x_primary']) and
            np.array_equal(x,r3['x_primary'])):
            raise RuntimeError('D23 exact action knot mismatch')
        ref=np.asarray(r3['fresh_R2_reference_primary'],complex)
        refdot=np.asarray(r3['fresh_R2_dot_primary'],complex)
        rhs=np.asarray(archive['GE05_M1_rhs_for_Z11_primary'],complex)
        if ref.shape!=(6,6,128) or refdot.shape!=(6,4,128) or rhs.shape!=(6,6,128):
            raise RuntimeError('D23 true R2/M1 dimensions mismatch')
        if not (np.array_equal(rhs,r3['new_GE05_M1_rhs_primary']) and
            np.all(np.isfinite(ref)) and np.all(np.isfinite(refdot))):
            raise RuntimeError('D23 archived true R2/source mismatch')
        sources={beta:{'rhs':np.asarray(archive[f'beta{ib}_H3F_D17_source_rows'],complex),
                        'rhs_constraint':np.asarray(archive[f'beta{ib}_H3F_D17_source_constraints'],complex)}
                  for ib,beta in enumerate(r7.BETAS)}
        z20=np.asarray(archive['Z20_D17_H3F_candidate_primary'],complex)
        d20z=np.asarray(archive['Z20dot_D17_H3F_candidate_primary'],complex)
        z20p=np.asarray(archive['Z20_source_aware_projected_p0_primary'],complex)
        if z20.shape!=(3,40,6,128) or d20z.shape!=(3,40,4,128) or z20p.shape!=(3,40,4):
            raise RuntimeError('D23 D22A H3 sources or archived trajectories changed')
        orig_point=r7._bg_point;orig_cache=r7._CANONICAL_LOCAL_CACHE
        try:
            ev,_=d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d17core.ActionBackground(r7,bg,ev);ctx.knot_check()
            r7._bg_point=lambda b,t:ctx(b,t)
            r7._CANONICAL_LOCAL_CACHE={}
            print('GE19_D23_H2_ACTION_COMPATIBLE_R2_MOMENTUM_PROJECTION_BEGIN',flush=True)
            projected=[];yinit=[]
            for im,m in enumerate(r7.FOURIER_N):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                s0=np.r_[rhs[im,:,0],np.zeros(2,complex)]
                q0=ref[im,[1,2,3,4],0]
                v0=refdot[im,:,0]
                yi,row,vnew=project_p(r7,mod6,mod7,bg,tag,k,float(x[0]),q0,v0,s0)
                row['mode']=int(m);projected.append(row);yinit.append(yi)
                print('GE19_D23_PROJECTED_H2_MODE',int(m),
                    'old_shift=%.3e'%row['old_initial_rows']['shift']['metric'],
                    'new_shift=%.3e'%row['projected_initial_rows']['shift']['metric'],
                    'R2_dot_delta=%.3e'%row['initial_R2_dot_relative_change'],flush=True)
            # Preserve the pre-existing local 1e-6 gate. Projection is only
            # diagnostic if R2 correction is not covered by independent errors.
            pcheck=all(row['projection_rank']==2 and row['projection_augmented_rank']==2 and
                       max(row['projected_initial_rows'][name]['metric']
                           for name in ('lapse','shift','anisotropy'))<=1e-6
                       for row in projected)
            if pcheck:
                print('GE19_D23_H2_SIX_MODE_PROJECTED_CANDIDATE_BEGIN',flush=True)
                for im,m in enumerate(r7.FOURIER_N):
                    k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                    rhsfun,confun=d22.h2.source_interp(x,rhs[im])
                    Y,di=r7._radau2_integrate_canonical(mod6,mod7,bg,tag,k,yinit[im][:,None],rhsfun,confun)
                    st,dt,od=r7._reconstruct_canonical_solution(mod6,mod7,bg,tag,k,Y,rhsfun,confun)
                    states[im]=st[0];dots[im]=dt[0]
                    solved.append({'mode':int(m),
                        'radau_relative':float(di['radau_block_scaled_relative_L2_residual_max']),
                        'algebraic_relative':float(od['algebraic_scaled_relative_L2_residual_max']),
                        'lapse_relative':float(od['lapse_noether_row_relative_residual_max']),
                        'shift_local_max':float(od['shift_constraint_relative_L2_max']),
                        'anisotropy_local_max':float(od['anisotropy_constraint_relative_L2_max']),
                        'finite':bool(od['all_outputs_finite'])})
                    print('GE19_D23_H2_PROJECTED_SOLVED',int(m),
                        'shift=%.3e'%solved[-1]['shift_local_max'],flush=True)
            else:
                print('GE19_D23_PROJECTED_INITIAL_CONSTRAINT_NOT_CLOSED_NO_H2_REINTEGRATION',flush=True)
            print('GE19_D23_H3_FIRST_INTERVAL_SHIFT_TRANSPORT_BEGIN',flush=True)
            # Worst archived early failure plus two independently selected mode controls.
            selections=[(14,2),(1,0),(40,2)]
            h3=[]
            for mode,ib in selections:
                item=h3_shift_transport(r7,mod6,mod7,bg,tag,mode,ib,x,sources,z20p,z20,d20z)
                h3.append(item)
                print('GE19_D23_H3_TRANSPORT',mode,'beta',item['beta'],
                    'gprime=%.3e'%abs(complex(*item['gprime0_complex'])),
                    'g1=%.3e'%item['first_step_absolute_shift_defect'],flush=True)
            forensic=json.loads((rd/pre['archived_files']['D22AR2_JSON'][0]).read_text())
            worst=forensic['original_action_new_Z20']['worst_relative']
            if not (int(worst['mode'])==14 and abs(float(worst['beta'])-h3[0]['beta'])<1e-14
                and int(worst['t_index'])==1 and
                abs(h3[0]['first_step_shift_backward']-float(worst['relative_backward']))<1e-9):
                raise RuntimeError('D23 H3 selected first-step residual fails independent D22AR2 replay')
            if not all(np.isfinite(t['gprime_step_halving_relative_report_only']) and
                       np.isfinite(t['first_step_shift_backward']) for t in h3):
                raise RuntimeError('D23 nonfinite first-interval diagnostic')
            print('GE19_D23_H3_WORST_FIRST_STEP_INDEPENDENT_FORENSIC_REPLAY_PASS',flush=True)
        finally:
            r7._bg_point=orig_point;r7._CANONICAL_LOCAL_CACHE=orig_cache
        out={'x_primary':x,'R2_fresh_reference_primary':ref,'R2_fresh_dot_primary':refdot,
             'new_M1_rhs_primary':rhs,
             'projected_H2_y0':np.asarray(yinit,complex),
             'projected_H2_Z11_diagnostic_primary':states,
             'projected_H2_Z11dot_diagnostic_primary':dots}
        classification=('GE19_D23_PROJECTED_H2_NUMERICAL_DIAGNOSTIC_AND_H3_TRANSPORT_COMPLETE_PARENTS_UNCERTIFIED'
                       if pcheck else 'GE19_D23_INITIAL_PROJECTION_NOT_CLOSED_H3_TRANSPORT_DIAGNOSTIC_ONLY')
        report={
          'classification':classification,'preregistration':pre['classification'],
          'D22A_SCIENCE_FAIL_immutable':True,'D22R3_equivalent_R2_immutable':True,
          'fresh_R2_momentum_projection':projected,
          'initial_projected_shift_lapse_anisotropy_frozen_1e6_pass':bool(pcheck),
          'R2_independent_error_budget_for_projected_dot_certified':False,
          'projected_six_mode_Z11_solve_performed':bool(pcheck),
          'projected_six_mode_Z11_diagnostics':solved,
          'H3_first_interval_constraint_transport':h3,
          'H3_source_from_immutable_D22A_Nx1024':True,
          'H3_40_modes_not_recomputed':True,
          'q20_B20_recomputed':False,'Z11_certified':False,'Z20_certified':False,
          'full_H4_Ward_certified':False,'Z21_certified':False,'lensing_licensed':False,
          'original_GE05_all_interval_certified':False,'no_observational_tuning':True,
          'sha256_inputs':{k:sha(rd/v[0]) for k,v in pre['archived_files'].items()},
          'claim_boundary':'D23 projects only R2 canonical momentum against original-action initial lapse+shift; every R2 deviation is reported, no R2 uncertainty enclosure or parent certification. H2 projected six-mode trajectory is diagnostic. H3 derivative uses archived original H3F source and canonical original-action operator on first interval, without H3 rerun. Failed D22A remains immutable. No q20, H4/Z21 or lensing.'
        }
        oj.parent.mkdir(parents=True,exist_ok=True)
        np.savez_compressed(on,**out)
        oj.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
        print('GE19_D23_CLASSIFICATION',classification,flush=True)

if __name__=='__main__':main()
