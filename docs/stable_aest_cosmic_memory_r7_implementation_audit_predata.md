# Stable AeST cosmic-memory R7 — implementation audit before first result

Date: 2026-09-14

No R7 science result existed when this audit was recorded.

## Frozen preregistration

R7 preregistration was committed first at

`5d4c514799f22fe13cc0ecf9a0be4d3e2326a514`.

## Implementation-only diff

From the preregistration commit through the audited implementation, exactly two new executable files were added:

- `fullj_weyl/stable_aest_cosmic_memory_r7_lookback_decomposition.py`
- `fullj_weyl/run_local_stable_aest_cosmic_memory_r7_lookback_decomposition.sh`

No historical R2d, R2e, R5b, or R6a source/result file was modified.

## Source construction audit

The runner constructs a fresh disposable CLASS tree on every invocation from the frozen corrected parent commit `e85808324f51fc694d12e3ed7439552a3c3f9540`. It then prospectively applies, in order:

1. the certified stable-chi residual patch;
2. the existing R2b variational runtime infrastructure;
3. the existing R2d full-history direct-RHS trace patch;
4. the existing R2e single-hook correction.

The final tree is required to contain exactly one physical eta multiplication, exactly one physical memory closure, exactly one direct R2d trace call, exactly one external replay hook, and exactly one runtime external-force helper definition.

No historical mutable R2e/R5 CLASS tree is reused.

## Replay-process isolation

The runtime external-force helper caches its force table on first use. R7 therefore runs every baseline/replay case in a separate Python process. The eta-zero trace, the four full-history signed-amplifier cases, and all eight epoch signed-amplifier cases cannot share a cached force table.

## Force-table and epoch audit

The eta-zero R2d all-k trace is normalized to unique `(k,tau)` rows before replay. The normalized full table is kept on a single sorted k/tau grid.

Each of the four epoch tables keeps that exact same full row grid. Only the force column is masked to zero outside the preregistered redshift window. Consequently the decomposition does not alter k-grid support, tau-grid support, or the external helper's interpolation topology.

The driver checks the row-wise sum of the four masked force tables against the full table before any epoch result can pass.

## Observable audit

R7 reuses the R5b observable construction for

- sigma8(z),
- effective f sigma8(z),
- linear C_L^kappa-kappa,

with the same tau H0, memory order, tolerance, redshift grid, multipole range, canonical initialization anchor, and nonlinear/Halofit-off setting.

The full replay is independently required to reproduce the frozen physical R5b derivative-at-zero tangent before epoch decomposition can be certified.

## Claim discipline

The epoch fractions are not used as success thresholds. R7 can certify a decomposition even if the ancient contribution is small, negative, or partially cancels another epoch. No result-dependent threshold was introduced during implementation.