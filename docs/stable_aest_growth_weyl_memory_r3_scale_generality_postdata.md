# Stable AeST growth–Weyl memory R3 — scale-generality post-data checkpoint

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This checkpoint records the completed R3 result without changing any historical classification.

## Formal outcome

`STABLE_AEST_GROWTH_WEYL_MEMORY_R3_SCALE_GENERALITY_CERTIFIED`

The runner completed with EXIT=0.

Parent R2e remains:

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED`.

## Frozen regime

- direct physical finite-eta calculation, no diagnostic variational forcing in the science metrics
- tau H0 = 10
- memory order = 20
- tolerance = 3e-8
- eta in {0, 0.005, 0.01}
- redshifts z = {6,5,4,3,2,1.5,1,0.5,0.2}
- held-out stable-chi scales k_h = {0.10000, 0.10125, 0.10250, 0.10375, 0.16500, 0.19750, 0.19875}
- D_m = CLASS `d_m`
- W = `phi+psi`

## Gates

All preregistered gates passed:

- R3-G1 provenance and parent lock: PASS
- R3-G2 transfer basis and finite-run validity: PASS
- R3-G3 individual finite-eta tangent consistency: PASS
- R3-G4 held-out common-mode generality: PASS
- R3-G5 nonzero late-time physical response: PASS

All 21 physical CLASS runs were finite and transfer-basis valid.

All seven held-out scales passed the strict tangent-consistency criterion and the strict common-mode criterion.

Summary:

- `tangent_strict_count = 7/7`
- `common_mode_strict_count = 7/7`
- `late_pass_count = 7/7`
- `max_B005 = 0.002142699940106572`
- `max_B01 = 0.002175482795441085`

Thus the worst observed relative growth–Weyl mismatch over the held-out scales is about 2.18e-3, well below the preregistered one-percent common-mode bound. The licensed statement remains the preregistered one-percent bound, not equality at the observed numerical level.

The finite-eta tangents are individually highly reproducible. Across the seven cells, the reported G and L tangent discrepancies are of order 1e-4 to 1e-3 with cosines effectively one.

## Physical interpretation

R3 establishes that the corrected R2e result is not confined to the three original anchors. In the certified tau H0=10 stable-AeST regime, direct physical finite-eta total-matter and Weyl responses remain common-mode across seven additional stable-chi scales.

The response is strongly late-time activated on every held-out scale. At very early redshifts some absolute tangent components are at approximately numerical-zero scale and individual signs are not used as a physics claim.

R3 does not certify a positive growth–Weyl separation. It strengthens the model-specific null result relative to the simple MCMG positive-lag expectation: in this stable AeST realization, the first-order physical memory perturbation maps almost identically into CLASS total-matter growth and Weyl response across the tested scale range.

## Licensed next step

`observable_projection_licensed = true`.

The next stage should project the certified physical response into linear observable combinations while preserving the distinction between model transfer responses and actual survey likelihood constraints.

No observational detection, permanent-elasticity-loss, or fundamental new-physics claim is licensed by R3.