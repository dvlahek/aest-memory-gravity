# GE06 analytic AeST directional source generator — result freeze

## Status

Frozen first locked GE06 execution.

Terminal classification:

`GE06_ANALYTIC_AEST_DIRECTIONAL_SOURCE_GENERATOR_PASS`.

GitHub Actions run:

`35473430942`.

Execution HEAD:

`e6e91089a045e6231e342bb5402b8b03d17f6074`.

Artifact:

- ID: `10593811926`;
- name: `results_bundle_ge06_analytic_aest_directional_source_generator`;
- ZIP SHA-256:
  `e0e308413ecf8daffa886083049c9ed5e9f58c10a13ecca9e7359064cb426757`.

## Frozen output hashes

Result JSON:

- bytes: `4113`;
- SHA-256:
  `b2ee017f88786598f4bc85d06695bfa5ca2232b11717440b890ae6908878cadb`.

Result log:

- bytes: `4113`;
- SHA-256:
  `b2ee017f88786598f4bc85d06695bfa5ca2232b11717440b890ae6908878cadb`.

Preregistration JSON:

- bytes: `3509`;
- SHA-256:
  `ffb12a90a0b2a34c3561aa9e640b0b2e3f08d64b6bffbe15acdb6228e0713ae3`.

Implementation lock:

- bytes: `4052`;
- SHA-256:
  `4976fb4d9c79ba4edb3671b55b80723dca8282f41da810f28880d7af7a4086f0`.

## Gate result

Every preregistered GE06 gate passes:

- exact Exp `K_QQ` identity;
- all required analytic memory-off source blocks generated;
- analytic `L[V]` agrees with full-residual finite differences;
- analytic `Q[V,V]` agrees with full-residual finite differences;
- primary/control finite-difference stability passes;
- all outputs are finite.

Global relative-L2 controls:

- analytic L versus primary finite difference:
  `2.7692996404332156e-7`;
- analytic Q versus primary finite difference:
  `2.0797452273717362e-7`;
- primary versus control finite-difference L:
  `2.520062827988982e-7`;
- primary versus control finite-difference Q:
  `1.8991339302906518e-7`.

All are far below the frozen `1e-5` limits.

## Generated source blocks

The memory-off analytic Einstein+AeST longitudinal scalar sector now has explicit directional generators for:

- metric lapse;
- metric longitudinal scale;
- metric transverse scale;
- metric shift;
- aether rapidity;
- scalar field.

The separately certified nonanalytic Y-sector is intentionally excluded and remains supplied by NL1A/NL1B2/GE04.

## Source-level implication

Together:

- GE04 supplies a converged high-resolution `DY2[Z10;Z11]` representation;
- GE05 supplies action-derived memory `M1` and `M2`;
- GE06 supplies analytic memory-off `L` and `Q` source generators for the Einstein+AeST scalar-longitudinal sector.

Therefore the remaining source-completeness gap before a true H3/H4 state solve is no longer the gravitational/AeST memory structure.

The explicitly remaining physics block is the minimally coupled matter nonlinear sector, plus the actual solution of the baseline second-order state `Z20` and normalized bath `q20`.

## Claim boundary

GE06 does not:

- include minimally coupled matter nonlinearities;
- solve `Z20` or `q20`;
- solve `Z21`;
- introduce finite eta;
- certify collapse, halo, lensing or observational predictions.

## Licensed continuation

The next source-completeness step is a separately preregistered **minimally coupled matter directional source generator**.

Only after that block is closed should the project preregister a baseline H3 state solve for

`L Z20 = -Q(Z10,Z10)-2Y2[Z10]`

with the full matter contribution included and an independent scalar constraint residual.

The H4 / `Z21` solve must wait until `Z20` and `q20` are available.
