#!/usr/bin/env python3
import argparse,json,math
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--free',required=True); p.add_argument('--eta0',required=True); p.add_argument('--json-out',required=True); a=p.parse_args()
f=json.loads(Path(a.free).read_text()); z=json.loads(Path(a.eta0).read_text())
d=float(f['final_chi2']-z['final_chi2']); eta=float(f['final_state']['eta'])
r={'classification':'V056_PLANCK_HIGHL_LOWL_COMPARISON_COMPLETE','chi2_eta0':z['final_chi2'],'chi2_free':f['final_chi2'],'delta_chi2_free_minus_eta0':d,'eta_hat':eta,'preference':'free_eta' if d<0 else 'eta0','locked_model':f['locked_model'],'likelihood':f['likelihood'],'interpretation':'Negative delta_chi2 means the frozen one-parameter memory extension improves the deterministic combined Planck fit. Statistical evidence requires the planned full posterior/likelihood-ratio validation.'}
Path(a.json_out).write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2))
