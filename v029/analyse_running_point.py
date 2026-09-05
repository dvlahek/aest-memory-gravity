#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
LAM=[30,100,300,1000]
V024_T10_MARG=2.134876057810337e-7; V024_T10_RAW=3.566813556705916e-7; V024_T10_RET=0.5985387304017017

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output_dir'); ap.add_argument('--tag',required=True); ap.add_argument('--q',type=float,required=True); ap.add_argument('--forcing-summary',required=True); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir); fs=json.loads(Path(z.forcing_summary).read_text()); scale=float(fs['points'][z.tag]['physical_tangent_rescale'])
    files={'base':out/'v029_base__cl.dat'}
    for L in LAM: files[f'p{L}']=out/f'v029_{z.tag}_l{L}_p__cl.dat'; files[f'm{L}']=out/f'v029_{z.tag}_l{L}_m__cl.dat'
    for x in a.PARAMS: files[f'nuis_{x}_p']=out/f'v029_nuis_{x}_p__cl.dat'; files[f'nuis_{x}_m']=out/f'v029_nuis_{x}_m__cl.dat'
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
    raw=a.wnorm(s,W); marg=a.wnorm(residual,W); retained=marg/max(raw,1e-300); rank_ok=len(qs)==6; bath_ok=bool(fs['points'][z.tag]['quadrature_gate'])
    anchor={}; anchor_ok=True
    if z.tag=='q0':
        anchor={'relative_marginalized_difference_vs_v024_t10':abs(marg-V024_T10_MARG)/V024_T10_MARG,'relative_raw_difference_vs_v024_t10':abs(raw-V024_T10_RAW)/V024_T10_RAW,'absolute_retained_difference_vs_v024_t10':abs(retained-V024_T10_RET)}
        anchor_ok=anchor['relative_marginalized_difference_vs_v024_t10']<0.10 and anchor['absolute_retained_difference_vs_v024_t10']<0.10
    gates={'quadrature':bath_ok,'tangent_three_point_plateau':tangent_ok,'nuisance_rank':rank_ok,'q0_v024_t10_anchor':anchor_ok}
    res={'classification':'V029_RUNNING_DIAGNOSTIC_VALIDATED' if all(gates.values()) else 'V029_RUNNING_DIAGNOSTIC_NUMERICAL_FOLLOWUP_REQUIRED','tag':z.tag,'q':z.q,'tauH0':10.0,'definition':'eta_eff(a)=eta0*(H/H0)^q in the FLRW tangent diagnostic','status':'phenomenological diagnostic; not a final covariant model',
      'numerical_force_divisor':scale,'lambda_ladder':LAM,'adjacent_lambda_controls':adjacent,'selected_plateau':triple,'selected_lambda_for_tangent':chosen,'raw_CV_SNR_per_unit_eta0':raw,'marginalized_CV_SNR_per_unit_eta0':marg,'CV_retained_fraction_after_core_LCDM_projection':retained,
      'eta0_for_CV_SNR_1':1.0/marg if marg>0 else None,'eta0_for_CV_SNR_3':3.0/marg if marg>0 else None,'q0_anchor':anchor,'nuisance_basis_rank':len(qs),'nuisance_basis_independence':bdiag,'memory_vs_parameter_CV_cosines':{x:a.wcos(s,deriv[x],W) for x in a.PARAMS},'gates':gates}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)
if __name__=='__main__': main()
