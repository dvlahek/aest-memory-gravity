# NL1C7B4 Repair04 predata — linear momentum interface audit

Status: **PRE-DATA / FROZEN BEFORE IMPLEMENTATION**

Date: 2026-09-17

Parent result freeze: commit `71ddc4b6135bde7eb83b68e8fc5a474211d75f72`.

Parent scientific artifact:

- Repair03 run `35217116467`
- head `27d0323f198720f14d82fb596923b93d232b081e`
- artifact `10495093609`
- digest `sha256:82900b1e2c85a63b9513841580c4ca71465d8adc03e58887d5f3ffdac3e11aca`
- classification `NL1C7B4_REPAIR03_CONSTRAINT_SOURCE_LOCALIZATION_COMPLETE`

## Problem

Repair03 leaves a nearly unit normalized radial-momentum residual and localizes 98.2--99.9% of the absolute contribution at the worst radius to the grouped `AeST_nonK_nonJ` sector. Its maximum momentum residual barely changes under the frozen amplitude ladder. Repair04 therefore tests if the mismatch is already present in the first directional derivative of the exact frozen constraint around the reconciled homogeneous background.

No state projection or repair is authorized in this checkpoint.

## Frozen state and physics

Repair04 uses the same exact C7A Repair01 retained primary-state artifact, dense trace, background point, AeST action, pressureless matter action, standard homogeneous sector, Y families, beta values, scales, and radial grids as Repair03. No CLASS rerun is allowed.

The frozen co-primary cases remain:

- scales: `5, 10, 20 h^-1 Mpc`
- radial grids: `Nr=256,512`
- Y families: `Simple, Exponential, Sharp`
- beta0: `1, 0.5, 0.1`

## Directional linearization

Let `z_bg` be the exact reconciled homogeneous C6 background and `Delta z` the unmodified certified C7A perturbation direction. For each case evaluate the exact Repair03 momentum source dictionary at

`z(lambda) = z_bg + lambda Delta z`,

including the already preregistered algebraic Q-target completion used in Repair02/03.

Use symmetric directional derivatives

`D_h M = [M(+h)-M(-h)]/(2 h)`

with the frozen ladder

`h = 0.04, 0.02, 0.01`.

The same derivative is computed separately for `GR`, `AeST_E2`, `AeST_EX`, `AeST_X2`, `AeST_J`, `AeST_K`, `dust`, and `standard_bg`. No coefficient, sign, scale factor, or source may be fitted from the result.

## Numerical tangent gate

For each active term and the total momentum tangent, report raw max-absolute and L2 norms at all three h values. A term is active for convergence gating only if its finest-step L2 norm is at least `1e-12` times the sum of finest-step sector L2 norms in that case.

The frozen convergence metric is

`||D_0.02 - D_0.01||_2 / max(||D_0.01||_2, ||D_0.02||_2, 1e-300)`.

The numerical tangent gate is `<= 5e-4` for the total and every active term. The `h=0.04` value is retained as a coarse consistency diagnostic but is not used to loosen this gate.

If this gate fails, the scientific classification is `NL1C7B4_REPAIR04_LINEARIZATION_NUMERICAL_FAIL`. It must not be interpreted as a physical constraint failure.

## Linear momentum closure metric

At the finest tangent `h=0.01`, define at every non-center radial point

`epsilon_M1 = |sum_i M_i^(1)| / [sum_i |M_i^(1)| + 1e-14 max_r sum_i |M_i^(1)|]`.

Report the maximum and RMS `epsilon_M1`, raw total max-absolute and L2 norms, the radius of maximum `epsilon_M1`, and the individual signed sector contributions there.

No radial point may be removed to obtain a PASS. The center may be excluded because the radial momentum equation is analytically degenerate there, exactly as in prior B4 diagnostics.

## E/X bridge audit

Repair04 additionally reports the background scalars used on both sides of the interface:

- `Q_CLASS = median CLASS Q(a_i,k)` used by the C7A reconstruction,
- `Q_action = stable Exp-K inversion of median CLASS KQ(a_i,k)` used by the exact C6 action,
- `H_CLASS = median CLASS H_Mpc_inv(a_i,k)` used in C7A,
- `H_action = H_DIRECT` from the reconciled B3 background.

Using the same radial derivative matrix as the constraint evaluator, compute the exact-frame first-order identities

`X_frame^(1) = Q_action u + phi_r/a_i`,

`E_frame^(1) = udot + H_action u`,

and compare them without adjustment to the frozen C7A identities

`X_C7A = Q_CLASS u + phi_r/a_i`,

`E_C7A = udot + H_CLASS u`.

Also verify the symmetric finite-difference tangents of the exact frame definitions against `X_frame^(1)` and `E_frame^(1)`. This is a convention/interface diagnostic only. No background value may be replaced after seeing the result.

## Frozen classifications

Provided provenance, state reproduction, symbolic dictionary integrity, finiteness, and tangent convergence pass:

1. `NL1C7B4_REPAIR04_LINEAR_MOMENTUM_INTERFACE_PASS` if every co-primary case has `max epsilon_M1 <= 1e-5`.
2. `NL1C7B4_REPAIR04_LEADING_ORDER_INTERFACE_MISMATCH` if every co-primary case has `max epsilon_M1 >= 0.1` and the grouped `AeST_E2 + AeST_EX + AeST_X2` contribution is the largest absolute grouped contribution at the maximum-residual radius in every case.
3. Otherwise `NL1C7B4_REPAIR04_LINEAR_MOMENTUM_DIAGNOSTIC_COMPLETE`.

These classifications are diagnostic. A mismatch classification does not authorize changing a sign or multiplying a term by a fitted factor.

## Claim boundary

Repair04 may identify a leading-order constraint/interface mismatch and may localize it to exact variational sectors and background E/X conventions. It does not modify the state, project the constraints, alter dust, add perturbed radiation or neutrino sources, change the action, evolve the system, introduce finite memory, or make an observable prediction.