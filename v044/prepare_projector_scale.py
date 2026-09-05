#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('prep39',ROOT/'v039'/'prepare_locked_tau_case.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

ALLOWED=(0.5,0.75,1.0,1.5,2.0)

def tag_scale(x): return ('%.6g'%x).replace('.','p').replace('-','m')

def change_scaled(params,p,sgn,scale):
    kind,h=m.HALF[p]; h*=scale
    if p=='lnA_s': return {'A_s':params['A_s']*math.exp(sgn*h)}
    base=params[p]
    return {p:base*(1+sgn*h) if kind=='fractional' else base+sgn*h}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('class_root')
    ap.add_argument('--scale',type=float,required=True)
    ap.add_argument('--meta',required=True)
    a=ap.parse_args()
    if a.scale not in ALLOWED: raise SystemExit(f'scale must be one of {ALLOWED}')
    dst=Path(a.class_root).resolve(); base=(ROOT/m.BASE).read_text(); params=dict(m.PARAMS)
    tag=f'kb0p0665_tau10_p0_s{tag_scale(a.scale)}'
    cases={'base':{},'ref':{},'l10_p':{},'l10_m':{}}
    for q in m.HALF:
        cases[f'nuis_{q}_p']=change_scaled(params,q,1,a.scale)
        cases[f'nuis_{q}_m']=change_scaled(params,q,-1,a.scale)
    for label,ch in cases.items():
        kb=0.1 if label=='ref' else m.KB_LOCK
        text=m.rewrite(base,f'output/v044_{tag}_{label}_',kb,params,10.0,ch).replace(
            'v0.39 locked-KB accepted-grid positive-Drude tau-generality case',
            'v0.44 locked-model whitened-SVD nuisance projector certification')
        (dst/f'v044_{tag}_{label}.ini').write_text(text)
    meta={'tag':tag,'KB':m.KB_LOCK,'tauH0':10.0,'p':0.0,'derivative_step_scale':a.scale,
          'base_half_steps':m.HALF,'locked_refitted_parameters':params,'locked_from_v038_run':m.V038_RUN,
          'purpose':'whitened-SVD nuisance-subspace/projector stability across pre-registered finite-difference scales; no model or cosmology retuning'}
    q=Path(a.meta); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(meta,indent=2)); print(tag)
if __name__=='__main__': main()
