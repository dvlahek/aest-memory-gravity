# NL1C7B4 Repair18c — implementation lock

## Status

Locked after implementation and before any Repair18c execution.

## Frozen Repair18b1 parent

- result-freeze commit:
  `77090aef851f217f194c0b977afd361bbf016682`
- freeze blob:
  `6ea7f986a441cfbf8256ef1bb77c52e57008d94c`
- result JSON SHA-256:
  `8e0d796e0368372d0b4cf75a075fba12ebde154b651d74929e745118c1ca6dab`
- classification:
  `NL1C7B4_REPAIR18B1_LOCAL_PROJECTION_RANK_DEFICIENCY`.

## Preregistration

- commit:
  `43ddb5e99ca4289663cdbcc614389e2958810f96`
- file:
  `docs/nl1c7b4_repair18c_predata_two_mode_nullspace_characterization.md`
- blob:
  `bf33fefaa075694f2486d01ce4c993cf6ea84da4`.

## Implementation

- commit:
  `3ac5f77991565019ac1fe216fe66b877a375579e`
- file:
  `nl1c7b/initial_constraint_certification_repair18c.py`
- blob:
  `719a4cff1aa793bf97443d4c5fa4ae5849d3f81c`.

## Frozen imported blobs

- Repair18b1 evaluator:
  `1a312dea619c46aa300cbd4c30f141d7d4b2e624`
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

## Frozen domain

- eta=0
- Y=Simple
- beta=1
- lambda=1
- Nr=256
- scales=5,10,20 h^-1 Mpc
- coordinates=(y_L,q_Rt)
- dense SciPy default 2-point Jacobian at x=0
- NumPy full SVD
- frozen rank tolerance from Repair18b1.

## Frozen null-space diagnostics

For every scale:

- exactly two deficient right singular directions;
- right projector leverage split between y_L/q_Rt;
- first/last 1,4,8,16-node leverage fractions;
- maximum leverage coordinate;
- eight preregistered candidate-mode capture fractions;
- left-null compatibility of the parent residual.

Across all three scale pairs:

- two principal angles between the two-dimensional right-null subspaces.

Individual singular-vector signs/order are not compared across scales.

## Frozen consistency limits

- parent Repair18b1 scalar reproduction:
  abs-or-rel <= 1e-12
- U0/V0 orthonormality Frobenius error <= 1e-12
- |trace(P0)-2| <= 1e-12
- full-SVD singular values vs values-only SVD relative-L2 <= 1e-12.

No localization, candidate-capture, principal-angle, or left-compatibility threshold is used for classification.

## Terminal classes

- `NL1C7B4_REPAIR18C_TWO_MODE_NULLSPACE_CHARACTERIZED`
- `NL1C7B4_REPAIR18C_IMPLEMENTATION_FAIL`.

No boundary/gauge condition, nonlinear solve, state artifact, physics term, threshold, eta value, or observational interpretation may be selected after first execution.
