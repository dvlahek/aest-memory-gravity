#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math, numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v022build',ROOT/'v022'/'build_offline_forcing.py')
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)


def simulate_response_evolving(N,H,x,tau0H0,p,n):
    """Positive Drude response with tau_eff H0=tau0H0*(H/H0)^(-p).

    In the v0.22 N-variable propagator the local dimensionless Hubble factor is
    h=H*tau. Hence hgrid=tau0H0*H**(1-p). For p=0 this is algebraically
    identical to v022.simulate_response(N,H,x,tau0H0,n).
    """
    omega,weights=b.tan_gl_nodes(n)
    q=np.zeros(int(n)); v=np.zeros(int(n)); out=np.empty(len(N)); out[0]=x[0]
    hgrid=tau0H0*np.power(H,1.0-p)
    for i in range(len(N)-1):
        dN=N[i+1]-N[i]
        if not (dN>0):
            out[i+1]=out[i]; continue
        hm=math.sqrt(hgrid[i]*hgrid[i+1])
        dt=dN/hm
        q,v=b._step_linear(q,v,omega,hm,x[i],x[i+1],dt)
        out[i+1]=x[i+1]-float(np.dot(weights,q))
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('trace')
    ap.add_argument('--KB',type=float,required=True)
    ap.add_argument('--tau0H0',type=float,required=True)
    ap.add_argument('--p',type=float,required=True)
    ap.add_argument('--out-prefix',required=True)
    ap.add_argument('--control-order',type=int,default=512)
    ap.add_argument('--primary-order',type=int,default=1024)
    ap.add_argument('--summary',required=True)
    a=ap.parse_args()
    if not (a.KB>0 and a.tau0H0>0 and a.p>=0): raise SystemExit('require KB>0, tau0H0>0, p>=0')
    histories=b.read_trace(a.trace); allc=[]; allp=[]; rcrows=[]; rprows=[]
    for k in sorted(histories):
        seq=histories[k]
        ct=np.array([r[0] for r in seq]); aa=np.array([r[1] for r in seq]); H=np.array([r[2] for r in seq]); chi=np.array([r[3] for r in seq]); Q=np.array([r[4] for r in seq])
        N=np.log(aa); x=chi/aa
        yc=simulate_response_evolving(N,H,x,a.tau0H0,a.p,a.control_order)
        yp=simulate_response_evolving(N,H,x,a.tau0H0,a.p,a.primary_order)
        fc=-0.5*aa*aa*Q*yc/a.KB; fp=-0.5*aa*aa*Q*yp/a.KB
        allc.extend(fc.tolist()); allp.extend(fp.tolist())
        rcrows.extend((k,t,f) for t,f in zip(ct,fc)); rprows.extend((k,t,f) for t,f in zip(ct,fp))
    rel,cos=b.rel_cos(allc,allp); pref=Path(a.out_prefix)
    for path,rows in [(Path(str(pref)+'_force_control.dat'),rcrows),(Path(str(pref)+'_force.dat'),rprows)]:
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('w') as f:
            for k,t,z in rows: f.write(f'{k:.17g} {t:.17g} {z:.17g}\n')
    res={'classification':'V040_LOCKED_KB_EVOLVING_POSITIVE_DRUDE_MEMORY','KB':a.KB,'tau0H0':a.tau0H0,'p':a.p,
         'tau_eff_law':'tau_eff(a) H0 = tau0H0 * (H(a)/H0)^(-p)',
         'local_hgrid':'H*tau_eff = tau0H0 * H^(1-p)',
         'control_order':a.control_order,'primary_order':a.primary_order,
         'relative_L2_control_vs_primary':rel,'cosine':cos,'gate':bool(rel<0.01 and cos>0.9999),
         'samples':len(rprows),'k_histories':len(histories)}
    Path(a.summary).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not res['gate']: raise SystemExit(2)

if __name__=='__main__': main()
