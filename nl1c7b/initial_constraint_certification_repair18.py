#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares
from scipy.sparse import lil_matrix

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair02 as r2
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair10 as r10
import nl1c7b.initial_constraint_certification_repair16 as r16

R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA256='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R17_JSON_SHA256='09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e'
R15A_CLASS='NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED'
R16_CLASS='NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL'
R17_CLASS='NL1C7B4_REPAIR17_REPAIR16_SOURCE_LOCALIZATION_PASS'
LAMBDAS=(1.0,0.5,0.25,0.125)
CANON_KIND='Simple'
CANON_BETA=1.0
REPRO_LIMIT=1e-12
Q_LIMIT=1e-12
CONSTRAINT_LIMIT=1e-7
ORDER_MIN=1.8
ORDER_MAX=2.2
GRID_RATIO_LIMIT=2.0
HALF_BAND=16
MAX_NFEV=400

PERT_FIELDS=(
    'L_minus_a','R_minus_ar','Ldot_minus_aH','Rdot_minus_aHr',
    'u','udot','phi','phidot_minus_Q','delta_b','dust_vr',
    'X_from_chi','X_from_state','E_from_class','E_from_state',
)
PROJECT_FIELDS={'L_minus_a','Rdot_minus_aHr'}


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def virtual_state(parent, lam):
    out={k:np.asarray(v,float).copy() for k,v in parent.items()}
    for k in PERT_FIELDS:
        if k in out:
            out[k]=lam*np.asarray(parent[k],float)
    return out


def source_arrays(st, kind, beta, qbg, zbg, funcs, dY):
    r=np.asarray(st['r'],float)
    D=b4.dmat(r)
    n=len(r)
    L=b4.AI+np.asarray(st['L_minus_a'],float)
    R=b4.AI*r+np.asarray(st['R_minus_ar'],float)
    Lt=b4.AI*b4.H_DIRECT+np.asarray(st['Ldot_minus_aH'],float)
    Rt=b4.AI*b4.H_DIRECT*r+np.asarray(st['Rdot_minus_aHr'],float)
    u=np.asarray(st['u'],float)
    ut=np.asarray(st['udot'],float)
    pr=D@np.asarray(st['phi'],float)
    Lr=D@L
    Rr=D@R
    ur=D@u
    dq=np.asarray(st['phidot_minus_Q'],float)

    qtarget=qbg+dq
    c=np.cosh(u)
    sh=np.sinh(u)
    pt=(qtarget-sh*pr/L)/c
    qexact=c*pt+sh*pr/L
    qscale=np.maximum(np.maximum(np.abs(qtarget),abs(qbg)),1e-300)
    qerr=float(np.max(np.abs(qexact-qtarget)/qscale))

    z=zbg+dq/b4.Z0
    w=z*z
    with np.errstate(over='ignore',invalid='ignore'):
        ew=np.exp(w)
    args=[L,R,u,Lt,Rt,ut,pt,Lr,Rr,ur,pr]
    X=sh*pt+c*pr/L

    base_names=list(funcs.keys())
    expected=[
        'GR_kin','GR_curv_NL','GR_curv_Rr','GR_Nr_boundary',
        'AeST_E2','AeST_EX','AeST_X2',
    ]
    if base_names!=expected:
        raise RuntimeError(f'unexpected frozen source order: {base_names}')

    CH=[]
    CM=[]
    for name in base_names:
        fN,fNr,fb,fbr=[r2.arrval(f,args,n) for f in funcs[name]]
        fNr=np.array(fNr,copy=True)
        fbr=np.array(fbr,copy=True)
        fNr[0]=0.0
        fbr[0]=0.0
        CH.append(fN-D@fNr)
        CM.append(fb-D@fbr)

    dyN,dyNr,dyb,dybr=[r2.arrval(f,args,n) for f in dY]
    j,J=r1.jJ(kind,np.abs(X)/b4.A0_GEO,beta)
    P=L*R**2
    jN=-b4.C*(P*J+P*j*dyN)
    jNr=-b4.C*(P*j*dyNr)
    jb=-b4.C*(P*j*dyb)
    jbr=-b4.C*(P*j*dybr)
    jNr=np.array(jNr,copy=True)
    jbr=np.array(jbr,copy=True)
    jNr[0]=0.0
    jbr[0]=0.0
    CH.append(jN-D@jNr)
    CM.append(jb-D@jbr)

    kN=4.0*b4.K2*L*R**2*(
        b4.Z0*b4.Z0*np.expm1(w)-2.0*c*pt*b4.Z0*z*ew
    )
    kb=-8.0*b4.K2*L*R**2*c*pr*b4.Z0*z*ew
    CH.append(kN)
    CM.append(kb)

    v=np.arctanh(np.asarray(st['dust_vr'],float))
    varrho=b4.VAR_B*(1.0+np.asarray(st['delta_b'],float))
    CH.append(-2.0*L*R**2*varrho*np.cosh(v)**2)
    CM.append(2.0*L**2*R**2*varrho*np.cosh(v)*np.sinh(v))
    CH.append(-2.0*L*R**2*b4.RHO_STD)
    CM.append(np.zeros(n))

    CH=np.asarray(CH,float)
    CM=np.asarray(CM,float)
    noncenter=np.arange(n)>0
    finite=bool(
        np.all(np.isfinite(CH[:,noncenter]))
        and np.all(np.isfinite(CM[:,noncenter]))
        and np.all(np.isfinite(L))
        and np.all(L>0)
        and np.isfinite(qerr)
    )
    if not finite:
        return {
            'finite':False,'qerr':qerr,'L':L,'Rt':Rt,
            'CH':CH,'CM':CM,
        }

    numH=np.sum(CH,axis=0)
    numM=np.sum(CM,axis=0)
    denH=np.sum(np.abs(CH),axis=0)
    denM=np.sum(np.abs(CM),axis=0)
    preH=float(np.max(denH[noncenter]))
    preM=float(np.max(denM[noncenter]))
    floorH=1e-14*preH
    floorM=1e-14*preM
    epsH=np.abs(numH)/(denH+floorH)
    epsM=np.abs(numM)/(denM+floorM)
    return {
        'finite':True,'qerr':qerr,'L':L,'Rt':Rt,
        'CH':CH,'CM':CM,
        'numH':numH,'numM':numM,
        'denH':denH,'denM':denM,
        'floorH':floorH,'floorM':floorM,
        'epsH':epsH,'epsM':epsM,
        'maxH':float(np.max(epsH[noncenter])),
        'maxM':float(np.max(epsM[noncenter])),
        'rmsH':r2.rms(epsH[noncenter]),
        'rmsM':r2.rms(epsM[noncenter]),
    }


