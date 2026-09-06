#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, os, subprocess, sys
import numpy as np
from scipy.linalg import solve_triangular
from scipy.optimize import lsq_linear

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from v054.planck_pliklite_profile import PlikLite, find_dataset, load_class_dl

BASE=ROOT/'v019/ini/aest_exp.ini'
KB=0.0665
TAUH0=10.0
LAMBDA=10.0
START={
 'H0':67.3324639084866,
 'omega_b':0.022377376877682164,
 'omega_cdm':0.12006705327635288,
 'tau_reio':0.06174082364515668,
 'n_s':0.9666229454895277,
 'lnA_s':math.log(2.1308864352626987e-9),
}
# Pre-data finite-difference scales inherited from the certified six-parameter nuisance basis.
STEP={
 'H0':START['H0']*0.0025,
 'omega_b':START['omega_b']*0.005,
 'omega_cdm':START['omega_cdm']*0.005,
 'tau_reio':0.0015,
 'n_s':0.003,
 'lnA_s':0.01,
}
PARAMS=list(STEP)
BOUNDS={
 'H0':(50.0,90.0),
 'omega_b':(0.018,0.026),
 'omega_cdm':(0.08,0.16),
 'tau_reio':(0.01,0.12),
 'n_s':(0.90,1.05),
 'lnA_s':(math.log(1.5e-9),math.log(3.0e-9)),
 'eta':(-10.0,10.0),
 'A_planck':(0.98,1.02),
}
APL_SIGMA=0.0025
NITER=3
TRUST_NUISANCE=1.0
TRUST_ETA=5.0
TRUST_APL=0.005


def physical_params(state):
    return {
      'H0':state['H0'],'omega_b':state['omega_b'],'omega_cdm':state['omega_cdm'],
      'tau_reio':state['tau_reio'],'n_s':state['n_s'],'A_s':math.exp(state['lnA_s'])
    }


def rewrite_ini(text,root,state):
    changes=physical_params(state); changes['aest_KB']=KB
    out=[]; seen=set(); lens_seen=False; lmax_seen=False
    for line in text.splitlines():
        s=line.strip(); key=s.split('=',1)[0].strip() if '=' in s else None
        if s.startswith('root ='): out.append(f'root = {root}')
        elif s.startswith('output ='): out.append('output = tCl,pCl,lCl')
        elif s.startswith('lensing ='): out.append('lensing = yes'); lens_seen=True
        elif key=='l_max_scalars': out.append('l_max_scalars = 2600'); lmax_seen=True
        elif key in changes:
            out.append(f'{key} = {changes[key]:.17g}'); seen.add(key)
        else: out.append(line)
    miss=set(changes)-seen
    if miss: raise RuntimeError(f'missing CLASS parameters {sorted(miss)}')
    if not lens_seen: out.append('lensing = yes')
    if not lmax_seen: out.append('l_max_scalars = 2600')
    out += [
      '# v0.55 Planck high-l iterated six-parameter refit; frozen AeST model',
      'aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0',f'aest_tau_H0 = {TAUH0:.17g}'
    ]
    return '\n'.join(out)+'\n'


