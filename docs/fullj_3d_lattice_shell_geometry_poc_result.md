# Full-J 3D lattice-shell geometry POC — locked result

## Classification

The preregistered 3D lattice-shell geometry diagnostic completed with

`FULLJ_3D_LATTICE_SHELL_GEOMETRY_POC_PASS`.

All seven frozen gates passed.

## Locked numerical result

The test used the central theory branch `sigma=0`, `kind=simple`, `beta0=1`, target redshifts `z={2,0.5,0.2}`, shell radii `n={3,5,8,10,15,20}`, 8 frozen Gaussian angular realizations, and grids `64^3` and `80^3`.

Key results:

- shell second-moment isotropy residuals were at floating-point level, with the largest fourth-moment shell error `6.079096e-3`;
- exact axial 3D-to-1D reduction residual: `0.0`;
- cubic rotation equivariance relative residual: `8.214650514193e-16`;
- all 48 three-dimensional operator evaluations on each grid were finite;
- minimum `1+j`: `1.9998868332118744`;
- `64^3 -> 80^3` shell-power convergence: median `7.711853135549371e-12`, maximum `2.744518446085538e-10`;
- maximum output angular-isotropy residual: `0.03568806618633391`.

The result file reports `P_L3/P_L0` very close to four across all retained cells. This is not interpreted as a generic geometric factor. In this diagnostic `L3 = div[(1+j) grad chi]` and `L0 = lap chi`; since the central `simple,beta0=1` branch is already very close to the saturated value `j=1` on the tested domain, `L3` is correspondingly close to `2 L0`, giving a power ratio near four.

## Gate status

- G1 provenance and frozen setup: PASS
- G2 shell geometry isotropy: PASS
- G3 axial 3D-to-1D reduction: PASS
- G4 cubic rotation equivariance: PASS
- G5 finite healthy 3D operator: PASS
- G6 `64^3 -> 80^3` shell-power convergence: PASS
- G7 output angular isotropy: PASS

## Interpretation lock

This PASS establishes that the retained nonlinear scalar-current operator can be evaluated consistently on isotropic three-dimensional lattice shells, reproduces the one-dimensional axial limit, respects cubic rotations, is numerically converged between the frozen grids, and produces acceptably isotropic shell output for the tested stochastic angular realizations.

It therefore licenses the next separately preregistered three-dimensional stochastic/statistical bridge diagnostic:

`THREE_D_EVOLVING_STOCHASTIC_ENSEMBLE_LICENSED=True`.

It does **not** establish a fully evolved 3D cosmological Weyl power spectrum. The radial amplitudes were seeded from the locked one-dimensional R2 trajectory and the 3D operator was evaluated at selected snapshots; no full three-dimensional time evolution was performed.

Therefore the following remain false:

- `THREE_D_ISOTROPIC_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

The next milestone will first test if the central physical branch is uniformly in the saturated constitutive regime `j≈1` over the full retained redshift interval and stochastic shell ensemble. If certified, this can collapse the expensive angular nonlinear coupling to a controlled isotropic Laplacian closure before constructing 3D Weyl power.