#!/usr/bin/env python3
from pathlib import Path
import argparse

MODELS={'cosh':'v019/ini/aest_cosh.ini','exp':'v019/ini/aest_exp.ini'}
CASES={
 'off':None,
 'n39_e0':(39,0.0),
 'n39_e003':(39,0.003),
 'n39_e01':(39,0.01),
 'n39_e03':(39,0.03),
 'n47_e0':(47,0.0),
 'n47_e01':(47,0.01),
}


def rewrite(text,root,case):
    out=[];root_found=False;seen_bg=False;seen_th=False
    for line in text.splitlines():
        s=line.strip()
        if s.startswith('root ='):
            out.append(f'root = {root}');root_found=True
        else:out.append(line)
        if s.startswith('write_background ='):seen_bg=True
        if s.startswith('write_thermodynamics ='):seen_th=True
    if not root_found:raise RuntimeError('root line not found')
    if not seen_bg:out.append('write_background = yes')
    if not seen_th:out.append('write_thermodynamics = yes')
    if case is not None:
        order,eta=case
        out += ['aest_memory_enabled = yes',f'aest_memory_order = {order}',f'aest_eta = {eta:.17g}','aest_tau_H0 = 1']
    return '\n'.join(out)+'\n'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('class_root');args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1];dst=Path(args.class_root).resolve()
    for model,rel in MODELS.items():
        base=(repo/rel).read_text()
        for label,case in CASES.items():
            name=f'v019u_{model}_{label}.ini';root=f'output/v019u_{model}_{label}_'
            (dst/name).write_text(rewrite(base,root,case));print(name)

if __name__=='__main__':main()
