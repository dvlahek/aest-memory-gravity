# GE07 pressureless-matter directional source generator — implementation lock

## Status

Implementation locked before first GE07 execution.

GE07 is the final source-completeness block before a baseline H3 second-order state solve.

## Theory provenance

Dependencies:

- `NL1C7B1_PRESSURELESS_MATTER_VARIATIONAL_CLOSURE_PASS`;
- `GE06_ANALYTIC_AEST_DIRECTIONAL_SOURCE_GENERATOR_PASS`;
- `NL1B2_DIRECTIONAL_SECOND_ORDER_ETA_TANGENT_PASS`.

The matter action is not new. It is the already certified minimally coupled pressureless dust action

`S_d=-1/2 int sqrt(-g) rho_phys (g^munu d_mu T d_nu T + 1)`

with

`varrho=8*pi*G*rho_phys`.

In the longitudinal 3+1 geometry,

`L_d=N L R^2 varrho [((T_t-bT_x)/N)^2-(T_x/L)^2-1]`.

No free matter-coupling coefficient exists.

## Preregistration

Commit:

`03bb7254ee13f620d20b1183fcc0cbf117cbb4e4`.

File:

`ge07/predata_pressureless_matter_directional_source_generator.json`.

Frozen blob:

`a6135f06181661c715f1c9b3473ce723eb004d69`.

## Implementation

Commit:

`5a5d6c8bafbae27c0e8a4f6ecce6ed41c3efbb56`.

File:

`ge07/pressureless_matter_directional_source_generator.py`.

Frozen blob:

`cde8da77a80799cef00fc7c09c3633310fc9e3d4`.

## Frozen background

Homogeneous comoving dust:

- `N=1`;
- `b=0`;
- `L=R=a(t)`;
- `T_t=1`;
- `T_x=0`;
- `varrho=rho0/a^3`;
- `rho0=0.25`.

Audit scale factor:

`a(t)=1+0.08 sin(t)+0.02 cos(2t)`.

## Generated source blocks

Required Euler-Lagrange source blocks:

- metric lapse;
- metric longitudinal scale;
- metric transverse scale;
- metric shift;
- dust potential T;
- dust density multiplier varrho.

For one common perturbation direction, generate

`L_m[V]`

and

`Q_m[V,V]`

as the first and second epsilon derivatives at epsilon=0.

## Exact frozen identities

Require:

- background dust normalization constraint exactly zero;
- background comoving dust current conservation exactly satisfied;
- no direct dependence on AeST/memory variables;
- zero contribution to the field-sector principal Hessian.

## Independent finite-difference audit

Periodic deterministic grid:

- Nt=48;
- Nx=64.

Frozen amplitude steps:

- primary `1e-3`;
- control `3e-4`.

For the complete dust Euler-Lagrange source vector:

`L_fd=[S(+h)-S(-h)]/(2h)`;

`Q_fd=[S(+h)-2S(0)+S(-h)]/h^2`.

## Frozen gates

Require:

- all six source blocks generated;
- analytic L vs primary FD global relative L2 <= `1e-5`;
- analytic Q vs primary FD global relative L2 <= `1e-5`;
- primary vs control FD L relative L2 <= `1e-5`;
- primary vs control FD Q relative L2 <= `1e-5`;
- all outputs finite;
- all exact identities above pass.

## Classification

Full closure:

`GE07_PRESSURELESS_MATTER_DIRECTIONAL_SOURCE_GENERATOR_PASS`.

Otherwise:

`GE07_PRESSURELESS_MATTER_DIRECTIONAL_SOURCE_GENERATOR_FAIL`.

## Claim boundary

A PASS certifies only the pressureless-matter L/Q source generator needed by H3/H4.

It does not:

- solve `Z20`, `q20` or `Z21`;
- add radiation, baryon-pressure or neutrino nonlinearities;
- introduce finite eta;
- certify nonlinear collapse or observables.

## Anti-tuning

After this lock do not change:

- dust action;
- background;
- perturbation direction;
- source list;
- grid;
- finite-difference steps;
- thresholds.
