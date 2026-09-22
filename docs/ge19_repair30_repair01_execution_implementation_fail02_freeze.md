# GE19 Repair30 Repair01 local execution — implementation failure 02 freeze

## Status

The Repair30 Repair01 local execution again stopped before producing a valid
Repair30 science JSON.

Terminal runner classification:

`GE19_REPAIR30_IMPLEMENTATION_OR_EXECUTION_FAILURE`.

Inner classification:

`GE19_REPAIR30_IMPLEMENTATION_FAIL`.

Therefore Repair30 science remains unconsumed and the original preregistered
science contract remains active.

## Successful pre-science checks

The repaired runner passed:

- `GE19_REPAIR30_LOCK_PASS`;
- `GE19_REPAIR30_LOCAL_PREEXECUTION_AUDIT_PASS`;
- `GE19_REPAIR30_LOCAL_PARENTS_PASS`;
- `GE19_REPAIR30_R2_REFERENCE_PASS`.

## Failure

Exception:

`TypeError('only 0-dimensional arrays can be converted to Python scalars')`.

Failure location:

`integrate_dust_tangent()`

at

`d0=float(std_dr[ik,0]/rho0)`.

The repaired GE15 state plumbing correctly produced per-mode background arrays

- `rho_dark.shape == (6,nt)`;
- `p_dark.shape == (6,nt)`.

The Repair29B tangent arrays also have mode/time shape

`(6,nt)`.

However Repair30 incorrectly formed

`rho_dark[None,:] * delta_dark_eta`

and

`(rho_dark+p_dark)[None,:] * theta_dark_eta`.

The inserted singleton dimension changed the standard-sector tangent from
the intended shape `(6,nt)` to `(1,6,nt)`. Consequently
`std_dr[ik,0]` was a time vector instead of a scalar.

The already frozen Repair28 tangent implementation uses the correct
elementwise identities without the singleton axis:

`std_dr = tan["total_delta_rho"] - rho*tan["delta_dark"]`

and

`std_mom = tan["total_rho_plus_p_theta"] - (rho+p)*tan["theta_dark"]`.

## Local log provenance

FULL log from the Repair01 attempt:

- SHA-256:
  `c378946c5cfab4446bd6faefcf56508bb9fe42ec232ca87920964887242c1f6c`;
- bytes:
  `864`.

Runner exit:

`1`.

## Allowed Repair02 implementation repair

Only remove the two erroneous singleton-axis insertions:

- `rho_dark[None,:]` -> `rho_dark`;
- `(rho_dark+p_dark)[None,:]` -> `(rho_dark+p_dark)`.

No equation changes.

No source changes.

No boundary changes.

No grids or thresholds change.

No parent changes.

No H4/Z21 execution.

This attempt is implementation-only and is not a Repair30 scientific PASS
or FAIL result.
