# Stable AeST ACT DR6 R6a — fixed-baseline local-memory template projection pre-data declaration

Date: 2026-09-14

## Parent result

R6a is licensed only by the completed R5b result

`STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED`.

R5b post-data lock:

`3242335ece23fbeb743f075a1df1aa70acaab211`.

The exact local parent result files used by R6a are frozen by SHA-256:

- `results/stable_aest_observable_projection_r5b_derivative_zero.json`: `26ce723e2b7b783fcd19765c9c7f01b6101992a3f09e6ee321299bf148259ca9`
- `results/stable_aest_observable_projection_r5b_derivative_zero.npz`: `a88f99254bc1a7393e40691d5dc539bb1e1648eae1b892e43b63f593f8e367e1`

R6a does not reclassify R5, R5a, R5b, or any earlier result.

## Scientific question

Does the R5b-certified derivative-at-zero CMB-lensing memory template project reproducibly into the official ACT DR6 baseline lensing bandpower space, and what fixed-cosmology overlap does that template have with the ACT DR6 lensing data?

R6a is deliberately a fixed-baseline template-projection stage. It is not a cosmological parameter fit and it is not an observational detection or parameter-bound stage.

## Official ACT likelihood lock

Use the official repository/package only:

- repository: `ACTCollaboration/act_dr6_lenslike`
- release: `v1.2.1`
- release commit: `b386ddbb5821c1216c709f051c9289292f174d30`
- likelihood data version: `v1.2`
- variant: `act_baseline`
- `lens_only = True`
- `like_corrections = False`
- `apply_hartlap = True`
- `nsims_act = 796`, explicitly frozen to match the generic likelihood interface and its official unit test
- `trim_lmax = 2998`
- ACT only; no Planck lensing combination
- no primary-CMB likelihood

The runner must install the likelihood from the exact release commit into a dedicated R6a environment and obtain the official v1.2 data through the package data-download interface if they are not already present. It must record package/module version information and SHA-256 hashes of every ACT data file directly consumed by the R6a calculation.

No historical local ACT/v0.62/v0.65 result or script is a parent of R6a.

## Official-interface control

Before using the memory template, independently reproduce the official package's ACT-only baseline lens-only unit-test calculation using the package fiducial theory files.

Frozen control target:

`chi2_fiducial = 14.06`.

The interface-control gate passes if the reconstructed value is finite and satisfies

`abs(chi2_fiducial - 14.06) <= 0.10`.

This control must use the same `load_data`/`generic_lnlike` path and frozen likelihood settings as the science projection.

## Frozen R5b template

Use only the R5b NPZ arrays

- `ell`,
- `ckk_nominal_e0`,
- `T_ckk_eta0p01`.

The parent multipole grid must be contiguous and exactly `L = 40,...,2000`. The baseline spectrum must be finite and positive; the derivative tangent must be finite.

The local first-order model is

`C_L^kk(eta) = C_L,0^kk [1 + eta T_L]`,

where `T_L = T_ckk_eta0p01` is the R5b-certified derivative-at-zero fractional tangent.

The physical local eta domain is frozen to

`0 <= eta <= 0.05`,

with reported physical grid points

`eta = [0, 0.01, 0.025, 0.05]`.

No eta value larger than 0.05 is permitted in a physical R6a model evaluation.

A signed linear template coefficient may be calculated only as a diagnostic matched-filter quantity. A negative signed coefficient is not interpreted as a licensed physical negative eta value.

## ACT bandpower projection

Use the official `binmat_act`, `data_binned_clkk`, covariance, and Hartlap-corrected inverse covariance returned by the frozen likelihood configuration.

Let

`b0 = B C0`

be the baseline ACT bandpower vector, and

`t = B (C0 T)`

be the absolute derivative template in ACT bandpower space.

Before using these vectors, require that the retained ACT baseline binning matrix has negligible support outside the certified R5b multipole interval `[40,2000]`. Define the total absolute outside-support fraction across retained rows. It must be <= `1e-10`. No extrapolation of the R5b tangent is allowed.

## Broadband-amplitude deprojection

R6a must separately quantify the part of the memory template that is distinguishable from a pure broadband lensing-amplitude rescaling.

Set `a = b0` and define the covariance-metric correlation

`rho = (a^T Cinv t) / sqrt[(a^T Cinv a)(t^T Cinv t)]`.

Define the amplitude-deprojected memory template

`t_perp = t - a (a^T Cinv t)/(a^T Cinv a)`.

