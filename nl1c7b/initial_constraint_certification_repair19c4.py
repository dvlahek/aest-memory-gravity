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
import nl1c7b.initial_constraint_certification_repair19c3 as r19c3

R19C3_JSON_SHA256='aa19480ce4d41f649368f192f27d85b823e0247aa6f9bcc9eb7a9d23b60ac5b0'
R19C3_CLASS='NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_NONLINEAR_CLOSURE_FAIL'
R19C3_FREEZE_COMMIT='b15eee7f15a5ef4dbb2c87050f4a55983d688d88'
R19C3_EXECUTION_HEAD='8317c38c1f6f3df18dcb4106c9b81f7bc543ceaa'
R19C3_IMPLEMENTATION_BLOB='08985f1ee334f038a7125cc239fb6b8929d428af'
PREREG_INITIAL_COMMIT='3ad5a4e1a9118d26a3c12d5b806f3afeeed6d52d'
PREREG_COMMIT='77a0b4977ee921d0693ad14880f38e5822d505a4'

METHOD='3-point'
CONTROL_STEP=3e-6
DIRECTION_STEPS=(1e-5,3e-6,1e-6,3e-7,1e-7,3e-8,1e-8,3e-9,1e-9)
CANDIDATE_STEPS=DIRECTION_STEPS
REFERENCE_STABILITY_LIMIT=5e-4
FIDELITY_LIMIT=1e-3
IMPROVEMENT_FACTOR=5.0
TINY=1e-300


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def block_norm(x,m,which):
    a=np.asarray(x,float)
    if which=='H':
        return float(np.linalg.norm(a[:m]))
    if which=='M':
        return float(np.linalg.norm(a[m:]))
    return float(np.linalg.norm(a))


def candidate_jacobian(fun_x,x,n,B,abs_step):
    Jx=approx_derivative(
        fun_x,np.asarray(x,float),
        method=METHOD,
        sparsity=r18a.jac_pattern(n),
        abs_step=float(abs_step),
    ).tocsr()
    J=(Jx@B).toarray()
    return J


def frozen_lambda1_rows(p19c3):
    out={}
    for row in p19c3['solve_rows']:
        if float(row['lambda'])==1.0:
            out[(float(row['scale_hinv_Mpc']),int(row['Nr']))]=row
    if len(out)!=6:
        raise RuntimeError(f'expected six frozen Repair19c3 lambda=1 rows, got {len(out)}')
    return out


def first_step_ratio_from_frozen(row):
    repro=row.get('first_step_reproduction') or {}
    for check in repro.get('checks',[]):
        if check.get('key')=='exact_full_step_frozen_residual_ratio':
            return float(check['observed'])
    raise RuntimeError('missing frozen first-step full-step ratio')


