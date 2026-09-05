#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math, os, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

BASE_INI=ROOT/'v019'/'ini'/'aest_exp.ini'
PARAMS=['H0','omega_b','omega_cdm','tau_reio','n_s','lnA_s']
START={'H0':67.32117,'omega_b':0.02238280,'omega_cdm':0.1201075,
       'tau_reio':0.05430842,'n_s':0.9660499,'A_s':2.100549e-9}
HALF={'H0':('fractional',0.0025),'omega_b':('fractional',0.005),
      'omega_cdm':('fractional',0.005),'tau_reio':('absolute',0.0015),
      'n_s':('absolute',0.003),'lnA_s':('log',0.01)}
BOUNDS={'H0':(50.0,85.0),'omega_b':(0.018,0.026),'omega_cdm':(0.08,0.16),
        'tau_reio':(0.01,0.12),'n_s':(0.85,1.10),'A_s':(1.0e-9,4.0e-9)}
TRUST={'H0':3.0,'omega_b':0.002,'omega_cdm':0.020,'tau_reio':0.020,'n_s':0.050,'lnA_s':0.20}


def ptag(x): return ('%.6g'%x).replace('.','p').replace('-','m')

def rewrite(text,root,kb,params):
    ch={'H0':params['H0'],'omega_b':params['omega_b'],'omega_cdm':params['omega_cdm'],
        'tau_reio':params['tau_reio'],'n_s':params['n_s'],'A_s':params['A_s'],'aest_KB':kb}
    out=[]; seen=set()
    for line in text.splitlines():
        s=line.strip(); key=s.split('=',1)[0].strip() if '=' in s else None
        if s.startswith('root ='): out.append(f'root = {root}')
        elif s.startswith('output ='): out.append('output = tCl,pCl')
        elif s.startswith('lensing ='): out.append('lensing = no')
        elif key in ch:
            out.append(f'{key} = {ch[key]:.17g}'); seen.add(key)
        else: out.append(line)
    miss=set(ch)-seen
    if miss: raise RuntimeError(f'missing parameter lines {sorted(miss)}')
    out += ['# v0.31 nonlinear baseline viability refit','aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0','aest_tau_H0 = 10']
    return '\n'.join(out)+'\n'

def run_class(class_root,tag,label,kb,params):
    text=BASE_INI.read_text(); ini=class_root/f'v031_{tag}_{label}.ini'
    root=f'output/v031_{tag}_{label}_'
    ini.write_text(rewrite(text,root,kb,params))
    env=os.environ.copy(); env['OMP_NUM_THREADS']='1'
    log=ROOT/'results'/f'v031_{tag}_{label}.log'
    with log.open('w') as f:
        cp=subprocess.run(['./class',ini.name,'../v019p/pre/p3.pre'],cwd=class_root,env=env,stdout=f,stderr=subprocess.STDOUT)
    if cp.returncode!=0: raise RuntimeError(f'CLASS failed for {label}; see {log}')
    cl=class_root/'output'/f'v031_{tag}_{label}__cl.dat'
    if not cl.exists(): raise RuntimeError(f'missing {cl}')
    return cl

def perturb(params,p,sgn):
    q=dict(params); kind,h=HALF[p]
    if p=='lnA_s': q['A_s']=params['A_s']*math.exp(sgn*h)
    elif kind=='fractional': q[p]=params[p]*(1.0+sgn*h)
    else: q[p]=params[p]+sgn*h
    return q

def delta_at(params,p):
    kind,h=HALF[p]
    if p=='lnA_s': return h
    if kind=='fractional': return params[p]*h
    return h

def cv_residual(ref_map,cand_map):
    ells=sorted(set(ref_map)&set(cand_map))
    W=a.invcov(ells,ref_map)
    r=a.vec(ells,cand_map,ref_map,1.0)
    return a.wnorm(r,W),ells,W,r

def apply_step(params,step,scale=1.0,trust_scale=1.0):
    q=dict(params); realized={}
    for i,p in enumerate(PARAMS):
        dx=float(step[i])*scale
        cap=TRUST[p]*trust_scale
        dx=max(-cap,min(cap,dx))
        if p=='lnA_s':
            old=math.log(q['A_s']); new=old+dx
            lo,hi=map(math.log,BOUNDS['A_s']); new=max(lo,min(hi,new)); q['A_s']=math.exp(new); realized[p]=new-old
        else:
            old=q[p]; lo,hi=BOUNDS[p]; new=max(lo,min(hi,old+dx)); q[p]=new; realized[p]=new-old
    return q,realized

