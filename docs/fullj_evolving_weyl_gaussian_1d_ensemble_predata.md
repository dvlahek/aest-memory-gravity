# Full-J evolving Weyl Gaussian 1D ensemble — pre-data declaration

## Purpose

The locked evolving R2 bridge classified

`FULLJ_EVOLVING_WEYL_BRIDGE_R2_PASS`

and the subsequent deterministic theory-grid covariance diagnostic classified

`FULLJ_EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_PASS`.

The latter is not a stochastic cosmological covariance because `sigma`, `kind`, and `beta0` are deterministic nonlinear-completion/model coordinates. This milestone therefore introduces the first actual random realization ensemble by randomizing the Fourier realization coefficients used in the one-dimensional periodic embedding.

This is a **1D Gaussian-realization Weyl spectrum/convergence diagnostic**, not a 3D isotropic cosmological power-spectrum calculation.

## Locked inputs and reference theory branch

Required ancestry:

- R2 PASS result lock: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- deterministic covariance PASS/scope-correction result: `87434c21866241b1b35588ec88e93e99a6f5db1a`

The stochastic primary test uses exactly one fixed theory branch chosen before stochastic output:

- `sigma = 0`
- `kind = simple`
- `beta0 = 1.0`

This is the same central/reference branch used by the locked R2 linear CLASS regression. No branch selection is made after seeing stochastic outputs.

The canonical D2C6 trajectory equations and R2 effective-fluid/metric closure are unchanged.

## Gaussian realization definition

The six retained input modes are the locked D2C6 modes

`n = [3,5,8,10,15,20]`

with the locked physical wavenumbers and base amplitudes

`MODE_AMP_j = sqrt(2 * WIDTH_j * P_R(k_j))`.

For realization `r` and input mode `j`, draw

`g_rj = (X_rj + i Y_rj)/sqrt(2)`

with independent

`X_rj, Y_rj ~ N(0,1)`.

Then `E[|g_rj|^2] = 1`.

The real-space basis for every CLASS/canonical/effective-fluid field in that realization is

`B_rj(x) = MODE_AMP_j * |g_rj| * cos(k_j x + arg(g_rj))`.

The same realization coefficients are used for all perturbation variables and at all times. This preserves the locked CLASS transfer-function relations while randomizing the primordial realization.

No amplitude clipping, phase clipping, rejection sampling, or post-data replacement of realizations is allowed.

## Frozen RNG and ensemble size

Use

`numpy.random.default_rng(20260912)`

and generate the complete coefficient array once in fixed order with shape `(32,6,2)` for `(realization, mode, X/Y)`.

Primary nonlinear ensemble size:

`N = 32`.

Convergence prefixes are frozen as

`N = 8, 16, 32`.

All prefixes use the first N members of the same locked 32-realization draw. No seed scan is allowed.

## Evolution and outputs

For each realization:

1. replace only the one-dimensional Fourier realization basis by the frozen Gaussian coefficients above,
2. run the existing R2 nonlinear bridge at `NX=128`, `NSTEP=4096`,
3. retain the same 9 redshift checkpoints `z = [6,5,4,3,2,1.5,1,0.5,0.2]`,
4. store the complex Weyl Fourier modes `n=0..32`,
5. retain canonical and metric-constraint health diagnostics.

No CLASS cosmological parameters, AeST parameters, nonlinear constitutive parameters, time steps, spatial resolution, or metric closure equations are changed.

For each realization the direct corrected-CLASS Weyl field assembled with the same Gaussian basis is also stored as a linear/reference spectrum. No separate linear R2 integration is required because R2 linear CLASS regression is already locked and the CLASS field assembly is linear in the realization coefficients.

## Stochastic spectrum definitions

At each redshift and prefix size N, define the centered 1D Weyl covariance

`C_N(z) = 1/(N-1) sum_r [W_r(z)-Wbar_N(z)] [W_r(z)-Wbar_N(z)]^dagger`.

The corresponding 1D mode-variance spectrum is

`S_W,N(n,z) = diag(C_N(z))`.

This is a variance of the retained one-dimensional periodic Fourier embedding. It is not labeled `P_W(k,z)` and is not inserted into a lensing integral.

Also report the direct-CLASS linear/reference spectrum from the same realizations and the nonlinear/reference ratio where the reference spectrum is numerically nonzero.

## Frozen band definitions

For convergence, use positive output modes only and three frozen mode-number bands:

- low: `n = 1..7`
- mid: `n = 8..15`
- high: `n = 16..32`

At each redshift define each band variance as the sum of `S_W,N(n,z)` over the modes in that band.

## Frozen gates

### G1 — provenance and ensemble identity

Require exact locked ancestry, exact reference theory branch, RNG seed `20260912`, exact 32 x 6 complex realization coefficient set, and unchanged R2 numerical settings.

### G2 — Gaussian coefficient normalization

Across all 32 x 6 coefficients require

`0.75 <= mean(|g|^2) <= 1.25`.

This is only an implementation sanity gate; no coefficient is rescaled to make it pass.

### G3 — finite nonlinear evolution

All 32 nonlinear realizations must complete all 9 checkpoints with finite canonical, effective-fluid, metric, and Weyl outputs.

No failed realization may be discarded or replaced.

### G4 — metric/canonical health

Across all realizations require

- metric Hamiltonian residual <= `1e-8`,
- metric momentum residual <= `1e-8`,
- metric shear residual <= `1e-8`,
- canonical constraint residual <= `1e-10`.

### G5 — stochastic covariance algebra

For every redshift and N in `{8,16,32}` require

- covariance Hermiticity relative residual <= `1e-12`,
- minimum eigenvalue / max absolute eigenvalue >= `-1e-12`,
- trace reconstruction identity relative residual <= `1e-12`.

### G6 — 8/16/32 bandpower convergence

For each of the 27 `(redshift, band)` cells define

`d16_32 = |B_32-B_16| / max(B_32,B_16,tiny)`.

Require

- median `d16_32 <= 0.25`,
- maximum `d16_32 <= 0.50`.

The `8 -> 16` changes are reported but are not required to decrease monotonically realization by realization.

### G7 — no deterministic-theory mixing

Only the fixed `(sigma=0, kind=simple, beta0=1)` branch may enter the primary stochastic covariance. The deterministic `sigma/kind/beta0` grid must not be pooled with Gaussian realizations.

## Classification

PASS:

`FULLJ_EVOLVING_WEYL_GAUSSIAN_1D_ENSEMBLE_PASS`

FAIL:

`FULLJ_EVOLVING_WEYL_GAUSSIAN_1D_ENSEMBLE_FAIL`

INCOMPLETE if locked R2 inputs/ancestry or the required corrected CLASS environment are unavailable:

`FULLJ_EVOLVING_WEYL_GAUSSIAN_1D_ENSEMBLE_INCOMPLETE`

## Interpretation lock

A PASS establishes that the locked R2 nonlinear evolving Weyl bridge supports a finite, internally consistent and prefix-convergent **1D Gaussian realization spectrum diagnostic** on the retained mode/redshift domain.

A PASS does not establish an isotropic three-dimensional cosmological Weyl power spectrum. The nonlinear evolution remains a one-dimensional periodic embedding, so direct use in a Limber/line-of-sight lensing integral is not licensed.

Therefore, regardless of PASS:

- `ONE_D_GAUSSIAN_WEYL_ENSEMBLE_TESTED=True`
- `THREE_D_ISOTROPIC_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

After a PASS, the next required milestone is an explicitly derived 3D/isotropic statistical bridge (or an equivalent shell-response construction) with its own convergence certification before any lensing projection is attempted.
