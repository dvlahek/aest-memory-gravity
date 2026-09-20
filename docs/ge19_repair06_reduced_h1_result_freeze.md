# GE19 Repair06 reduced-H1 result freeze

## Historical result

Repair06 local science execution is frozen as

`GE19_REPAIR06_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Failure stage:

`Stage_A_reduced_H1_reclosure`.

This historical classification must not be relabeled.

## Frozen local result hashes

Science JSON:

- SHA256: `8371a22d19e2b0ce4eb57684e6c48b7ae2124fdea225da22093613f01c3a73e9`
- bytes: `46036`

Inner FULL log:

- SHA256: `8371a22d19e2b0ce4eb57684e6c48b7ae2124fdea225da22093613f01c3a73e9`
- bytes: `46036`

Outer local runner log:

- SHA256: `ff3766076330e7638796b987cd6e7c37dfde30d5f2e0195c6c33963faf06a867`
- bytes: `47976`

## Frozen Stage-A controls

Global maxima:

- canonical/main linear-system relative L2 residual:
  `4.198335271454888e-16`;
- shift constraint monitor:
  `1.9979693163943717`;
- anisotropy constraint monitor:
  `1.0`;
- initial dynamic match abs-or-rel:
  `5.826069165486057e-14`;
- primary64/control32 state global relative L2:
  `1.31712788922018e-4`;
- all outputs finite: true.

The frozen Stage-A gates therefore passed for:

- linear-system residual;
- initial dynamic match;
- 64/32 time-grid convergence;
- finite outputs;

and failed only for:

- shift monitor;
- anisotropy monitor.

The Amendment01 stop rule was correctly applied:

`Z20_constructed=false`.

## Repair07 diagnosis boundary

Repair06 uses the Noether-regularized algebraic partition in which the anisotropy equation is an enforced algebraic row. The same run reports algebraic scaled residuals O(1e-16), while the separately reported anisotropy monitor is exactly O(1). This combination is incompatible with a genuine O(1) anisotropy-equation defect and identifies the monitor normalization as ill-conditioned near homogeneous cancellation.

The current shift/anisotropy monitors divide only by the magnitudes of the already-cancelled Einstein+AeST and matter pieces:

`|r| / max(|piece_ga|, |piece_m|, |source|, tiny)`.

When the exact constraint and each individual contribution are simultaneously tiny, this becomes roundoff divided by roundoff and is not a stable relative residual.

Repair06 already uses a stable row-scaled residual for the independently monitored lapse/Noether row:

`|r| / max(|lhs|, |rhs|, ||row||_inf ||w||_inf, tiny)`.

Repair07 may change only the shift and anisotropy monitor normalization to the same row-scaled operator normalization, preserving their exact residual numerators, source signs, equations, thresholds and solver.

Repair07 must not change:

- GE06 or GE07 generators;
- the continuum equations;
- the canonical/Noether DAE partition;
- the Radau-IIA integrator;
- stable-Z normalization;
- initial conditions;
- C values, beta values, modes or grids;
- the shift or anisotropy residual numerators;
- the frozen `1e-6` shift and anisotropy thresholds;
- Stage-A or Stage-B stop logic;
- the Repair06 historical FAIL classification.

## Interpretation

Repair06 is not evidence of a physical Stage-A failure. It is a historical FAIL caused by two frozen monitor values exceeding their gates. Repair07 is licensed only to determine if those values were artifacts of an ill-conditioned denominator.
