# GE19 Repair38 repair01 false-nonfinite implementation failure freeze

## Status

The first Repair38 repair01 local execution emitted a complete diagnostic JSON
but routed to IMPLEMENTATION_FAIL solely because the implementation's
all_outputs_finite gate inspected uninitialized np.empty slots inside the
per-mode loop.

This is an implementation/audit failure. It is not a valid Repair38
propagation result and does not relabel Repair37.

## Frozen artifacts

Canonical JSON:

- SHA-256:
  `38ba963eaaa4dad49aa876299f6a33e11d843b24ac555f74a7e586bb4ceb3240`;
- bytes:
  `4273`.

NPZ:

- SHA-256:
  `aff63771c1800b0db236cd020cf0d2772f6d9a0fd0328573d055392f2c60da67`;
- bytes:
  `16161137`.

Repair01 FULL log:

- SHA-256:
  `38ba963eaaa4dad49aa876299f6a33e11d843b24ac555f74a7e586bb4ceb3240`;
- bytes:
  `4273`.

Outer runner log:

- SHA-256:
  `66bbc767144824b1356880d9da9ebf9ddc30fe46631377ca9d7d20f32c3f3c28`;
- bytes:
  `7076`.

## Frozen classification

`GE19_REPAIR38_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION_IMPLEMENTATION_FAIL`.

Route:

`IMPLEMENTATION_FAIL`.

Factor-1 reproduction nevertheless passed exactly:

- Z21 global relative L2 = `0.0`;
- shift metric global relative L2 = `0.0`;
- projected p0 exact = `true`;
- frozen active sample count = `23850`.

All Lambda stage rho values were finite.

## Observed propagated metrics

These values are frozen as emitted but must not be promoted to a valid
Repair38 diagnostic conclusion until the implementation gate is repaired.

Substep 1:

- Linf = `1.1749387207106255e-6`;
- RMS = `1.0515104304068532e-6`.

Substep 2:

- Linf = `1.341600178925417e-6`;
- RMS = `1.1859570854138313e-6`.

Substep 4:

- Linf = `1.3797699672147026e-6`;
- RMS = `1.2040175184159568e-6`.

The emitted convergence ratios were greater than one, but the run remains an
implementation failure and these values are not yet a valid routing result.

## Root cause

Inside `run_factor`, the arrays

- `mt=np.empty(...)`;
- `at=np.empty(...)`;
- `sc=np.empty(...)`

are filled one Fourier mode at a time.

The finite gate was evaluated inside that mode loop as

`np.all(np.isfinite(mt))`,
`np.all(np.isfinite(at))`,
`np.all(np.isfinite(sc))`.

At that point future mode slots remain uninitialized `np.empty` memory.
Therefore the gate can depend on arbitrary allocator contents. Factor 1
happened to observe finite uninitialized bytes, while factors 2 and 4 did not.

Independent inspection of the frozen NPZ confirms that every saved numeric
array is finite after completion. Thus the false gate is not evidence of a
physical-state divergence.

## Licensed repair

Repair38 repair02 may change only the finite-output implementation check:

- inside the mode loop, inspect only the newly computed `Y`, `state`,
  `mtr`, `atr`, and `scr`;
- after all modes for a C tag are filled, check the completed `st`, `mt`,
  `at`, and `sc` arrays.

No source, propagation equation, substep coordinate, threshold, diagnostic
route, parent, or physical assumption may change.

## Claim boundary

Repair37 remains historical valid FAIL.

Repair38 repair01 is an implementation failure only.

Z21 remains uncertified and lensing remains blocked.
