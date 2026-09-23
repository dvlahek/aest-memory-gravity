# GE19 Repair38 repair01 local diagnostic runner — lock

## Status

The repaired local Repair38 diagnostic execution path is frozen before the
next attempt.

Runner:

`ge19/run_local_repair38_repair01_frozen_source_radau_substep_localization.sh`.

Runner commit:

`267c9fe687a46a988b6a9bbe1d88a3e7e39a0c24`.

Runner blob:

`4d8504e1ad6ed42498ea0e7a9436dbf50cb12c99`.

Static runner audit:

- run:
  `35858294399`;
- job:
  `107171992584`;
- conclusion:
  `success`.

## Repair01 implementation binding

Implementation repair commit:

`6915d67dfbe4b86940266a72c7e6141bc95e82c2`.

Implementation blob:

`fbab2cd31cfcb69c21c3e066e6d8d17844369d32`.

Repair01 implementation lock:

- commit:
  `4da06e54ce3ce46faf2b356660051d37099a7f23`;
- blob:
  `69936a8db68e305d6a82e8f7279dd450436438d1`.

Updated dedicated prelock:

- workflow commit:
  `cf65f82b4a564228d0bb9389f6def038b104a43c`;
- workflow blob:
  `38f4afee0384f4f5b3de870e4adc2c1187442137`;
- run:
  `35858136063`;
- job:
  `107171486168`;
- conclusion:
  `success`.

## Preserved initial failure

The initial Repair38 execution failure remains frozen at:

`docs/ge19_repair38_initial_execution_endpoint_domain_implementation_fail_freeze.md`.

FULL log SHA-256:

`9f07880a9a86e8d9be05407efd3f0f44d0e076be566f69bb915fa516a8f553f2`.

It is an implementation failure only and is not a diagnostic FAIL.

## Execution rule

The repaired runner binds:

- the unchanged Repair38 preregistration;
- the repaired endpoint-safe implementation;
- the updated prelock;
- the Repair37 valid-FAIL freeze;
- the Repair38 implementation-failure freeze;
- the Repair38 repair01 implementation lock.

The original Repair38 canonical JSON/NPZ output names are retained because no
valid diagnostic JSON has yet been emitted.

A distinct repair01 FULL log is used so the initial failure log is not
overwritten.

A valid Repair38 diagnostic JSON, if emitted, must be frozen exactly as
emitted.

Repair38 remains diagnostic-only. It cannot certify Z21 or license lensing.
