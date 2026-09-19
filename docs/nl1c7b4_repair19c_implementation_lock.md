# NL1C7B4 Repair19c — implementation lock

## Status

Locked after implementation and before any Repair19c execution.

Repair19c is an eta=0 nonlinear initial-constraint projection test only.

## Frozen Repair19b1 parent

- result-freeze commit:
  `5f33dd543f9b722438faa9659858be942287f14f`
- result-freeze blob:
  `58114df328eb4d47d8e5d049bdcfea4aa9c2bdd9`
- Repair19b1 JSON SHA-256:
  `33774c721bfd15c1c2f6b776408b3fc4623e3720f9199aa04fc43e8415be1a26`
- classification:
  `NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_FEASIBILITY_LSMR_STAGNATION_PASS`.

## Preregistration

- commit:
  `3eaefcccb6c44f2db12b24caf3bfa3c3ec16a712`
- file:
  `docs/nl1c7b4_repair19c_predata_orthonormal_direct_gn_nonlinear_closure.md`
- blob:
  `7749938dadb43f6cff6b974a9ee4af58bdf72a09`.

## Implementation

- commit:
  `5216c1afb9e27a24957aaade43f0857641f1b12d`
- file:
  `nl1c7b/initial_constraint_certification_repair19c.py`
- blob:
  `f27ed8b39c1351e27d4f3b43b195ff4423e04c76`.

## Frozen nonlinear algorithm

Coordinates:

- exact Repair19a orthonormal Helmert basis;
- physical pair only `(L,R_t)`;
- exact `Y4=0,Qmean=0`.

Residual/Jacobian:

- frozen-parent normalized H/M residual;
- exact moving-denominator constraints for certification;
- grouped sparse physical-coordinate two-point Jacobian;
- frozen Repair18a half-band-16 sparsity;
- algebraic `J_orth=J_x B_orth`.

Direct step:

- SciPy `lstsq`
- LAPACK `gelsy`
- `cond=max(J_orth.shape)*eps_float64`
- no alternate driver or iterative fallback.

Globalization:

- zero start;
- alpha sequence:
  `1,1/2,1/4,1/8,1/16,1/32,1/64,1/128`;
- Armijo constant `1e-4`;
- safety bounds `max|y_L|<=0.5`, `max|q_Rt|<=0.5`;
- maximum 12 accepted Gauss-Newton iterations;
- no trust region, LM term, multistart, or random perturbation.

## Frozen domain

Canonical nonlinear solves:

- eta=0
- Y=Simple
- beta=1
- lambda in {1,1/2,1/4,1/8}
- scales 5,10,20 h^-1 Mpc
- Nr=256,512.

Total: 24 solves.

Lambda=1 solved states are then retested without refit across:

- Y in {Simple,Exponential,Sharp}
- beta in {1,0.5,0.1}.

Total all-branch retests: 54.

## Frozen gates

- exact inherited provenance;
- orthonormal constrained basis;
- exact parent reproduction;
- first lambda=1 GELSY step reproduces frozen Repair19b1;
- all 24 canonical solves satisfy exact H/M <=1e-7;
- small-lambda correction slopes in [1.8,2.2];
- lambda=1 two-grid correction ratio <=2;
- all 54 branch retests satisfy H/M <=1e-7;
- bitwise freeze of all nonprojection fields;
- output NPZ written only if all preceding science gates pass and then validated exactly;
- claim boundary.

## Frozen imported blobs

- Repair19b1:
  `11a14221a4d6d5d639781134b5e55233f863b799`
- Repair19b:
  `862bb139ea9ff9f85907b0457119ad2916660278`
- Repair19a:
  `3322ed5cb6ed36471b5d700966d9a3fba646d2d8`
- Repair19:
  `2532094b518dfc2990fa0d77d8123d793b0107b3`
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

## Terminal classes

- `NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_EXACT_NONLINEAR_CONSTRAINT_PASS`
- `NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_NONLINEAR_CLOSURE_FAIL`
- `NL1C7B4_REPAIR19C_CORRECTION_SCALING_FAIL`
- `NL1C7B4_REPAIR19C_TWO_GRID_CONTROL_FAIL`
- `NL1C7B4_REPAIR19C_CANONICAL_PASS_BRANCH_RETEST_FAIL`
- `NL1C7B4_REPAIR19C_IMPLEMENTATION_FAIL`.

No solver, basis, line search, iteration limit, threshold, physical field, source, coefficient, sign, eta, branch, radial point set, case, or classification rule may change after the first Repair19c execution.
