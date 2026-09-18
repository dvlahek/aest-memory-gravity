#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import lsq_linear
from scipy.optimize._numdiff import approx_derivative
from scipy.sparse import issparse

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair16 as r16
import nl1c7b.initial_constraint_certification_repair18a as r18a

R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA256='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R17_JSON_SHA256='09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e'
R18_JSON_SHA256='8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922'
R18A_JSON_SHA256='29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782'
R18B_JSON_SHA256='cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855'

R15A_CLASS='NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED'
R16_CLASS='NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL'
R17_CLASS='NL1C7B4_REPAIR17_REPAIR16_SOURCE_LOCALIZATION_PASS'
R18_CLASS='NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_FAIL'
R18A_CLASS='NL1C7B4_REPAIR18A_DIMENSIONLESS_RT_COORDINATE_FEASIBILITY_FAIL'
R18B_CLASS='NL1C7B4_REPAIR18B_IMPLEMENTATION_FAIL'

CANON_KIND='Simple'
CANON_BETA=1.0
JAC_MATCH_LIMIT=1e-6
ALPHAS=(1.0,0.5,0.25,0.125)
BOUND=0.5
TINY=1e-300


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def normalize(v):
    v=np.asarray(v,float)
    n=float(np.linalg.norm(v))
    return v/max(n,TINY)


def scalar_match(a,b,limit=1e-12):
    if isinstance(a,(bool,np.bool_)) or isinstance(b,(bool,np.bool_)):
        return bool(a)==bool(b),0.0,0.0
    if isinstance(a,(int,np.integer)) and isinstance(b,(int,np.integer)):
        return int(a)==int(b),float(abs(int(a)-int(b))),0.0
    a=float(a); b=float(b)
    ae=abs(a-b)
    re=ae/max(abs(a),abs(b),1e-300)
    return bool(ae<=limit or re<=limit),float(ae),float(re)


def payload_reproduction(rows,frozen_rows):
    fidx={float(r['scale_hinv_Mpc']):r for r in frozen_rows}
    ok=True
    max_abs=0.0
    max_rel=0.0
    detail=[]
    scalar_keys=[
        'relative_Frobenius_sparse_vs_dense',
        'dense_sigma_max','dense_sigma_min','dense_sigma_min_over_sigma_max',
        'linear_lsq_max_abs_coordinate',
    ]
    exact_keys=['dense_numerical_rank','dense_full_column_rank','jacobian_structure_match']
    probe_keys=['max_epsilon_H','max_epsilon_M','frozen_parent_normalized_residual_l2']
    for r in rows:
        s=float(r['scale_hinv_Mpc'])
        fr=fidx.get(s)
        if fr is None:
            ok=False
            detail.append({'scale_hinv_Mpc':s,'pass':False,'reason':'missing frozen scale'})
            continue
        rok=True
        for k in exact_keys:
            same=(r[k]==fr[k])
            rok &= same
        for k in scalar_keys:
            same,ae,re=scalar_match(r[k],fr[k])
            rok &= same; max_abs=max(max_abs,ae); max_rel=max(max_rel,re)
        for name,val in r['deterministic_operator_action_relative_differences'].items():
            same,ae,re=scalar_match(val,fr['deterministic_operator_action_relative_differences'][name])
            rok &= same; max_abs=max(max_abs,ae); max_rel=max(max_rel,re)
        rp=r['exact_nonlinear_alpha_probes']
        fp=fr['exact_nonlinear_alpha_probes']
        if len(rp)!=len(fp):
            rok=False
        else:
            for q,fq in zip(rp,fp):
                same,ae,re=scalar_match(q['alpha'],fq['alpha'])
                rok &= same; max_abs=max(max_abs,ae); max_rel=max(max_rel,re)
                for k in probe_keys:
                    same,ae,re=scalar_match(q[k],fq[k])
                    rok &= same; max_abs=max(max_abs,ae); max_rel=max(max_rel,re)
        ok &= rok
        detail.append({'scale_hinv_Mpc':s,'pass':bool(rok)})
    return bool(ok and len(rows)==len(frozen_rows)),{
        'max_abs_error':float(max_abs),
        'max_relative_error':float(max_rel),
        'rows':detail,
        'limit_abs_or_rel':1e-12,
    }


