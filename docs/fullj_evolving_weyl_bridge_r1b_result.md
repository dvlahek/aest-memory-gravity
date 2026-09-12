# Full-J evolving-FLRW Weyl bridge R1B — Euler identity result

Status: **LOCKED RESULT AFTER R1B RUN**.

Classification:

`FULLJ_WEYL_R1B_EULER_IDENTITY_PASS`

The audit used corrected CLASS linear eta=0 data only, six Fourier modes and nine checkpoints (54 points total). No nonlinear trajectory was rerun.

## Frozen equation tested

The tested corrected-CLASS Euler identity was

\[
\Theta_A'=(3c_{\rm ad}^2-1)\mathcal H\Theta_A+
\frac{k^2\Pi_A}{1+w_A}+k^2\Psi,
\]

with

\[
\Pi_A=c_{\rm ad}^2\delta_A+
\frac{c_{\rm ad}^2k^2}{3a^2\rho_A}
\left[K_BE+(2-K_B)\chi\right].
\]

## Numerical result

All 54/54 audit points were finite.

Global relative L2 residual:

`5.149143371689e-06`.

Per-mode relative L2 residuals:

- k=0.0201997391725 Mpc^-1: `5.421723829160e-06`
- k=0.0336662319542 Mpc^-1: `1.762768379213e-05`
- k=0.0538659711268 Mpc^-1: `5.838195231461e-06`
- k=0.0673324639085 Mpc^-1: `1.414539828313e-05`
- k=0.100998695863 Mpc^-1: `6.044162525448e-06`
- k=0.134664927817 Mpc^-1: `4.859351891114e-06`

All frozen R1B gates passed:

- all 54 points finite;
- global residual <=5e-3;
- every per-mode residual <=1e-2.

## Conditioning diagnosis

The algebraic map

\[
\Theta_A=-a^{-1}\nabla^2(\chi/Q-\alpha)
\]

is numerically ill-conditioned on the D2C6 state representation. The measured condition-number proxy across the 54 linear audit points was:

- minimum `4.239103414039e+06`;
- median `1.378245690062e+09`;
- p84 `1.346743045886e+10`;
- maximum `3.546682937362e+11`.

This directly supports the interpretation of the historical R1 failure: the effective-fluid equations themselves are consistent with corrected CLASS, while repeated reconstruction of Theta_A through subtraction of nearly equal large canonical variables is numerically unstable.

R1A had already shown that the continuity equation is accurate at global relative L2 `3.451211231004e-06`; R1B now independently certifies the Euler equation at comparable accuracy. Therefore the next bridge is allowed to evolve `(delta_A, Theta_A)` directly as the effective-fluid pair instead of recomputing Theta_A from `chi/Q-alpha` at each RK stage.

## Licensing

This PASS licenses an R2 evolving-Weyl bridge diagnostic with a directly evolved effective-fluid pair `(delta_A,Theta_A)` and the already frozen corrected-CLASS/D2C5 closure. It does not license evolving Weyl power, ACT likelihood, or observational claims by itself.

Always:

- `NONLINEAR_TRAJECTORY_RERUN=False` for this audit;
- `EVOLVING_WEYL_POWER_LICENSED=False`;
- `ACT_LIKELIHOOD_LICENSED=False`;
- `OBSERVATIONAL_CLAIM_LICENSED=False`.
