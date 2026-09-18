# NL1C7B4 Repair18b — pre-data Jacobian-fidelity diagnostic

## Status

Pre-data / pre-run diagnostic preregistration.

Frozen parent results:

- Repair18:
  `NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_FAIL`
- Repair18a:
  `NL1C7B4_REPAIR18A_DIMENSIONLESS_RT_COORDINATE_FEASIBILITY_FAIL`

Repair18a result freeze:

- commit:
  `8cfce926a9075d77dd73c5bb5242c9d3e26b74ad`
- file:
  `docs/nl1c7b4_repair18a_result_freeze.md`
- blob:
  `21f12cdf27abc560812dabb1c6b1a3b9e41e14f5`
- Repair18a JSON SHA-256:
  `29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782`.

Repair18a demonstrated that dimensionless reparameterization of `delta R_t` did not close the exact constraints and did not materially change the physical correction norm.

Repair18b is diagnostic only. It does not write a state, change a physical projection variable, or change a science threshold.

## Diagnostic question

Is the Repair18/18a failure caused by the sparse finite-difference Jacobian approximation used by the locked least-squares solver, or does the local linearized constraint map in the physical pair

- `L(r)`
- `R_t(r)`

itself fail to provide a well-conditioned descent direction?

## Frozen diagnostic domain

Use only the canonical branch:

- Y = `Simple`
- beta = `1.0`
- eta = 0.

Use only:

- lambda = 1
- Nr = 256
- scales = `5,10,20 h^-1 Mpc`.

No 512 solve is required for this numerical diagnostic because Repair18 and Repair18a already established two-grid correction-amplitude agreement.

The parent state is the frozen Repair15a state used by Repair16/17/18/18a.

The solver coordinates are exactly Repair18a:

- `y_L`
- `q_Rt = delta R_t/(a H R_s)`.

The physical projection map and bounds are unchanged.

## Frozen residual

At each scale use the exact Repair18a normalized signed residual

`F(x) = [N_H/D_H^p, N_M/D_M^p]`

on all non-center points, with the parent denominators frozen before perturbing `x`.

No residual component, source, point, or denominator may be removed or reweighted.

## Jacobians to compare

At `x=0` construct two numerical Jacobians using SciPy's finite-difference machinery and the same residual function.

### J_dense

Unstructured 2-point finite difference:

- method: `2-point`
- default SciPy relative-step rule
- no sparsity structure.

### J_sparse

Sparse/grouped 2-point finite difference:

- method: `2-point`
- default SciPy relative-step rule
- exact frozen Repair18a `jac_pattern(n)`.

The comparison therefore isolates the effect of the declared sparsity/grouping pattern while leaving the finite-difference rule unchanged.

## Frozen Jacobian-fidelity metrics

For every scale report:

- relative Frobenius difference
  `||J_sparse-J_dense||_F / max(||J_dense||_F, tiny)`;
- relative operator-action difference on four deterministic vectors:
  1. all-one `y_L`, zero `q_Rt`;
  2. zero `y_L`, all-one `q_Rt`;
  3. sinusoidal `y_L`, zero `q_Rt`;
  4. zero `y_L`, sinusoidal `q_Rt`;
- dense singular values:
  - `sigma_max`;
  - `sigma_min`;
  - `sigma_min/sigma_max`;
- numerical rank using
  `tol = sigma_max * max(J.shape) * eps_float64`.

The fidelity flag is diagnostic and frozen before the run:

`jacobian_structure_match = (relative_Frobenius_difference <= 1e-6)`.

This threshold does not affect any historical science classification.

## Frozen linearized feasibility probe

Using `J_dense`, compute the bounded linear least-squares correction

`dx_lin = argmin ||F(0)+J_dense dx||_2`

with the same coordinate bounds:

- `y_L in [-0.5,0.5]`
- `q_Rt in [-0.5,0.5]`.

Use `scipy.optimize.lsq_linear` with:

- method `trf`
- tol `1e-12`
- max_iter `500`
- no multistart.

Evaluate the exact nonlinear Repair18a residual after the deterministic amplitudes

- alpha = 1
- alpha = 1/2
- alpha = 1/4
- alpha = 1/8

applied to `dx_lin`.

Report for each alpha:

- exact max epsilon H;
- exact max epsilon M;
- residual L2 norm in the frozen parent normalization;
- positivity of L;
- exact Q error;
- bound status.

No alpha is selected after the run. All four are diagnostic.

## Frozen interpretation logic

Repair18b does not certify a nonlinear state.

The following labels are descriptive diagnostic outcomes.

### Sparse-structure mismatch

If any scale has

`relative_Frobenius_difference > 1e-6`,

classify:

`NL1C7B4_REPAIR18B_SPARSE_JACOBIAN_STRUCTURE_MISMATCH`.

This licenses a later separately preregistered sparse-pattern repair.

### Sparse structure consistent, locally rank deficient

If all sparse/dense Jacobians match but any scale has numerical rank below full column rank, classify:

`NL1C7B4_REPAIR18B_LOCAL_PROJECTION_RANK_DEFICIENCY`.

This is evidence that the minimal local pair has a null/near-null direction under the frozen residual at that state. It does not prove global non-existence.

### Sparse structure consistent and full rank

If all sparse/dense Jacobians match and all three dense Jacobians are numerically full rank, classify:

`NL1C7B4_REPAIR18B_FULL_RANK_JACOBIAN_DIAGNOSTIC_PASS`.

In this case report the exact nonlinear residual after all four linearized amplitudes. A later solver repair may use this information only through a separately preregistered method.

### Implementation failure

If provenance, finite evaluation, Jacobian construction, deterministic-vector checks, or result serialization fails:

`NL1C7B4_REPAIR18B_IMPLEMENTATION_FAIL`.

## Claim boundary

Repair18 remains FAIL.
Repair18a remains FAIL.

Repair18b must not:

- change the 1e-7 historical constraint threshold;
- change any AeST source, coefficient, or sign;
- change Y/beta;
- change eta;
- remove radial points;
- clip K;
- linearize Q;
- write an official or diagnostic corrected NPZ;
- run nonlinear time evolution;
- make an observational claim;
- relabel Repair16, Repair18, or Repair18a.

Repair18b is a numerical-identifiability diagnostic for the frozen minimal projection pair only.
