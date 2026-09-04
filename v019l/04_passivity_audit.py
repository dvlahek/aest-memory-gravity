#!/usr/bin/env python3
from pathlib import Path
import json
import numpy as np
from passive_rational import interpolate_weights

OUT=Path('results');OUT.mkdir(exist_ok=True)
table=json.loads((OUT/'passive_table_N24.json').read_text())
anchors=np.asarray(table['h_anchors'],float)
q=np.asarray(table['q_nodes'],float)
W=np.asarray(table['weights'],float)

min_re=np.inf;min_w=np.inf;max_pole= -np.inf
# Test anchors and midpoints on a dense right-half-plane grid.
hvals=np.sort(np.r_[anchors,np.sqrt(anchors[:-1]*anchors[1:])])
for h in hvals:
    w=interpolate_weights(float(h),anchors,W)
    r=h*q
    min_w=min(min_w,float(w.min()))
    max_pole=max(max_pole,float(np.max(-r)))
    for er in [1e-8,1e-5,1e-3,.01,.1,1.,10.]:
        for wi in np.logspace(-4,4,100):
            z=h*(er+1j*wi)
            K=np.sum(w*z/(z+r))
            min_re=min(min_re,float(K.real))

out={
 'representation':'K_N(z,h)=sum_j w_j(h) z/[z+r_j(h)]',
 'all_rates_positive':bool(np.all(q>0)),
 'all_poles_strictly_left_half_plane':bool(max_pole<0),
 'minimum_interpolated_weight':float(min_w),
 'minimum_sampled_real_part_on_Re_z_positive':float(min_re),
 'analytic_reason':'Each z/(z+r_j) with r_j>0 is positive-real, and a nonnegative weighted sum preserves passivity.',
 'gate_status':'PASS' if np.all(q>0) and max_pole<0 and min_w>=0 and min_re>-1e-12 else 'CHECK'
}
(OUT/'passivity_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
