# Stable AeST growth–Weyl memory R2e — single-hook post-data checkpoint

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Frozen preregistration

R2e was preregistered before any corrected single-hook result in commit

`176b69261d61c9d43116a9bf82a99839fe328b43`.

Its immediate formal parent was

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_NON_HISTORY_NORMALIZATION_MISMATCH_CERTIFIED`,

with R2d post-data checkpoint

`d2589759cda81a590008c184cc2b061eada3ee28`.

All earlier historical classifications remain unchanged and are not retroactively reclassified by R2e.

## Source-level cause

The completed R2d CLASS source contained two consecutive copies of

`dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);`

so the diagnostic variational forcing entered the E equation twice while the physical finite-eta memory term entered once.

R2e prospectively corrected only this diagnostic duplication. The corrected source audit found

- historical external-force hook count = 2,
- corrected external-force hook count = 1,
- runtime external helper definition count = 1,
- physical `Bchi_aest *= aest_eta` occurrence count = 1,
- physical `E_rhs_aest -= 0.5*Q_aest*Bchi_aest` occurrence count = 1,
- stable `chi = Q*s` parent retained.

The physical finite-memory model was not changed.

## Formal R2e result

The completed run returned

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED`

with exit code 0.

All preregistered positive gates passed:

- R2E-G1 provenance and parent lock: PASS,
- R2E-G2 single-hook source correction: PASS,
- R2E-G3 patch neutrality: PASS,
- R2E-G4 corrected amplifier consistency: PASS,
- R2E-G5 duplicate-hook causal normalization: PASS,
- R2E-G6 corrected common-mode bound: PASS.

The resolved-separation gate did not pass.

Patch neutrality was exact at stored precision for both CLASS `d_m` and `phi+psi` at all three anchors.

## Absolute-normalization recovery

The corrected single-hook tangent reproduces the frozen finite-eta reference amplitude:

- k_h=0.09875: A_G=0.9928608817, A_L=0.9975142722,
- k_h=0.16125: A_G=0.9993303881, A_L=0.9996218637,
- k_h=0.19500: A_G=1.0046838377, A_L=0.9952634309.

Across all six channel/anchor values,

`0.9928608817 <= A <= 1.0046838377`.

The corrected tangent shapes also match the frozen finite-eta references with cosines above 0.9999993.

## Causal identification of the factor-two mismatch

The old R2d double-hook tangent divided by the corrected R2e single-hook tangent gives

- k_h=0.09875: S_G=1.9898025259, S_L=1.9950588894,
- k_h=0.16125: S_G=1.9993707303, S_L=1.9995941055,
- k_h=0.19500: S_G=1.9996543067, S_L=1.9997829499.

The old/new tangent cosines are essentially one. Thus the previously observed global factor-two variational normalization mismatch is certified as a diagnostic duplicate-hook artifact, not as a property of the physical finite-memory equations.

R2c and R2d remain valid historical records of the then-used diagnostic implementation and are not reclassified.

## Corrected growth–Weyl result

For the corrected lambda=30 tangent,

- k_h=0.09875: B_30=3.9653350e-3,
- k_h=0.16125: B_30=2.4319614e-4,
- k_h=0.19500: B_30=1.4418151e-4.

All three satisfy the preregistered one-percent common-mode criterion

`||L-G|| / max(||G||,||L||) <= 0.01`.

The residual `R=L-G` is not sufficiently reproducible under lambda=10 versus lambda=30 to certify a positive growth–Weyl separation. Therefore the positive MCMG shape bridge remains unlicensed in this stable-AeST regime.

The corrected G and L tangents are positive at all nine locked redshifts for all three anchors and increase strongly toward late times. Representative corrected lambda=30 values at z=0.2 are approximately

- k_h=0.09875: G=1.7523e-9, L=1.7454e-9,
- k_h=0.16125: G=1.88868e-8, L=1.88824e-8,
- k_h=0.19500: G=4.57984e-8, L=4.57918e-8.

## Licensed interpretation

R2e licenses the following statement in the locked stable-AeST regime (`tau H0=10`, order 20, tolerance 3e-8, tested anchors/redshifts):

The absolutely normalized first-order finite-memory response is common-mode between CLASS total-matter growth and the Weyl response to the preregistered one-percent bound.

It also licenses attribution of the historical factor-two variational normalization mismatch to the duplicated diagnostic external-force hook.

R2e does not license exact equality of growth and Weyl responses, a positive growth–Weyl separation, observational detection, permanent elasticity loss, or a fundamental new-physics claim.

## Next step

The numerical-normalization forensic line is closed. The next useful physics step should test generality and observational meaning of the corrected common-mode tangent, rather than further source forensics.
