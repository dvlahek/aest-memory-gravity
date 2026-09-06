#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--free',required=True); ap.add_argument('--eta0',required=True); ap.add_argument('--json-out',required=True)
    a=ap.parse_args(); f=json.loads(Path(a.free).read_text()); z=json.loads(Path(a.eta0).read_text())
    d=float(f['final_chi2']-z['final_chi2']); sig=f.get('sigma_eta_local_marginalized'); eta=f['final_state']['eta']
    res={
      'classification':'V055_PLANCK_HIGHL_FREE_ETA_VS_ETA0_COMPLETE',
      'free_eta_chi2':f['final_chi2'],'eta0_chi2':z['final_chi2'],'delta_chi2_free_minus_eta0':d,
      'eta_hat':eta,'sigma_eta_local_marginalized':sig,'eta_over_sigma':(eta/sig if sig else None),
      'free_state':f['final_state'],'eta0_state':z['final_state'],
      'interpretation':'Negative Delta chi2 favors the one-parameter memory extension. This is the iterated high-l TTTEEE six-parameter refit, before low-l TT/EE and before a full posterior sampler.',
      'frozen_physics':f['locked_model']
    }
    Path(a.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
if __name__=='__main__': main()
