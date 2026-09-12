# Full-J isotropic Weyl transfer nodes — pre-data declaration

## Purpose

The locked chain now contains:

- evolving R2 bridge PASS,
- Gaussian 1D ensemble PASS,
- 3D lattice-shell geometry POC PASS,
- 3D saturated constitutive closure PASS.

The last result licenses an isotropic transfer construction on the locked central theory branch because, over the tested shell/redshift domain,

`div[(1+j) grad chi]`

is numerically equivalent to

`2 Laplacian chi`

to much better accuracy than the frozen closure tolerances. This milestone constructs and independently checks the six **discrete radial Weyl transfer nodes**. It does not interpolate them into a continuous spectrum and does not perform lensing.

## Required ancestry

- R2 result lock: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- Gaussian 1D result lock: `05e38b273f91eb04b7b4c8753731017d0ed839c1`
- 3D geometry result lock: `ca6a102196055e27dc2b31379285bfc7aea1a35b`
- saturated closure result lock: `f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f`

Reference theory branch remains exactly

- `sigma = 0`
- `kind = simple`
- `beta0 = 1.0`.

The six radial nodes remain the locked values

`k/h = [0.03,0.05,0.08,0.10,0.15,0.20] Mpc^-1`

with mode numbers

`n = [3,5,8,10,15,20]`.

The nine redshifts remain

`z = [6,5,4,3,2,1.5,1,0.5,0.2]`.

## Transfer normalization

The existing real-space construction is

`field(x,z) = sum_j MODE_AMP_j * T_j(z) * cos(k_j x + PHASE_j)`

with

`MODE_AMP_j = sqrt(2 * Delta ln k_j * P_R(k_j))`.

For a real field, the positive Fourier coefficient at locked mode number `n_j` is therefore

`W_hat_j = (MODE_AMP_j / 2) * T_W(k_j,z) * exp(i PHASE_j)`.

Define the reconstructed nonlinear Weyl transfer node by

`T_W_R2(k_j,z) = 2 * W_hat_j * exp(-i PHASE_j) / MODE_AMP_j`.

The direct corrected-CLASS reference node is

`T_W_CLASS(k_j,z) = phi_CLASS(k_j,z) + psi_CLASS(k_j,z)`.

At the initial checkpoint `z=6`, R2 uses the corrected CLASS state directly, so this gives an independent normalization check.

A discrete dimensionless Weyl power node may then be reported as

`Delta_W^2(k_j,z) = P_R(k_j) * |T_W_R2(k_j,z)|^2`,

with dimensional node

`P_W(k_j,z) = 2*pi^2/k_j^3 * Delta_W^2(k_j,z)`.

These are discrete nodes only. No interpolation/extrapolation is licensed by this milestone.

## Frozen primary construction

Run one standard central six-mode nonlinear R2 evolution at `NX=128`, `NSTEP=4096` and extract the six matching Fourier coefficients of the evolving Weyl field at all nine checkpoints.

## Frozen single-mode separability audit

For each of the six modes, repeat the same R2 evolution with the realization basis containing only that one locked input mode, with its original `MODE_AMP` and `PHASE`. All CLASS/canonical/effective-fluid fields use the same one-mode basis consistently.

For each `(k,z)` compare the transfer node from the single-mode run with the matching node from the simultaneous six-mode run.

Also measure off-target Fourier leakage in each single-mode Weyl output over positive modes `1..32`.

## Frozen amplitude-homogeneity control

For anchor modes

`n = [3,10,20]`

repeat the single-mode construction with basis amplitudes scaled by

`0.5` and `2.0`.

The reconstructed transfer divides by the applied basis amplitude, so an effectively linear saturated closure must return the same transfer node.

No amplitude factor is fitted after seeing outputs.

## Gaussian-ensemble cross-check

Reproduce the frozen Gaussian coefficient draw from the locked 1D ensemble (`seed=20260912`, `N=32`) without rerunning those 32 trajectories.

Using the six constructed transfer nodes and the exact finite-sample coefficient variances, predict the low/mid/high nonlinear-to-CLASS bandpower ratios for the same three frozen bands and nine redshifts. Compare them with the ratios stored in the completed Gaussian 1D result JSON if that file is available locally.

This cross-check is validation only. It does not redefine any transfer node.

## Frozen gates

### G1 — provenance/setup

All required locks must be ancestors of HEAD and all frozen modes/redshifts/reference-branch/numerical settings must match exactly.

### G2 — finite/constraint health

The six-mode run, all six single-mode runs, and all six amplitude-control runs must be finite at all nine checkpoints. Require canonical constraint residual <= `1e-10` and metric Hamiltonian/momentum/shear residuals <= `1e-8`.

### G3 — initial CLASS normalization

At `z=6`, for all six modes require

`|T_W_R2 - T_W_CLASS| / max(|T_W_CLASS|,tiny) <= 5e-3`.

### G4 — transfer phase consistency

After removing the frozen spatial phase, require

`max |Im(T_W_R2)| / max(|T_W_R2|,tiny) <= 1e-8`.

The reported physical transfer is the real part only after this gate passes.

### G5 — single-mode separability

Across all 54 `(k,z)` cells require relative difference between single-mode and six-mode transfer nodes

- median <= `5e-4`,
- maximum <= `5e-3`.

### G6 — off-target leakage

For each single-mode output define leakage as total positive-mode power outside the target mode divided by total positive-mode power. Require maximum leakage across all checkpoints/modes <= `5e-3`.

### G7 — amplitude homogeneity

Across the three anchor modes, both scale factors, and all nine redshifts require relative transfer change relative to the unit-amplitude single-mode run

- median <= `5e-4`,
- maximum <= `5e-3`.

### G8 — Gaussian ensemble reconstruction

If the locked local Gaussian 1D result JSON is available, require predicted versus recorded nonlinear/CLASS band-ratio relative difference

- median <= `5e-3`,
- maximum <= `2e-2`.

If that local result file is unavailable, classify this milestone INCOMPLETE rather than silently skipping the cross-check.

### G9 — discrete power-node sanity

All `Delta_W^2` and `P_W` nodes must be finite and nonnegative, and direct reconstruction from `P_R |T|^2` must agree algebraically to relative residual <= `1e-12`.

## Classification

PASS:

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_PASS`

FAIL:

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_FAIL`

INCOMPLETE:

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_INCOMPLETE`

## Interpretation lock

A PASS licenses:

- `THREE_D_ISOTROPIC_WEYL_TRANSFER_NODES_LICENSED=True`
- `THREE_D_ISOTROPIC_WEYL_POWER_NODES_LICENSED=True`

A PASS does **not** license a continuous 3D Weyl power spectrum because only six radial nodes have been certified. Therefore, regardless of PASS:

- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

After a PASS, the next required milestone is a separately preregistered dense-k radial extension/interpolation/convergence audit before any line-of-sight lensing projection.
