#!/usr/bin/env python3
from pathlib import Path
import json,zipfile
R=Path('results')
def load(n):
    p=R/n;return json.loads(p.read_text()) if p.exists() else {}
sm=load('v019t_summary.json');sel=load('v019t_selected_bath.json')
overall='PASS_TAU1_COMPRESSED_POSITIVE_BATH' if sm.get('gate_status')=='PASS' else 'TAU1_COMPRESSION_NEEDS_REFINEMENT'
gates=[
 {'id':'T1','name':'eta=0 Cosh/Exp CLASS source trace','status':'PASS' if sm.get('traced_histories')==16 else 'CHECK'},
 {'id':'T2','name':'direct N=512 tauH0=1 control against N=16384 continuum','status':'PASS' if sm.get('direct_N512_control',{}).get('max',1)<1e-3 else 'CHECK'},
 {'id':'T3','name':'held-out compressed positive bath','status':'PASS' if sm.get('gate_status')=='PASS' else 'CHECK'},
 {'id':'T4','name':'overall tauH0=1 compression gate','status':overall},
]
next_step=('Patch the selected fixed positive bath into CLASS and run small-eta CMB response with same-bath eta=0 subtraction and eta-linearity controls.' if sm.get('gate_status')=='PASS' else 'Use the direct N=512 bath for the first tauH0=1 small-eta CMB diagnostic rather than forcing an inaccurate sparse reduction.')
out={'gates':gates,'overall_classification':overall,'summary':sm,'selected_bath':sel,'finite_eta_CMB_interpretation_allowed':False,'next_step':next_step}
(R/'MASTER_V019T_REPORT.json').write_text(json.dumps(out,indent=2))
lines=['AeST MEMORY tauH0=1 POSITIVE BATH COMPRESSION v0.19t','='*88]
for g in gates:lines.append(f"{g['id']:4s}| {g['status']:42s}| {g['name']}")
lines += ['',f'OVERALL: {overall}',f"DIRECT N512 CONTROL: {sm.get('direct_N512_control',{})}",f"ACTIVE MODES: {sel.get('active_modes','n/a')}",f"COMPRESSED METRICS: {sel.get('heldout_metrics',{})}",'NEXT: '+next_step]
(R/'MASTER_V019T_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019t.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('v019t*')):
        if p.is_file():z.write(p,arcname=p.name)
    for p in (R/'MASTER_V019T_REPORT.json',R/'MASTER_V019T_REPORT.txt'):
        if p.exists():z.write(p,arcname=p.name)
print((R/'MASTER_V019T_REPORT.txt').read_text())
