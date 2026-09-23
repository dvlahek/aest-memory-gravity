# GE19 Repair40 valid diagnostic — piecewise stage-source decomposition freeze

## Status

Repair40 repair01 completed successfully and is frozen as a valid diagnostic result.

Classification:

`GE19_REPAIR40_PIECEWISE_STAGE_SOURCE_DECOMPOSITION_COMPLETE`.

Route:

`PIECEWISE_STAGE_SOURCE_DECOMPOSITION_COMPLETE`.

Repair40 is diagnostic-only. It does not certify Z21 and does not license lensing.

The initial Repair40 cancellation-contaminated attempt remains an immutable implementation failure and is not relabelled.

## Frozen local artifacts

Canonical JSON:

- bytes: `11719`;
- SHA-256:
  `f5618344db31328dc4e680eb41bb6a715da3fbe7e54ddff3cb53bc027386bf44`.

NPZ:

- bytes: `40834448`;
- SHA-256:
  `06c7799787abcc510259c626bcb9ca925f96efce13c7949a89690f243fbf01b5`.

Repair01 FULL log:

- bytes: `11719`;
- SHA-256:
  `f5618344db31328dc4e680eb41bb6a715da3fbe7e54ddff3cb53bc027386bf44`.

Outer runner log:

- bytes: `20820`;
- SHA-256:
  `112bffc28a638bff5a1148795068111475ee4781a923432b6b52cd5a34ec72f4`.

Terminal marker:

`GE19_REPAIR40_REPAIR01_DIAGNOSTIC_COMPLETE`.

## Integrity gates

All Repair40 implementation gates pass.

PCHIP and Akima reproduce frozen Repair39 exactly:

- PCHIP Z21 relative L2 = `0.0`;
- PCHIP active shift relative L2 = `0.0`;
- Akima Z21 relative L2 = `0.0`;
- Akima active shift relative L2 = `0.0`.

Frozen source-node reproduction maximum relative L2:

`5.669184795383803e-16`.

Stage-source decomposition closure:

`7.050062442856047e-19`.

Direct-delta propagated Z21 response closure:

`2.8954027388379403e-14`.

The original preregistered closure threshold remains `1e-9`; no threshold was relaxed.

All outputs are finite.

## Baseline and full alternative

PCHIP baseline:

- active Linf = `1.3797699672147026e-6`;
- active RMS = `1.2040175184158852e-6`.

Full Akima:

- active Linf = `1.2068124462343292e-6`;
- active RMS = `9.931227636322887e-7`.

Full Akima-minus-PCHIP active shift-field RMS:

`3.782252303026018e-7`.

## Piecewise source-stage decomposition

Stage-source delta L2 divided by the full Akima-minus-PCHIP stage-source L2:

- `2Q_GE06_cross`: `1.0059917444442532`;
- `INTERPOLATION_COUPLING`: `0.06678456186664335`;
- `2M1_GE05_mapped`: `0.0021630467073249634`;
- `2DY2`: `9.13821209669208e-13`;
- `2M2_GE05_mapped`: `1.51507048614126e-14`;
- `2Q_GE07_cross`: `1.786904841139529e-23`;
- `2Q_Lambda_cross`: `5.644076728113289e-34`.

## Propagated Z21-response ranking

Descending propagated Z21 response L2:

1. `2M1_GE05_mapped`;
2. `INTERPOLATION_COUPLING`;
3. `2Q_GE06_cross`;
4. `2M2_GE05_mapped`;
5. `2DY2`;
6. `2Q_GE07_cross`;
7. `2Q_Lambda_cross`.

The `2M1_GE05_mapped` direct-delta Z21 response is essentially the full response:

- relative response norm = `1.000000025452115`;
- complex alignment with the full response = `0.9999999999999967`.

## Active shift-response ranking

Descending active shift-metric difference RMS:

1. `2Q_GE06_cross`;
2. `INTERPOLATION_COUPLING`;
3. `2M2_GE05_mapped`;
4. `2M1_GE05_mapped`;
5. `2DY2`;
6. `2Q_GE07_cross`;
7. `2Q_Lambda_cross`.

For `2Q_GE06_cross`:

- active shift-field RMS change = `3.3448872380344193e-7`;
- fraction of full Akima-minus-PCHIP shift RMS = `0.8843638578416142`;
- alignment with the full shift difference = `0.9896848662049436`;
- active Linf changes from `1.3797699672147026e-6` to
  `1.2156072341464537e-6`;
- active RMS changes to `1.01844015962814e-6`.

Thus `2Q_GE06_cross` carries the dominant shift-sensitive stage-source representation effect.

## Deterministic next targets

The preregistered rankings do not have the same first component.

Therefore the mandatory follow-up targets are exactly:

- `2M1_GE05_mapped`;
- `2Q_GE06_cross`.

Frozen follow-up kind:

`DIRECT_FINE_GRID_RECONSTRUCTION_OF_TARGET_PHYSICAL_PIECES`.

No post-hoc target selection is licensed.

## Interpretation

Repair40 separates two distinct numerical sensitivities.

The total propagated Z21 representation response is dominated by the mapped
GE05 linear-memory term `2M1_GE05_mapped`.

The actual active shift backward-error response is dominated by the GE06
quadratic cross term `2Q_GE06_cross`.

This distinction is important. A single source-piece metric is insufficient:
the large Z21 response and the shift-gate response live in different source
directions.

The next diagnostic must therefore reconstruct both target physical pieces
on a finer time representation and compare their direct fine-grid values
against the frozen PCHIP/Akima stage representations before any new H4/Z21
science reclosure.

## Claim boundary

Repair40 does not certify:

- Z21;
- finite physical eta;
- full-species nonlinear cosmology;
- lensing;
- any observational signal.

Repair37 remains historical valid FAIL. Repair38, Repair39 and Repair40 are
diagnostic results only.
