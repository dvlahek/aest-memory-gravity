# Stable AeST DESI DR1 R9b2e raw solver velocity closure preregistration

## Purpose

R9b2d completed as

`STABLE_AEST_DESI_DR1_R9B2D_DEFAULT_GRID_AEST_UNRESOLVED`.

It established three facts before this preregistration:

1. GR density and velocity source observables are invariant under DENSE versus DEFAULT CLASS k sampling at approximately 1e-7.
2. AeST eta=0 internal sigma8 and the historical integrated growth proxy are invariant under the same change at approximately 1e-6.
3. DEFAULT sampling repairs the density-source extraction to within the frozen 0.5% internal-sigma8 gate, but its velocity-source spectrum remains catastrophically pathological at the first three frozen redshifts.

Therefore the remaining question is below the transfer/Fourier output layer: are the raw ODE perturbation histories (`theta_b`, `theta_cdm`) healthy and then corrupted when mapped to transfer outputs (`t_b`, `t_cdm`), or is the pathology already present in the raw solver history?

R9b2e is a theory-only closure/localization audit. No DESI data vector, covariance, likelihood, eta derivative, matched filter, preference, or tau constraint is evaluated.

## Frozen provenance

Required ancestors/results:

- R9b2d post-result record: `6b26243f78b477f7d4040c6499085faf05e8ffac`
- R9b2d preregistration: `bb15759f23246d3b7af734ff7f7cb2052f44d651`
- R9b2d implementation: `a18020d3b307294b742614edc75a5ed28d7a91e8`
- R9b2c postdata: `7c4cc8a0a9f2a59a91cbb288a157f880d630f309`
- historical baryon matter-sector audit implementation: `nl1c6d2a/baryon_matter_sector_audit.py`, whose frozen dense-history gates are inherited where stated below.

The local completed R9b2d JSON is expected to have SHA256

`54db5acc49d4099d1173aa029a58e02cdac0e844c03aa72d95fa08b86a6f70df`

and classification

`STABLE_AEST_DESI_DR1_R9B2D_DEFAULT_GRID_AEST_UNRESOLVED`.

No historical result may be reclassified by R9b2e.

## Frozen model settings

Use the R9b2d DEFAULT AeST physical/numerical setup:

- `eta = 0`
- `tau_H0 = 10`
- `aest_memory_order = 20`
- `tol_perturbations_integration = 3e-8`
- DEFAULT CLASS k sampling: omit `k_per_decade_for_pk` and `k_per_decade_for_bao`
- `output = mPk,mTk,vTk`
- `P_k_max_h/Mpc = 5`
- `z_max_pk >= 2.3`
- no nonlinear correction
- no lensing.

The matched GR control changes only

- `aest_enabled = no`
- `aest_memory_enabled = no`
- `aest_eta = 0`.

## Frozen raw-history mode set

To obtain raw perturbation histories, add `k_output_values` only for this diagnostic. The physical requested modes are

`K_H = geomspace(0.02, 2.0, 24)` in `h/Mpc`,

serialized to CLASS as physical `1/Mpc` values `K_H * h` with `.17g` precision.

This mode set is fixed before the result and spans the sigma8-relevant range without selecting post-result suspicious k values.

The addition of `k_output_values` is diagnostic only. Its effect on internal observables is explicitly gated below against the completed no-`k_output_values` R9b2d DEFAULT result.

## Frozen redshift coordinates

Evaluate closure at the six existing theory coordinates:

- 0.29536404346937617
- 0.5096288678782911
- 0.7057956472488681
- 0.9185851971138159
- 1.3170658832980264
- 1.4905017757527006.

For continuity/smoothness checks, use the raw-history interval `0.2 <= z <= 1.6` with two endpoint samples dropped when enough points are available, following the historical dense-history audit pattern.

## Frozen fields and mapping

From `get_perturbations()` scalar histories require, for every requested mode:

- scale factor `a`
- conformal time `tau`
- `delta_b` (or `d_b`)
- `theta_b` (or `t_b`)
- `delta_cdm` (or `d_cdm`)
- `theta_cdm` (or `t_cdm`)
- `phi`
- use direct `phi_prime` if available; otherwise use the derivative of the cubic spline of `phi(tau)` exactly as in the historical baryon matter-sector audit.

From `get_transfer(z, output_format="class")` require

- `k (h/Mpc)`
- `d_b`, `t_b`, `d_cdm`, `t_cdm`.

The requested physical k modes must be present in the transfer grid to relative mismatch <= `1e-12`, inherited from the earlier dense-history audit.

Raw histories are evaluated at the six target scale factors using both cubic spline and PCHIP in `a`. Cubic is the primary historical mapping; PCHIP is the robustness control.

## Frozen gates

### E1 — provenance and requested-mode identity

