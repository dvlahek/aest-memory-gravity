#!/usr/bin/env python3
from pathlib import Path
import argparse, math, json

BASE='v019/ini/aest_exp.ini'

PARAMS={
    'H0': 67.32117,
    'omega_b': 0.02238280,
    'omega_cdm': 0.1201075,
    'tau_reio': 0.05430842,
    'n_s': 0.9660499,
    'A_s': 2.100549e-09,
}

# full step and half step.  A_s is differentiated with respect to ln A_s.
STEPS={
    'H0': {'kind':'fractional','full':0.005,'half':0.0025},
    'omega_b': {'kind':'fractional','full':0.01,'half':0.005},
    'omega_cdm': {'kind':'fractional','full':0.01,'half':0.005},
    'tau_reio': {'kind':'absolute','full':0.003,'half':0.0015},
    'n_s': {'kind':'absolute','full':0.006,'half':0.003},
    'lnA_s': {'kind':'log','full':0.02,'half':0.01},
}


def rewrite(text,root,memory_enabled=False,order=39,changes=None):
    changes=dict(changes or {})
    out=[]; seen_root=False; seen_output=False; seen_lensing=False
    replaced=set()
    for line in text.splitlines():
        s=line.strip()
        key=s.split('=',1)[0].strip() if '=' in s else None
        if s.startswith('root ='):
            out.append(f'root = {root}'); seen_root=True
        elif s.startswith('output ='):
            out.append('output = tCl,pCl'); seen_output=True
        elif s.startswith('lensing ='):
            out.append('lensing = no'); seen_lensing=True
        elif key in changes:
            out.append(f'{key} = {changes[key]:.17g}'); replaced.add(key)
        elif s.startswith('write_background =') or s.startswith('write_parameters ='):
            out.append(line)
        else:
            out.append(line)
    if not seen_root: raise RuntimeError('root line not found')
    if not seen_output: out.append('output = tCl,pCl')
    if not seen_lensing: out.append('lensing = no')
    missing=set(changes)-replaced
    if missing: raise RuntimeError(f'parameter lines not found: {sorted(missing)}')
    out += [
        '# v0.20 core-LambdaCDM projection / revolution gate',
        f'aest_memory_enabled = {"yes" if memory_enabled else "no"}',
        f'aest_memory_order = {order}',
        'aest_eta = 0',
        'aest_tau_H0 = 1',
    ]
    return '\n'.join(out)+'\n'


def value_for(param, sign, stepname):
    st=STEPS[param][stepname]
    if param=='lnA_s':
        return {'A_s': PARAMS['A_s']*math.exp(sign*st)}
    base=PARAMS[param]
    kind=STEPS[param]['kind']
    if kind=='fractional': val=base*(1.0+sign*st)
    elif kind=='absolute': val=base+sign*st
    else: raise RuntimeError(kind)
    return {param:val}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--steps-json',default=None); args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1]; dst=Path(args.class_root).resolve(); base=(repo/BASE).read_text()

    cases={
        'trace39': dict(memory_enabled=True,order=39,changes={}),
        'force_l0': dict(memory_enabled=False,order=39,changes={}),
        'force_p300': dict(memory_enabled=False,order=39,changes={}),
        'force_m300': dict(memory_enabled=False,order=39,changes={}),
        'force_p1000': dict(memory_enabled=False,order=39,changes={}),
        'force_m1000': dict(memory_enabled=False,order=39,changes={}),
    }
    for label,cfg in cases.items():
        name=f'v020_{label}.ini'; root=f'output/v020_{label}_'
        (dst/name).write_text(rewrite(base,root,**cfg)); print(name)

    for param in STEPS:
        for stepname in ('full','half'):
            for sign,labelsign in ((1,'p'),(-1,'m')):
                changes=value_for(param,sign,stepname)
                label=f'{param}_{stepname}_{labelsign}'
                name=f'v020_{label}.ini'; root=f'output/v020_{label}_'
                (dst/name).write_text(rewrite(base,root,False,39,changes)); print(name,changes)

    meta={'base_parameters':PARAMS,'steps':STEPS,
          'derivative_parameters':['H0','omega_b','omega_cdm','tau_reio','n_s','lnA_s']}
    if args.steps_json:
        p=Path(args.steps_json); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(meta,indent=2))

if __name__=='__main__': main()
