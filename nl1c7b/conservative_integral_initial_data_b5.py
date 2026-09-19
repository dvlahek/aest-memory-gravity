#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares
from scipy.optimize._numdiff import approx_derivative
from scipy.sparse import lil_matrix

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair16 as r16
import nl1c7b.initial_constraint_certification_repair18a as r18a
import nl1c7b.initial_constraint_certification_repair19 as r19
import nl1c7b.initial_constraint_certification_repair19a as r19a
import nl1c7b.initial_constraint_certification_repair19c as r19c

R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA256='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R19C4_JSON_SHA256='a5a7416cd93120f543dbe0f8a70ddc735e9704212d7db5266de87980fe768c18'
R19C4_CLASS='NL1C7B4_REPAIR19C4_NO_MATERIAL_POST_FIRST_STEP_DERIVATIVE_WINDOW'
R19C4_FREEZE_COMMIT='4237da31c972fc961a2f7c961450a529652baa51'
PREREG_COMMIT='13a1e33cc170688441fe979a277c3826952de5e0'

METHOD='3-point'
ABS_STEP=3e-6
HALF_BAND=16
MAX_NFEV=200
REPRO_LIMIT=1e-12
CONSTRAINT_LIMIT=1e-7
GRID_RATIO_LIMIT=2.0
SAFETY_BOUND=0.5
TINY=1e-300


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def abs_or_rel_array(a,b,limit=REPRO_LIMIT):
    a=np.asarray(a,float); b=np.asarray(b,float)
    ae=np.abs(a-b)
    den=np.maximum(np.maximum(np.abs(a),np.abs(b)),TINY)
    re=ae/den
    good=(ae<=limit)|(re<=limit)
    return bool(np.all(good)),float(np.max(ae)),float(np.max(re))


def source_flux(st,kind,beta,qbg,zbg,funcs,dY,D=None):
    r=np.asarray(st['r'],float)
    if D is None:
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
    qscale=np.maximum(np.maximum(np.abs(qtarget),abs(qbg)),TINY)
    qerr=float(np.max(np.abs(qexact-qtarget)/qscale))

    z=zbg+dq/b4.Z0
    w=z*z
    with np.errstate(over='ignore',invalid='ignore'):
        ew=np.exp(w)
    args=[L,R,u,Lt,Rt,ut,pt,Lr,Rr,ur,pr]
    X=sh*pt+c*pr/L

    base_names=list(funcs.keys())
    expected=['GR_kin','GR_curv_NL','GR_curv_Rr','GR_Nr_boundary','AeST_E2','AeST_EX','AeST_X2']
    if base_names!=expected:
        raise RuntimeError(f'unexpected frozen source order: {base_names}')

    SH=np.zeros(n,float); FH=np.zeros(n,float)
    SM=np.zeros(n,float); FM=np.zeros(n,float)
    for name in base_names:
        fN,fNr,fb,fbr=[r18a.r2.arrval(f,args,n) for f in funcs[name]]
        fNr=np.asarray(fNr,float).copy()
        fbr=np.asarray(fbr,float).copy()
        fNr[0]=0.0
        fbr[0]=0.0
        SH+=np.asarray(fN,float)
        FH+=fNr
        SM+=np.asarray(fb,float)
        FM+=fbr

    dyN,dyNr,dyb,dybr=[r18a.r2.arrval(f,args,n) for f in dY]
    j,J=r1.jJ(kind,np.abs(X)/b4.A0_GEO,beta)
    P=L*R**2
    jN=-b4.C*(P*J+P*j*dyN)
    jNr=-b4.C*(P*j*dyNr)
    jb=-b4.C*(P*j*dyb)
    jbr=-b4.C*(P*j*dybr)
    jNr=np.asarray(jNr,float).copy()
    jbr=np.asarray(jbr,float).copy()
    jNr[0]=0.0
    jbr[0]=0.0
    SH+=np.asarray(jN,float)
    FH+=jNr
    SM+=np.asarray(jb,float)
    FM+=jbr

    kN=4.0*b4.K2*L*R**2*(b4.Z0*b4.Z0*np.expm1(w)-2.0*c*pt*b4.Z0*z*ew)
    kb=-8.0*b4.K2*L*R**2*c*pr*b4.Z0*z*ew
    SH+=kN
    SM+=kb

    v=np.arctanh(np.asarray(st['dust_vr'],float))
    varrho=b4.VAR_B*(1.0+np.asarray(st['delta_b'],float))
    SH+=-2.0*L*R**2*varrho*np.cosh(v)**2
    SM+=2.0*L**2*R**2*varrho*np.cosh(v)*np.sinh(v)
    SH+=-2.0*L*R**2*b4.RHO_STD

    # Analytic regular-center source limits.  The raw lambdified expressions
    # contain removable 0/0 forms at R=0, while the regular spherical limits
    # vanish.  B5 Repair01 changes only these two center values.
    SH[0]=0.0
    SM[0]=0.0

    numH=SH-D@FH
    numM=SM-D@FM
    non=np.arange(n)>0
    finite=bool(
        np.all(np.isfinite(SH[non])) and np.all(np.isfinite(FH[non]))
        and np.all(np.isfinite(SM[non])) and np.all(np.isfinite(FM[non]))
        and np.all(np.isfinite(numH[non])) and np.all(np.isfinite(numM[non]))
        and np.all(np.isfinite(L)) and np.all(L>0) and np.isfinite(qerr)
    )
    return {
        'finite':finite,'qerr':qerr,'L':L,'Rt':Rt,
        'SH':SH,'FH':FH,'SM':SM,'FM':FM,
        'numH':numH,'numM':numM,
    }


