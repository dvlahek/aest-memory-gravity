# NL1C6D2C6B pre-data — all-27 physical nonlinear FLRW trajectories

Status: **PREREGISTERED BEFORE ANY D2C6B ALL-27 TRAJECTORY RESULT**.

Frozen label:

```text
NL1C6D2C6B_PREDATA_ALL27_PHYSICAL_NONLINEAR_TRAJECTORIES
```

Historical classifications remain immutable. In particular,

```text
NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_FAIL
```

remains the historical result of the original canonical representation, while the separately preregistered stable-canonical repair

```text
NL1C6D2C6AR1_STABLE_CANONICAL_VARIABLE_PASS
```

from GitHub Actions run `34445918519`, head `6f9defb69566c33b2190c0765ef50df5e787d4d7`, is the sole license for this campaign.

## 1. Scientific question

Does the action-derived physical-time nonlinear FLRW scalar-current evolution remain numerically controlled across the entire preregistered covariant completion family, and is the finite-amplitude nonlinear trajectory response robust or measurably sensitive to the completion ambiguity?

D2C6B is a trajectory campaign at `eta=0`. It does not enable the retarded-memory bath, finite physical eta, observational likelihoods, a refit, halo formation, or branch selection.

## 2. Frozen 27-member completion family

Use every Cartesian-product combination of

```text
sigma in {-1, 0, +1}
kind  in {simple, exponential, sharp}
beta0 in {1.0, 0.5, 0.1}
```

for exactly 27 co-primary members. No member may be removed, promoted, reranked, or assigned a different numerical gate after an output is inspected.

The completion is the derivative-bounded D2C4/D2C4R1 family, not the superseded earlier D2C/D2C3 additive family. Freeze

```text
epsilon_mix = 0.25
S(x) = x^2/(1+x^2)
G2(Z) = tanh(Z)^2
```

and

\[
j_{\rm eff}(x,Z;\sigma,\beta_0,\mathrm{kind})
=j(x;\beta_0,\mathrm{kind})
\left[1+\sigma\,\epsilon_{\rm mix}\,S(x)G_2(Z)\right].
\]

The three base interpolation functions `j(x)` and all physical constants are exactly those already frozen in D2C4/D2C5:

```text
K_B = 0.0665
K2  = 9500
Q0  = 1e-4 Mpc^-1
Z0  = 1e-17 Mpc^-1
a0  = 1.2e-10 m s^-2
```

The corrected Exp homogeneous background and its exact physical-time evaluation are unchanged.

## 3. Frozen input state and interval

Use the same isolated corrected CLASS build, cosmological parameter set, six signal-band modes,

```text
k_h = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20] h/Mpc
```

same deterministic phases/primordial amplitudes, and the same physical interval/checkpoints

```text
z = [6, 5, 4, 3, 2, 1.5, 1, 0.5, 0.2].
```

Memory remains disabled and `aest_eta=0`.

The exact background evaluation remains

