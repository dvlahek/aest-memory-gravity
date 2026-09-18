#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares
from scipy.sparse import csr_matrix, block_diag

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair02 as r2
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
R18B1_JSON_SHA256='8e0d796e0368372d0b4cf75a075fba12ebde154b651d74929e745118c1ca6dab'
R18C_JSON_SHA256='d49600f8b27536aeb0dca28d1d777d09439a376241c7f8f93b74e754c502e24b'
R18D_JSON_SHA256='adc1410d50118c8080c1f84e5733cb09e5ff7d8f51a4937f1e306a96fe416def'
R18D1_JSON_SHA256='21d5be34660f0054bd8550908f300de64ec1ec9e8f81e0f150c7c1540e3bf04c'

R15A_CLASS='NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED'
R16_CLASS='NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL'
R17_CLASS='NL1C7B4_REPAIR17_REPAIR16_SOURCE_LOCALIZATION_PASS'
R18_CLASS='NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_FAIL'
R18A_CLASS='NL1C7B4_REPAIR18A_DIMENSIONLESS_RT_COORDINATE_FEASIBILITY_FAIL'
R18B_CLASS='NL1C7B4_REPAIR18B_IMPLEMENTATION_FAIL'
R18B1_CLASS='NL1C7B4_REPAIR18B1_LOCAL_PROJECTION_RANK_DEFICIENCY'
R18C_CLASS='NL1C7B4_REPAIR18C_TWO_MODE_NULLSPACE_CHARACTERIZED'
R18D_CLASS='NL1C7B4_REPAIR18D_IMPLEMENTATION_FAIL'
R18D1_CLASS='NL1C7B4_REPAIR18D1_NULLSPACE_TRANSVERSALITY_AUDIT_PASS'

LAMBDAS=(1.0,0.5,0.25,0.125)
KINDS=('Simple','Exponential','Sharp')
BETAS=(1.0,0.5,0.1)
CANON_KIND='Simple'
CANON_BETA=1.0

LIMIT=1e-7
Q_LIMIT=1e-12
GAUGE_LIMIT=1e-12
BASIS_LIMIT=1e-12
REPRO_LIMIT=1e-12
SLOPE_MIN=1.8
SLOPE_MAX=2.2
GRID_RATIO_LIMIT=2.0
SAFETY_BOUND=0.5
TINY=1e-300


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


def reduced_basis(n):
    m=n-1
    if m<4:
        raise ValueError('need at least four non-center points')

    # y_L basis: chain incidence on first four nodes + identity on nodes 5..m.
    rows=[]; cols=[]; data=[]
    c=0
    for j in range(3):
        rows.extend([j,j+1]); cols.extend([c,c]); data.extend([1.0,-1.0]); c+=1
    for j in range(4,m):
        rows.append(j); cols.append(c); data.append(1.0); c+=1
    By=csr_matrix((data,(rows,cols)),shape=(m,m-1),dtype=float)

    # q_Rt basis: path incidence; every vector has exactly zero sum.
    rows=[]; cols=[]; data=[]
    for j in range(m-1):
        rows.extend([j,j+1]); cols.extend([j,j]); data.extend([1.0,-1.0])
    Bq=csr_matrix((data,(rows,cols)),shape=(m,m-1),dtype=float)

    B=block_diag((By,Bq),format='csr')
    return B,By,Bq


def gauge_rows(n):
    m=n-1
    gy=np.zeros(2*m,float)
    gy[:4]=0.5  # normalized uniform row on first four y_L coordinates
    gq=np.zeros(2*m,float)
    gq[m:]=1.0/math.sqrt(m)
    return gy,gq


def reduced_pattern(n,B):
    Sfull=r18a.jac_pattern(n).astype(np.int8)
    A=B.copy()
    A.data=np.ones_like(A.data,dtype=np.int8)
    Sred=(Sfull@A).tocsr()
    Sred.data=np.ones_like(Sred.data,dtype=np.int8)
    Sred.eliminate_zeros()
    return Sred


