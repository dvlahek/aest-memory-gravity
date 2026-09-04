#!/usr/bin/env python3
from pathlib import Path
import sys,csv,json
import numpy as np
from scipy.optimize import nnls

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'v019m'))
from timevarying import reference_nodes,simulate_fixed_modes,waveform_metrics

OUT=Path('results');OUT.mkdir(exist_ok=True)
TAUS=[1.0,.1,.01,.001]
TARGETS=np.array([1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1,3e-1])


def read_trace(path,model):
    rows=list(csv.DictReader(open(path)))
    data=[]
    for r in rows:
        try:
            data.append({k:float(v) for k,v in r.items()}|{'model':model})
        except Exception:
            pass
    return data


def bin_history(rows,target,dlna=.012):
    rr=[r for r in rows if abs(r['target_k']-target)/target<1e-10]
    if not rr:return None
    # Keep the actual k closest to the requested inserted k.
    kvals=sorted(set(r['k'] for r in rr),key=lambda x:abs(x-target))
    k0=kvals[0]
    rr=[r for r in rr if abs(r['k']-k0)/k0<1e-12]
    rr=[r for r in rr if r['a']>0 and r['H_over_H0']>0 and np.isfinite(r['chi'])]
    if len(rr)<20:return None
    lna=np.array([np.log(r['a']) for r in rr])
    lo=lna.min();bins=np.floor((lna-lo)/dlna).astype(int)
    out=[]
    for b in np.unique(bins):
        idx=np.where(bins==b)[0]
        # Median suppresses rejected/intermediate ODE evaluations at nearly identical a.
        vals={key:float(np.median([rr[i][key] for i in idx])) for key in ['a','H_over_H0','k_over_aH','chi','alpha','E','theta_div','Q']}
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


def dense_reference(N,h,x,Nref):
    om,w=reference_nodes(Nref,wmin=1e-8,wmax=1e8)
    return simulate_fixed_modes(N,h,x,om)@w


def basis_response(N,h,x,omega):
    return simulate_fixed_modes(N,h,x,omega)

allrows=[]
for model in ['cosh','exp']:
    allrows += read_trace(OUT/f'v019q_{model}_trace.csv',model)

histories={};coverage=[]
for model in ['cosh','exp']:
    mr=[r for r in allrows if r['model']==model]
    for k in TARGETS:
        h0=bin_history(mr,float(k))
        if h0 is None:continue
        h0=crop_active(h0)
        if h0 is None or len(h0)<25:continue
        N=np.log(np.array([r['a'] for r in h0]))
        H=np.array([r['H_over_H0'] for r in h0])
        chi=np.array([r['chi'] for r in h0])
        nu=np.array([r['k_over_aH'] for r in h0])
        x=chi/max(np.max(np.abs(chi)),1e-300)
        histories[(model,float(k))]=(N,H,x)
        coverage.append([model,k,len(N),float(H.min()),float(H.max()),float(nu.min()),float(nu.max()),float(np.max(np.abs(chi)))])