def run_class(class_root, base_text, state, label, env_extra=None):
    ini=class_root/f'v055_{label}.ini'; root=f'output/v055_{label}_'
    ini.write_text(rewrite_ini(base_text,root,state))
    env=os.environ.copy(); env['OMP_NUM_THREADS']='1'
    if env_extra: env.update({k:str(v) for k,v in env_extra.items()})
    log=ROOT/'results'/f'v055_{label}.log'
    with log.open('w') as f:
        subprocess.run([str(class_root/'class'),ini.name,str(ROOT/'v019p/pre/p3.pre')],cwd=class_root,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    return class_root/'output'/f'v055_{label}__cl.dat'


def binned(like,L0,tt,te,ee):
    vals=[]
    for tp,cell in enumerate([tt,te,ee]):
        for i in like.used_bins[tp]:
            vals.append(np.dot(cell[like.blmin[i]-L0:like.blmax[i]-L0+1],like.weights[like.blmin[i]:like.blmax[i]+1]))
    return np.asarray(vals,float)


def spectra(path):
    ell,tt,te,ee=load_class_dl(path)
    return ell,tt,te,ee


def generate_iteration(class_root,packages,base_text,state,it):
    resdir=ROOT/'results'; resdir.mkdir(exist_ok=True)
    trace=resdir/f'v055_it{it}_trace.dat'
    base_path=run_class(class_root,base_text,state,f'it{it}_base',{'AEST_OFFLINE_TRACE_FILE':trace})
    force_prefix=resdir/f'v055_it{it}'
    subprocess.run([sys.executable,str(ROOT/'v039/build_tau_forcing.py'),str(trace),'--KB',str(KB),'--tauH0',str(TAUH0),
                    '--out-prefix',str(force_prefix),'--control-order','512','--primary-order','1024',
                    '--summary',str(resdir/f'v055_it{it}_forcing.json')],check=True)
    force=str(force_prefix)+'_force.dat'
    plus_path=run_class(class_root,base_text,state,f'it{it}_l10p',{'AEST_TANGENT_FORCE_FILE':force,'AEST_TANGENT_LAMBDA':LAMBDA})
    minus_path=run_class(class_root,base_text,state,f'it{it}_l10m',{'AEST_TANGENT_FORCE_FILE':force,'AEST_TANGENT_LAMBDA':-LAMBDA})
    nuis={}
    for q in PARAMS:
        sp=dict(state); sm=dict(state); sp[q]+=STEP[q]; sm[q]-=STEP[q]
        pp=run_class(class_root,base_text,sp,f'it{it}_{q}_p')
        pm=run_class(class_root,base_text,sm,f'it{it}_{q}_m')
        nuis[q]=(pp,pm)
    like=PlikLite(find_dataset(packages))
    eb,ttb,teb,eeb=spectra(base_path); ep,ttp,tep,eep=spectra(plus_path); em,ttm,tem,eem=spectra(minus_path)
    if not (np.array_equal(eb,ep) and np.array_equal(eb,em)): raise RuntimeError('ell grid mismatch')
    L0=int(eb[0]); B=binned(like,L0,ttb,teb,eeb)
    T=binned(like,L0,(ttp-ttm)/(2*LAMBDA),(tep-tem)/(2*LAMBDA),(eep-eem)/(2*LAMBDA))
    D={}
    for q,(pp,pm) in nuis.items():
        e1,t1,x1,y1=spectra(pp); e2,t2,x2,y2=spectra(pm)
        if not (np.array_equal(eb,e1) and np.array_equal(eb,e2)): raise RuntimeError(f'ell mismatch {q}')
        D[q]=(binned(like,L0,t1,x1,y1)-binned(like,L0,t2,x2,y2))/(2*STEP[q])
    return like,B,T,D


def chi2(like,B,T,state):
    model=(B+state['eta']*T)/(state['A_planck']**2)
    d=like.X_data-model
    return float(d@like.invcov@d+((state['A_planck']-1.0)/APL_SIGMA)**2)


def fit(mode,class_root,packages,outfile):
    state=dict(START); state['eta']=0.0; state['A_planck']=1.0
    base_text=BASE.read_text(); history=[]; lastJ=None; last_like=None; lastB=None; lastT=None
    for it in range(NITER):
        like,B,T,D=generate_iteration(class_root,packages,base_text,state,it)
        A=state['A_planck']; eta=state['eta']
        model=(B+eta*T)/(A*A); data=like.X_data
        L=np.linalg.cholesky(like.cov)
        r=solve_triangular(L,data-model,lower=True)
        cols=[]; names=[]
        for q in PARAMS:
            cols.append(solve_triangular(L,D[q]/(A*A),lower=True)); names.append(q)
        if mode=='free':
            cols.append(solve_triangular(L,T/(A*A),lower=True)); names.append('eta')
        dMdA=-2.0*(B+eta*T)/(A**3)
        cols.append(solve_triangular(L,dMdA,lower=True)); names.append('A_planck')
        # Residual convention r=data-model, so linearized residual is r-J*delta.
        J=np.column_stack(cols)
        r_aug=np.r_[r,-(A-1.0)/APL_SIGMA]
        J_aug=np.vstack([J,np.array([0.0]*(len(names)-1)+[1.0/APL_SIGMA])])
        lo=[]; hi=[]
        for n in names:
            if n in PARAMS:
                trust=TRUST_NUISANCE*STEP[n]
            elif n=='eta': trust=TRUST_ETA
            else: trust=TRUST_APL
            lower,upper=BOUNDS[n]
            lo.append(max(-trust,lower-state[n])); hi.append(min(trust,upper-state[n]))
        sol=lsq_linear(J_aug,r_aug,bounds=(np.array(lo),np.array(hi)),lsq_solver='exact',tol=1e-10,max_iter=500)
        before=chi2(like,B,T,state)
        delta=dict(zip(names,sol.x))
        new=dict(state)
        for n,v in delta.items(): new[n]+=float(v)
        after_linear=float(np.sum((r_aug-J_aug@sol.x)**2))
        history.append({'iteration':it,'state_before':dict(state),'chi2_before':before,'delta':delta,
                        'linear_predicted_chi2_after':after_linear,'linear_solver_success':bool(sol.success),'linear_cost':float(sol.cost)})
        state=new; lastJ=J_aug; last_like=like; lastB=B; lastT=T
    # One final exact-in-spectrum evaluation at the final cosmology/tangent state.
    like,B,T,D=generate_iteration(class_root,packages,base_text,state,NITER)
    final_chi2=chi2(like,B,T,state)
    # Rebuild local Jacobian for a marginalized covariance estimate at the final point.
    A=state['A_planck']; eta=state['eta']; L=np.linalg.cholesky(like.cov); cols=[]; names=[]
    for q in PARAMS: cols.append(solve_triangular(L,D[q]/(A*A),lower=True)); names.append(q)
    if mode=='free': cols.append(solve_triangular(L,T/(A*A),lower=True)); names.append('eta')
    dMdA=-2.0*(B+eta*T)/(A**3); cols.append(solve_triangular(L,dMdA,lower=True)); names.append('A_planck')
    J=np.column_stack(cols); J=np.vstack([J,np.array([0.0]*(len(names)-1)+[1.0/APL_SIGMA])])
    fisher=J.T@J; cov=np.linalg.pinv(fisher,rcond=1e-12); cond=float(np.linalg.cond(fisher))
    sigma_eta=None
    if mode=='free': sigma_eta=float(math.sqrt(max(cov[names.index('eta'),names.index('eta')],0.0)))
    result={
      'classification':'V055_PLANCK_HIGHL_SIX_PARAMETER_GAUSS_NEWTON_COMPLETE',
      'mode':mode,'iterations':NITER,'final_state':state,'final_chi2':final_chi2,'sigma_eta_local_marginalized':sigma_eta,
      'eta_over_sigma':(state['eta']/sigma_eta if sigma_eta and sigma_eta>0 else None),'fisher_condition':cond,
      'history':history,
      'locked_model':{'KB':KB,'tauH0':TAUH0,'p':0.0,'lambda':LAMBDA,'CLASS_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540'},
      'likelihood':'Planck 2018 Plik-lite TTTEEE native high-l; A_planck Gaussian prior sigma=0.0025',
      'method':'Three deterministic bounded Gauss-Newton updates of H0, omega_b, omega_cdm, tau_reio, n_s, lnA_s and optionally eta. The certified centered eta tangent is recomputed at each iteration. A final fourth center evaluation reports the terminal likelihood.',
      'trust_region':{'nuisance_in_inherited_fd_steps':TRUST_NUISANCE,'eta_per_iteration':TRUST_ETA,'A_planck_per_iteration':TRUST_APL},
      'scope':'real Planck high-l TTTEEE only; no low-l TT/EE yet. This is an iterated nonlinear six-parameter refit, not a full MCMC posterior.',
      'anti_tuning':'Physics constants, CLASS commit, patch chain and eta bounds remain frozen. Optimizer settings are declared in this source before this run is inspected.'
    }
    Path(outfile).write_text(json.dumps(result,indent=2)); print(json.dumps(result,indent=2))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--class-root',required=True); ap.add_argument('--packages',required=True); ap.add_argument('--mode',choices=['free','eta0'],required=True); ap.add_argument('--json-out',required=True)
    a=ap.parse_args(); fit(a.mode,Path(a.class_root).resolve(),Path(a.packages).resolve(),a.json_out)

if __name__=='__main__': main()
