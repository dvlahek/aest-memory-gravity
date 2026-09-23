# GE19 Repair36 Lambda-complete H4/Z21 — valid FAIL numerical-localization freeze

## Status

The first valid Repair36 science execution is frozen exactly as emitted.

Classification:

`GE19_REPAIR36_LAMBDA_COMPLETE_H4_Z21_RECLOSURE_FAIL`.

Repair36 is not relabelled.

The Lambda-complete H4 construction closed the Repair35 O(1e-3) propagated
shift defect, but two preregistered gates remain false. Both are localized as
numerical/audit limitations rather than evidence for a physical H4
inconsistency.

## Frozen local artifacts

Science JSON:

- SHA-256:
  `5ba2dacf586ccbbdd5eb41c4ea7cf5c839f5aa2829c294702b4fc37d84ef113f`;
- bytes:
  `461359`.

Science NPZ:

- SHA-256:
  `e19962ca71ea002c61b3251365496ee46ac1467054fff81625fb2bce5b5c652a`;
- bytes:
  `27178396`.

Inner FULL log:

- SHA-256:
  `5ba2dacf586ccbbdd5eb41c4ea7cf5c839f5aa2829c294702b4fc37d84ef113f`;
- bytes:
  `461359`.

Outer runner log:

- SHA-256:
  `200ac7f4011420ca604b9518a52d791ef783e24de3f18d3b0ebc7bed6ea8e2d2`;
- bytes:
  `466386`.

Terminal marker:

`GE19_REPAIR36_VALID_SCIENCE_FAIL_FREEZE_REQUIRED`.

## What Repair36 closed

The exact frozen Repair11 Lambda first-directional operator was installed at
1146 canonical stage evaluations with finite `rho_lambda`, exactly zero
Lambda shift row and exactly zero Lambda anisotropy row.

The propagated matched-shift defect changed from the frozen Repair35 value

`6.259823617443525e-03`

to

`1.7627809358943246e-06`.

The matched Nt64 control is

`2.0966217090200273e-05`.

Observed convergence orders are

- Linf:
  `3.5318614331155236`;
- RMS:
  `3.3680198437218167`.

Thus the dominant Repair35 Lambda omission is closed.

Other controls remain strongly converged:

- canonical Radau/algebraic residual:
  `2.342470445459017e-13`;
- state Nt128/Nt64:
  `3.792872866710913e-05`;
- anisotropy:
  `2.530320504221839e-16`;
- source Nt128/Nt64:
  `1.8704084900967867e-04`;
- all boundary metrics:
  machine-level;
- all outputs finite.

## Failed gate 1 — floating polarization audit of a numerically negligible Lambda source

Frozen value:

`Q_lambda_direct_vs_exact_polarization_relative_L2_max = 4.9812967098147326e-08`

against the preregistered `1e-12` relative threshold.

However:

- direct Lambda swap symmetry is
  `9.727642209636082e-17`;
- the symbolic mixed-bilinear polarization identity was proved exactly in the
  dedicated Repair36 prelock;
- the complete primary `2Q_Lambda_cross` L2 norm is only
  `4.2444071395688146e-24`.

Therefore the one-direction Lambda cross norm is approximately

`2.1222035697844073e-24`.

Multiplying by the reported relative mismatch gives an absolute L2
polarization difference of only approximately

`1.06e-31`.

The reported relative failure is caused by subtractive cancellation in the
audit expression

`[Q(d+e)-Q(d-e)]/4`

on an already ~1e-24 source. It is not a source-construction mismatch.

Repair36 remains FAIL because the gate was preregistered, but this gate is a
floating-point audit defect.

## Failed gate 2 — fourth-order source-assembly truncation at the 1e-6 pointwise target

Frozen matched-shift values:

- Nt128 active Linf:
  `1.7627809358943246e-06`;
- Nt64 matched Linf:
  `2.0966217090200273e-05`;
- observed Linf order:
  `3.5318614331155236`;
- Nt128 active RMS:
  `1.4153159101661385e-06`;
- Nt64 matched RMS:
  `1.5006913942977151e-05`;
- observed RMS order:
  `3.3680198437218167`.

The worst Nt128 active sample has:

- C:
  `C_min`;
- beta0:
  `0.1`;
- mode:
  `8`;
- time index:
  `26`;
- absolute residual:
  `6.366035075700368e-17`;
- row scale:
  `3.611359157608906e-11`;
- backward-error metric:
  `1.7627809358943246e-06`.

The same frozen monitor defines

`S_ref = 2.967804510795483e-04`

and near-null absolute allowance

`1000 eps S_ref = 6.589849800943089e-17`.

Therefore the absolute residual of the worst active sample is already below
the monitor's own roundoff-scale near-null allowance.

The active/near-null split uses

`sqrt(eps) S_ref = 4.422373340719168e-12`.

This places a row of scale `3.61e-11` in the relative branch even though its
absolute residual is still at the global roundoff allowance. The branch
transition is therefore discontinuous relative to the two tolerances.

More importantly, the coarse/fine matched defect decreases by more than an
order of magnitude and with observed order ~3.4--3.5. This is consistent with
the frozen fourth-order `fd4_matrix` used inside the GE06/GE07 nonlinear
Euler-Lagrange source assembly for terms of the form

`Dt @ partial`.

Hence Repair36 does not show a nonconvergent physical shift inconsistency. It
shows that Nt128 with the frozen fourth-order nonlinear source derivative is
slightly under-resolved for the independent `1e-6` pointwise constraint
gate.

A formal extrapolation using the observed Linf order predicts approximately

`1.52e-7`

at the next factor-two time resolution.

This extrapolation is diagnostic only and is not a Repair36 PASS claim.

## Frozen interpretation

Repair36 remains a historical valid FAIL.

It must not be relabelled.

The FAIL does not license changing the `1e-6` shift threshold inside
Repair36.

The result localizes two numerical issues:

1. a cancellation-dominated relative Lambda polarization audit;
2. a fourth-order time-derivative/source-assembly resolution floor in the
   independent propagated-shift monitor.

Neither is evidence for a physical failure of the Lambda-complete H4
equation.

## Licensed next step

A separately preregistered follow-up may:

1. replace the Lambda polarization **audit only** by the exact direct symbolic
   identity plus a cancellation-safe absolute/backward-error diagnostic;
2. keep the H4 shift threshold at `1e-6`;
3. improve only the numerical time derivative/source-assembly accuracy
   (for example a separately audited higher-order derivative operator) or
   perform a genuine higher-time-resolution reclosure;
4. retain all Repair36 physical source formulas, parents, Lambda terms,
   memory normalization, boundary conditions, and observational independence.

No threshold relaxation, fitted normalization, finite eta, primordial Z21,
full-species Z21 or observational tuning is licensed.

## Canonical status

**Repair36 = historical valid FAIL. The dominant Lambda omission is closed.
The remaining failures are localized to a cancellation-dominated Lambda
audit and a convergent fourth-order source-assembly resolution floor. Z21
remains uncertified pending a separately locked numerical reclosure.**
