#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
import sympy as sp

import nl1c7b.initial_constraint_certification as b4

BETAS=(1.0,0.5,0.1)
KINDS=('Simple','Exponential','Sharp')
LIMIT=1e-7


def jJ(kind,x,beta):
    x=np.asarray(x,float); A=1.0+beta
    if kind=='Simple':
        j=x/(A+beta*x)
        J=2*b4.A0_GEO*b4.A0_GEO*(x*x/(2*beta)-A*x/(beta*beta)+(A*A/beta**3)*np.log((A+beta*x)/A))
        return j,J
    if kind=='Exponential':
        c=beta/A
        j=(1/beta)*(1-np.exp(-c*x))
        J=(2*b4.A0_GEO*b4.A0_GEO/beta)*(x*x/2-(1-(1+c*x)*np.exp(-c*x))/(c*c))
        return j,J
    xt=A/beta
    j=np.where(x<=xt,x/A,1/beta)
    J=np.where(x<=xt,2*b4.A0_GEO*b4.A0_GEO*x**3/(3*A),
               b4.A0_GEO*b4.A0_GEO*x*x/beta-b4.A0_GEO*b4.A0_GEO*A*A/(3*beta**3))
    return j,J


def build_nonK():
    N,L,R,b,u,Lt,Rt,ut,pt,Nr,Lr,Rr,br,ur,pr=sp.symbols(
        'N L R b u Lt Rt ut pt Nr Lr Rr br ur pr', real=True)
    c=sp.cosh(u); s=sp.sinh(u)
    kL=(Lt-b*Lr-L*br)/(N*L)
    kR=(Rt-b*Rr)/(N*R)
    sigma=(pt-b*pr)/N
    Q=c*sigma+s*pr/L
    X=s*sigma+c*pr/L
    Y=X**2
    E=c*((ut-b*ur)/N+Nr/(N*L))+s*(kL+ur/L)
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
    gauge={N:1,b:0,Nr:0,br:0}
    args=[L,R,u,Lt,Rt,ut,pt,Lr,Rr,ur,pr]
    funcs={}
    for name,t in terms.items():
        funcs[name]=[sp.lambdify(args,sp.diff(t,z).subs(gauge),'numpy') for z in (N,Nr,b,br)]
    dY=[sp.lambdify(args,sp.diff(Y,z).subs(gauge),'numpy') for z in (N,Nr,b,br)]
    qN=sp.simplify(sp.diff(Q,N).subs(gauge)+c*pt)
    qb=sp.simplify(sp.diff(Q,b).subs(gauge)+c*pr)
    exact=bool(qN==0 and qb==0 and sp.diff(Q,Nr)==0 and sp.diff(Q,br)==0)
    return funcs,dY,exact


def arrval(f,args,n):
    v=np.asarray(f(*args),float)
    return np.full(n,float(v)) if v.ndim==0 else np.broadcast_to(v,(n,)).copy()


