#!/usr/bin/env python3
"""D45 static integrity + actual saved D33 interpolation preflight. No physics promotion."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from ge19 import h4f3d45_h1_offclock_source_audit as d45

root=Path(__file__).resolve().parents[1]
pre=json.loads((root/'ge19/h4f3d45_h1_offclock_source_audit_prereg.json').read_text())
rd=root/'results'
d45.synth_test()
for name,want in pre['original_parent_results_sha256'].items():
    p=rd/name
    d45.require(p.is_file() and d45.sha(p)==want,'STATIC_FROZEN_PARENT_SHA_MISMATCH_'+name)
p=rd/'ge19_d44_readonly_archive/ge19_d44_full_cohort_complex_clock_error_budget.json'
d45.require(p.is_file() and d45.sha(p)==pre['original_d44_archive_report_sha256'],'STATIC_D44_SHA_MISMATCH')
with np.load(rd/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz',allow_pickle=False) as z33, \
     np.load(rd/'ge19_h4f3d43_full_40_mode_n2_n4_lapse.npz',allow_pickle=False) as z43:
    x=np.asarray(z43['clock_node_x'],float)
    main=np.stack([z33[f'beta{i}_candidate_C_main_six_by_128_by_41'] for i in range(3)],axis=-1)
    con=np.stack([z33[f'beta{i}_candidate_C_constraint_two_by_128_by_41'] for i in range(3)],axis=-1)
    mid,p,l,e=d45.source_at_midpoints(x,main,con)
    d45.require(np.array_equal(z43['diagnostic_modes'],np.arange(1,41)) and np.array_equal(z43['betas'],[1.,.5,.1]),'STATIC_D43_AXES_CHANGED')
    d45.require(np.isfinite(p).all() and np.isfinite(l).all() and mid.shape==(127,), 'STATIC_SOURCE_MID_INVALID')
    d45.require(np.array_equal(con[:,:,26,:],np.zeros((2,128,3),complex)), 'STATIC_FROZEN_M26_ZERO_SOURCE_CHANGED')
print('GE19_D45_STATIC_REAL_D33_D43_AND_D44_FROZEN_HASH_SOURCE_MIDPOINT_PREFLIGHT_PASS',flush=True)
