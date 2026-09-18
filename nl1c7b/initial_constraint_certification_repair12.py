#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair02 as r2
import nl1c7b.initial_constraint_certification_repair09 as r9

R8_JSON_SHA256='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA256='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R10_JSON_SHA256='f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d'
R11_JSON_SHA256='48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d'
R10_CLASS='NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS'
R11_CLASS='NL1C7B4_REPAIR11_ESECTOR_ANALYTIC_COVARIANT_AUDIT_PASS'
REPRO_LIMIT=1e-12
CLOSURE_LIMIT=1e-12
SLOPE_MIN=1.8
SLOPE_MAX=2.2
LAMBDAS=(0.0,1.0,0.5,0.25,0.125)
POS_LAMBDAS=(1.0,0.5,0.25,0.125)
KINDS=('Simple','Exponential','Sharp')
BETAS=(1.0,0.5,0.1)
SOURCE_NAMES=(
    'GR_kin','GR_curv_NL','GR_curv_Rr','GR_Nr_boundary',
    'AeST_E2','AeST_EX','AeST_X2','AeST_J','AeST_K','dust','standard_bg'
)


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def rel_or_abs(a,b,tol=REPRO_LIMIT):
    a=float(a); b=float(b)
    ae=abs(a-b)
    re=ae/max(abs(a),abs(b),1e-300)
    return bool(np.isfinite(ae) and np.isfinite(re) and (ae<=tol or re<=tol)),ae,re


def scaled_state_arrays(st,lam,qbg):
    r=np.asarray(st['r'],float)
    D=b4.dmat(r)
    a=b4.AI
    L0=a+np.asarray(st['L_minus_a'],float)
    R0=a*r+np.asarray(st['R_minus_ar'],float)
    Lt0=a*b4.H_DIRECT+np.asarray(st['Ldot_minus_aH'],float)
    Rt0=a*b4.H_DIRECT*r+np.asarray(st['Rdot_minus_aHr'],float)
    u0=np.asarray(st['u'],float)
    ut0=np.asarray(st['udot'],float)
    phi0=np.asarray(st['phi'],float)
    dq0=np.asarray(st['phidot_minus_Q'],float)
    db0=np.asarray(st['delta_b'],float)
    vr0=np.asarray(st['dust_vr'],float)

    L=a+lam*(L0-a)
    R=a*r+lam*(R0-a*r)
    Lt=a*b4.H_DIRECT+lam*(Lt0-a*b4.H_DIRECT)
    Rt=a*b4.H_DIRECT*r+lam*(Rt0-a*b4.H_DIRECT*r)
    u=lam*u0
    ut=lam*ut0
    phi=lam*phi0
    dq=lam*dq0
    db=lam*db0
    dust_vr=lam*vr0

    pr=D@phi
    Lr=D@L
    Rr=D@R
    ur=D@u
    c=np.cosh(u)
    s=np.sinh(u)
    qtarget=qbg+dq
    pt=(qtarget-s*pr/L)/c
    qexact=c*pt+s*pr/L

    return {
        'r':r,'D':D,'L':L,'R':R,'Lt':Lt,'Rt':Rt,'u':u,'ut':ut,'phi':phi,
        'dq':dq,'delta_b':db,'dust_vr':dust_vr,'pr':pr,'Lr':Lr,'Rr':Rr,
        'ur':ur,'c':c,'s':s,'pt':pt,'qexact':qexact,
    }


