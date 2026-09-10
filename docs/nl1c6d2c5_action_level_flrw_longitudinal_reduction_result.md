# NL1C6D2C5 action-level FLRW longitudinal reduction result

## Classification

`NL1C6D2C5_ACTION_LEVEL_FLRW_LONGITUDINAL_REDUCTION_PASS`

`NONLINEAR_BRANCH_EVOLUTION_LICENSED=True`

This result closes the preregistered D2C5 action-level reduction only within the frozen MOND weak-field ordering. It does not itself constitute a nonlinear cosmological trajectory, nonlinear matter evolution, memory result, observational likelihood result, or NL1C7 authorization.

## Provenance

- Repository branch: `v053-exp-normalization-corrected`.
- Actions run: `34439917817`.
- Run head: `debd4eacdff07cfbdd0a8ba8e9dfc6823743cd25`.
- Workflow: `NL1C6D2C5 action-level FLRW reduction`.
- Workflow conclusion: `success`.
- Preregistered derivation target: `docs/nl1c6d2c5_predata_action_level_flrw_longitudinal_reduction.md`.
- Action-level derivation: `docs/nl1c6d2c5_action_level_flrw_longitudinal_derivation.md`.

## Frozen gate results

The Actions log reported:

- A5.1 covariant geometry/order audit: maximum discrepancy `1.018846703718e-16`, PASS.
- A5.2 scalar/vector reduced-action versus covariant-current audit: maximum discrepancy `0.0`, PASS.
- A5.3 zero-expansion D1A regression: maximum discrepancy `1.522270386341e-16`, PASS.
- A5.4 fixed-a full-J/R3 operator regression: maximum discrepancy `1.474780063071e-15`, PASS.
- A5.5 corrected CLASS linearization: completion discrepancy `0.0`, CLASS mapping discrepancy `4.629127056437e-16`, PASS.
- A5.6 metric Hamiltonian/momentum/shear closure: power-counting and source anchors both PASS.
- A5.7 corrected D2AC matter convention: PASS.
- A5.8 scope: no nonlinear trajectory, finite eta, memory forcing, likelihood, refit, or branch selection was performed in D2C5.

All numerical/algebraic gates are therefore far inside the preregistered `1e-12` bound where applicable.

## Derived system licensed for the next stage

With

\[
\chi=\varphi+\bar Q\alpha,\qquad E=\dot\alpha+\Psi,
\]

\[
U=\dot\chi-\bar Q E-\dot{\bar Q}\alpha,
\]

and

\[
Y=a^{-2}|\nabla\chi|^2,
\]

D2C5 established

\[
P_\chi=2a^3K_{QQ}U,
\]

\[
P_\alpha=-2a^3\bar QK_{QQ}U
-\nabla\cdot(2aK_B\nabla E+2Aa\nabla\chi),
\]

and

\[
\dot P_\chi+2Aa\nabla^2E
-2Aa\nabla\cdot[(1+j_{\rm eff})\nabla\chi]
+2aK_Q\nabla^2\alpha=0,
\]

\[
\dot P_\alpha+2a^3K_{QQ}U\dot{\bar Q}
+2aK_Q\nabla^2\chi
-2aK_Q\bar Q\nabla^2\alpha=0.
\]

For the D2C4 completion,

\[
j_{\rm eff}=j(x)\left[1+\sigma\epsilon_{\rm mix}\frac{x^2}{1+x^2}\tanh^2\bar Z\right],
\quad x=\sqrt{Y}/a_0,
\quad \epsilon_{\rm mix}=0.25.
\]

The completion-dependent metric correction begins beyond the retained quadratic weak-field action, so the metric/effective-fluid forcing sector remains the corrected linear AeST one at this order.

## Interpretation and next license

D2C5 removes the previous theory-level blocker: a nonlinear FLRW scalar-current evolution can now be implemented from an action-derived system without treating pseudo-time, homotopy, arclength, or a numerical continuation parameter as physical time.

The next stage must still be separately preregistered. A numerical integrator/control stage may use the corrected CLASS background and linear metric/matter history as the externally supplied weak-field forcing permitted by D2C5. Such a stage is a nonlinear AeST-field trajectory on a linear cosmological forcing history, not a claim of fully coupled nonlinear matter structure formation.

Historical PASS/FAIL/INCOMPLETE classifications remain unchanged.