def basis_audit(n):
    B,By,Bq=reduced_basis(n)
    gy,gq=gauge_rows(n)
    GB=np.vstack([gy,gq])@B.toarray()
    colnorm=np.sqrt(np.asarray(B.power(2).sum(axis=0)).ravel())
    # Analytic rank: path-incidence blocks each have m-1 independent columns.
    analytic_rank=2*(n-2)
    return {
        'n':int(n),
        'shape':[int(B.shape[0]),int(B.shape[1])],
        'expected_shape':[int(2*(n-1)),int(2*(n-1)-2)],
        'analytic_rank':int(analytic_rank),
        'expected_rank':int(B.shape[1]),
        'GB_Frobenius':float(np.linalg.norm(GB)),
        'max_abs_GB':float(np.max(np.abs(GB))),
        'min_column_norm':float(np.min(colnorm)),
        'max_column_norm':float(np.max(colnorm)),
        'finite':bool(np.all(np.isfinite(B.data)) and np.all(np.isfinite(colnorm))),
        'pass':bool(
            B.shape==(2*(n-1),2*(n-1)-2)
            and analytic_rank==B.shape[1]
            and np.linalg.norm(GB)<=BASIS_LIMIT
            and np.all(np.isfinite(colnorm))
            and np.all(colnorm>0)
        ),
    },B


def gauge_values(x):
    x=np.asarray(x,float)
    m=len(x)//2
    y=x[:m]; q=x[m:]
    return float(np.sum(y[:4])/2.0),float(np.sum(q)/math.sqrt(m))


