# GE19 Repair13 self-consistent reduced-background H1 implementation lock

## Status

**IMPLEMENTATION LOCKED BEFORE REPAIR13 LOCAL SCIENCE EXECUTION**

Repair12 remains frozen as a diagnostic result with route

`BACKGROUND_OR_REDUCED_DYNAMICS_REMAIN`.

Repair11 remains a historical Stage-A FAIL and is not relabeled.

## Parent Repair12 freeze

Commit:

`8d27fe6cba7ce3e00f8b6714a22dc9d47de24c6a`

File:

`docs/ge19_repair12_standard_momentum_result_freeze.md`

Blob:

`7705cd781a7eed33d0c1a07354c97faebc624620`

Frozen Repair12 JSON:

- SHA-256 `e442e37dab7df97f890cc2b210d34446a204437650226f82a4887e1e2d0dc270`
- bytes `66404`.

## Repair13 preregistration

Commit:

`3a7e6931c4ba18cfe7c5da7221c9b98cb09d6b2f`

File:

`ge19/repair13_predata_self_consistent_reduced_background_h1_reclosure.json`

Blob:

`8e960e80da0b1acee3b1724169f222a4edc7bf1b`

## Repair13 implementation

Commit:

`b4e0fa9a051f28ab8c8413e9b49485d06f740bc5`

File:

`ge19/repair13_self_consistent_reduced_background_h1_reclosure.py`

Blob:

`362d63d03d7b850fceae393f535353ded79aeea7`

Only the homogeneous H(a) background supplied to the already-frozen Repair11 Lambda-inclusive first-order operator is changed.

For each C envelope:

`H_red(a)^2 = (Q K_Q - K)/3 + C/a^3 + rho_lambda`.

The same frozen stable Exp branch is retained:

`a^3 K_Q = I0`.

The same `Q(a)`, `Z(a)`, `K_Q(a)`, `K_QQ(a)`, dust C values and frozen CLASS rho_lambda are retained.

## Exact reduced background identities

The reduced lapse/Friedmann identity is

`3 H_red^2 - (Q K_Q-K) - 3(C/a^3+rho_lambda) = 0`.

Scalar conservation gives

`d K_Q / d ln a = -3 K_Q`

and hence

`d[(Q K_Q-K)/3]/d ln a = -Q K_Q`.

Therefore the reduced scale equation requires exactly

`p_required = -rho_lambda`.

No fitted H correction or empirical residual subtraction is used.

## Executable prelock audit

Workflow:

`.github/workflows/ge19-repair13-prelock-audit.yml`

Blob:

`edac57861eb719638b37516326c5cca56d02ecd4`

GitHub Actions run:

`35590788887`

Job:

`106304460656`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR13_PRELOCK_AUDIT_PASS`

Exact symbolic markers:

- `REDUCED_FRIEDMANN_IDENTITY = 0`;
- `REDUCED_PRESSURE_IDENTITY = -rL`.

Synthetic implementation probe:

- Friedmann relative L2 `4.428590758853519e-17`;
- pressure-identity relative L2 `2.556007674302437e-16`;
- all background values finite;
- H positive.

Static prelock audits also passed for both the preregistration and implementation commits.

## Frozen Stage-A experiment

Repair13 repeats only the mandatory reduced-H1 Stage A using:

- Nt=64 primary and Nt=32 control;
- the same six frozen modes;
- C_min, C_star, C_max;
- the same GE15/GE18 initial dynamic values and cosmic-time derivatives;
- the exact Repair11 first-directional Lambda operator;
- the same canonical/Noether algebraic partition;
- the same Radau-IIA integrator;
- the same shift/anisotropy metrics.

A separate reduced H(a) is used for each C envelope.

## Background gates

- Friedmann relative L2 <= `1e-12`;
- pressure identity relative L2 <= `1e-10`;
- all background values finite;
- H positive.

## Unchanged Stage-A gates

- canonical/linear residual <= `1e-8`;
- shift backward error <= `1e-6`;
- anisotropy backward error <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- initial dynamic match <= `1e-10`;
- all outputs finite.

No threshold is relaxed.

## Stop rule

Repair13 does not construct H3/Z20.

If Stage A passes, the result must be frozen before a separate H3 repair adds the Lambda second-directional metric source on this same reduced background.

If Stage A fails, the failing gate must be frozen and diagnosed without reverting to a full-CLASS post-hoc momentum substitution.

## Claim boundary

A Repair13 PASS certifies only self-consistent reduced-background H1 closure for the frozen window and C envelope.

It does not certify H3/Z20, finite eta, finite physical-amplitude nonlinear evolution, collapse, lensing or observational detection.
