# NL1C7B4 Repair19c3 — implementation lock

## Status

Locked after implementation and before any Repair19c3 execution.

Repair19c3 is the first nonlinear rerun licensed by the frozen Repair19c2 finite-difference selection.

## Frozen Repair19c2 parent

- result-freeze commit:
  `5f51cae7943679f6e96dcdefc7814c0f1551e244`
- result-freeze blob:
  `6a4df5a5e3ab71abf5339db10b358acbdd31dfa4`
- result JSON SHA-256:
  `6a724f46a70be8d23e7b9898fe6e70073879c12f77eefbdbddc63d87fb47a17c`
- selected Jacobian:
  `3-point, abs_step=3e-6`.

## Preregistration

- commit:
  `39d36344c9746c51f57cc2f1d85c773b62df2d3c`
- file:
  `docs/nl1c7b4_repair19c3_predata_selected_jacobian_nonlinear_closure.md`
- blob:
  `6e7d2c2ecdad036e5755db05a1519222b2f2d264`.

## Implementation

- commit:
  `0f5ac90a7b618f9769bcdf2367aeecdec8f4217d`
- file:
  `nl1c7b/initial_constraint_certification_repair19c3.py`
- blob:
  `08985f1ee334f038a7125cc239fb6b8929d428af`.

## Frozen solver

Unchanged Repair19c nonlinear solver except for the Repair19c2-selected Jacobian:

- orthonormal Y4=0/Qmean=0 basis
- direct GELSY least squares
- grouped half-band-16 physical-coordinate Jacobian
- `method='3-point'`
- `abs_step=3e-6`
- zero start
- same Armijo `c=1e-4`
- same alpha list:
  `1,1/2,1/4,1/8,1/16,1/32,1/64,1/128`
- same maximum 12 accepted iterations
- same safety bound 0.5
- same exact threshold `1e-7`
- same Q/gauge threshold `1e-12`
- same correction-scaling gate
- same two-grid gate
- same branch retests.

## Frozen domain

- eta=0
- scales 5,10,20 h^-1 Mpc
- Nr=256,512
- amplitudes 1,1/2,1/4,1/8
- canonical Simple beta=1
- branch retest Simple/Exponential/Sharp x beta 1,0.5,0.1.

## Frozen imported blobs

- Repair19c:
  `f27ed8b39c1351e27d4f3b43b195ff4423e04c76`
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
- reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

## Claim boundary

Repair19c3 may not change:

- physical projection pair
- source dictionary
- coefficients or signs
- branch definition
- eta
- historical thresholds
- radial point set
- selected Jacobian method or step
- line-search rule
- correction-scaling rule
- grid rule
- branch-retest rule.

It may not add a field, run time evolution, make an observational claim, or relabel an earlier repair.

## Terminal classes

- `NL1C7B4_REPAIR19C3_IMPLEMENTATION_FAIL`
- `NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_NONLINEAR_CLOSURE_FAIL`
- `NL1C7B4_REPAIR19C3_CORRECTION_SCALING_FAIL`
- `NL1C7B4_REPAIR19C3_TWO_GRID_CONTROL_FAIL`
- `NL1C7B4_REPAIR19C3_CANONICAL_PASS_BRANCH_RETEST_FAIL`
- `NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_EXACT_NONLINEAR_CONSTRAINT_PASS`.