def source_matrices(st,lam,qbg,zbg,funcs,dY,kind,beta):
    v=scaled_state_arrays(st,lam,qbg)
    r=v['r']; D=v['D']; n=len(r)
    L=v['L']; R=v['R']; Lt=v['Lt']; Rt=v['Rt']; u=v['u']; ut=v['ut']
    pr=v['pr']; Lr=v['Lr']; Rr=v['Rr']; ur=v['ur']; c=v['c']; s=v['s']; pt=v['pt']
    args=[L,R,u,Lt,Rt,ut,pt,Lr,Rr,ur,pr]

    base_names=list(funcs.keys())
    if base_names!=list(SOURCE_NAMES[:7]):
        raise RuntimeError(f'unexpected frozen source order: {base_names}')

    CH=[]; CM=[]
    for name in base_names:
        fs=funcs[name]
        fN,fNr,fb,fbr=[r2.arrval(f,args,n) for f in fs]
        fNr=np.array(fNr,copy=True); fbr=np.array(fbr,copy=True)
        fNr[0]=0.0; fbr[0]=0.0
        CH.append(fN-D@fNr)
        CM.append(fb-D@fbr)

    X=s*pt+c*pr/L
    dyN,dyNr,dyb,dybr=[r2.arrval(f,args,n) for f in dY]
    j,J=r1.jJ(kind,np.abs(X)/b4.A0_GEO,beta)
    P=L*R**2
    jN=-b4.C*(P*J+P*j*dyN)
    jNr=-b4.C*(P*j*dyNr)
    jb=-b4.C*(P*j*dyb)
    jbr=-b4.C*(P*j*dybr)
    jNr=np.array(jNr,copy=True); jbr=np.array(jbr,copy=True)
    jNr[0]=0.0; jbr[0]=0.0
    CH.append(jN-D@jNr)
    CM.append(jb-D@jbr)

    z=zbg+v['dq']/b4.Z0
    w=z*z
    with np.errstate(over='ignore',invalid='ignore'):
        ew=np.exp(w)
    kN=4.0*b4.K2*L*R**2*(
        b4.Z0*b4.Z0*np.expm1(w)-2.0*c*pt*b4.Z0*z*ew
    )
    kb=-8.0*b4.K2*L*R**2*c*pr*b4.Z0*z*ew
    CH.append(kN); CM.append(kb)

    rapid=np.arctanh(v['dust_vr'])
    varrho=b4.VAR_B*(1.0+v['delta_b'])
    CH.append(-2.0*L*R**2*varrho*np.cosh(rapid)**2)
    CM.append(2.0*L**2*R**2*varrho*np.cosh(rapid)*np.sinh(rapid))

    CH.append(-2.0*L*R**2*b4.RHO_STD)
    CM.append(np.zeros(n))

    CH=np.asarray(CH,float); CM=np.asarray(CM,float)
    if CH.shape!=(11,n) or CM.shape!=(11,n):
        raise RuntimeError('invalid source matrix shape')
    noncenter=np.arange(n)>0
    if not (
        np.all(np.isfinite(CH[:,noncenter]))
        and np.all(np.isfinite(CM[:,noncenter]))
        and np.all(np.isfinite(v['qexact'][noncenter]))
    ):
        raise RuntimeError(f'nonfinite source matrix lambda={lam} {kind} beta={beta}')

    numH=np.sum(CH,axis=0)
    numM=np.sum(CM,axis=0)
    denH=np.sum(np.abs(CH),axis=0)
    denM=np.sum(np.abs(CM),axis=0)
    floorH=1e-14*float(np.max(denH[noncenter]))
    floorM=1e-14*float(np.max(denM[noncenter]))
    epsH=np.abs(numH)/(denH+floorH)
    epsM=np.abs(numM)/(denM+floorM)

    namedH=np.zeros(n); namedM=np.zeros(n)
    for i,name in enumerate(SOURCE_NAMES):
        namedH=namedH+CH[i]
        namedM=namedM+CM[i]
    closeH=np.abs(numH-namedH)/(denH+floorH)
    closeM=np.abs(numM-namedM)/(denM+floorM)

    return {
        'CH':CH,'CM':CM,'numH':numH,'numM':numM,'denH':denH,'denM':denM,
        'epsH':epsH,'epsM':epsM,'closureH':closeH,'closureM':closeM,
        'r':r,'noncenter':noncenter,
    }


def row_key(row):
    return (float(row['scale_hinv_Mpc']),int(row['Nr']),str(row['Y_kind']),float(row['beta0']))


