# Stable AeST observable projection R5b — pre-result implementation audit

Date: 2026-09-14

This checkpoint was recorded after R5b implementation and before any R5b science result.

## Locked science design

Pre-data lock: `f6886b2b934330036e9239e3fb2d3678dee3c72f`.
Parent R5a post-data lock: `118c680c3c05e7ca95bbc16700bd846e200a7ab6`.
Parent classification required by the driver: `STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_ETA_SCALING_FAIL`.

## Diff audit

The implementation diff from the R5b pre-data lock contains exactly two added files:

- `fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py`,
- `fullj_weyl/run_local_stable_aest_observable_projection_r5b_derivative_zero.sh`.

No R5, R5a, R4, stable-chi patch, or historical result file was modified after the R5b pre-data lock.

## Anti-stale audit

The driver freezes certification eta values `0, 0.01, 0.025, 0.05`; `eta=0.1` is a diagnostic bridge only. Tight control is `eta=0,0.01`.

The certification boolean uses only:

- T(0.01) versus T(0.025),
- T(0.025) versus T(0.05).

T(0.05) versus T(0.1) is written only to `bridge_metrics` and is not used in the derivative PASS/FAIL expression.

The runner contains explicit anti-stale assertions rejecting historical R5 eta=10 labels, historical R5a eta=0.25/0.5 run labels, R4/R5 parent-lock variables, and R5/R5a disposable source-tree names from the R5b driver.

## Source/build audit

The runner always deletes and reconstructs a dedicated disposable R5b CLASS source tree and Python target from the frozen `e85808324f51fc694d12e3ed7439552a3c3f9540` parent.

It reapplies only the stable-chi residual patch, verifies the frozen `aest_memory.c` SHA, removes exactly one dormant historical diagnostic forcing hook in the disposable source, then requires exactly one physical eta multiplier, exactly one physical memory closure, and zero diagnostic external-force injections.

All `AEST_TANGENT_*`, R2d trace, and E-RHS diagnostic environment variables are explicitly unset before the science run.

No R5b result existed when this audit checkpoint was written.