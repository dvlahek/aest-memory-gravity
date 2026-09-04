#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

R=Path('results')
def load(n):
    p=R/n
    return json.loads(p.read_text()) if p.exists() else {}

c=load('complex_kernel_audit_summary.json')
s=load('spectral_identity_summary.json')
t=load('time_domain_drive_summary.json')
q=load('positive_quadrature_scan_summary.json')

complex_controlled=bool(c.get('N20_complex_controlled',False))
if (s.get('gate_status')=='PASS' and t.get('gate_status')=='PASS' and not complex_controlled):
    classification='FINITE_BATH_IMPLEMENTATION_CORRECT_BUT_COMPLEX_AXIS_UNDERRESOLVED'
    status='PASS_DIAGNOSTIC'
elif (s.get('gate_status')=='PASS' and t.get('gate_status')=='PASS' and complex_controlled):
    classification='CURRENT_FINITE_BATH_COMPLEX_AXIS_CONTROLLED'
    status='PASS'
else:
    classification='BATH_AUDIT_NEEDS_DEBUGGING'
    status='CHECK'

gates=[
 {'id':'V19K-1','name':'Existing N16/N20 complex-frequency audit','status':c.get('gate_status','UNKNOWN')},
 {'id':'V19K-2','name':'Exact positive continuum identity on complex branch','status':s.get('gate_status','UNKNOWN')},
 {'id':'V19K-3','name':'Time-domain oscillator vs finite transfer function','status':t.get('gate_status','UNKNOWN')},
 {'id':'V19K-4','name':'Positive high-order quadrature convergence scan','status':q.get('gate_status','UNKNOWN')},
 {'id':'V19K-5','name':'Overall interpretation','status':status},
]

report={
 'classification':classification,
 'gate_status':status,
 'gates':gates,
 'current_N20':c.get('N20',{}),
 'quadrature_scan':q,
 'interpretation':(
   'The field equations and finite oscillator implementation are internally correct, while the real-axis optimized N16/N20 bath is not sufficiently converged for oscillatory complex-frequency cosmology. The v0.19j CMB nonlinearity/order failure should therefore not be interpreted as physical memory behavior.'
   if classification.startswith('FINITE_BATH_IMPLEMENTATION_CORRECT') else
   'See individual gates.'
 ),
 'next':(
   'Replace the N16/N20 CLASS realization before another finite-eta CMB sweep. Prefer either a substantially higher-order positive continuum quadrature with a demonstrated complex-domain tolerance, or a passive rational/diffusive approximation designed directly on the retarded complex-frequency domain. Then repeat eta-linearity using tangent response.'
   if not complex_controlled else
   'Proceed to a precision-controlled small-eta CLASS response test.'
 ),
 'unaffected':['1/3 galactic drag law','Airy coefficient','conservative continuum Drude construction','eta=0 AeST CLASS baseline'],
}
R.mkdir(exist_ok=True)
(R/'MASTER_V019K_REPORT.json').write_text(json.dumps(report,indent=2))
lines=['AeST MEMORY COMPLEX-FREQUENCY BATH AUDIT v0.19k','='*92]
for g in gates: lines.append(f"{g['id']:8s}| {g['status']:38s}| {g['name']}")
lines += ['',f'CLASSIFICATION: {classification}','NEXT: '+report['next']]
(R/'MASTER_V019K_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019k.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('*')):
        if p.is_file():z.write(p,arcname=p.name)
print((R/'MASTER_V019K_REPORT.txt').read_text())
print('Created results_bundle_v019k.zip')
