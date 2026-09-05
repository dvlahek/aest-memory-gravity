#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math, sys

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v031refit',ROOT/'v031'/'refit_baseline.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

BASE=dict(r.START)

def shifted(**kw):
    q=dict(BASE)
    for k,v in kw.items():
        if k=='lnA_s': q['A_s']=BASE['A_s']*math.exp(v)
        else: q[k]=BASE[k]+v
    return q

STARTS={
  'canonical':dict(BASE),
  'plus':shifted(H0=1.5,omega_b=0.0004,omega_cdm=-0.004,tau_reio=0.010,n_s=-0.012,lnA_s=0.05),
  'minus':shifted(H0=-1.5,omega_b=-0.0004,omega_cdm=0.004,tau_reio=-0.010,n_s=0.012,lnA_s=-0.05),
  'cross':shifted(H0=1.0,omega_b=-0.0005,omega_cdm=0.005,tau_reio=0.008,n_s=0.015,lnA_s=-0.04),
}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('class_root')
    ap.add_argument('--kb',type=float,default=0.0665)
    ap.add_argument('--start',choices=sorted(STARTS),required=True)
    ap.add_argument('--iters',type=int,default=6)
    ap.add_argument('--json-out',required=True)
    a=ap.parse_args()
    r.START=dict(STARTS[a.start])
    tmp=str(Path(a.json_out).with_suffix('.raw.json'))
    old=sys.argv
    sys.argv=['refit_baseline.py',a.class_root,'--kb',str(a.kb),'--iters',str(a.iters),'--json-out',tmp]
    try: r.main()
    finally: sys.argv=old
    res=json.loads(Path(tmp).read_text()); Path(tmp).unlink(missing_ok=True)
    res['classification_v041']='V041_MULTISTART_REFIT_MEMBER'
    res['start_name']=a.start
    res['start_parameters_v041']=STARTS[a.start]
    res['locked_KB_v041']=0.0665
    res['locked_reference_run_v038']=33969456272
    Path(a.json_out).write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2))

if __name__=='__main__': main()
