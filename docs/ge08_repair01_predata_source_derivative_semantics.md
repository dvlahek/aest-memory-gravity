# GE08 Repair01 predata — source-callback derivative semantics

## Status

Result-informed implementation repair preregistration after the frozen first GE08 FAIL.

Historical parent classification remains:

`GE08_FULL_FIRST_ORDER_STATE_BRIDGE_FAIL`.

Parent result freeze:

`docs/ge08_full_first_order_state_bridge_result_freeze.md`.

## Narrow diagnosis

The two failed parent gates used the `dy` argument supplied to
`perturbations_sources()` as if it were a freshly evaluated physical RHS at
the accepted source state.

Pinned CLASS NDF15 does not guarantee that semantics.

When a requested source time is crossed by an integration step, NDF15 calls

`interp_from_dif(..., yinterp, ypinterp, yppinterp, ...)`

and passes

`output(t_vec[next], yinterp+1, ypinterp+1, ...)`.

Thus the callback `dy` is the derivative of the NDF interpolation polynomial
at interpolated source nodes, not a new call to `perturbations_derivs()` at
`yinterp`.

The parent numerical gates

- `dy(phi) == phi_prime_from_Einstein`;
- `dy(alpha) == a(E-psi)`

were therefore not valid `1e-12` source-callback invariants.

## Frozen Repair01 scope

Repair01 changes only how these two derivative identities are certified.

It does not change:

- the physical model;
- CLASS commit;
- AeST patch chain;
- accepted source-grid trace location;
- traced state fields;
- Newtonian-to-longitudinal dictionary;
- `chi` reconstruction;
- native `delta_m` closure;
- k or tau gates;
- redshift window;
- exact matter-completeness threshold;
- any evolution or source equation.

## Replacement derivative-semantic gates

The invalid numerical `dy` equality gates are replaced by source-code identity
gates on the pinned, patched runtime.

### Phi identity

Pinned CLASS `perturbations_derivs()` must contain exactly the Newtonian-gauge
RHS assignment

`dy[pv->index_pt_phi] = pvecmetric[ppw->index_mt_phi_prime];`.

### AeST alpha identity

The validated v0.19 AeST patch must contain exactly

`dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);`.

### NDF15 callback-semantics identity

Pinned `tools/evolver_ndf15.c` must contain the interpolated-source path

`interp_from_dif(... yinterp, ypinterp, yppinterp ...)`

followed by the source callback with

`output(... yinterp+1, ypinterp+1 ...)`.

This gate demonstrates that numerical equality of callback `dy` with a fresh
RHS is not required at interpolated accepted source nodes.

## Parent state gates retained unchanged

Require exactly as before:

- legacy/full trace row counts equal;
- legacy/full k-tau grid abs-or-rel error <= `1e-12`;
- reconstructed chi versus historical trace <= `1e-12`;
- traced native `delta_m` versus CLASS source <= `1e-12`;
- requested k miss <= `1e-12`;
- native tau mismatch <= `1e-12`;
- at least eight accepted times in `0.2<=z<=1.5`;
- all traced and derived quantities finite.

The historical numerical callback-`dy` mismatches remain reported
descriptively and are not deleted.

## Matter completeness remains frozen

After subtracting the exact frozen AeST effective-dark scalar stress, require

`||delta p_std||/||delta rho_std|| <= 1e-12`

and

`||shear_std||/||delta rho_std|| <= 1e-12`

for exact single-pressureless-fluid H3 readiness.

No tolerance relaxation is allowed.

## Terminal classifications

All repaired bridge gates pass and the exact pressureless-matter condition also
passes:

`GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_H3_READY`.

Bridge gates pass but exact pressureless-matter readiness fails:

`GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_PASS_MATTER_INCOMPLETE`.

Any repaired bridge gate fails:

`GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_FAIL`.

## Claim boundary

Even an H3_READY classification certifies only the basic first-order state
dictionary, not the complete GE06 local first-order jet.

A later separately preregistered jet-completion step is still required before a
true `Q(Z10,Z10)` construction unless every GE06 local input has already been
certified.

No Repair01 result itself solves `Z20` or `Z21`.
