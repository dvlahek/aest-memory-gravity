#!/usr/bin/env python3
from pathlib import Path
import sys, types

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'v050'/'refit_lm_multistart.py'
text=SRC.read_text()

# Exact verified v0.50 endpoints from run 34014387686. These are the only starts.
ENDPOINTS={
 'canonical': {'H0':67.37744236949891,'omega_b':0.022376986332963984,'omega_cdm':0.11994442335627246,'tau_reio':0.05933868889756233,'n_s':0.9671022447212743,'A_s':2.1194914193201632e-9},
 'plus': {'H0':67.38197104438457,'omega_b':0.02237253541916958,'omega_cdm':0.1199241507218672,'tau_reio':0.06920453880300305,'n_s':0.9676892371634201,'A_s':2.1605288188307727e-9},
 'minus': {'H0':67.33593121049695,'omega_b':0.02237058396058767,'omega_cdm':0.1200452288425074,'tau_reio':0.022952617208201645,'n_s':0.9673607545960584,'A_s':1.9705601532340805e-9},
 'cross': {'H0':67.3114837653117,'omega_b':0.02236867680726204,'omega_cdm':0.12010862728864526,'tau_reio':0.07019550448504268,'n_s':0.9673221642456696,'A_s':2.1659893789620195e-9},
}

# All four v0.50 members terminated with trust_scale=0.25.  Preserve that
# optimizer state instead of silently restarting the trust region at 1.0.
TERMINAL_TRUST_SCALE=0.25

old="params=dict(STARTS[z.start]); initial=dict(params); history=[]; best=None; trust_scale=1.0; stagnant=0"
new=f"params=dict(STARTS[z.start]); initial=dict(params); history=[]; best=None; trust_scale={TERMINAL_TRUST_SCALE!r}; stagnant=0"
if text.count(old)!=1:
    raise RuntimeError('expected unique v0.50 trust-state initialization; refusing silent solver drift')
text=text.replace(old,new,1)

# Give continuation runs their own CLASS/output tag while leaving the objective,
# damping ladder, line search, finite-difference construction, bounds and trust
# update logic unchanged.
old_tag="tag=f'v050_{z.start}'"
new_tag="tag=f'v052_{z.start}'"
if text.count(old_tag)!=1:
    raise RuntimeError('expected unique v0.50 output tag; refusing silent solver drift')
text=text.replace(old_tag,new_tag,1)

lm=types.ModuleType('v050_lm_v052_continuation')
lm.__file__=str(SRC)
lm.__package__=None
exec(compile(text,str(SRC),'exec'),lm.__dict__)
lm.STARTS={k:dict(v) for k,v in ENDPOINTS.items()}

if __name__=='__main__':
    lm.main()
