#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

R=Path('results')
def load(n):
    p=R/n
    return json.loads(p.read_text()) if p.exists() else {}

der=load('v019i_derivation.json')
app=load('v019i_apply_report.json')
conv=load('v019i_start_convergence.json')
build=load('v019i_build_report.json')
classification=conv.get('summary',{}).get('classification','UNKNOWN')

gates=[
 {'id':'V19I-1','name':'Leading adiabatic time-shift derivation','status':der.get('gate_status','UNKNOWN')},
 {'id':'V19I-2','name':'CLASS IC patch and source audit','status':'PASS' if app.get('classification')=='LEADING_SUPERHORIZON_ADIABATIC_IC' else 'UNKNOWN'},
 {'id':'V19I-3','name':'Patched CLASS compile','status':build.get('patched_build','UNKNOWN')},
 {'id':'V19I-4','name':'CDM/Cosh/Exp start-time ladder','status':build.get('start_ladder','UNKNOWN')},
 {'id':'V19I-5','name':'Finite-gradient IC start convergence','status':conv.get('gate_status','UNKNOWN')},
 {'id':'V19I-6','name':'Interpretation','status':classification},
]
report={
 'scope':'radiation-era eta=0 adiabatic IC; memory remains off',
 'gates':gates,
 'derivation':der,
 'start_convergence_summary':conv.get('summary',{}),
 'classification':classification,
 'central_relation':'delta_A=(1+w_A)delta_c, Theta_A=Theta_c, alpha_A=-a Theta_A/k^2, E_A=0 at leading superhorizon order',
 'caveat':'The time-shift derivation fixes the k/H -> 0 adiabatic mode. A start-convergence PASS shows that omitted O((k/H)^2) terms are numerically irrelevant at tested accuracy; it is not an all-orders analytic Frobenius solution.',
 'next':('If start convergence passes, freeze eta=0 CLASS initial conditions and only then design the first eta>0 memory perturbation gate.' if classification=='LEADING_ADIABATIC_START_CONVERGED' else 'Derive the explicit Frobenius series through O((k tau)^2) before enabling memory.'),
}
R.mkdir(exist_ok=True)
(R/'MASTER_V019I_REPORT.json').write_text(json.dumps(report,indent=2))
lines=['AeST RADIATION-ERA ADIABATIC IC GATE v0.19i','='*92]
for g in gates:lines.append(f"{g['id']:8s}| {g['status']:38s}| {g['name']}")
lines += ['',f'CLASSIFICATION: {classification}',report['central_relation'],report['caveat'],'NEXT: '+report['next']]
(R/'MASTER_V019I_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019i.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob('v019i*')):
        if p.is_file():z.write(p,arcname=p.name)
    for p in [R/'MASTER_V019I_REPORT.json',R/'MASTER_V019I_REPORT.txt']:
        if p.exists():z.write(p,arcname=p.name)
print((R/'MASTER_V019I_REPORT.txt').read_text())
print('Created results_bundle_v019i.zip')
