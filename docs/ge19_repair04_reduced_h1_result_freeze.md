# GE19 Repair04 reduced-H1 result freeze

## Historical result

Repair04 science execution is frozen as

`GE19_REPAIR04_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Failure stage:

`Stage_A_reduced_H1_reclosure`.

This historical classification must not be relabeled.

## Frozen local result hashes

User-local science JSON:

- SHA256: `dd03f40b392f8b5b31332de8526bfcf590a44aea8f3f356254e5d2ee86d845b7`
- bytes: `10549`

User-local science FULL log:

- SHA256: `dd03f40b392f8b5b31332de8526bfcf590a44aea8f3f356254e5d2ee86d845b7`
- bytes: `10549`

Outer local runner log:

- SHA256: `1309b263507aa5fd4a9df2d887e664b4a6cb3729eaa785461af8ba64a5ce2c1f`
- bytes: `13495`

The JSON and inner FULL log are byte-identical because the science executable writes the JSON object to stdout before the runner summary.

## Provenance and implementation controls that passed

- Repair04 lock audit: PASS.
- Required local frozen inputs: present.
- Mandatory local coordinate self-audit: PASS.
- active stable-GE06 background coordinate: `Z_action`.
- GE15 dense hash: exact.
- GE15 frozen 64-node jet error: `0.0`.
- GE18 Repair01 NPZ hash: exact.
- GE15/GE18 metric bridge: `0.0`.
- requested-k relative miss: `0.0`.
- background-mode mismatch remains diagnostic-only: `2.14156901519004e-6`.
- stable GE06 benign c1 relative L2: `1.013732536430478e-15`.
- stable GE06 benign c2 relative L2: `1.3343678633575401e-15`.
- stable GE06 c1/c2 physical probes: all finite.
- stable Exp background native controls: PASS.

Therefore the Repair03 wrong-coordinate defect is not present in this run.

## Stage-A frozen controls

Global maxima:

- linear-system relative L2 residual: `1.0`;
- shift-constraint relative L2: `1.000101435173245`;
- anisotropy-constraint relative L2: `1.0`;
- initial dynamic match abs-or-rel: `1.000000000117399`;
- primary64/control32 state relative L2: `1.0`;
- all outputs finite: true.

Primary 64-node solves reached linear residual `1.0` for all three C cases and initial-match values approximately `1.0`.

The 32-node controls were also unacceptable but not identical to the 64-node failure: linear residuals were `0.9989912371006521`, `0.748734703583371`, and `0.9840489695647787` for C_min/C_star/C_max, while their initial-match errors were approximately `1.52e-7`, `1.21e-8`, and `1.11e-7`.

No exception, matrix-rank warning, singular-matrix warning, traceback, or non-finite-state failure occurred in the captured runner log.

## Stop rule

The Amendment01 stop rule was correctly applied.

`Z20_constructed=false`.

No H3 interpretation is licensed by Repair04.

## Repair05 diagnosis boundary

The combination of:

- exact provenance,
- correct Z-coordinate wiring,
- finite operator probes,
- finite Stage-A outputs,
- severe linear residual,
- severe grid dependence,
- and loss of imposed initial conditions at 64 nodes

localizes the next repair target to numerical realization of the collocation linear solve.

Repair05 may change only algebraically equivalent numerical conditioning of the linear solve: deterministic diagonal row/column equilibration and residual-based iterative refinement performed on the same frozen matrix equation `A x = b`.

Repair05 must not change:

- the physical operator;
- the stable GE06 coordinate;
- equations;
- boundary rows or boundary values;
- matter model;
- grid sizes;
- modes/phases/beta0/C values;
- thresholds;
- Stage-A/Stage-B definitions;
- the Repair04 historical classification.
