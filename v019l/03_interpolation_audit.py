#!/usr/bin/env python3
from pathlib import Path
import json,csv
import numpy as np
from passive_rational import exact_kernel,interpolate_weights,basis,metrics

OUT=Path('results');OUT.mkdir(exist_ok=True)
table=json.loads((OUT/'passive_table_N24.json').read_text())
anchors=np.asarray(table['h_anchors'],float)
q=np.asarray(table['q_nodes'],float)
W=np.asarray(table['weights'],float)

# Midpoints in log h are the hardest interpolation locations for piecewise-linear tables.
test_h=np.sqrt(anchors[:-1]*anchors[1:])
omega=np.logspace(-3,3,81)
eps=np.array([1e-8,1e-6,1e-4,1e-2,1e-1])
rows=[];all_rel=[]
for h in test_h:
    w=interpolate_weights(float(h),anchors,W)
    z=np.array([h*(e+1j*om) for om in omega for e in eps],dtype=complex)
    K=exact_kernel(z,float(h))
    pred=basis(z,float(h),q)@w
    rel=np.abs(pred-K)/np.maximum(np.abs(K),1e-300)
    all_rel.extend(rel)
    m=metrics(rel)
    rows.append([h,m['median'],m['p95'],m['p99'],m['max'],float(w.min()),float(w.sum())])

all_rel=np.asarray(all_rel)
M=metrics(all_rel)
with open(OUT/'passive_interpolation_metrics.csv','w',newline='') as f:
    wr=csv.writer(f);wr.writerow(['Htau_midpoint','median','p95','p99','max','min_interpolated_weight','sum_weights']);wr.writerows(rows)

out={
 'N':int(table['N']),'anchor_count':len(anchors),'midpoint_count':len(test_h),
 'global_midpoint_metrics':M,
 'all_interpolated_weights_nonnegative':bool(min(r[5] for r in rows)>=0),
 'target':'p99 < 1e-3 and max < 1e-3 between H anchors',
 'gate_status':'PASS' if M['p99']<1e-3 and M['max']<1e-3 and min(r[5] for r in rows)>=0 else 'CHECK'
}
(OUT/'passive_interpolation_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
