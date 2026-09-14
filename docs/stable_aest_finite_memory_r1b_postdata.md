# Stable AeST finite-memory R1b — post-data checkpoint

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Formal result

The preregistered R1b classification is

    STABLE_AEST_FINITE_MEMORY_R1B_ETA_TANGENT_FAIL

This classification is historical and must not be reclassified.

All provenance, matched-baseline regularity, nonzero-response, and relaxation-time-dependence gates passed. The primary eta-tangent consistency gate and tight-tolerance tangent reproducibility gate failed because all three `tau H0 = 1` cells were unresolved.

## Resolved long-relaxation branch

For `tau H0 = 10`, all three anchors passed the primary matched-bath eta-tangent consistency test:

- k_h=0.10000: E_25_50=1.479e-3, E_50_100=4.150e-4
- k_h=0.16500: E_25_50=5.280e-5, E_50_100=7.723e-5
- k_h=0.19750: E_25_50=6.281e-5, E_50_100=6.133e-5

The same three cells also passed the preregistered tight-tolerance tangent reproducibility test between `tol_perturbations_integration = 1e-7` and `3e-8`:

- k_h=0.10000: C_tol=1.282e-2, cosine=0.999986067
- k_h=0.16500: C_tol=9.575e-3, cosine=0.999954262
- k_h=0.19750: C_tol=2.021e-4, cosine=0.999999993

The tight matched Weyl response amplitudes at eta=0.01 were finite and nonzero:

- 5.527e-12, 6.382e-11, 1.466e-10 across the three anchors.

Thus the long-relaxation `tau H0 = 10` branch exhibits a reproducible matched-bath first-order Weyl response within the tested k range.

## Unresolved short-relaxation branch

For `tau H0 = 1`, all three anchors failed both primary eta-tangent consistency and tight-tolerance reproducibility:

Primary max tangent errors were 0.761, 1.365, and 1.697.

Tight-tolerance comparison gave:

- k_h=0.10000: C_tol=0.3305, cosine=0.9443
- k_h=0.16500: C_tol=1.4077, cosine=-0.3874
- k_h=0.19750: C_tol=0.7939, cosine=0.7964

The matched response is nonzero but not numerically reproducible at the current tolerances. No physical nonlinearity or instability claim is licensed for this branch.

## Relaxation-time comparison

The preregistered matched-tangent relaxation-time statistic was finite and above threshold at all three anchors:

- T_tau=1.0831 at k_h=0.10000
- T_tau=1.5963 at k_h=0.16500
- T_tau=0.4475 at k_h=0.19750

Because the `tau H0 = 1` tangent is not tolerance-resolved, these values are diagnostic only and are not yet a certified physical comparison between relaxation times.

## Interpretation lock

The correct current interpretation is:

- historical R1 remains `STABLE_AEST_FINITE_MEMORY_R1_ETA_SMOOTHNESS_FAIL`;
- R1b remains `STABLE_AEST_FINITE_MEMORY_R1B_ETA_TANGENT_FAIL`;
- the stable AeST host itself remains numerically certified;
- the finite-memory `tau H0 = 10` branch shows a clean, reproducible first-order matched Weyl tangent;
- the `tau H0 = 1` branch is unresolved at the tested numerical precision;
- no observational, new-physics, physical-instability, or permanent-elasticity-loss claim is licensed.

## Recommended next step

Do not continue broad AeST forensic scans. Instead preregister a narrow R1c long-relaxation certification using `tau H0 = 10` only, held-out k anchors, and an independent bath-discretization check (`memory_order = 16` versus `20`). A successful R1c can formally license the growth-Weyl comparison against the host-independent MCMG first-moment relation without depending on the unresolved short-relaxation branch.
