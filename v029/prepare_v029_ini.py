#!/usr/bin/env python3
from pathlib import Path
import argparse, math, json
BASE='v019/ini/aest_exp.ini'
PARAMS={'H0':67.32117,'omega_b':0.02238280,'omega_cdm':0.1201075,'tau_reio':0.05430842,'n_s':0.9660499,'A_s':2.100549e-09}
HALF={'H0':('fractional',0.0025),'omega_b':('fractional',0.005),'omega_cdm':('fractional',0.005),'tau_reio':('absolute',0.0015),'n_s':('absolute',0.003),'lnA_s':('log',0.01)}
TAGS=['q0','q025','q05','q075','q1']; LAM=[30,100,300,1000]
def change(p,sgn):
    kind,h=HALF[p]
    if p=='lnA_s': return {'A_s':PARAMS['A_s']*math.exp(sgn*h)}
    base=PARAMS[p]; return {p:base*(1+sgn*h) if kind=='fractional' else base+sgn*h}
def rewrite(text,root,changes=None):
    ch=dict(changes or {}); out=[]; seen=set()
    for line in text.splitlines():
        s=line.strip(); key=s.split('=',1)[0].strip() if '=' in s else None
        if s.startswith('root ='): out.append(f'root = {root}')
        elif s.startswith('output ='): out.append('output = tCl,pCl')
        elif s.startswith('lensing ='): out.append('lensing = no')
        elif key in ch: out.append(f'{key} = {ch[key]:.17g}'); seen.add(key)
        else: out.append(line)
    if set(ch)-seen: raise RuntimeError(f'missing parameter lines {sorted(set(ch)-seen)}')
    out += ['# v0.29 running-coupling diagnostic','aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0','aest_tau_H0 = 10']
    return '\n'.join(out)+'\n'
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--meta',required=True); a=ap.parse_args(); repo=Path(__file__).resolve().parents[1]; dst=Path(a.class_root).resolve(); base=(repo/BASE).read_text(); cases={'base':{}}
    for tag in TAGS:
        for L in LAM: cases[f'{tag}_l{L}_p']={}; cases[f'{tag}_l{L}_m']={}
    for p in HALF: cases[f'nuis_{p}_p']=change(p,1); cases[f'nuis_{p}_m']=change(p,-1)
    for label,ch in cases.items(): (dst/f'v029_{label}.ini').write_text(rewrite(base,f'output/v029_{label}_',ch))
    Path(a.meta).write_text(json.dumps({'q_values':{'q0':0,'q025':0.25,'q05':0.5,'q075':0.75,'q1':1.0},'lambdas':LAM,'tauH0':10.0,'status':'phenomenological diagnostic, not final covariant model'},indent=2))
if __name__=='__main__': main()
