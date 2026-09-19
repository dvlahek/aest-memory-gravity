#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import lstsq
from scipy.optimize._numdiff import approx_derivative

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair16 as r16
import nl1c7b.initial_constraint_certification_repair18a as r18a
import nl1c7b.initial_constraint_certification_repair19 as r19
import nl1c7b.initial_constraint_certification_repair19a as r19a

R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA256='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R17_JSON_SHA256='09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e'
R18_JSON_SHA256='8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922'
R18A_JSON_SHA256='29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782'
R18B_JSON_SHA256='cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855'
R18B1_JSON_SHA256='8e0d796e0368372d0b4cf75a075fba12ebde154b651d74929e745118c1ca6dab'
R18C_JSON_SHA256='d49600f8b27536aeb0dca28d1d777d09439a376241c7f8f93b74e754c502e24b'
R18D_JSON_SHA256='adc1410d50118c8080c1f84e5733cb09e5ff7d8f51a4937f1e306a96fe416def'
R18D1_JSON_SHA256='21d5be34660f0054bd8550908f300de64ec1ec9e8f81e0f150c7c1540e3bf04c'
R19_JSON_SHA256='ccf4a362f6a8a791f681d565881ff5728520752b1cbd93d72024b0919e1fe879'
R19A_JSON_SHA256='b9b79d1fe12dff7b59d80260572129b746322412bf96ff214204f9651bd77761'
R19B_JSON_SHA256='d177394b45e19ac2bca739d4ff256694c5df65e9331276e3c1b1466f4fbe5929'
R19B1_JSON_SHA256='33774c721bfd15c1c2f6b776408b3fc4623e3720f9199aa04fc43e8415be1a26'

R19B1_CLASS='NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_FEASIBILITY_LSMR_STAGNATION_PASS'
CANON_KIND='Simple'
CANON_BETA=1.0
LAMBDAS=(1.0,0.5,0.25,0.125)
KINDS=('Simple','Exponential','Sharp')
BETAS=(1.0,0.5,0.1)

LIMIT=1e-7
Q_LIMIT=1e-12
GAUGE_LIMIT=1e-12
REPRO_LIMIT=1e-12
FIRST_STEP_LIMIT=1e-10
SLOPE_MIN=1.8
SLOPE_MAX=2.2
GRID_RATIO_LIMIT=2.0
SAFETY_BOUND=0.5
ARMIJO_C=1e-4
ALPHAS=(1.0,0.5,0.25,0.125,0.0625,0.03125,0.015625,0.0078125)
MAX_ITER=12
TINY=1e-300


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def smatch(a,b,limit=REPRO_LIMIT):
    a=float(a); b=float(b)
    ae=abs(a-b)
    re=ae/max(abs(a),abs(b),TINY)
    return bool(ae<=limit or re<=limit),float(ae),float(re)


def exact_ok(ev,x,freeze_ok):
    x=np.asarray(x,float)
    m=len(x)//2
    gy,gq=r19.gauge_values(x)
    return bool(
        ev.get('finite',False)
        and np.all(np.asarray(ev['L'])>0)
        and float(ev['qerr'])<=Q_LIMIT
        and abs(gy)<=GAUGE_LIMIT
        and abs(gq)<=GAUGE_LIMIT
        and float(np.max(np.abs(x[:m])))<=SAFETY_BOUND
        and float(np.max(np.abs(x[m:])))<=SAFETY_BOUND
        and float(ev['maxH'])<=LIMIT
        and float(ev['maxM'])<=LIMIT
        and freeze_ok
    )


