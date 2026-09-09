# NL1C6D1 predata — model-consistent dynamical AeST formulation audit

Status: **PREREGISTERED BEFORE NL1C6D1 DYNAMICAL FIELD RESULTS**.

Frozen test label:

```text
NL1C6D1_PREDATA_DYNAMICAL_FORMULATION_AUDIT
```

## Motivation fixed before dynamical results

NL1C6R3 is locked as

```text
NL1C6R3_FULL_J_BARYONIC_RECLOSURE_FAIL
```

in `docs/nl1c6r3_fixed_source_constitutive_homotopy_result.md`.

The decisive blocker is the first native snapshot `z=6.000000000000045`, interpolation `sharp`, `beta0=1.0`: the screened constitutive route crosses the neighbourhood of theta=1 but the exact endpoint correction fails with `theta1_gmres_failed_300` and relative residual `0.05794504649617346`, while the mass route exhausts 1200 accepted arclength points at `theta_max=0.004934468552216773`. Both routes therefore fail to provide a residual-valid physical endpoint under the frozen R3 rules.

The R3 predata stopping rule explicitly directs the next scientific step away from an open-ended sequence of static solver-tolerance repairs and toward physical time evolution / branch selection.

NL1C6D1 is therefore not an R4 solver repair and not yet a nonlinear cosmological science run. It asks the prerequisite question:

**Can a reduced time-dependent AeST system relevant to the present longitudinal weak-field problem be derived directly from the published AeST theory, validated against its known propagating-mode dynamics, and shown to reduce to the frozen full-J quasistatic equations without adding ad hoc evolution terms?**

Only a PASS permits a subsequent nonlinear dynamical branch-selection run.

## Authoritative theory sources

The dynamical formulation must be traceable to the published AeST theory and its constraint structure, using as primary theory references:

1. C. Skordis and T. Zlosnik, *A new relativistic theory for Modified Newtonian Dynamics*, Phys. Rev. Lett. 127, 161302 (2021), arXiv:2007.00082.
2. C. Skordis and T. Zlosnik, *Aether scalar tensor theory: Linear stability on Minkowski space*, Phys. Rev. D 106, 104041 (2022), arXiv:2109.13287.
3. M. Bataki, C. Skordis and T. Zlosnik, *Aether scalar tensor theory: Hamiltonian Formalism*, arXiv:2307.15126.
4. P. Verwayen, C. Skordis and C. Boehm, *Aether Scalar Tensor (AeST) theory: quasistatic spherical solutions and their phenomenology*, MNRAS 531, 272–289 (2024), doi:10.1093/mnras/stae1225.

A different convention is allowed only when an explicit algebraic mapping to these references and to the existing repository variables is supplied.

## Prohibited repairs

The following are forbidden in NL1C6D1:

- adding a relaxation law such as `d chi/dt = -Gamma R[chi]` by hand;
- adding an arbitrary damped-wave term solely to force convergence toward a static root;
- interpreting Newton iterations, pseudo-time, arclength, theta, or source amplitude lambda as physical time;
- tuning damping/friction coefficients to select a desired R3 endpoint branch;
- changing the frozen full-J interpolation functions in order to simplify evolution;
- changing `beta0`, `K_B`, `K2`, `Q0`, `a0`, or the physical endpoint equations to obtain stability;
- treating the non-smooth `sharp` interpolation as differentiable at its kink without an explicit weak/piecewise formulation;
- using NL1C6D1 to claim an observational detection or to evaluate causal-memory eta.

Any physical damping, Hubble friction, constraint term, or kinetic coefficient must follow from the AeST equations in the chosen background/gauge, not from numerical convenience.

## Frozen parameter mapping

The repository convention is retained:

```text
K_B = 0.0665
K2  = 9500
Q0  = 1e-4 Mpc^-1
beta0 in {1.0, 0.5, 0.1}
lambda_s = 1/beta0
```

The existing static mass parameter remains

```text
mu^2 = 2 K2 Q0^2 / (2-K_B)
```

and must not be silently identified with a dynamical normal-mode mass unless the derivation proves the relation.

## D1-A: derivation and variable audit

Before numerical evolution, the implementation must document:

- background spacetime and time coordinate;
- gauge choice;
- scalar/longitudinal perturbation variables retained from the metric, unit-timelike vector and scalar field;
- nondynamical variables and constraints;
- dynamical variables and their canonical/evolution equations;
- mapping from the derived variables to the repository weak-field potentials `Phi`, `tildePhi`, and `chi`;
- the nonlinear spatial constitutive term whose quasistatic limit produces `j(x)` with `x = |grad chi|/a0` in the repository convention;
- every approximation used to reduce the covariant theory to the numerical system.

No evolution code may be classified PASS if an evolved term lacks a traceable origin in the AeST action/equations.

