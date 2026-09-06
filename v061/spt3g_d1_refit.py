#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, os, subprocess, sys
import numpy as np
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import v056.planck_highl_lowl_refit as v
from v054.planck_pliklite_profile import load_class_dl

KB=0.0665; TAUH0=10.0; LAMBDA=10.0; NITER=3
ELL_MIN=400; ELL_MAX=2500; THEORY_LMAX=4500
START={'H0':67.29978079940001,'omega_b':0.022041716224516936,'omega_cdm':0.11939298177821148,
       'tau_reio':0.06624082364510152,'n_s':0.9611930331039573,'lnA_s':-19.967780399633433}
STEP=dict(v.STEP); PARAMS=list(v.PARAMS)
BOUNDS=dict(v.BOUNDS); BOUNDS['eta']=(-40.,40.); BOUNDS['Tcal']=(0.9,1.1); BOUNDS['Ecal']=(0.9,1.1)


def physical(s):
    return {'H0':s['H0'],'omega_b':s['omega_b'],'omega_cdm':s['omega_cdm'],'tau_reio':s['tau_reio'],'n_s':s['n_s'],'A_s':math.exp(s['lnA_s'])}

def rewrite_ini(text,root,s):
    ch=physical(s); ch['aest_KB']=KB; out=[]; seen=set(); lens=False; lm=False
    for line in text.splitlines():
        st=line.strip(); key=st.split('=',1)[0].strip() if '=' in st else None
        if st.startswith('root ='): out.append(f'root = {root}')
        elif st.startswith('output ='): out.append('output = tCl,pCl,lCl')
        elif st.startswith('lensing ='): out.append('lensing = yes'); lens=True
        elif key=='l_max_scalars': out.append(f'l_max_scalars = {THEORY_LMAX}'); lm=True
        elif key in ch: out.append(f'{key} = {ch[key]:.17g}'); seen.add(key)
        else: out.append(line)
    if set(ch)-seen: raise RuntimeError(f'missing CLASS parameters {sorted(set(ch)-seen)}')
    if not lens: out.append('lensing = yes')
    if not lm: out.append(f'l_max_scalars = {THEORY_LMAX}')
    out += ['# v0.61 predeclared SPT-3G D1 frozen-model test','aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0',f'aest_tau_H0 = {TAUH0:.17g}']
    return '\n'.join(out)+'\n'

