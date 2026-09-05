#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, numpy as np
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v022build',ROOT/'v022'/'build_offline_forcing.py')
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('trace'); ap.add_argument('--KB',type=float,required=True); ap.add_argument('--out-prefix',required=True)
    ap.add_argument('--control-order',type=int,default=512); ap.add_argument('--primary-order',type=int,default=1024); ap.add_argument('--summary',required=True)
    a=ap.parse_args(); histories=b.read_trace(a.trace); allc=[]; allp=[]; rcrows=[]; rprows=[]
    for k in sorted(histories):
        seq=histories[k]; ct=np.array([r[0] for r in seq]); aa=np.array([r[1] for r in seq]); H=np.array([r[2] for r in seq]); chi=np.array([r[3] for r in seq]); Q=np.array([r[4] for r in seq]); N=np.log(aa); x=chi/aa
        yc=b.simulate_response(N,H,x,10.0,a.control_order); yp=b.simulate_response(N,H,x,10.0,a.primary_order)
        fc=-0.5*aa*aa*Q*yc/a.KB; fp=-0.5*aa*aa*Q*yp/a.KB
        allc.extend(fc.tolist()); allp.extend(fp.tolist()); rcrows.extend((k,t,f) for t,f in zip(ct,fc)); rprows.extend((k,t,f) for t,f in zip(ct,fp))
    rel,cos=b.rel_cos(allc,allp); pref=Path(a.out_prefix)
    for path,rows in [(Path(str(pref)+'_force_control.dat'),rcrows),(Path(str(pref)+'_force.dat'),rprows)]:
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('w') as f:
            for k,t,z in rows: f.write(f'{k:.17g} {t:.17g} {z:.17g}\n')
    res={'classification':'V027_KB_TAU10_POSITIVE_DRUDE','KB':a.KB,'tauH0':10.0,'control_order':a.control_order,'primary_order':a.primary_order,
      'relative_L2_control_vs_primary':rel,'cosine':cos,'gate':bool(rel<0.01 and cos>0.9999),'samples':len(rprows),'k_histories':len(histories)}
    Path(a.summary).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not res['gate']: raise SystemExit(2)
if __name__=='__main__': main()
