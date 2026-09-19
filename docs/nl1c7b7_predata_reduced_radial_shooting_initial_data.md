# NL1C7B7 — pre-data reduced-radial shooting initial-data construction

## Status

Pre-data / pre-implementation preregistration.

Parent structural certification:

`NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS`.

Parent result-freeze commit:

`70c9fc2aa58b76bf3579260e54c6d85097769160`.

Parent result JSON SHA-256:

`ed1efdac5dee72d8c57cbda23d074213babd15fdf3bc7adc18e61789f862e635`.

NL1C7B7 is the first numerical construction licensed by B6.

It is not a continuation of Repair19c and not a B5 solver repair.

## Purpose

Solve the exact B6 first-order radial constraint system directly for the same physical pair

`L(r), R_t(r)`

without minimizing a profile-wide residual vector.

The only scalar numerical root solve is the shooting value `L(0)`, fixed by the physical outer metric condition.

The resulting state is independently certified by the unchanged original B4 differential evaluator.

## Frozen physics

Unchanged from B6:

- eta=0;
- Simple branch;
- beta=1;
- density-Q-completed parent state;
- exact-Q reconstruction;
- same AeST coefficients and signs;
- same frozen `R,L_t,u,u_t,phi,Q_target,dust` fields;
- only `L` and `R_t` may change;
- scales 5,10,20 h^-1 Mpc;
- Nr=256 and Nr=512;
- historical exact B4 threshold `1e-7`.

No additional physical field or phenomenological closure is allowed.

## Exact radial equations

Use the exact B6 continuous reduction.

Write the Hamiltonian constraint as

`H=A_H L_r+B_H=0`

with

`A_H=[4 R R_r + 2 K_B R^2 cosh(u)sinh(u)(L_t+u_r) + 2 C R^2 phi_r]/L^2`.

Thus

`L_r=-B_H/A_H`.

Write the momentum constraint after the exact GR cancellation as

`M=-4LR R_{t,r}+B_M(L,L_r; frozen fields)=0`.

After substituting the Hamiltonian value of `L_r`,

`R_{t,r}=B_M/(4LR)`.

The implementation must generate `B_H` and `B_M` from the same frozen action source/flux dictionary used by B4/B6.

No finite-difference Jacobian or nonlinear profile optimizer is permitted.

## Numerical variables

Integrate dimensionless solved variables

`ell=log(L/a_i)`

and

`w=R_t/(a_i H_i R_s)`

where

`R_s=scale/h`.

Then

`L=a_i exp(ell)`

and

`R_t=(a_i H_i R_s) w`.

This guarantees positive L by construction.

## Frozen-field radial representation

For every frozen parent field required by the exact reduced equations, use a deterministic local degree-8 polynomial representation on the same nine-node uniform-grid stencil family as the original B4 derivative matrix.

For a query point in cell `[r_i,r_{i+1}]`, use exactly

`start=min(max(i-4,0),n-9)`

and the nine nodes `start,...,start+8`.

Represent each field by its unique degree-8 polynomial in the cell-normalized coordinate.

Obtain first and second radial derivatives analytically from that polynomial.

At grid node `r_i`, the first derivative must reproduce the corresponding original B4 nine-node derivative row to abs-or-rel tolerance `1e-12`.

No PCHIP, cubic spline, smoothing or alternate interpolation is permitted.

## Regular center launch

The regular spherical center implies

- `R(0)=0`;
- `R_t(0)=0`;
- `L_r(0)=0`.

Because all non-GR momentum terms vanish faster than the leading GR `O(r)` term at a regular center, the one-sided regular slope is

`lim_{r->0+} R_t/r = L_t(0) R_r(0)/L(0)`.

For a trial shooting value `ell_0` define

`L_0=a_i exp(ell_0)`.

Do not divide the reduced equations at `r=0`.

Primary launch radius:

`epsilon = 1e-5 r_1`

where `r_1` is the first noncenter grid node.

Launch values:

`ell(epsilon)=ell_0`

and

`R_t(epsilon)=epsilon L_t(0)R_r(0)/L_0`.

Equivalently initialize `w(epsilon)` from that expression.

The omitted regular corrections are `O(epsilon^2)` in L and `O(epsilon^3)` in R_t.

## Center-launch control

Repeat the complete construction independently with

`epsilon_control=1e-4 r_1`.

The primary and control constructions use identical physics, shooting bracket and integrator settings.

After both are shot to the same outer L condition, require:

- relative L2 difference in L on common grid nodes `<=1e-6`;
- relative L2 difference in R_t `<=1e-6`.

This is a numerical center-launch control only.

The primary `1e-5 r_1` state is the candidate science state.

No third launch scale is allowed.

## Scalar shooting condition

The only free integration constant after regular-center R_t behavior is the central metric value `ell_0`.

Frozen shooting bracket:

`ell_0 in [-0.5,0.5]`.

This is the same physical L safety range used in the earlier two-field projection track.

Integrate outward and solve exactly one scalar equation:

`ell(r_max)=0`.

Thus the outer metric condition is

`L(r_max)=a_i`.

Use deterministic Brent bracketing root finding.