Record

- raw Fisher norm `F_raw = t^T Cinv t`,
- amplitude-deprojected Fisher norm `F_perp = t_perp^T Cinv t_perp`,
- `rho`,
- `sigma_eta_shape = 1/sqrt(F_perp)` when `F_perp > 0`.

This is a shape-information diagnostic, not a forecast claim, because the baseline cosmology is fixed.

## Data-template overlap

Let `r = data - b0`.

Record the fixed-baseline chi-square at eta=0 and at the frozen physical eta grid.

Also compute the signed amplitude-deprojected matched-filter coefficient

`eta_hat_signed = (t_perp^T Cinv r)/(t_perp^T Cinv t_perp)`

and its fixed-baseline standard deviation

`sigma_hat = 1/sqrt(t_perp^T Cinv t_perp)`.

Independently solve the two-column generalized least-squares problem

`data = b0 + deltaA * a + eta * t + residual`

and require the GLS eta coefficient to agree with `eta_hat_signed` to relative/absolute tolerance `1e-10` up to floating-point conditioning.

For the physical local interval `eta in [0,0.05]`, profile analytically over `deltaA` and record the minimum chi-square and its eta location. The location or improvement is descriptive and is not a PASS/FAIL criterion.

## Gates

### R6a-G1 parent/provenance

PASS iff:

- R5b post-data lock is an ancestor of HEAD;
- the local R5b JSON and NPZ SHA-256 values exactly match the frozen hashes above;
- the R5b JSON classification is exactly `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED`;
- all R5b gates are true.

### R6a-G2 official ACT likelihood provenance

PASS iff the installed likelihood identifies as version 1.2.1 from the pinned release-commit installation, the v1.2 data are available, `variant=act_baseline`, `lens_only=True`, `like_corrections=False`, `apply_hartlap=True`, `nsims_act=796`, and `trim_lmax=2998`, with a complete runtime SHA-256 manifest of consumed likelihood/data files.

### R6a-G3 official-interface control

PASS iff the official fiducial ACT baseline lens-only test is reproduced with

`abs(chi2_fiducial - 14.06) <= 0.10`.

### R6a-G4 template-domain/support validity

PASS iff the R5b parent arrays have the frozen grid/domain and finite values, the ACT retained binning rows require no R5b tangent extrapolation, and the total absolute outside-support fraction is <= `1e-10`.

### R6a-G5 bandpower-template algebra

PASS iff `b0`, `t`, covariance, inverse covariance, `t_perp`, and all frozen-grid model bandpowers are finite; covariance is symmetric; `F_raw > 0`; `F_perp > 0`; and the physical local model remains positive over the ACT-supported multipoles for eta in `[0,0.05]`.

### R6a-G6 independent matched-filter/GLS agreement

PASS iff the amplitude-deprojected matched-filter eta and the independently solved two-column GLS eta coefficient agree to `1e-10` in a scale-aware absolute/relative comparison.

No measured value of eta, delta chi-square, Fisher norm, correlation, or template signal-to-noise is used as a success threshold.

## Classification priority

1. `STABLE_AEST_ACT_DR6_R6A_INCOMPLETE`
2. `STABLE_AEST_ACT_DR6_R6A_PARENT_PROVENANCE_FAIL`
3. `STABLE_AEST_ACT_DR6_R6A_OFFICIAL_INTERFACE_FAIL`
4. `STABLE_AEST_ACT_DR6_R6A_TEMPLATE_SUPPORT_FAIL`
5. `STABLE_AEST_ACT_DR6_R6A_PROJECTION_ALGEBRA_FAIL`
6. `STABLE_AEST_ACT_DR6_R6A_MATCHED_FILTER_GLS_FAIL`
7. if G1-G6 pass: `STABLE_AEST_ACT_DR6_R6A_FIXED_TEMPLATE_PROJECTION_CERTIFIED`.

## Claim discipline

A PASS licenses only the statement that the R5b local CMB-lensing memory derivative has been reproducibly projected into the official ACT DR6 baseline lensing likelihood space and that its fixed-cosmology data overlap has been computed.

R6a does not license:

- a detection of gravitational memory,
- a cosmological constraint or confidence interval on eta,
- a likelihood preference for the AeST memory model,
- a Bayes factor,
- a tension claim,
- an ACT parameter bound,
- or a positive growth-Weyl separation claim.

Those require a later preregistered stage with cosmological/nuisance-parameter marginalization and an observationally adequate theory treatment.
