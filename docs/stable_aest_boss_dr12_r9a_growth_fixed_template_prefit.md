# Stable AeST cosmic memory R9a — BOSS DR12 real-data growth fixed-template test (pre-fit lock)

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Status and claim discipline

This document is locked before computing any memory-template fit, best-fit eta, Delta chi2, Fisher significance, or data preference for R9a.

The public BOSS DR12 data vector and covariance source were inspected only to verify that a complete reproducible compressed growth likelihood is publicly available and to freeze its provenance. Therefore this is a **pre-fit observational lock**, not a blind pre-data declaration.

No memory fit to the BOSS data has been calculated before this lock.

R9a is a compressed-observable real-data test. It is not a full-shape galaxy-clustering analysis and cannot by itself establish a modified-gravity detection.

## Frozen parents

The theory parent chain is:

- R7a: `STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED`, post-data lock `86c03e6ba2ee9fcbf33a9d319d12ae778a747881`;
- R8a2: `STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED`, post-data lock `590dbc69e2823f583b157af2297e357991103c47`;
- R8b: `STABLE_AEST_COSMIC_MEMORY_R8B_TWO_TAU_LOOKBACK_CERTIFIED`, post-data lock `9e21c61210979ab841918ba16f2210020daa245a`.

Historical classifications remain unchanged.

## Real observational dataset

Use the BOSS DR12 consensus compressed measurements as distributed in the public `CobayaSampler/bao_data` repository, pinned to commit

`bb0c1c9009dc76d1391300e169e8df38fd1096db`.

Frozen files:

1. `sdss_DR12Consensus_final.dat`
   - SHA256: `eae45d2629dc1214b351716b3ff9a6f5a22f170b71e3d0e93aeeddc169d80e30`
2. `final_consensus_covtot_dM_Hz_fsig.txt`
   - SHA256: `dea6d8d4893d2b84772f9b83d0653bf7d4ee81a0aeb63ce04859e20d0ad3a289`

The full data order at each redshift is `(D_M/r_s, H r_s, f sigma8)` for `z = 0.38, 0.51, 0.61`.

R9a uses only the marginal `f sigma8` subvector and its corresponding 3x3 covariance submatrix, selecting full-vector indices `[2,5,8]`. This avoids using BAO distances to constrain the fixed background cosmology in a test intended specifically for the growth-memory response.

Frozen BOSS growth data values are therefore

`d = [0.49749, 0.457523, 0.436148]`

at

`z_BOSS = [0.38, 0.51, 0.61]`.

The 3x3 covariance must be extracted directly from the pinned 9x9 file. No diagonal approximation is permitted.

## Frozen theory construction

Use the same direct physical stable-AeST source construction certified by R8a2/R8b:

