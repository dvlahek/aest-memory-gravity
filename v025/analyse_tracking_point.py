#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
V024_MARG=1.9802711486e-7; V024_RET=0.600327394

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output_dir'); ap.add_argument('--tag',required=True); ap.add_argument('--p',type=float,required=True)
    ap.add_argument('--lambdas',required=True); ap.add_argument('--force-control',required=True); ap.add_argument('--force-primary',required=True); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir); lams=[int(x) for x in z.lambdas.split(',') if x]
    files={'base':out/'v025_base__cl.dat'}
    for L in lams: files[f'p{L}']=out/f'v025_{z.tag}_l{L}_p__cl.dat'; files[f'm{L}']=out/f'v025_{z.tag}_l{L}_m__cl.dat'
    for q in a.PARAMS: files[f'nuis_{q}_p']=out/f'v025_nuis_{q}_p__cl.dat'; files[f'nuis_{q}_m']=out/f'v025_nuis_{q}_m__cl.dat'
    maps={k:a.load_cl(v) for k,v in files.items()}
    ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    W=a.invcov(ells,maps['base'])
    S={L:a.vec(ells,maps[f'p{L}'],maps[f'm{L}'],2.0*L) for L in lams}
    adjacent=[]
    for x,y in zip(lams[:-1],lams[1:]):
        adjacent.append({'low':x,'high':y,'relative_CV_norm':a.wrel(S[x],S[y],W),'cosine_CV':a.wcos(S[x],S[y],W),
                         'norm_low_CV':a.wnorm(S[x],W),'norm_high_CV':a.wnorm(S[y],W)})
    chosen=None; triple=None
    for i in range(len(lams)-2):
        c1=adjacent[i]; c2=adjacent[i+1]
        if c1['relative_CV_norm']<0.05 and c1['cosine_CV']>0.999 and c2['relative_CV_norm']<0.05 and c2['cosine_CV']>0.999:
            triple=lams[i:i+3]; chosen=triple[-1]; break
    tangent_ok=chosen is not None
    if chosen is None: chosen=lams[-1]
    s=S[chosen]
    deriv={q:a.vec(ells,maps[f'nuis_{q}_p'],maps[f'nuis_{q}_m'],2.0*a.delta(q)) for q in a.PARAMS}
    qs,bdiag=a.orthonormalize([(q,deriv[q]) for q in a.PARAMS],W); residual=a.project(s,qs,W)
    raw=a.wnorm(s,W); marg=a.wnorm(residual,W); retained=marg/max(raw,1e-300)
    overlaps={q:a.wcos(s,deriv[q],W) for q in a.PARAMS}
    fc=a.force_control(z.force_control,z.force_primary); bath_ok=fc['relative_L2']<0.01 and fc['cosine']>0.9999; rank_ok=len(qs)==6
    anchor={}; anchor_ok=True
    if z.tag=='p0':
        anchor={'relative_marginalized_difference_vs_v024':abs(marg-V024_MARG)/V024_MARG,'absolute_retained_difference_vs_v024':abs(retained-V024_RET)}
        anchor_ok=anchor['relative_marginalized_difference_vs_v024']<0.10 and anchor['absolute_retained_difference_vs_v024']<0.10
    gates={'quadrature':bath_ok,'tangent_three_point_plateau':tangent_ok,'nuisance_rank':rank_ok,'p0_v024_anchor':anchor_ok}
    if all(gates.values()):
        cls='PASS_TRACKING_CV_VISIBLE_PER_UNIT_ETA' if marg>=1 else ('PASS_TRACKING_STRONG_SUBUNIT_ETA_FORECAST' if marg>=0.1 else ('PASS_TRACKING_DISTINCT_LOW_SIGNIFICANCE' if marg>=1e-3 else 'PASS_TRACKING_DISTINCT_VERY_LOW_SIGNIFICANCE'))
    else: cls='TRACKING_POINT_NUMERICAL_FOLLOWUP_REQUIRED'
    res={'classification':cls,'tag':z.tag,'p':z.p,'tau0H0':1.0,'definition':'tau_eff H0 = (H/H0)^(-p)',
         'lambda_ladder':lams,'adjacent_lambda_controls':adjacent,'selected_plateau':triple,'selected_lambda_for_tangent':chosen,
         'force_quadrature_control':fc,'nuisance_basis_rank':len(qs),'nuisance_basis_independence':bdiag,'memory_vs_parameter_CV_cosines':overlaps,
         'raw_CV_SNR_per_unit_eta':raw,'marginalized_CV_SNR_per_unit_eta':marg,'CV_retained_fraction_after_core_LCDM_projection':retained,
         'eta_for_CV_SNR_1':1.0/marg if marg>0 else None,'eta_for_CV_SNR_3':3.0/marg if marg>0 else None,
         'p0_anchor':anchor,'gates':gates,'scope':'unlensed full-sky CV TT/EE/TE; six core LambdaCDM nuisance directions; background-tracking positive Drude spectrum'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)
if __name__=='__main__': main()
