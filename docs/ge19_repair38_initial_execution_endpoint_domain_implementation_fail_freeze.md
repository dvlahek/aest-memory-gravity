# GE19 Repair38 initial execution — endpoint-domain implementation failure freeze

## Status

The first local Repair38 attempt failed before any valid Repair38 diagnostic
JSON was emitted.

This is an implementation/execution failure only. It is not a Repair38
diagnostic result and it does not change any Repair37 or Z21 classification.

Terminal classification printed to the FULL log:

`GE19_REPAIR38_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION_IMPLEMENTATION_FAIL`.

Error:

`RuntimeError('nonfinite rho_lambda at canonical stage')`.

Traceback localization:

- `radau2_integrate_substepped`;
- second Radau stage `x2`;
- Repair11 `local_with_lambda`;
- frozen `PchipInterpolator(..., extrapolate=False)` for `rho_lambda`.

Frozen FULL log:

- SHA-256:
  `9f07880a9a86e8d9be05407efd3f0f44d0e076be566f69bb915fa516a8f553f2`;
- bytes:
  `1621`.

Terminal marker:

`GE19_REPAIR38_IMPLEMENTATION_OR_EXECUTION_FAILURE`.

Exit code:

`1`.

## Cause

Frozen Repair07 deliberately evaluates the Radau c2=1 stage as

`x2 = x[i+1]`

with the explicit invariant

`c2=1 exactly: stay on interpolation domain`.

The first Repair38 substepping implementation instead used

`x2 = xl + h`.

After interval subdivision, floating-point addition can place the final
internal c2 stage a few ULPs above the parent right endpoint. Since the
frozen Repair11 Lambda interpolator uses `extrapolate=False`, such an
out-of-domain coordinate returns NaN and triggers the reported runtime
error.

This is a coordinate-evaluation implementation defect. It is unrelated to
the H4 equation, source, projected boundary, shift threshold or Repair37
science result.

## Licensed repair

The frozen Repair38 preregistration explicitly permits repair of an
implementation/reproduction failure without changing the diagnostic
contract.

The only licensed change is to bind every internal substep to its parent
interval and set the c2 stage to the explicit substep right endpoint. The
final internal substep must use the exact frozen parent endpoint
`x[i+1]`.

No science source, threshold, diagnostic route or physical equation may
change.

## Classification boundary

Repair37 remains historical valid FAIL.

Repair38 has not yet produced a valid diagnostic result.

Z21 remains uncertified and lensing remains blocked.
