# NL1C7B4 Repair19c2 — implementation lock

## Status

Locked after implementation and before any Repair19c2 execution.

Repair19c2 is a finite-difference Jacobian characterization only.

## Frozen Repair19c1 parent

- result-freeze commit:
  `cbf05b2a2845cda70fb962b20c5062d516b24a5b`
- result-freeze blob:
  `e61978b2d0a0af7f4ad4b2fbdeafc7b9626681fc`
- Repair19c1 JSON SHA-256:
  `b4898fed6c6bbe7d4c91f8144ed35d03e6f318b298a2fc13c0daaef038c0e3cd`
- classification:
  `NL1C7B4_REPAIR19C1_FIRST_STEP_DIRECTIONAL_JACOBIAN_FIDELITY_CHARACTERIZED`.

## Preregistration

- commit:
  `a094d9b660b346c3fcf03f6b26f2ce39ce263894`
- file:
  `docs/nl1c7b4_repair19c2_predata_finite_difference_step_scale_audit.md`
- blob:
  `7c2a0372beab748127353ef0124527b824158a0a`.

## Implementation

- commit:
  `515cc6c0ed04ec02d6dd48422bb0e96cf6575373`
- file:
  `nl1c7b/initial_constraint_certification_repair19c2.py`
- blob:
  `802c37c03c75b9ca906b807dce3cbd1792a8a30f`.

## Frozen domain

Exactly six lambda=1 canonical cases:

- eta=0
- Y=Simple
- beta=1
- scales=5,10,20 h^-1 Mpc
- Nr=256,512.

## Frozen derivative reference

For each case:

1. reproduce the original Repair19c default 2-point GELSY direction;
2. evaluate exact residuals at +/-dx0 and +/-0.5 dx0;
3. form:
   - `D1=[F(dx0)-F(-dx0)]/2`
   - `Dhalf=[F(0.5dx0)-F(-0.5dx0)]`
   - `Dref=(4 Dhalf-D1)/3`.

No nonlinear iteration is performed.

## Frozen candidate Jacobians

Methods:

- `2-point`
- `3-point`.

Explicit absolute physical-coordinate steps:

- `1e-5`
- `3e-6`
- `1e-6`
- `3e-7`
- `1e-7`
- `3e-8`.

Same grouped half-band-16 sparsity pattern.

Total:

- 12 candidate Jacobians per case
- 72 candidate Jacobians overall.

## Frozen primary metric

For every candidate:

`m=||J_cand dz0-Dref||/||Dref||`.

Also record H- and M-block mismatches.

## Frozen selection rule

Aggregate every scheme/step across all six cases and select by lexicographic minimization of:

1. maximum primary mismatch;
2. median primary mismatch;
3. maximum M-block mismatch;
4. method preference: 3-point before 2-point;
5. step preference in the preregistered order.

Exact nonlinear one-step residuals are descriptive only and do not enter candidate selection.

## Frozen one-step cross-check

For each candidate/case, solve one GELSY linear system and evaluate exactly one full physical step.

No second step, line search, trust region, LM term, multistart, or nonlinear optimizer is permitted.

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

## Terminal classes

- `NL1C7B4_REPAIR19C2_FINITE_DIFFERENCE_STEP_SCALE_CHARACTERIZED`
- `NL1C7B4_REPAIR19C2_IMPLEMENTATION_FAIL`.

No candidate list, step size, method, ranking rule, physical field, source, coefficient, sign, eta, branch, threshold, radial point set, parent artifact, or interpretation rule may change after the first Repair19c2 execution.
