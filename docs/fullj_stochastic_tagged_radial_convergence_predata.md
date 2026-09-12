# Full-J stochastic tagged radial convergence — pre-data declaration

## Purpose

The stochastic-background tagged-mode POC passed at three radial targets and showed that the broadband Gaussian background restores the saturated constitutive regime, including at the previously anomalous isolated-mode low-k point. The symmetric response was effectively invariant under halving the tag amplitude.

The next bounded question is radial continuity/convergence of that tagged response. This milestone therefore tests a nested 6-to-11-node radial representation on a common broadband stochastic background construction. It does not perform line-of-sight lensing or an ACT likelihood.

## Required ancestry

Require:

- evolving R2 bridge PASS: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- Gaussian 1D ensemble PASS: `05e38b273f91eb04b7b4c8753731017d0ed839c1`
- 3D saturated closure PASS: `f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f`
- dense CLASS-residual R2 FAIL result lock: `4d87865a8e45985388dfab2b9d8922faa9290f7f`
- cardinality audit PASS: `df182a828b3c140fba22f1f5d58414ec41017e7b`
- stochastic tagged-mode POC PASS: `aff670fa8551163f5cde2b5146e0e5840d53b424`
- locked project history through that POC: `60fe83c37b74fea60d62df8fbe7a429218108af5`
- this pre-data commit.

Historical dense-radial FAIL classifications remain unchanged.

## Frozen physical branch

Use exactly:

- `sigma=0`, `kind=simple`, `beta0=1.0`
- redshift checkpoints `z=[6,5,4,3,2,1.5,1,0.5,0.2]`
- `NSTEP=4096`
- corrected CLASS dense-k64 environment already certified by the cardinality and tagged POC chain
- no nonlinear metric feedback into the locked canonical trajectory equations.

## Frozen Gaussian backgrounds

Use the same locked Gaussian coefficient draw:

- seed `20260912`
- draw shape `(32,6,2)`
- `g=(X+iY)/sqrt(2)`
- SHA256 `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`.

Primary background set:

`B4=[0,1,2,3]`.

Background convergence prefix:

`B2=[0,1]`.

The same Gaussian coefficient vector for a given background id must be reused for every radial target and sign (common random numbers).

## Frozen radial grids

Coarse six-node grid:

`K0=[0.03,0.05,0.08,0.10,0.15,0.20] h/Mpc`.

Primary eleven-node grid:

`K1=[0.03,0.04,0.05,0.065,0.08,0.09,0.10,0.125,0.15,0.175,0.20] h/Mpc`.

Direct K0-to-K1 holdouts are the five midpoint nodes:

`H1=[0.04,0.065,0.09,0.125,0.175] h/Mpc`.

No node may be added, removed or moved after results are seen.

## Common periodic embedding

All eleven targets use one common periodic geometry:

- `k_F/h=0.005 Mpc^-1`
- `BOX=2*pi/(0.005*h)`
- `NX=256`.

All K0 and K1 radial nodes and all six broadband background modes are therefore exact integer Fourier modes. The maximum index is 40 at `k/h=0.20`. `NX=256` preserves the physical grid spacing of the historical `k_F/h=0.01`, `NX=128` embedding.

This common geometry is mandatory so radial differences cannot be attributed to a target-dependent box or spatial resolution.

## CLASS mode set per target

For each target request the sorted union of K0 and the target radial node. This gives six histories for K0 nodes and seven histories for midpoint nodes. Use only the already documented dynamic `len(histories)==len(K_MPC)` loader repair.

## Tagged perturbation

The POC established epsilon consistency at `epsilon=0.10` versus `0.05` with maximum relative discrepancy `1.2944515507279873e-08`. This campaign therefore freezes the primary tag amplitude to

`epsilon=0.05`

and retains both signs `s=+1,-1`.

For target k add

`s * epsilon * A_tag(k) * cos(k x + phi_tag(k))`,

with the same frozen log-linear amplitude interpolation and phase interpolation used by the tagged POC.

The complex tagged response is

`T_tag(b;k,z) = [W_+ - W_-] exp(-i phi_tag) / [epsilon A_tag]`.

The primary stochastic response is the B4 ensemble mean

`Tbar_4(k,z)=mean_{b in B4} T_tag(b;k,z)`.

The primary tagged power proxy is

`Pbar_4(k,z)=mean_{b in B4} |T_tag(b;k,z)|^2`.

The B2 analogues use backgrounds `[0,1]` only.

## Frozen interpolation rule

Interpolate the ensemble-mean complex tagged response from radial nodes using PCHIP in `ln k`, separately for real and imaginary parts. Power comparisons use the physical nonnegative quantity `Pbar` directly; when a continuous power curve is required, PCHIP `Pbar` in `ln k` and require nonnegative finite output.

No spline family may be changed after results are seen.

## Frozen gates

### STR-G1 — provenance and frozen identity

