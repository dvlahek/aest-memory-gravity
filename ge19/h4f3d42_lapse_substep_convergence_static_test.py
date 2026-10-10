#!/usr/bin/env python3
"""D42 AST-extracted manufactured two-sector fingerprint and true masked endpoints."""
import ast,json
from pathlib import Path
import numpy as np
SRC=Path(__file__).with_name('h4f3d42_lapse_substep_convergence.py')
tree=ast.parse(SRC.read_text());funcs={v.name:v for v in tree.body if isinstance(v,ast.FunctionDef)}
assert {'failure_fingerprint','summarize_new'}<=funcs.keys()
ns={'np':np}
for name in ('failure_fingerprint','summarize_new'):
    mod=ast.Module(body=[funcs[name]],type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod),str(SRC),'exec'),ns)
fp=ns['failure_fingerprint'];summ=ns['summarize_new']
modes=np.arange(1,41);betas=np.array([1.,.5,.1]);subs=np.array([1,8])
la=np.zeros((128,40,3,2),float);off=np.array([1,4,9,14,19,21,22,24,26,27,29,31,32,33,34,36,37,38,39],int)
sup=np.array([m for m in modes if m not in set(off)],int)
la[1,off-1,:,0]=1.2e-6;la[115,sup-1,:,0]=1.3e-6
v=fp(la,modes,betas,subs,1e-6)
assert v['all_frozen_over_threshold_count']==120 and v['n1_x1_offsupport_count']==57 and v['n1_x115_smooth_support_count']==63
for wrong in ('missing_one','n8_fail','wrong_node','nan','wrong_beta','wrong_gate'):
    a=la.copy();bm=betas.copy();g=1e-6
    if wrong=='missing_one':a[1,off[0]-1,0,0]=0
    if wrong=='n8_fail':a[115,sup[0]-1,0,1]=2e-6
    if wrong=='wrong_node':a[115,sup[0]-1,0,0]=0;a[114,sup[0]-1,0,0]=2e-6
    if wrong=='nan':a[1,off[0]-1,0,0]=np.nan
    if wrong=='wrong_beta':bm[1]=.25
    if wrong=='wrong_gate':g=1e-5
    try:fp(a,modes,bm,subs,g)
    except RuntimeError:pass
    else:raise AssertionError('D42 accepted frozen fingerprint corruption '+wrong)
sh=np.full((128,5,3,3),1e-7);lap=sh.copy();mask=np.ones(sh.shape,bool)
q=summ(mask,sh,lap,1e-6)
assert q['new_endpoint_evaluated']==5715 and q['new_endpoint_unevaluated']==0
badmask=mask.copy();badshift=sh.copy();badlap=lap.copy()
badmask[5:,0,0,0]=False;badshift[5:,0,0,0]=np.nan;badlap[5:,0,0,0]=np.nan
q=summ(badmask,badshift,badlap,1e-6)
assert q['new_endpoint_evaluated']==5715-123 and q['new_endpoint_unevaluated']==123
for wrong in ('fake_nan_success','nan_unobserved_finite','reappeared_descendant','false_initial'):
    m=badmask.copy();s=badshift.copy();l=badlap.copy()
    if wrong=='fake_nan_success':s[4,0,0,0]=np.nan
    if wrong=='nan_unobserved_finite':s[5,0,0,0]=0.
    if wrong=='reappeared_descendant':m[6,0,0,0]=True;s[6,0,0,0]=1e-7;l[6,0,0,0]=1e-7
    if wrong=='false_initial':m[0,0,0,0]=False;s[0,0,0,0]=np.nan;l[0,0,0,0]=np.nan
    try:summ(m,s,l,1e-6)
    except RuntimeError:pass
    else:raise AssertionError('D42 accepted fabricated new trajectory '+wrong)
pre=json.loads(Path(__file__).with_name('h4f3d42_lapse_substep_convergence_prereg.json').read_text())
assert pre['modes']==[1,6,14,26,40] and pre['new_substeps']==[2,4,16] and pre['diagnostic_nodes']==[1,115]
assert 'd25.integrate(' in SRC.read_text() and 'd41.splice_full_window(' in SRC.read_text()
assert pre['lapse_fail_is_report_only'] and pre['original_shift_gate']==1e-6
print('GE19_D42_MANUFACTURED_TWO_SECTOR_FAILURE_AND_MISSING_ENDPOINT_NEGATIVE_CONTROLS_PASS',flush=True)
