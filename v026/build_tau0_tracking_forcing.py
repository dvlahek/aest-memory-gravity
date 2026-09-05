#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v025build',ROOT/'v025'/'build_tracking_forcing.py')
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
b=v.b

POINTS=[
 ('p05_t01',0.5,0.1),('p05_t1',0.5,1.0),('p05_t10',0.5,10.0),('p05_t100',0.5,100.0),
 ('p1_t01',1.0,0.1),('p1_t1',1.0,1.0),('p1_t10',1.0,10.0),('p1_t100',1.0,100.0),
]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('trace'); ap.add_argument('--out-dir',default='results')
    ap.add_argument('--KB',type=float,default=0.1); ap.add_argument('--control-order',type=int,default=512)
    ap.add_argument('--primary-order',type=int,default=1024); ap.add_argument('--summary',default='results/v026_forcing_summary.json')
    a=ap.parse_args(); out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); histories=b.read_trace(a.trace)
    summary={'classification':'V026_TAU0_TRACKING_POSITIVE_DRUDE','KB':a.KB,'control_order':a.control_order,
      'primary_order':a.primary_order,'k_histories':len(histories),'definition':'tau_eff H0 = tau0H0*(H/H0)^(-p)',
      'spectral_scope':'positive tan-theta Drude weights at every background time; total Drude normalization fixed','points':{}}
    for tag,p,tau0 in POINTS:
        allc=[]; allp=[]; rcrows=[]; rprows=[]
        for k in sorted(histories):
            seq=histories[k]; ct=np.array([r[0] for r in seq]); aa=np.array([r[1] for r in seq]); H=np.array([r[2] for r in seq])
            chi=np.array([r[3] for r in seq]); Q=np.array([r[4] for r in seq]); N=np.log(aa); x=chi/aa
            yc=v.simulate_tracking(N,H,x,tau0,p,a.control_order); yp=v.simulate_tracking(N,H,x,tau0,p,a.primary_order)
            fc=-0.5*aa*aa*Q*yc/a.KB; fp=-0.5*aa*aa*Q*yp/a.KB
            allc.extend(fc.tolist()); allp.extend(fp.tolist())
            rcrows.extend((k,t,f) for t,f in zip(ct,fc)); rprows.extend((k,t,f) for t,f in zip(ct,fp))
        rel,cos=b.rel_cos(allc,allp)
        for path,rows in [(out/f'v026_{tag}_force_control.dat',rcrows),(out/f'v026_{tag}_force.dat',rprows)]:
            with path.open('w') as f:
                for k,t,z in rows: f.write(f'{k:.17g} {t:.17g} {z:.17g}\n')
        summary['points'][tag]={'p':p,'tau0H0':tau0,'global_relative_L2_control_vs_primary':rel,'global_cosine':cos,
          'gate':bool(rel<0.01 and cos>0.9999),'samples':len(rprows)}
        print(tag,p,tau0,rel,cos,len(rprows),flush=True)
    summary['all_quadrature_gate']=all(x['gate'] for x in summary['points'].values())
    Path(a.summary).write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
    if not summary['all_quadrature_gate']: raise SystemExit(2)

if __name__=='__main__': main()
