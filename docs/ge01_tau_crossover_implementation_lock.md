# GE01 gravitational elastic tau-crossover — implementation lock

## Status

Implementation locked before first GE01 execution.

## Purpose

Map the already certified additive native total-matter state tangent across the analytically derived gravitational Maxwell/Drude crossover.

This is not a new nonlinear solver and does not modify any historical classification.

## Theory provenance

Canonical completion:

`NL0B_COVARIANT_MEMORY_COMPLETION_PASS`.

Canonical interpretation:

- `docs/gravitational_elasticity_canonical_nl0b_interpretation.md`;
- `docs/gravitational_maxwell_viscoelasticity.md`;
- `docs/gravitational_elasticity_timescale_map.md`.

Frozen analytic response:

`K(A)=A/(1+A)`

with

`A^2=tau^2 s(s+3H)`.

For growing modes `s=fH`, the crossover `K=1/2` occurs at

`H tau=1/sqrt[f(f+3)]`.

## Preregistration

Commit:

`ed8e415fdda39ccc5804bfd462a0ec46da8c9bd2`.

File:

`ge01/predata_tau_crossover_native_state.json`.

Blob:

`51f96fd5e1b0308e4e2cd0917ba2b94959658a8d`.

## Implementation

Commit:

`e0f4ffc92605cdd120e820b5cd5d4879cdc7bfa9`.

File:

`ge01/tau_crossover_native_state.py`.

Blob:

`5ba1d624f1219189ec3d4b2fc84692bbbb290032`.

## Frozen tau grid

`tau H0 = {0.1,0.3,0.5,0.7,1.0,3.0,10.0}`.

The historical `tau H0=10` point is retained as the unrelaxed control.

## Frozen tangent control

`lambda={2.5,1.25}`.

For each tau:

`T_lambda=[d_m(+lambda)-d_m(-lambda)]/(2 lambda)`.

No local division by `d_m` or power is used.

## Frozen native window

- `0.03 <= k <= 0.20 h/Mpc`;
- `0.2 <= z <= 1.5`.

Exactly the same additive native-state representation used by the historical v0.77 PASS.

## Frozen numerical configuration

- CLASS commit `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- `KB=0.0665`;
- `p=0`;
- `k_per_decade_for_pk=80`;
- `k_per_decade_for_bao=560`;
- forcing control order 512;
- forcing primary order 1024;
- one OpenMP thread.

## Gates

For every tau require:

- forcing control relative L2 <= `1e-2`;
- forcing cosine >= `0.9999`;
- eta=0 baseline relative L2 across tau <= `1e-12`;
- two-lambda tangent relative L2 <= `5e-3`;
- two-lambda tangent cosine >= `0.9999`;
- all state/tangent values finite.

No monotonic response-amplitude gate is imposed.

The response norm versus tau and cosine to the historical tau=10 tangent are descriptive physics outputs.

## Classification

Full numerical control:

`GE01_GRAVITATIONAL_ELASTIC_TAU_CROSSOVER_PASS`.

Otherwise:

`GE01_GRAVITATIONAL_ELASTIC_TAU_CROSSOVER_FAIL`.

PASS does not establish finite physical eta, nonlinear collapse, likelihood preference or observational detection.

## Anti-tuning

After this lock:

- do not change the tau grid;
- do not add/remove lambda values;
- do not change the native k-z window;
- do not change gates;
- do not select a preferred tau based on the output.

Any later observational/finite-eta tau choice requires a separate preregistration.
