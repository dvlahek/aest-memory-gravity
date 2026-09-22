# GE19 Repair30 first local execution — implementation failure freeze

## Status

The first local Repair30 attempt did not reach a valid science result.

Terminal runner classification:

`GE19_REPAIR30_IMPLEMENTATION_OR_EXECUTION_FAILURE`.

Inner exception classification:

`GE19_REPAIR30_IMPLEMENTATION_FAIL`.

No Repair30 science JSON was emitted.

Therefore the frozen Repair30 stop rule permits an implementation-only repair and a first science execution afterward.

## Successful pre-science checks

The local runner reached and passed:

- `GE19_REPAIR30_LOCK_PASS`;
- `GE19_REPAIR30_LOCAL_PREEXECUTION_AUDIT_PASS`;
- `GE19_REPAIR30_LOCAL_PARENTS_PASS`;
- `GE19_REPAIR30_R2_REFERENCE_PASS`.

Thus repository locking, parent hashes, virtual-environment execution and the lean R2 reference provenance all closed before the failure.

## Failure

Python exception:

`KeyError('rho_dark')`.

Trace location:

`integrate_dust_tangent()`

at the attempted access

`base_bg["rho_dark"]`.

The frozen GE15 helper

`build_ge15_reference()`

returns

`(bg, state, jets)`.

Its `bg` dictionary contains homogeneous/reduced-operator quantities such as

- x;
- a;
- H;
- Q;
- Q_action;
- KQ_action;
- KQQ_action;
- Z_action.

The CLASS dark-fluid fields

- `rho_dark`;
- `p_dark`;
- `cad2_dark`;

live in the returned per-mode `state` dictionaries.

Repair30 discarded that second return object and incorrectly attempted to read `rho_dark` and `p_dark` from `bg`.

## Local log provenance

Outer/inner Repair30 FULL log supplied by the first local attempt:

- SHA-256:
  `26ceafe673b6073704b9411a08ffe3d48e61d2258b4448e5376f3efa6ec1f1b9`;
- bytes:
  `779`.

Runner exit:

`1`.

## Repair boundary

The allowed implementation repair is only:

1. retain the already returned GE15 per-mode state object from `build_ge15_reference()`;
2. pass that frozen state object into `integrate_dust_tangent()`;
3. form the already preregistered standard-sector tangent as
   `total_delta_rho_eta-rho_dark*delta_dark_eta`
   and
   `total_rho_plus_p_theta_eta-(rho_dark+p_dark)*theta_dark_eta`
   using the per-mode frozen `rho_dark,p_dark` arrays.

No scientific formula changes.

No source sign changes.

No boundary changes.

No grid changes.

No threshold changes.

No Repair29B parent changes.

No H4/Z21 execution.

The failed attempt is implementation-only and is not a Repair30 PASS or FAIL science result.
