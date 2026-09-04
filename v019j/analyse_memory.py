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
    if peaks is None:
        peaks={c:max(abs(r[c-1]) for r in rows if 30<=r[0]<=2500) for c in PRIMARY_COLS}
    vec=[]
    for r in rows:
        if not (30<=r[0]<=2500):continue
        for c in PRIMARY_COLS:
            vec.append(r[c-1]/max(peaks[c],1e-300))
    return vec,peaks


def diff_vector(ref,test,peaks):
    a,_=primary_vector(ref,peaks);b,_=primary_vector(test,peaks)
    if len(a)!=len(b):raise RuntimeError('vector length mismatch')
    return [y-x for x,y in zip(a,b)]


def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):return math.sqrt(max(dot(a,a),0.))
def cosine(a,b):
    na,nb=norm(a),norm(b)
    return dot(a,b)/(na*nb) if na>0 and nb>0 else 1.0

def scale_fit(base,test):
    den=dot(base,base)
    return dot(test,base)/den if den>0 else math.nan


def compare_numeric_exact(a,b):
    aa=load_numeric(a);bb=load_numeric(b)
    if len(aa)!=len(bb):return False
    for ra,rb in zip(aa,bb):
        if len(ra)!=len(rb):return False
        for x,y in zip(ra,rb):
            if x!=y:return False
    return True


def case_path(out,model,label,suffix='cl_lensed.dat'):
    return find_one(out,f'v019j_{model}_{label}_',suffix)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('output_dir');ap.add_argument('--json-out',default='results/v019j_memory.json');args=ap.parse_args()
    out=Path(args.output_dir);res={'models':{}}
    all_ok=True
    for model in ('cosh','exp'):
        off=case_path(out,model,'off')
        _,peaks=primary_vector(off)
        labels=['n16_e0_t1','n16_e01_t1','n16_e03_t1','n16_e10_t1','n20_e0_t1','n20_e03_t1']
        vec={}
        for label in labels:
            base='n20_e0_t1' if label.startswith('n20_') else 'n16_e0_t1'
            ref=case_path(out,model,base)
            test=case_path(out,model,label)
            vec[label]=diff_vector(ref,test,peaks)

        common16=diff_vector(off,case_path(out,model,'n16_e0_t1'),peaks)
        common20=diff_vector(off,case_path(out,model,'n20_e0_t1'),peaks)
        d01=vec['n16_e01_t1'];d03=vec['n16_e03_t1'];d10=vec['n16_e10_t1']
        d20=vec['n20_e03_t1']
        n03=norm(d03);n20=norm(d20)

        lin03=scale_fit(d01,d03);lin10=scale_fit(d01,d10)
        cos03=cosine(d01,d03);cos10=cosine(d01,d10)
        order_rel=norm([a-b for a,b in zip(d03,d20)])/max(n20,1e-300)
        order_cos=cosine(d03,d20)

        # Background/thermodynamics must be exactly memory independent at fixed AeST model.
        bg_exact=compare_numeric_exact(find_one(out,f'v019j_{model}_n16_e0_t1_','background.dat'),find_one(out,f'v019j_{model}_n16_e03_t1_','background.dat'))
        th_exact=compare_numeric_exact(find_one(out,f'v019j_{model}_n16_e0_t1_','thermodynamics.dat'),find_one(out,f'v019j_{model}_n16_e03_t1_','thermodynamics.dat'))

        modelres={
          'memory_state_common_mode':{'N16_norm':norm(common16),'N20_norm':norm(common20)},
          'response_norms':{'eta_0p01_N16':norm(d01),'eta_0p03_N16':n03,'eta_0p10_N16':norm(d10),'eta_0p03_N20':n20},
          'eta_linearity':{
            'fit_eta0p03_over_eta0p01':lin03,'target':3.0,'cosine':cos03,
            'fit_eta0p10_over_eta0p01':lin10,'target_0p10':10.0,'cosine_0p10':cos10,
          },
          'bath_order_convergence_eta0p03':{'relative_L2_difference_N16_vs_N20':order_rel,'cosine':order_cos},
          'background_exact_across_eta':bg_exact,
          'thermodynamics_exact_across_eta':th_exact,
        }
        # The 0.01 -> 0.03 interval is the primary perturbative-linearity gate.
        linear_ok=math.isfinite(lin03) and abs(lin03/3.-1.)<.08 and cos03>.995
        order_ok=order_rel<.08 and order_cos>.99
        signal_ok=n03>1e-14
        modelres['gate_status']='PASS' if linear_ok and order_ok and signal_ok and bg_exact and th_exact else 'CHECK'
        all_ok &= modelres['gate_status']=='PASS'
        res['models'][model]=modelres

    res['classification']='FINITE_ETA_MEMORY_RESPONSE_RESOLVED' if all_ok else 'MEMORY_RESPONSE_NEEDS_FOLLOWUP'
    res['gate_status']='PASS' if all_ok else 'CHECK'
    res['interpretation']='Finite eta is compared to an eta=0 run carrying the same bath states, so ODE-dimension common mode is subtracted before testing eta-linearity and N=16/N=20 bath convergence.'
    res['caveat']='This is a CLASS response/consistency test, not a Planck likelihood bound. eta=0 AeST already differs from matched CDM and remains a separate effect.'
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2))
    print(json.dumps({'classification':res['classification'],'gate_status':res['gate_status'],'models':{m:{'gate_status':res['models'][m]['gate_status'],'response_norms':res['models'][m]['response_norms'],'eta_linearity':res['models'][m]['eta_linearity'],'order':res['models'][m]['bath_order_convergence_eta0p03']} for m in res['models']}},indent=2))

if __name__=='__main__':main()
