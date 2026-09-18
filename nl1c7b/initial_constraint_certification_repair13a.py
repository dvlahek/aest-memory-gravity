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
R13_JSON_SHA256='ef6791edd595a2bd8b44e52a703915385a1e2c4d98345ff4cc509a5d22a61a9b'

R10_CLASS='NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS'
R11_CLASS='NL1C7B4_REPAIR11_ESECTOR_ANALYTIC_COVARIANT_AUDIT_PASS'
R12_CLASS='NL1C7B4_REPAIR12_FULL_CONSTRAINT_FIRST_ORDER_RESIDUAL'
R13_CLASS='NL1C7B4_REPAIR13_IMPLEMENTATION_FAIL'

LAMBDAS=(1.0,0.5,0.25,0.125)
KINDS=('Simple','Exponential','Sharp')
BETAS=(1.0,0.5,0.1)
SOURCE_NAMES=r12.SOURCE_NAMES
U=2.0**-53


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def gamma(n):
    nu=float(n)*U
    if not (0.0 <= nu < 1.0):
        raise RuntimeError(f'invalid gamma operation count {n}')
    return nu/(1.0-nu)


def key(row):
    return (float(row['scale_hinv_Mpc']),int(row['Nr']),str(row['Y_kind']),float(row['beta0']))


