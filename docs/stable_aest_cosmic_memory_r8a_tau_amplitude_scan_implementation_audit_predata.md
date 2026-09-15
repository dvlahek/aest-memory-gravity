# Stable AeST cosmic memory R8a — implementation audit before results

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Frozen preregistration

R8a was preregistered before implementation in commit

`01e6a0adaee514bf859b7730f2784eb3832e02b1`.

Immediate physics parent:

- R7a post-data checkpoint `86c03e6ba2ee9fcbf33a9d319d12ae778a747881`,
- classification `STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED`.

Frozen parent artifact hashes used by the R8a driver/runner:

- R7a JSON SHA-256 `94977acfe47f3f58337ce45dd8df982cd04ff6459434ed9780e229623bc92c0b`,
- R7a NPZ SHA-256 `cc3e9b70809c44c8154abfc4cd3961d5f785f5cd3b327def2666e39bec789771`.

## Diff audit

Comparing preregistration `01e6a0ad...` to implementation head `903b9645...` gives exactly two added files:

1. `fullj_weyl/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.py`
2. `fullj_weyl/run_local_stable_aest_cosmic_memory_r8a_tau_amplitude_scan.sh`

No historical result, post-data document, prior driver, prior source patch, or threshold file was modified.

## Frozen implementation checks

The R8a implementation hard-codes:

- `TAUS = (10.0, 5.0, 2.5, 1.25)`,
- primary central difference `eta = +/-0.025`,
- control central difference `eta = +/-0.05`,
- one eta-zero baseline at every tau,
- epoch mode fixed to `full`,
- memory order 20,
- tolerance `3e-8`,
- linear observables only; nonlinear/Halofit disabled.

The runner always rebuilds a fresh disposable CLASS source from frozen parent `e85808324f51fc694d12e3ed7439552a3c3f9540`, applies the certified stable-chi patch, neutralizes exactly one dormant historical external tangent hook, applies the already-certified R7a live physical source construction including the signed-eta parser diagnostic repair, and requires zero R2d trace hooks and zero external replay hooks.

No force table, history replay, ACT likelihood, or observational data enter R8a.

## Gate audit

The driver implements only the preregistered gates:

- provenance/parent lock,
- direct physical source topology,
- all 20 runs finite plus eta-zero identity,
- tau10 bridge to frozen R7a direct derivative,
- central derivative consistency at every tau,
- finite nonzero response at every tau.

Amplitude ratios and cosine-to-tau10 values are recorded only after derivatives are constructed. They do not enter classification. No monotonicity condition is implemented.

## Status

At this checkpoint no R8a result has been generated or inspected.
