#!/usr/bin/env python3
"""D34 manufactured gate/cohort tests; no historical outputs modified."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from ge19 import h4f3d34_all_mode_first_interval_gate_scan as d34


def expect_fail(fun,label):
    try:fun()
    except RuntimeError:return
    raise RuntimeError('D34 negative control did not fail: '+label)


def run():
    d34_source=Path(d34.__file__).read_text()
    assert 'r7._source_interp(x,C,m)' in d34_source
    assert 'd31.projection(r7,mod6,mod7,bg,tag,k,x0,rf,cf,ib)' in d34_source
    assert 'd25.integrate(r7,mod6,mod7,bg,tag,k,y0,x0,x1,rr,cc,n)' in d34_source
    assert "'H3_full_window_solve_performed':False" in d34_source
    assert 'original_shift_gate' in d34_source and 'D34 REFUSE_OVERWRITE' in d34_source
    pre=json.loads(d34.PRE.read_text())
    assert tuple(pre['modes'])==tuple(range(1,41))
    assert tuple(pre['betas'])==(1.0,0.5,0.1) and tuple(pre['substeps'])==(1,8)
    assert pre['original_shift_gate']==pre['original_boundary_backward_gate']==1e-6
    assert len(pre['exact_quadratic_support'])==22 and 0 in pre['exact_quadratic_support']
    assert 1 not in pre['exact_quadratic_support'] and 14 not in pre['exact_quadratic_support']
    assert 40 in pre['exact_quadratic_support']
    modes=(1,14);betas=(1.0,0.1);substeps=(1,8)
    rows=[{'mode':m,'beta':b,'substeps':n,
           'shift':{'relative_backward':1e-7,'absolute_residual':1e-20}}
          for m in modes for b in betas for n in substeps]
    pos=d34.assess(rows,modes,betas,substeps,1e-6)
    assert pos['all_case_count']==8 and pos['all_first_interval_original_shift_gates_pass']
    rows[0]['shift']['relative_backward']=1.1e-6
    neg=d34.assess(rows,modes,betas,substeps,1e-6)
    assert neg['shift_gate_fail_count']==1 and not neg['all_first_interval_original_shift_gates_pass']
    rows[0]['shift']['relative_backward']=float('nan')
    expect_fail(lambda:d34.assess(rows,modes,betas,substeps,1e-6),'nonfinite gate')
    rows[0]['shift']['relative_backward']=1.1e-6
    expect_fail(lambda:d34.assess(rows[:-1],modes,betas,substeps,1e-6),'missing mode')
    expect_fail(lambda:d34.assess(rows+[rows[0]],modes,betas,substeps,1e-6),'duplicate mode')
    expect_fail(lambda:d34.assess([*rows[:-1],rows[0]],modes,betas,substeps,1e-6),'replaced mode')
    z=np.zeros((2,128,41),complex)
    support=set(pre['exact_quadratic_support'])
    assert all(np.array_equal(z[0,:,m],np.zeros(128,complex)) for m in range(41) if m not in support)
    z[0,0,1]=1e-29
    assert not all(np.array_equal(z[0,:,m],np.zeros(128,complex)) for m in range(41) if m not in support)
    print('GE19_D34_MANUFACTURED_FULL_COHORT_ORIGINAL_GATE_AND_OFFSUPPORT_NEGATIVE_CONTROLS_PASS',flush=True)

if __name__=='__main__':run()
