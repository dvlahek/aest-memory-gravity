# IMPORTANT PROJECT HISTORY

This file is the durable continuation checkpoint for the AeST memory-gravity project. Read this before reopening the DESI direct-velocity / ShapeFit chain or the ACT live-lensing chain.

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

Treat this as the high-priority continuation state for DESI direct-velocity work.

## 2026-09-15 — R10a ACT DR6 LIVE WEYL-MEMORY PROJECTION CERTIFIED

**IMPORTANT: the ACT DR6 live-lensing chain is now numerically closed for the certified local AeST regime. Do not revert to interpreting R6a as the final lensing result. R10a supersedes the fixed-template approximation with the certified live Weyl response.**

R10a classification:

`STABLE_AEST_ACT_DR6_R10A_LIVE_WEYL_MEMORY_PROJECTION_CERTIFIED`

All preregistered gates R10A-G1 through R10A-G7 passed:

- parent provenance;
- official ACT interface control;
- support and live eta-zero baseline consistency;
- central-derivative stability in ACT bandpower space;
- amplitude-deprojection algebra and physical local model;
- matched-filter / GLS identity;
- ACT-space tau coherence.

The official ACT control is reproduced: `chi2_fiducial = 14.057911788739439` for target `14.06 +/- 0.10`.

### Live ACT result

For tau/H0 = 10, 5, 2.5, 1.25:

- signed template S/N = `3.226`, `3.261`, `3.327`, `3.460`;
- signed eta_hat = `8.786e5`, `8.988e5`, `9.385e5`, `1.019e6`;
- sigma_eta = `2.723e5`, `2.756e5`, `2.820e5`, `2.945e5`;
- physical Delta chi2 at the edge `eta=0.05` = approximately `1.18e-06` for every tau;
- `F_perp/F_raw` = approximately `0.598`, `0.595`, `0.591`, `0.585`.

Therefore about 58.5%--59.8% of the raw covariance-metric lensing-template norm survives deprojection against a broadband lensing-amplitude nuisance. The memory fingerprint is not a pure amplitude rescaling.

### Tau result

ACT-space tangent coherence relative to tau10 is extremely high:

- tau5: norm ratio `0.991668`, cosine `0.99999348`;
- tau2.5: norm ratio `0.975770`, cosine `0.99994374`;
- tau1.25: norm ratio `0.951043`, cosine `0.99969046`.

Thus shorter relaxation time does not rescue ACT detectability in the certified interval.

### Detection interpretation

**There is no physical AeST-memory detection.**

The `3.2--3.5 sigma` values are signed mathematical template-overlap diagnostics obtained only if eta is allowed to extrapolate to values of order `10^6`. The certified physical interval is only `0 <= eta <= 0.05`, so the required unconstrained coefficient is roughly 1.8e7--2.0e7 times too large.

Inside the licensed physical interval, `Delta chi2 ~ 1.18e-06`, which is observationally negligible.

Therefore:

- no detection claim;
- no physical eta estimate from eta_hat_signed;
- no tau bound;
- no full cosmological inference claim;
- no nonlinear-lensing claim;
- live ACT DR6 projection is reportable as a validated physical null-sensitivity result.

### R6a relation

At tau10, R10a closely reproduces the earlier R6a fixed-template result (`sigma_eta`, `eta_hat`, shape fraction, and physical Delta chi2 differ only at the sub-percent level). This validates the earlier qualitative result while replacing it with a live-theory calculation.

### Frozen R10a identifiers

- R10a preregistration: `4c46fd21df048553b577a1927d8404bc493f649e`
- R10a final implementation: `af2b85cf2a4d564c7575aa9bdcdd9039ff48ba0f`
- R10a runner / run head: `dd295e0800e45a27d5acd01872915ca4e71bbb40`
- R10a full runner SHA256: `10a46b4f593220cee1198e7e4a577dd2c3ba027997ab7e2e0245bf0e2e4bb5b4`
- R10a environment SHA256: `2b362b30502bcc367a30b03ec9d26d89d99bf10ff77cebe3819b1e87414fb722`
- R10a JSON SHA256: `e794162e7090435e4344f29fb926460e012d3f37fa1c87729e711d172c73598f`
- R10a science log SHA256: `72ed65ec7f87f45e481c16c72f8f0a5cf22fd2a78dd0ccbb48d9549673aee789`
- R10a NPZ SHA256: `f37ebc39342a57c6f217a9593b3372aa162102ca337d119cc8a7bc785906c49b`
- R10a postdata freeze commit: `b7da648f1810ea0c047b6e511e3f87211e830329`

### Next scientific directions

Do not spend the next step on another ACT fixed-template variation. The amplitude, not numerical stability or shape distinctness, is the bottleneck.

Natural next questions are:

1. lensing detectability forecast: quantify the precision improvement needed for a physical `eta=0.05` signal and compare with next-generation surveys;
2. kSZ / velocity-sensitive observables: test if the memory model leaves a relatively larger signature in electron momentum / peculiar-velocity statistics than in CMB lensing or compressed DESI ShapeFit.

Treat R10a as the authoritative ACT live-lensing checkpoint.