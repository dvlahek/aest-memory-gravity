# NL1C7B4 Repair18 — pre-data minimal nonlinear constraint-projection feasibility

## Status

Pre-data / pre-run preregistration.

Repair17 is frozen at commit

`6a2cbd69218b63d8d7891e9deef43764365c47ff`

with terminal class

`NL1C7B4_REPAIR17_REPAIR16_SOURCE_LOCALIZATION_PASS`.

Repair18 is a feasibility stage only. It does not write an official corrected state artifact.

## Scientific question

Can the frozen Repair15a first-order eta=0 state be completed to exact nonlinear initial-constraint data using only second-order corrections to the radial metric variable `L(r)` and the areal-radius time derivative `R_t(r)`, while all frozen matter/scalar and first-order bridge quantities are held fixed?

## Motivation fixed before execution

Repair17 localizes the remaining Repair16 residual as:

- H dominant: `GR_Nr_boundary` in 54/54;
- H second: `GR_curv_NL` in 54/54;
- M dominant: `AeST_E2` in 54/54;
- M second: `AeST_EX` in 54/54.

In the frozen gauge `N=1,b=0,N_r=0,b_r=0`, the GR radial-momentum contribution reduces algebraically to

`C_M^GR = 4 R (L_t R_r - L d_r R_t)`.

Therefore `R_t` provides direct derivative control of the momentum constraint.

With `R(r)` held fixed, the GR curvature part of the Hamiltonian contains

`2L + 2 R_r^2/L - 4 d_r(R R_r/L)`,

which is first order in the radial derivative of `L`.

This motivates the preregistered projection pair

`(L, R_t)`.

No other state field may be adjusted in Repair18.

## Frozen parent

Repair15a:

- JSON SHA-256:
  `596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`;
- NPZ SHA-256:
  `997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e`.

Repair16 raw exact-constraint result:

- JSON SHA-256:
  `a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b`.

Repair17 localization result:

- JSON SHA-256:
  `09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e`.

## Projection variables

For each parent state define physical fields

`L_p = a + (L-a)_p`

and

`R_{t,p}=aHr + (R_t-aHr)_p`.

Repair18 may change only these two fields.

The solver variables are:

- `y_L(r_i)` for every non-center point, with
  `L=L_p exp(y_L)`;
- `delta R_t(r_i)` for every non-center point, with
  `R_t=R_{t,p}+delta R_t`.

At the center:

- `y_L(0)=0`;
- `delta R_t(0)=0`.

This preserves the parent center values exactly and guarantees `L>0`.

The following remain exactly frozen along each solve:

- `R`;
- `L_t`;
- `u`;
- `u_t`;
- `phi`;
- exact target `Q` / `phidot_minus_Q`;
- baryon density perturbation;
- dust radial velocity;
- all background constants.

## Virtual amplitude path

To test perturbative order, construct virtual parent states for

`lambda in {1, 1/2, 1/4, 1/8}`.

For every perturbation field relative to B3,

`delta f(lambda)=lambda delta f(parent)`.

This includes:

- `L-a`;
- `R-ar`;
- `L_t-aH`;
- `R_t-aHr`;
- `u`;
- `u_t`;
- `phi`;
- `phidot_minus_Q`;
- `delta_b`;
- `dust_vr`.

The density-Q completion is therefore scaled with the same lambda as the first-order state.

No lambda=0 solve is required.

## Canonical solve branch

The nonlinear solve is preregistered on

- Y family: `Simple`;
- beta: `1.0`.

This choice is made before execution because it is smooth and is the fiducial beta already carried through the historical suite.

Repair18 does not claim that the projected state is certified for all Y/beta branches.

All other historical Y/beta branches may be evaluated diagnostically after the canonical solve, but they are nongating in Repair18.

## Exact residual

Use the same frozen exact nonlinear 11-source dictionary as Repair10/16/17.

For each virtual parent state and grid, freeze the canonical parent denominators

`D_H^p(r)=sum_s |C_{H,s}^p(r)| + floor_H^p`

and

`D_M^p(r)=sum_s |C_{M,s}^p(r)| + floor_M^p`.

The nonlinear least-squares residual is the signed vector

