# GE19 Repair43 local GE06 source-row diagnostic runner — lock

## Status

The Repair43 local execution path is frozen before its first local run.
The runner is diagnostic-only; no H4 science reclosure, Z21 certification or
lensing is licensed.

Runner:
`ge19/run_local_repair43_qge06_main_constraint_stage_split.sh`.

Runner commit:
`f4b46d84b24124949ea28aea9d44b9a51d1a6f8e`.

Runner blob:
`9f4d110f9b2672f2b7e287a970095ddf007b856e`.

Static runner audit:
- run `35962211487`;
- job `107513010594`;
- conclusion `success`.

## Frozen bindings

Repair43 preregistration:
- commit `9aa0bfcb9e2e21979ad665037e1bd7b18213934a`;
- blob `b2161c074012c096fba8790fa377c69fd548a234`.

Repair43 implementation:
- commit `6257c3ba57e26035aaa2602440bedf0c368854f6`;
- blob `50769723c1ff5abce1548a15d41353fb295e932c`.

Repair43 implementation lock:
- commit `e8323cc6af85074d262efe5ded52961f616a255d`;
- blob `af4018ef73ddc931f7774f304bf83dae66f363d4`.

Repair43 dedicated prelock:
- workflow commit `c2c25dfc3f139fc616a672c3101fa5d4ed43356c`;
- blob `678a2f4d81d8ebce3c53246b86c6f89df1d7ad9b`;
- run `35962103386`;
- job `107512678243`;
- conclusion `success`.

Frozen Repair42:
- freeze commit `9a7fd6262832a44ca7d0d2cb73c322b856dcf514`;
- freeze blob `e3b89cc656ca5dade9a555aa21ae0ba65817af46`;
- JSON/FULL SHA-256:
  `4a211581a77c1ad00e14cc398ca7a19b12642f3f3e35b416314d6721f5f81e25`;
- NPZ SHA-256:
  `a60515f3d92bbd388fd2fadae6cf2dd07f3ee68e8690b07632bbe5091e9013c5`.

Frozen Repair41:
- JSON SHA-256:
  `1b18fede26b021e077ffe5c8b6b7ff0dc727b4defaab48e63491c86d868d1320`;
- NPZ SHA-256:
  `6bfb87ea21d55e2a1d2b16aee9bc8d7246111f91a064a78b74d2ed946ec2ba45`.

Frozen Repair37:
- JSON SHA-256:
  `da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a`;
- NPZ SHA-256:
  `572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f`.

## Execution and interpretation

The runner verifies exact repository blobs and local parent hashes before
propagation. It then runs PCHIP baseline and GE06 main-only,
constraint-only and both corrections separately at direct382 and direct763.
The full GE06 variants must reproduce Repair42 exactly in the frozen
Z21/shift metrics before the component-split diagnostic is interpreted.

It reports all active shift fields, absolute shift residuals, backward-error
scales, direct382/763 row attribution and the preregistered early-window
C_max/beta0/m8/time-index-3 hotspot.

Repair43 may route only to a valid preregistered row-sensitivity diagnostic
or to an implementation failure. It does not modify the science target
`1e-6`, certify Z21 or license lensing.
