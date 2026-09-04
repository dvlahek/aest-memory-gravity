#!/usr/bin/env python3
from pathlib import Path
import argparse

BASE='v019/ini/aest_exp.ini'

TRACE_CASES={
    'trace39':(39,'p3'),
}
FORCE_CASES={
    'force_l0':('p3',0.0),
    'force_p30':('p3',30.0),
    'force_m30':('p3',-30.0),
    'force_p100':('p3',100.0),
    'force_m100':('p3',-100.0),
    'force_p300':('p3',300.0),
    'force_m300':('p3',-300.0),
    'force_p1000':('p3',1000.0),
    'force_m1000':('p3',-1000.0),
    'force_p300_p4':('p4',300.0),
    'force_m300_p4':('p4',-300.0),
}


def rewrite(text,root,memory_enabled,order):
    out=[];seen_root=False;seen_output=False;seen_lensing=False
    for line in text.splitlines():
        s=line.strip()
        if s.startswith('root ='):
            out.append(f'root = {root}');seen_root=True
        elif s.startswith('output ='):
            out.append('output = tCl,pCl,mPk');seen_output=True
        elif s.startswith('lensing ='):
            out.append('lensing = no');seen_lensing=True
        elif s.startswith('write_thermodynamics ='):
            out.append('write_thermodynamics = yes')
        else:
            out.append(line)
    if not seen_root: raise RuntimeError('root line not found')
    if not seen_output: out.append('output = tCl,pCl,mPk')
    if not seen_lensing: out.append('lensing = no')
    out += [
        '# v0.19x eta=0 variational amplitude-ladder diagnostic',
        f'aest_memory_enabled = {"yes" if memory_enabled else "no"}',
        f'aest_memory_order = {order}',
        'aest_eta = 0',
        'aest_tau_H0 = 1',
    ]
    return '\n'.join(out)+'\n'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('class_root');args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1];dst=Path(args.class_root).resolve();base=(repo/BASE).read_text()
    for label,(order,precision) in TRACE_CASES.items():
        name=f'v019x_{label}.ini';root=f'output/v019x_{label}_';(dst/name).write_text(rewrite(base,root,True,order));print(name,precision,'trace',order)
    for label,(precision,lam) in FORCE_CASES.items():
        name=f'v019x_{label}.ini';root=f'output/v019x_{label}_';(dst/name).write_text(rewrite(base,root,False,39));print(name,precision,'force',lam)

if __name__=='__main__': main()
