#!/usr/bin/env python3
from pathlib import Path
import argparse

KS='1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1,3e-1'


def rewrite(text,root):
    out=[];root_ok=False;seen_k=False
    for line in text.splitlines():
        s=line.strip()
        if s.startswith('root ='):
            out.append(f'root = {root}');root_ok=True
        elif s.startswith('k_output_values ='):
            if not seen_k:
                out.append(f'k_output_values = {KS}');seen_k=True
        else:
            out.append(line)
    if not root_ok:out.append(f'root = {root}')
    if not seen_k:out.append(f'k_output_values = {KS}')
    return '\n'.join(out)+'\n'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('class_root');args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1];dst=Path(args.class_root).resolve()
    for model,src in [('cosh','aest_cosh.ini'),('exp','aest_exp.ini')]:
        base=(repo/'v019'/'ini'/src).read_text()
        (dst/f'v019s_{model}.ini').write_text(rewrite(base,f'output/v019s_{model}_'))
        print(f'v019s_{model}.ini')

if __name__=='__main__':main()
