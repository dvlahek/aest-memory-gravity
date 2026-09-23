# GE19 Repair36 local Lambda-complete H4/Z21 runner — lock

## Status

The first local Repair36 science execution path is frozen.

Runner:

`ge19/run_local_repair36_lambda_complete_h4_z21_reclosure.sh`.

Blob:

`4225ef8bea796f4b93ea9aa6981e15e7a0ec10e5`.

Commit:

`22e4a7ab79cfb18732d3de2d9ad63d044efe39cc`.

Global static audit:

- run:
  `35824417470`;
- conclusion:
  `success`.

Dedicated Repair36 Lambda-complete prelock:

- run:
  `35824217854`;
- job:
  `107062334933`;
- conclusion:
  `success`.

## Bound contract

Repair36 preregistration:

- commit:
  `fa5f6766bdc4df5f05147a57de292638a90af998`;
- blob:
  `89ec97f3b3e92d1077c9faf174a308ea73dce339`.

Repair36 implementation:

- final prelock implementation commit:
  `6b12114ff89be6b954f2dbcb5c09e0424e666a0c`;
- blob:
  `cf2caafd5ae2399cd3e6f6db7716aece20e8bb6c`.

Repair36 implementation lock:

- commit:
  `e3c60d0ac76a2c9cfcd3d0fe3c641136a421bb4a`;
- blob:
  `7aaa8ca967935d3a6c12b1aef2c938da00a1e91d`.

Repair35 valid FAIL localization:

- commit:
  `73dd25c9512256100e5a2e6391cd6d5cea822117`;
- blob:
  `578510ab2cf270edc518f0cbbe90c8e0ef50f4cd`.

## Execution rule

The first Repair36 invocation that emits a valid Repair36 science JSON is
frozen as PASS or FAIL.

Implementation/execution failures before a valid science JSON may be repaired
without changing the frozen Repair36 contract.

Repair35 remains historical and is not relabelled.

A Repair36 PASS certifies only the canonical window-local particular reduced
Z21 state. It does not certify a primordial homogeneous Z21 mode, a
full-species nonlinear cosmology, finite eta, or an observational signal.
