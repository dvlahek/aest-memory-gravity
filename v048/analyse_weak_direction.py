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
        L=np.linalg.cholesky(np.asarray(M,float))
        out.extend(L.T@v[3*i:3*i+3])
    return np.asarray(out)


def projector(Q):
    return Q@Q.T


def subspace(D):
    A=np.column_stack([D[p]/np.linalg.norm(D[p]) for p in PARAMS])
    U,s,Vt=np.linalg.svd(A,full_matrices=False)
    return A,U,s,Vt,float(s[0]/s[-1])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir')
    ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir); tag='kb0p0665_tau10_p0'

    paths=[out/f'v046_{tag}_base__cl.dat']
    for p in PARAMS:
        for s in ('m2','m1','p1','p2'):
            paths.append(out/f'v046_{tag}_nuis_{p}_{s}__cl.dat')
    maps={str(p):a.load_cl(p) for p in paths}
    ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    base=maps[str(out/f'v046_{tag}_base__cl.dat')]
    W=a.invcov(ells,base)

    D2={}; D5={}
    for p in PARAMS:
        h=a.delta(p)
        fm2=maps[str(out/f'v046_{tag}_nuis_{p}_m2__cl.dat')]
        fm1=maps[str(out/f'v046_{tag}_nuis_{p}_m1__cl.dat')]
        fp1=maps[str(out/f'v046_{tag}_nuis_{p}_p1__cl.dat')]
        fp2=maps[str(out/f'v046_{tag}_nuis_{p}_p2__cl.dat')]
        d2=a.vec(ells,fp1,fm1,2*h)
        vp2=np.asarray(a.vec(ells,fp2,base,1.0)); vp1=np.asarray(a.vec(ells,fp1,base,1.0))
        vm1=np.asarray(a.vec(ells,fm1,base,1.0)); vm2=np.asarray(a.vec(ells,fm2,base,1.0))
        d5=(-vp2+8*vp1-8*vm1+vm2)/(12*h)
        D2[p]=whiten(d2,W); D5[p]=whiten(d5,W)

    A2,U2,s2,Vt2,c2=subspace(D2); A5,U5,s5,Vt5,c5=subspace(D5)
    M=U2.T@U5
    L,cs,Rt=np.linalg.svd(M,full_matrices=False)
    cs=np.clip(cs,-1,1); angles=np.arccos(cs); sins=np.sin(angles)
    iw=int(np.argmax(sins))
    weak2=U2@L[:,iw]; weak5=U5@Rt.T[:,iw]
    if np.dot(weak2,weak5)<0: weak5=-weak5

    # Parameter mixtures of the weakest singular directions of each normalized design.
    mix2=Vt2[-1,:]; mix5=Vt5[-1,:]
    if np.dot(mix2,mix5)<0: mix5=-mix5
    param_mix2={p:float(mix2[i]) for i,p in enumerate(PARAMS)}
    param_mix5={p:float(mix5[i]) for i,p in enumerate(PARAMS)}

    # Which individual derivative changes feed the discrepant principal plane?
    contribution={}
    for p in PARAMS:
        x2=D2[p]/np.linalg.norm(D2[p]); x5=D5[p]/np.linalg.norm(D5[p])
        dx=x5-x2
        contribution[p]={
            'normalized_derivative_change':float(np.linalg.norm(dx)),
            'overlap_change_with_weak2':float(abs(np.dot(dx,weak2))),
            'overlap_change_with_weak5':float(abs(np.dot(dx,weak5)))
        }

    res={
      'classification':'V048_WEAK_DIRECTION_DECOMPOSED',
      'KB':0.0665,'tauH0':10.0,'parameters':PARAMS,
      'central_singular_values':s2.tolist(),'fivepoint_singular_values':s5.tolist(),
      'central_condition':c2,'fivepoint_condition':c5,
      'principal_angles_deg':(angles*180/np.pi).tolist(),
      'principal_angle_sines':sins.tolist(),
      'worst_principal_index':iw,
      'worst_principal_angle_deg':float(angles[iw]*180/np.pi),
      'worst_principal_sine':float(sins[iw]),
      'weakest_design_parameter_mixture_central':param_mix2,
      'weakest_design_parameter_mixture_fivepoint':param_mix5,
      'weakest_design_mixture_cosine':float(np.dot(mix2,mix5)/(np.linalg.norm(mix2)*np.linalg.norm(mix5))),
      'per_parameter_change_projection':contribution,
      'gates':{
        'rank_6_both':bool(len(s2)==6 and len(s5)==6 and s2[-1]>s2[0]*1e-8 and s5[-1]>s5[0]*1e-8),
        'condition_both':bool(math.isfinite(c2) and math.isfinite(c5) and max(c2,c5)<1e8)
      },
      'purpose':'isolate the weak combined nuisance direction responsible for the v0.46/v0.47 projector discrepancy without changing physics, derivative steps, covariance, stencil, or gates',
      'note':'This run diagnoses nuisance geometry only. Memory overlap with this direction is intentionally deferred to a separately locked projection run after the weak direction is identified.'
    }
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))

if __name__=='__main__': main()
