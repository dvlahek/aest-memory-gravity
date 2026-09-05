#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math, numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
LAM=[1,3,10,30,100,300,1000]
REF_MARG=0.1364941527698679

def inner(x,y,W):
    return float(np.dot(x, W @ y))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir'); ap.add_argument('--tag',required=True); ap.add_argument('--scale',type=float,required=True)
    ap.add_argument('--force-control',required=True); ap.add_argument('--force-primary',required=True); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir)
    files={'base':out/f'v043_{z.tag}_base__cl.dat','ref':out/f'v043_{z.tag}_ref__cl.dat'}
    for L in LAM:
        files[f'p{L}']=out/f'v043_{z.tag}_l{L}_p__cl.dat'; files[f'm{L}']=out/f'v043_{z.tag}_l{L}_m__cl.dat'
    for q in a.PARAMS:
        files[f'nuis_{q}_p']=out/f'v043_{z.tag}_nuis_{q}_p__cl.dat'; files[f'nuis_{q}_m']=out/f'v043_{z.tag}_nuis_{q}_m__cl.dat'
    maps={k:a.load_cl(v) for k,v in files.items()}
    ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    W=a.invcov(ells,maps['base'])
    S={L:a.vec(ells,maps[f'p{L}'],maps[f'm{L}'],2.0*L) for L in LAM}
    chosen=10; s=S[chosen]
    deriv={q:a.vec(ells,maps[f'nuis_{q}_p'],maps[f'nuis_{q}_m'],2.0*z.scale*a.delta(q)) for q in a.PARAMS}
    names=list(a.PARAMS)
    norms=np.array([max(a.wnorm(deriv[q],W),1e-300) for q in names])
    corr=np.empty((len(names),len(names)))
    for i,qi in enumerate(names):
        for j,qj in enumerate(names): corr[i,j]=inner(deriv[qi],deriv[qj],W)/(norms[i]*norms[j])
    eig=np.linalg.eigvalsh(corr)
    svals=np.linalg.svd(corr,compute_uv=False)
    cond=float(svals[0]/svals[-1])
    qs,bdiag=a.orthonormalize([(q,deriv[q]) for q in names],W)
    mem=a.project(s,qs,W); raw=a.wnorm(s,W); marg=a.wnorm(mem,W); retained=marg/max(raw,1e-300)
    fc=a.force_control(z.force_control,z.force_primary)
    rel_ref=abs(marg-REF_MARG)/REF_MARG
    rank_ok=len(qs)==6
    eig_ok=float(eig[0])>1e-6
    cond_ok=math.isfinite(cond) and cond<1e8
    step_ok=rel_ref<0.05
    quad_ok=fc['relative_L2']<0.01 and fc['cosine']>0.9999
    gates={'quadrature':quad_ok,'nuisance_rank_6':rank_ok,'normalized_gram_min_eigenvalue':eig_ok,'normalized_gram_condition':cond_ok,'memory_step_stability_vs_locked_reference':step_ok}
    res={'classification':'V043_NUISANCE_CONDITIONING_PASS' if all(gates.values()) else 'V043_NUISANCE_CONDITIONING_FOLLOWUP',
         'KB':0.0665,'tauH0':10.0,'p':0.0,'derivative_step_scale':z.scale,'selected_lambda':chosen,
         'nuisance_parameters':names,'normalized_derivative_correlation_matrix':corr.tolist(),'normalized_gram_eigenvalues':eig.tolist(),
         'normalized_gram_singular_values':svals.tolist(),'normalized_gram_condition_number':cond,'derivative_CV_norms':dict(zip(names,norms.tolist())),
         'orthogonalization_independence':bdiag,'nuisance_rank':len(qs),'memory_raw_CV_SNR_per_eta':raw,
         'memory_marginalized_CV_SNR_per_eta':marg,'memory_retained_fraction':retained,
         'locked_reference_marginalized_CV_SNR_per_eta':REF_MARG,'relative_difference_from_locked_reference':rel_ref,
         'force_quadrature_control':fc,'gates':gates,
         'purpose':'certify nuisance-space conditioning and finite-difference-step stability for the frozen AeST memory fingerprint; no parameter retuning',
         'scope':'unlensed full-sky CV TT/EE/TE ell=30..2500; six nuisance directions; no real-data likelihood'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)
if __name__=='__main__': main()
