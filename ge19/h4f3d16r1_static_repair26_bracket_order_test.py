#!/usr/bin/env python3
"""D16R1 source-level regression for Repair26 boundary-initialization order."""
from pathlib import Path
import ast,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'ge19/h4f3d16_actual_original_H1dot_Hermite_physical_bath.py'
NEW=ROOT/'ge19/h4f3d16r1_actual_original_H1dot_Hermite_physical_bath.py'
PRE=ROOT/'ge19/h4f3d16r1_predata_repair26_bracket_initialization.json'
pre=json.loads(PRE.read_text())
assert hashlib.sha256(OLD.read_bytes()).hexdigest()==pre['frozen_original_D16_source_SHA256']
o=OLD.read_text();n=NEW.read_text()
assert o.index('boundaries={n:r24.full_history_boundary') < o.index('bgs,_,_,_,_,_,_,_,_=d15.d13.old.build_context')
assert n.index('bgs,_,_,_,_,_,_,_,_=d15.d13.old.build_context') < n.index('boundaries={n:r24.full_history_boundary')
assert n.count('boundaries={n:r24.full_history_boundary')==1
# The new driver cannot change physical computation: remove exactly prereg guard,
# repaired bracket guard/order, implementation metadata and classification.
ast.parse(n)
assert 'r24.TRACE_LO_A!=d15.d13.old.r27.REPAIR26_TRACE_LO_A' in n
assert 'r24.TRACE_HI_A!=d15.d13.old.r27.REPAIR26_TRACE_HI_A' in n
assert "if oj.exists() or on.exists():raise RuntimeError('D16 refuses overwrite')" in n
assert "N_SUB=(4,8,16)" in n
assert "PARENT={" in n
assert "r24.step_linear_nd,sub,'hermite'" in n
print('GE19_H4F3D16R1_ORIGINAL_REPAIR26_BRACKET_ORDER_STATIC_PASS')