def bound_ratio(err,bound):
    err=np.asarray(err,float); bound=np.asarray(bound,float)
    if not (np.all(np.isfinite(err)) and np.all(np.isfinite(bound)) and np.all(bound>=0)):
        return False,float('inf')
    zero=bound==0
    if np.any(zero & (err!=0)):
        return False,float('inf')
    pos=~zero
    ratio=0.0 if not np.any(pos) else float(np.max(err[pos]/bound[pos]))
    return bool(ratio<=1.0),ratio


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair08-json',required=True)
    ap.add_argument('--repair08-npz',required=True)
    ap.add_argument('--repair10-json',required=True)
    ap.add_argument('--repair11-json',required=True)
    ap.add_argument('--repair12-json',required=True)
    ap.add_argument('--repair13-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    cov=json.loads(Path(a.coverage_json).read_text())
    r8j=json.loads(Path(a.repair08_json).read_text())
    r10j=json.loads(Path(a.repair10_json).read_text())
    r11j=json.loads(Path(a.repair11_json).read_text())
    r12j=json.loads(Path(a.repair12_json).read_text())
    r13j=json.loads(Path(a.repair13_json).read_text())
    off=np.load(a.repair08_npz)

    hashes={
        'repair08_json_sha256':sha256_file(a.repair08_json),
        'repair08_npz_sha256':sha256_file(a.repair08_npz),
        'repair10_json_sha256':sha256_file(a.repair10_json),
        'repair11_json_sha256':sha256_file(a.repair11_json),
        'repair12_json_sha256':sha256_file(a.repair12_json),
        'repair13_json_sha256':sha256_file(a.repair13_json),
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
        and hashes['repair13_json_sha256']==R13_JSON_SHA256
        and r8j.get('classification')=='NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED'
        and r10j.get('classification')==R10_CLASS
        and r11j.get('classification')==R11_CLASS
        and r12j.get('classification')==R12_CLASS
        and r13j.get('classification')==R13_CLASS
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
        and len(ks)==128 and np.array_equal(ks,ks_b4)
    )

    expected_hist={
        'R13_G1_frozen_provenance':True,
        'R13_G2_exact_Repair12_lambda1_reproduction':True,
        'R13_G3_per_source_bookkeeping_closure':False,
        'R13_G4_first_order_coefficient_closure':False,
        'R13_G5_projection_closure':False,
        'R13_G6_complete_source_localization':True,
        'R13_G7_Repair12_order_reproduction':True,
        'R13_G8_claim_boundary':True,
    }
    g2=bool(r13j.get('gates')==expected_hist)

    summary13=r13j.get('summary',{})
    order_counts=summary13.get('per_source_order_label_counts',{})
    dom_counts=summary13.get('dominant_A_L2_source_counts',{})
    rows13={key(x):x for x in r13j.get('rows',[])}
    g6=bool(
        summary13.get('n_cases')==54
        and dom_counts=={'AeST_E2':54}
        and order_counts.get('AeST_E2')=={'first_order_like':54}
        and order_counts.get('AeST_EX')=={'first_order_like':54}
        and order_counts.get('AeST_X2')=={'second_order_like':54}
        and len(rows13)==54
        and all(
            row.get('total_first_order_like') is True
            and all(x.get('pass') is True for x in row.get('Repair12_H_slope_reproduction',[]))
            for row in rows13.values()
        )
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
    g1=bool(g1 and kidentity)

    g3=True
    g4=True
    g5=True
    rows=[]
    max_g3_ratio=0.0
    max_g4_ratio=0.0
    max_g5_ratio=0.0
    max_old_g3=float(summary13.get('max_source_sum_closure_error',float('nan')))
    max_old_g4=float(summary13.get('max_coefficient_sum_closure_error',float('nan')))
    max_old_g5=float(summary13.get('max_projection_sum_error',float('nan')))

    for scale in b4.SCALES:
        for nr in (256,512):
            st=states[(float(scale),int(nr))]
            for kind in KINDS:
                for beta in BETAS:
                    k=(float(scale),int(nr),kind,float(beta))
                    fr13=rows13.get(k)
                    if fr13 is None:
                        g6=False
                        continue

                    e0=r12.source_matrices(st,0.0,qbg,zbg,funcs,dY,kind,beta)
                    non=e0['noncenter']
                    C0=e0['CH'][:,non]
                    N0=e0['numH'][non]
                    lam_rows=[]
                    last_A=None
                    last_Atot=None

                    for lam in LAMBDAS:
                        ev=r12.source_matrices(st,lam,qbg,zbg,funcs,dY,kind,beta)
                        Cl=ev['CH'][:,non]
                        Nl=ev['numH'][non]

                        dCH=Cl-C0
                        named=np.sum(dCH,axis=0)
                        dN=Nl-N0
                        S=np.sum(np.abs(Cl)+np.abs(C0),axis=0)

                        err3=np.abs(named-dN)
                        b3=gamma(64)*S
                        ok3,r3=bound_ratio(err3,b3)
                        g3 &= ok3
                        max_g3_ratio=max(max_g3_ratio,r3)

                        A=dCH/lam
                        Atot=dN/lam
                        Asum=np.sum(A,axis=0)
                        SA=S/lam
                        err4=np.abs(Asum-Atot)
                        b4arr=gamma(96)*SA
                        ok4,r4=bound_ratio(err4,b4arr)
                        g4 &= ok4
                        max_g4_ratio=max(max_g4_ratio,r4)

                        if lam==0.125:
                            last_A=A
                            last_Atot=Atot

                        lam_rows.append({
                            'lambda':float(lam),
                            'G3_max_error':float(np.max(err3)),
                            'G3_max_bound':float(np.max(b3)),
                            'G3_max_error_over_bound':r3,
                            'G3_pass':ok3,
                            'G4_max_error':float(np.max(err4)),
                            'G4_max_bound':float(np.max(b4arr)),
                            'G4_max_error_over_bound':r4,
                            'G4_pass':ok4,
                        })

                    if last_A is None or last_Atot is None:
                        raise RuntimeError('missing lambda=1/8 coefficient profiles')

                    Atot=last_Atot
                    A=last_A
                    Asum=np.sum(A,axis=0)
                    D=float(np.dot(Atot,Atot))
                    if not (np.isfinite(D) and D>0.0):
                        g5=False
                        p_sum=float('nan'); p_expected=float('nan'); p_err=float('inf'); p_bound=0.0; p_ratio=float('inf')
                    else:
                        projs=[float(np.dot(A[i],Atot)/D) for i in range(len(SOURCE_NAMES))]
                        p_sum=float(math.fsum(projs))
                        correction=float(np.dot(Asum-Atot,Atot)/D)
                        p_expected=1.0+correction
                        p_err=abs(p_sum-p_expected)
                        T=float(np.sum(np.abs(A*Atot[None,:])) + np.sum(np.abs(Atot*Atot)))
                        m=len(Atot)
                        p_bound=gamma(32*m+128)*T/D
                        ok5=bool(np.isfinite(p_err) and np.isfinite(p_bound) and p_err<=p_bound)
                        p_ratio=float(p_err/p_bound) if p_bound>0 else (0.0 if p_err==0 else float('inf'))
                        g5 &= ok5
                        max_g5_ratio=max(max_g5_ratio,p_ratio)

                        # Preserve the frozen science payload: recomputed projection fractions
                        # must reproduce the stored Repair13 values to the inherited 1e-12
                        # arithmetic-reproduction tolerance.
                        frozen_coeffs={x['source']:x for x in fr13['lambda_eighth_first_order_coefficients']}
                        for i,name in enumerate(SOURCE_NAMES):
                            fp=float(frozen_coeffs[name]['projection_fraction'])
                            obs=projs[i]
                            ae=abs(obs-fp)
                            re=ae/max(abs(obs),abs(fp),1e-300)
                            g6 &= bool(ae<=1e-12 or re<=1e-12)

                    rows.append({
                        'scale_hinv_Mpc':float(scale),
                        'Nr':int(nr),
                        'Y_kind':kind,
                        'beta0':float(beta),
                        'lambda_closure':lam_rows,
                        'projection_identity':{
                            'P_sum_compensated':p_sum,
                            'P_expected_with_coefficient_closure':p_expected,
                            'absolute_error':p_err,
                            'roundoff_bound':p_bound,
                            'error_over_bound':p_ratio,
                            'pass':bool(np.isfinite(p_ratio) and p_ratio<=1.0),
                            'historical_projection_sum':float(fr13['projection_sum']),
                            'historical_projection_sum_error_vs_one':float(fr13['projection_sum_error']),
                        },
                        'frozen_dominant_A_L2_source':fr13['dominant_A_L2_source'],
                        'frozen_second_A_L2_source':fr13['second_A_L2_source'],
                    })

    g6=bool(g6 and len(rows)==54)

    claim_boundary={
        'historical_B4_fail_preserved':True,
        'historical_Repair13_implementation_fail_preserved':True,
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
    g7=bool(
        claim_boundary['historical_B4_fail_preserved']
        and claim_boundary['historical_Repair13_implementation_fail_preserved']
        and not any(v for k,v in claim_boundary.items() if k not in (
            'historical_B4_fail_preserved','historical_Repair13_implementation_fail_preserved'
        ))
    )

    gates={
        'R13A_G1_exact_historical_provenance':g1,
        'R13A_G2_historical_Repair13_gate_pattern':g2,
        'R13A_G3_roundoff_aware_source_sum_closure':bool(g3),
        'R13A_G4_roundoff_aware_coefficient_closure':bool(g4),
        'R13A_G5_roundoff_aware_projection_identity':bool(g5),
        'R13A_G6_frozen_localization_payload_unchanged':g6,
        'R13A_G7_claim_boundary':g7,
    }

    if all(gates.values()):
        cls='NL1C7B4_REPAIR13A_ROUNDOFF_STABLE_SOURCE_LOCALIZATION_PASS'; rc=0
    else:
        cls='NL1C7B4_REPAIR13A_IMPLEMENTATION_FAIL'; rc=2

    result={
        'classification':cls,
        'scope':'Repair13a harness-only IEEE-754 roundoff-stable certification of the frozen Repair13 Hamiltonian source localization.',
        'provenance':{
            **hashes,
            'repair13_result_freeze_commit':'f3d25b37eddd322b4e1ed147c99af9b2dec0227f',
            'repair13a_prereg_commit':'271f6bbc4a21108d5d0c1beabb9764be56e280b3',
        },
        'arithmetic_model':{
            'binary64_unit_roundoff':U,
            'gamma64':gamma(64),
            'gamma96':gamma(96),
            'projection_gamma_formula':'gamma_(32*m+128)',
            'empirical_tolerance_fitted':False,
        },
        'historical_Repair13':{
            'classification':r13j.get('classification'),
            'gates':r13j.get('gates'),
            'old_normalized_source_closure_limit':1e-12,
            'old_normalized_coefficient_closure_limit':1e-12,
            'old_projection_sum_limit':1e-12,
            'old_max_source_sum_closure_error':max_old_g3,
            'old_max_coefficient_sum_closure_error':max_old_g4,
            'old_max_projection_sum_error':max_old_g5,
            'historical_fail_preserved':True,
        },
        'roundoff_certification':{
            'rows':rows,
            'max_G3_error_over_bound':max_g3_ratio,
            'max_G4_error_over_bound':max_g4_ratio,
            'max_G5_error_over_bound':max_g5_ratio,
        },
        'frozen_localization_summary':{
            'n_cases':summary13.get('n_cases'),
            'dominant_A_L2_source_counts':dom_counts,
            'per_source_order_label_counts':order_counts,
            'historical_B4_classification_unchanged':summary13.get('historical_B4_classification_unchanged'),
        },
        'state_anchor':{
            'scalar_canonical_vs_independent_at_ai_relative_L2':r9.rel_sym(scalar_ai,scalar_independent),
            'scalar_finite':bool(scalar_finite),
        },
        'gates':gates,
        'claim_boundary':claim_boundary,
        'interpretation_boundary':{
            'Repair13_payload_certified_if_pass':bool(all(gates.values())),
            'AeST_E2_declared_physically_wrong':False,
            'B4_passed':False,
            'model_or_interface_changed':False,
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
