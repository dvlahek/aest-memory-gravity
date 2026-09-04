#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

R=Path('results')
def load(n):
    p=R/n
    return json.loads(p.read_text()) if p.exists() else {}

tr=load('v019q_trace_patch.json')
sm=load('v019q_summary.json')
sel=load('v019q_selected_bath.json')

if sm.get('gate_status')=='PASS':
    overall='PASS_CLASS_TRAJECTORY_FIXED_BATH'
else:
    overall='CLASS_TRAJECTORY_BATH_NEEDS_REFINEMENT'

gates=[
 {'id':'Q1','name':'eta=0 CLASS chi trajectory trace','status':'PASS' if tr.get('classification')=='ETA0_CLASS_CHI_TRACE_PATCH' else 'UNKNOWN'},
 {'id':'Q2','name':'dense continuum reference convergence','status':'PASS' if sm.get('dense_reference_convergence',{}).get('max',1)<3e-4 else 'CHECK'},
 {'id':'Q3','name':'held-out source-weighted positive bath validation','status':sm.get('gate_status','UNKNOWN')},
 {'id':'Q4','name':'overall source-informed bath gate','status':overall},
]

next_step=(
 'Patch the selected fixed-frequency bath into CLASS and compute a tangent eta=0 memory response before finite-eta subtraction tests.'
 if overall=='PASS_CLASS_TRAJECTORY_FIXED_BATH' else
 'Use the traced held-out failures to refine the fixed-frequency grid/reference. Do not optimize against an artificial uniform complex box.'
)

out={
 'gates':gates,
 'overall_classification':overall,
 'trace_and_fit_summary':sm,
 'selected_bath':sel,
 'next_step':next_step,
 'finite_eta_CMB_interpretation_allowed':False,
 'important_methodological_result':'The reduction target is the actual eta=0 CLASS chi history, not a uniform near-imaginary complex-frequency box where any finite conservative oscillator discretization develops narrow resonances.',
 'frozen_results_unaffected':['continuum Drude construction','eta=0 AeST CLASS baseline','leading AeST adiabatic IC','smooth-source 1/3 drag law and Airy coefficient'],
}
R.mkdir(exist_ok=True)
(R/'MASTER_V019Q_REPORT.json').write_text(json.dumps(out,indent=2))
lines=['AeST MEMORY CLASS-TRAJECTORY SOURCE-WEIGHTED BATH v0.19q','='*94]
for g in gates:
    lines.append(f"{g['id']:4s}| {g['status']:42s}| {g['name']}")
lines += ['',f'OVERALL: {overall}','NEXT: '+next_step]
(R/'MASTER_V019Q_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019q.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('v019q*')):
        if p.is_file():z.write(p,arcname=p.name)
    for p in [R/'MASTER_V019Q_REPORT.json',R/'MASTER_V019Q_REPORT.txt']:
        if p.exists():z.write(p,arcname=p.name)
print((R/'MASTER_V019Q_REPORT.txt').read_text())
print('Created results_bundle_v019q.zip')