def reproduce_first_state(parent,scale,nr,h,qbg,zbg,funcs,dY,B,frozen):
    vp,base,fun_x,evaluate_x,char_rt=r19c.build_virtual_problem(
        parent,scale,1.0,h,qbg,zbg,funcs,dY
    )
    n=len(vp['r']); m=n-1
    z0=np.zeros(B.shape[1],float)
    x0=np.zeros(2*m,float)
    F0=np.asarray(fun_x(x0),float)
    F0norm=float(np.linalg.norm(F0))
    phi0=0.5*float(np.dot(F0,F0))

    J0=r19c3.selected_jacobian(fun_x,x0,n,B)
    step0,dz0,dx0=r19c.direct_gelsy_step(J0,F0,B)
    xfull=np.asarray(B@dz0,float).ravel()
    Ffull=np.asarray(fun_x(xfull),float)
    full_ratio=float(np.linalg.norm(Ffull)/max(F0norm,TINY))

    accepted=None
    trials=[]
    for alpha in r19c.ALPHAS:
        zt=alpha*dz0
        xt=np.asarray(B@zt,float).ravel()
        if (
            not np.all(np.isfinite(xt))
            or np.max(np.abs(xt[:m]))>r19c.SAFETY_BOUND
            or np.max(np.abs(xt[m:]))>r19c.SAFETY_BOUND
        ):
            trials.append({'alpha':float(alpha),'accepted':False,'reason':'safety_or_nonfinite'})
            continue
        Ft=np.asarray(fun_x(xt),float)
        if not np.all(np.isfinite(Ft)):
            trials.append({'alpha':float(alpha),'accepted':False,'reason':'nonfinite_residual'})
            continue
        phit=0.5*float(np.dot(Ft,Ft))
        armijo=bool(phit<=phi0*(1.0-r19c.ARMIJO_C*alpha))
        trials.append({
            'alpha':float(alpha),'accepted':armijo,
            'phi_trial':float(phit),
            'residual_L2_trial':float(np.linalg.norm(Ft)),
        })
        if armijo:
            accepted=(float(alpha),np.asarray(zt,float),xt,Ft,float(phit))
            break
    if accepted is None:
        raise RuntimeError(f'first Repair19c3 step did not reproduce an accepted state scale={scale} Nr={nr}')

    alpha1,z1,x1,F1,phi1=accepted
    frozen_h0=frozen['history'][0]
    frozen_direct=frozen_h0['direct_step']
    frozen_ratio=first_step_ratio_from_frozen(frozen)

    checks=[]
    for key,obs,fr in (
        ('rank',step0['rank'],frozen_direct['rank']),
        ('predicted_relative_residual',step0['predicted_relative_residual'],frozen_direct['predicted_relative_residual']),
        ('max_abs_yL',step0['max_abs_step_yL'],frozen_direct['max_abs_step_yL']),
        ('max_abs_qRt',step0['max_abs_step_qRt'],frozen_direct['max_abs_step_qRt']),
        ('exact_full_step_frozen_residual_ratio',full_ratio,frozen_ratio),
    ):
        if key=='rank':
            ok=int(obs)==int(fr); ae=float(abs(int(obs)-int(fr))); re=ae/max(abs(float(obs)),abs(float(fr)),1.0)
        else:
            ok,ae,re=r19c.smatch(obs,fr,r19c.FIRST_STEP_LIMIT)
        checks.append({
            'key':key,'pass':bool(ok),'observed':float(obs),'frozen':float(fr),
            'abs_error':float(ae),'relative_error':float(re),
        })

    accepted_alpha_match,alpha_ae,alpha_re=r19c.smatch(alpha1,frozen_h0['accepted_alpha'],r19c.FIRST_STEP_LIMIT)
    residual_match,res_ae,res_re=r19c.smatch(
        np.linalg.norm(F1),frozen_h0['residual_L2_after'],r19c.FIRST_STEP_LIMIT
    )
    checks_extra=[
        {'key':'accepted_alpha','pass':bool(accepted_alpha_match),'observed':float(alpha1),
         'frozen':float(frozen_h0['accepted_alpha']),'abs_error':alpha_ae,'relative_error':alpha_re},
        {'key':'accepted_residual_L2','pass':bool(residual_match),'observed':float(np.linalg.norm(F1)),
         'frozen':float(frozen_h0['residual_L2_after']),'abs_error':res_ae,'relative_error':res_re},
    ]

    st1,ev1,freeze1,freeze_rows1=evaluate_x(x1)
    gy,gq=r19.gauge_values(x1)
    inv_ok=bool(
        ev1.get('finite',False)
        and float(ev1['qerr'])<=r19c.Q_LIMIT
        and abs(gy)<=r19c.GAUGE_LIMIT
        and abs(gq)<=r19c.GAUGE_LIMIT
        and freeze1
    )
    return {
        'vp':vp,'fun_x':fun_x,'evaluate_x':evaluate_x,'n':n,'m':m,
        'z1':z1,'x1':x1,'F1':F1,'state1':st1,'ev1':ev1,
        'first_step':step0,'first_trials':trials,'accepted_alpha':alpha1,
        'reproduction':{
            'checks':checks,
            'extra_state_checks':checks_extra,
            'pass':bool(all(c['pass'] for c in checks) and all(c['pass'] for c in checks_extra)),
        },
        'invariants':{
            'pass':inv_ok,
            'Q_target_max_normalized_error':float(ev1['qerr']) if ev1.get('finite',False) else None,
            'Y4_residual':float(gy),'Qmean_residual':float(gq),
            'field_freeze_pass':bool(freeze1),'field_freeze':freeze_rows1,
            'max_epsilon_H':float(ev1['maxH']) if ev1.get('finite',False) else None,
            'max_epsilon_M':float(ev1['maxM']) if ev1.get('finite',False) else None,
        },
    }


