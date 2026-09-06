#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r31',ROOT/'v031'/'refit_baseline.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

BASE=dict(r.START)
PARAMS=list(r.PARAMS)
DAMPING=(0.0,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1)
LINE=(1.0,0.5,0.25,0.125,0.0625)
MIN_TRUST=1.0/64.0

def shifted(**kw):
    q=dict(BASE)
    for k,v in kw.items():
        if k=='lnA_s': q['A_s']=BASE['A_s']*math.exp(v)
        else: q[k]=BASE[k]+v
    return q

STARTS={
 'canonical':dict(BASE),
 'plus':shifted(H0=1.5,omega_b=0.0004,omega_cdm=-0.004,tau_reio=0.010,n_s=-0.012,lnA_s=0.05),
 'minus':shifted(H0=-1.5,omega_b=-0.0004,omega_cdm=0.004,tau_reio=-0.010,n_s=0.012,lnA_s=-0.05),
 'cross':shifted(H0=1.0,omega_b=-0.0005,omega_cdm=0.005,tau_reio=0.008,n_s=0.015,lnA_s=-0.04),
}

def normalized_system(deriv,residual,W):
    basis=[]; scales=[]; diag=[]
    for i,d in enumerate(deriv):
        x=r.finite_vector(f'derivative {PARAMS[i]}',d)
        amp=float(np.max(np.abs(x)))
        if not math.isfinite(amp) or amp<=1e-300: raise RuntimeError(f'invalid derivative amplitude {PARAMS[i]}')
        u=(x/amp).tolist(); n=float(r.a.wnorm(u,W))
        if not math.isfinite(n) or n<=1e-250: raise RuntimeError(f'invalid derivative norm {PARAMS[i]}')
        basis.append(r.a.scale(u,1.0/n)); scales.append((amp,n))
        diag.append({'parameter':PARAMS[i],'max_abs_derivative':amp,'CV_norm_after_maxabs_scaling':n})
    C=np.array([[r.a.inner(basis[i],basis[j],W) for j in range(6)] for i in range(6)],float)
    c=np.array([r.a.inner(basis[i],residual,W) for i in range(6)],float)
    C=0.5*(C+C.T)
    ev=np.linalg.eigvalsh(C)
    floor=max(float(np.max(np.abs(ev)))*1e-12,1e-12)
    cond=float(np.max(np.abs(ev))/max(np.min(np.abs(ev)),floor))
    return C,c,scales,diag,cond

def lm_step(C,c,scales,mu):
    A=C+mu*np.eye(6)
    try: y=np.linalg.solve(A,-c)
    except np.linalg.LinAlgError: y=np.linalg.lstsq(A,-c,rcond=1e-12)[0]
    step=np.array([(float(y[i])/scales[i][1])/scales[i][0] for i in range(6)],float)
    if not np.all(np.isfinite(step)): raise RuntimeError('non-finite LM step')
    return step