def jac_pattern(n):
    m=n-1
    S=lil_matrix((2*m,2*m),dtype=np.int8)
    for ii in range(m):
        i=ii+1
        lo=max(1,i-HALF_BAND)
        hi=min(n-1,i+HALF_BAND)
        for j in range(lo,hi+1):
            jj=j-1
            S[ii,jj]=1
            S[ii,m+jj]=1
            S[m+ii,jj]=1
            S[m+ii,m+jj]=1
    return S.tocsr()


def apply_projection(parent,x,char_rt):
    st={k:np.asarray(v,float).copy() for k,v in parent.items()}
    n=len(st['r'])
    m=n-1
    y=np.asarray(x[:m],float)
    drt=np.asarray(x[m:],float)
    Lp=b4.AI+np.asarray(parent['L_minus_a'],float)
    Rtp=b4.AI*b4.H_DIRECT*np.asarray(parent['r'],float)+np.asarray(parent['Rdot_minus_aHr'],float)
    L=Lp.copy()
    Rt=Rtp.copy()
    L[1:]=Lp[1:]*np.exp(y)
    Rt[1:]=Rtp[1:]+drt
    st['L_minus_a']=L-b4.AI
    st['Rdot_minus_aHr']=Rt-b4.AI*b4.H_DIRECT*np.asarray(parent['r'],float)
    return st


