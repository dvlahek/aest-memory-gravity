#!/usr/bin/env python3
from pathlib import Path
import argparse, glob, json, math
import numpy as np

V041_SPREAD=3.5544

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--glob',default='results/v042_*_refit.json')
    ap.add_argument('--json-out',required=True)
    a=ap.parse_args()
    files=sorted(glob.glob(a.glob))
    if len(files)!=4:
        raise SystemExit(f'expected 4 refit files, got {len(files)}')

    rows=[]; conds=[]
    for f in files:
        q=json.loads(Path(f).read_text())
        sn=float(q['best_verified_baseline_CV_SNR'])
        hs=q.get('history',[])
        cs=[float(h['normalized_GN_condition']) for h in hs if math.isfinite(float(h['normalized_GN_condition']))]
        conds.extend(cs)
        rows.append({
            'start':q['start_name'],
            'final_CV_SNR':sn,
            'best_parameters':q['best_parameters'],
            'iterations':len(hs),
            'max_GN_condition':max(cs) if cs else None,
            'best_iteration':q.get('best_iteration')
        })

    vals=np.array([r['final_CV_SNR'] for r in rows],dtype=float)
    spread=float(np.ptp(vals))
    gates={
        'all_four_finite':bool(np.all(np.isfinite(vals))),
        'all_four_baseline_below_5':bool(np.max(vals)<5.0),
        'final_SNR_spread_below_0p5':bool(spread<0.5),
        'spread_improves_over_v041':bool(spread<V041_SPREAD),
        'conditioning_finite':bool(len(conds)>0 and np.all(np.isfinite(np.asarray(conds,float))))
    }
    passed=all(gates.values())
    if passed:
        cls='V042_MULTISTART_CONVERGENCE_CERTIFIED'
    elif gates['spread_improves_over_v041']:
        cls='V042_MULTISTART_CONVERGENCE_IMPROVED_NEEDS_FOLLOWUP'
    else:
        cls='V042_MULTISTART_CONVERGENCE_NOT_RESOLVED'

    res={
        'classification':cls,
        'locked_KB':0.0665,
        'parent_v041_run':33981527693,
        'v041_final_SNR_spread_reference':V041_SPREAD,
        'starts':rows,
        'final_CV_SNR_min':float(vals.min()),
        'final_CV_SNR_max':float(vals.max()),
        'final_CV_SNR_spread':spread,
        'max_normalized_GN_condition_all_runs':float(max(conds)) if conds else None,
        'gates':gates,
        'scope':'same locked six-parameter nonlinear baseline-refit problem at KB=0.0665; same v031 normalized Gauss-Newton physics/numerics, with only the SNR<1 early stop removed and iteration budget increased to 12'
    }
    Path(a.json_out).write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2))
    if not passed:
        raise SystemExit(2)

if __name__=='__main__':
    main()
