#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
LAM=[1,3,10,30,100,300,1000]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output_dir'); ap.add_argument('--tag',required=True); ap.add_argument('--kb',type=float,required=True)
    ap.add_argument('--force-control',required=True); ap.add_argument('--force-primary',required=True); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir)
    files={'base':out/f'v027_{z.tag}_base__cl.dat','ref':out/f'v027_{z.tag}_ref__cl.dat'}
    for L in LAM: files[f'p{L}']=out/f'v027_{z.tag}_l{L}_p__cl.dat'; files[f'm{L}']=out/f'v027_{z.tag}_l{L}_m__cl.dat'
    for q in a.PARAMS: files[f'nuis_{q}_p']=out/f'v027_{z.tag}_nuis_{q}_p__cl.dat'; files[f'nuis_{q}_m']=out/f'v027_{z.tag}_nuis_{q}_m__cl.dat'
    maps={k:a.load_cl(v) for k,v in files.items()}; ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    W=a.invcov(ells,maps['base'])
    S={L:a.vec(ells,maps[f'p{L}'],maps[f'm{L}'],2.0*L) for L in LAM}
    adjacent=[]
    for x,y in zip(LAM[:-1],LAM[1:]):
        adjacent.append({'low':x,'high':y,'relative_CV_norm':a.wrel(S[x],S[y],W),'cosine_CV':a.wcos(S[x],S[y],W),
          'norm_low_CV':a.wnorm(S[x],W),'norm_high_CV':a.wnorm(S[y],W)})
    triple=None; chosen=None
    for i in range(len(LAM)-2):
        c1,c2=adjacent[i],adjacent[i+1]
        if c1['relative_CV_norm']<0.05 and c1['cosine_CV']>0.999 and c2['relative_CV_norm']<0.05 and c2['cosine_CV']>0.999:
            triple=LAM[i:i+3]; chosen=triple[-1]; break
    tangent_ok=chosen is not None
    if chosen is None: chosen=LAM[-1]
    s=S[chosen]; deriv={q:a.vec(ells,maps[f'nuis_{q}_p'],maps[f'nuis_{q}_m'],2.0*a.delta(q)) for q in a.PARAMS}
    qs,bdiag=a.orthonormalize([(q,deriv[q]) for q in a.PARAMS],W); residual=a.project(s,qs,W)
    raw=a.wnorm(s,W); marg=a.wnorm(residual,W); retained=marg/max(raw,1e-300)
    fc=a.force_control(z.force_control,z.force_primary); bath_ok=fc['relative_L2']<0.01 and fc['cosine']>0.9999; rank_ok=len(qs)==6
    baseline_delta=a.vec(ells,maps['base'],maps['ref'],1.0); baseline_shift=a.wnorm(baseline_delta,W)
    overlaps={q:a.wcos(s,deriv[q],W) for q in a.PARAMS}
    gates={'quadrature':bath_ok,'tangent_three_point_plateau':tangent_ok,'nuisance_rank':rank_ok}
    cls='V027_KB_NUMERICAL_FOLLOWUP_REQUIRED' if not all(gates.values()) else 'V027_KB_VALIDATED'
    res={'classification':cls,'tag':z.tag,'KB':z.kb,'tauH0':10.0,'lambda_ladder':LAM,'adjacent_lambda_controls':adjacent,
      'selected_plateau':triple,'selected_lambda_for_tangent':chosen,'force_quadrature_control':fc,
      'raw_CV_SNR_per_unit_eta':raw,'marginalized_CV_SNR_per_unit_eta':marg,'CV_retained_fraction_after_core_LCDM_projection':retained,
      'eta_for_CV_SNR_1':1.0/marg if marg>0 else None,'eta_for_CV_SNR_3':3.0/marg if marg>0 else None,
      'baseline_CV_shift_vs_KB_0p1':baseline_shift,'nuisance_basis_rank':len(qs),'nuisance_basis_independence':bdiag,
      'memory_vs_parameter_CV_cosines':overlaps,'gates':gates,
      'scope':'each KB has its own eta0 AeST baseline, accepted-grid trace, six LambdaCDM nuisance derivatives and positive Drude tauH0=10 tangent'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)
if __name__=='__main__': main()
