# IMPORTANT PROJECT HISTORY

This file is the durable continuation checkpoint for the AeST memory-gravity project. Read this before reopening the DESI direct-velocity / ShapeFit chain.

## 2026-09-15 — R9b2k native-k density breakthrough

**IMPORTANT: do not restart the investigation from R9b/R9b2/R9b2j. The main native-response numerical problem is already localized and closed.**

### What is now established

- Historical R9b2j remains `STABLE_AEST_DESI_DR1_R9B2J_CROSS_OPERATOR_FAIL` on the 108-node native CLASS grid.
- R9b2k increased the *actual solver grid*, not merely an interpolation grid:
  - historical default: 108 native k nodes
  - D1 `(k_per_decade_for_pk,k_per_decade_for_bao)=(80,560)`: 864 native k nodes
  - D2 `(160,1120)`: 1729 native k nodes.
- Every R9b2k Stage-A gate K1-K6 passed.
- D1 -> D2 response convergence passed.
- D2 epsilon consistency passed.
- D2 linear-vs-PCHIP signed-response agreement passed for every tau and both epsilon values.
- Typical D2 cross-operator values are E about 9.3e-4 and C about 0.999999991.
- Therefore the large R9b2j linear/PCHIP disagreement was caused by insufficient native CLASS k sampling at 108 nodes, not by an intrinsic physical instability of the source response.

### What failed next

R9b2k proceeded into DESI Stage B. Official DESI provenance passed, but the ShapeFit theory vector failed finiteness.

The failure is exactly localized:

- `qiso`: finite
- `qap`: finite
- `df`: finite
- `dm`: NaN in all six DESI bins

Thus only positions 3, 7, 11, 15, 19, 23 of the 24D vector fail.

The current adapter computes `dm = m - m_fid`, where `m` is the logarithmic slope of a BAO-smoothed bounded source-state Pdd.

## 2026-09-15 — R9b2k ShapeFit dm Repair01

**IMPORTANT: Repair01 is also frozen. Do not repeat it as if it were unresolved.**

Repair01 reused all 20 saved D2 checkpoints and did not rerun CLASS. It rebuilt the peak-average BAO filter on the bounded D2 source-state support, removing the original broad-fiducial-filter support mismatch.

Repair01 nevertheless classified

`STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_FILTER_SUPPORT_FAIL`.

The run emitted

`RuntimeWarning: invalid value encountered in log10`

from `cosmoprimo/interpolator.py` while constructing the no-wiggle interpolator.

### New localization

The remaining issue is now more specific than a generic filter-support mismatch.

`PowerSpectrumBAOFilter.smooth_pk_interpolator()` clones the source interpolator using the filter's raw `pknow` array. `PowerSpectrumInterpolator1D` represents the power spectrum logarithmically. Therefore a non-positive or non-finite `pknow` node anywhere on the full filter support can poison the global smooth interpolator, even though ShapeFit `m` only needs the local logarithmic slope around the pivot k ~ 0.03 h/Mpc.

Repair01 therefore does **not** establish that the physical/local ShapeFit pivot slope is undefined. It establishes that the global smooth-interpolator adapter imposes a stronger positivity requirement than the local `m` definition needs.

### Next authorized step: Repair02 raw-pknow local pivot audit

Repair02 only. Requirements:

1. Do **not** rerun CLASS.
2. Reuse `results/stable_aest_desi_dr1_r9b2k_work/*.pkl`.
3. Keep the R9b2k Stage-A K1-K6 PASS result frozen.
4. Use the same support-matched peak-average filter as Repair01.
5. Inspect raw `filter.k` and raw `filter.pknow` before any `smooth_pk_interpolator()` call.
6. Report all non-positive/non-finite raw no-wiggle nodes and their k locations.
7. Require a strictly positive finite neighborhood around both ShapeFit pivot points.
8. Compute local `m` directly from raw `pknow` in log k/log P, using preregistered linear and PCHIP local operators.
9. No clipping, no replacing negative values, no smoothing rewrite, no threshold relaxation.
10. If raw `pknow` is non-positive at the pivot neighborhood, stop and classify local pivot failure.
11. If the local pivot is healthy, require full 24D tangent epsilon consistency and cross-operator agreement before any DESI projection.
12. Preserve all historical FAILs and all existing projection definitions.

### Frozen identifiers

- R9b2k classification: `STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_VECTOR_FAIL`
- R9b2k JSON SHA256: `f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e`
- R9b2k science log SHA256: `5580e537971f38d7007eed66eb0b5ef8cb92a36583dad348d7afab07ad95d306`
- R9b2k postdata freeze commit: `dd3981b2fd838fb24a997af77f913c3d5dd8d07b`
- Repair01 postdata freeze commit: `8f789b8203dfbee4a9ef7a16ddfb1bfd201bc78b`

Treat this checkpoint as high-priority project history. If future work on DESI direct velocity starts without mentioning the 108 -> 864 -> 1729 result, the six `dm` NaNs, and Repair01's global raw-pknow/log-interpolator failure, stop and read this file first.
