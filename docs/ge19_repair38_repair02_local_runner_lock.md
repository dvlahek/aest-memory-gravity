# GE19 Repair38 repair02 local diagnostic runner — lock

## Status

The Repair38 repair02 local diagnostic execution path is frozen before its
first run.

Runner:

`ge19/run_local_repair38_repair02_frozen_source_radau_substep_localization.sh`.

Runner commit:

`5ebab5070e1cf57ddebe201c7d0f7c368b7c93a6`.

Runner blob:

`eaf4fde5ff115dcaa51f3c9d18f04ab92207c806`.

Static runner audit:

- run:
  `35862004336`;
- job:
  `107184232321`;
- conclusion:
  `success`.

## Repair02 implementation binding

Implementation commit:

`5d48eada0ea7e79dd7b959c9016f16bd098daa80`.

Implementation blob:

`df485d3c4752b96b2dae96ef9fa7d77b686fe158`.

Repair02 implementation lock:

- commit:
  `8cb261754babf3563d9a09897a325d50c5fda13f`;
- blob:
  `b57ef9237a2a980c9e761a6e6bcc47eaa0181af7`.

Dedicated prelock:

- workflow commit:
  `712da21262e2cb5f92878973084955798b7001c9`;
- workflow blob:
  `b09636b00cb9c29ae489dad096df1992009ce81b`;
- run:
  `35861865342`;
- job:
  `107183772633`;
- conclusion:
  `success`.

## Preserved failures

The initial endpoint-domain execution failure remains frozen and is not
relabelled.

Repair38 repair01 false-nonfinite execution remains frozen at:

`docs/ge19_repair38_repair01_false_nonfinite_implementation_fail_freeze.md`.

Its artifacts remain:

- JSON/FULL SHA-256:
  `38ba963eaaa4dad49aa876299f6a33e11d843b24ac555f74a7e586bb4ceb3240`;
- NPZ SHA-256:
  `aff63771c1800b0db236cd020cf0d2772f6d9a0fd0328573d055392f2c60da67`;
- outer runner SHA-256:
  `66bbc767144824b1356880d9da9ebf9ddc30fe46631377ca9d7d20f32c3f3c28`.

Repair01 remains IMPLEMENTATION_FAIL.

## Execution rule

Repair02 changes only the finite-output implementation check. It does not
change the H4 source, projected p0, Radau tableau, endpoint coordinates,
science target, diagnostic thresholds or routes.

Factor 1 must reproduce the frozen Repair37 result exactly before routing can
be interpreted.

If repair02 emits a valid diagnostic JSON, that result must be frozen exactly
as emitted.

Repair38 remains diagnostic-only. It cannot certify Z21 or license lensing.
