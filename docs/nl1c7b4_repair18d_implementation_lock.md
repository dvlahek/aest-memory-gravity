# NL1C7B4 Repair18d — implementation lock

## Status

Locked after implementation and before any Repair18d execution.

## Frozen Repair18c parent

- result-freeze commit:
  `c29ce80b65435b60882bd5140a9cfe648b4f3a5b`
- result-freeze blob:
  `dbb242c45bdc86bc88db6f39a9d54cf3c33d2f81`
- Repair18c JSON SHA-256:
  `d49600f8b27536aeb0dca28d1d777d09439a376241c7f8f93b74e754c502e24b`
- classification:
  `NL1C7B4_REPAIR18C_TWO_MODE_NULLSPACE_CHARACTERIZED`.

## Preregistration

- commit:
  `2f07ab2a5ffb905427f48c681f39b1a0be8221e3`
- file:
  `docs/nl1c7b4_repair18d_predata_nullspace_transversality_audit.md`
- blob:
  `225434cc3371e48aa1f536566544020b46302245`.

## Implementation

- commit:
  `2755dfdc75b30ed18f8ba5e945bd7cfaf4afcafa`
- file:
  `nl1c7b/initial_constraint_certification_repair18d.py`
- blob:
  `c7e5ab27e53798b9b907d0d3689f18cd97e36a79`.

## Frozen candidate order

Exactly:

1. `Y1+Qmean`
2. `Y4+Qmean`
3. `Y8+Qmean`
4. `Y16+Qmean`
5. `Y1+Q1`.

No other candidate may be added after first execution.

All functional rows are Euclidean-normalized before constructing the 2x2 null-space intersection matrix.

## Frozen transversality rule

At each scale:

`T=G V0`.

A pair is transverse if:

`sigma_min(T)>1e-6`.

A pair is globally transverse if this holds at all three scales.

## Frozen deterministic selection rule

For each globally transverse pair compute

`S=min_scale sigma_min(T)`.

Select the pair with largest S.

If two S values agree to absolute-or-relative `1e-12`, choose the earlier pair in the frozen candidate order.

Repair18d reports this selection but does not impose it.

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

## Frozen science domain

- eta=0
- Y=Simple
- beta=1
- lambda=1
- Nr=256
- scales=5,10,20 h^-1 Mpc
- projection pair unchanged
- dense default 2-point Jacobian
- Repair18c rank rule unchanged.

## Terminal classes

- `NL1C7B4_REPAIR18D_NULLSPACE_TRANSVERSALITY_AUDIT_PASS`
- `NL1C7B4_REPAIR18D_IMPLEMENTATION_FAIL`.

No nonlinear solve, state change, candidate addition/removal, threshold change, field change, physics change, or historical relabelling may occur after first execution.
