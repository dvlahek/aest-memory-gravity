# Full-J stochastic-background tagged-mode response POC — pre-data declaration

## Purpose

The completed dense-radial campaigns established two facts that must both be preserved:

1. direct nonlinear R2 single-mode nodes are numerically healthy, but a smooth scalar interpolation of the isolated finite-amplitude signed transfer is not convergent on the tested radial grid;
2. the separate same-environment cardinality audit excludes the 21-history versus 41-history CLASS state as the origin of that radial structure.

The next bounded question is therefore not another PCHIP refinement. This milestone tests a tagged-mode response **inside a frozen broadband Gaussian background**, so that the nonlinear constitutive factor `j_eff(|grad chi|)` is evaluated on a multi-mode field rather than on an isolated finite-amplitude mode.

This is a proof-of-concept response test only. It does not construct a continuous three-dimensional Weyl power spectrum and does not license lensing or ACT.

## Required ancestry

Require these locked ancestors:

- evolving R2 bridge PASS: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- Gaussian 1D ensemble PASS: `05e38b273f91eb04b7c8753731017d0ed839c1`
- 3D saturated closure PASS: `f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f`
- dense CLASS-residual R2 FAIL result lock: `4d87865a8e45985388dfab2b9d8922faa9290f7f`
- cardinality audit PASS result lock: `df182a828b3c140fba22f1f5d58414ec41017e7b`
- this pre-data commit.

Historical dense FAIL classifications remain unchanged.

## Frozen physical branch

Use exactly

- `sigma=0`,
- `kind=simple`,
- `beta0=1.0`,
- checkpoints `z=[6,5,4,3,2,1.5,1,0.5,0.2]`,
- `NSTEP=4096`,
- the same corrected CLASS provenance as the R2 chain,
- the isolated `dense-k64` corrected CLASS environment already used by the 41-mode audit.

No metric feedback is introduced into the locked canonical trajectory equations.

## Frozen Gaussian broadband backgrounds

Reuse the **first three** Gaussian coefficient vectors from the locked 1D ensemble draw:

