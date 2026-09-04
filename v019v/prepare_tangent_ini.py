#!/usr/bin/env python3
from pathlib import Path
import argparse

BASE='v019/ini/aest_exp.ini'
CASES={
 'n39_e0':(39,0.0,'p3'),
 'n39_p03':(39,0.03,'p3'),
 'n39_m03':(39,-0.03,'p3'),
 'n39_p01':(39,0.01,'p3'),
 'n39_m01':(39,-0.01,'p3'),
 'n39_p003':(39,0.003,'p3'),
 'n39_m003':(39,-0.003,'p3'),
 'n47_p01':(47,0.01,'p3'),
 'n47_m01':(47,-0.01,'p3'),
 'n39_p01_p4':(39,0.01,'p4'),
 'n39_m01_p4':(39,-0.01,'p4'),
}


def rewrite(text,root,order,eta):
    out=[];root_found=False;seen_bg=False;seen_th=False
    for line in text.splitlines():
        s=line.strip()
        if s.startswith('root ='):
            out.append(f'root = {root}');root_found=True
        else:
            out.append(line)
        if s.startswith('write_background ='):seen_bg=True
        if s.startswith('write_thermodynamics ='):seen_th=True
    if not root_found:raise RuntimeError('root line not found')
    if not seen_bg:out.append('write_background = yes')
    if not seen_th:out.append('write_thermodynamics = yes')
    out += [
      '# v0.19v signed-eta tangent-limit diagnostic only',
      'aest_memory_enabled = yes',
      f'aest_memory_order = {order}',
      f'aest_eta = {eta:.17g}',
      'aest_tau_H0 = 1',
    ]
    return '\n'.join(out)+'\n'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('class_root');args=ap.parse_args()
    repo=Path(__file__).resolve().parents[1];dst=Path(args.class_root).resolve()
    base=(repo/BASE).read_text()
    for label,(order,eta,precision) in CASES.items():
        name=f'v019v_exp_{label}.ini';root=f'output/v019v_exp_{label}_'
        (dst/name).write_text(rewrite(base,root,order,eta));print(name,precision)

if __name__=='__main__':main()
