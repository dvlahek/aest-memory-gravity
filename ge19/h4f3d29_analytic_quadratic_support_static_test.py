#!/usr/bin/env python3
"""Import-free test of the D29 exact harmonic rule and safety controls."""
from __future__ import annotations
import ast, hashlib, json
from pathlib import Path
p=Path(__file__).with_name('h4f3d29_analytic_quadratic_support.py')
source=p.read_text();tree=ast.parse(source)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='quadratic_support')
ns={};exec(compile(ast.Module(body=[node],type_ignores=[]),str(p),'exec'),ns)
f=ns['quadratic_support']
k=(3,5,8,10,15,20);s=f(k)
assert 14 not in s and 1 not in s and 40 in s and 0 in s
assert 14 in f(k+(11,)) and 1 in f(k+(4,))
assert 40 not in f((3,5,8,10,15))
for bad in ((3,3),(-3,5),()):
    try:f(bad)
    except ValueError:pass
    else:raise AssertionError('D29 wrong mode cohort accepted')
for needle in ("r7.assemble_ga_local(pd,Dt,k=k40,spatial_real=False)",
               "new_mbf=-pd['b_f']", "new_grad=1j*k40*pd['b_x']",
               "if m not in support and not np.any(np.abs(y)>0)",
               "'no_mode_exclusion':True", "'original_shift_threshold_unchanged':True"):
    assert needle in source, needle
pr=json.loads(p.with_name('h4f3d29_analytic_quadratic_support_prereg.json').read_text())
assert pr['expected_GE06_quadratic_support']=={'m14':False,'m1':False,'m40':True}
assert pr['in_support_b_term_replay_relative_limit']==1e-11
assert pr['in_support_global_row_replay_relative_limit']==1e-9
print('GE19_D29_MANUFACTURED_MODE_SUPPORT_SIGN_AND_ORIGINAL_GATE_NEGATIVE_CONTROLS_PASS',flush=True)
