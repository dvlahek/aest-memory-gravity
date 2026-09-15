# Stable AeST DESI DR1 R9b2i native variance-response ShapeFit preregistration

## Purpose

R9b2h completed as

`STABLE_AEST_DESI_DR1_R9B2H_CROSS_METHOD_DERIVATIVE_FAIL`.

The completed result showed that bounded value-level spectra are stable, three log-linear resolutions are converged, and both LL and PCHIP separately satisfy the original epsilon-consistency gate. Their tiny eta tangents nevertheless disagree because the response is O(1e-6), smaller than the method-dependent O(1e-5--1e-4) value-level interpolation offset. The requested P_k_max controls also did not extend the actual returned transfer support.

R9b2i changes the numerical object, not any physical parameter or threshold. It differentiates the linear variance functional on the native CLASS k nodes before square roots and ratios are formed. No P(k) interpolation and no extrapolation are used in the response calculation.

R9b2i is a single conditional pipeline:

1. theory-only native variance-response validation;
2. only if Stage A passes, load the frozen official DESI DR1 ShapeFit product and immediately perform the corrected compressed-data projection.

If Stage A fails, DESI data must not be loaded and the run terminates with a theory-only classification.

Historical R9b/R9b2/R9b2a/R9b2b/R9b2c/R9b2d/R9b2e/R9b2f/R9b2g/R9b2h classifications remain unchanged.

## Frozen provenance

Required repository ancestors:

- R9b2h post-result record: `ffd0a10892c65bf71f134c6d9e78dc9dc13f1a16`
- R9b2h preregistration: `e02eb97bf5675fb33a21f7545e0d7259ef5b97ce`
- R9b2h implementation: `ae5a3bbd3a535d01ceef06c4dd38776de2c6c6c6`
- R9b2g post-result record: `68ca78bcea41a18af46ec4ccf6e30ddf78f64471`
- R9b2f post-result record: `b569aebc41efc841755f5fcec63b91092c192ba3`
- corrected CLASS parent: `e85808324f51fc694d12e3ed7439552a3c3f9540`.

Frozen completed R9b2h artifact hashes:

- JSON: `7cdf0f17572c351acb118e858a8fc5c206484fa6af2cf8e66531b8cd5927eea2`
- science log: `3aa11987326590ed317b6751ae86536281896dfceb0eb8a5326425cb0047aaf0`
- full runner: `bb5834f73177c3494312d43354e02b886a276aec04f084bb3ee68bcf54562da1`.

Official DESI likelihood repository remains pinned to

`7d51f4f86dc3bee6bf10f1a684913c943a89a844`.

The DESI observable, six tracers, nuisance basis, eta physical interval, covariance treatment and projection algebra remain those of historical R9b.

## Frozen model grid

Use

- `tau_H0 = {10, 5, 2.5, 1.25}`
- `eta = {0, +0.025, -0.025, +0.05, -0.05}`
- `tol_perturbations_integration = 3e-8`
- `aest_memory_order = 20`
- `AEST_R7A_EPOCH_MODE=full`
- `output = mPk,mTk,vTk`
- `P_k_max_h/Mpc = 5`
- `z_max_pk >= 2.3`
- no nonlinear correction
- no lensing
- no `k_output_values`
- no explicit `k_per_decade_for_pk` or `k_per_decade_for_bao` overrides.

Frozen theory coordinates are the six DESI effective redshifts:

`{0.29536404346937617, 0.5096288678782911, 0.7057956472488681, 0.9185851971138159, 1.3170658832980264, 1.4905017757527006}`.

## Native source-state construction

At each model and redshift, use the same source-state transfer construction certified through R9b2f:

- `d_cb = f_b d_b + f_c d_cdm`
- `theta_cb = f_b t_b + f_c t_cdm`
- `v_cb = -theta_cb/Hconf`
- `C(k) = (2 pi^2/k^3) A_s (k/0.05)^(n_s-1)`
- `P_dd = C d_cb^2`
- `P_tt = C v_cb^2`, converted to `(Mpc/h)^3`.

Only actual returned common CLASS transfer nodes in `1e-4 <= k_h <= 5` are used.

For every tau, epsilon and z, the eta=0, +epsilon and -epsilon runs must have identical k-node arrays to relative tolerance `1e-12`. No node deletion, smoothing, clipping, interpolation, extrapolation or outlier rejection is allowed after the standard finite/common-node mask.

## Stage A — native variance response

Define the linear top-hat variance functional on the native nodes

`V[P] = (1/(2 pi^2)) integral dlnk k^3 P(k) W_TH(8 k)^2`.

Primary quadrature is SciPy Simpson directly on the original `ln k` nodes. Independent control is trapezoidal integration on the same original nodes.

For epsilon in `{0.025,0.05}` form the signed central difference spectra before integration:

`D_dd = [P_dd(+epsilon)-P_dd(-epsilon)]/(2 epsilon)`

`D_tt = [P_tt(+epsilon)-P_tt(-epsilon)]/(2 epsilon)`.

For each quadrature `Q`, compute at eta=0

- `Vdd0_Q = V_Q[P_dd(0)]`
- `Vtt0_Q = V_Q[P_tt(0)]`
- `sigma_dd0_Q = sqrt(Vdd0_Q)`
- `sigma_tt0_Q = sqrt(Vtt0_Q)`
- `f0_Q = sigma_tt0_Q/sigma_dd0_Q`.

Then

`dVdd/deta = V_Q[D_dd]`