def step_vector(realized): return np.array([realized[p] for p in PARAMS],dtype=float)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--kb',type=float,required=True)
    ap.add_argument('--iters',type=int,default=4); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); class_root=Path(z.class_root).resolve(); (ROOT/'results').mkdir(exist_ok=True); (class_root/'output').mkdir(exist_ok=True)
    tag='kb'+ptag(z.kb); ref_tag='refkb0p1'
    ref_cl=run_class(class_root,ref_tag,'base',0.1,START); ref=a.load_cl(ref_cl)
    params=dict(START); history=[]; best=None; trust_scale=1.0

    for it in range(z.iters):
        base_cl=run_class(class_root,tag,f'i{it}_base',z.kb,params); base=a.load_cl(base_cl)
        current,ells,W,r=cv_residual(ref,base)
        if best is None or current<best['snr']:
            best={'snr':current,'params':dict(params),'iteration':it,'label':f'i{it}_base'}
        # local derivatives, evaluated around the current candidate point
        jobs={}
        with ThreadPoolExecutor(max_workers=4) as ex:
            for p in PARAMS:
                for sgn,suf in [(1,'p'),(-1,'m')]:
                    pp=perturb(params,p,sgn); label=f'i{it}_{p}_{suf}'
                    jobs[ex.submit(run_class,class_root,tag,label,z.kb,pp)]=(p,sgn,label)
            paths={}
            for fut in as_completed(jobs):
                p,sgn,label=jobs[fut]; paths[(p,sgn)]=fut.result()
        deriv=[]
        for p in PARAMS:
            mp=a.load_cl(paths[(p,1)]); mm=a.load_cl(paths[(p,-1)])
            common=sorted(set(ells)&set(mp)&set(mm))
            if common!=ells: raise RuntimeError('multipole grid changed during derivative evaluation')
            deriv.append(a.vec(ells,mp,mm,2.0*delta_at(params,p)))
        G=np.array([[a.inner(deriv[i],deriv[j],W) for j in range(6)] for i in range(6)],dtype=float)
        b=np.array([a.inner(deriv[i],r,W) for i in range(6)],dtype=float)
        ridge=max(np.trace(G)/6.0,1e-300)*1e-12
        step=np.linalg.lstsq(G+ridge*np.eye(6),-b,rcond=None)[0]
        # clip to trust region, then test three actual CLASS points along the same direction
        trial_specs=[]
        for fac in (1.0,0.5,0.25):
            pp,real=apply_step(params,step,fac,trust_scale)
            trial_specs.append((fac,pp,real))
        trials=[]
        with ThreadPoolExecutor(max_workers=3) as ex:
            fs={ex.submit(run_class,class_root,tag,f'i{it}_ls{j}',z.kb,pp):(j,fac,pp,real) for j,(fac,pp,real) in enumerate(trial_specs)}
            for fut in as_completed(fs):
                j,fac,pp,real=fs[fut]; mm=a.load_cl(fut.result()); snr,_,_,_=cv_residual(ref,mm)
                trials.append({'factor':fac,'snr':snr,'params':pp,'realized_step':real})
        trials.sort(key=lambda x:x['snr']); chosen=trials[0]
        pred_step=step_vector(chosen['realized_step'])
        rp=list(r)
        for j in range(6): rp=a.sub(rp,a.scale(deriv[j],-pred_step[j]))  # r + J dx
        predicted=a.wnorm(rp,W)
        history.append({'iteration':it,'current_CV_SNR':current,'linear_predicted_CV_SNR':predicted,
                        'gram_condition':float(np.linalg.cond(G+ridge*np.eye(6))),
                        'raw_GN_step':{PARAMS[i]:float(step[i]) for i in range(6)},
                        'trust_scale':trust_scale,'line_search':trials,'chosen_factor':chosen['factor']})
        if chosen['snr']<best['snr']:
            best={'snr':chosen['snr'],'params':dict(chosen['params']),'iteration':it,'label':f'i{it}_line'}
        if chosen['snr'] < current*0.995:
            params=dict(chosen['params'])
        else:
            trust_scale*=0.5
            if trust_scale<0.125: break
        if best['snr']<1.0: break

    # independent final rerun of best parameters
    final_cl=run_class(class_root,tag,'best_verify',z.kb,best['params']); final_map=a.load_cl(final_cl)
    final_snr,_,_,_=cv_residual(ref,final_map)
    best['verified_CV_SNR']=final_snr
    if final_snr<5: cls='V031_REFIT_CV_CLOSE'
    elif final_snr<50: cls='V031_REFIT_PROMISING'
    else: cls='V031_REFIT_BASELINE_MISMATCH_PERSISTS'
    shifts={p:(math.log(best['params']['A_s']/START['A_s']) if p=='lnA_s' else best['params'][p]-START[p]) for p in PARAMS}
    res={'classification':cls,'KB':z.kb,'reference_KB':0.1,'initial_parameters':START,'best_parameters':best['params'],
         'parameter_shifts':shifts,'initial_baseline_CV_SNR':history[0]['current_CV_SNR'] if history else None,
         'best_verified_baseline_CV_SNR':final_snr,'best_iteration':best['iteration'],'history':history,
         'bounds':BOUNDS,'trust_caps_per_iteration':TRUST,
         'scope':'unlensed full-sky CV TT/EE/TE ell=30..2500; nonlinear Gauss-Newton refit of H0, omega_b, omega_cdm, tau_reio, n_s, lnA_s; no real-data likelihood yet'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))

if __name__=='__main__': main()
