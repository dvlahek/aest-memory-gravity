# NL1C7B4 Repair04 result freeze — linear momentum interface audit

Status: **OFFICIAL RESULT / FROZEN**

Official run: `35223365082`

Head SHA: `d245a3658d8f7043a702f1a09a862d0b9d3bb7f8`

Artifact: `10498905089`

Artifact SHA256: `1192b25acc1099bd24ff07c1e0b58c448d946513c895307a7c364aa9cfe66f3f`

GitHub Actions conclusion: `success`

Science classification:

`NL1C7B4_REPAIR04_LINEARIZATION_NUMERICAL_FAIL`

## What passed

- exact C7A retained-state reproduction: max relative L2 error `0.0` against the official NPZ;
- symbolic Exp K(Q) dictionary identity: PASS;
- all 54 audit cases remain finite;
- exact action/state claim boundary is preserved: no state projection, no fitted coefficient/sign/scale factor, no dust-sign change, no radial standard-species insertion, and no evolution;
- the action-background scalar interface agrees exactly in Q:
  - `Q_CLASS = 0.0001000000000000555 Mpc^-1`,
  - `Q_action = 0.0001000000000000555 Mpc^-1`;
- the independent frame bridge is numerically sound:
  - max finite-difference vs analytic relative L2 error in E: `5.624872617199967e-09`,
  - max finite-difference vs analytic relative L2 error in X: `4.187777549779537e-09`,
  - max frame-vs-C7A relative L2 error in E: `4.694819804205312e-08`,
  - frame-vs-C7A relative L2 error in X: `0.0`.

## Why the preregistered tangent gate failed

The symmetric finite-difference tangent used steps `h = 0.04, 0.02, 0.01` with a frozen relative convergence limit `5e-4`.

The gate does not distinguish a nonzero first derivative from a term whose exact first derivative vanishes. This is visible directly in the term scaling:

- `AeST_E2` is marked active but its reported tangent norm scales approximately as `h^2`; the relative fine-vs-middle comparison is therefore about `0.75` in all cases even though the estimate is converging to zero;
- `AeST_EX` shows the same approximately `h^2` behavior and the same about-`0.75` relative comparison;
- `AeST_X2` and `AeST_J` are below the preregistered active-term threshold but show analogous higher-order decay;
- `AeST_K` converges cleanly, with worst fine-vs-middle relative L2 difference `1.0088679417732867e-08`;
- dust converges cleanly, with worst relative difference `5.003950222075851e-14`;
- `GR_kin` is genuinely finite-step limited at the selected steps: 45/54 active cases exceed the `5e-4` relative convergence gate, with worst value `0.003123670807929728`.

Consequently `all_tangents_converged = false` and the preregistered implementation classification is correctly `LINEARIZATION_NUMERICAL_FAIL`.

## Non-certifying diagnostic signal

The unconverged fine-step diagnostic still gives large normalized momentum residuals,

- `min max epsilon_M1 = 0.9475350072683298`,
- `max max epsilon_M1 = 0.9999999999996758`,

but this cannot be promoted to a scientific leading-order mismatch claim because the preregistered tangent-convergence gate failed.

At the fine step the largest-residual point is dominated by GR in 27 cases and AeST K in 27 cases. Therefore the previous Repair03 `AeST_nonK_nonJ` dominance is not reproduced by this unconverged tangent estimator.

## Interpretation boundary

Repair04 is a numerical diagnostic failure, not a physical closure failure and not a PASS of the linear momentum constraint. The result only shows that the chosen finite-difference tangent/convergence criterion is unsuitable for a mixture of exactly-zero first derivatives and nonzero first derivatives at the frozen step sizes.

No nonlinear evolution, finite-eta run, turnaround, or collapse calculation is licensed by this result.

The next checkpoint must be preregistered separately and should evaluate the first directional derivative without this ambiguity, preferably analytically/symbolically at lambda=0 (or with an equivalently locked zero-derivative-aware construction) before any physical interpretation of the momentum interface.