`dVtt/deta = V_Q[D_tt]`

`d sigma_dd/deta = (dVdd/deta)/(2 sigma_dd0_Q)`

`d sigma_tt/deta = (dVtt/deta)/(2 sigma_tt0_Q)`

and

`df/deta = (d sigma_tt/deta)/sigma_dd0_Q - sigma_tt0_Q (d sigma_dd/deta)/sigma_dd0_Q^2`.

This is the frozen direct response estimator. Finite differences of already integrated sigma or f are diagnostic only and cannot determine PASS.

### Stage-A gates

Use unchanged derivative-shape thresholds

- `E <= 0.05`
- `C >= 0.995`.

Use inherited value closure threshold `REL_GATE = 5e-3`.

A1 provenance and frozen construction.

A2 all 20 CLASS models finite, all required powers positive at eta=0, and exact common-node identity for each central pair.

A3 eta=0 Simpson baseline closes to CLASS internal `sigma(8,z)` and historical `effective_f_sigma8/sigma8` at every tau,z within `5e-3`.

A4 eta=0 Simpson baseline is tau invariant within `5e-3` for sigma_dd, sigma_tt and f.

A5 within-Simpson epsilon response consistency: for each tau the six-component `df/deta` vectors from epsilon .025 and .05 satisfy E<=.05 and C>=.995, with primary norm >1e-12.

A6 within-trapezoid epsilon response consistency satisfies the same frozen gate.

A7 Simpson-vs-trapezoid direct response agreement: compare primary (.025) tangent vectors and separately control (.05) tangent vectors for every tau with E<=.05 and C>=.995.

Only A1--A7 all PASS licenses Stage B. If any fail, set `desi_data_loaded=false`, stop before calling the DESI loader, and classify the earliest failed gate.

## Stage B — corrected official DESI DR1 ShapeFit projection

Stage B uses the official six-bin Full-Shape+BAO ShapeFit compressed product exactly as historical R9b. The data vector, covariance, parameter ordering and file hashes are read by the existing R9b official loader only after Stage A passes.

For each tau, eta and z, geometry (`qiso/qap`) and ShapeFit broadband quantities (`m`, `A_p`) use the frozen historical R9b construction. The only replaced numerical quantity is the growth factor entering `df`.

At eta=0 define

`S0 = f0 * sqrt(Ap0)`

and the baseline ShapeFit `df` observable as

`df0 = S0 / S_fid`,

where `S_fid = f_fid sqrt(Ap_fid)` is the same DESI fiducial normalization used by R9b.

For each epsilon:

- qiso/qap derivative: ordinary central difference of the historical geometry scalar;
- dm derivative: ordinary central difference of the historical ShapeFit `m` scalar;
- `dAp/deta`: ordinary central difference of `Ap`;
- source-growth derivative `df_source/deta`: the direct native variance response from Stage A;
- product derivative:
  `dS/deta = sqrt(Ap0) df_source/deta + f0/(2 sqrt(Ap0)) dAp/deta`;
- ShapeFit df tangent component:
  `(dS/deta)/S_fid`.

Thus no finite difference of two separately integrated source-growth values enters the corrected `df` tangent.

The 24-component corrected tangent is assembled in the exact DESI parameter ordering.

### Stage-B gates

B1 official DESI data/repository provenance and positive-definite covariance, inherited from R9b.

B2 all corrected eta=0 24-vector baseline entries and all primary/control tangent entries finite.

B3 full 24-vector primary/control consistency for every tau: E<=.05 and C>=.995.

B4 Simpson-primary versus trapezoid-control construction agreement for the corrected full tangent: E<=.05 and C>=.995 for both epsilon levels at every tau.

B5 nuisance projection algebra: deprojected Fisher finite and positive and projection idempotence metric <=1e-8, using the unchanged historical R9b nuisance basis (`global_df_scale`, `global_dm_offset`).

B6 matched-filter/GLS identity: same historical numerical identity threshold

`|eta_MF-eta_GLS| <= max(1e-10, 1e-8 max(|eta_MF|,|eta_GLS|,1))`.

The physical eta interval remains `[0,0.05]`. No DESI likelihood threshold is changed.

## Frozen classifications

Stage-A failures, in order:

- `STABLE_AEST_DESI_DR1_R9B2I_PROVENANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_NATIVE_GRID_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_ETA0_CLOSURE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_ETA0_TAU_INVARIANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_SIMPSON_RESPONSE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_TRAPEZOID_RESPONSE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_CROSS_QUADRATURE_RESPONSE_FAIL`.

Stage-B failures, in order:

- `STABLE_AEST_DESI_DR1_R9B2I_DESI_PROVENANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_CORRECTED_VECTOR_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_FULL_TANGENT_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_FULL_CROSS_QUADRATURE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_NUISANCE_PROJECTION_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2I_MATCHED_FILTER_GLS_FAIL`.

Technical execution errors use

`STABLE_AEST_DESI_DR1_R9B2I_RUN_FAIL`.

All gates PASS gives

`STABLE_AEST_DESI_DR1_R9B2I_NATIVE_VARIANCE_RESPONSE_SHAPEFIT_CERTIFIED`.

## Interpretation policy

A PASS certifies a numerically stable corrected projection of the preregistered AeST memory tangent into the official DESI DR1 ShapeFit compressed product. It does not reclassify any historical failure, does not by itself license a detection claim, does not constitute a full EFT modified-gravity likelihood, and does not license a tau-bound claim.
