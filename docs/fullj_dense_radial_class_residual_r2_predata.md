# Full-J dense radial CLASS-residual R2 — pre-data declaration

## Purpose

The completed dense-radial signed-transfer milestone is locked as

`FULLJ_DENSE_RADIAL_WEYL_EXTENSION_FAIL`.

That FAIL did not arise from the direct 21 R2 nodes. All direct-node health, corrected-CLASS normalization, zero-safe phase, saturated closure, six-anchor recovery, and power sanity gates passed. The failed gates were specifically the preregistered PCHIP representation of the **full signed transfer** as a function of `ln k`.

Inspection of the locked direct result shows that at low redshift the corrected-CLASS Weyl transfer itself contains multiple radial extrema and zero crossings over `0.03 <= k/h <= 0.20 Mpc^-1`. The R2 construction is naturally a correction to that reference. Therefore this milestone tests the decomposition

`T_W_R2(k,z) = T_W_CLASS(k,z) + DeltaT_W(k,z)`

with only

`DeltaT_W = T_W_R2 - T_W_CLASS`

interpolated in k.

This is a new post-failure hypothesis. It does not alter the historical dense signed-transfer FAIL. To avoid validating the new representation on the same points that motivated it, this milestone uses **20 new direct R2 k holdouts** not present in the completed K2 grid.

## Required ancestry

Require the following ancestors:

- R2 evolving-Weyl result: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- Gaussian 1D result: `05e38b273f91eb04b7c8753731017d0ed839c1`
- 3D geometry result: `ca6a102196055e27dc2b31379285bfc7aea1a35b`
- saturated closure result: `f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f`
- historical six-node transfer FAIL: `b7bb0aef90ec935821f4dc1a63db0d79966a15f8`
- R1 zero-safe phase PASS: `20679c5274e936037c226904d40c9d6779b00a49`
- completed dense signed-transfer FAIL result: `55495cc968082f1cf6638785f7609c787971835c`

The local completed dense JSON must be present and classified exactly

`FULLJ_DENSE_RADIAL_WEYL_EXTENSION_FAIL`

with all of G1-G6 and G10 true and only G7-G9 false.

## Theory branch and numerics

Freeze exactly

- `sigma=0`,
- `kind=simple`,
- `beta0=1.0`,
- `z=[6,5,4,3,2,1.5,1,0.5,0.2]`,
- `NX=128`,
- `NSTEP=4096`,
- single-mode periodic embedding `n_embed=10`.

Use the same corrected CLASS provenance as the locked R2 chain.

## Radial grids

Retain the completed 21-node K2 grid exactly:

`K2/h = [0.03,0.035,0.04,0.045,0.05,0.0575,0.065,0.0725,0.08,0.085,0.09,0.095,0.10,0.1125,0.125,0.1375,0.15,0.1625,0.175,0.1875,0.20] Mpc^-1`.

Define K3 by subdividing every original K0 interval into eighths. Equivalently, for every adjacent original K0 pair `(a,b)`, include

`a + m*(b-a)/8`, for `m=0,...,8`.

Across all five original intervals this gives 41 unique nodes. K2 corresponds to the even eighth fractions. The **20 odd-eighth nodes** are the new frozen direct holdout set H3.

No K3/H3 location may be changed after new R2 outputs are seen.

## Probe amplitude and phase

Use exactly the completed dense rule:

- probe amplitude = log-linear interpolation of the original six locked `MODE_AMP` values in `log k`,
- phase = linear interpolation of the original six locked phases in k,
- transfer reconstruction removes the applied phase and divides out the applied amplitude.

No amplitude or phase is fitted to the new results.

## CLASS reference

Request corrected CLASS histories for all 41 K3 physical k values in one run. The inherited historical six-history cardinality guard may be generalized only to `len(histories)==len(K_MPC)` as already documented for the completed dense milestone.

The physical reference at every node is

`T_CLASS(k,z)=phi_CLASS(k,z)+psi_CLASS(k,z)`.

The 21 K2 CLASS values from this new 41-mode CLASS request must reproduce the stored completed-dense K2 CLASS values to numerical precision; this is a cross-run reference consistency check.

## Direct new R2 holdouts

Only the 20 H3 nodes require new nonlinear R2 integrations. Reuse the completed K2 R2 transfer nodes from the locked local dense JSON; do not rerun or refit them.

At each new H3 node report

- complex `T_R2`,
- real licensed transfer `Re(T_R2)`,
- direct `T_CLASS`,
- residual `DeltaT=T_R2-T_CLASS`,
- `Delta_W^2=P_R [Re(T_R2)]^2`,
- `P_W=2*pi^2 Delta_W^2/k^3`,
- canonical/metric health,
- saturated-operator residual.

## Frozen residual representation

For a training grid K, define

`DeltaT_K(k,z) = PCHIP_ln_k[ T_R2(K,z)-T_CLASS(K,z) ]`.

At any target k, the predicted total transfer is

`T_pred(k,z)=T_CLASS_direct(k,z)+DeltaT_K(k,z)`.

The corrected-CLASS part is never interpolated by this milestone when a direct CLASS value exists. No interpolation of the ratio `T_R2/T_CLASS` is allowed because it is singular at CLASS zero crossings.

Power is derived only after reconstructing the total transfer.

## Independent H3 holdout validation

Use K2 as the primary training grid and predict the 20 new H3 direct R2 transfers. For every redshift define on H3

