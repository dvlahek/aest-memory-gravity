#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, os, subprocess, sys
import numpy as np
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[1]

# Keep the ACT-only refit self-contained.  Importing the v0.56 Planck refit
# also imports the Planck/getdist likelihood stack, which is intentionally not
# installed in the v0.62 ACT-only workflow.  These are the unchanged v0.56
# base path, finite-difference steps, and physical parameter bounds.
BASE=ROOT/'v019/ini/aest_exp.ini'
KB=0.0665; TAUH0=10.0; LAMBDA=10.0; NITER=3
THEORY_LMAX=4000; TRIM_LMAX=2998
START={'H0':67.3324639084866,'omega_b':0.022377376877682164,'omega_cdm':0.12006705327635288,
       'tau_reio':0.06174082364515668,'n_s':0.9666229454895277,'lnA_s':math.log(2.1308864352626987e-9)}
STEP={'H0':START['H0']*0.0025,'omega_b':START['omega_b']*0.005,'omega_cdm':START['omega_cdm']*0.005,
      'tau_reio':0.0015,'n_s':0.003,'lnA_s':0.01}
PARAMS=list(STEP)
BOUNDS={'H0':(50,90),'omega_b':(0.018,0.026),'omega_cdm':(0.08,0.16),'tau_reio':(0.01,0.12),
        'n_s':(0.90,1.05),'lnA_s':(math.log(1.5e-9),math.log(3e-9)),'eta':(-40.,40.)}


def physical(s):
    return {'H0':s['H0'],'omega_b':s['omega_b'],'omega_cdm':s['omega_cdm'],
            'tau_reio':s['tau_reio'],'n_s':s['n_s'],'A_s':math.exp(s['lnA_s'])}


def rewrite_ini(text,root,s):
    ch=physical(s); ch['aest_KB']=KB
    out=[]; seen=set(); lens=False; lm=False; nl=False
    for line in text.splitlines():
        st=line.strip(); key=st.split('=',1)[0].strip() if '=' in st else None
        if st.startswith('root ='):
            out.append(f'root = {root}')
        elif st.startswith('output ='):
            out.append('output = tCl,pCl,lCl')
        elif st.startswith('lensing ='):
            out.append('lensing = yes'); lens=True
        elif key=='l_max_scalars':
            out.append(f'l_max_scalars = {THEORY_LMAX}'); lm=True
        elif key=='non linear':
            out.append('non linear = halofit'); nl=True
        elif key in ch:
            out.append(f'{key} = {ch[key]:.17g}'); seen.add(key)
        else:
            out.append(line)
    if set(ch)-seen:
        raise RuntimeError(f'missing CLASS parameters {sorted(set(ch)-seen)}')
    if not lens: out.append('lensing = yes')
    if not lm: out.append(f'l_max_scalars = {THEORY_LMAX}')
    if not nl: out.append('non linear = halofit')
    out += [
        '# v0.62 predeclared ACT DR6 lensing frozen-model test',
        'aest_memory_enabled = no',
        'aest_memory_order = 16',
        'aest_eta = 0',
        f'aest_tau_H0 = {TAUH0:.17g}'
    ]
    return '\n'.join(out)+'\n'


def run_class(cr,text,s,label,envx=None):
    ini=cr/f'v062_{label}.ini'; root=f'output/v062_{label}_'
    ini.write_text(rewrite_ini(text,root,s))
    env=os.environ.copy(); env['OMP_NUM_THREADS']='1'
    if envx: env.update({k:str(x) for k,x in envx.items()})
    with (ROOT/'results'/f'v062_{label}.log').open('w') as f:
        subprocess.run([str(cr/'class'),ini.name,str(ROOT/'v019p/pre/p3.pre')],cwd=cr,env=env,
                       stdout=f,stderr=subprocess.STDOUT,check=True)
    return cr/'output'/f'v062_{label}__cl.dat'


def load_class_ckk(path):
    arr=np.loadtxt(path)
    if arr.ndim!=2 or arr.shape[1] < 5:
        raise RuntimeError(f'CLASS pCl output missing phi-phi column: {path}, shape={arr.shape}')
    ell=arr[:,0].astype(int)
    # CLASS default format: every column is D_l=l(l+1)C_l/(2pi), and for pCl
    # column 5 is C_l^{phi phi}.  Therefore raw convergence C_l is
    # C_l^{kk}=[l(l+1)]^2 C_l^{phi phi}/4 = (pi/2) l(l+1) D_l^{phi phi}.
    dpp=arr[:,4]
    ckk=(np.pi/2.0)*ell*(ell+1.0)*dpp
    if not np.all(np.isfinite(ckk)):
        raise RuntimeError('non-finite CLASS lensing convergence spectrum')
    z=np.zeros(int(ell[-1])+1)
    z[ell]=ckk
    return ell,z


