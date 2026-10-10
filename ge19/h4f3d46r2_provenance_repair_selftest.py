#!/usr/bin/env python3
"""D46R2: audit the actual original D46 LOCAL log after preflight-only failure."""
from pathlib import Path
import json,hashlib,difflib,importlib.util,tempfile
ROOT=Path(__file__).resolve().parents[1]
G=ROOT/'ge19';R=ROOT/'results'
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
old_py=G/'h4f3d46_source_interpolation_counterfactual.py';new_py=G/'h4f3d46r1_source_interpolation_counterfactual.py'
old_pre=G/'h4f3d46_source_interpolation_counterfactual_prereg.json';new_pre=G/'h4f3d46r1_source_interpolation_counterfactual_prereg.json'
assert H(old_py)=='0b45c930b45623990567cdb085c831bf0fb2e0fe738710136f2ca856d0a8c56c','ORIGINAL_D46_SOURCE_CHANGED'
assert H(old_pre)=='8970c074786348ff6b04702a97e10d6f2f47d42582c793a0b97f4844b304946e','ORIGINAL_D46_PRE_DATA_CHANGED'
a=old_py.read_text();b=new_py.read_text()
assert a.count("PRE=ROOT/'ge19/h4f3d46_source_interpolation_counterfactual_prereg.json'")==a.count("require(pre['classification']=='GE19_D46_PREEXEC_FROZEN_D33_PCHIP_VS_LINEAR_SOURCE_INTERPOLATION_COUNTERFACTUAL','WRONG_PREREG')")==1
assert b==a.replace("PRE=ROOT/'ge19/h4f3d46_source_interpolation_counterfactual_prereg.json'","PRE=ROOT/'ge19/h4f3d46r1_source_interpolation_counterfactual_prereg.json'").replace("require(pre['classification']=='GE19_D46_PREEXEC_FROZEN_D33_PCHIP_VS_LINEAR_SOURCE_INTERPOLATION_COUNTERFACTUAL','WRONG_PREREG')","require(pre['classification']=='GE19_D46R1_PREEXEC_FROZEN_D33_PCHIP_VS_LINEAR_SOURCE_INTERPOLATION_COUNTERFACTUAL_SHA_REPAIR','WRONG_PREREG')"),'D46R1_DRIVER_SCOPE_CHANGED'
p=json.loads(old_pre.read_text());q=json.loads(new_pre.read_text())
assert q['classification']=='GE19_D46R1_PREEXEC_FROZEN_D33_PCHIP_VS_LINEAR_SOURCE_INTERPOLATION_COUNTERFACTUAL_SHA_REPAIR'
assert p['classification']=='GE19_D46_PREEXEC_FROZEN_D33_PCHIP_VS_LINEAR_SOURCE_INTERPOLATION_COUNTERFACTUAL'
for key in p:
 if key=='classification':continue
 if key=='frozen_original_parent_sha256':
  assert set(q[key])==set(p[key])
  assert all(q[key][name]==digest for name,digest in p[key].items() if name!='ge19_h4f3d33_direct_ge07_paired_first_interval.npz')
 else:assert q[key]==p[key],key
assert q['frozen_original_parent_sha256']['ge19_h4f3d33_direct_ge07_paired_first_interval.npz']=='41c75b883b7df7b1f57b72f0309d71e1c7c3779f291e524f33fa7532861eb264'
assert p['frozen_original_parent_sha256']['ge19_h4f3d33_direct_ge07_paired_first_interval.npz']!='41c75b883b7df7b1f57b72f0309d71e1c7c3779f291e524f33fa7532861eb264'
assert H(R/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz')==q['frozen_original_parent_sha256']['ge19_h4f3d33_direct_ge07_paired_first_interval.npz'],'D33_ACTUAL_NPZ_MISMATCH_D45'
d45=json.loads((R/'ge19_h4f3d45_h1_offclock_source_audit.json').read_text())
assert d45['originals_sha256']['ge19_h4f3d33_direct_ge07_paired_first_interval.npz']==q['frozen_original_parent_sha256']['ge19_h4f3d33_direct_ge07_paired_first_interval.npz'],'D45_PROVENANCE_MISMATCH'
failed=R/'ge19_H4F3D46_LOCAL_runner.log'
assert failed.is_file() and H(failed)=='4195bd8038fc84fcb78460d67306786c427b73dfcad1d69610a9ac32eb202d52' and 'GE19_D46_PARENT_SHA_FAIL_ge19_h4f3d33_direct_ge07_paired_first_interval.npz' in failed.read_text(),'ORIGINAL_D46_LOCAL_FAILURE_NOT_PRESERVED'
assert H(G/'run_local_h4f3d46r1_source_interpolation_counterfactual.sh')=='6d02ec331a6117b0e0528df58e912936c1876f8d1ae44d3821b78a4b348d5bfe','ORIGINAL_R1_RUNNER_CHANGED'
assert H(G/'h4f3d46r1_manifest_repair_selftest.py')=='27aabe60096e15ab7a0428e4d9a9578792eb25eae5161eba3b33a9e8db5f3822','ORIGINAL_R1_SELFTEST_CHANGED'
spec=importlib.util.spec_from_file_location('d46r1',new_py)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
mod.synth_test()
with tempfile.TemporaryDirectory() as tmp:
 bad=Path(tmp)/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz'
 bad.write_bytes((R/'ge19_h4f3d33_direct_ge07_paired_first_interval.npz').read_bytes()+b'\n')
 assert mod.sha(bad)!=q['frozen_original_parent_sha256']['ge19_h4f3d33_direct_ge07_paired_first_interval.npz'],'D33_TAMPER_NOT_REJECTED'
 try:mod.require(mod.sha(bad)==q['frozen_original_parent_sha256']['ge19_h4f3d33_direct_ge07_paired_first_interval.npz'],'PARENT_SHA_FAIL_ge19_h4f3d33_direct_ge07_paired_first_interval.npz')
 except RuntimeError as exc:assert 'PARENT_SHA_FAIL_ge19_h4f3d33_direct_ge07_paired_first_interval.npz' in str(exc)
 else:raise AssertionError('TAMPERED_D33_ACCEPTED')
print('GE19_D46R2_EXACT_TWO_LINE_DRIVER_AND_SINGLE_PARENT_HASH_REPAIR_PASS',flush=True)
print('GE19_D46R2_D45_ACCEPTED_REAL_D33_SHA_AND_TAMPER_NEGATIVE_PASS',flush=True)
print('GE19_D46R2_ORIGINAL_D46_FAILURE_AND_SOURCE_UNCHANGED_PASS',flush=True)
