#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np

import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair03 as r3

EPS=(0.04,0.02,0.01)
KINDS=('Simple','Exponential','Sharp')
BETAS=(1.0,0.5,0.1)
CONV_LIMIT=5e-4
ACTIVE_FRAC=1e-12
PASS_LIMIT=1e-5
MISMATCH_FLOOR=0.1


def l2(x):
    return float(np.linalg.norm(np.asarray(x,float)))


def rel_l2(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-300))


def stable_zbg(kq_bg):
    x=float(kq_bg)/(4*b4.K2*b4.Z0)
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


def scaled_fields(st,lam,qbg,D):
    r=st['r']
    L=b4.AI+lam*st['L_minus_a']
    R=b4.AI*r+lam*st['R_minus_ar']
    Lt=b4.AI*b4.H_DIRECT+lam*st['Ldot_minus_aH']
    Rt=b4.AI*b4.H_DIRECT*r+lam*st['Rdot_minus_aHr']
    u=lam*st['u']; ut=lam*st['udot']; phi=lam*st['phi']
    dq=lam*st['phidot_minus_Q']
    delta_b=lam*st['delta_b']; dust_vr=lam*st['dust_vr']
    pr=D@phi; Lr=D@L; Rr=D@R; ur=D@u
    c=np.cosh(u); sh=np.sinh(u)
    qtarget=qbg+dq
    pt=(qtarget-sh*pr/L)/c
    return {
      'L':L,'R':R,'Lt':Lt,'Rt':Rt,'u':u,'ut':ut,'phi':phi,
      'dq':dq,'delta_b':delta_b,'dust_vr':dust_vr,'pr':pr,
      'Lr':Lr,'Rr':Rr,'ur':ur,'c':c,'sh':sh,'pt':pt,'qtarget':qtarget,
    }


def momentum_terms(st,lam,kind,beta,qbg,zbg,funcs,dY,D):
    f=scaled_fields(st,lam,qbg,D); n=len(st['r'])
    args=[f['L'],f['R'],f['u'],f['Lt'],f['Rt'],f['ut'],f['pt'],
          f['Lr'],f['Rr'],f['ur'],f['pr']]
    out={}
    for name,fs in funcs.items():
        _,_,fb,fbr=[r3.arrval(g,args,n) for g in fs]
        fbr=np.array(fbr,copy=True); fbr[0]=0.0
        out[name]=fb-D@fbr

    _,_,dyb,dybr=[r3.arrval(g,args,n) for g in dY]
    X=f['sh']*f['pt']+f['c']*f['pr']/f['L']
    j,_=r1.jJ(kind,np.abs(X)/b4.A0_GEO,beta)
    P=f['L']*f['R']**2
    jb=-b4.C*(P*j*dyb)
    jbr=-b4.C*(P*j*dybr)
    jbr=np.array(jbr,copy=True); jbr[0]=0.0
    out['AeST_J']=jb-D@jbr

    z=zbg+f['dq']/b4.Z0
    ew=np.exp(z*z)
    out['AeST_K']=-8*b4.K2*f['L']*f['R']**2*f['c']*f['pr']*b4.Z0*z*ew

    v=np.arctanh(f['dust_vr'])
    varrho=b4.VAR_B*(1.0+f['delta_b'])
    out['dust']=2*f['L']**2*f['R']**2*varrho*np.cosh(v)*np.sinh(v)
    out['standard_bg']=np.zeros(n)
    return out


def frame_ex(st,lam,qbg,D):
    f=scaled_fields(st,lam,qbg,D)
    kL=f['Lt']/f['L']
    E=f['c']*f['ut']+f['sh']*(kL+f['ur']/f['L'])
    X=f['sh']*f['pt']+f['c']*f['pr']/f['L']
    return E,X


def central_dict(st,h,kind,beta,qbg,zbg,funcs,dY,D):
    p=momentum_terms(st,+h,kind,beta,qbg,zbg,funcs,dY,D)
    m=momentum_terms(st,-h,kind,beta,qbg,zbg,funcs,dY,D)
    return {k:(p[k]-m[k])/(2*h) for k in p}


