#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, numpy as np
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v022build',ROOT/'v022'/'build_offline_forcing.py')
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
TAUS=[('t0001',0.001),('t0003',0.003),('t001',0.01),('t003',0.03),('t01',0.1),('t03',0.3),('t1',1.0),('t3',3.0),('t10',10.0)]

def force_histories(histories,T,KB,n):
    allf=[]; rows=[]
    for k in sorted(histories):
        seq=histories[k]; ct=np.array([r[0] for r in seq]); aa=np.array([r[1] for r in seq]); H=np.array([r[2] for r in seq]); chi=np.array([r[3] for r in seq]); Q=np.array([r[4] for r in seq]); N=np.log(aa); x=chi/aa
        y=b.simulate_response(N,H,x,T,n); f=-0.5*aa*aa*Q*y/KB; allf.extend(f.tolist()); rows.extend((k,t,z) for t,z in zip(ct,f))
    return allf,rows

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('cosh_trace'); ap.add_argument('exp_trace'); ap.add_argument('--out-dir',default='results'); ap.add_argument('--control-order',type=int,default=512); ap.add_argument('--primary-order',type=int,default=1024); ap.add_argument('--summary',required=True)
    a=ap.parse_args(); out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); hc=b.read_trace(a.cosh_trace); he=b.read_trace(a.exp_trace)
    exp_p,_=force_histories(he,1.0,0.1,a.primary_order); exp_norm=max(float(np.linalg.norm(np.asarray(exp_p,float))),1e-300)
    summary={'classification':'V030_COSH_ACCEPTED_GRID_POSITIVE_DRUDE','model':'Cosh','KB':0.5,'reference_exp_tau1_force_L2':exp_norm,'control_order':a.control_order,'primary_order':a.primary_order,'points':{}}
    for tag,T in TAUS:
        c,rc=force_histories(hc,T,0.5,a.control_order); p,rp=force_histories(hc,T,0.5,a.primary_order); rel,cos=b.rel_cos(c,p); normp=float(np.linalg.norm(np.asarray(p,float))); ratio=normp/exp_norm; scale=max(1.0,ratio)
        for path,rows in [(out/f'v030_{tag}_force_control.dat',rc),(out/f'v030_{tag}_force.dat',rp)]:
            with path.open('w') as f:
                for k,t,z in rows: f.write(f'{k:.17g} {t:.17g} {z/scale:.17g}\n')
        summary['points'][tag]={'tauH0':T,'relative_L2_control_vs_primary':rel,'cosine':cos,'quadrature_gate':bool(rel<0.01 and cos>0.9999),'physical_force_L2_ratio_to_exp_tau1':ratio,'numerical_force_divisor':scale,'physical_tangent_rescale':scale,'samples':len(rp)}
        print(tag,T,rel,cos,ratio,scale,flush=True)
    summary['all_quadrature_gate']=all(v['quadrature_gate'] for v in summary['points'].values()); Path(a.summary).write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
    if not summary['all_quadrature_gate']: raise SystemExit(2)
if __name__=='__main__': main()
