#!/usr/bin/env python3
from pathlib import Path
import argparse

LEVELS = ('p0','p1','p2','p3')
MODELS = {
    'cdm': 'v019/ini/cdm_newtonian.ini',
    'exp': 'v019/ini/aest_exp.ini',
    'cosh': 'v019/ini/aest_cosh.ini',
}


def rewrite_root(text, root):
    out=[]
    found=False
    for line in text.splitlines():
        if line.strip().startswith('root ='):
            out.append(f'root = {root}')
            found=True
        else:
            out.append(line)
    if not found:
        raise RuntimeError('root line not found')
    return '\n'.join(out)+'\n'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('class_root')
    args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1]
    dst=Path(args.class_root).resolve()
    dst.mkdir(parents=True,exist_ok=True)
    for model,rel in MODELS.items():
        base=(repo/rel).read_text()
        levels=LEVELS if model in ('cdm','exp') else ('p0','p3')
        for level in levels:
            name=f'v019p_{model}_{level}.ini'
            root=f'output/v019p_{model}_{level}_'
            (dst/name).write_text(rewrite_root(base,root))
            print(name)

if __name__=='__main__':
    main()
