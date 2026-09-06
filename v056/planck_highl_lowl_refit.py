#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, os, subprocess, sys
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from v054.planck_pliklite_profile import PlikLite, find_dataset, load_class_dl

BASE=ROOT/'v019/ini/aest_exp.ini'
KB=0.0665; TAUH0=10.0; LAMBDA=10.0
START={'H0':67.3324639084866,'omega_b':0.022377376877682164,'omega_cdm':0.12006705327635288,
       'tau_reio':0.06174082364515668,'n_s':0.9666229454895277,'lnA_s':math.log(2.1308864352626987e-9)}
STEP={'H0':START['H0']*0.0025,'omega_b':START['omega_b']*0.005,'omega_cdm':START['omega_cdm']*0.005,
      'tau_reio':0.0015,'n_s':0.003,'lnA_s':0.01}
PARAMS=list(STEP)
BOUNDS={'H0':(50,90),'omega_b':(0.018,0.026),'omega_cdm':(0.08,0.16),'tau_reio':(0.01,0.12),
        'n_s':(0.90,1.05),'lnA_s':(math.log(1.5e-9),math.log(3e-9)),'eta':(-10,10),'A_planck':(0.98,1.02)}
APL_SIGMA=0.0025; NITER=3


def locate(packages,name):
    hits=list(Path(packages).rglob(name))
    if len(hits)!=1: raise RuntimeError(f'expected one {name}, found {hits}')
    return hits[0]

class LowTT:
    lmin=2; lmax=29
    def __init__(self,packages):
        p=locate(packages,'planck_2018_lowT_native')
        self.covinv=np.linalg.inv(np.loadtxt(p/'cov.txt'))
        self.mu=np.loadtxt(p/'mu.txt')
        mu_sigma=np.zeros(self.lmax+1); mu_sigma[self.lmin:]=np.loadtxt(p/'mu_sigma.txt')
        sc=np.loadtxt(p/'cl2x_1.txt'); sv=np.loadtxt(p/'cl2x_2.txt'); self.spl=[]; self.ds=[]; self.bounds=np.zeros((28,2))
        for i in range(28):
            j=0
            while abs(sv[j,i]+5)<1e-4: j+=1
            self.bounds[i,0]=sc[j+2,i]
            j=999
            while abs(sv[j,i]-5)<1e-4: j-=1
            self.bounds[i,1]=sc[j-2,i]
            s=InterpolatedUnivariateSpline(sc[:,i],sv[:,i]); self.spl.append(s); self.ds.append(s.derivative())
        self.offset=0.0; self.offset=self.loglike(mu_sigma,1.0)
    def loglike(self,tt,cal=1.0):
        th=tt[2:30]/cal**2
        if np.any(th<self.bounds[:,0]) or np.any(th>self.bounds[:,1]): return -np.inf
        x=np.zeros_like(th); ll=0.0
        for i,(s,d,c) in enumerate(zip(self.spl,self.ds,th)):
            der=float(d(c))
            if der<0: return -np.inf
            ll+=math.log(der); x[i]=s(c)
        z=x-self.mu; ll+=-0.5*float(z@self.covinv@z); ll-=self.offset
        return float(ll)

class LowEE:
    def __init__(self,packages): self.tab=np.loadtxt(locate(packages,'planck_2018_lowE_native')/'prob_table.txt')
    def loglike(self,ee,cal=1.0):
        idx=(ee[2:30]/(cal**2*1e-4)).astype(int)
        if np.any(idx<0) or np.any(idx>=self.tab.shape[0]): return -np.inf
        return float(np.take_along_axis(self.tab,idx[np.newaxis,:],axis=0).sum())


