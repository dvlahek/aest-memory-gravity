# GE18 Repair01 native-provenance gate — implementation lock

## Status

Locked before the first GE18 Repair01 execution.

## Parent

Historical parent:

`GE18_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_FAIL`.

Frozen parent result commit:

`971efa7634fe93387c69b463771d801a264dd2cf`.

The parent failed only the mixed 64-node cross-file interpolation gate at

`7.590304690330285e-8 > 1e-8`.

All preregistered dust integrator, initial-match and GE07-map controls passed.

## Repair scope

Repair01 changes only the interpretation of the implementation-added mixed-representation sanity quantity.

The parent compared:

- the frozen GE09/GE15 dense-state Hermite/PCHIP representation; and
- an independently PCHIP-interpolated raw CLASS/background representation

at 64 non-native common nodes.

Because native dense accepted-step trace versus raw CLASS perturbation output already agrees exactly with abs-or-rel maximum `0.0`, the mixed 64-node number is not a valid native provenance gate.

Repair01 therefore retains that number as a diagnostic only.

No threshold is relaxed.

## Frozen unchanged physics and numerics

Unchanged:

- pressureless Newtonian-gauge dust equations;
- `z=1.5` absolute density/momentum matching surface;
- all six frozen k modes;
- 64 common `ln(a)` nodes;
- `C_min,C_star,C_max`;
- GE07 variable map;
- primary DOP853 `rtol=1e-11, atol=1e-13`;
- control DOP853 `rtol=2e-12, atol=2e-14`;
- primary/control density global L2 gate `1e-8`;
- primary/control momentum global L2 gate `1e-8`;
- initial density match gate `1e-10`;
- initial momentum match gate `1e-10`;
- `dot T1=psi` gate `1e-9`;
- finite-output requirement.

No model-error acceptance gate is added.

## Native provenance gates

Require:

- local GE15 classification PASS;
- R1 dense SHA exact match to GE15 result;
- native dense trace versus raw CLASS perturbation abs-or-rel <= `1e-12`;
- requested-k relative miss <= `1e-12`.

## Diagnostic-only quantity

The mixed 64-node cross-interpolation mismatch remains reported under

`mixed_64node_cross_interpolation_diagnostic_abs_or_rel_max`.

Its value does not determine Repair01 PASS/FAIL.

## Preregistration

Commit:

`e8682358a09891a8ca879fc8bf3dc3cbceaea2cd`.

Blob:

`2f5d9f7cd07cde97e1c1747c1bff015006ef2d96`.

## Implementation

Commit:

`53df95fb6198a281fc9c5a568adab2ba2e42c312`.

Blob:

`b469b3c44eb8cf6c2545f80fccce5ad811ba8c33`.

## Terminal classifications

Pass:

`GE18_REPAIR01_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_PASS`.

Fail:

`GE18_REPAIR01_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_FAIL`.

## Historical integrity

Repair01 does not relabel historical GE18.

## Claim boundary

A Repair01 PASS certifies the internally consistent reduced pressureless first-order matter bridge for later reduced-H3 Z20 use. The discrepancy relative to full standard CLASS matter remains an explicit systematic and no full-species second-order solution is claimed.
