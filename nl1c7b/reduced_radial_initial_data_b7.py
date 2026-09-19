#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair16 as r16
import nl1c7b.initial_constraint_certification_repair18a as r18a
import nl1c7b.initial_constraint_certification_repair19 as r19
import nl1c7b.initial_constraint_certification_repair19c as r19c

B6_JSON_SHA256='ed1efdac5dee72d8c57cbda23d074213babd15fdf3bc7adc18e61789f862e635'
B6_CLASS='NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS'
B6_FREEZE_COMMIT='70c9fc2aa58b76bf3579260e54c6d85097769160'
B7_PREREG_COMMIT='3d77dd915b1fe1f5b26d102e8c7d9f90ec508fca'

R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA256='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'

CANON_KIND='Simple'
CANON_BETA=1.0
POLY_LIMIT=1e-12
CENTER_L2_LIMIT=1e-6
OUTER_RT_LIMIT=1e-7
CONSTRAINT_LIMIT=1e-7
Q_LIMIT=1e-12
SAFETY_BOUND=0.5
GRID_RATIO_LIMIT=2.0
PRIMARY_LAUNCH=1e-5
CONTROL_LAUNCH=1e-4
ELL_BRACKET=(-0.5,0.5)
ROOT_XTOL=1e-12
ROOT_RTOL=1e-12
ROOT_MAXITER=100
IVP_RTOL=1e-11
IVP_ATOL=1e-13
TINY=1e-300

FROZEN_INTERP_FIELDS=(
    'R','Lt','u','ut','phi','qtarget','delta_b','dust_vr',
)


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def abs_or_rel_array(a,b,limit=POLY_LIMIT):
    a=np.asarray(a,float); b=np.asarray(b,float)
    d=np.abs(a-b)
    s=np.maximum(np.maximum(np.abs(a),np.abs(b)),TINY)
    rel=d/s
    ok=(d<=limit)|(rel<=limit)
    return bool(np.all(ok)),float(np.max(d)),float(np.max(rel))


def scalar_match(a,b,limit=1e-12):
    a=float(a); b=float(b)
    d=abs(a-b)
    r=d/max(abs(a),abs(b),TINY)
    return bool(d<=limit or r<=limit),float(d),float(r)


class LocalDegree8:
    def __init__(self,r,fields):
        self.r=np.asarray(r,float)
        self.n=len(self.r)
        if self.n<9:
            raise ValueError('need at least nine nodes')
        dr=np.diff(self.r)
        if not np.allclose(dr,dr[0],rtol=1e-12,atol=1e-15*max(abs(self.r[-1]),1.0)):
            raise RuntimeError('B7 requires the frozen uniform radial grid')
        self.dr=float(dr[0])
        self.names=tuple(fields.keys())
        Y=np.column_stack([np.asarray(fields[k],float) for k in self.names])
        if Y.shape!=(self.n,len(self.names)):
            raise RuntimeError('bad frozen interpolation field shape')
        self.coeff=[]
        for i in range(self.n-1):
            start=min(max(i-4,0),self.n-9)
            ids=np.arange(start,start+9)
            d=self.r[ids]-self.r[i]
            A=np.vstack([d**m for m in range(9)])
            self.coeff.append(np.linalg.solve(A.T,Y[ids,:]))
        self.coeff=np.asarray(self.coeff,float)

    def _cell(self,x):
        if x<=self.r[0]:
            return 0
        if x>=self.r[-1]:
            return self.n-2
        return min(max(int(math.floor((x-self.r[0])/self.dr)),0),self.n-2)

    def eval(self,x):
        i=self._cell(float(x))
        d=float(x)-self.r[i]
        c=self.coeff[i]
        p=np.asarray([d**m for m in range(9)],float)
        p1=np.asarray([0.0]+[m*d**(m-1) for m in range(1,9)],float)
        p2=np.asarray([0.0,0.0]+[m*(m-1)*d**(m-2) for m in range(2,9)],float)
        v=p@c
        d1=p1@c
        d2=p2@c
        return {
            name:(float(v[j]),float(d1[j]),float(d2[j]))
            for j,name in enumerate(self.names)
        }

    def derivative_reproduction(self,fields):
        D=b4.dmat(self.r)
        rows={}
        allok=True
        for name in self.names:
            y=np.asarray(fields[name],float)
            got=np.empty(self.n,float)
            for i in range(self.n):
                start=min(max(i-4,0),self.n-9)
                ids=np.arange(start,start+9)
                d=self.r[ids]-self.r[i]
                A=np.vstack([d**m for m in range(9)])
                coef=np.linalg.solve(A.T,y[ids])
                got[i]=coef[1]
            ref=D@y
            ok,ae,re=abs_or_rel_array(got,ref)
            rows[name]={
                'pass':ok,
                'max_abs_error':ae,
                'max_relative_error':re,
            }
            allok &= ok
        return bool(allok),rows


