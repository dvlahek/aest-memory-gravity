# Full-J dense radial CLASS-residual R2 — locked result

## Classification

The preregistered independent 20-point H3 validation completed and is locked as

`FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_FAIL`.

This is a completed science result, not an infrastructure abort. The isolated dense-k64 corrected CLASS build used the same pinned CLASS commit and corrected AeST patch chain as the preceding R2 lineage, with only `_MAX_NUMBER_OF_K_FILES_` increased from 30 to 64 to permit the frozen 41-value `k_output_values` request.

## Completed direct holdouts

All 20/20 new H3 single-mode R2 integrations completed at

`k/h = [0.0325,0.0375,0.0425,0.0475,0.05375,0.06125,0.06875,0.07625,0.0825,0.0875,0.0925,0.0975,0.10625,0.11875,0.13125,0.14375,0.15625,0.16875,0.18125,0.19375] Mpc^-1`.

Canonical residuals were approximately `3.66e-15` to `6.24e-15`. Hamiltonian and momentum correction residuals remained at approximately machine precision (`~1e-16`) and shear residuals were zero.

## Numerical summary

- corrected-CLASS K2 cross-run median relative difference: `0.0`
- corrected-CLASS K2 cross-run maximum relative difference: `0.0`
- new H3 initial CLASS normalization maximum: `4.0242759111697296e-16`
- zero-safe phase global norm: `9.519516488978736e-10`
- maximum absolute imaginary transfer: `1.8285467002274772e-09`
- maximum real-projection power change: `1.493380934245691e-14`
- maximum new H3 saturation residual: `0.19981579344181175`
- K2-residual H3 transfer-L2 median: `2.3652640552532592e-05`
- K2-residual H3 transfer-L2 maximum: `0.0351059070615506`
- K2-residual H3 power-L2 median: `5.901993962221471e-06`
- K2-residual H3 power-L2 maximum: `0.008510304312152293`
- K2-residual H3 peak-normalized power maximum: `0.007829628106868124`
- holdout redshifts improved by K2 vs K1 in transfer: `0/9`
- holdout redshifts improved by K2 vs K1 in power: `0/9`
- continuous residual-correction K1->K2 median: `5.454101522984535e-05`
- continuous residual-correction K2->K3 median: `5.8392282390062464e-05`
- continuous residual-correction K2->K3 maximum: `0.08552128517634702`
- total K2->K3 transfer-L2 maximum on direct K3 nodes: `0.02437338490591279`
- total K2->K3 power-L2 maximum: `0.004868668241485719`
- total K2->K3 peak-normalized power difference maximum: `0.005368725248183992`
- direct power identity relative residual: `0.0`

## Gate state

PASS:

- `R2_G1_locked_provenance_setup`
- `R2_G2_completed_K2_state_integrity`
- `R2_G3_CLASS_cross_run_consistency`
- `R2_G4_new_H3_direct_health`
- `R2_G5_new_H3_initial_CLASS_normalization`
- `R2_G6_new_H3_zero_safe_phase`
- `R2_G11_power_sanity`

FAIL:

- `R2_G7_new_H3_saturated_closure`
- `R2_G8_independent_K2_residual_holdout_accuracy`
- `R2_G9_residual_refinement_improvement`
- `R2_G10_K2_to_K3_residual_convergence`

## Interpretation

The R2/metric solve itself remains numerically healthy. The first two low-k H3 nodes give saturation residuals `0.1336` and `0.1998`, while all subsequent H3 nodes return to approximately `4e-5` to `2e-4`. Therefore the preregistered blanket saturated-Laplacian closure does not hold uniformly over the isolated single-mode H3 probe set.

The residual representation is much more accurate in power than in signed transfer: the worst H3 power-L2 error is `0.851%` and the worst peak-normalized power error is `0.783%`, while the worst signed-transfer L2 error is `3.511%`, narrowly above the frozen 3% gate. However, K2 does not improve over K1 on any of the nine redshifts, and the residual-correction K2->K3 convergence is not monotone. These facts prevent licensing a bounded continuous representation from this milestone.

A further forensic issue remains before interpreting the radial jaggedness physically: the 21 stored K2 R2 nodes were produced in the previous dense environment, while the 20 H3 nodes were produced from the new 41-mode corrected-CLASS data object. Corrected CLASS itself agrees exactly across the two requests, but a direct same-environment R2 cardinality audit is required to verify that the single-mode R2 result is invariant to the number of inactive CLASS histories.

## Scope

Keep

- `THREE_D_DENSE_RADIAL_WEYL_NODES_LICENSED=False`
- `THREE_D_BOUNDED_CLASS_RESIDUAL_WEYL_TRANSFER_LICENSED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

The historical signed-transfer dense FAIL remains preserved.