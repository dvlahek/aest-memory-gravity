# NL1C7B4 Repair18b1 — implementation lock

## Status

Locked after implementation and before any Repair18b1 execution.

## Frozen Repair18b parent result

- result-freeze commit:
  `3edf1b11992008d7be383692369f28614ef94d6b`
- freeze blob:
  `ee240e5caac96c69630df6786439c3c541a96e1b`
- Repair18b JSON SHA-256:
  `cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855`
- frozen class:
  `NL1C7B4_REPAIR18B_IMPLEMENTATION_FAIL`.

## Preregistration

- commit:
  `df6968e904ec12c75276004cf4d5bd60486d91b0`
- file:
  `docs/nl1c7b4_repair18b1_predata_boolean_provenance_harness_repair.md`
- blob:
  `7874fb1cc11867d732b5f41a034f9d9ae16c6f60`.

## Implementation

- commit:
  `6e5f826ebf60f817abc78ffaf0bb1a4b8341a5e3`
- file:
  `nl1c7b/initial_constraint_certification_repair18b1.py`
- blob:
  `1a312dea619c46aa300cbd4c30f141d7d4b2e624`.

## Frozen repair

Exactly one harness predicate is changed:

Repair18b:

`kidentity <= 1e-12`

Repair18b1:

`bool(kidentity)`.

The imported `build_nonK()` returns this identity as a Boolean. No scientific/numerical quantity is changed.

## Frozen payload-reproduction gate

Repair18b1 must recompute and reproduce the frozen Repair18b payload to absolute-or-relative `1e-12` for all preregistered scalar diagnostics and exactly for integer/Boolean diagnostics.

The original Repair18b JSON is an explicit input with locked SHA-256.

## Frozen science domain

Unchanged:

- eta=0
- Y=Simple
- beta=1
- lambda=1
- Nr=256
- scales=5,10,20 h^-1 Mpc
- projection pair `(L,R_t)`
- solver coordinates `(y_L,q_Rt)`
- dense and sparse SciPy 2-point Jacobians
- frozen Repair18a sparse pattern
- Frobenius match limit 1e-6
- frozen numerical-rank tolerance
- bounded dense linearized probe
- alphas 1,1/2,1/4,1/8.

## Frozen imported evaluator blobs

- Repair18b evaluator:
  `9beb762d33d4026a446a1a19363e79087b5a6525`
- Repair18a evaluator:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`
- Repair16 evaluator:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`
- Repair01 source dictionary:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair09 exact helpers:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

## Terminal classifications

- `NL1C7B4_REPAIR18B1_SPARSE_JACOBIAN_STRUCTURE_MISMATCH`
- `NL1C7B4_REPAIR18B1_LOCAL_PROJECTION_RANK_DEFICIENCY`
- `NL1C7B4_REPAIR18B1_FULL_RANK_JACOBIAN_DIAGNOSTIC_PASS`
- `NL1C7B4_REPAIR18B1_IMPLEMENTATION_FAIL`.

No science or numerical setting may change after the first Repair18b1 execution.
