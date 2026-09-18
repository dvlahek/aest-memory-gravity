# NL1C7B4 Repair18c — local result freeze

## Status

Frozen local WSL PASS from the first locked Repair18c execution.

Terminal classification:

`NL1C7B4_REPAIR18C_TWO_MODE_NULLSPACE_CHARACTERIZED`

with

`SCIENCE_RC=0`.

Execution HEAD:

`ed94edf52043577af56bd54cff65e789f3c36a84`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `19369`
  - SHA-256:
    `d49600f8b27536aeb0dca28d1d777d09439a376241c7f8f93b74e754c502e24b`
- evaluator log:
  - bytes: `19815`
  - SHA-256:
    `ae4237850a88fa27cea802b7c5c457b03e1a0727cc8c4a63d7e33e6c1fafe56a`
- local runner log:
  - bytes: `27011`
  - SHA-256:
    `0cbb252a4077c154a921404f78fa21a2aede73867f452b36f925f81cdeaaa73d`.

## Gate result

All six Repair18c gates PASS:

- R18C_G1 exact frozen provenance
- R18C_G2 exact Repair18b1 Jacobian reproduction
- R18C_G3 exact two-mode deficiency
- R18C_G4 SVD/subspace consistency
- R18C_G5 complete characterization
- R18C_G6 claim boundary

## Rank result

All three canonical scale cases have:

- Nr = 256
- rank = `508/510`
- deficient dimension = `2`
- deficient singular indices = `508,509`.

The parent Repair18b1 singular values/rank diagnostics are reproduced exactly.

## Cross-scale stability

The two-dimensional right-null subspace is extremely stable across scales.

Principal angles:

- scale 5 vs 10:
  - `0.006170076598359154 deg`
  - `0.079770357543969 deg`
- scale 5 vs 20:
  - `0.03140877232512969 deg`
  - `0.3995468109239379 deg`
- scale 10 vs 20:
  - `0.02524412130563218 deg`
  - `0.31977713821921205 deg`.

Maximum principal angle:

`0.3995468109239379 deg`.

Thus the same two-dimensional deficient subspace is present across the tested scales to sub-degree accuracy.

## Coordinate content

The total null-projector trace is 2.

Across the three scales the null leverage splits approximately:

- y_L: `0.4395-0.4397` of total trace;
- q_Rt: `0.5603-0.5605`.

One direction is almost exactly the constant q_Rt mode:

- scale 5 capture:
  `0.9999997891381511`;
- scale 10:
  `0.9999966690032341`;
- scale 20:
  `0.9999466716501019`.

The linear-r q_Rt candidate also has large capture:

- approximately `0.775-0.780`.

## Inner y_L localization

The second deficient content is strongly localized toward the inner y_L grid.

The largest leverage coordinate is always:

- block: `yL`
- radial index: `1`
- normalized radius:
  `r/R_s = 0.03137254901960784`
- leverage:
  approximately `0.5497-0.5500`.

Within the y_L block:

- first noncenter node contains about `62.53%` of y_L null leverage;
- first four nodes contain about `87.14%`;
- first eight nodes contain about `93.28%`;
- first sixteen nodes contain about `96.65%`.

The outer y_L leverage is negligible:

- outermost y_L candidate capture:
  approximately `8e-6`;
- last 16 y_L nodes contain only approximately `1.6e-4` of the y_L null leverage.

Thus the second deficient content is an inner/center-side mode, not an outer-boundary mode.

## Left-null compatibility

The parent residual is nearly orthogonal to the two left-null directions.

Relative left-null compatibility:

- scale 5:
  `9.707232843664437e-11`
- scale 10:
  `2.1911761962074124e-10`
- scale 20:
  `1.6006841801170347e-10`.

Therefore the rank deficiency is not accompanied by a substantial local linear compatibility obstruction.

## Interpretation

The frozen result supports the following narrow conclusions:

1. the deficient subspace is two-dimensional and highly scale-stable;
2. one mode is essentially a global constant q_Rt offset/integration mode;
3. the other mode is strongly concentrated in the inner y_L regularity region;
4. the outer boundary is not the dominant source of the second null direction;
5. the parent residual is almost entirely in the Jacobian column space.

This is consistent with non-uniqueness associated with a global q_Rt integration/gauge mode plus an inner regularity/boundary degree of freedom.

It does not yet license a specific pair of gauge/regularity conditions.

## Licensed continuation

A separately preregistered transversality audit may compare fixed candidate pairs of simple linear conditions against the frozen two-dimensional null subspace.

No nonlinear solve or state write may occur until a pair is shown to intersect the frozen null subspace independently and stably across all three scales.
