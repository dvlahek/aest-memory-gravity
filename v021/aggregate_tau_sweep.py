#!/usr/bin/env python3
from pathlib import Path
import argparse,json,csv,math

V020={'marg':1.9398420148928963e-7,'retained':0.5978222583759274,'raw':3.244847423651913e-7}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root',nargs='?',default='tau_results')
    ap.add_argument('--json-out',default='results/v021_tau_sweep.json')
    ap.add_argument('--csv-out',default='results/v021_tau_sweep.csv')
    args=ap.parse_args()
    root=Path(args.root)
    files=sorted(root.rglob('v021_*_analysis.json'))
    if not files: files=sorted(Path('.').rglob('v021_*_analysis.json'))
    rows=[]
    for p in files:
        try: d=json.loads(p.read_text())
        except Exception: continue
        rows.append(d)
    uniq={}
    for d in rows: uniq[float(d['tauH0'])]=d
    rows=[uniq[k] for k in sorted(uniq)]
    if not rows: raise RuntimeError('no tau-point analyses found')
    valid=[d for d in rows if all(d.get('gates',{}).values())]
    best=max(valid,key=lambda d:d['marginalized_CV_SNR_per_unit_eta']) if valid else None
    most_distinct=max(valid,key=lambda d:d['CV_retained_fraction_after_core_LCDM_projection']) if valid else None
    tau1=min(rows,key=lambda d:abs(math.log10(d['tauH0']))) if rows else None
    tau1_cross=None
    if tau1 and abs(tau1['tauH0']-1.0)<1e-12:
        tau1_cross={
          'relative_marginalized_SNR_difference_vs_v020':abs(tau1['marginalized_CV_SNR_per_unit_eta']-V020['marg'])/V020['marg'],
          'absolute_retained_fraction_difference_vs_v020':abs(tau1['CV_retained_fraction_after_core_LCDM_projection']-V020['retained']),
          'relative_raw_SNR_difference_vs_v020':abs(tau1['raw_CV_SNR_per_unit_eta']-V020['raw'])/V020['raw'],
        }
        tau1_cross['passes']=tau1_cross['relative_marginalized_SNR_difference_vs_v020']<0.10 and tau1_cross['absolute_retained_fraction_difference_vs_v020']<0.10
    maxm=best['marginalized_CV_SNR_per_unit_eta'] if best else 0.0
    if len(valid)<max(5,len(rows)-1):
        classification='V021_TAU_SWEEP_NUMERICAL_FOLLOWUP_REQUIRED'
    elif tau1_cross is not None and not tau1_cross['passes']:
        classification='V021_TAU_SWEEP_TAU1_CROSSCHECK_FAILED'
    elif maxm>=1.0:
        classification='PASS_V021_CV_VISIBLE_TIMESCALE_FOUND'
    elif maxm>=0.1:
        classification='PASS_V021_PROMISING_SUBUNIT_ETA_TIMESCALE'
    elif maxm>=1e-3:
        classification='PASS_V021_DISTINCT_BUT_LOW_SIGNIFICANCE_TIMESCALE'
    else:
        classification='PASS_V021_DISTINCT_FINGERPRINT_CMB_NOT_OBSERVABLE_FOR_UNIT_ETA'
    summary={
      'model':'Exp','tau_points':[d['tauH0'] for d in rows],
      'valid_points':len(valid),'total_points':len(rows),
      'best_timescale':None if best is None else {'tauH0':best['tauH0'],'raw_CV_SNR_per_unit_eta':best['raw_CV_SNR_per_unit_eta'],'marginalized_CV_SNR_per_unit_eta':best['marginalized_CV_SNR_per_unit_eta'],'retained_fraction':best['CV_retained_fraction_after_core_LCDM_projection'],'eta_for_CV_SNR_1':best['eta_for_CV_SNR_1']},
      'most_distinct_timescale':None if most_distinct is None else {'tauH0':most_distinct['tauH0'],'retained_fraction':most_distinct['CV_retained_fraction_after_core_LCDM_projection'],'marginalized_CV_SNR_per_unit_eta':most_distinct['marginalized_CV_SNR_per_unit_eta']},
      'tau1_crosscheck_vs_v020':tau1_cross,
      'classification':classification,
      'points':rows,
      'scope':'direct positive N512 Drude bath, N256 convergence control; unlensed CV TT/EE/TE; core six-parameter LambdaCDM projection'
    }
    jout=Path(args.json_out); jout.parent.mkdir(parents=True,exist_ok=True); jout.write_text(json.dumps(summary,indent=2))
    cout=Path(args.csv_out); cout.parent.mkdir(parents=True,exist_ok=True)
    with cout.open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['tauH0','valid','raw_snr_per_eta','marg_snr_per_eta','retained_fraction','eta_1sigma','bath_rel','bath_cos','lambda_rel','lambda_cos','classification'])
        for d in rows:
            fc=d['bath_force_convergence_N256_vs_N512']; mc=d['memory_tangent_control_lambda300_vs1000']
            w.writerow([d['tauH0'],int(all(d['gates'].values())),d['raw_CV_SNR_per_unit_eta'],d['marginalized_CV_SNR_per_unit_eta'],d['CV_retained_fraction_after_core_LCDM_projection'],d['eta_for_CV_SNR_1'],fc['relative_L2'],fc['cosine'],mc['relative_CV_norm'],mc['cosine_CV'],d['classification']])
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
