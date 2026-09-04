#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

R=Path('results')
def load(name):
    p=R/name
    return json.loads(p.read_text()) if p.exists() else {}

a=load('diffusive_identity_summary.json')
b=load('passive_table_summary.json')
c=load('passive_interpolation_summary.json')
d=load('passivity_summary.json')

gates=[
 {'id':'V19L-1','name':'Exact fixed-H positive diffusive identity','status':a.get('gate_status','UNKNOWN')},
 {'id':'V19L-2','name':'N24 complex-domain nonnegative anchor fit','status':b.get('gate_status','UNKNOWN')},
 {'id':'V19L-3','name':'97-anchor log-H interpolation','status':c.get('gate_status','UNKNOWN')},
 {'id':'V19L-4','name':'Positive-real/passivity audit','status':d.get('gate_status','UNKNOWN')},
 {'id':'V19L-5','name':'Time-dependent H realization vs conservative bath','status':'NEXT_HARD_GATE'},
 {'id':'V19L-6','name':'Finite-eta CLASS tangent response','status':'BLOCKED_AFTER_V19L_5'}
]
passed=all(g['status']=='PASS' for g in gates[:4])
classification='PASS_LOCAL_PASSIVE_RATIONAL' if passed else 'PASSIVE_RATIONAL_NEEDS_FOLLOWUP'
report={
 'classification':classification,
 'gates':gates,
 'central_result':'For fixed H, the Hubble-dressed Drude kernel is exactly a positive Debye/Stieltjes superposition. A 24-mode nonnegative rational table can approximate the tested complex retarded domain with sub-1e-3 target accuracy if the interpolation gate passes.',
 'important_caveat':'The coefficients depend on H(t). A local constant-H transfer-function fit is not automatically equivalent to the original covariant conservative bath when H varies on the memory timescale.',
 'next':'Validate a non-autonomous first-order realization on radiation-to-matter H(t) against a high-order conservative oscillator bath before replacing the CLASS finite bath.'
}
R.mkdir(exist_ok=True)
(R/'MASTER_V019L_REPORT.json').write_text(json.dumps(report,indent=2))
lines=['AeST MEMORY PASSIVE RATIONAL DESIGN v0.19l','='*88]
for g in gates:
    lines.append(f"{g['id']:8s}| {g['status']:34s}| {g['name']}")
lines += ['',f'CLASSIFICATION: {classification}',report['central_result'],'CAVEAT: '+report['important_caveat'],'NEXT: '+report['next']]
(R/'MASTER_V019L_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019l.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('*')):
        if p.is_file(): z.write(p,arcname=p.name)
print((R/'MASTER_V019L_REPORT.txt').read_text())
print('Created results_bundle_v019l.zip')