Require a sign change on the frozen bracket.

If no sign change exists, terminate as a construction failure.

No bracket expansion, multistart, secant fallback or post-run boundary fitting is permitted.

Frozen scalar root tolerances:

- `xtol=1e-12`;
- `rtol=1e-12`;
- `maxiter=100`.

## Radial integrator

Use

`scipy.integrate.solve_ivp`

with method

`DOP853`.

Frozen tolerances for dimensionless variables `(ell,w)`:

- `rtol=1e-11`;
- `atol=1e-13`;
- `max_step=dr`, the frozen radial grid spacing.

Integrate from the frozen launch radius to `r_max`.

Evaluate the final candidate on the original radial grid.

No integrator switch or tolerance sweep is permitted.

## Outer R_t compatibility

Because regular-center momentum behavior fixes the additive constant of R_t and the single remaining shooting constant is consumed by `L(r_max)=a_i`, the outer R_t value is a prediction, not an additional fitted boundary datum.

Require

`abs[R_t(r_max)-a_i H_i r_max]/abs[a_i H_i r_max] <=1e-7`.

This is the frozen asymptotic-background compatibility gate.

It is not used in the shooting objective.

No R_t outer fit is allowed.

## Historical projection gauges

Do not impose

- `Y4=0`;
- `Qmean=0`.

Those were Repair18d1 discrete projection-nullspace transversality functionals.

They are not physical radial boundary conditions in B7.

They may be reported descriptively only.

## Safety and state integrity

For the primary state require:

- all values finite;
- `L>0`;
- exact-Q normalized error `<=1e-12`;
- every non-`L,R_t` field bitwise identical to the frozen parent;
- `max |log(L/L_parent)| <=0.5`;
- `max |(R_t-R_t,parent)/(a_i H_i R_s)| <=0.5`.

No clipping is permitted.

## Independent exact differential certification

The primary returned state must be evaluated by the unchanged original B4/Repair18a differential evaluator.

On every noncenter radial node require

`max epsilon_H <=1e-7`

and

`max epsilon_M <=1e-7`.

No reduced-equation residual may substitute for this gate.

No radial point may be removed except the analytic center.

## Two-grid correction control

For each physical scale define the same combined correction amplitude used previously:

`C=sqrt[RMS((L-L_parent)/a_i)^2 + RMS((R_t-R_t,parent)/(a_i H_i R_s))^2]`.

For Nr256 and Nr512 require symmetric ratio

`max(C256/C512,C512/C256)<=2.0`.

## Output

Write a corrected-state NPZ only if all six cases pass:

- frozen provenance;
- local-polynomial derivative reproduction;
- scalar shooting construction;
- center-launch control;
- outer R_t compatibility;
- safety/Q/field freeze;
- original differential exact constraints;
- two-grid correction control.

If any science gate fails, no NPZ is written.

## Gates

### B7_G1 — frozen provenance

Exact B6 PASS and inherited parent hashes.

### B7_G2 — frozen-field polynomial representation

All required first derivatives at grid nodes reproduce B4 derivative rows within `1e-12` abs-or-rel.

### B7_G3 — exact reduced-equation implementation

Machine-check that the implemented continuous H/M expressions reproduce the B6 symbolic derivative coefficients and structural identities.

### B7_G4 — complete scalar shooting construction

Both launch scales complete for all six cases with a valid bracket and converged Brent root.

### B7_G5 — center-launch stability

Primary/control L and R_t relative L2 differences `<=1e-6` in all six cases.

### B7_G6 — asymptotic-background compatibility

Outer R_t relative mismatch `<=1e-7` in all six cases.

### B7_G7 — safety, exact-Q and field freeze

All integrity conditions pass in all six primary states.

### B7_G8 — original B4 differential exact constraints

All six primary states satisfy H and M `<=1e-7`.

### B7_G9 — two-grid correction control

All three scale pairs satisfy ratio `<=2.0`.

### B7_G10 — output integrity and claim boundary

NPZ only on full PASS; no evolution, finite-eta or observational claim.

## Terminal classifications

Implementation/provenance failure:

`NL1C7B7_REDUCED_RADIAL_IMPLEMENTATION_FAIL`.

No root / integration construction:

`NL1C7B7_REDUCED_RADIAL_CONSTRUCTION_FAIL`.

Center launch unstable:

`NL1C7B7_REDUCED_RADIAL_CENTER_CONTROL_FAIL`.

Outer asymptotic R_t incompatible:

`NL1C7B7_REDUCED_RADIAL_ASYMPTOTIC_COMPATIBILITY_FAIL`.

Safe radial state exists but original differential constraints fail:

`NL1C7B7_REDUCED_RADIAL_DIFFERENTIAL_CERTIFICATION_FAIL`.

Two-grid correction control fails:

`NL1C7B7_REDUCED_RADIAL_TWO_GRID_CONTROL_FAIL`.

Full certification:

`NL1C7B7_REDUCED_RADIAL_INITIAL_DATA_CERTIFIED`.

Only the final class licenses eta=0 short-time evolution.

No B7a/B7b solver-parameter tuning sequence is licensed after the first complete locked B7 execution.
