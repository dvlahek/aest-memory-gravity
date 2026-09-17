# NL1C7B4 Repair06 — implementation lock

Status: **IMPLEMENTATION LOCKED BEFORE OFFICIAL RUN**

Pre-data preregistration commit:

`fac8014a1d8740fc2eb131504be812c8e209db67`

Repair05 frozen result commit:

`56de1b3bf028dfdbbab2684bde652056561074c1`

Repair05 frozen evaluator:

- path: `nl1c7b/initial_constraint_certification_repair05.py`
- blob SHA: `34fd22c73171fce5e32920a94d71d05de61521f6`

Repair06 implementation:

- path: `nl1c7b/initial_constraint_certification_repair06.py`
- implementation commit: `d7bc0b39af33e120299043be3d68bae862db8e47`
- blob SHA: `eca6a857def972663252c44165b6afd047a75fcd`

## Locked numerical design

Repair06 imports the Repair05 analytic evaluator directly. No physical term or normalization is reimplemented.

Primary resolutions are exactly `512`, `1024`, and `2048` radial points.

Both preregistered adjacent-grid gates are mandatory:

- 512 -> 1024 relative RMS difference <= `0.02`;
- 1024 -> 2048 relative RMS difference <= `0.02`.

The exception remains unchanged: a pair passes automatically only if both RMS normalized residuals are below `1e-8`.

All three scales (`5`, `10`, `20 h^-1 Mpc`) and all nine Y/beta labels are retained, giving exactly 81 primary analytic rows.

The retained 256-point C7A NPZ is used only for exact state-reproduction provenance control and is not one of the Repair06 primary grid levels.

## Frozen science thresholds

The Repair05 thresholds are inherited without modification:

- `PASS_LIMIT = 1e-5`;
- `MISMATCH_FLOOR = 0.1`;
- `ZERO_REL_LIMIT = 1e-12`;
- `ZERO_ABS_FLOOR = 1e-30`;
- `GRID_LIMIT = 2e-2`;
- `BRIDGE_LIMIT = 1e-6`.

## Parent provenance

Repair05 official run: `35225084320`

Repair05 head: `cfb43b99162db1b8cf25621d3de795b42e1e2cf9`

Repair05 artifact: `10498343763`

Repair05 artifact SHA256:

`5798127479d0a359b5805aa7bd846caee035e582b0fdb3a08b7cd7ab2dc2e9ce`

Expected parent classification:

`NL1C7B4_REPAIR05_IMPLEMENTATION_FAIL`

The implementation explicitly requires the parent 20-Mpc grid-control failure to be present. It does not reinterpret or overwrite Repair05.

## Claim boundary

No state projection, fitted coefficient, dust-sign change, radial standard-species insertion, Y selection, scale selection, nonlinear evolution, or finite-eta calculation is part of Repair06.

Any official run must verify the exact preregistration, Repair05 evaluator blob, Repair06 implementation blob, C7A retained inputs, and Repair05 artifact digest before execution.