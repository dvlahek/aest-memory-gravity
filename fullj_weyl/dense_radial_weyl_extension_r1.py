#!/usr/bin/env python3
from __future__ import annotations

import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "dense_radial_weyl_extension.py"

src = BASE.read_text()
old = "np.maximum(p_complex, delta2, 1.0e-300)"
new = "np.maximum(np.maximum(p_complex, delta2), 1.0e-300)"
if src.count(old) != 1:
    raise RuntimeError(f"expected exactly one dense-radial denominator expression, found {src.count(old)}")
src = src.replace(old, new)

# Technical source-load repair only. No equations, physical parameters, radial
# nodes, interpolation choices, tolerances, gates, or classification rules are
# changed relative to the preregistered implementation.
name = "fullj_weyl.dense_radial_weyl_extension_runtime"
mod = types.ModuleType(name)
mod.__file__ = str(BASE)
mod.__package__ = "fullj_weyl"
sys.modules[name] = mod
exec(compile(src, str(BASE), "exec"), mod.__dict__)

if __name__ == "__main__":
    raise SystemExit(mod.main())
