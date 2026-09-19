# NL1C7B4 Repair19c3 — pre-data selected-Jacobian nonlinear closure repair

## Status

Pre-data / pre-run preregistration.

Repair19c2 is frozen at:

- result-freeze commit:
  `5f51cae7943679f6e96dcdefc7814c0f1551e244`
- result-freeze blob:
  `6a4df5a5e3ab71abf5339db10b358acbdd31dfa4`
- result JSON SHA-256:
  `6a724f46a70be8d23e7b9898fe6e70073879c12f77eefbdbddc63d87fb47a17c`
- classification:
  `NL1C7B4_REPAIR19C2_FINITE_DIFFERENCE_STEP_SCALE_CHARACTERIZED`.

Repair19c2 selected exactly:

- method: `3-point`
- absolute physical-coordinate finite-difference step:
  `3e-6`.

No alternative candidate may be substituted after this preregistration.

## Scientific question

Does the exact same orthonormal direct GELSY Gauss-Newton nonlinear projection used in Repair19c reach the historical exact eta=0 constraint threshold when its grouped physical-coordinate Jacobian is replaced by the Repair19c2-selected finite-difference construction?

## Frozen physics and state

Unchanged from Repair19c:

- eta=0 only
- physical projection variables:
  `(y_L,q_Rt)`
- exact state map:
  `L=L_parent exp(y_L)`
  and
  `R_t=R_{t,parent}+q_Rt(a H R_s)`
- all other physical fields frozen
- exact orthonormal Helmert representation of:
  `Y4=0`
  and
  `Qmean=0`
- no direct modification of Q, alpha, phi, matter, sources, signs or coefficients.

## Frozen canonical domain

Exactly:

- scales `5,10,20 h^-1 Mpc`
- `Nr=256,512`
- virtual amplitudes:
  `1,1/2,1/4,1/8`
- Simple branch, beta=1.

Total canonical nonlinear solves:

`3 x 2 x 4 = 24`.

## Frozen Jacobian construction

At every nonlinear iteration:

- start from physical-coordinate residual map `F(x)`;
- use the same grouped half-band-16 sparsity pattern as Repair19c;
- use SciPy finite differences with:
  - `method='3-point'`
  - explicit `abs_step=3e-6`;
- form the reduced Jacobian:
  `J_orth = J_x B_orth`.

No relative-step fallback is allowed.

## Frozen linear solve

Unchanged from Repair19c:

- LAPACK driver: `gelsy`
- cutoff:
  `max(J_orth.shape) * eps_float64`
- solve:
  `min ||F + J_orth dz||_2`.

## Frozen globalization

Unchanged from Repair19c:

- start: zero correction
- Armijo constant:
  `1e-4`
- backtracking alpha list:
  `1,1/2,1/4,1/8,1/16,1/32,1/64,1/128`
- maximum accepted iterations:
  `12`
- safety bound:
  `max|y_L| <= 0.5`
  and
  `max|q_Rt| <= 0.5`.

No trust region, LM damping, alternate line search, multistart, restart, or continuation may be added.

## Historical thresholds

Unchanged:

- exact Hamiltonian:
  `max epsilon_H <= 1e-7`
- exact momentum:
  `max epsilon_M <= 1e-7`
- exact Q:
  `<=1e-12`
- exact gauge residuals:
  `<=1e-12`.

## First-step certification

For every lambda=1 canonical case, the first selected-Jacobian step must reproduce the corresponding Repair19c2 `3-point, abs_step=3e-6` descriptive one-step probe.

Compare with abs-or-rel tolerance `1e-10`:

- rank
- predicted relative residual
- max |y_L|
- max |q_Rt|
- exact frozen-denominator residual ratio after the full step.

This is a numerical reproduction gate, not a closure gate.

## Frozen correction-scaling gate

If all 24 canonical nonlinear solves close exactly, use the same correction metric and scaling gate as Repair19c.

For each scale/grid, using amplitudes ordered:
`1,1/2,1/4,1/8`,

require the last two adjacent log2 slopes to lie in:

`[1.8,2.2]`.

## Frozen two-grid gate

For every scale at lambda=1 require the symmetric correction-amplitude ratio between Nr=256 and Nr=512 to be:

`<=2.0`.

## Frozen branch retest

Only after a canonical lambda=1 state passes exact closure, retest that same frozen corrected state under the unchanged nine branch combinations:

- Y in `Simple, Exponential, Sharp`
- beta in `1.0,0.5,0.1`.

Require all 54 branch/grid/scale retests to satisfy the historical `1e-7` H and M thresholds.

No branch-specific refit is allowed.

## Output rule

A corrected-state NPZ may be written only if all core physics, scaling, grid, branch, field-freeze and claim-boundary gates pass.

Otherwise no corrected-state NPZ may remain.

## Gates

### R19C3_G1 — exact frozen provenance

Require exact Repair19c2 JSON SHA/classification/all gates and all inherited historical artifacts.

### R19C3_G2 — orthonormal constrained basis

Require exact Y4/Qmean nullspace basis and orthonormality checks as in Repair19c.

### R19C3_G3 — exact parent reproduction

Require exact canonical Repair16 parent residual reproduction.

### R19C3_G4 — selected first-step reproduction

Require the lambda=1 first selected-Jacobian steps to reproduce Repair19c2 selected one-step probes under the frozen `1e-10` tolerance.

### R19C3_G5 — exact canonical nonlinear closure

Require all 24 canonical cases to satisfy the historical exact H/M/Q/gauge and safety thresholds.

### R19C3_G6 — second-order correction scaling

Require the same small-amplitude correction-scaling gate as Repair19c.

### R19C3_G7 — two-grid correction amplitude

Require the same `<=2.0` grid ratio as Repair19c.

### R19C3_G8 — all branch lambda1 exact closure

Require all 54 branch retests to pass with no refit.

### R19C3_G9 — field-freeze invariant

Require all nonprojection fields frozen in all canonical solves.

### R19C3_G10 — output integrity

If all core gates pass, require the written state NPZ to reproduce all six lambda=1 corrected states exactly.

If core gates fail, require no state NPZ to remain.

### R19C3_G11 — claim boundary

No new field, source, coefficient, sign, branch, eta, threshold, radial-point removal, branch-specific fit, time evolution or observational claim.

## Terminal classifications

Implementation/provenance failure:

`NL1C7B4_REPAIR19C3_IMPLEMENTATION_FAIL`.

Canonical nonlinear closure failure:

`NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_NONLINEAR_CLOSURE_FAIL`.

Correction-scaling failure:

`NL1C7B4_REPAIR19C3_CORRECTION_SCALING_FAIL`.

Two-grid failure:

`NL1C7B4_REPAIR19C3_TWO_GRID_CONTROL_FAIL`.

Branch-retest failure:

`NL1C7B4_REPAIR19C3_CANONICAL_PASS_BRANCH_RETEST_FAIL`.

Full pass:

`NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_EXACT_NONLINEAR_CONSTRAINT_PASS`.

## Interpretation boundary

A full Repair19c3 PASS would certify the eta=0 radial nonlinear initial constraint projection for the frozen physical pair and selected numerical Jacobian under the existing gates.

It would not yet certify short-time eta=0 evolution, finite eta, or observational agreement.
