#!/usr/bin/env python3
from pathlib import Path
import csv,json
import numpy as np
from scipy.special import roots_legendre

OUT=Path('results');OUT.mkdir(exist_ok=True)
TAUS=[1.0,0.1,0.01,0.001]
TARGETS=np.array([1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1,3e-1])
REF_LO=8192
REF_HI=16384
CANDIDATES=[512,1024,2048,4096]


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


def waveform_metrics(test,ref,discard_fraction=.03):
    n=len(ref);i0=max(1,int(discard_fraction*n))
    a=np.asarray(test[i0:],float);b=np.asarray(ref[i0:],float)
    nr=np.linalg.norm(b);nt=np.linalg.norm(a)
    l2=float(np.linalg.norm(a-b)/max(nr,1e-300))
    cos=float(np.dot(a,b)/max(nt*nr,1e-300))
    peak=float(np.max(np.abs(a-b))/max(np.max(np.abs(b)),1e-300))
    return {'relative_L2':l2,'cosine':cos,'peak_normalized_error':peak,
            'reference_rms':float(np.sqrt(np.mean(b*b)))}


def tan_gl_nodes(n):
    z,w=roots_legendre(int(n))
    theta=0.25*np.pi*(z+1.0)
    omega=np.tan(theta)
    weights=0.5*w
    return np.asarray(omega,float),np.asarray(weights,float)


def _step_linear(q,v,omega,h,x0,x1,dt):
    # q'' + 3 h q' + omega^2 q = omega^2 x(t), with h frozen and
    # x(t) linear over this interval. v is q'.
    c=3.0*h
    d=0.5*c
    r=(x1-x0)/dt
    u0=q-x0
    vu0=v-r
    force=-c*r
    om2=omega*omega
    disc=om2-d*d
    scale=np.maximum(om2+d*d,1.0)
    under=disc>1.e-12*scale
    over=disc<-1.e-12*scale
    crit=~(under|over)
    un=np.empty_like(q)
    vn=np.empty_like(v)

    if np.any(under):
        O=np.sqrt(disc[under])
        z=O*dt
        ed=np.exp(-d*dt)
        C=np.cos(z);S=np.sin(z)
        uu=u0[under];vv=vu0[under];oo2=om2[under]
        hu=ed*(uu*C+(vv+d*uu)/O*S)
        hv=ed*(vv*C-(d*vv+oo2*uu)/O*S)
        one=1.0-ed*(C+d/O*S)
        G=ed*S/O
        un[under]=hu+force/oo2*one
        vn[under]=hv+force*G

    if np.any(over):
        oo2=om2[over]
        delta=np.sqrt(-disc[over])
        # Cancellation-safe slow root. Do not evaluate -d+delta directly.
        lam1=-oo2/(d+delta)
        lam2=-d-delta
        den=lam1-lam2
        e1=np.exp(lam1*dt);e2=np.exp(lam2*dt)
        uu=u0[over];vv=vu0[over]
        c1=(vv-lam2*uu)/den
        c2=(lam1*uu-vv)/den
        hu=c1*e1+c2*e2
        hv=lam1*c1*e1+lam2*c2*e2
        # 1-phi evaluated with expm1 so the omega->0 limit is stable.
        one=(-lam2*(-np.expm1(lam1*dt))+lam1*(-np.expm1(lam2*dt)))/den
        G=(e1-e2)/den
        un[over]=hu+force/oo2*one
        vn[over]=hv+force*G

    if np.any(crit):
        oo2=om2[crit]
        z=d*dt
        ed=np.exp(-z)
        uu=u0[crit];vv=vu0[crit]
        hu=ed*(uu+(vv+d*uu)*dt)
        hv=ed*(vv-(d*vv+oo2*uu)*dt)
        one=-np.expm1(-z)-z*ed
        G=ed*dt
        un[crit]=hu+force/oo2*one
        vn[crit]=hv+force*G

    return x1+un,vn+r


_NODE_CACHE={}
def simulate_quadrature(Ngrid,hgrid,xgrid,n):
    n=int(n)
    if n not in _NODE_CACHE:
        _NODE_CACHE[n]=tan_gl_nodes(n)
    omega,weights=_NODE_CACHE[n]
    q=np.zeros(n);v=np.zeros(n)
    out=np.empty(len(Ngrid))
    out[0]=np.dot(weights,xgrid[0]-q)
    for i in range(len(Ngrid)-1):
        hm=np.sqrt(hgrid[i]*hgrid[i+1])
        dt=(Ngrid[i+1]-Ngrid[i])/hm
        q,v=_step_linear(q,v,omega,hm,xgrid[i],xgrid[i+1],dt)
        out[i+1]=np.dot(weights,xgrid[i+1]-q)
    return out


allrows=[]
for model in ['cosh','exp']:
    allrows += read_trace(OUT/f'v019r_{model}_trace.csv',model)

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

