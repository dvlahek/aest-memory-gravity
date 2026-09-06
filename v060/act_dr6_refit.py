#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, os, subprocess, sys
import numpy as np
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import v056.planck_highl_lowl_refit as v
from v054.planck_pliklite_profile import load_class_dl

KB=v.KB; TAUH0=v.TAUH0; LAMBDA=v.LAMBDA
NITER=3
ELL_MIN=600; ELL_MAX=2500
START={
  'H0':67.29978079940001,
  'omega_b':0.022041716224516936,
  'omega_cdm':0.11939298177821148,
  'tau_reio':0.06624082364510152,
  'n_s':0.9611930331039573,
  'lnA_s':-19.967780399633433,
}
STEP=dict(v.STEP)
PARAMS=list(v.PARAMS)
BOUNDS=dict(v.BOUNDS); BOUNDS['eta']=(-40.,40.); BOUNDS['A_act']=(0.5,1.5); BOUNDS['P_act']=(0.9,1.1)

class ACTLike:
    def __init__(self, fits_path):
        import sacc
        sf=sacc.Sacc.load_fits(str(fits_path))
        self.spec_meta=[]; self.cull=[]; idx_max=0
        pol_dt={'t':'0','e':'e','b':'b'}
        for pol in ['TT','TE','EE']:
            p1,p2=pol.lower(); dt=f"cl_{pol_dt[p1]}{pol_dt[p2]}"
            for tr1,tr2 in sf.get_tracer_combinations(dt):
                ls,mu,ind=sf.get_ell_cl(dt,tr1,tr2,return_ind=True)
                mask=(ls>=ELL_MIN)&(ls<=ELL_MAX)
                if not np.all(mask): self.cull.append(ind[~mask])
                if np.any(mask):
                    window=sf.get_bandpower_windows(ind[mask])
                    self.spec_meta.append({'pol':pol.lower(),'idx':ind[mask],'spec':mu[mask],'window':window})
                    idx_max=max(idx_max,int(np.max(ind)))
        self.data_vec=np.zeros(idx_max+1)
        for m in self.spec_meta: self.data_vec[m['idx']]=m['spec']
        self.covmat=sf.covariance.covmat.copy()
        for cc in self.cull:
            self.covmat[cc,:]=0.; self.covmat[:,cc]=0.; self.covmat[cc,cc]=1e10
        self.inv_cov=np.linalg.inv(self.covmat)
        self.max_window_ell=max(int(np.max(m['window'].values)) for m in self.spec_meta)
    def chi2(self,cl,A_act,P_act):
        ps=np.zeros_like(self.data_vec)
        for m in self.spec_meta:
            idx=m['idx']; win=m['window'].weight.T; ls=m['window'].values.astype(int); pol=m['pol']
            dat=cl[pol][ls]/(A_act*A_act)
            if pol[0]=='e': dat=dat/P_act
            if pol[1]=='e': dat=dat/P_act
            ps[idx]=win@dat
        d=self.data_vec-ps
        return float(d@self.inv_cov@d)

def physical(s): return {'H0':s['H0'],'omega_b':s['omega_b'],'omega_cdm':s['omega_cdm'],'tau_reio':s['tau_reio'],'n_s':s['n_s'],'A_s':math.exp(s['lnA_s'])}
def rewrite_ini(text,root,s):
    ch=physical(s); ch['aest_KB']=KB; out=[]; seen=set(); lens=False; lm=False
    for line in text.splitlines():
        st=line.strip(); key=st.split('=',1)[0].strip() if '=' in st else None
        if st.startswith('root ='): out.append(f'root = {root}')
        elif st.startswith('output ='): out.append('output = tCl,pCl,lCl')
        elif st.startswith('lensing ='): out.append('lensing = yes'); lens=True
        elif key=='l_max_scalars': out.append('l_max_scalars = 9000'); lm=True
        elif key in ch: out.append(f'{key} = {ch[key]:.17g}'); seen.add(key)
        else: out.append(line)
    if set(ch)-seen: raise RuntimeError(f'missing CLASS parameters {sorted(set(ch)-seen)}')
    if not lens: out.append('lensing = yes')
    if not lm: out.append('l_max_scalars = 9000')
    out += ['# v0.60 predeclared ACT DR6 independent primary-CMB test','aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0',f'aest_tau_H0 = {TAUH0:.17g}']
    return '\n'.join(out)+'\n'
