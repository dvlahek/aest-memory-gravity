# NL1C7B4 Repair19c4 — local result freeze

## Status

Frozen local WSL science result from the first locked Repair19c4 execution.

Terminal classification:

`NL1C7B4_REPAIR19C4_NO_MATERIAL_POST_FIRST_STEP_DERIVATIVE_WINDOW`

with

`SCIENCE_RC=0`.

Execution HEAD:

`f00638497add00d93b5adec3a4f80cb50f1c06b7`.

This is a local WSL result, not an official GitHub Actions run.

Repair19c4 is the terminal post-first-step finite-difference derivative-scale diagnostic licensed by the Repair19c3 result freeze.

## Frozen output hashes

Result JSON:

- bytes: `185951`
- SHA-256:
  `a5a7416cd93120f543dbe0f8a70ddc735e9704212d7db5266de87980fe768c18`.

Evaluator log:

- bytes: `186397`
- SHA-256:
  `776f5918b9df72d71b496c762d6f16a59974241363b1a9776d066e75a43001b2`.

Full local runner log:

- bytes: `200402`
- SHA-256:
  `88c65f9d86a5e7f1956a8d96a142aa00ba89f212a4a4a378857dd26aec270ccd`.

No state NPZ was written or licensed.

## Gate result

All Repair19c4 gates PASS:

- R19C4_G1 exact frozen provenance
- R19C4_G2 exact first-step reproduction
- R19C4_G3 exact gauge/Q/field freeze at x1
- R19C4_G4 complete directional-reference sweep
- R19C4_G5 deterministic reference-window evaluation
- R19C4_G6 complete candidate Jacobian audit
- R19C4_G7 deterministic candidate selection
- R19C4_G8 complete single-step descriptive cross-check
- R19C4_G9 claim boundary.

This is a complete science characterization, not an implementation failure.

## Provenance

The runner reports exact lock provenance:

- Repair19c3 result JSON SHA-256:
  `aa19480ce4d41f649368f192f27d85b823e0247aa6f9bcc9eb7a9d23b60ac5b0`;
- Repair19c3 execution HEAD:
  `8317c38c1f6f3df18dcb4106c9b81f7bc543ceaa`;
- Repair19c3 implementation blob:
  `08985f1ee334f038a7125cc239fb6b8929d428af`;
- Repair19c4 preregistration commit:
  `77a0b4977ee921d0693ad14880f38e5822d505a4`;
- Repair19c4 implementation blob:
  `f9965d55af274e601268b41ce325a540e881165d`;
- Repair19c4 implementation lock:
  `fda9e02a6db7e40bdb9959daa22fb85126d1e7dc`.

The execution began with

`NL1C7B4_REPAIR19C4_LOCK_PASS`.

## First-state reproduction and invariants

All six lambda=1 canonical cases reproduce the frozen Repair19c3 first accepted state exactly under the preregistered controls.

Across the six x1 states:

- exact-Q reconstruction remains within the frozen tolerance;
- Y4 and Qmean remain numerically zero at the expected floating-point scale;
- all nonprojection fields remain frozen;
- no candidate modifies the physical state definition.

Therefore the Repair19c4 result is not caused by provenance drift, gauge loss or field mutation.

## Independent directional references

All six canonical cases resolve the independent Richardson directional reference.

For every scale/grid case, the first stable adjacent reference pair is

`1e-5 -> 3e-6`.

The full-vector and momentum-block reference changes on that pair are:

- scale 5, Nr=256:
  `4.829988951081331e-6`;
- scale 5, Nr=512:
  `1.0786720564837396e-5`;
- scale 10, Nr=256:
  `3.765681761301229e-5`;
- scale 10, Nr=512:
  `4.29259139209544e-5`;
- scale 20, Nr=256:
  `1.1578841326197615e-5`;
- scale 20, Nr=512:
  `3.288764715872927e-5`.

All are far below the frozen reference-stability limit `5e-4`.

Thus the independent directional derivative is already stable on the scale containing the Repair19c3 control probe `3e-6`.

## Candidate Jacobian result

The Repair19c3 control candidate

`3-point, abs_step=3e-6`

has aggregate directional fidelity:

- maximum full mismatch:
  `5.039306870066481e-5`;
- maximum momentum mismatch:
  `5.039306870066483e-5`;
- median full mismatch:
  `2.1117784777920557e-5`;
- median momentum mismatch:
  `2.111778477792068e-5`.

The frozen lexicographic rule selects

`3-point, abs_step=1e-8`

