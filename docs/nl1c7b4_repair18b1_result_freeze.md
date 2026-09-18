# NL1C7B4 Repair18b1 — local result freeze

## Status

Frozen local WSL diagnostic result from the first locked Repair18b1 execution.

Terminal classification:

`NL1C7B4_REPAIR18B1_LOCAL_PROJECTION_RANK_DEFICIENCY`

with

`SCIENCE_RC=2`.

Execution HEAD:

`a40447bac1a6fcff9884a987d60bb8f11f1db671`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `16340`
  - SHA-256:
    `8e0d796e0368372d0b4cf75a075fba12ebde154b651d74929e745118c1ca6dab`
- evaluator log:
  - bytes: `16786`
  - SHA-256:
    `7f16e5a9c2ce0d96e79cda289cfad7aa89155eb195455bd3707cf0ea740634ac`
- local runner log:
  - bytes: `20241`
  - SHA-256:
    `00ee5bae9b4fa1d079036f053e0facf0e71cede490dbfbfa7a56784ffde940b2`.

## Gate result

All four Repair18b1 gates PASS:

- R18B1_G1 frozen provenance
- R18B1_G2 frozen payload reproduction
- R18B1_G3 finite diagnostic
- R18B1_G4 claim boundary

Frozen Repair18b payload reproduction is exact:

- max absolute error: `0.0`
- max relative error: `0.0`
- all three scales reproduce exactly.

Repair18b remains classified IMPLEMENTATION_FAIL and is not relabelled.

## Jacobian result

For all scales 5,10,20 h^-1 Mpc:

- sparse and dense 2-point Jacobians agree exactly in the reported Frobenius metric:
  `relative_Frobenius_sparse_vs_dense = 0.0`;
- dense numerical rank is `508/510`;
- dense full-column-rank flag is false.

Singular-value ratios:

- scale 5:
  `sigma_min/sigma_max = 6.45649090133058e-20`;
- scale 10:
  `3.2080122441324997e-20`;
- scale 20:
  `2.551788846366277e-19`.

Thus the frozen local map has two deficient numerical directions under the preregistered rank rule.

## Interpretation

The result rules out the Repair18a sparse half-band Jacobian structure as the cause of the failed nonlinear closure.

The two-dimensional rank deficiency does not by itself imply lack of a constraint completion.

In fact, the dense bounded linear least-squares solve drives the linearized residual essentially to zero with no active bounds:

- scale 5 linear LSQ cost:
  `1.99861149247323e-18`;
- scale 10:
  `1.8707086529962613e-17`;
- scale 20:
  `6.256652128269264e-21`.

Therefore the parent residual is numerically compatible with the column space of the rank-deficient Jacobian. The deficiency is primarily a local non-uniqueness/null-space issue, not evidence of local linear inconsistency.

## Exact nonlinear probe

Applying the full dense linearized correction at alpha=1 yields:

- scale 5:
  - H `2.2075494135623804e-10`
  - M `6.409137112485408e-3`
- scale 10:
  - H `7.499680745150575e-10`
  - M `2.721523091739074e-1`
- scale 20:
  - H `1.7692173094108183e-10`
  - M `1.5226865731462237e-2`.

Thus the linearized step nearly annihilates the Hamiltonian residual but nonlinear momentum terms reappear at finite correction amplitude.

## Scientific meaning

Repair18b1 establishes:

1. the sparse Jacobian pattern is not the problem;
2. the local `(L,R_t)` projection map has exactly two numerically deficient directions;
3. the frozen residual nevertheless lies essentially in the Jacobian column space;
4. therefore the next issue is null-space/gauge/boundary non-uniqueness plus nonlinear momentum curvature, not a missing local linear correction direction.

No physics coefficient, source, sign, branch, eta, threshold, or point set was changed.

## Licensed continuation

A separately preregistered null-space characterization may now:

- compute the two right singular vectors associated with the deficient directions;
- characterize their `y_L` and `q_Rt` content;
- compare the two-dimensional null subspace across scales;
- test localization at center/outer boundary;
- project simple candidate global/boundary modes into the null subspace;
- compute the corresponding left near-null directions and compatibility of the parent residual.

The diagnostic must compare subspaces, not individual singular-vector signs/order, because the two null vectors may rotate within a nearly degenerate two-dimensional subspace.

Only after this characterization may a boundary/gauge fixing or null-space-projected nonlinear solver be preregistered.
