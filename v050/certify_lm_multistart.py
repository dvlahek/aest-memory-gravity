#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math

STARTS=('canonical','plus','minus','cross')
SPREAD_GATE=0.5
BASELINE_GATE=5.0
COND_GATE=1.0e8
V042_SPREAD=3.613062828875565

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('inputs',nargs=4); ap.add_argument('--json-out',required=True); z=ap.parse_args()
    data={}
    for p in z.inputs:
        d=json.loads(Path(p).read_text()); data[d['start_name']]=d
    if set(data)!=set(STARTS): raise RuntimeError(f'expected starts {STARTS}, got {sorted(data)}')
    rows=[]
    for s in STARTS:
        d=data[s]; snr=float(d['best_verified_baseline_CV_SNR']); hist=d.get('history',[])
        cond=max([float(x['normalized_GN_condition']) for x in hist] or [float('inf')])
        rows.append({'start':s,'final_CV_SNR':snr,'best_parameters':d['best_parameters'],'iterations':len(hist),
                     'best_iteration':d.get('best_iteration'),'max_normalized_condition':cond,
                     'final_trust_scale':hist[-1]['trust_scale'] if hist else None,
                     'selected_damping_last':hist[-1]['selected_LM_damping'] if hist else None})
    vals=[x['final_CV_SNR'] for x in rows]; spread=max(vals)-min(vals); maxcond=max(x['max_normalized_condition'] for x in rows)
    gates={'all_four_finite':all(math.isfinite(x) for x in vals),
           'all_four_baseline_below_5':all(x<BASELINE_GATE for x in vals),
           'final_SNR_spread_below_0p5':spread<SPREAD_GATE,
           'conditioning_below_1e8':math.isfinite(maxcond) and maxcond<COND_GATE}
    ok=all(gates.values())
    res={'classification':'V050_GLOBAL_REFIT_CERTIFIED' if ok else 'V050_GLOBAL_REFIT_NEEDS_FOLLOWUP',
         'locked_KB':0.0665,'starts':rows,'final_CV_SNR_min':min(vals),'final_CV_SNR_max':max(vals),'final_CV_SNR_spread':spread,
         'v042_spread_reference':V042_SPREAD,'spread_ratio_vs_v042':spread/V042_SPREAD,'max_normalized_condition_all_runs':maxcond,
         'predeclared_gates':{'baseline_each':BASELINE_GATE,'spread':SPREAD_GATE,'condition':COND_GATE},'gates':gates,
         'interpretation_scope':'optimizer certification only; no change to AeST physics, KB, tau, nuisance finite-difference steps, parameter bounds, or trust caps'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not ok: raise SystemExit(2)

if __name__=='__main__': main()
