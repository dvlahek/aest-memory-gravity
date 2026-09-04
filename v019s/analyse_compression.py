#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
import numpy as np
from scipy.optimize import nnls

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from stable_bath import simulate_modes,simulate_quadrature,waveform_metrics

OUT=Path('results');OUT.mkdir(exist_ok=True)
TAUS=[1.0,0.1,0.01,0.001]
TARGETS=np.array([1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1,3e-1])
REF_N=16384
POOL_N=640
MAX_ACTIVE=96
CHECKPOINTS=[16,24,32,40,48,64,80,96]


def read_trace(path,model):
    rows=list(csv.DictReader(open(path)))
    out=[]
    for r in rows:
        try: out.append({k:float(v) for k,v in r.items()}|{'model':model})
        except Exception: pass
    return out


def bin_history(rows,target,dlna=.012):
    rr=[r for r in rows if abs(r['target_k']-target)/target<1e-10]
    if not rr:return None
    kvals=sorted(set(r['k'] for r in rr),key=lambda x:abs(x-target))
    k0=kvals[0]
    rr=[r for r in rr if abs(r['k']-k0)/k0<1e-12]
    rr=[r for r in rr if r['a']>0 and r['H_over_H0']>0 and np.isfinite(r['chi'])]
    if len(rr)<20:return None
    lna=np.array([np.log(r['a']) for r in rr]);lo=lna.min()
    bins=np.floor((lna-lo)/dlna).astype(int)
    out=[]
    for b in np.unique(bins):
        idx=np.where(bins==b)[0]
        vals={key:float(np.median([rr[i][key] for i in idx])) for key in ['a','H_over_H0','k_over_aH','chi']}
        vals['k']=k0;vals['target_k']=target
        out.append(vals)
    out.sort(key=lambda r:r['a'])
    return out


def crop_active(hist,threshold=1e-5,pad=8):
    chi=np.array([r['chi'] for r in hist])
    m=np.max(np.abs(chi))
    if m<=0:return None
    active=np.where(np.abs(chi)>=threshold*m)[0]
    if len(active)==0:return None
    i0=max(0,active[0]-pad);i1=min(len(hist),active[-1]+pad+1)
    return hist[i0:i1]


def case_key(case):
    model,k,tau,*_=case
    return f'{model}|{k:.12g}|{tau:.12g}'


rows=[]
for model in ('cosh','exp'):
    rows += read_trace(OUT/f'v019s_{model}_trace.csv',model)

histories={};coverage=[]
for model in ('cosh','exp'):
    mr=[r for r in rows if r['model']==model]
    for k in TARGETS:
        h=bin_history(mr,float(k))
        if h is None:continue
        h=crop_active(h)
        if h is None or len(h)<25:continue
        N=np.log(np.array([r['a'] for r in h]))
        H=np.array([r['H_over_H0'] for r in h])
        chi=np.array([r['chi'] for r in h])
        nu=np.array([r['k_over_aH'] for r in h])
        x=chi/max(np.max(np.abs(chi)),1e-300)
        histories[(model,float(k))]=(N,H,x)
        coverage.append([model,k,len(N),float(H.min()),float(H.max()),float(nu.min()),float(nu.max()),float(np.max(np.abs(chi)))])

if len(histories)<10:
    raise RuntimeError(f'too few traced histories: {len(histories)}')

