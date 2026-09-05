#!/usr/bin/env python3
from pathlib import Path
import argparse, math, json

BASE='v019/ini/aest_exp.ini'
HALF={'H0':('fractional',0.0025),'omega_b':('fractional',0.005),'omega_cdm':('fractional',0.005),'tau_reio':('absolute',0.0015),'n_s':('absolute',0.003),'lnA_s':('log',0.01)}
LAM=[1,3,10,30,100,300,1000]

def ptag(x): return ('%.6g'%x).replace('.','p').replace('-','m')

def change(params,p,sgn):
    kind,h=HALF[p]
    if p=='lnA_s': return {'A_s':params['A_s']*math.exp(sgn*h)}
    base=params[p]
    return {p:base*(1+sgn*h) if kind=='fractional' else base+sgn*h}

def rewrite(text,root,kb,params,changes=None):
    changes=dict(params,**dict(changes or {})); changes['aest_KB']=kb
    out=[]; seen=set()
    for line in text.splitlines():
        s=line.strip(); key=s.split('=',1)[0].strip() if '=' in s else None
        if s.startswith('root ='): out.append(f'root = {root}')
        elif s.startswith('output ='): out.append('output = tCl,pCl')
        elif s.startswith('lensing ='): out.append('lensing = no')
        elif key in changes:
            out.append(f'{key} = {changes[key]:.17g}'); seen.add(key)
        else: out.append(line)
    miss=set(changes)-seen
    if miss: raise RuntimeError(f'missing parameter lines {sorted(miss)}')
    out += ['# v0.38 accepted-grid positive-Drude tangent at freshly refitted cosmology',
            'aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0','aest_tau_H0 = 10']
    return '\n'.join(out)+'\n'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--kb',type=float,required=True)
    ap.add_argument('--refit-json',required=True); ap.add_argument('--meta',required=True)
    a=ap.parse_args(); refit=json.loads(Path(a.refit_json).read_text())
    if abs(float(refit['KB'])-a.kb)>1e-10: raise RuntimeError('refit KB does not match requested KB')
    params=dict(refit['best_parameters'])
    repo=Path(__file__).resolve().parents[1]; dst=Path(a.class_root).resolve(); base=(repo/BASE).read_text(); tag='kb'+ptag(a.kb)
    cases={'base':{},'ref':{}}
    for L in LAM: cases[f'l{L}_p']={}; cases[f'l{L}_m']={}
    for p in HALF: cases[f'nuis_{p}_p']=change(params,p,1); cases[f'nuis_{p}_m']=change(params,p,-1)
    for label,ch in cases.items():
        kb=0.1 if label=='ref' else a.kb
        (dst/f'v038_{tag}_{label}.ini').write_text(rewrite(base,f'output/v038_{tag}_{label}_',kb,params,ch))
    q=Path(a.meta); q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps({'tag':tag,'KB':a.kb,'tauH0':10.0,'refitted_parameters':params,
      'refit_baseline_CV_SNR':refit['best_verified_baseline_CV_SNR'],'refit_parameter_shifts':refit['parameter_shifts'],
      'lambdas':LAM,'half_steps':HALF,'purpose':'dense critical-window scan with fresh nonlinear six-parameter refit followed by accepted-grid positive-Drude memory tangent at the same refitted cosmology'},indent=2))
    print(tag)
if __name__=='__main__': main()
