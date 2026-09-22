# GE19 Repair33 Repair01 trace-fetch repair — lock

## Status

Repair33 Repair01 is an implementation-only local-runner repair after the
first local invocation stopped before science because the frozen Repair26
full-history trace was not present under the hard-coded results path.

No Repair33 science JSON existed before this repair.

## Frozen failure parent

File:

`docs/ge19_repair33_initial_execution_missing_trace_freeze.md`.

Blob:

`5dfbfaba76d56e0d182fd6491ed065584a7716e0`.

Commit:

`c3294a169fc752e57ebc778673e49ea7cb4e3dc0`.

## Repaired runner

File:

`ge19/run_local_repair33_h4_z21_particular.sh`.

Blob:

`0d9d23357a0717ebf5424268c545f38acca83db0`.

Commit:

`5b07ee7f40f51b1db5a9b3580eca69e981c3781a`.

The only execution-path change is frozen-parent acquisition.

If the Repair26 R1 trace is absent locally, the runner downloads:

- repository:
  `dvlahek/aest-memory-gravity`;
- workflow run:
  `35721220889`;
- artifact:
  `results_bundle_ge19_repair26_cancellation_free_full_history_bath_boundary`.

It then locates:

`ge19_repair26_R1_full_history_trace.dat`

and verifies:

- SHA-256:
  `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`;
- bytes:
  `26643162`.

This is exactly the already certified Repair26 parent used by Repair27.

## Dedicated Repair01 prelock

Workflow:

`.github/workflows/ge19-repair33-repair01-prelock-audit.yml`.

Blob:

`1b0f5274a6d28f65891b6e26c3d7729c1cd602fd`.

Workflow commit:

`fd3ba43afddd7d3c91ec5d1076f01887010d8450`.

Run:

`35776057485`.

Job:

`106909432119`.

Conclusion:

`success`.

The prelock checks the exact run ID, artifact name, trace filename, SHA,
byte count and unchanged Repair33 science invocation.

## Unchanged science contract

Repair33 implementation remains exactly:

- blob:
  `6863f6dd1f8d22acb9f891659ded34abbb747763`;
- commit:
  `9534debc82d2d2a50c832f400754ea2feee866c0`.

No equation, source block, GE05->GE06 factor, parent, boundary, grid, threshold
or gate changed.

## Scientific status

Repair33 science remains unconsumed.

The next local invocation is still the first valid H4/Z21 science attempt.