def build_exact_reduced_rhs():
    L,R,u,Lt,Rt,ut,q,pr,Rr,ur=sp.symbols(
        'L R u Lt Rt ut q pr Rr ur', real=True
    )
    Lr,Rtr=sp.symbols('Lr Rtr', real=True)
    Rrr,Ltr,utr,qr,prr,urr=sp.symbols(
        'Rrr Ltr utr qr prr urr', real=True
    )
    delta_b,dust_vr,qbg,zbg=sp.symbols(
        'delta_b dust_vr qbg zbg', real=True
    )

    N,b,Nr,br,pt=sp.symbols('N b Nr br pt', real=True)
    ch=sp.cosh(u); sh=sp.sinh(u)
    kL=(Lt-b*Lr-L*br)/(N*L)
    kR=(Rt-b*Rr)/(N*R)
    sigma=(pt-b*pr)/N
    Q=ch*sigma+sh*pr/L
    X=sh*sigma+ch*pr/L
    Y=X**2
    E=ch*((ut-b*ur)/N+Nr/(N*L))+sh*(kL+ur/L)
    P=N*L*R**2

    terms={
        'GR_kin':P*(-4*kL*kR-2*kR**2),
        'GR_curv_NL':2*N*L,
        'GR_curv_Rr':2*N*Rr**2/L,
        'GR_Nr_boundary':4*Nr*R*Rr/L,
        'AeST_E2':P*sp.Float(b4.KB)*E**2,
        'AeST_EX':P*sp.Float(2*b4.C)*E*X,
        'AeST_X2':-P*sp.Float(b4.C)*X**2,
    }
    expected=[
        'GR_kin','GR_curv_NL','GR_curv_Rr','GR_Nr_boundary',
        'AeST_E2','AeST_EX','AeST_X2',
    ]
    if list(terms.keys())!=expected:
        raise RuntimeError('unexpected exact source dictionary')

    gauge={N:1,b:0,Nr:0,br:0}
    pt_exact=(q-sh*pr/L)/ch

    def gs(expr):
        return expr.subs(gauge).subs(pt,pt_exact)

    fN={k:gs(sp.diff(t,N)) for k,t in terms.items()}
    fNr={k:gs(sp.diff(t,Nr)) for k,t in terms.items()}
    fb={k:gs(sp.diff(t,b)) for k,t in terms.items()}
    fbr={k:gs(sp.diff(t,br)) for k,t in terms.items()}

    Xg=gs(X)
    YN=gs(sp.diff(Y,N))
    YNr=gs(sp.diff(Y,Nr))
    Yb=gs(sp.diff(Y,b))
    Ybr=gs(sp.diff(Y,br))

    # Frozen B7 branch: Simple, beta=1.
    x=sp.Abs(Xg)/sp.Float(b4.A0_GEO)
    j=x/(2+x)
    J=2*sp.Float(b4.A0_GEO)**2*(
        x**2/2-2*x+4*sp.log((2+x)/2)
    )
    Pg=L*R**2
    jN=-sp.Float(b4.C)*(Pg*J+Pg*j*YN)
    jNr=-sp.Float(b4.C)*(Pg*j*YNr)
    jb=-sp.Float(b4.C)*(Pg*j*Yb)
    jbr=-sp.Float(b4.C)*(Pg*j*Ybr)

    z=zbg+(q-qbg)/sp.Float(b4.Z0)
    ew=sp.exp(z*z)
    kN=4*sp.Float(b4.K2)*L*R**2*(
        sp.Float(b4.Z0)**2*(ew-1)
        -2*ch*pt_exact*sp.Float(b4.Z0)*z*ew
    )
    kb=-8*sp.Float(b4.K2)*L*R**2*ch*pr*sp.Float(b4.Z0)*z*ew

    varrho=sp.Float(b4.VAR_B)*(1+delta_b)
    vv=sp.atanh(dust_vr)
    dustH=-2*L*R**2*varrho*sp.cosh(vv)**2
    dustM=2*L**2*R**2*varrho*sp.cosh(vv)*sp.sinh(vv)
    bgH=-2*L*R**2*sp.Float(b4.RHO_STD)

    SH=sum(fN.values())+jN+kN+dustH+bgH
    FH=sum(fNr.values())+jNr
    SM=sum(fb.values())+jb+kb+dustM
    FM=sum(fbr.values())+jbr

    vars_=(L,R,u,Lt,Rt,ut,q,pr,Rr,ur)
    ders_=(Lr,Rr,ur,Ltr,Rtr,utr,qr,prr,Rrr,urr)

    def ddr(expr):
        out=0
        for z0,z1 in zip(vars_,ders_):
            out += sp.diff(expr,z0)*z1
        return out

    H=SH-ddr(FH)
    M=SM-ddr(FM)

    AH=sp.diff(H,Lr)
    BH=H.subs(Lr,0)
    Lr_expr=-BH/AH

    AM=sp.diff(M,Rtr)
    M_no_rtr=M.subs(Rtr,0)
    BM=M_no_rtr.subs(Lr,Lr_expr)
    Rtr_expr=-BM/AM

    AH_target=(
        4*R*Rr
        +2*sp.Float(b4.KB)*R**2*ch*sh*(Lt+ur)
        +2*sp.Float(b4.C)*R**2*pr
    )/L**2

    checks={
        'H_AH_identity':bool(sp.simplify(AH-AH_target)==0),
        'H_independent_of_Rtr':bool(sp.simplify(sp.diff(H,Rtr))==0),
        'H_affine_in_Lr':bool(sp.simplify(sp.diff(H,Lr,2))==0),
        'M_Rtr_coefficient_identity':bool(sp.simplify(AM+4*L*R)==0),
        'M_independent_of_Rt':bool(sp.simplify(sp.diff(M,Rt))==0),
        'M_affine_in_Lr':bool(sp.simplify(sp.diff(M,Lr,2))==0),
        'j_H_flux_zero':bool(sp.simplify(jNr)==0),
        'j_M_flux_zero':bool(sp.simplify(jbr)==0),
    }
    structural_pass=bool(all(checks.values()))

    args=(
        L,R,u,Lt,Rt,ut,q,pr,Rr,ur,
        Rrr,Ltr,utr,qr,prr,urr,
        delta_b,dust_vr,qbg,zbg,
    )
    rhs=sp.lambdify(args,(Lr_expr,Rtr_expr),'numpy',cse=True)
    coeff=sp.lambdify(args,(AH,AM),'numpy',cse=True)

    return rhs,coeff,{
        'pass':structural_pass,
        'checks':checks,
        'A_H':str(AH_target),
        'A_M':str(-4*L*R),
    }


