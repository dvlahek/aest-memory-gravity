#!/usr/bin/env python3
from pathlib import Path
import argparse, math, json

BASE='v019/ini/aest_exp.ini'
PARAMS={'H0':67.32117,'omega_b':0.02238280,'omega_cdm':0.1201075,
        'tau_reio':0.05430842,'n_s':0.9660499,'A_s':2.100549e-09}
HALF={
    'H0':('fractional',0.0025),
    'omega_b':('fractional',0.005),
    'omega_cdm':('fractional',0.005),
    'tau_reio':('absolute',0.0015),
    'n_s':('absolute',0.003),
    'lnA_s':('log',0.01),
}

def rewrite(text,root,tau,memory_enabled=False,order=512,changes=None):
    changes=dict(changes or {})
    out=[]; replaced=set()
    for line in text.splitlines():
        s=line.strip(); key=s.split('=',1)[0].strip() if '=' in s else None
        if s.startswith('root ='): out.append(f'root = {root}')
        elif s.startswith('output ='): out.append('output = tCl,pCl')
        elif s.startswith('lensing ='): out.append('lensing = no')
        elif key in changes:
            out.append(f'{key} = {changes[key]:.17g}'); replaced.add(key)
        else: out.append(line)
    missing=set(changes)-replaced
    if missing: raise RuntimeError(f'missing parameter lines: {sorted(missing)}')
    out += [
      '# v0.21 tau sweep',
      f'aest_memory_enabled = {"yes" if memory_enabled else "no"}',
      f'aest_memory_order = {order}',
      'aest_eta = 0',
      f'aest_tau_H0 = {tau:.17g}',
    ]
    return '\n'.join(out)+'\n'

def change(param,sign):
    kind,h=HALF[param]
    if param=='lnA_s': return {'A_s':PARAMS['A_s']*math.exp(sign*h)}
    base=PARAMS[param]
    if kind=='fractional': val=base*(1.0+sign*h)
    elif kind=='absolute': val=base+sign*h
    else: raise RuntimeError(kind)
    return {param:val}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('class_root'); ap.add_argument('--tau',type=float,required=True); ap.add_argument('--tag',required=True)
    ap.add_argument('--meta',default=None)
    args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1]; dst=Path(args.class_root).resolve(); base=(repo/BASE).read_text()
    tau=args.tau; tag=args.tag
    cases={
      'trace256':(True,256,{}),
      'trace512':(True,512,{}),
      'force_l0':(False,512,{}),
      'force_p300':(False,512,{}),
      'force_m300':(False,512,{}),
      'force_p1000':(False,512,{}),
      'force_m1000':(False,512,{}),
    }
    for label,(mem,order,ch) in cases.items():
        name=f'v021_{label}.ini'; root=f'output/v021_{label}_'
        (dst/name).write_text(rewrite(base,root,tau,mem,order,ch)); print(name)
    for p in HALF:
        for sign,sgn in ((1,'p'),(-1,'m')):
            label=f'nuis_{p}_{sgn}'; name=f'v021_{label}.ini'; root=f'output/v021_{label}_'
            (dst/name).write_text(rewrite(base,root,tau,False,512,change(p,sign))); print(name)
    meta={'tauH0':tau,'tag':tag,'nuisance_parameters':list(HALF),'half_steps':HALF}
    if args.meta:
        q=Path(args.meta); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(meta,indent=2))

if __name__=='__main__': main()
