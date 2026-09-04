#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

R=Path('results')
def load(n):
    p=R/n
    return json.loads(p.read_text()) if p.exists() else {}

tr=load('v019r_trace_patch.json')
sm=load('v019r_summary.json')
sel=load('v019r_selected_bath.json')

if sm.get('gate_status')=='PASS':
    overall='PASS_CLASS_TRAJECTORY_TAN_GL_BATH'
else:
    overall='TAN_GL_BATH_NEEDS_REFINEMENT'

gates=[
 {'id':'R1','name':'eta=0 CLASS chi trajectory trace','status':'PASS' if tr.get('classification')=='ETA0_CLASS_CHI_TRACE_PATCH_V019R' else 'UNKNOWN'},
 {'id':'R2','name':'8192 vs 16384 continuum reference convergence','status':'PASS' if sm.get('reference_convergence',{}).get('max',1)<2e-4 else 'CHECK'},
 {'id':'R3','name':'direct positive fixed-bath held-out validation','status':'PASS' if sm.get('selected_N') is not None and sm.get('selected_metrics',{}).get('max',1)<3e-3 else 'CHECK'},
 {'id':'R4','name':'overall stable Drude quadrature gate','status':overall},
]

next_step=(
 'Insert the selected direct positive fixed bath into CLASS and run a tangent finite-eta convergence campaign with eta-linearity, bath-order, precision, and eta->0 recovery controls.'
 if overall=='PASS_CLASS_TRAJECTORY_TAN_GL_BATH' else
 'Refine the theta quadrature or time-domain stepping before any finite-eta CLASS interpretation.'
)

out={
 'gates':gates,
 'overall_classification':overall,
 'summary':sm,
 'selected_bath':sel,
 'next_step':next_step,
 'finite_eta_CMB_interpretation_allowed':False,
 'numerical_correction':[
   'Use omega=tan(theta) so the Drude measure is uniform on a finite theta interval.',
   'Use exact linear-drive oscillator propagation rather than a piecewise-constant drive.',
   'Use a cancellation-safe overdamped root and expm1 evaluation in the omega->0 branch.'
 ],
 'structural_properties':['fixed positive frequencies','strictly positive quadrature weights','weights sum to unity','no fitted H-dependent coefficients'],
 'frozen_results_unaffected':['continuum Drude construction','eta=0 AeST CLASS baseline','leading AeST adiabatic IC','smooth-source 1/3 drag law and Airy coefficient'],
}
R.mkdir(exist_ok=True)
(R/'MASTER_V019R_REPORT.json').write_text(json.dumps(out,indent=2))
lines=['AeST MEMORY STABLE CLASS-TRAJECTORY DRUDE QUADRATURE v0.19r','='*96]
for g in gates:
    lines.append(f"{g['id']:4s}| {g['status']:42s}| {g['name']}")
lines += ['',f'OVERALL: {overall}','SELECTED N: '+str(sm.get('selected_N')),'NEXT: '+next_step]
(R/'MASTER_V019R_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019r.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('v019r*')):
        if p.is_file():z.write(p,arcname=p.name)
    for p in [R/'MASTER_V019R_REPORT.json',R/'MASTER_V019R_REPORT.txt']:
        if p.exists():z.write(p,arcname=p.name)
print((R/'MASTER_V019R_REPORT.txt').read_text())
print('Created results_bundle_v019r.zip')
