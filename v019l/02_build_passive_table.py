#!/usr/bin/env python3
from pathlib import Path
import json,csv
import numpy as np
from passive_rational import fit_nonnegative_weights,metrics

OUT=Path('results');OUT.mkdir(exist_ok=True)
N=24
anchors=np.logspace(0,3,97)
q=None;weights=[];rows=[];all_rel=[]
for h in anchors:
    q,w,rel=fit_nonnegative_weights(float(h),N=N,nomega=121,qmin=1e-6,qmax=4.0)
    weights.append(w)
    all_rel.extend(rel)
    m=metrics(rel)
    rows.append([h,m['median'],m['p95'],m['p99'],m['max'],float(w.min()),float(w.sum()),int(np.count_nonzero(w>1e-14))])
weights=np.asarray(weights)
all_rel=np.asarray(all_rel)

table={
 'N':N,
 'h_anchors':anchors.tolist(),
 'q_nodes':q.tolist(),
 'weights':weights.tolist(),
 'rate_rule':'r_j(h)=h*q_j',
 'weight_rule':'linear interpolation in log(h) between anchor rows',
 'all_weights_nonnegative':bool(np.all(weights>=0)),
}
(OUT/'passive_table_N24.json').write_text(json.dumps(table))
with open(OUT/'passive_anchor_metrics.csv','w',newline='') as f:
    wr=csv.writer(f);wr.writerow(['Htau','median','p95','p99','max','min_weight','sum_weights','nonzero_weights']);wr.writerows(rows)

M=metrics(all_rel)
out={
 'N':N,'anchors':len(anchors),'h_range':[1.0,1000.0],
 'q_range':[float(q[0]),float(q[-1])],
 'global_anchor_metrics':M,
 'minimum_weight':float(weights.min()),
 'maximum_sum_weight_error_from_one':float(np.max(np.abs(weights.sum(axis=1)-1))),
 'all_weights_nonnegative':bool(np.all(weights>=0)),
 'target':'p99 < 1e-3 and max < 1e-3 on fitted anchor grid',
 'gate_status':'PASS' if M['p99']<1e-3 and M['max']<1e-3 and np.all(weights>=0) else 'CHECK'
}
(OUT/'passive_table_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
