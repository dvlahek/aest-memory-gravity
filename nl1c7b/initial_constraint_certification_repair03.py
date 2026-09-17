#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np

import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1

LAMBDAS=(1.0,0.5,0.25)
BETAS=(1.0,0.5,0.1)
KINDS=('Simple','Exponential','Sharp')
DECOMP_LIMIT=1e-12


def arrval(f,args,n):
    v=np.asarray(f(*args),float)
    return np.full(n,float(v)) if v.ndim==0 else np.broadcast_to(v,(n,)).copy()


def rms(x):
    x=np.asarray(x,float)
    return float(np.sqrt(np.mean(x*x)))


def slope(y1,y2):
    if not (np.isfinite(y1) and np.isfinite(y2) and y1>0 and y2>0):
        return None
    return float(math.log(y1/y2,2.0))


def stable_zbg(kq_bg):
    x=kq_bg/(4*b4.K2*b4.Z0)
    lx=math.log(x)
    y=lx if lx>1.0 else x*x
    for _ in range(60):
        f=y+0.5*math.log(y)-lx
        fp=1.0+0.5/y
        yn=y-f/fp
        if abs(yn-y)<2e-14*(1.0+y):
            y=yn; break
        y=yn
    return math.sqrt(y)


def grouped(d):
    z=np.zeros_like(next(iter(d.values())))
    out={
      'GR':z.copy(),
      'AeST_nonK_nonJ':z.copy(),
      'AeST_J':d['AeST_J'].copy(),
      'AeST_K':d['AeST_K'].copy(),
      'dust':d['dust'].copy(),
      'standard_bg':d['standard_bg'].copy(),
    }
    for k,v in d.items():
        if k.startswith('GR_'): out['GR'] += v
        elif k in ('AeST_E2','AeST_EX','AeST_X2'): out['AeST_nonK_nonJ'] += v
    return out


def term_stats(g,total,idx,mask):
    norms={k:float(np.linalg.norm(v[mask])) for k,v in g.items()}
    sn=max(sum(norms.values()),1e-300)
    tn=float(np.dot(total[mask],total[mask]))
    abs_at={k:abs(float(v[idx])) for k,v in g.items()}
    sa=max(sum(abs_at.values()),1e-300)
    out={}
    for k,v in g.items():
        out[k]={
          'max_abs':float(np.max(np.abs(v[mask]))),
          'relative_L2_magnitude':float(norms[k]/sn),
          'signed_projection_on_total':None if tn==0 else float(np.dot(v[mask],total[mask])/tn),
          'value_at_max_residual_radius':float(v[idx]),
          'fractional_abs_at_max_residual_radius':float(abs_at[k]/sa),
        }
    return out


