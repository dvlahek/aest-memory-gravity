# Stable AeST cosmic memory R8b — implementation audit before first result

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Frozen science lock

R8b preregistration was locked before implementation in:

`26ad0f310e0cc203c3350330a17e6822771515a0`

Frozen parents remain:

- R7a post-data: `86c03e6ba2ee9fcbf33a9d319d12ae778a747881`;
- R8a2 post-data: `590dbc69e2823f583b157af2297e357991103c47`.

No R8b result had been generated or inspected before the implementation below was committed.

## Diff audit

Comparison from the preregistration lock `26ad0f310e0cc203c3350330a17e6822771515a0` to implementation head `ab5ad994b6f21c14fd50db8b7de1271e20a0d820` contains exactly two added files:

1. `fullj_weyl/stable_aest_cosmic_memory_r8b_two_tau_lookback.py`;
2. `fullj_weyl/run_local_stable_aest_cosmic_memory_r8b_two_tau_lookback.sh`.

No historical result, parent driver, source patch, science threshold, tau endpoint, epoch boundary, eta value, or observable definition was changed after preregistration.

## Implementation scope

The driver performs exactly the preregistered tau1.25 live physical decomposition:

- `full` eta=0;
- `full` eta=+-0.025;
- `full` eta=+-0.05;
- four frozen epoch modes at eta=+-0.025.

Total planned R8b runs: 13.

The runner builds a fresh disposable CLASS source from frozen parent `e85808324f51fc694d12e3ed7439552a3c3f9540`, applies the certified stable-chi patch, removes exactly one dormant historical external tangent hook, applies the existing R7a live epoch/signed-eta diagnostic patch, and verifies zero R2d trace/replay hooks.

## Parent-hash lock

The implementation checks exact frozen parent hashes:

- R7a JSON `94977acfe47f3f58337ce45dd8df982cd04ff6459434ed9780e229623bc92c0b`;
- R7a NPZ `cc3e9b70809c44c8154abfc4cd3961d5f785f5cd3b327def2666e39bec789771`;
- R8a2 JSON `2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66`;
- R8a2 NPZ `c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1`.

## Claim discipline

The implementation contains no gate on the sign or direction of temporal redistribution between tau10 and tau1.25. The measured differences in signed projection fractions, norm shares, epoch amplitudes, and cross-tau epoch cosines are descriptive science outputs only after all preregistered certification gates pass.
