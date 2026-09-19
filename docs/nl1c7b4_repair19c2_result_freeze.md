# NL1C7B4 Repair19c2 — local result freeze

## Status

Frozen local WSL characterization result from the first locked Repair19c2 execution.

Terminal classification:

`NL1C7B4_REPAIR19C2_FINITE_DIFFERENCE_STEP_SCALE_CHARACTERIZED`

with

`SCIENCE_RC=0`.

Execution HEAD:

`a3418fb649d34084325395b8b7f579cb9ac4bb53`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `145569`
  - SHA-256:
    `6a724f46a70be8d23e7b9898fe6e70073879c12f77eefbdbddc63d87fb47a17c`
- evaluator log:
  - bytes: `146015`
  - SHA-256:
    `01902b0a920041c22eacc6a24bca22478f90e2d6d1b1a155695ae5720d978e60`
- local runner log:
  - bytes: `159824`
  - SHA-256:
    `74992b9e84560391f9150e7a94fed26c094b27b4b0228706202a029546f735dc`.

## Gate result

All eight preregistered gates PASS:

- G1 exact frozen provenance
- G2 exact frozen-direction reproduction
- G3 finite symmetric directional reference
- G4 exact gauge/Q/field-freeze preservation for reference probes
- G5 complete finite candidate-Jacobian audit
- G6 complete one-step descriptive probes
- G7 deterministic selection completeness
- G8 claim boundary.

## Frozen selected Jacobian

The preregistered lexicographic rule selects exactly:

- method: `3-point`
- explicit absolute physical-coordinate step:
  `3e-6`.

Aggregate selected-candidate diagnostics across all six lambda=1 cases:

- maximum directional-action mismatch:
  `1.3488978416629585e-4`
- median directional-action mismatch:
  `4.24433123436393e-5`
- maximum H-block mismatch:
  `7.047244539288453e-7`
- maximum M-block mismatch:
  `1.3488978416629645e-4`
- maximum exact one-step frozen-denominator residual ratio, descriptive only:
  `9.515121237649822e-4`
- median exact one-step frozen-denominator residual ratio, descriptive only:
  `1.868304553197993e-4`.

## Comparison with frozen default control

Frozen default-control aggregate:

- maximum directional mismatch:
  `4.781774890514617e-2`
- median directional mismatch:
  `2.1027356157032207e-3`.

Selected `3-point, abs_step=3e-6` therefore improves:

- worst-case directional mismatch by a factor
  `354.494961947564`
- median directional mismatch by a factor
  `49.54221288570904`.

The maximum Richardson-reference instability is:

`3.383564090978392e-4`.

## Per-case selected one-step descriptive results

For `3-point, abs_step=3e-6`:

- scale 5, Nr=256:
  - directional mismatch `8.227345125783273e-5`
  - exact one-step residual ratio `6.52392742470065e-5`
  - rank `508`
- scale 5, Nr=512:
  - directional mismatch `1.3488978416629585e-4`
  - exact one-step residual ratio `1.5632765770334938e-4`
  - rank `1020`
- scale 10, Nr=256:
  - directional mismatch `4.0677422241533605e-5`
  - exact one-step residual ratio `7.866477512294377e-4`
  - rank `508`
- scale 10, Nr=512:
  - directional mismatch `4.4209202445745006e-5`
  - exact one-step residual ratio `9.515121237649822e-4`
  - rank `1020`
- scale 20, Nr=256:
  - directional mismatch `6.277411469937728e-6`
  - exact one-step residual ratio `1.7288582923796305e-4`
  - rank `508`
- scale 20, Nr=512:
  - directional mismatch `6.176958087749465e-6`
  - exact one-step residual ratio `2.0077508140163558e-4`
  - rank `1020`.

## Scientific interpretation

Repair19c2 confirms the Repair19c1 diagnosis.

The default grouped SciPy 2-point finite-difference construction was a dominant source of local derivative error in the cancellation-sensitive momentum residual.

A fixed central 3-point construction with explicit absolute physical-coordinate step `3e-6` reduces the frozen-direction derivative mismatch by approximately two to three orders of magnitude in the worst cases.

This improvement is achieved with:

- identical physical `(L,R_t)` projection variables;
- identical exact Y4/Qmean gauge;
- identical residual definition;
- identical eta=0 branch;
- identical radial points;
- no new field;
- no source/coefficient/sign change.

The selected candidate still does not itself certify nonlinear closure.

Its one-step exact residual ratios remain of order `1e-4` to `1e-3`, above the historical exact-constraint threshold `1e-7`.

## Licensed continuation

A separately preregistered Repair19c3 may rerun the Repair19c nonlinear Gauss-Newton procedure with exactly the selected Jacobian construction:

- grouped sparse physical-coordinate Jacobian;
- method `3-point`;
- explicit `abs_step=3e-6`;
- same orthonormal Y4=0/Qmean=0 basis;
- same GELSY direct solve;
- same backtracking alpha list;
- same Armijo constant;
- same maximum iteration count;
- same safety bound;
- same historical exact constraint, Q and gauge thresholds;
- same correction-scaling, two-grid and branch-retest gates.

Repair19c3 must not reinterpret Repair19c or Repair19c1/2 and must not tune the selected finite-difference step after observing nonlinear results.
