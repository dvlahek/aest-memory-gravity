# AeST Memory Gravity

Research code and validation harness for an AeST-based history-dependent gravitational memory model, developed on the `physics-first-gravitational-elasticity` branch.

The active physical interpretation is a **Maxwell-type gravitational viscoelastic medium**. The AeST Y sector supplies the static / gradient-dependent modified-gravity response and the NL0B memory sector supplies the history / rate-dependent response.

## Current GE19 recovery point — 2026-10-10

For the current scientific state, resume from:

- `docs/CURRENT_GE19_STATUS.md`
- `docs/ge19_history_2026-10-10.md`
- older persistent chronology: `docs/ge19_history.md`

Historical classifications are immutable. A later repair never relabels an earlier FAIL.

## Active corrected-Y weakly nonlinear chain

The current action-completed parent route is:

```text
Repair13 reduced background/H1
        ↓
continuous H1 / X10 / GE05 bath closure (D47-D55 route)
        ↓
D56 nonanalytic-Y action correction
        ↓
H3F corrected-Y Z20 CERTIFIED
        ↓
H3G corrected-Y q20 PASS
        ↓
H4F3B corrected six genuine H4 sources PASS
        ↓
H4F3D operator + all-parent Ward closure
        ↓
final Z21 science solve
        ↓
lensing only if Z21 passes
```

Current certified corrected parents:

- `GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED`
- `GE19_H3G_CORRECTED_Y_Q20_RECONSTRUCTION_PASS`
- `GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN`

The full H4 Ward/Noether identity is **not yet certified** and Z21/lensing are still blocked.

## Immediate remaining gates

Only three substantive gates remain on the active route:

1. exact background on-shell elimination of the unknown-state factors `E00*dchi(F21)` and `L21*E_L00-b21*E_b00` without assigning or solving `F21/L21/b21`;
2. one integrated actual common-grid H4 source + linear-operator + all-parent + boundary Ward test;
3. if that Ward test PASSes, one final action-completed Z21 solve using the unchanged original gate
   `H4_active_shift_Nt128_Linf <= 1e-6`.

Lensing becomes the next natural observable only after the final Z21 gate passes.

## Hard scientific rules

- Never relax the original `1e-6` H4 gate.
- Never tune the theory to observations.
- Never fit missing source coefficients.
- Never introduce ad hoc normalization factors.
- Never relabel historical failures.
- A sampled, source-only, restricted, conditional or clock-grid PASS is not a full H4 Ward certificate.
- Old frozen-H4 artifacts remain provenance, not active corrected-Y parent inputs.

## Important historical controls

The following remain immutable negative or diagnostic results:

- Repair37 old frozen-H4 science failure;
- Cr12ac coherent-M2 robust old-frozen-H4 failure;
- D22A parent-candidate failure under its original representation;
- historical implementation failures and subsequent repair versions throughout the H4F3D forensic chain.

The D22-D41 route later localized major low-mode numerical source-representation issues and achieved a full 128-node / 30,720-case shift replay with no observed original shift-gate failures in its declared numerical scope. This does not replace the full H4 Ward test.

## Canonical physical interpretation

The canonical memory sector may be viewed as a completed-square auxiliary-field realization with elastic mismatch

`e_j = sqrt(eta w_j) X - omega_j U_j`.

Gravity changes `X`, the internal modes cannot follow instantaneously, and the mismatch stores and returns elastic memory. For the positive Drude continuum,

`K(A)=A/(1+A)`

and for `H=0`,

`tau dB/dt + B = tau dX/dt`,

which gives the Maxwell-type viscoelastic interpretation.

Relevant interpretation documents:

- `docs/gravitational_elasticity_canonical_nl0b_interpretation.md`
- `docs/gravitational_maxwell_viscoelasticity.md`

## Repository organization

- `ge01` ... `ge19`: staged theory / numerical validation code.
- `docs/`: result freezes, implementation locks, scientific history and current recovery checkpoints.
- `docs/archive/`: superseded navigation/theory notes that are kept only for provenance.
- `results/`: local result products and scientific artifacts. Many large result artifacts are intentionally not treated as general source files.

Archive policy: `docs/archive/README.md`.

## Legacy CLASS line

The v0.18/v0.19 CLASS integration and finite-eta numerical studies remain part of the project history. They are not the active GE19 weakly nonlinear frontier. The old top-level `THEORY_v018.md` note has been moved to `docs/archive/THEORY_v018.md`.

The current theory work should be resumed from the GE19 recovery documents above, not from the legacy CLASS checkpoint.
