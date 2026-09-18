# NL1C7B4 Repair19 — local result freeze

## Status

Frozen local WSL science result from the first locked Repair19 execution.

Terminal classification:

`NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_FAIL`

with

`SCIENCE_RC=2`.

Execution HEAD:

`a17117f3b8bb28310e262af3c5bdaf3bc0bee9cb`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `67179`
  - SHA-256:
    `ccf4a362f6a8a791f681d565881ff5728520752b1cbd93d72024b0919e1fe879`
- evaluator log:
  - bytes: `67625`
  - SHA-256:
    `37d27b8f6e4db8cfb41bae53f845652db55d8dc315ae0f868746a23a339f8a3b`
- local runner log:
  - bytes: `77655`
  - SHA-256:
    `0c1cdba5645e581a0995557a3e33e6db03705c772df74d42c997ed902c4b7956`.

## Gate result

PASS:

- R19_G1 exact frozen provenance
- R19_G2 exact reduced-basis construction
- R19_G3 unprojected parent reproduction
- R19_G5 second-order correction scaling
- R19_G8 field-freeze invariant
- R19_G9 output artifact integrity
- R19_G10 claim boundary

FAIL:

- R19_G4 canonical gauge-fixed exact nonlinear closure
- R19_G6 two-grid correction-amplitude control
- R19_G7 all-branch exact nonlinear closure.

The result is therefore a science FAIL, not an implementation failure.

## Exact gauge/null-space removal

The fixed reduced basis worked exactly.

Maximum observed gauge residuals across all 24 solves:

- `max |Y4| = 3.970466940254533e-23`
- `max |Qmean| = 3.2004342869314823e-22`.

The reduced-basis audits also pass exactly at both grids:

- Nr=256: shape 510x508, analytic rank 508, `GB_F=0`
- Nr=512: shape 1022x1020, analytic rank 1020, `GB_F=0`.

Thus Repair19 did remove the two certified null directions exactly.

## Parent reproduction

All six lambda=1 unprojected canonical parent cases reproduce frozen Repair16 H/M values with exactly zero reported absolute and relative error.

Therefore Repair19 did not alter the parent state or source evaluator.

## Correction scaling

All six scale/grid paths pass the preregistered second-order scaling gates.

Gated slopes `1/2->1/4` and `1/4->1/8` lie inside `[1.8,2.2]` for every scale/grid pair.

Representative correction norms:

- scale 5, Nr=256:
  `1.54119e-6, 3.94060e-7, 9.96494e-8, 2.50640e-8`
- scale 10, Nr=256:
  `3.27036e-5, 8.74110e-6, 2.25823e-6, 5.73877e-7`
- scale 20, Nr=512:
  `2.44357e-5, 6.11727e-6, 1.53178e-6, 3.83349e-7`.

Thus the computed correction remains perturbatively second order even though the exact nonlinear closure gate fails.

## Canonical closure failure

All 24 canonical solves return SciPy solver success, usually through

`xtol termination condition is satisfied`,

but 0/24 satisfy the exact nonlinear B4 threshold.

At lambda=1:

- scale 5, Nr=256:
  - H `1.0650361033649796e-4`
  - M `2.2928767049196217e-4`
- scale 5, Nr=512:
  - H `2.7584061094410193e-5`
  - M `3.5817030807427957e-4`
- scale 10, Nr=256:
  - H `2.3601537219886345e-3`
  - M `8.453087332391951e-5`
- scale 10, Nr=512:
  - H `6.073828216988423e-4`
  - M `3.407225345404231e-4`
- scale 20, Nr=256:
  - H `3.8089524872516665e-3`
  - M `1.2560168748093242e-5`
- scale 20, Nr=512:
  - H `1.3531140380919745e-3`
  - M `2.619680346714823e-5`.

These are all above the frozen `1e-7` threshold.

## Solver-stagnation signature

Although every canonical run reports solver success, the reported first-order optimality remains extremely large.

Examples:

- scale 5, Nr=256, lambda=1:
  `1.1474587839637026e8`
- scale 10, Nr=512, lambda=1:
  `1.1222059115426652e9`
- scale 20, Nr=256, lambda=1:
  `1.0307441238161587e5`.

At smaller lambda some optimalities rise into the `1e11-1e12` range.

Therefore SciPy success here is an xtol/stagnation termination, not a small-gradient nonlinear optimum.

## Lambda behavior

The physical correction norm scales approximately as lambda^2.

However the exact nonlinear normalized momentum residual often worsens as lambda decreases.

For scale 5, Nr=256:

- lambda 1: M `2.2929e-4`
- lambda 1/2: M `2.2749e-4`
- lambda 1/4: M `2.5959e-3`
- lambda 1/8: M `1.1070e-2`.

This behavior is incompatible with interpreting the current nonlinear-solver output as a converged exact constraint projection.

## Two-grid control

At lambda=1:

- scale 5 correction ratio: `1.7608373975715634` PASS
- scale 10: `1.975426804471894` PASS
- scale 20: `2.2539550097058085` FAIL.

## All-branch retest

0/54 historical lambda=1 Y/beta cases pass the unchanged exact nonlinear threshold.

Within a fixed scale/grid state, the reported H/M values are essentially independent of Y-kind and beta, so the branch choice is not the source of the failure.

## Output rule

No official Repair19 NPZ was written.

This is the correct behavior because the science gates failed.

## Interpretation

Repair19 establishes that:

1. the certified Y4/Qmean null freedom can be removed exactly;
2. the required correction remains cleanly second order;
3. the historical exact nonlinear constraints still do not close under the locked nonlinear least-squares implementation;
4. the solver terminates by coordinate-step stagnation with large optimality, so the result does not establish non-existence of a gauge-fixed nonlinear completion.

The next step must distinguish reduced-coordinate conditioning / finite-difference solver stagnation from genuine insufficiency of the physical `(L,R_t)` projection ansatz.

## Licensed continuation

A separately preregistered diagnostic may compare the frozen Repair19 chain reduced basis with an orthonormal basis spanning exactly the same Y4=0/Qmean=0 subspace.

It may audit:

- basis condition numbers;
- reduced Jacobian rank/condition;
- sparse/grouped versus dense finite-difference reduced Jacobians;
- linearized residual feasibility in both coordinate systems;
- deterministic exact nonlinear alpha probes along the linearized correction.

No new physical field, threshold, source, coefficient, sign, eta value, branch-specific solve, or state artifact may be introduced by that diagnostic.
