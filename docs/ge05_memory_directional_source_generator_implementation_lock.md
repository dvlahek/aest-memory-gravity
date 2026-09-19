# GE05 memory directional source generator — implementation lock

## Status

Implementation locked before first GE05 execution.

## Purpose

Generate the first and second perturbative directional coefficients of the frozen NL0B longitudinal 3+1 memory source system around an FLRW point.

These are the explicit `M1` and `M2` source blocks required by the NL1B2 H4 hierarchy.

## Theory provenance

Dependencies:

- `NL0B_COVARIANT_MEMORY_COMPLETION_PASS`;
- `NL1B2_DIRECTIONAL_SECOND_ORDER_ETA_TANGENT_PASS`;
- `NL1C3A_COMPONENT_VARIATIONAL_GENERATOR_PASS`;
- `NL1C3B_LONGITUDINAL_3PLUS1_MEMORY_BRIDGE_PASS`.

Frozen NL1C3B implementation blob:

`f64e42186f489b37800f33d99f72668268211d23`.

Per-node normalized memory action:

`N L R^2/4 * [(Aq)^2-(omega q-sqrt(w) X)^2]`.

## Preregistration

Commit:

`4b56637730e0c91fe6ce44e8568f2687f19bdfab`.

File:

`ge05/predata_memory_directional_source_generator.json`.

Frozen blob:

`02debb3802e9cf7687e34de773edce535044a664`.

## Implementation

Commit:

`393657ff76e68bb751fd7859d762d2c5d0cc2479`.

File:

`ge05/memory_directional_source_generator.py`.

Frozen blob:

`40837d77f89028da30c28899e2d0530a4401844e`.

## Frozen expansion point

`N=1`;

`L=R=a`;

`b=0`;

`r=0`;

`q=qt=qx=px=0`;

`pt=Q`.

Deterministic audit values:

- `a=1`;
- `Q=0.6`;
- `omega=1.7`;
- `w=0.6`.

## Generated source blocks

Required and locked:

- scalar field;
- normalized bath;
- aether rapidity;
- metric lapse;
- metric shift;
- metric longitudinal scale;
- metric transverse scale.

For every local action partial, the implementation differentiates the exact symbolic expression with respect to a common perturbation amplitude epsilon at epsilon=0.

The first derivative generates `M1`.

The second derivative generates `M2[V,V]`.

Euler-Lagrange time/space derivative assembly is performed after the directional coefficient is generated.

## Independent finite-difference audit

Periodic deterministic audit grid:

- Nt=48;
- Nx=64.

Frozen amplitude steps:

- primary `h=1e-3`;
- control `h=3e-4`.

Independent full-source coefficients:

`M1_fd=[S(+h)-S(-h)]/(2h)`;

`M2_fd=[S(+h)-2S(0)+S(-h)]/h^2`.

## Frozen gates

Require:

- all seven source blocks generated;
- symbolic direct metric `M1` exactly zero;
- global analytic M1 versus primary FD relative L2 <= `1e-5`;
- global analytic M2 versus primary FD relative L2 <= `1e-5`;
- primary versus control FD M1 relative L2 <= `1e-5`;
- primary versus control FD M2 relative L2 <= `1e-5`;
- direct metric M2 finite and nonzero;
- all outputs finite.

## Classification

Full source-generator closure:

`GE05_MEMORY_DIRECTIONAL_SOURCE_GENERATOR_PASS`.

Otherwise:

`GE05_MEMORY_DIRECTIONAL_SOURCE_GENERATOR_FAIL`.

## Claim boundary

A PASS closes the explicit NL0B memory-source half of the NL1B2 H4 hierarchy.

It does not:

- generate the memory-off analytic `Q` block;
- solve `Z20` or `Z21`;
- introduce finite physical eta;
- certify nonlinear collapse or an observational result.

## Anti-tuning

After this lock do not change:

- action;
- expansion point;
- deterministic direction;
- grid sizes;
- finite-difference steps;
- source list;
- numerical thresholds.
