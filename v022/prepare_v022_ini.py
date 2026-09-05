#!/usr/bin/env python3
from pathlib import Path
import math, json, argparse

BASE='v019/ini/aest_exp.ini'
TAUS=[('t0001',0.001),('t0003',0.003),('t001',0.01),('t003',0.03),('t01',0.1),('t03',0.3),('t1',1.0),('t3',3.0),('t10',10.0)]
PARAMS={'H0':67.32117,'omega_b':0.02238280,'omega_cdm':0.1201075,
        'tau_reio':0.05430842,'n_s':0.9660499,'A_s':2.100549e-09}
HALF={'H0':('fractional',0.0025),'omega_b':('fractional',0.005),
      'omega_cdm':('fractional',0.005),'tau_reio':('absolute',0.0015),
      'n_s':('absolute',0.003),'lnA_s':('log',0.01)}


def rewrite(text,root,changes=None):
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
      '# v0.22 offline-continuum variational sweep',
      'aest_memory_enabled = no',
      'aest_memory_order = 16',
      'aest_eta = 0',
      'aest_tau_H0 = 1',
    ]
    return '\n'.join(out)+'\n'


def change(param,sign):
    kind,h=HALF[param]
    if param=='lnA_s': return {'A_s':PARAMS['A_s']*math.exp(sign*h)}
    base=PARAMS[param]
    if kind=='fractional': val=base*(1.+sign*h)
    elif kind=='absolute': val=base+sign*h
    else: raise RuntimeError(kind)
    return {param:val}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--meta',default=None)
    args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1]; dst=Path(args.class_root).resolve(); base=(repo/BASE).read_text()

    cases={'trace':{},'base':{}}
    for tag,T in TAUS:
        for lab in ('p300','m300','p1000','m1000'):
            cases[f'{tag}_force_{lab}']={}
    for p in HALF:
        for sign,sgn in ((1,'p'),(-1,'m')):
            cases[f'nuis_{p}_{sgn}']=change(p,sign)

    for label,ch in cases.items():
        name=f'v022_{label}.ini'; root=f'output/v022_{label}_'
        (dst/name).write_text(rewrite(base,root,ch)); print(name)

    meta={'tau_points':TAUS,'nuisance_parameters':list(HALF),'half_steps':HALF,
          'memory_runtime':'disabled; response supplied only through exact eta=0 variational external forcing'}
    if args.meta:
        q=Path(args.meta); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(meta,indent=2))


if __name__=='__main__': main()