def frozen_fields(parent,qbg):
    r=np.asarray(parent['r'],float)
    return {
        'R':b4.AI*r+np.asarray(parent['R_minus_ar'],float),
        'Lt':b4.AI*b4.H_DIRECT+np.asarray(parent['Ldot_minus_aH'],float),
        'u':np.asarray(parent['u'],float),
        'ut':np.asarray(parent['udot'],float),
        'phi':np.asarray(parent['phi'],float),
        'qtarget':qbg+np.asarray(parent['phidot_minus_Q'],float),
        'delta_b':np.asarray(parent['delta_b'],float),
        'dust_vr':np.asarray(parent['dust_vr'],float),
    }


def local_args(interp,r,L,Rt,qbg,zbg):
    e=interp.eval(r)
    R,Rr,Rrr=e['R']
    Lt,Ltr,_=e['Lt']
    u,ur,urr=e['u']
    ut,utr,_=e['ut']
    _,pr,prr=e['phi']
    q,qr,_=e['qtarget']
    db,_,_=e['delta_b']
    dv,_,_=e['dust_vr']
    return (
        float(L),R,u,Lt,float(Rt),ut,q,pr,Rr,ur,
        Rrr,Ltr,utr,qr,prr,urr,db,dv,float(qbg),float(zbg),
    )