PASS if all frozen ancestor/result checks pass, the local R9b2d JSON matches the frozen hash/classification/gate pattern, 24 scalar histories are returned, and every requested k mode matches a transfer-grid k node within relative `1e-12`.

### E2 — diagnostic `k_output_values` internal invariance

Compare AeST internal `sigma(8,z,h_units=True)` and `effective_f_sigma8/sigma8` from the raw-history diagnostic run against the no-`k_output_values` R9b2d DEFAULT rows.

PASS if all six relative differences are <= `5e-3`.

This retains the existing observational closure tolerance and prevents the raw-history request itself from being treated as a silent physics change.

### E3 — GR raw-history/transfer closure

For `d_b`, `t_b`, `d_cdm`, and `t_cdm`, compare the 24 raw histories evaluated at all six target redshifts with the transfer-table values at exactly the same requested k nodes.

For each field compute global relative L2 error over the full 24x6 matrix for cubic and PCHIP mappings.

PASS if every field has cubic relative L2 <= `2e-4` and PCHIP relative L2 <= `5e-4`.

The primary `2e-4` threshold is inherited from `NL1C6D2A` dense-native closure. The looser PCHIP control is frozen before the run and only tests interpolation robustness.

### E4 — AeST raw continuity and finiteness

For baryons and CDM separately, evaluate on every raw mode over `0.2 <= z <= 1.6`:

`delta' + theta - 3 phi' = 0`

using cubic derivatives with respect to conformal time.

For each species/mode normalize the L2 residual by the maximum L2 norm of `delta'`, `theta`, and `3 phi'`, exactly following the historical baryon audit convention.

PASS if all required raw arrays are finite and the maximum normalized residual for each species is <= `2e-3`.

This threshold is inherited from the historical continuity audit.

### E5 — AeST raw-history/transfer density closure

For `d_b` and `d_cdm`, require cubic raw-versus-transfer global relative L2 <= `2e-4` and PCHIP <= `5e-4`.

### E6 — AeST velocity discrepancy localization

Compute the same raw-versus-transfer closure for `t_b` and `t_cdm`.

Define material velocity-output discrepancy before the run as at least one of:

- cubic global relative L2 for `t_b` or `t_cdm` >= `5e-2`
- PCHIP global relative L2 for `t_b` or `t_cdm` >= `5e-2`
- at least one requested `(k,z)` point where the symmetric relative discrepancy in `t_b` or `t_cdm` is >= `0.5`, using denominator `max(|raw|,|transfer|, 1e-300)`.

E6 PASS if E4 and E5 pass and this material velocity discrepancy is present.

### E7 — raw interpolation robustness

For the raw histories themselves, compare cubic versus PCHIP values at the six target redshifts. Compute global relative L2 for each of `d_b,t_b,d_cdm,t_cdm`.

PASS if every field is <= `5e-3`.

This ensures a localized transfer discrepancy is not merely an artifact of the chosen raw-history interpolator.

## Classification

If E1-E7 all pass:

`STABLE_AEST_DESI_DR1_R9B2E_TRANSFER_VELOCITY_MAPPING_DEFECT_CERTIFIED`

This classification means the raw AeST eta=0 solver histories are finite, continuity-consistent, interpolation-robust, and density-closed, while the transfer/Fourier velocity output materially disagrees with those histories.

Otherwise use the first applicable class:

- `STABLE_AEST_DESI_DR1_R9B2E_PROVENANCE_OR_MODE_IDENTITY_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2E_KOUTPUT_INTERNAL_INVARIANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2E_GR_RAW_TRANSFER_CLOSURE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2E_RAW_SOLVER_HISTORY_UNRESOLVED`
- `STABLE_AEST_DESI_DR1_R9B2E_DENSITY_MAPPING_UNRESOLVED`
- `STABLE_AEST_DESI_DR1_R9B2E_VELOCITY_MAPPING_DEFECT_NOT_LOCALIZED`
- `STABLE_AEST_DESI_DR1_R9B2E_RAW_INTERPOLATION_ROBUSTNESS_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2E_RUN_FAIL` for a technical exception.

## Interpretation policy

A certified transfer-velocity mapping defect does not repair or reclassify historical R9 failures and does not itself license a DESI science likelihood. It licenses a separate theory repair/validation step in which the velocity observable is constructed directly from a certified raw solver-history representation or the underlying CLASS transfer-output mapping is corrected and revalidated against GR/CAMB and the raw histories.

If E4 fails, the problem is already in the raw AeST ODE history and transfer-layer debugging stops. If E4 passes but E5 fails, the transfer mapping is not velocity-specific. If E4/E5 pass and E6 is absent, the current 24-mode audit did not reproduce a localized mapping defect and must not be promoted to a science workaround.
