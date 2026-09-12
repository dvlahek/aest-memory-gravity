# Full-J evolving Weyl Gaussian 1D ensemble — locked result

## Classification

The preregistered 32-realization stochastic test completed with

`FULLJ_EVOLVING_WEYL_GAUSSIAN_1D_ENSEMBLE_PASS`.

Historical scope is preserved exactly: this is a stochastic Gaussian diagnostic on the one-dimensional periodic R2 embedding, not a three-dimensional isotropic cosmological Weyl power spectrum.

## Locked provenance

- R2 PASS result lock: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- deterministic covariance PASS/scope-correction result: `87434c21866241b1b35588ec88e93e99a6f5db1a`
- Gaussian 1D pre-data lock: `ad0b42694183d71b3ea1cab1eb1775c6456268c6`
- implementation commit: `604fa20db3761397bfeb0df74121779fc984d88f`
- runner / result-generating HEAD: `aecf313592b84eea310073dc7626b70fc22b8a13`
- RNG: `numpy.random.default_rng(20260912)`
- coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`
- reference theory branch: `sigma=0`, `kind=simple`, `beta0=1`

## Ensemble health

All 32 preregistered Gaussian realizations completed all nine redshift checkpoints.

- finite realizations: `32/32`
- mean `|g|^2`: `0.932547755456462`
- maximum canonical constraint residual: `1.4004303803631747e-14`
- maximum Hamiltonian residual: `1.7665191471755685e-16`
- maximum momentum residual: `1.7978245383236944e-16`
- maximum shear residual: `0`

The covariance algebra remained at floating-point precision:

- maximum Hermiticity relative residual: `2.084836842654342e-24`
- minimum eigenvalue / maximum absolute eigenvalue: `-3.4396997880209657e-16`
- maximum trace-reconstruction relative residual: `3.6885151268660805e-16`

## Prefix-convergence result

The frozen convergence prefixes were `N=8,16,32`.

Across the 27 `(redshift, band)` cells:

- median `d8_16 = 0.1382564577226931`
- maximum `d8_16 = 0.6079911676685963`
- median `d16_32 = 0.07153736527796394`
- maximum `d16_32 = 0.25695555072845827`

The preregistered G6 thresholds were:

- median `d16_32 <= 0.25`
- maximum `d16_32 <= 0.50`

Therefore G6 passes without changing thresholds or realizations.

The largest `d16_32` occurs in the high-mode band and is approximately `0.25695555`; it remains below the preregistered maximum threshold. The median convergence is substantially tighter than the gate.

## Nonlinear / direct-CLASS stochastic comparison

The nonlinear/reference bandpower ratio is close to unity at high redshift and departs progressively at late time. For the full `N=32` ensemble:

- at `z=6`: low = `1.0`, mid = `1.0`, high = `1.0`
- at `z=1`: low = `1.0003829241`, mid = `1.0033691462`, high = `1.0420457289`
- at `z=0.5`: low = `1.0036067037`, mid = `1.0376292867`, high = `0.7582556585`
- at `z=0.2`: low = `1.0160459536`, mid = `1.1859276335`, high = `0.7622115725`

These ratios establish a resolved late-time stochastic nonlinear response inside the retained one-dimensional embedding. They are not yet a three-dimensional cosmological power-spectrum prediction.

## Frozen gates

All preregistered gates passed:

- `G1_provenance_and_ensemble_identity = True`
- `G2_Gaussian_coefficient_normalization = True`
- `G3_finite_nonlinear_evolution_32of32 = True`
- `G4_metric_and_canonical_health = True`
- `G5_stochastic_covariance_algebra = True`
- `G6_prefix_bandpower_convergence = True`
- `G7_no_deterministic_theory_mixing = True`

## Interpretation lock

This PASS establishes that the locked R2 nonlinear evolving Weyl bridge supports a finite, internally consistent, prefix-convergent Gaussian stochastic Weyl variance diagnostic on the retained one-dimensional periodic embedding.

It does not justify identifying the 1D variance spectrum with an isotropic 3D cosmological `P_W(k,z)`. In the nonlinear equations, gradient/divergence mode coupling depends on multidimensional wavevector geometry, so a genuine 3D calculation or an independently derived shell-response reduction is still required before line-of-sight lensing.

Therefore the locked licensing state remains:

- `ONE_D_GAUSSIAN_WEYL_ENSEMBLE_TESTED=True`
- `THREE_D_ISOTROPIC_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

The next milestone must address the missing three-dimensional/isotropic mode-coupling geometry directly. No 1D-to-3D multiplicative lift is licensed from this result alone.
