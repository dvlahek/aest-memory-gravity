# NL1C6D2C2 A1 derivative-level preservation result

## Classification

`NL1C6D2C2_CORRECTED_COVARIANT_A1_DERIVATIVE_FAIL`

GitHub Actions run: `34437731332`.
Branch: `v053-exp-normalization-corrected`.
Run head: `77db0e655193583361fef1136d4f33ab2886e782`.

## Gate results

- A1.1 analytic derivative / finite-difference control: FAIL numerically at `1.171757174081e-06` versus the preregistered `1e-6` threshold. This marginal finite-difference miss is retained as recorded and is not retuned.
- A1.2 homogeneous FLRW preservation: PASS with zero reported discrepancy.
- A1.3 quasistatic tracking equation-level preservation: HARD FAIL. Maximum normalized discrepancy is exactly `1.0`; there are 72 deterministic co-primary cases with nonzero `F_Q(Y,Q0)`.
- A1.4 homogeneous shift-charge regression: PASS with zero reported discrepancy.
- A1.5 scope: PASS; no solver or physical evolution was performed.

## Analytic reason for the hard failure

The frozen D2C2 mixed control is

\[
\Delta F_\sigma=\sigma\epsilon(2-K_B)\lambda_s B(Y)\tanh Z,
\qquad Z=(Q-Q_0)/Z_0,
\]

with `B(Y)=Y^2/(a0^2+Y)`. Although `tanh(0)=0`,

\[
\partial_Q\Delta F_\sigma\big|_{Q_0}
=\sigma\epsilon(2-K_B)\lambda_s\frac{B(Y)}{Z_0},
\]

which is nonzero for finite `Y` and `sigma=+/-1`.

Equality of `F(Y,Q0)` alone is therefore insufficient to preserve the inherited quasistatic field equations. `F_Q` enters the scalar shift current directly and also enters the aether Euler-Lagrange equation through variation of `Q=A^mu nabla_mu phi`.

## Interpretation

This is a theory-completion preservation failure, not a numerical R3 solver failure and not a physical exclusion of AeST. Historical D2C2 A0 remains a valid structural PASS for the quantities it preregistered and tested; A1 adds the stronger derivative-level requirement and rejects the `tanh Z` nonseparable completion family.

No retuning of the D2C2 family is permitted. Any replacement mixed completion must be introduced as a separately preregistered model-completion phase and must preserve both the function and the first equation-level derivatives on the homogeneous and tracking slices before nonlinear FLRW evolution is considered.