def directional_reference(problem,B):
    fun_x=problem['fun_x']; evaluate_x=problem['evaluate_x']
    n=problem['n']; m=problem['m']; x1=problem['x1']; F1=problem['F1']

    Jctrl=candidate_jacobian(fun_x,x1,n,B,CONTROL_STEP)
    control_step,dz2,dx2=r19c.direct_gelsy_step(Jctrl,F1,B)
    n2=float(np.linalg.norm(dx2))
    direction_ok=bool(control_step['finite'] and np.isfinite(n2) and n2>0.0)
    if not direction_ok:
        return {
            'direction_ok':False,'control_step':control_step,'physical_step_L2':n2,
            'rows':[],'stable_pair':None,'Dstar':None,'vz':None,'vx':None,
        }

    vz=np.asarray(dz2,float)/n2
    vx=np.asarray(B@vz,float).ravel()
    unit_err=float(abs(np.linalg.norm(vx)-1.0))

    rows=[]
    drefs=[]
    all_probe_integrity=True
    for s in DIRECTION_STEPS:
        points={
            'plus':x1+s*vx,
            'minus':x1-s*vx,
            'half_plus':x1+0.5*s*vx,
            'half_minus':x1-0.5*s*vx,
        }
        Fp=np.asarray(fun_x(points['plus']),float)
        Fm=np.asarray(fun_x(points['minus']),float)
        Fhp=np.asarray(fun_x(points['half_plus']),float)
        Fhm=np.asarray(fun_x(points['half_minus']),float)
        finite=bool(
            np.all(np.isfinite(Fp)) and np.all(np.isfinite(Fm))
            and np.all(np.isfinite(Fhp)) and np.all(np.isfinite(Fhm))
        )
        D1=(Fp-Fm)/(2.0*s)
        Dh=(Fhp-Fhm)/s
        Dr=(4.0*Dh-D1)/3.0
        drefs.append(Dr)

        inv_rows=[]
        inv_ok=True
        for name,x in points.items():
            st,ev,freeze_ok,freeze_rows=evaluate_x(x)
            gy,gq=r19.gauge_values(x)
            ok=bool(
                ev.get('finite',False)
                and float(ev['qerr'])<=r19c.Q_LIMIT
                and abs(gy)<=r19c.GAUGE_LIMIT
                and abs(gq)<=r19c.GAUGE_LIMIT
                and freeze_ok
            )
            inv_ok &= ok
            inv_rows.append({
                'point':name,'pass':ok,
                'Q_target_max_normalized_error':float(ev['qerr']) if ev.get('finite',False) else None,
                'Y4_residual':float(gy),'Qmean_residual':float(gq),
                'field_freeze_pass':bool(freeze_ok),
            })
        all_probe_integrity &= bool(finite and inv_ok and np.all(np.isfinite(Dr)))
        corr=float(np.linalg.norm(Dh-D1)/max(np.linalg.norm(Dr),TINY))
        rows.append({
            's':float(s),'finite':finite,'invariants_pass':bool(inv_ok),
            'D1_L2':float(np.linalg.norm(D1)),
            'Dhalf_L2':float(np.linalg.norm(Dh)),
            'Dref_L2':float(np.linalg.norm(Dr)),
            'Dref_H_L2':block_norm(Dr,m,'H'),
            'Dref_M_L2':block_norm(Dr,m,'M'),
            'Richardson_correction_relative':corr,
            'invariants':inv_rows,
        })

    stable_pair=None
    pair_rows=[]
    for i in range(len(DIRECTION_STEPS)-1):
        a=drefs[i]; b=drefs[i+1]
        r=float(np.linalg.norm(a-b)/max(np.linalg.norm(b),TINY))
        rM=float(np.linalg.norm(a[m:]-b[m:])/max(np.linalg.norm(b[m:]),TINY))
        ok=bool(np.isfinite(r) and np.isfinite(rM) and r<=REFERENCE_STABILITY_LIMIT and rM<=REFERENCE_STABILITY_LIMIT)
        pr={
            's_large':float(DIRECTION_STEPS[i]),'s_small':float(DIRECTION_STEPS[i+1]),
            'relative_change_full':r,'relative_change_M':rM,'stable':ok,
        }
        pair_rows.append(pr)
        if stable_pair is None and ok:
            stable_pair={**pr,'index_small':int(i+1)}

    Dstar=None if stable_pair is None else drefs[stable_pair['index_small']]
    return {
        'direction_ok':True,
        'control_step':control_step,
        'physical_step_L2':n2,
        'physical_unit_norm_error':unit_err,
        'rows':rows,
        'pair_rows':pair_rows,
        'stable_pair':stable_pair,
        'Dstar':Dstar,'vz':vz,'vx':vx,
        'probe_integrity_pass':bool(all_probe_integrity),
    }


