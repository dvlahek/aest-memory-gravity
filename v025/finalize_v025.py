#!/usr/bin/env python3
from pathlib import Path
import argparse, json, csv
PTS=[('p0',0.0),('p05',0.5),('p1',1.0)]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('results_dir'); ap.add_argument('--json-out',default='results/v025_tracking_sweep.json'); ap.add_argument('--csv-out',default='results/v025_tracking_sweep.csv')
    a=ap.parse_args(); d=Path(a.results_dir); rows=[]
    for tag,p in PTS:
        q=json.loads((d/f'v025_{tag}_analysis.json').read_text())
        rows.append({'tag':tag,'p':p,'raw':q['raw_CV_SNR_per_unit_eta'],'marg':q['marginalized_CV_SNR_per_unit_eta'],
                     'retained':q['CV_retained_fraction_after_core_LCDM_projection'],'eta1':q['eta_for_CV_SNR_1'],
                     'lambda':q['selected_lambda_for_tangent'],'plateau':q['selected_plateau'],'classification':q['classification'],'gates':q['gates']})
    valid=[r for r in rows if all(r['gates'].values())]; best=max(valid,key=lambda r:r['marg']) if valid else None
    base=next(r for r in rows if r['tag']=='p0'); enhancement=(best['marg']/base['marg']) if best else None
    out={'classification':'V025_BACKGROUND_TRACKING_SWEEP_PASS' if len(valid)==3 else 'V025_BACKGROUND_TRACKING_SWEEP_FOLLOWUP',
         'definition':'tau_eff(a) H0 = (H(a)/H0)^(-p), tau0H0=1','points':rows,'best_point':best,'best_marginalized_enhancement_vs_p0':enhancement,
         'interpretation_gate':'p=0 must reproduce v0.24; p=0.5 and p=1 require positive-quadrature and adaptive three-point tangent plateaus before physical interpretation'}
    Path(a.json_out).write_text(json.dumps(out,indent=2))
    with Path(a.csv_out).open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['p','raw_CV_SNR_per_eta','marg_CV_SNR_per_eta','retained','eta1sigma','selected_lambda','classification'])
        for r in rows: w.writerow([r['p'],r['raw'],r['marg'],r['retained'],r['eta1'],r['lambda'],r['classification']])
    print(json.dumps(out,indent=2))
    if len(valid)!=3: raise SystemExit(2)
if __name__=='__main__': main()
