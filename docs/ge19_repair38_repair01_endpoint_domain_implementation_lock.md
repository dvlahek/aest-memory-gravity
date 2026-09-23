# GE19 Repair38 repair01 endpoint-domain implementation lock

## Status

Repair38 repair01 is frozen before the next local diagnostic execution.

The original Repair38 preregistration is unchanged. This repair changes only
the internal Radau substep coordinate evaluation needed to preserve the
frozen interpolation domain.

The first Repair38 attempt remains an implementation failure and is not
relabelled.

## Initial implementation failure

Freeze file:

`docs/ge19_repair38_initial_execution_endpoint_domain_implementation_fail_freeze.md`.

Freeze blob:

`714937146e55f70088e0d81cdcf4d035eab4f69c`.

Frozen FULL log:

- SHA-256:
  `9f07880a9a86e8d9be05407efd3f0f44d0e076be566f69bb915fa516a8f553f2`;
- bytes:
  `1621`.

Error:

`RuntimeError('nonfinite rho_lambda at canonical stage')`.

No valid Repair38 diagnostic JSON was emitted.

## Frozen preregistration

File:

`ge19/repair38_predata_frozen_source_radau_substep_localization.json`.

Final preregistration commit:

`a3c5ac84c7a0769f91f26fd3ead17445549bc964`.

Blob:

`41a2925cf4f705c4bf8418cbcc2cee48af4a673d`.

No preregistered threshold, route, physical equation or diagnostic condition
is changed by repair01.

## Repaired implementation

File:

`ge19/repair38_frozen_source_radau_substep_localization.py`.

Repair commit:

`6915d67dfbe4b86940266a72c7e6141bc95e82c2`.

Repaired blob:

`fbab2cd31cfcb69c21c3e066e6d8d17844369d32`.

The only implementation change is the c2=1 stage-coordinate construction.

Original defective form:

`x2 = xl + h`.

Repaired form:

- each internal substep is explicitly bound to a left endpoint `xl` and a
  right endpoint `xr`;
- the final internal substep uses exactly `xr = x[i+1]`;
- the c2 stage is exactly `x2 = xr`;
- the c1 stage is computed inside that explicit subinterval.

This restores the frozen Repair07 invariant:

`c2=1 exactly: stay on interpolation domain`.

No source array, operator coefficient, Radau tableau, projected boundary,
constraint metric or threshold is changed.

## Audits

Static audit after the repaired implementation:

- run:
  `35858061270`;
- conclusion:
  `success`.

Updated dedicated Repair38 prelock workflow:

- workflow commit:
  `cf65f82b4a564228d0bb9389f6def038b104a43c`;
- workflow blob:
  `38f4afee0384f4f5b3de870e4adc2c1187442137`;
- run:
  `35858136063`;
- job:
  `107171486168`;
- conclusion:
  `success`.

The updated prelock explicitly verifies that:

- `x2=float(xl+c2*h)` is absent;
- the final internal substep uses `float(x[i+1])`;
- `x2=xr`;
- the original Repair38 frozen-source/threshold/route contract remains
  unchanged.

## Execution boundary

The next local attempt is still the first opportunity to obtain a valid
Repair38 diagnostic result.

If factor-1 reproduction fails, that is still an implementation/reproduction
failure and may be repaired without changing the preregistered diagnostic
contract.

If a valid diagnostic JSON is emitted, it must be frozen exactly as emitted.

Repair38 itself cannot certify Z21 or license lensing.
