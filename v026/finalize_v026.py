#!/usr/bin/env python3
from pathlib import Path
import argparse, json, csv
POINTS=[('p05_t01',0.5,0.1),('p05_t1',0.5,1.0),('p05_t10',0.5,10.0),('p05_t100',0.5,100.0),('p1_t01',1.0,0.1),('p1_t1',1.0,1.0),('p1_t10',1.0,10.0),('p1_t100',1.0,100.0)]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('results_dir'); ap.add_argument('--json-out',default='results/v026_tau0_tracking_sweep.json'); ap.add_argument('--csv-out',default='results/v026_tau0_tracking_sweep.csv'); z=ap.parse_args()
    root=Path(z.results_dir); rows=[]; allpass=True
    for tag,p,tau0 in POINTS:
        d=json.loads((root/f'v026_{tag}_analysis.json').read_text()); ok=all(d['gates'].values()); allpass &= ok
        rows.append({'tag':tag,'p':p,'tau0H0':tau0,'raw':d['raw_CV_SNR_per_unit_eta'],'marginalized':d['marginalized_CV_SNR_per_unit_eta'],
          'retained':d['CV_retained_fraction_after_core_LCDM_projection'],'eta1':d['eta_for_CV_SNR_1'],'lambda':d['selected_lambda_for_tangent'],'plateau':d['selected_plateau'],'pass':ok})
    best=max(rows,key=lambda r:r['marginalized']); byp={}
    for p in (0.5,1.0):
        q=[r for r in rows if r['p']==p]; byp[str(p)]=max(q,key=lambda r:r['marginalized'])
    out={'classification':'V026_TAU0_TRACKING_SWEEP_PASS' if allpass else 'V026_TAU0_TRACKING_SWEEP_NEEDS_FOLLOWUP','definition':'tau_eff H0=tau0H0*(H/H0)^(-p)',
      'points':rows,'best_overall':best,'best_by_p':byp,'all_points_pass':allpass}
    Path(z.json_out).write_text(json.dumps(out,indent=2))
    with open(z.csv_out,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['tag','p','tau0H0','raw','marginalized','retained','eta1','lambda','pass']); w.writeheader()
        for r in rows: w.writerow({k:r[k] for k in w.fieldnames})
    print(json.dumps(out,indent=2))
    if not allpass: raise SystemExit(2)
if __name__=='__main__': main()
