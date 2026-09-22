# GE19 Repair34 local canonical H4/Z21 runner — lock

## Status

The first local Repair34 science execution path is frozen.

Runner:

`ge19/run_local_repair34_canonical_h4_z21_particular.sh`.

Blob:

`24ee474c51e635bc4ec00eb81de67c675ff05fb4`.

Commit:

`7ddb1c4b28db41032b330571888df13ea0823c5d`.

Global static audit:

- run:
  `35779076226`;
- conclusion:
  `success`.

Dedicated Repair34 prelock:

- run:
  `35778912256`;
- conclusion:
  `success`.

## Bound contract

Repair34 preregistration:

- commit:
  `701dce93ad30303b368de840955368027edd1271`;
- blob:
  `5653c99b4fc20fd4ccc286ac0aed6c54a8411185`.

Repair34 implementation:

- commit:
  `7740a1479e7499ff25e8d8dc006279cd061e76f9`;
- blob:
  `f2171a630c2e41055dd966e6dd3ab39cb7839e3b`.

Repair34 implementation lock:

- commit:
  `f5f828f5dbdae9a758de72e077ee2eeffe6cb8e4`;
- blob:
  `2fa57387357d1d25936051b7632c266e9749c1b2`.

Repair33 FAIL localization:

- commit:
  `34c7747f12e06b49aa660c4251409d593702f339`;
- blob:
  `434309199eb58901aa1c0ad6e3f96a6656d72389`.

## Execution rule

The first Repair34 invocation that emits a valid Repair34 JSON is frozen as
PASS or FAIL.

Implementation/execution failures before a valid science JSON may be repaired
without changing the frozen contract.

Repair34 does not relabel Repair33.
