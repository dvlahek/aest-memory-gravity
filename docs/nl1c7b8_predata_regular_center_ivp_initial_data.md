# NL1C7B8 — pre-data zero-parameter regular-center IVP initial data

## Status

Pre-data / pre-implementation preregistration.

Parent structural certification:

`NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS`.

Immediate parent construction result:

`NL1C7B7_REDUCED_RADIAL_CONSTRUCTION_FAIL`.

B7 result-freeze commit:

`6bd01d8e4c825fe4f150a851c4dc402644b664cc`.

B7 result JSON SHA-256:

`449201305c535e24e592296f5e2a53e7fc0866b5cae2970a147c2bcebe12bfc6`.

NL1C7B8 is a new project-level regular-center representation.

It is not B7a/B7b, does not expand the B7 shooting bracket and does not tune any B7 root/integrator parameter.

## Motivation

B7 correctly found no sign change in the frozen shooting residual for any of the six scale/grid cases.

Post-result analytic center inspection shows that the B7 shooting degree of freedom was not physical.

At a regular spherical center, the exact Hamiltonian has leading form

`H(0)=2 L_0 - 2 R_r(0)^2/L_0`.

For positive radial metric coefficient,

`H(0)=0`

therefore requires

`L(0)=R_r(0)`.

Together with regular

`R_t(0)=0`

and the exact leading momentum relation

`R_{t,r}(0)=L_t(0)R_r(0)/L(0)=L_t(0)`,

the reduced first-order system has no free shooting parameter.

B8 tests that unique regular-center branch directly.

## Frozen physics

Unchanged from B6/B7:

- eta=0;
- Simple branch;
- beta=1;
- density-Q-completed parent state;
- exact-Q reconstruction;
- identical AeST coefficients and signs;
- identical frozen `R,L_t,u,u_t,phi,Q_target,dust` fields;
- only `L` and `R_t` may change;
- scales 5,10,20 h^-1 Mpc;
- Nr=256 and Nr=512;
- original B4 exact differential threshold `1e-7`.

No additional field, fitted parameter or phenomenological closure is permitted.

## Exact reduced radial equations

Use exactly the B6/B7 first-order reduction:

`L_r=-B_H/A_H`

and

`R_{t,r}=B_M/(4LR)`.

Use the same exact action-derived source/flux dictionary and the same exact-Q substitution.

No profile-wide residual minimization is permitted.

No scalar shooting or boundary fitting is permitted.

## Frozen radial representation

Use the B7 local degree-8 polynomial representation on the original B4 nine-node stencil family for every frozen radial field required by the reduced equations.

At every original grid node, first derivatives must reproduce the original B4 derivative matrix to abs-or-rel tolerance `1e-12`.

No alternate interpolation is permitted.

## Analytic regular-center identity

The implementation must independently verify the center reduction:

1. GR curvature:
   `H_GR,curv(0)=2L_0-2R_r(0)^2/L_0`;
2. GR kinetic contribution vanishes at least as `O(r^2)`;
3. AeST E/X local and flux-divergence contributions vanish at least as `O(r)`;
4. j/J, K, dust and background Hamiltonian contributions vanish at least as `O(r^2)`;
5. regular momentum gives
   `R_{t,r}(0)=L_t(0)R_r(0)/L(0)`.

The candidate center data are then fixed, not fitted:

`L_0=R_r(0)>0`;

`R_t(0)=0`;

`R_{t,r}(0)=L_t(0)`.

## Solved variables

As in B7:

`ell=log(L/a_i)`

and

`w=R_t/(a_i H_i R_s)`.

The fixed center value is

`ell_0=log[R_r(0)/a_i]`.

Require `abs(ell_0)<=0.5`.

## Center launch

Do not divide the reduced equations at `r=0`.

Primary launch:

`epsilon=1e-5 r_1`.

Control launch:

`epsilon_control=1e-4 r_1`.

For both launches use the fixed analytic center data:

`ell(epsilon)=ell_0`;

`R_t(epsilon)=epsilon L_t(0)`.

The omitted regular corrections are `O(epsilon^2)` in L and `O(epsilon^3)` in R_t.

No alternative center launch is permitted.

## Radial integrator

Use exactly the B7 radial integrator:

`scipy.integrate.solve_ivp`

with

