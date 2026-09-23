# GE19 Repair40 piecewise stage-source decomposition — implementation lock

## Status

Repair40 is frozen before its first local diagnostic execution.

Repair40 is diagnostic-only. It cannot relabel Repair37--Repair39, certify
Z21, alter the frozen 1e-6 science target, or license lensing.

Its sole purpose is to decompose the valid Repair39 Akima-versus-PCHIP
stage-source dependence into the six frozen Repair37 H4 source pieces plus
an explicit nonlinear interpolation-coupling residual.

## Frozen Repair39 parent

Freeze file:

`docs/ge19_repair39_valid_stage_source_dependence_freeze.md`.

Freeze commit:

`5c6740d3ca4dbc49f148c869a2cbcca092b844cb`.

Freeze blob:

`1e93a0111d385fb062fb1eff2f34af6d722487e1`.

Frozen Repair39 artifacts:

- JSON/FULL SHA-256:
  `b058d4acb51dd4e0b964fcccb306b7eb105466941b5e0900ae0c84a29374624e`;
- NPZ SHA-256:
  `0bf5b0c2f26cc06b98eab1fb326757ed409cf91c86c23e995251dfd32571c451`;
- outer runner SHA-256:
  `d2470549728e2a34256753baa6330267ed1ba5df7d4ff23e8ffbbd1adf786504`.

Frozen Repair39 route:

`STAGE_SOURCE_REPRESENTATION_DEPENDENCE_CONFIRMED`.

## Frozen preregistration

File:

`ge19/repair40_predata_piecewise_stage_source_decomposition.json`.

Preregistration commit:

`98faa110fd46432e93e5637c2102691c4d3d9c96`.

Blob:

`05b34db63552d8e0c6be9ee90d705770350bd567`.

## Frozen implementation

File:

`ge19/repair40_piecewise_stage_source_decomposition.py`.

Implementation commit:

`edebd3a279b0e1732c4fd59c87ea051e6f678413`.

Blob:

`a8801d2b517540b6407a12ca2ff42774ea2b84b3`.

Repair40 loads, rather than reconstructs, the frozen Repair37 primary source
pieces:

- `2Q_GE06_cross`;
- `2Q_GE07_cross`;
- `2Q_Lambda_cross`;
- `2DY2`;
- `2M1_GE05_mapped`;
- `2M2_GE05_mapped`.

No H4 source builder, bath reconstruction, DY2 recomputation, Q-cross
recomputation or memory-source recomputation is called.

## Exact decomposition

Let

`S_P = PCHIP(total)`

and

`S_A = AKIMA(total)`.

For each physical source piece j:

`delta_j = AKIMA(piece_j) - PCHIP(piece_j)`.

The explicit nonlinear interpolation-coupling residual is

`delta_c = S_A - S_P - sum_j delta_j`.

Therefore the stage-source identity is exact by construction:

`S_A - S_P = sum_j delta_j + delta_c`.

Each component variant propagated by Repair40 is

`S_j = S_P + delta_j`.

The baseline and full alternative are also propagated directly.

## Frozen propagation

Every variant uses:

- the frozen Repair37 projected p0;
- the frozen Repair13 reduced background;
- the Repair07/Repair11 canonical H4 operator;
- the Repair07 cancellation-safe shift metric;
- the endpoint-safe Repair38 two-stage Radau IIA implementation;
- exactly four internal Radau substeps per frozen Nt128 interval.

No source node, projected boundary, operator coefficient, threshold or
physical assumption changes.

## Integrity gates

Before ranking is interpreted:

- PCHIP baseline Z21 must reproduce Repair39 within relative L2 <= 1e-11;
- PCHIP active shift metric must reproduce Repair39 within relative L2 <= 1e-10;
- full Akima Z21 must reproduce Repair39 within relative L2 <= 1e-11;
- full Akima active shift metric must reproduce Repair39 within relative L2 <= 1e-10;
- every component variant must reproduce the frozen source nodes within
  relative L2 <= 1e-12;
- stage-source decomposition closure must be <= 1e-12;
- propagated Z21 linear-response decomposition closure must be <= 1e-9;
- all outputs must be finite;
- active sample count must remain exactly 23850.

A failure is an implementation failure and no ranking may be interpreted.

## Ranking rule

There is no dominance threshold.

Repair40 reports two deterministic rankings:

1. descending propagated Z21 response L2;
2. descending active shift-metric difference RMS.

If the same component is first in both rankings, that component is the
primary follow-up target.

If the first components differ, both are mandatory follow-up targets.

If `INTERPOLATION_COUPLING` is a target, the next diagnostic must compare
sum-before-interpolation with interpolation-before-sum before direct
reconstruction of a physical source piece.

If only physical pieces are targets, a later diagnostic may directly
reconstruct those pieces on a finer time grid.

## Dedicated prelock

Workflow:

`.github/workflows/ge19-repair40-prelock-audit.yml`.

Workflow commit:

`972a589e3897b31dd40d2be4b703a4a2b7481a5c`.

Workflow blob:

`3c5ef1bd3b597c5f2da8a05937bff8daedf56c63`.

Run:

`35878449754`.

Run conclusion:

`success`.

## Claim boundary

Repair40 can only localize the source-representation response.

It cannot select a physically preferred interpolant, certify Z21, license
lensing, introduce finite physical eta or use observational data.