## D1-B: linear propagating-mode regression

The reduced dynamical implementation must reproduce the known healthy scalar propagating mode around Minkowski space in the tracking regime.

Using `lambda_s = 1/beta0`, the published scalar-mode target is

```text
omega^2 = c_s^2 k^2 + M^2
```

with

```text
c_s^2 = (2-K_B)/(K2 K_B) * (1 + 0.5 K_B lambda_s)
M^2   = (2-K_B)(1+lambda_s) Q0^2 / K_B
```

in the corresponding reference convention.

For each `beta0 in {1.0,0.5,0.1}`, at least six Fourier modes spanning the repository's low-k range must be evolved at sufficiently small amplitude that nonlinear terms are negligible. The fitted frequency must satisfy

```text
max |omega_num^2 - omega_ref^2| / max(|omega_ref^2|, floor) <= 5e-3
```

for a preregistered positive numerical floor small enough not to hide any tested nonzero mode. The floor and fit window must be written into the implementation before the first frequency result is inspected.

The regression must additionally show second-order-or-better convergence in the chosen time step or integrator tolerance for at least two representative Fourier modes.

## D1-C: constraint regression

Initial data constructed from an analytic linear normal mode must satisfy all retained scalar-sector constraints to a normalized residual of

```text
<= 1e-10
```

at initialization.

During the linear regression evolution, the maximum normalized constraint residual must remain

```text
<= 1e-7
```

without constraint projection after every time step unless such projection is derived as an exact solution of the nondynamical constraints rather than an empirical correction.

## D1-D: quasistatic full-J regression

The exact zero-time-derivative limit of the derived reduced system must reproduce the existing frozen weak-field equations used in NL1C6R3:

```text
Phi = tildePhi + chi
laplacian(tildePhi) + mu^2 Phi = 4 pi G_N rho_b / (1+beta0)
laplacian(tildePhi) = div[ j(x) grad chi ]
```

with the same physical-coordinate convention and

```text
x = c^2 |grad_phys chi| / (a0 Mpc_in_metres)
```

as already implemented in the repository.

This is a symbolic/algebraic gate plus a numerical manufactured-state gate. On deterministic finite Fourier states at `Nx=256`, the normalized difference between the D1 zero-time-derivative residual and the frozen NL1C6R3 residual must be

```text
<= 1e-12
```

for `simple` and `exponential` interpolation away from floating-point underflow.

For `sharp`, the comparison must be piecewise exact away from the kink. Grid points whose `x` lies within a preregistered floating-point neighbourhood of the kink are excluded only from the derivative/Jacobian comparison, never from the physical residual itself.

## D1-E: large-gradient regression

In the large-gradient tracking limit `j -> 1/beta0`, the D1 quasistatic reduction must reproduce the already validated analytic baryonic Helmholtz relation

```text
laplacian(Phi) + (1+beta0) mu^2 Phi = 4 pi G_N rho_b
chi = beta0/(1+beta0) Phi
```

with maximum numerical relative error

```text
<= 1e-10
```

on the same deterministic regression states used by NL1C6R3.

## D1-F: no artificial branch selection

D1 may report the dynamical variables and the sign/energy of the linear modes, but it must not yet use a nonlinear source history to select among R3 static branches.

The first nonlinear branch-selection run will be a separate `NL1C6D2` preregistration only after D1 passes. D2 must specify, before output is seen:

- the cosmological background and source history;
- an early-time initialization prescription from the dynamical theory rather than from a favorable R3 static branch;
- time integration and constraint handling;
- the physical observable used to decide whether the trajectory approaches a quasistatic full-J endpoint;
- treatment of the `sharp` interpolation kink;
- convergence and resolution controls;
- a rule for classifying persistent dynamics, branch switching, or failure to settle without redefining them as solver failure.

## Frozen D1 classifications

All derivation, linear-mode, constraint, quasistatic and high-gradient gates pass:

```text
NL1C6D1_DYNAMICAL_FORMULATION_AUDIT_PASS
```

Any derivation term is untraceable, a spurious mode is required to obtain the desired static reduction, the published linear dispersion is not reproduced within the frozen tolerance, constraints fail, or the zero-time-derivative limit differs from NL1C6R3:

```text
NL1C6D1_DYNAMICAL_FORMULATION_AUDIT_FAIL
```

No intermediate result may be promoted to a physical branch-selection claim.

## Continuation rule

Only

```text
NL1C6D1_DYNAMICAL_FORMULATION_AUDIT_PASS
```

permits preregistration and execution of `NL1C6D2` nonlinear dynamical branch selection.

NL1C7 causal-memory response remains blocked until a later dynamical phase establishes a self-consistent full-J native-time trajectory under its own frozen gates.
