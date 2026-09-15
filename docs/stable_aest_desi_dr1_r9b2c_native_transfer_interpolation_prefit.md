# Stable AeST DESI DR1 R9b2c native-transfer interpolation audit preregistration

## Purpose

R9b2b ended with historical classification

`STABLE_AEST_DESI_DR1_R9B2B_AEST_ETA0_CLOSURE_FAIL`.

The pure-GR source-state construction passed against the locked CLASS/CAMB adapter, but AeST-enabled eta=0 `get_transfer(z)` returned isolated catastrophic density/velocity states at four of the six frozen effective redshifts. The failure is almost exactly invariant across `tau_H0={10,5,2.5,1.25}`.

The preserved v0.78 audit already showed that native source/Fourier matter power closes at common native `(k,tau)` nodes while large discrepancies can appear at off-native times from distinct CLASS time-interpolation operators. R9b2c tests the remaining specific hypothesis: the native AeST density/velocity state is healthy and the pathology is introduced by the off-native `get_transfer(z)` accessor.

This is theory-only. No DESI data vector, covariance, likelihood, eta derivative, matched filter, or parameter preference is evaluated. The six DESI effective redshifts are used only as frozen theory coordinates.

## Frozen provenance

Required ancestors/results:

- R9b2b post-result lock: `3101581468bc8a5b85eb2b34c33df22418f1ce88`
- R9b2b result JSON SHA-256: `bc0013a70a1e13ef925efc39b57f8810d7c5bab80091eed1ba4407bc1862314e`
- R9b2 velocity adapter result lock: `f5484b4572b673dfcead51875e3aa790c698a18c`
- v0.78 successful result lock: `31c05c22b86e8ac01ce822306efecdcb03cff1d5`
- frozen CLASS parent: `e85808324f51fc694d12e3ed7439552a3c3f9540`

Historical classifications must remain unchanged:

- `STABLE_AEST_DESI_DR1_R9B2_CENTRAL_DERIVATIVE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2A_SERIALIZATION_FREE_EXTRACTION_UNRESOLVED`
- `STABLE_AEST_DESI_DR1_R9B2B_AEST_ETA0_CLOSURE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_VALIDATED`
- `V078_TIME_INTERPOLATION_OPERATOR_CLOSURE_PASS`
- `V078_TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED`

## Frozen redshifts and parameters

Theory-coordinate grid:

- 0.29536404346937617
- 0.5096288678782911
- 0.7057956472488681
- 0.9185851971138159
- 1.3170658832980264
- 1.4905017757527006

AeST eta=0 checks:

- `tau_H0={10,5,2.5,1.25}`
- `eta=0`
- `tol_perturbations_integration=3e-8`
- `aest_memory_order=20`
- `output=mPk,mTk,vTk`
- `P_k_max_h/Mpc=5`
- `z_max_pk>=2.3`
- no nonlinear correction
- no lensing
- no `k_output_values` request.

The GR control uses the same background/numerical setup with `aest_enabled=no` and `aest_memory_enabled=no`.

## Native-state extraction

Use only

`get_transfer_and_k_and_z(output_format="class", h_units=False)`

for the primary native state. Required native fields:

- `d_b`
- `d_cdm`
- `t_b`
- `t_cdm`.

The returned physical `k` and native `z` arrays are treated as the authoritative source grid. The implementation must not call `get_transfer(z)` to construct the primary native/PCHIP result.

For each native `z_j`, form

`d_cb = fb d_b + fc d_cdm`

`theta_cb = fb t_b + fc t_cdm`

and only after interpolation to a target redshift convert

`v_cb = -theta_cb / Hconf(z)`

with `Hconf(z)=Hubble(z)/(1+z)`.

The source spectra remain

`P_dd = C(k) d_cb^2`

`P_tt = C(k) v_cb^2`

with

`C(k)=(2 pi^2/k^3) A_s (k/0.05 Mpc^-1)^(n_s-1)`.

No `pk_lin`, `pk_cb_lin`, local `v/d`, or local division by density power is permitted in the primary construction.

## Frozen interpolation

Primary interpolation coordinate:

`a = 1/(1+z)`.

Primary operator: SciPy `PchipInterpolator` independently along the native time axis for each k mode, applied to the raw state variables `d_b,d_cdm,t_b,t_cdm`.

Robustness operator: linear interpolation in the same `a` coordinate on the same native state table.

No smoothing, clipping, mode removal, local outlier rejection, or hand-selected redshift/k filtering is allowed.

## Gates

All thresholds are frozen before the run.

### R9B2C_C1 — provenance and historical-lock gate

