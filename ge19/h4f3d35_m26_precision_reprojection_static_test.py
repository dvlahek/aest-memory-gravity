#!/usr/bin/env python3
"""Manufactured positive/negative controls; never uses observed science results."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from ge19 import h4f3d35_m26_precision_reprojection as d

p=np.asarray([2.0+0j,3e-20+0j,1e-3+0j,0j],complex)
z,mask,cut=d.zero_subroundoff_momenta(p,np.zeros(2,complex),16)
assert np.array_equal(mask,np.asarray([False,True,False,False]))
assert np.array_equal(z,np.asarray([2+0j,0j,1e-3+0j,0j]))
assert cut==16*np.finfo(float).eps*2
# Significant p must not be modified by a small-momentum roundoff representation.
p2=np.asarray([1.,1e-10,1e-3,0],complex)
z2,m2,_=d.zero_subroundoff_momenta(p2,np.zeros(2,complex),16)
assert np.array_equal(z2,p2) and not m2.any()
for bad in (np.asarray([1.,0.],complex),np.asarray([0.,1.],complex)):
    try:d.zero_subroundoff_momenta(p,bad,16)
    except ValueError:pass
    else:raise AssertionError('D35 NONZERO original constraint source wrongly accepted')
for bad_multiplier in (0,32,-1):
    try:d.zero_subroundoff_momenta(p,np.zeros(2,complex),bad_multiplier)
    except ValueError:pass
    else:raise AssertionError('D35 relaxed/tuned precision cutoff accepted')
pre=json.loads(d.PRE.read_text())
assert pre['target_mode']==26 and pre['tiny_component_multiplier_of_float64_epsilon']==16
assert pre['original_shift_gate']==pre['original_boundary_backward_gate']==1e-6
assert pre['modes']==list(range(1,41)) and pre['betas']==[1.0,0.5,0.1] and pre['substeps']==[1,8]
assert pre['strict_source_retention'] and pre['no_mode_exclusion'] and pre['no_physics_threshold_change']
# Incomplete evaluation is never reclassified as a complete gate PASS.
old=[{'mode':m,'beta':b,'substeps':n,'shift':{'relative_backward':0.,'absolute_residual':0.}}
     for m in (1,2) for b in (1.,0.5,0.1) for n in (1,8) if not (m==2 and b==0.1)]
fail=[{'mode':2,'beta':0.1,'reason':'manufactured missing boundary'}]
s=d.d34r1.summarize_observed(old,fail,(1,2),(1.,0.5,0.1),(1,8),1e-6,
                                [(m,b) for m in (1,2) for b in (1.,0.5,0.1)])
assert s['unevaluated_shift_case_count']==2 and s['all_first_interval_original_shift_gates_pass'] is None
assert s['shift_gate_fail_count'] is None and s['observed_shift_gate_fail_count']==0
print('GE19_D35_MANUFACTURED_FLOAT64_SUBROUNDOFF_ORIGINAL_SOURCE_ZERO_AND_UNEVALUATED_NEGATIVE_CONTROLS_PASS',flush=True)
