# NL1C7B4 Repair05 result freeze — analytic linear momentum identity

Status: **OFFICIAL RESULT / FROZEN**

Official run: `35225084320`

Head SHA: `cfb43b99162db1b8cf25621d3de795b42e1e2cf9`

Artifact: `10498343763`

Artifact SHA256: `5798127479d0a359b5805aa7bd846caee035e582b0fdb3a08b7cd7ab2dc2e9ce`

GitHub Actions conclusion: `success`

Science classification:

`NL1C7B4_REPAIR05_IMPLEMENTATION_FAIL`

## What passed

- exact retained C7A state reproduction: max relative L2 error `0.0`;
- symbolic Exp K(Q) dictionary identity: PASS;
- analytic-zero checks for the first-order `AeST_E2`, `AeST_EX`, `AeST_X2`, and `AeST_J` contributions: PASS in all 54 cases;
- E/X bridge: PASS on both radial grids and all three scales;
- maximum E action-vs-C7A relative L2 difference is about `4.695e-8` and X action-vs-C7A is exactly `0.0` in the retained evaluation;
- all 54 analytic cases are finite.

The analytic linearized momentum diagnostic gives

- minimum across cases of `max epsilon_M1`: `0.9478946803681939`;
- maximum across cases of `max epsilon_M1`: `0.9999999999919015`;
- minimum RMS epsilon_M1: `0.15127943352019685`;
- maximum RMS epsilon_M1: `0.5136360686047684`;
- dominant group at the maximum residual: `AeST_K` in `54/54` cases.

These values are diagnostic only because the preregistered implementation/grid gate did not fully pass.

## Grid-control result

The frozen grid-control limit is `0.02` and is not changed post-result.

- `R_sigma = 5 h^-1 Mpc`: relative 256-to-512 RMS difference `0.00038174750856598093` — PASS;
- `R_sigma = 10 h^-1 Mpc`: relative difference `0.003925028513139048` — PASS;
- `R_sigma = 20 h^-1 Mpc`: relative difference `0.026137957486093634` — FAIL against the unchanged `0.02` limit.

The 20-Mpc result is independent of Y family and beta0 in this linear audit, so all nine 20-Mpc Y/beta pairs fail the same grid-control gate.

Therefore `grid_control_pass = false`, which forces the preregistered science classification to `NL1C7B4_REPAIR05_IMPLEMENTATION_FAIL` even though the analytic-zero, bridge, state-reproduction, and finiteness gates pass.

## Interpretation boundary

Repair05 is a numerical/grid-convergence implementation failure, not a certified physical leading-order mismatch and not a PASS of the radial momentum constraint.

The very large analytic residual and the `AeST_K` dominance in all 54 cases are strong diagnostics, but they cannot be promoted to the preregistered `ANALYTIC_LEADING_ORDER_INTERFACE_MISMATCH` classification until the same unchanged grid threshold passes.

No threshold relaxation, fitted coefficient, sign change, state projection, radial standard-species insertion, nonlinear evolution, or finite-eta calculation is authorized by this result.

The next checkpoint should retain the same analytic evaluator and the same `0.02` grid threshold while adding higher radial resolution, especially for `R_sigma = 20 h^-1 Mpc`, to determine if the analytic linear momentum result converges before any physical interpretation.
