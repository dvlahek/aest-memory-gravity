#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
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
import nl1c7b.initial_constraint_certification_repair19c as r19c

R19C2_JSON_SHA256='6a724f46a70be8d23e7b9898fe6e70073879c12f77eefbdbddc63d87fb47a17c'
R19C2_CLASS='NL1C7B4_REPAIR19C2_FINITE_DIFFERENCE_STEP_SCALE_CHARACTERIZED'
SELECTED_METHOD='3-point'
SELECTED_ABS_STEP=3e-6
R19C2_FREEZE_COMMIT='5f51cae7943679f6e96dcdefc7814c0f1551e244'
PREREG_COMMIT='39d36344c9746c51f57cc2f1d85c773b62df2d3c'

TINY=1e-300


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def selected_parent_rows(p19c2):
    selected=p19c2['selected_candidate']
    if selected['method']!=SELECTED_METHOD or float(selected['abs_step'])!=SELECTED_ABS_STEP:
        raise RuntimeError('Repair19c2 selected candidate mismatch')
    out={}
    for row in p19c2['case_rows']:
        cand=next(
            c for c in row['candidates']
            if c['method']==SELECTED_METHOD and float(c['abs_step'])==SELECTED_ABS_STEP
        )
        out[(float(row['scale_hinv_Mpc']),int(row['Nr']))]=cand
    return out


def selected_jacobian(fun_x,x,n,B):
    Jx=approx_derivative(
        fun_x,np.asarray(x,float),
        method=SELECTED_METHOD,
        sparsity=r18a.jac_pattern(n),
        abs_step=SELECTED_ABS_STEP,
    ).tocsr()
    return (Jx@B).toarray()


def compare_first_step(step,dx,Ftrial,F0norm,frozen):
    fp=frozen['one_step_probe']
    checks=[]
    targets=(
        ('rank',step['rank'],fp['rank']),
        ('predicted_relative_residual',step['predicted_relative_residual'],fp['predicted_relative_residual']),
        ('max_abs_yL',step['max_abs_step_yL'],fp['max_abs_yL']),
        ('max_abs_qRt',step['max_abs_step_qRt'],fp['max_abs_qRt']),
        ('exact_full_step_frozen_residual_ratio',float(np.linalg.norm(Ftrial)/max(F0norm,TINY)),fp['frozen_residual_ratio']),
    )
    for key,obs,fr in targets:
        if key=='rank':
            ok=int(obs)==int(fr)
            ae=float(abs(int(obs)-int(fr)))
            re=ae/max(abs(float(obs)),abs(float(fr)),1.0)
        else:
            ok,ae,re=r19c.smatch(obs,fr,r19c.FIRST_STEP_LIMIT)
        checks.append({
            'key':key,'pass':bool(ok),
            'abs_error':float(ae),'relative_error':float(re),
            'observed':float(obs),'frozen':float(fr),
        })
    return {'checks':checks,'pass':bool(all(c['pass'] for c in checks))}


