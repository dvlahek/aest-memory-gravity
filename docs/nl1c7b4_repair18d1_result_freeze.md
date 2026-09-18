# NL1C7B4 Repair18d1 — local result freeze

## Status

Frozen local WSL PASS from the first locked Repair18d1 execution.

Terminal classification:

`NL1C7B4_REPAIR18D1_NULLSPACE_TRANSVERSALITY_AUDIT_PASS`

with

`SCIENCE_RC=0`.

Execution HEAD:

`4b15e589b18d3fa11e783b0e7725d0eb5c3c5afd`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `21164`
  - SHA-256:
    `21d5be34660f0054bd8550908f300de64ec1ec9e8f81e0f150c7c1540e3bf04c`
- evaluator log:
  - bytes: `21610`
  - SHA-256:
    `4f6b51987f56cbed6f65208edbd973410242d4b956f414b269c2145300affcae`
- local runner log:
  - bytes: `26130`
  - SHA-256:
    `a8d9afd45d09522971bdc59ea460dec236173376f2532527f0283ab5ad281ce2`.

## Gate result

All six Repair18d1 gates PASS:

- R18D1_G1 frozen provenance
- R18D1_G2 exact Repair18c reproduction
- R18D1_G3 exact Repair18d transversality payload reproduction
- R18D1_G4 deterministic selected pair
- R18D1_G5 finite diagnostic
- R18D1_G6 claim boundary

Both Repair18c scalar reproduction and Repair18d transversality payload reproduction are exact:

- maximum absolute error: `0.0`
- maximum relative error: `0.0`.

Repair18d remains classified IMPLEMENTATION_FAIL and is not relabelled.

## Certified selected pair

The frozen deterministic max-worst-scale rule selects:

`Y4 + Qmean`.

Definitions:

- `Y4`: normalized uniform functional on the first four non-center `y_L` coordinates;
- `Qmean`: normalized uniform functional on all non-center `q_Rt` coordinates.

Selected-pair transversality:

- scale 5:
  - sigma_min = `0.7582799682419049`
  - condition number = `1.3187739988996978`
- scale 10:
  - sigma_min = `0.7582405493326686`
  - condition number = `1.3188407223794012`
- scale 20:
  - sigma_min = `0.758089503930239`
  - condition number = `1.3190740772192389`.

Worst-scale sigma_min:

`0.758089503930239`.

Maximum condition number:

`1.3190740772192389`.

Relative sigma_min spread:

`0.0002511794055532205`.

Thus the selected pair intersects the certified two-dimensional null space strongly and almost scale-independently.

## Interpretation

Repair18d1 certifies a deterministic pair of simple conditions that removes the two local null directions identified by Repair18b1/Repair18c.

It does not yet establish nonlinear exact-constraint closure.

The selected pair may now be used by a separately preregistered nonlinear closure test.

## Licensed continuation

The next test may impose exactly:

- `Y4=0`
- `Qmean=0`

through an exact reduced-coordinate parametrization rather than a penalty term.

The nonlinear closure test must retain:

- physical projection pair `(L,R_t)`;
- eta=0;
- original exact nonlinear source dictionary;
- original B4 max-epsilon threshold `1e-7`;
- no source/coefficient/sign modification;
- no radial-point removal;
- no Q linearization;
- no K clipping.

A PASS must establish exact nonlinear closure before any short-time evolution or observational calculation.
