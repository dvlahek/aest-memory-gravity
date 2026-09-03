#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

R=Path('results')
def load(name):
    p=R/name
    return json.loads(p.read_text()) if p.exists() else {}

prec=load('v019p_precision.json')
build=load('v019p_build_report.json')
summary=prec.get('summary',{})
classification=summary.get('classification','UNKNOWN')

gates=[
    {'id':'V19P-1','name':'v0.19 patched CLASS build','status':build.get('patched_build','UNKNOWN')},
    {'id':'V19P-2','name':'CDM precision ladder p0-p3','status':build.get('cdm_runs','UNKNOWN')},
    {'id':'V19P-3','name':'Exp quasi-null precision ladder p0-p3','status':build.get('exp_runs','UNKNOWN')},
    {'id':'V19P-4','name':'Cosh p0/p3 control','status':build.get('cosh_runs','UNKNOWN')},
    {'id':'V19P-5','name':'Precision convergence diagnostic','status':prec.get('gate_status','UNKNOWN')},
    {'id':'V19P-6','name':'Interpretation','status':classification},
]
report={
    'scope':'eta=0 precision convergence only; memory remains off',
    'gates':gates,
    'summary':summary,
    'caveat':'Exp is a quasi-null background control, not a strict null perturbation theory. chi_i=0 remains a regular proxy rather than the unpublished exact AeST radiation-era adiabatic IC.',
    'next':'If the residual is persistent, build a strict structural-null extra-state control before interpreting it as physical AeST. If numerical-floor dominated, freeze v0.19 after convergence.'
}
R.mkdir(exist_ok=True)
(R/'MASTER_V019P_REPORT.json').write_text(json.dumps(report,indent=2))
lines=['AeST ETA=0 PRECISION / QUASI-NULL TEST v0.19p','='*88]
for g in gates:
    lines.append(f"{g['id']:8s}| {g['status']:34s}| {g['name']}")
lines += ['',f"CLASSIFICATION: {classification}",report['caveat'],'NEXT: '+report['next']]
(R/'MASTER_V019P_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019p.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('v019p*')):
        if p.is_file(): z.write(p,arcname=p.name)
    for p in [R/'MASTER_V019P_REPORT.json',R/'MASTER_V019P_REPORT.txt']:
        if p.exists(): z.write(p,arcname=p.name)
print((R/'MASTER_V019P_REPORT.txt').read_text())
print('Created results_bundle_v019p.zip')
