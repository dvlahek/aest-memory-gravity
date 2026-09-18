# NL1C7B4 Repair16 — local result freeze

## Status

Frozen local WSL science result from the first locked Repair16 execution.

Terminal classification:

`NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL`

with

`SCIENCE_RC=2`.

Execution HEAD:

`568a054c73aced9cb1cc602b2f214ff2103a7f63`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `51920`
  - SHA-256:
    `a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b`
- evaluator log:
  - bytes: `52366`
  - SHA-256:
    `1862c3147330ba491e8ed0d63f5229d3b9cb648367e5d61344ddfdc7edc118c7`
- local runner log:
  - bytes: `54757`
  - SHA-256:
    `325bbc68bad8df619d4df0a54c849b018e687cb591ce6024f3ca084ddbf55214`

## Gate result

- R16_G1 exact Repair15a provenance: PASS
- R16_G2 Repair15a state-anchor reproduction: PASS
- R16_G3 exact nonlinear dictionary: PASS
- R16_G4 original raw B4 constraints: FAIL
- R16_G5 two-grid control: PASS
- R16_G6 claim boundary: PASS

This is therefore a science FAIL of the historical exact nonlinear raw-constraint gate, not an implementation failure.

## Exact provenance and state reproduction

- Repair15a primary state anchor maximum relative-L2 error: `0.0`
- scalar canonical vs independent identity at a_i:
  `2.3926238952144846e-14`
- exact nonlinear Q reconstruction maximum normalized error:
  `0.0`
- frozen K-dictionary symbolic identity: PASS
- all action terms finite on all non-center points.

## Raw constraint result

All 54 historical cases fail the unchanged `1e-7` raw max-epsilon criterion.

Summary:

- number of exact cases: `54`
- number passing both H and M: `0`
- minimum max-epsilon_H:
  `2.82449072357526e-7`
- maximum max-epsilon_H:
  `9.458367877931119e-6`
- minimum max-epsilon_M:
  `0.9982808847025694`
- maximum max-epsilon_M:
  `0.9999999999944793`

Representative Simple, beta=1 cases:

- scale 5, Nr=256:
  - max H: `2.8244907235774306e-7`
  - max M: `0.99999392720923`
- scale 5, Nr=512:
  - max H: `2.8270674267627895e-7`
  - max M: `0.9999934459904575`
- scale 10, Nr=256:
  - max H: `6.591345400775493e-6`
  - max M: `0.9998965065630939`
- scale 10, Nr=512:
  - max H: `6.590922989560273e-6`
  - max M: `0.9999999999944793`
- scale 20, Nr=256:
  - max H: `9.458326870987007e-6`
  - max M: `0.9984002409940183`
- scale 20, Nr=512:
  - max H: `9.458367877931119e-6`
  - max M: `0.9982808847025694`

## Two-grid result

All 27 historical grid-control pairs PASS.

Observed RMS ratio ranges:

- H: `1.000000150473604 .. 1.0000026889447362`
- M: `1.0003178678466818 .. 1.000389059860866`

Therefore the remaining residual is numerically grid-stable under the frozen two-grid test.

## Comparison with historical Repair09

The density-Q completion strongly reduces the Hamiltonian max residual while leaving the exact nonlinear momentum failure essentially unchanged.

Representative Nr=256 Simple beta=1 Hamiltonian improvement factors relative to Repair09:

- scale 5: approximately `19.1x`
- scale 10: approximately `6.79x`
- scale 20: approximately `7.85x`

This is consistent with Repair14a identifying and removing the missing first-order Hamiltonian density-Q bridge term.

The remaining exact nonlinear residual is not licensed to be removed by threshold relaxation.

## Claim boundary

Preserved exactly:

- no B4 residual used to modify the state;
- no state projection;
- no coefficient fit/rescale;
- no source insertion/removal;
- no sign change;
- no K clipping;
- no Q linearization;
- no radial-point removal;
- no threshold change;
- no Y/beta/scale selection;
- no nonlinear evolution;
- eta=0;
- no observational claim.

## Licensed continuation

Repair16 FAIL licenses a separately preregistered exact signed source localization on the frozen Repair15a state.

The next diagnostic must:

- reproduce all 54 Repair16 H/M epsilon values;
- decompose the exact nonlinear numerators into the same frozen 11 source labels used by Repair10;
- retain both Nr=256 and Nr=512;
- preserve all Y/beta/scale cases;
- make no state change.

Only after that localization may a nonlinear-order constraint-correction construction be preregistered.
