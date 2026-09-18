# NL1C7B4 Repair18b1 — pre-data Boolean provenance harness repair

## Status

Pre-data / pre-run preregistration.

Repair18b is frozen as

`NL1C7B4_REPAIR18B_IMPLEMENTATION_FAIL`

at result-freeze commit

`3edf1b11992008d7be383692369f28614ef94d6b`.

Repair18b1 is harness-only. It does not modify the diagnostic physics, Jacobian construction, residual, numerical-rank rule, linearized probe, fields, scales, branch, or thresholds.

## Frozen Repair18b result

Repair18b JSON:

- bytes: `15558`
- SHA-256:
  `cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855`.

Repair18b result freeze:

- file:
  `docs/nl1c7b4_repair18b_result_freeze.md`.

The frozen Repair18b summary is:

- `finite_all = true`;
- `structure_match_all = true`;
- `full_rank_all = false`;
- `provenance_ok = false`;
- `max_relative_Frobenius_sparse_vs_dense = 0.0`;
- `min_sigma_min_over_sigma_max = 3.2080122441324997e-20`.

All three scales reported numerical rank `508/510`.

## Harness defect

The frozen imported function

`nl1c7b.initial_constraint_certification_repair01.build_nonK()`

returns the symbolic dictionary identity as a Boolean.

Repair18b erroneously required:

`kidentity <= 1e-12`.

For the valid Boolean value `True`, Python evaluates this as

`1 <= 1e-12`,

which is false.

Repair18b1 changes exactly that provenance predicate to:

`bool(kidentity)`.

No other scientific or numerical change is permitted.

## Frozen diagnostic

Unchanged from Repair18b:

- eta = 0;
- canonical Y = Simple;
- beta = 1;
- lambda = 1;
- Nr = 256;
- scales = 5, 10, 20 h^-1 Mpc;
- physical pair `(L,R_t)`;
- solver coordinates `(y_L,q_Rt)`;
- dense 2-point Jacobian;
- sparse/grouped 2-point Jacobian with Repair18a half-band-16 pattern;
- sparse-vs-dense Frobenius match threshold `1e-6`;
- numerical-rank tolerance
  `sigma_max * max(shape) * eps_float64`;
- bounded dense linearized probe with `lsq_linear`;
- alpha = 1, 1/2, 1/4, 1/8.

## R18B1_G1 — frozen provenance

Require exact hashes/classes for Repair15a, Repair16, Repair17, Repair18, Repair18a, and frozen Repair18b JSON.

Require Repair18b itself to remain classified IMPLEMENTATION_FAIL with only the provenance summary false.

Require exact Boolean symbolic identity:

`bool(kidentity) is True`.

## R18B1_G2 — frozen payload reproduction

Recompute the complete Repair18b diagnostic.

For each of the three scales require reproduction of:

- relative sparse-vs-dense Frobenius difference;
- dense numerical rank;
- sigma_max;
- sigma_min;
- sigma_min/sigma_max;
- all four deterministic operator-action differences;
- linearized correction max coordinate;
- all four exact nonlinear alpha-probe H/M values;
- all four alpha-probe normalized residual L2 values.

Scalar values must agree with the frozen Repair18b JSON to absolute-or-relative `1e-12`.
Integer and Boolean values must agree exactly.

## R18B1_G3 — finite diagnostic

Require all recomputed residuals and Jacobians finite.

## R18B1_G4 — claim boundary

Repair18b1 must not:

- relabel Repair18b;
- change the physical projection pair;
- change Jacobian methods;
- change the sparse pattern;
- change the rank tolerance;
- change the linear solver;
- change any alpha;
- change any physics source, coefficient, sign, branch, eta, point set, or threshold;
- write an NPZ;
- run nonlinear evolution;
- make an observational claim.

## Terminal classifications

After G1-G4 pass, apply the frozen Repair18b interpretation logic to the reproduced payload:

1. if any sparse-vs-dense Frobenius mismatch exceeds `1e-6`:

   `NL1C7B4_REPAIR18B1_SPARSE_JACOBIAN_STRUCTURE_MISMATCH`

2. else if any dense Jacobian is not full column rank:

   `NL1C7B4_REPAIR18B1_LOCAL_PROJECTION_RANK_DEFICIENCY`

3. else:

   `NL1C7B4_REPAIR18B1_FULL_RANK_JACOBIAN_DIAGNOSTIC_PASS`

If any harness/provenance/reproduction/serialization check fails:

`NL1C7B4_REPAIR18B1_IMPLEMENTATION_FAIL`.

## Interpretation boundary

A rank-deficiency classification means only that the frozen local linear map has fewer than 510 numerically independent directions under the preregistered rank rule.

It does not prove global non-existence of a nonlinear constraint completion.

Repair18b already suggests exactly two deficient directions, so a subsequent separately preregistered null-space characterization may identify if they are boundary/global integration modes before any nonlinear solver is redesigned.
