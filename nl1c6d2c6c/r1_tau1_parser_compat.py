#!/usr/bin/env python3
from __future__ import annotations

# D2C6C-R1 technical compatibility shim.
# The validated v0.19u tau1 parser accepts only memory orders 39/47 even when
# memory is disabled. The inherited D2C6B base CLASS helper still emits 16.
# Override only that inert memory-off parser value; no physics/gates change.

from nl1c6d2c6c import eta0_nonlinear_memory_tangent as c

_original_build_params = c.m.build_params


def _build_params_tau1_compatible():
    p = dict(_original_build_params())
    p["aest_memory_order"] = 39
    return p


c.m.build_params = _build_params_tau1_compatible

if __name__ == "__main__":
    raise SystemExit(c.main())
