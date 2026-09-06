#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math
STARTS=('canonical','plus','minus','cross')
SPREAD_GATE=0.5; BASELINE_GATE=5.0; COND_GATE=1e8
V050_SPREAD=0.6001539004913861

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('inputs',nargs=4); ap.add_argument('--json-out',required=True); z=ap.parse_args()
    data={}
    for p in z.inputs:
        d=json.loads(Path(p).read_text()); data[d['start_name']]=d
    if set(data)!=set(STARTS): raise RuntimeError(f'expected {STARTS}, got {sorted(data)}')
    rows=[]
    for s in STARTS:
        d=data[s]; hist=d.get('history',[]); snr=float(d['best_verified_baseline_CV_SNR'])
        cond=max([float(x['normalized_GN_condition']) for x in hist] or [float('inf')])
        rows.append({'start':s,'final_CV_SNR':snr,'best_parameters':d['best_parameters'],'iterations':len(hist),
                     'best_iteration':d.get('best_iteration'),'max_normalized_condition':cond})
    vals=[x['final_CV_SNR'] for x in rows]; spread=max(vals)-min(vals); maxcond=max(x['max_normalized_condition'] for x in rows)
    gates={'all_four_finite':all(math.isfinite(x) for x in vals),
           'all_four_baseline_below_5':all(x<BASELINE_GATE for x in vals),
           'final_SNR_spread_below_0p5':spread<SPREAD_GATE,
           'conditioning_below_1e8':math.isfinite(maxcond) and maxcond<COND_GATE}
    ok=all(gates.values())
    res={'classification':'V052_GLOBAL_REFIT_CONTINUATION_CERTIFIED' if ok else 'V052_GLOBAL_REFIT_RESIDUAL_BASIN_DEPENDENCE',
         'locked_KB':0.0665,'starts':rows,'final_CV_SNR_min':min(vals),'final_CV_SNR_max':max(vals),
         'final_CV_SNR_spread':spread,'v050_spread_reference':V050_SPREAD,'spread_ratio_vs_v050':spread/V050_SPREAD,
         'max_normalized_condition_all_runs':maxcond,'predeclared_gates':{'baseline_each':5.0,'spread':0.5,'condition':1e8},
         'gates':gates,'scope':'optimizer continuation certification only; starts are exact verified v0.50 endpoints; same locked objective, physics, FD steps, bounds, damping ladder, line search and trust caps'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not ok: raise SystemExit(2)
if __name__=='__main__': main()
