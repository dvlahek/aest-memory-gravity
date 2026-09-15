# Stable AeST DESI DR1 R9b2k ShapeFit dm Repair01 — predata lock

## Purpose

R9b2k certified the native source response at high CLASS k density but failed the conditional DESI Stage-B ShapeFit vector because all six `dm` components were non-finite. `qiso`, `qap`, and `df` were finite. This repair is restricted to the saved-source ShapeFit `m/dm` adapter and does not modify the source response, CLASS parameters, DESI data, likelihood algebra, or any numerical threshold.

Historical R9b2k remains `STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_VECTOR_FAIL` and is never reclassified.

## Frozen parent result

Required local parent:

- `results/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.json`
- SHA256 `f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e`
- classification `STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_VECTOR_FAIL`
- K1 through K6 all PASS
- B1 PASS
- B2 FAIL

Required D2 checkpoints are the existing files in `results/stable_aest_desi_dr1_r9b2k_work/`. No CLASS model may be recomputed by this repair.

## Localized implementation defect

The parent adapter reused `fcache[z]['filter']`, which was constructed from the broad fiducial cosmology power-spectrum interpolator. Cosmoprimo `BasePowerSpectrumBAOFilter` sets `self.k` in the constructor through `set_k()`. Later `__call__` invokes `set_pk()` and `_compute()` but does not call `set_k()` again. Therefore a filter prepared on broad fiducial support retains that support when later called with the bounded source-state Pdd.

The repair treats this as a support-matching defect. It does not change the ShapeFit definition.

## Frozen repaired construction

For each of the six DESI redshifts:

1. Load the D2 `tau_H0=10, eta=0` saved source state.
2. Construct the same bounded source-state Pdd interpolator used by R9b2k.
3. Construct a new `PowerSpectrumBAOFilter(..., engine='peakaverage')` using that bounded source Pdd as the constructor input, the source background cosmology as `cosmo`, and the same DESI fiducial cosmology as `cosmo_fid`.
4. This prepared filter fixes its k grid to the D2 bounded source support while retaining fiducial BAO peak locations through `cosmo_fid`.
5. Verify all D2 tau/eta checkpoints at that redshift have the identical native k grid before reusing the prepared source-support filter.
6. For each saved model, call the prepared filter with that model's bounded Pdd and source cosmology.
7. At the unchanged ShapeFit pivot `kp=0.03/s` and `dk=1e-2`, require both smoothed P(k) values to be finite and strictly positive before taking logarithms.
8. Compute the unchanged slope

   `m = d ln P_now / d ln k`

   from the two pivot points.
9. Compute the unchanged `Ap`, `apar`, `aper`, `df`, and `dm=m-m_fid` definitions.

No clipping, smoothing after the fact, NaN replacement, extrapolation beyond bounded support, parameter removal, or threshold relaxation is permitted.

## Independent support/filter control

For every saved D2 row, the `m` value from the cached per-redshift support-matched filter is compared with a freshly constructed support-matched peak-average filter for the same row. The maximum symmetric relative difference must be <= `1e-8`, and both values must be finite.

This gate tests that filter state reuse does not itself change the ShapeFit slope.

## Frozen Stage-B gates

Repair01 uses the same DESI files, covariance, six bins, 24D ordering, epsilon values `{0.025,0.05}`, tau grid `{10,5,2.5,1.25}`, physical eta interval `[0,0.05]`, and source-response bundles as R9b2k.

The existing thresholds remain:

- E <= 0.05
- C >= 0.995
- nonzero tangent norm gate inherited from R9b2k
- eta=0/source-response closure already frozen by parent K gates
- nuisance projection idempotence <= 1e-8
- matched-filter / GLS eta agreement with the existing tolerance.

Repair-specific gate order:

- R1 parent provenance and exact parent hash
- R2 all required D2 checkpoints valid and common-grid support verified
- R3 support-matched filter construction and finite positive pivot values
- R4 cached-vs-fresh filter `m` agreement <= 1e-8
- B1 official DESI provenance
- B2 full ShapeFit baseline/tangent vector finite
- B3 full 24D epsilon consistency
- B4 full 24D linear-vs-PCHIP consistency
- B5 nuisance projection algebra
- B6 matched-filter / GLS identity.

## Classification

PASS only if every R1-R4 and B1-B6 gate passes:

`STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_CERTIFIED`

Otherwise report the first failed gate with a dedicated Repair01 FAIL label. A Repair01 PASS licenses reporting the compressed DESI ShapeFit projection only. It does not license an observational detection claim, full-EFT modified-gravity claim, or tau bound.
