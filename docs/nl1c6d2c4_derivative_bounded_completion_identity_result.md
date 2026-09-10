# NL1C6D2C4 derivative-bounded completion identity result

## Classification

`NL1C6D2C4_DERIVATIVE_BOUNDED_COMPLETION_IDENTITY_FAIL`

GitHub Actions run: `34438584309`.
Run head: `61d8f854c5e39e9cb49f5900ed8edc2e58c04e22`.
Branch: `v053-exp-normalization-corrected`.

## Frozen gate results

- C4.1 corrected homogeneous slice: PASS. Maximum normalized discrepancy `0`.
- C4.2 tracking Euler-Lagrange slice: PASS. Maximum normalized discrepancy `2.771263564569e-16`.
- C4.3 deep-MOND subleading behavior: PASS. Maximum final mixed/base ratio `1.359433619617e-07`, below `5e-4`.
- C4.4 local constitutive boundedness: PASS. Range `[0.7500001125354, 1.249999887465]` within the frozen `[0.75,1.25]` bound.
- C4.5 high-gradient recovery: PASS. Worst base asymptotic error `1.099987900144e-05 <= 2e-5`; worst mixed-modulation error `2.500222251456e-13 <= 1e-10`.
- C4.6 finite-difference derivative control: FAIL. Maximum relative discrepancy `5.037472089274e-06`, above the frozen `2e-6` gate.
- C4.7 scope: PASS.

## Interpretation

The new derivative-bounded completion fixes the two substantive D2C3 shape failures without changing `epsilon_mix=0.25` or relaxing the inherited deep-MOND bound. All exact slice, asymptotic, and boundedness checks pass. The only blocker is the finite-difference derivative diagnostic. No threshold is changed. Before any new completion family or action-level evolution is considered, a step-size/convergence diagnostic must determine whether C4.6 indicates an analytic derivative error or numerical differentiation/quadrature error.

This historical D2C4 classification remains FAIL regardless of later diagnostics.
