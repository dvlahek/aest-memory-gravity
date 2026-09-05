#!/usr/bin/env python3
from pathlib import Path
import argparse,json,csv
ORDER=['t0001','t0003','t001','t003','t01','t03','t1','t3','t10']
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('results'); ap.add_argument('--json-out',required=True); ap.add_argument('--csv-out',required=True); z=ap.parse_args(); root=Path(z.results); pts=[]
    for tag in ORDER:
        p=root/f'v030_{tag}_analysis.json'
        if p.exists(): pts.append(json.loads(p.read_text()))
    valid=[x for x in pts if all(x.get('gates',{}).values())]; best=max(valid,key=lambda x:x['marginalized_CV_SNR_per_unit_eta']) if valid else None
    out={'classification':'V030_COSH_SWEEP_VALID' if valid else 'V030_COSH_SWEEP_NO_VALID_POINT','total_points':len(pts),'valid_points':len(valid),'best_point':best,'points':pts}
    Path(z.json_out).write_text(json.dumps(out,indent=2))
    with Path(z.csv_out).open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['tauH0','raw','marg','retained','eta1','baseline_shift','valid'])
        for x in pts: w.writerow([x['tauH0'],x['raw_CV_SNR_per_unit_eta'],x['marginalized_CV_SNR_per_unit_eta'],x['CV_retained_fraction_after_core_LCDM_projection'],x['eta_for_CV_SNR_1'],x['baseline_CV_shift_Cosh_vs_Exp_reference'],all(x.get('gates',{}).values())])
    print(json.dumps({'classification':out['classification'],'valid_points':len(valid),'best':None if best is None else {'tauH0':best['tauH0'],'marg':best['marginalized_CV_SNR_per_unit_eta'],'retained':best['CV_retained_fraction_after_core_LCDM_projection']}},indent=2))
if __name__=='__main__': main()
