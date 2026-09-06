#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('refit',ROOT/'v031'/'refit_baseline.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
a=r.a

KB=0.0665
REF_KB=0.1
ALPHAS=[0.0,0.125,0.25,0.5,0.75,1.0]
KNOWN={
 'canonical': {
  'params': {'H0':67.3324639084866,'omega_b':0.022377376877682164,'omega_cdm':0.12006705327635288,'tau_reio':0.06174082364515668,'n_s':0.9666229454895277,'A_s':2.1308864352626987e-09},
  'snr':2.32803921427129},
 'minus': {
  'params': {'H0':65.94510245398088,'omega_b':0.021972930478623334,'omega_cdm':0.1237390404790595,'tau_reio':0.02774677490342517,'n_s':0.9805243179345311,'A_s':1.9280413771034123e-09},
  'snr':4.472092214889027},
 'cross': {
  'params': {'H0':68.75049551652114,'omega_b':0.021881703341298655,'omega_cdm':0.1238969336867782,'tau_reio':0.05235734062388316,'n_s':0.9849766186713875,'A_s':1.969091576234291e-09},
  'snr':4.259593544697129},
 'plus': {
  'params': {'H0':68.83703130087879,'omega_b':0.02277827638394075,'omega_cdm':0.11605838822157599,'tau_reio':0.06266344784638739,'n_s':0.9546014805017466,'A_s':2.199858355344692e-09},
  'snr':0.8590293860134628}
}

def interp(p0,p1,t):
    q={}
    for k in ('H0','omega_b','omega_cdm','tau_reio','n_s'):
        q[k]=(1-t)*p0[k]+t*p1[k]
    # interpolate amplitude in the optimizer coordinate ln A_s
    q['A_s']=math.exp((1-t)*math.log(p0['A_s'])+t*math.log(p1['A_s']))
    return q

def snr_against_ref(class_root,ref_map,params,label):
    cl=r.run_class(class_root,'kb0p0665_v050',label,KB,params)
    m=a.load_cl(cl)
    s,_,_,_=r.cv_residual(ref_map,m)
    return float(s)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); cr=Path(z.class_root).resolve(); (ROOT/'results').mkdir(exist_ok=True); (cr/'output').mkdir(exist_ok=True)
    # Same fixed KB=0.1 reference definition as v0.31/v0.42.
    ref_cl=r.run_class(cr,'refkb0p1_v050','base',REF_KB,r.START); ref=a.load_cl(ref_cl)
    target=KNOWN['plus']['params']
    paths={}; endpoint_ok=True; early_descent_ok=True
    for name in ('canonical','minus','cross'):
        vals=[]
        for j,t in enumerate(ALPHAS):
            p=interp(KNOWN[name]['params'],target,t)
            s=snr_against_ref(cr,ref,p,f'{name}_a{j}')
            vals.append({'alpha':t,'CV_SNR':s,'params':p})
        src_rel=abs(vals[0]['CV_SNR']-KNOWN[name]['snr'])/KNOWN[name]['snr']
        tgt_rel=abs(vals[-1]['CV_SNR']-KNOWN['plus']['snr'])/KNOWN['plus']['snr']
        early_best=min(v['CV_SNR'] for v in vals if v['alpha']<=0.25)
        early_improvement=(vals[0]['CV_SNR']-early_best)/vals[0]['CV_SNR']
        src_pass=src_rel<0.01; tgt_pass=tgt_rel<0.01; descent=early_improvement>0.01
        endpoint_ok &= src_pass and tgt_pass; early_descent_ok &= descent
        paths[name]={'samples':vals,'source_reproduction_relative_difference':src_rel,
                     'plus_reproduction_relative_difference':tgt_rel,
                     'best_CV_SNR_alpha_le_0p25':early_best,
                     'early_relative_improvement':early_improvement,
                     'early_descent_gt_1pct':bool(descent)}
    allvals=[v['CV_SNR'] for p in paths.values() for v in p['samples']]
    gates={'all_finite':bool(np.all(np.isfinite(np.asarray(allvals,float)))),
           'known_endpoints_reproduced_lt_1pct':bool(endpoint_ok),
           'all_three_stalled_solutions_have_gt_1pct_descent_toward_plus_by_alpha_0p25':bool(early_descent_ok),
           'plus_endpoint_below_1':bool(max(p['samples'][-1]['CV_SNR'] for p in paths.values())<1.0)}
    passed=all(gates.values())
    cls='V050_OPTIMIZER_BASIN_BRIDGE_DESCENT_CONFIRMED' if passed else 'V050_OPTIMIZER_BASIN_BRIDGE_FOLLOWUP'
    res={'classification':cls,'KB':KB,'reference_KB':REF_KB,'alphas':ALPHAS,'known_v042':KNOWN,'paths':paths,'gates':gates,
         'purpose':'diagnose whether the v0.42 high-SNR multistart endpoints are genuine separated minima or stalled Gauss-Newton points by evaluating fixed interpolation bridges toward the independently found plus solution',
         'scope':'optimizer-method audit only; same six-parameter baseline objective, CLASS physics, KB, covariance definition, bounds and reference cosmology; no memory-model retuning'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not passed: raise SystemExit(2)
if __name__=='__main__': main()
