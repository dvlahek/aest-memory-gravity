#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
import numpy as np
from scipy.optimize import nnls

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'v019s'))
from stable_bath import tan_gl_nodes,simulate_modes,simulate_quadrature,waveform_metrics

OUT=Path('results');OUT.mkdir(exist_ok=True)
TAU=1.0
TARGETS=np.array([1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1,3e-1])
REF_N=16384
POOL_N=512
CHECKPOINTS=[16,24,32,40,48,64,80,96,112,128,160,192]
MAX_ACTIVE=max(CHECKPOINTS)


def read_trace(path,model):
    rows=list(csv.DictReader(open(path)));out=[]
    for r in rows:
        try:out.append({k:float(v) for k,v in r.items()}|{'model':model})
        except Exception:pass
    return out


def bin_history(rows,target,dlna=.012):
    rr=[r for r in rows if abs(r['target_k']-target)/target<1e-10]
    if not rr:return None
    k0=sorted(set(r['k'] for r in rr),key=lambda x:abs(x-target))[0]
    rr=[r for r in rr if abs(r['k']-k0)/k0<1e-12 and r['a']>0 and r['H_over_H0']>0 and np.isfinite(r['chi'])]
    if len(rr)<20:return None
    lna=np.array([np.log(r['a']) for r in rr]);lo=lna.min();bins=np.floor((lna-lo)/dlna).astype(int)
    out=[]
    for b in np.unique(bins):
        ii=np.where(bins==b)[0]
        d={key:float(np.median([rr[i][key] for i in ii])) for key in ['a','H_over_H0','chi']}
        d['k']=k0;d['target_k']=target;out.append(d)
    out.sort(key=lambda r:r['a']);return out


def crop_active(hist,threshold=1e-5,pad=8):
    chi=np.array([r['chi'] for r in hist]);m=np.max(np.abs(chi))
    if m<=0:return None
    ii=np.where(np.abs(chi)>=threshold*m)[0]
    if len(ii)==0:return None
    return hist[max(0,ii[0]-pad):min(len(hist),ii[-1]+pad+1)]

rows=[]
for model in ('cosh','exp'):rows+=read_trace(OUT/f'v019t_{model}_trace.csv',model)
hist={}
for model in ('cosh','exp'):
    mr=[r for r in rows if r['model']==model]
    for k in TARGETS:
        h=crop_active(bin_history(mr,float(k)) or [])
        if not h or len(h)<25:continue
        N=np.log(np.array([r['a'] for r in h]));H=np.array([r['H_over_H0'] for r in h]);chi=np.array([r['chi'] for r in h])
        x=chi/max(np.max(np.abs(chi)),1e-300)
        hist[(model,float(k))]=(N,H*TAU,x)
if len(hist)!=16:raise RuntimeError(f'expected 16 histories, got {len(hist)}')

train_k=set(TARGETS[::2]);val_k=set(TARGETS[1::2])
train=[(m,k,*v) for (m,k),v in hist.items() if k in train_k]
val=[(m,k,*v) for (m,k),v in hist.items() if k in val_k]

refs={}
for m,k,N,h,x in train+val:refs[(m,k)]=simulate_quadrature(N,h,x,REF_N)
omega_pool,direct_weights=tan_gl_nodes(POOL_N)

