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
R18C_JSON_SHA256='d49600f8b27536aeb0dca28d1d777d09439a376241c7f8f93b74e754c502e24b'
R18D_JSON_SHA256='adc1410d50118c8080c1f84e5733cb09e5ff7d8f51a4937f1e306a96fe416def'

R18C_CLASS='NL1C7B4_REPAIR18C_TWO_MODE_NULLSPACE_CHARACTERIZED'
R18D_CLASS='NL1C7B4_REPAIR18D_IMPLEMENTATION_FAIL'
REPRO_LIMIT=1e-12
TRANSVERSE_LIMIT=1e-6
TIE_LIMIT=1e-12
TINY=1e-300

CANDIDATES=(
    ('Y1+Qmean','Y1','Qmean'),
    ('Y4+Qmean','Y4','Qmean'),
    ('Y8+Qmean','Y8','Qmean'),
    ('Y16+Qmean','Y16','Qmean'),
    ('Y1+Q1','Y1','Q1'),
)


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


def payload_match(rows,scores,selected,p18d):
    ok=True
    max_abs=0.0
    max_rel=0.0
    detail=[]

    frozen_rows={float(r['scale_hinv_Mpc']):r for r in p18d.get('rows',[])}
    for row in rows:
        scale=float(row['scale_hinv_Mpc'])
        fr=frozen_rows.get(scale)
        rok=fr is not None and int(row['rank'])==int(fr['rank']) and int(row['deficient_dimension'])==int(fr['deficient_dimension'])
        if fr is not None:
            fcs={x['candidate']:x for x in fr['candidates']}
            for cr in row['candidates']:
                fc=fcs.get(cr['candidate'])
                if fc is None:
                    rok=False
                    continue
                for k in ('sigma_max','sigma_min','sigma_min_over_sigma_max','condition_number','abs_det'):
                    same,ae,re=scalar_match(cr[k],fc[k])
                    rok &= same
                    max_abs=max(max_abs,ae); max_rel=max(max_rel,re)
                rok &= bool(cr['transverse_at_scale'])==bool(fc['transverse_at_scale'])
                rok &= cr['functional_rows']==fc['functional_rows']
        ok &= rok
        detail.append({'scale_hinv_Mpc':scale,'pass':bool(rok)})

    frozen_scores={x['candidate']:x for x in p18d.get('candidate_scores',[])}
    score_detail=[]
    for sc in scores:
        fs=frozen_scores.get(sc['candidate'])
        sok=fs is not None
        if fs is not None:
            sok &= int(sc['order'])==int(fs['order'])
            sok &= bool(sc['globally_transverse'])==bool(fs['globally_transverse'])
            for k in ('worst_scale_sigma_min','max_scale_sigma_min','max_condition_number','relative_sigma_min_spread'):
                same,ae,re=scalar_match(sc[k],fs[k])
                sok &= same
                max_abs=max(max_abs,ae); max_rel=max(max_rel,re)
        ok &= sok
        score_detail.append({'candidate':sc['candidate'],'pass':bool(sok)})

    fs=p18d.get('selected_pair')
    sel_ok=bool(selected is not None and fs is not None)
    if sel_ok:
        sel_ok &= selected['candidate']==fs['candidate']
        sel_ok &= int(selected['order'])==int(fs['order'])
        sel_ok &= bool(selected['globally_transverse'])==bool(fs['globally_transverse'])
        for k in ('worst_scale_sigma_min','max_scale_sigma_min','max_condition_number','relative_sigma_min_spread'):
            same,ae,re=scalar_match(selected[k],fs[k])
            sel_ok &= same
            max_abs=max(max_abs,ae); max_rel=max(max_rel,re)
    ok &= sel_ok
    return bool(ok and len(rows)==len(frozen_rows) and len(scores)==len(frozen_scores)),{
        'max_abs_error':float(max_abs),
        'max_relative_error':float(max_rel),
        'row_checks':detail,
        'score_checks':score_detail,
        'selected_pair_pass':bool(sel_ok),
        'limit_abs_or_rel':REPRO_LIMIT,
    }


