#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math, numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
PARAMS=list(a.PARAMS)
TAUS=[0.01,0.03,0.1,0.3,1.0,3.0,10.0,30.0,100.0]

def ptag(x): return ('%.6g'%x).replace('.','p').replace('-','m')
def whiten(v,W):
    out=[]
    for i,M in enumerate(W):
        L=np.linalg.cholesky(np.asarray(M,float)); out.extend(L.T@np.asarray(v,float)[3*i:3*i+3])
    return np.asarray(out)
def nuisance_subspace(D):
    A=np.column_stack([D[p]/np.linalg.norm(D[p]) for p in PARAMS])
    U,s,_=np.linalg.svd(A,full_matrices=False); rank=int(np.sum(s>s[0]*1e-8))
    return U[:,:rank],s,rank,float(s[0]/s[-1])
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output_dir'); ap.add_argument('--json-out',required=True); z=ap.parse_args(); out=Path(z.output_dir)
    base=out/'v039_kb0p0665_tau10_base__cl.dat'
    nuis={}
    for p in PARAMS:
        for s in ['m2','m1','p1','p2']: nuis[(p,s)]=out/f'v046_kb0p0665_tau10_p0_nuis_{p}_{s}__cl.dat'
    mem={t:(out/f'v039_kb0p0665_tau{ptag(t)}_l10_p__cl.dat',out/f'v039_kb0p0665_tau{ptag(t)}_l10_m__cl.dat') for t in TAUS}
    files=[base]+list(nuis.values())+[q for pair in mem.values() for q in pair]
    maps={str(p):a.load_cl(p) for p in files}; ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    b=maps[str(base)]; W=a.invcov(ells,b); D5={}
    for p in PARAMS:
        h=a.delta(p); fm2=maps[str(nuis[(p,'m2')])]; fm1=maps[str(nuis[(p,'m1')])]; fp1=maps[str(nuis[(p,'p1')])]; fp2=maps[str(nuis[(p,'p2')])]
        vp2=np.asarray(a.vec(ells,fp2,b,1.0)); vp1=np.asarray(a.vec(ells,fp1,b,1.0)); vm1=np.asarray(a.vec(ells,fm1,b,1.0)); vm2=np.asarray(a.vec(ells,fm2,b,1.0))
        D5[p]=whiten((-vp2+8*vp1-8*vm1+vm2)/(12*h),W)
    Q,sn,rank,cond=nuisance_subspace(D5)
    projected=[]; raw_norm=[]; proj_norm=[]
    for t in TAUS:
        fp,fm=mem[t]; v=whiten(a.vec(ells,maps[str(fp)],maps[str(fm)],20.0),W); r=v-Q@(Q.T@v)
        nr=float(np.linalg.norm(r)); raw_norm.append(float(np.linalg.norm(v))); proj_norm.append(nr)
        if not np.isfinite(nr) or nr<=1e-14: raise RuntimeError(f'degenerate projected template tau={t}: {nr}')
        projected.append(r/nr)
    X=np.column_stack(projected); U,sv,Vt=np.linalg.svd(X,full_matrices=False); power=sv**2; frac=power/power.sum(); cum=np.cumsum(frac)
    G=X.T@X; locked_i=TAUS.index(10.0); locked=X[:,locked_i]
    d1=float(np.linalg.norm(locked-U[:,:1]@(U[:,:1].T@locked))); d2=float(np.linalg.norm(locked-U[:,:2]@(U[:,:2].T@locked))); d3=float(np.linalg.norm(locked-U[:,:3]@(U[:,:3].T@locked)))
    p=frac[frac>0]; erank=float(np.exp(-np.sum(p*np.log(p))))
    gates={'nuisance_rank_6':rank==6,'nuisance_condition_lt_1e8':math.isfinite(cond) and cond<1e8,'first_2_modes_fraction_ge_0p90':float(cum[1])>=0.90,'first_3_modes_fraction_ge_0p95':float(cum[2])>=0.95}
    res={'classification':'V057_STRONG_DOMINANT_MEMORY_SUBSPACE_PASS' if all(gates.values()) else 'V057_DOMINANT_MEMORY_SUBSPACE_GATE_FAIL','tauH0_grid':TAUS,'singular_values':sv.tolist(),'explained_fraction':frac.tolist(),'cumulative_explained_fraction':cum.tolist(),'fraction_mode_1':float(frac[0]),'fraction_modes_1_2':float(cum[1]),'fraction_modes_1_3':float(cum[2]),'effective_rank_entropy':erank,'pairwise_projected_template_cosines':G.tolist(),'raw_CV_norm_per_eta':raw_norm,'projected_CV_norm_per_eta':proj_norm,'locked_tau10_distance_to_mode1':d1,'locked_tau10_distance_to_modes12':d2,'locked_tau10_distance_to_modes123':d3,'nuisance_D5_singular_values':sn.tolist(),'nuisance_rank':rank,'nuisance_condition':cond,'gates':gates,'scope':'pre-data unlensed full-sky CV TT/TE/EE ell=30..2500; unit-normalized projected shapes; frozen KB=0.0665 cosmology and D5 nuisance definition','anti_tuning':'Protocol frozen before v0.57 outputs. Failure is retained; no grid/metric/projection/normalization changes to recover dominance.'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)
if __name__=='__main__': main()