def slope_series(norms):
    vals=[]
    for x,y in zip(norms[:-1],norms[1:]):
        if x>0 and y>0 and np.isfinite(x) and np.isfinite(y):
            vals.append(float(math.log(x/y,2.0)))
        else:
            vals.append(None)
    return vals


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair08-json',required=True)
    ap.add_argument('--repair08-npz',required=True)
    ap.add_argument('--repair10-json',required=True)
    ap.add_argument('--repair11-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    cov=json.loads(Path(a.coverage_json).read_text())
    r8j=json.loads(Path(a.repair08_json).read_text())
    r10j=json.loads(Path(a.repair10_json).read_text())
    r11j=json.loads(Path(a.repair11_json).read_text())
    off=np.load(a.repair08_npz)

    h8j=sha256_file(a.repair08_json)
    h8n=sha256_file(a.repair08_npz)
    h10=sha256_file(a.repair10_json)
    h11=sha256_file(a.repair11_json)

    z=rec.read_trace(a.trace)
    ks,gs=rec.groups(z)
    tv_rec=rec.at_ai(gs,'pchip')
    ks_b4,gs_b4=b4.groups(b4.read_trace(a.trace))
    tv_b4=b4.at_ai(gs_b4)
    h=float(cov['h'])

    g1=bool(
        h8j==R8_JSON_SHA256 and h8n==R8_NPZ_SHA256
        and h10==R10_JSON_SHA256 and h11==R11_JSON_SHA256
        and r8j.get('classification')=='NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED'
        and len(r8j.get('gates',{}))==10 and all(r8j['gates'].values())
        and r10j.get('classification')==R10_CLASS
        and len(r10j.get('gates',{}))==6 and all(r10j['gates'].values())
        and r11j.get('classification')==R11_CLASS
        and len(r11j.get('gates',{}))==8 and all(r11j['gates'].values())
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
        and len(ks)==128 and np.array_equal(ks,ks_b4)
    )

    scalar_ai,scalar_independent,scalar_finite,_=r8.scalar_composites_at_ai(ks,gs,'pchip')
    states={}
    for scale in b4.SCALES:
        states[(float(scale),256)]=r9.load_primary_state(off,scale)
        states[(float(scale),512)]=r9.repaired_state_nr(scale,512,ks,h,tv_b4,tv_rec,scalar_ai)

    kq_bg=float(np.median(tv_b4['KQ']))
    qbg=b4.stable_q_from_kq(kq_bg)
    zbg=r9.stable_zbg(kq_bg)
    funcs,dY,kidentity=r1.build_nonK()

    frozen={row_key(x):x for x in r10j.get('localization_rows',[])}
    repro_rows=[]
    audit_rows=[]
    g2=bool(kidentity and len(frozen)==54)
    g3=True
    g4=True
    g5=True
    g6=True
    g7=True

    closure_max_H=0.0
    closure_max_M=0.0
    gated_H=[]
    gated_M=[]
    linf_H_all=[]
    linf_M_all=[]

    for scale in b4.SCALES:
        for nr in (256,512):
            st=states[(float(scale),int(nr))]
            for kind in KINDS:
                for beta in BETAS:
                    key=(float(scale),int(nr),kind,float(beta))
                    fr=frozen.get(key)
                    if fr is None:
                        g2=False
                        continue

                    evaluations={}
                    for lam in LAMBDAS:
                        ev=source_matrices(st,lam,qbg,zbg,funcs,dY,kind,beta)
                        evaluations[lam]=ev
                        non=ev['noncenter']
                        ch=float(np.max(ev['closureH'][non]))
                        cm=float(np.max(ev['closureM'][non]))
                        closure_max_H=max(closure_max_H,ch)
                        closure_max_M=max(closure_max_M,cm)
                        g3 &= bool(np.isfinite(ch) and np.isfinite(cm) and ch<=CLOSURE_LIMIT and cm<=CLOSURE_LIMIT)

                    e1=evaluations[1.0]
                    non=e1['noncenter']
                    ih=int(np.argmax(e1['epsH'][non])+1)
                    im=int(np.argmax(e1['epsM'][non])+1)
                    vals=[
                        ('max_epsilon_H',float(e1['epsH'][ih]),float(fr['max_epsilon_H'])),
                        ('max_epsilon_M',float(e1['epsM'][im]),float(fr['max_epsilon_M'])),
                        ('H_hotspot_numerator',float(e1['numH'][int(fr['H_hotspot']['index'])]),float(fr['H_hotspot']['numerator_signed'])),
                        ('M_hotspot_numerator',float(e1['numM'][int(fr['M_hotspot']['index'])]),float(fr['M_hotspot']['numerator_signed'])),
                    ]
                    rr={'scale_hinv_Mpc':float(scale),'Nr':int(nr),'Y_kind':kind,'beta0':float(beta)}
                    for label,obs,exp in vals:
                        ok,ae,re=rel_or_abs(obs,exp,REPRO_LIMIT)
                        rr[label+'_observed']=obs
                        rr[label+'_repair10']=exp
                        rr[label+'_abs_error']=ae
                        rr[label+'_relative_error']=re
                        rr[label+'_pass']=ok
                        g2 &= ok

                    # E2/EX Repair11 anchor at the stored M hotspot.
                    midx=int(fr['M_hotspot']['index'])
                    for name in ('AeST_E2','AeST_EX'):
                        src_idx=SOURCE_NAMES.index(name)
                        obs=float(e1['CM'][src_idx,midx])
                        exp=float(fr['M_hotspot']['signed_sources'][name])
                        ok,ae,re=rel_or_abs(obs,exp,REPRO_LIMIT)
                        rr[name+'_hotspot_abs_error']=ae
                        rr[name+'_hotspot_relative_error']=re
                        rr[name+'_hotspot_pass']=ok
                        g2 &= ok
                    repro_rows.append(rr)

                    e0=evaluations[0.0]
                    non0=e0['noncenter']
                    baseline_H=e0['numH'][non0]
                    baseline_M=e0['numM'][non0]
                    baseline_finite=bool(np.all(np.isfinite(baseline_H)) and np.all(np.isfinite(baseline_M)))
                    g4 &= baseline_finite

                    normsH=[]; normsM=[]; maxH=[]; maxM=[]
                    lambda_metrics=[]
                    for lam in POS_LAMBDAS:
                        ev=evaluations[lam]
                        nonp=ev['noncenter']
                        dH=ev['numH'][nonp]-baseline_H
                        dM=ev['numM'][nonp]-baseline_M
                        nH=float(np.linalg.norm(dH)); nM=float(np.linalg.norm(dM))
                        mH=float(np.max(np.abs(dH))); mM=float(np.max(np.abs(dM)))
                        normsH.append(nH); normsM.append(nM); maxH.append(mH); maxM.append(mM)
                        lambda_metrics.append({
                            'lambda':float(lam),
                            'deltaN_H_L2':nH,'deltaN_M_L2':nM,
                            'deltaN_H_Linf':mH,'deltaN_M_Linf':mM,
                        })
                    slopesH=slope_series(normsH)
                    slopesM=slope_series(normsM)
                    slopesHinf=slope_series(maxH)
                    slopesMinf=slope_series(maxM)
                    linf_H_all.extend([x for x in slopesHinf if x is not None])
                    linf_M_all.extend([x for x in slopesMinf if x is not None])

                    # Gate only intervals 1/2->1/4 and 1/4->1/8, i.e. slope indices 1 and 2.
                    for p in slopesH[1:]:
                        ok=bool(p is not None and np.isfinite(p) and SLOPE_MIN<=p<=SLOPE_MAX)
                        g5 &= ok
                        if p is not None: gated_H.append(float(p))
                    for p in slopesM[1:]:
                        ok=bool(p is not None and np.isfinite(p) and SLOPE_MIN<=p<=SLOPE_MAX)
                        g6 &= ok
                        if p is not None: gated_M.append(float(p))

                    audit_rows.append({
                        'scale_hinv_Mpc':float(scale),'Nr':int(nr),'Y_kind':kind,'beta0':float(beta),
                        'baseline':{
                            'N_H_noncenter':baseline_H.tolist(),
                            'N_M_noncenter':baseline_M.tolist(),
                            'N_H_L2':float(np.linalg.norm(baseline_H)),
                            'N_M_L2':float(np.linalg.norm(baseline_M)),
                            'N_H_Linf':float(np.max(np.abs(baseline_H))),
                            'N_M_Linf':float(np.max(np.abs(baseline_M))),
                            'finite':baseline_finite,
                        },
                        'lambda_metrics':lambda_metrics,
                        'positive_lambdas':list(POS_LAMBDAS),
                        'H_L2_adjacent_log2_slopes':slopesH,
                        'M_L2_adjacent_log2_slopes':slopesM,
                        'H_Linf_adjacent_log2_slopes':slopesHinf,
                        'M_Linf_adjacent_log2_slopes':slopesMinf,
                        'gated_slope_indices':[1,2],
                        'H_gated_pass':bool(all(p is not None and SLOPE_MIN<=p<=SLOPE_MAX for p in slopesH[1:])),
                        'M_gated_pass':bool(all(p is not None and SLOPE_MIN<=p<=SLOPE_MAX for p in slopesM[1:])),
                    })

    g3=bool(g3 and closure_max_H<=CLOSURE_LIMIT and closure_max_M<=CLOSURE_LIMIT)
    g7=bool(len(audit_rows)==54 and len(repro_rows)==54 and all(len(x['lambda_metrics'])==4 for x in audit_rows))
    claim_boundary={
        'historical_B4_fail_preserved':True,
        'state_written_or_projected':False,
        'nonlinear_constraint_correction_performed':False,
        'coefficient_fitted_or_rescaled':False,
        'source_inserted_or_removed':False,
        'sign_changed':False,
        'K_clipped':False,
        'Q_linearized':False,
        'historical_threshold_changed':False,
        'radial_points_removed':False,
        'Y_beta_or_scale_selected':False,
        'nonlinear_evolution_executed':False,
        'finite_eta_executed':False,
        'B4_pass_relabel_claimed':False,
        'observational_detection_claimed':False,
    }
    g8=bool(r11j.get('classification')==R11_CLASS and all(r11j.get('gates',{}).values())
            and claim_boundary['historical_B4_fail_preserved']
            and not any(v for k,v in claim_boundary.items() if k!='historical_B4_fail_preserved'))

    gates={
        'R12_G1_frozen_provenance':g1,
        'R12_G2_lambda1_exact_Repair10_reproduction':bool(g2),
        'R12_G3_source_bookkeeping_closure':g3,
        'R12_G4_finite_fixed_B3_baseline':bool(g4),
        'R12_G5_full_Hamiltonian_asymptotic_second_order_scaling':bool(g5),
        'R12_G6_full_momentum_asymptotic_second_order_scaling':bool(g6),
        'R12_G7_complete_case_grid_reporting':g7,
        'R12_G8_Repair11_consistency_and_claim_boundary':g8,
    }

    core_impl=bool(g1 and g2 and g3 and g4 and g7 and g8)
    if all(gates.values()):
        cls='NL1C7B4_REPAIR12_FULL_CONSTRAINT_SECOND_ORDER_AUDIT_PASS'; rc=0
    elif core_impl and (not g5 or not g6):
        cls='NL1C7B4_REPAIR12_FULL_CONSTRAINT_FIRST_ORDER_RESIDUAL'; rc=2
    else:
        cls='NL1C7B4_REPAIR12_IMPLEMENTATION_FAIL'; rc=2

    result={
        'classification':cls,
        'scope':'Repair12 perturbative-order audit of the complete signed exact nonlinear B4 Hamiltonian and radial-momentum residual on the frozen Repair08 first-order growing-mode state; no state correction or evolution.',
        'provenance':{
            'repair08_json_sha256':h8j,
            'repair08_npz_sha256':h8n,
            'repair10_json_sha256':h10,
            'repair11_json_sha256':h11,
            'repair11_result_freeze_commit':'559650a2de9bf57a344401ba459adf2268212b81',
            'repair12_prereg_commit':'d1b5c5f3aab13b3929f8c91eeea216724951c5f3',
        },
        'settings':{
            'lambdas':list(LAMBDAS),
            'positive_lambdas':list(POS_LAMBDAS),
            'gated_slope_indices':[1,2],
            'gated_intervals':['1/2->1/4','1/4->1/8'],
            'slope_interval':[SLOPE_MIN,SLOPE_MAX],
            'Repair10_reproduction_limit':REPRO_LIMIT,
            'bookkeeping_closure_limit':CLOSURE_LIMIT,
            'scales_hinv_Mpc':[float(x) for x in b4.SCALES],
            'radial_grids':[256,512],
            'Y_families':list(KINDS),
            'beta_values':list(BETAS),
        },
        'state_anchor':{
            'scalar_canonical_vs_independent_at_ai_relative_L2':r9.rel_sym(scalar_ai,scalar_independent),
            'scalar_finite':bool(scalar_finite),
        },
        'repair10_reproduction':{'rows':repro_rows,'pass':bool(g2)},
        'bookkeeping_closure':{
            'max_H':closure_max_H,'max_M':closure_max_M,'limit':CLOSURE_LIMIT,'pass':g3,
        },
        'order_audit_rows':audit_rows,
        'summary':{
            'n_cases':len(audit_rows),
            'H_gated_min_slope':float(min(gated_H)) if gated_H else None,
            'H_gated_max_slope':float(max(gated_H)) if gated_H else None,
            'M_gated_min_slope':float(min(gated_M)) if gated_M else None,
            'M_gated_max_slope':float(max(gated_M)) if gated_M else None,
            'H_Linf_all_min_slope':float(min(linf_H_all)) if linf_H_all else None,
            'H_Linf_all_max_slope':float(max(linf_H_all)) if linf_H_all else None,
            'M_Linf_all_min_slope':float(min(linf_M_all)) if linf_M_all else None,
            'M_Linf_all_max_slope':float(max(linf_M_all)) if linf_M_all else None,
            'historical_B4_classification_unchanged':'NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL',
        },
        'gates':gates,
        'claim_boundary':claim_boundary,
        'interpretation_boundary':{
            'first_order_constraint_consistency_claim_allowed_if_pass':bool(all(gates.values())),
            'exact_nonlinear_B4_passed':False,
            'nonlinear_constraint_corrected_state_constructed':False,
            'observational_detection_claimed':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
