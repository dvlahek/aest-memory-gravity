#!/usr/bin/env python3
from pathlib import Path
import argparse, json


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--free',required=True); ap.add_argument('--eta0',required=True); ap.add_argument('--json-out',required=True)
    a=ap.parse_args()
    f=json.loads(Path(a.free).read_text()); z=json.loads(Path(a.eta0).read_text())
    if f['classification']!='V062_ACT_DR6_LENSING_REFIT_COMPLETE' or z['classification']!='V062_ACT_DR6_LENSING_REFIT_COMPLETE':
        raise RuntimeError('unexpected v0.62 member classification')
    cf=float(f['final_chi2']); c0=float(z['final_chi2']); eta=float(f['final_state']['eta'])
    r={
      'classification':'V062_ACT_DR6_LENSING_FREE_ETA_VS_ETA0_COMPLETE',
      'chi2_free':cf,'chi2_eta0':c0,
      'delta_chi2_free_minus_eta0':cf-c0,
      'delta_chi2_improvement':c0-cf,
      'eta_hat':eta,
      'free_state':f['final_state'],'eta0_state':z['final_state'],
      'act_variant':f['act_variant'],'lens_only':f['lens_only'],'like_corrections':f['like_corrections'],
      'act_lensing_nbins':f['act_lensing_nbins'],'act_lensing_bin_centers':f['act_lensing_bin_centers'],
      'locked_model':f['locked_model'],
      'interpretation_rule':'Positive delta_chi2_improvement favors the frozen one-parameter memory extension. Report regardless of sign and compare to Planck, ACT primary CMB, and SPT without retuning.',
      'anti_tuning':'Predeclared v0.62 independent ACT DR6 lensing test.'
    }
    Path(a.json_out).write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))

if __name__=='__main__': main()
