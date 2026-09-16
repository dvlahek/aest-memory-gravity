#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, json, os, sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import v063.theory_response_map as v63

H0=float(v63.START['H0']); h=H0/100.0
K_H=np.geomspace(0.0015,1.2,128); K_MPC=K_H*h
AI=0.02; BATCH_SIZE=24; SAMPLE_STEP=0.025
FIELDS=['k','tau','a','H_Mpc_inv','H_over_H0','chi','Q','rhoA','KQ','KQQ','delta_b','theta_b','delta_A','theta_A','alpha_A','E_A','Phi','Phi_prime','Psi']


def read_trace(path):
    rows=[]
    with open(path,newline='') as f:
        rd=csv.DictReader(f,delimiter=' ')
        if rd.fieldnames != FIELDS:
            raise RuntimeError(f'trace header mismatch: {rd.fieldnames}')
        for rr in rd:
            if None in rr or any(rr[k] in (None,'') for k in FIELDS):
                continue
            rows.append({k:float(rr[k]) for k in FIELDS})
    if not rows: raise RuntimeError('empty extended trace')
    return rows


def cluster(rows):
    rr=sorted(rows,key=lambda x:x['tau']); groups=[]; cur=[]; center=None
    for row in rr:
        t=row['tau']
        if center is None or abs(t-center)<=1e-12*max(abs(t),abs(center),1.0):
            cur.append(row); center=float(np.median([x['tau'] for x in cur]))
        else:
            groups.append(cur); cur=[row]; center=t
    if cur: groups.append(cur)
    return [{k:float(np.median([x[k] for x in g])) for k in FIELDS} for g in groups]


def exact_rows(rows,k):
    rel=np.array([abs(x['k']-k)/max(abs(k),1e-300) for x in rows])
    m=float(np.min(rel)); sel=[x for x,e in zip(rows,rel) if e<=1e-12]
    return sel,m


def select(rows,k):
    sel,m=exact_rows(rows,k)
    if not sel: raise RuntimeError(f'k={k} missing; best rel={m}')
    return cluster(sel),m


def common_grid(modes):
    ref=modes[0]; t0=np.array([x['tau'] for x in ref]); maxrel=0.0
    for mm in modes[1:]:
        tt=np.array([x['tau'] for x in mm])
        if len(tt)!=len(t0): raise RuntimeError(f'native time count mismatch {len(t0)} vs {len(tt)}')
        rel=np.abs(tt-t0)/np.maximum(np.maximum(np.abs(tt),np.abs(t0)),1.0)
        if float(np.max(rel))>1e-12: raise RuntimeError(f'native tau mismatch {float(np.max(rel))}')
        aa=np.array([x['a'] for x in mm]); a0=np.array([x['a'] for x in ref])
        ar=np.abs(aa-a0)/np.maximum(np.maximum(np.abs(aa),np.abs(a0)),1e-300)
        if float(np.max(ar))>1e-12: raise RuntimeError(f'native a mismatch {float(np.max(ar))}')
        maxrel=max(maxrel,float(np.max(rel)),float(np.max(ar)))
    return maxrel


def run_class_batch(trace,k_batch):
    from classy import Class
    if trace.exists(): trace.unlink()
    saved={k:os.environ.get(k) for k in ['AEST_OFFLINE_TRACE_FILE','AEST_TANGENT_FORCE_FILE','AEST_TANGENT_LAMBDA','OMP_NUM_THREADS']}
    c=None
    try:
        os.environ['AEST_OFFLINE_TRACE_FILE']=str(trace.resolve())
        os.environ.pop('AEST_TANGENT_FORCE_FILE',None); os.environ.pop('AEST_TANGENT_LAMBDA',None)
        os.environ['OMP_NUM_THREADS']='1'
        pars=dict(v63.class_params())
        pars.update({
          'output':'mTk','lensing':'no','aest_memory_enabled':'no','aest_eta':0.0,
          'k_output_values':', '.join(f'{k:.17g}' for k in k_batch),
          'P_k_max_h/Mpc':1.3,'z_max_pk':60.0,
          'k_per_decade_for_pk':80.0,'k_per_decade_for_bao':560.0,
          'perturbations_sampling_stepsize':SAMPLE_STEP,
        })
        # Repair01 changes source-function sampling only. It intentionally does
        # not override perturbations_integration_stepsize or integration tolerances.
        forbidden={'perturbations_integration_stepsize','tol_perturbations_integration'}
        if forbidden & set(pars):
            raise RuntimeError(f'Repair01 forbidden integration override present: {forbidden & set(pars)}')
        c=Class(); c.set(pars); c.compute()
        c.get_transfer_and_k_and_z(output_format='class',h_units=False)
        c.struct_cleanup(); c.empty(); c=None
    finally:
        if c is not None:
            try: c.struct_cleanup(); c.empty()
            except Exception: pass
        for k,v in saved.items():
            if v is None: os.environ.pop(k,None)
            else: os.environ[k]=v
    if not trace.exists() or trace.stat().st_size==0:
        raise RuntimeError(f'extended trace not produced for {trace.name}')


