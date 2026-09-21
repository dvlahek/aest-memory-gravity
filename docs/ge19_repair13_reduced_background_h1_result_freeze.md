# GE19 Repair13 self-consistent reduced-background H1 result freeze

## Status

Frozen first locked Repair13 local science execution.

Terminal classification:

`GE19_REPAIR13_SELF_CONSISTENT_REDUCED_BACKGROUND_H1_RECLOSURE_PASS`.

Repair13 closes the mandatory GE19 Stage-A reduced-H1 reclosure on the self-consistent AeST+dust+Lambda background.

Repair11 remains historical FAIL. Repair12 remains a diagnostic audit. Neither is relabeled.

## Locked implementation parent

Runner/science HEAD used by the local execution:

`c25887376b030364773782494b9ad6df685463ce`.

Repair13 implementation lock:

`docs/ge19_repair13_reduced_background_h1_implementation_lock.md`.

## Frozen local outputs

Science JSON:

- bytes: `71999`;
- SHA-256: `ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7`.

NPZ:

- bytes: `277071`;
- SHA-256: `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`.

Inner FULL log:

- bytes: `71999`;
- SHA-256: `ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7`.

Outer runner log:

- bytes: `75349`;
- SHA-256: `ae898ba50227bdba4f5af3354c723155aab880b721499001fd3565094508940e`.

The JSON and inner FULL log are byte-identical.

Runner terminal code:

`GE19_REPAIR13_EXIT=0`.

## Frozen background

For each C envelope the Stage-A operator is evolved on

`H_red(a)^2 = (Q K_Q-K)/3 + C/a^3 + rho_lambda`

with the frozen scalar charge

`a^3 K_Q = I0`.

No fitted background correction is used.

Global background controls:

- Friedmann relative L2 max: `5.3148141262610533e-17`;
- pressure-identity relative L2 max: `4.9400107598617e-16`;
- all background values finite: PASS;
- H positive: PASS.

Difference from the previous full-species CLASS H(a), primary grids:

- C_min: `7.474528574531103e-5`;
- C_star: `3.465442004332329e-5`;
- C_max: `6.534659570806197e-5`.

Thus a background mismatch at only O(1e-5--1e-4) was sufficient to dominate the previous shift monitor.

## Frozen Stage-A controls

Global maxima:

- canonical/linear residual: `4.3389056048311334e-16`;
- shift backward error: `4.54500027983174e-7`;
- anisotropy backward error: `2.0133086499281873e-16`;
- initial dynamic match: `5.826069165486057e-14`;
- primary64/control32 state relative L2: `1.317515813217615e-4`;
- all outputs finite: PASS.

All preregistered Stage-A gates pass:

- linear residual <= `1e-8`;
- shift backward error <= `1e-6`;
- anisotropy backward error <= `1e-6`;
- primary64/control32 state <= `5e-3`;
- initial dynamic match <= `1e-10`;
- all outputs finite.

## Per-C shift controls

Primary:

- C_min: `6.369905709933526e-8`;
- C_star: `6.369963695182228e-8`;
- C_max: `6.370007701051935e-8`.

Control:

- C_min: `4.5448668109910536e-7`;
- C_star: `4.544924615217168e-7`;
- C_max: `4.54500027983174e-7`.

The near-identical values across C support the interpretation that the previous C-dependent Repair11 residual was caused by using the full-species CLASS background with the reduced AeST+dust+Lambda operator.

## Scientific interpretation

Repair13 establishes that the reduced Einstein+AeST+dust+Lambda first-order system can be evolved on its own homogeneous on-shell background while satisfying the frozen linear equations and independent shift/anisotropy constraints under the preregistered numerical gates.

This closes the mandatory GE19 H1 reclosure:

`L_total Z10_reduced = 0`

for the frozen window and C envelope.

The key repair was not a new perturbative source. It was restoring consistency between the homogeneous background and the reduced perturbative operator.

## H3 boundary

`Z20_constructed = false`.

Repair13 does not itself certify H3/Z20.

The next licensed step is a separately preregistered H3 construction on this same self-consistent reduced background, including the Lambda second-directional metric source required by the frozen action, followed by the original H3 equation

`L_total Z20 = -Q_total(Z10,Z10) - 2 Y2[Z10]`.

## Claim boundary

Repair13 certifies only the self-consistent reduced-background H1 Stage-A closure.

It does not establish gravitational memory, finite eta, finite physical-amplitude nonlinear evolution, collapse, lensing or any observational detection.