def cell_quadrature(r):
    r=np.asarray(r,float)
    n=len(r)
    if n<9:
        raise RuntimeError('need at least nine radial nodes')
    dr=np.diff(r)
    if not np.allclose(dr,dr[0],rtol=1e-12,atol=1e-15*max(abs(r[-1]),1.0)):
        raise RuntimeError('B5 preregistration requires the frozen uniform radial grid')
    W=np.zeros((n-1,n),float)
    for i in range(n-1):
        start=min(max(i-4,0),n-9)
        ids=np.arange(start,start+9)
        hcell=r[i+1]-r[i]
        u=(r[ids]-r[i])/hcell
        A=np.vstack([u**k for k in range(9)])
        moments=np.asarray([1.0/(k+1.0) for k in range(9)],float)
        w=hcell*np.linalg.solve(A,moments)
        W[i,ids]=w
    return W


def cell_pattern(n):
    m=n-1
    S=lil_matrix((2*m,2*m),dtype=np.int8)
    for i in range(m):
        right=i+1
        lo=max(1,right-HALF_BAND)
        hi=min(n-1,right+HALF_BAND)
        for j in range(lo,hi+1):
            jj=j-1
            S[i,jj]=1
            S[i,m+jj]=1
            S[m+i,jj]=1
            S[m+i,m+jj]=1
    return S.tocsr()


