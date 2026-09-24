# GE19 H3F — corrected-Y Z20 parent reclosure preregistration lock

## Status

The next corrected variational parent science test has been
preregistered and passed its static prelock. This file
contains **no new Z20 numerical result** and does not
replace historical Repair22.

Preregistration:

`ge19/h3f_predata_action_completed_y_z20_parent_reclosure.json`.

Preregistration commit:
`a7456aa9e87691c34b6b92c95d9198af699e9750`.

Preregistration blob:
`6ae1dd8c27ee1f94d85831cd5ae7b5ec21e3794e`.

Dedicated prelock:

- workflow:
  `.github/workflows/ge19-h3f-parent-prelock.yml`;
- workflow commit:
  `ad612c91ac5da165c36b0d0a6d0ecb6d226d1056`;
- workflow blob:
  `f074a60afeb0e135f1e16060472c57cdcdcf59ea`;
- run: `35995943887`;
- job: `107620762977`;
- result: `success`;
- marker: `GE19_H3F_PARENT_PREDATA_PRELOCK_PASS`.

## Precise science boundary

H3F retains the original reduced H1/GE06/GE07/Lambda
physics, C/beta/m cohorts, Nt128/Nt64 time controls,
Nx1024/Nx2048 spatial controls, original active shift
target `1e-6`, 2.5 matched convergence orders,
near-null rule and frozen two-stage Radau structure.

The **only physical H3 source update** is the complete
Stage E action-derived NL0C Y sector: both aether and
scalar raw RHS rows, with the common `a^3`
action-density conversion. The historical scalar-only Y
piece must be replaced in its entirety, not added to
the new Y piece.

The initial projected boundary uses the **same Repair18
projection algorithm** but is recomputed on the
versioned total H3 source. It must not blindly reuse
the old numerical p0 array when the source has changed.
The old Repair22 solution and p0 are baseline
comparators, not new corrected-parent certifications.

A valid separately executed H3F PASS would certify
only the new window-local particular corrected-Y Z20.
The dependent normalized q20 bath projection must then
be recomputed and independently controlled. The old
Repair27 result cannot silently serve as corrected q20.

The independent full all-sector H4 source/Noether
identity must still be established before a new
science H4/Z21 reclosure. No finite physical eta,
observational inference, science-threshold relaxation,
historical relabeling or lensing is licensed.

## Next execution order

1. Locally reproduce the lightweight Stage E source
   tests with the already frozen runner, if a local
   byte-level trace is desired.
2. Implement a separate H3F corrected-Y source adapter,
   preserving frozen old solver modules and p0 algorithm.
3. Statically and scientifically audit/reproduce H3F
   under its exact preregistration before calling it
   a corrected Z20 parent.
4. Only after a valid new Z20 result, rebuild the
   dependent q20 parent and its time/quadrature controls.

No H3F implementation, science run or PASS is
contained in this prelock.
