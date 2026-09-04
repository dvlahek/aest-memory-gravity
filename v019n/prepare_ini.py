#!/usr/bin/env python3
from pathlib import Path
import argparse


def rewrite(text,root,null_states):
    out=[]
    root_found=False
    gauge_found=False
    for line in text.splitlines():
        s=line.strip()
        if s.startswith('root ='):
            out.append(f'root = {root}')
            root_found=True
        else:
            out.append(line)
        if s == 'gauge = newtonian':
            gauge_found=True
            if null_states:
                out.append('aest_null_states = yes')
    if not root_found or not gauge_found:
        raise RuntimeError('required root/gauge anchor missing')
    # Add thermodynamics output to strengthen the null comparison.
    out.append('write_thermodynamics = yes')
    return '\n'.join(out)+'\n'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('class_root')
    args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1]
    dst=Path(args.class_root).resolve()
    base=(repo/'v019'/'ini'/'cdm_newtonian.ini').read_text()
    for level in ('p0','p3'):
        for model,null_states in [('cdm',False),('null',True)]:
            name=f'v019n_{model}_{level}.ini'
            root=f'output/v019n_{model}_{level}_'
            (dst/name).write_text(rewrite(base,root,null_states))
            print(name)

if __name__=='__main__':
    main()
