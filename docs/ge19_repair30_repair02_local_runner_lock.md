# GE19 Repair30 Repair02 local runner — lock

## Status

The local Repair30 runner is rebound to the Repair02 shape-repaired
implementation. No valid Repair30 science JSON exists yet.

## Runner

File:

`ge19/run_local_repair30_reduced_h2_z11_reclosure.sh`.

Blob:

`fa850322f349f3df45a5a9922dff5747d913222a`.

Runner commit:

`fb34aec2ba164307448014d980ebd1c28c5294f9`.

Static audit:

- run:
  `35751078203`;
- job:
  `106825067675`;
- conclusion:
  `success`.

## Bound Repair02 implementation

Science implementation blob:

`e32631bceb4ceb11037eef70b8a47b5f7622faff`.

Repair02 implementation commit:

`fc1f12f68df99e0e5cd7bc2e76090bf36a84e2f5`.

Dedicated Repair02 shape prelock:

- run:
  `35750958907`;
- job:
  `106824641242`;
- conclusion:
  `success`.

The prelock inspected the actual frozen R2 NPZ and confirmed all relevant
arrays have the expected mode/time shape `(6,128)`.

## Integrity

The original Repair30 science contract is unchanged.

The only Repair02 repair removes an erroneous singleton broadcast dimension
and adds shape guards. No source formula, boundary, grid, threshold or parent
changes are present.

The next local invocation remains the first valid Repair30 science attempt.
