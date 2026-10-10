#!/usr/bin/env python3
import ast,hashlib,pathlib
p=pathlib.Path(__file__).with_name('ge19_d47_parent_preflight.py')
t=ast.parse(p.read_text()); assert any(isinstance(n,ast.FunctionDef) and n.name=='digest' for n in t.body)
s=p.read_text();assert "'physics_certified':False" in s and "if out.exists()" in s
print('GE19_D47_PREFLIGHT_STATIC_SELFTEST_PASS')
