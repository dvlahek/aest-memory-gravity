# GE19 Repair39 local stage-interpolation diagnostic runner — lock

## Status

The first local Repair39 diagnostic execution path is frozen.

Runner:

`ge19/run_local_repair39_frozen_source_stage_interpolation_localization.sh`.

Runner commit:

`b29810d49af4d9a44868faadcc845e9cd203f279`.

Runner blob:

`71d3baf0967ce4a3f6d2e3af0bb7e91de0c05c81`.

Static runner audit:

- run:
  `35870636584`;
- job:
  `107213478522`;
- conclusion:
  `success`.

## Bound contract

Repair39 preregistration:

- commit:
  `87aff396a2a8505b50001a1a5169a3167477e1f7`;
- blob:
  `7f289263768e0eb1e3a9af47ecc6b10f71f0065a`.

Repair39 implementation:

- commit:
  `0ae58cc9c71c7afac85654b30a85162d27d79f4f`;
- blob:
  `91e65251198983205394196893b862f08dd2a585`.

Repair39 implementation lock:

- commit:
  `6e7f21073978a2c866bd467ed32e8a5fc39200d9`;
- blob:
  `a1c2f6d97d06c46a460c38c3327b772e732156d9`.

Repair39 prelock:

- workflow commit:
  `9bcfdd4d9d93d7739079c3034bc7b9fe7dd32ac0`;
- workflow blob:
  `2470783b6cd3307c8d03922ebe9391cc82ebbd6b`;
- run:
  `35870448283`;
- job:
  `107212831905`;
- conclusion:
  `success`.

Repair38 valid diagnostic freeze:

- commit:
  `ada593c99c7bc217313b1f7c8ff99504f13e8d10`;
- blob:
  `040af5dcb90070d05e3ab7e98623a4e03aa25009`.

## Execution rule

Repair39 keeps the Repair37 source nodes, Repair37 projected p0, Repair13
reduced background, canonical operator, shift metric, active mask and science
target fixed.

It uses four internal Repair38 Radau substeps per Nt128 interval for every
method.

Only the off-node source-at-stage interpolation varies:

- PCHIP;
- CubicSpline not-a-knot;
- Akima.

The PCHIP factor4 result must reproduce frozen Repair38 substep4 before any
routing can be interpreted.

The interpolation sensitivity is normalized by the already frozen Repair38
PCHIP factor2-to-factor4 active-field change.

A valid result routes only to:

- `STAGE_SOURCE_REPRESENTATION_DEPENDENCE_CONFIRMED`;
- `STAGE_SOURCE_REPRESENTATION_INVARIANT_OTHER_FLOOR`;
- `MIXED_STAGE_REPRESENTATION_SENSITIVITY`.

Implementation failures may be repaired without changing this frozen
diagnostic contract.

Repair39 cannot certify Z21 or license lensing.
