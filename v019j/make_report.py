#!/usr/bin/env python3
from pathlib import Path
import json,zipfile
R=Path('results')
def load(n):
 p=R/n
 return json.loads(p.read_text()) if p.exists() else {}
rep=load('v019j_representation.json');apply=load('v019j_apply_report.json');off=load('v019j_off_regression.json');mem=load('v019j_memory.json');build=load('v019j_build_report.json')
gates=[
 {'id':'V19J-1','name':'Finite positive bath representation','status':rep.get('gate_status','UNKNOWN')},
 {'id':'V19J-2','name':'CLASS finite-eta memory patch/source audit','status':'PASS' if apply.get('classification')=='FINITE_POSITIVE_DRUDE_MEMORY_CLASS_PATCH' else 'UNKNOWN'},
 {'id':'V19J-3','name':'eta=0 and memory-patched CLASS builds','status':build.get('builds','UNKNOWN')},
 {'id':'V19J-4','name':'Memory-disabled zero regression','status':off.get('gate_status','UNKNOWN')},
 {'id':'V19J-5','name':'Finite-eta Cosh/Exp campaign','status':build.get('memory_runs','UNKNOWN')},
 {'id':'V19J-6','name':'eta-linearity and bath-order convergence','status':mem.get('gate_status','UNKNOWN')},
 {'id':'V19J-7','name':'Interpretation','status':mem.get('classification','UNKNOWN')},
]
report={
 'scope':'first full CLASS finite-eta memory response; no Planck likelihood',
 'gates':gates,
 'classification':mem.get('classification','UNKNOWN'),
 'representation':rep,
 'memory_analysis':mem,
 'frozen_eta0_IC':'leading radiation-era adiabatic mode from v0.19i',
 'central_drag_law':'unchanged: a_drag proportional to -(v tau)^(1/3) with the Airy coefficient in the deep-MOND smooth-source limit',
 'next':'If finite eta is resolved with linear eta scaling and N=16/N=20 convergence, add tau_H0 response mapping and only then move to likelihood-level C_l constraints.'
}
R.mkdir(exist_ok=True)
(R/'MASTER_V019J_REPORT.json').write_text(json.dumps(report,indent=2))
lines=['AeST FIRST FINITE-ETA CLASS MEMORY TEST v0.19j','='*92]
for g in gates:lines.append(f"{g['id']:8s}| {g['status']:36s}| {g['name']}")
lines += ['',f"CLASSIFICATION: {report['classification']}",'NEXT: '+report['next']]
(R/'MASTER_V019J_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019j.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(R.glob('v019j*')):
  if p.is_file():z.write(p,arcname=p.name)
 for p in [R/'MASTER_V019J_REPORT.json',R/'MASTER_V019J_REPORT.txt']:
  if p.exists():z.write(p,arcname=p.name)
print((R/'MASTER_V019J_REPORT.txt').read_text());print('Created results_bundle_v019j.zip')
