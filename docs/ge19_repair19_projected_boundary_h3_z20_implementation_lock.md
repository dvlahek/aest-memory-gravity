# GE19 Repair19 projected-boundary reduced-H3 Z20 propagation lock

## Status

**SCIENCE IMPLEMENTATION LOCKED BEFORE REPAIR19 LOCAL RESULT**

Repair18 is frozen as

`ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_CERTIFIED`.

Repair19 is the first new H3/Z20 propagation after the Repair14 FAIL. The only science change relative to Repair14 is the initial canonical boundary.

## Parent Repair18 freeze

Commit:

`3892ee81c8030ee7c5131d1aaf1f333cbdbe6509`

File:

`docs/ge19_repair18_projected_momentum_boundary_result_freeze.md`

Blob:

`c8bf1226cc6491c3be9246c629d958f681255e81`

Frozen Repair18 JSON:

- SHA-256 `d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc`;
- bytes `3265739`.

## Repair19 preregistration

Commit:

`ce0b1767874d71eee59b55ad4633033c3d714892`

File:

`ge19/repair19_predata_projected_boundary_reduced_h3_z20_propagation.json`

Blob:

`8eefdfd8f3a5b07702a5e1f6b28f911dc3b6089a`

## Repair19 implementation

Final implementation commit before lock:

`2bc808214b7b099ecb78084e5c41acebc1d3be7b`

File:

`ge19/repair19_projected_boundary_reduced_h3_z20_propagation.py`

Blob:

`ecf1577b19c7f03e8762c1c29822881158c3cb56`

The earlier implementation commit `8dabdf370d82483fbb829d159546e36a8d766b01` is superseded only by a temporary-NPZ filename wiring fix. No science formula, boundary rule or threshold changed.

## Frozen unchanged physics blobs

Repair07 canonical integrator/source infrastructure:

`ge19/repair07_window_retarded_reduced_h3_z20_particular.py`

blob:

`e34d28a2062c748f48bc82fa928844b02631de25`.

Repair14 H3 source + Lambda c2 + Stage-B pipeline:

`ge19/repair14_self_consistent_reduced_h3_z20_particular.py`

blob:

`06c5ced952c2370cfa4aaadb6ef8f72d2d7221de`.

Repair18 projected-boundary solver:

`ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py`

blob:

`c7b3a5c689bd78a65a8150c26e1fbfae108cb580`.

## Exact Repair19 change relative to Repair14

Repair14 used:

`q0=0, qdot0=0`

at z=1.5.

Repair19 uses:

`q0=0`

and

`p0 = Repair18 projected canonical momentum`

from the frozen doubly equilibrated GELSD lapse+shift solve with exactly four refinement sweeps.

Everything after y0 construction uses the frozen Repair07 Radau2 canonical propagation and reconstruction machinery.

## Frozen boundary reproduction gates

- Repair18 p0 relative L2 <= `1e-12`;
- primary/control p0 relative L2 <= `1e-12`;
- initial scaled constraint residual <= `1e-8`;
- initial lapse backward error <= `1e-6`;
- initial shift backward error <= `1e-6`;
- initial eliminated algebraic residual <= `1e-8`;
- rank = augmented rank = `2`.

## Unchanged Stage-B gates

- Nx1024/Nx2048 source m=1..40 relative L2 <= `5e-4`;
- primary linear-system relative residual <= `1e-8`;
- shift backward error <= `1e-6`;
- anisotropy backward error <= `1e-6`;
- Nt64/Nt32 propagated-state relative L2 <= `5e-3`;
- all C and beta cases complete;
- all outputs finite.

No threshold is changed from Repair14.

## Executable prelock audit

Workflow:

`.github/workflows/ge19-repair19-prelock-audit.yml`

Blob:

`2b9c3bf4f817c427b1f9914c65aa77e401a1379f`

Run:

`35617194247`

Job:

`106390820266`

Conclusion:

`success`.

Terminal marker:

`GE19_REPAIR19_PRELOCK_AUDIT_PASS`.

The audit explicitly reproduced the frozen blobs:

- Repair07 `e34d28a2062c748f48bc82fa928844b02631de25`;
- Repair14 `06c5ced952c2370cfa4aaadb6ef8f72d2d7221de`;
- Repair18 `c7b3a5c689bd78a65a8150c26e1fbfae108cb580`.

It also verifies that Repair19 defines no replacement GE06/GE07/Lambda/Y2 source function.

## Output contract

Repair19 writes:

- science JSON;
- NPZ containing the Repair14 payload plus exact projected p0 and qdot0 arrays for primary/control;
- FULL log.

PASS requires every boundary-reproduction gate and every unchanged Stage-B gate.

## Stop rule

No q20 and no H4/Z21 until the Repair19 result is frozen PASS.

No observational bridge is licensed by implementation lock alone.

## Claim boundary

A Repair19 PASS would certify only the low-mode constraint-compatible window-local reduced-H3 Z20 particular directional state on the Repair13 self-consistent background. It would not certify the omitted homogeneous/primordial second-order state, full species, finite eta, physical-amplitude nonlinear evolution, lensing or observations.
