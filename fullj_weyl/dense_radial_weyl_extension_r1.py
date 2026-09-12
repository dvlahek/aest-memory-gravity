#!/usr/bin/env python3
from __future__ import annotations

import inspect
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "dense_radial_weyl_extension.py"

# Repair 1: NumPy accepts only two positional arrays in maximum().  This is a
# postprocessing expression repair only; no gate or physical quantity changes.
src = BASE.read_text()
old = "np.maximum(p_complex, delta2, 1.0e-300)"
new = "np.maximum(np.maximum(p_complex, delta2), 1.0e-300)"
if src.count(old) != 1:
    raise RuntimeError(f"expected exactly one dense-radial denominator expression, found {src.count(old)}")
src = src.replace(old, new)

# Load the preregistered dense-radial implementation without editing its source.
name = "fullj_weyl.dense_radial_weyl_extension_runtime"
mod = types.ModuleType(name)
mod.__file__ = str(BASE)
mod.__package__ = "fullj_weyl"
sys.modules[name] = mod
exec(compile(src, str(BASE), "exec"), mod.__dict__)

# Repair 2: the inherited D2C6 CLASS loader was written for the historical
# six-mode campaign and contains the literal guard len(histories) != 6.  The
# dense-radial preregistration intentionally asks CLASS for 21 k values.  Patch
# only that cardinality check in the runtime function so the expected number is
# len(K_MPC), which is set by the dense implementation before data preparation.
# The underlying D2C6 source file remains untouched.
prepare = mod.m.prepare_class_data
prepare_src = inspect.getsource(prepare)
old_guard = "if len(histories)!=6:"
new_guard = "if len(histories)!=len(K_MPC):"
old_msg = 'raise InputIncomplete(f"expected 6 dense scalar histories, got {len(histories)}")'
new_msg = 'raise InputIncomplete(f"expected {len(K_MPC)} dense scalar histories, got {len(histories)}")'
if prepare_src.count(old_guard) != 1:
    raise RuntimeError(
        f"expected exactly one inherited six-history guard, found {prepare_src.count(old_guard)}"
    )
if prepare_src.count(old_msg) != 1:
    raise RuntimeError(
        f"expected exactly one inherited six-history error message, found {prepare_src.count(old_msg)}"
    )
prepare_src = prepare_src.replace(old_guard, new_guard).replace(old_msg, new_msg)
prepare_globals = prepare.__globals__
exec(compile(prepare_src, inspect.getsourcefile(prepare) or "<dense-loader-repair>", "exec"), prepare_globals)

DENSE_HISTORY_LOADER_REPAIR_ACTIVE = True

# Technical runtime repairs only. No equations, physical parameters, radial
# nodes, interpolation choices, tolerances, gates, or classification rules are
# changed relative to the preregistered implementation.
if __name__ == "__main__":
    raise SystemExit(mod.main())
