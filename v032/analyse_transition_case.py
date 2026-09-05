#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
LAM=[1,3,10,30,100,300,1000]


def finite(x):
    return isinstance(x,(int,float)) and math.isfinite(float(x))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir')
    ap.add_argument('--tag',required=True)
    ap.add_argument('--kb',type=float,required=True)
    ap.add_argument('--force-control',required=True)
    ap.add_argument('--force-primary',required=True)
    ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir)

    files={'base':out/f'v027_{z.tag}_base__cl.dat','ref':out/f'v027_{z.tag}_ref__cl.dat'}
    for L in LAM:
        files[f'p{L}']=out/f'v027_{z.tag}_l{L}_p__cl.dat'
        files[f'm{L}']=out/f'v027_{z.tag}_l{L}_m__cl.dat'
    for q in a.PARAMS:
        files[f'nuis_{q}_p']=out/f'v027_{z.tag}_nuis_{q}_p__cl.dat'
        files[f'nuis_{q}_m']=out/f'v027_{z.tag}_nuis_{q}_m__cl.dat'

    maps={k:a.load_cl(v) for k,v in files.items()}
    ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')

    Wcand=a.invcov(ells,maps['base'])
    Wref=a.invcov(ells,maps['ref'])

    S={L:a.vec(ells,maps[f'p{L}'],maps[f'm{L}'],2.0*L) for L in LAM}
    adjacent=[]
    for x,y in zip(LAM[:-1],LAM[1:]):
        adjacent.append({
            'low':x,'high':y,
            'relative_CV_norm_candidate_cov':a.wrel(S[x],S[y],Wcand),
            'cosine_CV_candidate_cov':a.wcos(S[x],S[y],Wcand),
            'norm_low_CV_candidate_cov':a.wnorm(S[x],Wcand),
            'norm_high_CV_candidate_cov':a.wnorm(S[y],Wcand)
        })

    triple=None; chosen=None
    for i in range(len(LAM)-2):
        c1,c2=adjacent[i],adjacent[i+1]
        if (c1['relative_CV_norm_candidate_cov']<0.05 and c1['cosine_CV_candidate_cov']>0.999 and
            c2['relative_CV_norm_candidate_cov']<0.05 and c2['cosine_CV_candidate_cov']>0.999):
            triple=LAM[i:i+3]; chosen=triple[-1]; break
    tangent_ok=chosen is not None
    if chosen is None: chosen=LAM[-1]

    s=S[chosen]
    deriv={q:a.vec(ells,maps[f'nuis_{q}_p'],maps[f'nuis_{q}_m'],2.0*a.delta(q)) for q in a.PARAMS}

    qs_c,bdiag_c=a.orthonormalize([(q,deriv[q]) for q in a.PARAMS],Wcand)
    mem_res_c=a.project(s,qs_c,Wcand)
    raw_c=a.wnorm(s,Wcand); marg_c=a.wnorm(mem_res_c,Wcand)

    qs_r,bdiag_r=a.orthonormalize([(q,deriv[q]) for q in a.PARAMS],Wref)
    mem_res_r=a.project(s,qs_r,Wref)
    raw_r=a.wnorm(s,Wref); marg_r=a.wnorm(mem_res_r,Wref)

    base_delta=a.vec(ells,maps['base'],maps['ref'],1.0)
    baseline_raw_ref=a.wnorm(base_delta,Wref)
    baseline_proj_ref=a.wnorm(a.project(base_delta,qs_r,Wref),Wref)
    baseline_raw_cand=a.wnorm(base_delta,Wcand)

    fc=a.force_control(z.force_control,z.force_primary)
    bath_ok=fc['relative_L2']<0.01 and fc['cosine']>0.9999
    rank_ok=(len(qs_c)==6 and len(qs_r)==6)

    numerical_ok=(bath_ok and tangent_ok and rank_ok and all(finite(v) for v in [raw_c,marg_c,raw_r,marg_r,baseline_raw_ref,baseline_proj_ref]))
    if not numerical_ok:
        cls='V032_TRANSITION_NUMERICAL_FOLLOWUP_REQUIRED'
    elif baseline_proj_ref<5:
        cls='V032_TRANSITION_BASELINE_CLOSE'
    elif baseline_proj_ref<50:
        cls='V032_TRANSITION_BASELINE_PROMISING'
    else:
        cls='V032_TRANSITION_BASELINE_MISMATCH'

    res={
      'classification':cls,'tag':z.tag,'KB':z.kb,'tauH0':10.0,
      'purpose':'map the KB=0.04..0.09 transition between viable baseline and amplified memory',
      'lambda_ladder':LAM,'adjacent_lambda_controls':adjacent,
      'selected_plateau':triple,'selected_lambda_for_tangent':chosen,
      'force_quadrature_control':fc,
      'memory_candidate_covariance':{
          'raw_CV_SNR_per_unit_eta':raw_c,
          'marginalized_CV_SNR_per_unit_eta':marg_c,
          'retained_fraction':marg_c/max(raw_c,1e-300),
          'eta_for_CV_SNR_1':1.0/marg_c if marg_c>0 else None
      },
      'memory_reference_covariance_crosscheck':{
          'raw_CV_SNR_per_unit_eta':raw_r,
          'marginalized_CV_SNR_per_unit_eta':marg_r,
          'retained_fraction':marg_r/max(raw_r,1e-300)
      },
      'baseline_viability':{
          'raw_CV_SNR_reference_covariance':baseline_raw_ref,
          'linear_six_parameter_projected_CV_SNR_reference_covariance':baseline_proj_ref,
          'raw_CV_SNR_candidate_covariance':baseline_raw_cand,
          'note':'projected value is a local linear nuisance estimate; any promising point still requires an actual nonlinear CLASS refit'
      },
      'nuisance_basis_rank_candidate_covariance':len(qs_c),
      'nuisance_basis_rank_reference_covariance':len(qs_r),
      'nuisance_basis_independence_candidate_covariance':bdiag_c,
      'nuisance_basis_independence_reference_covariance':bdiag_r,
      'gates':{'quadrature':bath_ok,'tangent_three_point_plateau':tangent_ok,'nuisance_rank_both_metrics':rank_ok},
      'scope':'unlensed full-sky CV TT/EE/TE ell=30..2500; fixed-parameter baseline plus local six-parameter projection; no real-data likelihood'
    }
    Path(z.json_out).write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2))
    if not numerical_ok: raise SystemExit(2)

if __name__=='__main__': main()
