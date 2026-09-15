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

### Historical Stage-B failure

R9b2k proceeded into DESI Stage B. Official DESI provenance passed, but the ShapeFit theory vector failed finiteness.

The failure was exactly localized:

- `qiso`: finite
- `qap`: finite
- `df`: finite
- `dm`: NaN in all six DESI bins

Thus only positions 3, 7, 11, 15, 19, 23 of the 24D vector failed.

The adapter computes `dm = m - m_fid`, where `m` is the logarithmic slope of a BAO-smoothed bounded source-state Pdd.

## 2026-09-15 — R9b2k ShapeFit dm Repair01

**IMPORTANT: Repair01 is frozen. Do not repeat it as if it were unresolved.**

Repair01 reused all 20 saved D2 checkpoints and did not rerun CLASS. It rebuilt the peak-average BAO filter on the bounded D2 source-state support, removing the original broad-fiducial-filter support mismatch.

Repair01 nevertheless classified

`STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_FILTER_SUPPORT_FAIL`.

The run emitted

`RuntimeWarning: invalid value encountered in log10`

from `cosmoprimo/interpolator.py` while constructing the no-wiggle interpolator.

### Localization from Repair01

`PowerSpectrumBAOFilter.smooth_pk_interpolator()` clones the source interpolator using the filter's raw `pknow` array. `PowerSpectrumInterpolator1D` represents the power spectrum logarithmically. Therefore a non-positive raw `pknow` node anywhere on the full filter support can poison the global smooth interpolator, even though ShapeFit `m` only needs the local logarithmic slope around the pivot k ~ 0.03 h/Mpc.

Repair01 therefore did **not** establish that the physical/local ShapeFit pivot slope was undefined. It established that the global smooth-interpolator adapter imposed a stronger positivity requirement than the local `m` definition needs.

## 2026-09-15 — R9b2k ShapeFit dm Repair02 CERTIFIED

**IMPORTANT: the direct-velocity compressed ShapeFit numerical chain is now closed and certified. Do not reopen the dm issue or restart from R9b2j.**

Repair02 classification:

`STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_CERTIFIED`

All preregistered gates passed:

- P1 parent provenance
- P2 saved D2 checkpoints
- P3 local positive pivot
- P4 local m operator agreement
- B1 DESI provenance
- B2 finite 24D ShapeFit vector
- B3 full-tangent epsilon consistency
- B4 full cross-operator agreement
- B5 nuisance projection
- B6 matched-filter / GLS identity

### What Repair02 proved about the dm failure

Repair02 inspected raw peak-average `pknow` directly and never called the global `smooth_pk_interpolator()`.

Across all saved D2 rows, the raw no-wiggle spectrum is finite on all 1024 filter nodes. The only non-positive values occur for the lowest-redshift bin and negative eta cases at one isolated high-k node around `k = 4.233831910284027 h/Mpc`. This is far from the ShapeFit pivot near `k = 0.0300165756 h/Mpc`.

The local positive segment containing the pivot is healthy. In the affected cases it still extends to about `4.1893418468 h/Mpc`.

The maximum symmetric relative difference between preregistered local linear and local PCHIP m values is

`4.367779654032155e-05`,

well below the frozen `0.005` gate.

Therefore the historical six-dm NaNs were a global-log-interpolator artifact caused by an irrelevant high-k non-positive `pknow` node. They were not a failure of the local ShapeFit slope.

### Full 24D robustness

The complete tangent is now finite and stable.

- epsilon consistency E is approximately `8.8e-05` to `9.8e-04`, with C >= about `0.99999959`;
- primary/control cross-operator E is approximately `9.27e-04` to `9.28e-04`, with C about `0.9999999935` or higher;
- all frozen `E <= 0.05`, `C >= 0.995` gates pass by a large margin.

### DESI compressed projection result

For tau/H0 = 10, 5, 2.5, 1.25:

- signed shape S/N is approximately `1.357`, `1.357`, `1.357`, `1.355`;
- signed eta_hat is approximately `12370`, `12466`, `12667`, `13055`;
- sigma_eta is approximately `9116`, `9187`, `9333`, `9632`;
- restricting to the physical interval `0 <= eta <= 0.05` puts the best fit at `eta=0.05` for every tau;
- physical Delta chi2 relative to eta=0 is only about `1.4e-05` to `1.5e-05`.

Matched-filter and GLS estimates agree to floating-point precision. Projection idempotence is approximately `2.24e-16`.

### Scientific meaning

This is a certified **compressed DESI ShapeFit null-sensitivity result** in the physical eta interval.

The data have only an O(1.35 sigma) alignment with the signed mathematical template direction, and the required best-fit amplitude is O(10^4), many orders of magnitude outside the physical interval. Inside `0 <= eta <= 0.05`, the likelihood change is negligible.

Therefore:

- no observational detection claim;
- no useful DESI eta bound;
- no tau bound;
- no full-EFT modified-gravity claim;
- compressed corrected ShapeFit projection is reportable as a validated null result.

### Frozen identifiers

- R9b2k classification: `STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_VECTOR_FAIL`
- R9b2k JSON SHA256: `f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e`
- R9b2k postdata freeze commit: `dd3981b2fd838fb24a997af77f913c3d5dd8d07b`
- Repair01 classification: `STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_FILTER_SUPPORT_FAIL`
- Repair01 JSON SHA256: `af92b8f7c6186a5e04c7a4973840617dd64ef7afb33deddc24804c1b974f40ad`
- Repair01 postdata freeze commit: `8f789b8203dfbee4a9ef7a16ddfb1bfd201bc78b`
- Repair02 preregistration: `9e9fd426e3030727f0723cf7e50ae4ef0c2799e8`
- Repair02 implementation: `aa3909146b438581f41f0de97171e6d0e2a34ec9`
- Repair02 runner: `c536e64d134f3de40af9c502807a09b431ff1566`
- Repair02 JSON SHA256: `eb221160bf64b0905ec0b620fb8441aea2a1e55fc2981f8b3974954917f1cea4`
- Repair02 log SHA256: `cb7f0d528d118c72edd7c2bd0c678bd48ab16ac6e8f580df21b1963115dd604e`
- Repair02 NPZ SHA256: `f83e7c86278891c220941f2fad13d2b21fb96cbaffd87ab91fafad557eae06ce`
- Repair02 full runner SHA256: `490f0c7c842c1974b6003b70611409128ff27924fa642984a72afcb9c1588498`
- Repair02 postdata freeze commit: `d3fd6191d55f4e74aa8666f842dae64bd8aee09b`

Treat this as the high-priority continuation state. Future DESI direct-velocity work must begin from the certified Repair02 result, not from the historical R9b2/R9b2j failures.