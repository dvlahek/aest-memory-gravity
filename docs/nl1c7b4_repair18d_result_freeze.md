# NL1C7B4 Repair18d — local result freeze

## Status

Frozen local WSL result from the first locked Repair18d execution.

Terminal classification:

`NL1C7B4_REPAIR18D_IMPLEMENTATION_FAIL`

with

`SCIENCE_RC=2`.

Execution HEAD:

`eebef5c8fab0b679aa5d994bd97fba8313fe347a`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `20628`
  - SHA-256:
    `adc1410d50118c8080c1f84e5733cb09e5ff7d8f51a4937f1e306a96fe416def`
- evaluator log:
  - bytes: `21074`
  - SHA-256:
    `b00c7ca20ac66468f10221d182da6cf439886f27d06630df996042643888f702`
- local runner log:
  - bytes: `26028`
  - SHA-256:
    `9bacfadd6706208069efc3bf4e1bad8b8a5863c02683e9aaa2351d7254390232`.

## Gate result

PASS:

- R18D_G1 exact frozen provenance
- R18D_G3 exact candidate set
- R18D_G4 complete finite transversality audit
- R18D_G5 at least one globally transverse pair
- R18D_G6 deterministic selection rule
- R18D_G7 claim boundary

FAIL:

- R18D_G2 exact Repair18c null-space reproduction

Repair18d therefore remains IMPLEMENTATION_FAIL and is not relabelled.

## Frozen transversality payload

All five preregistered candidate pairs are globally transverse at all three scales.

The deterministic frozen selection rule chooses

`Y4+Qmean`.

Selected-pair metrics:

- worst-scale sigma_min:
  `0.758089503930239`
- maximum condition number:
  `1.3190740772192389`
- relative sigma_min spread:
  `0.0002511794055532205`.

Per scale:

- scale 5:
  - sigma_min `0.7582799682419049`
  - sigma_max `0.9999999060039128`
  - condition `1.3187739988996978`
- scale 10:
  - sigma_min `0.7582405493326686`
  - sigma_max `0.9999985138192506`
  - condition `1.3188407223794012`
- scale 20:
  - sigma_min `0.758089503930239`
  - sigma_max `0.9999762128463706`
  - condition `1.3190740772192389`.

This payload is diagnostic only because G2 failed.

## Exact implementation defect

Repair18c intentionally computed two SVDs:

`s_ref = np.linalg.svd(J, compute_uv=False)`

for the frozen scalar singular-value/rank diagnostics, and

`U,s,Vh = np.linalg.svd(J, full_matrices=True)`

for the singular vectors/subspace.

Repair18d instead used only the full-SVD singular values `s` for both purposes.

At the enormous condition numbers present here, the values-only and full-SVD LAPACK paths agree at the large singular values and at the rank classification, but do not agree at the tiny bottom singular values.

Observed Repair18d reproduction pattern:

- rank reproduces exactly at 508/510 for all three scales;
- rank tolerance reproduces to ~1e-15 relative;
- sigma_max reproduces to ~1e-15 relative;
- sigma_min does not reproduce;
- the transversality payload, which depends on the full-SVD right subspace V0, remains finite and stable.

Thus G2 failed because Repair18d did not reproduce the exact Repair18c SVD-path semantics.

## Licensed continuation

A separately preregistered Repair18d1 may change only the frozen-scalar reproduction path:

- compute `s_ref=np.linalg.svd(J,compute_uv=False)`;
- use `s_ref` for sigma_max, sigma_min, rank tolerance, and numerical rank;
- retain the full-SVD `V0` exactly as in Repair18d for the transversality matrices.

Repair18d1 must also reproduce the entire frozen Repair18d transversality payload before assigning a scientific PASS.

No candidate, threshold, selection rule, physical field, Jacobian, state, source, coefficient, sign, branch, eta value, or historical classification may change.
