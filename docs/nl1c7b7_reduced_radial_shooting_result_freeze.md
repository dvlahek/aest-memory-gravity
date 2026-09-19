# NL1C7B7 — reduced-radial shooting result freeze

## Status

Frozen first locked NL1C7B7 execution.

Terminal classification:

`NL1C7B7_REDUCED_RADIAL_CONSTRUCTION_FAIL`.

Science return code:

`SCIENCE_RC=2`.

Execution HEAD:

`7cc6ccd1dc627d070989b474967c8eb49e77175f`.

The run began with

`NL1C7B7_REDUCED_RADIAL_SHOOTING_LOCK_PASS`.

This is a construction failure before any candidate state was returned to the exact B4 differential science gate.

It is not a B4 differential-certification failure.

## Frozen output hashes

Result JSON:

- bytes: `17638`;
- SHA-256:
  `449201305c535e24e592296f5e2a53e7fc0866b5cae2970a147c2bcebe12bfc6`.

Evaluator log:

- bytes: `18084`;
- SHA-256:
  `2364fda0d150af059a32e3640534c0fb9ee6b5a063676c67fe5639eed2e1d221`.

Full runner log:

- bytes: `22578`;
- SHA-256:
  `05ee332f4e24aafb0493626eb880b894a5f1664a68bcd320dd0801aa9741c206`.

No state NPZ was written.

## Gate result

PASS:

- B7_G1 frozen provenance;
- B7_G2 frozen-field polynomial representation;
- B7_G3 exact reduced-equation implementation;
- B7_G10 output integrity and claim boundary.

FAIL / not reached:

- B7_G4 complete scalar shooting construction;
- B7_G5 center-launch stability;
- B7_G6 asymptotic-background compatibility;
- B7_G7 safety/exact-Q/field freeze;
- B7_G8 original B4 differential exact constraints;
- B7_G9 two-grid correction control.

Thus the failure occurs at the scalar shooting boundary construction, upstream of all returned-state science tests.

## Parent and equation integrity

All six parent H/M values reproduce the frozen Repair16 values exactly.

The local degree-8 frozen-field representation passes on all six scale/grid cases.

The exact reduced-equation audit passes:

- Hamiltonian derivative coefficient matches the B6 result;
- H is affine in `L_r`;
- H is independent of `R_{t,r}`;
- momentum derivative coefficient is exactly `-4LR`;
- M is affine in `L_r`;
- M is independent of algebraic `R_t`;
- j-sector H and M radial fluxes vanish as expected.

Therefore the construction failure is not caused by provenance drift or by loss of the B6 first-order structure.

## Exact shooting failure

Every frozen case and both preregistered center-launch radii fail because the shooting residual

`ell(r_max)`

has the same negative sign at both ends of the frozen bracket

`ell_0 in [-0.5,+0.5]`.

Primary launch `epsilon=1e-5 r_1`:

- scale 5, Nr=256:
  `[-3.2730045646915904e-6, -3.2406576625335762e-6]`;
- scale 5, Nr=512:
  `[-3.3304901041220602e-6, -3.3022571860338936e-6]`;
- scale 10, Nr=256:
  `[-1.9455358815977506e-6, -1.8914177902436547e-6]`;
- scale 10, Nr=512:
  `[-2.2315262505921945e-6, -2.220733965973643e-6]`;
- scale 20, Nr=256:
  `[-1.8435310571142648e-5, -1.844389955685603e-5]`;
- scale 20, Nr=512:
  `[-1.8038154538780602e-5, -1.797874195208241e-5]`.

Control launch `epsilon=1e-4 r_1` shows the same no-sign-change outcome in all six cases.

The shooting response is also extremely weak across an order-unity change in `ell_0`.

No bracket expansion is licensed.

## Post-result analytic interpretation

The B7 preregistration treated `L(0)` as the one remaining shooting integration constant after imposing regular `R_t(0)=0`.

The exact center Hamiltonian structure shows that this is not the correct regular-center degree-of-freedom count.

At a regular spherical center:

- `R(0)=0`;
- `R_r(0)` is finite and positive;
- `L(0)>0`;
- `L_r(0)=0`;
- all regular non-GR Hamiltonian matter/aether terms carry at least `R^2` and vanish at the center.

The GR curvature part of the exact Hamiltonian at the center reduces to

`H(0)=2L_0-2R_r(0)^2/L_0`.

Therefore exact regularity plus `H(0)=0` gives

`L_0^2=R_r(0)^2`.

With positive radial metric coefficient,

`L(0)=R_r(0)`.

Thus `L(0)` is fixed algebraically by the regular-center constraint and is not a free shooting parameter.

The frozen B7 scalar shooting formulation is therefore not the natural regular-center formulation of the singular first-order system.

The weak dependence of the outer residual on the imposed trial `ell_0` is consistent with rapid attraction toward the unique regular branch, but this observation is descriptive and is not used to relabel the B7 result.

## Project decision boundary

The B7 result remains frozen as

`NL1C7B7_REDUCED_RADIAL_CONSTRUCTION_FAIL`.

Do not:

- expand the B7 shooting bracket;
- change Brent tolerances;
- change DOP853 tolerances;
- choose a second shooting parameter;
- fit the outer `R_t`;
- reinterpret B7 as a differential-constraint failure.

No B7a/B7b repair sequence is licensed.

The next scientifically distinct representation may impose the exact center algebraic condition

`L(0)=R_r(0)`

together with regular

`R_t(0)=0`

and the analytic center slope

`R_{t,r}(0)=L_t(0)R_r(0)/L(0)=L_t(0)`.

This leaves no free shooting parameter.

A separately preregistered regular-center IVP may then integrate the exact B6 first-order system outward and treat both outer `L` and outer `R_t` background compatibility as predictions.

Any such state must still pass the unchanged original B4 differential threshold `1e-7` on both grids before evolution is licensed.
