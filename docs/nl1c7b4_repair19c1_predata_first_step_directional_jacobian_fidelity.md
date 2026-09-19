# NL1C7B4 Repair19c1 — pre-data first-step directional Jacobian fidelity audit

## Status

Pre-data / pre-run diagnostic preregistration.

Repair19c is frozen as

`NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_NONLINEAR_CLOSURE_FAIL`

at result-freeze commit

`e0d7415be5da36757327c0d36cc2eaaae2ecc2d5`.

Frozen Repair19c result JSON:

- bytes: `293215`
- SHA-256:
  `5ad02254c512f90d0f82a42d0f5aa00f15c1dae6248bdbe7ad69addb183b600a`.

Repair19c1 is diagnostic only.

## Scientific question

Why does the frozen Repair19c first direct GELSY step predict near-annihilation of the linearized residual while the exact nonlinear residual after the same accepted physical step remains many orders of magnitude larger?

Repair19c1 tests the directional fidelity of the frozen grouped finite-difference Jacobian along the already certified first Gauss-Newton direction.

It does not change the physical projection ansatz or run a new nonlinear optimizer.

## Frozen domain

Use only the six lambda=1 canonical cases:

- eta=0
- Y=Simple
- beta=1
- scales=5,10,20 h^-1 Mpc
- Nr=256,512.

The parent states, residual normalization, source dictionaries and radial point sets are exactly those of Repair19c.

## Frozen physical subspace

Use exactly:

- physical correction pair `(L,R_t)`;
- Repair19a orthonormal Helmert basis;
- exact gauge conditions `Y4=0,Qmean=0`.

No chain-basis science result is produced.

## Frozen first direction

At x=0 for each case:

1. compute the exact same grouped physical-coordinate SciPy two-point Jacobian used by Repair19c;
2. form `J_orth=J_x B_orth`;
3. compute exactly one GELSY least-squares direction with the frozen Repair19c cutoff rule;
4. require this direction to reproduce the frozen Repair19c first-step rank, predicted residual, max |y_L| and max |q_Rt| to abs-or-rel `1e-10`.

No later Gauss-Newton iteration is performed.

## Deterministic directional amplitude sweep

Evaluate the exact nonlinear frozen-denominator residual at

`x(alpha)=alpha * dx_0`

for

`alpha = 1, 1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/128, 1/256, 1/512, 1/1024, 1/2048, 1/4096`.

For each alpha record:

- exact residual L2;
- exact residual ratio to `||F0||`;
- linear-predicted residual L2;
- linear-predicted residual ratio;
- nonlinear remainder
  `R(alpha)=F(alpha dx_0)-[F0+alpha J dx_0]`;
- `||R(alpha)||_2`;
- relative remainder `||R(alpha)||/||F0||`;
- directional derivative mismatch
  `||[F(alpha dx_0)-F0]/alpha - J dx_0|| / max(||J dx_0||,tiny)`;
- H-block and M-block versions of the exact residual and remainder;
- moving-denominator exact `max epsilon_H` and `max epsilon_M`;
- exact-Q reconstruction error;
- Y4 and Qmean residuals.

## Remainder scaling

For adjacent amplitudes compute

`s_R = log2(||R(alpha)|| / ||R(alpha/2)||)`.

A smooth first-order-valid Jacobian with ordinary quadratic nonlinear remainder would show `s_R approximately 2` over an amplitude range before roundoff dominates.

Also report directional-mismatch scaling. No post-run threshold is allowed.

## Frozen interpretation metrics

Repair19c1 is a characterization audit, not a new nonlinear closure gate.

Report for every case:

- minimum directional derivative mismatch over the amplitude sweep;
- alpha at that minimum;
- minimum exact residual ratio;
- alpha at that minimum;
- median remainder slope over the three largest alphas;
- median remainder slope over the three smallest finite alphas;
- exact/predicted residual ratio at alpha=1.

These metrics are descriptive.

## Gates

### R19C1_G1 — exact frozen provenance

Require exact Repair19c hash/classification/gates and all inherited parent hashes.

Repair19c must remain science FAIL.

### R19C1_G2 — exact orthonormal basis reproduction

Require the frozen Repair19c orthonormal basis audit at both grids to reproduce to abs-or-rel `1e-12`.

### R19C1_G3 — exact parent reproduction

For all six lambda=1 cases reproduce the frozen Repair19c parent residual inputs to abs-or-rel `1e-12`.

### R19C1_G4 — exact first-step reproduction

For all six cases reproduce the frozen Repair19c first GELSY step to abs-or-rel `1e-10` for:

- rank;
- predicted relative residual;
- max |step y_L|;
- max |step q_Rt|;
- exact nonlinear residual L2 at alpha=1.

### R19C1_G5 — complete finite directional sweep

Require all 78 exact directional samples finite:

- 6 cases x 13 amplitudes.

### R19C1_G6 — exact gauge and Q preservation

For all 78 samples require:

- exact-Q reconstruction error <= `1e-12`;
- |Y4| <= `1e-12`;
- |Qmean| <= `1e-12`.

### R19C1_G7 — field-freeze invariant

Require all nonprojection fields bitwise frozen for all 78 directional samples.

### R19C1_G8 — claim boundary

Repair19c1 must not:

- run more than the single x=0 direct linear direction per case;
- run a nonlinear optimizer;
- accept or certify a corrected state;
- write a state NPZ;
- change the physical projection pair;
- add a field;
- change Y4/Qmean;
- alter any source, coefficient, sign, eta, branch, threshold, radial point set, or historical artifact;
- run time evolution;
- make an observational claim;
- relabel Repair19c.

## Terminal classifications

If all eight gates pass:

`NL1C7B4_REPAIR19C1_FIRST_STEP_DIRECTIONAL_JACOBIAN_FIDELITY_CHARACTERIZED`.

Otherwise:

`NL1C7B4_REPAIR19C1_IMPLEMENTATION_FAIL`.

## Interpretation boundary

Repair19c1 does not decide in advance if the mismatch is dominated by:

- genuine nonlinear curvature over the full first-step amplitude;
- finite-difference Jacobian scale error;
- cancellation/roundoff in the residual map;
- another numerical loss of local derivative fidelity.

The amplitude dependence of the exact secant and nonlinear remainder will distinguish these possibilities without modifying the frozen physics or nonlinear solver.
