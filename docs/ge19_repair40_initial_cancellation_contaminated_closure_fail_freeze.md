# GE19 Repair40 initial execution — cancellation-contaminated Z21 response closure freeze

## Status

The first local Repair40 attempt is frozen as an implementation/reproduction
failure.

It is not a valid Repair40 diagnostic result and no ranking from this attempt
may be promoted as the frozen Repair40 conclusion.

Terminal classification:

`GE19_REPAIR40_PIECEWISE_STAGE_SOURCE_DECOMPOSITION_IMPLEMENTATION_FAIL`.

Terminal route:

`IMPLEMENTATION_FAIL`.

## Frozen artifacts

JSON:

- bytes: `11537`;
- SHA-256:
  `c6e58996d4637ea9648e367cb5ecdcf891a996875bd8197d54fb6c67fc7d58f7`.

NPZ:

- bytes: `21780136`;
- SHA-256:
  `bb24dcd5efafdf5bdc9d8df0cd230659b71e177f92a7509f742f19c0ebac22ef`.

FULL log:

- bytes: `11537`;
- SHA-256:
  `c6e58996d4637ea9648e367cb5ecdcf891a996875bd8197d54fb6c67fc7d58f7`.

Outer runner log:

- bytes: `20423`;
- SHA-256:
  `f2041dd218f8f5e316661c7629f37aee45761334f2ffb38affecb7e804173554`.

Terminal marker:

`GE19_REPAIR40_IMPLEMENTATION_REPRODUCTION_FAIL`.

## Gates

All frozen-input, baseline/full reproduction, nodal identity, stage-source
closure and finiteness gates passed.

The sole false gate was:

`propagated_Z21_response_decomposition_closure_relative_L2_le_1e9`.

Measured closure:

`2.4312527973498394e-07`.

Required preregistered closure:

`1e-9`.

No threshold relaxation is licensed.

## Root cause localization

The implementation formed propagated source responses by subtracting complete
physical states:

`Delta Z_j = Z[S_P + delta_j] - Z[S_P]`.

This is mathematically correct but numerically ill-conditioned in the frozen
Repair40 representation.

From the frozen NPZ:

- ||Z_PCHIP|| is approximately `7.65e11` for each C case;
- ||Z_AKIMA - Z_PCHIP|| is approximately `5.98e3`;
- therefore the desired response is extracted by cancellation of states that
  are about eight orders of magnitude larger than the response;
- machine epsilon times the baseline-state norm is approximately
  `1.7e-4`;
- observed absolute closure defects are approximately `1.1e-3` to
  `1.7e-3`, consistent with accumulated floating-point cancellation in
  repeated baseline subtraction.

The stage-source decomposition itself closes at

`7.050062442856047e-19`,

so the failure is not a source-decomposition identity failure.

PCHIP and full Akima baseline reproduction are both exactly zero relative L2
against the frozen Repair39 outputs, so the failure is not a propagation
binding error.

## Licensed implementation repair

The frozen Repair40 preregistration requires a propagated linear-response
closure. It does not require extracting that linear response by subtracting
two approximately `1e12` physical states.

Repair40 repair01 may therefore compute the same linear response in its
numerically stable form:

- propagate `delta S_A = S_A - S_P` directly;
- propagate every component `delta S_j` directly;
- use zero initial delta canonical state, because projected p0 is frozen and
  identical for all variants;
- reconstruct the delta Z21 state directly from the delta canonical state and
  delta source;
- apply the unchanged preregistered `1e-9` closure gate to
  `Delta Z_A - sum_j Delta Z_j`.

Baseline/full physical propagations remain required for Repair39
reproduction and the nonlinear shift-metric response diagnostics.

No H4 source node, interpolation definition, physical operator, projected
boundary, active mask, science threshold, finite-eta assumption or
observational input may change.

## Claim boundary

Repair40 remains not complete.

The first-run rankings are report-only implementation-failure artifacts until
repair01 passes every preregistered gate.

Z21 remains uncertified and lensing remains blocked.