with open(OUT/'v019r_active_coverage.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['model','k_Mpc^-1','points','H_over_H0_min','H_over_H0_max','k_over_aH_min','k_over_aH_max','max_abs_chi']);w.writerows(coverage)

if len(histories)<10:
    raise RuntimeError(f'too few traced histories: {len(histories)}')

# Interlaced held-out k values. There is no fitted parameter in v0.19r, but keeping
# the same held-out split as v0.19q makes the gate directly comparable.
val_k=set(TARGETS[1::2])
val_cases=[]
for (model,k),(N,H,x) in histories.items():
    if k not in val_k:continue
    for tau in TAUS:
        val_cases.append((model,k,tau,N,H*tau,x))

refs_hi={};refrows=[]
for model,k,tau,N,h,x in val_cases:
    rlo=simulate_quadrature(N,h,x,REF_LO)
    rhi=simulate_quadrature(N,h,x,REF_HI)
    refs_hi[(model,k,tau)]=rhi
    m=waveform_metrics(rlo,rhi)
    refrows.append([model,k,tau,m['relative_L2'],m['cosine'],m['peak_normalized_error']])

with open(OUT/'v019r_reference_convergence.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['model','k','tauH0','relative_L2_8192_vs_16384','cosine','peak_normalized_error']);w.writerows(refrows)

ref_l2=np.asarray([r[3] for r in refrows],float)
ref_metrics={'median':float(np.median(ref_l2)),'p95':float(np.quantile(ref_l2,.95)),'max':float(np.max(ref_l2))}

candidate_objects={};candidate_rows=[];selected=None
for n in CANDIDATES:
    om,wt=tan_gl_nodes(n)
    vals=[];rows=[]
    for model,k,tau,N,h,x in val_cases:
        pred=simulate_quadrature(N,h,x,n)
        ref=refs_hi[(model,k,tau)]
        m=waveform_metrics(pred,ref)
        vals.append(m['relative_L2'])
        rows.append([model,k,tau,m['relative_L2'],m['cosine'],m['peak_normalized_error']])
    vals=np.asarray(vals,float)
    met={'median':float(np.median(vals)),'p95':float(np.quantile(vals,.95)),'max':float(np.max(vals))}
    positive=bool(np.all(om>0.) and np.all(wt>0.))
    sumerr=float(abs(np.sum(wt)-1.0))
    passes=bool(met['median']<5e-4 and met['p95']<1e-3 and met['max']<3e-3 and positive and sumerr<1e-12)
    obj={'N':int(n),'metrics':met,'all_frequencies_positive':bool(np.all(om>0.)),'all_weights_positive':bool(np.all(wt>0.)),
         'sum_weights':float(np.sum(wt)),'sum_weight_error':sumerr,'passes':passes,'validation_rows':rows}
    candidate_objects[str(n)]=obj
    candidate_rows.append([n,met['median'],met['p95'],met['max'],int(positive),obj['sum_weights'],sumerr,int(passes)])
    if selected is None and passes:selected=n

with open(OUT/'v019r_candidates.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['N','median_L2','p95_L2','max_L2','positive','sum_weights','sum_weight_error','passes']);w.writerows(candidate_rows)

ref_pass=bool(ref_metrics['max']<2e-4)
if selected is not None and ref_pass:
    classification='PASS_CLASS_TRAJECTORY_TAN_GL_BATH'
    gate_status='PASS'
else:
    classification='TAN_GL_BATH_NEEDS_REFINEMENT'
    gate_status='CHECK'

selected_obj={}
if selected is not None:
    om,wt=tan_gl_nodes(selected)
    selected_obj={
      'selected_N':int(selected),
      'omega_tau':om.tolist(),
      'positive_weights':wt.tolist(),
      'sum_weights':float(np.sum(wt)),
      'heldout_metrics':candidate_objects[str(selected)]['metrics'],
      'all_frequencies_positive':True,
      'all_weights_positive':True,
      'construction':'direct Gauss-Legendre quadrature after omega=tan(theta)',
      'fitted_parameters':False,
      'classification':classification,
    }
(OUT/'v019r_selected_bath.json').write_text(json.dumps(selected_obj,indent=2))
(OUT/'v019r_candidates.json').write_text(json.dumps(candidate_objects,indent=2))

cov_arr=np.array([[r[3],r[4],r[5],r[6]] for r in coverage],float)
summary={
 'traced_histories':len(histories),
 'validation_cases':len(val_cases),
 'active_source_H_over_H0_range':[float(cov_arr[:,0].min()),float(cov_arr[:,1].max())],
 'active_source_k_over_aH_range':[float(cov_arr[:,2].min()),float(cov_arr[:,3].max())],
 'tauH0_values':TAUS,
 'reference_orders':[REF_LO,REF_HI],
 'reference_convergence':ref_metrics,
 'candidate_orders':CANDIDATES,
 'selected_N':selected,
 'selected_metrics':candidate_objects[str(selected)]['metrics'] if selected is not None else None,
 'positive_measure_identity':'(2/pi) dω/(1+ω²) = (2/pi) dθ under ω=tanθ',
 'time_stepper':'exact linear-drive damped-oscillator propagation with cancellation-safe overdamped branch',
 'classification':classification,
 'gate_status':gate_status,
}
(OUT/'v019r_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