def integrate_trial(interp,scale,h,qbg,zbg,rhs_fun,ell0,launch_frac,profile):
    rgrid=interp.r
    r1=float(rgrid[1])
    eps=float(launch_frac*r1)
    Rs=float(scale)/float(h)
    char=float(b4.AI*b4.H_DIRECT*Rs)
    L0=float(b4.AI*math.exp(float(ell0)))
    e0=interp.eval(0.0)
    Lt0=float(e0['Lt'][0])
    Rr0=float(e0['R'][1])
    slope_rt=float(Lt0*Rr0/L0)
    w0=float(eps*slope_rt/char)

    def fun(rr,y):
        ell=float(y[0]); w=float(y[1])
        L=float(b4.AI*np.exp(ell))
        Rt=float(char*w)
        vals=rhs_fun(*local_args(interp,rr,L,Rt,qbg,zbg))
        Lr=float(np.asarray(vals[0]))
        Rtr=float(np.asarray(vals[1]))
        out=np.asarray([Lr/L,Rtr/char],float)
        if not np.all(np.isfinite(out)):
            raise FloatingPointError('nonfinite reduced radial RHS')
        return out

    t_eval=np.asarray(rgrid[1:],float) if profile else None
    try:
        sol=solve_ivp(
            fun,(eps,float(rgrid[-1])),np.asarray([ell0,w0],float),
            method='DOP853',rtol=IVP_RTOL,atol=IVP_ATOL,
            max_step=float(interp.dr),t_eval=t_eval,
        )
    except Exception as exc:
        return {
            'success':False,'exception':f'{type(exc).__name__}: {exc}',
            'ell0':float(ell0),'launch_fraction':float(launch_frac),
        }
    if not sol.success or sol.y.shape[1]==0 or not np.all(np.isfinite(sol.y)):
        return {
            'success':False,'message':str(sol.message),
            'ell0':float(ell0),'launch_fraction':float(launch_frac),
            'nfev':int(sol.nfev),
        }
    if profile:
        if sol.y.shape[1] != len(rgrid)-1:
            return {
                'success':False,'message':'incomplete profile sample',
                'ell0':float(ell0),'launch_fraction':float(launch_frac),
                'nfev':int(sol.nfev),
            }
        ell=np.empty(len(rgrid),float)
        w=np.empty(len(rgrid),float)
        ell[0]=float(ell0)
        w[0]=0.0
        ell[1:]=np.asarray(sol.y[0],float)
        w[1:]=np.asarray(sol.y[1],float)
        L=b4.AI*np.exp(ell)
        Rt=char*w
        return {
            'success':True,'ell0':float(ell0),
            'launch_fraction':float(launch_frac),
            'epsilon':eps,'center_Rt_slope':slope_rt,
            'nfev':int(sol.nfev),'L':L,'Rt':Rt,'ell':ell,'w':w,
            'outer_ell':float(ell[-1]),
        }
    return {
        'success':True,'ell0':float(ell0),
        'launch_fraction':float(launch_frac),
        'epsilon':eps,'center_Rt_slope':slope_rt,
        'nfev':int(sol.nfev),
        'outer_ell':float(sol.y[0,-1]),
        'outer_w':float(sol.y[1,-1]),
    }


