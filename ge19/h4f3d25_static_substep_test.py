#!/usr/bin/env python3
"""Fast independent syntax/source-scope/manufactured smoke test for D25."""
import ast
from pathlib import Path
from ge19 import h4f3d25_first_interval_shift_substep_decision as d25
p=Path(d25.__file__)
t=p.read_text()
root=ast.parse(t)
funcs={n.name for n in root.body if isinstance(n,ast.FunctionDef)}
required={'step','integrate','shift_at','metric_from_y','archived_y','manufactured_test','main'}
if not required.issubset(funcs):raise RuntimeError('D25 missing frozen step/constraint functions')
if any(s in t for s in ('np.linalg.lstsq(', 'source_projection(', 'relabel_as_certified(', 'args.tolerance')):
    raise RuntimeError('D25 forbidden source fitting or gate change code')
if d25.NSUB!=(1,2,4,8) or d25.MODE_BETA!=((14,0.1),(1,1.0),(40,0.1)):
    raise RuntimeError('D25 cohort/substep preregistration changed')
d25.manufactured_test()
print('GE19_D25_STATIC_FROZEN_SOURCE_SUBSTEP_AND_NO_FALSE_CERTIFICATION_PASS',flush=True)
