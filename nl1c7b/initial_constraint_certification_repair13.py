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
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair12 as r12

R8_JSON_SHA256='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA256='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R10_JSON_SHA256='f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d'
R11_JSON_SHA256='48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d'
R12_JSON_SHA256='99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c'
R10_CLASS='NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS'
R11_CLASS='NL1C7B4_REPAIR11_ESECTOR_ANALYTIC_COVARIANT_AUDIT_PASS'
R12_CLASS='NL1C7B4_REPAIR12_FULL_CONSTRAINT_FIRST_ORDER_RESIDUAL'
REPRO_LIMIT=1e-12
CLOSURE_LIMIT=1e-12
PROJECTION_LIMIT=1e-12
LAMBDAS=(1.0,0.5,0.25,0.125)
KINDS=('Simple','Exponential','Sharp')
BETAS=(1.0,0.5,0.1)
SOURCE_NAMES=r12.SOURCE_NAMES


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


def norm_error(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    den=max(float(np.linalg.norm(b)),float(np.linalg.norm(a)),1e-300)
    return float(np.linalg.norm(a-b))/den


def order_label(norms):
    if all(float(x)<=1e-24 for x in norms):
        return 'numerically_zero', [None,None,None]
    slopes=[]
    for x,y in zip(norms[:-1],norms[1:]):
        if x>0 and y>0 and np.isfinite(x) and np.isfinite(y):
            slopes.append(float(math.log(x/y,2.0)))
        else:
            slopes.append(None)
    gated=slopes[1:]
    if all(p is not None and 0.8<=p<=1.2 for p in gated):
        label='first_order_like'
    elif all(p is not None and 1.8<=p<=2.2 for p in gated):
        label='second_order_like'
    else:
        label='higher_or_mixed'
    return label,slopes


def key(row):
    return (float(row['scale_hinv_Mpc']),int(row['Nr']),str(row['Y_kind']),float(row['beta0']))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair08-json',required=True)
    ap.add_argument('--repair08-npz',required=True)
    ap.add_argument('--repair10-json',required=True)
    ap.add_argument('--repair11-json',required=True)
    ap.add_argument('--repair12-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    cov=json.loads(Path(a.coverage_json).read_text())
    r8j=json.loads(Path(a.repair08_json).read_text())
    r10j=json.loads(Path(a.repair10_json).read_text())
    r11j=json.loads(Path(a.repair11_json).read_text())
    r12j=json.loads(Path(a.repair12_json).read_text())
    off=np.load(a.repair08_npz)

    hashes={
        'repair08_json_sha256':sha256_file(a.repair08_json),
        'repair08_npz_sha256':sha256_file(a.repair08_npz),
        'repair10_json_sha256':sha256_file(a.repair10_json),
        'repair11_json_sha256':sha256_file(a.repair11_json),
        'repair12_json_sha256':sha256_file(a.repair12_json),
    }

    z=rec.read_trace(a.trace)
    ks,gs=rec.groups(z)
    tv_rec=rec.at_ai(gs,'pchip')
    ks_b4,gs_b4=b4.groups(b4.read_trace(a.trace))
    tv_b4=b4.at_ai(gs_b4)
    h=float(cov['h'])

    g1=bool(
        hashes['repair08_json_sha256']==R8_JSON_SHA256
        and hashes['repair08_npz_sha256']==R8_NPZ_SHA256
        and hashes['repair10_json_sha256']==R10_JSON_SHA256
        and hashes['repair11_json_sha256']==R11_JSON_SHA256
        and hashes['repair12_json_sha256']==R12_JSON_SHA256
        and r8j.get('classification')=='NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED'
        and len(r8j.get('gates',{}))==10 and all(r8j['gates'].values())
        and r10j.get('classification')==R10_CLASS
        and len(r10j.get('gates',{}))==6 and all(r10j['gates'].values())
        and r11j.get('classification')==R11_CLASS
        and len(r11j.get('gates',{}))==8 and all(r11j['gates'].values())
        and r12j.get('classification')==R12_CLASS
        and r12j.get('gates',{}).get('R12_G5_full_Hamiltonian_asymptotic_second_order_scaling') is False
        and r12j.get('gates',{}).get('R12_G6_full_momentum_asymptotic_second_order_scaling') is True
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

    r10rows={key(x):x for x in r10j.get('localization_rows',[])}
    r12rows={key(x):x for x in r12j.get('order_audit_rows',[])}

    rows=[]
    g2=bool(kidentity and len(r10rows)==54 and len(r12rows)==54)
    g3=True
    g4=True
    g5=True
    g6=True
    g7=True

    closure_max=0.0
    coeff_closure_max=0.0
    projection_sum_error_max=0.0
    dominant_counts={}
    order_label_counts={name:{} for name in SOURCE_NAMES}

    for scale in b4.SCALES:
        for nr in (256,512):
            st=states[(float(scale),int(nr))]
            for kind in KINDS:
                for beta in BETAS:
                    k=(float(scale),int(nr),kind,float(beta))
                    fr10=r10rows.get(k); fr12=r12rows.get(k)
                    if fr10 is None or fr12 is None:
                        g2=False; g6=False
                        continue

                    e0=r12.source_matrices(st,0.0,qbg,zbg,funcs,dY,kind,beta)
                    non=e0['noncenter']
                    baseCH=e0['CH'][:,non]
                    baseNum=e0['numH'][non]

                    evals={}
                    source_deltas={name:[] for name in SOURCE_NAMES}
                    source_norms={name:[] for name in SOURCE_NAMES}
                    source_linf={name:[] for name in SOURCE_NAMES}
                    total_norms=[]
                    total_profiles={}
                    per_lambda=[]

                    for lam in LAMBDAS:
                        ev=r12.source_matrices(st,lam,qbg,zbg,funcs,dY,kind,beta)
                        evals[lam]=ev
                        dCH=ev['CH'][:,non]-baseCH
                        dN=ev['numH'][non]-baseNum
                        named=np.sum(dCH,axis=0)
                        ce=norm_error(named,dN)
                        closure_max=max(closure_max,ce)
                        g3 &= bool(np.isfinite(ce) and ce<=CLOSURE_LIMIT)

                        A=dCH/lam
                        Atot=dN/lam
                        Ace=np.sum(A,axis=0)
                        ae=norm_error(Ace,Atot)
                        coeff_closure_max=max(coeff_closure_max,ae)
                        g4 &= bool(np.isfinite(ae) and ae<=CLOSURE_LIMIT)

                        total_profiles[lam]=Atot
                        total_norms.append(float(np.linalg.norm(dN)))
                        srcrow={}
                        for i,name in enumerate(SOURCE_NAMES):
                            prof=dCH[i]
                            source_deltas[name].append(prof)
                            n2=float(np.linalg.norm(prof))
                            ni=float(np.max(np.abs(prof)))
                            source_norms[name].append(n2)
                            source_linf[name].append(ni)
                            srcrow[name]={'delta_L2':n2,'delta_Linf':ni}
                        per_lambda.append({
                            'lambda':float(lam),
                            'total_delta_H_L2':float(np.linalg.norm(dN)),
                            'total_delta_H_Linf':float(np.max(np.abs(dN))),
                            'source_metrics':srcrow,
                            'source_sum_closure_error':ce,
                            'coefficient_sum_closure_error':ae,
                        })

                    # lambda=1 reproduction
                    e1=evals[1.0]
                    non1=e1['noncenter']
                    ih=int(np.argmax(e1['epsH'][non1])+1)
                    expected_eps=float(fr10['max_epsilon_H'])
                    ok_eps,ae_eps,re_eps=rel_or_abs(float(e1['epsH'][ih]),expected_eps)
                    expected_num=float(fr10['H_hotspot']['numerator_signed'])
                    hidx=int(fr10['H_hotspot']['index'])
                    ok_num,ae_num,re_num=rel_or_abs(float(e1['numH'][hidx]),expected_num)
                    g2 &= bool(ok_eps and ok_num)

                    # Total H slope reproduction / first-order-like
                    total_slopes=[]
                    for x,y in zip(total_norms[:-1],total_norms[1:]):
                        total_slopes.append(float(math.log(x/y,2.0)) if x>0 and y>0 else None)
                    total_first=bool(all(p is not None and 0.8<=p<=1.2 for p in total_slopes[1:]))
                    g7 &= total_first
                    r12_slopes=fr12['H_L2_adjacent_log2_slopes']
                    slope_repro=[]
                    for obs,exp in zip(total_slopes,r12_slopes):
                        ok,ae,re=rel_or_abs(obs,exp,REPRO_LIMIT)
                        slope_repro.append({'observed':obs,'repair12':exp,'abs_error':ae,'relative_error':re,'pass':ok})
                        g2 &= ok

                    # Source order labels
                    labels={}
                    source_slopes={}
                    for name in SOURCE_NAMES:
                        label,slopes=order_label(source_norms[name])
                        labels[name]=label
                        source_slopes[name]=slopes
                        order_label_counts[name][label]=order_label_counts[name].get(label,0)+1

                    # Smallest lambda first-order coefficient profiles
                    lam=0.125
                    Atot=total_profiles[lam]
                    ntot=float(np.linalg.norm(Atot))
                    denom2=float(np.dot(Atot,Atot))
                    coeffs=[]
                    Aall=[]
                    for i,name in enumerate(SOURCE_NAMES):
                        Ai=source_deltas[name][-1]/lam
                        Aall.append(Ai)
                        ni=float(np.linalg.norm(Ai))
                        proj=None if denom2==0.0 else float(np.dot(Ai,Atot)/denom2)
                        cos=None if ni==0.0 or ntot==0.0 else float(np.dot(Ai,Atot)/(ni*ntot))
                        conv=norm_error(source_deltas[name][-2]/0.25,Ai) if ni>0.0 else 0.0
                        coeffs.append({
                            'source':name,
                            'order_label':labels[name],
                            'A_L2':ni,
                            'A_Linf':float(np.max(np.abs(Ai))),
                            'projection_fraction':proj,
                            'cosine_with_total':cos,
                            'A_quarter_vs_eighth_relative_L2':conv,
                            'delta_norms_L2':source_norms[name],
                            'delta_norms_Linf':source_linf[name],
                            'adjacent_log2_slopes':source_slopes[name],
                        })
                    Aall=np.asarray(Aall,float)
                    proj_values=[x['projection_fraction'] for x in coeffs if x['projection_fraction'] is not None]
                    psum=float(sum(proj_values)) if proj_values else 0.0
                    perr=abs(psum-1.0) if denom2>0.0 else 0.0
                    projection_sum_error_max=max(projection_sum_error_max,perr)
                    g5 &= bool(np.isfinite(perr) and perr<=PROJECTION_LIMIT)

                    order=np.argsort([x['A_L2'] for x in coeffs])[::-1]
                    dominant=coeffs[int(order[0])]['source']
                    second=coeffs[int(order[1])]['source']
                    dominant_counts[dominant]=dominant_counts.get(dominant,0)+1

                    pair_rows=[]
                    for i in range(len(SOURCE_NAMES)):
                        ni=float(np.linalg.norm(Aall[i]))
                        for j in range(i+1,len(SOURCE_NAMES)):
                            nj=float(np.linalg.norm(Aall[j]))
                            den=ni+nj
                            cij=None if den==0.0 else float(np.linalg.norm(Aall[i]+Aall[j])/den)
                            pair_rows.append({'source_i':SOURCE_NAMES[i],'source_j':SOURCE_NAMES[j],'c_ij':cij})
                    finite_pairs=[x for x in pair_rows if x['c_ij'] is not None and np.isfinite(x['c_ij'])]
                    strongest=min(finite_pairs,key=lambda x:x['c_ij']) if finite_pairs else None
                    sum_norms=float(sum(np.linalg.norm(x) for x in Aall))
                    global_cancel=None if sum_norms==0.0 else ntot/sum_norms

                    rows.append({
                        'scale_hinv_Mpc':float(scale),'Nr':int(nr),'Y_kind':kind,'beta0':float(beta),
                        'lambda1_reproduction':{
                            'max_epsilon_H_observed':float(e1['epsH'][ih]),
                            'max_epsilon_H_repair10':expected_eps,
                            'max_epsilon_H_abs_error':ae_eps,
                            'max_epsilon_H_relative_error':re_eps,
                            'max_epsilon_H_pass':ok_eps,
                            'H_hotspot_numerator_observed':float(e1['numH'][hidx]),
                            'H_hotspot_numerator_repair10':expected_num,
                            'H_hotspot_numerator_abs_error':ae_num,
                            'H_hotspot_numerator_relative_error':re_num,
                            'H_hotspot_numerator_pass':ok_num,
                        },
                        'per_lambda':per_lambda,
                        'total_H_L2_adjacent_log2_slopes':total_slopes,
                        'Repair12_H_slope_reproduction':slope_repro,
                        'total_first_order_like':total_first,
                        'lambda_eighth_first_order_coefficients':coeffs,
                        'projection_sum':psum,
                        'projection_sum_error':perr,
                        'dominant_A_L2_source':dominant,
                        'second_A_L2_source':second,
                        'strongest_cancelling_pair':strongest,
                        'total_A_L2':ntot,
                        'sum_source_A_L2':sum_norms,
                        'global_cancellation_fraction':global_cancel,
                    })

    g6=bool(g6 and len(rows)==54 and all(len(x['lambda_eighth_first_order_coefficients'])==11 and len(x['per_lambda'])==4 for x in rows))
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
    g8=bool(claim_boundary['historical_B4_fail_preserved']
            and not any(v for k,v in claim_boundary.items() if k!='historical_B4_fail_preserved'))

    gates={
        'R13_G1_frozen_provenance':g1,
        'R13_G2_exact_Repair12_lambda1_reproduction':bool(g2),
        'R13_G3_per_source_bookkeeping_closure':bool(g3),
        'R13_G4_first_order_coefficient_closure':bool(g4),
        'R13_G5_projection_closure':bool(g5),
        'R13_G6_complete_source_localization':g6,
        'R13_G7_Repair12_order_reproduction':bool(g7),
        'R13_G8_claim_boundary':g8,
    }
    if all(gates.values()):
        cls='NL1C7B4_REPAIR13_HAMILTONIAN_FIRST_ORDER_SOURCE_LOCALIZATION_PASS'; rc=0
    else:
        cls='NL1C7B4_REPAIR13_IMPLEMENTATION_FAIL'; rc=2

    result={
        'classification':cls,
        'scope':'Repair13 source-by-source localization of the frozen Repair12 first-order Hamiltonian residual; no source/state/model correction.',
        'provenance':{
            **hashes,
            'repair12_result_freeze_commit':'167af8e7b6d610c307b67fed7890fe0547c27bfa',
            'repair13_prereg_commit':'f2bd2d3b693d41680e254d714aec1233502e3ce0',
        },
        'settings':{
            'positive_lambdas':list(LAMBDAS),
            'source_labels':list(SOURCE_NAMES),
            'source_first_order_interval':[0.8,1.2],
            'source_second_order_interval':[1.8,2.2],
            'numerically_zero_L2_threshold':1e-24,
            'closure_limit':CLOSURE_LIMIT,
            'projection_sum_limit':PROJECTION_LIMIT,
        },
        'rows':rows,
        'summary':{
            'n_cases':len(rows),
            'per_source_order_label_counts':order_label_counts,
            'dominant_A_L2_source_counts':dominant_counts,
            'max_source_sum_closure_error':closure_max,
            'max_coefficient_sum_closure_error':coeff_closure_max,
            'max_projection_sum_error':projection_sum_error_max,
            'historical_B4_classification_unchanged':'NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL',
        },
        'state_anchor':{
            'scalar_canonical_vs_independent_at_ai_relative_L2':r9.rel_sym(scalar_ai,scalar_independent),
            'scalar_finite':bool(scalar_finite),
        },
        'gates':gates,
        'claim_boundary':claim_boundary,
        'interpretation_boundary':{
            'source_localized_not_declared_wrong':True,
            'B4_passed':False,
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
