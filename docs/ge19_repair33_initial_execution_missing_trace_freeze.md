# GE19 Repair33 first local execution — missing Repair26 trace freeze

## Status

The first local Repair33 invocation stopped before any H4/Z21 science execution.

Terminal route:

`GE19_REPAIR33_MISSING_REPAIR26_TRACE`.

No Repair33 science JSON was produced.

Therefore the frozen Repair33 science contract remains unconsumed and an
implementation-only runner repair is permitted.

## Passed pre-science checks

The local invocation passed:

- `GE19_REPAIR33_LOCK_PASS`;
- `GE19_REPAIR33_LOCAL_PREEXECUTION_AUDIT_PASS`;
- `GE19_REPAIR33_LOCAL_PARENTS_PASS`.

It then stopped because the runner expected the Repair26 R1 full-history trace
at a fixed local path:

`results/ge19_repair26_R1_full_history_trace.dat`.

## Missing parent

Frozen Repair26 trace:

- filename:
  `ge19_repair26_R1_full_history_trace.dat`;
- SHA-256:
  `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`;
- bytes:
  `26643162`;
- workflow run:
  `35721220889`;
- artifact:
  `results_bundle_ge19_repair26_cancellation_free_full_history_bath_boundary`;
- artifact ID:
  `10690709843`.

The same frozen parent was already downloaded on demand by the certified
Repair27 local runner.

## Allowed Repair33 Repair01 change

Only the local runner may change.

If the exact Repair26 trace is not already present locally, the runner may:

1. require authenticated GitHub CLI;
2. download the frozen Repair26 artifact from run `35721220889`;
3. locate the exact R1 full-history trace inside a dedicated frozen artifact
   directory;
4. verify SHA-256 and byte count;
5. pass that verified path to the unchanged Repair33 science implementation.

No Repair33 source, equation, parent selection, boundary, grid, threshold,
normalization or gate changes are permitted.

## Scientific status

Repair33 has not yet produced a valid science PASS or FAIL result.

Z11 remains certified.

H4/Z21 remains licensed but not yet executed.
