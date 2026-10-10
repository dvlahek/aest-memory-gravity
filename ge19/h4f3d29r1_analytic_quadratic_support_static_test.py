#!/usr/bin/env python3
"""D29R1 canonical-D28-hash-only repair checks, including historical D29 negative controls."""
from __future__ import annotations
import ast,hashlib,json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=R/'ge19/h4f3d29_analytic_quadratic_support.py'
new=R/'ge19/h4f3d29r1_analytic_quadratic_support.py'
old_pre=R/'ge19/h4f3d29_analytic_quadratic_support_prereg.json'
pre=R/'ge19/h4f3d29r1_analytic_quadratic_support_prereg.json'
d28lock=R/'ge19/h4f3d28_ge06_shift_two_term_lock.json'
lock=R/'ge19/h4f3d29r1_analytic_quadratic_support_lock.json'
original=json.loads(old_pre.read_text()); updated=json.loads(pre.read_text())
d=json.loads(d28lock.read_text()); l=json.loads(lock.read_text())
assert sha(old)==updated['D29_original_driver_sha256']
assert sha(old_pre)==updated['D29_original_prereg_sha256']
assert sha(d28lock)==updated['D28_original_lock_sha256']
key='ge19/h4f3d28_ge06_shift_two_term_provenance.py'
assert len(original['frozen_source_code_sha256'][key])==43
assert len(updated['frozen_source_code_sha256'][key])==64
assert updated['frozen_source_code_sha256'][key]==d['sha256_local_files'][key]
for p,want in l['sha256_local_files'].items():
    assert sha(R/p)==want,(p,'local file SHA mismatch')
old_ast=ast.parse(old.read_text());new_ast=ast.parse(new.read_text())
for name in ('quadratic_support','positive_mode_jet','original_ge06_mode40','relative','pair'):
    o=next(n for n in old_ast.body if isinstance(n,ast.FunctionDef) and n.name==name)
    n=next(n for n in new_ast.body if isinstance(n,ast.FunctionDef) and n.name==name)
    assert ast.dump(o)==ast.dump(n),name
assert updated['in_support_b_term_replay_relative_limit']==original['in_support_b_term_replay_relative_limit']==1e-11
assert updated['in_support_global_row_replay_relative_limit']==original['in_support_global_row_replay_relative_limit']==1e-9
assert updated['first_order_modes']==original['first_order_modes']
assert updated['selected_modes']==original['selected_modes']
assert updated['frozen_outputs_sha256']==original['frozen_outputs_sha256']
# Verify that the correction cannot be generalized to a fabricated SHA.
def pure_guard(u,o,d):
    src='ge19/h4f3d28_ge06_shift_two_term_provenance.py'
    assert len(o['frozen_source_code_sha256'][src])==43
    assert u['frozen_source_code_sha256']=={src:d['sha256_local_files'][src]}
pure_guard(updated,original,d)
for bad in ('0'*64,original['frozen_source_code_sha256'][key]):
    u=dict(updated);u['frozen_source_code_sha256']={key:bad}
    try:pure_guard(u,original,d)
    except AssertionError:pass
    else:raise AssertionError('D29R1 accepted bad/fabricated SHA')
subprocess.run([sys.executable,str(R/'ge19/h4f3d29_analytic_quadratic_support_static_test.py')],cwd=R,check=True)
print('GE19_D29R1_64_HEX_CORRECTION_ONLY_AND_NEGATIVE_CONTROLS_PASS',flush=True)