def eval_case(st,s,nr,kind,beta,lam,qbg,zbg,funcs,dY):
    r=st['r']; D=b4.dmat(r); n=len(r); mask=np.arange(n)>0
    L=b4.AI+lam*st['L_minus_a']
    R=b4.AI*r+lam*st['R_minus_ar']
    Lt=b4.AI*b4.H_DIRECT+lam*st['Ldot_minus_aH']
    Rt=b4.AI*b4.H_DIRECT*r+lam*st['Rdot_minus_aHr']
    u=lam*st['u']; ut=lam*st['udot']; phi=lam*st['phi']
    dq=lam*st['phidot_minus_Q']; delta_b=lam*st['delta_b']; dust_vr=lam*st['dust_vr']
    pr=D@phi; Lr=D@L; Rr=D@R; ur=D@u
    c=np.cosh(u); sh=np.sinh(u)
    qtarget=qbg+dq
    pt=(qtarget-sh*pr/L)/c
    qexact=c*pt+sh*pr/L
    z=zbg+dq/b4.Z0; w=z*z; ew=np.exp(w)
    args=[L,R,u,Lt,Rt,ut,pt,Lr,Rr,ur,pr]
    X=sh*pt+c*pr/L

    H={}; M={}
    for name,fs in funcs.items():
        fN,fNr,fb,fbr=[arrval(f,args,n) for f in fs]
        fNr=np.array(fNr,copy=True); fbr=np.array(fbr,copy=True)
        fNr[0]=0.0; fbr[0]=0.0
        H[name]=fN-D@fNr; M[name]=fb-D@fbr

    dyN,dyNr,dyb,dybr=[arrval(f,args,n) for f in dY]
    j,J=r1.jJ(kind,np.abs(X)/b4.A0_GEO,beta)
    P=L*R**2
    jN=-b4.C*(P*J+P*j*dyN); jNr=-b4.C*(P*j*dyNr)
    jb=-b4.C*(P*j*dyb); jbr=-b4.C*(P*j*dybr)
    jNr=np.array(jNr,copy=True); jbr=np.array(jbr,copy=True); jNr[0]=0.0; jbr[0]=0.0
    H['AeST_J']=jN-D@jNr; M['AeST_J']=jb-D@jbr

    H['AeST_K']=4*b4.K2*L*R**2*(b4.Z0*b4.Z0*np.expm1(w)-2*c*pt*b4.Z0*z*ew)
    M['AeST_K']=-8*b4.K2*L*R**2*c*pr*b4.Z0*z*ew

    v=np.arctanh(dust_vr); varrho=b4.VAR_B*(1.0+delta_b)
    H['dust']=-2*L*R**2*varrho*np.cosh(v)**2
    M['dust']=2*L**2*R**2*varrho*np.cosh(v)*np.sinh(v)
    H['standard_bg']=-2*L*R**2*b4.RHO_STD
    M['standard_bg']=np.zeros(n)

    names=list(H)
    HA=np.asarray([H[k] for k in names],float); MA=np.asarray([M[k] for k in names],float)
    finite=bool(np.all(np.isfinite(HA[:,mask])) and np.all(np.isfinite(MA[:,mask])))
    totalH=np.sum(HA,axis=0); totalM=np.sum(MA,axis=0)
    denH=np.sum(np.abs(HA),axis=0); denM=np.sum(np.abs(MA),axis=0)
    preH=float(np.max(denH[mask])); preM=float(np.max(denM[mask]))
    floorH=1e-14*preH; floorM=1e-14*preM
    epsH=np.abs(totalH)/(denH+floorH); epsM=np.abs(totalM)/(denM+floorM)
    idxH=int(np.arange(n)[mask][np.argmax(epsH[mask])]); idxM=int(np.arange(n)[mask][np.argmax(epsM[mask])])

    gH=grouped(H); gM=grouped(M)
    closeH=np.sum(np.asarray(list(gH.values())),axis=0)-totalH
    closeM=np.sum(np.asarray(list(gM.values())),axis=0)-totalM
    deH=float(np.linalg.norm(closeH[mask])/max(np.linalg.norm(totalH[mask]),1e-300))
    deM=float(np.linalg.norm(closeM[mask])/max(np.linalg.norm(totalM[mask]),1e-300))

    base={
      'scale_hinv_Mpc':s,'Nr':nr,'Y_kind':kind,'beta0':beta,'lambda':lam,
      'finite':finite,
      'max_epsilon_H':float(np.max(epsH[mask])),'max_epsilon_M':float(np.max(epsM[mask])),
      'rms_epsilon_H':rms(epsH[mask]),'rms_epsilon_M':rms(epsM[mask]),
      'Q_target_max_normalized_error':float(np.max(np.abs(qexact-qtarget)/np.maximum(np.maximum(np.abs(qtarget),abs(qbg)),1e-300))),
      'max_residual_H':{'index':idxH,'r_Mpc':float(r[idxH]),'x':float(r[idxH]/(s/b4.H_SMALL_H))},
      'max_residual_M':{'index':idxM,'r_Mpc':float(r[idxM]),'x':float(r[idxM]/(s/b4.H_SMALL_H))},
    }
    if lam==1.0:
        base['decomposition_closure_relative_L2_H']=deH
        base['decomposition_closure_relative_L2_M']=deM
        base['terms_H']=term_stats(gH,totalH,idxH,mask)
        base['terms_M']=term_stats(gM,totalM,idxM,mask)
    return base


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--official-npz',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    cov=json.loads(Path(a.coverage_json).read_text()); off=np.load(a.official_npz)
    ks,gs=b4.groups(b4.read_trace(a.trace)); tv=b4.at_ai(gs); h=float(cov['h'])
    provenance_ok=bool(cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS' and len(ks)==128 and cov.get('n_native_times')==179)
    kq_bg=float(np.median(tv['KQ'])); qbg=b4.stable_q_from_kq(kq_bg); zbg=stable_zbg(kq_bg)
    funcs,dY,kdict=r1.build_nonK()

    states={}; maxrep=0.0
    for s in b4.SCALES:
        st=b4.make_state(s,256,ks,h,tv); states[(s,256)]=st
        for k,v in st.items():
            key=f's{int(s)}_{k}'
            if key in off.files: maxrep=max(maxrep,b4.rel(np.asarray(v),np.asarray(off[key])))
        states[(s,512)]=b4.make_state(s,512,ks,h,tv)
    rep_ok=bool(maxrep<=1e-12)

    rows=[]
    for lam in LAMBDAS:
      for s in b4.SCALES:
       for nr in (256,512):
        for kind in KINDS:
         for beta in BETAS:
          rows.append(eval_case(states[(s,nr)],s,nr,kind,beta,lam,qbg,zbg,funcs,dY))

    baseline=[x for x in rows if x['lambda']==1.0]
    decomp=max(max(x['decomposition_closure_relative_L2_H'],x['decomposition_closure_relative_L2_M']) for x in baseline)
    allfinite=all(x['finite'] for x in rows)
    target_ok=max(x['Q_target_max_normalized_error'] for x in rows)<=1e-12

    scaling=[]
    for s in b4.SCALES:
      for nr in (256,512):
       for kind in KINDS:
        for beta in BETAS:
         q=sorted([x for x in rows if x['scale_hinv_Mpc']==s and x['Nr']==nr and x['Y_kind']==kind and x['beta0']==beta],key=lambda z:-z['lambda'])
         scaling.append({'scale_hinv_Mpc':s,'Nr':nr,'Y_kind':kind,'beta0':beta,
           'H_max_slopes':[slope(q[0]['max_epsilon_H'],q[1]['max_epsilon_H']),slope(q[1]['max_epsilon_H'],q[2]['max_epsilon_H'])],
           'M_max_slopes':[slope(q[0]['max_epsilon_M'],q[1]['max_epsilon_M']),slope(q[1]['max_epsilon_M'],q[2]['max_epsilon_M'])],
           'H_rms_slopes':[slope(q[0]['rms_epsilon_H'],q[1]['rms_epsilon_H']),slope(q[1]['rms_epsilon_H'],q[2]['rms_epsilon_H'])],
           'M_rms_slopes':[slope(q[0]['rms_epsilon_M'],q[1]['rms_epsilon_M']),slope(q[1]['rms_epsilon_M'],q[2]['rms_epsilon_M'])]})

    complete=bool(provenance_ok and rep_ok and kdict and allfinite and target_ok and decomp<=DECOMP_LIMIT and len(rows)==162 and len(baseline)==54 and len(scaling)==54)
    cls='NL1C7B4_REPAIR03_CONSTRAINT_SOURCE_LOCALIZATION_COMPLETE' if complete else 'NL1C7B4_REPAIR03_LOCALIZATION_IMPLEMENTATION_FAIL'
    result={
      'classification':cls,
      'scope':'Diagnostic source localization of the Repair02-completed eta=0 constraints only; no state projection and no evolution.',
      'parent':{'run':35216284867,'artifact':10495377062,'artifact_sha256':'f74795d3c57ba6f307655b1ec15513b57babc7eadbe0c81c4f62bf1949643d49','freeze_commit':'9c1f5c6a17467467bcf82e134f21793a3f63d0d4'},
      'state_reproduction':{'max_relative_L2':maxrep,'limit':1e-12,'pass':rep_ok},
      'symbolic_K_dictionary_identity':bool(kdict),
      'settings':{'lambdas':list(LAMBDAS),'scales_hinv_Mpc':list(b4.SCALES),'grids':[256,512],'Y_kinds':list(KINDS),'betas':list(BETAS),'decomposition_limit':DECOMP_LIMIT},
      'summary':{'n_rows':len(rows),'n_baseline_cases':len(baseline),'n_scaling_cases':len(scaling),'all_finite':allfinite,'max_decomposition_closure_relative_L2':decomp,'Q_target_preserved_all_amplitudes':target_ok},
      'baseline_decomposition':baseline,'amplitude_scaling':scaling,
      'claim_boundary':{'state_projected':False,'dust_sign_changed':False,'radial_standard_species_added':False,'source_fit_used':False,'nonlinear_evolution_executed':False}}
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True)); raise SystemExit(0 if complete else 2)

if __name__=='__main__': main()
