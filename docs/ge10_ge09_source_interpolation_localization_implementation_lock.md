# GE10 GE09 source-interpolation localization — implementation lock

## Status

Implementation locked before first GE10 execution.

GE10 is a result-informed diagnostic of the frozen GE09 science FAIL.

It cannot alter GE09.

## Frozen parent

GE09 classification:

`GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.

Result-freeze commit:

`456152e751f191a7bd6c9d596e3ab90492ec5162`.

Result-freeze blob:

`67eb2b1008a360560da486f592b57be23ffff54a`.

Frozen artifact:

- workflow run `35494446296`;
- artifact ID `10600457104`;
- digest
  `sha256:494639b2074336e704e06cf18b8875bc88d71c62cebfdb687e8e4c3f5270da38`.

Historical failed gate:

`source_grid_state_validation_abs_or_rel_le_1e4`.

Historical maximum:

`1.0032254188771416e-4`.

## Preregistration

Commit:

`b362517f5892cebd08f6b8435d9390aba47c4eef`.

File:

`ge10/predata_ge09_source_interpolation_localization.json`.

Frozen blob:

`0f128f46c23a12af48fe695e56b356da518f80bb`.

## Implementation

Commit:

`a896f662c41c3500115c214fe79414e7b1b556d0`.

File:

`ge10/ge09_source_interpolation_localization.py`.

Frozen blob:

`6762e53b80c21dbb907abc6f01080dd38cfa634c`.

Frozen imported GE09 driver blob:

`509fa9d7bb323034bbf77b26792f35e1cc2ff7c7`.

## Diagnostic representation

Use only the frozen artifact.

For `delta_dark`, reconstruct the source-grid mismatch with the unchanged GE09 cubic-Hermite representation.

Then deterministically repeat after accepted-endpoint decimation strides

`{4,2,1}`.

Fit

`log E = c + p log(stride)`.

Since physical endpoint spacing scales with stride, positive `p` is the observed convergence order as the representation is refined from stride 4 to 1.

Descriptive-only comparisons at the historical worst source row:

- state-only PCHIP;
- state-only linear interpolation.

Neither may replace GE09 Hermite.

## Frozen gates

- exact artifact provenance;
- exact parent FAIL classification;
- 30755 dense rows;
- 48 selected source rows;
- reproduce historical primary maximum within `1e-15`;
- historical global worst field remains `delta_dark`;
- strict error decrease stride 4 -> 2 -> 1;
- fitted convergence order >= `2.5`;
- primary Hermite error smaller than PCHIP at historical worst row;
- primary Hermite error smaller than linear interpolation;
- worst source row lies strictly inside an accepted-endpoint interval;
- all outputs finite.

## Terminal classifications

All gates pass:

`GE10_GE09_SOURCE_INTERPOLATION_LIMIT_CONFIRMED`.

Otherwise:

`GE10_GE09_SOURCE_INTERPOLATION_DIAGNOSTIC_FAIL`.

## Claim boundary

GE10 cannot:

- relabel GE09;
- relax `1e-4`;
- certify the complete GE06 jet;
- license Z20;
- change the interpolation representation.

A later representation-refinement study requires a new preregistration.
