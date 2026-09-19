# NL1C7B4 Repair19b1 — local result freeze

## Status

Frozen local WSL result from the first locked Repair19b1 execution.

Terminal classification:

`NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_FEASIBILITY_LSMR_STAGNATION_PASS`

with

`SCIENCE_RC=0`.

Execution HEAD:

`17a7656e361568dd06024d13022331081edb3e7a`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `36865`
  - SHA-256:
    `33774c721bfd15c1c2f6b776408b3fc4623e3720f9199aa04fc43e8415be1a26`
- evaluator log:
  - bytes: `37311`
  - SHA-256:
    `7aee53ebc12e808099cab27992bc62b86eb0c7fff348ce54fe971cb51ec6a3e5`
- local runner log:
  - bytes: `40646`
  - SHA-256:
    `1b2457a8b32ede3a40dc6a6cca715a3affb6d97dea55224ebf983e5ce996e4fa`.

## Gate result

All nine preregistered gates PASS:

- G1 exact frozen provenance
- G2 exact orthonormal basis reproduction
- G3 exact Repair19b orth payload reproduction
- G4 finite direct orth solves
- G5 orth direct residual-space feasibility
- G6 exact gauge satisfaction
- G7 LSMR stagnation identified
- G8 chain conditioning control retained
- G9 claim boundary.

## Direct residual-space feasibility

Across all six canonical scale/grid cases and both direct LAPACK drivers, the unchanged relative linear-feasibility threshold `1e-6` is satisfied.

Maximum direct relative residual:

`1.1984362607786484e-07`.

Representative orthonormal direct residuals:

- scale 5, Nr=256:
  - GELSD: `4.196346283532464e-12`
  - GELSY: `1.5663729951762432e-12`
- scale 5, Nr=512:
  - GELSD: `3.48273712439107e-08`
  - GELSY: `1.7489655116360486e-12`
- scale 10, Nr=256:
  - GELSD: `1.0389389472679538e-10`
  - GELSY: `5.003651006236471e-11`
- scale 10, Nr=512:
  - GELSD: `1.1984362607786484e-07`
  - GELSY: `1.4187698416422544e-10`
- scale 20, Nr=256:
  - GELSD: `5.5409575977125e-11`
  - GELSY: `5.4126764474937896e-11`
- scale 20, Nr=512:
  - GELSD: `2.0056795697491796e-11`
  - GELSY: `1.1499017775154694e-11`.

## LSMR stagnation

Minimum frozen Repair19a LSMR/direct residual ratio over all cases and both direct drivers:

`4833536.02985291`.

The iterative LSMR result was therefore at least 4.8 million times less converged in residual space than the corresponding direct solve.

## Gauge preservation

Every direct orthonormal correction satisfies:

- `|Y4| <= 1e-12`
- `|Qmean| <= 1e-12`.

Observed values are at roundoff scale.

## Numerical rank

Returned rank remains descriptive only.

- Nr=256: both drivers return 508/508 for all three scales.
- Nr=512:
  - scale 5: GELSD 1019/1020, GELSY 1020/1020
  - scale 10: GELSD 1019/1020, GELSY 1020/1020
  - scale 20: both 1020/1020.

This confirms the frozen Repair19b interpretation that numerical rank near the weakest singular direction is cutoff/driver sensitive, while residual-space feasibility is stable.

## Scientific interpretation

Repair19b1 certifies that the same physical `(L,R_t)` correction subspace with exact `Y4=0` and `Qmean=0` admits a direct linear correction in all six canonical cases.

It also certifies that Repair19a's iterative LSMR failure was numerical stagnation, not demonstrated residual-space incompatibility.

This does not certify nonlinear exact B4 closure.

## Licensed continuation

A separately preregistered nonlinear diagnostic may now:

- keep exactly the same physical `(L,R_t)` pair;
- keep the same orthonormal Y4=0/Qmean=0 basis;
- use the same grouped two-point Jacobian;
- use a deterministic direct rank-revealing Gauss-Newton/Newton step;
- evaluate exact nonlinear moving-denominator B4 closure at the historical `1e-7` threshold;
- preserve all nonprojection fields bitwise.

No new physical field, source modification, threshold change, case removal, or finite-eta evolution is licensed by this result.
