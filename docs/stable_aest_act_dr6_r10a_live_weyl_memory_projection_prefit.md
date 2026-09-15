# Stable AeST ACT DR6 R10a — live Weyl-memory projection preregistration

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Purpose

R6a certified the official ACT DR6 lensing-only interface and a fixed-template projection, but its theory template was inherited from the earlier R5b derivative-at-zero construction. R8a2 subsequently certified the live AeST relaxation-time-dependent CMB-lensing response on `tau H0 = [10, 5, 2.5, 1.25]` using direct physical central derivatives. R10a combines these two already-certified objects.

R10a asks one narrow question: after projection through the official ACT DR6 lensing window and covariance, what overlap does the **live AeST Weyl-memory `C_L^{kk}` tangent** have with the ACT DR6 lensing bandpowers?

R10a is a postprocessing-only observational projection. It does not rerun CLASS, alter the AeST equations, change the certified R8a2 theory response, or reuse the historical R6a fixed theory template.

## Frozen parents

### ACT DR6 interface parent

- R6a post-data commit: `540f8f85c618209abb509e3c9c7dc188698d8e25`
- R6a classification: `STABLE_AEST_ACT_DR6_R6A_FIXED_TEMPLATE_PROJECTION_CERTIFIED`
- official ACT likelihood source commit: `b386ddbb5821c1216c709f051c9289292f174d30`
- ACT internal version: `1.2.0`
- ACT data version: `v1.2`
- variant: `act_baseline`
- `lens_only=True`
- `like_corrections=False`
- `apply_hartlap=True`
- `nsims_act=796`
- `trim_lmax=2998`
- official-interface control target: `chi2_fiducial = 14.06 +/- 0.10`

R6a is used only to define and validate the official ACT likelihood interface, data vector, covariance, inverse covariance, and binning operator. Its R5b fixed memory template is not an R10a theory parent.

### Live AeST theory parent

- R8a2 post-data commit: `590dbc69e2823f583b157af2297e357991103c47`
- R8a2 classification: `STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED`
- R8a2 JSON SHA256: `2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66`
- R8a2 NPZ SHA256: `c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1`
- tau grid: `(10.0, 5.0, 2.5, 1.25)`
- primary central derivative step: `epsilon = 0.025`
- control central derivative step: `epsilon = 0.05`

The stored R8a2 lensing tangent is fractional:

`T_L = [C_L(+epsilon) - C_L(-epsilon)] / [2 epsilon C_L(0)]`.

Therefore the absolute R10a tangent is frozen as

`dC_L/deta = C_L(0) * T_L`.

No smoothing, refitting, rescaling, sign change, clipping, or replacement of this tangent is permitted.

## Frozen multipole and ACT construction

For each tau, R10a reads from the certified R8a2 NPZ:

- `ell`,
- `baseline_tau{tag}_ckk`,
- `T_tau{tag}_ckk_eps025`,
- `T_tau{tag}_ckk_eps05`.

The certified parent range is `L = 40,...,2000`. The arrays are embedded into the full ACT input multipole vector with zeros outside this certified range. This is allowed only if the retained ACT binning matrix has total absolute support leakage outside `40 <= L <= 2000` no larger than `1e-10`, as already established by R6a and rechecked in R10a.

For each tau,

- `b0 = B @ C0_full`,
- `t25 = B @ (C0*T25)_full`,
- `t50 = B @ (C0*T50)_full`,

where `B` is the official ACT DR6 binning matrix.

## Frozen nuisance treatment

Exactly one nuisance direction is profiled: an overall broadband lensing-amplitude rescaling,

`a = b0`.

For the primary live tangent,

`t_perp = t25 - a (a^T C^-1 t25)/(a^T C^-1 a)`.

No additional nuisance directions, cosmological derivatives, data cuts, covariance modifications, rebinning choices, or post-data template rotations are allowed in R10a.

## Frozen physical interval and diagnostics

The local physical interval remains

`0 <= eta <= 0.05`.

The fixed eta grid used for reported chi-square values is

`eta = [0.0, 0.01, 0.025, 0.05]`.

The unconstrained signed coefficient `eta_hat_signed` is a matched-filter diagnostic only. Values outside `[0,0.05]` are not physical parameter estimates.

For each tau R10a reports:

- raw and amplitude-deprojected Fisher information,
- amplitude-memory correlation,
- primary-vs-control binned tangent metrics,
- `eta_hat_signed`, `sigma_eta`, and signed template S/N,
- matched-filter versus independent two-column GLS agreement,
- fixed and amplitude-profiled chi-square on the frozen eta grid,
- physical clipped eta and corresponding `Delta chi2`,
- primary live tangent norm and ACT-space tau-to-tau cosine/amplitude ratio.

