# NL1C6D1B predata — linear scalar-mode regression implementation

Status: **PREREGISTERED BEFORE NL1C6D1B NUMERICAL FREQUENCY RESULTS**.

Frozen test label:

```text
NL1C6D1B_PREDATA_LINEAR_SCALAR_MODE_REGRESSION
```

This is a subtest of `NL1C6D1_PREDATA_DYNAMICAL_FORMULATION_AUDIT`. It does not constitute the full D1 audit and cannot by itself permit D2.

## Published target and repository mapping

The Minkowski scalar sector of Skordis & Zlosnik, Phys. Rev. D 106, 104041 (2022), has one propagating massive scalar normal mode with

```text
omega^2 = c_s^2 k^2 + M^2
c_s^2 = (2-K_B)/(K2 K_B) * (1 + 0.5 K_B lambda_s)
M^2   = (2-K_B)(1+lambda_s) Q0^2 / K_B
```

in the reference convention. The same paper defines the gauge-invariant scalar combination `chi = varphi + Q0 alpha` and the quasistatic expansion has `J_Y -> lambda_s` in the tracking/high-gradient limit. The repository interpolation convention has `j -> 1/beta0`, therefore the frozen map is

```text
lambda_s = 1/beta0.
```

The static weak-field mass parameter is separately

```text
mu^2 = 2 K2 Q0^2/(2-K_B).
```

`mu^2` MUST NOT be substituted for the propagating-mode `M^2`.

Frozen repository constants:

```text
H0 = 67.3324639084866 km/s/Mpc
h  = 0.673324639084866
K_B = 0.0665
K2 = 9500
Q0 = 1e-4 Mpc^-1
beta0 = {1.0, 0.5, 0.1}
```

The six frozen physical Fourier wavenumbers are the existing repository low-k modes

```text
k_h = {0.03, 0.05, 0.08, 0.10, 0.15, 0.20} h/Mpc
k = h k_h in Mpc^-1.
```

## Dynamical variable for D1B only

D1B evolves the already constraint-reduced propagating scalar normal-mode coordinate `X_k`. It is NOT yet an evolution of the nonlinear repository field `chi`.

For each Fourier mode the reduced Hamiltonian oscillator is represented by the canonical pair `(X,P)` with

```text
dX/dt = P/2
dP/dt = -2 omega_ref^2 X,
```

which implies

```text
d2X/dt2 + omega_ref^2 X = 0.
```

This is only a numerical regression of the published propagating normal mode. Constraint reconstruction and the nonlinear map to `(Phi, tildePhi, chi)` remain separate D1 gates.

## Frozen numerical method

- deterministic velocity-Verlet / leapfrog integration of `(X,P)`;
- initial `X=1e-8`, `P=0`;
- no damping, forcing, filtering, fitting regularizer, or constraint projection;
- primary frequency run: `80` steps per analytic period;
- duration: `24` analytic periods;
- frequency estimator: linearly interpolated downward zero crossings of `X`; discard the first and last complete crossing interval and use the mean period of the remaining intervals;
- numerical floor in the preregistered squared-frequency relative error: `1e-12 Mpc^-2`;
- primary gate for every `beta0 x k` case:

```text
abs(omega_num^2-omega_ref^2)/max(abs(omega_ref^2),1e-12) <= 5e-3.
```

## Frozen convergence check

Second-order convergence is tested on the two extreme repository modes, `0.03` and `0.20 h/Mpc`, for all three beta0 values. Runs use `40`, `80`, and `160` steps per analytic period with the same 24-period window and estimator.

For consecutive resolutions define

```text
p_40_80  = log2(error_40/error_80)
p_80_160 = log2(error_80/error_160),
```

where `error = abs(omega_num^2-omega_ref^2)`.

Both observed orders must satisfy

```text
p >= 1.8
```

for all six representative convergence cases. If an error is at floating-point zero, the corresponding order is recorded as `inf` and passes.

## D1B classification

All 18 primary frequency cases pass and all six convergence cases satisfy both order gates:

```text
NL1C6D1B_LINEAR_SCALAR_MODE_REGRESSION_PASS
```

Otherwise:

```text
NL1C6D1B_LINEAR_SCALAR_MODE_REGRESSION_FAIL
```

A D1B PASS is necessary but not sufficient for `NL1C6D1_DYNAMICAL_FORMULATION_AUDIT_PASS`. In particular D1-A derivation/mapping, D1-C constraints, D1-D quasistatic full-J identity, and D1-E large-gradient identity must still pass independently.

## References

- C. Skordis and T. Zlosnik, *Aether scalar tensor theory: Linear stability on Minkowski space*, Phys. Rev. D 106, 104041 (2022), arXiv:2109.13287.
- P. Verwayen, C. Skordis and C. Boehm, *Aether Scalar Tensor theory: quasistatic spherical solutions and their phenomenology*, MNRAS 531, 272–289 (2024), doi:10.1093/mnras/stae1225.
