# NL1C7B4 Repair13 — local result freeze

## Status

Frozen local WSL result for the preregistered Repair13 Hamiltonian first-order source localization.

Terminal classification:

`NL1C7B4_REPAIR13_IMPLEMENTATION_FAIL`

with `SCIENCE_RC=2`.

This is an implementation/harness failure, not a science classification and not an official GitHub Actions run.

## Execution provenance

- execution HEAD: `c92edf5d88c050052f6c25b3670ed74eefd968cc`;
- Repair13 preregistration commit: `f2bd2d3b693d41680e254d714aec1233502e3ce0`;
- Repair13 implementation commit: `df3250a70c37303bde723688e87a071f42b2d380`;
- Repair13 implementation-lock commit: `49ce63ee685d7ef2c80270ca5881444de78b5fc4`;
- Repair12 result-freeze commit: `167af8e7b6d610c307b67fed7890fe0547c27bfa`;
- Repair12 JSON SHA-256: `99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c`.

## Frozen local output hashes

The local Repair13 output is preserved as produced and must not be relabeled.

Observed terminal gates:

- G1 frozen provenance: PASS
- G2 exact Repair12 lambda=1 reproduction: PASS
- G3 per-source bookkeeping closure: FAIL
- G4 first-order coefficient closure: FAIL
- G5 projection closure: FAIL
- G6 complete source localization: PASS
- G7 Repair12 order reproduction: PASS
- G8 claim boundary: PASS

The failing gates used fixed normalized tolerances of `1e-12`.

Observed maxima:

- source-sum normalized closure error: `1.209853523675103e-10`;
- coefficient-sum normalized closure error: `1.209853523675103e-10`;
- projection-sum error: `4.28834745491713e-12`.

These failures occur when two algebraically equivalent floating-point association orders are compared after subtraction of large, nearly cancelling background contributions.

## Non-gating diagnostic signal

Although Repair13 did not certify, its non-gating localization output is preserved:

- all 54 cases were present;
- all 11 source labels were present;
- Repair12 total Hamiltonian slopes were reproduced exactly;
- `AeST_E2` was the largest first-order coefficient by L2 norm in 54/54 cases;
- `AeST_EX` was second in the representative scale/grid cases;
- `AeST_E2` was labelled `first_order_like` in 54/54 cases;
- `AeST_EX` was labelled `first_order_like` in 54/54 cases;
- `AeST_X2` was labelled `second_order_like` in 54/54 cases.

This signal is **not certified by Repair13** because G3-G5 failed.

Representative Simple, beta=1 results at lambda=1/8:

- scale 5, Nr=256:
  - E2 projection fraction `0.9895615869454023`;
  - EX projection fraction `0.010054552164260159`;
- scale 10, Nr=256:
  - E2 projection fraction `0.9893265464944163`;
  - EX projection fraction `0.009976617813575317`;
- scale 20, Nr=256:
  - E2 projection fraction `0.988941473907316`;
  - EX projection fraction `0.010026211240311913`.

No physical conclusion is licensed from these values until a separately preregistered harness repair certifies the decomposition.

## Diagnosis of the harness failure

For each radial point, Repair13 compared two mathematically identical expressions evaluated with different floating-point association:

`sum_i [C_i(lambda)-C_i(0)]`

against

`[sum_i C_i(lambda)]-[sum_i C_i(0)]`.

When the background source sums are much larger than the perturbative increment, dividing the tiny difference between these two floating-point paths by the tiny perturbative residual produces a cancellation-amplified relative error.

The same issue propagates to

`sum_i A_i(lambda)=A_tot(lambda)`

and to the projection-sum identity.

Repair13a may repair only this numerical closure certification. It may not change any source array, state, amplitude, source-order label, slope, projection definition, dominant-source definition, or physical threshold.

## Licensed next step

A harness-only Repair13a may replace G3-G5 by condition-aware IEEE-754 forward-error checks whose scale is determined from the actual magnitudes and operation counts of the frozen source sums.

The old Repair13 normalized errors and failed gates must remain reported.

No empirical tolerance may be selected from the observed `1.2098e-10` or `4.2883e-12` values.
