# NL1C7B4 Repair09 — local result freeze

## Status

Frozen local WSL reproduction result for the preregistered Repair09 exact nonlinear B4 retest on the certified Repair08 identity-preserving state.

This is a valid science result with terminal classification:

`NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL`

and `SCIENCE_RC=2`.

The earlier Repair09 attempt-01 ancestry failure remains separately frozen as a pre-evaluation harness failure and is not a science result.

## Execution provenance

- branch execution HEAD: `ff2cbc8cd03c96dc14bd293b0962493afb7b74c1`;
- exact Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`;
- Repair09 preregistration commit: `ee97aec340b9b8dcc508d092730b795f01eb65bd`;
- Repair09 implementation commit: `8f04b382aaa44960df18f662c2fa8330665e82c2`;
- original implementation-lock commit: `14b2a05000a8ea73105ede6c4188013df11be88a`;
- provenance-correction commit: `555bc34a98eb918730aebe6f46bbb9f7a1497fc6`;
- corrected runner commit: `1de4be8003f07425df716bf4bbac9425f7041025`;
- workflow-alignment/execution HEAD: `ff2cbc8cd03c96dc14bd293b0962493afb7b74c1`.

## Frozen local output hashes

- result JSON:
  - file: `nl1c7b4_repair09_repair08_exact_constraint_retest.json`
  - bytes: `51514`
  - SHA-256: `be8b54823690ffefb62470c34ee3d7addeef45e2db81e40b10cce4b833376ffc`
- evaluator log:
  - file: `nl1c7b4_repair09_repair08_exact_constraint_retest.log`
  - bytes: `51960`
  - SHA-256: `a928c543d3e4f9056c489e9e80da0795db36b5902bd8ab6ebdd2c295b36a72fc`
- local runner log:
  - file: `nl1c7b4_repair09_repair08_exact_constraint_retest_LOCAL_runner.log`
  - bytes: `52902`
  - SHA-256: `d3f2efa3ee2b131201432ec1b866b962802a94507cb80d88b15356ac4d8d8e88`

## Gate result

- R9_G1 exact Repair08 provenance: PASS
- R9_G2 Repair08 state-anchor reproduction: PASS
- R9_G3 exact nonlinear Q dictionary: PASS
- R9_G4 original raw B4 constraints: FAIL
- R9_G5 two-grid control: PASS
- R9_G6 claim boundary: PASS

The Repair08 state-anchor max relative L2 error is exactly `0.0`, with independent scalar identity relative L2 `2.3926238952144846e-14`.

The exact nonlinear Q target reconstruction has maximum normalized error `0.0`.

## Raw-constraint result

Original B4 limit remains `1e-7` for both Hamiltonian and radial momentum constraints.

All `54/54` frozen cases fail the raw-constraint gate.

Across all cases:

- minimum case-wise max epsilon_H: `5.386807727720773e-06`;
- maximum case-wise max epsilon_H: `7.427970959927211e-05`;
- minimum case-wise max epsilon_M: `0.9982810686119208`;
- maximum case-wise max epsilon_M: `0.9999999999944811`.

Representative stable values by scale:

- 5 h^-1 Mpc:
  - Nr=256 max epsilon_H `5.38687509546703e-06`
  - Nr=256 max epsilon_M `0.9999939272091828`
  - Nr=512 max epsilon_H `5.386807727720773e-06`
  - Nr=512 max epsilon_M `0.9999934459904295`
- 10 h^-1 Mpc:
  - Nr=256 max epsilon_H `4.472759562556653e-05`
  - Nr=256 max epsilon_M `0.9998968500568601`
  - Nr=512 max epsilon_H `4.472949362645421e-05`
  - Nr=512 max epsilon_M `0.9999999999944811`
- 20 h^-1 Mpc:
  - Nr=256 max epsilon_H `7.427827589376325e-05`
  - Nr=256 max epsilon_M `0.9984004027833683`
  - Nr=512 max epsilon_H `7.427970959927211e-05`
  - Nr=512 max epsilon_M `0.9982810686119208`

## Grid control

All 27 matched 256/512 grid-control pairs pass.

- maximum RMS ratio H: `1.0001882562800875`;
- maximum RMS ratio M: `1.00038741861736`;
- frozen limit: `2.0`.

Therefore the observed raw-constraint failure is not removed by doubling the radial resolution.

## Interpretation boundary

Repair09 establishes that the historical scalar bridge cancellation artifact has been removed, but the certified Repair08 state still does not satisfy the frozen exact nonlinear B4 raw constraints.

This result does **not** establish observational detection, finite-eta viability, or nonlinear-evolution viability.

No coefficient fitting, source insertion, sign change, K clipping, Q linearization, radial-point removal, scale selection, Y-branch selection, threshold change, nonlinear evolution, or finite eta was used.

## Licensed next step

The next legal diagnostic is a separately preregistered source-term localization of the exact raw Hamiltonian and especially radial-momentum constraint on the same frozen Repair08 state.

The scalar representation must remain frozen. The localization may decompose signed EL contributions and identify which frozen term(s) dominate the residual, but it may not fit or modify coefficients, signs, sources, states, radial points, thresholds, Y branches, or beta values.
