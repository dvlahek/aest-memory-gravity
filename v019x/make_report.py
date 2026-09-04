#!/usr/bin/env python3
from pathlib import Path
import json,zipfile

p=Path('results/v019x_analysis.json')
if not p.exists(): raise SystemExit('missing results/v019x_analysis.json')
r=json.loads(p.read_text())
lines=[
'AeST MEMORY EXP tauH0=1 VARIATIONAL AMPLITUDE LADDER v0.19x',
'='*86,
f"X1  | {'PASS' if r['gates']['lambda_invariance'] else 'CHECK':8s} | lambda-invariant tangent (100,300,1000)",
f"X2  | {'PASS' if r['gates']['norm_stability'] else 'CHECK':8s} | tangent norm stability",
f"X3  | {'PASS' if r['gates']['precision'] else 'CHECK':8s} | p3/p4 lambda=300 spectrum convergence",
f"X4  | {r['classification']:45s} | overall",
'',
'TANGENT NORMS: '+repr(r['tangent_norms']),
'LAMBDA CONVERGENCE: '+repr(r['lambda_convergence']),
'NORM SPREAD: '+repr(r['lambda_100_300_1000_norm_spread']),
'PRECISION: '+repr(r['precision_convergence_p3_vs_p4']),
'EVEN CURVATURE: '+repr(r['quadratic_even_curvature_norms']),
'',
'IMPORTANT: lambda is a numerical amplifier of the eta=0 first-order forcing, not physical eta.',
'Scope: unlensed TT/EE/TE tangent diagnostic; no likelihood or detectability claim.',
]
Path('results/v019x_report.txt').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019x.zip','w',zipfile.ZIP_DEFLATED) as z:
    for q in Path('results').glob('v019x*'):
        z.write(q,q.as_posix())
print('Created results_bundle_v019x.zip')
