# GE19 Repair40 repair01 local diagnostic runner — lock

## Status

The repaired local Repair40 diagnostic execution path is frozen before the
next attempt.

Runner:

`ge19/run_local_repair40_repair01_piecewise_stage_source_decomposition.sh`.

Runner commit:

`707cb70a8c0cf98a06147930551c841726672f54`.

Runner blob:

`5f811e541457e9911aa35f6e6d5eecaf2cd4e4d6`.

Static runner audit:

- run:
  `35889613193`;
- job:
  `107278466892`;
- conclusion:
  `success`.

## Repair01 implementation binding

Implementation repair commit:

`547b9a5bb897f7d44720358af59d73716b5f7efc`.

Implementation blob:

`b0cd4b29e20339d11cac83a073fb0c662094f891`.

Repair01 implementation lock:

- commit:
  `3130550544c52da1590b4727cc77392556da01c8`;
- blob:
  `11c1cc0634b4452c9b641054ad8cff104dc02323`.

Updated dedicated prelock:

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

## Preserved initial failure

The initial Repair40 cancellation-contaminated closure attempt remains frozen
at:

`docs/ge19_repair40_initial_cancellation_contaminated_closure_fail_freeze.md`.

Its artifacts remain:

- JSON/FULL SHA-256:
  `c6e58996d4637ea9648e367cb5ecdcf891a996875bd8197d54fb6c67fc7d58f7`;
- NPZ SHA-256:
  `bb24dcd5efafdf5bdc9d8df0cd230659b71e177f92a7509f742f19c0ebac22ef`;
- outer runner SHA-256:
  `f2041dd218f8f5e316661c7629f37aee45761334f2ffb38affecb7e804173554`.

That attempt remains IMPLEMENTATION_FAIL and is not relabelled.

## Execution rule

Repair40 repair01 retains every original preregistered gate, including the
Z21 response decomposition closure threshold of `1e-9`.

Only the numerical response extraction changed from subtraction of complete
physical states to direct propagation of source deltas from exact zero delta
p0.

The physical baseline/full/component propagations remain unchanged for the
shift-metric diagnostics and Repair39 reproduction.

A valid Repair40 diagnostic JSON, if emitted, must be frozen exactly as
emitted.

Repair40 remains diagnostic-only and cannot certify Z21 or license lensing.
