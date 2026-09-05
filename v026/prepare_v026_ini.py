#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math
BASE='v019/ini/aest_exp.ini'
POINTS=[('p05_t01',0.5,0.1),('p05_t1',0.5,1.0),('p05_t10',0.5,10.0),('p05_t100',0.5,100.0),('p1_t01',1.0,0.1),('p1_t1',1.0,1.0),('p1_t10',1.0,10.0),('p1_t100',1.0,100.0)]
LAM=[1,3,10,30,100,300,1000]
PARAMS={'H0':67.32117,'omega_b':0.02238280,'omega_cdm':0.1201075,'tau_reio':0.05430842,'n_s':0.9660499,'A_s':2.100549e-09}
HALF={'H0':('fractional',0.0025),'omega_b':('fractional',0.005),'omega_cdm':('fractional',0.005),'tau_reio':('absolute',0.0015),'n_s':('absolute',0.003),'lnA_s':('log',0.01)}

def rewrite(text,root,changes=None):
    changes=dict(changes or {}); out=[]; seen=set()
    for line in text.splitlines():
        s=line.strip(); key=s.split('=',1)[0].strip() if '=' in s else None
        if s.startswith('root ='): out.append(f'root = {root}')
        elif s.startswith('output ='): out.append('output = tCl,pCl')
        elif s.startswith('lensing ='): out.append('lensing = no')
        elif key in changes: out.append(f'{key} = {changes[key]:.17g}'); seen.add(key)
        else: out.append(line)
    if set(changes)-seen: raise RuntimeError(f'missing parameter lines: {sorted(set(changes)-seen)}')
    out += ['# v0.26 tau0 tracking sweep','aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0','aest_tau_H0 = 1']
    return '\n'.join(out)+'\n'

def change(p,sgn):
    kind,h=HALF[p]
    if p=='lnA_s': return {'A_s':PARAMS['A_s']*math.exp(sgn*h)}
    base=PARAMS[p]; return {p:base*(1+sgn*h) if kind=='fractional' else base+sgn*h}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--meta',default='results/v026_meta.json'); z=ap.parse_args()
    repo=Path(__file__).resolve().parents[1]; dst=Path(z.class_root).resolve(); base=(repo/BASE).read_text(); cases={'base':{}}
    for tag,_,_ in POINTS:
        for L in LAM:
            cases[f'{tag}_l{L}_p']={}; cases[f'{tag}_l{L}_m']={}
    for q in HALF: cases[f'nuis_{q}_p']=change(q,1); cases[f'nuis_{q}_m']=change(q,-1)
    for label,ch in cases.items(): (dst/f'v026_{label}.ini').write_text(rewrite(base,f'output/v026_{label}_',ch))
    q=Path(z.meta); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps({'points':[{'tag':t,'p':p,'tau0H0':x} for t,p,x in POINTS],
      'lambdas':LAM,'half_steps':HALF,'definition':'tau_eff H0=tau0H0*(H/H0)^(-p)'},indent=2))
if __name__=='__main__': main()