def row_functional(name,m):
    v=np.zeros(2*m,float)
    if name=='Y1':
        v[0]=1.0
    elif name in ('Y4','Y8','Y16'):
        k=int(name[1:])
        v[:k]=1.0
    elif name=='Qmean':
        v[m:]=1.0
    elif name=='Q1':
        v[m]=1.0
    else:
        raise KeyError(name)
    n=float(np.linalg.norm(v))
    if n<=0 or not np.isfinite(n):
        raise RuntimeError(f'bad functional {name}')
    return v/n


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
    }
    p18c=json.loads(Path(a.repair18c_json).read_text())
    p18d=json.loads(Path(a.repair18d_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g18c=p18c.get('gates',{})
    g1=bool(
        hashes['repair15a_json']==R15A_JSON_SHA256
        and hashes['repair15a_npz']==R15A_NPZ_SHA256
        and hashes['repair16_json']==R16_JSON_SHA256
        and hashes['repair17_json']==R17_JSON_SHA256
        and hashes['repair18_json']==R18_JSON_SHA256
        and hashes['repair18a_json']==R18A_JSON_SHA256
        and hashes['repair18b_json']==R18B_JSON_SHA256
        and hashes['repair18b1_json']==R18B1_JSON_SHA256
        and hashes['repair18c_json']==R18C_JSON_SHA256
        and hashes['repair18d_json']==R18D_JSON_SHA256
        and p18c.get('classification')==R18C_CLASS
        and p18d.get('classification')==R18D_CLASS
        and len(p18d.get('gates',{}))==7
        and p18d.get('gates',{}).get('R18D_G2_exact_Repair18c_nullspace_reproduction') is False
        and all(v for k,v in p18d.get('gates',{}).items() if k!='R18D_G2_exact_Repair18c_nullspace_reproduction')
        and len(g18c)==6 and all(g18c.values())
        and p18c.get('summary',{}).get('all_rank_508_of_510') is True
        and p18c.get('summary',{}).get('all_deficient_dimension_2') is True
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

    frozen={float(r['scale_hinv_Mpc']):r for r in p18c['rows']}
    rows=[]
    reproduce=[]
    g2=True
    g3=True
    g4=True
    candidate_names=[x[0] for x in CANDIDATES]
    expected_names=['Y1+Qmean','Y4+Qmean','Y8+Qmean','Y16+Qmean','Y1+Q1']
    g3=bool(candidate_names==expected_names)

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
        V0=np.asarray(V[:,-2:],float)

        fr=frozen[float(scale)]
        checks={}
        vals={
            'rank':rank,
            'rank_tolerance':rank_tol,
            'sigma_max':smax,
            'sigma_min':smin,
            'sigma_ratio':float(smin/max(smax,TINY)),
        }
        frmap={
            'rank':'rank',
            'rank_tolerance':'rank_tolerance',
            'sigma_max':'sigma_max',
            'sigma_min':'sigma_min',
            'sigma_ratio':'sigma_min_over_sigma_max',
        }
        for k,val in vals.items():
            if k=='rank':
                ok=(int(val)==int(fr[frmap[k]]))
                checks[k]={'pass':ok,'observed':int(val),'frozen':int(fr[frmap[k]])}
            else:
                ok,ae,re=scalar_match(val,fr[frmap[k]])
                checks[k]={'pass':ok,'abs_error':ae,'relative_error':re}
            g2 &= checks[k]['pass']
        reproduce.append({'scale_hinv_Mpc':float(scale),'checks':checks,'pass':bool(all(x['pass'] for x in checks.values()))})

        crows=[]
        for cname,a1,a2 in CANDIDATES:
            gA=row_functional(a1,m)
            gB=row_functional(a2,m)
            norms=(float(np.linalg.norm(gA)),float(np.linalg.norm(gB)))
            dot=float(gA@gB)
            normalized=bool(abs(norms[0]-1.0)<=1e-14 and abs(norms[1]-1.0)<=1e-14 and abs(dot)<=1e-14)
            g3 &= normalized
            G=np.vstack([gA,gB])
            T=G@V0
            sv=np.linalg.svd(T,compute_uv=False)
            smaxT=float(sv[0]); sminT=float(sv[-1])
            ratio=float(sminT/max(smaxT,TINY))
            cond=float(smaxT/max(sminT,TINY))
            det=float(abs(np.linalg.det(T)))
            finite=bool(np.all(np.isfinite(T)) and np.all(np.isfinite(sv)) and np.isfinite([ratio,cond,det]).all())
            g4 &= finite
            crows.append({
                'candidate':cname,
                'functional_rows':[a1,a2],
                'functional_row_norms':list(norms),
                'functional_row_dot':dot,
                'functional_rows_normalized_and_orthogonal':normalized,
                'T':[[float(x) for x in row] for row in T],
                'sigma_max':smaxT,
                'sigma_min':sminT,
                'sigma_min_over_sigma_max':ratio,
                'condition_number':cond,
                'abs_det':det,
                'transverse_at_scale':bool(sminT>TRANSVERSE_LIMIT),
            })
        rows.append({
            'scale_hinv_Mpc':float(scale),
            'Nr':256,
            'rank':rank,
            'deficient_dimension':int(J.shape[1]-rank),
            'candidates':crows,
        })

    scores=[]
    for order,(cname,_,__) in enumerate(CANDIDATES):
        cr=[]
        for row in rows:
            rr=next(x for x in row['candidates'] if x['candidate']==cname)
            cr.append(rr)
        globally=bool(all(x['transverse_at_scale'] for x in cr))
        worst=float(min(x['sigma_min'] for x in cr))
        best=float(max(x['sigma_min'] for x in cr))
        scores.append({
            'candidate':cname,
            'order':order,
            'globally_transverse':globally,
            'worst_scale_sigma_min':worst,
            'max_scale_sigma_min':best,
            'max_condition_number':float(max(x['condition_number'] for x in cr)),
            'relative_sigma_min_spread':float((best-worst)/max(best,TINY)),
        })

    transverse=[x for x in scores if x['globally_transverse']]
    g5=bool(len(transverse)>=1)
    selected=None
    if transverse:
        # Frozen rule: largest worst-scale sigma_min; ties within abs-or-rel 1e-12 go to earlier order.
        selected=transverse[0]
        for cand in transverse[1:]:
            a0=float(selected['worst_scale_sigma_min'])
            b0=float(cand['worst_scale_sigma_min'])
            tie=bool(abs(a0-b0)<=TIE_LIMIT or abs(a0-b0)/max(abs(a0),abs(b0),TINY)<=TIE_LIMIT)
            if (b0>a0) and not tie:
                selected=cand

    recomputed=None
    if transverse:
        sorted_ref=sorted(
            transverse,
            key=lambda x:(-x['worst_scale_sigma_min'],x['order'])
        )
        # Resolve numerical ties explicitly according to prereg rule.
        recomputed=sorted_ref[0]
        for cand in transverse:
            if cand['order']==recomputed['order']:
                continue
            a0=float(recomputed['worst_scale_sigma_min'])
            b0=float(cand['worst_scale_sigma_min'])
            tie=bool(abs(a0-b0)<=TIE_LIMIT or abs(a0-b0)/max(abs(a0),abs(b0),TINY)<=TIE_LIMIT)
            if tie and cand['order']<recomputed['order']:
                recomputed=cand
        g6=bool(selected is not None and selected['candidate']==recomputed['candidate'])
    else:
        g6=False

    selected_detail=None
    if selected is not None:
        cname=selected['candidate']
        per=[]
        for row in rows:
            rr=next(x for x in row['candidates'] if x['candidate']==cname)
            per.append({
                'scale_hinv_Mpc':row['scale_hinv_Mpc'],
                'sigma_max':rr['sigma_max'],
                'sigma_min':rr['sigma_min'],
                'condition_number':rr['condition_number'],
                'abs_det':rr['abs_det'],
            })
        selected_detail={
            **selected,
            'per_scale':per,
        }

    payload_ok,payload_diag=payload_match(rows,scores,selected,p18d)

    claim_boundary={
        'nonlinear_state_modified_or_solved':False,
        'candidate_condition_imposed':False,
        'projection_pair_changed':False,
        'jacobian_rule_changed':False,
        'rank_rule_changed':False,
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
        'Repair18d_relabelled':False,
    }
    g7=bool(not any(claim_boundary.values()))

    gates={
        'R18D1_G1_frozen_provenance':g1,
        'R18D1_G2_exact_Repair18c_reproduction':bool(g2),
        'R18D1_G3_exact_Repair18d_transversality_payload_reproduction':bool(payload_ok),
        'R18D1_G4_deterministic_selected_pair':g6,
        'R18D1_G5_finite_diagnostic':bool(g4 and g5),
        'R18D1_G6_claim_boundary':g7,
    }
    if all(gates.values()):
        classification='NL1C7B4_REPAIR18D1_NULLSPACE_TRANSVERSALITY_AUDIT_PASS'; rc=0
    else:
        classification='NL1C7B4_REPAIR18D1_IMPLEMENTATION_FAIL'; rc=2

    result={
        'classification':classification,
        'scope':'Repair18d1 harness-only repair of the Repair18c SVD-path reproduction semantics with exact frozen Repair18d transversality payload reproduction.',
        'provenance':{
            **hashes,
            'repair18c_result_freeze_commit':'c29ce80b65435b60882bd5140a9cfe648b4f3a5b',
            'repair18d_result_freeze_commit':'1806635e031f269bfd9a9184fb148672941ad5c0',
            'repair18d1_prereg_commit':'72da0a2347e412b3f596afaa6a341532a9c5a2f1',
        },
        'domain':{
            'eta':0.0,'Y_kind':'Simple','beta0':1.0,'lambda':1.0,
            'Nr':256,'scales_hinv_Mpc':[float(s) for s in b4.SCALES],
        },
        'candidate_order':candidate_names,
        'transversality_limit_sigma_min':TRANSVERSE_LIMIT,
        'tie_limit_abs_or_rel':TIE_LIMIT,
        'reproduction':{
            'limit_abs_or_rel':REPRO_LIMIT,
            'rows':reproduce,
            'pass':bool(g2),
        },
        'rows':rows,
        'candidate_scores':scores,
        'selected_pair':selected_detail,
        'payload_reproduction':payload_diag,
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'n_candidates':len(CANDIDATES),
            'n_globally_transverse':int(sum(x['globally_transverse'] for x in scores)),
            'selected_candidate':None if selected is None else selected['candidate'],
            'selected_worst_scale_sigma_min':None if selected is None else selected['worst_scale_sigma_min'],
            'selected_max_condition_number':None if selected is None else selected['max_condition_number'],
        },
    }
    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