with open(OUT/'v019q_active_coverage.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['model','k_Mpc^-1','points','H_over_H0_min','H_over_H0_max','k_over_aH_min','k_over_aH_max','max_abs_chi']);w.writerows(coverage)

if len(histories)<10:
    raise RuntimeError(f'too few traced histories: {len(histories)}')

# Train on alternating k values, validate on the interlaced held-out k values.
train_k=set(TARGETS[::2]); val_k=set(TARGETS[1::2])
train_cases=[];val_cases=[]
for (model,k),(N,H,x) in histories.items():
    for tau in TAUS:
        case=(model,k,tau,N,H*tau,x)
        (train_cases if k in train_k else val_cases).append(case)

# Dense reference cache. Cropping to the actual chi-active interval makes high dynamic-range
# continuum quadrature far better conditioned than the artificial v0.19o box test.
refs={};refconv=[]
for case in train_cases+val_cases:
    model,k,tau,N,h,x=case;key=(model,k,tau)
    r2048=dense_reference(N,h,x,2048)
    refs[key]=r2048
    if case in val_cases:
        r1024=dense_reference(N,h,x,1024)
        m=waveform_metrics(r1024,r2048,discard_fraction=.03)
        refconv.append(m['relative_L2'])

candidates=[48,64,80,96,128]
fitrows=[];objects={};selected=None
for Ncand in candidates:
    omega=np.logspace(-7,8,Ncand)
    M=[];y=[]
    for model,k,tau,N,h,x in train_cases:
        B=basis_response(N,h,x,omega)
        ref=refs[(model,k,tau)]
        sel=np.arange(max(1,int(.03*len(N))),len(N),3)
        scale=np.sqrt(np.mean(ref[sel]**2))+1e-12
        M.append(B[sel]/scale);y.append(ref[sel]/scale)
    M=np.vstack(M);y=np.concatenate(y)
    # Exact high-frequency normalization of the Drude measure.
    M=np.vstack([M,40.*np.ones((1,Ncand))]);y=np.r_[y,40.]
    weights,_=nnls(M,y,maxiter=50000)
    active=weights>max(1e-13,1e-9*np.max(weights))

    vals=[];vrows=[]
    for model,k,tau,N,h,x in val_cases:
        ref=refs[(model,k,tau)]
        pred=basis_response(N,h,x,omega)@weights
        m=waveform_metrics(pred,ref,discard_fraction=.03)
        vals.append(m['relative_L2'])
        vrows.append([model,k,tau,m['relative_L2'],m['cosine'],m['peak_normalized_error']])
    vals=np.asarray(vals)
    met={'median':float(np.median(vals)),'p95':float(np.quantile(vals,.95)),'max':float(np.max(vals))}
    obj={'Ngrid':Ncand,'active_modes':int(np.count_nonzero(active)),'sum_weights':float(weights.sum()),'metrics':met,
         'omega':omega.tolist(),'weights':weights.tolist(),'active_mask':active.astype(int).tolist(),'validation_rows':vrows}
    objects[str(Ncand)]=obj
    fitrows.append([Ncand,obj['active_modes'],obj['sum_weights'],met['median'],met['p95'],met['max']])
    if selected is None and met['median']<5e-4 and met['p95']<1e-3 and met['max']<3e-3:
        selected=Ncand

if selected is None:
    selected=min(candidates,key=lambda n:objects[str(n)]['metrics']['max'])
    classification='CLASS_SOURCE_WEIGHTED_BATH_NEEDS_REFINEMENT'
else:
    classification='PASS_CLASS_SOURCE_WEIGHTED_FIXED_BATH'

sel=objects[str(selected)];mask=np.asarray(sel['active_mask'],bool)
omega=np.asarray(sel['omega'])[mask];weights=np.asarray(sel['weights'])[mask]
selected_obj={'selected_grid_N':selected,'active_modes':int(len(omega)),'omega_tau':omega.tolist(),'positive_weights':weights.tolist(),
              'sum_weights':float(weights.sum()),'heldout_metrics':sel['metrics'],'classification':classification}
(OUT/'v019q_selected_bath.json').write_text(json.dumps(selected_obj,indent=2))
(OUT/'v019q_fit_candidates.json').write_text(json.dumps({'selected':selected,'classification':classification,'candidates':objects},indent=2))
with open(OUT/'v019q_fit_candidates.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['Ngrid','active','sum_weights','val_median_L2','val_p95_L2','val_max_L2']);w.writerows(fitrows)
with open(OUT/'v019q_selected_validation.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['model','k','tauH0','relative_L2','cosine','peak_normalized_error']);w.writerows(sel['validation_rows'])

cov_arr=np.array([[r[3],r[4],r[5],r[6]] for r in coverage],float)
summary={
 'traced_histories':len(histories),
 'train_cases':len(train_cases),'validation_cases':len(val_cases),
 'active_source_H_over_H0_range':[float(cov_arr[:,0].min()),float(cov_arr[:,1].max())],
 'active_source_k_over_aH_range':[float(cov_arr[:,2].min()),float(cov_arr[:,3].max())],
 'tauH0_values':TAUS,
 'dense_reference_convergence':{'median':float(np.median(refconv)),'p95':float(np.quantile(refconv,.95)),'max':float(np.max(refconv))},
 'selected_grid_N':selected,'selected_active_modes':selected_obj['active_modes'],'selected_metrics':sel['metrics'],
 'classification':classification,
 'gate_status':'PASS' if classification.startswith('PASS') and max(refconv)<3e-4 else 'CHECK',
}
(OUT/'v019q_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
