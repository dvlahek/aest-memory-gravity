# Full-J 3D lattice-shell geometry POC — pre-data declaration

## Purpose

The locked 1D Gaussian ensemble classified

`FULLJ_EVOLVING_WEYL_GAUSSIAN_1D_ENSEMBLE_PASS`

at result lock

`05e38b273f91eb04b7b4c8753731017d0ed839c1`.

That result establishes stochastic evolving-Weyl behavior only in the one-dimensional periodic embedding. The next unresolved issue is geometric: the nonlinear scalar-current operator contains

`div[(1+j_eff)|grad chi direction] = div[(1+j_eff) grad chi]`,

so in three dimensions mode coupling depends on angles between wavevectors. A one-dimensional spectrum cannot be converted into a three-dimensional isotropic Weyl power spectrum by a multiplicative shell factor.

This milestone is therefore a bounded **3D lattice-shell geometry POC**. It tests the isotropic shell representation and the three-dimensional nonlinear scalar-current operator on R2-informed radial amplitudes. It does not perform a full 3D time evolution and does not define cosmological `P_W(k,z)`.

## Locked inputs

Required ancestry:

- R2 evolving Weyl PASS result lock: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- corrected deterministic covariance result/scope lock: `87434c21866241b1b35588ec88e93e99a6f5db1a`
- 1D Gaussian stochastic PASS result lock: `05e38b273f91eb04b7b4c8753731017d0ed839c1`

The reference theory branch is fixed to

- `sigma = 0`
- `kind = simple`
- `beta0 = 1.0`.

The existing R2 equations are not modified.

## R2-informed radial seed

Run exactly one locked central-branch nonlinear R2 trajectory at the existing numerical settings (`NX=128`, `NSTEP=4096`). At the three frozen redshifts

`z = [2.0, 0.5, 0.2]`

extract the complex Fourier coefficients of the canonical `chi` field at the six locked input mode numbers

`n = [3,5,8,10,15,20]`.

For each shell, define the radial seed variance by the corresponding one-dimensional pair power

`V_chi(n,z) = 2 |chi_hat_n(z)|^2`.

Only these six radial seed variances are lifted into three dimensions. Nonlinear harmonics outside the six locked shells are not imported from the 1D trajectory.

## 3D lattice-shell construction

Use the same periodic box length as the locked 1D embedding. For target integer shell radius `n_j`, define the 3D lattice shell

`S_j = {q in Z^3 \ {0}: ||q|-n_j| <= 0.5}`.

The shell half-width is frozen at `0.5` lattice units.

For each shell use all lattice vectors in `S_j`. Hermitian pairs `q,-q` are generated from one independent half-lattice representative. For realization `r`, draw independent complex Gaussian coefficients

`g_rq = (X_rq + i Y_rq)/sqrt(2)`

with `X,Y ~ N(0,1)` using

`numpy.random.default_rng(20260913)`.

Use `Nreal = 8` realizations. The same realization coefficients are embedded at both spatial resolutions.

For shell `j` with `Npair_j` independent Hermitian pairs, choose normalized Fourier coefficients

`chi_hat(q) = sqrt(V_chi(j,z)) * g_rq / sqrt(2 Npair_j)`

for the independent representative and `chi_hat(-q)=conj(chi_hat(q))`.

Therefore the expected total real-field variance carried by shell `j` equals the locked radial seed variance `V_chi(j,z)`.

## Frozen spatial grids

Primary grid:

`N = 64` per Cartesian dimension.

Control grid:

`N = 80` per Cartesian dimension.

Both use the same physical box and the same lattice shell vectors. The nonlinear flux is dealiased using the standard componentwise two-thirds mask

`|m_x|, |m_y|, |m_z| <= N/3`.

All retained input shell vectors satisfy the primary-grid cutoff.

## 3D nonlinear operator

At each `(realization,z,N)`, compute spectrally

`grad chi`,

`x = ACC_CONV * |grad chi| / a`,

and on the fixed reference branch

