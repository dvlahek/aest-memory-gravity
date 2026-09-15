# Stable AeST DESI DR1 R9b2k ShapeFit dm Repair01 postdata

## Frozen status

Repair01 completed without any CLASS rerun and classified

`STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_FILTER_SUPPORT_FAIL`.

The parent R9b2k Stage-A K1-K6 PASS result remains frozen and is not reclassified.

## What Repair01 established

- all 20 saved D2 checkpoints were present and validated;
- no CLASS worker was invoked;
- the official DESI repository/data provenance path remained available;
- the ShapeFit `m/dm` failure persists even after constructing the peak-average BAO filter on the bounded D2 source-state support;
- cosmoprimo emitted `RuntimeWarning: invalid value encountered in log10` from `interpolator.py` when the repaired path attempted to construct the smooth-power interpolator.

The relevant implementation detail is that `PowerSpectrumBAOFilter.smooth_pk_interpolator()` clones the input power-spectrum interpolator using the filter's raw `pknow` array. `PowerSpectrumInterpolator1D` then forms a logarithmic representation. Therefore any non-finite or non-positive `pknow` value anywhere on the full filter support can invalidate the smooth interpolator, even if the ShapeFit pivot around k~0.03 h/Mpc is locally finite and positive.

## Interpretation

Repair01 does **not** show that the ShapeFit pivot slope itself is undefined. It shows that the current adapter requires a stronger global-positivity condition than the local ShapeFit definition requires.

The next test must inspect raw `filter.k` and raw `filter.pknow` directly before any `smooth_pk_interpolator()` construction. No clipping, smoothing replacement, threshold relaxation, or postdata choice of a favorable operator is allowed.

## Authorized next step: Repair02 local raw-pknow pivot audit

Repair02 must:

1. reuse only the existing D2 checkpoints;
2. preserve the parent R9b2k Stage-A K1-K6 PASS result;
3. construct the same support-matched peak-average filter as Repair01;
4. inspect raw `filter.pknow` over its full grid and report the count/location/range of non-positive or non-finite nodes;
5. require a finite strictly positive raw no-wiggle neighborhood bracketing both ShapeFit pivot points;
6. evaluate `m` directly from the raw no-wiggle output in that local positive neighborhood, without constructing a global `smooth_pk_interpolator()`;
7. use two preregistered local interpolation operators (linear in log k/log P and PCHIP in log k/log P) and require `E <= 0.05`, `C >= 0.995` for the resulting full ShapeFit tangents before projection;
8. stop if the raw no-wiggle spectrum is non-positive at or around the pivot;
9. preserve all DESI projection definitions and historical classifications.

Repair01 is a historical technical/numerical FAIL and must not be reclassified.