#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize._numdiff import approx_derivative

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair16 as r16
import nl1c7b.initial_constraint_certification_repair18b1 as r18b1

R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA256='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R17_JSON_SHA256='09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e'
R18_JSON_SHA256='8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922'
R18A_JSON_SHA256='29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782'
R18B_JSON_SHA256='cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855'
R18B1_JSON_SHA256='8e0d796e0368372d0b4cf75a075fba12ebde154b651d74929e745118c1ca6dab'

R18B1_CLASS='NL1C7B4_REPAIR18B1_LOCAL_PROJECTION_RANK_DEFICIENCY'
REPRO_LIMIT=1e-12
ORTH_LIMIT=1e-12
WINDOWS=(1,4,8,16)
TINY=1e-300


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def smatch(a,b):
    return r18b1.scalar_match(a,b,REPRO_LIMIT)


def capture_fraction(V0,v):
    v=np.asarray(v,float)
    n=np.linalg.norm(v)
    if not np.isfinite(n) or n<=0:
        return None
    v=v/n
    return float(np.linalg.norm(V0.T@v)**2)


def boundary_fraction(lev,m,k,block=None):
    lev=np.asarray(lev,float)
    if block=='yL':
        arr=lev[:m]
    elif block=='qRt':
        arr=lev[m:]
    else:
        arr=lev[:m]+lev[m:]
    total=float(np.sum(arr))
    if total<=TINY:
        return {'first':None,'last':None,'total_leverage':total}
    return {
        'first':float(np.sum(arr[:k])/total),
        'last':float(np.sum(arr[-k:])/total),
        'total_leverage':total,
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
    }
    p18b1=json.loads(Path(a.repair18b1_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g18b1=p18b1.get('gates',{})
    g1=bool(
        hashes['repair15a_json']==R15A_JSON_SHA256
        and hashes['repair15a_npz']==R15A_NPZ_SHA256
        and hashes['repair16_json']==R16_JSON_SHA256
        and hashes['repair17_json']==R17_JSON_SHA256
        and hashes['repair18_json']==R18_JSON_SHA256
        and hashes['repair18a_json']==R18A_JSON_SHA256
        and hashes['repair18b_json']==R18B_JSON_SHA256
        and hashes['repair18b1_json']==R18B1_JSON_SHA256
        and p18b1.get('classification')==R18B1_CLASS
        and len(g18b1)==4 and all(g18b1.values())
        and p18b1.get('summary',{}).get('payload_reproduction_ok') is True
        and p18b1.get('summary',{}).get('provenance_ok') is True
        and p18b1.get('summary',{}).get('structure_match_all') is True
        and p18b1.get('summary',{}).get('full_rank_all') is False
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
    qbg=b4.stable_q_from_kq(float(np.median(tv_b4['KQ'])))
    kqq_bg=float(np.median(tv_rec['KQQ']))
    zbg=r9.stable_zbg(float(np.median(tv_b4['KQ'])))
    funcs,dY,kidentity=r1.build_nonK()
    g1=bool(
        g1 and len(ks)==128 and np.array_equal(ks,ks_b4)
        and scalar_finite and scalar_identity<=1e-10
        and np.isfinite([qbg,kqq_bg,zbg]).all()
        and bool(kidentity)
    )

    frozen={float(r['scale_hinv_Mpc']):r for r in p18b1['rows']}
    rows=[]
    repro_rows=[]
    g2=True
    g3=True
    g4=True
    Vspaces={}
    complete=True

    for scale in b4.SCALES:
        parent=r16.load_primary_state(off,scale)
        base,fun,char_rt=r18b1.residual_builder(parent,scale,h,qbg,zbg,funcs,dY)
        n=len(parent['r']); m=n-1
        x0=np.zeros(2*m,float)
        f0=np.asarray(fun(x0),float)
        J=np.asarray(approx_derivative(fun,x0,method='2-point'),float)

        s_ref=np.linalg.svd(J,compute_uv=False)
        U,s,Vh=np.linalg.svd(J,full_matrices=True)
        V=Vh.T
        smax=float(s_ref[0]); smin=float(s_ref[-1])
        rank_tol=float(smax*max(J.shape)*np.finfo(float).eps)
        rank=int(np.count_nonzero(s_ref>rank_tol))
        deficient=int(J.shape[1]-rank)
        deficient_indices=np.where(s_ref<=rank_tol)[0].astype(int).tolist()

        fr=frozen[float(scale)]
        checks={}
        for key,val in [
            ('sigma_max',smax),
            ('sigma_min',smin),
            ('sigma_ratio',float(smin/max(smax,TINY))),
            ('rank_tolerance',rank_tol),
            ('parent_residual_l2',float(np.linalg.norm(f0))),
        ]:
            fkey={
                'sigma_max':'dense_sigma_max',
                'sigma_min':'dense_sigma_min',
                'sigma_ratio':'dense_sigma_min_over_sigma_max',
                'rank_tolerance':'dense_rank_tolerance',
                'parent_residual_l2':'parent_normalized_residual_l2',
            }[key]
            ok,ae,re=smatch(val,fr[fkey])
            checks[key]={'pass':ok,'abs_error':ae,'relative_error':re}
            g2 &= ok
        rank_ok=(rank==int(fr['dense_numerical_rank'])==508)
        checks['rank']={'pass':rank_ok,'observed':rank,'frozen':int(fr['dense_numerical_rank'])}
        g2 &= rank_ok
        repro_rows.append({'scale_hinv_Mpc':float(scale),'checks':checks,'pass':bool(all(v['pass'] for v in checks.values()))})

        exact_two=bool(rank==508 and deficient==2 and len(deficient_indices)==2 and deficient_indices==[508,509])
        g3 &= exact_two

        V0=np.asarray(V[:,-2:],float)
        U0=np.asarray(U[:,-2:],float)
        Vspaces[float(scale)]=V0
        Pv=V0@V0.T
        lev=np.diag(Pv)
        ov=float(np.linalg.norm(V0.T@V0-np.eye(2)))
        ou=float(np.linalg.norm(U0.T@U0-np.eye(2)))
        tr=float(np.trace(Pv))
        svd_match=float(np.linalg.norm(s-s_ref)/max(np.linalg.norm(s_ref),TINY))
        lev_ok=bool(np.all(np.isfinite(lev)) and np.min(lev)>=-1e-12 and np.max(lev)<=1+1e-12)
        consistency=bool(
            np.all(np.isfinite(U)) and np.all(np.isfinite(s)) and np.all(np.isfinite(Vh))
            and ov<=ORTH_LIMIT and ou<=ORTH_LIMIT and abs(tr-2.0)<=ORTH_LIMIT
            and svd_match<=REPRO_LIMIT and lev_ok
        )
        g4 &= consistency

        ylev=float(np.sum(lev[:m])); qlev=float(np.sum(lev[m:]))
        boundary={}
        for k in WINDOWS:
            boundary[str(k)]={
                'yL':boundary_fraction(lev,m,k,'yL'),
                'qRt':boundary_fraction(lev,m,k,'qRt'),
                'combined':boundary_fraction(lev,m,k,None),
            }

        imax=int(np.argmax(lev))
        block='yL' if imax<m else 'qRt'
        local=imax if imax<m else imax-m
        radial_index=local+1
        Rs=float(scale)/h
        rarr=np.asarray(parent['r'],float)[1:]
        rnorm=rarr/Rs

        ones=np.ones(m,float)
        candidate_vectors={
            'constant_yL':np.concatenate([ones,np.zeros(m)]),
            'constant_qRt':np.concatenate([np.zeros(m),ones]),
            'linear_r_over_Rs_yL':np.concatenate([rnorm,np.zeros(m)]),
            'linear_r_over_Rs_qRt':np.concatenate([np.zeros(m),rnorm]),
            'first_noncenter_yL':np.concatenate([np.eye(1,m,0).ravel(),np.zeros(m)]),
            'first_noncenter_qRt':np.concatenate([np.zeros(m),np.eye(1,m,0).ravel()]),
            'outermost_yL':np.concatenate([np.eye(1,m,m-1).ravel(),np.zeros(m)]),
            'outermost_qRt':np.concatenate([np.zeros(m),np.eye(1,m,m-1).ravel()]),
        }
        captures={k:capture_fraction(V0,v) for k,v in candidate_vectors.items()}
        complete &= bool(len(captures)==8 and all(v is not None and np.isfinite(v) for v in captures.values()))

        compat_vec=np.asarray(U0.T@f0,float)
        compat_ratio=float(np.linalg.norm(compat_vec)/max(np.linalg.norm(f0),TINY))
        complete &= bool(np.all(np.isfinite(compat_vec)) and np.isfinite(compat_ratio))

        rows.append({
            'scale_hinv_Mpc':float(scale),
            'Nr':256,
            'n_unknowns':int(J.shape[1]),
            'rank':rank,
            'rank_tolerance':rank_tol,
            'deficient_dimension':deficient,
            'deficient_singular_indices':deficient_indices,
            'bottom_singular_values':[float(x) for x in s_ref[-8:]],
            'sigma_max':smax,
            'sigma_min':smin,
            'sigma_min_over_sigma_max':float(smin/max(smax,TINY)),
            'svd_full_vs_values_relative_L2':svd_match,
            'V0_orthonormality_error_F':ov,
            'U0_orthonormality_error_F':ou,
            'null_projector_trace':tr,
            'null_leverage':{
                'yL_total':ylev,
                'qRt_total':qlev,
                'yL_fraction_of_trace2':ylev/2.0,
                'qRt_fraction_of_trace2':qlev/2.0,
                'boundary_windows':boundary,
                'max_coordinate':{
                    'flat_coordinate_index':imax,
                    'block':block,
                    'radial_index':radial_index,
                    'r_over_Rs':float(rnorm[local]),
                    'leverage':float(lev[imax]),
                },
            },
            'candidate_capture_fractions':captures,
            'left_null_compatibility':{
                'components':[float(x) for x in compat_vec],
                'components_abs':[float(abs(x)) for x in compat_vec],
                'relative_L2':compat_ratio,
                'parent_residual_L2':float(np.linalg.norm(f0)),
            },
            'two_mode_gate_pass':exact_two,
            'subspace_consistency_pass':consistency,
        })

    pairs=[]
    scales=[float(s) for s in b4.SCALES]
    for i in range(len(scales)):
        for j in range(i+1,len(scales)):
            a0,b0=scales[i],scales[j]
            cs=np.linalg.svd(Vspaces[a0].T@Vspaces[b0],compute_uv=False)
            cs=np.clip(cs,0.0,1.0)
            ang=np.degrees(np.arccos(cs))
            row={
                'scale_a_hinv_Mpc':a0,
                'scale_b_hinv_Mpc':b0,
                'cosines':[float(x) for x in cs],
                'principal_angles_deg':[float(x) for x in ang],
            }
            complete &= bool(len(ang)==2 and np.all(np.isfinite(ang)))
            pairs.append(row)

    g5=bool(complete and len(rows)==3 and len(pairs)==3 and all(
        len(r['null_leverage']['boundary_windows'])==4
        and len(r['candidate_capture_fractions'])==8
        for r in rows
    ))

    claim_boundary={
        'nonlinear_state_modified_or_solved':False,
        'boundary_or_gauge_condition_selected':False,
        'projection_pair_changed':False,
        'jacobian_rule_changed':False,
        'rank_tolerance_changed':False,
        'source_changed':False,
        'coefficient_changed':False,
        'sign_changed':False,
        'branch_changed':False,
        'finite_eta_executed':False,
        'radial_points_removed':False,
        'historical_threshold_changed':False,
        'official_NPZ_written':False,
        'nonlinear_time_evolution_executed':False,
        'observational_claimed':False,
        'historical_result_relabelled':False,
    }
    g6=bool(not any(claim_boundary.values()))

    gates={
        'R18C_G1_exact_frozen_provenance':g1,
        'R18C_G2_exact_Repair18b1_Jacobian_reproduction':bool(g2),
        'R18C_G3_exact_two_mode_deficiency':bool(g3),
        'R18C_G4_SVD_subspace_consistency':bool(g4),
        'R18C_G5_complete_characterization':g5,
        'R18C_G6_claim_boundary':g6,
    }
    if all(gates.values()):
        classification='NL1C7B4_REPAIR18C_TWO_MODE_NULLSPACE_CHARACTERIZED'; rc=0
    else:
        classification='NL1C7B4_REPAIR18C_IMPLEMENTATION_FAIL'; rc=2

    result={
        'classification':classification,
        'scope':'Repair18c basis-invariant characterization of the certified two-dimensional local null space of the frozen L/R_t projection map.',
        'provenance':{
            **hashes,
            'repair18b1_result_freeze_commit':'77090aef851f217f194c0b977afd361bbf016682',
            'repair18c_prereg_commit':'43ddb5e99ca4289663cdbcc614389e2958810f96',
        },
        'domain':{
            'eta':0.0,'Y_kind':'Simple','beta0':1.0,'lambda':1.0,
            'Nr':256,'scales_hinv_Mpc':scales,
        },
        'rank_rule':'tol = sigma_max * max(J.shape) * eps_float64',
        'reproduction':{
            'limit_abs_or_rel':REPRO_LIMIT,
            'rows':repro_rows,
            'pass':bool(g2),
        },
        'rows':rows,
        'cross_scale_right_null_subspace':pairs,
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'all_rank_508_of_510':bool(all(r['rank']==508 for r in rows)),
            'all_deficient_dimension_2':bool(all(r['deficient_dimension']==2 for r in rows)),
            'max_left_null_compatibility_relative_L2':float(max(r['left_null_compatibility']['relative_L2'] for r in rows)),
            'max_principal_angle_deg':float(max(max(p['principal_angles_deg']) for p in pairs)),
            'min_principal_angle_deg':float(min(min(p['principal_angles_deg']) for p in pairs)),
        },
    }
    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