def generate(cr,text,s,it):
    rd=ROOT/'results'; trace=rd/f'v062_it{it}_trace.dat'
    bp=run_class(cr,text,s,f'it{it}_base',{'AEST_OFFLINE_TRACE_FILE':trace})
    pref=rd/f'v062_it{it}'
    subprocess.run([
        sys.executable,str(ROOT/'v039/build_tau_forcing.py'),str(trace),
        '--KB',str(KB),'--tauH0',str(TAUH0),'--out-prefix',str(pref),
        '--control-order','512','--primary-order','1024',
        '--summary',str(rd/f'v062_it{it}_forcing.json')
    ],check=True)
    force=str(pref)+'_force.dat'
    pp=run_class(cr,text,s,f'it{it}_l10p',{'AEST_TANGENT_FORCE_FILE':force,'AEST_TANGENT_LAMBDA':LAMBDA})
    pm=run_class(cr,text,s,f'it{it}_l10m',{'AEST_TANGENT_FORCE_FILE':force,'AEST_TANGENT_LAMBDA':-LAMBDA})
    eb,B=load_class_ckk(bp); ep,P=load_class_ckk(pp); em,M=load_class_ckk(pm)
    if not (np.array_equal(eb,ep) and np.array_equal(eb,em)):
        raise RuntimeError('CLASS lensing ell grids differ')
    T=(P-M)/(2*LAMBDA)
    D={}
    for q in PARAMS:
        sp=dict(s); sm=dict(s); sp[q]+=STEP[q]; sm[q]-=STEP[q]
        ap=run_class(cr,text,sp,f'it{it}_{q}_p'); am=run_class(cr,text,sm,f'it{it}_{q}_m')
        e1,c1=load_class_ckk(ap); e2,c2=load_class_ckk(am)
        if not np.array_equal(e1,e2): raise RuntimeError(f'CLASS ell grids differ for {q}')
        D[q]=(c1-c2)/(2*STEP[q])
    return B,T,D


class ACTLensLike:
    def __init__(self):
        import act_dr6_lenslike as alike
        self.alike=alike
        self.data=alike.load_data('act_baseline',lens_only=True,like_corrections=False,trim_lmax=TRIM_LMAX)
        self.bcents=np.asarray(self.data['bcents_act'],dtype=float)
        self.nbins=int(np.asarray(self.data['data_binned_clkk']).size)
    def chi2(self,ckk):
        # The official loader standardizes the ACT binning matrix to
        # trim_lmax + 2 multipoles (L=0,...,trim_lmax+1).  Match that exact
        # matrix width rather than assuming trim_lmax+1 samples.
        ntheory=int(np.asarray(self.data['binmat_act']).shape[1])
        if len(ckk)<ntheory: return 1e100
        theory=np.asarray(ckk[:ntheory],dtype=float)
        b=np.asarray(self.data['binmat_act'])@theory
        d=np.asarray(self.data['data_binned_clkk'])-b
        return float(d@np.asarray(self.data['cinv'])@d)


def total_chi2(like,B,T,D,s,delta=None,names=None):
    c=dict(s); cl=B+s['eta']*T
    if delta is not None:
        for n,x in zip(names,delta):
            x=float(x); c[n]+=x
            if n in PARAMS: cl=cl+D[n]*x
            elif n=='eta': cl=cl+T*x
    if not np.all(np.isfinite(cl)): return 1e100
    return like.chi2(cl)


def fit(mode,cr,out):
    like=ACTLensLike(); state=dict(START); state['eta']=0.0
    text=BASE.read_text(); hist=[]
    for it in range(NITER):
        B,T,D=generate(cr,text,state,it)
        if len(B)<=TRIM_LMAX:
            raise RuntimeError(f'CLASS lensing lmax={len(B)-1} < required {TRIM_LMAX}')
        names=PARAMS+(['eta'] if mode=='free' else [])
        bounds=[]
        for n in names:
            trust=STEP[n] if n in PARAMS else 15.0
            lo,hi=BOUNDS[n]
            bounds.append((max(-trust,lo-state[n]),min(trust,hi-state[n])))
        f=lambda x: total_chi2(like,B,T,D,state,x,names)
        before=f(np.zeros(len(names)))
        sol=minimize(f,np.zeros(len(names)),method='Powell',bounds=bounds,
                     options={'maxiter':700,'xtol':1e-6,'ftol':1e-6})
        delta=dict(zip(names,sol.x))
        hist.append({'iteration':it,'chi2_before':float(before),'local_chi2_after':float(sol.fun),
                     'delta':{k:float(x) for k,x in delta.items()},
                     'success':bool(sol.success),'message':str(sol.message)})
        for n,x in delta.items(): state[n]+=float(x)
    B,T,D=generate(cr,text,state,NITER)
    final=total_chi2(like,B,T,D,state)
    r={
      'classification':'V062_ACT_DR6_LENSING_REFIT_COMPLETE',
      'mode':mode,'iterations':NITER,'final_state':state,'final_chi2':float(final),'history':hist,
      'act_variant':'act_baseline','lens_only':True,'like_corrections':False,
      'act_lensing_nbins':like.nbins,
      'act_lensing_bin_centers':[float(x) for x in like.bcents],
      'theory_lmax':THEORY_LMAX,'likelihood_trim_lmax':TRIM_LMAX,
      'locked_model':{'KB':KB,'tauH0':TAUH0,'p':0.0,'lambda':LAMBDA,
                      'CLASS_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540'},
      'likelihood':'Official ACT DR6 ACT-only baseline CMB-lensing likelihood, lens_only=True and likelihood corrections disabled as prescribed for standalone lensing.',
      'observable':'Raw C_L^{kappa kappa} derived from the CLASS phi-phi spectrum and passed through the official ACT binning matrix/covariance.',
      'scope':'Deterministic iterated six-parameter ACT DR6 lensing-only refit, free eta versus eta=0.',
      'anti_tuning':'Predeclared v0.62 lensing member. Frozen memory physics and native ACT baseline lensing selection unchanged.'
    }
    Path(out).write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--class-root',required=True)
    ap.add_argument('--mode',choices=['free','eta0'],required=True); ap.add_argument('--json-out',required=True)
    a=ap.parse_args(); fit(a.mode,Path(a.class_root).resolve(),a.json_out)

if __name__=='__main__': main()