`E_T_L2 = ||T_pred-T_direct||_2 / max(||T_direct||_2,tiny)`,

`E_P_L2 = ||P_pred-P_direct||_2 / max(||P_direct||_2,tiny)`,

`E_P_peak = max|P_pred-P_direct| / max(P_direct)`.

Also form K1-residual predictions on the same new H3 set, where K1 is the completed 11-node grid. K2 must improve the new-holdout prediction relative to K1 in aggregate.

## Residual refinement convergence

After the 20 H3 direct results are available, K3 contains 41 direct residual nodes. On a fixed 801-point uniform grid in `ln k` over the closed bounded interval compare

- K1 residual interpolant vs K2 residual interpolant,
- K2 residual interpolant vs K3 residual interpolant.

Because the direct CLASS contribution is common and exactly cancels between residual representations, the continuous-grid convergence quantity is the residual-correction difference itself. Report

`E_DeltaT_L2 = ||DeltaT_fine-DeltaT_coarse||_2 / max(||T_CLASS_K3||_nodes, ||T_R2_K3||_nodes, tiny)`

using the direct K3 node norm as a fixed physical normalization per redshift.

Additionally evaluate total-transfer and total-power refinement differences on all 41 direct K3 nodes using their direct corrected-CLASS values. This tests zero-crossing sensitivity without interpolating CLASS.

## Frozen gates

### R2-G1 — locked provenance/setup

All required locks must be ancestors. Require exact K1/K2/K3/H3 construction, reference branch, redshift list, `n_embed=10`, `NX=128`, and `NSTEP=4096`.

### R2-G2 — completed K2 state integrity

Require the local completed dense JSON to retain classification FAIL with original gates G1-G6 and G10 true and G7-G9 false. Require all 21 stored K2 direct nodes finite.

### R2-G3 — corrected-CLASS cross-run consistency

Across the 189 K2 `(k,z)` cells require the new 41-mode CLASS request to reproduce the stored K2 `T_CLASS` values with

- median relative difference <= `1e-8`,
- maximum relative difference <= `1e-5`,

using the same zero-safe scalar denominator convention as earlier audits.

### R2-G4 — new H3 direct health

All 20 new R2 holdouts must be finite at all nine checkpoints with

- canonical residual <= `1e-10`,
- Hamiltonian/momentum/shear residuals <= `1e-8`.

### R2-G5 — new H3 initial CLASS normalization

At z=6 require max relative `|T_R2-T_CLASS| <= 5e-3` across H3.

### R2-G6 — new H3 zero-safe phase

Across all 180 new `(k,z)` cells require

- global `||Im T||_2/||T||_2 <= 1e-8`,
- max absolute `|Im T| <= 1e-8`,
- real projection changes each power node by max relative amount <= `1e-12`.

### R2-G7 — new H3 saturated closure

Require max direct H3 `eps_sat <= 2e-2`.

### R2-G8 — independent K2-residual holdout accuracy

Across the nine redshifts on the 20 new H3 nodes require

- max `E_T_L2 <= 3e-2`,
- max `E_P_L2 <= 5e-2`,
- max `E_P_peak <= 1e-1`.

These retain the original signed-transfer holdout tolerances; they are not relaxed after the previous FAIL.

### R2-G9 — residual refinement improvement on new H3 holdouts

K2-residual predictions must improve over K1-residual predictions in transfer-L2 and power-L2 for at least `7/9` redshifts, and the median K2 error must be smaller than the median K1 error for both quantities.

### R2-G10 — K2->K3 residual convergence

On the fixed 801-point log-k grid require

- max normalized continuous residual-correction K2->K3 L2 <= `2e-2`,
- median K2->K3 correction difference smaller than median K1->K2 difference.

On all 41 direct K3 nodes, using direct CLASS values, require K2->K3 representation differences

- max total-transfer L2 <= `3e-2`,
- max total-power L2 <= `5e-2`,
- max peak-normalized power difference <= `1e-1`,

and median K2->K3 transfer/power differences smaller than the corresponding K1->K2 medians.

### R2-G11 — power sanity

All new direct and residual-reconstructed power values must be finite and nonnegative. Direct-node identity must close to <= `1e-12` relative residual.

## Classification

PASS:

`FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_PASS`

FAIL:

`FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_FAIL`

INCOMPLETE:

`FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_INCOMPLETE`

## Interpretation lock

A PASS licenses a bounded **composite** radial representation on

`0.03 <= k/h <= 0.20 Mpc^-1`, `0.2 <= z <= 6`,

of the form

`T_W(k,z)=T_CLASS_corrected(k,z)+DeltaT_R2_PCHIP(k,z)`.

A PASS may set

- `THREE_D_DENSE_RADIAL_WEYL_NODES_LICENSED=True`,
- `THREE_D_BOUNDED_CLASS_RESIDUAL_WEYL_TRANSFER_LICENSED=True`,
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=True`,
- `BOUNDED_K_H_MPC_MIN=0.03`,
- `BOUNDED_K_H_MPC_MAX=0.20`.

The representation requires corrected CLASS to be evaluated at the target k; it does not replace CLASS by a six/21-node interpolant.

Even after PASS, do not license unrestricted lensing or ACT because the physical k-domain has not yet been extended beyond 0.20 h/Mpc. Therefore keep

- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`,
- `EVOLVING_WEYL_POWER_LICENSED=False`,
- `ACT_LIKELIHOOD_LICENSED=False`,
- `OBSERVATIONAL_CLAIM_LICENSED=False`.