# NL1C7B4 Repair18c — pre-data two-mode null-space characterization

## Status

Pre-data / pre-run diagnostic preregistration.

Repair18b1 is frozen as

`NL1C7B4_REPAIR18B1_LOCAL_PROJECTION_RANK_DEFICIENCY`

at result-freeze commit

`77090aef851f217f194c0b977afd361bbf016682`.

Frozen Repair18b1 result JSON:

- SHA-256:
  `8e0d796e0368372d0b4cf75a075fba12ebde154b651d74929e745118c1ca6dab`.

Repair18c does not solve or modify the nonlinear state. It characterizes the two-dimensional local null space already certified by Repair18b1.

## Scientific question

What are the two numerically deficient directions of the frozen local constraint map in the physical projection pair

- `L(r)`
- `R_t(r)`

and do they behave like global/boundary non-uniqueness modes rather than missing local correction directions?

## Frozen diagnostic domain

Unchanged from Repair18b1:

- eta = 0
- Y = `Simple`
- beta = `1.0`
- lambda = `1`
- Nr = `256`
- scales = `5,10,20 h^-1 Mpc`
- projection coordinates:
  - `y_L`
  - `q_Rt = delta R_t/(a H R_s)`
- all non-projection state fields frozen.

## Frozen Jacobian

At each scale reconstruct exactly the Repair18b1 dense 2-point Jacobian at x=0 from the same frozen residual

`F=[N_H/D_H^p,N_M/D_M^p]`.

Use SciPy default 2-point relative steps, no sparsity structure for the SVD Jacobian.

Require exact Repair18b1 reproduction before any null-space interpretation.

## SVD and rank

Compute

`J = U diag(s) V^T`

with NumPy full SVD.

Use the same frozen rank tolerance:

`tol = s_max * max(J.shape) * eps_float64`.

Require for every scale:

- numerical rank = `508`;
- deficient dimension = `2`;
- exactly the last two singular values lie at or below the frozen rank tolerance.

Define the right deficient subspace

`V0 = V[:, -2:]`

and left deficient subspace

`U0 = U[:, -2:]`.

All subspace diagnostics must be invariant to sign and ordering of the two singular vectors whenever possible.

## Right-null-space decomposition

Let

`P0 = V0 V0^T`.

Report the basis-invariant coordinate leverage

`ell_i = (P0)_{ii}`.

Because `trace(P0)=2`, report:

- total y_L leverage:
  `sum ell_i` over the y_L block;
- total q_Rt leverage:
  `sum ell_i` over the q_Rt block;
- corresponding fractions of the two-dimensional null-space leverage.

Report boundary localization separately for each block and for the combined coordinates.

For radial node windows

`k = 1,4,8,16`,

report the fraction of total null-space leverage in:

- first k non-center nodes;
- last k nodes.

Also report:

- maximum-leverage coordinate;
- its block (y_L or q_Rt);
- radial index;
- r/R_s;
- leverage value.

No localization threshold is imposed.

## Candidate-mode projections

For each scale construct and normalize the following deterministic right-coordinate vectors:

1. constant y_L, zero q_Rt;
2. zero y_L, constant q_Rt;
3. linear r/R_s in y_L, zero q_Rt;
4. zero y_L, linear r/R_s in q_Rt;
5. first-noncenter y_L coordinate basis vector;
6. first-noncenter q_Rt coordinate basis vector;
7. outermost y_L coordinate basis vector;
8. outermost q_Rt coordinate basis vector.

For every candidate v report the basis-invariant capture fraction

`||P0 v||^2 / ||v||^2`.

These are descriptive diagnostics only. No candidate is preregistered as the expected null mode.

## Cross-scale subspace comparison

The coordinate grids have the same Nr and the same normalized radial coordinate r/R_s.

Compare the two-dimensional right-null subspaces between each pair of scales using the singular values of

`V0_a^T V0_b`.

Report the two principal angles in degrees.

Do not compare individual singular-vector signs or ordering across scales.

No principal-angle threshold is imposed.

## Left-null compatibility

For the frozen parent residual F0 at each scale report

`c_left = ||U0^T F0||_2 / max(||F0||_2,tiny)`.

Also report the absolute two-component vector `U0^T F0`.

This tests compatibility of the parent residual with the Jacobian column space.

No compatibility threshold is used for terminal classification.

## Frozen gates

### R18C_G1 — exact frozen provenance

Require exact Repair18b1 JSON hash/classification/gates and all frozen parent hashes.

### R18C_G2 — exact Repair18b1 Jacobian reproduction

For each scale reproduce to absolute-or-relative `1e-12`:

- sigma_max;
- sigma_min;
- sigma_min/sigma_max;
- numerical rank;
- rank tolerance;
- parent normalized residual L2.

### R18C_G3 — exact two-mode deficiency

Require rank `508/510` and exactly two singular values at or below the frozen tolerance for all three scales.

### R18C_G4 — SVD/subspace consistency

Require:

- finite U,s,V;
- `||V0^T V0-I||_F <= 1e-12`;
- `||U0^T U0-I||_F <= 1e-12`;
- `|trace(P0)-2| <= 1e-12`;
- all leverage values finite and within numerical roundoff of [0,1].

### R18C_G5 — complete characterization

Require all preregistered leverage windows, eight candidate captures, three pairwise cross-scale comparisons, and left-null compatibility diagnostics to be present and finite.

### R18C_G6 — claim boundary

Repair18c must not:

- alter or solve the nonlinear state;
- choose boundary/gauge conditions;
- change the projection pair;
- change the Jacobian finite-difference rule;
- change the rank tolerance;
- change any source, coefficient, sign, branch, eta, point set, or historical threshold;
- write an NPZ;
- run nonlinear evolution;
- make an observational claim;
- relabel Repair18, Repair18a, Repair18b, or Repair18b1.

## Terminal classifications

If all six gates pass:

`NL1C7B4_REPAIR18C_TWO_MODE_NULLSPACE_CHARACTERIZED`.

Otherwise:

`NL1C7B4_REPAIR18C_IMPLEMENTATION_FAIL`.

## Interpretation boundary

Repair18c characterizes the certified two-dimensional local null space.

It does not decide a boundary/gauge fixing in advance.

After Repair18c is frozen, a subsequent preregistration may impose exactly two conditions only if they are motivated by the frozen null-space structure and then rerun the nonlinear closure without changing the historical `1e-7` constraint threshold.
