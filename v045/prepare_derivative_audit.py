#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('prep39',ROOT/'v039'/'prepare_locked_tau_case.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

SCALES=(0.25,0.5,1.0,1.5,2.0)

def tag_scale(x): return ('%.6g'%x).replace('.','p').replace('-','m')

def change_scaled(params,p,sgn,scale):
    kind,h=m.HALF[p]; h*=scale
    if p=='lnA_s': return {'A_s':params['A_s']*math.exp(sgn*h)}
    base=params[p]
    return {p:base*(1+sgn*h) if kind=='fractional' else base+sgn*h}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--meta',required=True)
    z=ap.parse_args(); dst=Path(z.class_root).resolve(); base=(ROOT/m.BASE).read_text(); params=dict(m.PARAMS)
    made=[]
    for sc in SCALES:
        tag=f'kb0p0665_tau10_p0_s{tag_scale(sc)}'
        for p in m.HALF:
            for suffix,sgn in [('p',1),('m',-1)]:
                ch=change_scaled(params,p,sgn,sc)
                text=m.rewrite(base,f'output/v045_{tag}_nuis_{p}_{suffix}_',m.KB_LOCK,params,10.0,ch).replace(
                    'v0.39 locked-KB accepted-grid positive-Drude tau-generality case',
                    'v0.45 locked-model per-parameter nuisance derivative convergence audit')
                (dst/f'v045_{tag}_nuis_{p}_{suffix}.ini').write_text(text)
                made.append(f'v045_{tag}_nuis_{p}_{suffix}.ini')
    # Locked base only for covariance whitening.
    tag='kb0p0665_tau10_p0_s1'
    text=m.rewrite(base,f'output/v045_{tag}_base_',m.KB_LOCK,params,10.0,{}).replace(
        'v0.39 locked-KB accepted-grid positive-Drude tau-generality case',
        'v0.45 locked-model per-parameter nuisance derivative convergence audit')
    (dst/f'v045_{tag}_base.ini').write_text(text); made.append(f'v045_{tag}_base.ini')
    meta={'classification':'V045_PREPARED_DERIVATIVE_AUDIT','KB':m.KB_LOCK,'tauH0':10.0,
          'scales':list(SCALES),'parameters':list(m.HALF),'base_half_steps':m.HALF,
          'locked_refitted_parameters':params,'made_files':made,
          'purpose':'identify which nuisance finite-difference derivative is step dependent; no model or cosmology retuning'}
    q=Path(z.meta); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(meta,indent=2)); print(json.dumps(meta,indent=2))
if __name__=='__main__': main()
