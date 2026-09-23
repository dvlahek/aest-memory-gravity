# GE19 Repair40 local piecewise stage-source diagnostic runner — lock

## Status

The first local Repair40 diagnostic execution path is frozen.

Runner:

`ge19/run_local_repair40_piecewise_stage_source_decomposition.sh`.

Runner commit:

`99137bd8645965d8543ce24f6ce4b937894f1ccc`.

Runner blob:

`8160be8b08a45947d30fa0a0795a6645a567b327`.

Static runner audit:

- run:
  `35878701034`;
- job:
  `107241236547`;
- conclusion:
  `success`.

## Bound Repair40 contract

Preregistration:

- commit:
  `98faa110fd46432e93e5637c2102691c4d3d9c96`;
- blob:
  `05b34db63552d8e0c6be9ee90d705770350bd567`.

Implementation:

- commit:
  `edebd3a279b0e1732c4fd59c87ea051e6f678413`;
- blob:
  `a8801d2b517540b6407a12ca2ff42774ea2b84b3`.

Implementation lock:

- commit:
  `7194f5543a9297794e8b2847a91dc7336b652d22`;
- blob:
  `36155cc821701e27cd9a79e6cf526174affff856`.

Dedicated prelock:

- workflow commit:
  `972a589e3897b31dd40d2be4b703a4a2b7481a5c`;
- workflow blob:
  `3c5ef1bd3b597c5f2da8a05937bff8daedf56c63`;
- run:
  `35878449754`;
- conclusion:
  `success`.

Frozen Repair39 parent:

- freeze commit:
  `5c6740d3ca4dbc49f148c869a2cbcca092b844cb`;
- freeze blob:
  `1e93a0111d385fb062fb1eff2f34af6d722487e1`;
- JSON/FULL SHA-256:
  `b058d4acb51dd4e0b964fcccb306b7eb105466941b5e0900ae0c84a29374624e`;
- NPZ SHA-256:
  `0bf5b0c2f26cc06b98eab1fb326757ed409cf91c86c23e995251dfd32571c451`;
- outer runner SHA-256:
  `d2470549728e2a34256753baa6330267ed1ba5df7d4ff23e8ffbbd1adf786504`.

## Execution rule

The local runner verifies exact repository blobs and frozen local parent
hashes before execution.

Repair40 propagates:

- the exact Repair39 PCHIP baseline;
- the exact Repair39 full Akima alternative;
- one PCHIP-baseline plus delta variant for each of the six frozen Repair37
  H4 source pieces;
- one PCHIP-baseline plus the explicit interpolation-coupling residual.

All variants use the same frozen projected p0, factor-4 endpoint-safe Radau
march, H4 operator, active mask and shift metric.

Before ranking can be interpreted, baseline/full reproduction, frozen-node
identity, stage-source decomposition closure, propagated Z21 response
closure and finiteness must all pass.

A valid result may route only to:

`PIECEWISE_STAGE_SOURCE_DECOMPOSITION_COMPLETE`.

The deterministic follow-up target is then read from the two preregistered
rankings.

Repair40 cannot certify Z21 or license lensing.
