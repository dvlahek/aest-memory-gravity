#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('prep39',ROOT/'v039'/'prepare_locked_tau_case.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def ptag(x): return ('%.6g'%x).replace('.','p').replace('-','m')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--p',type=float,required=True); ap.add_argument('--tau0H0',type=float,default=10.0); ap.add_argument('--meta',required=True)
    a=ap.parse_args()
    if not (0<=a.p<=1 and a.tau0H0>0): raise SystemExit('require 0<=p<=1 and tau0H0>0')
    dst=Path(a.class_root).resolve(); base=(ROOT/m.BASE).read_text(); params=dict(m.PARAMS); tag=f'kb0p0665_tau0{ptag(a.tau0H0)}_p{ptag(a.p)}'
    cases={'base':{},'ref':{}}
    for L in m.LAM: cases[f'l{L}_p']={}; cases[f'l{L}_m']={}
    for q in m.HALF: cases[f'nuis_{q}_p']=m.change(params,q,1); cases[f'nuis_{q}_m']=m.change(params,q,-1)
    # CLASS memory remains disabled: v0.40 injects the positive Drude response through the validated external tangent forcing.
    for label,ch in cases.items():
        kb=0.1 if label=='ref' else m.KB_LOCK
        text=m.rewrite(base,f'output/v040_{tag}_{label}_',kb,params,a.tau0H0,ch).replace('v0.39 locked-KB accepted-grid positive-Drude tau-generality case','v0.40 locked-KB time-dependent positive-Drude memory case')
        (dst/f'v040_{tag}_{label}.ini').write_text(text)
    meta={'tag':tag,'KB':m.KB_LOCK,'tau0H0':a.tau0H0,'p':a.p,'tau_law':'tau_eff*H0=tau0H0*(H/H0)^(-p)',
          'locked_refitted_parameters':params,'locked_from_v038_run':m.V038_RUN,'lambdas':m.LAM,'half_steps':m.HALF,
          'p0_regression_target_v039_tau10_marginalized_CV_SNR_per_unit_eta':m.V038_TAU10_MARG,
          'purpose':'time-dependent memory generality at pre-locked KB=0.0665 and pre-locked nonlinear-refitted cosmology; no KB or cosmology retuning'}
    q=Path(a.meta); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(meta,indent=2)); print(tag)
if __name__=='__main__': main()
