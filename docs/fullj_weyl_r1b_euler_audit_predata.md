# Full-J evolving Weyl bridge R1B — corrected CLASS Euler identity audit predata

Status: **PREREGISTERED AFTER THE R1A CONTINUITY AUDIT AND BEFORE ANY R1B OUTPUT**.

Frozen label: `FULLJ_WEYL_R1B_EULER_AUDIT_PREDATA`.

## Motivation fixed before data

R1A established that the corrected-CLASS effective-fluid continuity equation is numerically satisfied on the 6-mode x 9-checkpoint grid: its global relative L2 residual is ~3.45e-6 and every per-mode residual is <2e-5. R1A nevertheless retained its historical FAIL because the separately preregistered algebraic `Theta_A = -lap(chi/Q-alpha)/a` identity gate was 1e-12 while finite-precision reconstruction gave ~1e-7.

The R1 full bridge had used this subtraction-based algebraic velocity reconstruction inside a 4096-step time integrator. Since `chi/Q` and `alpha` are individually many orders of magnitude larger than their difference, this map is numerically ill-conditioned even when the analytic identity is correct. No R1/R1A result or threshold is reclassified.

Before replacing that subtraction by an independently evolved effective-fluid velocity state, R1B must verify the exact corrected-CLASS Euler equation directly on the locked linear CLASS solution.

## Frozen equation

Use the exact conformal-time equation implemented by the corrected CLASS bridge:

`Theta_A' = (3 c_ad^2 - 1) Hconf Theta_A + k^2 Pi_A/(1+w_A) + k^2 Psi`,

with

`Hconf = a H`,

`w_A = p_A/rho_A`,

`c_ad^2 = K_Q/(Q K_QQ)`,

and

`Pi_A = c_ad^2 delta_A + c_ad^2 k^2 [K_B E + (2-K_B) chi]/(3 a^2 rho_A)`.

Here `Theta_A` is the corrected-CLASS `theta_cdm` variable, not the velocity potential. `delta_A`, `E`, `chi`, `Psi`, and `Theta_A'` are taken directly from the same D2C6-certified corrected CLASS splines. No nonlinear trajectory is run.

## Grid

Exactly the same 6 retained CLASS modes and 9 redshift checkpoints used by R1A, i.e. 54 points total.

## Diagnostics

Store for every point:

- CLASS `Theta_A'`;
- the frozen Euler RHS;
- residual and relative contribution norms;
- `Pi_A`;
- each RHS term separately;
- the cancellation condition number of the algebraic velocity-potential map,

`kappa_theta = (|chi/Q| + |alpha|) / max(|chi/Q-alpha|, tiny)`.

The condition number is diagnostic only. It is not used to alter any gate.

## Frozen gates

R1B PASS requires:

- global Euler relative L2 `<= 5e-3`;
- every retained mode Euler relative L2 `<= 1e-2`;
- all 54 evaluated points finite.

Classification:

- all gates pass: `FULLJ_WEYL_R1B_EULER_IDENTITY_PASS`;
- otherwise: `FULLJ_WEYL_R1B_EULER_IDENTITY_FAIL`;
- unavailable required corrected-CLASS field: `FULLJ_WEYL_R1B_EULER_IDENTITY_INCOMPLETE`.

## Consequence fixed before data

A PASS licenses a separately implemented R2 numerical-coordinate repair in which `(delta_A, Theta_A)` are evolved as the effective-fluid pair using the already derived continuity/Euler equations, while the locked canonical full-J trajectory `(alpha,chi,P_chi,S)` remains unchanged and one-way. The subtraction `chi/Q-alpha` may remain an audit identity but is not used as the evolving velocity source.

A FAIL does not license R2 and requires revisiting the effective-fluid equation/convention first.

Always:

- `NONLINEAR_TRAJECTORY_RERUN=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`
