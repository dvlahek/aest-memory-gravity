#!/usr/bin/env python3
from pathlib import Path
import json,csv
import numpy as np
from bath_designs import retarded_A,exact_kernel,finite_kernel,log_quadrature,NODES20,WEIGHTS20

OUT=Path('results');OUT.mkdir(exist_ok=True)
hvals=[1.,3.,10.,30.,100.,300.,1000.]
wH=np.logspace(-3,3,181)
eH=[1e-6,1e-3,.03]

As=[];targets=[]
for h in hvals:
    for w in wH:
        for e in eH:
            A=retarded_A(h*(e+1j*w),h)
            As.append(A);targets.append(exact_kernel(A))
As=np.asarray(As);targets=np.asarray(targets)

def metrics(nodes,weights):
    pred=finite_kernel(As,nodes,weights)
    rel=np.abs(pred-targets)/np.maximum(np.abs(targets),1e-300)
    return {'median_relative_error':float(np.median(rel)),'p95_relative_error':float(np.quantile(rel,.95)),
            'p99_relative_error':float(np.quantile(rel,.99)),'max_relative_error':float(np.max(rel)),
            'weight_sum':float(np.sum(weights)),'positive_weights':bool(np.all(weights>=0))}

summary={'current_fitted_N20':metrics(NODES20,WEIGHTS20),'direct_positive_log_quadrature':{}}
rows=[]
for N in [20,32,48,64,96,128]:
    r,w=log_quadrature(N,T=10.)
    m=metrics(r,w);summary['direct_positive_log_quadrature'][str(N)]=m
    rows.append([N,m['median_relative_error'],m['p95_relative_error'],m['p99_relative_error'],m['max_relative_error'],m['weight_sum']])

with open(OUT/'positive_quadrature_scan.csv','w',newline='') as f:
    wr=csv.writer(f);wr.writerow(['N','median_rel','p95_rel','p99_rel','max_rel','weight_sum']);wr.writerows(rows)

p95=[summary['direct_positive_log_quadrature'][str(N)]['p95_relative_error'] for N in [20,32,48,64,96,128]]
summary['p95_improves_overall']=bool(p95[-1]<p95[0])
summary['first_N_with_p95_below_0p5pct']=next((N for N in [20,32,48,64,96,128] if summary['direct_positive_log_quadrature'][str(N)]['p95_relative_error']<.005),None)
summary['interpretation']='The exact continuum has a positive spectral measure, but oscillatory complex-frequency convergence is much slower than the real-axis fit suggested. Large N or a different passive rational representation is required for a controlled CMB implementation.'
summary['gate_status']='PASS_DIAGNOSTIC' if summary['p95_improves_overall'] else 'CHECK'
(OUT/'positive_quadrature_scan_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