def solve_one(parent,scale,nr,lam,h,qbg,zbg,funcs,dY,B,Sred):
    vp=r18a.virtual_state(parent,lam)
    base=r18a.source_arrays(vp,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
    if not base.get('finite',False):
        raise RuntimeError(f'nonfinite parent scale={scale} Nr={nr} lambda={lam}')

    n=len(vp['r']); m=n-1
    non=np.arange(n)>0
    denomH=np.asarray(base['denH'][non]+base['floorH'],float)
    denomM=np.asarray(base['denM'][non]+base['floorM'],float)
    Rs=float(scale)/float(h)
    char_rt=b4.AI*b4.H_DIRECT*Rs

    def fun(z):
        x=np.asarray(B@np.asarray(z,float)).ravel()
        st=r18a.apply_projection(vp,x,char_rt)
        ev=r18a.source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
        if not ev.get('finite',False):
            return np.full(2*m,1e6,float)
        return np.concatenate([
            np.asarray(ev['numH'][non]/denomH,float),
            np.asarray(ev['numM'][non]/denomM,float),
        ])

    z0=np.zeros(B.shape[1],float)
    res=least_squares(
        fun,z0,method='trf',jac='2-point',jac_sparsity=Sred,
        x_scale='jac',ftol=1e-12,xtol=1e-12,gtol=1e-12,
        max_nfev=400,
    )
    z=np.asarray(res.x,float)
    x=np.asarray(B@z).ravel()
    solved=r18a.apply_projection(vp,x,char_rt)
    ev=r18a.source_arrays(solved,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
    gy,gq=gauge_values(x)
    corr=r18a.correction_metrics(vp,solved,scale,h)
    freeze_ok,freeze_rows=r18a.field_freeze(vp,solved)

    maxy=float(np.max(np.abs(x[:m])))
    maxq=float(np.max(np.abs(x[m:])))
    closure=bool(
        res.success and np.all(np.isfinite(z)) and np.all(np.isfinite(x))
        and ev.get('finite',False) and np.all(ev['L']>0)
        and ev['qerr']<=Q_LIMIT
        and abs(gy)<=GAUGE_LIMIT and abs(gq)<=GAUGE_LIMIT
        and maxy<=SAFETY_BOUND and maxq<=SAFETY_BOUND
        and ev['maxH']<=LIMIT and ev['maxM']<=LIMIT
        and freeze_ok
    )
    row={
        'scale_hinv_Mpc':float(scale),'Nr':int(nr),'lambda':float(lam),
        'solver_success':bool(res.success),'solver_status':int(res.status),
        'solver_message':str(res.message),'nfev':int(res.nfev),
        'njev':None if res.njev is None else int(res.njev),
        'cost':float(res.cost),'optimality':float(res.optimality),
        'reduced_coordinate_count':int(len(z)),
        'full_coordinate_count':int(len(x)),
        'max_abs_reduced_coordinate':float(np.max(np.abs(z))),
        'max_abs_yL':maxy,'max_abs_qRt':maxq,
        'Y4_residual':gy,'Qmean_residual':gq,
        'Q_target_max_normalized_error':float(ev['qerr']) if ev.get('finite',False) else None,
        'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else None,
        'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else None,
        'rms_epsilon_H':float(ev['rmsH']) if ev.get('finite',False) else None,
        'rms_epsilon_M':float(ev['rmsM']) if ev.get('finite',False) else None,
        'correction':corr,
        'field_freeze_pass':bool(freeze_ok),
        'field_freeze':freeze_rows,
        'pass':closure,
    }
    return row,solved,x


def slopes(vals):
    out=[]
    for a,b in zip(vals[:-1],vals[1:]):
        if a>0 and b>0 and np.isfinite(a) and np.isfinite(b):
            out.append(float(math.log(a/b,2.0)))
        else:
            out.append(None)
    return out


def write_npz(path,states,h,ks):
    payload={
        'a_i':np.asarray(b4.AI),
        'h':np.asarray(h),
        'k_grid_Mpc_inv':np.asarray(ks,float),
        'scales_hinv_Mpc':np.asarray(b4.SCALES,float),
        'Nrs':np.asarray([256,512],int),
        'repair19_gauge_fixed_exact_nonlinear':np.asarray(True),
        'selected_conditions':np.asarray('Y4=0,Qmean=0'),
        'repair18d1_json_sha256':np.asarray(R18D1_JSON_SHA256),
        'parent_repair15a_npz_sha256':np.asarray(R15A_NPZ_SHA256),
    }
    for (scale,nr),st in sorted(states.items()):
        prefix=f's{int(scale)}_n{int(nr)}_'
        for k,v in st.items():
            payload[prefix+k]=np.asarray(v,float)
    np.savez_compressed(path,**payload)


def validate_npz(path,states):
    if not Path(path).is_file() or Path(path).stat().st_size<=0:
        return False,{'exists':False}
    z=np.load(path)
    ok=bool(
        bool(np.asarray(z['repair19_gauge_fixed_exact_nonlinear']))
        and str(np.asarray(z['selected_conditions']))=='Y4=0,Qmean=0'
        and str(np.asarray(z['repair18d1_json_sha256']))==R18D1_JSON_SHA256
        and str(np.asarray(z['parent_repair15a_npz_sha256']))==R15A_NPZ_SHA256
        and np.array_equal(np.asarray(z['Nrs']),np.asarray([256,512]))
    )
    count=0
    for (scale,nr),st in sorted(states.items()):
        prefix=f's{int(scale)}_n{int(nr)}_'
        for k,v in st.items():
            key=prefix+k
            present=key in z.files
            ok &= present
            if present:
                arr=np.asarray(z[key],float)
                ok &= arr.shape==np.asarray(v).shape and np.all(np.isfinite(arr))
            count+=1
    return bool(ok and len(states)==6),{
        'exists':True,'bytes':int(Path(path).stat().st_size),
        'n_states':int(len(states)),'n_state_arrays_checked':int(count),
        'sha256':sha256_file(path),'pass':bool(ok and len(states)==6),
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
    ap.add_argument('--repair18c-json',required=True)
    ap.add_argument('--repair18d-json',required=True)
    ap.add_argument('--repair18d1-json',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--state-npz',required=True)
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
    }
    parents={
        'r15a':json.loads(Path(a.repair15a_json).read_text()),
        'r16':json.loads(Path(a.repair16_json).read_text()),
        'r17':json.loads(Path(a.repair17_json).read_text()),
        'r18':json.loads(Path(a.repair18_json).read_text()),
        'r18a':json.loads(Path(a.repair18a_json).read_text()),
        'r18b':json.loads(Path(a.repair18b_json).read_text()),
        'r18b1':json.loads(Path(a.repair18b1_json).read_text()),
        'r18c':json.loads(Path(a.repair18c_json).read_text()),
        'r18d':json.loads(Path(a.repair18d_json).read_text()),
        'r18d1':json.loads(Path(a.repair18d1_json).read_text()),
    }
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    expected_hashes={
        'repair15a_json':R15A_JSON_SHA256,'repair15a_npz':R15A_NPZ_SHA256,
        'repair16_json':R16_JSON_SHA256,'repair17_json':R17_JSON_SHA256,
        'repair18_json':R18_JSON_SHA256,'repair18a_json':R18A_JSON_SHA256,
        'repair18b_json':R18B_JSON_SHA256,'repair18b1_json':R18B1_JSON_SHA256,
        'repair18c_json':R18C_JSON_SHA256,'repair18d_json':R18D_JSON_SHA256,
        'repair18d1_json':R18D1_JSON_SHA256,
    }
    classes_ok=bool(
        parents['r15a'].get('classification')==R15A_CLASS
        and parents['r16'].get('classification')==R16_CLASS
        and parents['r17'].get('classification')==R17_CLASS
        and parents['r18'].get('classification')==R18_CLASS
        and parents['r18a'].get('classification')==R18A_CLASS
        and parents['r18b'].get('classification')==R18B_CLASS
        and parents['r18b1'].get('classification')==R18B1_CLASS
        and parents['r18c'].get('classification')==R18C_CLASS
        and parents['r18d'].get('classification')==R18D_CLASS
        and parents['r18d1'].get('classification')==R18D1_CLASS
        and all(parents['r18d1'].get('gates',{}).values())
        and parents['r18d1'].get('summary',{}).get('selected_candidate')=='Y4+Qmean'
        and parents['r18d1'].get('payload_reproduction',{}).get('max_abs_error')==0.0
        and parents['r18d1'].get('payload_reproduction',{}).get('max_relative_error')==0.0
    )
    g1=bool(
        hashes==expected_hashes and classes_ok
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
    patterns={}
    for nr in (256,512):
        br,B=basis_audit(nr)
        basis_rows.append(br)
        bases[nr]=B
        patterns[nr]=reduced_pattern(nr,B)
    g2=bool(len(basis_rows)==2 and all(x['pass'] for x in basis_rows))

    states={}
    for scale in b4.SCALES:
        states[(scale,256)]=r16.load_primary_state(off,scale)
        states[(scale,512)]=r16.reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    frozen16={
        (float(x['scale_hinv_Mpc']),int(x['Nr']),x['Y_kind'],float(x['beta0'])):x
        for x in parents['r16']['constraint_rows']
    }
    repro=[]
    g3=True
    for scale in b4.SCALES:
        for nr in (256,512):
            ev=r18a.source_arrays(states[(scale,nr)],CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
            fr=frozen16[(float(scale),int(nr),CANON_KIND,CANON_BETA)]
            ph,ah,rh=scalar_match(ev['maxH'],fr['max_epsilon_H'])
            pm,am,rm=scalar_match(ev['maxM'],fr['max_epsilon_M'])
            ok=bool(ev.get('finite',False) and ph and pm)
            g3 &= ok
            repro.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                'H_abs_error':ah,'H_relative_error':rh,
                'M_abs_error':am,'M_relative_error':rm,'pass':ok,
            })

    solve_rows=[]
    solved={}
    g4=True
    freeze_all=True
    for scale in b4.SCALES:
        for nr in (256,512):
            for lam in LAMBDAS:
                row,st,x=solve_one(
                    states[(scale,nr)],scale,nr,lam,h,qbg,zbg,funcs,dY,
                    bases[nr],patterns[nr]
                )
                solve_rows.append(row)
                solved[(scale,nr,lam)]=st
                g4 &= row['pass']
                freeze_all &= row['field_freeze_pass']
    g4=bool(g4 and len(solve_rows)==24)

    scaling=[]
    g5=True
    for scale in b4.SCALES:
        for nr in (256,512):
            rr=sorted(
                [x for x in solve_rows if x['scale_hinv_Mpc']==float(scale) and x['Nr']==nr],
                key=lambda x:-x['lambda']
            )
            vals=[x['correction']['combined_norm'] for x in rr]
            ss=slopes(vals)
            ok=bool(
                len(ss)==3 and ss[1] is not None and ss[2] is not None
                and SLOPE_MIN<=ss[1]<=SLOPE_MAX
                and SLOPE_MIN<=ss[2]<=SLOPE_MAX
            )
            g5 &= ok
            scaling.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                'combined_norms':vals,'adjacent_log2_slopes':ss,
                'gated_pass':ok,
            })

    grid=[]
    g6=True
    for scale in b4.SCALES:
        c256=next(x['correction']['combined_norm'] for x in solve_rows if x['scale_hinv_Mpc']==float(scale) and x['Nr']==256 and x['lambda']==1.0)
        c512=next(x['correction']['combined_norm'] for x in solve_rows if x['scale_hinv_Mpc']==float(scale) and x['Nr']==512 and x['lambda']==1.0)
        ratio=float(max(c256,c512)/max(min(c256,c512),TINY))
        ok=bool(np.isfinite(ratio) and ratio<=GRID_RATIO_LIMIT)
        g6 &= ok
        grid.append({
            'scale_hinv_Mpc':float(scale),'C256':float(c256),'C512':float(c512),
            'symmetric_ratio':ratio,'limit':GRID_RATIO_LIMIT,'pass':ok,
        })

    branch_rows=[]
    g7=True
    for scale in b4.SCALES:
        for nr in (256,512):
            st=solved[(scale,nr,1.0)]
            for kind in KINDS:
                for beta in BETAS:
                    ev=r18a.source_arrays(st,kind,beta,qbg,zbg,funcs,dY)
                    ok=bool(ev.get('finite',False) and ev['maxH']<=LIMIT and ev['maxM']<=LIMIT)
                    g7 &= ok
                    branch_rows.append({
                        'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                        'Y_kind':kind,'beta0':float(beta),
                        'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else None,
                        'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else None,
                        'rms_epsilon_H':float(ev['rmsH']) if ev.get('finite',False) else None,
                        'rms_epsilon_M':float(ev['rmsM']) if ev.get('finite',False) else None,
                        'Q_target_max_normalized_error':float(ev['qerr']) if ev.get('finite',False) else None,
                        'pass':ok,
                    })
    g7=bool(g7 and len(branch_rows)==54)
    g8=bool(freeze_all)

    claim_boundary={
        'source_changed':False,'coefficient_changed':False,'sign_changed':False,
        'historical_threshold_changed':False,'radial_points_removed':False,
        'Q_linearized':False,'K_clipping_used':False,'finite_eta_executed':False,
        'branch_specific_state_solved':False,'multistart_used':False,
        'lambda_continuation_used':False,'historical_artifact_modified':False,
        'nonlinear_time_evolution_executed':False,'observational_claimed':False,
    }
    g10=bool(not any(claim_boundary.values()))

    state_npz=Path(a.state_npz)
    if state_npz.exists():
        state_npz.unlink()

    science_preoutput=bool(g1 and g2 and g3 and g4 and g5 and g6 and g7 and g8 and g10)
    output_info={'written':False,'pass':False}
    g9=False
    if science_preoutput:
        lambda1_states={(scale,nr):solved[(scale,nr,1.0)] for scale in b4.SCALES for nr in (256,512)}
        write_npz(state_npz,lambda1_states,h,ks)
        g9,output_info=validate_npz(state_npz,lambda1_states)
        output_info['written']=bool(state_npz.is_file())
    else:
        g9=bool(not state_npz.exists())
        output_info={'written':False,'pass':g9,'reason':'science gate failed before official state write'}

    gates={
        'R19_G1_exact_frozen_provenance':g1,
        'R19_G2_exact_reduced_basis_construction':g2,
        'R19_G3_unprojected_parent_reproduction':bool(g3),
        'R19_G4_canonical_gauge_fixed_exact_nonlinear_closure':bool(g4),
        'R19_G5_second_order_correction_scaling':bool(g5),
        'R19_G6_two_grid_correction_amplitude_control':bool(g6),
        'R19_G7_all_branch_exact_nonlinear_closure':bool(g7),
        'R19_G8_field_freeze_invariant':g8,
        'R19_G9_output_artifact_integrity':g9,
        'R19_G10_claim_boundary':g10,
    }

    impl_ok=bool(g1 and g2 and g3 and g8 and g10 and g9)
    science_ok=bool(g4 and g5 and g6 and g7)
    if not impl_ok:
        classification='NL1C7B4_REPAIR19_IMPLEMENTATION_FAIL'; rc=2
    elif not science_ok:
        classification='NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_FAIL'; rc=2
    else:
        classification='NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_PASS'; rc=0

    result={
        'classification':classification,
        'scope':'Repair19 gauge-fixed exact nonlinear eta=0 constraint closure in L/R_t using the independently certified Y4=0 and Qmean=0 null-space conditions.',
        'provenance':{
            **hashes,
            'repair18d1_result_freeze_commit':'814450553dc9680f13f329cb6e578350498163aa',
            'repair19_prereg_commit':'167eb24812d539dd273e6a5185d11c6402477940',
        },
        'selected_conditions':{
            'candidate':'Y4+Qmean','Y4_target':0.0,'Qmean_target':0.0,
            'imposed_by_exact_reduced_basis':True,
            'penalty_residual_used':False,
        },
        'solver_lock':{
            'method':'trf','jacobian':'2-point','x_scale':'jac',
            'ftol':1e-12,'xtol':1e-12,'gtol':1e-12,'max_nfev':400,
            'initial_reduced_coordinates':'zero',
            'multistart':False,'lambda_continuation':False,
            'explicit_reduced_coordinate_bounds':False,
            'full_coordinate_safety_bound':SAFETY_BOUND,
        },
        'basis_audit':basis_rows,
        'parent_reproduction':repro,
        'solve_rows':solve_rows,
        'correction_scaling':scaling,
        'two_grid_correction_control':grid,
        'all_branch_lambda1_rows':branch_rows,
        'output':output_info,
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'n_canonical_solves':len(solve_rows),
            'n_canonical_pass':int(sum(x['pass'] for x in solve_rows)),
            'n_all_branch_cases':len(branch_rows),
            'n_all_branch_pass':int(sum(x['pass'] for x in branch_rows)),
            'max_canonical_epsilon_H':max((x['max_epsilon_H'] for x in solve_rows if x['max_epsilon_H'] is not None),default=None),
            'max_canonical_epsilon_M':max((x['max_epsilon_M'] for x in solve_rows if x['max_epsilon_M'] is not None),default=None),
            'max_all_branch_epsilon_H':max((x['max_epsilon_H'] for x in branch_rows if x['max_epsilon_H'] is not None),default=None),
            'max_all_branch_epsilon_M':max((x['max_epsilon_M'] for x in branch_rows if x['max_epsilon_M'] is not None),default=None),
            'max_abs_Y4_residual':max(abs(x['Y4_residual']) for x in solve_rows),
            'max_abs_Qmean_residual':max(abs(x['Qmean_residual']) for x in solve_rows),
        },
        'interpretation_boundary':{
            'initial_constraints_certified':classification.endswith('_PASS'),
            'nonlinear_time_evolution_certified':False,
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