Require all ancestry locks, exact Gaussian hash, exact B4/B2 sets, exact K0/K1/H1 grids, epsilon, common geometry, reference member, redshift list and `NSTEP`.

### STR-G2 — all 88 tagged runs finite and constraint-clean

There are exactly

`11 targets * 4 backgrounds * 2 signs = 88`

nonlinear R2 integrations. Require all finite at all nine checkpoints, with:

- canonical residual `<=1e-10`
- Hamiltonian/momentum/shear residual each `<=1e-8`.

### STR-G3 — broadband saturated closure

Across all 88 runs and checkpoints require

`max eps_sat <= 2e-2`.

The threshold is unchanged from the saturated-closure and tagged-POC milestones.

### STR-G4 — tagged response/power algebra

Require all complex `T_tag` values finite and all `|T_tag|^2` finite/nonnegative. The stored real/imaginary response and power identity must close to relative residual `<=1e-12`.

### STR-G5 — common-geometry regression to the locked POC

For targets `k/h=0.10` and `0.175`, backgrounds `0,1,2`, compare the new `epsilon=0.05` response vectors with the locked POC `epsilon=0.05` responses. Require:

- median relative L2 `<=1e-6`
- maximum relative L2 `<=1e-5`.

This tests that the common `k_F/h=0.005`, `NX=256` embedding does not alter the already locked tagged response.

### STR-G6 — background convergence B2 to B4

On the full direct K1 grid compare B2 and B4 ensemble means.

For complex response, compute a global relative L2 over `(k,z)` and a maximum per-k relative L2 over redshift. Require:

- global response difference `<=1e-2`
- maximum per-k response difference `<=3e-2`.

For ensemble mean tagged power require:

- global power difference `<=2e-2`
- maximum per-k power difference `<=5e-2`.

### STR-G7 — direct K0-to-K1 holdout accuracy

For each redshift, interpolate `Tbar_4` from K0 and predict the five direct H1 values. Compare with direct K1/H1 tagged responses. Require over all redshifts:

- maximum complex-transfer L2 across H1 `<=3e-2`
- maximum tagged-power L2 across H1 `<=5e-2`
- maximum tagged-power peak-normalized absolute error `<=1e-1`.

Power prediction for this holdout gate is derived from the interpolated complex response via `|T_pred|^2` and compared with direct `Pbar_4`; this directly tests the response-to-power representation.

### STR-G8 — K0-to-K1 continuous radial convergence

On a fixed 401-point log-spaced radial grid over `0.03<=k/h<=0.20`, compare the K0 and K1 PCHIP representations of `Tbar_4` and `Pbar_4`.

Require across all redshifts:

- maximum transfer L2 `<=3e-2`
- maximum power L2 `<=5e-2`
- maximum power peak-normalized absolute difference `<=1e-1`.

Also require median K0-to-K1 transfer L2 `<=1.5e-2` and median power L2 `<=2.5e-2`.

### STR-G9 — direct radial smoothness/no hidden midpoint spike

At every H1 midpoint and redshift require the direct B4 mean response magnitude to remain within a factor of 2 of the larger magnitude of its two adjacent K0 endpoints plus a numerical floor. This is a broad spike veto only; it does not require monotonicity and permits physical zero crossings.

Equivalently:

`|T_mid| <= 2 * max(|T_left|,|T_right|,1e-12)`.

### STR-G10 — preserved low-k broadband regime

For the lowest K1 targets `0.03,0.04,0.05`, require each target's maximum broadband saturation residual across backgrounds/signs/redshifts to remain `<=2e-2`. Report these three values explicitly.

## Non-gating diagnostics

Report:

- per-k/per-z B4 mean complex response, response RMS scatter and power CV
- B2/B4 convergence by radial node
- H1 holdout errors by redshift
- K0/K1 continuous convergence by redshift
- direct tagged response versus corrected CLASS transfer as a descriptive reference only
- POC low-k `k/h=0.0375` result as a historical external control only; it is not part of K1 and is not rerun here.

## Classification

PASS:

`FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_PASS`

FAIL:

`FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_FAIL`

INCOMPLETE:

`FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_INCOMPLETE`.

## Interpretation lock

A PASS establishes a bounded, common-geometry, common-random-background radial continuum representation for the **directional stochastic tagged response** on `0.03<=k/h<=0.20 Mpc^-1`.

A PASS may set:

- `STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED=True`
- `STOCHASTIC_TAGGED_BOUNDED_RESPONSE_TESTED=True`.

A PASS does not by itself establish a full 3D isotropic nonlinear Weyl power spectrum because off-diagonal stochastic mode coupling has not yet been closed against the scalar tagged response. Therefore even on PASS keep:

- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`.

The next milestone after a PASS is a bounded stochastic response-kernel/covariance closure test that determines if the diagonal tagged response is sufficient for `P_W(k,z)` or if an off-diagonal kernel `K(k,k',z)` is required.