# C3 direct bath bridge audit R2 — technical common-domain repair

## Status

The prior direct bath-bridge audit run `34484186780` is an immutable technical INCOMPLETE. It did not reach any bath-state or residual comparison because the audit required the finite common-domain start to precede z=6. For mode 0 the first finite common-domain point is tau = 5728.718072200329 Mpc, about 1.60 Mpc after the z=6 checkpoint at tau ~ 5727.116 Mpc.

This R2 declaration is made before any repaired bath-bridge result is generated.

## Frozen repair

Only the audit-domain guard is changed.

For each frozen k mode, the audit starts at the earliest point where all CLASS bath states and all offline background quantities needed by the existing `bath_advance` path are finite. The offline bath is initialized from the transformed CLASS q_j,p_j at that exact common point.

Any frozen checkpoint earlier than the selected common start is skipped. All later frozen checkpoints are evaluated unchanged. No backward extrapolation is allowed.

The bath mapping, equations, source construction, order 39, tauH0=1, physical eta=0, six k modes, D2C6C `bath_advance`, and all existing comparison thresholds are unchanged.

## Interpretation

The historical R1 technical INCOMPLETE remains unchanged. R2 reports the same `SOURCE_BRIDGE_PASS`, `BATH_STATE_BRIDGE_PASS`, and `B_RESIDUAL_BRIDGE_PASS` quantities on the valid common domain. It may classify as `C3_BATH_BRIDGE_PASS`, `C3_BATH_BRIDGE_MISMATCH_IDENTIFIED`, or `C3_BATH_BRIDGE_INCOMPLETE` under the existing rules.

Finite-positive-eta nonlinear memory remains unlicensed regardless of this diagnostic outcome.
