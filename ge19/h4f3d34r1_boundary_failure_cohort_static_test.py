#!/usr/bin/env python3
"""D34R1 manufactured full vs incomplete diagnostic; no physical output modified."""
import json
from pathlib import Path
from ge19 import h4f3d34r1_boundary_failure_cohort as x


def must_fail(fn):
    try:fn()
    except RuntimeError:return
    raise AssertionError('D34R1 negative control not rejected')


def test():
    pre=json.loads(x.PRE.read_text());source=Path(x.__file__).read_text()
    assert pre['original_shift_gate']==pre['original_boundary_backward_gate']==1e-6
    assert tuple(pre['modes'])==tuple(range(1,41))
    assert tuple(pre['betas'])==(1.0,0.5,0.1) and tuple(pre['substeps'])==(1,8)
    assert 'd31.projection(r7,mod6,mod7,bg,tag,k,x0,rf,cf,ib)' in source
    assert 'd25.integrate(r7,mod6,mod7,bg,tag,k,y0,x0,x1,rr,cc,n)' in source
    assert 'continue' in source and "'candidate_C_y1_valid_by_mode_beta_substep'" in source
    assert "'all_first_interval_original_shift_gates_pass': original['all_first_interval_original_shift_gates_pass'] if complete else None" in source
    attempts=[(1,1.0),(1,0.1)]
    sample=lambda m,b,n: {'mode':m,'beta':b,'substeps':n,'shift':{'relative_backward':1e-7,'absolute_residual':1e-28}}
    full=[sample(m,b,n) for m,b in attempts for n in (1,8)]
    p=x.summarize_observed(full,[],(1,),(1.0,0.1),(1,8),1e-6,attempts)
    assert p['all_240_shift_cases_evaluated'] and p['all_first_interval_original_shift_gates_pass'] and p['unevaluated_shift_case_count']==0
    failed=[{'mode':1,'beta':1.0}]
    partial=[sample(1,0.1,n) for n in (1,8)]
    r=x.summarize_observed(partial,failed,(1,),(1.0,0.1),(1,8),1e-6,attempts)
    assert not r['all_240_shift_cases_evaluated'] and r['unevaluated_shift_case_count']==2 and r['initial_boundary_failure_count']==1
    assert r['all_first_interval_original_shift_gates_pass'] is None and r['shift_gate_fail_count'] is None
    must_fail(lambda:x.summarize_observed(partial,[],(1,),(1.0,0.1),(1,8),1e-6,attempts))
    must_fail(lambda:x.summarize_observed(full,failed,(1,),(1.0,0.1),(1,8),1e-6,attempts))
    must_fail(lambda:x.summarize_observed(partial,failed,(1,),(1.0,0.1),(1,8),1e-6,attempts[:-1]))
    print('GE19_D34R1_MANUFACTURED_ORIGINAL_BOUNDARY_FAIL_PRESERVED_AND_UNEVALUATED_ENDPOINT_MASK_NEGATIVE_CONTROLS_PASS',flush=True)

if __name__=='__main__':test()
