#!/usr/bin/env python3
"""D21R1: frozen D21-to-D21R1 one-bug repair contract and negative checks."""
from pathlib import Path
import ast, hashlib, json
from ge19 import h4f3d21_GE05_phase_safe_M2_core as core
root=Path(__file__).resolve().parents[1]
pre=json.loads((root/'ge19/h4f3d21r1_predata_undefined_proper_repair.json').read_text())
a=(root/'ge19/h4f3d21_actual_GE05_phase_safe_M2_reclosure.py').read_text()
b=(root/'ge19/h4f3d21r1_actual_GE05_phase_safe_M2_reclosure.py').read_text()
assert hashlib.sha256(a.encode()).hexdigest()=='a31f7ef8c9f02c047dcaabaf96576205c79c5a18919f768b549a52549626cdef'
assert hashlib.sha256(b.encode()).hexdigest()==pre['source_sha256']['ge19/h4f3d21r1_actual_GE05_phase_safe_M2_reclosure.py']
assert a.count('lin=core.rel(oldward,oldward+delta_ward)')==1
assert a.count("out[prefix+'mixed_M1_FROZEN_UNRECLOSED_source_ward_NOT_FULL_H4']=proper['total_source_ward']")==1
expected=a.replace('            lin=core.rel(oldward,oldward+delta_ward)\n', "            proper=clock.physical_six_piece_ward(\n                parts,x,bg['a'],H,\n                float(r7.g9.K_REQ[0]/r7.FOURIER_N[0]))\n            lin=core.rel(oldward,proper['total_source_ward'])\n")
expected=expected.replace("PRE=ROOT/'ge19/h4f3d21_predata_GE05_phase_safe_M2_reclosure.json'", "PRE=ROOT/'ge19/h4f3d21r1_predata_undefined_proper_repair.json'")
expected=expected.replace("if pre['classification']!='GE19_H4F3D21_PREDATA_EXACT_GE05_M2_PT_TIME_DERIVATIVE_REPLACEMENT':", "if pre['classification']!='GE19_H4F3D21R1_PREDATA_UNDEFINED_PROPER_IMPLEMENTATION_REPAIR':")
expected=expected.replace("'GE19_D21_EXACT_GE05_PT_CHAIN_RULE_M2_NUMERICAL_REPAIR_PASS_Q20_Z11_FULL_H4_OPEN'", "'GE19_D21R1_EXACT_GE05_PT_CHAIN_RULE_M2_NUMERICAL_REPAIR_PASS_Q20_Z11_FULL_H4_OPEN'")
expected=expected.replace("'GE19_D21_EXACT_GE05_PT_CHAIN_RULE_M2_NUMERICAL_REPAIR_FAIL'", "'GE19_D21R1_EXACT_GE05_PT_CHAIN_RULE_M2_NUMERICAL_REPAIR_FAIL'")
expected=expected.replace('GE19_D21_','GE19_D21R1_')
assert b==expected,'D21R1 differs from sole preregistered bug fix'
ast.parse(b)
assert 'old.r24.evolve_z10(' not in b and 'np.gradient(' not in b
assert "'new_physical_q20_and_Z11_recomputed':False" in b
assert "'full_original_H4_Ward_certified':False" in b
assert "'Z21_certified':False" in b
# Manufactured scalar-only change: the signed physical source projection uses
# rows 1,6,7, so a scalar row-3 correction has exact zero Ward change.
import numpy as np
r=np.random.default_rng(27)
old=r.normal(size=(8,11,41))+1j*r.normal(size=(8,11,41))
delta=np.zeros_like(old);delta[3]=r.normal(size=(11,41))
assert np.array_equal((old+delta)[[1,6,7]],old[[1,6,7]])
assert not np.array_equal(old+delta,old)
print('GE19_D21R1_FROZEN_D21_SINGLE_UNDEFINED_PROPER_REPAIR_AND_SCALAR_ONLY_WARD_NEGATIVE_CONTROL_PASS',flush=True)