def build_virtual_problem(parent,scale,lam,h,qbg,zbg,funcs,dY):
    vp=r18a.virtual_state(parent,lam)
    base=r18a.source_arrays(vp,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
    if not base.get('finite',False):
        raise RuntimeError(f'nonfinite virtual parent scale={scale} lambda={lam}')
    n=len(vp['r']); m=n-1
    non=np.arange(n)>0
    denomH=np.asarray(base['denH'][non]+base['floorH'],float)
    denomM=np.asarray(base['denM'][non]+base['floorM'],float)
    Rs=float(scale)/float(h)
    char_rt=b4.AI*b4.H_DIRECT*Rs

    def fun_x(x):
        st=r18a.apply_projection(vp,np.asarray(x,float),char_rt)
        ev=r18a.source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
        if not ev.get('finite',False):
            return np.full(2*m,1e100,float)
        return np.concatenate([
            np.asarray(ev['numH'][non]/denomH,float),
            np.asarray(ev['numM'][non]/denomM,float),
        ])

    def evaluate_x(x):
        st=r18a.apply_projection(vp,np.asarray(x,float),char_rt)
        ev=r18a.source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
        freeze_ok,freeze_rows=r18a.field_freeze(vp,st)
        return st,ev,freeze_ok,freeze_rows

    return vp,base,fun_x,evaluate_x,char_rt


def direct_gelsy_step(J,F,B):
    A=np.asarray(J,float)
    F=np.asarray(F,float)
    cond=float(max(A.shape)*np.finfo(float).eps)
    dz,residuals,rank,s=lstsq(
        A,-F,cond=cond,lapack_driver='gelsy',check_finite=True
    )
    dz=np.asarray(dz,float)
    dx=np.asarray(B@dz,float).ravel()
    pred=np.asarray(F+A@dz,float)
    rel=float(np.linalg.norm(pred)/max(np.linalg.norm(F),TINY))
    m=len(dx)//2
    return {
        'rank':int(rank),
        'expected_rank':int(A.shape[1]),
        'cond_cutoff_relative':cond,
        'predicted_relative_residual':rel,
        'predicted_residual_L2':float(np.linalg.norm(pred)),
        'step_reduced_L2':float(np.linalg.norm(dz)),
        'step_physical_L2':float(np.linalg.norm(dx)),
        'max_abs_step_yL':float(np.max(np.abs(dx[:m]))),
        'max_abs_step_qRt':float(np.max(np.abs(dx[m:]))),
        'finite':bool(
            np.all(np.isfinite(A)) and np.all(np.isfinite(F))
            and np.all(np.isfinite(dz)) and np.all(np.isfinite(dx))
            and np.all(np.isfinite(pred))
        ),
    },dz,dx


def solve_one(parent,scale,nr,lam,h,qbg,zbg,funcs,dY,B,frozen_first=None):
    vp,base,fun_x,evaluate_x,char_rt=build_virtual_problem(
        parent,scale,lam,h,qbg,zbg,funcs,dY
    )
    n=len(vp['r']); m=n-1
    z=np.zeros(B.shape[1],float)
    x=np.zeros(2*m,float)
    F=np.asarray(fun_x(x),float)
    phi=0.5*float(np.dot(F,F))
    history=[]
    first_repro=None
    converged=False
    fail_reason=None
    accepted_iterations=0

    for it in range(MAX_ITER+1):
        st,ev,freeze_ok,freeze_rows=evaluate_x(x)
        if exact_ok(ev,x,freeze_ok):
            converged=True
            break
        if it==MAX_ITER:
            fail_reason='max_iterations'
            break

        Jx=approx_derivative(
            fun_x,x,method='2-point',sparsity=r18a.jac_pattern(n)
        )
        Jx=Jx.tocsr()
        J=(Jx@B).toarray()
        step,dz,dx=direct_gelsy_step(J,F,B)
        if not step['finite']:
            fail_reason='nonfinite_direct_step'
            break

        if it==0 and frozen_first is not None:
            checks=[]
            for key,obs,fr in (
                ('rank',step['rank'],frozen_first['rank']),
                ('predicted_relative_residual',step['predicted_relative_residual'],frozen_first['relative_final_linear_residual']),
                ('max_abs_yL',step['max_abs_step_yL'],frozen_first['max_abs_yL']),
                ('max_abs_qRt',step['max_abs_step_qRt'],frozen_first['max_abs_qRt']),
            ):
                if key=='rank':
                    ok=int(obs)==int(fr); ae=float(abs(int(obs)-int(fr))); re=ae/max(abs(float(obs)),abs(float(fr)),1.0)
                else:
                    ok,ae,re=smatch(obs,fr,FIRST_STEP_LIMIT)
                checks.append({'key':key,'pass':bool(ok),'abs_error':ae,'relative_error':re,'observed':float(obs),'frozen':float(fr)})
            first_repro={'checks':checks,'pass':bool(all(c['pass'] for c in checks))}

        accepted=False
        trial_record=[]
        for alpha in ALPHAS:
            zt=z+alpha*dz
            xt=np.asarray(B@zt,float).ravel()
            if (
                np.max(np.abs(xt[:m]))>SAFETY_BOUND
                or np.max(np.abs(xt[m:]))>SAFETY_BOUND
                or not np.all(np.isfinite(xt))
            ):
                trial_record.append({'alpha':alpha,'accepted':False,'reason':'safety_or_nonfinite'})
                continue
            Ft=np.asarray(fun_x(xt),float)
            if not np.all(np.isfinite(Ft)):
                trial_record.append({'alpha':alpha,'accepted':False,'reason':'nonfinite_residual'})
                continue
            phit=0.5*float(np.dot(Ft,Ft))
            armijo=bool(phit<=phi*(1.0-ARMIJO_C*alpha))
            trial_record.append({
                'alpha':alpha,'accepted':armijo,
                'phi_trial':phit,'residual_L2_trial':float(np.linalg.norm(Ft)),
            })
            if armijo:
                z=zt; x=xt; F=Ft; phi=phit
                accepted=True
                accepted_iterations+=1
                break

        history.append({
            'iteration':int(it),
            'phi_before':float(history[-1]['phi_after']) if history and 'phi_after' in history[-1] else None,
            'residual_L2_before':None,
            'direct_step':step,
            'trials':trial_record,
            'accepted':accepted,
            'accepted_alpha':None if not accepted else float(next(t['alpha'] for t in trial_record if t['accepted'])),
            'phi_after':float(phi),
            'residual_L2_after':float(np.linalg.norm(F)),
        })
        if not accepted:
            fail_reason='backtracking_failed'
            break

    st,ev,freeze_ok,freeze_rows=evaluate_x(x)
    gy,gq=r19.gauge_values(x)
    corr=r18a.correction_metrics(vp,st,scale,h)
    passed=exact_ok(ev,x,freeze_ok)
    if not passed and fail_reason is None:
        fail_reason='exact_closure_not_reached'

    return {
        'scale_hinv_Mpc':float(scale),
        'Nr':int(nr),
        'lambda':float(lam),
        'pass':bool(passed),
        'converged':bool(converged),
        'fail_reason':fail_reason,
        'accepted_iterations':int(accepted_iterations),
        'final_frozen_residual_L2':float(np.linalg.norm(F)),
        'final_phi':float(phi),
        'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else None,
        'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else None,
        'rms_epsilon_H':float(ev['rmsH']) if ev.get('finite',False) else None,
        'rms_epsilon_M':float(ev['rmsM']) if ev.get('finite',False) else None,
        'Q_target_max_normalized_error':float(ev['qerr']) if ev.get('finite',False) else None,
        'Y4_residual':float(gy),
        'Qmean_residual':float(gq),
        'max_abs_yL':float(np.max(np.abs(x[:m]))),
        'max_abs_qRt':float(np.max(np.abs(x[m:]))),
        'correction':corr,
        'field_freeze_pass':bool(freeze_ok),
        'field_freeze':freeze_rows,
        'first_step_reproduction':first_repro,
        'history':history,
    },st,x


def slopes(vals):
    out=[]
    for a,b in zip(vals[:-1],vals[1:]):
        if a>0 and b>0 and np.isfinite(a) and np.isfinite(b):
            out.append(float(math.log(a/b,2.0)))
        else:
            out.append(None)
    return out


def write_npz(path,states,h,ks):
    payload={
        'a_i':np.asarray(b4.AI),
        'h':np.asarray(h),
        'k_grid_Mpc_inv':np.asarray(ks,float),
        'scales_hinv_Mpc':np.asarray(b4.SCALES,float),
        'Nrs':np.asarray([256,512],int),
        'repair19c_orthonormal_direct_gn_exact_nonlinear':np.asarray(True),
        'selected_conditions':np.asarray('Y4=0,Qmean=0'),
        'solver':np.asarray('orthonormal direct GELSY Gauss-Newton'),
        'repair19b1_json_sha256':np.asarray(R19B1_JSON_SHA256),
        'parent_repair15a_npz_sha256':np.asarray(R15A_NPZ_SHA256),
    }
    for (scale,nr),st in sorted(states.items()):
        prefix=f's{int(scale)}_n{int(nr)}_'
        for k,v in st.items():
            payload[prefix+k]=np.asarray(v,float)
    np.savez_compressed(path,**payload)


def validate_npz(path,states):
    p=Path(path)
    if not p.is_file() or p.stat().st_size<=0:
        return False,{'exists':False}
    z=np.load(p)
    ok=bool(
        bool(np.asarray(z['repair19c_orthonormal_direct_gn_exact_nonlinear']))
        and str(np.asarray(z['selected_conditions']))=='Y4=0,Qmean=0'
        and str(np.asarray(z['solver']))=='orthonormal direct GELSY Gauss-Newton'
        and str(np.asarray(z['repair19b1_json_sha256']))==R19B1_JSON_SHA256
        and str(np.asarray(z['parent_repair15a_npz_sha256']))==R15A_NPZ_SHA256
        and np.array_equal(np.asarray(z['Nrs']),np.asarray([256,512]))
    )
    count=0
    for (scale,nr),st in sorted(states.items()):
        prefix=f's{int(scale)}_n{int(nr)}_'
        for k,v in st.items():
            key=prefix+k
            present=key in z.files
            ok &= present
            if present:
                arr=np.asarray(z[key],float)
                vv=np.asarray(v,float)
                ok &= arr.shape==vv.shape and np.array_equal(arr,vv)
            count+=1
    ok=bool(ok and len(states)==6)
    return ok,{
        'exists':True,'bytes':int(p.stat().st_size),
        'n_states':int(len(states)),
        'n_state_arrays_checked':int(count),
        'sha256':sha256_file(p),
        'pass':ok,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair15a-json',required=True)
    ap.add_argument('--repair15a-npz',required=True)
    ap.add_argument('--repair16-json',required=True)
    ap.add_argument('--repair17-json',required=True)
    ap.add_argument('--repair18-json',required=True)
    ap.add_argument('--repair18a-json',required=True)
    ap.add_argument('--repair18b-json',required=True)
    ap.add_argument('--repair18b1-json',required=True)
    ap.add_argument('--repair18c-json',required=True)
    ap.add_argument('--repair18d-json',required=True)
    ap.add_argument('--repair18d1-json',required=True)
    ap.add_argument('--repair19-json',required=True)
    ap.add_argument('--repair19a-json',required=True)
    ap.add_argument('--repair19b-json',required=True)
    ap.add_argument('--repair19b1-json',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--state-npz',required=True)
    a=ap.parse_args()

    state_path=Path(a.state_npz)
    if state_path.exists():
        state_path.unlink()

    hashes={
        'repair15a_json':sha256_file(a.repair15a_json),
        'repair15a_npz':sha256_file(a.repair15a_npz),
        'repair16_json':sha256_file(a.repair16_json),
        'repair17_json':sha256_file(a.repair17_json),
        'repair18_json':sha256_file(a.repair18_json),
        'repair18a_json':sha256_file(a.repair18a_json),
        'repair18b_json':sha256_file(a.repair18b_json),
        'repair18b1_json':sha256_file(a.repair18b1_json),
        'repair18c_json':sha256_file(a.repair18c_json),
        'repair18d_json':sha256_file(a.repair18d_json),
        'repair18d1_json':sha256_file(a.repair18d1_json),
        'repair19_json':sha256_file(a.repair19_json),
        'repair19a_json':sha256_file(a.repair19a_json),
        'repair19b_json':sha256_file(a.repair19b_json),
        'repair19b1_json':sha256_file(a.repair19b1_json),
    }
    expected={
        'repair15a_json':R15A_JSON_SHA256,'repair15a_npz':R15A_NPZ_SHA256,
        'repair16_json':R16_JSON_SHA256,'repair17_json':R17_JSON_SHA256,
        'repair18_json':R18_JSON_SHA256,'repair18a_json':R18A_JSON_SHA256,
        'repair18b_json':R18B_JSON_SHA256,'repair18b1_json':R18B1_JSON_SHA256,
        'repair18c_json':R18C_JSON_SHA256,'repair18d_json':R18D_JSON_SHA256,
        'repair18d1_json':R18D1_JSON_SHA256,'repair19_json':R19_JSON_SHA256,
        'repair19a_json':R19A_JSON_SHA256,'repair19b_json':R19B_JSON_SHA256,
        'repair19b1_json':R19B1_JSON_SHA256,
    }
    p16=json.loads(Path(a.repair16_json).read_text())
    p19b1=json.loads(Path(a.repair19b1_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p19b1.get('classification')==R19B1_CLASS
        and all(p19b1.get('gates',{}).values())
        and p19b1.get('summary',{}).get('max_direct_relative_residual',1.0)<=1.1984362607786484e-07*(1.0+1e-12)
        and p19b1.get('summary',{}).get('min_lsmr_to_direct_residual_ratio',0.0)>=4833536.02985291*(1.0-1e-12)
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
    )

    ztrace=rec.read_trace(a.trace)
    ks,gs=rec.groups(ztrace)
    tv_rec=rec.at_ai(gs,'pchip')
    ks_b4,gs_b4=b4.groups(b4.read_trace(a.trace))
    tv_b4=b4.at_ai(gs_b4)
    h=float(cov['h'])
    scalar_ai,scalar_independent,scalar_finite,_=r8.scalar_composites_at_ai(ks,gs,'pchip')
    scalar_identity=r16.rel_sym(scalar_ai,scalar_independent)
    kq_bg=float(np.median(tv_b4['KQ']))
    qbg=b4.stable_q_from_kq(kq_bg)
    kqq_bg=float(np.median(tv_rec['KQQ']))
    zbg=r9.stable_zbg(kq_bg)
    funcs,dY,kidentity=r1.build_nonK()
    g1=bool(
        g1 and len(ks)==128 and np.array_equal(ks,ks_b4)
        and scalar_finite and scalar_identity<=1e-10
        and np.isfinite([qbg,kqq_bg,zbg]).all() and bool(kidentity)
    )

    basis_rows=[]
    bases={}
    g2=True
    for nr in (256,512):
        br,Bc,Bo=r19a.basis_audit(nr)
        ok=bool(
            br['pass']
            and br['orth']['GB_Frobenius']<=GAUGE_LIMIT
            and br['orth']['orthonormality_Frobenius']<=GAUGE_LIMIT
            and abs(br['orth']['condition_number']-1.0)<=REPRO_LIMIT
        )
        basis_rows.append({'Nr':nr,'audit':br,'pass':ok})
        bases[nr]=Bo
        g2 &= ok

    states={}
    for scale in b4.SCALES:
        states[(scale,256)]=r16.load_primary_state(off,scale)
        states[(scale,512)]=r16.reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    frozen16={
        (float(x['scale_hinv_Mpc']),int(x['Nr']),x['Y_kind'],float(x['beta0'])):x
        for x in p16['constraint_rows']
    }
    parent_repro=[]
    g3=True
    for scale in b4.SCALES:
        for nr in (256,512):
            ev=r18a.source_arrays(states[(scale,nr)],CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
            fr=frozen16[(float(scale),nr,CANON_KIND,CANON_BETA)]
            ph,ah,rh=smatch(ev['maxH'],fr['max_epsilon_H'])
            pm,am,rm=smatch(ev['maxM'],fr['max_epsilon_M'])
            ok=bool(ev.get('finite',False) and ph and pm)
            g3 &= ok
            parent_repro.append({
                'scale_hinv_Mpc':float(scale),'Nr':nr,'pass':ok,
                'H_abs_error':ah,'H_relative_error':rh,
                'M_abs_error':am,'M_relative_error':rm,
            })

    frozen_b1={(float(r['scale_hinv_Mpc']),int(r['Nr'])):r for r in p19b1['rows']}

    solve_rows=[]
    solved={}
    g4=True
    g5=True
    g9=True
    for scale in b4.SCALES:
        for nr in (256,512):
            for lam in LAMBDAS:
                frozen_first=None
                if lam==1.0:
                    frozen_first=frozen_b1[(float(scale),nr)]['drivers']['gelsy']['probe']
                row,st,x=solve_one(
                    states[(scale,nr)],scale,nr,lam,h,qbg,zbg,funcs,dY,
                    bases[nr],frozen_first
                )
                solve_rows.append(row)
                solved[(scale,nr,lam)]=st
                g5 &= row['pass']
                g9 &= row['field_freeze_pass']
                if lam==1.0:
                    g4 &= bool(row['first_step_reproduction'] is not None and row['first_step_reproduction']['pass'])
    g4=bool(g4 and sum(1 for r in solve_rows if r['lambda']==1.0)==6)
    g5=bool(g5 and len(solve_rows)==24)
    g9=bool(g9 and len(solve_rows)==24)

    scaling=[]
    g6=True
    for scale in b4.SCALES:
        for nr in (256,512):
            rr=sorted(
                [r for r in solve_rows if r['scale_hinv_Mpc']==float(scale) and r['Nr']==nr],
                key=lambda r:-r['lambda']
            )
            vals=[float(r['correction']['combined_norm']) for r in rr]
            ss=slopes(vals)
            ok=bool(
                len(ss)==3 and ss[1] is not None and ss[2] is not None
                and SLOPE_MIN<=ss[1]<=SLOPE_MAX
                and SLOPE_MIN<=ss[2]<=SLOPE_MAX
            )
            g6 &= ok
            scaling.append({
                'scale_hinv_Mpc':float(scale),'Nr':nr,
                'combined_norms':vals,'adjacent_log2_slopes':ss,
                'gated_pass':ok,
            })

    grid=[]
    g7=True
    for scale in b4.SCALES:
        c256=next(r['correction']['combined_norm'] for r in solve_rows if r['scale_hinv_Mpc']==float(scale) and r['Nr']==256 and r['lambda']==1.0)
        c512=next(r['correction']['combined_norm'] for r in solve_rows if r['scale_hinv_Mpc']==float(scale) and r['Nr']==512 and r['lambda']==1.0)
        ratio=float(max(c256,c512)/max(min(c256,c512),TINY))
        ok=bool(np.isfinite(ratio) and ratio<=GRID_RATIO_LIMIT)
        g7 &= ok
        grid.append({
            'scale_hinv_Mpc':float(scale),'C256':float(c256),'C512':float(c512),
            'symmetric_ratio':ratio,'limit':GRID_RATIO_LIMIT,'pass':ok,
        })

    branch_rows=[]
    g8=True
    for scale in b4.SCALES:
        for nr in (256,512):
            canonical_row=next(r for r in solve_rows if r['scale_hinv_Mpc']==float(scale) and r['Nr']==nr and r['lambda']==1.0)
            if not canonical_row['pass']:
                g8=False
                for kind in KINDS:
                    for beta in BETAS:
                        branch_rows.append({
                            'scale_hinv_Mpc':float(scale),'Nr':nr,
                            'Y_kind':kind,'beta0':float(beta),
                            'skipped_due_to_canonical_fail':True,'pass':False,
                        })
                continue
            st=solved[(scale,nr,1.0)]
            for kind in KINDS:
                for beta in BETAS:
                    ev=r18a.source_arrays(st,kind,beta,qbg,zbg,funcs,dY)
                    ok=bool(ev.get('finite',False) and ev['maxH']<=LIMIT and ev['maxM']<=LIMIT)
                    g8 &= ok
                    branch_rows.append({
                        'scale_hinv_Mpc':float(scale),'Nr':nr,
                        'Y_kind':kind,'beta0':float(beta),
                        'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else None,
                        'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else None,
                        'rms_epsilon_H':float(ev['rmsH']) if ev.get('finite',False) else None,
                        'rms_epsilon_M':float(ev['rmsM']) if ev.get('finite',False) else None,
                        'pass':ok,
                    })
    g8=bool(g8 and len(branch_rows)==54)

    claim_boundary={
        'physical_field_added':False,'Q_modified_directly':False,
        'alpha_modified':False,'phi_modified':False,'matter_modified':False,
        'source_dictionary_changed':False,'coefficient_changed':False,'sign_changed':False,
        'finite_eta_executed':False,'branch_definition_changed':False,
        'radial_points_removed':False,'historical_threshold_changed':False,
        'branch_specific_refit':False,'time_evolution_run':False,
        'observational_claimed':False,'earlier_repair_relabelled':False,
    }
    g11=bool(not any(claim_boundary.values()))

    core=bool(g1 and g2 and g3 and g4 and g5 and g6 and g7 and g8 and g9 and g11)
    output_info={'written':False,'exists_after_run':False}
    g10=False
    lambda1_states={(scale,nr):solved[(scale,nr,1.0)] for scale in b4.SCALES for nr in (256,512)}
    if core:
        state_path.parent.mkdir(parents=True,exist_ok=True)
        write_npz(state_path,lambda1_states,h,ks)
        g10,output_info=validate_npz(state_path,lambda1_states)
        output_info['written']=True
        output_info['exists_after_run']=state_path.exists()
    else:
        if state_path.exists():
            state_path.unlink()
        g10=not state_path.exists()
        output_info={'written':False,'exists_after_run':state_path.exists(),'pass':g10}

    gates={
        'R19C_G1_exact_frozen_provenance':g1,
        'R19C_G2_orthonormal_constrained_basis':bool(g2),
        'R19C_G3_exact_parent_reproduction':bool(g3),
        'R19C_G4_certified_first_step_reproduction':bool(g4),
        'R19C_G5_exact_canonical_nonlinear_closure':bool(g5),
        'R19C_G6_second_order_correction_scaling':bool(g6),
        'R19C_G7_two_grid_correction_amplitude':bool(g7),
        'R19C_G8_all_branch_lambda1_exact_closure':bool(g8),
        'R19C_G9_field_freeze_invariant':bool(g9),
        'R19C_G10_output_integrity':bool(g10),
        'R19C_G11_claim_boundary':g11,
    }

    impl_ok=bool(g1 and g2 and g3 and g4 and g9 and g10 and g11)
    if not impl_ok:
        classification='NL1C7B4_REPAIR19C_IMPLEMENTATION_FAIL'; rc=2
    elif not g5:
        classification='NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_NONLINEAR_CLOSURE_FAIL'; rc=2
    elif not g6:
        classification='NL1C7B4_REPAIR19C_CORRECTION_SCALING_FAIL'; rc=2
    elif not g7:
        classification='NL1C7B4_REPAIR19C_TWO_GRID_CONTROL_FAIL'; rc=2
    elif not g8:
        classification='NL1C7B4_REPAIR19C_CANONICAL_PASS_BRANCH_RETEST_FAIL'; rc=2
    else:
        classification='NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_EXACT_NONLINEAR_CONSTRAINT_PASS'; rc=0

    result={
        'classification':classification,
        'scope':'Repair19c exact nonlinear eta=0 constraint projection with the frozen physical (L,R_t) pair, orthonormal Y4=0/Qmean=0 coordinates, and deterministic direct GELSY Gauss-Newton.',
        'provenance':{
            **hashes,
            'repair19b1_result_freeze_commit':'5f33dd543f9b722438faa9659858be942287f14f',
            'repair19c_prereg_commit':'3eaefcccb6c44f2db12b24caf3bfa3c3ec16a712',
        },
        'solver':{
            'basis':'orthonormal Helmert Y4=0,Qmean=0',
            'linear_driver':'gelsy',
            'cond_rule':'max(J_orth.shape)*eps_float64',
            'jacobian':'grouped sparse physical-coordinate 2-point half-band-16, then J_orth=J_x B_orth',
            'start':'zero',
            'backtracking_alphas':list(ALPHAS),
            'armijo_c':ARMIJO_C,
            'max_accepted_iterations':MAX_ITER,
            'safety_bound_yL_qRt':SAFETY_BOUND,
        },
        'limits':{
            'exact_constraint':LIMIT,'exact_Q':Q_LIMIT,'gauge':GAUGE_LIMIT,
            'first_step_reproduction_abs_or_rel':FIRST_STEP_LIMIT,
            'small_lambda_slope':[SLOPE_MIN,SLOPE_MAX],
            'two_grid_ratio':GRID_RATIO_LIMIT,
        },
        'basis_rows':basis_rows,
        'parent_reproduction':parent_repro,
        'solve_rows':solve_rows,
        'correction_scaling':scaling,
        'two_grid_control':grid,
        'branch_retests':branch_rows,
        'output':output_info,
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'canonical_pass_count':int(sum(r['pass'] for r in solve_rows)),
            'canonical_total':len(solve_rows),
            'lambda1_pass_count':int(sum(r['pass'] for r in solve_rows if r['lambda']==1.0)),
            'max_exact_epsilon_H':float(max(r['max_epsilon_H'] for r in solve_rows if r['max_epsilon_H'] is not None)),
            'max_exact_epsilon_M':float(max(r['max_epsilon_M'] for r in solve_rows if r['max_epsilon_M'] is not None)),
            'max_accepted_iterations':int(max(r['accepted_iterations'] for r in solve_rows)),
            'all_branch_pass_count':int(sum(r.get('pass',False) for r in branch_rows)),
            'all_branch_total':len(branch_rows),
        },
        'interpretation_boundary':{
            'short_time_eta0_evolution_certified':False,
            'finite_eta_certified':False,
            'observational_claimed':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
