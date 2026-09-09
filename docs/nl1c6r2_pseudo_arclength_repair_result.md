# NL1C6R2 result — pseudo-arclength continuation repair

## Status

GitHub Actions run: `34351229257`

Head commit: `d40679fbafa8b608e20a56bf521b028fa3ce6367`

Artifact: `results_bundle_nl1c6r2_pseudo_arclength_repair`

Artifact ID: `10108738796`

Artifact SHA-256: `74fd5007cb12413baf1011de155b23437f3bbd1db140bfbd472af6a81c47d9cb`

Final preregistered classification:

```text
NL1C6R2_FULL_J_BARYONIC_RECLOSURE_FAIL
```

The workflow completed successfully and produced the expected JSON, NPZ, stdout log, predata declaration, and solver source. This is therefore a scientific/numerical FAIL under the frozen NL1C6R2 gates, not a CI or packaging failure.

## Frozen controls

The run retained the NL1C5B baryon source, the NL1C6 full-J equations, the three interpolation families, beta0 in `{0.1,0.5,1.0}`, the periodic physical-coordinate box, and all original physical acceptance gates. No physical eta, memory forcing, matter re-evolution, observational data, or likelihood was evaluated.

The NL1C5B input identity gate passed exactly. The high-gradient regression also passed for every beta0 and every evaluation snapshot, with

```text
max high-gradient regression error = 1.5679255329173794e-14
```

so the previously validated sign, normalization, source convention, and large-gradient reduction remain intact.

## Gate outcome

```text
G1_input_identity                  PASS
G2_high_gradient_regression        PASS
G3_all_primary_solutions_converged FAIL
G3_all_finite                      FAIL
G3_R1 <= 1e-10                     FAIL
G3_R2 <= 1e-8                      FAIL
G4_resolution <= 5e-3             FAIL
G5_no_distinct_residual_valid_root PASS
```

The zero values written to the aggregate R1/R2/resolution metrics are empty-result placeholders because no primary physical `lambda=1` solution was obtained. They must not be interpreted as successful residual or resolution measurements.

## Pseudo-arclength outcome

All nine co-primary branches failed on the first native snapshot, `z = 6.000000000000045`, before a physical `lambda=1` crossing was reached.

| interpolation | beta0 | largest positive lambda reached | smallest lambda visited | accepted arclength points | final failure |
|---|---:|---:|---:|---:|---|
| simple | 0.1 | 2.8398727e-7 | 5.8207661e-11 | 44 | augmented line search failed |
| simple | 0.5 | 3.3790560e-7 | -1.6940836e-7 | 69 | augmented line search failed |
| simple | 1.0 | 6.8082803e-7 | -4.2645645e-7 | 30 | augmented line search failed |
| exponential | 0.1 | 2.8422787e-7 | -1.0126479e-7 | 36 | augmented line search failed |
| exponential | 0.5 | 4.2105727e-7 | 5.8207661e-11 | 11 | augmented GMRES failed at 400 iterations |
| exponential | 1.0 | 6.8010290e-7 | -4.2621943e-7 | 30 | augmented line search failed |
| sharp | 0.1 | 2.8403465e-7 | -1.3075324e-7 | 87 | augmented line search failed |
| sharp | 0.5 | 3.8825101e-7 | 5.8207661e-11 | 26 | augmented GMRES failed at 400 iterations |
| sharp | 1.0 | 6.7956957e-7 | -4.2598218e-7 | 112 | augmented line search failed |

The continuation therefore entered the zero-source-connected nonlinear branch and, for several branches, explicitly traversed a fold far enough for lambda to reverse sign. However, the augmented corrector became numerically singular/stiff at arclength steps of order `1e-10` before any subsequent continuation could approach `lambda=1`.

The final solver-relative residual reported at termination is approximately `2.0e-10` on all nine branches, close to the frozen augmented tolerance, but no exact physical-source state exists in the result bundle because the continuation never reached `lambda=1`.

## Interpretation

NL1C6R2 confirms that the NL1C6/NL1C6R failure was not merely caused by using lambda as a monotone continuation coordinate: pseudo-arclength does follow the connected branch through an initial fold. It nevertheless encounters a much more severe near-singular regime at source amplitudes of only a few times `1e-7`.

Under the preregistered rules this remains a numerical continuation result. It is not evidence that the physical full-J field equations have no `lambda=1` solution, and it is not a residual-valid multibranch result. The physical `lambda=1` trajectory required for the eta=0 retarded-memory test has therefore not been established.

## Consequence

Per the NL1C6R2 predata declaration, NL1C7 must not be started from this result. Any further attempt must be separately preregistered and must preserve the same physical equations, source, interpolation branches, and physical gates while changing only the numerical continuation/globalization strategy.