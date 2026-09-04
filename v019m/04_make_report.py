#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

R=Path('results')
def load(n):
    p=R/n
    return json.loads(p.read_text()) if p.exists() else {}

cov=load('v019m_coverage.json')
na=load('v019m_nonautonomous_summary.json')
fx=load('v019m_fixed_oscillator_summary.json')

if na.get('classification','').startswith('FAIL'):
    overall='TIME_DEPENDENT_RATIONAL_NOT_VALIDATED'
elif cov.get('gate_status')=='COVERAGE_EXTENSION_REQUIRED':
    overall='LOCAL_TIME_DEPENDENT_PASS_BUT_CMB_COVERAGE_EXTENSION_REQUIRED'
else:
    overall='PASS_TIME_DEPENDENT_MEMORY_REALIZATION'

refconv=na.get('reference_convergence_max_relative_L2',1)
gates=[
 {'id':'M1','name':'v0.19l Htau coverage for full CMB history','status':cov.get('gate_status','UNKNOWN')},
 {'id':'M2','name':'dense conservative reference convergence','status':'PASS' if refconv<5e-4 else 'CHECK'},
 {'id':'M3','name':'instantaneous N24 rational under time-dependent H','status':na.get('classification','UNKNOWN')},
 {'id':'M4','name':'positive fixed-oscillator fallback candidate','status':fx.get('classification','UNKNOWN')},
 {'id':'M5','name':'overall recommendation','status':overall},
]

next_step=(
 'Do not insert the H-dependent frozen rational table into CLASS. Use the exact time-dependent conservative bath structure and reduce its positive spectral measure directly, or derive the missing Hdot/state-transport terms of a non-autonomous diffusive realization.'
 if overall=='TIME_DEPENDENT_RATIONAL_NOT_VALIDATED' else
 'Extend the validated Htau domain to the full CLASS history, then run a tangent finite-eta CLASS test.'
)

out={
 'gates':gates,
 'overall_classification':overall,
 'coverage':cov,
 'nonautonomous':na,
 'fixed_oscillator_candidate':fx,
 'next_step':next_step,
 'frozen_results_unaffected':['continuum Drude construction','v0.19l frozen-H positive Stieltjes identity','eta=0 CLASS baseline','leading AeST adiabatic IC','smooth-source 1/3 drag law and Airy coefficient'],
 'finite_eta_CMB_interpretation_allowed':False,
}
R.mkdir(exist_ok=True)
(R/'MASTER_V019M_REPORT.json').write_text(json.dumps(out,indent=2))
lines=['AeST MEMORY TIME-DEPENDENT-H AUDIT v0.19m','='*88]
for g in gates:
    lines.append(f"{g['id']:4s}| {g['status']:48s}| {g['name']}")
lines += ['',f'OVERALL: {overall}','NEXT: '+next_step]
(R/'MASTER_V019M_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019m.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('*')):
        if p.is_file():z.write(p,arcname=p.name)
print((R/'MASTER_V019M_REPORT.txt').read_text())
print('Created results_bundle_v019m.zip')
