# GE19 Repair42 direct-target H4 propagation — implementation lock

## Status

Repair42 is frozen before its first local execution.

Repair42 is diagnostic-only. It cannot relabel Repair37--Repair41, certify
Z21, relax the frozen 1e-6 science target, introduce finite physical eta,
use observational data, or license lensing.

## Frozen Repair41 parent

Freeze:

`docs/ge19_repair41_valid_direct_fine_grid_target_reference_freeze.md`.

Freeze commit:

`1e1ffa694eb9661be72907f59b1de317d87f713d`.

Freeze blob:

`cfbc013969a6572c52c5d8d3d090355755b81ee2`.

Artifacts:

- JSON/FULL SHA-256:
  `1b18fede26b021e077ffe5c8b6b7ff0dc727b4defaab48e63491c86d868d1320`;
- NPZ SHA-256:
  `6bfb87ea21d55e2a1d2b16aee9bc8d7246111f91a064a78b74d2ed946ec2ba45`;
- outer runner SHA-256:
  `8d9360c8bad9f7f7ed985957cf2230e0713715dd7057347feb10f31f5bee4375`.

Frozen route:

`DIRECT_TARGET_REFERENCE_RESOLVED`.

## Frozen Repair37 baseline

Repair42 retains:

- the frozen Repair37 primary total H4 source nodes;
- the unchanged Repair07 PCHIP total-source stage representation;
- the frozen Repair37 projected p0;
- the frozen Repair37 active mask;
- the frozen Repair07+Repair11 canonical operator;
- the original factor-1 two-stage Radau IIA propagation.

Repair37 remains immutable FAIL and is not relabelled.

## Frozen preregistration

File:

`ge19/repair42_predata_direct_target_h4_propagation_diagnostic.json`.

Commit:

`8aa14dffd3d508bcc4920b9cb68ff520a4d2520d`.

Blob:

`cbdb7b66e57a24c44fb03c0856ffdc1977303844`.

## Frozen implementation

File:

`ge19/repair42_direct_target_h4_propagation_diagnostic.py`.

Commit:

`e2634cfe7be0eb5590305ae55197d483dbd9818f`.

Blob:

`8576118fec60dd6ac1593459da9354d424d04fd5`.

## Direct correction

The mandatory Repair40/41 target pieces are:

- `2M1_GE05_mapped`;
- `2Q_GE06_cross`.

For direct resolution N in {382,763}:

`delta_target_N(stage) = direct_target_N(stage) - frozen_target_PCHIP(stage)`.

The corrected total source at the frozen factor-1 stage is:

`S_corrected = S_total_PCHIP + sum(delta_target_N)`.

The direct target arrays are never interpolated inside Repair42.

They are located by exact/tolerance-bounded lookup on the frozen Repair41
stage coordinate array.

At the initial x0 point the frozen PCHIP node value is retained, because the
Repair41 direct reference is defined only at factor-1 stage/right-endpoint
coordinates and the projected p0 is frozen.

## Propagated variants

Repair42 propagates:

- `PCHIP_BASELINE`;
- `DIRECT382_M1_ONLY`;
- `DIRECT382_Q_GE06_ONLY`;
- `DIRECT382_BOTH`;
- `DIRECT763_M1_ONLY`;
- `DIRECT763_Q_GE06_ONLY`;
- `DIRECT763_BOTH`.

It also propagates the source corrections directly from zero delta p0 for
stable report-only delta-Z21 diagnostics.

## Interpretation gates

Before routing:

- Repair41 and Repair37 hashes/routes must match;
- Repair41 stage coordinates must reproduce generated factor-1 stage
  coordinates within `1e-13`;
- saved Repair41 target PCHIP values must reproduce Repair37 standalone
  target PCHIP within relative L2 `1e-12`;
- PCHIP baseline Z21 must reproduce Repair37 within relative L2 `1e-11`;
- PCHIP baseline shift metric must reproduce Repair37 within relative L2
  `1e-10`;
- projected p0 must match exactly;
- active count must remain exactly 23850;
- all outputs must be finite.

## Routing

No new improvement threshold exists.

Only the frozen science target `1e-6` is used.

- if both `DIRECT382_BOTH` and `DIRECT763_BOTH` have active Linf
  <= `1e-6`:
  `DIRECT_TARGET_CORRECTION_BELOW_SCIENCE_TARGET`;
- if both are > `1e-6`:
  `DIRECT_TARGET_CORRECTION_ABOVE_SCIENCE_TARGET`;
- if they lie on opposite sides:
  `DIRECT_TARGET_CORRECTION_THRESHOLD_SIDE_UNRESOLVED`.

Repair42 itself cannot certify Z21.

## Audits

Static implementation audit:

- run:
  `35918028322`;
- conclusion:
  `success`.

Dedicated prelock:

- workflow commit:
  `a7303cb29ec0929c8e2d00350804af70856a60fb`;
- workflow blob:
  `ece1e7ca5522b71ad92f045bf7cc6cefbd896080`;
- run:
  `35918082912`;
- job:
  `107374703486`;
- conclusion:
  `success`.

## Claim boundary

Repair42 is only a direct-target stage-correction propagation diagnostic.

It does not perform a science H4/Z21 reclosure, certify Z21, introduce finite
eta, use observations or license lensing.
