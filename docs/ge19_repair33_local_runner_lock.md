# GE19 Repair33 local H4/Z21 runner — lock

## Status

The first local Repair33 science execution path is frozen.

Runner:

`ge19/run_local_repair33_h4_z21_particular.sh`.

Blob:

`53ff2bd381314101977a85b5152d549c349abf12`.

Commit:

`0c881ec19e4c596bb3f43b5663251b025601b47d`.

Global static audit:

- run:
  `35767272285`;
- conclusion:
  `success`.

## Bound science contract

Repair33 preregistration:

- blob:
  `f1c646e3011193b7df61014365e985b47ad8e0b4`;
- commit:
  `b98af3f09a3adcca779f27fd19c9f8d78fa3b814`.

Repair33 implementation:

- blob:
  `6863f6dd1f8d22acb9f891659ded34abbb747763`;
- commit:
  `9534debc82d2d2a50c832f400754ea2feee866c0`.

Dedicated prelock:

- workflow blob:
  `4e022a0050a7be1b69895343915f6300fd019475`;
- run:
  `35767062116`;
- conclusion:
  `success`.

Implementation lock:

- blob:
  `ae2bf35a76b67667b07175ca696dff23bf6dcceb`;
- commit:
  `a5d4b7d013346c5501ed59f353a57261057b17cf`.

## Execution rule

The runner hash-checks all local parents before science starts, including the
frozen Repair26 full-history trace.

The first execution that emits a valid Repair33 JSON is frozen as scientific
PASS or FAIL.

Implementation/execution failures before a valid Repair33 JSON may be repaired
without changing the frozen Repair33 science contract.

Repair33 itself makes no observational claim and does not certify a primordial
or full-species Z21 state.