## Preregistered gates

### R10A-G1 — parent provenance

PASS iff:

1. both frozen post-data commits are ancestors of HEAD;
2. the local R8a2 JSON and NPZ exist and exactly match the frozen SHA256 values;
3. the R8a2 JSON classification is `STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED`, `diagnostic_complete=true`, and all R8a2 gates are true;
4. the R6a implementation used by R10a retains the frozen official ACT constants above.

### R10A-G2 — official ACT interface control

PASS iff the exact official ACT source commit and internal version are loaded, the official v1.2 data manifest is present, and the independent official-interface control gives

`|chi2_fiducial - 14.06| <= 0.10`.

### R10A-G3 — support and live baseline

PASS iff:

1. the R8a2 `ell` grid is exactly `40,...,2000`;
2. all four live eta-zero `C_L^{kk}` baselines and both stored tangents are finite, and every baseline is strictly positive;
3. total absolute ACT binning support outside `40 <= L <= 2000` is `<= 1e-10`;
4. tau-dependent eta-zero baselines agree with the tau10 baseline to maximum relative error `<= 1e-8`.

### R10A-G4 — live central-derivative stability in ACT space

For each tau, compare the **binned absolute** primary and control tangents. With

`E = ||t25 - t50|| / max(||t25||, ||t50||)`

and cosine `C`, PASS iff for every tau

- `E <= 0.10`,
- `C >= 0.995`,
- `||t25|| > 1e-20`.

No gate may be relaxed after seeing ACT data.

### R10A-G5 — projection algebra and physical local model

PASS iff for every tau:

- data, covariance, inverse covariance, baseline and tangents are finite;
- covariance is symmetric;
- `a^T C^-1 a > 0`, `t25^T C^-1 t25 > 0`, and `F_perp > 0`;
- the covariance-metric residual amplitude overlap satisfies
  `|a^T C^-1 t_perp| / sqrt[(a^T C^-1 a) F_perp] <= 1e-10`;
- all frozen local spectra `C0*(1 + eta*T25)` for eta in `[0,0.01,0.025,0.05]` remain finite and strictly positive.

### R10A-G6 — matched-filter / GLS identity

For every tau, the amplitude-profiled matched-filter estimate and an independent two-column GLS solve using columns `[a,t25]` must agree to

`|eta_hat_MF - eta_hat_GLS| <= 1e-10 * max(1, |eta_hat_MF|, |eta_hat_GLS|)`.

### R10A-G7 — ACT-space tau coherence

Using the primary amplitude-deprojected tangents, compare each tau with tau10. PASS iff every tangent is finite and nonzero and every ACT-space cosine satisfies

`C(tau,tau10) >= 0.98`.

This gate checks that the relaxation-time sequence remains a coherent observable family after ACT windowing; it does not require monotonic amplitudes.

## Classification

PASS only if R10A-G1 through R10A-G7 all pass:

`STABLE_AEST_ACT_DR6_R10A_LIVE_WEYL_MEMORY_PROJECTION_CERTIFIED`

Otherwise classify at the first failed stage as one of:

- `STABLE_AEST_ACT_DR6_R10A_PARENT_PROVENANCE_FAIL`
- `STABLE_AEST_ACT_DR6_R10A_OFFICIAL_INTERFACE_FAIL`
- `STABLE_AEST_ACT_DR6_R10A_SUPPORT_BASELINE_FAIL`
- `STABLE_AEST_ACT_DR6_R10A_LIVE_CENTRAL_DERIVATIVE_FAIL`
- `STABLE_AEST_ACT_DR6_R10A_PROJECTION_ALGEBRA_FAIL`
- `STABLE_AEST_ACT_DR6_R10A_MATCHED_FILTER_GLS_FAIL`
- `STABLE_AEST_ACT_DR6_R10A_TAU_COHERENCE_FAIL`

## Claim discipline

A PASS licenses a reproducible **compressed ACT DR6 lensing-only projection of the certified live AeST linear response** over the tested tau grid. It licenses reporting ACT-space response shape, matched-filter overlap, physical local `Delta chi2`, and tau dependence of those quantities.

A PASS does not by itself license:

- detection of gravitational memory;
- a physical eta estimate from an unconstrained signed coefficient outside `[0,0.05]`;
- a tau bound;
- full cosmological or nuisance-parameter inference;
- a full ACT primary-CMB likelihood result;
- nonlinear-lensing or Halofit claims;
- extrapolation beyond the certified local eta interval or below `tau H0=1.25`.

Historical R6a remains a certified fixed-template result and is not reclassified. Historical DESI results remain unchanged.