- CLASS parent `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- stable `chi = Q s` residual dynamics;
- memory order 20;
- no nonlinear/Halofit;
- no R2d trace/replay hook;
- exactly one physical memory closure;
- signed eta permitted only for symmetric derivative diagnostics in the disposable source.

Frozen relaxation-time grid:

`tau H0 = [10.0, 5.0, 2.5, 1.25]`.

For each tau evaluate the exact BOSS redshifts, not an interpolation from the R8a2 redshift grid.

At nominal perturbation tolerance `3e-8`, compute

- eta = 0,
- eta = +0.025,
- eta = -0.025,
- eta = +0.05,
- eta = -0.05.

For each tau define the primary exact-redshift tangent

`T_tau = [f_sigma8(+0.025)-f_sigma8(-0.025)] / [0.05 f_sigma8(0)]`

and the control tangent analogously at epsilon 0.05.

## Fixed-template observational model

For each tau define

`b = f_sigma8(eta=0)`

and the dimensional memory template

`t = b * T_tau`.

The direct local model is

`m(eta) = b + eta t`.

The physically certified local eta interval is frozen to

`0 <= eta <= 0.05`.

A signed unconstrained eta coefficient may be reported only as a diagnostic linear-template projection.

## Broadband growth-amplitude nuisance

To prevent an overall sigma8/growth normalization mismatch from being misidentified as memory, include a free linear broadband amplitude direction

`a = b`.

With BOSS covariance C, define the covariance-weighted memory shape after amplitude projection:

`t_perp = t - a (a^T C^-1 t)/(a^T C^-1 a)`.

Define

`F_raw = t^T C^-1 t`,

`F_perp = t_perp^T C^-1 t_perp`,

`rho = (a^T C^-1 t)/sqrt[(a^T C^-1 a)(t^T C^-1 t)]`.

The signed amplitude-deprojected matched-filter coefficient is

`eta_hat_signed = (t_perp^T C^-1 r)/(t_perp^T C^-1 t_perp)`,

where `r = d - b` after the equivalent two-column GLS treatment of baseline amplitude and memory template.

The implementation must also solve the independent two-column GLS problem with design matrix `[a,t]`; the eta coefficient from GLS and the deprojected matched filter must agree numerically.

Profile the physical eta only over `[0,0.05]`, jointly with the unrestricted linear broadband amplitude nuisance.

## Reported quantities — never gates

For every tau report, without using them as PASS criteria:

- baseline chi2 with amplitude fixed to one;
- best-fit broadband amplitude at eta=0 and its profiled chi2;
- `F_raw`, `F_perp`, `rho`;
- signed `eta_hat` and `sigma_eta = 1/sqrt(F_perp)`;
- signed template S/N `eta_hat/sigma_eta`;
- physical best-fit eta in `[0,0.05]`;
- physical Delta chi2 relative to eta=0 after profiling broadband amplitude;
- comparison of eta_hat and Fisher sensitivity across the four tau values.

No threshold on eta_hat, Delta chi2, S/N, or preference for any tau is allowed to gate certification.

## Preregistered gates

### R9A-G1 parent and provenance lock

PASS if this pre-fit lock and all three parent post-data locks are ancestors of HEAD, parent classifications match exactly, and the pinned BOSS repository commit and both frozen file SHA256 values match.

### R9A-G2 direct physical source topology

PASS if the disposable CLASS source contains the certified stable-chi construction, exactly one physical memory closure and multiplier, zero external tangent replay hooks and zero R2d trace hooks.

### R9A-G3 exact-redshift theory runs

PASS if all 20 frozen theory runs complete, are finite/domain-positive, and return `f sigma8` at exactly `z = [0.38,0.51,0.61]`.

### R9A-G4 central derivative consistency

For every tau, primary epsilon=0.025 and control epsilon=0.05 tangents must satisfy

- relative L2 `E <= 0.10`,
- cosine `C >= 0.995`.

### R9A-G5 BOSS likelihood algebra

PASS if the extracted 3x3 covariance is finite, symmetric and positive definite; `F_raw > 0`; `F_perp > 0`; and all baseline/profile likelihood quantities are finite.

### R9A-G6 matched-filter / GLS identity

PASS if, for every tau, the signed eta coefficient from covariance-projected matched filtering and from independent two-column GLS agree to relative tolerance `1e-10` (with an absolute floor `1e-12`).

## Formal classifications

Priority order:

1. `STABLE_AEST_BOSS_DR12_R9A_INCOMPLETE`
2. `STABLE_AEST_BOSS_DR12_R9A_PARENT_PROVENANCE_FAIL`
3. `STABLE_AEST_BOSS_DR12_R9A_SOURCE_TOPOLOGY_FAIL`
4. `STABLE_AEST_BOSS_DR12_R9A_THEORY_RUN_FAIL`
5. `STABLE_AEST_BOSS_DR12_R9A_CENTRAL_DERIVATIVE_FAIL`
6. `STABLE_AEST_BOSS_DR12_R9A_LIKELIHOOD_ALGEBRA_FAIL`
7. `STABLE_AEST_BOSS_DR12_R9A_MATCHED_FILTER_GLS_FAIL`
8. if G1-G6 pass: `STABLE_AEST_BOSS_DR12_R9A_GROWTH_TEMPLATE_PROJECTION_CERTIFIED`.

## Licensed interpretation of PASS

A PASS licenses reporting the BOSS DR12 compressed-growth projection of the certified local memory template across the frozen tau grid, including signed diagnostic eta projections and the physical `[0,0.05]` profile.

A PASS does **not** by itself license an observational detection, a model-independent modified-gravity constraint, a full cosmological parameter bound, or a claim that BOSS prefers gravitational memory. The compressed `f sigma8` measurements were derived within a standard RSD compression framework; any interesting preference must be followed by a full-shape clustering likelihood analysis.
