# NL1C7B4 Repair19a — local result freeze

## Status

Frozen local WSL diagnostic result from the first locked Repair19a execution.

Terminal classification:

`NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_INFEASIBILITY`

with

`SCIENCE_RC=2`.

Execution HEAD:

`0412b48a777b56fcc1c710538745a2badaac4b5d`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `22475`
  - SHA-256:
    `b9b79d1fe12dff7b59d80260572129b746322412bf96ff214204f9651bd77761`
- evaluator log:
  - bytes: `22921`
  - SHA-256:
    `96e0447b3cdd7db252614164cdb56fa89f6a468b80b65d568a64b6084d0d7c83`
- local runner log:
  - bytes: `30896`
  - SHA-256:
    `ec3a4b808ca37ff0e59e90e5b929b80763b405955195edde7c644fcd90354222`.

## Gate result

PASS:

- R19A_G1 exact frozen provenance
- R19A_G2 exact same constrained subspace
- R19A_G3 exact parent reproduction
- R19A_G4 finite Jacobian and linear probes
- R19A_G7 complete nonlinear alpha probe
- R19A_G8 claim boundary

FAIL:

- R19A_G5 gauge-fixed linear feasibility
- R19A_G6 physical-coordinate agreement.

The preregistered terminal class is therefore

`NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_INFEASIBILITY`.

## Basis result

The same Y4=0 / Qmean=0 physical subspace was represented by two coordinate bases.

Chain basis:

- Nr=256 condition number:
  `162.33598862000716`
- Nr=512:
  `325.3116790240505`.

Orthonormal Helmert basis:

- condition number:
  `1.0`
at both grids;
- gauge-constraint residuals and orthonormality errors are at approximately `1e-15`.

Thus the basis-coordinate conditioning difference is real.

## Iterative linear-solve result

However, neither coordinate system reaches the preregistered linear-feasibility threshold.

All 12 LSMR solves terminate with:

- `istop=7`
- `iterations=10000`.

The retained relative residuals are large.

Orth basis:

- scale 5, Nr=256: `0.3901230126403223`
- scale 5, Nr=512: `0.4933288207030169`
- scale 10, Nr=256: `0.5117097753920875`
- scale 10, Nr=512: `0.5792684845955796`
- scale 20, Nr=256: `0.3853222147419097`
- scale 20, Nr=512: `0.5471984348568231`.

Chain basis residuals are similarly large, with maximum

`0.7091532488556874`.

The physical corrections produced by the two unfinished iterative solves differ by order unity:

- maximum relative difference:
  `1.122367467853596`.

## Relation to frozen Repair18b1/Repair18c

This terminal class must be interpreted together with the earlier certified dense-Jacobian results.

Repair18b1 established for all three Nr=256 scale cases that:

- grouped sparse and dense two-point Jacobians agree to the frozen fidelity test;
- the full Jacobian has rank 508/510;
- dense bounded linear least squares drives the linearized residual essentially to zero with no active bounds.

Repair18c then measured parent-residual projection onto the two left-null directions:

- scale 5: `9.707232843664437e-11`
- scale 10: `2.1911761962074124e-10`
- scale 20: `1.6006841801170347e-10`.

Therefore the large Repair19a LSMR residual cannot by itself be interpreted as a demonstrated physical linear compatibility obstruction.

The Repair19a LSMR solves did not converge; they reached the fixed iteration ceiling.

## Nonlinear alpha probes

The orth-basis unfinished LSMR direction does not provide a useful nonlinear completion.

At alpha=1 the momentum epsilon is approximately:

- scale 5, Nr=256: `0.9891`
- scale 5, Nr=512: `0.9914`
- scale 10: essentially `1.0`
- scale 20: approximately `0.996-1.0`.

These values are diagnostic only and reflect the unfinished linear direction.

## Interpretation

Repair19a establishes:

1. the chain basis is substantially worse conditioned than the orthonormal basis;
2. merely switching basis does not make the iterative LSMR solve converge under the frozen 10000-iteration budget;
3. the two unfinished iterative solutions disagree strongly;
4. because earlier dense direct linear solves and left-null projections showed near-perfect compatibility, Repair19a does not establish genuine physical linear infeasibility.

The next step must directly solve the same frozen reduced linear systems with a deterministic dense direct least-squares method before any new nonlinear solve is attempted.

## Licensed continuation

A separately preregistered diagnostic may:

- reuse exactly the Repair19a grouped Jacobian and both frozen bases;
- densify the two reduced matrices;
- solve them with a deterministic direct LAPACK least-squares driver;
- use the same `1e-6` linear-feasibility threshold;
- compare rank, residual, and physical correction across chain and orth bases;
- compare direct results to the frozen incomplete LSMR results.

It may not:

- run nonlinear least squares;
- alter the physical projection pair;
- change Y4/Qmean;
- add fields;
- alter physics, eta, branch, thresholds, radial points, or historical artifacts;
- write a state NPZ.
