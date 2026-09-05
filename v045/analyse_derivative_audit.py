#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math, numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

SCALES=(0.25,0.5,1.0,1.5,2.0)
PARAMS=list(a.PARAMS)

def tag_scale(x): return ('%.6g'%x).replace('.','p').replace('-','m')

def whiten_vec(v,W):
    out=[]; v=np.asarray(v,dtype=float)
    for i,M in enumerate(W):
        L=np.linalg.cholesky(np.asarray(M,dtype=float))
        out.extend(L.T @ v[3*i:3*i+3])
    return np.asarray(out,dtype=float)

def cosine(x,y):
    nx=np.linalg.norm(x); ny=np.linalg.norm(y)
    return float(np.dot(x,y)/(nx*ny)) if nx>0 and ny>0 else float('nan')

def rel_l2(x,y):
    return float(np.linalg.norm(x-y)/max(np.linalg.norm(y),1e-300))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output_dir'); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir)
    basefile=out/'v045_kb0p0665_tau10_p0_s1_base__cl.dat'
    files=[basefile]
    for sc in SCALES:
        t=f'kb0p0665_tau10_p0_s{tag_scale(sc)}'
        for p in PARAMS:
            files += [out/f'v045_{t}_nuis_{p}_p__cl.dat',out/f'v045_{t}_nuis_{p}_m__cl.dat']
    maps={str(p):a.load_cl(p) for p in files}
    ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    base=maps[str(basefile)]; W=a.invcov(ells,base)

    per={}; offenders=[]
    for p in PARAMS:
        D={}; N={}
        for sc in SCALES:
            t=f'kb0p0665_tau10_p0_s{tag_scale(sc)}'
            pp=maps[str(out/f'v045_{t}_nuis_{p}_p__cl.dat')]
            pm=maps[str(out/f'v045_{t}_nuis_{p}_m__cl.dat')]
            d=a.vec(ells,pp,pm,2.0*sc*a.delta(p)); dw=whiten_vec(d,W)
            D[sc]=dw; N[sc]=float(np.linalg.norm(dw))
        pairs={}
        for lo,hi in [(0.25,0.5),(0.5,1.0),(1.0,1.5),(1.0,2.0)]:
            pairs[f'{lo:g}_vs_{hi:g}']={'cosine':cosine(D[lo],D[hi]),'relative_L2':rel_l2(D[lo],D[hi]),
                                       'norm_ratio':N[lo]/max(N[hi],1e-300)}
        # Central differences are nominally O(h^2): compare fine-grid differences for Richardson trend.
        e10=np.linalg.norm(D[1.0]-D[0.5]); e05=np.linalg.norm(D[0.5]-D[0.25])
        rich=float(e10/max(e05,1e-300))
        fine_cos=pairs['0.25_vs_0.5']['cosine']; fine_rel=pairs['0.25_vs_0.5']['relative_L2']
        nominal_cos=pairs['0.5_vs_1']['cosine']; nominal_rel=pairs['0.5_vs_1']['relative_L2']
        stable=bool(fine_cos>0.999 and fine_rel<0.05 and nominal_cos>0.999 and nominal_rel<0.05)
        if not stable: offenders.append(p)
        per[p]={'CV_norm_by_scale':{str(k):v for k,v in N.items()},'pairwise':pairs,
                'richardson_difference_ratio_e1_to_ehalf':rich,
                'expected_ratio_for_Oh2_approximately':4.0,
                'fine_step_stable':stable}

    gates={'all_parameters_fine_step_stable':len(offenders)==0}
    res={'classification':'V045_DERIVATIVE_AUDIT_PASS' if all(gates.values()) else 'V045_DERIVATIVE_AUDIT_FOLLOWUP',
         'KB':0.0665,'tauH0':10.0,'derivative_step_scales':list(SCALES),'parameters':PARAMS,
         'per_parameter':per,'offending_parameters':offenders,'gates':gates,
         'criterion':'for both 0.25-vs-0.5 and 0.5-vs-1.0 scales require cosine > 0.999 and relative L2 < 0.05',
         'purpose':'localize nuisance finite-difference derivative instability seen in v0.43-v0.44; no parameter retuning and no memory projection used for the pass/fail decision'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)
if __name__=='__main__': main()
