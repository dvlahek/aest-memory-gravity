# NL1C7B4 Repair17 — implementation lock

## Status

Locked after implementation and before any Repair17 execution.

## Parent Repair16 freeze

- freeze commit: `af47a7c33c0f09744b98828e0727279b1c3d6475`
- freeze blob: `c5456a8947e33d5625a29ddeb600ca3c9236bfda`
- Repair16 JSON SHA-256:
  `a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b`

## Preregistration

- commit: `ef7e23770590ab70691feb701e33a4a6624e7ad8`
- file: `docs/nl1c7b4_repair17_predata_repair16_source_localization.md`
- blob: `3a7471d6c5b9704656880b7e8578e403bedc60cb`

## Implementation

- commit: `9bb8afef7ca657d35b2e8737020c508982dde551`
- file: `nl1c7b/initial_constraint_certification_repair17.py`
- blob: `c39d9e7bc20eef55fbd0bcea2bd19f42d8cfd8b5`

## Frozen imported blobs

- Repair16 state/evaluator semantics:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`
- Repair10 exact signed 11-source decomposition:
  `c72a85d6d42176fb8c6a5ebf5f8e101541272701`
- Repair09 exact nonlinear evaluator:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- Repair01 source dictionary:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- base B4 evaluator:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08 evaluator:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

## Locked diagnostic settings

- exact Repair16 H/M reproduction tolerance: absolute-or-relative `1e-12`
- signed decomposition closure limit: `1e-12`
- scales: 5,10,20 h^-1 Mpc
- Nr: 256,512
- Y: Simple, Exponential, Sharp
- beta: 1.0,0.5,0.1
- cases: 54
- all non-center radial points retained
- eta=0
- 11 frozen source labels unchanged

No source label is preregistered as expected dominant.

## Claim boundary

Repair17 is diagnostic only.

It cannot modify/project the state, fit/rescale any coefficient, insert/remove a source, change a sign, clip K, linearize Q, remove radial points, select scales/Y/beta values, alter historical thresholds, run nonlinear evolution, run finite eta, relabel Repair16, or make an observational claim.

## Terminal classes

- `NL1C7B4_REPAIR17_REPAIR16_SOURCE_LOCALIZATION_PASS`
- `NL1C7B4_REPAIR17_IMPLEMENTATION_FAIL`

A PASS licenses only a separately preregistered nonlinear-order correction design informed by the frozen localization.
