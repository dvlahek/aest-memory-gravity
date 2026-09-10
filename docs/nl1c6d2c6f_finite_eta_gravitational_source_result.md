# D2C6F result — finite-eta direct gravitational source

Date: 2026-09-10

Parent implementation head: `df953b9df86ee0b4d73d1691aa713535e27e57fa`.

Final classification:

`NL1C6D2C6F_FINITE_ETA_DIRECT_GRAVITATIONAL_SOURCE_FAIL`

This FAIL is retained as a historical result. It must not be relabeled after follow-up work.

## What passed

The direct metric-source implementation derived from the frozen NL0B/NL1C3B action passed its finite-difference and z-to-q bridge audits:

- metric-source finite-difference maximum relative error: `2.594848457787e-10`;
- spectral z-to-q bridge relative L2: `6.967305905863e-15`.

All 81 primary finite-eta trajectories were healthy. The retained scalar-current constraint stayed at approximately `1e-15` to `1e-14`, `min(1+j_eff)` remained positive, and the completed-square energy identity was satisfied at approximately `1e-17`.

The D2C6E retained-trajectory regression was exact to printed precision:

- state relative L2: `0`;
- E relative L2: `0`.

Time and space source convergence passed with very large margin:

- worst time-source convergence: `5.625224438237e-07` (gate `2e-3`);
- worst space-source convergence: `1.906043361904e-06` (gate `5e-3`).

The direct gravitational source is nonzero and scales smoothly with eta. Source amplitude, sign, eta scaling and completion spread were non-gating diagnostics.

## Why the formal gate failed

Only F6 failed:

- worst 39-mode versus 47-mode bath-order source difference: `2.439247041718e-02`;
- frozen F6 gate: `1e-2`.

The failures are localized to the `beta0=0.1` members with `sigma=0` or `sigma=+1`, for all three completion kinds. The dominant discrepancy is the direct spatial metric source `S_Phi`.

For `sigma=0, beta0=0.1`, the worst 39/47 source difference is approximately `1.275185e-02`. For `sigma=+1, beta0=0.1`, it is approximately `2.439247e-02`. In the latter sector the component differences are approximately:

- `S_Phi = 2.439247e-02`;
- `S_b = 1.428461e-02`;
- `S_Psi = 7.42635e-04`;
- `S_shear = 2.16618e-06`.

The same trajectories remain healthy, and time/space convergence remain excellent. Therefore the observed failure is specifically a bath-discretization/source-convergence failure, not a demonstrated physical instability or action-level inconsistency.

## Interpretation

The 39- and 47-mode positive compressed baths were originally selected to reproduce the scalar memory response. D2C6F is the first test of quadratic direct metric-stress observables, which can be more sensitive to bath quadrature and cancellation. The original 39/47 F6 failure cannot be repaired by changing the `1e-2` gate.

A clean follow-up must instead evaluate the unresolved six members against a direct, non-fitted tan-Gauss-Legendre Drude quadrature sequence fixed before those follow-up results are generated.

Until that source-convergence follow-up passes:

- `SELF_CONSISTENT_WEAKFIELD_FEEDBACK_STEP_LICENSED=False`;
- `OBSERVATIONAL_STEP_LICENSED=False`.
