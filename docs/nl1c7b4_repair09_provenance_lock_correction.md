# NL1C7B4 Repair09 — provenance-lock correction

## Status

Execution-harness correction after the frozen local attempt-01 pre-evaluation failure at commit `31245e697143304e37440d2dd939bd3965d50fc3`.

This document does not alter the Repair09 preregistration, evaluator, scientific thresholds, gates, or allowed classifications.

## Corrected provenance literal

The original implementation-lock document remains historically unchanged and contains a clerical error in the full preregistration commit SHA.

Incorrect literal:

`ee97aec3e274f3996c87c622a770f5233666f7f6`

Correct preregistration commit:

`ee97aec340b9b8dcc508d092730b795f01eb65bd`

The correct commit is the parent of the frozen Repair09 implementation commit `8f04b382aaa44960df18f662c2fa8330665e82c2` and contains the already locked preregistration blob:

`3e4f6ed8cf8a70a791f0ffef68c9b780ba7552c6`.

## Unchanged scientific lock

The following remain unchanged:

- preregistration file blob: `3e4f6ed8cf8a70a791f0ffef68c9b780ba7552c6`;
- Repair09 evaluator commit: `8f04b382aaa44960df18f662c2fa8330665e82c2`;
- Repair09 evaluator blob: `0cd67cecfbd590cb8819ad37314dc5b49047bc93`;
- original implementation-lock commit: `14b2a05000a8ea73105ede6c4188013df11be88a`;
- original implementation-lock blob: `d36b8238d83fdb13199d5e7709c8fbccafaf7df7`;
- exact Repair08 JSON SHA-256: `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`;
- exact Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`;
- Q-dictionary limit: `1e-12`;
- Repair08 state-anchor reproduction limit: `1e-12`;
- raw B4 Hamiltonian and momentum limits: `1e-7`;
- two-grid RMS ratio limit: `2.0`;
- all 54 frozen constraint cases;
- eta = 0 only.

## Execution rule

Any corrected Repair09 runner/workflow must verify this correction document in addition to the original lock and must use the correct preregistration commit SHA above. No other scientific or numerical change is licensed.
