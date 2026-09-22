# GE19 Repair34 canonical H4/Z21 — first valid result FAIL freeze and localization

## Frozen result

Classification:

`GE19_REPAIR34_CANONICAL_WINDOW_LOCAL_REDUCED_H4_Z21_PARTICULAR_FAIL`.

Terminal route:

`GE19_REPAIR34_VALID_SCIENCE_FAIL_FREEZE_REQUIRED`.

Repair34 is frozen exactly as emitted and is not relabelled.

## Frozen local artifacts

Science JSON:

- SHA-256:
  `5d6fd3b90e4980e2397058f6785f15b156e4a3826b5b21b614f2fea3acee03d8`;
- bytes:
  `457793`.

Science NPZ:

- SHA-256:
  `8e6f7f2b02b48ee5c956822a09a591fa32237cd0c5865a7dfb838996d08824ed`;
- bytes:
  `25135821`.

Inner FULL log:

- SHA-256:
  `5d6fd3b90e4980e2397058f6785f15b156e4a3826b5b21b614f2fea3acee03d8`;
- bytes:
  `457793`.

The JSON and inner FULL log are byte-identical.

Outer local runner log:

- SHA-256:
  `bddfb28c1f590593c9d14c4e9148912fcf8d3bbf12a17055d3de7396fd71bfee`;
- bytes:
  `779223`.

## What Repair34 fixed successfully

The canonical H3-matched propagation path works.

Frozen Repair34 controls:

- canonical Radau/algebraic linear residual:
  `2.1230308479303956e-13`;
- H4 state Nt128/Nt64 global relative L2:
  `3.792872969929106e-05`;
- anisotropy backward error:
  `2.7171159875532174e-16`;
- boundary q0:
  `0.0`;
- boundary projected-momentum scaled residual:
  `2.784080369027546e-16`;
- boundary lapse backward error:
  `2.7840782933623786e-16`;
- boundary shift backward error:
  `3.657522292813954e-16`;
- boundary algebraic residual:
  `2.124296542730337e-16`;
- all outputs finite.

Thus the Repair33 global sparse-BVP defect is closed.

## Source convergence also remains good

- DY2 Nx1024/Nx2048:
  `2.9384475883958845e-05`;
- total H4 source Nx1024/Nx2048:
  `4.726941943867389e-17`;
- memory source Nq1024/Nq2048:
  `1.0712218077978013e-06`;
- total H4 source Nt128/Nt64:
  `1.8704084900397904e-04`.

## Two failed gates

Only two Repair34 gates fail:

1. balanced Q-cross polarization self-consistency:
   `1.3937144320141648e-09 > 1e-12`;
2. propagated shift constraint backward error:
   `1.9331075076102835 > 1e-6`.

All other science gates pass.

## Localization A — Repair34 repeated a known invalid all-row shift audit

Repair34 used the raw maximum

`odiag["shift_constraint_relative_L2_max"]`

from the Repair07 canonical reconstruction as the H4 shift gate.

This takes a relative backward-error ratio on every shift row, including rows
whose natural shift scale is at or below floating-point resolution.

That exact all-row interpretation was already rejected by the frozen
Repair21/Repair22 H3 certification chain.

Repair21 established the frozen rule:

- define
  `S_ref = max shift scale`
  on the Nt128 on-shell solution;
- define a near-null row by
  `scale <= sqrt(eps) S_ref`;
- on active rows, gate the unchanged relative shift backward error at
  `1e-6`;
- on near-null rows, gate the absolute residual through
  `max |residual| / S_ref <= 1000 eps`;
- compare Nt64 and Nt128 active metrics on the common Nt128 grid and require
  the expected Radau convergence order.

This was not a threshold relaxation. It was the certified
machine-level interpretation of structurally near-zero shift rows.

Repair22 explicitly inherited that rule.

Repair34 accidentally reverted to the pre-Repair21 all-row maximum and
therefore its propagated shift gate is implementation-confounded.

The pattern in Repair34 is consistent with the same issue: the canonical
linear residual is machine-level while individual all-row shift ratios jump
from about `6e-3` to order unity, even though the initial projected shift
boundary is about `1e-16` and anisotropy remains about `1e-16`.

## Localization B — balanced floating polarization is still cancellation limited

Repair34 improved the Q-cross polarization by norm-balancing Z10 and Z11
before evaluating

`[Q2(A+mu B)-Q2(A-mu B)]/(4 mu)`.

The discrepancy dropped from the Repair33 level
`3.683354016827578e-08`
to
`1.3937144320141648e-09`,
but it still cannot satisfy the exact `1e-12` audit because the operation
still subtracts two floating evaluations of a large quadratic source.

GE06 and GE07 already expose the exact symbolic second-direction coefficient
expressions. Since those expressions are homogeneous quadratic polynomials in
the directional variables, the mixed bilinear coefficient can be evaluated
directly as

`B(d,e) = (1/2) sum_i (partial Q2(d)/partial d_i) e_i`.

This identity is exactly equal symbolically to the polarization formula and
avoids subtractive cancellation.

A follow-up must certify the exact symbolic identity before execution and
must retain a numerical symmetry audit
`B(Z10,Z11)=B(Z11,Z10)`.

No fitted factor or physical source rescaling is permitted.

## Frozen interpretation

Repair34 remains a historical FAIL.

However:

- its canonical H4 propagation closes;
- its state time-resolution control closes;
- its boundary closes;
- its anisotropy closes;
- all source-resolution controls close.

The two remaining FAIL gates are implementation/audit defects already
localized to:

1. an all-row shift metric that contradicts the previously certified
   Repair21/Repair22 active/near-null rule;
2. a floating subtractive Q-cross audit that should be replaced by the exact
   symbolic bilinear form of the same frozen GE06/GE07 quadratic source.

Repair34 does not certify Z21.

## Licensed next step

A separately preregistered Repair35 may:

1. keep the exact same H4 equation, parents, grids, source coefficients and
   GE05->GE06 factor two;
2. evaluate the GE06/GE07 Q cross through its exact symbolic bilinear form,
   with exact symbolic polarization identity and numerical symmetry audit;
3. apply the already-certified Repair21/Repair22 propagated-shift rule:
   active relative backward error plus near-null absolute-residual control and
   matched Nt64/Nt128 convergence;
4. retain the Repair18 projected boundary and Repair07 canonical Radau
   propagation unchanged.

No observational input, finite eta, fitted normalization, threshold fitting,
source rescaling, primordial Z21 or full-species claim is licensed.

## Canonical status

**Repair34 = historical valid FAIL, audit-confounded. The canonical H4 solver
defect from Repair33 is closed. Z21 is NOT CERTIFIED. A separately
preregistered Repair35 is licensed to repair only the two localized audits.**
