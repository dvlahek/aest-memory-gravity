#!/usr/bin/env python3
from pathlib import Path
import argparse,json,csv,math

V020={'marg':1.9398420148928963e-7,'retained':0.5978222583759274,'raw':3.244847423651913e-7}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--forcing-summary',required=True)
    ap.add_argument('--json-out',default='results/v022_tau_sweep.json'); ap.add_argument('--csv-out',default='results/v022_tau_sweep.csv')
    args=ap.parse_args(); root=Path(args.root)
    fs=json.loads(Path(args.forcing_summary).read_text())
    rows=[]
    for p in sorted(root.glob('raw_v021_*_analysis.json')):
        d=json.loads(p.read_text()); tag=d['tag']; fc=fs['tau_points'][tag]
        # Replace the direct-in-CLASS bath metadata/control by the actual
        # offline exact-continuum quadrature control used in v0.22.
        d['bath']='offline exact linear-drive positive tan-theta Drude continuum; N1024 primary, N512 control'
        d['offline_quadrature_convergence_N512_vs_N1024']={
          'relative_L2':fc['global_relative_L2_control_vs_primary'],
          'cosine':fc['global_cosine'],
          'per_k_relative_L2_p95':fc['per_k_relative_L2_p95'],
          'per_k_relative_L2_max':fc['per_k_relative_L2_max'],
          'per_k_min_cosine':fc['per_k_min_cosine'],
          'samples':fc['samples']}
        d.pop('bath_force_convergence_N256_vs_N512',None)
        d['gates']['bath_convergence']=bool(fc['gate'])
        if all(d['gates'].values()):
            marg=d['marginalized_CV_SNR_per_unit_eta']
            if marg>=1: cls='PASS_V022_TAU_POINT_CV_VISIBLE_PER_UNIT_ETA'
            elif marg>=0.1: cls='PASS_V022_TAU_POINT_STRONG_SUBUNIT_ETA_FORECAST'
            elif marg>=1e-3: cls='PASS_V022_TAU_POINT_DISTINCT_LOW_SIGNIFICANCE'
            else: cls='PASS_V022_TAU_POINT_DISTINCT_VERY_LOW_SIGNIFICANCE'
        else: cls='V022_TAU_POINT_NUMERICAL_FOLLOWUP_REQUIRED'
        d['classification']=cls
        d['scope']='offline exact Drude continuum forcing; unlensed full-sky CV TT/EE/TE; six core LambdaCDM nuisance directions; no instrumental noise/foregrounds/lensing'
        q=root/f'v022_{tag}_analysis.json'; q.write_text(json.dumps(d,indent=2)); rows.append(d)

    rows=sorted(rows,key=lambda d:float(d['tauH0']))
    if not rows: raise RuntimeError('no raw v0.22 point analyses')
    valid=[d for d in rows if all(d.get('gates',{}).values())]
    best=max(valid,key=lambda d:d['marginalized_CV_SNR_per_unit_eta']) if valid else None
    distinct=max(valid,key=lambda d:d['CV_retained_fraction_after_core_LCDM_projection']) if valid else None
    tau1=min(rows,key=lambda d:abs(math.log10(d['tauH0'])))
    cross=None
    if abs(tau1['tauH0']-1.)<1e-12:
        cross={
          'relative_marginalized_SNR_difference_vs_v020':abs(tau1['marginalized_CV_SNR_per_unit_eta']-V020['marg'])/V020['marg'],
          'absolute_retained_fraction_difference_vs_v020':abs(tau1['CV_retained_fraction_after_core_LCDM_projection']-V020['retained']),
          'relative_raw_SNR_difference_vs_v020':abs(tau1['raw_CV_SNR_per_unit_eta']-V020['raw'])/V020['raw']}
        cross['passes']=cross['relative_marginalized_SNR_difference_vs_v020']<0.10 and cross['absolute_retained_fraction_difference_vs_v020']<0.10
    maxm=best['marginalized_CV_SNR_per_unit_eta'] if best else 0.
    if len(valid)<8: classification='V022_TAU_SWEEP_NUMERICAL_FOLLOWUP_REQUIRED'
    elif cross is not None and not cross['passes']: classification='V022_TAU_SWEEP_TAU1_CROSSCHECK_FAILED'
    elif maxm>=1: classification='PASS_V022_CV_VISIBLE_TIMESCALE_FOUND'
    elif maxm>=0.1: classification='PASS_V022_PROMISING_SUBUNIT_ETA_TIMESCALE'
    elif maxm>=1e-3: classification='PASS_V022_DISTINCT_BUT_LOW_SIGNIFICANCE_TIMESCALE'
    else: classification='PASS_V022_DISTINCT_FINGERPRINT_CMB_NOT_OBSERVABLE_FOR_UNIT_ETA'
    summary={'model':'Exp','method':'eta0 native CLASS trace + exact offline positive Drude quadrature + external variational CLASS forcing',
      'tau_points':[d['tauH0'] for d in rows],'valid_points':len(valid),'total_points':len(rows),
      'best_timescale':None if best is None else {'tauH0':best['tauH0'],'raw_CV_SNR_per_unit_eta':best['raw_CV_SNR_per_unit_eta'],'marginalized_CV_SNR_per_unit_eta':best['marginalized_CV_SNR_per_unit_eta'],'retained_fraction':best['CV_retained_fraction_after_core_LCDM_projection'],'eta_for_CV_SNR_1':best['eta_for_CV_SNR_1']},
      'most_distinct_timescale':None if distinct is None else {'tauH0':distinct['tauH0'],'retained_fraction':distinct['CV_retained_fraction_after_core_LCDM_projection'],'marginalized_CV_SNR_per_unit_eta':distinct['marginalized_CV_SNR_per_unit_eta']},
      'tau1_crosscheck_vs_v020':cross,'offline_forcing_all_tau_gate':fs['all_tau_quadrature_gate'],'classification':classification,'points':rows,
      'scope':'offline exact positive Drude continuum; unlensed CV TT/EE/TE; core six-parameter LambdaCDM projection'}
    jout=Path(args.json_out); jout.parent.mkdir(parents=True,exist_ok=True); jout.write_text(json.dumps(summary,indent=2))
    cout=Path(args.csv_out); cout.parent.mkdir(parents=True,exist_ok=True)
    with cout.open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['tauH0','valid','raw_snr_per_eta','marg_snr_per_eta','retained_fraction','eta_1sigma','quad_rel','quad_cos','lambda_rel','lambda_cos','classification'])
        for d in rows:
            fc=d['offline_quadrature_convergence_N512_vs_N1024']; mc=d['memory_tangent_control_lambda300_vs1000']
            w.writerow([d['tauH0'],int(all(d['gates'].values())),d['raw_CV_SNR_per_unit_eta'],d['marginalized_CV_SNR_per_unit_eta'],d['CV_retained_fraction_after_core_LCDM_projection'],d['eta_for_CV_SNR_1'],fc['relative_L2'],fc['cosine'],mc['relative_CV_norm'],mc['cosine_CV'],d['classification']])
    print(json.dumps(summary,indent=2))


if __name__=='__main__': main()
