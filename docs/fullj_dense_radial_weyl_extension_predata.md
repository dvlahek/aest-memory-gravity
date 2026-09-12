# Full-J dense radial Weyl extension — pre-data declaration

## Purpose

The locked chain now licenses six discrete isotropic 3D Weyl transfer/power nodes on the central saturated branch. The R1 zero-safe phase audit is locked as PASS and preserves the historical original phase-gate FAIL.

This milestone asks a narrower next question:

**Can the licensed six-node radial transfer be extended to a directly computed nested dense radial grid on the already tested interval `0.03 <= k/h <= 0.20 Mpc^-1`, with interpolation errors and refinement convergence small enough to define a bounded continuous radial Weyl-power representation?**

This milestone does not extend the physical k-range and does not perform line-of-sight lensing.

## Required ancestry

Required locked ancestors:

- R2 evolving-Weyl bridge result: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- Gaussian 1D ensemble result: `05e38b273f91eb04b7b4c8753731017d0ed839c1`
- 3D lattice-shell geometry result: `ca6a102196055e27dc2b31379285bfc7aea1a35b`
- 3D saturated constitutive closure result: `f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f`
- historical six-node transfer FAIL lock: `b7bb0aef90ec935821f4dc1a63db0d79966a15f8`
- R1 zero-safe phase-audit result: `20679c5274e936037c226904d40c9d6779b00a49`

The reference theory branch remains exactly

- `sigma=0`
- `kind=simple`
- `beta0=1.0`.

The nine redshifts remain

`z=[6,5,4,3,2,1.5,1,0.5,0.2]`.

## Nested radial grids

The original licensed level-0 nodes are

`K0/h = [0.03,0.05,0.08,0.10,0.15,0.20] Mpc^-1`.

Define level 1 by inserting one midpoint into each adjacent level-0 interval:

`K1 = K0 union {(a+b)/2 for adjacent a,b in K0}`.

This gives 11 nodes.

Define level 2 by also inserting the quarter and three-quarter points of every original level-0 interval:

`K2 = K0 union {a+(b-a)/4, a+(b-a)/2, a+3(b-a)/4}`

for every adjacent level-0 pair. This gives 21 nodes.

The level-2 grid is the only new direct transfer grid used for the primary result. No node locations may be changed after seeing outputs.

## Single-mode periodic embedding

Each radial node is evolved independently as a single physical Fourier mode. To avoid restricting new physical k values to the original shared-box integer lattice, each single-mode run uses a periodic box chosen so that the physical target mode is always represented by integer Fourier index

`n_embed = 10`,

namely

`BOX(k) = 2*pi*n_embed/k`.

This changes only the numerical periodic representation of an isolated Fourier mode. The physical wave number entering CLASS, canonical initialization, spectral derivatives, and metric reconstruction remains the requested `k`.

`NX=128`, `NSTEP=4096`, and the central nonlinear R2 equations remain unchanged.

## Frozen numerical probe amplitude and phase

The single-mode probe amplitude is not fitted to any new result. At each new k it is the log-linear interpolation of the original six locked `MODE_AMP` values in `log(k)`.

The numerical spatial phase is the linear interpolation of the original six locked phases as a function of k.

At all six original nodes, both amplitude and phase therefore recover the original values exactly.

The reconstructed transfer divides out the applied probe amplitude and removes the applied phase:

`T_W(k,z) = 2 W_hat_nembed(z) exp(-i phase(k)) / probe_amp(k)`.

The R1 audit already licensed reporting the physical transfer as `Re(T_W)` provided the zero-safe quadrature conditions remain satisfied.

## CLASS input

A single corrected-CLASS run is requested with all 21 level-2 physical k values. No cosmological parameter is changed. The same corrected CLASS provenance used by R2 is required.

## Direct dense-node quantities

At every `(k,z)` level-2 cell report

- complex reconstructed `T_W`,
- physical real transfer `Re(T_W)`,
- direct corrected-CLASS `T_W_CLASS=phi+psi`,
- `Delta_W^2 = P_R(k) [Re(T_W)]^2`,
- `P_W(k,z)=2*pi^2 Delta_W^2/k^3`,
- canonical and metric constraint health,
- a direct single-mode saturated-operator residual.

The primordial spectrum is evaluated analytically from the already locked constants

`P_R(k)=A_s (k/k_piv)^(n_s-1)`.

## Dense single-mode saturated-operator residual

For each checkpoint, using the actual evolved `chi`, evaluate

`L_nl = div[(1+j_eff) grad chi]`

and

`L_sat = 2 Laplacian chi`.

Define

`eps_sat = ||L_nl-L_sat|| / max(||L_nl||,||L_sat||,tiny)`.

This extends the already certified saturated closure from the original anchor shells to the new intermediate radial nodes.

## Anchor recovery

At the six original k nodes compare the new direct single-mode real transfer with the already completed six-node transfer JSON. The historical six-node calculation used a simultaneous six-mode construction but independently certified single-mode separability to `~1e-6`, so this is an independent bridge check.

No anchor value is overwritten or refitted.

## Interpolation rule

The only candidate continuous radial representation is a shape-preserving PCHIP interpolation of the **signed real transfer** as a function of `ln k`.