def shoot_case(interp,scale,h,qbg,zbg,rhs_fun,launch_frac):
    cache={}
    calls=0

    def residual(ell0):
        nonlocal calls
        k=float(ell0)
        if k not in cache:
            cache[k]=integrate_trial(
                interp,scale,h,qbg,zbg,rhs_fun,k,launch_frac,False
            )
            calls += 1
        row=cache[k]
        if not row.get('success',False):
            raise RuntimeError(f'IVP failed during shooting at ell0={k}: {row}')
        return float(row['outer_ell'])

    lo,hi=ELL_BRACKET
    try:
        flo=residual(lo)
        fhi=residual(hi)
    except Exception as exc:
        return {
            'success':False,'exception':f'{type(exc).__name__}: {exc}',
            'launch_fraction':float(launch_frac),
        }
    bracket_ok=bool(
        np.isfinite([flo,fhi]).all()
        and (flo==0.0 or fhi==0.0 or np.signbit(flo)!=np.signbit(fhi))
    )
    if not bracket_ok:
        return {
            'success':False,'reason':'shooting_bracket_no_sign_change',
            'launch_fraction':float(launch_frac),
            'bracket':[float(lo),float(hi)],
            'bracket_residuals':[float(flo),float(fhi)],
        }
    try:
        root,info=brentq(
            residual,lo,hi,xtol=ROOT_XTOL,rtol=ROOT_RTOL,
            maxiter=ROOT_MAXITER,full_output=True,disp=False,
        )
    except Exception as exc:
        return {
            'success':False,'exception':f'{type(exc).__name__}: {exc}',
            'launch_fraction':float(launch_frac),
            'bracket':[float(lo),float(hi)],
            'bracket_residuals':[float(flo),float(fhi)],
        }
    prof=integrate_trial(
        interp,scale,h,qbg,zbg,rhs_fun,float(root),launch_frac,True
    )
    calls += 1
    if not prof.get('success',False):
        return {
            'success':False,'reason':'final_profile_integration_failed',
            'profile':prof,'launch_fraction':float(launch_frac),
        }
    prof['root_converged']=bool(info.converged)
    prof['root_iterations']=int(info.iterations)
    prof['root_function_calls']=int(info.function_calls)
    prof['total_ivp_calls']=int(calls)
    prof['bracket']=[float(lo),float(hi)]
    prof['bracket_residuals']=[float(flo),float(fhi)]
    prof['shooting_pass']=bool(
        info.converged and abs(float(prof['outer_ell']))<=1e-10
    )
    return prof


def build_state(parent,L,Rt):
    st={k:np.asarray(v,float).copy() for k,v in parent.items()}
    r=np.asarray(parent['r'],float)
    st['L_minus_a']=np.asarray(L,float)-b4.AI
    st['Rdot_minus_aHr']=np.asarray(Rt,float)-b4.AI*b4.H_DIRECT*r
    return st


def rel_l2(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(b),TINY))


def evaluate_primary(parent,L,Rt,scale,h,qbg,zbg,funcs,dY):
    st=build_state(parent,L,Rt)
    ev=r18a.source_arrays(st,CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY)
    freeze_ok,freeze_rows=r18a.field_freeze(parent,st)
    r=np.asarray(parent['r'],float)
    Lp=b4.AI+np.asarray(parent['L_minus_a'],float)
    Rtp=b4.AI*b4.H_DIRECT*r+np.asarray(parent['Rdot_minus_aHr'],float)
    Rs=float(scale)/float(h)
    char=float(b4.AI*b4.H_DIRECT*Rs)
    y=np.log(np.asarray(L[1:],float)/Lp[1:])
    qrt=(np.asarray(Rt[1:],float)-Rtp[1:])/char
    x=np.concatenate([y,qrt])
    gy,gq=r19.gauge_values(x)
    corr=r18a.correction_metrics(parent,st,scale,h)

    safe=bool(
        ev.get('finite',False)
        and np.all(np.asarray(L)>0)
        and np.all(np.isfinite(L))
        and np.all(np.isfinite(Rt))
        and float(ev.get('qerr',np.inf))<=Q_LIMIT
        and freeze_ok
        and np.max(np.abs(y))<=SAFETY_BOUND
        and np.max(np.abs(qrt))<=SAFETY_BOUND
    )
    exact=bool(
        safe
        and float(ev['maxH'])<=CONSTRAINT_LIMIT
        and float(ev['maxM'])<=CONSTRAINT_LIMIT
    )
    return st,{
        'safety_pass':safe,
        'field_freeze_pass':bool(freeze_ok),
        'field_freeze':freeze_rows,
        'Q_target_max_normalized_error':float(ev.get('qerr',np.inf)),
        'max_abs_log_L_over_parent':float(np.max(np.abs(y))),
        'max_abs_qRt_correction':float(np.max(np.abs(qrt))),
        'Y4_descriptive':float(gy),
        'Qmean_descriptive':float(gq),
        'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else None,
        'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else None,
        'rms_epsilon_H':float(ev['rmsH']) if ev.get('finite',False) else None,
        'rms_epsilon_M':float(ev['rmsM']) if ev.get('finite',False) else None,
        'differential_constraint_pass':exact,
        'correction':corr,
    }


