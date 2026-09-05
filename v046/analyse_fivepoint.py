#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math, numpy as np
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
PARAMS=list(a.PARAMS)

def whiten(v,W):
    v=np.asarray(v,float); out=[]
    for i,M in enumerate(W):
        L=np.linalg.cholesky(np.asarray(M,float)); out.extend(L.T@v[3*i:3*i+3])
    return np.asarray(out)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output_dir'); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir); tag='kb0p0665_tau10_p0'
    paths=[out/f'v046_{tag}_base__cl.dat']
    for p in PARAMS:
        for s in ('m2','m1','p1','p2'): paths.append(out/f'v046_{tag}_nuis_{p}_{s}__cl.dat')
    maps={str(p):a.load_cl(p) for p in paths}; ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    base=maps[str(out/f'v046_{tag}_base__cl.dat')]; W=a.invcov(ells,base)
    per={}; D2={}; D5={}
    for p in PARAMS:
        h=a.delta(p)
        fm2=maps[str(out/f'v046_{tag}_nuis_{p}_m2__cl.dat')]; fm1=maps[str(out/f'v046_{tag}_nuis_{p}_m1__cl.dat')]
        fp1=maps[str(out/f'v046_{tag}_nuis_{p}_p1__cl.dat')]; fp2=maps[str(out/f'v046_{tag}_nuis_{p}_p2__cl.dat')]
        d2=a.vec(ells,fp1,fm1,2*h)
        # a.vec returns flattened difference/denominator. Build fourth-order stencil componentwise.
        vp2=np.asarray(a.vec(ells,fp2,base,1.0)); vp1=np.asarray(a.vec(ells,fp1,base,1.0))
        vm1=np.asarray(a.vec(ells,fm1,base,1.0)); vm2=np.asarray(a.vec(ells,fm2,base,1.0))
        d5=(-vp2+8*vp1-8*vm1+vm2)/(12*h)
        w2=whiten(d2,W); w5=whiten(d5,W); n2=np.linalg.norm(w2); n5=np.linalg.norm(w5)
        cos=float(np.dot(w2,w5)/(n2*n5)); rel=float(np.linalg.norm(w5-w2)/n5)
        D2[p]=w2; D5[p]=w5
        per[p]={'central_CV_norm':float(n2),'fivepoint_CV_norm':float(n5),'cosine':cos,'relative_L2':rel,
                'stable':bool(cos>0.999 and rel<0.05)}
    def subspace(D):
        A=np.column_stack([D[p]/np.linalg.norm(D[p]) for p in PARAMS]); U,s,_=np.linalg.svd(A,full_matrices=False)
        rank=int(np.sum(s>s[0]*1e-8)); return U[:,:rank],s,rank,float(s[0]/s[-1])
    Q2,s2,r2,c2=subspace(D2); Q5,s5,r5,c5=subspace(D5)
    cs=np.clip(np.linalg.svd(Q2.T@Q5,compute_uv=False),-1,1); ang=np.arccos(cs); maxsin=float(np.max(np.sin(ang)))
    gates={'rank_6_both':r2==6 and r5==6,'condition_both':math.isfinite(c2) and math.isfinite(c5) and max(c2,c5)<1e8,
           'all_derivatives_two_vs_five_stable':all(v['stable'] for v in per.values()),'projector_two_vs_five_stable':maxsin<0.05}
    res={'classification':'V046_FIVEPOINT_CERTIFICATION_PASS' if all(gates.values()) else 'V046_FIVEPOINT_CERTIFICATION_FOLLOWUP',
         'KB':0.0665,'tauH0':10.0,'per_parameter':per,'central_singular_values':s2.tolist(),'fivepoint_singular_values':s5.tolist(),
         'central_condition':c2,'fivepoint_condition':c5,'principal_angles_deg':(ang*180/np.pi).tolist(),
         'max_sin_principal_angle':maxsin,'gates':gates,
         'method':'locked covariance-whitened comparison of symmetric two-point D(h) and fourth-order five-point D5(h)=[-f(+2h)+8f(+h)-8f(-h)+f(-2h)]/(12h)',
         'purpose':'test whether the v0.45 small-step failure is cancellation/noise rather than a physical nuisance-subspace instability'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)
if __name__=='__main__': main()
