# Stable AeST growth–Weyl memory R2b — technical repair 5 checkpoint

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This checkpoint is created after the fifth local R2b launch attempt stopped during compilation, before any R2b force-table normalization or signed lambda science probe was executed.

Observed state before repair:

- R2b import, science-lock, parent, and old-provenance checks passed.
- The native R2b variational patch completed its source audit successfully: stable host marker, R2b marker, native source function, trace on the stable residual `s`, `chi=Q*s`, external-force hook, trace hook, runtime force/lambda/trace support, prototypes, preserved physical memory closure, stable RHS chi count, legacy literal normalization, and required I/O headers all passed.
- Compilation then failed in `source/aest_memory.c` because the file already contained one complete historical `aest_tangent_*` runtime helper and the R2b patch appended a second complete copy. The compiler reported duplicate definitions of `_aest_tf_*`, `aest_tangent_trace_force`, `_aest_tangent_load_force`, `_aest_tangent_select_k`, and `aest_tangent_external_force`.
- Therefore no R2b forcing trace or lambda-probe result exists from this attempt and no R2b science classification is assigned.

Repair rule fixed before another launch:

1. Do not change the frozen R2b preregistration commit `fc118356ea77be3b81854a95992a89ff7a1630bc`, physical equations, tau, bath order, tolerance, k anchors, redshift grid, lambda values, observables, gates, or thresholds.
2. Treat the existing complete `aest_tangent_*` runtime implementation as reusable infrastructure. Detect it by function symbols and required environment-variable support, not by the new R2b helper comment marker.
3. If both `aest_tangent_trace_force(...)` and `aest_tangent_external_force(...)` plus `AEST_TANGENT_TRACE_FILE`, `AEST_TANGENT_FORCE_FILE`, and `AEST_TANGENT_LAMBDA` already exist, do not append another helper. Ensure required prototypes and standard C headers remain present.
4. If only a partial/inconsistent helper is found, stop with an explicit technical error instead of mixing implementations.
5. Keep the R2b native source trace and external-force insertion unchanged. Historical R2/R2a/R1c results and all earlier R2b technical attempts remain unchanged.

This repair changes build idempotence only. It does not alter the R2b scientific test or the memory model.
