# Full-J 3D saturated constitutive closure — pre-data declaration

## Purpose

The locked 3D lattice-shell geometry POC classified

`FULLJ_3D_LATTICE_SHELL_GEOMETRY_POC_PASS`

and licensed a next 3D stochastic/statistical bridge diagnostic. The POC also showed `1+j` extremely close to two on the tested central branch. For `kind=simple`, `beta0=1`, the constitutive function obeys `j(x)=x/(2+x)` and approaches one for large `x`.

This milestone tests, before constructing any 3D Weyl power, if the nonlinear scalar-current operator is uniformly well approximated on the retained stochastic 3D shell domain by the saturated isotropic closure

`div[(1+j) grad chi] ~= 2 lap chi`.

The test is an operator/closure audit. It is not a 3D cosmological power-spectrum calculation and does not use a lensing likelihood.

## Locked ancestry and theory branch

Required locked ancestry:

- R2 PASS result: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- 1D Gaussian ensemble PASS result: `05e38b273f91eb04b7b4c8753731017d0ed839c1`
- 3D lattice-shell geometry PASS result: `ca6a102196055e27dc2b31379285bfc7aea1a35b`

Use only the fixed central branch

- `sigma=0`
- `kind=simple`
- `beta0=1.0`.

No deterministic `sigma/kind/beta0` theory-grid members are pooled into the stochastic ensemble.

## Radial evolving seed

Run the already locked central R2 trajectory once with unchanged `NX=128`, `NSTEP=4096` and retain the six positive radial `chi` mode variances at all nine locked checkpoints

`z = [6,5,4,3,2,1.5,1,0.5,0.2]`.

The 3D audit does not modify or feed back into that trajectory.

## 3D shell ensemble

Use the already certified lattice shells

`n = [3,5,8,10,15,20]`

with half-width `0.5` and the same periodic box convention.

Generate 16 independent angular Gaussian realizations using

`numpy.random.default_rng(20260914)`.

For every shell, assign independent complex coefficients

`g=(X+iY)/sqrt(2)`, `X,Y~N(0,1)`

to the positive lattice half-shell and impose Hermitian conjugates on the negative half-shell. Scale each shell so its ensemble radial variance equals the locked evolving `chi` variance at the corresponding redshift.

No realization rejection, clipping, or post-data seed replacement is allowed.

## Grids

Primary full-redshift audit: `64^3`.

Resolution controls at `z={6,1,0.2}`: repeat the same frozen angular coefficient realization on `80^3`.

The shell vectors themselves are unchanged between grids.

## Saturation diagnostics

For each `(z,realization)` define

`L3 = div[(1+j) grad chi]`,

`Lsat = 2 lap chi`,

and the weighted constitutive-flux mismatch

`eps_flux = ||(j-1) grad chi||_2 / max(||2 grad chi||_2,tiny)`.

Define the full operator mismatch

`eps_op = ||L3-Lsat||_2 / max(||L3||_2,||Lsat||_2,tiny)`.

For every retained radial shell define

`R_shell = P_shell(L3) / max(4 P_shell(lap chi),tiny)`.

Exact saturation gives `eps_flux=0`, `eps_op=0`, and `R_shell=1`.

## Frozen gates

### G1 — locked provenance/setup

Require exact locked ancestry, central branch, nine redshifts, six shell radii, seed `20260914`, `Nreal=16`, primary grid `64^3`, and control grid `80^3` only at `z={6,1,0.2}`.

### G2 — finite healthy constitutive operator

All fields, gradients, `j`, and operator outputs must be finite and `min(1+j)>0` in every evaluation.

### G3 — weighted flux saturation

Across all `64^3` evaluations require

- median `eps_flux <= 5e-3`,
- maximum `eps_flux <= 2e-2`.

### G4 — full operator saturation

Across all `64^3` evaluations require

- median `eps_op <= 5e-3`,
- maximum `eps_op <= 2e-2`.

### G5 — shell-power saturation

Across all `(z,shell)` cells after averaging over the 16 primary realizations require

- median `|R_shell-1| <= 1e-2`,
- maximum `|R_shell-1| <= 5e-2`.

### G6 — `64^3 -> 80^3` control consistency

At `z={6,1,0.2}` require

- maximum absolute change in mean `eps_op` between grids <= `5e-3`,
- maximum absolute change in any mean shell `R_shell` <= `1e-2`.

### G7 — no deterministic theory mixing

Only the central `sigma=0, simple, beta0=1` branch may enter this closure audit.

No gate may be changed after output is observed.

## Classification

PASS:

`FULLJ_3D_SATURATED_CONSTITUTIVE_CLOSURE_PASS`

FAIL:

`FULLJ_3D_SATURATED_CONSTITUTIVE_CLOSURE_FAIL`

INCOMPLETE:

`FULLJ_3D_SATURATED_CONSTITUTIVE_CLOSURE_INCOMPLETE`

## Interpretation lock

A PASS establishes that, on the locked central branch and retained shell/redshift/amplitude domain, the 3D nonlinear scalar-current operator is numerically equivalent within the frozen error budget to the isotropic saturated closure

`div[(1+j) grad chi] -> 2 lap chi`.

A PASS licenses a separately preregistered isotropic transfer construction using this quantified closure:

- `THREE_D_SATURATED_LAPLACIAN_CLOSURE_LICENSED=True`
- `THREE_D_ISOTROPIC_TRANSFER_CONSTRUCTION_LICENSED=True`.

A PASS still does not itself establish a 3D Weyl power spectrum or observational result. Therefore regardless of PASS:

- `THREE_D_ISOTROPIC_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`.
