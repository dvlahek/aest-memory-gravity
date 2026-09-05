#!/usr/bin/env python3
from pathlib import Path
import argparse, glob, json, math, numpy as np

LOCKED=2.32804

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--glob',default='results/v041_*_refit.json'); ap.add_argument('--json-out',required=True)
    a=ap.parse_args(); files=sorted(glob.glob(a.glob))
    if len(files)!=4: raise SystemExit(f'expected 4 refit files, got {len(files)}')
    rows=[]; conds=[]
    for f in files:
        q=json.loads(Path(f).read_text()); sn=float(q['best_verified_baseline_CV_SNR'])
        cs=[float(h['normalized_GN_condition']) for h in q.get('history',[]) if math.isfinite(float(h['normalized_GN_condition']))]
        conds.extend(cs)
        rows.append({'start':q['start_name'],'final_CV_SNR':sn,'best_parameters':q['best_parameters'],'iterations':len(q.get('history',[])),'max_GN_condition':max(cs) if cs else None})
    vals=np.array([r['final_CV_SNR'] for r in rows],float)
    canonical=next(r['final_CV_SNR'] for r in rows if r['start']=='canonical')
    gates={
      'all_four_finite':bool(np.all(np.isfinite(vals))),
      'all_four_baseline_below_5':bool(np.max(vals)<5.0),
      'final_SNR_spread_below_0p5':bool(np.ptp(vals)<0.5),
      'canonical_reproduces_locked_v038_within_0p1':bool(abs(canonical-LOCKED)<0.1),
      'conditioning_finite':bool(len(conds)>0 and np.all(np.isfinite(np.array(conds,float))))
    }
    passed=all(gates.values())
    res={'classification':'V041_PUBLICATION_CERTIFICATION_PASS' if passed else 'V041_PUBLICATION_CERTIFICATION_NEEDS_FOLLOWUP',
         'locked_KB':0.0665,'locked_v038_baseline_CV_SNR':LOCKED,'starts':rows,
         'final_CV_SNR_min':float(vals.min()),'final_CV_SNR_max':float(vals.max()),'final_CV_SNR_spread':float(np.ptp(vals)),
         'canonical_difference_from_locked_v038':float(canonical-LOCKED),
         'max_normalized_GN_condition_all_runs':float(max(conds)) if conds else None,'gates':gates,
         'scope':'deterministic four-start nonlinear six-parameter baseline refit certification at pre-locked KB=0.0665; no model retuning'}
    Path(a.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not passed: raise SystemExit(2)
if __name__=='__main__': main()
