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
import nl1c7b.initial_constraint_certification_repair19a as r19a
import nl1c7b.initial_constraint_certification_repair19b as r19b

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

R19B_CLASS='NL1C7B4_REPAIR19B_IMPLEMENTATION_FAIL'
CANON_KIND='Simple'
CANON_BETA=1.0
REPRO_LIMIT=1e-12
FEAS_LIMIT=1e-6
GAUGE_LIMIT=1e-12
STAGNATION_FACTOR=1e3
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


def compare_probe(obs,fr):
    checks=[]
    for key in (
        'initial_residual_L2','final_linear_residual_L2',
        'relative_final_linear_residual','max_abs_yL','max_abs_qRt',
        'Y4_residual','Qmean_residual'
    ):
        ok,ae,re=smatch(obs[key],fr[key])
        checks.append({'key':key,'pass':ok,'abs_error':ae,'relative_error':re})
    checks.append({'key':'rank','pass':int(obs['rank'])==int(fr['rank']),
                   'observed':int(obs['rank']),'frozen':int(fr['rank'])})
    return checks,bool(all(x['pass'] for x in checks))


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
    }
    expected={
        'repair15a_json':R15A_JSON_SHA256,'repair15a_npz':R15A_NPZ_SHA256,
        'repair16_json':R16_JSON_SHA256,'repair17_json':R17_JSON_SHA256,
        'repair18_json':R18_JSON_SHA256,'repair18a_json':R18A_JSON_SHA256,
        'repair18b_json':R18B_JSON_SHA256,'repair18b1_json':R18B1_JSON_SHA256,
        'repair18c_json':R18C_JSON_SHA256,'repair18d_json':R18D_JSON_SHA256,
        'repair18d1_json':R18D1_JSON_SHA256,'repair19_json':R19_JSON_SHA256,
        'repair19a_json':R19A_JSON_SHA256,'repair19b_json':R19B_JSON_SHA256,
    }
    p19a=json.loads(Path(a.repair19a_json).read_text())
    p19b=json.loads(Path(a.repair19b_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p19b.get('classification')==R19B_CLASS
        and p19b.get('gates',{}).get('R19B_G1_exact_frozen_provenance') is True
        and p19b.get('gates',{}).get('R19B_G2_exact_frozen_subspace_basis_reproduction') is True
        and p19b.get('gates',{}).get('R19B_G3_exact_parent_Jacobian_input_reproduction') is True
        and p19b.get('gates',{}).get('R19B_G8_exact_gauge_satisfaction') is True
        and p19b.get('gates',{}).get('R19B_G9_LSMR_stagnation_diagnosis') is True
        and p19b.get('gates',{}).get('R19B_G10_claim_boundary') is True
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
    g8=True
    for nr in (256,512):
        obs,Bc,Bo=r19a.basis_audit(nr)
        fr=next(x for x in p19b['basis_reproduction'] if int(x['Nr'])==nr)['observed']
        checks=[]
        for key in ('GB_Frobenius','condition_number','sigma_max','sigma_min'):
            ok,ae,re=smatch(obs['orth'][key],fr['orth'][key])
            checks.append({'block':'orth','key':key,'pass':ok,'abs_error':ae,'relative_error':re})
        ok,ae,re=smatch(obs['orth']['orthonormality_Frobenius'],fr['orth']['orthonormality_Frobenius'])
        checks.append({'block':'orth','key':'orthonormality_Frobenius','pass':ok,'abs_error':ae,'relative_error':re})
        checks.append({'block':'orth','key':'shape','pass':obs['orth']['shape']==fr['orth']['shape']})
        g2 &= bool(all(x['pass'] for x in checks))
        chain_expected=162.33598862000716 if nr==256 else 325.3116790240505
        cok,cae,cre=smatch(obs['chain']['condition_number'],chain_expected)
        g8 &= cok
        basis_rows.append({
            'Nr':nr,'orth_checks':checks,
            'chain_condition_control':{
                'observed':float(obs['chain']['condition_number']),
                'expected':chain_expected,'pass':cok,
                'abs_error':cae,'relative_error':cre,
            },
        })
        bases[nr]=Bo

    states={}
    for scale in b4.SCALES:
        states[(scale,256)]=r16.load_primary_state(off,scale)
        states[(scale,512)]=r16.reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    frozen_rows={(float(r['scale_hinv_Mpc']),int(r['Nr'])):r for r in p19b['rows']}
    rows=[]
    g3=True; g4=True; g5=True; g6=True; g7=True

    for scale in b4.SCALES:
        for nr in (256,512):
            parent=states[(scale,nr)]
            base,fun_x,char_rt=r19a.residual_builder(parent,scale,h,qbg,zbg,funcs,dY)
            n=len(parent['r']); m=n-1
            F0=np.asarray(fun_x(np.zeros(2*m,float)),float)
            Jx=approx_derivative(fun_x,np.zeros(2*m,float),method='2-point',sparsity=r18a.jac_pattern(n))
            Jx=Jx.tocsr()
            Bo=bases[nr]
            A=(Jx@Bo).toarray()
            fr=frozen_rows[(float(scale),int(nr))]
            row={'scale_hinv_Mpc':float(scale),'Nr':int(nr),'drivers':{}}

            for driver in ('gelsd','gelsy'):
                obs,dx=r19b.direct_probe(A,F0,Bo,driver)
                frozen=fr['bases']['orth'][driver]
                checks,repro=compare_probe(obs,frozen)
                g3 &= repro
                g4 &= bool(obs['finite'])
                g5 &= bool(obs['relative_final_linear_residual']<=FEAS_LIMIT)
                g6 &= bool(abs(obs['Y4_residual'])<=GAUGE_LIMIT and abs(obs['Qmean_residual'])<=GAUGE_LIMIT)

                old=float(fr['bases']['orth']['frozen_lsmr_relative_residual'])
                ratio=float(old/max(obs['relative_final_linear_residual'],TINY))
                stag=bool(ratio>=STAGNATION_FACTOR)
                g7 &= stag
                row['drivers'][driver]={
                    'probe':obs,
                    'frozen_payload_checks':checks,
                    'reproduction_pass':repro,
                    'feasibility_pass':bool(obs['relative_final_linear_residual']<=FEAS_LIMIT),
                    'gauge_pass':bool(abs(obs['Y4_residual'])<=GAUGE_LIMIT and abs(obs['Qmean_residual'])<=GAUGE_LIMIT),
                    'frozen_lsmr_relative_residual':old,
                    'lsmr_to_direct_residual_ratio':ratio,
                    'stagnation_pass':stag,
                }
            rows.append(row)

    g3=bool(g3 and len(rows)==6)
    g4=bool(g4 and len(rows)==6)
    g5=bool(g5 and len(rows)==6)
    g6=bool(g6 and len(rows)==6)
    g7=bool(g7 and len(rows)==6)

    claim_boundary={
        'nonlinear_least_squares_run':False,
        'nonlinear_corrected_state_evaluated_or_accepted':False,
        'state_NPZ_written':False,
        'parent_state_modified':False,
        'Y4_or_Qmean_changed':False,
        'physical_field_added':False,
        'source_changed':False,'coefficient_changed':False,'sign_changed':False,
        'finite_eta_executed':False,'branch_changed':False,'radial_points_removed':False,
        'historical_threshold_changed':False,'failed_case_removed':False,
        'time_evolution_run':False,'observational_claimed':False,
        'Repair19_relabelled':False,'Repair19a_relabelled':False,'Repair19b_relabelled':False,
    }
    g9=bool(not any(claim_boundary.values()))

    gates={
        'R19B1_G1_exact_frozen_provenance':g1,
        'R19B1_G2_exact_orthonormal_basis_reproduction':bool(g2),
        'R19B1_G3_exact_Repair19b_orth_payload_reproduction':bool(g3),
        'R19B1_G4_finite_direct_orth_solves':bool(g4),
        'R19B1_G5_orth_direct_residual_space_feasibility':bool(g5),
        'R19B1_G6_exact_gauge_satisfaction':bool(g6),
        'R19B1_G7_LSMR_stagnation_identified':bool(g7),
        'R19B1_G8_chain_conditioning_control_retained':bool(g8),
        'R19B1_G9_claim_boundary':g9,
    }

    impl_ok=bool(g1 and g2 and g3 and g4 and g6 and g8 and g9)
    if not impl_ok:
        classification='NL1C7B4_REPAIR19B1_IMPLEMENTATION_FAIL'; rc=2
    elif not g5:
        classification='NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_INFEASIBILITY'; rc=2
    elif not g7:
        classification='NL1C7B4_REPAIR19B1_LSMR_STAGNATION_NOT_ESTABLISHED'; rc=2
    else:
        classification='NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_FEASIBILITY_LSMR_STAGNATION_PASS'; rc=0

    result={
        'classification':classification,
        'scope':'Repair19b1 certification of residual-space feasibility in the predeclared orthonormal Y4=0/Qmean=0 representation, with direct-vs-LSMR stagnation comparison.',
        'provenance':{
            **hashes,
            'repair19b_result_freeze_commit':'cdc50f56d31f8a0007a80fe7fcaee98e687fe867',
            'repair19b1_prereg_commit':'520f25bc3d8a71a96872b54fad669d8d72f88539',
        },
        'limits':{
            'reproduction_abs_or_rel':REPRO_LIMIT,
            'linear_feasibility':FEAS_LIMIT,
            'gauge':GAUGE_LIMIT,
            'lsmr_stagnation_factor':STAGNATION_FACTOR,
        },
        'basis_rows':basis_rows,
        'rows':rows,
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'max_direct_relative_residual':float(max(
                r['drivers'][d]['probe']['relative_final_linear_residual']
                for r in rows for d in ('gelsd','gelsy')
            )),
            'min_lsmr_to_direct_residual_ratio':float(min(
                r['drivers'][d]['lsmr_to_direct_residual_ratio']
                for r in rows for d in ('gelsd','gelsy')
            )),
            'returned_ranks':[
                {'scale_hinv_Mpc':r['scale_hinv_Mpc'],'Nr':r['Nr'],
                 'gelsd':r['drivers']['gelsd']['probe']['rank'],
                 'gelsy':r['drivers']['gelsy']['probe']['rank']}
                for r in rows
            ],
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
