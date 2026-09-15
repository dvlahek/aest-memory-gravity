# Stable AeST DESI DR1 R9b2j signed-response dense quadrature and source-state ShapeFit preregistration

## Status and chronology

This record is frozen before the R9b2j implementation and before any R9b2j result is inspected.

R9b2i remains permanently classified as

`STABLE_AEST_DESI_DR1_R9B2I_CROSS_QUADRATURE_RESPONSE_FAIL`.

Its completed local artifact is identified by SHA-256

`859d92d849c295d3a5219980a9caa82c283952f814e98df19a1b44ca5fe97164`.

R9b2i established that the central signed response itself is stable with respect to epsilon inside each native-node quadrature, while Simpson and trapezoid applied directly to the sparse 108-node automatic CLASS grid differ materially in response amplitude. The failing cross-quadrature gate is therefore treated as an under-resolved quadrature diagnostic, not as physical evidence and not as permission to relax E or C.

No historical classification is changed.

## Purpose

R9b2j tests the same physical eta response with the subtraction performed before interpolation or integration:

`D_P(k) = [P(+epsilon,k)-P(-epsilon,k)]/(2 epsilon)`.

The signed response spectrum is then interpolated as a signed quantity in `ln k` onto a dense bounded grid and integrated. This removes the common-mode absolute-spectrum bias diagnosed in R9b2h while also removing the sparse-native-grid Simpson/trapezoid ambiguity diagnosed in R9b2i.

R9b2j also removes the remaining `pk_cb_lin(z)` dependency from the ShapeFit `Ap` and `m` construction. ShapeFit amplitude and slope are constructed from the same bounded source-state `P_dd(k,z)` used for the growth response.

DESI data are not loaded until all theory-only Stage A gates pass.

## Frozen model settings

- six DESI DR1 ShapeFit effective redshifts, used as theory coordinates in Stage A
- `tau_H0 = {10, 5, 2.5, 1.25}`
- `eta = {0, +/-0.025, +/-0.05}`
- primary epsilon `0.025`
- control epsilon `0.05`
- `tol_perturbations_integration = 3e-8`
- memory order inherited from the certified stable-AeST parent
- output `mPk,mTk,vTk`
- `P_k_max_h/Mpc = 5`
- no nonlinear correction
- no lensing
- no `k_output_values`
- no explicit `k_per_decade_for_pk` or `k_per_decade_for_bao`

The returned common bounded transfer support is authoritative. No extrapolation beyond that support is permitted.

## Frozen source-state construction

At each target redshift, construct

- `delta_cb = f_b delta_b + f_c delta_cdm`
- `theta_cb = f_b theta_b + f_c theta_cdm`
- `v_cb = -theta_cb / Hconf`
- `P_dd` and `P_tt` from the common primordial prefactor and these transfer states.

The eta response is formed pointwise on identical CLASS k nodes before any interpolation:

`D_dd = [P_dd(+epsilon)-P_dd(-epsilon)]/(2 epsilon)`

`D_tt = [P_tt(+epsilon)-P_tt(-epsilon)]/(2 epsilon)`.

## Frozen quadrature

Use `x = ln k`.

### Primary response operator: LINEAR8192

Interpolate the signed `D_dd(x)` and `D_tt(x)` linearly onto 8192 uniformly spaced x nodes over the exact returned support and integrate

`dV/deta = integral dx k^3 D_P(k) W^2(8k) / (2 pi^2)`

with Simpson quadrature on the dense x grid.

Positive eta=0 baseline spectra are interpolated log-linearly on the same dense grid before variance integration.

### Resolution controls

Repeat LINEAR with 4096 and 16384 dense nodes.

### Independent shape-preserving response operator: PCHIP8192

Apply PCHIP directly to the signed response spectrum `D_P(x)`; do not take its logarithm. Integrate on the same 8192-node dense x grid.

Positive eta=0 baseline spectra use PCHIP in log power.

No smoothing, clipping, outlier rejection, fitted response template, or extrapolation is allowed.

## Derivative propagation

For each operator,

`d sigma / d eta = (dV/deta)/(2 sigma_0)`

and

`d f/deta = d sigma_tt/deta / sigma_dd,0 - sigma_tt,0 d sigma_dd/deta / sigma_dd,0^2`.

## Source-state ShapeFit construction

For Stage B, construct the model `P_dd(k,z)` from the same bounded source state. A bounded `PowerSpectrumInterpolator1D` may be used only as the input representation required by the DESI/cosmoprimo BAO filter. It must not extrapolate beyond the returned source-state support.

