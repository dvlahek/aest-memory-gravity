#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

OUT=Path('results')
r=json.loads((OUT/'v019u_response.json').read_text())
a=json.loads((OUT/'v019u_apply_report.json').read_text())
lines=['AeST MEMORY tauH0=1 FINITE-MEMORY CLASS RESPONSE v0.19u','='*88]
lines.append(f"U1  | {'PASS' if all(a['checks'].values()) else 'CHECK':<40} | validated 39/47-mode positive bath patch")
for m in ('cosh','exp'):
    lines.append(f"U2-{m:<4} | {r['models'][m]['gate_status']:<40} | eta-linearity + bath-order + bg/thermo controls")
lines.append(f"U3  | {r['classification']:<40} | overall tauH0=1 finite-memory gate")
lines += ['',f"OVERALL: {r['classification']}"]
for m in ('cosh','exp'):
    q=r['models'][m]
    lines.append(f"{m.upper()} response norms: {q['response_norms']}")
    lines.append(f"{m.upper()} eta linearity: {q['eta_linearity']}")
    lines.append(f"{m.upper()} bath order: {q['bath_order_convergence_eta0p01']}")
lines.append('NEXT: if PASS, repeat the response at stricter CLASS precision and then map tauH0 before any likelihood claim; if CHECK, diagnose the failing gate only.')
text='\n'.join(lines)+'\n';print(text)
(OUT/'MASTER_V019U_REPORT.txt').write_text(text)
(OUT/'MASTER_V019U_REPORT.json').write_text(json.dumps({'apply':a,'response':r},indent=2))
with zipfile.ZipFile('results_bundle_v019u.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.iterdir()):
        if p.is_file() and ('v019u' in p.name or p.name.startswith('MASTER_V019U')):z.write(p,p.name)
print('Created results_bundle_v019u.zip')
