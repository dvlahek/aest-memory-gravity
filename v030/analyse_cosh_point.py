#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
LAM=[30,100,300,1000]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output_dir'); ap.add_argument('--tag',required=True); ap.add_argument('--tau',type=float,required=True); ap.add_argument('--forcing-summary',required=True); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir); fs=json.loads(Path(z.forcing_summary).read_text()); scale=float(fs['points'][z.tag]['physical_tangent_rescale'])
    files={'base':out/'v030_cosh_base__cl.dat','ref':out/'v030_exp_ref__cl.dat'}
    for L in LAM: files[f'p{L}']=out/f'v030_{z.tag}_l{L}_p__cl.dat'; files[f'm{L}']=out/f'v030_{z.tag}_l{L}_m__cl.dat'
    for x in a.PARAMS: files[f'nuis_{x}_p']=out/f'v030_nuis_{x}_p__cl.dat'; files[f'nuis_{x}_m']=out/f'v030_nuis_{x}_m__cl.dat'
    maps={k:a.load_cl(v) for k,v in files.items()}; ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    W=a.invcov(ells,maps['base']); S={L:a.scale(a.vec(ells,maps[f'p{L}'],maps[f'm{L}'],2.0*L),scale) for L in LAM}
    adjacent=[]
    for x,y in zip(LAM[:-1],LAM[1:]): adjacent.append({'low':x,'high':y,'relative_CV_norm':a.wrel(S[x],S[y],W),'cosine_CV':a.wcos(S[x],S[y],W),'norm_low_CV':a.wnorm(S[x],W),'norm_high_CV':a.wnorm(S[y],W)})
    triple=None; chosen=None
    for i in range(len(LAM)-2):
        c1,c2=adjacent[i],adjacent[i+1]
        if c1['relative_CV_norm']<0.05 and c1['cosine_CV']>0.999 and c2['relative_CV_norm']<0.05 and c2['cosine_CV']>0.999: triple=LAM[i:i+3]; chosen=triple[-1]; break
    tangent_ok=chosen is not None
    if chosen is None: chosen=LAM[-1]
    s=S[chosen]; deriv={x:a.vec(ells,maps[f'nuis_{x}_p'],maps[f'nuis_{x}_m'],2.0*a.delta(x)) for x in a.PARAMS}; qs,bdiag=a.orthonormalize([(x,deriv[x]) for x in a.PARAMS],W); residual=a.project(s,qs,W)
    raw=a.wnorm(s,W); marg=a.wnorm(residual,W); retained=marg/max(raw,1e-300); baseline_shift=a.wnorm(a.vec(ells,maps['base'],maps['ref'],1.0),W); bath_ok=bool(fs['points'][z.tag]['quadrature_gate']); rank_ok=len(qs)==6; gates={'quadrature':bath_ok,'tangent_three_point_plateau':tangent_ok,'nuisance_rank':rank_ok}
    if all(gates.values()):
        cls='V030_COSH_CV_VISIBLE_PER_UNIT_ETA' if marg>=1 else ('V030_COSH_STRONG_SUBUNIT_ETA_FORECAST' if marg>=0.1 else ('V030_COSH_DISTINCT_LOW_SIGNIFICANCE' if marg>=1e-3 else 'V030_COSH_DISTINCT_VERY_LOW_SIGNIFICANCE'))
    else: cls='V030_COSH_NUMERICAL_FOLLOWUP_REQUIRED'
    res={'classification':cls,'model':'Cosh','tag':z.tag,'tauH0':z.tau,'benchmark_parameters':{'KB':0.5,'Q0':0.1,'K2':7500,'Z0':1e-9},'physical_force_L2_ratio_to_exp_tau1':fs['points'][z.tag]['physical_force_L2_ratio_to_exp_tau1'],'numerical_force_divisor':scale,
      'lambda_ladder':LAM,'adjacent_lambda_controls':adjacent,'selected_plateau':triple,'selected_lambda_for_tangent':chosen,'raw_CV_SNR_per_unit_eta':raw,'marginalized_CV_SNR_per_unit_eta':marg,'CV_retained_fraction_after_core_LCDM_projection':retained,'eta_for_CV_SNR_1':1.0/marg if marg>0 else None,'eta_for_CV_SNR_3':3.0/marg if marg>0 else None,
      'baseline_CV_shift_Cosh_vs_Exp_reference':baseline_shift,'nuisance_basis_rank':len(qs),'nuisance_basis_independence':bdiag,'memory_vs_parameter_CV_cosines':{x:a.wcos(s,deriv[x],W) for x in a.PARAMS},'gates':gates,
      'scope':'original v0.19 Cosh benchmark; accepted source grid; exact positive Drude offline continuum; six core LambdaCDM nuisance directions; unlensed CV TT/EE/TE'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)
if __name__=='__main__': main()
