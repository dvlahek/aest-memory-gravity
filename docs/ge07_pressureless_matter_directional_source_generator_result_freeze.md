# GE07 pressureless-matter directional source generator — result freeze

## Status

Frozen first clean locked GE07 execution.

Terminal classification:

`GE07_PRESSURELESS_MATTER_DIRECTIONAL_SOURCE_GENERATOR_PASS`.

GitHub Actions run:

`35490609115`.

Execution HEAD:

`758095d7e946326411f20a92bd7a1260d941cd83`.

Artifact:

- ID: `10598757346`;
- name: `results_bundle_ge07_pressureless_matter_directional_source_generator`;
- ZIP SHA-256:
  `a1a3b6463af56895b230af8ecd4bbc0abcb322bb1f8662a60897c61e4fdc47d1`.

## Frozen output hashes

Result JSON:

- bytes: `4324`;
- SHA-256:
  `6823592d338c1d93bab568346909f8c243c472cbc67f286dbb6cfecdaa4e45b0`.

Result log:

- bytes: `4324`;
- SHA-256:
  `6823592d338c1d93bab568346909f8c243c472cbc67f286dbb6cfecdaa4e45b0`.

Preregistration JSON:

- bytes: `3185`;
- SHA-256:
  `e19018ac1f1c3e23a916baf1c662574a73bf8a47e1d14944a4d1673748cee289`.

Implementation lock:

- bytes: `3215`;
- SHA-256:
  `6a01c52d0c31dd3c9d0ee1192c4e01e6f477dd5807a515c5586408060611c045`.

## Runner Repair01 provenance

The first two workflow attempts generated a GE07 PASS science payload but failed at the runner level because `tee` opened the log path before `results/` existed.

The locked runner-only Repair01 added only

`mkdir -p results`

before the unchanged generator pipeline.

No science code or threshold changed.

The clean run above has workflow conclusion `success`.

## Gate result

Every exact and numerical GE07 gate passes:

- background dust normalization constraint is exactly zero;
- homogeneous comoving dust current conservation is exact;
- no direct AeST or memory coupling appears in the dust action;
- the dust field-sector principal Hessian contribution is exactly zero;
- all six required source blocks are generated;
- analytic `L_m[V]` matches finite differences;
- analytic `Q_m[V,V]` matches finite differences;
- primary/control finite-difference stability passes;
- all outputs are finite.

Global relative-L2 controls:

- analytic L versus primary finite difference:
  `8.17152555696435e-9`;
- analytic Q versus primary finite difference:
  `8.973815463342767e-9`;
- primary versus control finite-difference L:
  `7.436052162437138e-9`;
- primary versus control finite-difference Q:
  `9.466761298318719e-8`.

All are far below the frozen `1e-5` gates.

## Source-completeness consequence

The pressureless-matter nonlinear source gap is now closed for the frozen scalar-longitudinal dust sector.

The source ingredients required for the baseline H3 hierarchy are now available as separately certified blocks:

- analytic Einstein+AeST `L/Q`: GE06 PASS;
- nonanalytic Y-sector `Y2`: NL1A/NL1B2;
- high-resolution Y representation: GE04 PASS;
- pressureless matter `L_m/Q_m`: GE07 PASS.

The memory ingredients required later by H4 are separately available:

- `M1/M2`: GE05 PASS;
- `DY2`: NL1B2/GE04.

Therefore the next active nonlinear step is no longer a source-generator audit.

It is a separately preregistered baseline second-order state solve for

`L_total Z20 = -Q_total(Z10,Z10)-2Y2[Z10]`

with the pressureless-matter contribution included in `L_total` and `Q_total`.

## What remains before Z21

The H3 solve must produce:

- the physical baseline second-order state `Z20`;
- the second-order normalized bath response `q20` from the eta-independent bath equation;
- an independent scalar constraint residual.

Only then is the H4 equation for `Z21` numerically complete.

## Claim boundary

GE07 does not:

- solve `Z20`, `q20` or `Z21`;
- include additional nonlinear radiation, baryon-pressure or neutrino species;
- introduce finite eta;
- certify collapse, halo, lensing or observational predictions.
