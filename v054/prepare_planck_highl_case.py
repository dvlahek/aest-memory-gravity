#!/usr/bin/env python3
from pathlib import Path
import argparse, json

BASE='v019/ini/aest_exp.ini'
KB=0.0665
TAUH0=10.0
LAMBDA=10.0
# Locked v0.38/v0.39 cosmology. This first real-data profile is a fixed-cosmology
# preflight only; it is not the final six-parameter posterior.
PARAMS={'H0':67.3324639084866,'omega_b':0.022377376877682164,'omega_cdm':0.12006705327635288,
        'tau_reio':0.06174082364515668,'n_s':0.9666229454895277,'A_s':2.1308864352626987e-09}


def rewrite(text, root):
    changes=dict(PARAMS); changes['aest_KB']=KB
    out=[]; seen=set(); lens_seen=False; lmax_seen=False
    for line in text.splitlines():
        s=line.strip(); key=s.split('=',1)[0].strip() if '=' in s else None
        if s.startswith('root ='):
            out.append(f'root = {root}')
        elif s.startswith('output ='):
            out.append('output = tCl,pCl,lCl')
        elif s.startswith('lensing ='):
            out.append('lensing = yes'); lens_seen=True
        elif key == 'l_max_scalars':
            out.append('l_max_scalars = 2600'); lmax_seen=True
        elif key in changes:
            out.append(f'{key} = {changes[key]:.17g}'); seen.add(key)
        else:
            out.append(line)
    miss=set(changes)-seen
    if miss:
        raise RuntimeError(f'missing parameter lines {sorted(miss)}')
    if not lens_seen: out.append('lensing = yes')
    if not lmax_seen: out.append('l_max_scalars = 2600')
    out += [
      '# v0.54 pre-data technical adapter: lensed spectra required by Planck high-l likelihood',
      '# Primary finite-memory model remains locked; no parameter was selected from Planck data.',
      'aest_memory_enabled = no','aest_memory_order = 16','aest_eta = 0',f'aest_tau_H0 = {TAUH0:.17g}'
    ]
    return '\n'.join(out)+'\n'


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--meta',required=True)
    a=ap.parse_args(); repo=Path(__file__).resolve().parents[1]; dst=Path(a.class_root).resolve()
    base=(repo/BASE).read_text(); tag='kb0p0665_tau10_plancklensed'
    for label in ['base','l10_p','l10_m']:
        (dst/f'v054_{tag}_{label}.ini').write_text(rewrite(base,f'output/v054_{tag}_{label}_'))
    meta={
      'classification':'V054_PREDATA_PLANCK_HIGHL_PROFILE_DECLARATION',
      'locked_model_manifest':'v053/model_freeze.json','KB':KB,'tauH0':TAUH0,'p':0.0,'lambda':LAMBDA,
      'cosmology':PARAMS,'eta_grid':[-10,-7.5,-5,-2.5,0,2.5,5,7.5,10],
      'likelihood':'Planck 2018 Plik-lite TTTEEE native, nuisance-marginalized high-l',
      'calibration':'profile A_planck with N(1,0.0025) prior',
      'technical_extension':'Use lensed TT/TE/EE spectra because the real Planck high-l likelihood is defined for lensed theory spectra. Declared before any Planck likelihood value is read.',
      'scope':'first real-data fixed-cosmology eta profile; not final six-parameter cosmological marginalization',
      'anti_tuning':'No KB, tauH0, p, lambda, CLASS commit, patch chain or eta grid may be changed in response to this result.'
    }
    q=Path(a.meta); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(meta,indent=2)); print(tag)

if __name__=='__main__': main()
