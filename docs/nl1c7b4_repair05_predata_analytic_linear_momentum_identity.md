# NL1C7B4 Repair05 — analytic linear momentum identity audit

Status: **PRE-DATA / LOCKED BEFORE IMPLEMENTATION**

Parent Repair04 official run: `35223365082`

Parent Repair04 artifact: `10498905089`

Parent artifact SHA256: `1192b25acc1099bd24ff07c1e0b58c448d946513c895307a7c364aa9cfe66f3f`

Parent Repair04 result freeze commit: `148b5f51b08fae9eb3cf1b49404cca99816bb639`

## Problem

Repair04 used a symmetric finite-difference directional derivative of the exact eta=0 radial momentum constraint. That audit was scientifically non-interpretable because the frozen relative convergence gate penalized terms whose exact first directional derivative vanishes. In particular, several quadratic AeST terms produced finite-difference tangent estimates that decrease as the step squared, while the nonzero GR tangent remained finite-step limited at the selected steps.

Repair05 removes this ambiguity by evaluating the first directional derivative at lambda=0 analytically, term by term. No finite-difference tangent is used for the primary result.

## Frozen state and background

The state direction is exactly the retained C7A Repair01 growing-mode spherical state. The 256-point retained NPZ must be reproduced with maximum relative L2 error <= `1e-12`; the 512-point state is reconstructed from the same frozen dense trace using the already locked C7A reconstruction.

Frozen scales: `5, 10, 20 h^-1 Mpc`.

Frozen radial resolutions: `Nr = 256, 512`.

All 9 co-primary Y choices remain present (`Simple`, `Exponential`, `Sharp`) x `beta0 = 1, 0.5, 0.1`. A Y branch may not be selected after the result.

The homogeneous background remains the certified B3 Repair01 direct background. The completed Repair02 scalar dictionary is retained so the exact invariant Q follows the frozen C7A target direction.

## Analytic directional derivative

Write every perturbation as its frozen C7A direction multiplied by lambda around the homogeneous eta=0 background. Repair05 evaluates

`M1(r) = d C_M(lambda,r) / d lambda |_(lambda=0)`

for the original action-derived radial momentum constraint.

For local variational terms generated symbolically from the frozen spherical action, the derivative is obtained by the exact chain rule: the Jacobian of the local `delta L / delta b` and `delta L / delta b_r` source functions with respect to the state arguments is evaluated on the homogeneous background and contracted with the frozen C7A perturbation direction. The radial Euler-Lagrange divergence is then applied with the same locked derivative matrix used in B4.

The following groups are reported separately:

- GR kinetic/shift sector;
- `AeST_E2`;
- `AeST_EX`;
- `AeST_X2`;
- AeST Y/J sector;
- AeST Exp K(Q) sector;
- pressureless dust;
- homogeneous standard background.

Quadratic terms are not numerically forced to zero. Their analytic derivative must itself evaluate to zero to machine precision if the action implies a vanishing first-order contribution.

For the completed Exp K(Q) momentum term, the analytic derivative is evaluated directly at the homogeneous background, including the frozen stable Exp background coordinate. No clipping, logarithmic replacement, or Q linearization is permitted.

For dust, the analytic derivative follows the already locked B1 action and the frozen B4 velocity convention; no dust-sign alternative is tested.

## Primary normalized linear residual

At every non-center radial point,

`epsilon_M1 = |sum_i M1_i| / (sum_i |M1_i| + floor)`

with `floor = 1e-14 * max_r(sum_i |M1_i|)` on that case. The center is excluded only because the spherical momentum constraint is identically degenerate there; no other radial point may be excluded.

Primary diagnostic threshold carried forward from Repair04:

- linear-interface PASS region: `max epsilon_M1 <= 1e-5` in all 54 cases;
- strong leading-order mismatch region: `max epsilon_M1 >= 0.1` in all 54 cases.

Values between these regions are diagnostic-complete but not classified as either pass or strong mismatch.

These thresholds are diagnostic only and do not replace the original B4 nonlinear raw-constraint threshold `1e-7`.

## Required analytic controls

Repair05 is interpretable only if all controls pass:

1. C7A state reproduction <= `1e-12`.
2. Parent Repair04 provenance and artifact digest match exactly.
3. Symbolic Exp K(Q) dictionary identity remains true.
4. The analytic first derivative of `AeST_E2`, `AeST_EX`, `AeST_X2`, and the Y/J contribution must be finite; if mathematically zero, the reported maximum absolute value must be <= `1e-12` times the largest nonzero first-order term scale in that case, with an absolute floor of `1e-30`.
5. Independent E/X bridge: the analytic linear-frame expressions must reproduce the frozen C7A relations `E1 = udot + H u` and `X1 = Q u + phi_r/a` with relative L2 error <= `1e-6`.
6. 256/512 grid control: for each scale and Y branch, the RMS normalized residual on the common x-grid must agree to relative difference <= `2e-2` unless both RMS values are below `1e-8`.
7. No state projection, fitted coefficient, sign flip, scale selection, Y selection, radial standard-species insertion, or evolution.

## Preregistered classifications

- `NL1C7B4_REPAIR05_ANALYTIC_LINEAR_MOMENTUM_INTERFACE_PASS`
  - all analytic controls pass and all 54 cases satisfy `max epsilon_M1 <= 1e-5`.

- `NL1C7B4_REPAIR05_ANALYTIC_LEADING_ORDER_INTERFACE_MISMATCH`
  - all analytic controls pass, all 54 cases satisfy `max epsilon_M1 >= 0.1`, and the reported nonzero term decomposition identifies the uncancelled first-order sectors without any fitted correction.

- `NL1C7B4_REPAIR05_ANALYTIC_LINEAR_MOMENTUM_DIAGNOSTIC_COMPLETE`
  - all analytic controls pass but the 54 cases do not satisfy either uniform PASS or uniform strong-mismatch region.

- `NL1C7B4_REPAIR05_IMPLEMENTATION_FAIL`
  - any provenance, state reproduction, symbolic identity, analytic-zero, E/X bridge, finiteness, or grid-control requirement fails.

## Claim boundary

Repair05 is a linear identity audit only. It does not modify the initial state, does not solve the nonlinear Hamiltonian or momentum constraints, and does not authorize nonlinear evolution, turnaround, collapse, or finite-eta comparison. Any subsequent nonlinear completion must be separately preregistered after the Repair05 classification is frozen.
