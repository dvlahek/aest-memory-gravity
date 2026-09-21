# GE19 Repair11 Lambda-inclusive reduced-H1 result freeze

## Status

Frozen first locked Repair11 local science execution.

Terminal classification:

`GE19_REPAIR11_LAMBDA_INCLUSIVE_REDUCED_H1_RECLOSURE_FAIL`.

Stage:

`Stage_A_reduced_H1_reclosure_only`.

Repair11 is a historical FAIL and must not be relabeled.

## Frozen local outputs

Science JSON:

- bytes: `67437`;
- SHA-256: `5283dd425864e8f6613678a1ad90a71e2d69243cbecd868685af45c52be077ab`.

NPZ:

- bytes: `273299`;
- SHA-256: `ed2431e59d89f820796f6e9b534b8ca19ae026ad55597302bf92ddb120dfec83`.

Inner FULL log:

- bytes: `67437`;
- SHA-256: `5283dd425864e8f6613678a1ad90a71e2d69243cbecd868685af45c52be077ab`.

Outer local runner log:

- bytes: `70669`;
- SHA-256: `07430adcc7b0eb47737366de541a030d14f593523cb8d5fe591647b192572654`.

The JSON and inner FULL log are byte-identical.

## Stage-A result

Global controls:

- canonical/linear residual:
  `4.835355891984503e-16`;
- shift constraint componentwise backward error:
  `5.016294027155656e-5`;
- anisotropy constraint backward error:
  `2.0132048989771212e-16`;
- initial dynamic match:
  `5.826069165486057e-14`;
- primary64/control32 state relative L2:
  `1.3171270252823885e-4`;
- all outputs finite: true.

All frozen gates pass except shift:

- linear residual <= 1e-8: PASS;
- shift <= 1e-6: FAIL;
- anisotropy <= 1e-6: PASS;
- 64/32 state <= 5e-3: PASS;
- initial match <= 1e-10: PASS;
- finite outputs: PASS.

Therefore:

`stage_A_pass=false`

and

`Z20_constructed=false`.

## Lambda effect

Repair07 historical shift maximum:

`7.116549016013037e-2`.

Repair11 shift maximum:

`5.016294027155656e-5`.

Improvement factor:

`1418.6865796717002`.

Thus the omitted cosmological-constant sector was the dominant Stage-A off-shell mechanism, but it was not the entire residual.

## C-envelope pattern

Primary-grid shift maxima:

- C_min: `4.9816372961221245e-5`;
- C_star: `3.5081380612536495e-5`;
- C_max: `1.8334663557444917e-5`.

Control-grid shift maxima:

- C_min: `5.016294027155656e-5`;
- C_star: `3.535570869607955e-5`;
- C_max: `1.850394799036023e-5`.

The residual decreases systematically as C increases and is highly reproducible between Nt=64 and Nt=32.

## Interpretation

Repair11 excludes the following as explanations for the remaining shift defect:

- solver residual;
- anisotropy closure;
- time-grid nonconvergence;
- initial dynamic mismatch;
- nonfinite values;
- missing Lambda action.

The remaining defect is compatible with the residual mismatch introduced by replacing the full standard sector by a single pressureless dust surrogate. This is not yet proven by Repair11 alone.

A subsequent preregistered diagnostic must compare the Repair11 shift residual directly against the omitted full-standard minus reduced-dust momentum contribution on the same frozen trajectory.

No threshold may be relaxed.

## Claim boundary

Repair11 does not certify H3/Z20. It introduces no finite-eta, finite-amplitude, collapse, lensing or observational claim.
