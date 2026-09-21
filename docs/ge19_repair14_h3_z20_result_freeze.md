# GE19 Repair14 self-consistent reduced-H3 Z20 result freeze

## Status

Frozen first locked Repair14 local science execution.

Terminal classification:

`GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Repair13 remains the certified reduced-H1 parent. Repair14 is a historical Stage-B FAIL and must not be relabeled.

## Frozen local outputs

Science JSON:

- bytes: `697196`;
- SHA-256: `741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57`.

NPZ:

- bytes: `9467673`;
- SHA-256: `b72626bd45b02b537d21f035fc8c746eb06eee669869c4aea921861328303c42`.

Inner FULL log:

- bytes: `697196`;
- SHA-256: `741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57`.

Outer runner log SHA-256 was not preregistered as a science binding; the terminal runner code is frozen as

`GE19_REPAIR14_EXIT=2`.

## Provenance

Repair13 parent hashes are exact.

Repair13 Stage A is PASS.

The reconstructed Repair13 reduced H(a) agrees with the frozen parent NPZ with relative L2 max `0.0`.

Frozen Repair13 Z10 is loaded without H1 recomputation and is finite.

The locked Repair11 first-directional Lambda operator and exact Repair14 common-direction Lambda c2 source were used.

## Source controls

All sources are finite.

Nx=1024 vs Nx=2048 source convergence for m=1..40:

`1.1166216258507802e-12`

against gate `5e-4`: PASS.

Thus the Repair14 failure is not a spatial source-convergence failure.

## Source decomposition

Across the C envelope:

- Einstein+AeST quadratic source L2 is approximately `1.446e10`;
- dust quadratic source L2 is approximately `8.4e-6`;
- Lambda quadratic source L2 is approximately `3.09e-16`;
- Y_H3 L2 is approximately `0.030--0.055`.

Therefore:

- Lambda c2 is negligible relative to Einstein+AeST+dust at approximately `2.14e-26`;
- Y_H3 is approximately `2.09e-12--3.80e-12` of the total analytic quadratic source.

The central Z20 state is correspondingly almost beta-independent:

- beta0=0.5 vs beta0=1 relative L2: `1.3922322777504615e-12`;
- beta0=0.1 vs beta0=1 relative L2: `1.5387587874486087e-12`.

This is descriptive only because Repair14 fails Stage B.

## Primary solve controls

- linear-system relative L2 max:
  `1.3665579847915249e-8` against gate `1e-8`: FAIL;
- shift constraint backward error max:
  `1.6504055271415055` against gate `1e-6`: FAIL;
- anisotropy constraint backward error max:
  `5.176430012533252e-16` against gate `1e-6`: PASS.

The shift failure is the dominant failure.

Representative mode diagnostics show:

- well-conditioned local algebraic matrices (condition numbers O(2.6));
- Radau block scaled residuals O(1e-16);
- anisotropy O(1e-16);
- shift backward errors O(1) over many modes.

This pattern does not indicate a generic integrator instability.

## Control solve and time-grid controls

Nt=32 control:

- linear-system relative L2 max:
  `1.3643176644286886e-8`;
- shift constraint backward error max:
  `1.6473553166699726`;
- anisotropy constraint backward error max:
  `6.394777335818628e-16`.

Primary64/control32 state relative L2 max:

`5.470805059400488e-4`

against gate `5e-3`: PASS.

Thus the large shift defect reproduces on both time grids while the Z20 state itself is time-grid converged.

## Frozen gates

PASS:

- exact Repair13 parent provenance;
- all sources finite;
- Nx1024/Nx2048 source convergence;
- anisotropy constraint;
- 64/32 state convergence;
- all C and beta cases complete;
- all outputs finite.

FAIL:

- primary linear residual;
- shift constraint.

## Interpretation

Repair14 constructs a numerically stable, spatially converged and time-grid-converged window-local Z20 candidate, but it does not satisfy the frozen second-order shift constraint. Therefore Z20 is not certified.

The failure pattern points to second-order constraint/source compatibility rather than to source-grid resolution, time integration, Lambda c2, or anisotropy closure.

A particularly important implementation fact is that the current canonical H3 initial state fixes the dynamic Z20 values and cosmic-time derivatives to zero and determines only N20 and delta_varrho20 from the lapse and dust-density equations. It does not independently impose the nonzero quadratic shift constraint on the initial surface.

That does not yet prove that the initialization is the sole cause. A separate preregistered diagnostic must determine if the full H3 quadratic source obeys the required initial lapse/density/shift compatibility and if a constraint-compatible window-retarded initial algebraic state exists.

## Stop rule

No q20 construction and no H4/Z21 is licensed.

No Stage-B threshold is relaxed.

## Claim boundary

Repair14 does not certify Z20. It does not establish finite-eta nonlinear memory propagation, finite physical-amplitude evolution, collapse, lensing or observations.
