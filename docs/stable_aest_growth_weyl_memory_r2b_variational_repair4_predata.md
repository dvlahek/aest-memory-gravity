# Stable AeST growth–Weyl memory R2b — technical repair 4 checkpoint

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This checkpoint is created after the fourth local R2b launch attempt stopped before any R2b science run, force-table normalization, or signed lambda probe was executed.

Observed state before repair:

- R2b import, science-lock, parent, and old-provenance checks passed.
- The native variational patch itself was installed: the stable residual marker, R2b marker, stable `s` trace, `chi=Q*s`, external-force hook, trace hook, runtime force/lambda/trace helpers, prototypes, preserved physical memory closure, and stable RHS chi count all audited true.
- The patcher stopped only because the audit key `old_trace_subtraction_absent` searched the entire generated `perturbations.c` for the historical expression `Q_aest*(a*theta_aest/(k*k)+alpha_aest)` and found an occurrence outside the newly inserted R2b trace block.
- Therefore no R2b forcing trace or lambda-probe result exists from this attempt and no science classification is assigned.

Repair rule fixed before another launch:

1. Do not change the frozen R2b preregistration commit `fc118356ea77be3b81854a95992a89ff7a1630bc`, physical equations, tau, bath order, integration tolerance, k anchors, redshift grid, lambda values, observables, gates, or thresholds.
2. Keep the R2b trace requirement exactly `chi = Q*s`.
3. Replace the over-broad whole-file absence audit by a scoped audit of the inserted R2b native-source trace block itself. The historical subtraction expression must be absent from that trace block. Unrelated legacy/source occurrences elsewhere in `perturbations.c` do not invalidate R2b.
4. Apply the same scoped source audit in the R2b Python science driver so G1 tests the actual diagnostic trace implementation rather than unrelated source text.
5. Historical R2, R2a, R1c, and all earlier R2b technical attempts remain unchanged.

This is a build/source-audit repair only. It does not alter the scientific test.