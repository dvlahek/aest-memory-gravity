#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math,bisect
from collections import defaultdict

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
    p=out/f'v019w_{label}__cl.dat'
    if not p.exists(): raise RuntimeError(f'missing {p}')
    return p


def primary(path,peaks=None):
    rows=load_numeric(path)
    if peaks is None:
        peaks={c:max(abs(r[c-1]) for r in rows if 30<=r[0]<=2500) for c in PRIMARY_COLS}
    v=[]
    for r in rows:
        if 30<=r[0]<=2500:
            for c in PRIMARY_COLS:
                v.append(r[c-1]/max(peaks[c],1e-300))
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


def load_force(path):
    groups=defaultdict(list)
    for line in Path(path).read_text(errors='replace').splitlines():
        p=line.split()
        if len(p)!=3: continue
        k,t,f=map(float,p)
        groups[k].append((t,f))
    for k in groups:
        groups[k].sort()
    return dict(groups)


def interp(seq,t):
    ts=[x[0] for x in seq]
    i=bisect.bisect_left(ts,t)
    if i<=0: return 0.0
    if i>=len(seq): return seq[-1][1]
    t0,f0=seq[i-1]; t1,f1=seq[i]
    if t1<=t0: return f0
    x=(t-t0)/(t1-t0)
    return f0+x*(f1-f0)


def compare_force(ref_path,test_path):
    A=load_force(ref_path); B=load_force(test_path)
    bks=sorted(B)
    va=[];vb=[];miss=0
    for k,seq in A.items():
        j=bisect.bisect_left(bks,k)
        cand=[]
        if j<len(bks): cand.append(bks[j])
        if j>0: cand.append(bks[j-1])
        if not cand:
            miss+=1; continue
        kb=min(cand,key=lambda x:abs(x-k))
        if abs(kb-k)/(abs(k)+1e-300)>2e-10:
            miss+=1; continue
        bseq=B[kb]
        for t,f in seq:
            va.append(f); vb.append(interp(bseq,t))
    if not va: raise RuntimeError('no common forcing samples')
    return {
        'relative_L2':rel(vb,va),
        'cosine':cosine(vb,va),
        'reference_norm':norm(va),
        'test_norm_on_reference_grid':norm(vb),
        'common_samples':len(va),
        'missing_k_groups':miss,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir')
    ap.add_argument('--force39',required=True)
    ap.add_argument('--force47',required=True)
    ap.add_argument('--force39-p4',required=True)
    ap.add_argument('--json-out',default='results/v019w_analysis.json')
    args=ap.parse_args()
    out=Path(args.output_dir)

    v0,peaks=primary(cl_path(out,'force_l0'))
    vtrace,_=primary(cl_path(out,'trace39'),peaks)
    baseline={'relative_L2_trace39_vs_force0':rel(vtrace,v0),'cosine':cosine(vtrace,v0)}

    d1,p1,m1=central(out,'force_p1','force_m1',1.0,peaks)
    d10,p10,m10=central(out,'force_p10','force_m10',10.0,peaks)
    d30,p30,m30=central(out,'force_p30','force_m30',30.0,peaks)
    d10p4,p10p4,m10p4=central(out,'force_p10_p4','force_m10_p4',10.0,peaks)

    c1=curvature(p1,m1,v0,1.0)
    c10=curvature(p10,m10,v0,10.0)
    c30=curvature(p30,m30,v0,30.0)

    lam_conv={
        'lambda1_vs_10':{'relative_L2':rel(d1,d10),'cosine':cosine(d1,d10)},
        'lambda10_vs_30':{'relative_L2':rel(d10,d30),'cosine':cosine(d10,d30)},
    }
    curv_conv={
        'lambda1_vs_10':{'relative_L2':rel(c1,c10),'cosine':cosine(c1,c10)},
        'lambda10_vs_30':{'relative_L2':rel(c10,c30),'cosine':cosine(c10,c30)},
    }
    precision={'relative_L2_p3_vs_p4':rel(d10,d10p4),'cosine':cosine(d10,d10p4)}
    bath_force=compare_force(args.force39,args.force47)
    precision_force=compare_force(args.force39,args.force39_p4)

    signal_ok=norm(d10)>1e-8
    lambda_ok=(lam_conv['lambda10_vs_30']['relative_L2']<0.02 and
               lam_conv['lambda10_vs_30']['cosine']>0.999 and
               lam_conv['lambda1_vs_10']['relative_L2']<0.05 and
               lam_conv['lambda1_vs_10']['cosine']>0.995)
    bath_ok=bath_force['relative_L2']<0.01 and bath_force['cosine']>0.999
    force_precision_ok=precision_force['relative_L2']<0.01 and precision_force['cosine']>0.999
    cl_precision_ok=precision['relative_L2_p3_vs_p4']<0.02 and precision['cosine']>0.999
    baseline_ok=baseline['relative_L2_trace39_vs_force0']<1e-5 and baseline['cosine']>0.999999
    ok=signal_ok and lambda_ok and bath_ok and force_precision_ok and cl_precision_ok and baseline_ok

    res={
        'model':'Exp','tauH0':1.0,
        'method':'eta=0 variational forcing; signed lambda scales the exact first-order E-equation forcing and is not physical eta',
        'spectra_scope':'unlensed TT/EE/TE, 30<=ell<=2500',
        'tangent_norms':{'lambda1':norm(d1),'lambda10':norm(d10),'lambda30':norm(d30),'lambda10_p4':norm(d10p4)},
        'lambda_convergence':lam_conv,
        'quadratic_even_curvature_norms':{'lambda1':norm(c1),'lambda10':norm(c10),'lambda30':norm(c30)},
        'quadratic_even_curvature_convergence':curv_conv,
        'bath_force_convergence_39_vs_47':bath_force,
        'forcing_precision_convergence_p3_vs_p4':precision_force,
        'spectrum_precision_convergence_p3_vs_p4':precision,
        'eta0_baseline':baseline,
        'gates':{
            'signal':signal_ok,
            'lambda_invariance':lambda_ok,
            'bath_force':bath_ok,
            'forcing_precision':force_precision_ok,
            'spectrum_precision':cl_precision_ok,
            'eta0_baseline':baseline_ok,
        },
        'classification':'PASS_EXP_TAU1_VARIATIONAL_TANGENT' if ok else 'EXP_TAU1_VARIATIONAL_TANGENT_NEEDS_FOLLOWUP',
        'gate_status':'PASS' if ok else 'CHECK',
        'scope':'first-order unlensed tangent only; no likelihood or detectability claim',
    }
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2))


if __name__=='__main__':
    main()
