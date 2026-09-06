#!/usr/bin/env python3
from pathlib import Path
import argparse, json

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--free',required=True); ap.add_argument('--eta0',required=True); ap.add_argument('--json-out',required=True); a=ap.parse_args()
    fr=json.load(open(a.free)); z=json.load(open(a.eta0))
    if fr.get('classification')!='V061_SPT3G_D1_REFIT_COMPLETE' or z.get('classification')!='V061_SPT3G_D1_REFIT_COMPLETE':
        raise RuntimeError('incomplete SPT refit member')
    d=float(fr['final_chi2']-z['final_chi2'])
    r={'classification':'V061_SPT3G_D1_FREE_ETA_VS_ETA0_COMPLETE','chi2_free':float(fr['final_chi2']),'chi2_eta0':float(z['final_chi2']),
       'delta_chi2_free_minus_eta0':d,'delta_chi2_improvement':-d,'eta_hat':float(fr['final_state']['eta']),
       'free_state':fr['final_state'],'eta0_state':z['final_state'],'spt_ell_cuts':fr['spt_ell_cuts'],'locked_model':fr['locked_model'],
       'interpretation_rule':'Negative delta_chi2_free_minus_eta0 favors the frozen one-parameter memory extension. Report regardless of sign and compare to Planck and ACT without retuning.',
       'anti_tuning':'Predeclared v0.61 independent SPT-3G D1 test.'}
    Path(a.json_out).write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))
if __name__=='__main__': main()
