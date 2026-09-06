#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('lm',ROOT/'v050'/'refit_lm_multistart.py')
lm=importlib.util.module_from_spec(spec); spec.loader.exec_module(lm)

# Exact verified v0.50 endpoints from run 34014387686.  These are the only starts.
ENDPOINTS={
 'canonical': {'H0':67.37744236949891,'omega_b':0.022376986332963984,'omega_cdm':0.11994442335627246,'tau_reio':0.05933868889756233,'n_s':0.9671022447212743,'A_s':2.1194914193201632e-9},
 'plus': {'H0':67.38197104438457,'omega_b':0.02237253541916958,'omega_cdm':0.1199241507218672,'tau_reio':0.06920453880300305,'n_s':0.9676892371634201,'A_s':2.1605288188307727e-9},
 'minus': {'H0':67.33593121049695,'omega_b':0.02237058396058767,'omega_cdm':0.1200452288425074,'tau_reio':0.022952617208201645,'n_s':0.9673607545960584,'A_s':1.9705601532340805e-9},
 'cross': {'H0':67.3114837653117,'omega_b':0.02236867680726204,'omega_cdm':0.12010862728864526,'tau_reio':0.07019550448504268,'n_s':0.9673221642456696,'A_s':2.1659893789620195e-9},
}

# Reuse the certified v0.50 implementation verbatim; only replace its deterministic start dictionary
# with the verified v0.50 endpoints. Physics, objective, FD steps, damping ladder, line search,
# trust caps and convergence logic are therefore unchanged.
lm.STARTS={k:dict(v) for k,v in ENDPOINTS.items()}

if __name__=='__main__':
    lm.main()
