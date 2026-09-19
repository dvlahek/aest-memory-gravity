# NL1C7B4 Repair19b — pre-data direct reduced linear feasibility audit

## Status

Pre-data / pre-run diagnostic preregistration.

Repair19a is frozen as

`NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_INFEASIBILITY`

at result-freeze commit

`e8f6e93f17066cbfb2355dc64f5b36e91a06f527`.

Frozen Repair19a result JSON:

- bytes: `22475`
- SHA-256:
  `b9b79d1fe12dff7b59d80260572129b746322412bf96ff214204f9651bd77761`.

Repair19b is diagnostic only.

## Scientific question

Was the Repair19a linear-feasibility failure caused by the fixed LSMR iteration ceiling, or does the same frozen Y4=0/Qmean=0 reduced linear system remain incompatible under a direct least-squares solve?

Repair19b does not change the physical subspace, Jacobian rule, residual, threshold, or state.

## Frozen domain

Exactly the six lambda=1 canonical cases:

- eta=0
- Y=Simple
- beta=1
- scales=5,10,20 h^-1 Mpc
- Nr=256,512.

## Frozen parent and Jacobian

Reuse exactly the Repair19a parent-state construction and residual normalization.

For each case compute the full physical grouped two-point Jacobian at x=0 using the frozen Repair18a half-band-16 pattern.

For Nr=256 additionally reproduce the frozen Repair18b1 dense/grouped Jacobian fidelity fact through the existing parent/evaluator provenance; no new dense finite-difference rule is introduced.

## Frozen coordinate bases

Use exactly the two Repair19a bases:

- `B_chain`
- `B_orth`.

Both span the same exact Y4=0/Qmean=0 physical subspace.

Form:

- `J_chain = J_x B_chain`
- `J_orth = J_x B_orth`.

Densify only these reduced matrices for direct LAPACK solution.

## Direct least-squares solver

For each basis/case solve

`min ||F0 + J_red dz||_2`

using SciPy `scipy.linalg.lstsq` with:

- LAPACK driver: `gelsd`
- cond: `max(J_red.shape) * eps_float64`
- check_finite: true.

The rank cutoff therefore follows the same relative machine-precision rule used in the frozen SVD diagnostics.

Compute:

- returned numerical rank;
- singular-value maximum/minimum over retained spectrum;
- direct residual L2;
- relative direct residual;
- reduced-coordinate norm;
- physical correction `dx=B dz`;
- maximum |y_L| and |q_Rt|;
- exact gauge residuals.

## Independent direct-driver cross-check

For the same matrix/right-hand side also solve with:

- `scipy.linalg.lstsq`
- LAPACK driver: `gelsy`
- same cond.

No Gelsy result is used as the primary solution.

It is an independent deterministic cross-check of the physical correction.

Require chain/orth/GELSD/GELSY physical corrections to agree under the gates below.

## Frozen feasibility threshold

Retain the Repair19a threshold exactly:

`||F0 + J_red dz||_2 / max(||F0||_2,tiny) <= 1e-6`.

No threshold relaxation is allowed.

## Gates

### R19B_G1 — exact frozen provenance

Require exact frozen hashes/classes for Repair19a and all imported parents.

Repair19 and Repair19a remain unchanged.

### R19B_G2 — exact frozen subspace/basis reproduction

Reproduce both Repair19a basis audits for Nr=256 and Nr=512 to abs-or-rel `1e-12`.

### R19B_G3 — exact parent/Jacobian input reproduction

Reproduce all six Repair19a parent initial residual L2 values and grouped Jacobian shapes/nnz exactly.

### R19B_G4 — finite direct solves

Require all 24 direct solutions:

- 6 cases x 2 bases x 2 LAPACK drivers

finite and returned with full reduced-column rank.

### R19B_G5 — direct gauge-fixed linear feasibility

For the primary GELSD solution require both bases and all six cases to satisfy the unchanged relative residual threshold `1e-6`.

### R19B_G6 — basis-invariant physical correction

For every case require

`||dx_chain_gelsd-dx_orth_gelsd||_2 / max(norms,tiny) <= 1e-8`.

### R19B_G7 — LAPACK-driver physical agreement

For each basis/case require

`||dx_gelsd-dx_gelsy||_2 / max(norms,tiny) <= 1e-8`.

### R19B_G8 — exact gauge satisfaction

For all primary GELSD physical corrections require

- `|Y4| <=1e-12`
- `|Qmean| <=1e-12`.

### R19B_G9 — LSMR-stagnation diagnosis

If G5-G8 all pass, require every frozen Repair19a LSMR primary residual to exceed the corresponding direct GELSD residual by at least a factor of `1e3`.

This gate tests the specific numerical-stagnation hypothesis.

### R19B_G10 — claim boundary

Repair19b must not:

- run nonlinear least squares;
- evaluate or accept a nonlinear corrected state;
- write an NPZ;
- modify a physical field or parent artifact;
- change Y4/Qmean;
- alter any source, coefficient, sign, branch, eta, radial point set, or historical threshold;
- remove cases;
- run time evolution;
- make an observational claim;
- relabel Repair19 or Repair19a.

## Terminal classifications

If implementation/provenance/completeness gates G1-G4, G8, and G10 fail:

`NL1C7B4_REPAIR19B_IMPLEMENTATION_FAIL`.

Else if G5 fails:

`NL1C7B4_REPAIR19B_DIRECT_LINEAR_INFEASIBILITY`.

Else if G6 or G7 fails:

`NL1C7B4_REPAIR19B_DIRECT_SOLVER_COORDINATE_DISAGREEMENT`.

Else if G9 fails:

`NL1C7B4_REPAIR19B_LSMR_STAGNATION_NOT_ESTABLISHED`.

Else:

`NL1C7B4_REPAIR19B_LSMR_STAGNATION_IDENTIFIED`.

## Interpretation boundary

A terminal LSMR-stagnation identification certifies only that the same frozen gauge-fixed linearized problem is feasible under a direct solver and that Repair19a failed because the iterative linear solve did not converge sufficiently.

It does not certify nonlinear exact constraint closure.

Only after that result may a separately preregistered nonlinear solver use a direct gauge-fixed Gauss-Newton/Newton step.
