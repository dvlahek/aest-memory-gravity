#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize._numdiff import approx_derivative
from scipy.sparse import block_diag, csr_matrix
from scipy.sparse.linalg import lsmr

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair16 as r16
import nl1c7b.initial_constraint_certification_repair18a as r18a
import nl1c7b.initial_constraint_certification_repair19 as r19

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

R19_CLASS='NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_FAIL'
CANON_KIND='Simple'
CANON_BETA=1.0
ALPHAS=(1.0,0.5,0.25,0.125)
TINY=1e-300
REPRO_LIMIT=1e-12
GAUGE_LIMIT=1e-12
ORTH_LIMIT=1e-12
LINEAR_FEAS_LIMIT=1e-6
PHYSICAL_AGREE_LIMIT=1e-5


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


def helmert(m):
    rows=[]; cols=[]; data=[]
    for j in range(1,m):
        den=math.sqrt(j*(j+1.0))
        for i in range(j):
            rows.append(i); cols.append(j-1); data.append(1.0/den)
        rows.append(j); cols.append(j-1); data.append(-j/den)
    return csr_matrix((data,(rows,cols)),shape=(m,m-1),dtype=float)


def orth_basis(n):
    m=n-1
    Hy=helmert(4)
    if m==4:
        By=Hy
    else:
        By=block_diag((Hy,csr_matrix(np.eye(m-4))),format='csr')
    Bq=helmert(m)
    return block_diag((By,Bq),format='csr')


def basis_spectrum_chain(n):
    m=n-1
    sy=np.linalg.svd(np.array([
        [1.,0.,0.],
        [-1.,1.,0.],
        [0.,-1.,1.],
        [0.,0.,-1.],
    ]),compute_uv=False)
    qmin=2.0*math.sin(math.pi/(2.0*m))
    qmax=2.0*math.cos(math.pi/(2.0*m))
    smin=min(float(np.min(sy)),qmin,1.0)
    smax=max(float(np.max(sy)),qmax,1.0)
    return {'sigma_min':smin,'sigma_max':smax,'condition_number':smax/smin}


def basis_audit(n):
    Bc,_,_=r19.reduced_basis(n)
    Bo=orth_basis(n)
    gy,gq=r19.gauge_rows(n)
    G=np.vstack([gy,gq])
    cgb=float(np.linalg.norm(G@Bc.toarray()))
    ogb=float(np.linalg.norm(G@Bo.toarray()))
    oerr=float(np.linalg.norm((Bo.T@Bo).toarray()-np.eye(Bo.shape[1])))
    cs=basis_spectrum_chain(n)
    os={'sigma_min':1.0,'sigma_max':1.0,'condition_number':1.0}
    return {
        'Nr':int(n),
        'chain':{
            **cs,'shape':[int(Bc.shape[0]),int(Bc.shape[1])],
            'GB_Frobenius':cgb,
        },
        'orth':{
            **os,'shape':[int(Bo.shape[0]),int(Bo.shape[1])],
            'GB_Frobenius':ogb,
            'orthonormality_Frobenius':oerr,
        },
        'pass':bool(
            Bc.shape==Bo.shape==(2*(n-1),2*(n-1)-2)
            and cgb<=GAUGE_LIMIT and ogb<=GAUGE_LIMIT and oerr<=ORTH_LIMIT
        ),
    },Bc,Bo


