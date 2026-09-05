#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('v022build', ROOT/'v022'/'build_offline_forcing.py')
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)

PVALS=[('p0',0.0),('p05',0.5),('p1',1.0)]

def simulate_tracking(N,H,x,tau0,p,n):
    r,weights=b.tan_gl_nodes(n)
    q=np.zeros(int(n)); v=np.zeros(int(n)); out=np.empty(len(N)); out[0]=x[0]
    for i in range(len(N)-1):
        dN=N[i+1]-N[i]
        if not (dN>0): out[i+1]=out[i]; continue
        Hm=math.sqrt(H[i]*H[i+1])
        h=Hm*tau0
        dt=dN/h
        # tau_eff=tau0*(H/H0)^(-p), so physical Omega=r/tau_eff and
        # Omega*tau0 = r*(H/H0)^p in xi=t/tau0 units.
        omega=r*(Hm**p)
        q,v=b._step_linear(q,v,omega,h,x[i],x[i+1],dt)
        out[i+1]=x[i+1]-float(np.dot(weights,q))
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('trace'); ap.add_argument('--out-dir',default='results')
    ap.add_argument('--tau0H0',type=float,default=1.0); ap.add_argument('--KB',type=float,default=0.1)
    ap.add_argument('--control-order',type=int,default=512); ap.add_argument('--primary-order',type=int,default=1024)
    ap.add_argument('--summary',default='results/v025_tracking_forcing_summary.json')
    a=ap.parse_args(); out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True)
    histories=b.read_trace(a.trace)
    summary={'classification':'V025_BACKGROUND_TRACKING_POSITIVE_DRUDE','tau0H0':a.tau0H0,'KB':a.KB,
             'control_order':a.control_order,'primary_order':a.primary_order,'k_histories':len(histories),
             'definition':'tau_eff(a) H0 = tau0H0 * (H/H0)^(-p)',
             'spectral_scope':'positive tan-theta Drude weights retained at every background time; this linear gate does not by itself establish the full nonstationary covariant energy accounting',
             'points':{}}
    for tag,p in PVALS:
        allc=[]; allp=[]; rcrows=[]; rprows=[]; per=[]
        for k in sorted(histories):
            seq=histories[k]
            ct=np.array([r[0] for r in seq]); aa=np.array([r[1] for r in seq]); H=np.array([r[2] for r in seq])
            chi=np.array([r[3] for r in seq]); Q=np.array([r[4] for r in seq]); N=np.log(aa); x=chi/aa
            yc=simulate_tracking(N,H,x,a.tau0H0,p,a.control_order)
            yp=simulate_tracking(N,H,x,a.tau0H0,p,a.primary_order)
            fc=-0.5*aa*aa*Q*yc/a.KB; fp=-0.5*aa*aa*Q*yp/a.KB
            rr,cc=b.rel_cos(fc,fp); per.append((rr,cc))
            allc.extend(fc.tolist()); allp.extend(fp.tolist())
            rcrows.extend((k,t,f) for t,f in zip(ct,fc)); rprows.extend((k,t,f) for t,f in zip(ct,fp))
        rel,cos=b.rel_cos(allc,allp)
        for path,rows in [(out/f'v025_{tag}_force_control.dat',rcrows),(out/f'v025_{tag}_force.dat',rprows)]:
            with path.open('w') as f:
                for k,t,z in rows: f.write(f'{k:.17g} {t:.17g} {z:.17g}\n')
        summary['points'][tag]={'p':p,'global_relative_L2_control_vs_primary':rel,'global_cosine':cos,
            'gate':bool(rel<0.01 and cos>0.9999),'samples':len(rprows)}
        print(tag,p,rel,cos,len(rprows),flush=True)
    summary['all_quadrature_gate']=all(v['gate'] for v in summary['points'].values())
    Path(a.summary).write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
    if not summary['all_quadrature_gate']: raise SystemExit(2)
if __name__=='__main__': main()
