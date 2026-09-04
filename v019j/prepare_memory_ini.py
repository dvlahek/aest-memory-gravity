#!/usr/bin/env python3
from pathlib import Path
import argparse

MODELS={'cosh':'v019/ini/aest_cosh.ini','exp':'v019/ini/aest_exp.ini'}
CASES={
 'off':None,
 'n16_e0_t1':(16,0.0,1.0),
 'n16_e01_t1':(16,0.01,1.0),
 'n16_e03_t1':(16,0.03,1.0),
 'n16_e10_t1':(16,0.10,1.0),
 'n20_e0_t1':(20,0.0,1.0),
 'n20_e03_t1':(20,0.03,1.0),
}


def rewrite(text,root,case):
    out=[];root_found=False
    for line in text.splitlines():
        s=line.strip()
        if s.startswith('root ='):
            out.append(f'root = {root}');root_found=True
        else:
            out.append(line)
    if not root_found:raise RuntimeError('root line not found')
    out += ['write_background = yes','write_thermodynamics = yes']
    if case is not None:
        order,eta,tau=case
        out += [
          'aest_memory_enabled = yes',
          f'aest_memory_order = {order}',
          f'aest_eta = {eta:.17g}',
          f'aest_tau_H0 = {tau:.17g}',
        ]
    return '\n'.join(out)+'\n'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('class_root');args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1];dst=Path(args.class_root).resolve()
    for model,rel in MODELS.items():
        base=(repo/rel).read_text()
        for label,case in CASES.items():
            name=f'v019j_{model}_{label}.ini';root=f'output/v019j_{model}_{label}_'
            (dst/name).write_text(rewrite(base,root,case));print(name)

if __name__=='__main__':main()