def physical(s): return {'H0':s['H0'],'omega_b':s['omega_b'],'omega_cdm':s['omega_cdm'],'tau_reio':s['tau_reio'],'n_s':s['n_s'],'A_s':math.exp(s['lnA_s'])}
def rewrite_ini(text,root,s):
    ch=physical(s); ch['aest_KB']=KB; out=[]; seen=set(); lens=False; lm=False
    for line in text.splitlines():
        st=line.strip(); key=st.split('=',1)[0].strip() if '=' in st else None
        if st.startswith('root ='): out.append(f'root = {root}')
        elif st.startswith('output ='): out.append('output = tCl,pCl,lCl')
        elif st.startswith('lensing ='): out.append('lensing = yes'); lens=True
        elif key=='l_max_scalars': out.append('l_max_scalars = 2600'); lm=True
        elif key in ch: out.append(f'{key} = {ch[key]:.17g}'); seen.add(key)
        else: out.append(line)
    if set(ch)-seen: raise RuntimeError(f'missing CLASS parameters {sorted(set(ch)-seen)}')
    if not lens: out.append('lensing = yes')
    if not lm: out.append('l_max_scalars = 2600')
    out += ['# v0.56 frozen combined Planck likelihood','aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0',f'aest_tau_H0 = {TAUH0:.17g}']
    return '\n'.join(out)+'\n'

