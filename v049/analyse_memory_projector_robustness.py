#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math, numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
PARAMS=list(a.PARAMS)
LOCKED_MARG=0.1364941527698679


def whiten(v,W):
    v=np.asarray(v,float); out=[]
    for i,M in enumerate(W):
        L=np.linalg.cholesky(np.asarray(M,float))
        out.extend(L.T@v[3*i:3*i+3])
    return np.asarray(out)


def build_subspace(D):
    A=np.column_stack([D[p]/np.linalg.norm(D[p]) for p in PARAMS])
    U,s,Vt=np.linalg.svd(A,full_matrices=False)
    rank=int(np.sum(s>s[0]*1e-8))
    return U[:,:rank],s,Vt,rank,float(s[0]/s[-1])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir')
    ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir)
    tag='kb0p0665_tau10'
    fbase=out/f'v039_{tag}_base__cl.dat'
    fp=out/f'v039_{tag}_l10_p__cl.dat'; fm=out/f'v039_{tag}_l10_m__cl.dat'
    nuis={}
    for p in PARAMS:
        nuis[(p,'m2')]=out/f'v046_kb0p0665_tau10_p0_nuis_{p}_m2__cl.dat'
        nuis[(p,'m1')]=out/f'v046_kb0p0665_tau10_p0_nuis_{p}_m1__cl.dat'
        nuis[(p,'p1')]=out/f'v046_kb0p0665_tau10_p0_nuis_{p}_p1__cl.dat'
        nuis[(p,'p2')]=out/f'v046_kb0p0665_tau10_p0_nuis_{p}_p2__cl.dat'
    files=[fbase,fp,fm]+list(nuis.values())
    maps={str(p):a.load_cl(p) for p in files}
    ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    base=maps[str(fbase)]; W=a.invcov(ells,base)

    s=a.vec(ells,maps[str(fp)],maps[str(fm)],20.0)
    ws=whiten(s,W); raw=float(np.linalg.norm(ws))

    D2={}; D5={}
    for p in PARAMS:
        h=a.delta(p)
        fm2=maps[str(nuis[(p,'m2')])]; fm1=maps[str(nuis[(p,'m1')])]
        fp1=maps[str(nuis[(p,'p1')])]; fp2=maps[str(nuis[(p,'p2')])]
        d2=a.vec(ells,fp1,fm1,2*h)
        vp2=np.asarray(a.vec(ells,fp2,base,1.0)); vp1=np.asarray(a.vec(ells,fp1,base,1.0))
        vm1=np.asarray(a.vec(ells,fm1,base,1.0)); vm2=np.asarray(a.vec(ells,fm2,base,1.0))
        d5=(-vp2+8*vp1-8*vm1+vm2)/(12*h)
        D2[p]=whiten(d2,W); D5[p]=whiten(d5,W)

    Q2,s2,Vt2,r2,c2=build_subspace(D2); Q5,s5,Vt5,r5,c5=build_subspace(D5)
    rmem2=ws-Q2@(Q2.T@ws); rmem5=ws-Q5@(Q5.T@ws)
    marg2=float(np.linalg.norm(rmem2)); marg5=float(np.linalg.norm(rmem5))
    rel25=abs(marg5-marg2)/max(marg5,1e-300)
    rel_locked=abs(marg5-LOCKED_MARG)/LOCKED_MARG

    cs=np.clip(np.linalg.svd(Q2.T@Q5,compute_uv=False),-1,1)
    ang=np.arccos(cs)
    L,_,Rt=np.linalg.svd(Q2.T@Q5,full_matrices=False)
    iw=int(np.argmax(np.sin(ang)))
    weak2=Q2@L[:,iw]; weak5=Q5@Rt.T[:,iw]
    if np.dot(weak2,weak5)<0: weak5=-weak5
    ov2=float(abs(np.dot(ws,weak2))/max(raw,1e-300))
    ov5=float(abs(np.dot(ws,weak5))/max(raw,1e-300))

    gates={
      'rank_6_both':bool(r2==6 and r5==6),
      'condition_both':bool(math.isfinite(c2) and math.isfinite(c5) and max(c2,c5)<1e8),
      'memory_D2_vs_D5_within_5pct':bool(rel25<0.05),
      'fivepoint_vs_locked_reference_within_5pct':bool(rel_locked<0.05)
    }
    res={
      'classification':'V049_MEMORY_PROJECTOR_ROBUSTNESS_PASS' if all(gates.values()) else 'V049_MEMORY_PROJECTOR_ROBUSTNESS_FOLLOWUP',
      'KB':0.0665,'tauH0':10.0,'selected_lambda':10,
      'raw_memory_CV_SNR_per_unit_eta':raw,
      'D2_marginalized_CV_SNR_per_unit_eta':marg2,
      'D5_marginalized_CV_SNR_per_unit_eta':marg5,
      'D2_retained_fraction':marg2/max(raw,1e-300),
      'D5_retained_fraction':marg5/max(raw,1e-300),
      'relative_difference_D2_vs_D5':rel25,
      'locked_reference_marginalized_CV_SNR_per_unit_eta':LOCKED_MARG,
      'relative_difference_D5_vs_locked_reference':rel_locked,
      'principal_angles_deg':(ang*180/np.pi).tolist(),
      'max_sin_principal_angle':float(np.max(np.sin(ang))),
      'memory_fractional_overlap_with_worst_principal_direction_D2':ov2,
      'memory_fractional_overlap_with_worst_principal_direction_D5':ov5,
      'central_singular_values':s2.tolist(),'fivepoint_singular_values':s5.tolist(),
      'central_condition':c2,'fivepoint_condition':c5,'gates':gates,
      'scope':'unlensed full-sky CV TT/EE/TE ell=30..2500 at locked KB=0.0665, tauH0=10, strict-accuracy CLASS, fixed refitted cosmology',
      'purpose':'pre-locked test of whether the memory conclusion is stable to the D2 versus D5 nuisance projector after v0.48 isolated the weak tau_reio-lnA_s degeneracy'
    }
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)

if __name__=='__main__': main()
