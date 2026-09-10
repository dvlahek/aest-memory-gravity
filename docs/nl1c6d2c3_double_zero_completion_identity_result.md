# NL1C6D2C3 double-zero completion identity result

## Classification

`NL1C6D2C3_DOUBLE_ZERO_COMPLETION_IDENTITY_FAIL`

GitHub Actions run: `34438336316`.
Run head: `2254c0d310b8efb5099fa933a20da2fa04c8dcb6`.
Branch: `v053-exp-normalization-corrected`.

## Frozen gate results

- C3.1 corrected homogeneous slice: PASS. Maximum normalized discrepancy `0`.
- C3.2 tracking value/first-derivative slice: PASS. Maximum normalized discrepancy `2.771263564569e-16`.
- C3.3 deep-MOND subleading behavior: FAIL. Maximum final mixed/base action-density ratio at the preregistered final point is `2.991007520243e-03`, above the frozen `5e-4` gate.
- C3.4 high-gradient boundedness: FAIL. Minimum coefficient ratio is `6.509010159355e-01`, below the frozen lower bound `0.75`; maximum is `1.249999887465`.
- C3.5 analytic derivative control: PASS. Maximum relative discrepancy `1.075939388999e-06`, below the frozen `2e-6` gate.
- C3.6 scope: PASS. No nonlinear FLRW evolution, solver modification, memory/likelihood, refit, or branch selection.

## Interpretation

The double-zero replacement `G_2(Z)=tanh^2 Z` successfully fixes the D2C2 tracking-derivative problem: the completion preserves `F`, `F_Y`, and `F_Q` at `Q=Q0`. The remaining failure is in the chosen spatial mixed-action shape `B(Y)=Y^2/(a0^2+Y)`: it is not sufficiently subleading at the preregistered deep-MOND points, and its additive `F_Y` correction can push the finite-x coefficient below the frozen high-gradient lower bound before the base interpolation has fully saturated.

This is a completion-family FAIL, not an AeST physical exclusion and not a numerical solver failure. Historical D2C2 and D2C3 classifications remain unchanged. D2C3 does not license the action-level nonlinear FLRW derivation.