def write_npz(path,states):
    payload={}
    for (scale,nr),st in states.items():
        tag=f's{int(scale)}_n{int(nr)}'
        for k,v in st.items():
            payload[f'{tag}_{k}']=np.asarray(v)
    np.savez(path,**payload)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair15a-json',required=True)
    ap.add_argument('--repair15a-npz',required=True)
    ap.add_argument('--repair16-json',required=True)
    ap.add_argument('--b6-json',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--state-npz',required=True)
    a=ap.parse_args()

    hashes={
        'repair15a_json':sha256_file(a.repair15a_json),
        'repair15a_npz':sha256_file(a.repair15a_npz),
        'repair16_json':sha256_file(a.repair16_json),
        'b6_json':sha256_file(a.b6_json),
    }
    expected={
        'repair15a_json':R15A_JSON_SHA256,
        'repair15a_npz':R15A_NPZ_SHA256,
        'repair16_json':R16_JSON_SHA256,
        'b6_json':B6_JSON_SHA256,
    }

    p15=json.loads(Path(a.repair15a_json).read_text())
    p16=json.loads(Path(a.repair16_json).read_text())
    pb6=json.loads(Path(a.b6_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p15.get('classification')==r18a.R15A_CLASS
        and p16.get('classification')==r18a.R16_CLASS
        and pb6.get('classification')==B6_CLASS
        and pb6.get('project_boundary',{}).get('reduced_radial_numerical_construction_licensed') is True
        and pb6.get('project_boundary',{}).get('eta0_short_time_evolution_licensed') is False
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
        and np.isfinite([qbg,kqq_bg,zbg]).all()
        and bool(kidentity)
    )

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
    for scale in b4.SCALES:
        for nr in (256,512):
            ev=r18a.source_arrays(
                parents[(scale,nr)],CANON_KIND,CANON_BETA,qbg,zbg,funcs,dY
            )
            fr=frozen16[(float(scale),nr,CANON_KIND,CANON_BETA)]
            ph,ah,rh=scalar_match(ev['maxH'],fr['max_epsilon_H'])
            pm,am,rm=scalar_match(ev['maxM'],fr['max_epsilon_M'])
            ok=bool(ev.get('finite',False) and ph and pm)
            g1 &= ok
            parent_repro.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),'pass':ok,
                'H_abs_error':ah,'H_relative_error':rh,
                'M_abs_error':am,'M_relative_error':rm,
            })

    rhs_fun,coeff_fun,rhs_audit=build_exact_reduced_rhs()
    g3=bool(rhs_audit['pass'])

    poly_rows=[]
    case_context={}
    g2=True
    for scale in b4.SCALES:
        for nr in (256,512):
            parent=parents[(scale,nr)]
            ff=frozen_fields(parent,qbg)
            interp=LocalDegree8(parent['r'],ff)
            pok,prows=interp.derivative_reproduction(ff)
            g2 &= pok
            poly_rows.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                'pass':bool(pok),'fields':prows,
            })
            case_context[(scale,nr)]=(interp,parent)

    case_rows=[]
    solved_states={}
    construct_ok=True
    center_ok=True
    outer_ok=True
    safety_ok=True
    exact_ok=True

    for scale in b4.SCALES:
        for nr in (256,512):
            interp,parent=case_context[(scale,nr)]
            primary=shoot_case(interp,scale,h,qbg,zbg,rhs_fun,PRIMARY_LAUNCH)
            control=shoot_case(interp,scale,h,qbg,zbg,rhs_fun,CONTROL_LAUNCH)
            c_ok=bool(
                primary.get('success',False) and primary.get('shooting_pass',False)
                and control.get('success',False) and control.get('shooting_pass',False)
            )
            construct_ok &= c_ok
            row={
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                'primary_launch':{
                    k:v for k,v in primary.items()
                    if k not in ('L','Rt','ell','w')
                },
                'control_launch':{
                    k:v for k,v in control.items()
                    if k not in ('L','Rt','ell','w')
                },
                'construction_pass':c_ok,
            }
            if not c_ok:
                row.update({
                    'center_control_pass':False,
                    'outer_Rt_compatibility_pass':False,
                    'safety_pass':False,
                    'differential_constraint_pass':False,
                })
                center_ok=False; outer_ok=False; safety_ok=False; exact_ok=False
                case_rows.append(row)
                continue

            Lp=np.asarray(primary['L'],float)
            Rtp=np.asarray(primary['Rt'],float)
            Lc=np.asarray(control['L'],float)
            Rtc=np.asarray(control['Rt'],float)
            dL=rel_l2(Lc,Lp)
            dRt=rel_l2(Rtc,Rtp)
            cc=bool(dL<=CENTER_L2_LIMIT and dRt<=CENTER_L2_LIMIT)
            center_ok &= cc

            rmax=float(parent['r'][-1])
            rtbg=float(b4.AI*b4.H_DIRECT*rmax)
            ort=float(abs(Rtp[-1]-rtbg)/max(abs(rtbg),TINY))
            op=bool(ort<=OUTER_RT_LIMIT)
            outer_ok &= op

            st,ev=evaluate_primary(
                parent,Lp,Rtp,scale,h,qbg,zbg,funcs,dY
            )
            safety_ok &= bool(ev['safety_pass'])
            exact_ok &= bool(ev['differential_constraint_pass'])
            solved_states[(scale,nr)]=st

            # Descriptive exact reduced coefficient check on final grid nodes.
            coeff_min_H=np.inf
            coeff_min_M=np.inf
            coeff_finite=True
            for i,rr in enumerate(np.asarray(parent['r'],float)[1:],start=1):
                e=interp.eval(float(rr))
                args=local_args(
                    interp,float(rr),float(Lp[i]),float(Rtp[i]),qbg,zbg
                )
                aa=coeff_fun(*args)
                ah=float(np.asarray(aa[0])); am=float(np.asarray(aa[1]))
                coeff_finite &= bool(np.isfinite([ah,am]).all())
                coeff_min_H=min(coeff_min_H,abs(ah))
                coeff_min_M=min(coeff_min_M,abs(am))

            row.update({
                'center_control':{
                    'L_relative_L2':dL,
                    'Rt_relative_L2':dRt,
                    'limit':CENTER_L2_LIMIT,
                    'pass':cc,
                },
                'outer_Rt_compatibility':{
                    'R_t_outer':float(Rtp[-1]),
                    'R_t_background':rtbg,
                    'relative_mismatch':ort,
                    'limit':OUTER_RT_LIMIT,
                    'pass':op,
                },
                'final_reduced_coefficients':{
                    'finite':bool(coeff_finite),
                    'min_abs_A_H_noncenter':float(coeff_min_H),
                    'min_abs_A_M_noncenter':float(coeff_min_M),
                },
                **ev,
            })
            case_rows.append(row)

    g4=bool(construct_ok)
    g5=bool(g4 and center_ok)
    g6=bool(g4 and outer_ok)
    g7=bool(g4 and safety_ok)
    g8=bool(g4 and exact_ok)

    two_grid=[]
    g9=True
    if all((s,n) in solved_states for s in b4.SCALES for n in (256,512)):
        for scale in b4.SCALES:
            c256=r18a.correction_metrics(
                parents[(scale,256)],solved_states[(scale,256)],scale,h
            )['combined_norm']
            c512=r18a.correction_metrics(
                parents[(scale,512)],solved_states[(scale,512)],scale,h
            )['combined_norm']
            ratio=float(max(c256/max(c512,TINY),c512/max(c256,TINY)))
            ok=bool(np.isfinite(ratio) and ratio<=GRID_RATIO_LIMIT)
            g9 &= ok
            two_grid.append({
                'scale_hinv_Mpc':float(scale),
                'C256':float(c256),'C512':float(c512),
                'symmetric_ratio':ratio,'limit':GRID_RATIO_LIMIT,'pass':ok,
            })
    else:
        g9=False

    gates={
        'B7_G1_frozen_provenance':bool(g1),
        'B7_G2_frozen_field_polynomial_representation':bool(g2),
        'B7_G3_exact_reduced_equation_implementation':bool(g3),
        'B7_G4_complete_scalar_shooting_construction':bool(g4),
        'B7_G5_center_launch_stability':bool(g5),
        'B7_G6_asymptotic_background_compatibility':bool(g6),
        'B7_G7_safety_exactQ_field_freeze':bool(g7),
        'B7_G8_original_B4_differential_exact_constraints':bool(g8),
        'B7_G9_two_grid_correction_control':bool(g9),
        'B7_G10_output_integrity_claim_boundary':True,
    }

    if not (g1 and g2 and g3):
        classification='NL1C7B7_REDUCED_RADIAL_IMPLEMENTATION_FAIL'
    elif not g4:
        classification='NL1C7B7_REDUCED_RADIAL_CONSTRUCTION_FAIL'
    elif not g5:
        classification='NL1C7B7_REDUCED_RADIAL_CENTER_CONTROL_FAIL'
    elif not g6:
        classification='NL1C7B7_REDUCED_RADIAL_ASYMPTOTIC_COMPATIBILITY_FAIL'
    elif not g7:
        classification='NL1C7B7_REDUCED_RADIAL_CONSTRUCTION_FAIL'
    elif not g8:
        classification='NL1C7B7_REDUCED_RADIAL_DIFFERENTIAL_CERTIFICATION_FAIL'
    elif not g9:
        classification='NL1C7B7_REDUCED_RADIAL_TWO_GRID_CONTROL_FAIL'
    else:
        classification='NL1C7B7_REDUCED_RADIAL_INITIAL_DATA_CERTIFIED'

    science_pass=bool(
        classification=='NL1C7B7_REDUCED_RADIAL_INITIAL_DATA_CERTIFIED'
    )
    state_path=Path(a.state_npz)
    if science_pass:
        write_npz(state_path,solved_states)
    elif state_path.exists():
        state_path.unlink()

    output={
        'written':bool(science_pass),
        'exists_after_run':bool(state_path.exists()),
        'pass':bool(state_path.exists()==science_pass),
    }
    gates['B7_G10_output_integrity_claim_boundary']=bool(output['pass'])

    result={
        'classification':classification,
        'scope':'NL1C7B7 direct shooting construction of the exact B6 first-order eta=0 radial constraint system for (L,R_t), independently certified by the unchanged B4 differential constraints.',
        'provenance':{
            **hashes,
            'b6_result_freeze_commit':B6_FREEZE_COMMIT,
            'b7_prereg_commit':B7_PREREG_COMMIT,
        },
        'settings':{
            'variables':['ell=log(L/a_i)','w=R_t/(a_i H_i R_s)'],
            'interpolation':'local degree-8 polynomial on frozen B4 nine-node stencil family',
            'primary_launch_fraction_r1':PRIMARY_LAUNCH,
            'control_launch_fraction_r1':CONTROL_LAUNCH,
            'ell0_bracket':list(ELL_BRACKET),
            'root_method':'brentq',
            'root_xtol':ROOT_XTOL,'root_rtol':ROOT_RTOL,
            'root_maxiter':ROOT_MAXITER,
            'ivp_method':'DOP853','ivp_rtol':IVP_RTOL,
            'ivp_atol':IVP_ATOL,'ivp_max_step':'dr',
            'center_L2_limit':CENTER_L2_LIMIT,
            'outer_Rt_relative_limit':OUTER_RT_LIMIT,
            'exact_constraint_limit':CONSTRAINT_LIMIT,
            'two_grid_ratio_limit':GRID_RATIO_LIMIT,
        },
        'rhs_audit':rhs_audit,
        'parent_reproduction':parent_repro,
        'polynomial_representation':poly_rows,
        'case_rows':case_rows,
        'two_grid_control':two_grid,
        'gates':gates,
        'output':output,
        'summary':{
            'case_count':6,
            'constructed_case_count':int(sum(bool(r['construction_pass']) for r in case_rows)),
            'center_pass_count':int(sum(bool(r.get('center_control_pass',r.get('center_control',{}).get('pass',False))) for r in case_rows)),
            'outer_pass_count':int(sum(bool(r.get('outer_Rt_compatibility_pass',r.get('outer_Rt_compatibility',{}).get('pass',False))) for r in case_rows)),
            'safe_case_count':int(sum(bool(r.get('safety_pass',False)) for r in case_rows)),
            'differential_pass_count':int(sum(bool(r.get('differential_constraint_pass',False)) for r in case_rows)),
            'max_exact_epsilon_H':max([r.get('max_epsilon_H') for r in case_rows if r.get('max_epsilon_H') is not None],default=None),
            'max_exact_epsilon_M':max([r.get('max_epsilon_M') for r in case_rows if r.get('max_epsilon_M') is not None],default=None),
        },
        'project_boundary':{
            'eta0_initial_data_certified':science_pass,
            'eta0_short_time_evolution_licensed':science_pass,
            'finite_eta_certified':False,
            'observational_claimed':False,
            'further_B7_solver_parameter_repairs_licensed':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(0 if science_pass else 2)


if __name__=='__main__':
    main()
