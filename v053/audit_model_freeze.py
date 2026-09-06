#!/usr/bin/env python3
from pathlib import Path
import json, math

ROOT = Path(__file__).resolve().parents[1]
F = json.loads((ROOT/'v053'/'model_freeze.json').read_text())

EXPECTED = {
    ('physics','KB'): 0.0665,
    ('physics','tauH0'): 10.0,
    ('physics','tau_evolution_p'): 0.0,
    ('physics','lambda_regularization'): 10.0,
    ('observable_scope','ell_min'): 30,
    ('observable_scope','ell_max'): 2500,
    ('pre_data_certification','locked_memory_marginalized_SNR_per_eta_tau10'): 0.1364941527698679,
    ('pre_data_certification','v050_v052_spread'): 0.6001539004913861,
    ('pre_data_certification','spread_gate'): 0.5,
}

fail=[]
for path,val in EXPECTED.items():
    x=F
    for k in path: x=x[k]
    if isinstance(val,float):
        if not math.isclose(float(x),val,rel_tol=0.0,abs_tol=1e-15): fail.append((path,x,val))
    elif x!=val: fail.append((path,x,val))

assert F['frozen_source_commit']=='5bf61cf74b315056ffd94d93ad71e44ba6f7dc3b'
assert F['theory_engine']['CLASS_commit']=='e85808324f51fc694d12e3ed7439552a3c3f9540'
assert F['observable_scope']['spectra']==['TT','TE','EE']
assert F['observable_scope']['lensed'] is False
assert F['nuisance_cosmology']['parameters']==['H0','omega_b','omega_cdm','tau_reio','n_s','lnA_s']
assert F['pre_data_certification']['spread_gate_passed'] is False
assert 'no change' in F['anti_tuning_rule'].lower()
if fail:
    raise SystemExit('freeze mismatch: '+repr(fail))

print(json.dumps({
    'classification':'V053_MODEL_FREEZE_AUDIT_PASS',
    'frozen_source_commit':F['frozen_source_commit'],
    'CLASS_commit':F['theory_engine']['CLASS_commit'],
    'KB':F['physics']['KB'],
    'tauH0':F['physics']['tauH0'],
    'p':F['physics']['tau_evolution_p'],
    'lambda':F['physics']['lambda_regularization'],
    'ell_range':[F['observable_scope']['ell_min'],F['observable_scope']['ell_max']],
    'nuisance_parameters':F['nuisance_cosmology']['parameters'],
    'anti_tuning_rule_locked':True
},indent=2))
