#!/usr/bin/env python3
from __future__ import annotations

from fullj_weyl import stable_aest_r12a_eg_weyl_growth_consistency as base

# R12a Repair01 is a provenance-pointer correction only.
# The original preregistration and implementation remain frozen.
CORRECT_R11A_R02_POSTDATA_LOCK = "84c4ba550ce3b262c78c69054056ab2778014677"
INVALID_R11A_R02_POSTDATA_LOCK = "d9e2e0e6da65126a81d02f32e65f83410bc8cc7c"

if base.R11A_R02_POSTDATA_LOCK != INVALID_R11A_R02_POSTDATA_LOCK:
    raise RuntimeError(
        "R12a Repair01 expected the frozen original invalid R11a Repair02 lock; "
        f"found {base.R11A_R02_POSTDATA_LOCK}"
    )

base.R11A_R02_POSTDATA_LOCK = CORRECT_R11A_R02_POSTDATA_LOCK


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