def grouped(d):
    z=np.zeros_like(next(iter(d.values())))
    g={'GR':z.copy(),'AeST_nonK_nonJ':z.copy(),'AeST_J':d['AeST_J'].copy(),
       'AeST_K':d['AeST_K'].copy(),'dust':d['dust'].copy(),'standard_bg':d['standard_bg'].copy()}
    for k,v in d.items():
        if k.startswith('GR_'): g['GR'] += v
        elif k in ('AeST_E2','AeST_EX','AeST_X2'): g['AeST_nonK_nonJ'] += v
    return g


def case_audit(st,s,nr,kind,beta,qbg,zbg,funcs,dY):
    r=st['r']; D=b4.dmat(r); mask=np.arange(len(r))>0
    tangents={h:central_dict(st,h,kind,beta,qbg,zbg,funcs,dY,D) for h in EPS}
    fine=tangents[0.01]; mid=tangents[0.02]
    names=list(fine)
    fine_sum_norm=sum(l2(fine[k][mask]) for k in names)
    active={k:bool(l2(fine[k][mask])>=ACTIVE_FRAC*max(fine_sum_norm,1e-300)) for k in names}
    conv={k:rel_l2(mid[k][mask],fine[k][mask]) for k in names}
    term_gate=all((not active[k]) or conv[k]<=CONV_LIMIT for k in names)
    total={h:np.sum(np.asarray(list(tangents[h].values())),axis=0) for h in EPS}
    conv_total=rel_l2(total[0.02][mask],total[0.01][mask])
    conv_ok=bool(term_gate and conv_total<=CONV_LIMIT)

    den=np.sum(np.abs(np.asarray(list(fine.values()))),axis=0)
    floor=1e-14*float(np.max(den[mask]))
    eps=np.abs(total[0.01])/(den+floor)
    idx=int(np.arange(len(r))[mask][np.argmax(eps[mask])])
    g=grouped(fine)
    grouped_at={k:float(v[idx]) for k,v in g.items()}
    dominant=max(grouped_at,key=lambda k:abs(grouped_at[k]))

    raw={}
    for k in names:
        raw[k]={str(h):{'max_abs':float(np.max(np.abs(tangents[h][k][mask]))),
                        'L2':l2(tangents[h][k][mask])} for h in EPS}
        raw[k]['active_for_convergence_gate']=active[k]
        raw[k]['fine_vs_mid_relative_L2']=conv[k]

    return {
      'scale_hinv_Mpc':s,'Nr':nr,'Y_kind':kind,'beta0':beta,
      'tangent_convergence_pass':conv_ok,
      'total_fine_vs_mid_relative_L2':conv_total,
      'max_epsilon_M1':float(np.max(eps[mask])),
      'rms_epsilon_M1':float(np.sqrt(np.mean(eps[mask]**2))),
      'total_M1_max_abs':float(np.max(np.abs(total[0.01][mask]))),
      'total_M1_L2':l2(total[0.01][mask]),
      'max_residual':{'index':idx,'r_Mpc':float(r[idx]),'x':float(st['x'][idx])},
      'grouped_contributions_at_max_residual':grouped_at,
      'dominant_group_at_max_residual':dominant,
      'individual_terms':raw,
    }


