#!/usr/bin/env python3
from pathlib import Path
import argparse, json, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
REF_TAU=10.0
REF_MARG=0.1364941527698679

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir'); ap.add_argument('--tag',required=True); ap.add_argument('--kb',type=float,required=True)
    ap.add_argument('--tauH0',type=float,required=True); ap.add_argument('--force-control',required=True); ap.add_argument('--force-primary',required=True)
    ap.add_argument('--json-out',required=True); ap.add_argument('--prefix',default='v039')
    z=ap.parse_args()
    with tempfile.NamedTemporaryFile(suffix='.json',delete=False) as tf: tmp=tf.name
    cmd=[sys.executable,str(ROOT/'v032'/'analyse_transition_case.py'),z.output_dir,'--tag',z.tag,'--kb',str(z.kb),
         '--prefix',z.prefix,'--force-control',z.force_control,'--force-primary',z.force_primary,'--json-out',tmp]
    subprocess.run(cmd,check=True)
    res=json.loads(Path(tmp).read_text()); Path(tmp).unlink(missing_ok=True)
    res['classification']='V039_TAU_GENERALITY_PASS'
    res['tauH0']=z.tauH0
    res['purpose']='test positive/passive Drude memory-timescale generality at pre-locked KB=0.0665 and fixed v0.38 refitted cosmology'
    res['locked_KB']=0.0665
    res['locked_v038_run']=33969456272
    marg=res['memory_candidate_covariance']['marginalized_CV_SNR_per_unit_eta']
    if abs(z.tauH0-REF_TAU)<1e-12:
        rel=abs(marg-REF_MARG)/REF_MARG
        reg=bool(rel<0.01)
        res['tau10_regression']={'reference':REF_MARG,'measured':marg,'relative_difference':rel,'gate':reg}
        res['gates']['tau10_v038_regression']=reg
        if not reg: res['classification']='V039_TAU10_REGRESSION_FAIL'
    else:
        res['tau10_regression']=None
    numerical=all(bool(v) for v in res['gates'].values())
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not numerical: raise SystemExit(2)

if __name__=='__main__': main()
