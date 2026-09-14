# Project history continuation — corrected growth–Weyl bridge through R2e

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This continuation extends `docs/project_history_checkpoint_2026-09-14.md`. Historical classifications remain fixed and are not retroactively changed.

## Stable AeST growth–Weyl sequence

12. `STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TANGENT_FAIL`
   - direct finite-eta total-matter/Weyl test using CLASS `d_m` and `phi+psi`.
   - individual G and L tangents were smooth, but the small residual R=L-G was cancellation dominated and failed preregistered tangent/separation gates.
   - this historical FAIL remains unchanged.

13. `STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEPARATION_UNRESOLVED`
   - eta leverage was increased and a tighter tolerance control added.
   - direct finite differencing showed that the residual separation was at a numerical floor while G and L individually remained smooth.
   - no positive growth–Weyl separation was certified.

14. `STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED`
   - eta=0 variational forcing isolated the first-order response below the direct finite-difference residual floor.
   - the preregistered positive separation gate did not pass.
   - the one-percent common-mode bound passed on all three anchors.
   - a posthoc comparison found a global approximately factor-two absolute-normalization mismatch relative to the direct finite-eta tangent.

15. `STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED`
   - source-grid forcing was densified from 123 to 489 target-k time samples.
   - the variational response converged with density, but the absolute amplitude factor remained approximately 0.50 relative to the direct finite-eta reference.
   - sparse source-grid interpolation was therefore rejected as the explanation.

16. `STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_NON_HISTORY_NORMALIZATION_MISMATCH_CERTIFIED`
   - forcing was traced directly from the physical memory RHS throughout the perturbation ODE history.
   - full-history traces extended to tau near the beginning of integration and agreed with the dense source-grid forcing on their overlap at about 1e-5 relative L2.
   - the approximately factor-two mismatch persisted.
   - missing early forcing history was therefore rejected as the explanation.

17. `STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED`
   - a source audit found two consecutive copies of the diagnostic external variational-force hook in the completed R2d source.
   - R2e was preregistered before correction and removed exactly one duplicate hook without changing the physical finite-memory equations.
   - source audit: historical hook count 2, corrected hook count 1, one runtime helper, one physical eta multiplication, one physical memory closure.
   - the old/new tangent norm ratio was 1.9898--1.9998 with cosine essentially one.
   - the corrected finite-eta-reference amplitude factor became 0.99286--1.00468 across all six growth/Weyl anchor cells.
   - all corrected G and L tangents were positive over the nine locked redshifts.
   - corrected common-mode statistic B_30 was 3.965e-3, 2.432e-4, and 1.442e-4 for k_h=0.09875, 0.16125, and 0.19500.
   - the preregistered one-percent common-mode gate passed on all three anchors.
   - residual R=L-G was not reproducible enough to certify a positive separation.

R2e post-data checkpoint:

`c0fe57f73a7785c21b1fecd7455f19148d5f812d`.

## Current scientific interpretation

The approximately factor-two variational mismatch was a diagnostic implementation artifact caused by duplicate forcing injection. After correction, the full-history eta=0 variational tangent agrees in both shape and absolute amplitude with the direct finite-eta derivative.

In the certified stable-AeST long-relaxation regime (`tau H0=10`, order 20), the first-order finite-memory perturbation produces a measurable numerical response in both CLASS total-matter growth and Weyl response, but those two fractional responses are common-mode to the preregistered one-percent bound over the tested anchors and redshifts.

Therefore the simple positive MCMG growth–Weyl lag is not reproduced in this tested stable-AeST realization. This is a host-dependent model-discriminating result, not a contradiction of the host-independent MCMG theorem.

No observational detection, permanent elasticity loss, or fundamental new-physics claim is licensed.

## Roadmap after R2e

The numerical-forensic phase is closed. The next useful sequence is:

1. corrected scale-generality test at the already certified tau H0=10 regime;
2. if common-mode persists over a broader k interval, project the corrected response into direct observables such as growth-rate/f-sigma8 and linear lensing quantities;
3. only after scale generality and observable projection, consider data or forecast work;
4. tau H0=1 remains uncertified and should not be folded into the main result without a separate dedicated validation.
