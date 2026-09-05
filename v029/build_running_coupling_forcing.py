#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v022build',ROOT/'v022'/'build_offline_forcing.py')
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
POINTS=[('q0',0.0),('q025',0.25),('q05',0.5),('q075',0.75),('q1',1.0)]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('trace'); ap.add_argument('--out-dir',default='results'); ap.add_argument('--KB',type=float,default=0.1)
    ap.add_argument('--control-order',type=int,default=512); ap.add_argument('--primary-order',type=int,default=1024); ap.add_argument('--summary',required=True)
    a=ap.parse_args(); out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); histories=b.read_trace(a.trace)
    C={tag:[] for tag,_ in POINTS}; P={tag:[] for tag,_ in POINTS}; rowsC={tag:[] for tag,_ in POINTS}; rowsP={tag:[] for tag,_ in POINTS}
    for k in sorted(histories):
        seq=histories[k]; ct=np.array([r[0] for r in seq]); aa=np.array([r[1] for r in seq]); H=np.array([r[2] for r in seq]); chi=np.array([r[3] for r in seq]); Q=np.array([r[4] for r in seq]); N=np.log(aa); x=chi/aa
        yc=b.simulate_response(N,H,x,10.0,a.control_order); yp=b.simulate_response(N,H,x,10.0,a.primary_order)
        fc0=-0.5*aa*aa*Q*yc/a.KB; fp0=-0.5*aa*aa*Q*yp/a.KB
        for tag,q in POINTS:
            g=np.power(H,q); fc=fc0*g; fp=fp0*g
            C[tag].extend(fc.tolist()); P[tag].extend(fp.tolist()); rowsC[tag].extend((k,t,f) for t,f in zip(ct,fc)); rowsP[tag].extend((k,t,f) for t,f in zip(ct,fp))
    n0=max(float(np.linalg.norm(np.asarray(P['q0'],float))),1e-300)
    summary={'classification':'V029_EXPANSION_RUNNING_COUPLING_DIAGNOSTIC','definition':'eta_eff(a)=eta0*(H/H0)^q multiplying the validated tauH0=10 memory feedback tangent','covariant_note':'diagnostic FLRW form; a final theory would require a covariant completion, e.g. dependence on the aether expansion scalar','points':{},'k_histories':len(histories)}
    for tag,q in POINTS:
        rel,cos=b.rel_cos(C[tag],P[tag]); nq=float(np.linalg.norm(np.asarray(P[tag],float))); ratio=nq/n0; scale=max(1.0,ratio)
        for path,rows in [(out/f'v029_{tag}_force_control.dat',rowsC[tag]),(out/f'v029_{tag}_force.dat',rowsP[tag])]:
            with path.open('w') as f:
                for k,t,z in rows: f.write(f'{k:.17g} {t:.17g} {z/scale:.17g}\n')
        summary['points'][tag]={'q':q,'relative_L2_control_vs_primary':rel,'cosine':cos,'quadrature_gate':bool(rel<0.01 and cos>0.9999),
          'physical_force_L2_ratio_to_q0':ratio,'numerical_force_divisor':scale,'physical_tangent_rescale':scale,'samples':len(rowsP[tag])}
        print(tag,q,rel,cos,ratio,scale,flush=True)
    summary['all_quadrature_gate']=all(v['quadrature_gate'] for v in summary['points'].values()); Path(a.summary).write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
    if not summary['all_quadrature_gate']: raise SystemExit(2)
if __name__=='__main__': main()