def predicted_norm(step,deriv,residual,W,trust_scale):
    _,real=r.apply_step(dict(BASE),step,1.0,trust_scale)  # only cap magnitudes; origin irrelevant for non-boundary steps
    sv=r.step_vector(real)
    rp=list(residual)
    for j in range(6): rp=r.a.sub(rp,r.a.scale(deriv[j],-sv[j]))
    return float(r.a.wnorm(rp,W))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--kb',type=float,default=0.0665)
    ap.add_argument('--start',choices=sorted(STARTS),required=True); ap.add_argument('--iters',type=int,default=18); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); class_root=Path(z.class_root).resolve(); (ROOT/'results').mkdir(exist_ok=True); (class_root/'output').mkdir(exist_ok=True)
    # The reference cosmology and all physical/FD settings are exactly v0.31/v0.42.
    ref_cl=r.run_class(class_root,'v050_refkb0p1','base',0.1,BASE); ref=r.a.load_cl(ref_cl)
    params=dict(STARTS[z.start]); initial=dict(params); history=[]; best=None; trust_scale=1.0; stagnant=0
    tag=f'v050_{z.start}'
    for it in range(z.iters):
        base_cl=r.run_class(class_root,tag,f'i{it}_base',z.kb,params); base=r.a.load_cl(base_cl)
        current,ells,W,residual=r.cv_residual(ref,base)
        if best is None or current<best['snr']: best={'snr':current,'params':dict(params),'iteration':it}
        jobs={}
        with ThreadPoolExecutor(max_workers=4) as ex:
            for p in PARAMS:
                for sgn,suf in ((1,'p'),(-1,'m')):
                    pp=r.perturb(params,p,sgn); jobs[ex.submit(r.run_class,class_root,tag,f'i{it}_{p}_{suf}',z.kb,pp)]=(p,sgn)
            paths={}
            for fut in as_completed(jobs): paths[jobs[fut]]=fut.result()
        deriv=[]
        for p in PARAMS:
            mp=r.a.load_cl(paths[(p,1)]); mm=r.a.load_cl(paths[(p,-1)])
            common=sorted(set(ells)&set(mp)&set(mm))
            if common!=ells: raise RuntimeError('multipole grid changed during derivative evaluation')
            deriv.append(r.a.vec(ells,mp,mm,2.0*r.delta_at(params,p)))
        C,c,scales,diag,cond=normalized_system(deriv,residual,W)
        # Choose damping only from the local linear model; no extra CLASS tuning.
        lm=[]
        for mu in DAMPING:
            st=lm_step(C,c,scales,mu)
            pp,real=r.apply_step(params,st,1.0,trust_scale)
            sv=r.step_vector(real); rp=list(residual)
            for j in range(6): rp=r.a.sub(rp,r.a.scale(deriv[j],-sv[j]))
            lm.append((float(r.a.wnorm(rp,W)),mu,st))
        lm.sort(key=lambda x:(x[0],x[1])); pred,mu,step=lm[0]
        trial_specs=[]
        for fac in LINE:
            pp,real=r.apply_step(params,step,fac,trust_scale); trial_specs.append((fac,pp,real))
        trials=[]
        with ThreadPoolExecutor(max_workers=5) as ex:
            fs={ex.submit(r.run_class,class_root,tag,f'i{it}_ls{j}',z.kb,pp):(fac,pp,real) for j,(fac,pp,real) in enumerate(trial_specs)}
            for fut in as_completed(fs):
                fac,pp,real=fs[fut]; mm=r.a.load_cl(fut.result()); snr,_,_,_=r.cv_residual(ref,mm)
                trials.append({'factor':fac,'snr':float(snr),'params':pp,'realized_step':real})
        trials.sort(key=lambda x:x['snr']); chosen=trials[0]; improvement=current-chosen['snr']
        history.append({'iteration':it,'current_CV_SNR':current,'selected_LM_damping':mu,'linear_predicted_CV_SNR':pred,
                        'normalized_GN_condition':cond,'trust_scale':trust_scale,'derivative_scaling':diag,
                        'line_search':trials,'chosen_factor':chosen['factor'],'actual_improvement':improvement})
        if chosen['snr']<best['snr']: best={'snr':chosen['snr'],'params':dict(chosen['params']),'iteration':it}
        # Acceptance criterion is objective-only, independent of any target S/N threshold.
        if improvement>max(1e-5,1e-5*current):
            params=dict(chosen['params']); stagnant=stagnant+1 if improvement<1e-4 else 0
            if chosen['factor']>=0.5 and trust_scale<1.0: trust_scale=min(1.0,2.0*trust_scale)
        else:
            trust_scale*=0.5; stagnant+=1
        if stagnant>=3 and trust_scale<=0.125: break
        if trust_scale<MIN_TRUST: break
    final_cl=r.run_class(class_root,tag,'best_verify',z.kb,best['params']); fm=r.a.load_cl(final_cl); final_snr,_,_,_=r.cv_residual(ref,fm)
    res={'classification':'V050_LM_MULTISTART_MEMBER','start_name':z.start,'locked_KB':0.0665,'initial_parameters':initial,
         'best_parameters':best['params'],'best_verified_baseline_CV_SNR':float(final_snr),'best_iteration':best['iteration'],
         'history':history,'solver':'deterministic CV-normalized Levenberg-Marquardt trust-region with bounded line search',
         'solver_only_changes_from_v042':{'objective_threshold_early_stop_removed':True,'damping_ladder':list(DAMPING),'line_search_factors':list(LINE),
           'convergence_is_objective_and_trust_based':True},'unchanged':{'physics':True,'KB':0.0665,'reference_KB':0.1,'finite_difference_steps':r.HALF,'bounds':r.BOUNDS,'trust_caps':r.TRUST},
         'scope':'unlensed full-sky CV TT/EE/TE ell=30..2500; same locked six-parameter nonlinear baseline refit; no real-data likelihood'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))

if __name__=='__main__': main()