def solve_one(parent,scale,nr,lam,h,qbg,zbg,funcs,dY,B,frozen_first=None):
    vp,base,fun_x,evaluate_x,char_rt=r19c.build_virtual_problem(
        parent,scale,lam,h,qbg,zbg,funcs,dY
    )
    n=len(vp['r']); m=n-1
    z=np.zeros(B.shape[1],float)
    x=np.zeros(2*m,float)
    F=np.asarray(fun_x(x),float)
    F0norm=float(np.linalg.norm(F))
    phi=0.5*float(np.dot(F,F))
    history=[]
    first_repro=None
    converged=False
    fail_reason=None
    accepted_iterations=0

    for it in range(r19c.MAX_ITER+1):
        st,ev,freeze_ok,freeze_rows=evaluate_x(x)
        if r19c.exact_ok(ev,x,freeze_ok):
            converged=True
            break
        if it==r19c.MAX_ITER:
            fail_reason='max_iterations'
            break

        J=selected_jacobian(fun_x,x,n,B)
        step,dz,dx=r19c.direct_gelsy_step(J,F,B)
        if not step['finite']:
            fail_reason='nonfinite_direct_step'
            break

        if it==0 and frozen_first is not None:
            xfull=np.asarray(B@(z+dz),float).ravel()
            Ffull=np.asarray(fun_x(xfull),float)
            first_repro=compare_first_step(step,dx,Ffull,F0norm,frozen_first)

        accepted=False
        trial_record=[]
        for alpha in r19c.ALPHAS:
            zt=z+alpha*dz
            xt=np.asarray(B@zt,float).ravel()
            if (
                np.max(np.abs(xt[:m]))>r19c.SAFETY_BOUND
                or np.max(np.abs(xt[m:]))>r19c.SAFETY_BOUND
                or not np.all(np.isfinite(xt))
            ):
                trial_record.append({'alpha':alpha,'accepted':False,'reason':'safety_or_nonfinite'})
                continue
            Ft=np.asarray(fun_x(xt),float)
            if not np.all(np.isfinite(Ft)):
                trial_record.append({'alpha':alpha,'accepted':False,'reason':'nonfinite_residual'})
                continue
            phit=0.5*float(np.dot(Ft,Ft))
            armijo=bool(phit<=phi*(1.0-r19c.ARMIJO_C*alpha))
            trial_record.append({
                'alpha':alpha,'accepted':armijo,
                'phi_trial':phit,
                'residual_L2_trial':float(np.linalg.norm(Ft)),
            })
            if armijo:
                z=zt; x=xt; F=Ft; phi=phit
                accepted=True
                accepted_iterations+=1
                break

        history.append({
            'iteration':int(it),
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
    passed=r19c.exact_ok(ev,x,freeze_ok)
    if not passed and fail_reason is None:
        fail_reason='exact_closure_not_reached'

    return {
        'scale_hinv_Mpc':float(scale),'Nr':int(nr),'lambda':float(lam),
        'pass':bool(passed),'converged':bool(converged),
        'fail_reason':fail_reason,
        'accepted_iterations':int(accepted_iterations),
        'final_frozen_residual_L2':float(np.linalg.norm(F)),
        'final_phi':float(phi),
        'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else None,
        'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else None,
        'rms_epsilon_H':float(ev['rmsH']) if ev.get('finite',False) else None,
        'rms_epsilon_M':float(ev['rmsM']) if ev.get('finite',False) else None,
        'Q_target_max_normalized_error':float(ev['qerr']) if ev.get('finite',False) else None,
        'Y4_residual':float(gy),'Qmean_residual':float(gq),
        'max_abs_yL':float(np.max(np.abs(x[:m]))),
        'max_abs_qRt':float(np.max(np.abs(x[m:]))),
        'correction':corr,
        'field_freeze_pass':bool(freeze_ok),
        'field_freeze':freeze_rows,
        'first_step_reproduction':first_repro,
        'history':history,
    },st,x


def write_npz(path,states,h,ks):
    payload={
        'a_i':np.asarray(b4.AI),
        'h':np.asarray(h),
        'k_grid_Mpc_inv':np.asarray(ks,float),
        'scales_hinv_Mpc':np.asarray(b4.SCALES,float),
        'Nrs':np.asarray([256,512],int),
        'repair19c3_selected_jacobian_exact_nonlinear':np.asarray(True),
        'selected_conditions':np.asarray('Y4=0,Qmean=0'),
        'solver':np.asarray('orthonormal direct GELSY Gauss-Newton'),
        'jacobian_method':np.asarray(SELECTED_METHOD),
        'jacobian_abs_step':np.asarray(SELECTED_ABS_STEP),
        'repair19c2_json_sha256':np.asarray(R19C2_JSON_SHA256),
        'parent_repair15a_npz_sha256':np.asarray(r19c.R15A_NPZ_SHA256),
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
        bool(np.asarray(z['repair19c3_selected_jacobian_exact_nonlinear']))
        and str(np.asarray(z['selected_conditions']))=='Y4=0,Qmean=0'
        and str(np.asarray(z['solver']))=='orthonormal direct GELSY Gauss-Newton'
        and str(np.asarray(z['jacobian_method']))==SELECTED_METHOD
        and float(np.asarray(z['jacobian_abs_step']))==SELECTED_ABS_STEP
        and str(np.asarray(z['repair19c2_json_sha256']))==R19C2_JSON_SHA256
        and str(np.asarray(z['parent_repair15a_npz_sha256']))==r19c.R15A_NPZ_SHA256
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
    ap.add_argument('--repair19c-json',required=True)
    ap.add_argument('--repair19c1-json',required=True)
    ap.add_argument('--repair19c2-json',required=True)
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
        'repair19c_json':sha256_file(a.repair19c_json),
        'repair19c1_json':sha256_file(a.repair19c1_json),
        'repair19c2_json':sha256_file(a.repair19c2_json),
    }
    expected={
        'repair15a_json':r19c.R15A_JSON_SHA256,
        'repair15a_npz':r19c.R15A_NPZ_SHA256,
        'repair16_json':r19c.R16_JSON_SHA256,
        'repair17_json':r19c.R17_JSON_SHA256,
        'repair18_json':r19c.R18_JSON_SHA256,
        'repair18a_json':r19c.R18A_JSON_SHA256,
        'repair18b_json':r19c.R18B_JSON_SHA256,
        'repair18b1_json':r19c.R18B1_JSON_SHA256,
        'repair18c_json':r19c.R18C_JSON_SHA256,
        'repair18d_json':r19c.R18D_JSON_SHA256,
        'repair18d1_json':r19c.R18D1_JSON_SHA256,
        'repair19_json':r19c.R19_JSON_SHA256,
        'repair19a_json':r19c.R19A_JSON_SHA256,
        'repair19b_json':r19c.R19B_JSON_SHA256,
        'repair19b1_json':r19c.R19B1_JSON_SHA256,
        'repair19c_json':'5ad02254c512f90d0f82a42d0f5aa00f15c1dae6248bdbe7ad69addb183b600a',
        'repair19c1_json':'b4898fed6c6bbe7d4c91f8144ed35d03e6f318b298a2fc13c0daaef038c0e3cd',
        'repair19c2_json':R19C2_JSON_SHA256,
    }

    p16=json.loads(Path(a.repair16_json).read_text())
    p19b1=json.loads(Path(a.repair19b1_json).read_text())
    p19c2=json.loads(Path(a.repair19c2_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p19c2.get('classification')==R19C2_CLASS
        and all(p19c2.get('gates',{}).values())
        and p19c2.get('selected_candidate',{}).get('method')==SELECTED_METHOD
        and float(p19c2.get('selected_candidate',{}).get('abs_step',0.0))==SELECTED_ABS_STEP
        and p19b1.get('classification')==r19c.R19B1_CLASS
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

    bases={}
    basis_rows=[]
    g2=True
    for nr in (256,512):
        br,Bc,Bo=r19a.basis_audit(nr)
        ok=bool(
            br['pass']
            and br['orth']['GB_Frobenius']<=r19c.GAUGE_LIMIT
            and br['orth']['orthonormality_Frobenius']<=r19c.GAUGE_LIMIT
            and abs(br['orth']['condition_number']-1.0)<=r19c.REPRO_LIMIT
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
            ev=r18a.source_arrays(states[(scale,nr)],r19c.CANON_KIND,r19c.CANON_BETA,qbg,zbg,funcs,dY)
            fr=frozen16[(float(scale),nr,r19c.CANON_KIND,r19c.CANON_BETA)]
            ph,ah,rh=r19c.smatch(ev['maxH'],fr['max_epsilon_H'])
            pm,am,rm=r19c.smatch(ev['maxM'],fr['max_epsilon_M'])
            ok=bool(ev.get('finite',False) and ph and pm)
            g3 &= ok
            parent_repro.append({
                'scale_hinv_Mpc':float(scale),'Nr':nr,'pass':ok,
                'H_abs_error':ah,'H_relative_error':rh,
                'M_abs_error':am,'M_relative_error':rm,
            })

    frozen_selected=selected_parent_rows(p19c2)

    solve_rows=[]
    solved={}
    g4=True; g5=True; g9=True
    for scale in b4.SCALES:
        for nr in (256,512):
            for lam in r19c.LAMBDAS:
                fr=frozen_selected[(float(scale),nr)] if lam==1.0 else None
                row,st,x=solve_one(
                    states[(scale,nr)],scale,nr,lam,h,qbg,zbg,funcs,dY,bases[nr],fr
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
            ss=r19c.slopes(vals)
            ok=bool(
                len(ss)==3 and ss[1] is not None and ss[2] is not None
                and r19c.SLOPE_MIN<=ss[1]<=r19c.SLOPE_MAX
                and r19c.SLOPE_MIN<=ss[2]<=r19c.SLOPE_MAX
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
        ok=bool(np.isfinite(ratio) and ratio<=r19c.GRID_RATIO_LIMIT)
        g7 &= ok
        grid.append({
            'scale_hinv_Mpc':float(scale),
            'C256':float(c256),'C512':float(c512),
            'symmetric_ratio':ratio,'limit':r19c.GRID_RATIO_LIMIT,'pass':ok,
        })

    branch_rows=[]
    g8=True
    for scale in b4.SCALES:
        for nr in (256,512):
            canonical=next(r for r in solve_rows if r['scale_hinv_Mpc']==float(scale) and r['Nr']==nr and r['lambda']==1.0)
            if not canonical['pass']:
                g8=False
                for kind in r19c.KINDS:
                    for beta in r19c.BETAS:
                        branch_rows.append({
                            'scale_hinv_Mpc':float(scale),'Nr':nr,
                            'Y_kind':kind,'beta0':float(beta),
                            'skipped_due_to_canonical_fail':True,'pass':False,
                        })
                continue
            st=solved[(scale,nr,1.0)]
            for kind in r19c.KINDS:
                for beta in r19c.BETAS:
                    ev=r18a.source_arrays(st,kind,beta,qbg,zbg,funcs,dY)
                    ok=bool(ev.get('finite',False) and ev['maxH']<=r19c.LIMIT and ev['maxM']<=r19c.LIMIT)
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
        'source_dictionary_changed':False,'coefficient_changed':False,
        'sign_changed':False,'finite_eta_executed':False,
        'branch_definition_changed':False,'radial_points_removed':False,
        'historical_threshold_changed':False,'branch_specific_refit':False,
        'time_evolution_run':False,'observational_claimed':False,
        'earlier_repair_relabelled':False,'selected_Jacobian_changed':False,
    }
    g11=bool(not any(claim_boundary.values()))

    core=bool(g1 and g2 and g3 and g4 and g5 and g6 and g7 and g8 and g9 and g11)
    g10=False
    output_info={'written':False,'exists_after_run':False}
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
        'R19C3_G1_exact_frozen_provenance':g1,
        'R19C3_G2_orthonormal_constrained_basis':bool(g2),
        'R19C3_G3_exact_parent_reproduction':bool(g3),
        'R19C3_G4_selected_first_step_reproduction':bool(g4),
        'R19C3_G5_exact_canonical_nonlinear_closure':bool(g5),
        'R19C3_G6_second_order_correction_scaling':bool(g6),
        'R19C3_G7_two_grid_correction_amplitude':bool(g7),
        'R19C3_G8_all_branch_lambda1_exact_closure':bool(g8),
        'R19C3_G9_field_freeze_invariant':bool(g9),
        'R19C3_G10_output_integrity':bool(g10),
        'R19C3_G11_claim_boundary':g11,
    }

    impl_ok=bool(g1 and g2 and g3 and g4 and g9 and g10 and g11)
    if not impl_ok:
        classification='NL1C7B4_REPAIR19C3_IMPLEMENTATION_FAIL'; rc=2
    elif not g5:
        classification='NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_NONLINEAR_CLOSURE_FAIL'; rc=2
    elif not g6:
        classification='NL1C7B4_REPAIR19C3_CORRECTION_SCALING_FAIL'; rc=2
    elif not g7:
        classification='NL1C7B4_REPAIR19C3_TWO_GRID_CONTROL_FAIL'; rc=2
    elif not g8:
        classification='NL1C7B4_REPAIR19C3_CANONICAL_PASS_BRANCH_RETEST_FAIL'; rc=2
    else:
        classification='NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_EXACT_NONLINEAR_CONSTRAINT_PASS'; rc=0

    result={
        'classification':classification,
        'scope':'Repair19c3 exact nonlinear eta=0 constraint projection using the Repair19c2-selected 3-point abs_step=3e-6 grouped physical-coordinate Jacobian and otherwise frozen Repair19c solver.',
        'provenance':{
            **hashes,
            'repair19c2_result_freeze_commit':R19C2_FREEZE_COMMIT,
            'repair19c3_prereg_commit':PREREG_COMMIT,
        },
        'solver':{
            'basis':'orthonormal Helmert Y4=0,Qmean=0',
            'linear_driver':'gelsy',
            'cond_rule':'max(J_orth.shape)*eps_float64',
            'jacobian':'grouped sparse physical-coordinate 3-point half-band-16 with explicit abs_step=3e-6, then J_orth=J_x B_orth',
            'jacobian_method':SELECTED_METHOD,
            'jacobian_abs_step':SELECTED_ABS_STEP,
            'selection_source':'frozen Repair19c2 derivative-fidelity lexicographic rule',
            'start':'zero',
            'backtracking_alphas':list(r19c.ALPHAS),
            'armijo_c':r19c.ARMIJO_C,
            'max_accepted_iterations':r19c.MAX_ITER,
            'safety_bound_yL_qRt':r19c.SAFETY_BOUND,
        },
        'limits':{
            'exact_constraint':r19c.LIMIT,
            'exact_Q':r19c.Q_LIMIT,
            'gauge':r19c.GAUGE_LIMIT,
            'first_step_reproduction_abs_or_rel':r19c.FIRST_STEP_LIMIT,
            'small_lambda_slope':[r19c.SLOPE_MIN,r19c.SLOPE_MAX],
            'two_grid_ratio':r19c.GRID_RATIO_LIMIT,
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
