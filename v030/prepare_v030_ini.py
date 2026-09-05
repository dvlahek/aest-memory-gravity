#!/usr/bin/env python3
from pathlib import Path
import argparse, math, json
COSH='v019/ini/aest_cosh.ini'; EXP='v019/ini/aest_exp.ini'
PARAMS={'H0':67.32117,'omega_b':0.02238280,'omega_cdm':0.1201075,'tau_reio':0.05430842,'n_s':0.9660499,'A_s':2.100549e-09}
HALF={'H0':('fractional',0.0025),'omega_b':('fractional',0.005),'omega_cdm':('fractional',0.005),'tau_reio':('absolute',0.0015),'n_s':('absolute',0.003),'lnA_s':('log',0.01)}
TAUS=[('t0001',0.001),('t0003',0.003),('t001',0.01),('t003',0.03),('t01',0.1),('t03',0.3),('t1',1.0),('t3',3.0),('t10',10.0)]
LAM=[30,100,300,1000]
def change(p,sgn):
    kind,h=HALF[p]
    if p=='lnA_s': return {'A_s':PARAMS['A_s']*math.exp(sgn*h)}
    base=PARAMS[p]; return {p:base*(1+sgn*h) if kind=='fractional' else base+sgn*h}
def rewrite(text,root,changes=None,tau=1.0):
    ch=dict(changes or {}); out=[]; seen=set()
    for line in text.splitlines():
        s=line.strip(); key=s.split('=',1)[0].strip() if '=' in s else None
        if s.startswith('root ='): out.append(f'root = {root}')
        elif s.startswith('output ='): out.append('output = tCl,pCl')
        elif s.startswith('lensing ='): out.append('lensing = no')
        elif key in ch: out.append(f'{key} = {ch[key]:.17g}'); seen.add(key)
        else: out.append(line)
    if set(ch)-seen: raise RuntimeError(f'missing parameter lines {sorted(set(ch)-seen)}')
    out += ['# v0.30 accepted-grid Cosh memory gate','aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0',f'aest_tau_H0 = {tau:.17g}']
    return '\n'.join(out)+'\n'
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--meta',required=True); z=ap.parse_args(); repo=Path(__file__).resolve().parents[1]; dst=Path(z.class_root).resolve(); cosh=(repo/COSH).read_text(); exp=(repo/EXP).read_text()
    (dst/'v030_cosh_base.ini').write_text(rewrite(cosh,'output/v030_cosh_base_',tau=1))
    (dst/'v030_exp_ref.ini').write_text(rewrite(exp,'output/v030_exp_ref_',tau=1))
    for p in HALF:
        (dst/f'v030_nuis_{p}_p.ini').write_text(rewrite(cosh,f'output/v030_nuis_{p}_p_',change(p,1)))
        (dst/f'v030_nuis_{p}_m.ini').write_text(rewrite(cosh,f'output/v030_nuis_{p}_m_',change(p,-1)))
    for tag,T in TAUS:
        for L in LAM:
            (dst/f'v030_{tag}_l{L}_p.ini').write_text(rewrite(cosh,f'output/v030_{tag}_l{L}_p_',tau=T))
            (dst/f'v030_{tag}_l{L}_m.ini').write_text(rewrite(cosh,f'output/v030_{tag}_l{L}_m_',tau=T))
    Path(z.meta).write_text(json.dumps({'model':'Cosh','benchmark_parameters':{'KB':0.5,'Q0':0.1,'K2':7500,'Z0':1e-9},'taus':TAUS,'lambdas':LAM,'reference':'Exp tauH0=1 forcing used only for numerical normalization'},indent=2))
if __name__=='__main__': main()
