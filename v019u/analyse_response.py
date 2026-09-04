#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math

PRIMARY_COLS=(2,3,4)


def load_numeric(path):
    rows=[]
    with open(path,'r',errors='replace') as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('#'):continue
            try:rows.append([float(x) for x in t.split()])
            except ValueError:pass
    if not rows:raise RuntimeError(f'no numeric data in {path}')
    return rows


def find_one(out,prefix,suffix):
    m=sorted(out.glob(prefix+'*'+suffix))
    if len(m)!=1:raise RuntimeError(f'expected one {prefix}*{suffix}, found {len(m)}')
    return m[0]


def primary_vector(path,peaks=None):
    rows=load_numeric(path)
    if peaks is None:peaks={c:max(abs(r[c-1]) for r in rows if 30<=r[0]<=2500) for c in PRIMARY_COLS}
    vec=[]
    for r in rows:
        if 30<=r[0]<=2500:
            for c in PRIMARY_COLS:vec.append(r[c-1]/max(peaks[c],1e-300))
    return vec,peaks


def diff_vector(ref,test,peaks):
    a,_=primary_vector(ref,peaks);b,_=primary_vector(test,peaks)
    if len(a)!=len(b):raise RuntimeError('vector length mismatch')
    return [y-x for x,y in zip(a,b)]

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):return math.sqrt(max(dot(a,a),0.))
def cosine(a,b):
    na,nb=norm(a),norm(b);return dot(a,b)/(na*nb) if na>0 and nb>0 else 1.0
def scale_fit(base,test):
    den=dot(base,base);return dot(test,base)/den if den>0 else math.nan

def compare_numeric_exact(a,b):
    aa=load_numeric(a);bb=load_numeric(b)
    if len(aa)!=len(bb):return False
    return all(len(x)==len(y) and all(u==v for u,v in zip(x,y)) for x,y in zip(aa,bb))

def case(out,model,label,suffix='cl_lensed.dat'):
    return find_one(out,f'v019u_{model}_{label}_',suffix)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('output_dir');ap.add_argument('--json-out',default='results/v019u_response.json');args=ap.parse_args()
    out=Path(args.output_dir);res={'models':{}};overall=True
    for model in ('cosh','exp'):
        off=case(out,model,'off');_,peaks=primary_vector(off)
        b39=case(out,model,'n39_e0');b47=case(out,model,'n47_e0')
        d003=diff_vector(b39,case(out,model,'n39_e003'),peaks)
        d01=diff_vector(b39,case(out,model,'n39_e01'),peaks)
        d03=diff_vector(b39,case(out,model,'n39_e03'),peaks)
        d47=diff_vector(b47,case(out,model,'n47_e01'),peaks)
        common39=diff_vector(off,b39,peaks);common47=diff_vector(off,b47,peaks)
        fit01=scale_fit(d003,d01);fit03=scale_fit(d01,d03)
        cos01=cosine(d003,d01);cos03=cosine(d01,d03)
        order_rel=norm([a-b for a,b in zip(d01,d47)])/max(norm(d47),1e-300)
        order_cos=cosine(d01,d47)
        bg_exact=compare_numeric_exact(find_one(out,f'v019u_{model}_n39_e0_','background.dat'),find_one(out,f'v019u_{model}_n39_e01_','background.dat'))
        th_exact=compare_numeric_exact(find_one(out,f'v019u_{model}_n39_e0_','thermodynamics.dat'),find_one(out,f'v019u_{model}_n39_e01_','thermodynamics.dat'))
        linear_ok=abs(fit01/(0.01/0.003)-1.)<0.08 and abs(fit03/3.-1.)<0.08 and cos01>.995 and cos03>.995
        order_ok=order_rel<0.08 and order_cos>.995
        signal_ok=norm(d01)>1e-14
        ok=linear_ok and order_ok and signal_ok and bg_exact and th_exact
        overall &= ok
        res['models'][model]={
          'common_mode_norms':{'order39':norm(common39),'order47':norm(common47)},
          'response_norms':{'eta0p003_order39':norm(d003),'eta0p01_order39':norm(d01),'eta0p03_order39':norm(d03),'eta0p01_order47':norm(d47)},
          'eta_linearity':{'fit_0p01_over_0p003':fit01,'target_0p01_over_0p003':0.01/0.003,'cosine':cos01,'fit_0p03_over_0p01':fit03,'target_0p03_over_0p01':3.0,'cosine_0p03':cos03},
          'bath_order_convergence_eta0p01':{'relative_L2_difference_39_vs_47':order_rel,'cosine':order_cos},
          'background_exact_across_eta':bg_exact,'thermodynamics_exact_across_eta':th_exact,
          'gate_status':'PASS' if ok else 'CHECK'}
    res['classification']='PASS_TAU1_FINITE_MEMORY_CLASS_RESPONSE' if overall else 'TAU1_FINITE_MEMORY_RESPONSE_NEEDS_FOLLOWUP'
    res['gate_status']='PASS' if overall else 'CHECK'
    res['scope']='tauH0=1 only; same-bath eta=0 subtraction; no likelihood claim'
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))

if __name__=='__main__':main()
