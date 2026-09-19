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
from scipy.sparse import csr_matrix

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

R19_CLASS='NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_FAIL'
R19A_CLASS='NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_INFEASIBILITY'
CANON_KIND='Simple'
CANON_BETA=1.0
TINY=1e-300
REPRO_LIMIT=1e-12
LINEAR_FEAS_LIMIT=1e-6
PHYSICAL_AGREE_LIMIT=1e-8
GAUGE_LIMIT=1e-12
STAGNATION_FACTOR=1e3


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def scalar_match(a,b,limit=REPRO_LIMIT):
    a=float(a); b=float(b)
    ae=abs(a-b)
    re=ae/max(abs(a),abs(b),TINY)
    return bool(ae<=limit or re<=limit),float(ae),float(re)


def direct_probe(A,F0,B,driver):
    A=np.asarray(A,float)
    F0=np.asarray(F0,float)
    cond=float(max(A.shape)*np.finfo(float).eps)
    z,residuals,rank,s=lstsq(
        A,-F0,cond=cond,lapack_driver=driver,check_finite=True
    )
    z=np.asarray(z,float)
    final=np.asarray(F0+A@z,float)
    dx=np.asarray(B@z,float).ravel()
    m=len(dx)//2
    gy,gq=r19.gauge_values(dx)
    rel=float(np.linalg.norm(final)/max(np.linalg.norm(F0),TINY))
    svals=None if s is None else np.asarray(s,float)
    return {
        'driver':driver,
        'cond_cutoff_relative':cond,
        'rank':int(rank),
        'expected_rank':int(A.shape[1]),
        'full_column_rank':bool(rank==A.shape[1]),
        'initial_residual_L2':float(np.linalg.norm(F0)),
        'final_linear_residual_L2':float(np.linalg.norm(final)),
        'relative_final_linear_residual':rel,
        'reduced_coordinate_L2':float(np.linalg.norm(z)),
        'physical_dx_L2':float(np.linalg.norm(dx)),
        'max_abs_yL':float(np.max(np.abs(dx[:m]))),
        'max_abs_qRt':float(np.max(np.abs(dx[m:]))),
        'Y4_residual':float(gy),
        'Qmean_residual':float(gq),
        'singular_sigma_max':None if svals is None or len(svals)==0 else float(svals[0]),
        'singular_sigma_min':None if svals is None or len(svals)==0 else float(svals[-1]),
        'finite':bool(
            np.all(np.isfinite(A)) and np.all(np.isfinite(z))
            and np.all(np.isfinite(final)) and np.all(np.isfinite(dx))
            and np.isfinite([rel,gy,gq]).all()
        ),
    },dx