def run_class(cr,text,s,label,envx=None):
    ini=cr/f'v061_{label}.ini'; root=f'output/v061_{label}_'; ini.write_text(rewrite_ini(text,root,s)); env=os.environ.copy(); env['OMP_NUM_THREADS']='1'
    if envx: env.update({k:str(x) for k,x in envx.items()})
    with (ROOT/'results'/f'v061_{label}.log').open('w') as f:
        subprocess.run([str(cr/'class'),ini.name,str(ROOT/'v019p/pre/p3.pre')],cwd=cr,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    return cr/'output'/f'v061_{label}__cl.dat'

def zero(ell,x):
    z=np.zeros(int(ell[-1])+1); z[ell.astype(int)]=x; return z

def generate(cr,text,s,it):
    rd=ROOT/'results'; trace=rd/f'v061_it{it}_trace.dat'
    bp=run_class(cr,text,s,f'it{it}_base',{'AEST_OFFLINE_TRACE_FILE':trace})
    pref=rd/f'v061_it{it}'
    subprocess.run([sys.executable,str(ROOT/'v039/build_tau_forcing.py'),str(trace),'--KB',str(KB),'--tauH0',str(TAUH0),'--out-prefix',str(pref),'--control-order','512','--primary-order','1024','--summary',str(rd/f'v061_it{it}_forcing.json')],check=True)
    force=str(pref)+'_force.dat'
    pp=run_class(cr,text,s,f'it{it}_l10p',{'AEST_TANGENT_FORCE_FILE':force,'AEST_TANGENT_LAMBDA':LAMBDA})
    pm=run_class(cr,text,s,f'it{it}_l10m',{'AEST_TANGENT_FORCE_FILE':force,'AEST_TANGENT_LAMBDA':-LAMBDA})
    eb,ttb,teb,eeb=load_class_dl(bp); ep,ttp,tep,eep=load_class_dl(pp); em,ttm,tem,eem=load_class_dl(pm)
    if not (np.array_equal(eb,ep) and np.array_equal(eb,em)): raise RuntimeError('CLASS ell grids differ')
    B={'TT':zero(eb,ttb),'TE':zero(eb,teb),'EE':zero(eb,eeb)}
    T={'TT':zero(eb,(ttp-ttm)/(2*LAMBDA)),'TE':zero(eb,(tep-tem)/(2*LAMBDA)),'EE':zero(eb,(eep-eem)/(2*LAMBDA))}
    D={}
    for q in PARAMS:
        sp=dict(s); sm=dict(s); sp[q]+=STEP[q]; sm[q]-=STEP[q]
        ap=run_class(cr,text,sp,f'it{it}_{q}_p'); am=run_class(cr,text,sm,f'it{it}_{q}_m')
        e1,t1,x1,y1=load_class_dl(ap); e2,t2,x2,y2=load_class_dl(am)
        D[q]={'TT':zero(e1,(t1-t2)/(2*STEP[q])),'TE':zero(e1,(x1-x2)/(2*STEP[q])),'EE':zero(e1,(y1-y2)/(2*STEP[q]))}
    return B,T,D

class SPTLike:
    def __init__(self):
        import candl, spt_candl_data
        self.like=candl.Like(spt_candl_data.SPT3G_D1_TnE_lite,feedback=True,
                            data_selection=['ell<400 remove','ell>2500 remove'])
        self.ell_max=int(self.like.ell_max)
        self.required=list(self.like.required_nuisance_parameters)
    def chi2(self,cl,state):
        ell=np.arange(2,self.ell_max+1,dtype=int)
        if max(ell)>=len(cl['TT']): return 1e100
        pars={'Dl':{'ell':ell,'TT':cl['TT'][2:self.ell_max+1],'TE':cl['TE'][2:self.ell_max+1],'EE':cl['EE'][2:self.ell_max+1]},
              'tau':state['tau_reio'],'Tcal':state['Tcal'],'Ecal':state['Ecal']}
        return float(-2.0*self.like.log_like(pars))

def total_chi2(like,B,T,D,s,delta=None,names=None):
    c=dict(s); cl={k:B[k]+s['eta']*T[k] for k in B}
    if delta is not None:
        for n,x in zip(names,delta):
            c[n]+=float(x)
            if n in PARAMS:
                for k in cl: cl[k]=cl[k]+D[n][k]*float(x)
            elif n=='eta':
                for k in cl: cl[k]=cl[k]+T[k]*float(x)
    return like.chi2(cl,c)

def fit(mode,cr,out):
    like=SPTLike(); state=dict(START); state.update(eta=0.0,Tcal=1.0,Ecal=1.0); text=v.BASE.read_text(); hist=[]
    for it in range(NITER):
        B,T,D=generate(cr,text,state,it)
        if len(B['TT'])<=like.ell_max: raise RuntimeError(f'CLASS lmax={len(B["TT"])-1} < SPT required ell_max={like.ell_max}')
        names=PARAMS+(['eta'] if mode=='free' else [])+['Tcal','Ecal']; bounds=[]
        for n in names:
            trust=STEP[n] if n in PARAMS else (5.0 if n=='eta' else 0.02)
            lo,hi=BOUNDS[n]; bounds.append((max(-trust,lo-state[n]),min(trust,hi-state[n])))
        f=lambda x: total_chi2(like,B,T,D,state,x,names)
        before=f(np.zeros(len(names)))
        sol=minimize(f,np.zeros(len(names)),method='Powell',bounds=bounds,options={'maxiter':700,'xtol':1e-6,'ftol':1e-6})
        delta=dict(zip(names,sol.x)); hist.append({'iteration':it,'chi2_before':float(before),'local_chi2_after':float(sol.fun),'delta':{k:float(x) for k,x in delta.items()},'success':bool(sol.success),'message':str(sol.message)})
        for n,x in delta.items(): state[n]+=float(x)
    B,T,D=generate(cr,text,state,NITER); final=total_chi2(like,B,T,D,state)
    r={'classification':'V061_SPT3G_D1_REFIT_COMPLETE','mode':mode,'iterations':NITER,'final_state':state,'final_chi2':float(final),'history':hist,
       'spt_ell_cuts':[ELL_MIN,ELL_MAX],'candl_ell_max':like.ell_max,'required_nuisance_parameters':like.required,
       'locked_model':{'KB':KB,'tauH0':TAUH0,'p':0.0,'lambda':LAMBDA,'CLASS_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540'},
       'likelihood':'Official SPT-3G D1 T&E SPTlite likelihood from SouthPoleTelescope/spt_candl_data via candl, preserving its internal priors and profiling Tcal/Ecal.',
       'scope':'Deterministic iterated six-parameter SPT-3G D1 refit, free eta versus eta=0, with candl angular-scale selection restricted to 400<=ell<=2500.',
       'anti_tuning':'Predeclared v0.61 SPT member. Frozen memory physics and selected SPT multipole policy unchanged.'}
    Path(out).write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--class-root',required=True); ap.add_argument('--mode',choices=['free','eta0'],required=True); ap.add_argument('--json-out',required=True); a=ap.parse_args()
    fit(a.mode,Path(a.class_root).resolve(),a.json_out)
if __name__=='__main__': main()
