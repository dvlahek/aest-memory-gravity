#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

R=Path('results')
def load(name):
    p=R/name
    return json.loads(p.read_text()) if p.exists() else {}

apply=load('v019n_apply_report.json')
null=load('v019n_null.json')
build=load('v019n_build_report.json')
classification=null.get('classification','UNKNOWN')

gates=[
 {'id':'V19N-1','name':'v0.19 + structural-null patch application','status':'PASS' if apply.get('classification')=='STRICT_STRUCTURAL_NULL_PATCH' else 'UNKNOWN'},
 {'id':'V19N-2','name':'Patched CLASS compile','status':build.get('patched_build','UNKNOWN')},
 {'id':'V19N-3','name':'Standard CDM p0/p3 runs','status':build.get('cdm_runs','UNKNOWN')},
 {'id':'V19N-4','name':'Frozen-extra-state p0/p3 runs','status':build.get('null_runs','UNKNOWN')},
 {'id':'V19N-5','name':'Strict structural-null output comparison','status':null.get('gate_status','UNKNOWN')},
 {'id':'V19N-6','name':'Interpretation','status':classification},
]

report={
 'scope':'strict structural null at eta=0; memory remains off',
 'gates':gates,
 'classification':classification,
 'comparison':null,
 'previous_result':'v0.19p Exp-CDM primary TT/EE/TE residual = 6.855294693e-4 and unchanged across p0-p3 precision.',
 'caveat':'A structural-null PASS identifies the persistent v0.19p residual with the active eta=0 AeST proxy dynamics rather than ODE-vector dimension. It does not validate chi_i=0 as the exact AeST radiation-era adiabatic initial condition.',
 'next':'If strict null passes, freeze the numerical/software baseline and derive/test the true AeST radiation-era initial-condition mode before enabling memory eta>0.'
}
R.mkdir(exist_ok=True)
(R/'MASTER_V019N_REPORT.json').write_text(json.dumps(report,indent=2))
lines=['AeST ETA=0 STRICT STRUCTURAL-NULL TEST v0.19n','='*90]
for g in gates:
    lines.append(f"{g['id']:8s}| {g['status']:34s}| {g['name']}")
lines += ['',f'CLASSIFICATION: {classification}',report['caveat'],'NEXT: '+report['next']]
(R/'MASTER_V019N_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019n.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('v019n*')):
        if p.is_file():z.write(p,arcname=p.name)
    for p in [R/'MASTER_V019N_REPORT.json',R/'MASTER_V019N_REPORT.txt']:
        if p.exists():z.write(p,arcname=p.name)
print((R/'MASTER_V019N_REPORT.txt').read_text())
print('Created results_bundle_v019n.zip')