def audit_candidates(problem,B,reference):
    fun_x=problem['fun_x']; evaluate_x=problem['evaluate_x']
    n=problem['n']; m=problem['m']; x1=problem['x1']; F1=problem['F1']
    Dstar=reference['Dstar']; vz=reference['vz']
    rows=[]
    for abs_step in CANDIDATE_STEPS:
        J=candidate_jacobian(fun_x,x1,n,B,abs_step)
        jac_finite=bool(np.all(np.isfinite(J)))
        if vz is not None:
            action=np.asarray(J@vz,float)
            action_finite=bool(np.all(np.isfinite(action)))
        else:
            action=None; action_finite=False

        mismatch=Hmis=Mmis=None
        if Dstar is not None and action is not None and action_finite:
            mismatch=float(np.linalg.norm(action-Dstar)/max(np.linalg.norm(Dstar),TINY))
            Hmis=float(np.linalg.norm(action[:m]-Dstar[:m])/max(np.linalg.norm(Dstar[:m]),TINY))
            Mmis=float(np.linalg.norm(action[m:]-Dstar[m:])/max(np.linalg.norm(Dstar[m:]),TINY))

        step,dz,dx=r19c.direct_gelsy_step(J,F1,B)
        xt=np.asarray(x1+dx,float)
        Ft=np.asarray(fun_x(xt),float)
        st,ev,freeze_ok,freeze_rows=evaluate_x(xt)
        gy,gq=r19.gauge_values(xt)
        trial_finite=bool(np.all(np.isfinite(Ft)) and ev.get('finite',False))
        trial={
            'attempted':True,
            'finite':trial_finite,
            'rank':int(step['rank']),
            'predicted_relative_residual':float(step['predicted_relative_residual']),
            'exact_frozen_residual_ratio':float(np.linalg.norm(Ft)/max(np.linalg.norm(F1),TINY)) if np.all(np.isfinite(Ft)) else None,
            'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else None,
            'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else None,
            'physical_correction_L2':float(np.linalg.norm(dx)),
            'max_abs_delta_yL':float(np.max(np.abs(dx[:m]))),
            'max_abs_delta_qRt':float(np.max(np.abs(dx[m:]))),
            'Q_target_max_normalized_error':float(ev['qerr']) if ev.get('finite',False) else None,
            'Y4_residual':float(gy),'Qmean_residual':float(gq),
            'field_freeze_pass':bool(freeze_ok),
            'invariants_pass':bool(
                ev.get('finite',False)
                and float(ev['qerr'])<=r19c.Q_LIMIT
                and abs(gy)<=r19c.GAUGE_LIMIT
                and abs(gq)<=r19c.GAUGE_LIMIT
                and freeze_ok
            ),
        }
        rows.append({
            'abs_step':float(abs_step),'method':METHOD,
            'jacobian_finite':jac_finite,'action_finite':action_finite,
            'directional_action_mismatch':mismatch,
            'H_action_mismatch':Hmis,'M_action_mismatch':Mmis,
            'one_step_probe':trial,
        })
    return rows


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
    ap.add_argument('--repair19c3-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

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
        'repair19c3_json':sha256_file(a.repair19c3_json),
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
        'repair19c2_json':r19c3.R19C2_JSON_SHA256,
        'repair19c3_json':R19C3_JSON_SHA256,
    }

    p16=json.loads(Path(a.repair16_json).read_text())
    p19c3=json.loads(Path(a.repair19c3_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    expected_r19c3_gates={
        'R19C3_G1_exact_frozen_provenance':True,
        'R19C3_G2_orthonormal_constrained_basis':True,
        'R19C3_G3_exact_parent_reproduction':True,
        'R19C3_G4_selected_first_step_reproduction':True,
        'R19C3_G5_exact_canonical_nonlinear_closure':False,
        'R19C3_G6_second_order_correction_scaling':False,
        'R19C3_G7_two_grid_correction_amplitude':True,
        'R19C3_G8_all_branch_lambda1_exact_closure':False,
        'R19C3_G9_field_freeze_invariant':True,
        'R19C3_G10_output_integrity':True,
        'R19C3_G11_claim_boundary':True,
    }
    g1=bool(
        hashes==expected
        and p19c3.get('classification')==R19C3_CLASS
        and p19c3.get('gates')==expected_r19c3_gates
        and p19c3.get('summary',{}).get('canonical_pass_count')==0
        and p19c3.get('summary',{}).get('canonical_total')==24
        and p19c3.get('summary',{}).get('lambda1_pass_count')==0
        and p19c3.get('solver',{}).get('jacobian_method')==METHOD
        and float(p19c3.get('solver',{}).get('jacobian_abs_step',0.0))==CONTROL_STEP
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
    basis_ok=True
    for nr in (256,512):
        br,Bc,Bo=r19a.basis_audit(nr)
        ok=bool(
            br['pass']
            and br['orth']['GB_Frobenius']<=r19c.GAUGE_LIMIT
            and br['orth']['orthonormality_Frobenius']<=r19c.GAUGE_LIMIT
            and abs(br['orth']['condition_number']-1.0)<=r19c.REPRO_LIMIT
        )
        basis_ok &= ok
        bases[nr]=Bo
        basis_rows.append({'Nr':nr,'audit':br,'pass':ok})
    g1=bool(g1 and basis_ok)

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
    parent_ok=True
    for scale in b4.SCALES:
        for nr in (256,512):
            ev=r18a.source_arrays(states[(scale,nr)],r19c.CANON_KIND,r19c.CANON_BETA,qbg,zbg,funcs,dY)
            fr=frozen16[(float(scale),nr,r19c.CANON_KIND,r19c.CANON_BETA)]
            ph,ah,rh=r19c.smatch(ev['maxH'],fr['max_epsilon_H'])
            pm,am,rm=r19c.smatch(ev['maxM'],fr['max_epsilon_M'])
            ok=bool(ev.get('finite',False) and ph and pm)
            parent_ok &= ok
            parent_repro.append({
                'scale_hinv_Mpc':float(scale),'Nr':nr,'pass':ok,
                'H_abs_error':ah,'H_relative_error':rh,
                'M_abs_error':am,'M_relative_error':rm,
            })
    g1=bool(g1 and parent_ok)

    frozen_rows=frozen_lambda1_rows(p19c3)
    case_rows=[]
    g2=True
    g3=True
    g4=True
    g5=True
    g6=True
    all_references_resolved=True

    for scale in b4.SCALES:
        for nr in (256,512):
            problem=reproduce_first_state(
                states[(scale,nr)],scale,nr,h,qbg,zbg,funcs,dY,bases[nr],
                frozen_rows[(float(scale),nr)]
            )
            g2 &= bool(problem['reproduction']['pass'])
            g3 &= bool(problem['invariants']['pass'])

            ref=directional_reference(problem,bases[nr])
            g4 &= bool(
                ref['direction_ok']
                and ref.get('probe_integrity_pass',False)
                and len(ref['rows'])==len(DIRECTION_STEPS)
            )
            g5 &= bool(ref['direction_ok'] and len(ref.get('pair_rows',[]))==len(DIRECTION_STEPS)-1)
            resolved=bool(ref.get('stable_pair') is not None)
            all_references_resolved &= resolved

            cand=audit_candidates(problem,bases[nr],ref)
            g6 &= bool(
                len(cand)==len(CANDIDATE_STEPS)
                and all(c['jacobian_finite'] and c['action_finite'] for c in cand)
                and (
                    (not resolved)
                    or all(
                        c['directional_action_mismatch'] is not None
                        and np.isfinite(c['directional_action_mismatch'])
                        and np.isfinite(c['H_action_mismatch'])
                        and np.isfinite(c['M_action_mismatch'])
                        for c in cand
                    )
                )
            )

            case_rows.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                'first_state_reproduction':problem['reproduction'],
                'x1_invariants':problem['invariants'],
                'control_post_step':{
                    'direction_ok':ref['direction_ok'],
                    'direct_step':ref['control_step'],
                    'physical_step_L2':ref['physical_step_L2'],
                    'physical_unit_norm_error':ref.get('physical_unit_norm_error'),
                },
                'directional_reference_rows':ref['rows'],
                'reference_pair_rows':ref.get('pair_rows',[]),
                'stable_reference_pair':ref.get('stable_pair'),
                'reference_resolved':resolved,
                'candidates':cand,
            })

    g2=bool(g2 and len(case_rows)==6)
    g3=bool(g3 and len(case_rows)==6)
    g4=bool(g4 and len(case_rows)==6)
    g5=bool(g5 and len(case_rows)==6)
    g6=bool(g6 and len(case_rows)==6)

    aggregates=[]
    selected=None
    g7=True
    if all_references_resolved:
        for abs_step in CANDIDATE_STEPS:
            rr=[
                next(c for c in row['candidates'] if float(c['abs_step'])==float(abs_step))
                for row in case_rows
            ]
            full=np.asarray([c['directional_action_mismatch'] for c in rr],float)
            mom=np.asarray([c['M_action_mismatch'] for c in rr],float)
            agg={
                'method':METHOD,'abs_step':float(abs_step),
                'max_directional_action_mismatch':float(np.max(full)),
                'median_directional_action_mismatch':float(np.median(full)),
                'max_M_action_mismatch':float(np.max(mom)),
                'median_M_action_mismatch':float(np.median(mom)),
            }
            aggregates.append(agg)
        selected=min(
            aggregates,
            key=lambda a:(
                a['max_directional_action_mismatch'],
                a['max_M_action_mismatch'],
                a['median_directional_action_mismatch'],
                a['median_M_action_mismatch'],
                -a['abs_step'],
            )
        )
        g7=bool(len(aggregates)==len(CANDIDATE_STEPS) and selected is not None)
    else:
        selected=None
        g7=bool(len(aggregates)==0)

    g8=bool(
        len(case_rows)==6
        and sum(len(row['candidates']) for row in case_rows)==54
        and all(c['one_step_probe'].get('attempted',False) for row in case_rows for c in row['candidates'])
    )

    control_agg=None
    if aggregates:
        control_agg=next(a for a in aggregates if float(a['abs_step'])==CONTROL_STEP)

    material=False
    material_checks={
        'all_six_references_resolved':bool(all_references_resolved),
        'selected_exists':bool(selected is not None),
        'selected_full_mismatch_le_1e3':False,
        'selected_M_mismatch_le_1e3':False,
        'selected_is_new_step':False,
        'fivefold_full_mismatch_improvement':False,
        'control_not_already_within_both_1e3_bounds':False,
    }
    if selected is not None and control_agg is not None:
        material_checks.update({
            'selected_full_mismatch_le_1e3':bool(selected['max_directional_action_mismatch']<=FIDELITY_LIMIT),
            'selected_M_mismatch_le_1e3':bool(selected['max_M_action_mismatch']<=FIDELITY_LIMIT),
            'selected_is_new_step':bool(float(selected['abs_step'])!=CONTROL_STEP),
            'fivefold_full_mismatch_improvement':bool(
                selected['max_directional_action_mismatch']
                <= control_agg['max_directional_action_mismatch']/IMPROVEMENT_FACTOR
            ),
            'control_not_already_within_both_1e3_bounds':bool(
                not (
                    control_agg['max_directional_action_mismatch']<=FIDELITY_LIMIT
                    and control_agg['max_M_action_mismatch']<=FIDELITY_LIMIT
                )
            ),
        })
        material=bool(all(material_checks.values()))

    claim_boundary={
        'nonlinear_iteration_beyond_single_candidate_probe':False,
        'line_search_after_x1':False,
        'corrected_state_certified':False,
        'state_npz_written':False,
        'physical_projection_pair_changed':False,
        'physical_field_added':False,
        'gauge_changed':False,
        'source_dictionary_changed':False,
        'coefficient_changed':False,
        'sign_changed':False,
        'finite_eta_executed':False,
        'branch_definition_changed':False,
        'historical_threshold_changed':False,
        'radial_points_removed':False,
        'candidate_selected_from_exact_closure':False,
        'time_evolution_run':False,
        'observational_claimed':False,
        'historical_result_relabelled':False,
    }
    g9=bool(not any(claim_boundary.values()))

    gates={
        'R19C4_G1_exact_frozen_provenance':bool(g1),
        'R19C4_G2_exact_first_step_reproduction':bool(g2),
        'R19C4_G3_exact_gauge_Q_field_freeze_at_x1':bool(g3),
        'R19C4_G4_complete_directional_reference_sweep':bool(g4),
        'R19C4_G5_deterministic_reference_window_evaluation':bool(g5),
        'R19C4_G6_complete_candidate_Jacobian_audit':bool(g6),
        'R19C4_G7_deterministic_candidate_selection':bool(g7),
        'R19C4_G8_complete_single_step_descriptive_cross_check':bool(g8),
        'R19C4_G9_claim_boundary':bool(g9),
    }
    impl_ok=bool(all(gates.values()))
    if not impl_ok:
        classification='NL1C7B4_REPAIR19C4_IMPLEMENTATION_FAIL'; rc=2
    elif material:
        classification='NL1C7B4_REPAIR19C4_POST_FIRST_STEP_DERIVATIVE_WINDOW_IDENTIFIED'; rc=0
    else:
        classification='NL1C7B4_REPAIR19C4_NO_MATERIAL_POST_FIRST_STEP_DERIVATIVE_WINDOW'; rc=0

    result={
        'classification':classification,
        'scope':'Terminal post-first-step derivative-scale characterization after the first accepted Repair19c3 step; no nonlinear closure iteration, physics change, threshold change or state certification.',
        'provenance':{
            **hashes,
            'repair19c3_result_freeze_commit':R19C3_FREEZE_COMMIT,
            'repair19c3_execution_head':R19C3_EXECUTION_HEAD,
            'repair19c3_implementation_blob':R19C3_IMPLEMENTATION_BLOB,
            'repair19c4_initial_prereg_commit':PREREG_INITIAL_COMMIT,
            'repair19c4_prereg_commit':PREREG_COMMIT,
        },
        'frozen_diagnostic':{
            'method':METHOD,
            'control_abs_step':CONTROL_STEP,
            'directional_amplitudes':list(DIRECTION_STEPS),
            'candidate_abs_steps':list(CANDIDATE_STEPS),
            'reference_stability_limit':REFERENCE_STABILITY_LIMIT,
            'fidelity_limit':FIDELITY_LIMIT,
            'required_improvement_factor':IMPROVEMENT_FACTOR,
            'candidate_selection':'lexicographic: max full mismatch, max M mismatch, median full mismatch, median M mismatch, larger abs_step on exact tie',
            'candidate_selection_uses_exact_one_step_residual':False,
        },
        'basis_rows':basis_rows,
        'parent_reproduction':parent_repro,
        'case_rows':case_rows,
        'candidate_aggregates':aggregates,
        'selected_candidate':selected,
        'control_aggregate':control_agg,
        'material_derivative_window_checks':material_checks,
        'material_derivative_window_identified':bool(material),
        'final_nonlinear_closure_execution_licensed':bool(impl_ok and material),
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'cases':len(case_rows),
            'references_resolved':int(sum(row['reference_resolved'] for row in case_rows)),
            'all_references_resolved':bool(all_references_resolved),
            'candidate_case_probes':int(sum(len(row['candidates']) for row in case_rows)),
            'selected_abs_step':None if selected is None else float(selected['abs_step']),
            'selected_max_full_mismatch':None if selected is None else float(selected['max_directional_action_mismatch']),
            'selected_max_M_mismatch':None if selected is None else float(selected['max_M_action_mismatch']),
            'control_max_full_mismatch':None if control_agg is None else float(control_agg['max_directional_action_mismatch']),
            'control_max_M_mismatch':None if control_agg is None else float(control_agg['max_M_action_mismatch']),
            'material_window':bool(material),
        },
        'project_decision_boundary':{
            'further_fd_scale_diagnostics_licensed':False,
            'one_final_nonlinear_closure_execution_licensed':bool(impl_ok and material),
            'physical_infeasibility_claimed_if_no_window':False,
            'eta0_evolution_certified':False,
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