def residual_builder(parent,scale,h,qbg,zbg,funcs,dY):
    base=r18a.source_arrays(parent,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
    if not base.get('finite',False):
        raise RuntimeError(f'nonfinite parent scale={scale}')
    n=len(parent['r'])
    m=n-1
    denomH=np.asarray(base['denH'][1:]+base['floorH'],float)
    denomM=np.asarray(base['denM'][1:]+base['floorM'],float)
    Rs=float(scale)/float(h)
    char_rt=b4.AI*b4.H_DIRECT*Rs

    def fun(x):
        st=r18a.apply_projection(parent,np.asarray(x,float),char_rt)
        ev=r18a.source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
        if not ev.get('finite',False):
            return np.full(2*m,1e6,dtype=float)
        return np.concatenate([
            np.asarray(ev['numH'][1:]/denomH,float),
            np.asarray(ev['numM'][1:]/denomM,float),
        ])

    return base,fun,char_rt


def exact_probe(parent,x,alpha,scale,h,qbg,zbg,funcs,dY):
    Rs=float(scale)/float(h)
    char_rt=b4.AI*b4.H_DIRECT*Rs
    xa=float(alpha)*np.asarray(x,float)
    st=r18a.apply_projection(parent,xa,char_rt)
    ev=r18a.source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
    cm=r18a.correction_metrics(parent,st,scale,h)
    return {
        'alpha':float(alpha),
        'finite':bool(ev.get('finite',False)),
        'within_bounds':bool(np.max(np.abs(xa))<=BOUND+1e-15),
        'max_abs_coordinate':float(np.max(np.abs(xa))),
        'L_min':float(np.min(ev['L'])) if ev.get('finite',False) else None,
        'exact_Q_max_normalized_error':float(ev['qerr']) if ev.get('finite',False) else None,
        'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else None,
        'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else None,
        'correction':cm,
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
    }
    p15=json.loads(Path(a.repair15a_json).read_text())
    p16=json.loads(Path(a.repair16_json).read_text())
    p17=json.loads(Path(a.repair17_json).read_text())
    p18=json.loads(Path(a.repair18_json).read_text())
    p18a=json.loads(Path(a.repair18a_json).read_text())
    p18b=json.loads(Path(a.repair18b_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g18=p18.get('gates',{})
    g18a=p18a.get('gates',{})
    provenance_ok=bool(
        hashes['repair15a_json']==R15A_JSON_SHA256
        and hashes['repair15a_npz']==R15A_NPZ_SHA256
        and hashes['repair16_json']==R16_JSON_SHA256
        and hashes['repair17_json']==R17_JSON_SHA256
        and hashes['repair18_json']==R18_JSON_SHA256
        and hashes['repair18a_json']==R18A_JSON_SHA256
        and hashes['repair18b_json']==R18B_JSON_SHA256
        and p15.get('classification')==R15A_CLASS
        and p16.get('classification')==R16_CLASS
        and p17.get('classification')==R17_CLASS
        and p18.get('classification')==R18_CLASS
        and p18a.get('classification')==R18A_CLASS
        and p18b.get('classification')==R18B_CLASS
        and p18b.get('summary',{}).get('provenance_ok') is False
        and p18b.get('summary',{}).get('finite_all') is True
        and p18b.get('summary',{}).get('structure_match_all') is True
        and p18b.get('summary',{}).get('full_rank_all') is False
        and len(g18)==7
        and g18.get('R18_G3_canonical_nonlinear_solve_closure') is False
        and all(v for k,v in g18.items() if k!='R18_G3_canonical_nonlinear_solve_closure')
        and len(g18a)==7
        and g18a.get('R18A_G3_canonical_nonlinear_solve_closure') is False
        and all(v for k,v in g18a.items() if k!='R18A_G3_canonical_nonlinear_solve_closure')
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

    provenance_ok=bool(
        provenance_ok
        and len(ks)==128
        and np.array_equal(ks,ks_b4)
        and scalar_finite
        and scalar_identity<=1e-10
        and np.isfinite([qbg,kqq_bg,zbg]).all()
        and bool(kidentity)
    )

    rows=[]
    structure_match_all=True
    full_rank_all=True
    finite_all=True

    for scale in b4.SCALES:
        parent=r16.load_primary_state(off,scale)
        base,fun,char_rt=residual_builder(parent,scale,h,qbg,zbg,funcs,dY)
        n=len(parent['r'])
        m=n-1
        x0=np.zeros(2*m,float)
        f0=np.asarray(fun(x0),float)
        finite_all &= bool(np.all(np.isfinite(f0)))

        Jd=approx_derivative(fun,x0,method='2-point')
        Js=approx_derivative(fun,x0,method='2-point',sparsity=r18a.jac_pattern(n))
        if issparse(Js):
            Js=Js.toarray()
        Jd=np.asarray(Jd,float)
        Js=np.asarray(Js,float)
        finite=bool(np.all(np.isfinite(Jd)) and np.all(np.isfinite(Js)))
        finite_all &= finite

        diff=Js-Jd
        frob=float(np.linalg.norm(diff)/max(np.linalg.norm(Jd),TINY))
        structure_match=bool(np.isfinite(frob) and frob<=JAC_MATCH_LIMIT)
        structure_match_all &= structure_match

        idx=np.arange(1,m+1,dtype=float)
        sinv=np.sin(np.pi*idx/(m+1.0))
        vecs={
            'ones_yL':np.concatenate([np.ones(m),np.zeros(m)]),
            'ones_qRt':np.concatenate([np.zeros(m),np.ones(m)]),
            'sin_yL':np.concatenate([sinv,np.zeros(m)]),
            'sin_qRt':np.concatenate([np.zeros(m),sinv]),
        }
        action={}
        for name,v in vecs.items():
            v=normalize(v)
            jd=Jd@v
            js=Js@v
            action[name]=float(np.linalg.norm(js-jd)/max(np.linalg.norm(jd),TINY))

        svals=np.linalg.svd(Jd,compute_uv=False)
        smax=float(svals[0])
        smin=float(svals[-1])
        rank_tol=float(smax*max(Jd.shape)*np.finfo(float).eps)
        rank=int(np.count_nonzero(svals>rank_tol))
        full_rank=bool(rank==Jd.shape[1])
        full_rank_all &= full_rank

        lin=lsq_linear(
            Jd,-f0,bounds=(-BOUND,BOUND),method='trf',
            tol=1e-12,max_iter=500,verbose=0,
        )
        dx=np.asarray(lin.x,float)
        probes=[]
        for alpha in ALPHAS:
            pr=exact_probe(parent,dx,alpha,scale,h,qbg,zbg,funcs,dY)
            pr['frozen_parent_normalized_residual_l2']=float(np.linalg.norm(fun(alpha*dx)))
            probes.append(pr)

        rows.append({
            'scale_hinv_Mpc':float(scale),
            'Nr':256,
            'n_unknowns':int(2*m),
            'parent_max_epsilon_H':float(base['maxH']),
            'parent_max_epsilon_M':float(base['maxM']),
            'parent_normalized_residual_l2':float(np.linalg.norm(f0)),
            'relative_Frobenius_sparse_vs_dense':frob,
            'jacobian_structure_match_limit':JAC_MATCH_LIMIT,
            'jacobian_structure_match':structure_match,
            'deterministic_operator_action_relative_differences':action,
            'dense_sigma_max':smax,
            'dense_sigma_min':smin,
            'dense_sigma_min_over_sigma_max':float(smin/max(smax,TINY)),
            'dense_rank_tolerance':rank_tol,
            'dense_numerical_rank':rank,
            'dense_full_column_rank':full_rank,
            'linear_lsq_success':bool(lin.success),
            'linear_lsq_status':int(lin.status),
            'linear_lsq_message':str(lin.message),
            'linear_lsq_cost':float(lin.cost),
            'linear_lsq_optimality':float(lin.optimality),
            'linear_lsq_max_abs_coordinate':float(np.max(np.abs(dx))),
            'linear_lsq_active_mask_nonzero':int(np.count_nonzero(lin.active_mask)),
            'exact_nonlinear_alpha_probes':probes,
        })

    payload_ok,payload_diag=payload_reproduction(rows,p18b.get('rows',[]))

    claim_boundary={
        'Repair16_relabelled':False,
        'Repair18_relabelled':False,
        'Repair18a_relabelled':False,
        'Repair18b_relabelled':False,
        'official_NPZ_written':False,
        'coefficient_changed':False,
        'source_changed':False,
        'sign_changed':False,
        'historical_threshold_changed':False,
        'branch_changed':False,
        'finite_eta_executed':False,
        'radial_points_removed':False,
        'K_clipping_used':False,
        'Q_linearized':False,
        'nonlinear_time_evolution_executed':False,
        'observational_claimed':False,
    }
    boundary_ok=bool(not any(claim_boundary.values()))

    g1=bool(provenance_ok)
    g2=bool(payload_ok)
    g3=bool(finite_all and len(rows)==3)
    g4=bool(boundary_ok)
    gates={
        'R18B1_G1_frozen_provenance':g1,
        'R18B1_G2_frozen_payload_reproduction':g2,
        'R18B1_G3_finite_diagnostic':g3,
        'R18B1_G4_claim_boundary':g4,
    }

    if not all(gates.values()):
        classification='NL1C7B4_REPAIR18B1_IMPLEMENTATION_FAIL'
        rc=2
    elif not structure_match_all:
        classification='NL1C7B4_REPAIR18B1_SPARSE_JACOBIAN_STRUCTURE_MISMATCH'
        rc=2
    elif not full_rank_all:
        classification='NL1C7B4_REPAIR18B1_LOCAL_PROJECTION_RANK_DEFICIENCY'
        rc=2
    else:
        classification='NL1C7B4_REPAIR18B1_FULL_RANK_JACOBIAN_DIAGNOSTIC_PASS'
        rc=0

    result={
        'classification':classification,
        'scope':'Repair18b1 harness-only Boolean provenance repair with exact reproduction of the frozen Repair18b Jacobian diagnostic payload.',
        'provenance':{
            **hashes,
            'repair18a_result_freeze_commit':'8cfce926a9075d77dd73c5bb5242c9d3e26b74ad',
            'repair18b_result_freeze_commit':'3edf1b11992008d7be383692369f28614ef94d6b',
            'repair18b1_prereg_commit':'df6968e904ec12c75276004cf4d5bd60486d91b0',
        },
        'canonical_branch':{'Y_kind':CANON_KIND,'beta0':CANON_BETA,'eta':0.0},
        'domain':{'lambda':1.0,'Nr':256,'scales_hinv_Mpc':[5.0,10.0,20.0]},
        'jacobian_lock':{
            'dense_method':'2-point',
            'sparse_method':'2-point',
            'relative_step':'SciPy default',
            'sparse_pattern':'Repair18a jac_pattern with half-band 16',
            'structure_match_limit':JAC_MATCH_LIMIT,
        },
        'linearized_probe_lock':{
            'solver':'scipy.optimize.lsq_linear',
            'method':'trf','tol':1e-12,'max_iter':500,
            'bounds':[-BOUND,BOUND],
            'alphas':list(ALPHAS),
        },
        'rows':rows,
        'payload_reproduction':payload_diag,
        'gates':gates,
        'summary':{
            'provenance_ok':provenance_ok,
            'payload_reproduction_ok':payload_ok,
            'finite_all':finite_all,
            'structure_match_all':structure_match_all,
            'full_rank_all':full_rank_all,
            'max_relative_Frobenius_sparse_vs_dense':float(max(x['relative_Frobenius_sparse_vs_dense'] for x in rows)) if rows else None,
            'min_sigma_min_over_sigma_max':float(min(x['dense_sigma_min_over_sigma_max'] for x in rows)) if rows else 0.0,
        },
        'claim_boundary':claim_boundary,
    }
    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
