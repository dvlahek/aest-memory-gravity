# Stable AeST growth–Weyl memory R2b — technical repair note

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Status

The first local R2b invocation stopped before any variational trace or science run was produced.

The preregistered science lock, parent lock, and frozen CLASS provenance all passed. The failure occurred while applying the historical `v019w/apply_variational_forcing_patch.py` helper to the dedicated stable-R2b CLASS copy.

Observed error:

    RuntimeError: variational helper includes: expected one anchor, found 0 in .../source/aest_memory.c

No R2b result JSON/NPZ or variational science classification was produced. Therefore this is a technical pre-result failure and does not count as a scientific R2b outcome.

## Cause

The historical v0.19w helper expects the exact contiguous include block

    #include <math.h>
    #include <stddef.h>
    #include "aest_memory.h"

in `source/aest_memory.c` so that it can add file-I/O/runtime-loader headers. The current stable finite-memory source has an equivalent but differently arranged include header, so the historical literal anchor is absent.

This is a patch-compatibility issue only. It does not involve the AeST equations, memory closure, bath dynamics, certified residual state, observables, redshift grid, k anchors, variational lambdas, or any preregistered R2b gate.

## Frozen repair

Before invoking the unchanged historical v0.19w helper, the R2b wrapper may canonicalize only the relevant include lines in the dedicated temporary R2b CLASS copy:

- remove duplicate/existing exact include lines for `math.h`, `stddef.h`, `stdio.h`, `stdlib.h`, `string.h`, and `aest_memory.h`;
- prepend the exact three-line historical input anchor (`math.h`, `stddef.h`, `aest_memory.h`);
- invoke the unchanged v0.19w variational patch, which then expands the anchor to the required five standard headers plus `aest_memory.h`;
- preserve all existing R2b source audits, including stable `chi=Q*s`, physical memory closure, forcing hook, and absence of the subtraction-based trace.

No physical source equation or science threshold may change.

## Classification rule

The failed invocation is recorded only as `R2B_TECHNICAL_PATCH_COMPATIBILITY_FAIL_PRE_RESULT` in project history/provenance language. It does not alter the preregistration commit `fc118356ea77be3b81854a95992a89ff7a1630bc`, R2/R2a historical classifications, or any future R2b science classification.
