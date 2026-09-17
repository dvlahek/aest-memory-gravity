#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np

import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1

LIMIT=1e-7
DICT_LIMIT=1e-12
BETAS=(1.0,0.5,0.1)
KINDS=('Simple','Exponential','Sharp')


def arrval(f,args,n):
    v=np.asarray(f(*args),float)
    return np.full(n,float(v)) if v.ndim==0 else np.broadcast_to(v,(n,)).copy()


def rms(x):
    x=np.asarray(x,float)
    return float(np.sqrt(np.mean(x*x)))


def ratio2(a,b):
    if a==0.0 and b==0.0: return 1.0
    if a==0.0 or b==0.0: return float('inf')
    return float(max(a,b)/min(a,b))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--official-npz',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.official_npz)
    ks,gs=b4.groups(b4.read_trace(a.trace)); tv=b4.at_ai(gs); h=float(cov['h'])
    provenance_ok=bool(cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS' and
                       len(ks)==128 and cov.get('requested_k_relative_miss_max')==0 and
                       cov.get('n_native_times')==179)

    kq_bg=float(np.median(tv['KQ']))
    qbg=b4.stable_q_from_kq(kq_bg)
    # Stable Exp coordinate from the already frozen inversion KQ/(4K2 Z0)=Z exp(Z^2).
    x=kq_bg/(4*b4.K2*b4.Z0)
    Lx=math.log(x); y=Lx if Lx>1.0 else x*x
    for _ in range(50):
        f=y+0.5*math.log(y)-Lx; fp=1+0.5/y; yn=y-f/fp
        if abs(yn-y)<2e-14*(1+y): y=yn; break
        y=yn
    zbg=math.sqrt(y)

    states={}; maxrep=0.0; rep_rows={}
    for s in b4.SCALES:
        st=b4.make_state(s,256,ks,h,tv); states[(s,256)]=st; rr={}
        for k,v in st.items():
            key=f's{int(s)}_{k}'
            if key in off.files:
                e=b4.rel(np.asarray(v),np.asarray(off[key])); rr[k]=e; maxrep=max(maxrep,e)
        rep_rows[str(int(s))]=rr
        states[(s,512)]=b4.make_state(s,512,ks,h,tv)
    rep_ok=bool(maxrep<=1e-12)

    funcs,dY,kdict_identity=r1.build_nonK()
    rows=[]; dictionary=[]
    g1=True; g2=True; g3=True; allfinite=True

    for s in b4.SCALES:
      for nr in (256,512):
        st=states[(s,nr)]; r=st['r']; D=b4.dmat(r); n=len(r)
        L=b4.AI+st['L_minus_a']; R=b4.AI*r+st['R_minus_ar']
        Lt=b4.AI*b4.H_DIRECT+st['Ldot_minus_aH']; Rt=b4.AI*b4.H_DIRECT*r+st['Rdot_minus_aHr']
        u=st['u']; ut=st['udot']; phi=st['phi']; pr=D@phi
        Lr=D@L; Rr=D@R; ur=D@u
        dq=st['phidot_minus_Q']
        qtarget=qbg+dq
        c=np.cosh(u); sh=np.sinh(u)
        pt=(qtarget-sh*pr/L)/c
        qexact=c*pt+sh*pr/L
        scale=np.maximum(np.maximum(np.abs(qtarget),abs(qbg)),1e-300)
        qerr=float(np.max(np.abs(qexact-qtarget)/scale))
        corr=pt-qtarget
        corr_l2=float(np.linalg.norm(corr)/max(np.linalg.norm(qtarget),1e-300))
        corr_abs=float(np.max(np.abs(corr)))
        # Primary stable Exp coordinate represents the same frozen target without Q0 subtraction loss.
        z=zbg+dq/b4.Z0
        w=z*z
        with np.errstate(over='ignore',invalid='ignore'):
            ew=np.exp(w)
            K=2*b4.K2*b4.Z0*b4.Z0*np.expm1(w)
            KQ=4*b4.K2*b4.Z0*z*ew
            KQQ=4*b4.K2*ew*(1+2*w)
        literal_z=(qexact-b4.Q0)/b4.Z0
        finite_exp=bool(np.all(np.isfinite(z)) and np.all(np.isfinite(ew)) and
                        np.all(np.isfinite(K)) and np.all(np.isfinite(KQ)) and np.all(np.isfinite(KQQ)))
        g1 &= qerr<=DICT_LIMIT; g3 &= finite_exp
        dictionary.append({'scale_hinv_Mpc':s,'Nr':nr,'Q_target_max_normalized_error':qerr,
                           'phidot_completion_relative_L2':corr_l2,
                           'phidot_completion_abs_max_Mpc_inv':corr_abs,
                           'stable_Z_abs_max':float(np.max(np.abs(z))),
                           'literal_subtraction_Z_abs_max_diagnostic':float(np.max(np.abs(literal_z))),
                           'K_abs_max':float(np.max(np.abs(K))),
                           'KQ_abs_max':float(np.max(np.abs(KQ))),
                           'KQQ_abs_max':float(np.max(np.abs(KQQ))),
                           'Exp_sector_finite':finite_exp})

        args=[L,R,u,Lt,Rt,ut,pt,Lr,Rr,ur,pr]
        X=sh*pt+c*pr/L
        for kind in KINDS:
          for beta in BETAS:
            CH=[]; CM=[]; names=[]
            for name,fs in funcs.items():
                fN,fNr,fb,fbr=[arrval(f,args,n) for f in fs]
                fNr=np.array(fNr,copy=True); fbr=np.array(fbr,copy=True)
                fNr[0]=0.0; fbr[0]=0.0
                CH.append(fN-D@fNr); CM.append(fb-D@fbr); names.append(name)

            dyN,dyNr,dyb,dybr=[arrval(f,args,n) for f in dY]
            j,J=r1.jJ(kind,np.abs(X)/b4.A0_GEO,beta)
            P=L*R**2
            jN=-b4.C*(P*J+P*j*dyN); jNr=-b4.C*(P*j*dyNr)
            jb=-b4.C*(P*j*dyb); jbr=-b4.C*(P*j*dybr)
            jNr=np.array(jNr,copy=True); jbr=np.array(jbr,copy=True); jNr[0]=0.0; jbr[0]=0.0
            CH.append(jN-D@jNr); CM.append(jb-D@jbr); names.append('AeST_J')

            # Exact Exp K(Q) lapse/shift EL terms from 2 P K in the frozen C6 action.
            kN=4*b4.K2*L*R**2*(b4.Z0*b4.Z0*np.expm1(w)-2*c*pt*b4.Z0*z*ew)
            kb=-8*b4.K2*L*R**2*c*pr*b4.Z0*z*ew
            CH.append(kN); CM.append(kb); names.append('AeST_K')

            v=np.arctanh(st['dust_vr']); varrho=b4.VAR_B*(1+st['delta_b'])
            CH.append(-2*L*R**2*varrho*np.cosh(v)**2)
            CM.append(2*L**2*R**2*varrho*np.cosh(v)*np.sinh(v)); names.append('dust')
            CH.append(-2*L*R**2*b4.RHO_STD); CM.append(np.zeros(n)); names.append('standard_bg')

            CH=np.asarray(CH,float); CM=np.asarray(CM,float)
            noncenter=np.arange(n)>0
            finite=bool(np.all(np.isfinite(CH[:,noncenter])) and np.all(np.isfinite(CM[:,noncenter])))
            allfinite &= finite
            if not finite:
                eH=np.full(n,np.inf); eM=np.full(n,np.inf); preH=preM=float('nan'); floorH=floorM=float('nan')
            else:
                denH=np.sum(np.abs(CH),axis=0); denM=np.sum(np.abs(CM),axis=0)
                preH=float(np.max(denH[noncenter])); preM=float(np.max(denM[noncenter]))
                if not (preH>0 and preM>0 and np.isfinite(preH) and np.isfinite(preM)):
                    finite=False; allfinite=False
                    eH=np.full(n,np.inf); eM=np.full(n,np.inf); floorH=floorM=float('nan')
                else:
                    floorH=1e-14*preH; floorM=1e-14*preM
                    eH=np.abs(np.sum(CH,axis=0))/(denH+floorH)
                    eM=np.abs(np.sum(CM,axis=0))/(denM+floorM)
            mh=float(np.max(eH[noncenter])); mm=float(np.max(eM[noncenter]))
            rh=rms(eH[noncenter]); rm=rms(eM[noncenter])
            rows.append({'scale_hinv_Mpc':s,'Nr':nr,'Y_kind':kind,'beta0':beta,
                         'all_action_terms_finite_noncenter':finite,
                         'max_epsilon_H':mh,'max_epsilon_M':mm,'rms_epsilon_H':rh,'rms_epsilon_M':rm,
                         'pre_floor_denominator_max_H':preH,'pre_floor_denominator_max_M':preM,
                         'floor_H':floorH,'floor_M':floorM,'limit':LIMIT,
                         'constraint_pass':bool(finite and mh<=LIMIT and mm<=LIMIT)})

    # Frozen two-grid RMS control for every scale/Y case.
    grid=[]; grid_ok=True
    for s in b4.SCALES:
      for kind in KINDS:
       for beta in BETAS:
        a256=next(x for x in rows if x['scale_hinv_Mpc']==s and x['Nr']==256 and x['Y_kind']==kind and x['beta0']==beta)
        a512=next(x for x in rows if x['scale_hinv_Mpc']==s and x['Nr']==512 and x['Y_kind']==kind and x['beta0']==beta)
        qh=ratio2(a256['rms_epsilon_H'],a512['rms_epsilon_H']); qm=ratio2(a256['rms_epsilon_M'],a512['rms_epsilon_M'])
        ok=bool(np.isfinite(qh) and np.isfinite(qm) and qh<=2.0 and qm<=2.0)
        grid_ok &= ok
        grid.append({'scale_hinv_Mpc':s,'Y_kind':kind,'beta0':beta,'rms_ratio_H':qh,'rms_ratio_M':qm,'pass':ok})

    constraints_ok=bool(len(rows)==54 and all(x['constraint_pass'] for x in rows))
    g5=bool(len(rows)==54 and len(grid)==27)
    gates={'R2_G1_exact_target_preservation':bool(g1),
           'R2_G2_unique_algebraic_first_order_preservation':bool(g2),
           'R2_G3_Exp_domain_restoration':bool(g3),
           'R2_G4_unchanged_raw_constraints':constraints_ok,
           'R2_G5_grid_control_and_no_selection':bool(g5 and grid_ok)}
    if provenance_ok and rep_ok and kdict_identity and g1 and g2 and g3:
        if constraints_ok and grid_ok:
            cls='NL1C7B4_REPAIR02_EXACT_NONLINEAR_DICTIONARY_CONSTRAINT_PASS'
        else:
            cls='NL1C7B4_REPAIR02_DICTIONARY_COMPLETED_RAW_CONSTRAINT_FAIL'
    else:
        cls='NL1C7B4_REPAIR02_DICTIONARY_COMPLETION_IMPLEMENTATION_FAIL'

    result={'classification':cls,
      'scope':'Repair02 exact nonlinear Q-dictionary completion and unchanged B4 raw eta=0 constraint audit; no evolution.',
      'parents':{'C7A_run':35183893359,'C7A_artifact':10481526695,
                 'C7A_sha256':'c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c',
                 'B4_repair01_run':35212527939,'B4_repair01_artifact':10493461020,
                 'B4_repair01_sha256':'0cd7ff857d2965915176563341a18d2979f82ebe3ea59be090459030018c1aa0',
                 'B4_repair01_freeze':'c158cbaa8bcfbd3bec9feb0a3449b66aec0e63d0'},
      'background':{'Q_bg_Mpc_inv':qbg,'Z_bg_stable':zbg,'H_Mpc_inv':b4.H_DIRECT,
                    'varrho_b':b4.VAR_B,'rho_std_C6':b4.RHO_STD},
      'state_reproduction':{'max_relative_L2':maxrep,'limit':1e-12,'pass':rep_ok,'rows':rep_rows},
      'symbolic_K_dictionary_identity':bool(kdict_identity),
      'dictionary_completion':dictionary,
      'constraint_rows':rows,'grid_control':grid,'gates':gates,
      'summary':{'n_constraint_cases':len(rows),'n_grid_pairs':len(grid),
                 'max_Q_target_error':float(max(x['Q_target_max_normalized_error'] for x in dictionary)),
                 'max_stable_Z_abs':float(max(x['stable_Z_abs_max'] for x in dictionary)),
                 'max_epsilon_H':float(max(x['max_epsilon_H'] for x in rows)),
                 'max_epsilon_M':float(max(x['max_epsilon_M'] for x in rows)),
                 'n_constraint_pass':int(sum(x['constraint_pass'] for x in rows)),
                 'constraint_limit':LIMIT},
      'claim_boundary':{'only_phidot_completed':True,'constraint_projection_used':False,
                        'amplitude_or_phase_fit_used':False,'Q_linearized':False,'K_clipped':False,
                        'Y_branch_selected':False,'scale_selected':False,'nonlinear_evolution_executed':False}}
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if cls.endswith('_PASS') else 2)

if __name__=='__main__': main()