def correction_metrics(parent,solved,scale,h):
    r=np.asarray(parent['r'],float)
    Lp=b4.AI+np.asarray(parent['L_minus_a'],float)
    Ls=b4.AI+np.asarray(solved['L_minus_a'],float)
    Rtp=b4.AI*b4.H_DIRECT*r+np.asarray(parent['Rdot_minus_aHr'],float)
    Rts=b4.AI*b4.H_DIRECT*r+np.asarray(solved['Rdot_minus_aHr'],float)
    dL=Ls-Lp
    dRt=Rts-Rtp
    mask=np.arange(len(r))>0
    Rs=float(scale)/float(h)
    char_rt=b4.AI*b4.H_DIRECT*Rs
    nL=float(np.sqrt(np.mean((dL[mask]/b4.AI)**2)))
    nRt=float(np.sqrt(np.mean((dRt[mask]/char_rt)**2)))
    combined=float(math.sqrt(nL*nL+nRt*nRt))
    return {
        'deltaL_over_a_rms':nL,
        'deltaRt_over_aHRs_rms':nRt,
        'combined_norm':combined,
        'deltaL_abs_max':float(np.max(np.abs(dL[mask]))),
        'deltaRt_abs_max':float(np.max(np.abs(dRt[mask]))),
        'char_Rt':char_rt,
    }


def field_freeze(parent,solved):
    rows={}
    ok=True
    for k,v in parent.items():
        if k in PROJECT_FIELDS:
            continue
        same=bool(np.array_equal(np.asarray(v),np.asarray(solved[k])))
        rows[k]=same
        ok &= same
    return bool(ok),rows