def build_problem(parent,scale,h,qbg,zbg,funcs,dY,B):
    n=len(parent['r'])
    m=n-1
    W=cell_quadrature(parent['r'])
    D=b4.dmat(np.asarray(parent['r'],float))
    sf0=source_flux(parent,r19c.CANON_KIND,r19c.CANON_BETA,qbg,zbg,funcs,dY,D=D)
    if not sf0['finite']:
        raise RuntimeError(f'nonfinite B5 parent source/flux scale={scale} Nr={n}')

    rawH=np.abs(sf0['FH'][1:])+np.abs(sf0['FH'][:-1])+np.abs(W)@np.abs(sf0['SH'])
    rawM=np.abs(sf0['FM'][1:])+np.abs(sf0['FM'][:-1])+np.abs(W)@np.abs(sf0['SM'])
    floorH=1e-14*max(float(np.max(rawH)),TINY)
    floorM=1e-14*max(float(np.max(rawM)),TINY)
    denH=rawH+floorH
    denM=rawM+floorM
    Rs=float(scale)/float(h)
    char_rt=b4.AI*b4.H_DIRECT*Rs
    pattern=cell_pattern(n)

    def fun_x(x):
        st=r18a.apply_projection(parent,np.asarray(x,float),char_rt)
        sf=source_flux(st,r19c.CANON_KIND,r19c.CANON_BETA,qbg,zbg,funcs,dY,D=D)
        if not sf['finite']:
            return np.full(2*m,1e100,float)
        cH=sf['FH'][1:]-sf['FH'][:-1]-W@sf['SH']
        cM=sf['FM'][1:]-sf['FM'][:-1]-W@sf['SM']
        return np.concatenate([cH/denH,cM/denM])

    def fun_z(z):
        x=np.asarray(B@np.asarray(z,float),float).ravel()
        return fun_x(x)

    def jac_z(z):
        x=np.asarray(B@np.asarray(z,float),float).ravel()
        Jx=approx_derivative(
            fun_x,x,method=METHOD,sparsity=pattern,abs_step=ABS_STEP
        )
        if hasattr(Jx,'tocsr'):
            Jx=Jx.tocsr()
        return Jx@B

    return sf0,W,denH,denM,char_rt,fun_x,fun_z,jac_z


def conservative_metrics(fun_x,x):
    f=np.asarray(fun_x(x),float)
    m=len(f)//2
    H=np.abs(f[:m]); M=np.abs(f[m:])
    return {
        'max_H':float(np.max(H)),
        'rms_H':float(np.sqrt(np.mean(H*H))),
        'max_M':float(np.max(M)),
        'rms_M':float(np.sqrt(np.mean(M*M))),
        'L2':float(np.linalg.norm(f)),
        'finite':bool(np.all(np.isfinite(f))),
    }


def solve_case(parent,scale,nr,h,qbg,zbg,funcs,dY,B):
    sf0,W,denH,denM,char_rt,fun_x,fun_z,jac_z=build_problem(
        parent,scale,h,qbg,zbg,funcs,dY,B
    )
    z0=np.zeros(B.shape[1],float)
    initial=conservative_metrics(fun_x,np.zeros(B.shape[0],float))
    if not initial['finite']:
        raise RuntimeError('nonfinite conservative residual after analytic regular-center source limit')

    sol=least_squares(
        fun_z,z0,jac=jac_z,method='trf',loss='linear',
        ftol=1e-12,xtol=1e-12,gtol=1e-12,max_nfev=MAX_NFEV,
        x_scale='jac',verbose=0,
    )
    z=np.asarray(sol.x,float)
    x=np.asarray(B@z,float).ravel()
    st=r18a.apply_projection(parent,x,char_rt)
    sf=source_flux(st,r19c.CANON_KIND,r19c.CANON_BETA,qbg,zbg,funcs,dY)
    ev=r18a.source_arrays(st,r19c.CANON_KIND,r19c.CANON_BETA,qbg,zbg,funcs,dY)
    freeze_ok,freeze_rows=r18a.field_freeze(parent,st)
    gy,gq=r19.gauge_values(x)
    corr=r18a.correction_metrics(parent,st,scale,h)
    final=conservative_metrics(fun_x,x)

    non=np.arange(nr)>0
    dh_ok,dh_abs,dh_rel=abs_or_rel_array(sf['numH'][non],ev['numH'][non])
    dm_ok,dm_abs,dm_rel=abs_or_rel_array(sf['numM'][non],ev['numM'][non])
    decomposition_final=bool(dh_ok and dm_ok)

    m=nr-1
    safe=bool(
        np.all(np.isfinite(z)) and np.all(np.isfinite(x))
        and sf['finite'] and ev.get('finite',False)
        and np.all(np.asarray(ev['L'])>0)
        and np.max(np.abs(x[:m]))<=SAFETY_BOUND
        and np.max(np.abs(x[m:]))<=SAFETY_BOUND
        and float(ev['qerr'])<=r19c.Q_LIMIT
        and abs(gy)<=r19c.GAUGE_LIMIT
        and abs(gq)<=r19c.GAUGE_LIMIT
        and freeze_ok
        and decomposition_final
    )
    exact=bool(
        safe
        and float(ev['maxH'])<=CONSTRAINT_LIMIT
        and float(ev['maxM'])<=CONSTRAINT_LIMIT
    )
    return {
        'scale_hinv_Mpc':float(scale),'Nr':int(nr),
        'solver':{
            'success':bool(sol.success),'status':int(sol.status),'message':str(sol.message),
            'nfev':int(sol.nfev),'njev':None if sol.njev is None else int(sol.njev),
            'cost':float(sol.cost),'optimality':float(sol.optimality),
        },
        'initial_conservative':initial,
        'initial_conservative_residual_finite':bool(initial['finite']),
        'final_conservative':final,
        'physical_correction_L2':float(np.linalg.norm(x)),
        'reduced_correction_L2':float(np.linalg.norm(z)),
        'max_abs_yL':float(np.max(np.abs(x[:m]))),
        'max_abs_qRt':float(np.max(np.abs(x[m:]))),
        'Q_target_max_normalized_error':float(ev['qerr']) if ev.get('finite',False) else None,
        'Y4_residual':float(gy),'Qmean_residual':float(gq),
        'field_freeze_pass':bool(freeze_ok),'field_freeze':freeze_rows,
        'decomposition_final':{
            'pass':decomposition_final,
            'H_max_abs_error':dh_abs,'H_max_relative_error':dh_rel,
            'M_max_abs_error':dm_abs,'M_max_relative_error':dm_rel,
        },
        'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else None,
        'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else None,
        'rms_epsilon_H':float(ev['rmsH']) if ev.get('finite',False) else None,
        'rms_epsilon_M':float(ev['rmsM']) if ev.get('finite',False) else None,
        'correction':corr,
        'safety_pass':safe,
        'differential_constraint_pass':exact,
    },st


