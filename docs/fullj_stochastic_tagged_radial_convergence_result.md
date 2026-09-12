# Stochastic tagged radial convergence — locked result

Classification:

`FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_FAIL`

This result preserves the preregistered gates in `docs/fullj_stochastic_tagged_radial_convergence_predata.md`. No threshold is changed post-data and no historical PASS/FAIL result is reinterpreted.

## Frozen setup

- Gaussian coefficient seed: `20260912`.
- Frozen coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`.
- Backgrounds: `B4={0,1,2,3}`, with `B2={0,1}` convergence control.
- `K0={0.03,0.05,0.08,0.10,0.15,0.20}` h/Mpc.
- `K1={0.03,0.04,0.05,0.065,0.08,0.09,0.10,0.125,0.15,0.175,0.20}` h/Mpc.
- Holdouts `H1={0.04,0.065,0.09,0.125,0.175}` h/Mpc.
- Symmetric tagged response at `epsilon=0.05`.
- Common periodic geometry for every radial target: `kF/h=0.005`, `NX=256`, `BOX=1866.3167638478922 Mpc`.
- `NSTEP=4096`.
- Reference nonlinear member: `sigma=0`, `kind=simple`, `beta0=1`.

## Numerical health

All 88/88 nonlinear R2 integrations completed and remained finite and constraint-clean. Canonical residuals stayed at order `1e-14` or better, metric constraints at order `1e-16`, and shear residuals were zero.

The broadband constitutive closure remained deeply saturated over the entire campaign:

`broadband_saturation_max = 4.711176043473348e-05`,

well below the frozen `2e-2` gate. The low-k subset remained equally clean:

- `k/h=0.03`: `4.517944029497273e-05`
- `k/h=0.04`: `4.517945855755603e-05`
- `k/h=0.05`: `4.711176043473348e-05`

The tagged response/power algebra closed to

`6.2227342453784706e-18` relative residual.

## Regression and background convergence

The common-geometry rerun reproduced the locked tagged-mode POC at overlapping targets essentially exactly:

- POC regression median: `2.9676833376032046e-15`
- POC regression max: `7.636652146293406e-15`

Background convergence was much stronger than required:

- response B2->B4 global relative L2: `5.703906201175753e-09`
- response per-k max: `2.9245679443099263e-08`
- power B2->B4 global relative L2: `2.3328648804301455e-09`
- power per-k max: `1.9054934079443584e-08`

The maximum ensemble response scatter normalized by RMS was `9.217795873943965e-07`.

Therefore stochastic-background sampling, box geometry, finite-tag construction, and broadband constitutive saturation are not the source of the radial failure.

## Frozen gate outcome

PASS:

- `STR_G1_provenance_and_frozen_identity`
- `STR_G2_all_88_tagged_runs_finite_constraint_clean`
- `STR_G3_broadband_saturated_closure`
- `STR_G4_tagged_response_power_algebra`
- `STR_G5_common_geometry_regression_to_POC`
- `STR_G6_background_convergence_B2_to_B4`
- `STR_G9_direct_radial_smoothness_spike_veto`
- `STR_G10_preserved_lowk_broadband_regime`

FAIL:

- `STR_G7_direct_K0_to_K1_holdout_accuracy`
- `STR_G8_K0_to_K1_continuous_radial_convergence`

## Radial failure

The direct K0->K1 holdout errors are strongly redshift dependent. They are small at high redshift and become large only after the tagged response develops late-time radial zero crossings and sign changes.

At `z>=1.5`, holdout power L2 is at most about `1.03e-2`; at `z=1.0` it rises to `2.7814e-2`. The large failures are localized to

- `z=0.5`: transfer L2 `0.1938719833`, power L2 `0.0988303163`, power peak `0.0938377481`;
- `z=0.2`: transfer L2 `0.4559224514`, power L2 `0.4306184314`, power peak `0.4547259119`.

The continuous K0->K1 comparison shows the same structure. Median errors over redshift remain modest,

- transfer median `0.0050480376`,
- power median `0.0136543580`,

but late-time maxima are

- transfer `0.2452343960`,
- power `0.1481798637`,
- power peak `0.1933583041`.

The fine-grid interpolated power remained finite and nonnegative.

## Physical/numerical interpretation

This FAIL is different from the earlier isolated-mode dense-radial failure. The tagged construction itself remains healthy: it is broadband-saturated, background-converged, common-geometry invariant, solver-clean, and POC-consistent. The failure is specifically that the six-node K0 radial grid is too coarse to represent the late-time oscillatory/sign-changing tagged response.

Examples from the direct K1 mean response illustrate the structure:

At `z=0.5`, the real response changes from `+0.06563` at `k/h=0.15` to `-0.05191` at `0.175` and `-0.05220` at `0.20`.

At `z=0.2`, the direct sequence contains multiple sharp changes and sign reversals, including approximately

- `T(0.09)=+0.14638`,
- `T(0.10)=+0.00617`,
- `T(0.125)=-0.04358`,
- `T(0.15)=+0.03082`,
- `T(0.175)=-0.23392`,
- `T(0.20)=-0.21989`.

Therefore no bounded radial continuum is licensed from K0/K1. However, this result does not invalidate the stochastic tagged-response construction; it requires a denser preregistered radial refinement.

## Scope flags

`STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED=False`

`STOCHASTIC_TAGGED_BOUNDED_RESPONSE_TESTED=False`

`THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`

`THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`

`EVOLVING_WEYL_POWER_LICENSED=False`

`ACT_LIKELIHOOD_LICENSED=False`

`OBSERVATIONAL_CLAIM_LICENSED=False`

## Next bounded milestone

Do not loosen K0->K1 thresholds and do not jump directly to ACT. The next bounded test is a K1->K2 tagged-response refinement using the same common geometry, the same frozen Gaussian backgrounds, and only the ten new midpoint nodes needed to form the 21-node nested grid

`K2={0.03,0.035,0.04,0.045,0.05,0.0575,0.065,0.0725,0.08,0.085,0.09,0.095,0.10,0.1125,0.125,0.1375,0.15,0.1625,0.175,0.1875,0.20}`.

The existing K1 direct responses must be reused unchanged. The refinement must test direct midpoint holdouts and K1->K2 continuous convergence with the same accuracy thresholds. Only a genuine K1->K2 PASS may license the bounded stochastic tagged radial continuum.