def run_batched(trace):
    trace.parent.mkdir(parents=True,exist_ok=True); kept=[]; reports=[]
    for ib,lo in enumerate(range(0,len(K_MPC),BATCH_SIZE),start=1):
        hi=min(lo+BATCH_SIZE,len(K_MPC)); batch=np.asarray(K_MPC[lo:hi],float)
        tmp=trace.with_name(f'{trace.stem}_batch{ib:02d}{trace.suffix}')
        run_class_batch(tmp,batch); rows=read_trace(tmp); maxmiss=0.0; nkept=0
        for k in batch:
            sel,m=exact_rows(rows,float(k)); maxmiss=max(maxmiss,m)
            if not sel: raise RuntimeError(f'batch {ib}: requested k={k} missing; best rel={m}')
            kept.extend(sel); nkept+=len(sel)
        reports.append({'batch':ib,'requested_count':int(len(batch)),'kept_rows':int(nkept),'requested_k_relative_miss_max':float(maxmiss)})
        tmp.unlink(missing_ok=True)
    with open(trace,'w') as f:
        f.write(' '.join(FIELDS)+'\n')
        for row in kept: f.write(' '.join(f'{row[k]:.17g}' for k in FIELDS)+'\n')
    return reports


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--class-root',required=True); ap.add_argument('--trace-out',required=True); ap.add_argument('--json-out',required=True); args=ap.parse_args()
    trace=Path(args.trace_out); out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True)
    batches=run_batched(trace); rows=read_trace(trace)
    modes=[]; misses=[]
    for k in K_MPC:
        m,e=select(rows,float(k)); modes.append(m); misses.append(e)
    gridrel=common_grid(modes); avec=np.array([x['a'] for x in modes[0]])
    window=(avec>=0.015)&(avec<=0.03); below=np.where(window&(avec<AI))[0]; above=np.where(window&(avec>AI))[0]
    finite=True
    for fld in FIELDS[3:]:
        vals=np.array([[row[fld] for row in m] for m in modes],float); finite &= bool(np.all(np.isfinite(vals)))
    gates={
      'R3_all_128_exact_k':len(modes)==128 and float(max(misses))<=1e-12,
      'R3_common_native_time_grid':gridrel<=1e-12,
      'R3_more_than_historical_46_native_times':len(avec)>46,
      'R3_at_least_8_below_ai':len(below)>=8,
      'R3_at_least_8_above_ai':len(above)>=8,
      'R3_all_fields_finite':finite,
    }
    classification='NL1C7A_NATIVE_TRACE_COVERAGE_PASS' if all(gates.values()) else 'NL1C7A_REPAIR01_NATIVE_DENSITY_FAIL'
    nearest=np.argsort(np.abs(avec-AI))[:12]
    result={
      'classification':classification,
      'repair01':{'source_sampling_only':True,'perturbations_sampling_stepsize':SAMPLE_STEP,'historical_default':0.1,
                  'perturbations_integration_stepsize_overridden':False,'integration_tolerance_overridden':False,
                  'diagnostic_batching_only':True,'batch_size':BATCH_SIZE,'n_batches':len(batches),'batches':batches,
                  'interpolation_used':False,'nearest_neighbour_substitution_used':False},
      'CLASS_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540','H0_km_s_Mpc':H0,'h':h,'a_i':AI,
      'k_grid_h_Mpc':K_H.tolist(),'k_grid_Mpc_inv':K_MPC.tolist(),
      'requested_k_relative_miss_max':float(max(misses)),'native_time_grid_relative_mismatch_max':gridrel,
      'n_native_times':int(len(avec)),'historical_n_native_times':46,
      'window_0p015_0p03':{'below_ai':int(len(below)),'above_ai':int(len(above))},
      'nearest_native_a':[float(avec[i]) for i in nearest], 'all_fields_finite':bool(finite),'gates':gates,
    }
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if all(gates.values()) else 2)

if __name__=='__main__': main()