\[
H=\frac{a'}{a^2},\qquad K_Q=\frac{I_0}{a^3},\qquad
\dot Q=-3H\frac{K_Q}{K_{QQ}},
\]

with no clipping, extrapolation, empirical damping, post-step projection, or outcome-dependent background modification.

## 4. Stable canonical evolution

Use the D2C6A-R1 variable

\[
S_c\equiv P_\alpha+\bar Q P_\chi
\]

directly. The subscript `c` only distinguishes this canonical variable from the constitutive shape `S(x)` above.

Retain

\[
P_\chi=2a^3K_{QQ}U,
\qquad
U=\dot\chi-\bar Q E-\dot{\bar Q}\alpha,
\]

and reconstruct

\[
E=\frac{\nabla^{-2}[-S_c/(2a)]-A\chi}{K_B},
\qquad A=2-K_B.
\]

The exact transformed equations are the already validated R1 equations, with the only member dependence occurring in the D2C5 projected scalar-current divergence:

\[
\dot\alpha=E-\Psi,
\]

\[
\dot\chi=U+\bar Q E+\dot{\bar Q}\alpha,
\]

\[
\dot P_\chi=-2Aa\nabla^2E
+2Aa\nabla\cdot[(1+j_{\rm eff})\nabla\chi]
-2aK_Q\nabla^2\alpha,
\]

\[
\dot S_c=-2aK_Q\nabla^2\chi
-2Aa\bar Q\nabla^2E
+2Aa\bar Q\nabla\cdot[(1+j_{\rm eff})\nabla\chi].
\]

The implementation may use conformal-time RHS values exactly as in D2C6A-R1 by multiplying the cosmic-time equations by `a`. No other equation change is allowed.

## 5. Frozen numerical representation

Retain the D2C6A-R1 pseudospectral representation and 2/3 dealiased nonlinear flux.

For every one of the 27 nonlinear members use:

```text
primary:       Nx=128, RK4 steps=4096
time control:  Nx=128, RK4 steps=8192
space control: Nx=256, RK4 steps=4096
```

Use the exact fixed time grid `t_n=t_0+n h`, with the final node explicitly equal to `t_1`, as already validated in D2C6A-R1.

A single shared linear control at `Nx=128`, 4096 RK4 steps is sufficient and is frozen here because the action-derived D2C5 linear limit is independent of `sigma`, `kind`, `beta0`, `epsilon_mix`, and `a0`. The shared linear control must still reproduce the same frozen CLASS trajectory within the inherited D2C6A linear gates.

No adaptive timestep, member-specific resolution, solver fallback, clipping, saturation override, or member-specific tolerance is permitted.

## 6. Locked gates

### B1. Provenance and family coverage

Require the corrected CLASS provenance audit to pass and require exactly the 27 unique Cartesian-product members declared in Section 2. Any missing or duplicated member is a FAIL.

### B2. Shared initial-state and linear regression

Recompute the stable R1 initial state once. Require

```text
max(initial elliptic residual,
    P_chi-definition residual,
    zero-mode residuals) <= 1e-12
```

and all values finite.

For the shared linear control versus CLASS at all nine checkpoints require the unchanged D2C6A limits

```text
alpha <= 5e-3
E     <= 5e-3
chi   <= 5e-3.
```

### B3. Per-member trajectory health

For every member and every stored checkpoint require

```text
all state/field diagnostics finite
canonical constraint residual <= 1e-10
min(1 + j_eff) > 0.
```

A failure in any co-primary member fails the conjunctive D2C6B numerical gate. It is not permission to drop that member.

### B4. Per-member timestep convergence

Retain the inherited D2C6A/R1 convergence metric exactly. For each member compare the complete stored canonical state arrays

```text
(alpha, chi, P_chi, P_alpha)
```

between the `Nx=128, 4096` primary run and the `Nx=128, 8192` time-control run. Here `P_alpha` is the reconstructed historical canonical variable `S_c-Q P_chi` used by the inherited R1 output/comparison convention.

For each of the four states compute the inherited full-array relative L2 discrepancy over all nine checkpoints and spatial samples. The maximum over the four states must satisfy

```text
<= 2e-3
```

for every one of the 27 members.

### B5. Per-member spatial convergence

Retain the inherited D2C6A/R1 spatial comparison exactly. For each member, for each stored canonical state

```text
(alpha, chi, P_chi, P_alpha),
```

spectrally resample every `Nx=256` checkpoint field to `Nx=128` using the already frozen `static.spectral_resample` routine, then compute the same full-array relative L2 discrepancy against the `Nx=128` primary run.

The maximum over the four canonical states must satisfy

```text
<= 5e-3
```

for every one of the 27 members.

### B6. Scope

No memory bath, finite eta, likelihood, observational data, refit, parameter optimization, completion selection, or post-result gate change is allowed.

## 7. Preregistered physics diagnostics — not PASS/FAIL gates

For each member report the full-trajectory relative nonlinear response against the single shared linear control,

\[
R_f=\frac{\|f_{\rm NL}-f_{\rm lin}\|_2}{\|f_{\rm lin}\|_2},
\qquad f\in\{\alpha,E,\chi\},
\]

using all nine checkpoints. Report the 27-member minimum, median, maximum, and the member attaining each extreme.

Also report `x_max`, `x_p01`, `x_p50`, `x_p99`, spatial fractions in the frozen gradient-regime bins, `j_eff_max`, and `min(1+j_eff)` for every member.

For each fixed `(kind,beta0)` and each field, define completion displacement

\[
C_f^{\pm}=\frac{\|f_{\sigma=\pm1}-f_{\sigma=0}\|_2}
{\|f_{\sigma=0}\|_2}.
\]

For each fixed `(kind,beta0)` define a conservative block numerical floor `N_block` as the largest inherited B4 timestep maximum or B5 spatial maximum among the three `sigma` members in that block. This deliberately uses the already frozen canonical convergence gate rather than introducing a new post hoc field-specific tolerance.

A completion displacement is labelled **resolved** only when

\[
C_f^{\pm}>10N_{\rm block}.
\]

This label is diagnostic and does not affect D2C6B PASS/FAIL. Resolved differences are reported as completion dependence; unresolved differences are reported as completion-insensitive at the achieved numerical resolution. No favorable completion is selected.

## 8. Classification

If B1-B6 pass for all 27 co-primary members:

```text
NL1C6D2C6B_ALL27_PHYSICAL_NONLINEAR_TRAJECTORIES_PASS
```

If at least one evaluated co-primary member violates a frozen numerical/health gate:

```text
NL1C6D2C6B_ALL27_PHYSICAL_NONLINEAR_TRAJECTORIES_FAIL
```

If the required corrected input, variable mapping, or complete 27-member evaluation cannot be constructed before a valid all-27 physics result exists:

```text
NL1C6D2C6B_ALL27_PHYSICAL_NONLINEAR_TRAJECTORIES_INCOMPLETE
```

PASS establishes a numerically controlled physical-time nonlinear scalar-current trajectory family under the preregistered weak-field FLRW reduction. It does not by itself establish nonlinear matter growth, halo formation, finite-memory physics, or observational agreement.

## 9. Continuation rule

Only D2C6B PASS may license the next preregistered nonlinear-memory step. The next step must first evolve the already certified `eta=0` retarded bath/tangent on the D2C6B nonlinear trajectories before any finite physical eta or observational likelihood is evaluated.
