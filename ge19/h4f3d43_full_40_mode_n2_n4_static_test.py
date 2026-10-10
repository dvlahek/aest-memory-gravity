#!/usr/bin/env python3
"""D43 purely synthetic contract tests. DOES NOT run GE19 physics."""
import ast, pathlib, numpy as np, json
ROOT=pathlib.Path(__file__).resolve().parents[1]
src=(ROOT/'ge19/h4f3d43_full_40_mode_n2_n4_lapse.py').read_text()
pre=json.loads((ROOT/'ge19/h4f3d43_full_40_mode_n2_n4_prereg.json').read_text())
tree=ast.parse(src)
node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='summarize_new')
ns={'np':np};exec(compile(ast.Module(body=[node],type_ignores=[]),'<D43_HELPER_AST>','exec'),ns)
f=ns['summarize_new'];g=1e-6
valid=np.ones((128,40,3,2),bool);s=np.zeros(valid.shape,float);l=np.zeros(valid.shape,float)
x=f(valid,s,l,g)
assert x['new_endpoint_evaluated']==30480 and x['new_endpoint_unevaluated']==0
assert x['observed_new_shift_gate_fail_count']==x['observed_new_lapse_over_reference_count']==0
broken=valid.copy();broken[100,0,0,0]=False;broken[101:,0,0,0]=False
sb=s.copy();lb=l.copy();sb[~broken]=np.nan;lb[~broken]=np.nan
v=f(broken,sb,lb,g)
assert v['new_endpoint_unevaluated']==28 and v['new_endpoint_evaluated']==30452
bad=broken.copy();bad[101,0,0,0]=True
try:f(bad,sb,lb,g)
except RuntimeError:pass
else:raise AssertionError('D43 gap negative control failed')
sf=s.copy();sf[10,0,0,0]=2*g
z=f(valid,sf,l,g)
assert z['observed_new_shift_gate_fail_count']==1
lf=l.copy();lf[10,0,0,0]=2*g
z=f(valid,s,lf,g)
assert z['observed_new_lapse_over_reference_count']==1
assert pre['new_endpoint_expected']==30480
assert pre['modes']==list(range(1,41)) and pre['new_substeps']==[2,4]
assert src.count('np.take(frozenlap[:,:,:,0 if n==1 else 1],selected_indices,axis=1)')==1
assert src.count('np.take(frozenshift[:,:,:,0 if n==1 else 1],selected_indices,axis=1)')==1
assert 'GE19_D43_FULL_40_MODE_N2_N4_CLOCK_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED' in src
assert 'GE19_D43_FULL_40_MODE_N2_N4_CLOCK_DIAGNOSTIC_GATE_FAILURE_PARENTS_UNCERTIFIED' in src
print('GE19_D43_SYNTHETIC_30480_ENDPOINT_MASK_SHIFT_LAPSE_NEGATIVES_AND_AST_PASS',flush=True)