def lower_bound(logA,B):
    out=np.zeros_like(B,float)
    gap=np.full_like(B,-np.inf,float)
    ok=np.isfinite(logA)
    pos=B>0
    idx=ok & pos
    gap[idx]=logA[idx]-np.log(B[idx])
    huge=idx & (gap>50)
    out[huge]=1.0-2.0*np.exp(-gap[huge])
    mid=idx & ~huge
    ratio=np.exp(-gap[mid])
    out[mid]=np.where(ratio<1,(1-ratio)/(1+ratio),0.0)
    out[ok & ~pos]=1.0
    return out,gap


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--official-npz',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.official_npz)
    ks,gs=b4.groups(b4.read_trace(a.trace))
    tv=b4.at_ai(gs)
    h=float(cov['h'])
    qbg=b4.stable_q_from_kq(float(np.median(tv['KQ'])))
    funcs,dY,identity=build_nonK()

    states={}
    maxrep=0.0
    for s in b4.SCALES:
        st=b4.make_state(s,256,ks,h,tv)
        states[(s,256)]=st
        for k,v in st.items():
            key=f's{int(s)}_{k}'
            if key in off.files:
                maxrep=max(maxrep,b4.rel(np.asarray(v),np.asarray(off[key])))
        states[(s,512)]=b4.make_state(s,512,ks,h,tv)

    rows=[]
    allfinite=True
    any_fail=False
    for s in b4.SCALES:
      for nr in (256,512):
        st=states[(s,nr)]
        r=st['r']; D=b4.dmat(r); n=len(r)
        L=b4.AI+st['L_minus_a']
        R=b4.AI*r+st['R_minus_ar']
        Lt=b4.AI*b4.H_DIRECT+st['Ldot_minus_aH']
        Rt=b4.AI*b4.H_DIRECT*r+st['Rdot_minus_aHr']
        u=st['u']; ut=st['udot']; pt=qbg+st['phidot_minus_Q']
        Lr=D@L; Rr=D@R; ur=D@u; pr=D@st['phi']
        args=[L,R,u,Lt,Rt,ut,pt,Lr,Rr,ur,pr]
        c=np.cosh(u)
        Q=c*pt+np.sinh(u)*pr/L
        X=np.sinh(u)*pt+c*pr/L
        z=(Q-b4.Q0)/b4.Z0
        w=z*z

        expneg=np.where(w<745,np.exp(-w),0.0)
        bracketH=b4.Z0*b4.Z0*(1-expneg)-2*c*pt*b4.Z0*z
        with np.errstate(divide='ignore',invalid='ignore'):
            logAH=np.log(4*b4.K2)+np.log(np.abs(L))+2*np.log(np.abs(R))+w+np.log(np.abs(bracketH))
            logAM=np.log(8*b4.K2*b4.Z0)+np.log(np.abs(L))+2*np.log(np.abs(R))+np.log(c)+np.log(np.abs(pr))+np.log(np.abs(z))+w

        for kind in KINDS:
          for beta in BETAS:
            CH=[]; CM=[]
            for _,fs in funcs.items():
                fN,fNr,fb,fbr=[arrval(f,args,n) for f in fs]
                # The analytic center is not used by the proof.  Set only the center
                # flux placeholder before matrix multiplication; proof points begin at i=5,
                # whose 9-point stencils contain no center value.
                fNr2=np.array(fNr,copy=True); fbr2=np.array(fbr,copy=True)
                fNr2[0]=0.0; fbr2[0]=0.0
                CH.append(fN-D@fNr2); CM.append(fb-D@fbr2)

            dyN,dyNr,dyb,dybr=[arrval(f,args,n) for f in dY]
            j,J=jJ(kind,np.abs(X)/b4.A0_GEO,beta)
            P=L*R**2
            jN=-b4.C*(P*J+P*j*dyN)
            jNr=-b4.C*(P*j*dyNr)
            jb=-b4.C*(P*j*dyb)
            jbr=-b4.C*(P*j*dybr)
            jNr2=np.array(jNr,copy=True); jbr2=np.array(jbr,copy=True)
            jNr2[0]=0.0; jbr2[0]=0.0
            CH.append(jN-D@jNr2); CM.append(jb-D@jbr2)

            v=np.arctanh(st['dust_vr'])
            varrho=b4.VAR_B*(1+st['delta_b'])
            CH.append(-2*L*R**2*varrho*np.cosh(v)**2)
            CM.append(2*L**2*R**2*varrho*np.cosh(v)*np.sinh(v))
            CH.append(-2*L*R**2*b4.RHO_STD)
            CM.append(np.zeros(n))

            CH=np.asarray(CH); CM=np.asarray(CM)
            # A failing point on this strict non-center subset proves failure of the
            # full original max over all r>0.  No point is excluded for a PASS claim.
            mask=np.arange(n)>=5
            finite=bool(np.all(np.isfinite(CH[:,mask])) and np.all(np.isfinite(CM[:,mask])))
            allfinite &= finite
            BH=np.sum(np.abs(CH),axis=0); BM=np.sum(np.abs(CM),axis=0)
            lbH,gH=lower_bound(logAH,BH); lbM,gM=lower_bound(logAM,BM)
            mh=float(np.max(lbH[mask])); mm=float(np.max(lbM[mask]))
            this_fail=bool(mh>LIMIT or mm>LIMIT)
            any_fail |= this_fail
            rows.append({'scale_hinv_Mpc':s,'Nr':nr,'Y_kind':kind,'beta0':beta,
                         'proof_subset_first_noncenter_index':5,
                         'subset_failure_implies_full_max_failure':True,
                         'nonK_finite_on_proof_subset':finite,
                         'max_H_lower_bound':mh,'max_M_lower_bound':mm,
                         'max_logA_minus_logB_H':float(np.nanmax(gH[mask])),
                         'max_logA_minus_logB_M':float(np.nanmax(gM[mask])),
                         'limit':LIMIT,'raw_constraint_pass':not this_fail})

    repok=bool(maxrep<=1e-12)
    provenance_ok=bool(cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS' and len(ks)==128)
    if identity and repok and provenance_ok and allfinite and any_fail:
        cls='NL1C7B4_REPAIR01_RAW_INITIAL_CONSTRAINT_FAIL'
    else:
        cls='NL1C7B4_REPAIR01_LOG_DOMAIN_IMPLEMENTATION_FAIL'

    result={'classification':cls,
      'scope':'Repair01 log-domain evaluation of the exact frozen Exp Q-sector for the raw eta=0 initial constraints; no state modification or evolution.',
      'historical_parent':{'run':35211367954,'artifact':10492575332,
        'artifact_sha256':'9fdf56fd2c2b224c934cc15be31d5d27076971b50ab2961849c151939d60ef74',
        'freeze_commit':'d42e22945e2ca6acaf412741198e4b8c6659598a'},
      'symbolic_K_dictionary_identity':identity,
      'state_reproduction':{'max_relative_L2':maxrep,'limit':1e-12,'pass':repok},
      'all_nonK_terms_finite_on_proof_subsets':allfinite,
      'all_54_cases_fail':bool(len(rows)==54 and all(not r['raw_constraint_pass'] for r in rows)),
      'summary':{'n_cases':len(rows),
        'min_over_cases_max_H_lower_bound':float(min(r['max_H_lower_bound'] for r in rows)),
        'min_over_cases_max_M_lower_bound':float(min(r['max_M_lower_bound'] for r in rows)),
        'min_over_cases_log_gap_H':float(min(r['max_logA_minus_logB_H'] for r in rows)),
        'min_over_cases_log_gap_M':float(min(r['max_logA_minus_logB_M'] for r in rows)),
        'constraint_limit':LIMIT},
      'rows':rows,
      'claim_boundary':{'state_modified':False,'Q_linearized':False,'K_clipped':False,
                        'Y_branch_selected':False,'scale_selected':False,
                        'nonlinear_evolution_executed':False,'finite_eta_executed':False}}
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True)); raise SystemExit(2)

if __name__=='__main__': main()
