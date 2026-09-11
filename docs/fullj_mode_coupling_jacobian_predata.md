# Full-J mode-coupling Jacobian diagnostic — predata

Classification before implementation: **FULLJ_MODE_COUPLING_JACOBIAN_PREDATA**

This diagnostic follows the dense-map result `FULLJ_DENSE_RECLOSURE_MAP_UV_STRUCTURE_CHANGED`: all 90/90 nonlinear snapshots were residual-valid and every fitted high-k slope was below -1, but only 63/90 snapshots had strictly monotone `T_phi=|Phi_k|/|S_k|`. The strongest anomaly occurs near `z=0.25, k=0.6 1/Mpc`, where the direct source Fourier coefficient is close to a node while the nonlinear field remains finite.

## Scientific question

Is the dense-map non-monotonicity mainly caused by dividing a nonlinear, mode-coupled response by a small same-mode source coefficient, rather than by a divergent local UV response of the full-J equations?

The correct local object is the Jacobian of the converged nonlinear solution,

\[
K_{ij}(z)=\frac{\partial \hat\Phi_{k_i}}{\partial \hat S_{k_j}},
\]

evaluated at the full physical multimode background. Because the operator is nonlinear and the background breaks Fourier-mode independence, `K` need not be diagonal.

## Frozen model and grid

Use exactly the dense-map physical model, source normalization, `Nx=384`, 13 Fourier modes, phases, de-aliasing, and full-J constitutive continuation. No physical parameter is changed.

Target redshifts are frozen to

`z = {0.25, 0.5, 1.0}`

representing the strongest source-node anomaly, the transition regime, and a lensing-relevant control redshift.

All nine co-primary branches are retained:

- `kind in {simple, exponential, sharp}`;
- `beta0 in {1.0, 0.5, 0.1}`.

Thus 27 nonlinear background states are solved. At each background, all 13 source modes are probed, for 351 tangent solves.

## Tangent Jacobian

For a converged full-J state `chi*`, linearize the exact lambda=1 residual

\[
R(\chi,S)=0.
\]

For each frozen input mode `j`, use the phase-aligned unit Fourier forcing

\[
\delta S_j(x)=2\cos(k_j x+\varphi_j),
\]

whose positive-frequency Fourier coefficient has unit magnitude. Solve

\[
J_{\rm full}(\chi_*)\,\delta\chi_j=\delta S_j
\]

with the exact analytic tangent coefficient `j+x j'` already used by the Newton solver. Then compute `delta Phi_j` through the same linearized operator and inverse-Laplacian relation.

No finite-difference step is introduced.

Define

\[
|K_{ij}|=|\delta\hat\Phi_{k_i}|/|\delta\hat S_{k_j}|.
\]

This is a phase-aligned local Jacobian for the frozen realization, not yet the full two-quadrature response operator.

## Numerical gates

Every nonlinear background must satisfy the existing dense-map gates:

- `R2_relative_L2 <= 1e-8`;
- `R1_relative_L2 <= 1e-10`;
- constitutive continuation reaches `lambda=1`.

Every tangent solve must be finite and satisfy

`||J delta_chi - delta_S|| / ||delta_S|| <= 1e-8`.

Any failed background or tangent solve gives

**FULLJ_MODE_COUPLING_JACOBIAN_INCONCLUSIVE_SOLVER**.

## Local UV diagnostic

For each of the 27 backgrounds, use the diagonal high-k response

`|K_ii|` for `k >= 0.4 1/Mpc`

and fit its log slope versus `k`. A locally UV-suppressive diagonal response requires

`slope_diag <= -1.0`.

No strict point-by-point monotonicity gate is imposed here; the dense run showed that such a gate is sensitive to source nodes and nonlinear coupling.

## Frozen z=0.25 node/coupling test

For each of the nine z=0.25 branches define

- source-node ratio `N = |S_0.6| / sqrt(|S_0.4 S_0.8|)`;
- raw-transfer bump `B_raw = T_0.6 / sqrt(T_0.4 T_0.8)`;
- local-diagonal bump `B_diag = |K_0.6,0.6| / sqrt(|K_0.4,0.4 K_0.8,0.8|)`;
- output-row coupling ratio `C_0.6 = sqrt(sum_{j != 0.6}|K_0.6,j|^2) / |K_0.6,0.6|`.

A branch supports the source-node/mode-coupling interpretation when

- `N <= 0.25`;
- `B_raw >= 3`;
- `B_diag <= 3`;
- `C_0.6 >= 1`.

The interpretation is called robust when at least 6/9 co-primary branches support it.

## Classification

If all nonlinear and tangent solves are valid, all 27 diagonal high-k slopes are `<= -1`, and at least 6/9 z=0.25 branches support the frozen node/coupling criteria:

**FULLJ_MODE_COUPLING_JACOBIAN_NODE_COUPLING_SUPPORTED**

If all solves are valid and all diagonal slopes are `<= -1`, but fewer than 6/9 node/coupling tests pass:

**FULLJ_MODE_COUPLING_JACOBIAN_DIAGONAL_UV_STABLE_NODE_UNRESOLVED**

If all solves are valid but at least one diagonal slope exceeds -1:

**FULLJ_MODE_COUPLING_JACOBIAN_LOCAL_UV_STRUCTURE_CHANGED**

In all cases:

`observational_claim_licensed = false`.

A positive diagnostic licenses construction of a response-operator-based nonlinear lensing closure. It does not itself license an ACT comparison.