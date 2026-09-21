# GE19 Repair08 shift-constraint localization audit — result freeze

## Status

Frozen first locked Repair08 local diagnostic execution.

Terminal classification:

`GE19_REPAIR08_SHIFT_CONSTRAINT_LOCALIZATION_AUDIT_COMPLETE`.

Repair07 remains historically frozen as

`GE19_REPAIR07_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Repair08 is diagnostic only and does not relabel Repair07.

## Execution provenance

Repository HEAD used by the locked local runner:

`6b0661cf2200a660f2a4d069b7458b787a14099d`.

Frozen Repair07 science parent SHA-256:

`f27d31b637332bd043ebabdcc47a18e1126f05065aea2cca794ac8e0f2b2e894`.

Repair08 result JSON:

- bytes: `48562`;
- SHA-256:
  `8402a9f3ede227ca4c0c762976c8de247dd07161b41f504c438c6f248361d7d0`.

Repair08 inner FULL log:

- bytes: `48562`;
- SHA-256:
  `8402a9f3ede227ca4c0c762976c8de247dd07161b41f504c438c6f248361d7d0`.

Repair08 outer runner log:

- bytes: `54479`;
- SHA-256:
  `4a48e8220933095efae209752311da1f6bcc0dcc91476c27380427aed36ef49b`.

The result JSON and inner FULL log are byte-identical.

The runner completed with terminal marker

`GE19_REPAIR08_DIAGNOSTIC_COMPLETE`.

## Global localization result

The prescribed initial surface satisfies the frozen shift gate:

`initial_prescribed_shift_backward_error_max = 3.9269986174371925e-8`

against the unchanged reference gate

`1e-6`.

Therefore the Repair07 shift failure is not an initial-surface defect.

The frozen mixed GE15 + GE18 reduced-dust reference develops a much smaller but genuine shift mismatch:

`mixed_reference_reduced_dust_shift_backward_error_max = 5.752028513468997e-4`.

The internally evolved Repair07 canonical state develops

`canonical_repair07_shift_backward_error_max = 7.116549016013037e-2`.

Thus the canonical violation is approximately 124--266 times larger than the maximum reduced-reference mismatch, depending on C and mode.

## Constraint-propagation onset

For every one of the 18 frozen C x mode cases, the canonical shift residual is below the gate on the initial node and exceeds it already on the first subsequent Nt=64 node.

The common first-crossing redshift is

`z = 1.471043244117181`.

The first-crossing backward error lies in the narrow range

`5.530397340784823e-4` to
`5.545985072336348e-4`.

This mode- and C-insensitive onset is strong evidence for a structural propagation inconsistency, not a localized Fourier-mode instability.

## Full-standard CLASS momentum control

Using the frozen GE07 action normalization, the full-standard CLASS momentum cancels the GE15 gravitational+AeST shift contribution to

`full_standard_CLASS_pair_metric_max = 6.142613426914724e-6`.

The preregistered diagnostic acceptance scale was

`1e-4`.

The intentionally wrong full-standard sign gives

`1.9999999788320433`.

Therefore the physical matter-shift sign used by the audit is correct and the GE15/GE06 plus full-standard CLASS convention is mutually consistent at the expected interpolation level.

## Sign-flip falsification controls

A hypothetical reduced-matter T/sign flip gives a worst initial pair metric

`1.9999997660666908`.

A hypothetical AeST scalar-phi sign flip gives

`0.9147364921497281`.

Neither improves the initial shift cancellation.

The maximum reported improvement factors are

- T/matter sign flip:
  `5.180276082444124e-7`;
- AeST scalar-phi sign flip:
  `1.1328372343704689e-6`.

Therefore neither sign convention is a plausible Repair08 explanation.

## Frozen routing

Repair08 reports:

- `initial_surface_defect=false`;
- `propagation_defect=true`;
- `full_standard_CLASS_shift_convention_closes=true`;
- `reduced_reference_exceeds_shift_gate=true`;
- `matter_sign_suspect=false`;
- `aest_scalar_sign_suspect=false`.

Frozen next route:

`REDUCED_DUST_BRIDGE_OR_BACKGROUND_OFFSHELL_SUSPECT`.

## Interpretation

The result separates three levels:

1. the initial GE15+GE18 map is constraint-compatible at the frozen initial surface;
2. the pressureless reduced-dust surrogate on the frozen full-species background develops a small O(1e-4--1e-3) shift inconsistency across the late-time window;
3. the current anisotropy-enforced canonical DAE realization amplifies the inconsistency to O(7e-2).

Repair08 therefore does not yet prove that the only required change is the background.  A remaining ambiguity is the DAE constraint partition: anisotropy is currently enforced algebraically and shift is monitored.

The next diagnostic must distinguish:

- a genuinely off-shell reduced background / reduced-matter model, for which no admissible constraint partition propagates both independent constraints; from
- a partition-choice defect, for which enforcing shift algebraically allows anisotropy to propagate at the frozen tolerance.

No threshold may be changed to make either outcome pass.

## Claim boundary

Repair08 licenses no H3/Z20 construction.

It introduces no finite eta, finite physical amplitude, collapse, lensing or observational claim.

It is only a localization result for the reduced-H1 constraint closure problem.
