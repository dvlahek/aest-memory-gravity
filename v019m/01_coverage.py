#!/usr/bin/env python3
from pathlib import Path
import json
from timevarying import h_lcdm

OUT=Path('results');OUT.mkdir(exist_ok=True)

z_rec=1089.4
z_eq=3400.0
z_early=1e5
points={
 'today':1.0,
 'recombination':1.0/(1.0+z_rec),
 'equality':1.0/(1.0+z_eq),
 'z_1e5':1.0/(1.0+z_early),
}
base={k:float(h_lcdm(a)) for k,a in points.items()}

taus=[1.0,0.1,0.01,0.001]
rows={}
for t in taus:
    rows[str(t)]={k:t*v for k,v in base.items()}

# v0.19l table covers 1 <= H tau <= 1000.
def covers(vals):
    return all(1.0<=v<=1000.0 for v in vals.values())

out={
 'v019l_table_range_Htau':[1.0,1000.0],
 'H_over_H0':base,
 'tauH0_cases':rows,
 'full_today_to_recombination_covered':{str(t):covers({'today':rows[str(t)]['today'],'recombination':rows[str(t)]['recombination']}) for t in taus},
 'full_today_to_equality_covered':{str(t):covers({'today':rows[str(t)]['today'],'equality':rows[str(t)]['equality']}) for t in taus},
 'important_result':'No tested tauH0 maps both today and recombination into the current [1,1000] table; for tauH0=1 recombination/equality lie far above its upper edge.',
 'gate_status':'COVERAGE_EXTENSION_REQUIRED'
}
(OUT/'v019m_coverage.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