def solve_projection(parent,scale,nr,h,qbg,zbg,funcs,dY):
    base=source_arrays(parent,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
    if not base.get('finite',False):
        raise RuntimeError(f'nonfinite parent scale={scale} Nr={nr}')

    n=len(parent['r'])
    m=n-1
    denomH=np.asarray(base['denH'][1:]+base['floorH'],float)
    denomM=np.asarray(base['denM'][1:]+base['floorM'],float)
    Rs=float(scale)/float(h)
    char_rt=b4.AI*b4.H_DIRECT*Rs

    def fun(x):
        st=apply_projection(parent,x,char_rt)
        ev=source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
        if not ev.get('finite',False):
            return np.full(2*m,1e6,dtype=float)
        return np.concatenate([
            np.asarray(ev['numH'][1:]/denomH,float),
            np.asarray(ev['numM'][1:]/denomM,float),
        ])

    x0=np.zeros(2*m,float)
    lb=np.concatenate([
        np.full(m,-0.5),
        np.full(m,-0.5*char_rt),
    ])
    ub=np.concatenate([
        np.full(m,0.5),
        np.full(m,0.5*char_rt),
    ])
    sol=least_squares(
        fun,x0,method='trf',jac='2-point',jac_sparsity=jac_pattern(n),
        bounds=(lb,ub),x_scale='jac',
        ftol=1e-12,xtol=1e-12,gtol=1e-12,max_nfev=MAX_NFEV,
        verbose=0,
    )
    st=apply_projection(parent,sol.x,char_rt)
    ev=source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
    freeze_ok,freeze_rows=field_freeze(parent,st)
    cm=correction_metrics(parent,st,scale,h)
    dist_low=np.min(sol.x-lb)
    dist_high=np.min(ub-sol.x)
    span=np.maximum(ub-lb,1e-300)
    rel_to_bound=float(min(
        np.min((sol.x-lb)/span),
        np.min((ub-sol.x)/span),
    ))
    return st,{
        'scale_hinv_Mpc':float(scale),
        'Nr':int(nr),
        'solver_success':bool(sol.success),
        'solver_status':int(sol.status),
        'solver_message':str(sol.message),
        'nfev':int(sol.nfev),
        'njev':None if sol.njev is None else int(sol.njev),
        'cost':float(sol.cost),
        'optimality':float(sol.optimality),
        'active_mask_nonzero':int(np.count_nonzero(sol.active_mask)),
        'minimum_relative_distance_to_bound':rel_to_bound,
        'canonical_parent_max_epsilon_H':float(base['maxH']),
        'canonical_parent_max_epsilon_M':float(base['maxM']),
        'canonical_projected_max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else float('inf'),
        'canonical_projected_max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else float('inf'),
        'canonical_projected_rms_epsilon_H':float(ev['rmsH']) if ev.get('finite',False) else float('inf'),
        'canonical_projected_rms_epsilon_M':float(ev['rmsM']) if ev.get('finite',False) else float('inf'),
        'exact_Q_max_normalized_error':float(ev['qerr']),
        'L_min':float(np.min(ev['L'])),
        'finite':bool(ev.get('finite',False)),
        'field_freeze_pass':freeze_ok,
        'field_freeze_rows':freeze_rows,
        'correction':cm,
    }


def slope(a,b):
    if not (np.isfinite(a) and np.isfinite(b) and a>0 and b>0):
        return None
    return float(math.log(a/b,2.0))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair15a-json',required=True)
    ap.add_argument('--repair15a-npz',required=True)
    ap.add_argument('--repair16-json',required=True)
    ap.add_argument('--repair17-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    h15j=sha256_file(a.repair15a_json)
    h15n=sha256_file(a.repair15a_npz)
    h16=sha256_file(a.repair16_json)
    h17=sha256_file(a.repair17_json)
    p15=json.loads(Path(a.repair15a_json).read_text())
    p16=json.loads(Path(a.repair16_json).read_text())
    p17=json.loads(Path(a.repair17_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    z=rec.read_trace(a.trace)
    ks,gs=rec.groups(z)
    tv_rec=rec.at_ai(gs,'pchip')
    ks_b4,gs_b4=b4.groups(b4.read_trace(a.trace))
    tv_b4=b4.at_ai(gs_b4)
    h=float(cov['h'])

    g15=p15.get('gates',{})
    g15i=p15.get('inherited_Repair15_gates',{})
    g16=p16.get('gates',{})
    g17=p17.get('gates',{})
    g1=bool(
        h15j==R15A_JSON_SHA256 and h15n==R15A_NPZ_SHA256
        and h16==R16_JSON_SHA256 and h17==R17_JSON_SHA256
        and p15.get('classification')==R15A_CLASS
        and p16.get('classification')==R16_CLASS
        and p17.get('classification')==R17_CLASS
        and len(g15)==3 and all(g15.values())
        and len(g15i)==6 and all(g15i.values())
        and g16.get('R16_G1_exact_Repair15a_provenance') is True
        and g16.get('R16_G2_Repair15a_state_anchor_reproduction') is True
        and g16.get('R16_G3_exact_nonlinear_dictionary') is True
        and g16.get('R16_G4_original_raw_B4_constraints') is False
        and g16.get('R16_G5_two_grid_control') is True
        and g16.get('R16_G6_claim_boundary') is True
        and len(g17)==6 and all(g17.values())
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
        and len(ks)==128 and np.array_equal(ks,ks_b4)
    )

    scalar_ai,scalar_independent,scalar_finite,_=r8.scalar_composites_at_ai(ks,gs,'pchip')
    scalar_identity=r16.rel_sym(scalar_ai,scalar_independent)
    kq_bg=float(np.median(tv_b4['KQ']))
    qbg=b4.stable_q_from_kq(kq_bg)
    kqq_bg=float(np.median(tv_rec['KQQ']))
    zbg=r9.stable_zbg(kq_bg)
    funcs,dY,kidentity=r1.build_nonK()
    g1=bool(
        g1 and scalar_finite and scalar_identity<=1e-10
        and np.isfinite([qbg,kqq_bg,zbg]).all() and kidentity
    )

    parent_full={}
    for scale in b4.SCALES:
        parent_full[(scale,256)]=r16.load_primary_state(off,scale)
        parent_full[(scale,512)]=r16.reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    frozen16={
        (float(x['scale_hinv_Mpc']),int(x['Nr']),str(x['Y_kind']),float(x['beta0'])):x
        for x in p16['constraint_rows']
    }
    reproduction=[]
    repro_ok=True
    for scale in b4.SCALES:
        for nr in (256,512):
            st=parent_full[(scale,nr)]
            ev=source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
            fr=frozen16[(float(scale),nr,CANON_KIND,CANON_BETA)]
            ph,ah,rh=r10.scalar_match(ev['maxH'],fr['max_epsilon_H'],REPRO_LIMIT)
            pm,am,rm=r10.scalar_match(ev['maxM'],fr['max_epsilon_M'],REPRO_LIMIT)
            ok=bool(ev.get('finite',False) and ph and pm)
            repro_ok &= ok
            reproduction.append({
                'scale_hinv_Mpc':float(scale),'Nr':nr,
                'H_abs_error':ah,'H_relative_error':rh,
                'M_abs_error':am,'M_relative_error':rm,
                'pass':ok,
            })
    g2=bool(repro_ok and len(reproduction)==6)

    solve_rows=[]
    solved_states={}
    freeze_all=True
    closure_all=True
    for scale in b4.SCALES:
        for nr in (256,512):
            for lam in LAMBDAS:
                vp=virtual_state(parent_full[(scale,nr)],lam)
                solved,row=solve_projection(vp,scale,nr,h,qbg,zbg,funcs,dY)
                row['lambda']=float(lam)
                row['constraint_limit']=CONSTRAINT_LIMIT
                row['Q_limit']=Q_LIMIT
                row['solve_closure_pass']=bool(
                    row['solver_success'] and row['finite'] and row['L_min']>0
                    and row['exact_Q_max_normalized_error']<=Q_LIMIT
                    and row['canonical_projected_max_epsilon_H']<=CONSTRAINT_LIMIT
                    and row['canonical_projected_max_epsilon_M']<=CONSTRAINT_LIMIT
                )
                solve_rows.append(row)
                solved_states[(scale,nr,lam)]=solved
                freeze_all &= row['field_freeze_pass']
                closure_all &= row['solve_closure_pass']

    g3=bool(len(solve_rows)==24 and closure_all)

    scaling=[]
    scaling_ok=True
    for scale in b4.SCALES:
        for nr in (256,512):
            vals=[
                next(x for x in solve_rows if x['scale_hinv_Mpc']==float(scale) and x['Nr']==nr and x['lambda']==lam)['correction']['combined_norm']
                for lam in LAMBDAS
            ]
            slopes=[slope(vals[i],vals[i+1]) for i in range(3)]
            gated=slopes[1:]
            ok=bool(all(s is not None and ORDER_MIN<=s<=ORDER_MAX for s in gated))
            scaling_ok &= ok
            scaling.append({
                'scale_hinv_Mpc':float(scale),'Nr':nr,
                'lambdas':list(LAMBDAS),'combined_norms':vals,
                'adjacent_log2_slopes':slopes,
                'gated_slope_indices':[1,2],
                'gated_range':[ORDER_MIN,ORDER_MAX],
                'pass':ok,
            })
    g4=bool(len(scaling)==6 and scaling_ok)

    grid=[]
    grid_ok=True
    for scale in b4.SCALES:
        c256=next(x for x in solve_rows if x['scale_hinv_Mpc']==float(scale) and x['Nr']==256 and x['lambda']==1.0)['correction']['combined_norm']
        c512=next(x for x in solve_rows if x['scale_hinv_Mpc']==float(scale) and x['Nr']==512 and x['lambda']==1.0)['correction']['combined_norm']
        ratio=max(c256,c512)/max(min(c256,c512),1e-300)
        ok=bool(np.isfinite(ratio) and ratio<=GRID_RATIO_LIMIT)
        grid_ok &= ok
        grid.append({
            'scale_hinv_Mpc':float(scale),
            'combined_norm_256':c256,
            'combined_norm_512':c512,
            'symmetric_ratio':float(ratio),
            'limit':GRID_RATIO_LIMIT,
            'pass':ok,
        })
    g5=bool(len(grid)==3 and grid_ok)
    g6=bool(freeze_all)

    # Nongating all-branch diagnostic at lambda=1 after canonical projection.
    branch_diag=[]
    for scale in b4.SCALES:
        for nr in (256,512):
            st=solved_states[(scale,nr,1.0)]
            for kind in ('Simple','Exponential','Sharp'):
                for beta in (1.0,0.5,0.1):
                    ev=source_arrays(st,kind,beta,qbg,zbg,funcs,dY)
                    branch_diag.append({
                        'scale_hinv_Mpc':float(scale),'Nr':nr,
                        'Y_kind':kind,'beta0':float(beta),
                        'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else float('inf'),
                        'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else float('inf'),
                        'historical_1e-7_pass':bool(
                            ev.get('finite',False)
                            and ev['maxH']<=CONSTRAINT_LIMIT
                            and ev['maxM']<=CONSTRAINT_LIMIT
                        ),
                    })

    claim_boundary={
        'official_NPZ_written':False,
        'Repair16_relabelled':False,
        'coefficient_changed':False,
        'source_changed':False,
        'sign_changed':False,
        'K_clipping_used':False,
        'Q_linearized':False,
        'radial_points_removed':False,
        'historical_threshold_changed':False,
        'solver_multistart_used':False,
        'finite_eta_executed':False,
        'nonlinear_time_evolution_executed':False,
        'observational_claimed':False,
    }
    g7=bool(not any(claim_boundary.values()))

    gates={
        'R18_G1_frozen_provenance':g1,
        'R18_G2_unprojected_lambda1_reproduction':g2,
        'R18_G3_canonical_nonlinear_solve_closure':g3,
        'R18_G4_second_order_correction_scaling':g4,
        'R18_G5_two_grid_correction_amplitude_control':g5,
        'R18_G6_field_freeze_invariant':g6,
        'R18_G7_claim_boundary':g7,
    }

    impl_ok=bool(g1 and g2 and g6 and g7)
    if not impl_ok:
        classification='NL1C7B4_REPAIR18_IMPLEMENTATION_FAIL'; rc=2
    elif not (g3 and g4 and g5):
        classification='NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_FAIL'; rc=2
    else:
        classification='NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_PASS'; rc=0

    result={
        'classification':classification,
        'scope':'Repair18 diagnostic feasibility of minimal exact nonlinear eta=0 constraint projection in L and R_t only; no official state artifact.',
        'provenance':{
            'repair15a_json_sha256':h15j,
            'repair15a_npz_sha256':h15n,
            'repair16_json_sha256':h16,
            'repair17_json_sha256':h17,
            'repair17_result_freeze_commit':'6a2cbd69218b63d8d7891e9deef43764365c47ff',
            'repair18_prereg_commit':'ddec97d478bfd667666830fb0e2203b7334464f5',
        },
        'projection_pair':['L_minus_a','Rdot_minus_aHr'],
        'canonical_branch':{'Y_kind':CANON_KIND,'beta0':CANON_BETA},
        'lambda_path':list(LAMBDAS),
        'solver_lock':{
            'method':'trf','initial_correction':'zero','x_scale':'jac',
            'ftol':1e-12,'xtol':1e-12,'gtol':1e-12,
            'max_nfev':MAX_NFEV,'jacobian_half_band':HALF_BAND,
            'yL_bounds':[-0.5,0.5],
            'deltaRt_over_aHRs_bounds':[-0.5,0.5],
            'multistart':False,
        },
        'unprojected_lambda1_reproduction':reproduction,
        'solve_rows':solve_rows,
        'correction_scaling':scaling,
        'two_grid_correction_amplitude':grid,
        'nongating_all_branch_lambda1_diagnostic':branch_diag,
        'summary':{
            'n_solves':len(solve_rows),
            'n_solver_success':int(sum(x['solver_success'] for x in solve_rows)),
            'n_canonical_constraint_pass':int(sum(x['solve_closure_pass'] for x in solve_rows)),
            'min_projected_max_epsilon_H':float(min(x['canonical_projected_max_epsilon_H'] for x in solve_rows)),
            'max_projected_max_epsilon_H':float(max(x['canonical_projected_max_epsilon_H'] for x in solve_rows)),
            'min_projected_max_epsilon_M':float(min(x['canonical_projected_max_epsilon_M'] for x in solve_rows)),
            'max_projected_max_epsilon_M':float(max(x['canonical_projected_max_epsilon_M'] for x in solve_rows)),
            'all_branch_lambda1_pass_count_nongating':int(sum(x['historical_1e-7_pass'] for x in branch_diag)),
            'all_branch_lambda1_total_nongating':len(branch_diag),
        },
        'gates':gates,
        'claim_boundary':claim_boundary,
        'interpretation_boundary':{
            'official_corrected_state_certified':False,
            'all_Y_beta_branches_certified':False,
            'nonlinear_evolution_certified':False,
        },
    }
    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