- RNG: `numpy.random.default_rng(20260912)`,
- draw shape `(32,6,2)`,
- `g=(X+iY)/sqrt(2)`,
- full locked coefficient hash: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`,
- background indices: `[0,1,2]`.

For original mode `j`, the broadband real-space contribution is

`MODE_AMP[j] * abs(g_j) * cos(k_j x + arg(g_j))`.

The three backgrounds are fixed before any tagged response is evaluated.

## Frozen tagged modes

Test exactly

`k_tag/h = [0.0375, 0.10, 0.175] Mpc^-1`.

They represent

- the anomalous isolated low-k saturation region,
- the known late-time transfer-zero region,
- a stable high-k control.

The tag amplitude scale `A_tag(k)` is the same log-linear interpolation of the six locked `MODE_AMP` values used in the dense-radial tests. The tag phase is the same linear interpolation of the six locked phases in physical k.

Use two dimensionless symmetric tag amplitudes

`epsilon = [0.10, 0.05]`.

For sign `s=+1,-1`, add

`s * epsilon * A_tag(k) * cos(k x + phi_tag(k))`

to the corresponding CLASS mode row. If `k_tag` coincides with an original broadband mode (`0.10`), the tag is added to that same row rather than creating a duplicate CLASS history.

## Periodic embedding and spatial resolution

For each target use the smallest frozen lattice fundamental that makes all six broadband modes and the tagged mode exact integer Fourier modes:

| `k_tag/h` | `k_F/h` | tag index | maximum original index | `NX` |
|---:|---:|---:|---:|---:|
| 0.0375 | 0.0025 | 15 | 80 | 512 |
| 0.10   | 0.0100 | 10 | 20 | 128 |
| 0.175  | 0.0050 | 35 | 40 | 256 |

Set `BOX=2*pi/(k_F*h)` for the corresponding target. The rule preserves the original physical grid spacing because `NX=128*(0.01/k_F_h)`.

No target k, box, Fourier index or spatial resolution may be changed after results are seen.

## CLASS mode sets

For each target request corrected CLASS histories for the sorted union of

`[0.03,0.05,0.08,0.10,0.15,0.20]`

and the target `k_tag/h`. This gives 7 histories for `0.0375` and `0.175`, and the original 6 histories for `0.10`.

The inherited six-history loader guard may only use the already documented runtime generalization `len(histories)==len(K_MPC)`.

## Tagged response definition

Let `W_+(k,z;epsilon,b)` and `W_-(k,z;epsilon,b)` be the positive-frequency Fourier coefficients of the reconstructed Weyl field for background `b` and opposite tag signs.

The frozen directional tagged transfer is

`T_tag(epsilon,b;k,z) = [W_+ - W_-] * exp(-i phi_tag) / [epsilon A_tag]`.

There is no extra factor of two because the positive-frequency coefficient of `epsilon A cos(kx+phi)` is `epsilon A exp(i phi)/2`, and the `+/-` input difference is `epsilon A exp(i phi)`.

This is one frozen real-direction response in tag phase. It is not claimed to be the full complex Frechet operator.

The primary response estimate is the smaller-amplitude value `epsilon=0.05`. The `epsilon=0.10` value is an independent finite-amplitude consistency control.

## Broadband constitutive diagnostic

For every `+/-` run and checkpoint evaluate

`eps_sat = || div[(1+j_eff) grad chi] - 2 lap chi || / max(||full||,||2 lap chi||)`.

This directly tests if the broadband Gaussian field restores the saturated constitutive regime at the problematic low-k tag.

## Frozen gates

### ST-G1 — provenance and frozen identity

Require all ancestry locks, the exact seed/hash/background indices, target list, epsilon list, reference member, redshift list, `NSTEP`, box rules and `NX` rules above.

### ST-G2 — Gaussian background identity

Regenerate the locked 32x6 coefficient draw and require the exact SHA256 hash above. Use exactly background indices `[0,1,2]`.

### ST-G3 — all tagged runs finite and constraint-clean

There are exactly

`3 backgrounds * 3 targets * 2 epsilon levels * 2 signs = 36`

nonlinear R2 integrations. Require all 36 finite at all nine checkpoints with

- canonical residual `<=1e-10`,
- Hamiltonian/momentum/shear residuals each `<=1e-8`.

### ST-G4 — symmetric tagged-response finite-amplitude consistency

For each of the 9 `(background,k_tag)` pairs compare the nine-redshift complex response vectors at `epsilon=0.10` and `0.05`:

`E_eps = ||T_tag(0.10)-T_tag(0.05)||_2 / max(||T_tag(0.10)||_2,||T_tag(0.05)||_2,tiny)`.

Require

- median `E_eps <= 3e-2`,
- maximum `E_eps <= 1e-1`.

No epsilon may be changed after seeing this result.

### ST-G5 — broadband saturated closure

Across all 36 runs and nine checkpoints require

`max eps_sat <= 2e-2`.

This retains the previous saturated-closure numerical threshold. It is not relaxed for the low-k tag.

### ST-G6 — tagged response/power sanity

Require all complex tagged responses finite. For the primary `epsilon=0.05` estimate define

`P_tag = |T_tag|^2`.

Require every `P_tag` finite and nonnegative. The algebraic identity between stored real/imaginary response and `|T_tag|^2` must close to `<=1e-12` relative residual.

## Descriptive, non-gating diagnostics

Report, but do not gate on:

- per-target/per-redshift ensemble mean and standard deviation of `T_tag`,
- ensemble mean and coefficient of variation of `|T_tag|^2`,
- background-to-background RMS scatter normalized by response RMS,
- low-k `eps_sat` distribution compared with the isolated-mode value from the completed R2 FAIL,
- primary tagged response versus the corresponding isolated single-mode direct transfer where available.

Three backgrounds are insufficient for a publication-grade stochastic convergence claim; these quantities are diagnostic only.

## Classification

PASS:

`FULLJ_STOCHASTIC_TAGGED_MODE_POC_PASS`

FAIL:

`FULLJ_STOCHASTIC_TAGGED_MODE_POC_FAIL`

INCOMPLETE:

`FULLJ_STOCHASTIC_TAGGED_MODE_POC_INCOMPLETE`

## Interpretation lock

A PASS establishes only that a symmetric directional tagged response can be measured reproducibly inside the frozen broadband Gaussian backgrounds, with the nonlinear constitutive operator remaining in the saturated regime and with controlled finite-tag-amplitude dependence.

A PASS may set

- `STOCHASTIC_BROADBAND_TAGGED_RESPONSE_POC_TESTED=True`,
- `STOCHASTIC_BROADBAND_LOWK_SATURATION_TESTED=True`.

It does **not** license a continuous radial transfer, a converged stochastic power spectrum, line-of-sight lensing, ACT, or an observational claim. Keep

- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`,
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`,
- `EVOLVING_WEYL_POWER_LICENSED=False`,
- `ACT_LIKELIHOOD_LICENSED=False`,
- `OBSERVATIONAL_CLAIM_LICENSED=False`.
