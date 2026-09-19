# NL1C7B4 Repair19c2 — pre-data finite-difference step-scale Jacobian audit

## Status

Pre-data / pre-run diagnostic preregistration.

Repair19c1 is frozen as

`NL1C7B4_REPAIR19C1_FIRST_STEP_DIRECTIONAL_JACOBIAN_FIDELITY_CHARACTERIZED`

at result-freeze commit

`cbf05b2a2845cda70fb962b20c5062d516b24a5b`.

Frozen Repair19c1 result JSON:

- bytes: `151045`
- SHA-256:
  `b4898fed6c6bbe7d4c91f8144ed35d03e6f318b298a2fc13c0daaef038c0e3cd`.

## Scientific question

Can the loss of local derivative fidelity identified by Repair19c1 be reduced by changing only the finite-difference scheme and absolute step size used to construct the same grouped physical-coordinate Jacobian?

No physics, state variable, gauge condition, residual, branch, threshold, or nonlinear solver is changed.

## Frozen domain

Exactly six lambda=1 canonical cases:

- eta=0
- Y=Simple
- beta=1
- scales=5,10,20 h^-1 Mpc
- Nr=256,512.

## Frozen parent and coordinates

Use exactly the Repair19c parent state and residual map.

Coordinates remain:

- physical pair `(y_L,q_Rt)`;
- same orthonormal Helmert basis;
- exact `Y4=0,Qmean=0`.

## Frozen reference direction

For each case reproduce the frozen Repair19c first GELSY direction using the original default grouped SciPy 2-point Jacobian.

This frozen direction `dz0` is not recomputed from any candidate Jacobian for the primary derivative-fidelity score.

## Symmetric exact directional reference

For the frozen physical direction `dx0=B_orth dz0`, evaluate exact residuals at:

- `+dx0`
- `-dx0`
- `+0.5 dx0`
- `-0.5 dx0`.

Define central directional secants:

`D1 = [F(dx0)-F(-dx0)]/2`

`Dhalf = [F(0.5 dx0)-F(-0.5 dx0)]/1`.

Define the preregistered Richardson reference:

`Dref = (4 Dhalf - D1)/3`.

Record reference stability:

`||Dhalf-D1|| / max(||Dref||,tiny)`.

The Richardson reference is used only as an independent directional derivative target.

## Candidate Jacobians

Keep the same grouped half-band-16 sparsity pattern.

Evaluate both finite-difference methods:

- `2-point`
- `3-point`

at the following absolute physical-coordinate steps:

- `1e-5`
- `3e-6`
- `1e-6`
- `3e-7`
- `1e-7`
- `3e-8`.

Total candidates per case: 12.

The original default SciPy 2-point Jacobian is retained separately as the frozen control.

At x=0 every candidate is constructed with explicit `abs_step`; no relative-step fallback is permitted.

## Primary derivative-fidelity metric

For candidate reduced Jacobian

`J_cand = Jx_cand B_orth`

evaluate its action on the frozen reduced direction:

`A_cand = J_cand dz0`.

Primary mismatch:

`m = ||A_cand-Dref|| / max(||Dref||,tiny)`.

Also record H-block and M-block mismatch separately.

The default-control mismatch is evaluated by the same formula.

## Deterministic candidate ranking

For every scheme/step pair aggregate across all six cases:

- maximum primary mismatch;
- median primary mismatch;
- maximum H-block mismatch;
- maximum M-block mismatch.

Select exactly one candidate by lexicographic minimization of:

1. maximum primary mismatch;
2. median primary mismatch;
3. maximum M-block mismatch;
4. method preference: 3-point before 2-point;
5. step preference in the frozen listed order.

This selection rule is fixed before execution.

No candidate is selected from exact nonlinear closure performance.

## One-step descriptive cross-check

For every candidate and case, independently solve

`min ||F0 + J_cand dz||_2`

with the same GELSY cutoff rule as Repair19c.

Evaluate exactly one full physical step `x=B_orth dz`.

Record, but do not use for candidate selection:

- returned rank;
- predicted relative residual;
- exact frozen-denominator residual ratio after the full step;
- moving-denominator max epsilon_H and epsilon_M;
- max |y_L| and max |q_Rt|;
- exact Q and gauge residuals.

No second step or line search is permitted.

## Gates

### R19C2_G1 — exact frozen provenance

Require exact Repair19c1 PASS hash/classification/gates and all inherited parents.

### R19C2_G2 — exact frozen direction reproduction

For all six cases reproduce the frozen Repair19c first direction to abs-or-rel `1e-10` for:

- rank;
- predicted relative residual;
- max |step y_L|;
- max |step q_Rt|.

### R19C2_G3 — finite symmetric directional reference

Require all 24 reference evaluations finite:

- 6 cases x {+1,-1,+1/2,-1/2}.

### R19C2_G4 — exact gauge/Q/field freeze for reference probes

Require all 24 reference evaluations to preserve:

- exact-Q error <= `1e-12`;
- |Y4| <= `1e-12`;
- |Qmean| <= `1e-12`;
- all nonprojection fields bitwise frozen.

### R19C2_G5 — complete finite candidate Jacobian audit

Require all 72 candidate Jacobians finite:

- 6 cases x 12 candidates.

Require all primary directional-action mismatch metrics finite.

### R19C2_G6 — complete one-step descriptive probes

Require all 72 candidate GELSY one-step probes finite.

No closure threshold is imposed.

### R19C2_G7 — deterministic selection completeness

Require exactly one candidate selected by the frozen lexicographic rule and exact reproduction of its aggregate score from the stored case rows.

### R19C2_G8 — claim boundary

Repair19c2 must not:

- run a nonlinear iteration;
- run line search;
- certify a corrected state;
- write a state NPZ;
- change the physical projection pair;
- add a field;
- change Y4/Qmean;
- alter sources, coefficients, signs, eta, branch, historical thresholds, radial points, or parent artifacts;
- run time evolution;
- make an observational claim;
- relabel Repair19c or Repair19c1.

## Terminal classifications

If all eight gates pass:

`NL1C7B4_REPAIR19C2_FINITE_DIFFERENCE_STEP_SCALE_CHARACTERIZED`.

Otherwise:

`NL1C7B4_REPAIR19C2_IMPLEMENTATION_FAIL`.

## Interpretation boundary

Repair19c2 may identify a numerically preferred finite-difference method/step under the preregistered derivative-fidelity metric.

It does not certify exact nonlinear constraint closure.

Only after Repair19c2 is frozen may a separate nonlinear repair use the selected Jacobian construction.
