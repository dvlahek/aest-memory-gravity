# NL1C1 result — full AeST Y-sector interpolation/operator bridge

Final classification: **NL1C1_FULL_Y_OPERATOR_BRIDGE_PASS**

Predata: `docs/nl1c1_predata_full_y_operator_bridge.md`.

Workflow commit: `737a3f26b2016898e22a8909add7737a84315327`.

A first workflow attempt failed only in the predata-audit string check because the workflow referenced `NL1C1_LINEAR_STATE_HIGH_GRADIENT_REGIME` instead of the actual preserved predecessor classification `NL1C0_LINEAR_STATE_HIGH_GRADIENT_REGIME`. No numerical operator result was produced in that attempt.

A second attempt reached the operator calculation. All 1D and 3D operator gates passed, but the coefficient audit failed only for the Sharp interpolation at `beta0=0.1` because direct evaluation of

\[
\frac{\beta_0x+(1+\beta_0)-|\beta_0x-(1+\beta_0)|}
{2\beta_0(1+\beta_0)}
\]

at `x=1e10` suffered floating-point cancellation. This was a numerical representation issue, not a change of the frozen function or gate. The implementation was replaced by the algebraically identical stable piecewise form

\[
j_H(x)=\min\left(\frac{x}{1+\beta_0},\frac1{\beta_0}\right),
\]

commit `84a93ae47df868958441d8271989f5d7195622e3`.

Final GitHub Actions run: `34325827481` — technical SUCCESS.

Artifact: `results_bundle_nl1c1_full_y_operator_bridge`, artifact ID `10093701558`, SHA256 `6b889b68a99e70cba5c46afb7679182d925554f44a3e66590e42e3962b94b18b`.

Scope: operator/interpolation audit only. No physical-amplitude cosmological nonlinear evolution, finite-eta nonlinear prediction, halo calculation, likelihood, or observational data were used.

## Frozen co-primary family

All nine combinations were retained:

- interpolation: `Simple`, `Exponential`, `Sharp`;
- `beta0 in {1, 0.5, 0.1}`.

No combination was selected after the result.

## Final gates

All three aggregate gates passed:

- `coefficient_checks_all_nine = true`;
- `operator_1d_all_nine = true`;
- `operator_3d_all_nine = true`.

Thus

\[
\boxed{\mathrm{NL1C1\_FULL\_Y\_OPERATOR\_BRIDGE\_PASS}}
\]

## Numerical margins

Across all nine co-primary combinations:

- maximum 1D variational-identity relative error: `1.9542824118907006e-16`;
- maximum translation relative error: `9.503402109724926e-14`;
- constant-field null maximum: `0.0`;
- maximum `N=512` vs `N=1024` low-mode relative error: `1.5734404955313445e-4`, below the `5e-4` gate;
- maximum deep-MOND reduction error at `x_rms=1e-6`: `1.040826607598449e-6`, below the `1e-4` gate;
- maximum 3D variational-identity relative error: `2.1201412128067292e-16`;
- maximum 3D axis-permutation relative error: `1.7128025695997837e-15`.

The coefficient limits also pass for every interpolation/beta0 pair. At `x=1e10`, the stable Sharp implementation reaches the exact high-gradient coefficient `1/beta0`; the Simple and Exponential forms satisfy the preregistered high-limit tolerance as well.

## Interpretation

NL1C1 validates the full published Y-sector interpolation operator across the complete preregistered interpolation/beta0 family. Together with NL1C0, this establishes that the physical-amplitude late-time state must be treated with the full/high-gradient Y-sector rather than the deep-MOND `Y^(3/2)` truncation.

This does **not** yet provide a self-consistent physical-amplitude cosmological solution. The next strong-path task is therefore to construct a baseline with the full Y-sector active and then compute the eta=0 memory tangent around that baseline using the frozen NL0B memory action.

Historical v0.77/v0.78 PASS results and all earlier FAIL classifications remain unchanged.
