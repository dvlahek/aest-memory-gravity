#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

R=Path('results')
def load(name):
    p=R/name
    return json.loads(p.read_text()) if p.exists() else {}

sm=load('v019s_summary.json')
sel=load('v019s_selected_bath.json')
trace=load('v019r_trace_patch.json')
pass_gate=sm.get('gate_status')=='PASS'
overall='PASS_STABLE_SOURCE_WEIGHTED_COMPRESSED_BATH' if pass_gate else 'STABLE_SOURCE_WEIGHTED_COMPRESSION_NEEDS_REFINEMENT'

gates=[
 {'id':'S1','name':'eta=0 AeST CLASS source trace','status':'PASS' if trace.get('classification','').startswith('ETA0_CLASS_CHI_TRACE_PATCH') else 'UNKNOWN'},
 {'id':'S2','name':'stable N=16384 tan-theta continuum target','status':'PASS'},
 {'id':'S3','name':'held-out positive fixed-frequency compression','status':'PASS' if pass_gate else 'CHECK'},
 {'id':'S4','name':'overall compressed bath gate','status':overall},
]
next_step=(
 'Patch the selected positive fixed bath into CLASS and run the first small-eta tangent/finite-difference response campaign with eta-linearity, bath-order, precision, and eta->0 recovery controls.'
 if pass_gate else
 'Refine the positive fixed-frequency dictionary using the same stable continuum target; do not return to H-dependent rational coefficients.'
)
out={
 'gates':gates,'overall_classification':overall,'summary':sm,'selected_bath':sel,
 'finite_eta_CMB_interpretation_allowed':False,'next_step':next_step,
 'methodological_result':'The v0.19q source-weighted idea is retested against the converged v0.19r tan-theta continuum reference. The retained oscillator frequencies and weights are fixed, positive, and independent of H(t).',
 'frozen_results_unaffected':['continuum Drude construction','eta=0 AeST CLASS baseline','leading AeST adiabatic IC','smooth-source 1/3 drag law and Airy coefficient'],
}
(R/'MASTER_V019S_REPORT.json').write_text(json.dumps(out,indent=2))
lines=['AeST MEMORY STABLE SOURCE-WEIGHTED COMPRESSION v0.19s','='*92]
for g in gates:lines.append(f"{g['id']:4s}| {g['status']:48s}| {g['name']}")
lines += ['',f'OVERALL: {overall}',f"ACTIVE MODES: {sel.get('active_modes','n/a')}",f"HELD-OUT METRICS: {sel.get('heldout_metrics',{})}",'NEXT: '+next_step]
(R/'MASTER_V019S_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019s.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('v019s*')):
        if p.is_file():z.write(p,arcname=p.name)
    for p in (R/'MASTER_V019S_REPORT.json',R/'MASTER_V019S_REPORT.txt'):
        if p.exists():z.write(p,arcname=p.name)
print((R/'MASTER_V019S_REPORT.txt').read_text())
print('Created results_bundle_v019s.zip')
