# NL1C6D1A predata — vector-complete longitudinal weak-field reduction audit

Status: **PREREGISTERED BEFORE NL1C6D1A NUMERICAL/ALGEBRAIC RESULTS**.

Frozen label:

```text
NL1C6D1A_PREDATA_LONGITUDINAL_WEAKFIELD_REDUCTION_AUDIT
```

## Context

NL1C6R3 is locked as a numerical/static-snapshot FAIL. NL1C6D1B subsequently passed the published AeST scalar-mode frequency and convergence regression, and NL1C6D1CDE passed the linear constraint, exact quasistatic full-J identity, and high-gradient regressions. Full D1 remains unclassified because the time-dependent nonlinear longitudinal weak-field reduction has not yet been explicitly written and audited.

This phase closes that derivation gap. It is an action/equation audit, not a nonlinear cosmological branch-selection run.

## Vector-completeness check fixed before D1A output

Mistele, Phys. Rev. D 110, 024062 (2024), showed that the general AeST quasistatic weak-field system contains a curl sector controlled by

```text
m_cross = sqrt((2-K_B)/(2 K_B)) Q0.
```

For the frozen repository parameters this is

```text
K_B = 0.0665
Q0  = 1e-4 Mpc^-1
m_cross = 3.8128196895424266e-4 Mpc^-1
m_cross^-1 = 2622.730895832132 Mpc.
```

However, the repository experiment is strictly one-dimensional and longitudinal: the spatial vector perturbation has the form `A_i = partial_i alpha` with dependence on one periodic coordinate only. Therefore `curl A = 0` and `curl U = 0` identically, where `U_i = partial_i varphi + Q0 A_i = partial_i chi`. The Mistele double-curl term is exactly absent in this ansatz for every finite `m_cross`. This fact must be demonstrated in the implementation and recorded; it may not be used to reinterpret the historical R3 FAIL.

## Controlled weak-field longitudinal action

Let

```text
A = 2-K_B
E = dot(alpha) + Psi
U = dot(chi) - Q0 E
Y = |grad chi|^2
j(Y) = dJ/dY.
```

The D1A reduced gravitational action is the weak-field scalar/longitudinal action obtained from the covariant AeST action while retaining the nonlinear spatial constitutive function `J(Y)`:

```text
L = -6 dot(Phi)^2
    + 2 |grad Phi|^2
    - 4 grad Phi . grad Psi
    + 2 K2 U^2
    + K_B |grad E|^2
    + 2 A grad E . grad chi
    - A [ |grad chi|^2 + J(Y) ]
    - 16 pi G_tilde rho_b Psi
    - 48 pi G_tilde P_b Phi.
```

This is a weak-field reduction, not a claim of a fully nonlinear spacetime evolution system. The constitutive nonlinearity in spatial gradients is retained because it is the nonlinearity needed for the frozen full-J quasistatic equations.

The action must satisfy two source-traceability checks:

1. In the tracking/high-gradient limit `J_Y -> lambda_s = 1/beta0`, the gradient term becomes `-A(1+lambda_s)|grad chi|^2`, reproducing the published quadratic Minkowski scalar action.
2. Setting all time derivatives to zero must reproduce the frozen NL1C6R3 full-J equations exactly.

No extra damping, friction, relaxation, or branch-selection term is permitted.

## Derived canonical quantities and equations to audit

With the definitions above, the canonical momenta are frozen as

```text
P_Phi  = -12 dot(Phi)
P_chi  =  4 K2 U
P_alpha = -4 K2 Q0 U - 2 K_B lap(E) - 2 A lap(chi).
```

The nondynamical `Psi` equation is the Hamiltonian/scalar constraint

```text
4 lap(Phi) + P_alpha - 16 pi G_tilde rho_b = 0.
```

For vanishing baryonic pressure the remaining longitudinal field equations are

```text
3 ddot(Phi) - lap(Phi) + lap(Psi) = 0,

2 K2 dot(U)
+ A [ lap(E) - lap(chi) - div(j grad chi) ] = 0,

dot(P_alpha) = 0
```

for a time-independent external source. The last equation is the alpha equation in the reduced fixed-source sector. It must not be applied to an arbitrarily time-varying density without the matter momentum/continuity sector and the pre-gauge-fixing momentum constraint. Treatment of evolving matter is explicitly deferred to D2 preregistration.

## Static reduction gate

For a static dust source,

```text
dot(*) = 0
P_b = 0
Psi = Phi
E = Phi
U = -Q0 Phi.
```

The chi equation must reduce to

```text
lap(Phi-chi) = div(j grad chi).
```

Writing `tildePhi=Phi-chi`, the Psi constraint must reduce to

```text
lap(tildePhi) + mu^2 Phi = 8 pi G_tilde rho_b/(2-K_B),
mu^2 = 2 K2 Q0^2/(2-K_B).
```

Using

```text
G_N = 2(1+beta0) G_tilde/(2-K_B),
```

this must be exactly identical to the frozen repository equation

```text
lap(tildePhi) + mu^2 Phi = 4 pi G_N rho_b/(1+beta0).
```

The manufactured-state normalized discrepancy against the frozen operator must be `<=1e-12`.

## Tracking linearization gate

In vacuum and in the tracking limit `j -> lambda_s=1/beta0`, the quadratic action/canonical equations must recover the published scalar propagating mode

```text
omega^2 = c_s^2 k^2 + M^2
c_s^2 = (2-K_B)/(K2 K_B) * (1 + 0.5 K_B lambda_s)
M^2 = (2-K_B)(1+lambda_s) Q0^2/K_B.
```

The D1A implementation must independently reconstruct the coefficient relation to relative error `<=1e-12` for all three beta0 values and all six frozen low-k modes. This is an algebraic consistency gate complementary to the already-completed D1B time-integration regression.

The tracking regression must not be described as the linearization of the deep-MOND `j(x) ~ x/(1+beta0)` branch at exactly zero gradient. It is the published tracking/high-gradient quadratic limit.

## One-dimensional curl gate

For deterministic periodic longitudinal fields at `Nx=256`, a three-component embedding

```text
U = (d_x chi, 0, 0),  chi=chi(x)
```

must give exactly zero discrete spectral curl and double curl to numerical precision. Frozen gate:

```text
max normalized curl/double-curl residual <= 1e-14.
```

This establishes that the additional finite-m_cross quasistatic term identified by Mistele is inactive in the geometry actually used by the repository. No claim is made for general 2D/3D sources.

## D1A classifications

All source-traceability, canonical/constraint, one-dimensional vector-completeness, static-reduction and tracking-linearization gates pass:

```text
NL1C6D1A_LONGITUDINAL_WEAKFIELD_REDUCTION_AUDIT_PASS
```

Any mismatch, an untraceable term, a required ad hoc evolution term, failure of the static reduction, or a nonzero omitted curl contribution in the repository geometry:

```text
NL1C6D1A_LONGITUDINAL_WEAKFIELD_REDUCTION_AUDIT_FAIL
```

## Consequence for full D1 and D2

A D1A PASS together with the already frozen D1B and D1CDE PASS results is sufficient to classify the **gravitational longitudinal formulation audit** D1 as passed for the repository's one-dimensional weak-field geometry.

It is not yet a D2 branch-selection result. Before any evolving baryonic source is used, D2 must separately preregister a constraint-consistent matter sector, including density evolution and the required momentum/velocity information. An externally prescribed `rho_b(t,x)` may not be inserted into the fixed-source alpha equation while claiming physical constraint preservation.

NL1C7 causal-memory physics remains blocked until D2 establishes a self-consistent nonlinear full-J trajectory.