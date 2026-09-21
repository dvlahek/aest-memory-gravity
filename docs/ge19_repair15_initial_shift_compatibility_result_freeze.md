# GE19 Repair15 H3 initial shift/Noether compatibility result freeze

## Status

Frozen first locked Repair15 local diagnostic execution.

Terminal classification:

`GE19_REPAIR15_H3_INITIAL_SHIFT_NOETHER_COMPATIBILITY_AUDIT_COMPLETE`.

Frozen routing:

`INITIAL_SOURCE_INCOMPATIBILITY`.

Repair14 remains historical FAIL. Repair15 is diagnostic only and does not certify Z20.

## Frozen local outputs

Science JSON:

- bytes: `3507539`;
- SHA-256: `a8c86b6056a3d6ab2f6f443850bef34881452b4a11b32bb6a66e2ac7920f1e50`.

Inner FULL log:

- bytes: `3507539`;
- SHA-256: `a8c86b6056a3d6ab2f6f443850bef34881452b4a11b32bb6a66e2ac7920f1e50`.

Outer local runner log:

- bytes: `3512328`;
- SHA-256: `e76d603b946df54e3a8be5498a9eadf0373732a2d078b5870d8b1b93c454d7a0`.

The JSON and inner FULL log are byte-identical.

Terminal marker:

`GE19_REPAIR15_DIAGNOSTIC_COMPLETE`.

## Provenance

Frozen Repair13 JSON/NPZ hashes are exact.

Frozen Repair14 JSON hash is exact.

Repair14 parent classification is FAIL.

Repair15 does not recompute the Repair14 Z20 trajectory.

## Global audit result

- initial target norm max: `1914885.7075823217`;
- material source cases: `378`;
- all cases: `720`;
- current initial shift metric max: `1.0000314679807352`;
- current initial anisotropy metric max: `1.1583683829829314`;
- material 3x2 least-squares relative residual max: `0.24244997981714522`;
- material left-null compatibility residual max: `0.2424499798171455`;
- best pair unfitted equation metric max: `1.0000314679807352`.

Against the preregistered compatibility threshold `1e-6`, the frozen zero-dynamic initial surface is strongly incompatible.

## Rank result

For representative material modes, the row-scaled system formed from

- lapse;
- dust density;
- shift

for algebraic unknowns

`(N20, delta_varrho20)`

has:

- coefficient rank 2;
- augmented rank 3.

Thus no choice of only N20 and delta_varrho20 can close all three equations when

`S20=u20=phi20=T20=0`

and

`S20dot=u20dot=phi20dot=T20dot=0`.

Example C_min, beta0=1, primary, m=2:

- 3x2 least-squares residual `0.24237601721710691`;
- left-null residual `0.2423760172171067`;
- current shift metric `0.999876421364487`.

The same pattern repeats across material modes and on both time grids.

## Important interpretation boundary

Repair15 does **not** prove that the GE06+GE07+Lambda quadratic source itself violates the nonlinear Noether/Bianchi identity.

It proves that the source cannot be made compatible with the current initial convention using only algebraic N20 and delta_varrho20 while all dynamic values and dynamic cosmic-time derivatives are fixed to zero.

The canonical integrator evolves

`y=(S,u,phi,T,pS,pu,pphi,pT)`,

not

`(q,qdot)`.

Therefore the next diagnostic must test the canonical zero state

`y0=0`

directly. Under that boundary condition, the frozen algebraic map determines

`N20, delta_varrho20, S20dot, u20dot, phi20dot, T20dot`

from the quadratic source. Lapse and shift then remain independent Noether monitors.

## Next licensed question

Test if

`y0=(q0,p0)=0`

on the same frozen Repair13 background and Repair14 source yields:

- algebraic p/density/anisotropy equations closed by construction;
- independent lapse residual <= 1e-6;
- independent shift residual <= 1e-6.

If yes, the Repair14 failure is an initial-variable convention error rather than a quadratic-source inconsistency.

If not, proceed to a direct quadratic Noether/source identity audit.

## Stop rule

No Repair14 rerun, q20, H4 or Z21 is licensed by Repair15 alone.

No threshold is relaxed.

## Claim boundary

Repair15 certifies only the failure of the zero-dynamic-velocity initial compatibility test. It does not certify or falsify Z20 or nonlinear memory propagation.