def run_class(cr,text,s,label,envx=None):
    ini=cr/f'v056_{label}.ini'; root=f'output/v056_{label}_'; ini.write_text(rewrite_ini(text,root,s)); env=os.environ.copy(); env['OMP_NUM_THREADS']='1'
    if envx: env.update({k:str(v) for k,v in envx.items()})
    with (ROOT/'results'/f'v056_{label}.log').open('w') as f: subprocess.run([str(cr/'class'),ini.name,str(ROOT/'v019p/pre/p3.pre')],cwd=cr,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    return cr/'output'/f'v056_{label}__cl.dat'
def arr(path): return load_class_dl(path)
def zero(ell,x):
    z=np.zeros(int(ell[-1])+1); z[ell.astype(int)]=x; return z
def binned(like,L0,tt,te,ee):
    v=[]
    for tp,c in enumerate([tt,te,ee]):
        for i in like.used_bins[tp]: v.append(np.dot(c[like.blmin[i]-L0:like.blmax[i]-L0+1],like.weights[like.blmin[i]:like.blmax[i]+1]))
    return np.asarray(v)

def generate(cr,packages,text,s,it):
    rd=ROOT/'results'; trace=rd/f'v056_it{it}_trace.dat'; bp=run_class(cr,text,s,f'it{it}_base',{'AEST_OFFLINE_TRACE_FILE':trace})
    pref=rd/f'v056_it{it}'; subprocess.run([sys.executable,str(ROOT/'v039/build_tau_forcing.py'),str(trace),'--KB',str(KB),'--tauH0',str(TAUH0),'--out-prefix',str(pref),'--control-order','512','--primary-order','1024','--summary',str(rd/f'v056_it{it}_forcing.json')],check=True)
    force=str(pref)+'_force.dat'; pp=run_class(cr,text,s,f'it{it}_l10p',{'AEST_TANGENT_FORCE_FILE':force,'AEST_TANGENT_LAMBDA':LAMBDA}); pm=run_class(cr,text,s,f'it{it}_l10m',{'AEST_TANGENT_FORCE_FILE':force,'AEST_TANGENT_LAMBDA':-LAMBDA})
    nd={}
    for q in PARAMS:
        sp=dict(s); sm=dict(s); sp[q]+=STEP[q]; sm[q]-=STEP[q]; nd[q]=(run_class(cr,text,sp,f'it{it}_{q}_p'),run_class(cr,text,sm,f'it{it}_{q}_m'))
    hl=PlikLite(find_dataset(packages)); ell,tt,te,ee=arr(bp); ep,tp,xp,yp=arr(pp); em,tm,xm,ym=arr(pm); L0=int(ell[0])
    B=binned(hl,L0,tt,te,ee); T=binned(hl,L0,(tp-tm)/(2*LAMBDA),(xp-xm)/(2*LAMBDA),(yp-ym)/(2*LAMBDA))
    fullB={'tt':zero(ell,tt),'ee':zero(ell,ee)}; fullT={'tt':zero(ell,(tp-tm)/(2*LAMBDA)),'ee':zero(ell,(yp-ym)/(2*LAMBDA))}; D={}; FD={}
    for q,(a,b) in nd.items():
        e1,t1,x1,y1=arr(a); e2,t2,x2,y2=arr(b); D[q]=(binned(hl,L0,t1,x1,y1)-binned(hl,L0,t2,x2,y2))/(2*STEP[q]); FD[q]={'tt':zero(e1,(t1-t2)/(2*STEP[q])),'ee':zero(e1,(y1-y2)/(2*STEP[q]))}
    return hl,B,T,D,fullB,fullT,FD

def total_chi2(hl,lt,le,B,T,fb,ft,s,delta=None,D=None,FD=None,names=None):
    c=dict(s)
    if delta is not None:
        for n,v in zip(names,delta): c[n]+=float(v)
    hb=B+s['eta']*T
    t=fb['tt']+s['eta']*ft['tt']; e=fb['ee']+s['eta']*ft['ee']
    if delta is not None:
        for n,v in zip(names,delta):
            if n in PARAMS: hb=hb+D[n]*v; t=t+FD[n]['tt']*v; e=e+FD[n]['ee']*v
            elif n=='eta': hb=hb+T*v; t=t+ft['tt']*v; e=e+ft['ee']*v
    A=c['A_planck']; diff=hl.X_data-hb/(A*A); h=float(diff@hl.invcov@diff); ltt=lt.loglike(t,A); lee=le.loglike(e,A)
    if not np.isfinite(ltt+lee): return 1e100
    return h-2*ltt-2*lee+((A-1)/APL_SIGMA)**2

def fit(mode,cr,packages,out):
    state=dict(START); state.update(eta=0.0,A_planck=1.0); text=BASE.read_text(); lt=LowTT(packages); le=LowEE(packages); hist=[]
    for it in range(NITER):
        hl,B,T,D,fb,ft,FD=generate(cr,packages,text,state,it); names=PARAMS+(['eta'] if mode=='free' else [])+['A_planck']; bounds=[]
        for n in names:
            trust=STEP[n] if n in PARAMS else (5.0 if n=='eta' else 0.005); lo,hi=BOUNDS[n]; bounds.append((max(-trust,lo-state[n]),min(trust,hi-state[n])))
        f=lambda x: total_chi2(hl,lt,le,B,T,fb,ft,state,x,D,FD,names); before=f(np.zeros(len(names))); sol=minimize(f,np.zeros(len(names)),method='Powell',bounds=bounds,options={'maxiter':500,'xtol':1e-6,'ftol':1e-6})
        delta=dict(zip(names,sol.x)); hist.append({'iteration':it,'chi2_before':before,'local_chi2_after':float(sol.fun),'delta':delta,'success':bool(sol.success),'message':str(sol.message)})
        for n,v in delta.items(): state[n]+=float(v)
    hl,B,T,D,fb,ft,FD=generate(cr,packages,text,state,NITER); final=total_chi2(hl,lt,le,B,T,fb,ft,state)
    r={'classification':'V056_PLANCK_HIGHL_LOWL_REFIT_COMPLETE','mode':mode,'iterations':NITER,'final_state':state,'final_chi2':final,'history':hist,
       'locked_model':{'KB':KB,'tauH0':TAUH0,'p':0.0,'lambda':LAMBDA,'CLASS_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540'},
       'likelihood':'Planck 2018 Plik-lite TTTEEE native high-l + native low-l TT + native low-l EE; common A_planck Gaussian prior sigma=0.0025',
       'scope':'Deterministic iterated six-parameter refit with exact low-l native likelihood evaluations on local CLASS spectral linearizations. Not a full posterior.',
       'anti_tuning':'Frozen v0.53 physics and theory engine unchanged; no post-Planck physics retuning.'}
    Path(out).write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))
def main():
    a=argparse.ArgumentParser(); a.add_argument('--class-root',required=True); a.add_argument('--packages',required=True); a.add_argument('--mode',choices=['free','eta0'],required=True); a.add_argument('--json-out',required=True); z=a.parse_args(); fit(z.mode,Path(z.class_root).resolve(),Path(z.packages).resolve(),z.json_out)
if __name__=='__main__': main()
