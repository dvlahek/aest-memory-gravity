#!/usr/bin/env python3
from pathlib import Path
import json,csv
import numpy as np
from bath_designs import *

OUT=Path('results');OUT.mkdir(exist_ok=True)

# For tau H0=1 in an expanding cosmology, H tau >= O(1) through the late universe
# and is much larger at early times. omega/H spans super- to deeply-subhorizon modes.
hvals=[1.,3.,10.,30.,100.,300.,1000.]
wH=np.logspace(-3,3,241)
eH=[1e-8,1e-6,1e-4,1e-2,0.1]

def audit(nodes,weights):
    rows=[];errs=[];worst=None
    for h in hvals:
        for w in wH:
            for e in eH:
                z=h*(e+1j*w)
                A=retarded_A(z,h)
                ex=exact_kernel(A)
                ap=finite_kernel(A,nodes,weights)
                rel=float(abs(ap-ex)/max(abs(ex),1e-300))
                errs.append(rel)
                if worst is None or rel>worst['relative_error']:
                    worst={'relative_error':rel,'Htau':h,'omega_over_H':float(w),'eps_over_H':e,
                           'A_real':float(A.real),'A_imag':float(A.imag),
                           'exact_real':float(ex.real),'exact_imag':float(ex.imag),
                           'finite_real':float(ap.real),'finite_imag':float(ap.imag)}
                rows.append([h,w,e,A.real,A.imag,ex.real,ex.imag,ap.real,ap.imag,rel])
    q=np.quantile(errs,[.5,.9,.95,.99])
    return rows,{
      'points':len(errs),'median_relative_error':float(q[0]),'p90_relative_error':float(q[1]),
      'p95_relative_error':float(q[2]),'p99_relative_error':float(q[3]),
      'max_relative_error':float(max(errs)),'worst_case':worst}

summary={}
for name,nodes,weights in [('N16',NODES16,WEIGHTS16),('N20',NODES20,WEIGHTS20)]:
    rows,res=audit(nodes,weights);summary[name]=res
    with open(OUT/f'complex_kernel_{name}.csv','w',newline='') as f:
        w=csv.writer(f);w.writerow(['Htau','omega_over_H','eps_over_H','A_real','A_imag','exact_real','exact_imag','finite_real','finite_imag','relative_error']);w.writerows(rows)

# A controlled oscillatory realization should be much better than the CMB response target.
# 2% p95 / 5% max are already deliberately loose compared with the real-axis v0.17 errors.
summary['N20_complex_controlled']=bool(summary['N20']['p95_relative_error']<.02 and summary['N20']['max_relative_error']<.05)
summary['classification']='COMPLEX_AXIS_CONTROLLED' if summary['N20_complex_controlled'] else 'REAL_AXIS_FIT_NOT_COMPLEX_CONTROLLED'
summary['gate_status']='PASS_COMPLEX' if summary['N20_complex_controlled'] else 'DIAGNOSTIC_FAIL_EXPECTED'
(OUT/'complex_kernel_audit_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