Power is derived only after interpolation:

`P_W(k,z) proportional to P_R(k) [T_W(k,z)]^2`.

Power itself is not log-interpolated. This preserves transfer zero crossings and avoids singular logarithms near the observed low-z transfer node.

## Direct holdout validation

The ten level-2 quarter/three-quarter nodes that are absent from level 1 form a frozen holdout set.

For every redshift:

1. fit the level-0 PCHIP transfer using only K0,
2. fit the level-1 PCHIP transfer using only K1,
3. predict the direct level-2 holdout transfers,
4. compare both predictions with the directly evolved K2 holdout values.

Use zero-safe aggregate errors:

`E_T_L2 = ||T_pred-T_direct||_2 / max(||T_direct||_2,tiny)`

and

`E_P_L2 = ||P_pred-P_direct||_2 / max(||P_direct||_2,tiny)`.

Also define

`E_P_peak = max|P_pred-P_direct| / max(P_direct)`

on the same holdout set.

## Fine-grid refinement convergence

At each redshift evaluate the K0, K1, and K2 PCHIP transfer interpolants on a fixed 401-point uniform grid in `ln k` spanning the closed licensed interval.

Define zero-safe transfer and power differences for K0->K1 and K1->K2. The K1->K2 refinement must be smaller than K0->K1 in aggregate and must satisfy the frozen absolute convergence gates below.

## Frozen gates

### G1 — locked provenance and setup

All required result locks must be ancestors of HEAD. Require exact reference branch, redshift list, K0/K1/K2 construction, `n_embed=10`, `NX=128`, and `NSTEP=4096`.

### G2 — finite/constraint health

All 21 direct single-mode runs must be finite at all nine checkpoints. Require

- canonical residual <= `1e-10`,
- Hamiltonian/momentum/shear residuals <= `1e-8`.

### G3 — initial corrected-CLASS normalization

At `z=6` require all 21 direct transfer nodes to reproduce corrected CLASS with max relative error <= `5e-3`.

### G4 — zero-safe phase consistency

Across all 189 dense `(k,z)` cells require

- global `||Im T||_2/||T||_2 <= 1e-8`,
- max absolute `|Im T| <= 1e-8`,
- replacing complex T by Re(T) changes each power node by max relative amount <= `1e-12`.

No local `|Im T|/|T|` gate is used because the separately locked R1 audit demonstrated that metric is singular at transfer zero crossings.

### G5 — dense saturated closure

Require maximum `eps_sat <= 2e-2` across all direct level-2 runs/checkpoints.

### G6 — recovery of the six licensed anchor nodes

Across the 54 original `(k,z)` anchor cells require new direct-single versus locked original-transfer real difference

- median <= `5e-4`,
- maximum <= `5e-3`.

### G7 — direct level-2 holdout accuracy of level-1 interpolation

Across nine redshifts require for the level-1 PCHIP prediction on the frozen level-2 holdout set

- max `E_T_L2 <= 3e-2`,
- max `E_P_L2 <= 5e-2`,
- max `E_P_peak <= 1e-1`.

### G8 — refinement improvement

On the same direct holdout nodes, level 1 must improve over level 0 in both transfer-L2 and power-L2 error for at least 7 of 9 redshifts, and the median level-1 error must be smaller than the median level-0 error for both quantities.

### G9 — fine-grid K1->K2 interpolation convergence

On the fixed 401-point log-k grid require

- max transfer L2 difference between K1 and K2 interpolants <= `3e-2`,
- max power L2 difference <= `5e-2`,
- max peak-normalized power difference <= `1e-1`,
- median K1->K2 transfer and power differences smaller than the corresponding K0->K1 medians.

### G10 — power-node sanity

All direct and interpolated bounded-domain power values must be finite and nonnegative. Direct node identity `Delta_W^2=P_R [Re(T)]^2` must close to relative residual <= `1e-12`.

## Classification

PASS:

`FULLJ_DENSE_RADIAL_WEYL_EXTENSION_PASS`

FAIL:

`FULLJ_DENSE_RADIAL_WEYL_EXTENSION_FAIL`

INCOMPLETE:

`FULLJ_DENSE_RADIAL_WEYL_EXTENSION_INCOMPLETE`

## Interpretation lock

A PASS licenses only the bounded interpolation domain

`0.03 <= k/h <= 0.20 Mpc^-1`, `0.2 <= z <= 6`.

A PASS may set

- `THREE_D_DENSE_RADIAL_WEYL_NODES_LICENSED=True`,
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=True`,
- `BOUNDED_K_H_MPC_MIN=0.03`,
- `BOUNDED_K_H_MPC_MAX=0.20`.

Even after PASS, the current k-range is insufficient for an unrestricted line-of-sight lensing projection. Therefore keep

- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`,
- `EVOLVING_WEYL_POWER_LICENSED=False`,
- `ACT_LIKELIHOOD_LICENSED=False`,
- `OBSERVATIONAL_CLAIM_LICENSED=False`.

The next milestone after PASS is a separately preregistered k-range extension/convergence audit driven by the k-domain required by the lensing line-of-sight kernel, not ACT fitting.
