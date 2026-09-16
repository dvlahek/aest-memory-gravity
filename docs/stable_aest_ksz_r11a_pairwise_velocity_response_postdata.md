# Stable AeST kSZ R11a — theory-only pairwise velocity response (post-data)

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`

## Formal classification

`STABLE_AEST_KSZ_R11A_NATIVE_DENSITY_FAIL`

R11a is a diagnostic numerical FAIL, not an observational kSZ null result.

## Frozen parent chain

- R11a prefit: `a34c4d13738383c670222472b3af8ab4e1802fdf`
- R11a implementation: `44a65aea8f671a0af7534447c31f415a6c9d314c`
- R11a runner / run head: `8868dc344b83f69f7429b507e750450c724ddd63`
- R9b2k postdata: `dd3981b2fd838fb24a997af77f913c3d5dd8d07b`
- R9b2k Repair02 postdata: `d3fd6191d55f4e74aa8666f842dae64bd8aee09b`
- R10a postdata: `b7da648f1810ea0c047b6e511e3f87211e830329`

All 25 saved R9b2k checkpoints were found and validated. The frozen native grids remain D1 = 864 nodes and D2 = 1729 nodes, both above the historical 108-node grid.

## Gate result

Passed:

- R11A-G1 provenance/checkpoints
- R11A-G2 baseline physicality and eta-zero tau invariance
- R11A-G3 baseline Simpson/trapezoid agreement
- R11A-G4 epsilon consistency
- R11A-G7 local eta=0.05 linearity

Failed:

- R11A-G5 native-density convergence
- R11A-G6 cross-quadrature tangent agreement

Therefore the pairwise-velocity tangent is not numerically certified in the current native-grid integration form.

## What is healthy

The eta-zero pairwise velocity is numerically stable. Across the frozen tau grid, the Simpson and trapezoid baseline vectors agree at approximately

- `E = 0.00132014`
- `C = 0.999999157`.

The eta-zero baseline is also tau-invariant to approximately `1.45e-9` pointwise relative error.

The physical pairwise-velocity range over the frozen 40--200 Mpc/h and six-redshift grid is roughly `-69.3` to `-1.89 km/s` for Simpson, with finite `1 + xi` everywhere.

The eta stencil itself is locally stable inside each integration operator. For every tau, `eps=0.025` versus `eps=0.05` gives E of order `1e-6` to `1e-5` and cosine indistinguishable from unity. The direct eta=0.05 shift also agrees with the local linear prediction at E about `0.0017` and C about `0.9999999`.

## Failure localization

The small signed tangent is not robust to the numerical representation of the oscillatory Bessel integrals.

At tau H0 = 10, D1 -> D2 tangent convergence fails strongly:

- Simpson: `E ~ 0.604`, `C ~ 0.799`
- trapezoid: `E ~ 0.834`, `C ~ 0.644`.

At D2, Simpson versus trapezoid tangent agreement also fails for every tau and both epsilon values:

- `E ~ 0.289`
- `C ~ 0.958`.

By contrast, the eta-zero integrals themselves are stable. This localizes the problem to extracting a tiny signed response from an oscillatory pairwise-velocity integral on the native k grids, not to baseline pairwise velocity, eta nonlinearity, tau instability, or checkpoint provenance.

This is closely analogous in numerical character to the earlier DESI signed-response problem: subtracting or comparing nearly equal integrated quantities is substantially less stable than forming the response before integration.

## Provisional amplitude diagnostic — NOT CERTIFIED SCIENCE

The uncertified direct D2/Simpson diagnostic gives, for physical eta = 0.05:

- maximum fractional shift about `5.4e-5` to `5.7e-5` across tau;
- RMS fractional shift about `8.9e-6` to `9.3e-6`;
- maximum absolute velocity shift below `8.4e-4 km/s`, i.e. below about `0.84 m/s`;
- the largest fractional shift occurs near `z = 0.29536`, `r = 180 Mpc/h`.

These values are recorded only to quantify the scale seen by the failed estimator. They are not licensed as a physical AeST prediction until the response integral passes density and operator convergence.

The tau dependence of the failed-estimator tangent is nevertheless highly coherent: relative norm ratios to tau10 are approximately 0.993, 0.978, and 0.951 for tau = 5, 2.5, and 1.25, with cosines above 0.999997.

## Scientific interpretation

R11a does **not** establish a kSZ detection, kSZ null, eta bound, or pairwise-velocity constraint.

What R11a does establish is that the baseline linear pairwise-velocity construction is healthy, while the tiny AeST derivative is under-resolved by direct native-grid oscillatory integration. The next permitted numerical step is a separately preregistered response-before-integration repair.

A suitable repair should form signed central responses of the relevant source spectra (`P_dd` and the sign-preserving density-velocity cross spectrum) before the spherical-Bessel integration, interpolate the signed response itself on a dense bounded log-k grid, and then evaluate the derivative of the pairwise-velocity ratio. No smoothing, clipping, extrapolation, post-data scale selection, or gate relaxation is permitted.

Only after such a repair passes density and operator robustness may the physical eta=0.05 amplitude be used to decide if an observational R11b kSZ likelihood is worthwhile.

## Frozen artifact hashes

- R11a JSON SHA256: `a868dbbb6b5b08bf54139abf9d3a288d52bee501f23cc4b61f9422f9fb2d98ab`
- R11a NPZ SHA256: `4c48329839af71f30f56f2b54b48de5cbf8cef395cee105b4fa2fd378ad39b08`
- R11a science log SHA256: `ff9a4e30234485e58ae65974bce4024ba8280127d74e1bed319e883d93366691`
