#!/usr/bin/env python3
"""Manufactured complex-interpolation, real-parent and tampered-parent tests."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'ge19/h4f3d46_source_interpolation_counterfactual.py'
spec=importlib.util.spec_from_file_location('ge19_D46_source_counterfactual',MOD)
assert spec and spec.loader
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.synth_test()
pre=json.loads((ROOT/'ge19/h4f3d46_source_interpolation_counterfactual_prereg.json').read_text())
assert pre['diagnostic_modes']==[1,6,14,26,40]
assert pre['betas']==[1.,.5,.1]
assert pre['n_substeps']==4 and pre['original_shift_gate']==1e-6
assert pre['original_D33_41_mode_source_retained']
assert pre['original_D43_n4_frozen_reference_only']
assert pre['do_not_promote_linear_source_to_physical_truth']

# The real frozen five-mode D43/D42R2 agreement MUST be bitwise.
rd=ROOT/'results'
names=('ge19_h4f3d42r2_lapse_substep_convergence.npz','ge19_h4f3d43_full_40_mode_n2_n4_lapse.npz',
       'ge19_h4f3d45_h1_offclock_source_audit.npz','ge19_h4f3d33_direct_ge07_paired_first_interval.npz')
if all((rd/n).is_file() for n in names):
    import numpy as np
    with np.load(rd/names[0],allow_pickle=False) as z42,np.load(rd/names[1],allow_pickle=False) as z43,\
         np.load(rd/names[2],allow_pickle=False) as z45,np.load(rd/names[3],allow_pickle=False) as z33:
        sel=np.array(pre['diagnostic_modes'])-1
        assert np.array_equal(np.take(z43['new_states_by_node_mode_beta_substep'][:,:,:,1,:],sel,axis=1),
                              z42['new_states_by_node_mode_beta_substep'][:,:,:,1,:])
        x=z45['clock_node_x']
        main=np.stack([z33[f'beta{i}_candidate_C_main_six_by_128_by_41'] for i in range(3)],axis=-1)
        con=np.stack([z33[f'beta{i}_candidate_C_constraint_two_by_128_by_41'] for i in range(3)],axis=-1)
        for mm in pre['diagnostic_modes']:
            lin,cl=m.source_linear(x,main,con,mm)
            for it in (0,114,126):
                mid=float((x[it]+x[it+1])/2)
                got=np.concatenate((lin(mid),cl(mid)),axis=0)
                target=z45['source_linear_mid'][:,it,mm,:]
                assert m.rel_l2(got,target)<3e-13
    print('GE19_D46_REAL_FROZEN_D42R2_D43_STATES_AND_D45_SOURCE_MIDPOINT_PASS',flush=True)
else:
    print('GE19_D46_REAL_PARENT_PRETEST_DEFERRED_TO_USER_LOCAL_SHA_GATED_RUN',flush=True)
import tempfile
parent_json=rd/'ge19_h4f3d45_h1_offclock_source_audit.json'
if parent_json.is_file():
    expected=pre['frozen_original_parent_sha256'][parent_json.name]
    assert m.sha(parent_json)==expected
    with tempfile.TemporaryDirectory() as folder:
        forged=Path(folder)/parent_json.name
        forged.write_bytes(parent_json.read_bytes()+b'\n')
        assert m.sha(forged)!=expected
    print('GE19_D46_ACTUAL_D45_SHA_TAMPER_NEGATIVE_PASS',flush=True)
print('GE19_D46_STATIC_AND_PREREG_SCOPE_PASS',flush=True)