def write_npz(path,states,h,ks):
    payload={
        'a_i':np.asarray(b4.AI),
        'h':np.asarray(h),
        'k_grid_Mpc_inv':np.asarray(ks,float),
        'scales_hinv_Mpc':np.asarray(b4.SCALES,float),
        'Nrs':np.asarray([256,512],int),
        'nl1c7b5_conservative_initial_data':np.asarray(True),
        'eta':np.asarray(0.0),
        'source_branch':np.asarray('Simple'),
        'beta':np.asarray(1.0),
        'projection':np.asarray('L=L_parent*exp(y_L); Rt=Rt_parent+q_Rt*(a H Rs)'),
        'gauge':np.asarray('Y4=0,Qmean=0'),
        'constructor':np.asarray('degree-8 local conservative cell balance + TRF'),
        'jacobian_method':np.asarray(METHOD),
        'jacobian_abs_step':np.asarray(ABS_STEP),
        'repair19c4_json_sha256':np.asarray(R19C4_JSON_SHA256),
        'repair15a_npz_sha256':np.asarray(R15A_NPZ_SHA256),
    }
    for (scale,nr),st in sorted(states.items()):
        prefix=f's{int(scale)}_n{int(nr)}_'
        for k,v in st.items():
            payload[prefix+k]=np.asarray(v,float)
    np.savez_compressed(path,**payload)


