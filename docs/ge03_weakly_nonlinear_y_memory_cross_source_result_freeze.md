# GE03 weakly nonlinear Y-memory cross-source — result freeze

## Status

Frozen first science-reaching GE03 execution after the two implementation-only repairs.

Terminal classification:

`GE03_WEAKLY_NONLINEAR_Y_MEMORY_CROSS_SOURCE_FAIL`.

GitHub Actions run:

`35472721120`.

Execution HEAD:

`3cf032278f424a0b435980b5b4ff70c6152b04cd`.

The workflow science step completed successfully and produced the frozen GE03 JSON/NPZ outputs.

This is a scientific/numerical FAIL under the preregistered GE03 gates.

It is not an implementation failure.

## Artifact

Artifact ID:

`10593516123`.

Artifact name:

`results_bundle_ge03_weakly_nonlinear_y_memory_cross_source`.

Artifact ZIP SHA-256:

`295f1769c68b7bbb2ee6a36bb0b326efb7af4b932c03f610bbee183fc78a84ef`.

## Frozen output hashes

Result JSON:

- bytes: `12485`;
- SHA-256:
  `9cd1925ea8d0933f1b4bb35da5fd7a338360e74bb3fa7023dacf612d4e99b028`.

Result log:

- bytes: `12485`;
- SHA-256:
  `9cd1925ea8d0933f1b4bb35da5fd7a338360e74bb3fa7023dacf612d4e99b028`.

Result NPZ:

- bytes: `70734`;
- SHA-256:
  `c3231ade48b1af6e781447c608356c052a1e9c42f44f825a06866973d455fafb`.

Artifact metadata JSON:

- bytes: `835`;
- SHA-256:
  `78fc8a9c0f80359e3910525bd40596b6620fb9eadae2e79d6dfa4b77e0e9feac`.

## Gate result

PASS:

- exact retained artifact provenance;
- requested-k matching;
- common native-grid matching;
- at least eight native evaluation times;
- four-lambda `chi11` affinity;
- analytic versus finite-difference `DY2`;
- primary versus control finite-difference stability;
- exact beta0 scaling;
- finite outputs;
- no finite-eta or observational input.

FAIL:

- `Nx256` versus `Nx512` low-mode `DY2` convergence.

Frozen limit:

`5e-4`.

Observed maximum:

`1.1665436252484428e-3`.

Therefore GE03 remains FAIL.

The convergence threshold is not relaxed.

## Strong operator identities that nevertheless passed

The four-lambda retained-trace tangent is exceptionally stable:

- maximum relative-L2 spread:
  `8.775428679463291e-5`;
- minimum cosine:
  `0.999999996810412`.

The exact NL1B2 directional derivative agrees with centered finite differences of the already certified NL1A nonlinear operator at

`3.62253428109363e-11`

maximum relative L2 error.

Changing the finite-difference direction step from the frozen primary `1e-4` to control `3e-5` changes the finite-difference result by at most

`1.238686555448628e-10`.

The beta0 scaling error is

`2.4424906541753446e-16`.

Thus the GE03 failure is not caused by a wrong directional derivative identity, lambda nonlinearity, finite-difference step selection or beta0 implementation.

## Resolution pattern

The failing low-mode discrepancy is nearly independent of redshift and beta0.

Across the eight native times the Nx256 versus Nx512 low-mode relative errors remain approximately

`1.16650e-3 -- 1.16654e-3`.

The same value appears for all three co-primary beta0 branches at each time.

This strongly localizes the failure to the spatial representation/convergence of the nonanalytic `|grad chi|` cross-source rather than to time evolution or beta scaling.

This observation is descriptive and does not alter the FAIL classification.

## Physical cross-source signal

Despite the numerical convergence FAIL, the source geometry is highly coherent.

For beta0=1, the ratio

`||2 DY2|| / ||2 Y2||`

per unit eta tangent increases monotonically over the frozen native window:

- z=1.38524: `0.0148315`;
- z=1.16117: `0.0200519`;
- z=0.95756: `0.0269693`;
- z=0.77247: `0.0361080`;
- z=0.60419: `0.0481425`;
- z=0.45116: `0.0639468`;
- z=0.31201: `0.0846777`;
- z=0.24762: `0.0972675`.

The cosine between `Y2` and `DY2` is negative and extremely close to -1 at every native time, from approximately

`-0.999999973`

to

`-0.999999999`.

Thus the retained memory tangent points almost exactly opposite to the baseline leading Y-sector nonlinear source on this frozen reference.

This is a descriptive physical pattern only because the spatial-convergence gate failed.

## Scientific interpretation

GE03 establishes two things simultaneously:

1. the NL1B2 analytic cross-source identity is implemented correctly and is numerically differentiable to near machine precision;
2. the preregistered 256/512 spatial pair is not sufficiently converged under the strict `5e-4` low-mode gate for the nonanalytic `|grad chi|` cross-source.

The second point prevents a GE03 PASS.

The nearly constant convergence discrepancy is consistent with a representation error associated with the cusp/nonanalyticity of `|grad chi|`, but that cause is not yet certified.

## Project boundary

Do not:

- relax the GE03 convergence gate;
- relabel GE03 as PASS;
- replace the failed 256/512 gate by a post-hoc 512/1024 gate inside GE03;
- infer the sign of a solved `Z21` state from the source cosine alone;
- introduce finite eta.

A scientifically distinct follow-up may characterize the spectral convergence of the same frozen cross-source over a preregistered resolution ladder.

Such a study may determine if the `1.1665e-3` discrepancy converges regularly and may identify an adequate representation for the later N2 state solve.

It cannot retroactively change the GE03 classification.
