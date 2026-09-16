# Stable AeST kSZ R11a Repair01 — response-before-integration (post-data)

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`

## Formal classification

`STABLE_AEST_KSZ_R11A_REPAIR01_RESOLUTION_FAIL`

Repair01 is a diagnostic numerical FAIL. It is not a kSZ detection or null result.

## What Repair01 fixed

Repair01 formed the signed source responses before the oscillatory spherical-Bessel integration and propagated them analytically through the pairwise-velocity ratio.

This successfully removed the two dominant failures of historical R11a:

- D1 -> D2 native-density convergence now passes;
- LINEAR8192 -> PCHIP8192 cross-operator agreement now passes.

At tau/H0 = 10, for example:

- D1 -> D2 LINEAR: `E = 0.0024009`, `C = 0.99999768`;
- D1 -> D2 PCHIP: `E = 0.0005150`, `C = 0.99999988`;
- LINEAR8192 -> PCHIP8192: `E = 0.0035433`, `C = 0.99999372`.

The epsilon stencil also remains stable. Across tau and both interpolation operators, eps=0.025 versus eps=0.05 gives E between about `9e-6` and `1.8e-4`, with cosine essentially one.

The background prefactor derivative is exactly zero at the stored precision: `max_abs_DlnA_per_eta = 0.0`.

The direct eta=0.05 shift agrees with the local linear response at E about `0.0162--0.0164` and C about `0.999875--0.999878`, so the local eta expansion remains healthy.

## Remaining failure: dense-grid resolution

Only R11A-R01-G3 fails.

The 4096-node dense response grid is under-resolved for the oscillatory Bessel transform:

- 4096 -> 8192: `E ~ 0.780`, `C ~ 0.682`.

However, the next refinement is already within the frozen tangent gate:

- 8192 -> 16384: `E ~ 0.03926`, `C ~ 0.99930`

for all tau values and both epsilon values.

Therefore Repair01 strongly localizes the remaining issue to coarse dense-grid resolution, not native CLASS density, eta nonlinearity, interpolation-operator ambiguity, background response, or support mismatch.

The historical R11a native-density failure is not reclassified. Repair01 remains a separate historical FAIL because its preregistered G3 required the 4096 -> 8192 comparison to pass.

## Scientific interpretation

No physical kSZ/pairwise-velocity amplitude is licensed yet because Repair01 classification is FAIL and `science_evaluated=false`.

The appropriate next step is a separately preregistered dense-resolution closure using the same response-before-integration construction, with a finer asymptotic sequence centered above 8192 nodes, e.g. 8192 -> 16384 -> 32768. The existing numerical thresholds must not be relaxed.

If 16384 -> 32768 also passes and the physical eta=0.05 amplitude stabilizes, the pairwise-velocity response can then be certified or closed as observationally unpromising.

No CLASS rerun is needed for this continuation; the existing 25 checkpoints are sufficient.

## Frozen identifiers

- Repair01 preregistration: `608851bff8d4fc8ab063cc338ec0cd102a9f74f8`
- Repair01 implementation: `11f51614a5c5ddecdcb24e898011d0d47df2b7ea`
- Repair01 runner / run head: `d2c1b9d811cdc7344039a015210a675ec7361360`
- Repair01 JSON SHA256: `4fc3612674ae5ae6b2093e9642a3984bf4c7a3dbcd72b6b9eba6d9e664caa239`
- Repair01 NPZ SHA256: `4e655243c9e9216759832583b6057313c7c0ca6823799d3f184371f6153d5199`
- Repair01 science log SHA256: `8e564eabad92a3b1397978eb364dd92dcf245517bc4dfa978071c3b4a447d432`
- Repair01 full runner SHA256: `d4bffa98d6283bd9f162a8cdc4eda42f01087a1cc0acd7304a0eb25e30d2bacf`
- Repair01 environment SHA256: `5906e3da69af5f9764978f62da23af61883e745dccb2ecf4b70dfc7fce9217bf`

Treat this as the authoritative continuation state for the kSZ pairwise-velocity response chain.