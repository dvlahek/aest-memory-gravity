# Full-J evolving-FLRW Weyl bridge R2 — directly evolved effective-fluid pair predata

Status: **PREREGISTERED AFTER THE LOCKED R1B EULER PASS AND BEFORE ANY R2 WEYL OUTPUT**.

Frozen label: `FULLJ_EVOLVING_WEYL_BRIDGE_R2_PREDATA`.

## Motivation fixed before data

R1A established that the corrected-CLASS effective-fluid continuity equation is satisfied at global relative L2 `3.451211231004e-06` over six modes and nine checkpoints. R1B independently established that the corrected-CLASS Euler equation is satisfied at global relative L2 `5.149143371689e-06`, with all 54/54 points finite and every per-mode residual below `1e-2`.

R1B also measured severe conditioning of the algebraic map

`Theta_A = -lap(chi/Q-alpha)/a`,

with a condition-number proxy from `4.239103414039e+06` to `3.546682937362e+11`, median `1.378245690062e+09`.

Therefore R2 removes repeated evaluation of this ill-conditioned subtraction from the time-stepping RHS. This is a numerical-state reparameterization only. No physical coefficient, branch, background, nonlinear J law, initial condition, threshold, or retained weak-field equation is changed.

The historical R0 and R1 FAIL classifications remain unchanged.

## Frozen R2 state and one-way structure

The locked D2C6 nonlinear scalar-current state remains

`(alpha, chi, P_chi, S)`

and its RHS is unchanged. In particular, the canonical D2C6 trajectory does not depend on the R2 fluid variables or reconstructed R2 metric.

R2 augments this locked trajectory by directly evolving the effective-fluid pair

`(delta_A, Theta_A)`.

The canonical state enters the fluid pair only through the already frozen pressure closure

`Pi_A = c_ad^2 delta_A - c_ad^2 lap[K_B E + (2-K_B) chi]/(3 a^2 rho_A)`.

The R2 metric reconstruction uses the same corrected-CLASS baseline and the same D2C6G Hamiltonian/momentum/shear projection as R0/R1.

## Frozen equations

Background quantities:

`rho_A = (Q K_Q-K)/3`,

`p_A = K/3`,

`w_A = p_A/rho_A`,

`c_ad^2 = K_Q/(Q K_QQ)`,

`rho_A+p_A = Q K_Q/3`.

Pressure closure:

`Pi_A = c_ad^2 delta_A - c_ad^2 lap[K_B E + (2-K_B) chi]/(3 a^2 rho_A)`.

Metric-source differences relative to corrected CLASS:

`Delta rho_A = rho_A (delta_A-delta_A_CLASS)`,

`Delta q_A = (rho_A+p_A) (Theta_A-Theta_A_CLASS)`,

`Delta shear_A = 0`.

Metric projection:

`X = Delta Phi' + Hconf Delta Psi`,

`k^2 X = (3/2) a^2 Delta q_A`,

`k^2 Delta Phi + 3 Hconf X + (3/2) a^2 Delta rho_A = 0`,

`k^2(Delta Psi-Delta Phi)=0` for the nonlinear correction at retained order.

Total metric:

`Phi = Phi_CLASS + Delta Phi`,

`Psi = Psi_CLASS + Delta Psi`,

`W = Phi+Psi`,

`Phi' = Phi_CLASS' + X - Hconf Delta Psi`.

Effective-fluid continuity equation:

`delta_A' = 3 Hconf (w_A delta_A-Pi_A) + (1+w_A)(3 Phi'-Theta_A)`.

Effective-fluid Euler equation:

`Theta_A' = (3 c_ad^2-1) Hconf Theta_A - lap[Pi_A/(1+w_A) + Psi]`.

The real-space Laplacian convention is the same spectral operator used in D2C6; for a Fourier mode `-lap -> k^2`, so this exactly reproduces the R1B mode equation.

## Initial conditions

At the locked D2C6 start redshift `z=6`:

`delta_A(z=6) = delta_A_CLASS(z=6)`,

`Theta_A(z=6) = Theta_A_CLASS(z=6)`.

No canonical-to-fluid algebraic reconstruction is used for initialization or time stepping.

## Numerical rule

Use exactly the locked D2C6 numerical grid:

- `Nx=128`;
- `Nstep=4096`;
- the same fixed-grid classical RK4 interval;
- the same nine checkpoints;
- the same 27 nonlinear members.

Integrate `(alpha,chi,P_chi,S,delta_A,Theta_A)` together as a triangular system. The canonical RHS must not read `delta_A`, `Theta_A`, `Phi_R2`, or `Psi_R2`.

No refit, rescaling, smoothing, clipping, sign change, mode removal, checkpoint removal, adaptive tolerance, or gate change is permitted after results are seen.

## Frozen gates

### G1 — source/equation provenance

All identities used by R2 must be traceable to D2C5, corrected CLASS, R1A, or R1B. The exact algebraic identity

`rho_A+p_A = Q K_Q/3`

must hold to relative error `<=1e-12`; the nonlinear completion adds zero retained shear source. R1A and R1B PASS commits must be ancestors of the R2 run.

The ill-conditioned algebraic map `Theta_A=-lap(chi/Q-alpha)/a` is diagnostic only and is explicitly not a R2 gate or RHS source.

### G2 — linear corrected-CLASS regression

With nonlinear completion disabled, the directly evolved R2 pair and reconstructed metric must reproduce corrected CLASS over all nine checkpoints with relative L2

- `delta_A <=5e-3`,
- `Theta_A <=5e-3`,
- `Phi <=5e-3`,
- `Psi <=5e-3`,
- `W=Phi+Psi <=5e-3`.

### G3 — static full-J regression

Retain the original static full-J operator regression gate:

`max_error <=1e-10`.

### G4 — metric constraint closure

Across all 27 nonlinear members, maximum Hamiltonian, momentum, and shear projection residuals must each be

`<=1e-8`.

### G5 — finite evolving output

All `27/27` nonlinear members must remain finite over the full interval and all nine checkpoints.

### G6 — evolving slip distinction

Because the nonlinear completion adds no retained shear source, the nonlinear metric correction must preserve the corrected-CLASS slip algebraically:

`slip_to_CLASS_slip_relL2 <=1e-12`,

and the retained CLASS slip must not be silently overwritten by zero.

### G7 — no ill-conditioned Theta reconstruction in the R2 RHS

The R2 implementation must evolve `Theta_A` directly through the frozen Euler equation. The expression `chi/Q-alpha` may appear only in an optional diagnostic and must not be used to construct the R2 RHS or metric momentum source.

## Classification

All frozen gates pass:

`FULLJ_EVOLVING_WEYL_BRIDGE_R2_PASS`.

One or more frozen gates fail with a numerically complete run:

`FULLJ_EVOLVING_WEYL_BRIDGE_R2_FAIL`.

The system cannot be completed without an extra physical closure beyond D2C5/corrected CLASS:

`FULLJ_EVOLVING_WEYL_BRIDGE_R2_INCOMPLETE_METRIC_CLOSURE`.

A PASS licenses a separately preregistered evolving-Weyl covariance/power diagnostic on the locked nonlinear trajectory grid. It still does not license ACT.

Always:

- `HISTORICAL_R0_FAIL_PRESERVED=True`;
- `HISTORICAL_R1_FAIL_PRESERVED=True`;
- `ACT_LIKELIHOOD_LICENSED=False`;
- `OBSERVATIONAL_CLAIM_LICENSED=False`;
- `NO_STATIC_W_EQUALS_2PHI_PROMOTION=True`.
