# GE19 Repair40 repair01 direct-delta closure — implementation lock

## Status

Repair40 repair01 is frozen before its first local execution.

Repair01 changes only the numerical extraction of the propagated Z21
representation response used by the preregistered linear-response closure
and Z21-response ranking.

No Repair40 threshold, source decomposition, physical source node, H4
operator, projected p0, active mask, interpolation definition, Radau tableau,
finite-eta assumption or observational input is changed.

## Initial Repair40 implementation failure

Freeze file:

`docs/ge19_repair40_initial_cancellation_contaminated_closure_fail_freeze.md`.

Freeze blob:

`9542709fed99f72414e2154aaeeeae56051c595b`.

Frozen failed artifacts:

- JSON/FULL SHA-256:
  `c6e58996d4637ea9648e367cb5ecdcf891a996875bd8197d54fb6c67fc7d58f7`;
- NPZ SHA-256:
  `bb24dcd5efafdf5bdc9d8df0cd230659b71e177f92a7509f742f19c0ebac22ef`;
- outer runner SHA-256:
  `f2041dd218f8f5e316661c7629f37aee45761334f2ffb38affecb7e804173554`.

The sole false gate was the propagated Z21 response decomposition closure:

`2.4312527973498394e-07 > 1e-9`.

The preregistered `1e-9` threshold is unchanged.

## Root cause

The original implementation extracted every propagated representation
response as a subtraction of full physical states:

`Delta Z = Z[S_P + delta S] - Z[S_P]`.

The frozen NPZ shows ||Z|| approximately `7.65e11` while the desired
response norm is only approximately `6e3`.

The response extraction is therefore ill-conditioned by roughly eight
orders of magnitude and the observed closure defect is consistent with
floating-point cancellation.

The stage-source decomposition itself closes at
`7.050062442856047e-19`, and baseline/full Repair39 reproduction is exact.

## Repaired implementation

File:

`ge19/repair40_piecewise_stage_source_decomposition.py`.

Repair01 commit:

`547b9a5bb897f7d44720358af59d73716b5f7efc`.

Repair01 blob:

`b0cd4b29e20339d11cac83a073fb0c662094f891`.

Repair01 propagates the same linear responses directly:

- full response source:
  `delta S_A = S_A - S_P`;
- component response source:
  `delta S_j`;
- initial delta canonical state:
  exactly zero, because projected p0 is frozen and identical for every
  baseline/full/component representation;
- endpoint-safe factor-4 Repair38 Radau propagation is unchanged;
- reconstructed delta Z21 is obtained directly from the delta canonical
  state and delta source.

The preregistered closure is then evaluated on

`Delta Z_A - sum_j Delta Z_j`

without subtracting approximately `1e12` physical baseline states.

Full physical baseline/component propagations remain unchanged and continue
to provide the nonlinear shift-metric differences.

## Audits

Static implementation audit:

- run:
  `35889439831`;
- conclusion:
  `success`.

Updated dedicated Repair40 prelock:

- workflow commit:
  `3ed249d33c06e21502be6fe5b9be0a28e9e10550`;
- workflow blob:
  `de7fcb70fd6b947881c8c66a00454152e3fc8c91`;
- run:
  `35889464378`;
- job:
  `107277958852`;
- conclusion:
  `success`.

The prelock explicitly verifies:

- zero delta p0;
- direct full and component source deltas;
- factor-4 endpoint-safe Repair38 propagation;
- absence of full-state subtraction in the Z21 response extraction;
- unchanged preregistered closure gate and claim boundary.

## Claim boundary

Repair40 repair01 remains diagnostic-only.

The initial Repair40 attempt remains an implementation failure and is not
relabelled.

Repair40 becomes a valid diagnostic result only if repair01 passes every
original preregistered gate.

Z21 remains uncertified and lensing remains blocked.
