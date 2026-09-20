# GE09 dense accepted-step local-jet bridge — implementation lock v2

## Status

This is the executable GE09 lock.

The first GE09 lock at commit
`e0c6e3c4bff50b23b117a87bd73f4d54d615e6ad`
was not executed. A pre-execution audit found that the already preregistered p3
perturbation precision values were not explicitly passed through
`Class.set()`.

No GE09 science result was inspected before this correction.

## Preregistration

Commit:

`823ffd1a9da8e103e4568044f0f3ceb29c374aac`.

Frozen preregistration blob:

`239a0296a25b3740e67c02759c1998560c37de4f`.

## Pre-execution correction

Commit:

`068b35d4f26caef07938b6177fc05458063367e5`.

File:

`docs/ge09_preexecution_precision_injection_correction.md`.

Frozen blob:

`e39e3f4f563521ef780e7799bb93fc8354a55a25`.

The only licensed change was explicit injection of

- `tol_perturb_integration = 5e-8`;
- `perturb_sampling_stepsize = 0.0025`.

## Diagnostic trace patch

Unchanged:

`ge09/apply_dense_accepted_step_trace_patch.py`.

Frozen blob:

`23b0cd22ebab499aee0ce03e6b3b678fe727ef55`.

## Corrected audit implementation

Commit:

`675da5b47499fb4d870d5bbc949a554cf53f292c`.

File:

`ge09/dense_accepted_step_local_jet_bridge.py`.

Frozen blob:

`f34b54d74bd4d913fdb6e61cd47903b1ddffe87f`.

## Frozen representation and gates

All representation choices and gates are identical to the original GE09 lock:

- successful NDF15 step endpoints with fresh physical RHS;
- 64 common uniform `ln(a)` nodes over `0.2<=z<=1.5`;
- CubicHermiteSpline for derivative-aware fields;
- PCHIP for algebraic/background fields;
- deterministic every-second-endpoint control;
- same six NL1C4 Fourier modes/phases;
- analytic spatial derivatives;
- CLASS trace identity <= `1e-12`;
- source-grid state validation <= `1e-4`;
- primary/control global relative L2 <= `5e-4`;
- primary/control pointwise abs-or-rel <= `2e-3`;
- scalar pt identity <= `1e-12`;
- finite complete jet.

## Classification

- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_PASS`;
- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.

## Project boundary

Even PASS does not license Z20. The separately frozen GE08 Repair01
standard-matter incompleteness remains active.
