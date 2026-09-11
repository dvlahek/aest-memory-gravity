# Full-J local Weyl covariance derived diagnostic

Date: 2026-09-11

Status: **POST-LOCK DERIVED DIAGNOSTIC DESIGN**

This is not an independent preregistered physics test. Its inputs are already locked and inspected. The purpose is to make the statistical consequence of the locked mode-coupled Jacobian explicit and reproducible, without introducing a new nonlinear solve, fit parameter, or observational claim.

Parent:

```text
fullj-weyl-lensing-closure-audit
d0701d292ca794dc63f6ec4ba5f731e1184fbd7a
FULLJ_STATIC_SNAPSHOT_WEYL_OPERATOR_IDENTITY_PASS
```

## Tangent-coordinate covariance

For each of the 27 locked nonlinear backgrounds, the local full-J Jacobian provides the complex response matrix

\[
K^\Phi_{ij}=\frac{\partial \Phi_{k_i}}{\partial S_{k_j}}
\]

for the 13 **phase-aligned real tangent directions** used by the certified Jacobian test. The static snapshot Weyl identity gives

\[
K^W=2K^\Phi.
\]

For a covariance `C^S` in those 13 tangent coordinates,

\[
C^W=K^W C^S K^{W\dagger}.
\]

The output Weyl variance at coordinate `i` is

\[
P^W_i=(C^W)_{ii}.
\]

This is a local covariance in the certified finite tangent basis. Because the nonlinear background breaks translation invariance and only one phase-aligned direction per k was calibrated, this is **not** yet a general random-phase cosmological Fourier covariance.

## Two transparent covariance probes

No covariance model is fitted. Two diagnostic choices are reported.

### Unit tangent covariance

\[
C^S_{j\ell}=\delta_{j\ell}.
\]

This measures the geometry of the local response operator independently of the frozen source-amplitude spectrum.

### Frozen-shape tangent covariance

Let `A_j=|S_j|` be the locked absolute RHS Fourier amplitude already stored in each Jacobian record. Define

\[
C^S_{j\ell}\propto A_j^2\delta_{j\ell}.
\]

The overall proportionality is normalized away by dividing the variances by their positive median. This probe therefore uses only the locked **spectral shape** of the source, not its arbitrary global normalization.

## Reported coupling diagnostics

For each output coordinate,

\[
P^{W,\mathrm{diag}}_i=|K^W_{ii}|^2 C^S_{ii},
\]

\[
R_i=\frac{P^W_i}{P^{W,\mathrm{diag}}_i},
\]

and

\[
f^{\mathrm{off}}_i=1-\frac{P^{W,\mathrm{diag}}_i}{P^W_i}.
\]

`R_i=1` means the scalar/diagonal response is sufficient in this tangent basis. `R_i>1` quantifies the power missed by dropping off-diagonal response. `f_off` is the fraction of output variance supplied by off-diagonal tangent directions for diagonal input covariance.

The previously identified `z=0.25, k_out=0.6 Mpc^-1` node is reported separately, but no threshold on its size is used to manufacture a PASS/FAIL result.

## Algebraic health only

The only hard checks are identities that must hold for a correctly constructed covariance:

- all 27 locked backgrounds present;
- locked Jacobian classification matches exactly;
- finite nonnegative input variances;
- `C^W` Hermitian to relative residual `<=1e-12`;
- Hermitianized `C^W` positive semidefinite within relative numerical tolerance `1e-12` of its largest eigenvalue;
- all reported variances finite and nonnegative to roundoff.

If these checks hold, the classification is

```text
FULLJ_LOCAL_WEYL_COVARIANCE_DERIVED_COMPLETE
```

Otherwise:

```text
FULLJ_LOCAL_WEYL_COVARIANCE_ALGEBRAIC_FAIL
```

No physical outcome threshold is defined because this is a deterministic derived diagnostic from already inspected locked inputs.

## Scope

```text
STATIC_SNAPSHOT_ONLY=True
PHASE_ALIGNED_TANGENT_BASIS_ONLY=True
COSMOLOGICAL_RANDOM_PHASE_ENSEMBLE=False
EVOLVING_FLRW_WEYL_POWER_LICENSED=False
ACT_LIKELIHOOD_LICENSED=False
OBSERVATIONAL_CLAIM_LICENSED=False
```

A true cosmological power prediction would still require either a certified statistical response over phase/background realizations or a more complete nonlinear stochastic evolution, followed by the evolving metric/Weyl closure and line-of-sight projection.