with open(OUT/'v019s_active_coverage.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['model','k_Mpc^-1','points','H_over_H0_min','H_over_H0_max','k_over_aH_min','k_over_aH_max','max_abs_chi']);w.writerows(coverage)

# Interlaced k split. Both Cosh and Exp and all tau values appear in train and validation.
train_k=set(TARGETS[::2]);val_k=set(TARGETS[1::2])
train=[];val=[]
for (model,k),(N,H,x) in histories.items():
    for tau in TAUS:
        c=(model,k,tau,N,H*tau,x)
        (train if k in train_k else val).append(c)

# Stable continuum reference from the v0.19r tan(theta) construction.
refs={}
for c in train+val:
    model,k,tau,N,h,x=c
    refs[case_key(c)]=simulate_quadrature(N,h,x,REF_N)

# Global fixed-frequency candidate pool. This is deliberately independent of H(t).
# The broad log grid is only a dictionary; all retained weights are constrained positive.
omega_pool=np.logspace(-7,7,POOL_N)

# Build a source-weighted training matrix. Each history is RMS normalized so no one
# k/tau case dominates simply because its bath response is larger.
Mparts=[];yparts=[]
for c in train:
    model,k,tau,N,h,x=c
    B=simulate_modes(N,h,x,omega_pool)
    ref=refs[case_key(c)]
    i0=max(1,int(.03*len(N)))
    stride=max(1,(len(N)-i0)//220)
    sel=np.arange(i0,len(N),stride)
    scale=np.sqrt(np.mean(ref[sel]**2))+1e-12
    Mparts.append(B[sel]/scale)
    yparts.append(ref[sel]/scale)
M=np.vstack(Mparts);y=np.concatenate(yparts)

# Enforce the exact Drude high-frequency normalization sum_j w_j=1 strongly.
NORM_STRENGTH=60.0
M=np.vstack([M,NORM_STRENGTH*np.ones((1,POOL_N))])
y=np.r_[y,NORM_STRENGTH]
colnorm=np.linalg.norm(M,axis=0)+1e-300

selected=[];residual=y.copy();checkpoint_models={}
for step in range(1,MAX_ACTIVE+1):
    score=(M.T@residual)/colnorm
    if selected: score[np.asarray(selected,int)]=-np.inf
    j=int(np.argmax(score))
    if not np.isfinite(score[j]):break
    selected.append(j)
    A=M[:,selected]
    weights,_=nnls(A,y,maxiter=200000)
    residual=y-A@weights

    if step not in CHECKPOINTS:continue
    active=np.asarray(weights)>max(1e-13,1e-10*np.max(weights))
    idx=np.asarray(selected,int)[active]
    wt=np.asarray(weights)[active]
    om=omega_pool[idx]
    # Renormalize the tiny remaining sum error. Positivity is preserved.
    wt=wt/max(np.sum(wt),1e-300)

    vals=[];vrows=[]
    for c in val:
        model,k,tau,N,h,x=c
        ref=refs[case_key(c)]
        pred=simulate_modes(N,h,x,om)@wt
        met=waveform_metrics(pred,ref)
        vals.append(met['relative_L2'])
        vrows.append([model,k,tau,met['relative_L2'],met['cosine'],met['peak_normalized_error']])
    vals=np.asarray(vals,float)
    metrics={'median':float(np.median(vals)),'p95':float(np.quantile(vals,.95)),'max':float(np.max(vals))}
    passes=bool(metrics['median']<5e-4 and metrics['p95']<1e-3 and metrics['max']<3e-3 and len(om)<=96 and np.all(wt>0) and np.all(om>0))
    checkpoint_models[str(step)]={
      'greedy_step':step,'active_modes':int(len(om)),'sum_weights':float(np.sum(wt)),
      'omega_tau':om.tolist(),'positive_weights':wt.tolist(),'metrics':metrics,
      'validation_rows':vrows,'passes':passes,
    }

# Select the first passing checkpoint, otherwise the one with the smallest held-out max error.
passing=[int(k) for k,v in checkpoint_models.items() if v['passes']]
if passing:
    chosen=min(passing)
    classification='PASS_STABLE_SOURCE_WEIGHTED_COMPRESSED_BATH'
    gate='PASS'
else:
    chosen=min((int(k) for k in checkpoint_models),key=lambda k:checkpoint_models[str(k)]['metrics']['max'])
    classification='STABLE_SOURCE_WEIGHTED_COMPRESSION_NEEDS_REFINEMENT'
    gate='CHECK'
sel=checkpoint_models[str(chosen)]

with open(OUT/'v019s_checkpoints.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['greedy_step','active_modes','median_L2','p95_L2','max_L2','passes'])
    for k in sorted(checkpoint_models,key=int):
        o=checkpoint_models[k];m=o['metrics']
        w.writerow([o['greedy_step'],o['active_modes'],m['median'],m['p95'],m['max'],int(o['passes'])])

with open(OUT/'v019s_selected_validation.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['model','k','tauH0','relative_L2','cosine','peak_normalized_error']);w.writerows(sel['validation_rows'])

selected_obj={
 'classification':classification,'gate_status':gate,'reference_N':REF_N,'pool_N':POOL_N,
 'selected_checkpoint':chosen,'active_modes':sel['active_modes'],'omega_tau':sel['omega_tau'],
 'positive_weights':sel['positive_weights'],'sum_weights':sel['sum_weights'],'heldout_metrics':sel['metrics'],
 'all_frequencies_positive':bool(np.all(np.asarray(sel['omega_tau'])>0)),
 'all_weights_positive':bool(np.all(np.asarray(sel['positive_weights'])>0)),
 'fixed_frequencies':True,'H_dependent_coefficients':False,
 'fit_target':'actual eta=0 AeST CLASS chi histories against stable N=16384 tan-theta Drude continuum',
}
(OUT/'v019s_selected_bath.json').write_text(json.dumps(selected_obj,indent=2))
(OUT/'v019s_all_checkpoints.json').write_text(json.dumps(checkpoint_models,indent=2))

cov=np.array([[r[3],r[4],r[5],r[6]] for r in coverage],float)
summary={
 'traced_histories':len(histories),'training_cases':len(train),'validation_cases':len(val),
 'active_source_H_over_H0_range':[float(cov[:,0].min()),float(cov[:,1].max())],
 'active_source_k_over_aH_range':[float(cov[:,2].min()),float(cov[:,3].max())],
 'tauH0_values':TAUS,'reference_N':REF_N,'candidate_pool_N':POOL_N,
 'selected_checkpoint':chosen,'selected_active_modes':sel['active_modes'],'selected_metrics':sel['metrics'],
 'classification':classification,'gate_status':gate,
}
(OUT/'v019s_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
