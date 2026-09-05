#!/usr/bin/env python3
from pathlib import Path
import argparse, json, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
REF_P=0.0
REF_MARG=0.1364941527698679

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir'); ap.add_argument('--tag',required=True); ap.add_argument('--kb',type=float,required=True)
    ap.add_argument('--tau0H0',type=float,required=True); ap.add_argument('--p',type=float,required=True)
    ap.add_argument('--force-control',required=True); ap.add_argument('--force-primary',required=True)
    ap.add_argument('--json-out',required=True); ap.add_argument('--prefix',default='v040')
    z=ap.parse_args()
    with tempfile.NamedTemporaryFile(suffix='.json',delete=False) as tf: tmp=tf.name
    cmd=[sys.executable,str(ROOT/'v032'/'analyse_transition_case.py'),z.output_dir,'--tag',z.tag,'--kb',str(z.kb),
         '--prefix',z.prefix,'--force-control',z.force_control,'--force-primary',z.force_primary,'--json-out',tmp]
    subprocess.run(cmd,check=True)
    res=json.loads(Path(tmp).read_text()); Path(tmp).unlink(missing_ok=True)
    res['classification']='V040_EVOLVING_TAU_GENERALITY_PASS'
    res['tau0H0']=z.tau0H0; res['p']=z.p
    res['tau_eff_law']='tau_eff(a) H0 = tau0H0 * (H(a)/H0)^(-p)'
    res['purpose']='test time-dependent positive/passive Drude memory at pre-locked KB=0.0665 and tau0H0=10'
    res['locked_KB']=0.0665; res['locked_tau0H0']=10.0
    res['locked_v038_run']=33969456272; res['constant_tau_v039_run']=33972545591
    marg=res['memory_candidate_covariance']['marginalized_CV_SNR_per_unit_eta']
    if abs(z.p-REF_P)<1e-12:
        rel=abs(marg-REF_MARG)/REF_MARG
        reg=bool(rel<0.01)
        res['p0_v039_regression']={'reference':REF_MARG,'measured':marg,'relative_difference':rel,'gate':reg}
        res['gates']['p0_v039_regression']=reg
        if not reg: res['classification']='V040_P0_REGRESSION_FAIL'
    else:
        res['p0_v039_regression']=None
    numerical=all(bool(v) for v in res['gates'].values())
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not numerical: raise SystemExit(2)

if __name__=='__main__': main()
