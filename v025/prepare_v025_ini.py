#!/usr/bin/env python3
from pathlib import Path
import math, json, argparse
BASE='v019/ini/aest_exp.ini'
PARAMS={'H0':67.32117,'omega_b':0.02238280,'omega_cdm':0.1201075,'tau_reio':0.05430842,'n_s':0.9660499,'A_s':2.100549e-09}
HALF={'H0':('fractional',0.0025),'omega_b':('fractional',0.005),'omega_cdm':('fractional',0.005),'tau_reio':('absolute',0.0015),'n_s':('absolute',0.003),'lnA_s':('log',0.01)}
LAM={'p0':[100,300,1000],'p05':[1,3,10,30,100,300,1000],'p1':[1,3,10,30,100,300,1000]}

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
    out += ['# v0.25 background-tracking memory tangent','aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0','aest_tau_H0 = 1']
    return '\n'.join(out)+'\n'

def change(p,sgn):
    kind,h=HALF[p]
    if p=='lnA_s': return {'A_s':PARAMS['A_s']*math.exp(sgn*h)}
    base=PARAMS[p]; val=base*(1+sgn*h) if kind=='fractional' else base+sgn*h
    return {p:val}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--meta',default='results/v025_meta.json'); a=ap.parse_args()
    repo=Path(__file__).resolve().parents[1]; dst=Path(a.class_root).resolve(); base=(repo/BASE).read_text()
    cases={'trace':{},'base':{}}
    for tag,lams in LAM.items():
        for lam in lams:
            cases[f'{tag}_l{lam}_p']={}; cases[f'{tag}_l{lam}_m']={}
    for p in HALF:
        cases[f'nuis_{p}_p']=change(p,1); cases[f'nuis_{p}_m']=change(p,-1)
    for label,ch in cases.items():
        (dst/f'v025_{label}.ini').write_text(rewrite(base,f'output/v025_{label}_',ch))
    q=Path(a.meta); q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps({'p_values':{'p0':0.0,'p05':0.5,'p1':1.0},'tau0H0':1.0,'lambdas':LAM,'half_steps':HALF,
      'definition':'tau_eff H0 = tau0H0*(H/H0)^(-p)','memory_runtime':'disabled; exact eta0 external variational forcing only'},indent=2))
if __name__=='__main__': main()
