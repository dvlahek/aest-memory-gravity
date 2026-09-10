# NL1C6D2C4R1 derivative-control repair result

## Classification

`NL1C6D2C4R1_DERIVATIVE_CONTROL_REPAIR_PASS`

GitHub Actions run: `34438801676`.
Run head: `430190b8f98fe05958695a1b19085854e229c5b1`.
Branch: `v053-exp-normalization-corrected`.

The first R1 workflow run failed before any gate because the repository root was not on `sys.path`; commit `430190b8f98fe05958695a1b19085854e229c5b1` fixed only that import path. No physics formula, test point, step-size set, or tolerance changed.

## Frozen gate results

- inherited structural gates: all PASS (`background`, `tracking`, `deep-MOND`, local constitutive bound, high-gradient recovery);
- Y-direction finite-difference maximum relative discrepancy: `4.252626612129e-07` <= `2e-6`;
- Z-direction `h=1e-3`: maximum `6.087825935389e-07` <= `2e-6`;
- Z-direction `h=3e-4`: maximum `6.739998542175e-08` <= `2e-6`;
- Z-direction `h=1e-4`: maximum `6.480270144195e-08` <= `2e-6`;
- all three preregistered Z steps pass individually; no best-step selection was used.

The historical D2C4 identity classification remains FAIL. D2C4R1 establishes that the D2C4 analytic derivative formulas are consistent with numerically converged finite differences and licenses the next action-level nonlinear FLRW current/vector/constraint derivation. It does not license nonlinear branch evolution, memory, likelihoods, or NL1C7.
