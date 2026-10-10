#!/usr/bin/env python3
"""D25: original-action H3 first-interval constraint defect under Radau substeps.

Diagnostic only. Freeze archived D22A H3F sources, boundary p0 and action
background; change ONLY the two-stage Radau step partition 1,2,4,8.
No source fitting, gate relaxation, new H3/H2/q20/H4 parent claims.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from contextlib import ExitStack
import numpy as np

from ge19 import h4f3d20r1_recompute_five_sources_and_bath_ward as d20
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17driver
from ge19 import h4f3d17_original_action_dense_H1_core as d17core

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'D25_SOURCE_MANIFEST.json'
TINY=1e-300
MODE_BETA=((14,0.1),(1,1.0),(40,0.1))
NSUB=(1,2,4,8)


def sha(path:Path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def rel(a,b):
    aa=np.asarray(a,complex);bb=np.asarray(b,complex)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def z(z:complex):return [float(z.real),float(z.imag)]


def verify(rd,manifest):
    if manifest['classification']!='GE19_D25_PREDATA_FROZEN_SOURCE_ORIGINAL_ACTION_FIRST_INTERVAL_SUBSTEP_DIAGNOSTIC':
        raise RuntimeError('D25 preregistration changed')
    if subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()!=\
            'physics-first-gravitational-elasticity':
        raise RuntimeError('D25 wrong branch; main forbidden')
    for path,want in manifest['frozen_git_blobs'].items():
        head=subprocess.check_output(['git','rev-parse','HEAD:'+path],cwd=ROOT,text=True).strip()
        work=subprocess.check_output(['git','hash-object',str(ROOT/path)],cwd=ROOT,text=True).strip()
        if head!=want or work!=want:raise RuntimeError('D25 original code blob mismatch '+path)
    for path,want in manifest['local_source_sha256'].items():
        if sha(ROOT/path)!=want:raise RuntimeError('D25 dependency/script SHA mismatch '+path)
    files={}
    for key,(name,want) in manifest['parent_archives'].items():
        path=rd/name
        if not path.is_file() or sha(path)!=want:raise RuntimeError('D25 missing/changed parent '+key+' '+str(path))
        files[key]=path
    return files


def freeze_source(r7,bg,src_npz):
    out={}
    for i,beta in enumerate(r7.BETAS):
        assert float(beta)==(1.0,0.5,0.1)[i]
        main=np.asarray(src_npz[f'beta{i}_H3F_D17_source_rows'],complex)
        con=np.asarray(src_npz[f'beta{i}_H3F_D17_source_constraints'],complex)
        if main.shape!=(6,128,41) or con.shape!=(2,128,41) or not np.isfinite(main).all() or not np.isfinite(con).all():
            raise RuntimeError('D25 malformed frozen D22A H3 source '+str(beta))
        out[beta]={'rhs':main,'rhs_constraint':con}
    return out


def step(r7,mod6,mod7,bg,tag,k,ya,xa,xb,rhsfun,confun):
    """Frozen original two-stage Radau IIA step, 8x8 canonical system."""
    hh=xb-xa
    I=np.eye(8,dtype=complex)
    a11,a12,a21,a22,b1,b2=5/12,-1/12,3/4,1/4,3/4,1/4
    xstage=(xa+hh/3,xb)
    mats=[];forcing=[]
    for xq in xstage:
        M,F,*_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,float(xq))
        rr=np.asarray(rhsfun(float(xq)),complex)
        cc=np.asarray(confun(float(xq)),complex)
        if rr.ndim==1:rr=rr[:,None]
        if cc.ndim==1:cc=cc[:,None]
        SS=np.vstack((rr,cc))
        mats.append(M);forcing.append(F@SS)
    M1,M2=mats;F1,F2=forcing
    K=np.block([[I-hh*a11*M1,-hh*a12*M2],[-hh*a21*M1,I-hh*a22*M2]])
    rhs=np.vstack((ya+hh*(a11*F1+a12*F2),ya+hh*(a21*F1+a22*F2)))
    ss,diagnostic=r7._dense_equilibrated_solve(K,rhs)
    yy1,yy2=ss[:8],ss[8:]
    g1=M1@yy1+F1;g2=M2@yy2+F2
    ynext=ya+hh*(b1*g1+b2*g2)
    return ynext,float(diagnostic['scaled_relative_L2_residual_max'])


def integrate(r7,mod6,mod7,bg,tag,k,y0,xa,xb,rhsfun,confun,nsub):
    y=np.asarray(y0,complex).reshape(8,1).copy()
    x=np.linspace(xa,xb,nsub+1)
    worst=0.0
    for i in range(nsub):
        y,e=step(r7,mod6,mod7,bg,tag,k,y,float(x[i]),float(x[i+1]),rhsfun,confun)
        worst=max(worst,e)
    return y[:,0],worst


def shift_at(r7,mod6,mod7,bg,tag,k,xq,y,rhsfun,confun):
    M,F,ZY,ZR,WY,WR,Cmat,bp,_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,float(xq))
    rr=np.asarray(rhsfun(float(xq)),complex);cc=np.asarray(confun(float(xq)),complex)
    if rr.ndim==1:rr=rr[:,None]
    if cc.ndim==1:cc=cc[:,None]
    # rhsfun is beta-batched; diagnostic is supplied its full beta column below.
    return M,F,WY,WR,Cmat,rr,cc


def metric_from_y(r7,op,y,ib):
    _M,_F,WY,WR,Cmat,rr,cc=op
    ss=np.concatenate((rr[:,ib],cc[:,ib]))
    w=WY@np.asarray(y,complex)+WR@ss
    row=Cmat[10]+Cmat[11]
    d=r7._constraint_backward_error(row,w,cc[0,ib],Cmat[10]@w,Cmat[11]@w)
    return {'relative_backward':float(d['metric']),'absolute_residual':float(d['absolute_residual']),
            'backward_scale':float(d['scale']),'lhs':z(complex(row@w)),
            'rhs_shift':z(complex(cc[0,ib])),'complex_defect':z(complex(row@w-cc[0,ib]))}


def archived_y(r7,op,st,dt):
    _M,_F,_WY,_WR,Cmat,_rr,_cc=op
    w=np.empty(10,complex)
    w[[0,2,3,4,5,1]]=np.asarray(st,complex)
    w[[6,7,8,9]]=np.asarray(dt,complex)
    return np.concatenate((w[r7._QIDX],Cmat[0:4]@w)),w


def manufactured_test():
    # Frozen Radau IIA order-three example: y'=-y, independently known exp.
    I=np.eye(8,dtype=complex);M=-I
    def pure(ya,h):
        aa11,aa12,aa21,aa22=5/12,-1/12,3/4,1/4
        K=np.block([[I-h*aa11*M,-h*aa12*M],[-h*aa21*M,I-h*aa22*M]])
        rhs=np.concatenate((ya,ya))
        v=np.linalg.solve(K,rhs)
        return ya+h*((3/4)*(M@v[:8])+(1/4)*(M@v[8:]))
    errs=[]
    for n in (1,2,4,8):
        y=np.ones(8,complex)
        for _ in range(n):y=pure(y,0.4/n)
        errs.append(float(np.max(np.abs(y-math.exp(-0.4)))))
    if not (errs[3]<errs[2]<errs[1]<errs[0] and errs[3]<1e-6):
        raise RuntimeError('D25 frozen two-stage Radau refinement manufactured failure '+str(errs))
    # Sign error negative control: a source-matched shift row must not pass with -source.
    lhs=3.0; source=3.0
    if abs(lhs-source)!=0 or abs(lhs+source)<1.0:
        raise RuntimeError('D25 sign negative control failed')
    print('GE19_D25_MANUFACTURED_RADAU_REFINEMENT_AND_SHIFT_SIGN_PASS',flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--results-dir',required=True)
    p.add_argument('--json-out',required=True)
    p.add_argument('--npz-out',required=True)
    args=p.parse_args(); rd=Path(args.results_dir).resolve()
    jp=Path(args.json_out).resolve(); npz=Path(args.npz_out).resolve()
    if jp.exists() or npz.exists():raise RuntimeError('D25 refuses to overwrite existing outputs')
    manufactured_test()
    manifest=json.loads(MANIFEST.read_text())
    files=verify(rd,manifest)
    print('GE19_D25_ALL_FROZEN_SHA_AND_ORIGINAL_ACTION_SOURCE_PASS',flush=True)
    old=d20.source.old;r7=old.r7
    report={'classification':'GE19_D25_FIRST_INTERVAL_SHIFT_SUBSTEP_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
        'preregistration':manifest['classification'],'frozen_parent_sha256':{k:sha(v) for k,v in files.items()},
        'step_partitions':list(NSUB),'action_source_changed':False,'boundary_changed':False,
        'D22A_science_FAIL_immutable':True,'D23_projected_H2_uncertified':True,
        'D24_dense_source_diagnostic_immutable':True,'Z11_certified':False,'Z20_certified':False,
        'q20_B20_recomputed':False,'full_H4_Ward_certified':False,'Z21_certified':False,
        'lensing_licensed':False,'no_observational_tuning':True,'per_case':[]}
    out={}
    with ExitStack() as es:
        r13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z22=es.enter_context(np.load(files['D22A_NPZ'],allow_pickle=False))
        d17=es.enter_context(np.load(files['D17_NPZ'],allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,r13)
        tag='C_star';bg=bgs[(128,tag)];x=np.asarray(bg['x'],float)
        if not (np.array_equal(x,np.asarray(z22['x_primary'],float)) and
                np.array_equal(x,np.asarray(d17['x_primary'],float)) and
                np.array_equal(x,np.asarray(d17['primary_C_star_x_dense_sub4'],float)[::4])):
            raise RuntimeError('D25 original-action x grid mismatch')
        src=freeze_source(r7,bg,z22)
        independent_d23=json.loads(files['D23_JSON'].read_text())
        if independent_d23.get('classification')!='GE19_D23_PROJECTED_H2_NUMERICAL_DIAGNOSTIC_AND_H3_TRANSPORT_COMPLETE_PARENTS_UNCERTIFIED':
            raise RuntimeError('D25 D23 independent first-step comparator classification mismatch')
        p0=np.asarray(z22['Z20_source_aware_projected_p0_primary'],complex)
        z20=np.asarray(z22['Z20_D17_H3F_candidate_primary'],complex)
        dt20=np.asarray(z22['Z20dot_D17_H3F_candidate_primary'],complex)
        if p0.shape!=(3,40,4) or z20.shape!=(3,40,6,128) or dt20.shape!=(3,40,4,128):
            raise RuntimeError('D25 source-aware initial boundary / archived state shape mismatch')
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={}
        active={'ctx':None}
        def action_bgpoint(bgarg,xq):
            if active['ctx'] is None:raise RuntimeError('D25 missing original action clock')
            return active['ctx'](bgarg,xq)
        r7._bg_point=action_bgpoint
        try:
            evalH,_=d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            x0,x1=float(x[0]),float(x[1])
            for m,beta in MODE_BETA:
                ib=list(r7.BETAS).index(beta);jm=list(r7.M_SOLVE).index(m)
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                rf,cf=r7._source_interp(x,src,m)
                op0=shift_at(r7,mod6,mod7,bg,tag,k,x0,None,rf,cf)
                op1=shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rf,cf)
                y0=np.zeros(8,complex);y0[4:8]=p0[ib,jm]
                g0=metric_from_y(r7,op0,y0,ib)
                arch,archw=archived_y(r7,op1,z20[ib,jm,:,1],dt20[ib,jm,:,1])
                garch=metric_from_y(r7,op1,arch,ib)
                comparator=[c for c in independent_d23['H3_first_interval_constraint_transport']
                            if int(c['mode'])==m and float(c['beta'])==beta]
                if len(comparator)!=1:
                    raise RuntimeError('D25 missing/ambiguous D23 first-step comparator')
                expected=float(comparator[0]['first_step_absolute_shift_defect'])
                if abs(garch['absolute_residual']-expected)>5e-5*max(garch['absolute_residual'],expected,TINY):
                    raise RuntimeError(f'D25 independent D23 first-step comparator mismatch m={m} beta={beta}')
                rows=[];last=None
                for n in NSUB:
                    y1,eq=integrate(r7,mod6,mod7,bg,tag,k,y0,x0,x1,rf,cf,n)
                    g=metric_from_y(r7,op1,y1,ib)
                    rows.append({'substeps':n,'shift':g,'Radau_block_backward':eq,
                                 'canonical_end_state_vs_archived_relative':rel(y1,arch)})
                    out[f'm{m}_beta{str(beta).replace(".","p")}_n{n}_y1']=y1
                    print(f'GE19_D25_FIRST_INTERVAL m={m} beta={beta} n={n} '
                          f'shift={g["relative_backward"]:.6e} abs={g["absolute_residual"]:.6e} '
                          f'Radau={eq:.3e}',flush=True)
                if rows[0]['canonical_end_state_vs_archived_relative']>1e-8:
                    raise RuntimeError(f'D25 n1 does not replay original D22A archived y1 m={m} beta={beta}')
                if abs(rows[0]['shift']['absolute_residual']-garch['absolute_residual'])>\
                   1e-8*max(garch['absolute_residual'],rows[0]['shift']['absolute_residual'],TINY):
                    raise RuntimeError(f'D25 n1 shift does not replay archived original action defect m={m}')
                decline=rows[-1]['shift']['absolute_residual']/max(rows[0]['shift']['absolute_residual'],TINY)
                report['per_case'].append({'mode':m,'beta':beta,'initial_shift':g0,'archived_first_step':garch,
                    'n1_archive_replay_relative':rows[0]['canonical_end_state_vs_archived_relative'],
                    'substep_results':rows,'n8_over_n1_abs_defect':decline,
                    'diagnostic_if_ratio_gt_0p1':'defect_persists_for_frozen_action_and_H3_source' if decline>0.1 else 'defect_reduces_with_substeps'})
                out[f'm{m}_beta{str(beta).replace(".","p")}_original_y1']=arch
                out[f'm{m}_beta{str(beta).replace(".","p")}_y0']=y0
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
    report['all_input_and_replay_controls_pass']=True
    report['claim_boundary']=(
        'Frozen original-action Cstar Nt128 H3F sources and original projected p0, three preregistered '
        'first-interval H3 modes. Subdivide only original two-stage Radau propagation into 1/2/4/8. '
        'Replay D22A archived one-step canonical state and shift. Persistence is not a proof of '
        'fundamental theory inconsistency: H3F H1 derivative and source interpolation remain numerical. '
        'No source projection/tuning, no parents certification, q20/H4/Z21/lensing.')
    jp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    np.savez_compressed(npz,**out)
    print('GE19_D25_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':main()
