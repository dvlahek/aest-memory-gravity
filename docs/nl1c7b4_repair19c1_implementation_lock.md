# NL1C7B4 Repair19c1 — implementation lock

## Status

Locked after implementation and before any Repair19c1 execution.

Repair19c1 is a diagnostic characterization only.

## Frozen Repair19c parent

- result-freeze commit:
  `e0d7415be5da36757327c0d36cc2eaaae2ecc2d5`
- result-freeze blob:
  `bdfa2f60bd909ab25669aaedd20b7945a004eaf2`
- Repair19c JSON SHA-256:
  `5ad02254c512f90d0f82a42d0f5aa00f15c1dae6248bdbe7ad69addb183b600a`
- classification:
  `NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_NONLINEAR_CLOSURE_FAIL`.

## Preregistration

- commit:
  `6318ce0f3a61a6503c4090bde6f4f247563cb704`
- file:
  `docs/nl1c7b4_repair19c1_predata_first_step_directional_jacobian_fidelity.md`
- blob:
  `9388ef43b7e6e215f89383d154a04a266d385ef8`.

## Implementation

- commit:
  `cbbbdf0db23b65412f99ce73b2c1c15aaac989da`
- file:
  `nl1c7b/initial_constraint_certification_repair19c1.py`
- blob:
  `616570dd106d92ffcb08bdaed99b646dd08a12e1`.

## Frozen domain

Exactly six lambda=1 canonical cases:

- eta=0
- Y=Simple
- beta=1
- scales=5,10,20 h^-1 Mpc
- Nr=256,512.

## Frozen direction

For each case compute exactly one x=0 direct GELSY direction using:

- same parent state as Repair19c;
- same frozen-denominator residual;
- same grouped physical-coordinate SciPy two-point Jacobian;
- same Repair18a half-band-16 sparsity;
- same orthonormal Helmert basis;
- same GELSY cutoff rule.

The first-step rank and amplitudes must reproduce the frozen Repair19c result.

## Frozen directional sweep

Exact amplitudes:

`1,1/2,1/4,1/8,1/16,1/32,1/64,1/128,1/256,1/512,1/1024,1/2048,1/4096`.

Total exact samples:

`6 x 13 = 78`.

For each sample measure:

- exact and linear-predicted residuals;
- nonlinear remainder;
- directional derivative mismatch;
- H and M block residual/remainder;
- moving-denominator H/M epsilon;
- exact-Q error;
- Y4/Qmean;
- field-freeze invariant.

No nonlinear iteration is run after the single x=0 direction is formed.

## Frozen gates

- exact provenance;
- exact orthonormal basis reproduction;
- exact parent residual reproduction;
- exact frozen first-step reproduction;
- all 78 samples finite;
- exact Q and gauge preservation;
- all nonprojection fields bitwise frozen;
- claim boundary.

No threshold is imposed on the measured remainder slopes or directional mismatch. They are characterization outputs.

## Terminal classes

- `NL1C7B4_REPAIR19C1_FIRST_STEP_DIRECTIONAL_JACOBIAN_FIDELITY_CHARACTERIZED`
- `NL1C7B4_REPAIR19C1_IMPLEMENTATION_FAIL`.

## Frozen imported blobs

- Repair19c:
  `f27ed8b39c1351e27d4f3b43b195ff4423e04c76`
- Repair19b1:
  `11a14221a4d6d5d639781134b5e55233f863b799`
- Repair19a:
  `3322ed5cb6ed36471b5d700966d9a3fba646d2d8`
- Repair18a:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`
- Repair16:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`
- Repair01:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair09:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

No amplitude, basis, Jacobian rule, driver, cutoff, source, field, threshold, eta, branch, radial point set, case, or interpretation rule may change after the first Repair19c1 execution.