PASS if all required commits are ancestors, the local R9b2b JSON has exact SHA-256 `bc0013a70a1e13ef925efc39b57f8810d7c5bab80091eed1ba4407bc1862314e`, its classification/gates match the locked R9b2b result, the velocity adapter remains validated, and the v0.78 preserved interpretation contains both locked PASS/localization strings.

### R9B2C_C2 — native state coverage and finiteness gate

For GR and each AeST eta=0 tau run, PASS if:

- the native transfer arrays have orientation `(n_k,n_z)` and all four required state arrays share it;
- native k and z coordinates are finite and strictly usable after sorting/deduplication;
- all six target redshifts are bracketed by the retained native time grid;
- retained state values are finite;
- the retained k support contains at least 32 modes and spans `k_h<=2e-4` to `k_h>=2`.

### R9B2C_C3 — pure-GR custom-interpolation benchmark

At all six target redshifts, build PCHIP source-state spectra and compare to the already locked GR adapter.

PASS if each of the following is <= `5e-3`:

- relative `sigma8_dd` difference vs locked CLASS adapter;
- relative `sigma8_tt` difference vs locked CLASS adapter;
- relative `f` difference vs locked CLASS adapter;
- relative `f` difference vs locked CAMB.

All spectra/RMS values must be finite and positive.

### R9B2C_C4 — AeST native-state sanity gate

For `tau_H0=10`, evaluate source spectra directly at every retained native time node with `0.2<=z<=1.6`.

PASS if all such nodes satisfy:

- finite positive source spectra/RMS values;
- `0.1 < sigma8_dd < 2`;
- `0.05 < f_native < 2`.

This gate directly tests if the pathology is already present in the native AeST state.

### R9B2C_C5 — AeST PCHIP target closure gate

For `tau_H0=10`, at all six frozen target redshifts require:

- `0.1 < sigma8_dd_PCHIP < 2`;
- `0.05 < f_PCHIP < 2`;
- relative `sigma8_dd_PCHIP` vs CLASS internal `sigma(8,z,h_units=True)` <= `5e-3`;
- relative `f_PCHIP` vs the historical internal diagnostic `effective_f_sigma8/sigma8` <= `5e-3`.

The internal growth proxy remains a closure control only, not the DESI df definition.

### R9B2C_C6 — interpolation-operator discrepancy localization gate

At `tau_H0=10`, also evaluate the historical direct accessor `get_transfer(z)` only as a diagnostic comparator, using the same source-state `P_dd=C d_cb^2`, `P_tt=C v_cb^2` construction.

Define the maximum target-wise relative discrepancy between direct-accessor and PCHIP values over `sigma8_dd` and `f`.

PASS if this maximum is >= `5e-2` while C4 and C5 pass.

This gate requires a material off-native accessor discrepancy and forbids declaring localization if the native/PCHIP state is itself unhealthy.

### R9B2C_C7 — external-interpolation robustness gate

Compare PCHIP and linear-in-a source-state results at all six target redshifts for `tau_H0=10`.

PASS if the maximum relative difference in each of

- `sigma8_dd`
- `sigma8_tt`
- `f`

is <= `5e-3`.

### R9B2C_C8 — eta=0 tau-invariance gate

Using PCHIP source-state extraction at `tau_H0={10,5,2.5,1.25}`, compare each tau to tau=10 at all six target redshifts.

PASS if the maximum relative change in each of

- `sigma8_dd`
- `sigma8_tt`
- `f`

is <= `5e-3`.

## Classification

If C1-C8 all pass:

`STABLE_AEST_DESI_DR1_R9B2C_OFFNATIVE_TRANSFER_INTERPOLATION_DEFECT_CERTIFIED`

Failure classes, in order:

- `STABLE_AEST_DESI_DR1_R9B2C_PROVENANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2C_NATIVE_STATE_COVERAGE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2C_GR_INTERPOLATION_BENCHMARK_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2C_NATIVE_AEST_STATE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2C_PCHIP_TARGET_CLOSURE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2C_ACCESSOR_DISCREPANCY_NOT_LOCALIZED`
- `STABLE_AEST_DESI_DR1_R9B2C_INTERPOLATION_ROBUSTNESS_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2C_ETA0_TAU_INVARIANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2C_RUN_FAIL` for a technical exception.

## Interpretation policy

A PASS certifies a numerical implementation defect/localization in the off-native AeST transfer accessor under the frozen CLASS implementation: the native state is healthy, two external interpolation operators agree, the externally interpolated state closes against internal integrated observables, and the historical direct accessor materially disagrees.

A PASS does not reclassify R9b2/R9b2a/R9b2b, does not constitute DESI evidence, and does not establish a nonzero eta or constrain tau.

Only a PASS may license a separately preregistered DESI projection using the externally interpolated certified native state representation.
