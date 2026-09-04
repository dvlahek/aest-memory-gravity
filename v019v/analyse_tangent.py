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


def find_one(out,label,suffix='cl_lensed.dat'):
    m=sorted(out.glob(f'v019v_exp_{label}_*{suffix}'))
    if len(m)!=1:raise RuntimeError(f'expected one {label} * {suffix}, found {len(m)}: {m}')
    return m[0]


def primary_vector(path,peaks=None):
    rows=load_numeric(path)
    if peaks is None:
        peaks={c:max(abs(r[c-1]) for r in rows if 30<=r[0]<=2500) for c in PRIMARY_COLS}
    vec=[]
    for r in rows:
        if 30<=r[0]<=2500:
            for c in PRIMARY_COLS:vec.append(r[c-1]/max(peaks[c],1e-300))
    return vec,peaks


def vec(path,peaks):return primary_vector(path,peaks)[0]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):return math.sqrt(max(dot(a,a),0.))
def cosine(a,b):
    na,nb=norm(a),norm(b)
    return dot(a,b)/(na*nb) if na>0 and nb>0 else 1.0
def sub(a,b):return [x-y for x,y in zip(a,b)]
def scale(a,c):return [c*x for x in a]
def add(a,b):return [x+y for x,y in zip(a,b)]
def rel(a,b):return norm(sub(a,b))/max(norm(b),1e-300)
def scale_fit(base,test):
    den=dot(base,base);return dot(test,base)/den if den>0 else math.nan


def central(out,plus,minus,h,peaks):
    vp=vec(find_one(out,plus),peaks);vm=vec(find_one(out,minus),peaks)
    if len(vp)!=len(vm):raise RuntimeError('central vector length mismatch')
    tangent=scale(sub(vp,vm),1./(2.*h))
    odd=scale(sub(vp,vm),0.5)
    return tangent,odd,vp,vm


def compare_numeric_exact(a,b):
    aa=load_numeric(a);bb=load_numeric(b)
    if len(aa)!=len(bb):return False
    return all(len(x)==len(y) and all(u==v for u,v in zip(x,y)) for x,y in zip(aa,bb))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('output_dir');ap.add_argument('--json-out',default='results/v019v_tangent.json');args=ap.parse_args()
    out=Path(args.output_dir)
    zero=find_one(out,'n39_e0');v0,peaks=primary_vector(zero)

    t03,o03,p03,m03=central(out,'n39_p03','n39_m03',0.03,peaks)
    t01,o01,p01,m01=central(out,'n39_p01','n39_m01',0.01,peaks)
    t003,o003,p003,m003=central(out,'n39_p003','n39_m003',0.003,peaks)
    t47,o47,_,_=central(out,'n47_p01','n47_m01',0.01,peaks)
    tp4,op4,_,_=central(out,'n39_p01_p4','n39_m01_p4',0.01,peaks)

    e03=sub(scale(add(p03,m03),0.5),v0)
    e01=sub(scale(add(p01,m01),0.5),v0)
    e003=sub(scale(add(p003,m003),0.5),v0)

    conv_03_01={'relative_L2':rel(t03,t01),'cosine':cosine(t03,t01)}
    conv_01_003={'relative_L2':rel(t01,t003),'cosine':cosine(t01,t003)}
    bath={'relative_L2_39_vs_47':rel(t01,t47),'cosine':cosine(t01,t47)}
    precision={'relative_L2_p3_vs_p4':rel(t01,tp4),'cosine':cosine(t01,tp4)}
    odd_scaling={
      'fit_0p01_over_0p003':scale_fit(o003,o01),'target_0p01_over_0p003':0.01/0.003,
      'cosine_0p01_0p003':cosine(o003,o01),
      'fit_0p03_over_0p01':scale_fit(o01,o03),'target_0p03_over_0p01':3.0,
      'cosine_0p03_0p01':cosine(o01,o03),
    }

    bg_exact=compare_numeric_exact(find_one(out,'n39_p01','background.dat'),find_one(out,'n39_m01','background.dat'))
    th_exact=compare_numeric_exact(find_one(out,'n39_p01','thermodynamics.dat'),find_one(out,'n39_m01','thermodynamics.dat'))

    signal_ok=norm(t003)>1e-10
    h_ok=conv_01_003['relative_L2']<0.05 and conv_01_003['cosine']>0.995
    bath_ok=bath['relative_L2_39_vs_47']<0.02 and bath['cosine']>0.999
    precision_ok=precision['relative_L2_p3_vs_p4']<0.03 and precision['cosine']>0.999
    ok=signal_ok and h_ok and bath_ok and precision_ok and bg_exact and th_exact

    res={
      'model':'Exp','tauH0':1.0,
      'method':'symmetric signed-eta tangent-limit diagnostic; negative eta is non-physical and used only to estimate d/deta at eta=0',
      'tangent_norms':{'h0p03':norm(t03),'h0p01':norm(t01),'h0p003':norm(t003),'order47_h0p01':norm(t47),'p4_h0p01':norm(tp4)},
      'odd_response_norms':{'h0p03':norm(o03),'h0p01':norm(o01),'h0p003':norm(o003)},
      'even_contamination_norms':{'h0p03':norm(e03),'h0p01':norm(e01),'h0p003':norm(e003)},
      'h_convergence':{'h0p03_vs_h0p01':conv_03_01,'h0p01_vs_h0p003':conv_01_003},
      'odd_scaling':odd_scaling,
      'bath_order_convergence':bath,
      'precision_convergence':precision,
      'background_exact_plus_minus':bg_exact,
      'thermodynamics_exact_plus_minus':th_exact,
      'gates':{'signal':signal_ok,'h_limit':h_ok,'bath_order':bath_ok,'precision':precision_ok,'background':bg_exact,'thermodynamics':th_exact},
      'classification':'PASS_EXP_TAU1_TANGENT_LIMIT' if ok else 'EXP_TAU1_TANGENT_LIMIT_NEEDS_FOLLOWUP',
      'gate_status':'PASS' if ok else 'CHECK',
      'scope':'diagnostic tangent limit only; no physical negative-eta claim; no likelihood claim'
    }
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))

if __name__=='__main__':main()
