# Stable AeST cosmic-memory R7 — lookback decomposition post-data checkpoint

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Frozen preregistration

R7 was preregistered before the run in commit

`5d4c514799f22fe13cc0ecf9a0be4d3e2326a514`.

The implementation/audit checkpoint before the first R7 result was

`b94071d1c85ec99522359ecb6397fd755cc0d52a`.

The frozen scientific parents were:

- R2e post-data: `c0fe57f73a7785c21b1fecd7455f19148d5f812d`;
- R5b post-data: `3242335ece23fbeb743f075a1df1aa70acaab211`;
- R6a post-data: `540f8f85c618209abb509e3c9c7dc188698d8e25`.

All historical classifications remain unchanged.

## Formal R7 result

The completed run returned

`STABLE_AEST_COSMIC_MEMORY_R7_PHYSICAL_BRIDGE_FAIL`

with exit code 1.

The preregistered gates were:

- R7-G1 provenance and parent lock: PASS;
- R7-G2 single-hook + full-history source topology: PASS;
- R7-G3 trace and epoch-partition integrity: PASS;
- R7-G4 full-replay amplifier consistency: PASS;
- R7-G5 physical derivative bridge: FAIL;
- R7-G6 epoch reconstruction: PASS.

Therefore the lookback decomposition is **not certified**, and the measured epoch fractions are not licensed as physical model results.

## Provenance and source topology

The disposable R7 source was rebuilt from the frozen CLASS parent

`e85808324f51fc694d12e3ed7439552a3c3f9540`.

The final source audit found exactly:

- one physical eta multiplier;
- one physical memory closure;
- one R2d full-history trace call;
- one corrected R2e external replay hook;
- one runtime external-force helper;
- stable `chi = Q s` dynamics retained.

All 12 replay runs were finite and had positive required observable domains.

The R7 eta-zero baseline reproduced the frozen R5b eta-zero observables exactly at stored precision for `sigma8`, `effective_f_sigma8`, and linear `C_L^{kappa kappa}`. Thus the failed physical bridge is not caused by a changed background cosmology, output setup, or baseline observable normalization.

## Trace and partition integrity

The raw full-history trace contained

- 12,712,153 rows;
- 7,507,485 normalized unique `(k,tau)` rows;
- 686 k values;
- conformal-time support from approximately `0.0206423` to `14151.6266` Mpc.

The same-run background covered the full trace support. Every normalized row was assigned to exactly one preregistered redshift epoch, and the four epoch tables reconstructed the normalized full forcing row by row with zero stored reconstruction error.

The epoch-force L2 norms were strongly late weighted:

- ancient (`z >= 10`): `1.1055294419073046e-4`;
- intermediate (`2 <= z < 10`): `0.7640302766990238`;
- recent structure (`0.5 <= z < 2`): `40.965757846370735`;
- late (`z < 0.5`): `162.25062879550015`.

These force norms are diagnostic properties of the normalized replay table, not certified physical epoch fractions.

A notable transport diagnostic is

`max_duplicate_relative_spread = 1.251599599059765`

when repeated adaptive-RHS samples at identical stored `(k,tau)` values are collapsed to a single replay value. This quantity was reported but was not a preregistered R7 gate.

## Full-replay internal consistency

The full-history replay itself was stable under the preregistered lambda change from 30 to 10:

- `C_L^{kappa kappa}`: relative L2 `2.6791e-6`, cosine `0.999999999998`;
- `f sigma8`: relative L2 `0.0340113`, cosine `0.9995533270`;
- `sigma8`: relative L2 `0.0249055`, cosine `0.9996938634`.

Thus R7-G4 passed for all three observables.

## Failed physical derivative bridge

The corrected full-history lambda=30 replay tangent was compared with the frozen direct-physical R5b eta=0.01 derivative-at-zero tangent.

The bridge metrics were:

- `C_L^{kappa kappa}`: relative L2 `0.0076147051`, cosine `0.9999781660` — within the preregistered bridge bound;
- `sigma8`: relative L2 `0.0485811935`, cosine `0.9988246087` — within the preregistered bridge bound;
- `f sigma8`: relative L2 `0.2569048202`, cosine `0.9680171406` — fails both preregistered bridge conditions.

Therefore R7-G5 failed and determines the formal classification.

The failure is concentrated in the late-time `f sigma8` response. Elementwise, the replay/physical tangent ratio is approximately

- z=0.2: `1.3623`;
- z=0.5: `0.8086`;
- z=1.0: `1.0451`;
- z=1.5: `0.9605`;
- z=2.0: `0.9897`.

This pattern is consistent with a small redshift-dependent replay distortion being amplified by the effective growth-rate derivative, but R7 alone does not identify a unique cause.

## Epoch reconstruction

Despite the failed physical bridge, the four epoch replay tangents reconstruct the full replay tangent accurately:

- `C_L^{kappa kappa}`: relative L2 `8.1306e-6`, cosine `0.999999999983`;
- `f sigma8`: relative L2 `0.00555723`, cosine `0.9999990037`;
- `sigma8`: relative L2 `0.00806158`, cosine `0.9999817442`.

Thus the partition/reconstruction algebra is internally consistent. The failure is specifically the normalization/shape bridge from the replay representation to the direct physical observable derivative.

## Diagnostic-only epoch pattern

Because R7-G5 failed, the following values are **not licensed for publication as physical epoch fractions**. They are retained only as a directional diagnostic for the follow-up design.

For the full-vector signed projection metric, the replay decomposition suggests:

- `sigma8`: ancient `0.00376`, intermediate `0.1852`, recent structure `0.7390`, late `0.0774`;
- `f sigma8`: ancient `0.00146`, intermediate `0.0956`, recent structure `0.6657`, late `0.2426`;
- lensing `C_L^{kappa kappa}`: ancient `-0.00365`, intermediate `-0.17295`, recent structure `0.28895`, late `0.88764`.

The lensing diagnostic therefore contains cancellation between intermediate/high-redshift and late contributions. Again, these are replay diagnostics only, not certified physical lookback fractions.

## Interpretation

R7 establishes two useful facts while remaining a formal FAIL:

1. the four-window decomposition and reconstruction machinery is numerically coherent;
2. the frozen full-history table replay is not sufficiently faithful to the direct physical derivative for `effective_f_sigma8` under the preregistered bridge criterion.

A plausible numerical mechanism is the compression of repeated adaptive ODE RHS evaluations at identical stored `(k,tau)` coordinates into a single averaged forcing value. The observed maximum duplicate spread is large enough that this must be tested explicitly, but it is not retrospectively promoted to the certified cause of the R7 failure.

The correct next step is not to loosen R7 thresholds or re-run the same table-replay construction. A new preregistered test should remove force-table transport entirely and compute the epoch derivatives directly from the physical memory feedback at eta=0.
