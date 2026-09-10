# NL1C6D2C4R1 pre-data: derivative-control numerical repair

Status: **PREREGISTERED BEFORE ANY D2C4R1 RESULT**.

## Purpose

D2C4 passed every exact structural, deep-MOND, constitutive-bound, and high-gradient gate, but its finite-difference derivative control failed at `5.037472089274e-06` versus the frozen `2e-6` tolerance. Inspection shows the worst quantities are extremely small `F_Q/F_YQ` values differentiated in dimensionless `Z` with the original `h_Z=1e-6`, where subtractive cancellation dominates.

Historical D2C4 remains FAIL. This R1 does not alter the completion family, `epsilon_mix`, any physics parameter, or the derivative tolerance.

## Frozen repair

Retain the D2C4 analytic formulas and all deterministic `(beta0, kind, sigma, x, Z)` test points.

- Keep the existing Y-direction finite-difference rule unchanged.
- Replace the single Z-direction step `h_Z=1e-6` by the fixed three-step set:

`h_Z = [1e-3, 3e-4, 1e-4]`.

For every tested `F_Q` and `F_YQ` derivative, **all three** step sizes must satisfy the unchanged relative tolerance `2e-6`. No minimum-over-step or best-step selection is allowed.

All D2C4 C4.1-C4.5 exact/asymptotic gates are recomputed unchanged and must still pass. The Y-direction derivative check must remain <= `2e-6`.

## Classification

PASS only if all inherited D2C4 structural gates pass and every preregistered finite-difference check at every fixed step passes:

`NL1C6D2C4R1_DERIVATIVE_CONTROL_REPAIR_PASS`

otherwise:

`NL1C6D2C4R1_DERIVATIVE_CONTROL_REPAIR_FAIL`

Only PASS licenses the action-level nonlinear FLRW current/vector/constraint derivation. No nonlinear trajectory, solver change, memory/eta/likelihood/refit, or branch selection is performed here.