def residual_builder(parent,scale,h,qbg,zbg,funcs,dY):
    base=r18a.source_arrays(parent,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
    if not base.get('finite',False):
        raise RuntimeError('nonfinite parent')
    n=len(parent['r']); m=n-1; non=np.arange(n)>0
    denomH=np.asarray(base['denH'][non]+base['floorH'],float)
    denomM=np.asarray(base['denM'][non]+base['floorM'],float)
    Rs=float(scale)/float(h)
    char_rt=b4.AI*b4.H_DIRECT*Rs

    def fun_x(x):
        st=r18a.apply_projection(parent,np.asarray(x,float),char_rt)
        ev=r18a.source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
        if not ev.get('finite',False):
            return np.full(2*m,1e6,float)
        return np.concatenate([
            np.asarray(ev['numH'][non]/denomH,float),
            np.asarray(ev['numM'][non]/denomM,float),
        ])
    return base,fun_x,char_rt


def lsmr_probe(J,F0,B):
    sol=lsmr(J,-F0,atol=1e-12,btol=1e-12,conlim=1e16,maxiter=10000)
    z=np.asarray(sol[0],float)
    dx=np.asarray(B@z).ravel()
    final=np.asarray(F0+J@z,float)
    rel=float(np.linalg.norm(final)/max(np.linalg.norm(F0),TINY))
    m=len(dx)//2
    return {
        'istop':int(sol[1]),'iterations':int(sol[2]),
        'normr_reported':float(sol[3]),'normar_reported':float(sol[4]),
        'normA_estimate':float(sol[5]),'condA_estimate':float(sol[6]),
        'normx_reported':float(sol[7]),
        'initial_residual_L2':float(np.linalg.norm(F0)),
        'final_linear_residual_L2':float(np.linalg.norm(final)),
        'relative_final_linear_residual':rel,
        'physical_dx_L2':float(np.linalg.norm(dx)),
        'max_abs_yL':float(np.max(np.abs(dx[:m]))),
        'max_abs_qRt':float(np.max(np.abs(dx[m:]))),
        'finite':bool(np.all(np.isfinite(z)) and np.all(np.isfinite(dx)) and np.all(np.isfinite(final))),
    },dx


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
    }
    expected={
        'repair15a_json':R15A_JSON_SHA256,'repair15a_npz':R15A_NPZ_SHA256,
        'repair16_json':R16_JSON_SHA256,'repair17_json':R17_JSON_SHA256,
        'repair18_json':R18_JSON_SHA256,'repair18a_json':R18A_JSON_SHA256,
        'repair18b_json':R18B_JSON_SHA256,'repair18b1_json':R18B1_JSON_SHA256,
        'repair18c_json':R18C_JSON_SHA256,'repair18d_json':R18D_JSON_SHA256,
        'repair18d1_json':R18D1_JSON_SHA256,'repair19_json':R19_JSON_SHA256,
    }
    p19=json.loads(Path(a.repair19_json).read_text())
    p16=json.loads(Path(a.repair16_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p19.get('classification')==R19_CLASS
        and p19.get('gates',{}).get('R19_G4_canonical_gauge_fixed_exact_nonlinear_closure') is False
        and p19.get('gates',{}).get('R19_G5_second_order_correction_scaling') is True
        and p19.get('gates',{}).get('R19_G8_field_freeze_invariant') is True
        and p19.get('output',{}).get('written') is False
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
    basis_map={}
    g2=True
    for nr in (256,512):
        br,Bc,Bo=basis_audit(nr)
        basis_rows.append(br); basis_map[nr]=(Bc,Bo)
        g2 &= br['pass']

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

    rows=[]
    g3=True; g4=True; g5=True; g6=True; g7=True
    for scale in b4.SCALES:
        for nr in (256,512):
            parent=states[(scale,nr)]
            base,fun_x,char_rt=residual_builder(parent,scale,h,qbg,zbg,funcs,dY)
            fr=frozen16[(float(scale),int(nr),CANON_KIND,CANON_BETA)]
            ph,ah,rh=scalar_match(base['maxH'],fr['max_epsilon_H'])
            pm,am,rm=scalar_match(base['maxM'],fr['max_epsilon_M'])
            repro=bool(ph and pm and base.get('finite',False))
            g3 &= repro

            n=len(parent['r']); m=n-1
            x0=np.zeros(2*m,float)
            F0=np.asarray(fun_x(x0),float)
            Jx=approx_derivative(fun_x,x0,method='2-point',sparsity=r18a.jac_pattern(n))
            if not hasattr(Jx,'tocsr'):
                Jx=csr_matrix(Jx)
            else:
                Jx=Jx.tocsr()

            Bc,Bo=basis_map[nr]
            Jc=(Jx@Bc).tocsr()
            Jo=(Jx@Bo).tocsr()
            pc,dxc=lsmr_probe(Jc,F0,Bc)
            po,dxo=lsmr_probe(Jo,F0,Bo)
            finite=bool(
                np.all(np.isfinite(Jx.data)) and np.all(np.isfinite(Jc.data)) and np.all(np.isfinite(Jo.data))
                and pc['finite'] and po['finite']
            )
            g4 &= finite
            linfeas=bool(
                pc['relative_final_linear_residual']<=LINEAR_FEAS_LIMIT
                and po['relative_final_linear_residual']<=LINEAR_FEAS_LIMIT
            )
            g5 &= linfeas

            pdiff=float(np.linalg.norm(dxc-dxo)/max(np.linalg.norm(dxc),np.linalg.norm(dxo),TINY))
            agree=bool(np.isfinite(pdiff) and pdiff<=PHYSICAL_AGREE_LIMIT)
            g6 &= agree

            probes=[]
            for alpha in ALPHAS:
                st=r18a.apply_projection(parent,alpha*dxo,char_rt)
                ev=r18a.source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
                non=np.arange(n)>0
                if ev.get('finite',False):
                    vec=np.concatenate([ev['epsH'][non],ev['epsM'][non]])
                    nl2=float(np.linalg.norm(vec)/math.sqrt(len(vec)))
                    qerr=float(ev['qerr'])
                    row={
                        'alpha':float(alpha),
                        'max_epsilon_H':float(ev['maxH']),
                        'max_epsilon_M':float(ev['maxM']),
                        'moving_normalized_residual_L2':nl2,
                        'Q_target_max_normalized_error':qerr,
                        'finite':True,
                    }
                    ok=bool(np.isfinite([nl2,qerr,ev['maxH'],ev['maxM']]).all() and qerr<=1e-12)
                else:
                    row={
                        'alpha':float(alpha),'max_epsilon_H':None,'max_epsilon_M':None,
                        'moving_normalized_residual_L2':None,'Q_target_max_normalized_error':None,
                        'finite':False,
                    }
                    ok=False
                probes.append(row)
                g7 &= ok

            rows.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                'parent_reproduction':{
                    'H_abs_error':ah,'H_relative_error':rh,
                    'M_abs_error':am,'M_relative_error':rm,'pass':repro,
                },
                'full_J_shape':[int(Jx.shape[0]),int(Jx.shape[1])],
                'full_J_nnz':int(Jx.nnz),
                'chain_reduced_shape':[int(Jc.shape[0]),int(Jc.shape[1])],
                'orth_reduced_shape':[int(Jo.shape[0]),int(Jo.shape[1])],
                'chain_linear_probe':pc,
                'orth_linear_probe':po,
                'physical_dx_relative_difference':pdiff,
                'physical_dx_agreement_pass':agree,
                'linear_feasibility_pass':linfeas,
                'exact_nonlinear_alpha_probes_orth_dx':probes,
            })

    g7=bool(g7 and len(rows)==6 and sum(len(r['exact_nonlinear_alpha_probes_orth_dx']) for r in rows)==24)
    claim_boundary={
        'state_artifact_written':False,'nonlinear_least_squares_run':False,
        'physical_field_added':False,'Y4_or_Qmean_changed':False,
        'source_changed':False,'coefficient_changed':False,'sign_changed':False,
        'finite_eta_executed':False,'branch_changed':False,'radial_points_removed':False,
        'historical_threshold_changed':False,'failed_case_removed':False,
        'time_evolution_run':False,'observational_claimed':False,'Repair19_relabelled':False,
    }
    g8=bool(not any(claim_boundary.values()))

    gates={
        'R19A_G1_exact_frozen_provenance':g1,
        'R19A_G2_exact_same_constrained_subspace':bool(g2),
        'R19A_G3_exact_parent_reproduction':bool(g3),
        'R19A_G4_finite_Jacobian_and_linear_probes':bool(g4),
        'R19A_G5_gauge_fixed_linear_feasibility':bool(g5),
        'R19A_G6_physical_coordinate_agreement':bool(g6),
        'R19A_G7_complete_nonlinear_alpha_probe':bool(g7),
        'R19A_G8_claim_boundary':g8,
    }

    impl_ok=bool(g1 and g2 and g3 and g4 and g7 and g8)
    if not impl_ok:
        classification='NL1C7B4_REPAIR19A_IMPLEMENTATION_FAIL'; rc=2
    elif not g5:
        classification='NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_INFEASIBILITY'; rc=2
    elif not g6:
        classification='NL1C7B4_REPAIR19A_REDUCED_COORDINATE_NUMERICAL_DISAGREEMENT'; rc=2
    else:
        classification='NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_CONDITIONING_CHARACTERIZED'; rc=0

    result={
        'classification':classification,
        'scope':'Repair19a diagnostic comparison of frozen chain versus orthonormal coordinates on exactly the same Y4=0/Qmean=0 physical subspace.',
        'provenance':{
            **hashes,
            'repair19_result_freeze_commit':'f42b238052d9db58f8eecf7098bd83c231863612',
            'repair19a_prereg_commit':'e022993a8f006c15e8a1ab845d0dc2837d9d4adb',
        },
        'basis_audit':basis_rows,
        'linear_feasibility_limit':LINEAR_FEAS_LIMIT,
        'physical_agreement_limit':PHYSICAL_AGREE_LIMIT,
        'rows':rows,
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'chain_condition_Nr256':next(x['chain']['condition_number'] for x in basis_rows if x['Nr']==256),
            'chain_condition_Nr512':next(x['chain']['condition_number'] for x in basis_rows if x['Nr']==512),
            'orth_condition':1.0,
            'max_chain_linear_relative_residual':float(max(r['chain_linear_probe']['relative_final_linear_residual'] for r in rows)),
            'max_orth_linear_relative_residual':float(max(r['orth_linear_probe']['relative_final_linear_residual'] for r in rows)),
            'max_physical_dx_relative_difference':float(max(r['physical_dx_relative_difference'] for r in rows)),
        },
    }
    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
