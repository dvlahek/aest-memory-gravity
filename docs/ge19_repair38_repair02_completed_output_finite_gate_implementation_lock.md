# GE19 Repair38 repair02 completed-output finite-gate implementation lock

## Status

Repair38 repair02 is frozen before its first local execution.

Repair02 changes only the finite-output implementation gate that was shown to
inspect uninitialized np.empty mode slots in Repair38 repair01.

The Repair38 preregistration, H4 source, projected boundary, propagation
equation, Radau tableau, endpoint-domain repair01 fix, thresholds and
diagnostic routes are unchanged.

## Repair01 implementation failure

Freeze file:

`docs/ge19_repair38_repair01_false_nonfinite_implementation_fail_freeze.md`.

Freeze blob:

`97361f32eb2deac2a74c1672810bf2310baf7fec`.

Frozen artifacts:

- JSON SHA-256:
  `38ba963eaaa4dad49aa876299f6a33e11d843b24ac555f74a7e586bb4ceb3240`;
- NPZ SHA-256:
  `aff63771c1800b0db236cd020cf0d2772f6d9a0fd0328573d055392f2c60da67`;
- FULL SHA-256:
  `38ba963eaaa4dad49aa876299f6a33e11d843b24ac555f74a7e586bb4ceb3240`;
- outer runner SHA-256:
  `66bbc767144824b1356880d9da9ebf9ddc30fe46631377ca9d7d20f32c3f3c28`.

Repair01 remains IMPLEMENTATION_FAIL and is not relabelled.

## Repair02 implementation

Implementation file:

`ge19/repair38_frozen_source_radau_substep_localization.py`.

Repair02 commit:

`5d48eada0ea7e79dd7b959c9016f16bd098daa80`.

Repair02 blob:

`df485d3c4752b96b2dae96ef9fa7d77b686fe158`.

The only code change is the finite-output check:

- inside the per-mode loop, only the just-computed `Y`, `state`,
  `mtr`, `atr`, and `scr` are inspected;
- after all modes for a C tag are filled, the completed `st`, `mt`,
  `at`, and `sc` arrays are inspected.

No future uninitialized `np.empty` slots are included in the gate.

Independent inspection of the frozen repair01 NPZ found zero nonfinite
entries in every saved numeric array.

## Audits

Static audit after repair02 implementation:

- run:
  `35861843358`;
- conclusion:
  `success`.

Updated dedicated Repair38 prelock:

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

The updated prelock explicitly verifies the completed-output finite-gate
repair while retaining the repair01 endpoint-domain checks.

## Expected classification boundary

Repair02 must still reproduce factor 1 exactly before any diagnostic routing
is interpreted.

If all implementation gates pass, the emitted Repair38 JSON may route to one
of the preregistered diagnostic outcomes:

- `RADAU_PROPAGATION_FLOOR_CONFIRMED`;
- `PROPAGATION_ACCURACY_DEPENDENCE_CONFIRMED`;
- `PCHIP_OR_OTHER_FLOOR_REMAINS`.

Repair38 remains diagnostic-only and cannot certify Z21 or license lensing.
