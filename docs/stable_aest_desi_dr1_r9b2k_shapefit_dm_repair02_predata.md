# Stable AeST DESI DR1 R9b2k ShapeFit dm Repair02 preregistration

## Frozen parent chain

Repair02 is a postprocessing-only continuation of the frozen R9b2k and Repair01 results.

Parent R9b2k:
- classification `STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_VECTOR_FAIL`;
- Stage-A gates K1-K6 all PASS;
- JSON SHA256 `f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e`.

Parent Repair01:
- classification `STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_FILTER_SUPPORT_FAIL`;
- JSON SHA256 `af92b8f7c6186a5e04c7a4973840617dd64ef7afb33deddc24804c1b974f40ad`;
- science log SHA256 `3e9ac93488a9cc43166671abe3c4aac54a6b75465f132d437d4af56b6437dbee`.

No historical result may be reclassified.

## Problem

Repair01 removed the broad-fiducial-filter support mismatch by constructing a peak-average filter on the bounded D2 source-state Pdd support. It still failed because `smooth_pk_interpolator()` builds a global logarithmic power-spectrum interpolator from raw `filter.pknow`; any non-positive/non-finite raw node anywhere on the full filter support can make that global interpolator non-finite.

ShapeFit `m`, however, is defined from the logarithmic slope between only two pivot points

`k_- = 0.03/s * (1 - 0.01)` and `k_+ = 0.03/s * (1 + 0.01)`.

Repair02 tests the raw no-wiggle output locally without altering it.

## Frozen construction

1. No CLASS call or worker subprocess is permitted.
2. Reuse all 20 validated D2 checkpoint files from `results/stable_aest_desi_dr1_r9b2k_work/`.
3. Use the same DESI fiducial cosmology and same support-matched `peakaverage` filter as Repair01.
4. Never call `smooth_pk_interpolator()` in Repair02.
5. Read raw `filter.k` and raw `filter.pknow` after `filter(pkdd, cosmo=source_cosmo)`.
6. Audit the full raw no-wiggle grid for non-finite and non-positive values. Record counts, minimum/maximum finite P, first/last bad k, and bad-k range.
7. Define `good = isfinite(pknow) & (pknow > 0)`.
8. Find the unique contiguous `good` segment containing both ShapeFit pivot points. The segment must contain at least 8 raw nodes and both pivot points must lie strictly inside the segment's k range. No bad node may lie between the two pivot points.
9. No clipping, flooring, sign replacement, smoothing rewrite, extrapolation, or omission of bad nodes inside the selected contiguous segment is allowed.
10. Evaluate raw no-wiggle P at the two pivot points using two preregistered local operators on the same contiguous positive segment:
   - primary: linear interpolation in `(log k, log P)`;
   - control: PCHIP interpolation in `(log k, log P)`.
11. For each operator compute

`m = [log P(k_+) - log P(k_-)] / [log k_+ - log k_-]`.

12. `Ap`, `qiso`, `qap`, `df`, fiducial `m`, nuisance projection, covariance, physical eta interval, and GLS definitions remain unchanged.
13. Both local operators must produce finite positive pivot P values and finite `m` for every one of the 20 x 6 saved D2 rows.
14. The per-row linear-vs-PCHIP `m` disagreement must satisfy symmetric relative error <= 5e-3. This is a value-level adapter gate and is fixed before seeing Repair02 output.
15. Construct two complete 24D ShapeFit tangent families:
   - primary family: source signed-response `linear8192` plus local-linear raw-pknow `m`;
   - control family: source signed-response `pchip8192` plus local-PCHIP raw-pknow `m`.
16. Full-tangent epsilon consistency and primary-vs-control agreement retain the frozen gates `E <= 0.05`, `C >= 0.995`, with both norms > the inherited nonzero norm gate.
17. DESI nuisance projection and matched-filter/GLS identity are evaluated only after all preceding gates pass.

## Classification logic

- provenance/checkpoint mismatch -> technical/provenance FAIL;
- pivot not contained in a valid positive raw-pknow segment -> `...LOCAL_PIVOT_FAIL`;
- per-row local-linear/PCHIP m value gate fail -> `...LOCAL_M_OPERATOR_FAIL`;
- non-finite 24D vector -> `...VECTOR_FAIL`;
- full tangent epsilon fail -> `...FULL_TANGENT_EPSILON_FAIL`;
- full primary/control tangent fail -> `...FULL_CROSS_OPERATOR_FAIL`;
- nuisance projection or GLS identity fail -> corresponding FAIL;
- only if every gate passes -> `STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_CERTIFIED`.

A PASS licenses only the compressed DESI ShapeFit projection under this corrected source-state construction. It does not license a full-EFT modified-gravity claim, observational detection claim, or tau bound.