# NL1C2 result — screened/high-gradient asymptotic reclosure

Final classification: **NL1C2_SCREENED_ASYMPTOTIC_RECLOSURE_PASS**

Predata commit: `5c35e58824036ad67f89c75e7fa483772c35602f`.

Implementation commit: `2d26f7314ec18e17062ea104d03b412c3e5fa31a`.

Workflow commit: `6bbaa367b91e46e3c6f622799909cfe16941c64c`.

GitHub Actions run: `34333799473` — technical SUCCESS.

Artifact: `results_bundle_nl1c2_screened_asymptotic_reclosure`, artifact ID `10096842798`, SHA256 `00778026f2bf92e43efdf77c974b51aab56a554bbbae447f0f655292e30bd3bb`.

Scope: result-informed theory/coefficient and mass-scale audit only. No time-dependent reclosed cosmology, no finite-eta nonlinear prediction, no likelihood, and no observational data were used.

## 1. Full-J saturation at the measured physical amplitude

NL1C0 fixed the physical-gradient checkpoints

\[
x_{\rm phys}\in\{1.0911\times10^7,\;4.3274\times10^7,\;9.4551\times10^7\}.
\]

Across all nine co-primary combinations of `Simple/Exponential/Sharp` and `beta0={1,0.5,0.1}`, the full published interpolation coefficient is already saturated to

\[
j_\infty=1/\beta_0.
\]

The worst saturation error over all physical checkpoints is

\[
\boxed{\epsilon_{\rm sat,max}=1.00816\times10^{-6}},
\]

and the worst logarithmic coefficient stiffness is

\[
\boxed{s_{j,\max}=1.00816\times10^{-6}}.
\]

Both are below the preregistered `2e-6` gates.

The worst case is the slowly saturating Simple interpolation at `beta0=0.1` and the smallest measured physical gradient. Exponential and Sharp are already numerically at their exact asymptotic coefficients over the tested physical checkpoints.

Thus, at the physical amplitude already measured in the certified late-time band, interpolation-family uncertainty in the Y-sector coefficient is at most at the part-per-million level.

## 2. Frozen AeST mass scale

Using the published relation

\[
\mu^2=\frac{2K_2Q_0^2}{2-K_B}
\]

with the frozen values `K_B=0.0665`, `K2=9500`, and `Q0=1e-4 Mpc^-1` gives

\[
\boxed{\mu=9.912991\times10^{-3}\ {\rm Mpc}^{-1}},
\]

or

\[
\boxed{\mu^{-1}=100.878\ {\rm Mpc}}.
\]

For the three beta0 values, the large-gradient Helmholtz scales

\[
k_\mu=\sqrt{1+\beta_0}\,\mu
\]

are approximately `0.01402`, `0.01214`, and `0.01040 Mpc^-1` for `beta0=1,0.5,0.1` respectively.

Every frozen mode in `0.03 <= k_h <= 0.20 h/Mpc` lies above `k_mu`. The smallest ratio is

\[
\boxed{\min(k/k_\mu)=1.44087},
\]

so there is no high-gradient Helmholtz pole crossing inside the certified band.

## 3. Scale dependence of the mass term

In the historically identified structured-memory sub-band

\[
0.08\le k_h\le0.20\ h/{\rm Mpc},
\]

the largest asymptotic Helmholtz-to-Poisson transfer correction is

\[
\boxed{\max |R_H-1|=0.072656},
\]

or about `7.27%`, attained at the low edge `k_h=0.08 h/Mpc` for `beta0=1`.

The correction falls rapidly with k. For `beta0=1` it is about `4.53%` at `0.10`, `1.96%` at `0.15`, and `1.10%` at `0.20 h/Mpc`.

The context-only low modes are more sensitive to the mass scale: at `0.03 h/Mpc` the asymptotic correction can be order unity. This is reported explicitly and was not hidden by the signal-band gate.

## 4. Physical interpretation

The important result is not merely that the full interpolation functions are numerically stable. The physical-amplitude state is so deep in the high-gradient branch that

\[
\mathcal J_{\mathcal Y}\simeq 1/\beta_0
\]

to part-per-million accuracy over all co-primary interpolation choices.

Therefore the Y-sector no longer behaves like the deep-MOND nonlinear operator

\[
\nabla\cdot(|\nabla\chi|\nabla\chi).
\]

At the measured physical amplitude it is, to controlled accuracy, a **screened linear spatial stiffness** proportional to

\[
\frac1{\beta_0}\nabla^2\chi,
\]

with the frozen AeST mass scale supplying an additional scale-dependent Helmholtz term.

This substantially simplifies the strong path. A physical-amplitude reclosure does not require carrying the detailed Simple/Exponential/Sharp pointwise nonlinearity in the certified signal band. The next calculation can use the saturated coefficient as a controlled amplitude-resummed limit, while retaining the exact beta0 and mu dependence.

This does not yet prove that the original memory signal survives the reclosure. That question remains the next dynamical test.

## 5. Next locked task

The next step is **NL1C3: screened-resummed dynamical bridge**. It must derive the time-dependent scalar/aether equations from the frozen covariant AeST action with `J_Y=1/beta0` in the physical-amplitude high-gradient branch, reproduce the published static Helmholtz limit, and then add the already frozen NL0B eta=0 memory tangent without introducing a GR/Poisson toy closure.

Historical v0.77/v0.78, NL1C0, NL1C1 and all earlier PASS/FAIL classifications remain unchanged.
