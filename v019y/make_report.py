#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

p=Path('results/v019y_analysis.json')
r=json.loads(p.read_text())
lines=[]
lines.append('AeST MEMORY EXP tauH0=1 HIGH-OUTPUT-PRECISION TANGENT v0.19y')
lines.append('='*84)
lines.append(f"Y1  | {'PASS' if r['gates']['lambda_invariance'] else 'CHECK':8s} | lambda-invariant tangent at 17-digit output")
lines.append(f"Y2  | {'PASS' if r['gates']['norm_stability'] else 'CHECK':8s} | tangent norm stability")
lines.append(f"Y3  | {'PASS' if r['gates']['precision'] else 'CHECK':8s} | p3/p4 lambda=300 convergence")
lines.append(f"Y4  | {r['classification']} | overall")
lines.append('')
lines.append(f"TANGENT NORMS: {r['tangent_norms']}")
lines.append(f"LAMBDA CONVERGENCE: {r['lambda_convergence']}")
lines.append(f"NORM SPREAD: {r['lambda_100_300_1000_norm_spread']}")
lines.append(f"PRECISION: {r['precision_convergence_p3_vs_p4']}")
lines.append('')
lines.append('IMPORTANT: only text-output precision was changed to 17 significant digits; physics and solver tolerances are unchanged.')
lines.append('Lambda is a numerical amplifier of the eta=0 tangent forcing, not physical eta.')
report='\n'.join(lines)+'\n'
Path('results/v019y_report.txt').write_text(report)
print(report)
with zipfile.ZipFile('results_bundle_v019y.zip','w',zipfile.ZIP_DEFLATED) as z:
    for q in Path('results').glob('v019y*'):
        if q.is_file(): z.write(q,q.name)
print('Created results_bundle_v019y.zip')