Mparts=[];yparts=[]
for m,k,N,h,x in train:
    B=simulate_modes(N,h,x,omega_pool);ref=refs[(m,k)]
    i0=max(1,int(.03*len(N)));stride=max(1,(len(N)-i0)//260);sel=np.arange(i0,len(N),stride)
    scale=np.sqrt(np.mean(ref[sel]**2))+1e-12
    Mparts.append(B[sel]/scale);yparts.append(ref[sel]/scale)
M=np.vstack(Mparts);y=np.concatenate(yparts)
# Strong normalization row preserves the Drude high-frequency limit.
strength=80.0
M=np.vstack([M,strength*np.ones((1,POOL_N))]);y=np.r_[y,strength]
colnorm=np.linalg.norm(M,axis=0)+1e-300
selected=[];res=y.copy();models={}
for step in range(1,MAX_ACTIVE+1):
    score=(M.T@res)/colnorm
    if selected:score[np.asarray(selected,int)]=-np.inf
    j=int(np.argmax(score));selected.append(j)
    A=M[:,selected];w,_=nnls(A,y,maxiter=200000);res=y-A@w
    if step not in CHECKPOINTS:continue
    active=w>max(1e-13,1e-10*np.max(w));idx=np.asarray(selected)[active];wt=w[active];wt=wt/np.sum(wt);om=omega_pool[idx]
    vals=[];rowsv=[]
    for m,k,N,h,x in val:
        ref=refs[(m,k)];pred=simulate_modes(N,h,x,om)@wt;met=waveform_metrics(pred,ref)
        vals.append(met['relative_L2']);rowsv.append([m,k,met['relative_L2'],met['cosine'],met['peak_normalized_error']])
    vals=np.asarray(vals)
    metrics={'median':float(np.median(vals)),'p95':float(np.quantile(vals,.95)),'max':float(np.max(vals))}
    passes=bool(metrics['median']<2e-4 and metrics['p95']<5e-4 and metrics['max']<1e-3 and len(om)<=128)
    models[str(step)]={'greedy_step':step,'active_modes':int(len(om)),'omega_tau':om.tolist(),'positive_weights':wt.tolist(),'sum_weights':float(np.sum(wt)),'metrics':metrics,'validation_rows':rowsv,'passes':passes}

passing=[int(k) for k,v in models.items() if v['passes']]
if passing:
    chosen=min(passing);classification='PASS_TAU1_COMPRESSED_POSITIVE_BATH';gate='PASS'
else:
    chosen=min((int(k) for k in models),key=lambda k:models[str(k)]['metrics']['max']);classification='TAU1_COMPRESSION_NEEDS_REFINEMENT';gate='CHECK'
sel=models[str(chosen)]

# Direct N=512 control on exactly the same held-out histories.
dvals=[]
for m,k,N,h,x in val:
    met=waveform_metrics(simulate_modes(N,h,x,omega_pool)@direct_weights,refs[(m,k)]);dvals.append(met['relative_L2'])
direct={'median':float(np.median(dvals)),'p95':float(np.quantile(dvals,.95)),'max':float(np.max(dvals))}

with open(OUT/'v019t_checkpoints.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['step','active','median','p95','max','passes'])
    for k in sorted(models,key=int):
        o=models[k];mm=o['metrics'];w.writerow([o['greedy_step'],o['active_modes'],mm['median'],mm['p95'],mm['max'],int(o['passes'])])
with open(OUT/'v019t_validation.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['model','k','relative_L2','cosine','peak_normalized_error']);w.writerows(sel['validation_rows'])

selected_obj={'classification':classification,'gate_status':gate,'tauH0':TAU,'reference_N':REF_N,'pool':'direct tan-theta N=512 nodes','selected_checkpoint':chosen,'active_modes':sel['active_modes'],'omega_tau':sel['omega_tau'],'positive_weights':sel['positive_weights'],'sum_weights':sel['sum_weights'],'heldout_metrics':sel['metrics'],'direct_N512_control':direct,'fixed_positive_frequencies':True,'H_dependent_coefficients':False}
(OUT/'v019t_selected_bath.json').write_text(json.dumps(selected_obj,indent=2))
(OUT/'v019t_all_checkpoints.json').write_text(json.dumps(models,indent=2))
summary={'traced_histories':len(hist),'training_histories':len(train),'validation_histories':len(val),'tauH0':TAU,'reference_N':REF_N,'pool_N':POOL_N,'direct_N512_control':direct,'selected_checkpoint':chosen,'selected_active_modes':sel['active_modes'],'selected_metrics':sel['metrics'],'classification':classification,'gate_status':gate}
(OUT/'v019t_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
