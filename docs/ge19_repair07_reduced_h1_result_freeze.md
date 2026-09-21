# GE19 Repair07 reduced-H1 result freeze

## Status

Frozen first locked Repair07 local execution.

Terminal classification:

`GE19_REPAIR07_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Failure stage:

`Stage_A_reduced_H1_reclosure`.

Repair07 remains historical FAIL and must not be relabeled.

## Frozen local outputs

Science JSON:

- bytes: `67609`;
- SHA-256: `f27d31b637332bd043ebabdcc47a18e1126f05065aea2cca794ac8e0f2b2e894`.

Inner FULL log:

- bytes: `67609`;
- SHA-256: `f27d31b637332bd043ebabdcc47a18e1126f05065aea2cca794ac8e0f2b2e894`.

Outer local runner log:

- bytes: `70643`;
- SHA-256: `76ed915a2f38b24c644df98a0db602ca7bfd25273b73868030eeb2ca9e1d50d2`.

The JSON and inner FULL log are byte-identical.

## Locked Repair07 provenance

Repair07 lock audit passed locally before science execution.

The final Repair07 implementation used the componentwise backward-error constraint metric preregistered before the result.

No physics equation, sign, solver, threshold, C value, mode, grid or initial-match rule was changed from Repair06.

## Stage-A result

Global maxima:

- linear-system/canonical residual:
  `4.198335271454888e-16`;
- shift constraint componentwise backward error:
  `0.07116549016013037`;
- anisotropy constraint componentwise backward error:
  `2.0507171418980342e-16`;
- initial dynamic match:
  `5.826069165486057e-14`;
- primary64/control32 state relative L2:
  `1.31712788922018e-4`;
- all outputs finite: true.

Only the shift gate fails.

The old piece-normalized diagnostics remain:

- shift: `1.9979693163943717`;
- anisotropy: `1.0`.

The new metric proves these two historical O(1) diagnostics had different meanings:

- anisotropy is a pure cancellation-normalization artifact because its backward error is O(1e-16);
- shift remains a real nonzero constraint defect because its backward error is O(7e-2).

Maximum absolute residuals:

- shift: `1.2786829469515981e-11`;
- anisotropy: `7.067434251707117e-24`.

Maximum row scales:

- shift: `1.7969320965856464e-10`;
- anisotropy: `3.633670150077511e-8`.

Radau and local algebraic systems remain well solved:

- Radau scaled residual max: `4.198335271454888e-16`;
- Radau scaled condition max: `27.25758479717291`;
- local algebraic condition max: `2.7496602821998843`;
- independent lapse/Noether residual max: `1.288773318052877e-19`.

## Robustness pattern

The shift defect is not a single-mode or single-background outlier.

Across all six frozen modes, all three C values and both Nt=64/Nt=32 grids, the shift backward error is approximately `0.0711` while anisotropy remains at roundoff.

The C-envelope changes the shift defect only weakly.

Therefore Repair07 excludes:

- an ill-conditioned shift denominator;
- Radau solve failure;
- local algebraic conditioning failure;
- time-grid nonconvergence;
- anisotropy closure failure;
- provenance failure.

## Stop rule

The frozen Amendment01 stop rule was correctly applied:

`Z20_constructed=false`.

No H3/Z20 result is licensed from Repair07.

## Next diagnostic question

Repair07 alone does not locate the shift defect.

The next audit must distinguish:

1. **initial-surface convention defect**:
   the frozen GE15+GE18 initial state already violates the GE06+GE07 shift equation; from
2. **constraint-propagation defect**:
   the initial shift closes but the canonical reduced evolution generates the violation.

No equation or threshold should be changed until this distinction is measured directly.

## Claim boundary

Repair07 is a numerical/structural reduced-H1 result only. It makes no finite-eta, nonlinear-amplitude, collapse, lensing or observational claim.
