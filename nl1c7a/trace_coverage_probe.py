#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,json,os,sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import v063.theory_response_map as v63

H0=float(v63.START['H0']); h=H0/100.0
K_H=np.geomspace(0.0015,1.2,128)
K_MPC=K_H*h
AI=0.02
BATCH_SIZE=24
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
    m=float(np.min(rel))
    sel=[x for x,e in zip(rows,rel) if e<=1e-12]
    return sel,m


def select(rows,k):
    sel,m=exact_rows(rows,k)
    if not sel: raise RuntimeError(f'k={k} missing; best rel={m}')
    return cluster(sel),m


def common_grid(modes):
    ref=modes[0]
    out=[ref]
    maxrel=0.0
    t0=np.array([x['tau'] for x in ref])
    for mm in modes[1:]:
        tt=np.array([x['tau'] for x in mm])
        if len(tt)!=len(t0):
            raise RuntimeError(f'native time count mismatch {len(t0)} vs {len(tt)}')
        rel=np.abs(tt-t0)/np.maximum(np.maximum(np.abs(tt),np.abs(t0)),1.0)
        maxrel=max(maxrel,float(np.max(rel)))
        if float(np.max(rel))>1e-12:
            raise RuntimeError(f'native tau mismatch {float(np.max(rel))}')
        aa=np.array([x['a'] for x in mm]); a0=np.array([x['a'] for x in ref])
        ar=np.abs(aa-a0)/np.maximum(np.maximum(np.abs(aa),np.abs(a0)),1e-300)
        maxrel=max(maxrel,float(np.max(ar)))
        if float(np.max(ar))>1e-12:
            raise RuntimeError(f'native a mismatch {float(np.max(ar))}')
        out.append(mm)
    return out,maxrel


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
          'output':'mTk', 'lensing':'no', 'aest_memory_enabled':'no','aest_eta':0.0,
          'k_output_values':', '.join(f'{k:.17g}' for k in k_batch),
          'P_k_max_h/Mpc':1.3, 'z_max_pk':60.0,
          'k_per_decade_for_pk':80.0,'k_per_decade_for_bao':560.0,
        })
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


def run_class_batched(trace):
    if trace.exists(): trace.unlink()
    trace.parent.mkdir(parents=True,exist_ok=True)
    kept=[]
    batch_reports=[]
    n_batches=int(np.ceil(len(K_MPC)/BATCH_SIZE))
    for ib in range(n_batches):
        lo=ib*BATCH_SIZE; hi=min((ib+1)*BATCH_SIZE,len(K_MPC))
        batch=np.asarray(K_MPC[lo:hi],dtype=float)
        tmp=trace.with_name(f'{trace.stem}_batch{ib+1:02d}{trace.suffix}')
        run_class_batch(tmp,batch)
        rows=read_trace(tmp)
        batch_max_miss=0.0
        batch_kept=0
        for k in batch:
            sel,m=exact_rows(rows,float(k))
            batch_max_miss=max(batch_max_miss,m)
            if not sel:
                raise RuntimeError(f'batch {ib+1}: requested k={k} missing; best rel={m}')
            kept.extend(sel); batch_kept+=len(sel)
        batch_reports.append({
            'batch':ib+1,'start_index':lo,'stop_index_exclusive':hi,
            'requested_count':int(len(batch)),'kept_rows':int(batch_kept),
            'requested_k_relative_miss_max':float(batch_max_miss),
        })
        tmp.unlink(missing_ok=True)
    with open(trace,'w') as f:
        f.write(' '.join(FIELDS)+'\n')
        for row in kept:
            f.write(' '.join(f'{row[k]:.17g}' for k in FIELDS)+'\n')
    return batch_reports


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--class-root',required=True); ap.add_argument('--trace-out',required=True); ap.add_argument('--json-out',required=True); args=ap.parse_args()
    trace=Path(args.trace_out); trace.parent.mkdir(parents=True,exist_ok=True)
    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True)
    batch_reports=run_class_batched(trace)
    rows=read_trace(trace)
    modes=[]; misses=[]
    for k in K_MPC:
        m,e=select(rows,float(k)); modes.append(m); misses.append(e)
    modes,gridrel=common_grid(modes)
    avec=np.array([x['a'] for x in modes[0]])
    window=(avec>=0.015)&(avec<=0.03)
    below=np.where(window & (avec<AI))[0]; above=np.where(window & (avec>AI))[0]; exact=np.where(np.abs(avec-AI)<=1e-14)[0]
    finite=True
    field_max_abs={}
    for fld in FIELDS[3:]:
        vals=np.array([[row[fld] for row in m] for m in modes],dtype=float)
        finite=finite and bool(np.all(np.isfinite(vals)))
        field_max_abs[fld]=float(np.max(np.abs(vals)))
    gates={
      'A4_all_requested_k_found':float(max(misses))<=1e-12,
      'A4_common_native_time_grid':gridrel<=1e-12,
      'A4_three_native_times_below_ai':len(below)>=3,
      'A4_three_native_times_above_ai':len(above)>=3,
      'A4_all_required_fields_finite':finite,
    }
    classification='NL1C7A_NATIVE_TRACE_COVERAGE_PASS' if all(gates.values()) else 'NL1C7A_NATIVE_TRACE_COVERAGE_FAIL'
    nearest=np.argsort(np.abs(avec-AI))[:8]
    result={
      'classification':classification,
      'scope':'C7A A3/A4 output-only eta0 accepted-source trace coverage; no interpolation, radial reconstruction, spherical evolution, or finite eta.',
      'repair05':{
        'diagnostic_batching_only':True,'batch_size':BATCH_SIZE,
        'n_batches':len(batch_reports),'batches':batch_reports,
        'interpolation_used':False,'nearest_neighbour_substitution_used':False,
      },
      'CLASS_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540',
      'H0_km_s_Mpc':H0,'h':h,'a_i':AI,
      'k_grid_h_Mpc':K_H.tolist(),
      'k_grid_Mpc_inv':K_MPC.tolist(),
      'requested_k_relative_miss_max':float(max(misses)),
      'native_time_grid_relative_mismatch_max':gridrel,
      'n_native_times':int(len(avec)),
      'window_0p015_0p03':{'below_ai':int(len(below)),'above_ai':int(len(above)),'exact_ai':int(len(exact))},
      'nearest_native_a':[float(avec[i]) for i in nearest],
      'field_max_abs':field_max_abs,
      'all_fields_finite':finite,
      'gates':gates,
    }
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if all(gates.values()) else 1)

if __name__=='__main__': main()
