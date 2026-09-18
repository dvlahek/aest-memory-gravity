# NL1C7B4 Repair18a — pre-data dimensionless-Rt coordinate repair

## Status

Pre-data / pre-run preregistration.

Repair18 is frozen as

`NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_FAIL`

at result-freeze commit

`ff3517dc9a5d394339d20e82b3dd4158346f5498`.

Repair18a is an implementation/numerical-coordinate repair only. It does not alter the physical projection pair, exact constraint equations, historical threshold, canonical branch, amplitude path, correction-order gate, or two-grid gate.

## Frozen Repair18 result

Repair18 result JSON:

- bytes: `62984`
- SHA-256:
  `8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922`.

Repair18 result freeze:

- file:
  `docs/nl1c7b4_repair18_result_freeze.md`
- blob:
  `aa934847951036cfe925becd91740b35b3c0d065`.

Repair18 demonstrated:

- all 24 locked least-squares calls returned solver success;
- no solve hit a bound;
- R18_G4 second-order correction scaling PASS;
- R18_G5 two-grid correction-amplitude control PASS;
- R18_G6 field-freeze PASS;
- only R18_G3 exact nonlinear closure FAIL;
- solver termination was commonly `xtol` with large reported optimality.

## Scientific question unchanged

Can the frozen Repair15a first-order eta=0 state be completed to exact nonlinear initial-constraint data using only corrections to

- `L(r)`;
- `R_t(r)`;

with all non-projection fields frozen?

Repair18a does not introduce a new physical degree of freedom.

## Repair

Repair18 represented the second correction directly in physical units,

`delta R_t`.

Repair18a instead uses the dimensionless solver coordinate

`q_Rt = delta R_t / (a H R_s)`,

where

`R_s = scale / h`.

The physical projected field is still exactly

`R_t = R_{t,p} + delta R_t`

with

`delta R_t = q_Rt (a H R_s)`.

The first coordinate remains

`y_L`

with

`L=L_p exp(y_L)`.

Thus Repair18a is a coordinate reparameterization of exactly the same two-dimensional field space used by Repair18.

## Frozen solver coordinates and bounds

For every non-center point the solver vector is

`x = [y_L, q_Rt]`.

Bounds:

- `y_L in [-0.5,0.5]`;
- `q_Rt in [-0.5,0.5]`.

These are physically identical to the Repair18 bounds

`delta R_t/(a H R_s) in [-0.5,0.5]`.

Center corrections remain exactly zero.

## Frozen solver

Use `scipy.optimize.least_squares` with exactly:

- method `trf`;
- 2-point finite-difference Jacobian;
- the same sparse half-bandwidth 16 pattern;
- zero initial correction;
- `x_scale='jac'`;
- `ftol=1e-12`;
- `xtol=1e-12`;
- `gtol=1e-12`;
- `max_nfev=400`;
- no multistart.

No explicit post-run change of finite-difference step is permitted in Repair18a.

The purpose of the reparameterization is to make the automatic finite-difference perturbation act on a dimensionless `q_Rt` coordinate instead of a very small physical-unit `delta R_t`.

## Exact residual and canonical branch

Unchanged from Repair18.

Canonical solve branch:

- Y = `Simple`;
- beta = `1.0`.

The nonlinear least-squares residual remains the signed vector

`[N_H/D_H^p, N_M/D_M^p]`

on every non-center point, where the parent denominators are frozen before the solve.

Final PASS/FAIL remains the historical exact nonlinear epsilon definition with threshold

`1e-7`.

## Frozen amplitude path, scales, and grids

Unchanged:

- lambda:
  `1, 1/2, 1/4, 1/8`;
- scales:
  `5,10,20 h^-1 Mpc`;
- grids:
  `Nr=256,512`.

Total canonical solves: 24.

## Frozen gates

### R18A_G1 — exact frozen provenance

Require exact Repair15a, Repair16, Repair17, and Repair18 result hashes/classes/gates plus frozen imported evaluator blobs.

Repair18 itself must reproduce as FAIL with only G3 false.

### R18A_G2 — unprojected lambda=1 reproduction

Unchanged from Repair18.

Reproduce canonical Repair16 max-epsilon H/M values for all six scale/grid states to abs-or-rel `1e-12`.

### R18A_G3 — canonical nonlinear solve closure

For all 24 solves require:

- finite solver output;
- `L>0`;
- exact Q reconstruction normalized error <= `1e-12`;
- canonical max epsilon H <= `1e-7`;
- canonical max epsilon M <= `1e-7`.

### R18A_G4 — second-order correction scaling

Use the same combined physical correction norm as Repair18,

`C(lambda)=sqrt(mean[(delta L/a)^2] + mean[(delta R_t/(a H R_s))^2])`.

For each scale/grid the gated slopes

- `1/2 -> 1/4`;
- `1/4 -> 1/8`

must remain in `[1.8,2.2]`.

### R18A_G5 — two-grid correction-amplitude control

At lambda=1 require for every scale

`max(C256,C512)/min(C256,C512) <= 2.0`.

### R18A_G6 — field-freeze invariant

Bitwise require all non-projection fields unchanged.

Only

- `L_minus_a`;
- `Rdot_minus_aHr`

may change.

### R18A_G7 — coordinate-equivalence and claim boundary

Require:

- physical bounds identical to Repair18;
- physical projection pair identical to Repair18;
- no source/coefficient/sign change;
- no threshold change;
- no branch selection change;
- no point removal;
- no K clipping;
- no Q linearization;
- no multistart;
- no finite eta;
- no nonlinear time evolution;
- no official NPZ;
- no observational claim;
- Repair18 remains FAIL.

## Nongating diagnostics

Report:

- solver termination status;
- `nfev/njev`;
- first-order optimality;
- active bounds;
- final least-squares cost;
- individual `delta L` and `delta R_t` correction norms/slopes;
- lambda=1 all-Y/beta exact constraint values.

These diagnostics cannot change a frozen classification.

## Terminal classifications

If provenance, coordinate-equivalence, field-freeze, or claim-boundary checks fail:

`NL1C7B4_REPAIR18A_IMPLEMENTATION_FAIL`.

If implementation gates pass but any exact solve, correction-order, or grid-amplitude gate fails:

`NL1C7B4_REPAIR18A_DIMENSIONLESS_RT_COORDINATE_FEASIBILITY_FAIL`.

If all seven gates pass:

`NL1C7B4_REPAIR18A_DIMENSIONLESS_RT_COORDINATE_FEASIBILITY_PASS`.

## Interpretation boundary

A PASS means that the Repair18 physical projection pair was feasible but the Repair18 physical-unit solver coordinate was numerically inadequate.

A PASS does not relabel Repair18 and does not certify an official projected state.

A PASS licenses Repair19 construction and independent certification of the lambda=1 projected state.

A FAIL is preserved as evidence that this one-coordinate numerical repair was insufficient. No solver setting or threshold may be retuned after the first Repair18a execution.
