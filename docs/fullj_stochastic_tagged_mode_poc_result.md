# Stochastic broadband tagged-mode POC — locked result

Classification:

`FULLJ_STOCHASTIC_TAGGED_MODE_POC_PASS`

This result preserves the preregistered scope in `docs/fullj_stochastic_tagged_mode_poc_predata.md` and does not modify the historical dense-radial FAIL results.

## Frozen setup

- Gaussian coefficient seed: `20260912`.
- Frozen coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`.
- Gaussian background IDs: `0,1,2`.
- Tagged radial targets: `k/h = 0.0375, 0.10, 0.175 Mpc^-1`.
- Symmetric tag amplitudes: `epsilon = 0.10, 0.05` with both signs.
- Total tagged R2 integrations: 36.
- Reference nonlinear member: `sigma=0`, `kind=simple`, `beta0=1`.
- The low-k target used the preregistered enlarged periodic box and matched physical grid spacing (`NX=512` for `k/h=0.0375`).

## Main numerical result

All 36/36 tagged nonlinear R2 runs completed and remained finite and constraint-clean. Canonical constraints remained of order `1e-14` or better and metric constraint residuals remained of order `1e-16`, with zero shear correction.

The preregistered broadband saturation diagnostic gave

`broadband_saturation_max = 4.731066674148239e-05`,

well below the frozen `2e-2` gate. In particular, the previously problematic isolated-mode target `k/h=0.0375` is deeply saturated on all three broadband Gaussian backgrounds, with maxima between approximately `4.12e-05` and `4.42e-05`.

The symmetric tagged response is extremely stable under halving the tag amplitude:

- `epsilon_consistency_median = 5.214054686491488e-15`
- `epsilon_consistency_max = 1.2944515507279873e-08`

The primary tagged-response background scatter is also very small:

- `primary_max_scatter_over_rms = 8.793934553894611e-07`
- `primary_median_power_cv = 7.454709267977411e-15`

Tagged power reconstruction is algebraically clean:

`tagged_power_identity_relative_residual = 7.646310444953125e-21`.

Primary mean tagged power by target:

- `k/h=0.0375`: `0.1675057143529476`
- `k/h=0.10`: `0.01833275896482308`
- `k/h=0.175`: `0.010278810851069827`

## Frozen gates

All preregistered gates passed:

- `ST_G1_provenance_and_frozen_identity = true`
- `ST_G2_Gaussian_background_identity = true`
- `ST_G3_all_tagged_runs_finite_constraint_clean = true`
- `ST_G4_symmetric_response_epsilon_consistency = true`
- `ST_G5_broadband_saturated_closure = true`
- `ST_G6_tagged_response_power_sanity = true`

## Interpretation

The isolated single-mode low-k desaturation seen in the dense-radial campaign is not reproduced when the same tagged radial mode is probed on a broadband Gaussian background. The nonlinear constitutive state is therefore controlled by the broadband field configuration, and the isolated finite-amplitude single-mode transfer is not an adequate continuum object for this nonlinear system.

Within the tested three radial targets and three frozen Gaussian backgrounds, a symmetric stochastic-background tagged response is numerically well defined, epsilon-stable, constraint-clean, and compatible with the saturated constitutive closure. This validates the stochastic tagged-response construction in principle and motivates a bounded radial tagged-response convergence campaign.

This PASS does **not** license a continuous Weyl power spectrum, line-of-sight lensing prediction, ACT likelihood, or observational claim.

## Scope flags

`STOCHASTIC_BROADBAND_TAGGED_RESPONSE_POC_TESTED=True`

`STOCHASTIC_BROADBAND_LOWK_SATURATION_TESTED=True`

`STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED=False`

`THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`

`THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`

`EVOLVING_WEYL_POWER_LICENSED=False`

`ACT_LIKELIHOOD_LICENSED=False`

`OBSERVATIONAL_CLAIM_LICENSED=False`

## Next bounded milestone

The next test should extend the tagged response to a preregistered radial node set over the bounded interval `0.03 <= k/h <= 0.20 Mpc^-1`, use common-random Gaussian backgrounds, retain symmetric tagging, and test radial convergence and background convergence directly on the tagged response and tagged power. No ACT/lensing calculation is licensed before that bounded stochastic tagged-response continuum passes.
