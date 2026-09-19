# GE06 analytic AeST directional source generator — implementation lock

## Status

Implementation locked before first GE06 execution.

GE06 is the final action-source completeness step before a second-order state solve, apart from standard minimally coupled matter nonlinearities.

## Theory provenance

Dependencies:

- `NL1B2_DIRECTIONAL_SECOND_ORDER_ETA_TANGENT_PASS`;
- `NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_PASS`;
- `GE04_DY2_SPECTRAL_CONVERGENCE_PASS`;
- `GE05_MEMORY_DIRECTIONAL_SOURCE_GENERATOR_PASS`.

The nonanalytic Y sector is not included in GE06. Its `Y2` and `DY2` blocks remain separately certified by NL1A/NL1B2/GE04.

## Preregistration

Commit:

`de71bd33fa44b9ec7f9242621d3156bb0a30713a`.

File:

`ge06/predata_analytic_aest_directional_source_generator.json`.

Frozen blob:

`007cd6c726735b3979191f7a7cd1c6b3cac9c854`.

## Implementation

Commit:

`36473d6cb9428844e6b922787bc5204662bea7a9`.

File:

`ge06/analytic_aest_directional_source_generator.py`.

Frozen blob:

`a7afe0035054a9dca55d74a6497c081422114b4c`.

Reference NL1C6 spherical self-gravity implementation blob:

`e3eeb820fa1826fb7ac29f3fce2fe0bdde8d564f`.

## Frozen analytic action

Plane-symmetric longitudinal 3+1 geometry:

`theta0=N dt`;

`theta1=L(dx+b dt)`;

`theta2=R dy`;

`theta3=R dz`.

Extrinsic rates:

`kL=(Lt-b Lx-L bx)/(N L)`;

`kR=(Rt-b Rx)/(N R)`.

GR analytic sector:

`N L R^2[-4 kL kR-2 kR^2] + 2 N Rx^2/L + 4 Nx R Rx/L`.

AeST analytic sector:

`N L R^2[KB E^2+2 C E X-C X^2+2 K(Q)]`

with

`C=2-KB`

and the exact invariant dictionary inherited from NL1C6.

Exp branch:

`K(Q)=2 K2 Z0^2[exp(((Q-Q0)/Z0)^2)-1]`.

The `J(Y)` term is explicitly excluded from GE06.

## Frozen directional expansion

Homogeneous background:

- `N=1`;
- `b=u=0`;
- `L=R=a(t)`;
- `Lt=Rt=adot(t)`;
- `pt=Q(t)`;
- all spatial gradients zero.

Audit background:

`a(t)=1+0.08 sin(t)+0.02 cos(2t)`;

`Q(t)=0.2+0.03 cos(t)`.

Representative generator-conditioning constants:

- `KB=0.1`;
- `C=1.9`;
- `K2=0.4`;
- `Q0=0.2`;
- `Z0=0.7`.

These are audit values only and introduce no new theory branch.

## Generated source blocks

Required:

- metric lapse;
- metric longitudinal scale;
- metric transverse scale;
- metric shift;
- aether rapidity;
- scalar field.

For every exact local action partial, the implementation differentiates with respect to one common perturbation amplitude epsilon.

First derivative at epsilon=0:

`L[V]`.

Second derivative at epsilon=0:

`Q[V,V]`.

Euler-Lagrange time and space derivative assembly is performed after directional differentiation.

## Independent full-residual finite-difference audit

Periodic deterministic grid:

- Nt=48;
- Nx=64.

Frozen amplitude steps:

- primary `h=1e-3`;
- control `h=3e-4`.

For the full exact Euler-Lagrange source system:

`L_fd=[S(+h)-S(-h)]/(2h)`;

`Q_fd=[S(+h)-2S(0)+S(-h)]/h^2`.

## Frozen gates

Require:

- exact Exp `K_QQ` identity;
- all six source blocks generated;
- global analytic L versus primary finite difference relative L2 <= `1e-5`;
- global analytic Q versus primary finite difference relative L2 <= `1e-5`;
- primary versus control finite-difference L relative L2 <= `1e-5`;
- primary versus control finite-difference Q relative L2 <= `1e-5`;
- all outputs finite.

## Classification

Full generator closure:

`GE06_ANALYTIC_AEST_DIRECTIONAL_SOURCE_GENERATOR_PASS`.

Otherwise:

`GE06_ANALYTIC_AEST_DIRECTIONAL_SOURCE_GENERATOR_FAIL`.

## Claim boundary

A PASS certifies the memory-off analytic Einstein+AeST directional source generator in the controlled scalar-longitudinal plane-symmetric sector.

It does not:

- include the separately certified nonanalytic Y block;
- include minimally coupled matter nonlinearities;
- solve `Z20` or `Z21`;
- introduce finite eta;
- certify collapse, halo, lensing or observational predictions.

## Anti-tuning

After this lock do not change:

- action terms;
- representative audit parameters;
- background functions;
- deterministic perturbation direction;
- grid sizes;
- finite-difference steps;
- source list;
- numerical gates.