`j = j_simple(x,beta0=1)`.

Then evaluate

`L3[chi] = div[(1+j) grad chi]`

with the dealiased flux. Also evaluate the linear comparator

`L0[chi] = lap chi`.

No metric closure, Weyl projection, new interpolation parameter, angular response fit, or effective 3D Poisson prescription is introduced here.

## Frozen shell diagnostics

For each target shell and redshift report ensemble-mean shell powers of

- `L3`,
- `L0`,
- nonlinear excess `L3-L0`,
- ratio `P(L3)/P(L0)` when the denominator is nonzero.

Also report the power-weighted directional second moment

`M_ab = sum_q P(q) qhat_a qhat_b / sum_q P(q)`

for the `L3` output on each shell.

## Frozen gates

### G1 — provenance and frozen setup

Require all three result locks in ancestry, the fixed central theory branch, exact redshift list, exact shell radii, `Nreal=8`, seed `20260913`, and grids `64/80`.

### G2 — shell geometry isotropy

For every shell, before using dynamics:

- second-moment tensor residual `max|<qhat_a qhat_b>-delta_ab/3| <= 1e-12`,
- fourth-moment deviations `|<qhat_x^4>-1/5|` and `|<qhat_x^2 qhat_y^2>-1/15|` each <= `1e-2`.

This checks that the finite-width lattice shells approximate isotropic angular sampling through fourth order.

### G3 — axial 3D-to-1D reduction

For a field depending only on `x` with the six locked mode numbers, evaluate the same constitutive operator in 1D and in 3D. Require the relative L2 difference between the 1D output and any 3D `(y,z)` slice to be <= `1e-12`.

### G4 — cubic rotation equivariance

For one frozen realization at `z=0.2` on `N=64`, permute the spatial axes cyclically, reevaluate `L3`, rotate the output back, and require relative L2 mismatch <= `1e-12`.

### G5 — finite healthy 3D operator

All `8 x 3 x 2 = 48` stochastic operator evaluations must be finite. Require finite `x`, `j`, `L3`, `L0`, and strictly positive `min(1+j)`.

### G6 — N64-to-N80 shell-power convergence

For each of the 18 `(z,shell)` cells compare ensemble-mean `L3` shell power:

`d64_80 = |P80-P64| / max(P80,P64,tiny)`.

Require

- median `d64_80 <= 0.15`,
- maximum `d64_80 <= 0.35`.

No threshold changes are allowed after results.

### G7 — output angular isotropy

For the ensemble-mean N=80 `L3` shell power, require across all `(z,shell)` cells

`max_ab |M_ab-delta_ab/3| <= 0.08`.

This is a finite-ensemble POC isotropy gate, not a precision cosmological isotropy claim.

## Classification

PASS:

`FULLJ_3D_LATTICE_SHELL_GEOMETRY_POC_PASS`

FAIL:

`FULLJ_3D_LATTICE_SHELL_GEOMETRY_POC_FAIL`

INCOMPLETE if required locked inputs or corrected CLASS environment are unavailable:

`FULLJ_3D_LATTICE_SHELL_GEOMETRY_POC_INCOMPLETE`.

## Interpretation lock

A PASS establishes that the R2-informed nonlinear scalar-current operator admits a finite, rotation-equivariant, approximately isotropic and spatially converged 3D lattice-shell representation on the six retained radial shells.

A PASS does **not** establish a fully evolved 3D AeST cosmology or a three-dimensional Weyl power spectrum. The radial amplitudes are imported from the locked 1D R2 trajectory and only the 3D nonlinear geometry is tested.

Therefore, regardless of PASS:

- `THREE_D_LATTICE_SHELL_GEOMETRY_TESTED=True`
- `THREE_D_EVOLVING_STOCHASTIC_ENSEMBLE_LICENSED=False` unless every gate passes
- `THREE_D_ISOTROPIC_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

If PASS, the next milestone is a separately preregistered full 3D evolving stochastic ensemble using the certified lattice-shell geometry.