with:

- maximum full mismatch:
  `4.242603857525267e-5`;
- maximum momentum mismatch:
  `4.2426038575252716e-5`;
- median full mismatch:
  `3.008493325792277e-5`;
- median momentum mismatch:
  `3.0084933257922777e-5`.

The selected candidate improves the worst-case full mismatch over the control by only a factor

`1.1877863310589492`

or approximately 15.8 percent.

It does not satisfy the preregistered required fivefold improvement.

Its median full mismatch is approximately 1.425 times larger than the control median.

## Material-window decision

The preregistered material-window checks evaluate as follows:

PASS:

- all six independent references resolve;
- a selected candidate exists;
- the selected candidate differs from the control;
- selected maximum full mismatch is <=1e-3;
- selected maximum momentum mismatch is <=1e-3.

FAIL:

- fivefold full-mismatch improvement;
- requirement that the control not already lie within both 1e-3 fidelity bounds.

In particular, the Repair19c3 control already has worst-case full and momentum directional mismatches near `5e-5`, approximately twenty times below the frozen `1e-3` fidelity limit.

Therefore Repair19c4 does not identify a materially better post-first-step finite-difference scale.

## Exact one-step behavior

The descriptive post-first-step probes reveal a second important fact.

The control post-first-step physical correction norms are:

- scale 5, Nr=256:
  `6.415431464959965e-12`;
- scale 5, Nr=512:
  `3.033235643927026e-11`;
- scale 10, Nr=256:
  `1.2272494859625228e-9`;
- scale 10, Nr=512:
  `1.6472728671952785e-9`;
- scale 20, Nr=256:
  `1.9166668082893804e-9`;
- scale 20, Nr=512:
  `2.719904933540006e-9`.

For the same control Jacobian, the exact frozen-residual ratios after the single full post-first-step correction are approximately:

- scale 5, Nr=256:
  `1.2598595021387533`;
- scale 5, Nr=512:
  `0.6662882774293986`;
- scale 10, Nr=256:
  `0.12216136872637669`;
- scale 10, Nr=512:
  `0.09481974487874786`;
- scale 20, Nr=256:
  `0.020842188048549405`;
- scale 20, Nr=512:
  `0.025998749277299983`.

The direct linear predictions for those same steps are many orders smaller.

For example, scale 5, Nr=256 predicts a relative residual of approximately

`1.2646521707255405e-8`

but the exact frozen residual ratio is approximately

`1.25986`.

Changing the finite-difference probe over the preregistered candidate range does not materially remove this discrepancy.

The discrepancy is strongest for the smallest physical corrections and becomes less severe for corrections of order `1e-9`.

## Scientific interpretation

Repair19c4 falsifies the specific working hypothesis that the Repair19c3 post-first-step stagnation is primarily caused by using a fixed `3e-6` finite-difference probe after the Newton correction becomes much smaller.

The Repair19c3 `3e-6` Jacobian is already an accurate directional approximation to the independent stable Richardson reference under the preregistered fidelity metric.

The remaining failure is therefore not explained by selecting a different finite-difference step.

At the same time, Repair19c4 does not establish physical insufficiency of the frozen `(L,R_t)` ansatz.

The data instead point to a distinction between:

1. a stable derivative measured over physical perturbations of order `1e-5--3e-6`; and
2. the realization of predicted residual cancellation under actual Newton corrections of order `1e-12--1e-9`.

The present evidence is consistent with a numerical resolution, conditioning, cancellation or discretized state-to-residual evaluation floor at those extremely small corrections.

Repair19c4 does not distinguish uniquely among those mechanisms and does not license another finite-difference step-scale search.

## Project decision

The frozen Repair19c4 decision boundary now applies.

Therefore:

- no further finite-difference scale diagnostic is licensed;
- no final Repair19c nonlinear closure rerun is licensed;
- the finite-difference Gauss-Newton solver-repair track terminates here;
- the historical `1e-7` exact constraint threshold is unchanged;
- Repair19c3 remains a nonlinear closure FAIL;
- eta=0 short-time evolution is not yet certified;
- finite eta is not yet certified;
- no observational AeST result is licensed from this track;
- no physical infeasibility claim for `(L,R_t)` is justified.

Any further initial-data work must be a project-level reformulation, not an extension of the Repair19c finite-difference tuning sequence.

Observational/data-side infrastructure may continue in parallel, but finite-eta observational interpretation remains gated by a defensible eta=0 initial-data/evolution path and a finite-eta observable construction.
