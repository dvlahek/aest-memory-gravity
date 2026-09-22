# GE19 Repair35 local H4/Z21 runner — lock

## Status

The first local Repair35 science execution path is frozen.

Runner:

`ge19/run_local_repair35_direct_bilinear_matched_shift_h4_z21.sh`.

Blob:

`278befa3dc9d4d69446704ca5adca07b6b4a9402`.

Commit:

`69e4894aa13a24b473b1346664b10f7f00e9bb53`.

Global static audit:

- run:
  `35782475664`;
- conclusion:
  `success`.

Dedicated Repair35 prelock:

- run:
  `35782081114`;
- job:
  `106929790398`;
- conclusion:
  `success`.

## Bound contract

Repair35 preregistration:

- commit:
  `17464d784fd35ef8bd6d67d4f0c6da660c20ff9a`;
- blob:
  `77779a3e1fefa2847c47a3afe8000d5434377ed1`.

Repair35 implementation:

- final prelock implementation commit:
  `f02508170615c32be171fa4dc4121a6b4f6c9ce6`;
- blob:
  `41e2907772dd53eb43d41e390bb616b270921cfa`.

Repair35 implementation lock:

- commit:
  `af2e3ed0e7ecf5baa01bb925536116fc379d3dbb`;
- blob:
  `d64d80cfa1d0c1300f0f878a71f43ee8aa7136f3`.

Repair34 valid FAIL localization:

- commit:
  `8bab319dccd212ed6a92f4e0f448e46b84eed5c8`;
- blob:
  `f985d45ebc983b56697eb0a3bb37c8b71333339b`.

## Execution rule

The first Repair35 invocation that emits a valid Repair35 JSON is frozen as
PASS or FAIL.

Implementation/execution failures before a valid science JSON may be repaired
without changing the frozen Repair35 contract.

Repair35 does not relabel Repair34.