`DOP853`.

Frozen settings:

- rtol `1e-11`;
- atol `1e-13`;
- max_step equal to the frozen radial grid spacing.

No method or tolerance sweep.

## Center-launch control

After independently integrating the primary and control launches, sample both on the original radial grid.

Require in each of the six cases:

- relative L2 difference in L `<=1e-6`;
- relative L2 difference in R_t `<=1e-6`.

The primary launch is the candidate science state.

## Outer background predictions

There is no shooting parameter.

Both outer conditions are therefore predictions.

For the primary state require:

### Outer L compatibility

`abs[L(r_max)-a_i]/a_i <=1e-7`.

### Outer R_t compatibility

`abs[R_t(r_max)-a_i H_i r_max]/abs[a_i H_i r_max] <=1e-7`.

Neither condition may be used to alter the center data or the integrated profile.

No finite-radius constant shift is permitted.

## Safety and state integrity

For every primary state require:

- all values finite;
- `L>0`;
- exact-Q normalized error `<=1e-12`;
- all non-`L,R_t` fields bitwise identical to the parent;
- `max |log(L/L_parent)|<=0.5`;
- `max |(R_t-R_t,parent)/(a_i H_i R_s)|<=0.5`.

No clipping.

Historical `Y4/Qmean` values are descriptive only.

## Independent original differential certification

Evaluate each primary state with the unchanged original B4/Repair18a differential evaluator.

On every noncenter node require:

`max epsilon_H<=1e-7`;

`max epsilon_M<=1e-7`.

No reduced-equation residual may substitute.

Only the analytic center may be excluded.

## Two-grid correction control

Use the same combined correction amplitude as previous tracks.

For each scale require symmetric Nr256/Nr512 ratio `<=2.0`.

## Output

Write a corrected-state NPZ only if every B8 science gate passes.

Any non-PASS classification must leave the NPZ absent.

## Gates

### B8_G1 — frozen provenance

Exact B6 PASS, exact B7 frozen construction FAIL, and inherited parent hashes.

### B8_G2 — frozen-field polynomial representation

All required first derivatives reproduce B4 within `1e-12` abs-or-rel.

### B8_G3 — exact reduced-equation and center identity

B6/B7 reduced RHS structural identities and the regular-center algebraic identities all pass.

### B8_G4 — complete zero-parameter IVP construction

Primary and control IVPs complete for all six cases with the fixed analytic center data.

### B8_G5 — center-launch stability

L and R_t primary/control relative L2 differences are each `<=1e-6`.

### B8_G6 — outer L background compatibility

All six primary states satisfy the frozen `1e-7` relative L boundary criterion.

### B8_G7 — outer R_t background compatibility

All six primary states satisfy the frozen `1e-7` relative R_t boundary criterion.

### B8_G8 — safety, exact-Q and field freeze

All six primary states pass.

### B8_G9 — original B4 differential exact constraints

All six primary states satisfy H and M `<=1e-7`.

### B8_G10 — two-grid correction control

All three scale pairs satisfy ratio `<=2.0`.

### B8_G11 — output integrity and claim boundary

NPZ only on full PASS; no evolution, finite-eta or observational claim otherwise.

## Terminal classifications

Implementation/provenance failure:

`NL1C7B8_REGULAR_CENTER_IVP_IMPLEMENTATION_FAIL`.

IVP construction failure:

`NL1C7B8_REGULAR_CENTER_IVP_CONSTRUCTION_FAIL`.

Center launch instability:

`NL1C7B8_REGULAR_CENTER_CONTROL_FAIL`.

Outer L incompatibility:

`NL1C7B8_OUTER_L_COMPATIBILITY_FAIL`.

Outer R_t incompatibility:

`NL1C7B8_OUTER_RT_COMPATIBILITY_FAIL`.

Safe state returned but original B4 differential constraints fail:

`NL1C7B8_DIFFERENTIAL_CERTIFICATION_FAIL`.

Two-grid correction control fails:

`NL1C7B8_TWO_GRID_CONTROL_FAIL`.

Full certification:

`NL1C7B8_REGULAR_CENTER_INITIAL_DATA_CERTIFIED`.

Only the final class licenses eta=0 short-time evolution.

No B8a/B8b solver-parameter repair sequence is licensed after the first complete locked B8 execution.
