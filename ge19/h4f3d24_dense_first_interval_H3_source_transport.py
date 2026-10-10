#!/usr/bin/env python3
"""D24: original-action D17 dense-H1 / H3 first-interval source resolution.

Only the first 9 D17 sub4 knots and three preselected (m,beta) controls.
Never reclassifies the original D22A FAIL or certifies H3, q20, H4, Z21.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
from ge19 import h4f3d22a_action_parent_reclosure as d22
from ge19 import h4f3d23_action_constraint_boundary_transport as d23
from ge19 import h4f3d20r1_recompute_five_sources_and_bath_ward as d20
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17driver
from ge19 import h4f3d17_original_action_dense_H1_core as d17core
from ge19 import repair18_zero_coordinate_constraint_projected_momentum_boundary as r18
from ge19 import h3f_corrected_y_source_adapter as h3f
from ge19 import repair14_self_consistent_reduced_h3_z20_particular as r14

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d24_predata_dense_first_interval_H3_source_transport.json'
TINY=1e-300

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def rel(a,b):
    a=np.asarray(a);b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))

def pair(v):return [float(np.real(v)),float(np.imag(v))]

def source_on_grid(r7,grid,src,mode,ib):
    rf,cf=r7._source_interp(grid,src,int(mode))
    def source(t):
        a=np.asarray(rf(float(t)),complex);b=np.asarray(cf(float(t)),complex)
        return np.r_[a[:,ib],b[:,ib]]
    return source

def projected_initial(r7,mod6,mod7,bg,tag,k,x0,src0):
    M,F,ZY,ZR,WY,WR,C,bp,_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,x0)
    lr=C[4];sr=C[10]+C[11]
    offset=WR@src0
    A=np.stack((lr@WY[:,4:8],sr@WY[:,4:8]))
    b=np.array([src0[0]-lr@offset,src0[6]-sr@offset],complex)
    p,diag=r18.projected_momentum_solve(A,b)
    if (diag['rank']!=2 or diag['augmented_rank']!=2 or
        not np.all(np.isfinite(p))):
        raise RuntimeError('D24 original-action projected momentum rank or finite failure')
    y=np.r_[np.zeros(4,complex),p]
    w=WY@y+WR@src0
    init=r7._constraint_backward_error(sr,w,src0[6])['metric']
    return y,float(init),diag

def original_radau_first_step(r7,mod6,mod7,bg,tag,k,x0,x1,y0,source):
    """Exactly the frozen Repair07 two-stage Radau IIA block for ONE step."""
    h=float(x1-x0);a11=5/12;a12=-1/12;a21=3/4;a22=1/4;b1=3/4;b2=1/4
    t1=float(x0+h/3);t2=float(x1)
    M1,F1,*_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,t1)
    M2,F2,*_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,t2)
    s1=source(t1);s2=source(t2);f1=F1@s1;f2=F2@s2
    I=np.eye(8,dtype=complex)
    K=np.block([[I-h*a11*M1,-h*a12*M2],[-h*a21*M1,I-h*a22*M2]])
    RHS=np.r_[y0+h*(a11*f1+a12*f2),y0+h*(a21*f1+a22*f2)]
    stages,diag=r7._dense_equilibrated_solve(K,RHS)
    Y1=stages[:8];Y2=stages[8:]
    g1=M1@Y1+f1;g2=M2@Y2+f2
    yend=y0+h*(b1*g1+b2*g2)
    return yend,float(diag['scaled_relative_L2_residual_max'])

def transport(r7,mod6,mod7,bg,tag,k,x0,x1,y0,y1,source):
    dx=float(x1-x0)
    def maps(t):
        M,F,_,_,WY,WR,C,_,_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,t)
        row=C[10]+C[11];gs=row@WR;gs[6]-=1
        return M,F,row@WY,gs,row,WY,WR
    M,F,gy,gs,row,WY,WR=maps(x0)
    s0=source(x0);ydot=M@y0+F@s0
    g0=gy@y0+gs@s0
    def deriv(e):
        _,_,gy1,gs1,*_=maps(float(x0+e))
        return ((gy1-gy)@y0+(gs1@source(x0+e)-gs@s0))/e+gy@ydot
    eps=dx/1024;gp=deriv(eps);gph=deriv(eps/2)
    _,_,gy1,gs1,row1,WY1,WR1=maps(x1)
    s1=source(x1);w1=WY1@y1+WR1@s1
    g1=gy1@y1+gs1@s1
    backward=r7._constraint_backward_error(row1,w1,s1[6])['metric']
    return dict(g0=pair(g0),gprime=pair(gp),g1=pair(g1),
        first_step_shift_backward=float(backward),
        first_step_abs_defect=float(abs(g1)),
        derivative_halving_relative=rel(np.array([gp]),np.array([gph])),
        first_step_linear_predictor_over_abs_defect=float(abs(dx*gp)/max(abs(g1),TINY)),
        first_step_source_shift_x0=pair(s0[6]),first_step_source_shift_x1=pair(s1[6]))

def main():
    ap=argparse.ArgumentParser()
    for s in ('results-dir','repair26-trace','json-out','npz-out'):
        ap.add_argument('--'+s,required=True)
    a=ap.parse_args();rd=Path(a.results_dir).resolve();trace=Path(a.repair26_trace).resolve()
    oj=Path(a.json_out).resolve();on=Path(a.npz_out).resolve()
    if oj.exists() or on.exists():raise RuntimeError('D24 no overwrite')
    pre=json.loads(PRE.read_text())
    if pre['classification']!='GE19_D24_PREDATA_DENSE_H1_FIRST_INTERVAL_H3_SOURCE_RESOLUTION':
        raise RuntimeError('D24 predata classification changed')
    for key,(name,want) in pre['archives'].items():
        path=rd/name
        if not path.is_file() or sha(path)!=want:raise RuntimeError('D24 immutable archive mismatch: '+key)
    if not trace.is_file() or sha(trace)!=pre['repair26_trace_sha256']:
        raise RuntimeError('D24 Repair26 trace SHA mismatch')
    for filename,want in pre['frozen_git_blobs'].items():
        head=subprocess.check_output(['git','rev-parse','HEAD:'+filename],cwd=ROOT,text=True).strip()
        work=subprocess.check_output(['git','hash-object',str(ROOT/filename)],cwd=ROOT,text=True).strip()
        if head!=want or work!=want:raise RuntimeError('D24 frozen source blob mismatch '+filename)
    with ExitStack() as stack:
        dn=stack.enter_context(np.load(rd/pre['archives']['D17_NPZ'][0],allow_pickle=False))
        oldarch=stack.enter_context(np.load(rd/pre['archives']['D22A_NPZ'][0],allow_pickle=False))
        z13=stack.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        files,inputs,locks=d22.verify(rd,trace,json.loads(d22.PRE.read_text()))
        if pre['archives']['D22A_JSON'][1]!=sha(rd/pre['archives']['D22A_JSON'][0]):
            raise RuntimeError('D24 D22A science FAIL input changed')
        d22j=json.loads((rd/pre['archives']['D22A_JSON'][0]).read_text())
        d23j=json.loads((rd/pre['archives']['D23_JSON'][0]).read_text())
        if (d22j['classification']!='GE19_D22A_CSTAR_PARENT_NUMERICAL_CANDIDATE_FAIL_Q20_AND_FULL_H4_OPEN' or
            d23j['classification']!='GE19_D23_PROJECTED_H2_NUMERICAL_DIAGNOSTIC_AND_H3_TRANSPORT_COMPLETE_PARENTS_UNCERTIFIED'):
            raise RuntimeError('D24 frozen failure/diagnostic classification changed')
        old=d20.source.old;r7=old.r7
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';xc=np.asarray(bg['x'],float)
        xf=np.asarray(dn['primary_C_star_x_dense_sub4'],float)
        Y=np.asarray(dn['primary_C_star_H1_canonical_y_dense_sub4'],complex)
        if not (np.array_equal(xc,xf[::4]) and Y.shape==(6,8,509) and len(xf)>=9 and
            np.array_equal(xc,np.asarray(oldarch['x_primary'],float))):
            raise RuntimeError('D24 original D17 dense/archived time representation changed')
        original_bgpoint=r7._bg_point;original_cache=r7._CANONICAL_LOCAL_CACHE
        try:
            ev,_=d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d17core.ActionBackground(r7,bg,ev);ctx.knot_check()
            r7._bg_point=lambda b,t:ctx(b,t)
            r7._CANONICAL_LOCAL_CACHE={}
            shortx=xf[:9];states=np.empty((6,6,9),complex);dots=np.empty((6,4,9),complex)
            for im,m in enumerate(r7.FOURIER_N):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                for j,t in enumerate(shortx):
                    _,_,_,_,WY,WR,C,bp,_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,float(t))
                    w=WY@Y[im,:,j]
                    states[im,:,j]=w[[0,2,3,4,5,1]]
                    dots[im,:,j]=w[[6,7,8,9]]
                print('GE19_D24_D17_DENSE_H1_MODE',int(m),'6',flush=True)
            savedH=np.asarray(oldarch['D17_H1_action_primary'],complex)
            savedD=np.asarray(oldarch['D17_H1dot_action_primary'],complex)
            xreplay=max(rel(states[:,:,::4],savedH[:,:,:3]),rel(dots[:,:,::4],savedD[:,:,:3]))
            Xdense=old.r24.first_order_X_modes(r7,{
                **bg,'x':shortx,'a':np.exp(shortx),
                'Q_action':np.asarray([ctx(bg,float(v))['Q_action'] for v in shortx])
            },states)
            Xarch=np.asarray(dn['primary_C_star_X10_original_action_dense_sub4'],complex)[:,:9]
            xerr=rel(Xdense,Xarch)
            if max(xerr,xreplay)>1e-9:
                raise RuntimeError('D24 dense original action H1 source projection mismatch')
            shortbg=dict(bg)
            shortbg['x']=shortx.copy()
            for key in ('a','H','Q_action','Z_action'):
                shortbg[key]=np.asarray([ctx(bg,float(v))[key] for v in shortx],float)
            rho=np.asarray(bg['rho_lambda_action'],float)
            shortbg['rho_lambda_action']=np.asarray(PchipInterpolator(xc,rho,extrapolate=False)(shortx),float)
            # All other background fields remain frozen. The H3F source
            # below reads only the explicitly replaced time-dependent keys.
            print('GE19_D24_NINE_DENSE_KNOTS_H3F_SOURCE_BEGIN',flush=True)
            sources=h3f.source_bundle_reduced_lambda(
                r7,r14,mod6,mod7,shortbg,shortbg['rho_lambda_action'],
                tag,1024,states,dots)
            archived={b:{'rhs':np.asarray(oldarch[f'beta{ib}_H3F_D17_source_rows'],complex),
                         'rhs_constraint':np.asarray(oldarch[f'beta{ib}_H3F_D17_source_constraints'],complex)}
                      for ib,b in enumerate(r7.BETAS)}
            sourcegrid=max(rel(sources[b]['rhs'][:,[0,4,8],:41],archived[b]['rhs'][:,0:3,:41])
                           for b in r7.BETAS)
            sourcecons=max(rel(sources[b]['rhs_constraint'][:,[0,4,8],:41],
                               archived[b]['rhs_constraint'][:,0:3,:41]) for b in r7.BETAS)
            print('GE19_D24_DENSE_VS_COARSE_FIRST_THREE_SOURCE_KNOTS',
                'main=%.3e'%sourcegrid,'con=%.3e'%sourcecons,flush=True)
            result=[];npz={'x_original_first_interval_dense_sub4':shortx,
                         'D17_H1_first_nine_dense':states,
                         'D17_H1dot_first_nine_dense':dots}
            for m,ib in [(14,2),(1,0),(40,2)]:
                beta=r7.BETAS[ib];k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0]);i=m-1
                new_src=source_on_grid(r7,shortx,sources,m,ib)
                old_src=source_on_grid(r7,xc,archived,m,ib)
                ynew,init,initdiag=projected_initial(r7,mod6,mod7,bg,tag,k,float(xc[0]),new_src(xc[0]))
                yold=np.r_[np.zeros(4,complex),oldarch['Z20_source_aware_projected_p0_primary'][ib,i]]
                old1,oldrad=original_radau_first_step(r7,mod6,mod7,bg,tag,k,float(xc[0]),float(xc[1]),yold,old_src)
                new1,newrad=original_radau_first_step(r7,mod6,mod7,bg,tag,k,float(xc[0]),float(xc[1]),ynew,new_src)
                original=transport(r7,mod6,mod7,bg,tag,k,float(xc[0]),float(xc[1]),yold,old1,old_src)
                dense=transport(r7,mod6,mod7,bg,tag,k,float(xc[0]),float(xc[1]),ynew,new1,new_src)
                baseline=next(q for q in d23j['H3_first_interval_constraint_transport']
                              if q['mode']==m and q['beta']==float(beta))
                baseline_diff=float(abs(original['first_step_abs_defect']-baseline['first_step_absolute_shift_defect'])/
                                    max(original['first_step_abs_defect'],baseline['first_step_absolute_shift_defect'],TINY))
                if baseline_diff>1e-5:
                    raise RuntimeError('D24 archived first-step exact Radau reproduction failed')
                result.append(dict(mode=m,beta=float(beta),original=original,dense=dense,
                    exact_frozen_first_step_replay_relative=baseline_diff,
                    original_Radau_block_backward=oldrad,dense_Radau_block_backward=newrad,
                    dense_projected_initial_shift=init,
                    source_main_knot_relative=rel(sources[beta]['rhs'][:,[0,4],m],archived[beta]['rhs'][:,:2,m]),
                    source_constraint_knot_relative=rel(sources[beta]['rhs_constraint'][:,[0,4],m],
                                                       archived[beta]['rhs_constraint'][:,:2,m])))
                npz[f'm{m}_beta{ib}_dense_first_step_canonical_y']=new1
                print('GE19_D24_H3_FIRST_STEP',m,'beta',beta,
                    'coarse=%.3e'%original['first_step_shift_backward'],
                    'dense=%.3e'%dense['first_step_shift_backward'],flush=True)
            if not all(np.isfinite(np.asarray(v)).all() for v in npz.values()):
                raise RuntimeError('D24 nonfinite dense H1/source result')
        finally:
            r7._bg_point=original_bgpoint;r7._CANONICAL_LOCAL_CACHE=original_cache
    report=dict(
        classification='GE19_D24_DENSE_FIRST_INTERVAL_H3_SOURCE_RESOLUTION_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
        preregistration=pre['classification'],
        D22A_SCIENCE_FAIL_immutable=True,D23_H2_projected_diagnostic_only=True,
        D17_dense_H1_vs_archived_first_three_coarse_relative=xreplay,
        D17_original_X10_dense_reconstruction_relative=xerr,
        H3_dense_vs_coarse_first_three_source_main_relative=sourcegrid,
        H3_dense_vs_coarse_first_three_source_constraint_relative=sourcecons,
        selected_first_step=result,
        original_action_H3_full_Ward_certified=False,Z11_certified=False,Z20_certified=False,
        q20_B20_recomputed=False,H4_Z21_solve_performed=False,lensing_licensed=False,
        no_observational_tuning=True,
        input_sha256={k:sha(rd/v[0]) for k,v in pre['archives'].items()},
        claim_boundary='D24 reconstructs only first nine D17 dense H1 sub4 nodes and evaluates original GE06/GE07/Lambda/H3F StageE on those nodes. It compares exactly three preselected first-interval H3 modes using the frozen Radau step and reprojected source-dependent boundary. Dense FD4 still approximates derivatives, and the D17 dense first-order trajectory is numerical, not a certified enclosure. No full H3, q20, H4, Z21, lensing or observational tuning. Immutable D22A FAIL.'
    )
    oj.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(on,**npz)
    oj.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print('GE19_D24_CLASSIFICATION',report['classification'],flush=True)

if __name__=='__main__':main()