def ex_bridge(st,s,nr,qbg,qclass,hclass):
    r=st['r']; D=b4.dmat(r); mask=np.arange(len(r))>0
    pr1=D@st['phi']
    E_frame=st['udot']+b4.H_DIRECT*st['u']
    X_frame=qbg*st['u']+pr1/b4.AI
    E_c7a=st['udot']+hclass*st['u']
    X_c7a=qclass*st['u']+pr1/b4.AI
    num={}
    for h in EPS:
        Ep,Xp=frame_ex(st,+h,qbg,D); Em,Xm=frame_ex(st,-h,qbg,D)
        num[h]=((Ep-Em)/(2*h),(Xp-Xm)/(2*h))
    return {
      'scale_hinv_Mpc':s,'Nr':nr,
      'E_frame_fd_vs_analytic_relative_L2':rel_l2(num[0.01][0][mask],E_frame[mask]),
      'X_frame_fd_vs_analytic_relative_L2':rel_l2(num[0.01][1][mask],X_frame[mask]),
      'E_frame_fine_vs_mid_relative_L2':rel_l2(num[0.02][0][mask],num[0.01][0][mask]),
      'X_frame_fine_vs_mid_relative_L2':rel_l2(num[0.02][1][mask],num[0.01][1][mask]),
      'E_frame_vs_C7A_relative_L2':rel_l2(E_frame[mask],E_c7a[mask]),
      'X_frame_vs_C7A_relative_L2':rel_l2(X_frame[mask],X_c7a[mask]),
      'E_frame_L2':l2(E_frame[mask]),'X_frame_L2':l2(X_frame[mask]),
      'E_C7A_L2':l2(E_c7a[mask]),'X_C7A_L2':l2(X_c7a[mask]),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--official-npz',required=True)
    ap.add_argument('--parent-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    cov=json.loads(Path(a.coverage_json).read_text())
    parent=json.loads(Path(a.parent_json).read_text())
    off=np.load(a.official_npz)
    parent_ok=bool(parent.get('classification')=='NL1C7B4_REPAIR03_CONSTRAINT_SOURCE_LOCALIZATION_COMPLETE'
                   and parent.get('summary',{}).get('n_rows')==162
                   and parent.get('summary',{}).get('n_baseline_cases')==54
                   and parent.get('summary',{}).get('n_scaling_cases')==54)

    ks,gs=b4.groups(b4.read_trace(a.trace)); tv=b4.at_ai(gs); h=float(cov['h'])
    provenance_ok=bool(cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
                       and len(ks)==128 and cov.get('n_native_times')==179
                       and abs(float(cov.get('a_i'))-b4.AI)<1e-15 and parent_ok)
    qclass=float(np.median(tv['Q'])); hclass=float(np.median(tv['H_Mpc_inv']))
    kqbg=float(np.median(tv['KQ'])); qbg=b4.stable_q_from_kq(kqbg); zbg=stable_zbg(kqbg)
    funcs,dY,kdict=r1.build_nonK()

    states={}; maxrep=0.0
    for s in b4.SCALES:
        st=b4.make_state(s,256,ks,h,tv); states[(s,256)]=st
        for k,v in st.items():
            key=f's{int(s)}_{k}'
            if key in off.files:
                maxrep=max(maxrep,b4.rel(np.asarray(v),np.asarray(off[key])))
        states[(s,512)]=b4.make_state(s,512,ks,h,tv)
    rep_ok=bool(maxrep<=1e-12)

    bridge=[]
    for s in b4.SCALES:
      for nr in (256,512):
        bridge.append(ex_bridge(states[(s,nr)],s,nr,qbg,qclass,hclass))

    rows=[]
    for s in b4.SCALES:
      for nr in (256,512):
       for kind in KINDS:
        for beta in BETAS:
         rows.append(case_audit(states[(s,nr)],s,nr,kind,beta,qbg,zbg,funcs,dY))

    finite=all(np.isfinite(x['max_epsilon_M1']) and np.isfinite(x['total_M1_L2']) for x in rows)
    conv_ok=all(x['tangent_convergence_pass'] for x in rows)
    implementation_ok=bool(provenance_ok and rep_ok and kdict and finite and len(rows)==54 and conv_ok)
    all_close=bool(implementation_ok and all(x['max_epsilon_M1']<=PASS_LIMIT for x in rows))
    all_strong=bool(implementation_ok and all(x['max_epsilon_M1']>=MISMATCH_FLOOR for x in rows))
    all_nonK=bool(implementation_ok and all(x['dominant_group_at_max_residual']=='AeST_nonK_nonJ' for x in rows))

    if not implementation_ok:
        cls='NL1C7B4_REPAIR04_LINEARIZATION_NUMERICAL_FAIL'
        rc=2
    elif all_close:
        cls='NL1C7B4_REPAIR04_LINEAR_MOMENTUM_INTERFACE_PASS'; rc=0
    elif all_strong and all_nonK:
        cls='NL1C7B4_REPAIR04_LEADING_ORDER_INTERFACE_MISMATCH'; rc=0
    else:
        cls='NL1C7B4_REPAIR04_LINEAR_MOMENTUM_DIAGNOSTIC_COMPLETE'; rc=0

    result={
      'classification':cls,
      'scope':'Preregistered first-directional-derivative audit of the frozen Repair03 eta=0 radial momentum constraint; no state projection and no evolution.',
      'parent':{'run':35217116467,'head_sha':'27d0323f198720f14d82fb596923b93d232b081e',
                'artifact':10495093609,'artifact_sha256':'82900b1e2c85a63b9513841580c4ca71465d8adc03e58887d5f3ffdac3e11aca',
                'result_freeze_commit':'71ddc4b6135bde7eb83b68e8fc5a474211d75f72',
                'predata_commit':'451465178a3d0885713a8979d4af96708d54cbeb'},
      'state_reproduction':{'max_relative_L2':maxrep,'limit':1e-12,'pass':rep_ok},
      'symbolic_K_dictionary_identity':bool(kdict),
      'background_interface':{
        'Q_CLASS_Mpc_inv':qclass,'Q_action_Mpc_inv':qbg,
        'Q_action_minus_CLASS_Mpc_inv':float(qbg-qclass),
        'Q_relative_difference':float(abs(qbg-qclass)/max(abs(qclass),abs(qbg),1e-300)),
        'H_CLASS_Mpc_inv':hclass,'H_action_Mpc_inv':b4.H_DIRECT,
        'H_action_minus_CLASS_Mpc_inv':float(b4.H_DIRECT-hclass),
        'H_relative_difference':float(abs(b4.H_DIRECT-hclass)/max(abs(hclass),abs(b4.H_DIRECT),1e-300)),
      },
      'settings':{'directional_steps':list(EPS),'fine_step':0.01,'middle_step':0.02,
                  'convergence_limit':CONV_LIMIT,'active_fraction':ACTIVE_FRAC,
                  'linear_pass_limit':PASS_LIMIT,'strong_mismatch_floor':MISMATCH_FLOOR,
                  'scales_hinv_Mpc':list(b4.SCALES),'grids':[256,512],
                  'Y_kinds':list(KINDS),'betas':list(BETAS)},
      'EX_bridge':bridge,
      'rows':rows,
      'summary':{
        'n_cases':len(rows),'all_finite':finite,'all_tangents_converged':conv_ok,
        'max_total_fine_vs_mid_relative_L2':float(max(x['total_fine_vs_mid_relative_L2'] for x in rows)),
        'min_max_epsilon_M1':float(min(x['max_epsilon_M1'] for x in rows)),
        'max_max_epsilon_M1':float(max(x['max_epsilon_M1'] for x in rows)),
        'min_rms_epsilon_M1':float(min(x['rms_epsilon_M1'] for x in rows)),
        'max_rms_epsilon_M1':float(max(x['rms_epsilon_M1'] for x in rows)),
        'all_cases_linear_close':all_close,
        'all_cases_strong_mismatch':all_strong,
        'all_cases_nonK_dominant_at_max':all_nonK,
        'max_E_frame_vs_C7A_relative_L2':float(max(x['E_frame_vs_C7A_relative_L2'] for x in bridge)),
        'max_X_frame_vs_C7A_relative_L2':float(max(x['X_frame_vs_C7A_relative_L2'] for x in bridge)),
        'max_E_fd_vs_analytic_relative_L2':float(max(x['E_frame_fd_vs_analytic_relative_L2'] for x in bridge)),
        'max_X_fd_vs_analytic_relative_L2':float(max(x['X_frame_fd_vs_analytic_relative_L2'] for x in bridge)),
      },
      'claim_boundary':{
        'state_projected':False,'state_modified':False,'coefficient_fit_used':False,
        'sign_fit_used':False,'scale_factor_fit_used':False,'dust_sign_changed':False,
        'radial_standard_species_added':False,'action_changed':False,
        'nonlinear_evolution_executed':False,'finite_eta_executed':False,
      }
    }
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(rc)

if __name__=='__main__':
    main()
