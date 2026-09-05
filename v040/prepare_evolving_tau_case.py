#!/usr/bin/env python3
from pathlib import Path
import argparse, math, json

BASE='v019/ini/aest_exp.ini'
KB_LOCK=0.0665
TAU0H0_LOCK=10.0
PARAMS={'H0':67.3324639084866,'omega_b':0.022377376877682164,'omega_cdm':0.12006705327635288,'tau_reio':0.06174082364515668,'n_s':0.9666229454895277,'A_s':2.1308864352626987e-09}
HALF={'H0':('fractional',0.0025),'omega_b':('fractional',0.005),'omega_cdm':('fractional',0.005),'tau_reio':('absolute',0.0015),'n_s':('absolute',0.003),'lnA_s':('log',0.01)}
LAM=[1,3,10,30,100,300,1000]
V038_RUN=33969456272
V039_RUN=33972545591
V039_TAU10_MARG=0.1364941527698679

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
    out += ['# v0.40 locked-KB evolving positive-Drude memory case',
            'aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0',f'aest_tau_H0 = {TAU0H0_LOCK:.17g}']
    return '\n'.join(out)+'\n'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--p',type=float,required=True); ap.add_argument('--meta',required=True)
    a=ap.parse_args()
    if a.p<0: raise SystemExit('p must be nonnegative')
    repo=Path(__file__).resolve().parents[1]; dst=Path(a.class_root).resolve(); base=(repo/BASE).read_text()
    tag=f'kb0p0665_tau0H010_p{ptag(a.p)}'; params=dict(PARAMS)
    cases={'base':{},'ref':{}}
    for L in LAM: cases[f'l{L}_p']={}; cases[f'l{L}_m']={}
    for q in HALF: cases[f'nuis_{q}_p']=change(params,q,1); cases[f'nuis_{q}_m']=change(params,q,-1)
    for label,ch in cases.items():
        kb=0.1 if label=='ref' else KB_LOCK
        (dst/f'v040_{tag}_{label}.ini').write_text(rewrite(base,f'output/v040_{tag}_{label}_',kb,params,ch))
    meta={'tag':tag,'KB':KB_LOCK,'tau0H0':TAU0H0_LOCK,'p':a.p,
          'tau_eff_law':'tau_eff(a) H0 = tau0H0 * (H(a)/H0)^(-p)',
          'locked_refitted_parameters':params,'locked_from_v038_run':V038_RUN,'constant_tau_reference_run':V039_RUN,
          'v039_tau10_marginalized_CV_SNR_per_unit_eta':V039_TAU10_MARG,'lambdas':LAM,'half_steps':HALF,
          'purpose':'time-dependent positive/passive memory generality at pre-locked KB=0.0665 and tau0H0=10; no KB or tau0 retuning'}
    q=Path(a.meta); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(meta,indent=2)); print(tag)

if __name__=='__main__': main()
