# NL1C7B4 Repair01 — raw nonlinear initial-constraint result

Status: **POST-RESULT / FROZEN**

Official run: `35212527939`.
Head SHA: `56aa4eda5318cb596ca311cb227ced93b69824bb`.
Artifact: `10493461020`.
Artifact SHA256: `0cd7ff857d2965915176563341a18d2979f82ebe3ea59be090459030018c1aa0`.

Final science classification:

`NL1C7B4_REPAIR01_RAW_INITIAL_CONSTRAINT_FAIL`.

## What passed

- The official C7A primary state is reproduced with maximum relative L2 error `2.8776273478160806e-14`, below the frozen `1e-12` reproduction limit.
- The symbolic nonlinear Exp-Q dictionary audit passes.
- All non-K action contributions are finite on the strict proof subsets.
- No state modification, Q linearization, K clipping, Y-branch selection, scale selection, nonlinear evolution, or finite-eta evolution was used.

## Decisive result

All `54 = 9 Y branches x 3 scales x 2 radial grids` cases fail the unchanged `1e-7` raw initial-constraint gate.

The rigorous log-domain lower bounds satisfy

- `min over cases max Hamiltonian lower bound = 1.0`,
- `min over cases max momentum lower bound = 1.0`.

The smallest retained log dominance gaps are

- Hamiltonian: `7.039082672011615e14`,
- momentum: `7.039082672011666e14`.

Thus the result is not a float64 overflow artifact. For the raw linear C7A field dictionary inserted directly into the exact nonlinear C6 invariant,

`Q = cosh(u) sigma + sinh(u) phi_r/L`,

the Exp K(Q) contribution dominates all finite non-K terms by an overwhelming margin. No cancellation with the retained GR, Y-sector, dust, or standard homogeneous background terms can satisfy the frozen constraint gate.

## Interpretation boundary

This result does **not** show that the AeST nonlinear model itself is inconsistent. It shows that the linear growing-mode dictionary used by C7A cannot be promoted to a nonlinear initial state by the naive substitutions `sigma = Q_bg + deltaQ_linear` and otherwise unchanged first-order fields.

The next admissible step is a separately preregistered nonlinear dictionary completion that preserves the certified CLASS scalar invariant `Q_target = Q_bg + deltaQ_C7A` exactly and modifies only the time derivative of phi by the exact inverse spherical invariant relation. Constraint solving or fitting is not licensed by this result.