`[N_H(r_i)/D_H^p(r_i), N_M(r_i)/D_M^p(r_i)]`

for every non-center point.

The normalization is fixed from the unprojected parent and does not move with the iteration.

After solving, PASS/FAIL is evaluated using the historical exact nonlinear epsilon definition, not the least-squares objective.

## Numerical solver lock

Use `scipy.optimize.least_squares` with:

- method `trf`;
- initial correction exactly zero;
- `x_scale='jac'`;
- `ftol=1e-12`;
- `xtol=1e-12`;
- `gtol=1e-12`;
- `max_nfev=400`;
- a conservative sparse finite-difference Jacobian pattern allowing coupling within 16 radial indices in either correction field.

No multistart is allowed.

If the locked solver does not converge, Repair18 records a feasibility FAIL. Solver settings are not altered after first execution.

## Frozen grids and scales

For every lambda:

- scales `5,10,20 h^-1 Mpc`;
- Nr `256,512`.

Total canonical nonlinear solves:

`4 x 3 x 2 = 24`.

## Correction-order diagnostic

For each solve define the dimensionless combined correction norm

`C(lambda)=sqrt(mean[(delta L/a)^2] + mean[(delta R_t/(a H R_s))^2])`

over non-center points, where

`R_s = scale/h`.

Report adjacent log2 slopes for:

- `1 -> 1/2`;
- `1/2 -> 1/4`;
- `1/4 -> 1/8`.

The first interval is diagnostic only.

The two smaller-amplitude slopes are gating and must lie in

`[1.8,2.2]`

for every scale and grid.

Individual `delta L` and `delta R_t` norms/slopes are reported but nongating.

## Two-grid correction-amplitude control

At lambda=1, compare the combined correction norms at Nr=256 and Nr=512.

For each scale require the symmetric ratio

`max(C_256,C_512)/min(C_256,C_512) <= 2.0`.

No post-run profile-selection rule is allowed.

## Gates

### R18_G1 — frozen provenance

Require exact Repair15a/16/17 hashes/classes/gates and frozen imported evaluator blobs.

### R18_G2 — unprojected lambda=1 reproduction

Before any solve, reproduce the canonical Simple beta=1 Repair16 max-epsilon H/M values for all six scale/grid states to absolute-or-relative `1e-12`.

### R18_G3 — canonical nonlinear solve closure

For all 24 solves require:

- finite solver output;
- `L>0` at all points;
- exact Q reconstruction normalized error <= `1e-12`;
- canonical Simple beta=1
  `max epsilon_H <= 1e-7`;
- canonical Simple beta=1
  `max epsilon_M <= 1e-7`.

### R18_G4 — second-order correction scaling

For every scale/grid, both gated combined-norm slopes must lie in `[1.8,2.2]`.

### R18_G5 — two-grid correction-amplitude control

For every scale at lambda=1 the symmetric combined-correction norm ratio must be <= `2.0`.

### R18_G6 — field-freeze invariant

Numerically verify that every non-projection field is bitwise unchanged from its virtual parent state for every solved state.

Only `L_minus_a` and `Rdot_minus_aHr` may change.

### R18_G7 — claim boundary

Require:

- no official NPZ written;
- no Repair16 relabel;
- no coefficient/source/sign change;
- no K clipping;
- no Q linearization;
- no point removal;
- no threshold change;
- no solver multistart;
- no finite eta;
- no nonlinear time evolution;
- no observational claim.

## Terminal classifications

If provenance/reproduction/field-freeze/claim gates fail:

`NL1C7B4_REPAIR18_IMPLEMENTATION_FAIL`.

If implementation gates pass but any nonlinear solve, second-order scaling, or two-grid correction gate fails:

`NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_FAIL`.

If all seven gates pass:

`NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_PASS`.

## Interpretation boundary

A Repair18 PASS means the frozen first-order Repair15a state admits a numerically stable exact-constraint completion through corrections restricted to `L` and `R_t`, and those corrections scale asymptotically as second order over the preregistered amplitude path.

It does not create or certify an official nonlinear initial-state artifact.

A PASS licenses Repair19: construction and independent certification of the lambda=1 projected state, including all historical Y/beta branches and a separately frozen output NPZ.
