# Full-J stochastic tagged radial K1->K2 refinement — pre-data declaration

## Purpose

The locked K0->K1 stochastic tagged radial campaign ended in

`FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_FAIL`

while all non-radial gates passed. The tagged response was solver-clean, broadband-saturated, background-converged, common-geometry invariant, and consistent with the earlier tagged-mode POC. The failure was localized to late-time radial interpolation after the response developed multiple zero crossings/sign changes.

This milestone asks one bounded question: is the already validated 11-node K1 grid sufficiently close to a converged radial description once one independent interior node is added inside every K1 interval, while preserving exactly the same periodic geometry and all physics choices?

No old threshold is relaxed. No ACT/lensing calculation is licensed here.

## Required ancestry

Require:

- R2 PASS: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- Gaussian 1D PASS: `05e38b273f91eb04b7b4c8753731017d0ed839c1`
- saturated closure PASS: `f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f`
- cardinality PASS: `df182a828b3c140fba22f1f5d58414ec41017e7b`
- tagged POC PASS: `aff670fa8551163f5cde2b5146e0e5840d53b424`
- K0->K1 tagged radial FAIL result: `2531a10772f97958ab221bd1f39ceffc23e964a5`
- updated project history: `c80b8034787be17b20d6757f3043a0a55c49f68a`
- this pre-data commit.

## Locked K1 input

Reuse the completed K1 outputs unchanged from

`results/fullj_stochastic_tagged_radial_convergence.{json,npz}`.

Require the local JSON classification

`FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_FAIL`

and require that all non-radial gates G1-G6, G9 and G10 are true. The existing K1 response array must not be recomputed or modified.

K1 is

`[0.03,0.04,0.05,0.065,0.08,0.09,0.10,0.125,0.15,0.175,0.20] h/Mpc`.

## Common geometry and physics

Keep exactly:

- `kF/h = 0.005`
- `NX = 256`
- `BOX = 2*pi/(0.005*h)`
- `NSTEP = 4096`
- `epsilon = 0.05`
- symmetric `+/-` tags
- `sigma=0`, `kind=simple`, `beta0=1`
- checkpoints `z=[6,5,4,3,2,1.5,1,0.5,0.2]`
- frozen Gaussian draw seed `20260912`
- frozen coefficient SHA256 `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`
- backgrounds `B4={0,1,2,3}` and `B2={0,1}`.

No metric feedback is introduced into the canonical trajectories.

## Frozen new-node rule

For each consecutive K1 interval `[a,b]`, choose one interior node from the existing `0.005 h/Mpc` Fourier lattice. Select the lattice point nearest the logarithmic midpoint `sqrt(a*b)`; if an exact tie occurs choose the lower point.

This gives the ten new nodes

`H2=[0.035,0.045,0.055,0.070,0.085,0.095,0.110,0.135,0.160,0.185] h/Mpc`.

The resulting nested K2 grid is

`K2=[0.03,0.035,0.04,0.045,0.05,0.055,0.065,0.070,0.08,0.085,0.09,0.095,0.10,0.110,0.125,0.135,0.15,0.160,0.175,0.185,0.20] h/Mpc`.

All nodes are exact integer Fourier modes of the same frozen `kF/h=0.005` box. No target-dependent box or resolution is allowed.

## New computation

Run only the ten H2 nodes for all four backgrounds and both tag signs:

`10 nodes * 4 backgrounds * 2 signs = 80` new nonlinear R2 integrations.

Combine these new responses with the locked K1 array to form K2. Existing K1 values are immutable input data, not reruns.

## Frozen gates

### K2-G1 provenance and locked-input identity

Require every ancestry lock, exact seed/hash, exact K1/H2/K2 arrays, common geometry, reference member, epsilon, NSTEP and background indices. Require the locked K1 JSON/NPZ input and its historical FAIL classification.

### K2-G2 all 80 new runs finite and constraint-clean

Require all 80 new runs finite at all checkpoints with

- canonical residual `<=1e-10`
- Hamiltonian/momentum/shear residual each `<=1e-8`.

### K2-G3 broadband saturated closure

Across all 80 new runs/checkpoints require

`max eps_sat <= 2e-2`.

### K2-G4 tagged response/power algebra

Require all new tagged responses finite, all powers finite/nonnegative, and the stored `|T|^2` identity residual `<=1e-12`.

### K2-G5 new-node background convergence B2->B4

On H2 require

- global response relative L2 `<=1e-2`
- per-node response relative L2 max `<=3e-2`
- global power relative L2 `<=2e-2`
- per-node power relative L2 max `<=5e-2`.

These are unchanged from the K0->K1 campaign.

### K2-G6 direct K1->K2 holdout accuracy

For each redshift, interpolate complex mean tagged response from K1 in `ln k` using separate real/imag PCHIP components and predict the ten H2 nodes. Compare with their direct B4 means.

Require across all redshifts:

- transfer L2 `<=3e-2`
- power L2 `<=5e-2`
- power peak relative error `<=1e-1`.

These are exactly the previous holdout thresholds.

### K2-G7 continuous K1->K2 radial convergence

On a 401-point log-spaced fine grid spanning `0.03<=k/h<=0.20`, compare PCHIP reconstructions from K1 and K2.

Require

- transfer L2 max `<=3e-2`
- power L2 max `<=5e-2`
- power peak max `<=1e-1`
- median transfer L2 over redshift `<=1.5e-2`
- median power L2 over redshift `<=2.5e-2`
- K2 interpolated power finite and nonnegative everywhere.

These are exactly the previous continuous-convergence thresholds.

### K2-G8 direct radial spike veto

For each H2 direct node and redshift, require

`|T(H2)| <= 2 * max(|T(left K1)|, |T(right K1)|)`

using the bracketing K1 interval endpoints. This preserves the previous bounded-spike criterion.

### K2-G9 refinement improvement

Because K0->K1 failed, require genuine refinement improvement at every redshift in both transfer and power:

`E_holdout_K1_to_K2 <= E_holdout_K0_to_K1`

for the aggregate direct-holdout L2 metrics stored in the locked K1 JSON.

This is an additional guard against repeating the historical nonmonotonic-refinement failure.

## Classification

PASS:

`FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_PASS`

FAIL:

`FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_FAIL`

INCOMPLETE:

`FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_INCOMPLETE`

## Interpretation lock

A PASS may set

- `STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED=True`
- `STOCHASTIC_TAGGED_BOUNDED_RESPONSE_TESTED=True`.

A PASS still does not by itself prove that a scalar tagged response is sufficient to reconstruct the full stochastic Weyl power. Therefore even after PASS keep

- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`.

The next step after a PASS is a response-kernel/covariance closure test, not ACT directly.