# GE08 Repair01 source-derivative semantics — implementation lock

## Status

Implementation locked before the first Repair01 execution.

Historical parent result remains:

`GE08_FULL_FIRST_ORDER_STATE_BRIDGE_FAIL`.

## Repair01 preregistration

Commit:

`0bdcaf65e65de48cb099d428123984c7074f0e4a`.

File:

`docs/ge08_repair01_predata_source_derivative_semantics.md`.

Frozen blob:

`4562cb507f76fb99c58ef5c3e537c3af4e3d571a`.

## Frozen diagnostic trace patch

Unchanged from parent GE08:

`ge08/apply_full_state_trace_patch.py`.

Frozen blob:

`20a3afe24a73b3512c5b5ea639466b8ca9bc3b8c`.

No traced field or trace location changes.

## Repair01 audit implementation

Commit:

`5834ea8168c35db19170b00a1e124454e1aefb1b`.

File:

`ge08/repair01_full_first_order_state_bridge.py`.

Frozen blob:

`8e7fe47d5fa7adc0e67a899aa4d62dcba7fe350a`.

## Frozen physics/runtime

Unchanged:

- CLASS commit `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- `KB=0.0665`;
- `eta=0`;
- `tau H0=10`;
- Newtonian gauge;
- validated v0.19/v0.23/v0.72 patch chain;
- six frozen k values;
- `0.2<=z<=1.5`;
- exact matter-completeness limit `1e-12`.

## Repair-only semantic gates

Pinned patched `perturbations.c` must contain

`dy[pv->index_pt_phi] = pvecmetric[ppw->index_mt_phi_prime];`

and

`dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);`.

Pinned NDF15 must contain both:

- interpolation of `yinterp,ypinterp,yppinterp`;
- source callback with `yinterp+1,ypinterp+1`.

The parent numerical callback-`dy` mismatches remain reported descriptively.

## Parent state gates retained

No threshold changes:

- trace count equality;
- source-grid identity <= `1e-12`;
- chi closure <= `1e-12`;
- native delta_m closure <= `1e-12`;
- k and tau closure <= `1e-12`;
- at least 8 native times;
- finite values.

## Matter completeness retained

No tolerance change:

- standard pressure / density <= `1e-12`;
- standard shear / density <= `1e-12`.

## Terminal classes

- `GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_H3_READY`;
- `GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_PASS_MATTER_INCOMPLETE`;
- `GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_FAIL`.

## Project boundary

Repair01 can certify the **basic first-order state dictionary** only.

Even an H3_READY result does not certify the complete GE06 local jet.

Therefore Repair01 alone never licenses a `Z20` solve.
