#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

R=Path('results')
def load(n):
    p=R/n
    return json.loads(p.read_text()) if p.exists() else {}

cx=load('v019o_complex_fit_summary.json')
tm=load('v019o_time_validation_summary.json')
pa=load('v019o_passivity_summary.json')

if cx.get('gate_status')=='PASS_COMPLEX' and tm.get('gate_status')=='PASS_TIME_DOMAIN' and pa.get('gate_status')=='PASS':
    overall='PASS_GLOBAL_FIXED_POSITIVE_BATH'
else:
    overall='FIXED_BATH_NEEDS_REFINEMENT'

gates=[
 {'id':'O1','name':'global retarded complex-domain fit','status':cx.get('gate_status','UNKNOWN')},
 {'id':'O2','name':'independent time-dependent-H validation','status':tm.get('gate_status','UNKNOWN')},
 {'id':'O3','name':'positive fixed-frequency/passivity audit','status':pa.get('gate_status','UNKNOWN')},
 {'id':'O4','name':'overall fixed-bath gate','status':overall},
]

next_step=(
 'Insert the selected fixed-frequency positive bath into CLASS and compute the eta=0 tangent memory response before finite-eta subtraction tests.'
 if overall=='PASS_GLOBAL_FIXED_POSITIVE_BATH' else
 'Refine the fixed-frequency node grid/weights using the failed validation cases; do not return to H-dependent rational coefficients.'
)

out={
 'gates':gates,
 'overall_classification':overall,
 'complex_fit':cx,
 'time_domain':tm,
 'passivity':pa,
 'next_step':next_step,
 'finite_eta_CMB_interpretation_allowed':False,
 'frozen_results_unaffected':['continuum Drude field theory','eta=0 CLASS baseline','leading AeST adiabatic initial conditions','smooth-source 1/3 drag law and Airy coefficient'],
}
R.mkdir(exist_ok=True)
(R/'MASTER_V019O_REPORT.json').write_text(json.dumps(out,indent=2))
lines=['AeST MEMORY GLOBAL FIXED-POSITIVE-BATH GATE v0.19o','='*92]
for g in gates:
    lines.append(f"{g['id']:4s}| {g['status']:40s}| {g['name']}")
lines += ['',f'OVERALL: {overall}','NEXT: '+next_step]
(R/'MASTER_V019O_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019o.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('v019o*')):
        if p.is_file():z.write(p,arcname=p.name)
    for p in [R/'MASTER_V019O_REPORT.json',R/'MASTER_V019O_REPORT.txt']:
        if p.exists():z.write(p,arcname=p.name)
print((R/'MASTER_V019O_REPORT.txt').read_text())
print('Created results_bundle_v019o.zip')
