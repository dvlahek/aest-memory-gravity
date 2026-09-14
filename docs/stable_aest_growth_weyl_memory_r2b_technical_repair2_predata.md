# Stable AeST growth–Weyl memory R2b — technical repair 2 pre-result note

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Status before repair

The second local R2b attempt failed before any variational science result was generated.

The run passed the R2b import, science-lock, parent and old-CLASS provenance checks. The first technical include compatibility repair also passed:

    STABLE_AEST_R2B_VARIATIONAL_INCLUDE_COMPAT_PASS

The historical v0.19w patch then stopped while looking for its literal `native source-grid tangent trace` anchor in the current stable-residual `perturbations.c`:

    RuntimeError: native source-grid tangent trace: expected one anchor, found 0

No force table, lambda probe, R2b JSON/NPZ science result, or R2b classification was produced. Therefore the preregistered R2b science gates remain untouched and unevaluated.

## Diagnosis

The failure is a source-layout compatibility problem. The historical v0.19w helper searches for one exact multi-line text block around the CLASS `perturbations_sources()` background setup. The current stable AeST source no longer contains that literal block even though the same native source function and required variables remain present.

Continuing to adapt historical literal anchors one by one would be fragile and is unnecessary.

## Allowed repair

Replace the dependency on the historical v0.19w patcher with an R2b-local diagnostic patch that implements the same two operations directly:

1. add the historical trace/force-table runtime helper functions to `aest_memory.c` and their prototypes to `aest_memory.h`;
2. inside `perturbations_sources()`, locate the function semantically and insert the eta=0 force trace immediately after its native `a2 = a * a;` setup;
3. compute the trace with the certified stable residual state only,

       s = evolved index_pt_s_aest,
       chi = Q s,

   and the unchanged order-20 bath expression;
4. add the external diagnostic forcing hook immediately after the existing AeST E-equation derivative assignment.

The trace remains on the native CLASS source-sampling grid, as required by the frozen R2b preregistration. The physical finite-memory equations and physical `aest_eta=0` regime are unchanged.

## Frozen science remains unchanged

Do not alter:

- R2b predata commit `fc118356ea77be3b81854a95992a89ff7a1630bc`;
- R2a post-data parent `bbcf1e8e88743fb63ebe9b7e8da1202b8d3438dc`;
- `tau H0 = 10`;
- `memory_order = 20`;
- physical `aest_eta = 0`;
- integration tolerance `3e-8`;
- anchors, redshifts, observables, lambda values, thresholds, gates or classification logic.

This note is a pre-result technical repair record only. It does not reclassify R2, R2a, R1c, or any other historical result.
