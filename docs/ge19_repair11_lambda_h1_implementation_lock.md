# GE19 Repair11 Lambda-inclusive reduced-H1 implementation lock

## Status

**IMPLEMENTATION LOCKED BEFORE REPAIR11 LOCAL SCIENCE EXECUTION**

Repair10 remains frozen as a diagnostic result. Repair06/Repair07 remain historical FAIL results and are not relabeled.

## Parent Repair10 result freeze

Commit:

`b66e780b9d3b5f119ef4deafa0cd2e82d5333580`

File:

`docs/ge19_repair10_reduced_background_vacuum_onshell_result_freeze.md`

Blob:

`b24435a4c6233ab383a544a0bf231fa0e6db9c19`

Frozen Repair10 science JSON:

- SHA-256 `0903363695f071e635f91875903893041bfe728d9ff6c85b424604b933c8baa5`;
- bytes `5335`.

Frozen Repair10 routing:

`OMITTED_LAMBDA_DOMINANT_OFFSHELL_MECHANISM`.

## Repair11 preregistration

Commit:

`6eee56fb6764926117d1a0b93705d4ba3acc617d`

File:

`ge19/repair11_predata_lambda_inclusive_reduced_h1_reclosure.json`

Blob:

`1487b99fa3ab403134fe19a073d35c32279ea813`

## Repair11 implementation

Commit:

`03b428155f06ed7764ca520acb80fd1d63e13d95`

File:

`ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py`

Blob:

`dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7`

Repair11 augments only the frozen Repair07 local first-order canonical matrix by the exact first directional coefficients of

`L_lambda = -6 rho_lambda N L R^2`.

The frozen `rho_lambda` is interpolated from the same GE15 CLASS background table.

## Exact first-directional Lambda coefficients

In gauge `L=R=S`:

- lapse:
  `delta E_N^lambda = -18 rho_lambda a^2 S`;
- isotropic metric:
  `delta(E_L+E_R)^lambda = -18 rho_lambda a^2 N - 36 rho_lambda a S`;
- anisotropy:
  `delta(E_L-0.5 E_R)^lambda = 0`;
- shift:
  `0`;
- aether, scalar, dust-potential, dust-density:
  `0`.

No other first-order operator entry is changed.

## Final executable prelock audit

Workflow:

`.github/workflows/ge19-repair11-prelock-audit.yml`

Final workflow commit:

`60f99e4f92acd1e718440e9edc5e36e1977bc33a`

Workflow blob:

`ffb633e67eda142cf1dce882d65dfeb1baaa62e5`

GitHub Actions run:

`35568313478`

Job:

`106234453709`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR11_PRELOCK_AUDIT_PASS`

The successful symbolic audit independently derived:

- `LAMBDA_EN_C1 = -18*S*a**2*rho`;
- `LAMBDA_ISO_C1 = -36*S*a*rho - 18*a**2*dN*rho`;
- `LAMBDA_ANISO_C1 = 0`.

At the fixed numerical probe `a=0.6`, `rho_lambda=3.451969239349119e-8`, the implementation matrix gave:

- `EN_S = -2.2368760670982289e-7`;
- `ISO_N = -2.2368760670982289e-7`;
- `ISO_S = -7.456253556994097e-7`.

All other Lambda matrix entries were exactly zero in the audit.

The earlier failed prelock run `35567644113` was an audit-code error only: it attempted a SymPy derivative with respect to an already-expanded expression. No Repair11 science implementation was changed by that failure. The corrected audit removed only that dead audit line.

## Frozen Stage-A experiment

Repair11 repeats only the mandatory reduced-H1 Stage A on:

- Nt=64 primary;
- Nt=32 control;
- `C_min,C_star,C_max`;
- the same six frozen input modes;
- the same GE15/GE18 initial dynamic values and cosmic-time derivatives.

The canonical/Noether partition, stable-Z implementation, Radau-IIA scheme, constraint metrics and pressureless-dust sector are unchanged.

## Unchanged Stage-A gates

- linear-system/canonical residual <= `1e-8`;
- shift constraint backward error <= `1e-6`;
- anisotropy constraint backward error <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- initial dynamic match abs-or-rel <= `1e-10`;
- all outputs finite.

No threshold is relaxed.

## Stop rule

Repair11 does not construct H3/Z20.

If Stage A fails, the failing gate is frozen and localized before any further change.

If Stage A passes, a separate preregistered repair is required to add the exact second directional Lambda metric source before H3/Z20 can be attempted.

## Claim boundary

A Repair11 PASS certifies only Lambda-inclusive reduced-H1 closure on the frozen window and reduced-matter setup.

It does not certify H3/Z20, finite eta, finite physical-amplitude nonlinear evolution, collapse, lensing or observational detection.
