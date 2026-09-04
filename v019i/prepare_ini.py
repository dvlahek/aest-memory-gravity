#!/usr/bin/env python3
from pathlib import Path
import argparse

LEVELS=('s0','c1','c2','s1','s2','s3')
MODELS={
 'cdm':'v019/ini/cdm_newtonian.ini',
 'exp':'v019/ini/aest_exp.ini',
 'cosh':'v019/ini/aest_cosh.ini',
}


def rewrite(text,root,model):
    out=[];found=False
    for line in text.splitlines():
        if line.strip().startswith('root ='):
            out.append(f'root = {root}')
            found=True
        else:
            out.append(line)
    if not found:raise RuntimeError('root line not found')
    out.append('write_thermodynamics = yes')
    return '\n'.join(out)+'\n'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('class_root');args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1]
    dst=Path(args.class_root).resolve();dst.mkdir(parents=True,exist_ok=True)
    for model,rel in MODELS.items():
        base=(repo/rel).read_text()
        for level in LEVELS:
            name=f'v019i_{model}_{level}.ini'
            root=f'output/v019i_{model}_{level}_'
            (dst/name).write_text(rewrite(base,root,model))
            print(name)

if __name__=='__main__':main()
