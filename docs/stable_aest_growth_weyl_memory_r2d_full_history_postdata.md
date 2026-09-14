# Stable AeST growth–Weyl memory R2d — post-data checkpoint

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Frozen parent

R2d was preregistered in commit

`ee6ad94194802aed2622a314ac44df679fdee0f8`

after the completed R2c result

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED`.

R2c post-data checkpoint commit:

`23af2c6f1abbedfa63c7e41d4cb7fc0aaf36424c`.

R2b remains formally

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED`

and all earlier historical classifications remain unchanged.

## Formal R2d result

The completed full-history RHS variational audit returned

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_NON_HISTORY_NORMALIZATION_MISMATCH_CERTIFIED`

with exit code 0.

The preregistered gates were:

- G1 provenance and parent lock: PASS
- G2 full-history coverage: PASS
- G3 overlap trace consistency and patch neutrality: PASS
- G4 full-history amplifier consistency: PASS
- G5 absolute normalization: FAIL
- G6 full-history common-mode bound: PASS
- G7 resolved full-history separation: FAIL
- G8 persistent coherent normalization mismatch: PASS.

Therefore the completed experiment rejects missing pre-source-grid history as the explanation of the approximately factor-two normalization mismatch.

## Full-history coverage

The direct physical-RHS trace extended from approximately tau=0.53--1.05 to tau=14151.63 across the three locked anchors, compared with the R2c source-grid start at tau=5174.72.

Target-k unique tau counts were:

- k_h=0.09875: 4075
- k_h=0.16125: 5315
- k_h=0.19500: 6128.

The transport table covered the full CLASS transfer grid with 699 k modes.

## Direct RHS/source-grid overlap

On the already completed R2c source-grid interval, the direct in-block RHS forcing and dense R2c forcing agreed extremely well:

- k_h=0.09875: E_force=9.63548e-6, C_force=0.999999999962
- k_h=0.16125: E_force=1.08618e-5, C_force=0.999999999951
- k_h=0.19500: E_force=1.00357e-5, C_force=0.999999999959.

This strongly supports that the R2c forcing reconstruction measured the same physical forcing on their common temporal interval.

Patch neutrality was exact at stored precision for both CLASS total matter and Weyl transfer vectors at all three anchors.

## Persistent absolute normalization mismatch

The full-history variational tangents retained the same approximately factor-two amplitude mismatch against the frozen finite-eta reference.

The six amplitude factors were tightly clustered:

- k_h=0.09875: A_G=0.498975, A_L=0.499992
- k_h=0.16125: A_G=0.499822, A_L=0.499912
- k_h=0.19500: A_G=0.502429, A_L=0.497686.

Thus

`A in [0.497686, 0.502429]`.

The temporal/redshift shapes remained almost perfectly aligned with the finite-eta reference, with absolute-shape cosines above 0.9999993.

Hence the mismatch is a stable global normalization difference, not a source-grid density effect and not a missing-early-history effect.

No ad hoc factor-two rescaling is licensed.

## Growth–Weyl relation

The primary full-history common-mode statistic remained below the preregistered one-percent bound at all three anchors:

- k_h=0.09875: B_30=1.36049e-3
- k_h=0.16125: B_30=1.33359e-4
- k_h=0.19500: B_30=8.15619e-5.

However, because the absolute full-history tangent is not normalized against the finite-eta reference, R2d does not license the absolute full-history tangent or a new positive growth–Weyl separation claim. The formal R2b one-percent common-mode result remains unchanged and is not reclassified.

## Licensed interpretation

R2d establishes that extending the diagnostic forcing from the late CLASS source grid to the full perturbation-RHS history does not remove the coherent approximately factor-two normalization mismatch.

Therefore the next follow-up must audit source-equation / parameter semantics rather than source-grid sampling density or missing early temporal support.

The most direct next question is why the signed external forcing corresponding to the analytic eta derivative produces approximately twice the finite-eta tangent despite matching its redshift shape nearly perfectly.

No observational detection, permanent elasticity loss, exact growth/Weyl equality, or fundamental new-physics claim is licensed.

## Packaging note

The full-k RHS trace contains several million generated rows per anchor and inflated the original reproducibility ZIP above 300 MB. These tables are deterministic intermediate products and are not needed to classify R2d once the JSON, NPZ, logs, source code, preregistration, and post-data checkpoint are retained. Future bundles should exclude the raw/full-k trace tables and retain only compact result artifacts plus reproducibility code and metadata.