def validate_npz(path,states):
    p=Path(path)
    if not p.is_file() or p.stat().st_size<=0:
        return False,{'exists':False}
    z=np.load(p)
    ok=bool(
        bool(np.asarray(z['nl1c7b5_conservative_initial_data']))
        and float(np.asarray(z['eta']))==0.0
        and str(np.asarray(z['source_branch']))=='Simple'
        and float(np.asarray(z['beta']))==1.0
        and str(np.asarray(z['gauge']))=='Y4=0,Qmean=0'
        and str(np.asarray(z['jacobian_method']))==METHOD
        and float(np.asarray(z['jacobian_abs_step']))==ABS_STEP
        and str(np.asarray(z['repair19c4_json_sha256']))==R19C4_JSON_SHA256
        and str(np.asarray(z['repair15a_npz_sha256']))==R15A_NPZ_SHA256
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
                vv=np.asarray(v,float)
                ok &= arr.shape==vv.shape and np.array_equal(arr,vv)
            count+=1
    ok=bool(ok and len(states)==6)
    return ok,{
        'exists':True,'bytes':int(p.stat().st_size),'n_states':int(len(states)),
        'n_state_arrays_checked':int(count),'sha256':sha256_file(p),'pass':ok,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair15a-json',required=True)
    ap.add_argument('--repair15a-npz',required=True)
    ap.add_argument('--repair16-json',required=True)
    ap.add_argument('--repair19c4-json',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--state-npz',required=True)
    a=ap.parse_args()

    state_path=Path(a.state_npz)
    if state_path.exists():
        state_path.unlink()

    hashes={
        'repair15a_json':sha256_file(a.repair15a_json),
        'repair15a_npz':sha256_file(a.repair15a_npz),
        'repair16_json':sha256_file(a.repair16_json),
        'repair19c4_json':sha256_file(a.repair19c4_json),
    }
    expected={
        'repair15a_json':R15A_JSON_SHA256,
        'repair15a_npz':R15A_NPZ_SHA256,
        'repair16_json':R16_JSON_SHA256,
        'repair19c4_json':R19C4_JSON_SHA256,
    }

    p15=json.loads(Path(a.repair15a_json).read_text())
    p16=json.loads(Path(a.repair16_json).read_text())
    p19c4=json.loads(Path(a.repair19c4_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p15.get('classification')==r18a.R15A_CLASS
        and p16.get('classification')==r18a.R16_CLASS
        and p19c4.get('classification')==R19C4_CLASS
        and p19c4.get('material_derivative_window_identified') is False
        and p19c4.get('final_nonlinear_closure_execution_licensed') is False
        and all(p19c4.get('gates',{}).values())
        and p19c4.get('provenance',{}).get('repair15a_npz')==R15A_NPZ_SHA256
        and p19c4.get('provenance',{}).get('repair16_json')==R16_JSON_SHA256
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
    )

    ztrace=rec.read_trace(a.trace)
    ks,gs=rec.groups(ztrace)
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

    bases={}
    basis_rows=[]
    g3=True
    for nr in (256,512):
        br,Bc,Bo=r19a.basis_audit(nr)
        ok=bool(
            br['pass']
            and br['orth']['GB_Frobenius']<=r19c.GAUGE_LIMIT
            and br['orth']['orthonormality_Frobenius']<=r19c.GAUGE_LIMIT
            and abs(br['orth']['condition_number']-1.0)<=r19c.REPRO_LIMIT
        )
        bases[nr]=Bo
        basis_rows.append({'Nr':nr,'audit':br,'pass':ok})
        g3 &= ok

    parents={}
    for scale in b4.SCALES:
        parents[(scale,256)]=r16.load_primary_state(off,scale)
        parents[(scale,512)]=r16.reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    frozen16={
        (float(x['scale_hinv_Mpc']),int(x['Nr']),x['Y_kind'],float(x['beta0'])):x
        for x in p16['constraint_rows']
    }
    parent_repro=[]
    decomposition_rows=[]
    g2=True
    for scale in b4.SCALES:
        for nr in (256,512):
            parent=parents[(scale,nr)]
            ev=r18a.source_arrays(parent,r19c.CANON_KIND,r19c.CANON_BETA,qbg,zbg,funcs,dY)
            fr=frozen16[(float(scale),nr,r19c.CANON_KIND,r19c.CANON_BETA)]
            ph,ah,rh=r19c.smatch(ev['maxH'],fr['max_epsilon_H'])
            pm,am,rm=r19c.smatch(ev['maxM'],fr['max_epsilon_M'])
            repro=bool(ev.get('finite',False) and ph and pm)
            g1 &= repro
            parent_repro.append({
                'scale_hinv_Mpc':float(scale),'Nr':nr,'pass':repro,
                'H_abs_error':ah,'H_relative_error':rh,
                'M_abs_error':am,'M_relative_error':rm,
            })

            sf=source_flux(parent,r19c.CANON_KIND,r19c.CANON_BETA,qbg,zbg,funcs,dY)
            non=np.arange(nr)>0
            hok,ha,hr=abs_or_rel_array(sf['numH'][non],ev['numH'][non])
            mok,ma,mr=abs_or_rel_array(sf['numM'][non],ev['numM'][non])
            ok=bool(sf['finite'] and hok and mok)
            g2 &= ok
            decomposition_rows.append({
                'scale_hinv_Mpc':float(scale),'Nr':nr,'pass':ok,
                'H_max_abs_error':ha,'H_max_relative_error':hr,
                'M_max_abs_error':ma,'M_max_relative_error':mr,
            })
    g1=bool(g1)
    g2=bool(g2 and len(decomposition_rows)==6)
    g3=bool(g3 and len(basis_rows)==2)

    rows=[]
    solved_states={}
    g4=True
    g5=True
    g6=True
    for scale in b4.SCALES:
        for nr in (256,512):
            try:
                row,st=solve_case(
                    parents[(scale,nr)],scale,nr,h,qbg,zbg,funcs,dY,bases[nr]
                )
                row['attempted']=True
                solved_states[(scale,nr)]=st
                g5 &= bool(row['safety_pass'])
                g6 &= bool(row['differential_constraint_pass'])
            except Exception as exc:
                row={
                    'scale_hinv_Mpc':float(scale),'Nr':int(nr),'attempted':True,
                    'exception':f'{type(exc).__name__}: {exc}',
                    'safety_pass':False,'differential_constraint_pass':False,
                }
                g4=False
                g5=False
                g6=False
            rows.append(row)
    g4=bool(g4 and len(rows)==6 and all(r.get('attempted',False) for r in rows))
    g5=bool(g5 and len(solved_states)==6)
    g6=bool(g6 and len(solved_states)==6)

    grid_rows=[]
    g7=True
    if len(solved_states)==6:
        for scale in b4.SCALES:
            r256=next(r for r in rows if r['scale_hinv_Mpc']==float(scale) and r['Nr']==256)
            r512=next(r for r in rows if r['scale_hinv_Mpc']==float(scale) and r['Nr']==512)
            c256=float(r256['correction']['combined_norm'])
            c512=float(r512['correction']['combined_norm'])
            ratio=float(max(c256,c512)/max(min(c256,c512),TINY))
            ok=bool(np.isfinite(ratio) and ratio<=GRID_RATIO_LIMIT)
            g7 &= ok
            grid_rows.append({
                'scale_hinv_Mpc':float(scale),'C256':c256,'C512':c512,
                'symmetric_ratio':ratio,'limit':GRID_RATIO_LIMIT,'pass':ok,
            })
    else:
        g7=False

    claim_boundary={
        'eta_changed':False,
        'source_function_changed':False,
        'coefficient_changed':False,
        'sign_changed':False,
        'physical_field_added':False,
        'density_Q_bridge_changed':False,
        'source_branch_changed':False,
        'historical_constraint_threshold_changed':False,
        'radial_points_removed':False,
        'boundary_fit_from_results':False,
        'time_evolution_run':False,
        'finite_eta_claimed':False,
        'observational_claimed':False,
        'historical_result_relabelled':False,
        'solver_fallback_or_parameter_sweep':False,
    }
    g9=bool(not any(claim_boundary.values()))

    science_preoutput=bool(g1 and g2 and g3 and g4 and g5 and g6 and g7 and g9)
    if science_preoutput:
        state_path.parent.mkdir(parents=True,exist_ok=True)
        write_npz(state_path,solved_states,h,ks)
        g8,output=validate_npz(state_path,solved_states)
        output['written']=True
        output['exists_after_run']=state_path.exists()
    else:
        if state_path.exists():
            state_path.unlink()
        g8=bool(not state_path.exists())
        output={'written':False,'exists_after_run':state_path.exists(),'pass':g8}

    gates={
        'B5_G1_frozen_provenance':bool(g1),
        'B5_G2_conservative_decomposition_identity':bool(g2),
        'B5_G3_orthonormal_gauge_representation':bool(g3),
        'B5_G4_complete_conservative_construction':bool(g4),
        'B5_G5_safety_Q_gauge_field_freeze':bool(g5),
        'B5_G6_original_differential_exact_constraints':bool(g6),
        'B5_G7_two_grid_correction_control':bool(g7),
        'B5_G8_output_integrity':bool(g8),
        'B5_G9_claim_boundary':bool(g9),
    }

    implementation_ok=bool(g1 and g2 and g3 and g4 and g8 and g9)
    if not implementation_ok:
        classification='NL1C7B5_CONSERVATIVE_INITIAL_DATA_IMPLEMENTATION_FAIL'; rc=2
    elif not g5:
        classification='NL1C7B5_CONSERVATIVE_INITIAL_DATA_CONSTRUCTION_FAIL'; rc=2
    elif not g6:
        classification='NL1C7B5_CONSERVATIVE_DIFFERENTIAL_CERTIFICATION_FAIL'; rc=2
    elif not g7:
        classification='NL1C7B5_CONSERVATIVE_TWO_GRID_CONTROL_FAIL'; rc=2
    else:
        classification='NL1C7B5_CONSERVATIVE_INITIAL_DATA_CERTIFIED'; rc=0

    result={
        'classification':classification,
        'scope':'NL1C7B5 eta=0 conservative cell-integrated construction of the frozen two-field (L,Rt) initial state, certified only by the unchanged original B4 differential constraints.',
        'provenance':{
            **hashes,
            'repair19c4_result_freeze_commit':R19C4_FREEZE_COMMIT,
            'b5_prereg_commit':PREREG_COMMIT,
        },
        'constructor':{
            'unknowns':'orthonormal reduced coordinates z with x=B_orth z and x=(y_L,q_Rt)',
            'start':'z=0 only',
            'cell_balance':'F[i+1]-F[i]-integral_cell(S)=0',
            'cell_quadrature':'degree-8 Lagrange integral on frozen nine-node stencil',
            'normalization':'fixed parent cell flux-plus-source absolute scale with 1e-14 floor',
            'driver':'scipy.optimize.least_squares',
            'method':'trf','loss':'linear',
            'ftol':1e-12,'xtol':1e-12,'gtol':1e-12,'max_nfev':MAX_NFEV,
            'x_scale':'jac',
            'jacobian_method':METHOD,'jacobian_abs_step':ABS_STEP,
            'jacobian_physical_half_band':HALF_BAND,
            'fallbacks':False,'continuation':False,'multistart':False,
        },
        'limits':{
            'decomposition_abs_or_rel':REPRO_LIMIT,
            'exact_constraint':CONSTRAINT_LIMIT,
            'exact_Q':r19c.Q_LIMIT,
            'gauge':r19c.GAUGE_LIMIT,
            'safety_bound_yL_qRt':SAFETY_BOUND,
            'two_grid_ratio':GRID_RATIO_LIMIT,
        },
        'basis_rows':basis_rows,
        'parent_reproduction':parent_repro,
        'decomposition_identity':decomposition_rows,
        'case_rows':rows,
        'two_grid_control':grid_rows,
        'output':output,
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'case_count':len(rows),
            'safe_case_count':int(sum(bool(r.get('safety_pass',False)) for r in rows)),
            'differential_pass_count':int(sum(bool(r.get('differential_constraint_pass',False)) for r in rows)),
            'max_exact_epsilon_H':None if not solved_states else float(max(
                r['max_epsilon_H'] for r in rows if r.get('max_epsilon_H') is not None
            )),
            'max_exact_epsilon_M':None if not solved_states else float(max(
                r['max_epsilon_M'] for r in rows if r.get('max_epsilon_M') is not None
            )),
        },
        'project_boundary':{
            'eta0_short_time_evolution_licensed':bool(classification=='NL1C7B5_CONSERVATIVE_INITIAL_DATA_CERTIFIED'),
            'further_B5_solver_parameter_repairs_licensed':False,
            'finite_eta_certified':False,
            'observational_claimed':False,
            'physical_L_Rt_infeasibility_claimed_on_fail':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
