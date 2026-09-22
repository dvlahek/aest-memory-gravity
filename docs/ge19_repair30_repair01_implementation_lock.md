# GE19 Repair30 Repair01 — implementation repair lock

## Status

This lock records the only implementation repair permitted after the first local Repair30 attempt stopped before producing a valid science JSON.

The original Repair30 science preregistration, equations, inputs, grids, boundary rule and thresholds are unchanged.

## Frozen failure parent

Implementation-failure freeze:

- file:
  `docs/ge19_repair30_initial_execution_implementation_fail_freeze.md`;
- blob:
  `4e803520f73c97272a3f35ff62b017021908dc1d`;
- commit:
  `0939742f9c518818091bed8a84465b2148c73153`.

Failure:

`KeyError('rho_dark')`.

The failure occurred before any valid Repair30 science JSON existed.

## Repair01 code change

Original implementation:

- commit:
  `91e59269dbfd4476230cf8cc25c5579b44691b8d`;
- blob:
  `2ce2bf7ccd5bf48504c619500d12d4eb03bfe259`.

Repaired implementation:

- commit:
  `37d8b6f1e2e5980f1f423c014b6a6b60157f78bd`;
- blob:
  `a014dd3a56914858cb6ca7e0f5bdd45afdf573db`.

The sole change is dictionary plumbing:

- retain the second return value `state` from
  `build_ge15_reference()`;
- read `rho_dark` and `p_dark` from those frozen per-mode state dictionaries;
- pass those arrays into the already preregistered standard-sector tangent construction.

No formula is changed.

Specifically, the frozen standard-sector identities remain

`delta_rho_std_11 = total_delta_rho_eta - rho_dark delta_dark_eta`

and

`momentum_std_11 = total_rho_plus_p_theta_eta - (rho_dark+p_dark) theta_dark_eta`.

## Repair01 dedicated prelock

Workflow:

`.github/workflows/ge19-repair30-repair01-prelock-audit.yml`.

Blob:

`4cad3fee8bc4574cbf0aec8dcbd31944b877c5d5`.

Workflow commit:

`dc6774329b53531fc0b90f66c3d60916ad05e9d8`.

Run:

`35749669679`.

Job:

`106820207030`.

Conclusion:

`success`.

The dedicated Repair01 prelock verifies:

- original Repair30 preregistration blob remains exact;
- repaired implementation blob is exact;
- frozen implementation-failure document is exact;
- all science thresholds are unchanged;
- `L_total Z11=-M1[Z10,q10]` is unchanged;
- `B10=X10-weighted_z10` is unchanged;
- exact symbolic GE05 M1 identities still pass;
- H2 aether/scalar source signs are unchanged;
- no H4/Z21 solve is present.

The historical original Repair30 prelock remains tied to the original implementation blob and therefore fails on the repaired blob by design. That historical prelock is not relabelled.

## Science status

Repair30 science has still not run successfully.

There is no valid Repair30 PASS/FAIL JSON yet.

Therefore the next local invocation after the runner is rebound to this repaired blob remains the first valid Repair30 science attempt under the original preregistered contract.
