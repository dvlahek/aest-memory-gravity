#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math, numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

SCALES=(0.5,0.75,1.0,1.5,2.0)
PARAMS=list(a.PARAMS)
REF_SCALE=1.0
REF_MARG=0.1364941527698679

def tag_scale(x): return ('%.6g'%x).replace('.','p').replace('-','m')

def whiten_vec(v,W):
    out=[]
    v=np.asarray(v,dtype=float)
    for i,M in enumerate(W):
        M=np.asarray(M,dtype=float)
        L=np.linalg.cholesky(M)
        out.extend(L.T @ v[3*i:3*i+3])
    return np.asarray(out,dtype=float)

def normalized_design(deriv,W):
    cols=[]; norms={}
    for p in PARAMS:
        x=whiten_vec(deriv[p],W)
        n=float(np.linalg.norm(x)); norms[p]=n
        if not math.isfinite(n) or n<=0: raise RuntimeError(f'bad derivative norm for {p}: {n}')
        cols.append(x/n)
    A=np.column_stack(cols)
    U,s,Vt=np.linalg.svd(A,full_matrices=False)
    rank=int(np.sum(s > s[0]*1e-8))
    Q=U[:,:rank]
    cond=float(s[0]/s[-1]) if s[-1]>0 else math.inf
    return A,Q,s,rank,cond,norms

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir')
    ap.add_argument('--force-control',required=True)
    ap.add_argument('--force-primary',required=True)
    ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir)

    tags={s:f'kb0p0665_tau10_p0_s{tag_scale(s)}' for s in SCALES}
    ref_tag=tags[REF_SCALE]
    common_files=[out/f'v044_{ref_tag}_base__cl.dat',out/f'v044_{ref_tag}_l10_p__cl.dat',out/f'v044_{ref_tag}_l10_m__cl.dat']
    for s in SCALES:
        t=tags[s]
        for p in PARAMS:
            common_files += [out/f'v044_{t}_nuis_{p}_p__cl.dat',out/f'v044_{t}_nuis_{p}_m__cl.dat']
    maps={str(p):a.load_cl(p) for p in common_files}
    ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')

    base=maps[str(out/f'v044_{ref_tag}_base__cl.dat')]
    W=a.invcov(ells,base)
    sp=maps[str(out/f'v044_{ref_tag}_l10_p__cl.dat')]
    sm=maps[str(out/f'v044_{ref_tag}_l10_m__cl.dat')]
    s=a.vec(ells,sp,sm,20.0)
    sw=whiten_vec(s,W)
    raw=float(np.linalg.norm(sw))

    per={}; Qs={}
    for sc in SCALES:
        t=tags[sc]
        deriv={}
        for p in PARAMS:
            pp=maps[str(out/f'v044_{t}_nuis_{p}_p__cl.dat')]
            pm=maps[str(out/f'v044_{t}_nuis_{p}_m__cl.dat')]
            deriv[p]=a.vec(ells,pp,pm,2.0*sc*a.delta(p))
        A,Q,sv,rank,cond,norms=normalized_design(deriv,W)
        Qs[sc]=Q
        resid=sw-Q@(Q.T@sw)
        marg=float(np.linalg.norm(resid)); retained=marg/max(raw,1e-300)
        per[sc]={'rank':rank,'normalized_design_singular_values':sv.tolist(),
                 'normalized_design_condition_number':cond,'derivative_CV_norms':norms,
                 'memory_marginalized_CV_SNR_per_eta':marg,'memory_retained_fraction':retained,
                 'relative_difference_from_locked_reference':abs(marg-REF_MARG)/REF_MARG}

    Q0=Qs[REF_SCALE]
    for sc in SCALES:
        Q=Qs[sc]
        k=min(Q0.shape[1],Q.shape[1])
        cs=np.linalg.svd(Q0.T@Q,compute_uv=False)[:k]
        cs=np.clip(cs,-1.0,1.0)
        ang=np.arccos(cs)
        sinang=np.sin(ang)
        per[sc]['principal_angles_deg_vs_scale1']=(ang*180.0/np.pi).tolist()
        per[sc]['max_sin_principal_angle_vs_scale1']=float(np.max(sinang)) if len(sinang) else math.inf

    vals=np.array([per[sc]['memory_marginalized_CV_SNR_per_eta'] for sc in SCALES])
    rel_spread=float((vals.max()-vals.min())/vals[np.where(np.array(SCALES)==REF_SCALE)[0][0]])
    max_angle=max(per[sc]['max_sin_principal_angle_vs_scale1'] for sc in SCALES)
    max_cond=max(per[sc]['normalized_design_condition_number'] for sc in SCALES)
    min_rank=min(per[sc]['rank'] for sc in SCALES)
    fc=a.force_control(z.force_control,z.force_primary)

    gates={
      'quadrature':fc['relative_L2']<0.01 and fc['cosine']>0.9999,
      'rank_6_all_scales':min_rank==6,
      'normalized_design_condition_all_scales':math.isfinite(max_cond) and max_cond<1e8,
      'projector_principal_angle_stability':max_angle<0.05,
      'marginalized_memory_spread':rel_spread<0.05,
    }
    res={'classification':'V044_PROJECTOR_STABILITY_PASS' if all(gates.values()) else 'V044_PROJECTOR_STABILITY_FOLLOWUP',
         'KB':0.0665,'tauH0':10.0,'p':0.0,'selected_lambda':10,'derivative_step_scales':list(SCALES),
         'reference_scale':REF_SCALE,'reference_locked_marginalized_CV_SNR_per_eta':REF_MARG,
         'memory_raw_CV_SNR_per_eta':raw,'per_scale':{str(k):v for k,v in per.items()},
         'marginalized_memory_relative_spread_across_scales':rel_spread,
         'max_sin_principal_angle_across_scales':max_angle,
         'max_normalized_design_condition_number':max_cond,
         'force_quadrature_control':fc,'gates':gates,
         'method':'whiten each TT/EE/TE ell block with the locked cosmic-variance inverse covariance, normalize the six nuisance derivative columns, form their SVD subspace, and project the fixed memory tangent with the orthogonal projector',
         'purpose':'test nuisance-subspace/projector stability independently of Gram-Schmidt basis ordering across pre-registered finite-difference scales; no model or cosmology retuning',
         'scope':'unlensed full-sky CV TT/EE/TE ell=30..2500; six nuisance directions; no real-data likelihood'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)

if __name__=='__main__': main()