def reproduce_basis(p19a,nr):
    obs,Bc,Bo=r19a.basis_audit(nr)
    fr=next(x for x in p19a['basis_audit'] if int(x['Nr'])==int(nr))
    checks=[]
    for block in ('chain','orth'):
        for key in ('GB_Frobenius','condition_number','sigma_max','sigma_min'):
            ok,ae,re=scalar_match(obs[block][key],fr[block][key])
            checks.append({'block':block,'key':key,'pass':ok,'abs_error':ae,'relative_error':re})
        if block=='orth':
            ok,ae,re=scalar_match(obs[block]['orthonormality_Frobenius'],fr[block]['orthonormality_Frobenius'])
            checks.append({'block':block,'key':'orthonormality_Frobenius','pass':ok,'abs_error':ae,'relative_error':re})
        checks.append({'block':block,'key':'shape','pass':obs[block]['shape']==fr[block]['shape']})
    return obs,Bc,Bo,checks,bool(all(x['pass'] for x in checks))


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
    }
    expected={
        'repair15a_json':R15A_JSON_SHA256,'repair15a_npz':R15A_NPZ_SHA256,
        'repair16_json':R16_JSON_SHA256,'repair17_json':R17_JSON_SHA256,
        'repair18_json':R18_JSON_SHA256,'repair18a_json':R18A_JSON_SHA256,
        'repair18b_json':R18B_JSON_SHA256,'repair18b1_json':R18B1_JSON_SHA256,
        'repair18c_json':R18C_JSON_SHA256,'repair18d_json':R18D_JSON_SHA256,
        'repair18d1_json':R18D1_JSON_SHA256,'repair19_json':R19_JSON_SHA256,
        'repair19a_json':R19A_JSON_SHA256,
    }
    p19=json.loads(Path(a.repair19_json).read_text())
    p19a=json.loads(Path(a.repair19a_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p19.get('classification')==R19_CLASS
        and p19a.get('classification')==R19A_CLASS
        and p19a.get('gates',{}).get('R19A_G5_gauge_fixed_linear_feasibility') is False
        and p19a.get('gates',{}).get('R19A_G6_physical_coordinate_agreement') is False
        and p19a.get('gates',{}).get('R19A_G1_exact_frozen_provenance') is True
        and p19a.get('gates',{}).get('R19A_G2_exact_same_constrained_subspace') is True
        and p19a.get('gates',{}).get('R19A_G3_exact_parent_reproduction') is True
        and p19a.get('gates',{}).get('R19A_G4_finite_Jacobian_and_linear_probes') is True
        and p19a.get('gates',{}).get('R19A_G7_complete_nonlinear_alpha_probe') is True
        and p19a.get('gates',{}).get('R19A_G8_claim_boundary') is True
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
    )

    z=rec.read_trace(a.trace)
    ks,gs=rec.groups(z)
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
        obs,Bc,Bo,checks,ok=reproduce_basis(p19a,nr)
        basis_rows.append({'Nr':int(nr),'observed':obs,'checks':checks,'pass':ok})
        bases[nr]=(Bc,Bo)
        g2 &= ok

    states={}
    for scale in b4.SCALES:
        states[(scale,256)]=r16.load_primary_state(off,scale)
        states[(scale,512)]=r16.reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    frozen_rows={(float(r['scale_hinv_Mpc']),int(r['Nr'])):r for r in p19a['rows']}
    rows=[]
    g3=True; g4=True; g5=True; g6=True; g7=True; g8=True; g9=True

    for scale in b4.SCALES:
        for nr in (256,512):
            parent=states[(scale,nr)]
            base,fun_x,char_rt=r19a.residual_builder(parent,scale,h,qbg,zbg,funcs,dY)
            n=len(parent['r']); m=n-1
            x0=np.zeros(2*m,float)
            F0=np.asarray(fun_x(x0),float)
            Jx=approx_derivative(fun_x,x0,method='2-point',sparsity=r18a.jac_pattern(n))
            Jx=Jx.tocsr() if hasattr(Jx,'tocsr') else csr_matrix(Jx)
            fr=frozen_rows[(float(scale),int(nr))]

            pr0,ae0,re0=scalar_match(np.linalg.norm(F0),fr['chain_linear_probe']['initial_residual_L2'])
            shape_ok=list(Jx.shape)==fr['full_J_shape']
            nnz_ok=int(Jx.nnz)==int(fr['full_J_nnz'])
            repro=bool(pr0 and shape_ok and nnz_ok)
            g3 &= repro

            Bc,Bo=bases[nr]
            case={'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                  'input_reproduction':{
                      'initial_residual_abs_error':ae0,
                      'initial_residual_relative_error':re0,
                      'shape_pass':shape_ok,'nnz_pass':nnz_ok,'pass':repro,
                  },
                  'bases':{}}

            phys={}
            for bname,B in (('chain',Bc),('orth',Bo)):
                A=(Jx@B).toarray()
                pg,dg=direct_probe(A,F0,B,'gelsd')
                py,dy=direct_probe(A,F0,B,'gelsy')
                case['bases'][bname]={
                    'gelsd':pg,'gelsy':py,
                    'driver_physical_relative_difference':float(
                        np.linalg.norm(dg-dy)/max(np.linalg.norm(dg),np.linalg.norm(dy),TINY)
                    ),
                }
                phys[(bname,'gelsd')]=dg
                phys[(bname,'gelsy')]=dy

                g4 &= bool(pg['finite'] and py['finite'] and pg['full_column_rank'] and py['full_column_rank'])
                g5 &= bool(pg['relative_final_linear_residual']<=LINEAR_FEAS_LIMIT)
                g7 &= bool(case['bases'][bname]['driver_physical_relative_difference']<=PHYSICAL_AGREE_LIMIT)
                g8 &= bool(
                    abs(pg['Y4_residual'])<=GAUGE_LIMIT
                    and abs(pg['Qmean_residual'])<=GAUGE_LIMIT
                )

                old=float(fr[f'{bname}_linear_probe']['relative_final_linear_residual'])
                ratio=float(old/max(pg['relative_final_linear_residual'],TINY))
                case['bases'][bname]['frozen_lsmr_relative_residual']=old
                case['bases'][bname]['lsmr_to_gelsd_residual_ratio']=ratio
                case['bases'][bname]['stagnation_factor_pass']=bool(ratio>=STAGNATION_FACTOR)
                g9 &= bool(ratio>=STAGNATION_FACTOR)

            cross=float(
                np.linalg.norm(phys[('chain','gelsd')]-phys[('orth','gelsd')])
                /max(np.linalg.norm(phys[('chain','gelsd')]),np.linalg.norm(phys[('orth','gelsd')]),TINY)
            )
            case['chain_vs_orth_gelsd_physical_relative_difference']=cross
            case['basis_invariant_physical_pass']=bool(cross<=PHYSICAL_AGREE_LIMIT)
            g6 &= bool(cross<=PHYSICAL_AGREE_LIMIT)
            rows.append(case)

    g4=bool(g4 and len(rows)==6)

    claim_boundary={
        'nonlinear_least_squares_run':False,
        'nonlinear_corrected_state_evaluated_or_accepted':False,
        'state_NPZ_written':False,
        'physical_field_modified':False,
        'parent_artifact_modified':False,
        'Y4_or_Qmean_changed':False,
        'source_changed':False,'coefficient_changed':False,'sign_changed':False,
        'branch_changed':False,'finite_eta_executed':False,'radial_points_removed':False,
        'historical_threshold_changed':False,'failed_case_removed':False,
        'time_evolution_run':False,'observational_claimed':False,
        'Repair19_relabelled':False,'Repair19a_relabelled':False,
    }
    g10=bool(not any(claim_boundary.values()))

    gates={
        'R19B_G1_exact_frozen_provenance':g1,
        'R19B_G2_exact_frozen_subspace_basis_reproduction':bool(g2),
        'R19B_G3_exact_parent_Jacobian_input_reproduction':bool(g3),
        'R19B_G4_finite_full_rank_direct_solves':bool(g4),
        'R19B_G5_direct_gauge_fixed_linear_feasibility':bool(g5),
        'R19B_G6_basis_invariant_physical_correction':bool(g6),
        'R19B_G7_LAPACK_driver_physical_agreement':bool(g7),
        'R19B_G8_exact_gauge_satisfaction':bool(g8),
        'R19B_G9_LSMR_stagnation_diagnosis':bool(g9),
        'R19B_G10_claim_boundary':g10,
    }

    impl_ok=bool(g1 and g2 and g3 and g4 and g8 and g10)
    if not impl_ok:
        classification='NL1C7B4_REPAIR19B_IMPLEMENTATION_FAIL'; rc=2
    elif not g5:
        classification='NL1C7B4_REPAIR19B_DIRECT_LINEAR_INFEASIBILITY'; rc=2
    elif not (g6 and g7):
        classification='NL1C7B4_REPAIR19B_DIRECT_SOLVER_COORDINATE_DISAGREEMENT'; rc=2
    elif not g9:
        classification='NL1C7B4_REPAIR19B_LSMR_STAGNATION_NOT_ESTABLISHED'; rc=2
    else:
        classification='NL1C7B4_REPAIR19B_LSMR_STAGNATION_IDENTIFIED'; rc=0

    result={
        'classification':classification,
        'scope':'Repair19b direct LAPACK audit of exactly the frozen Repair19a gauge-fixed reduced linear systems.',
        'provenance':{
            **hashes,
            'repair19a_result_freeze_commit':'e8f6e93f17066cbfb2355dc64f5b36e91a06f527',
            'repair19b_prereg_commit':'b79ecb52840c304abb5b915766f23785db0c3adc',
        },
        'limits':{
            'linear_feasibility':LINEAR_FEAS_LIMIT,
            'physical_agreement':PHYSICAL_AGREE_LIMIT,
            'gauge':GAUGE_LIMIT,
            'lsmr_stagnation_factor':STAGNATION_FACTOR,
        },
        'basis_reproduction':basis_rows,
        'rows':rows,
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'max_gelsd_relative_residual':float(max(
                r['bases'][b]['gelsd']['relative_final_linear_residual']
                for r in rows for b in ('chain','orth')
            )),
            'max_chain_vs_orth_physical_difference':float(max(
                r['chain_vs_orth_gelsd_physical_relative_difference'] for r in rows
            )),
            'max_driver_physical_difference':float(max(
                r['bases'][b]['driver_physical_relative_difference']
                for r in rows for b in ('chain','orth')
            )),
            'min_lsmr_to_gelsd_residual_ratio':float(min(
                r['bases'][b]['lsmr_to_gelsd_residual_ratio']
                for r in rows for b in ('chain','orth')
            )),
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
