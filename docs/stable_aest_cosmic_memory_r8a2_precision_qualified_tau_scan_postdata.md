# Stable AeST cosmic memory R8a2 — precision-qualified relaxation-time scan (post-data)

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Formal result

`STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED`

All preregistered R8a2 gates G1--G6 passed. Historical R8a remains `STABLE_AEST_COSMIC_MEMORY_R8A_RUN_FAIL` and is not reclassified.

## Frozen parent and result hashes

- R7a post-data checkpoint: `86c03e6ba2ee9fcbf33a9d319d12ae778a747881`
- R8a post-data checkpoint: `9b138cf04d3a8c323bbf3a82e3e747deea0393dc`
- R8a2 preregistration lock: `e01db75882717b7f2e230d634ff8f930604d8011`
- R8a2 JSON SHA256: `2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66`
- R8a2 NPZ SHA256: `c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1`

## Certified tau grid

`tau H0 = [10, 5, 2.5, 1.25]`

For each tau the direct physical central derivative was evaluated using `eta = +/-0.025`, with `eta = +/-0.05` as a control and same-tau nominal-vs-tight eta-zero precision checks.

## Main quantitative result

Relative tangent amplitudes, normalized to tau H0 = 10:

| tau H0 | sigma8 | f sigma8 | C_L^kk |
|---:|---:|---:|---:|
| 10 | 1.000000 | 1.000000 | 1.000000 |
| 5 | 0.992873 | 0.991058 | 0.982748 |
| 2.5 | 0.977425 | 0.973070 | 0.950796 |
| 1.25 | 0.950164 | 0.939402 | 0.894622 |

Thus, over the tested range, shortening the relaxation time does not amplify the observable memory tangent. The norm decreases modestly: about 5.0% for sigma8, 6.1% for f sigma8, and 10.5% for linear CMB-lensing convergence between tau H0 = 10 and 1.25.

## Shape stability

Cosine similarity to the tau H0 = 10 tangent remains extremely high for growth observables:

- tau H0 = 1.25: sigma8 cosine = 0.9999920
- tau H0 = 1.25: f sigma8 cosine = 0.9998548
- tau H0 = 1.25: C_L^kk cosine = 0.9917739

The growth response is therefore nearly shape-invariant across the certified tau grid. Lensing changes somewhat more, but remains strongly aligned with the tau10 fingerprint.

The two lensing tangent zero crossings move smoothly across the grid:

- tau H0 = 10: L ~= 595.28 and 1819.16
- tau H0 = 5: L ~= 596.28 and 1813.02
- tau H0 = 2.5: L ~= 598.19 and 1801.11
- tau H0 = 1.25: L ~= 601.98 and 1777.59

These crossing locations are descriptive post-data diagnostics derived from the certified NPZ and are not separate pass/fail gates.

## Precision and derivative controls

All nominal-vs-tight eta-zero differences are at the approximately 7e-10 to 2.2e-9 level with cosine approximately one. Primary-vs-control central derivatives agree far more tightly than preregistered thresholds, with relative errors roughly 1e-4 to 1.5e-3 across all tau values and observables.

The tau10 derivative reproduces the frozen R7a tau10 parent exactly to stored precision for all three observables.

## Licensed interpretation

R8a2 licenses reporting tau dependence of the local observable memory tangent on the tested grid and establishes numerical generality down to tau H0 = 1.25 in the locked stable-AeST setup.

The certified result is that shortening tau from 10 to 1.25 does not produce a larger observable tangent; the response remains of comparable size and its growth shape is almost unchanged. This removes the simple hypothesis that the ACT-amplitude problem can be solved by moving to a shorter relaxation time within this tested interval.

R8a2 does not license monotonic extrapolation below tau H0 = 1.25, an observational detection or bound, a claim that tau10 is globally maximal, or a new lookback decomposition at shorter tau. A separate preregistered follow-up is required for those questions.