def run_class(cr,text,s,label,envx=None):
    ini=cr/f'v060_{label}.ini'; root=f'output/v060_{label}_'; ini.write_text(rewrite_ini(text,root,s)); env=os.environ.copy(); env['OMP_NUM_THREADS']='1'
    if envx: env.update({k:str(x) for k,x in envx.items()})
    with (ROOT/'results'/f'v060_{label}.log').open('w') as f: subprocess.run([str(cr/'class'),ini.name,str(ROOT/'v019p/pre/p3.pre')],cwd=cr,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    return cr/'output'/f'v060_{label}__cl.dat'
def zero(ell,x):
    z=np.zeros(int(ell[-1])+1); z[ell.astype(int)]=x; return z

def generate(cr,text,s,it):
    rd=ROOT/'results'; trace=rd/f'v060_it{it}_trace.dat'; bp=run_class(cr,text,s,f'it{it}_base',{'AEST_OFFLINE_TRACE_FILE':trace})
    pref=rd/f'v060_it{it}'; subprocess.run([sys.executable,str(ROOT/'v039/build_tau_forcing.py'),str(trace),'--KB',str(KB),'--tauH0',str(TAUH0),'--out-prefix',str(pref),'--control-order','512','--primary-order','1024','--summary',str(rd/f'v060_it{it}_forcing.json')],check=True)
    force=str(pref)+'_force.dat'; pp=run_class(cr,text,s,f'it{it}_l10p',{'AEST_TANGENT_FORCE_FILE':force,'AEST_TANGENT_LAMBDA':LAMBDA}); pm=run_class(cr,text,s,f'it{it}_l10m',{'AEST_TANGENT_FORCE_FILE':force,'AEST_TANGENT_LAMBDA':-LAMBDA})
    eb,ttb,teb,eeb=load_class_dl(bp); ep,ttp,tep,eep=load_class_dl(pp); em,ttm,tem,eem=load_class_dl(pm)
    if not (np.array_equal(eb,ep) and np.array_equal(eb,em)): raise RuntimeError('CLASS ell grids differ')
    B={'tt':zero(eb,ttb),'te':zero(eb,teb),'ee':zero(eb,eeb)}
    T={'tt':zero(eb,(ttp-ttm)/(2*LAMBDA)),'te':zero(eb,(tep-tem)/(2*LAMBDA)),'ee':zero(eb,(eep-eem)/(2*LAMBDA))}
    D={}
    for q in PARAMS:
        sp=dict(s); sm=dict(s); sp[q]+=STEP[q]; sm[q]-=STEP[q]
        ap=run_class(cr,text,sp,f'it{it}_{q}_p'); am=run_class(cr,text,sm,f'it{it}_{q}_m')
        e1,t1,x1,y1=load_class_dl(ap); e2,t2,x2,y2=load_class_dl(am)
        D[q]={'tt':zero(e1,(t1-t2)/(2*STEP[q])),'te':zero(e1,(x1-x2)/(2*STEP[q])),'ee':zero(e1,(y1-y2)/(2*STEP[q]))}
    return B,T,D

def total_chi2(like,B,T,D,s,delta=None,names=None):
    c=dict(s); cl={k:B[k]+s['eta']*T[k] for k in B}
    if delta is not None:
        for n,x in zip(names,delta):
            c[n]+=float(x)
            if n in PARAMS:
                for k in cl: cl[k]=cl[k]+D[n][k]*float(x)
            elif n=='eta':
                for k in cl: cl[k]=cl[k]+T[k]*float(x)
    return like.chi2(cl,c['A_act'],c['P_act'])

def fit(mode,cr,fits_path,out):
    like=ACTLike(fits_path)
    state=dict(START); state.update(eta=0.0,A_act=1.0,P_act=1.0); text=v.BASE.read_text(); hist=[]
    for it in range(NITER):
        B,T,D=generate(cr,text,state,it)
        if len(B['tt'])<=like.max_window_ell: raise RuntimeError(f'CLASS lmax={len(B["tt"])-1} < ACT window lmax={like.max_window_ell}')
        names=PARAMS+(['eta'] if mode=='free' else [])+['A_act','P_act']; bounds=[]
        for n in names:
            trust=STEP[n] if n in PARAMS else (5.0 if n=='eta' else (0.02 if n=='A_act' else 0.02))
            lo,hi=BOUNDS[n]; bounds.append((max(-trust,lo-state[n]),min(trust,hi-state[n])))
        f=lambda x: total_chi2(like,B,T,D,state,x,names)
        before=f(np.zeros(len(names)))
        sol=minimize(f,np.zeros(len(names)),method='Powell',bounds=bounds,options={'maxiter':700,'xtol':1e-6,'ftol':1e-6})
        delta=dict(zip(names,sol.x)); hist.append({'iteration':it,'chi2_before':float(before),'local_chi2_after':float(sol.fun),'delta':{k:float(x) for k,x in delta.items()},'success':bool(sol.success),'message':str(sol.message)})
        for n,x in delta.items(): state[n]+=float(x)
    B,T,D=generate(cr,text,state,NITER); final=total_chi2(like,B,T,D,state)
    r={'classification':'V060_ACT_DR6_REFIT_COMPLETE','mode':mode,'iterations':NITER,'final_state':state,'final_chi2':float(final),'history':hist,
       'act_ell_cuts':[ELL_MIN,ELL_MAX],'act_window_lmax_used':like.max_window_ell,
       'locked_model':{'KB':KB,'tauH0':TAUH0,'p':0.0,'lambda':LAMBDA,'CLASS_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540'},
       'likelihood':'ACT DR6 foreground-marginalized CMB-only TT/TE/EE SACC likelihood, with A_act and P_act profiled',
       'scope':'Deterministic iterated six-parameter ACT DR6 refit, free eta versus eta=0. Selected ACT band centers remain restricted to ell=600..2500; CLASS is evaluated to l_max_scalars=9000 only because the native ACT bandpower windows for those selected bands have support through ell=8501.',
       'anti_tuning':'v0.60 is one member of the predeclared ACT/SPT/lensing three-test campaign. Frozen physics, selected ACT band centers, and forcing construction unchanged. The theory support extension is documented in provenance/v060_act_window_support_amendment.json before any ACT eta result is read.'}
    Path(out).write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--class-root',required=True); ap.add_argument('--fits',required=True); ap.add_argument('--mode',choices=['free','eta0'],required=True); ap.add_argument('--json-out',required=True); a=ap.parse_args()
    fit(a.mode,Path(a.class_root).resolve(),Path(a.fits).resolve(),a.json_out)
if __name__=='__main__': main()
