#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('prep39',ROOT/'v039'/'prepare_locked_tau_case.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

MULTS=(-2.0,-1.0,1.0,2.0)

def mt(x): return ('p' if x>0 else 'm')+str(abs(int(x)))

def change(params,p,mult):
    kind,h=m.HALF[p]; d=mult*h
    if p=='lnA_s': return {'A_s':params['A_s']*math.exp(d)}
    base=params[p]
    return {p:base*(1+d) if kind=='fractional' else base+d}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--meta',required=True)
    z=ap.parse_args(); dst=Path(z.class_root).resolve(); base=(ROOT/m.BASE).read_text(); params=dict(m.PARAMS)
    made=[]; tag='kb0p0665_tau10_p0'
    for p in m.HALF:
        for mult in MULTS:
            ch=change(params,p,mult)
            suf=mt(mult)
            text=m.rewrite(base,f'output/v046_{tag}_nuis_{p}_{suf}_',m.KB_LOCK,params,10.0,ch).replace(
                'v0.39 locked-KB accepted-grid positive-Drude tau-generality case',
                'v0.46 locked-model five-point nuisance derivative certification')
            fn=f'v046_{tag}_nuis_{p}_{suf}.ini'; (dst/fn).write_text(text); made.append(fn)
    text=m.rewrite(base,f'output/v046_{tag}_base_',m.KB_LOCK,params,10.0,{}).replace(
        'v0.39 locked-KB accepted-grid positive-Drude tau-generality case',
        'v0.46 locked-model five-point nuisance derivative certification')
    fn=f'v046_{tag}_base.ini'; (dst/fn).write_text(text); made.append(fn)
    meta={'classification':'V046_PREPARED_FIVEPOINT','KB':m.KB_LOCK,'tauH0':10.0,'multipliers':list(MULTS),
          'parameters':list(m.HALF),'base_half_steps':m.HALF,'locked_refitted_parameters':params,'made_files':made,
          'purpose':'compare central two-point and fourth-order five-point nuisance derivatives at the locked model; no physics or parameter retuning'}
    q=Path(z.meta); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(meta,indent=2)); print(json.dumps(meta,indent=2))
if __name__=='__main__': main()
