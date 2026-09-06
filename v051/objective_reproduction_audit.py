#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r31',ROOT/'v031'/'refit_baseline.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

BASE=dict(r.START)
KB=0.0665
REFERENCE_KB=0.1
REL_GATE=1.0e-6

# Exact v0.42 reported endpoints.  The audit does not optimize or retune them.
POINTS={
 'canonical': {
   'params': {'H0':67.3324639084866,'omega_b':0.022377376877682164,'omega_cdm':0.12006705327635288,'tau_reio':0.06174082364515668,'n_s':0.9666229454895277,'A_s':2.1308864352626987e-9},
   'reported_v042_snr':2.32803921427129,
 },
 'plus': {
   'params': {'H0':68.83703130087879,'omega_b':0.02277827638394075,'omega_cdm':0.11605838822157599,'tau_reio':0.06266344784638739,'n_s':0.9546014805017466,'A_s':2.199858355344692e-9},
   'reported_v042_snr':0.8590293860134628,
 },
 'minus': {
   'params': {'H0':65.94510245398088,'omega_b':0.021972930478623334,'omega_cdm':0.1237390404790595,'tau_reio':0.02774677490342517,'n_s':0.9805243179345311,'A_s':1.9280413771034123e-9},
   'reported_v042_snr':4.472092214889027,
 },
 'cross': {
   'params': {'H0':68.75049551652114,'omega_b':0.021881703341298655,'omega_cdm':0.1238969336867782,'tau_reio':0.05235734062388316,'n_s':0.9849766186713875,'A_s':1.969091576234291e-9},
   'reported_v042_snr':4.259593544697129,
 },
}

def evaluate(class_root, ref, name, params):
    cl=r.run_class(class_root,'v051',name,KB,params)
    m=r.a.load_cl(cl)
    snr,_,_,_=r.cv_residual(ref,m)
    return float(snr)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--json-out',required=True); z=ap.parse_args()
    class_root=Path(z.class_root).resolve(); (ROOT/'results').mkdir(exist_ok=True); (class_root/'output').mkdir(exist_ok=True)
    ref_cl=r.run_class(class_root,'v051_refkb0p1','base',REFERENCE_KB,BASE); ref=r.a.load_cl(ref_cl)
    rows=[]
    for name,d in POINTS.items():
        got=evaluate(class_root,ref,name,d['params']); old=float(d['reported_v042_snr'])
        rel=abs(got-old)/max(abs(old),1e-12)
        rows.append({'point':name,'reported_v042_CV_SNR':old,'recomputed_locked_evaluator_CV_SNR':got,
                     'relative_difference':rel,'reproduced_lt_1e6':rel<REL_GATE,'parameters':d['params']})
    ok=all(x['reproduced_lt_1e6'] for x in rows)
    res={'classification':'V051_OBJECTIVE_REPRODUCTION_PASS' if ok else 'V051_OBJECTIVE_REFERENCE_MISMATCH_CONFIRMED',
         'locked_KB':KB,'reference_KB':REFERENCE_KB,'relative_gate':REL_GATE,'rows':rows,
         'all_four_reproduced':ok,
         'scope':'objective/reference reproduction audit only; exact reported v0.42 parameter points; no optimization and no AeST physics or gate changes',
         'interpretation_if_fail':'At least one reported v0.42 endpoint is not reproduced by the locked evaluator. Do not interpret bridge topology or old multistart spread until the reference/objective provenance difference is identified.'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not ok: raise SystemExit(2)

if __name__=='__main__': main()
