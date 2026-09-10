# NL1C6D2C6A-R1 pre-data: stable canonical-variable repair

Status: **PREREGISTERED BEFORE ANY R1 TRAJECTORY OUTPUT**.

## Purpose

Historical D2C6A remains `NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_FAIL` because the preregistered I2 initial-state metric was `2.469918916957e-10 > 1e-12`, while I1 and I3-I6 passed.

R1 tests a strictly algebraic numerical reformulation of the same D2C5 physical system. No physics parameter, constitutive function, CLASS forcing, RK4 step count, spatial resolution, checkpoint redshift, or numerical gate is relaxed.

## Stable canonical variable

Replace the evolved variable `P_alpha` by

\[
S \equiv P_\alpha + \bar Q P_\chi.
\]

The canonical elliptic identity is then represented directly as

\[
S=-2aK_B\nabla^2E-2Aa\nabla^2\chi,
\qquad A=2-K_B,
\]

and

\[
\nabla^2(K_BE+A\chi)=-\frac{S}{2a}.
\]

This avoids reconstructing the small elliptic combination by subtracting the nearly cancelling floating-point quantities `P_alpha` and `Q P_chi`.

From the already preregistered D2C6A equations,

\[
\dot P_\chi=-2Aa\nabla^2E+2Aa\nabla\cdot[(1+j_{\rm eff})\nabla\chi]-2aK_Q\nabla^2\alpha,
\]

\[
\dot P_\alpha=-P_\chi\dot{\bar Q}-2aK_Q\nabla^2\chi+2aK_Q\bar Q\nabla^2\alpha,
\]

and `S=P_alpha+Q P_chi`, the exact transformed evolution is

\[
\dot S=-2aK_Q\nabla^2\chi
-2Aa\bar Q\nabla^2E
+2Aa\bar Q\nabla\cdot[(1+j_{\rm eff})\nabla\chi].
\]

Conformal-time derivatives remain `d/dtau = a d/dt`.

At output checkpoints reconstruct

\[
P_\alpha=S-\bar QP_\chi
\]

only for reporting and the unchanged I5/I6 comparisons.

## Frozen numerical setup

Identical to D2C6A:

- corrected branch and pinned CLASS `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- sigma=0, simple interpolation, beta0=1;
- memory disabled, eta=0;
- primary `Nx=128, Nstep=4096`;
- time control `Nx=128, Nstep=8192`;
- spatial control `Nx=256, Nstep=4096`;
- explicit fixed-step classical RK4;
- redshift checkpoints `[6,5,4,3,2,1.5,1,0.5,0.2]`;
- same corrected CLASS metric forcing and exact corrected background evaluation;
- same chain-rule initial `dchi/dtau`.

## R1 gates

The numerical thresholds are unchanged from D2C6A.

R1-I1: corrected provenance and required dense inputs PASS.

R1-I2: at z=6 require direct-S canonical elliptic residual <= `1e-12`, `P_chi` definition residual <= `1e-12`, all state arrays finite, and reconstructed perturbation zero modes <= `1e-12` relative to RMS.

R1-I3: linear-control global relative L2 against corrected CLASS for alpha, E and chi each <= `5e-3`.

R1-I4: nonlinear trajectory finite; direct-S canonical residual <= `1e-10` at all stored checkpoints; finite x and j; minimum `1+j_eff > 0`; no projection, root solve, pseudo-time or branch continuation.

R1-I5: maximum time-control relative L2 over alpha, chi, P_chi and reconstructed P_alpha <= `2e-3`.

R1-I6: maximum spatial-control relative L2 over the same four fields <= `5e-3` after spectral restriction.

R1-I7: report nonlinear-vs-linear alpha/E/chi and x/j diagnostics descriptively only.

R1-I8: same scope exclusions as D2C6A.

Additionally report, descriptively only, the condition ratio

\[
\kappa_{\rm cancel}=\frac{\|P_\alpha\|+\|\bar QP_\chi\|}{\|S\|}
\]

at z=6 to document the degree of cancellation in the historical variable choice. It has no PASS/FAIL threshold.

## Classification

All applicable R1-I1 through R1-I8 gates pass:

`NL1C6D2C6AR1_STABLE_CANONICAL_VARIABLE_PASS`

Any evaluated numerical/derived gate fails:

`NL1C6D2C6AR1_STABLE_CANONICAL_VARIABLE_FAIL`

Required input unavailable before evaluation:

`NL1C6D2C6AR1_STABLE_CANONICAL_VARIABLE_INCOMPLETE`

Only R1 PASS may repair the numerical implementation gate and license the later all-27 D2C6B trajectory campaign. Historical D2C6A remains FAIL regardless of R1 outcome.
