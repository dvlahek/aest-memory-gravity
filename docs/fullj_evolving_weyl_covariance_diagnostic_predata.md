# Full-J evolving Weyl covariance diagnostic — pre-data declaration

## Purpose

This milestone is allowed only because the locked R2 result classified

`FULLJ_EVOLVING_WEYL_BRIDGE_R2_PASS`

and explicitly set

`EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_LICENSED=True`.

The purpose is to construct and audit an evolving covariance object from the already locked R2 Weyl outputs without promoting the 27 deterministic theory-grid members to a cosmological stochastic ensemble.

## Input lock

Required input:

`results/fullj_evolving_weyl_bridge_r2.npz`

with the R2 result classification `FULLJ_EVOLVING_WEYL_BRIDGE_R2_PASS` and R2 implementation head

`970b5fd1612e52aa3adff98d6d0b0a6084a40cf7`.

Expected arrays:

- 27 member names,
- 9 redshift checkpoints,
- Fourier mode numbers 0..32,
- complex `W` with shape `(27,9,33)`,
- the locked member grid `sigma in {-1,0,+1}`, `kind in {simple,exponential,sharp}`, `beta0 in {1,0.5,0.1}`.

No R2 trajectory is rerun or modified.

## Primary covariance definition

The 27 co-primary members are not treated as 27 random cosmological realizations. The model/interpolation choices `(kind,beta0)` are systematic theory-grid directions.

For each fixed `(kind,beta0,z)` the three locked sigma members define a small phase-conditioned diagnostic sample. Let

`W_sigma(z)`

be the complex 33-mode Weyl vector for `sigma=-1,0,+1`, and let

`Wbar(z) = (1/3) sum_sigma W_sigma(z)`.

Define the centered phase-conditioned covariance

`C_W(z) = (1/(3-1)) sum_sigma [W_sigma-Wbar] [W_sigma-Wbar]^dagger`.

This is computed separately for all 9 `(kind,beta0)` branches and all 9 redshift checkpoints, giving 81 covariance matrices of shape 33x33.

Because only three sigma samples exist, each centered covariance has rank at most two. This rank limit is structural and is not interpreted as a physical low-rank cosmological field.

## Secondary theory-grid sensitivity diagnostic

At each redshift, a separate centered covariance over all 27 members may be reported as a theory-grid sensitivity object. It is explicitly labeled non-stochastic and is not used to define cosmological power.

## Frozen diagnostics

For every primary covariance matrix report:

- Hermiticity relative residual,
- minimum eigenvalue divided by max absolute eigenvalue,
- trace,
- effective numerical rank using eigenvalues > `1e-12 * max_eigenvalue`,
- diagonal variance vector `diag(C_W)`,
- Frobenius off-diagonal fraction `||C-diag(C)||_F / ||C||_F`,
- covariance reconstruction identity residual between `trace(C_W)` and the centered sample mean-square norm.

Across the 81 matrices report min/median/max summaries and redshift evolution of the covariance trace and off-diagonal fraction for each `(kind,beta0)` branch.

For the secondary 27-member theory-grid covariance report the same algebraic health quantities, but do not call its diagonal a cosmological power spectrum.

## Frozen gates

### G1 — locked R2 provenance

Require:

- R2 classification PASS,
- R2 result/implementation ancestry present,
- exact 27 x 9 x 33 expected Weyl array shape,
- all 27 expected member labels present exactly once.

### G2 — finite covariance construction

All input Weyl values and all 81 primary covariance matrices must be finite.

### G3 — Hermiticity

For every primary and secondary covariance matrix:

`||C-C^dagger|| / max(||C||, tiny) <= 1e-12`.

### G4 — positive semidefinite consistency

For every covariance matrix:

`lambda_min / max(|lambda|, tiny) >= -1e-12`.

No eigenvalue clipping is allowed before this gate.

### G5 — sample-covariance reconstruction identity

For every primary covariance matrix, the relative mismatch between

`trace(C_W)`

and

`(1/(N-1)) sum_sigma ||W_sigma-Wbar||^2`

must be <= `1e-12`.

### G6 — structural phase-rank bound

Each 3-sample centered primary covariance must have numerical rank <= 2 using the frozen `1e-12 * lambda_max` threshold.

This is an algebraic consistency gate, not a physics claim.

## Classification

PASS:

`FULLJ_EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_PASS`

FAIL:

`FULLJ_EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_FAIL`

INCOMPLETE if the locked R2 input or expected member grid is unavailable:

`FULLJ_EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_INCOMPLETE`

## Interpretation lock

A PASS establishes only that the locked evolving R2 Weyl outputs support a finite, Hermitian, positive-semidefinite, internally consistent phase-conditioned covariance diagnostic across the retained redshifts and theory-grid branches.

A PASS does **not** establish a cosmological random-phase Weyl power spectrum because the primary sample has only the three locked sigma members and `(kind,beta0)` are systematic theory choices rather than random draws.

Therefore, regardless of PASS:

- `EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_TESTED=True`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`
- `THEORY_GRID_IS_COSMOLOGICAL_ENSEMBLE=False`

The next possible milestone after a PASS is a separately preregistered stochastic/random-phase ensemble construction sufficient to define and converge an evolving Weyl power spectrum. Only after that may a line-of-sight lensing calculation be considered.