Compute `Ap` and the ShapeFit smooth-spectrum slope `m` from this bounded source-state spectrum. The old CLASS `pk_cb_lin(z)` path is forbidden in R9b2j.

Geometry (`qpar`, `qper`, `qiso`, `qap`) remains the same background CLASS geometry as in the frozen R9b construction.

The `df` response uses the signed source-state `df/deta` above and the source-state `Ap` response.

## Frozen thresholds

The historical response thresholds are unchanged:

- relative tangent error `E <= 0.05`
- tangent cosine `C >= 0.995`
- tangent norm `> 1e-12`
- eta=0 value closure relative error `<= 5e-3`
- eta=0 tau invariance relative error `<= 5e-3`.

No threshold may be relaxed after results are seen.

## Stage A gates

### J1 provenance

Require the frozen R9b2i artifact SHA and classification, all required ancestor commits, and certified direct physical source topology.

### J2 common bounded k grid

For every tau, epsilon pair and target redshift, `eta=0,+epsilon,-epsilon` must have identical finite k nodes, positive finite baseline `P_dd/P_tt`, at least 32 modes, and support from at most `2e-4 h/Mpc` to at least `2 h/Mpc`.

### J3 eta=0 closure and tau invariance

Using LINEAR8192, require all six redshifts and all tau values to satisfy the frozen `5e-3` closure against CLASS internal sigma8 and the historical effective-growth proxy. Eta=0 tau variation in sigma8_dd, sigma8_tt, and f must also be `<=5e-3`.

### J4 LINEAR response resolution convergence

For each tau and each epsilon, compare LINEAR4096 vs LINEAR8192 and LINEAR8192 vs LINEAR16384 for the six-component `df/deta` vector. Every comparison must satisfy `E<=0.05`, `C>=0.995`, and both norms `>1e-12`.

### J5 within-operator epsilon consistency

For each tau, compare epsilon 0.025 vs 0.05 for LINEAR8192 and PCHIP8192. Every comparison must satisfy `E<=0.05`, `C>=0.995`, and both norms `>1e-12`.

### J6 cross-operator response agreement

For each tau and each epsilon, compare LINEAR8192 vs PCHIP8192. Every comparison must satisfy `E<=0.05`, `C>=0.995`, and both norms `>1e-12`.

Only J1-J6 PASS permits Stage B and DESI loading.

## Stage B gates

### K1 official DESI provenance

Require the same pinned official DESI DR1 likelihood repository and six 24-dimensional ShapeFit blocks used by historical R9b.

### K2 corrected source-state ShapeFit vector

Baseline and all tangents must be finite. `Ap/m` must come from bounded source-state `P_dd`, with no `pk_cb_lin(z)` use in the R9b2j path.

### K3 full 24D epsilon consistency

For each tau, LINEAR8192 full ShapeFit tangents at epsilon 0.025 and 0.05 must satisfy `E<=0.05`, `C>=0.995`, norms `>1e-12`.

### K4 full 24D cross-operator agreement

For each tau and epsilon, LINEAR8192 and PCHIP8192 full ShapeFit tangents must satisfy `E<=0.05`, `C>=0.995`, norms `>1e-12`.

### K5 nuisance projection algebra

Require positive finite deprojected Fisher information and projection idempotence metric `<=1e-8`.

### K6 matched-filter/GLS identity

Require the same numerical identity tolerance as the frozen R9b projection.

## Classification

All gates PASS:

`STABLE_AEST_DESI_DR1_R9B2J_SIGNED_RESPONSE_SHAPEFIT_CERTIFIED`.

Ordered failures:

- `STABLE_AEST_DESI_DR1_R9B2J_PROVENANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_GRID_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_ETA0_CLOSURE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_RESPONSE_RESOLUTION_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_EPSILON_CONSISTENCY_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_CROSS_OPERATOR_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_DESI_PROVENANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_SHAPEFIT_VECTOR_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_FULL_TANGENT_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_FULL_CROSS_OPERATOR_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_NUISANCE_PROJECTION_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_MATCHED_FILTER_GLS_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2J_RUN_FAIL`.

A PASS licenses reporting the corrected compressed DESI ShapeFit projection. It does not by itself license an observational detection claim, a full-EFT modified-gravity claim, or a tau bound. Historical FAILs remain historical FAILs.