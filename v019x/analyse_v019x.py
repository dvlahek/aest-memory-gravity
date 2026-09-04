#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math

PRIMARY_COLS=(2,3,4)


def load_numeric(path):
    rows=[]
    with open(path,'r',errors='replace') as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('#'): continue
            try: rows.append([float(x) for x in t.split()])
            except ValueError: pass
    if not rows: raise RuntimeError(f'no numeric rows in {path}')
    return rows


def cl_path(out,label):
    p=out/f'v019x_{label}__cl.dat'
    if not p.exists(): raise RuntimeError(f'missing {p}')
    return p


def primary(path,peaks=None):
    rows=load_numeric(path)
    if peaks is None:
        peaks={c:max(abs(r[c-1]) for r in rows if 30<=r[0]<=2500) for c in PRIMARY_COLS}
    v=[]
    for r in rows:
        if 30<=r[0]<=2500:
            for c in PRIMARY_COLS: v.append(r[c-1]/max(peaks[c],1e-300))
    return v,peaks


def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm(a): return math.sqrt(max(dot(a,a),0.0))
def sub(a,b): return [x-y for x,y in zip(a,b)]
def add(a,b): return [x+y for x,y in zip(a,b)]
def scale(a,c): return [c*x for x in a]
def rel(a,b): return norm(sub(a,b))/max(norm(b),1e-300)
def cosine(a,b):
    na,nb=norm(a),norm(b)
    return dot(a,b)/(na*nb) if na>0 and nb>0 else 1.0


def central(out,plus,minus,lam,peaks):
    vp=primary(cl_path(out,plus),peaks)[0]
    vm=primary(cl_path(out,minus),peaks)[0]
    return scale(sub(vp,vm),1.0/(2.0*lam)),vp,vm


def curvature(vp,vm,v0,lam):
    return scale(sub(add(vp,vm),scale(v0,2.0)),1.0/(2.0*lam*lam))


def cmp(a,b): return {'relative_L2':rel(a,b),'cosine':cosine(a,b)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('output_dir');ap.add_argument('--json-out',default='results/v019x_analysis.json');args=ap.parse_args()
    out=Path(args.output_dir)
    v0,peaks=primary(cl_path(out,'force_l0'))
    d30,p30,m30=central(out,'force_p30','force_m30',30.0,peaks)
    d100,p100,m100=central(out,'force_p100','force_m100',100.0,peaks)
    d300,p300,m300=central(out,'force_p300','force_m300',300.0,peaks)
    d1000,p1000,m1000=central(out,'force_p1000','force_m1000',1000.0,peaks)
    d300p4,_,_=central(out,'force_p300_p4','force_m300_p4',300.0,peaks)

    c30=curvature(p30,m30,v0,30.0)
    c100=curvature(p100,m100,v0,100.0)
    c300=curvature(p300,m300,v0,300.0)
    c1000=curvature(p1000,m1000,v0,1000.0)

    conv={
      'lambda30_vs_100':cmp(d30,d100),
      'lambda100_vs_300':cmp(d100,d300),
      'lambda300_vs_1000':cmp(d300,d1000),
    }
    curv={
      'lambda30_vs_100':cmp(c30,c100),
      'lambda100_vs_300':cmp(c100,c300),
      'lambda300_vs_1000':cmp(c300,c1000),
    }
    precision=cmp(d300,d300p4)

    # In exact linear perturbation theory T=T0+lambda*S. Therefore the odd C_ell
    # derivative is lambda-independent. Large lambda is only a numerical amplifier.
    signal_ok=norm(d300)>1e-9
    lambda_ok=(conv['lambda100_vs_300']['relative_L2']<0.01 and conv['lambda100_vs_300']['cosine']>0.9999 and
               conv['lambda300_vs_1000']['relative_L2']<0.005 and conv['lambda300_vs_1000']['cosine']>0.99999)
    precision_ok=precision['relative_L2']<0.01 and precision['cosine']>0.9999
    norm_spread=max(norm(d100),norm(d300),norm(d1000))/max(min(norm(d100),norm(d300),norm(d1000)),1e-300)-1.0
    norm_ok=norm_spread<0.01
    ok=signal_ok and lambda_ok and precision_ok and norm_ok

    res={
      'model':'Exp','tauH0':1.0,
      'method':'eta=0 exact first-order forcing with signed numerical amplifier lambda; unlensed TT/EE/TE',
      'tangent_norms':{'lambda30':norm(d30),'lambda100':norm(d100),'lambda300':norm(d300),'lambda1000':norm(d1000),'lambda300_p4':norm(d300p4)},
      'lambda_convergence':conv,
      'lambda_100_300_1000_norm_spread':norm_spread,
      'quadratic_even_curvature_norms':{'lambda30':norm(c30),'lambda100':norm(c100),'lambda300':norm(c300),'lambda1000':norm(c1000)},
      'quadratic_even_curvature_convergence':curv,
      'precision_convergence_p3_vs_p4':precision,
      'gates':{'signal':signal_ok,'lambda_invariance':lambda_ok,'norm_stability':norm_ok,'precision':precision_ok},
      'classification':'PASS_EXP_TAU1_VARIATIONAL_TANGENT_AMPLIFIED' if ok else 'EXP_TAU1_VARIATIONAL_AMPLITUDE_LADDER_NEEDS_FOLLOWUP',
      'gate_status':'PASS' if ok else 'CHECK',
      'scope':'first-order unlensed tangent only; lambda is not physical eta; no likelihood/detectability claim',
    }
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))

if __name__=='__main__': main()
