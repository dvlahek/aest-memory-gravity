# NL1C2 predata — screened/high-gradient asymptotic reclosure

Classification before result: **NL1C2_PREDATA_SCREENED_ASYMPTOTIC_RECLOSURE**

This is a result-informed theory diagnostic created after `NL1C0_LINEAR_STATE_HIGH_GRADIENT_REGIME` and `NL1C1_FULL_Y_OPERATOR_BRIDGE_PASS`, before any screened-resummed cosmological evolution or eta-memory tangent around that state.

Historical classifications remain immutable.

## 1. Purpose

NL1C0 established that the physical-amplitude late-time state in the certified band has

\[
1.0911\times 10^7 \le x_{\rm rms}=\sqrt{\mathcal Y}_{\rm rms}/a_0 \le 9.4551\times 10^7.
\]

NL1C1 validated all three published interpolation functions for all three frozen beta0 values. NL1C2 asks a narrower question before a dynamical reclosure is attempted:

> At the physical gradient amplitudes already measured, has the full published Y-sector effectively saturated to its screened/high-gradient coefficient, and what mass-scale correction follows from the frozen AeST parameters over the certified k band?

This is not a nonlinear-growth result and does not use observational likelihood data.

## 2. Frozen theory inputs

Use exactly

- `K_B = 0.0665`;
- `K2 = 9500`;
- `Q0 = 1e-4 Mpc^-1`;
- `H0 = 67.3324639084866 km/s/Mpc`;
- `beta0 in {1, 0.5, 0.1}` as co-primary;
- `Simple`, `Exponential`, and `Sharp` as co-primary interpolation functions;
- certified band `k_h = {0.03,0.05,0.08,0.10,0.15,0.20} h/Mpc`;
- historically identified structured-signal sub-band `0.08 <= k_h <= 0.20 h/Mpc`;
- physical-gradient checkpoints from NL1C0: `x = {1.0911e7, 4.3274e7, 9.4551e7}`.

The published high-gradient coefficient is

\[
j_\infty=\frac1{\beta_0}.
\]

The three frozen functions are

\[
j_S(x)=\frac{x}{1+\beta_0+\beta_0x},
\]

\[
j_E(x)=\frac1{\beta_0}\left[1-e^{-\beta_0x/(1+\beta_0)}\right],
\]

and the numerically stable but algebraically identical Sharp form

\[
j_H(x)=\min\left(\frac{x}{1+\beta_0},\frac1{\beta_0}\right).
\]

## 3. Frozen AeST mass scale

Use the published AeST relation

\[
\mu^2=\frac{2K_2Q_0^2}{2-K_B}.
\]

For the large-gradient branch, the static weak-field equation reduces to

\[
\nabla^2\Phi+(1+\beta_0)\mu^2\Phi=4\pi G_N\rho,
\]

so define

\[
k_\mu(\beta_0)=\sqrt{1+\beta_0}\,\mu.
\]

For Fourier modes with `k > k_mu`, define the magnitude of the Helmholtz-to-Poisson transfer correction

\[
R_H(k,\beta_0)=\frac{k^2}{k^2-k_\mu^2}.
\]

This quantity is reported as an asymptotic scale diagnostic only. It is not substituted for the full time-dependent cosmological equations.

## 4. Locked saturation diagnostics

For every interpolation/beta0 pair and each frozen physical-gradient checkpoint, compute

\[
\epsilon_{\rm sat}=|\beta_0 j(x)-1|.
\]

Also compute the local logarithmic coefficient stiffness

\[
s_j=\left|\frac{x j'(x)}{j(x)}\right|.
\]

At the smallest physical-gradient checkpoint `x=1.0911e7`, both must satisfy

- `epsilon_sat <= 2e-6`;
- `s_j <= 2e-6`.

These gates test that the full Y-sector is already numerically indistinguishable, at the physical amplitude, from the screened coefficient `1/beta0` to a few parts per million.

## 5. Locked mass-scale diagnostics

For every beta0:

1. `mu` must be finite and positive;
2. every frozen `k_h` mode must satisfy `k > k_mu`, so no mode in the certified band crosses the high-gradient Helmholtz pole;
3. on the historically identified structured-signal sub-band `0.08 <= k_h <= 0.20 h/Mpc`, require
   \[
   |R_H-1| <= 0.10.
   \]

The lower context modes `0.03` and `0.05 h/Mpc` are reported but are not required to satisfy the 10% signal-band bound.

## 6. Classification

If all frozen saturation/stiffness and mass-scale gates pass:

**NL1C2_SCREENED_ASYMPTOTIC_RECLOSURE_PASS**

Otherwise:

**NL1C2_SCREENED_ASYMPTOTIC_RECLOSURE_FAIL**

## 7. Interpretation rule

A PASS establishes only that, at the already measured physical gradient amplitude, all nine published full-J branches have collapsed to the same screened/high-gradient coefficient to the preregistered accuracy, and that the frozen AeST mass scale does not introduce a pole in the certified band.

A PASS would justify replacing the expensive pointwise interpolation function by its controlled saturated coefficient in the next **screened-resummed dynamical bridge**, while retaining the exact beta0 dependence and the frozen mu term.

It does **not** establish a self-consistent cosmological solution, nonlinear suppression, memory survival, halo formation, or observational agreement. The next step after PASS is to derive/implement the time-dependent screened-resummed AeST scalar bridge and compute the eta=0 memory tangent around that reclosed baseline.

No GR/Poisson toy closure may be used as a substitute for that dynamical bridge.
