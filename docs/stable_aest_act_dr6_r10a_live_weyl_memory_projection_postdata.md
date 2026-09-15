# Stable AeST ACT DR6 R10a — live Weyl-memory projection post-data

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Formal classification

`STABLE_AEST_ACT_DR6_R10A_LIVE_WEYL_MEMORY_PROJECTION_CERTIFIED`

All preregistered gates R10A-G1 through R10A-G7 passed. The run exited with code 0.

## Frozen provenance

- R10a preregistration lock: `4c46fd21df048553b577a1927d8404bc493f649e`
- R10a final implementation: `af2b85cf2a4d564c7575aa9bdcdd9039ff48ba0f`
- R10a runner / run head: `dd295e0800e45a27d5acd01872915ca4e71bbb40`
- R6a post-data parent: `540f8f85c618209abb509e3c9c7dc188698d8e25`
- R8a2 post-data parent: `590dbc69e2823f583b157af2297e357991103c47`
- R8a2 JSON SHA256: `2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66`
- R8a2 NPZ SHA256: `c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1`
- official ACT likelihood source commit: `b386ddbb5821c1216c709f051c9289292f174d30`
- ACT data version: `v1.2`
- ACT internal version: `1.2.0`
- ACT variant: `act_baseline`
- `lens_only=True`
- `like_corrections=False`
- Hartlap correction enabled
- `nsims_act=796`
- `trim_lmax=2998`

The official ACT interface control returned

`chi2_fiducial = 14.057911788739439`

against the frozen target `14.06 +/- 0.10`.

## Artifact hashes

- full runner SHA256: `10a46b4f593220cee1198e7e4a577dd2c3ba027997ab7e2e0245bf0e2e4bb5b4`
- environment SHA256: `2b362b30502bcc367a30b03ec9d26d89d99bf10ff77cebe3819b1e87414fb722`
- JSON SHA256: `e794162e7090435e4344f29fb926460e012d3f37fa1c87729e711d172c73598f`
- science log SHA256: `72ed65ec7f87f45e481c16c72f8f0a5cf22fd2a78dd0ccbb48d9549673aee789`
- NPZ SHA256: `f37ebc39342a57c6f217a9593b3372aa162102ca337d119cc8a7bc785906c49b`

## What R10a tests

R10a is a postprocessing-only live-theory projection. It does not rerun CLASS and does not use the historical R5b fixed lensing template. It consumes the certified R8a2 live AeST lensing response for

`tau H0 = [10, 5, 2.5, 1.25]`

and projects the absolute tangent

`d C_L^{kappa kappa}/d eta = C_L^{kappa kappa}(eta=0) * T_L`

through the official ACT DR6 lensing binning matrix and covariance.

Only one preregistered nuisance direction is projected out: a broadband lensing-amplitude rescaling.

## Gate result

All seven gates passed:

- G1 parent provenance
- G2 official ACT interface control
- G3 support and live baseline consistency
- G4 live central derivative stability in ACT bandpower space
- G5 projection algebra and positive local physical model
- G6 matched-filter / GLS identity
- G7 ACT-space tau coherence

## Numerical stability

The primary epsilon is `0.025`, with `0.05` as control.

In ACT bandpower space, the primary/control tangent agreement is excellent:

| tau H0 | E(0.025,0.05) | cosine |
|---:|---:|---:|
| 10 | 9.2125e-05 | 0.9999999968 |
| 5 | 2.0750e-03 | 0.9999980830 |
| 2.5 | 2.7825e-03 | 0.9999962448 |
| 1.25 | 3.4234e-03 | 0.9999955838 |

All values are far inside the frozen `E <= 0.10`, `C >= 0.995` gate.

## ACT-space tau coherence

Relative to `tau H0=10`, the live ACT-space tangent remains highly coherent:

| tau H0 | norm ratio | cosine to tau10 |
|---:|---:|---:|
| 10 | 1.000000 | 1.0000000000 |
| 5 | 0.991668 | 0.9999934817 |
| 2.5 | 0.975770 | 0.9999437399 |
| 1.25 | 0.951043 | 0.9996904571 |

Thus shortening the relaxation time over the certified range changes the ACT-weighted shape only weakly and modestly reduces its norm.

## Projection result

| tau H0 | F_perp/F_raw | eta_hat_signed | sigma_eta | signed S/N | physical Delta chi2 at eta=0.05 |
|---:|---:|---:|---:|---:|---:|
| 10 | 0.597942 | 878594.49 | 272318.61 | 3.22635 | 1.18477e-06 |
| 5 | 0.595441 | 898761.57 | 275641.03 | 3.26062 | 1.18292e-06 |
| 2.5 | 0.591441 | 938462.86 | 282046.87 | 3.32733 | 1.17971e-06 |
| 1.25 | 0.585432 | 1019175.07 | 294542.58 | 3.46020 | 1.17477e-06 |

The broadband-amplitude projection leaves about 58.5%--59.8% of the raw covariance-metric memory-template norm. Therefore the live memory fingerprint is not equivalent to a pure overall lensing-amplitude rescaling.

Matched-filter and two-column GLS eta estimates agree to floating-point precision.

## Scientific interpretation

R10a is a certified live-AeST ACT DR6 lensing null-sensitivity result in the physical local interval `0 <= eta <= 0.05`.

The ACT residuals have a formal signed alignment of about `3.23`--`3.46 sigma` with the mathematical live-memory template direction. However, the corresponding unconstrained signed coefficient is `eta_hat ~ 0.9e6--1.0e6`, approximately 1.8e7--2.0e7 times larger than the maximum physically licensed local value `eta=0.05`.

Inside the physical interval, the improvement is only

`Delta chi2 ~ 1.18e-06`.

Therefore the signed overlap is not a physical detection of AeST memory. It is an extrapolated template-overlap diagnostic.

## Comparison to R6a

At `tau H0=10`, the live R10a result closely reproduces the earlier fixed-template R6a result:

- `sigma_eta`: about 272617 (R6a) -> 272319 (R10a)
- `eta_hat_signed`: about 885002 -> 878594
- `F_perp/F_raw`: about 0.5967 -> 0.5979
- physical `Delta chi2`: remains about 1.2e-06

This validates the earlier R6a qualitative conclusion while replacing its fixed-template approximation with the certified live Weyl-memory response.

## Licensed claims

Licensed:

- live AeST `C_L^{kappa kappa}` response is reproducibly projected into official ACT DR6 lensing space;
- the ACT-space live tangent is stable under the frozen epsilon control;
- the lensing fingerprint retains a nontrivial shape component after broadband-amplitude deprojection;
- shortening tau from 10 to 1.25 does not materially improve physical detectability in ACT DR6;
- ACT DR6 gives a validated null-sensitivity result in the certified physical eta interval.

Not licensed:

- detection of gravitational memory;
- a physical estimate of eta from the unconstrained signed coefficient;
- a tau bound;
- full cosmological parameter inference;
- nonlinear-lensing claims;
- full ACT primary-CMB likelihood claims;
- extrapolation of the local linear response to eta of order 1e6.

## Strategic consequence

The limiting factor is observable amplitude, not template distinctness or numerical instability. The natural next question is detectability: determine how much lensing precision would be required for a physical `eta=0.05` signal and compare that requirement with next-generation lensing observables. A separate kSZ/velocity-sensitive route is also scientifically motivated because kSZ probes electron momentum and therefore peculiar velocities more directly than CMB lensing.