#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r31',ROOT/'v031'/'refit_baseline.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

REF_START=dict(r.START)
LOCKED_V038={
    'H0':67.3324639084866,
    'omega_b':0.022377376877682164,
    'omega_cdm':0.12006705327635288,
    'tau_reio':0.06174082364515668,
    'n_s':0.9666229454895277,
    'A_s':2.1308864352626987e-9,
}

def shifted(**dx):
    q=dict(REF_START)
    for k,v in dx.items():
        if k=='lnA_s': q['A_s']*=math.exp(v)
        else: q[k]+=v
    return q

STARTS={
    'canonical':dict(REF_START),
    'locked_v038':dict(LOCKED_V038),
    'plus_halftrust':shifted(H0=1.5,omega_b=0.001,omega_cdm=0.010,tau_reio=0.010,n_s=0.025,lnA_s=0.10),
    'minus_halftrust':shifted(H0=-1.5,omega_b=-0.001,omega_cdm=-0.010,tau_reio=-0.010,n_s=-0.025,lnA_s=-0.10),
    'mixed':shifted(H0=-1.0,omega_b=0.0005,omega_cdm=0.006,tau_reio=0.012,n_s=-0.015,lnA_s=0.05),
}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('class_root')
    ap.add_argument('--kb',type=float,default=0.0665)
    ap.add_argument('--start',choices=sorted(STARTS),required=True)
    ap.add_argument('--iters',type=int,default=6)
    ap.add_argument('--json-out',required=True)
    z=ap.parse_args()
    class_root=Path(z.class_root).resolve(); (ROOT/'results').mkdir(exist_ok=True); (class_root/'output').mkdir(exist_ok=True)
    start=dict(STARTS[z.start]); tag='v042_'+z.start+'_kb'+r.ptag(z.kb); ref_tag='v042_refkb0p1'

    # IMPORTANT: all starts are compared against the same fixed KB=0.1 reference at the canonical pre-registered cosmology.
    ref_cl=r.run_class(class_root,ref_tag,'base',0.1,REF_START); ref=r.a.load_cl(ref_cl)
    params=dict(start); history=[]; best=None; trust_scale=1.0

    for it in range(z.iters):
        base_cl=r.run_class(class_root,tag,f'i{it}_base',z.kb,params); base=r.a.load_cl(base_cl)
        current,ells,W,resid=r.cv_residual(ref,base)
        if best is None or current<best['snr']:
            best={'snr':current,'params':dict(params),'iteration':it,'label':f'i{it}_base'}
        jobs={}
        with ThreadPoolExecutor(max_workers=4) as ex:
            for p in r.PARAMS:
                for sgn,suf in [(1,'p'),(-1,'m')]:
                    pp=r.perturb(params,p,sgn); label=f'i{it}_{p}_{suf}'
                    jobs[ex.submit(r.run_class,class_root,tag,label,z.kb,pp)]=(p,sgn,label)
            paths={}
            for fut in as_completed(jobs):
                p,sgn,label=jobs[fut]; paths[(p,sgn)]=fut.result()
        deriv=[]
        for p in r.PARAMS:
            mp=r.a.load_cl(paths[(p,1)]); mm=r.a.load_cl(paths[(p,-1)])
            common=sorted(set(ells)&set(mp)&set(mm))
            if common!=ells: raise RuntimeError('multipole grid changed during derivative evaluation')
            deriv.append(r.a.vec(ells,mp,mm,2.0*r.delta_at(params,p)))
        step,gn_condition,deriv_diag=r.normalized_gn_step(deriv,resid,W)
        trial_specs=[]
        for fac in (1.0,0.5,0.25):
            pp,real=r.apply_step(params,step,fac,trust_scale); trial_specs.append((fac,pp,real))
        trials=[]
        with ThreadPoolExecutor(max_workers=3) as ex:
            fs={ex.submit(r.run_class,class_root,tag,f'i{it}_ls{j}',z.kb,pp):(j,fac,pp,real) for j,(fac,pp,real) in enumerate(trial_specs)}
            for fut in as_completed(fs):
                j,fac,pp,real=fs[fut]; mm=r.a.load_cl(fut.result()); snr,_,_,_=r.cv_residual(ref,mm)
                trials.append({'factor':fac,'snr':snr,'params':pp,'realized_step':real})
        trials.sort(key=lambda x:x['snr']); chosen=trials[0]
        pred_step=r.step_vector(chosen['realized_step']); rp=list(resid)
        for j in range(6): rp=r.a.sub(rp,r.a.scale(deriv[j],-pred_step[j]))
        predicted=r.a.wnorm(rp,W)
        history.append({'iteration':it,'current_CV_SNR':current,'linear_predicted_CV_SNR':predicted,
                        'normalized_GN_condition':gn_condition,'derivative_scaling':deriv_diag,
                        'raw_GN_step':{r.PARAMS[i]:float(step[i]) for i in range(6)},
                        'trust_scale':trust_scale,'line_search':trials,'chosen_factor':chosen['factor']})
        if chosen['snr']<best['snr']:
            best={'snr':chosen['snr'],'params':dict(chosen['params']),'iteration':it,'label':f'i{it}_line'}
        if chosen['snr'] < current*0.995:
            params=dict(chosen['params'])
        else:
            trust_scale*=0.5
            if trust_scale<0.125: break
        if best['snr']<1.0: break

    final_cl=r.run_class(class_root,tag,'best_verify',z.kb,best['params']); final_map=r.a.load_cl(final_cl)
    final_snr,_,_,_=r.cv_residual(ref,final_map)
    best['verified_CV_SNR']=final_snr
    shifts_from_ref={p:(math.log(best['params']['A_s']/REF_START['A_s']) if p=='lnA_s' else best['params'][p]-REF_START[p]) for p in r.PARAMS}
    shifts_from_start={p:(math.log(best['params']['A_s']/start['A_s']) if p=='lnA_s' else best['params'][p]-start[p]) for p in r.PARAMS}
    res={'classification':'V042_MULTISTART_REFIT_RESULT','KB':z.kb,'reference_KB':0.1,'start_name':z.start,
         'fixed_reference_parameters':REF_START,'initial_candidate_parameters':start,'best_parameters':best['params'],
         'initial_baseline_CV_SNR':history[0]['current_CV_SNR'] if history else None,
         'best_verified_baseline_CV_SNR':final_snr,'best_iteration':best['iteration'],
         'parameter_shifts_from_fixed_reference':shifts_from_ref,'parameter_shifts_from_this_start':shifts_from_start,
         'history':history,'bounds':r.BOUNDS,'trust_caps_per_iteration':r.TRUST,
         'solver':'same v0.31 CV-unit-normalized symmetric Gauss-Newton with bounded line search; six iterations maximum',
         'certification_purpose':'test basin/start dependence of locked KB=0.0665 nonlinear baseline refit without changing physics, reference, objective, bounds, or trust caps',
         'scope':'unlensed full-sky CV TT/EE/TE ell=30..2500; no real-data likelihood'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))

if __name__=='__main__': main()
