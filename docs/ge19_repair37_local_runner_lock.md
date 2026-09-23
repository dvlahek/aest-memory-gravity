# GE19 Repair37 local cancellation-safe FD8 H4/Z21 runner — lock

## Status

The first local Repair37 science execution path is frozen.

Runner:

`ge19/run_local_repair37_cancellation_safe_fd8_h4_z21_reclosure.sh`.

Blob:

`db197b842392e67afcfcabf1f1c1741376a0585f`.

Commit:

`7391cc9c29f23a1a5a68f4acba05500c8e3b4839`.

Global static audit:

- run:
  `35826793781`;
- job:
  `107070191167`;
- conclusion:
  `success`.

Dedicated Repair37 prelock:

- run:
  `35826658894`;
- job:
  `107069773711`;
- conclusion:
  `success`.

## Bound contract

Repair37 preregistration:

- commit:
  `1ef3d95bbd9977d89c3f12beef8eada82995c1a9`;
- blob:
  `cd60e8bc725588cdc13f22255fcba16ba27393d1`.

Repair37 implementation:

- final implementation commit:
  `110f066a9d1bbb2b8ca28cff6b4c08404c457a67`;
- blob:
  `45d203a092f9ac71cc612b15df5f0c0c630f5898`.

Repair37 implementation lock:

- commit:
  `93633e7c58ce478c6953da0011d3e19b27733ad1`;
- blob:
  `a9709da00465d19bc9c173fcc11ccc4f124ffbc4`.

Repair36 valid FAIL localization:

- commit:
  `fa82cf21c3bfd0b1bdb9f6c451670e83b1e115c0`;
- blob:
  `4ff3b601e96936963e8f2d36e2a22ba5c5f059ed`.

## Execution rule

The first Repair37 invocation that emits a valid Repair37 science JSON is
frozen as PASS or FAIL.

Implementation/execution failures before a valid science JSON may be repaired
without changing the frozen Repair37 contract.

Repair36 remains historical and is not relabelled.

A Repair37 PASS certifies only the canonical window-local particular reduced
Z21 state. It does not certify a primordial homogeneous Z21 mode, a
full-species nonlinear cosmology, finite eta, or an observational signal.
