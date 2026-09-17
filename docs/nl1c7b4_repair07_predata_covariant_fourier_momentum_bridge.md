# NL1C7B4 Repair07 — covariant/Fourier momentum-bridge audit

Status: **PRE-DATA / LOCKED BEFORE REPAIR07 IMPLEMENTATION OR WORKFLOW**

## Parent state

Repair07 begins only after the frozen Repair06 high-resolution analytic momentum audit.

- Repair06 official workflow run: `35227370644`.
- Repair06 head: `630023a976d8a6e5aa0eb5a349ae56750dd8a376`.
- Repair06 artifact: `10500046102`.
- Repair06 artifact SHA256: `b589d1f595782d793cdcc0f6cde1de1e4df1994b32f27ac64ee253fd665b4b1d`.
- Repair06 science classification: `NL1C7B4_REPAIR06_ANALYTIC_LEADING_ORDER_INTERFACE_MISMATCH`.
- Frozen Repair05 analytic evaluator blob: `34fd22c73171fce5e32920a94d71d05de61521f6`.
- Frozen B4 reconstruction/domain evaluator blob: `8559120dc273be3174eca130ca313ed6ff5acb25`.

The historical Repair06 classification is immutable. Repair07 does not reinterpret it as a PASS and does not change any Repair04–Repair06 threshold.

## Problem

Repair06 established that the Repair05 radial linear-momentum residual converges with radial resolution to a nonzero value. Increasing `Nr` therefore does not resolve the mismatch. The dominant Repair06 contribution is the Exp `K(Q)` sector in most cases.

Before changing an equation or the certified C7A state, one remaining interface question must be separated from the radial residual: does the covariant shift constraint, its C7A Fourier growing-mode representation, and the radial C7A scalar reconstruction represent the same first-order momentum identity?

This question is especially sharp because C7A reconstructs the scalar perturbation from the difference

`varphi = chi - Q alpha`,

while the frozen v0.19 variable dictionary also gives the same composite directly as

`varphi = a Q theta_A / k^2`.

The two formulas are algebraically identical in the frozen linear theory, but `chi` and `Q alpha` can be much larger than their difference. Repair07 audits the numerical representation of this exact composite without replacing the certified C7A NPZ.

## Frozen theory and inputs

No physical parameter changes are permitted.

- physical memory coupling: `eta=0`;
- AeST model: Exp;
- `KB=0.0665`, `Q0=1e-4 Mpc^-1`, `K2=9500`, `Z0=1e-17 Mpc^-1`;
- `a_i=0.02`;
- frozen scales: `R_sigma={5,10,20} h^-1 Mpc`;
- frozen C7A k band and 128 modes;
- frozen C7A dense accepted-time trace;
- frozen official C7A primary-state NPZ;
- frozen B3 Repair01 direct homogeneous background;
- frozen B1 pressureless-matter normalization.

Required retained inputs:

- C7A final artifact `10481526695`, SHA256 `c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`;
- C7A dense-trace artifact `10469031693`, SHA256 `193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`;
- Repair06 artifact `10500046102`, SHA256 `b589d1f595782d793cdcc0f6cde1de1e4df1994b32f27ac64ee253fd665b4b1d`.

No trace may be regenerated for Repair07.

## Exact covariant identities to audit

### R7-I1 — Exp K-sector shift variation

The frozen spherical Exp contribution is

`L_K = 2 N L R^2 K(Q)`,

with

`Q = cosh(u) (phidot - b phi_r)/N + sinh(u) phi_r/L`.

Before imposing `N=1,b=0`, the exact shift source must reduce symbolically to

`C_M^K = d L_K/db = -2 L R^2 cosh(u) K_Q phi_r`.

On the homogeneous B3 background,

`u=0`, `L=a`, `R=a r`, `phi_r=0`, `Q=Q_bg`.

For `U(lambda)=U_bg+lambda delta U_C7A`, the exact first variation must therefore be

`D C_M^K[U_bg](delta U) = -2 a^3 r^2 K_Q(Q_bg) delta phi_r`.

Terms from the variations of `L R^2`, `cosh(u)`, and `K_Q` multiply the homogeneous `phi_r=0` and must vanish at first order. Repair07 must verify this symbolically. It may not introduce a fitted K coefficient or an additional K derivative term.

### R7-I2 — GR shift first variation

For the frozen spherical GR action, the radial first variation must independently reduce to

`M_GR,1 = 4 a^3 r^2 d_r(H Psi + Phi_dot)`

or, using the C7A stored metric direction,

`M_GR,1 = -4 a^3 r^2 d_r[(Ldot_1 - H L_1)/a]`.

The closed form and the frozen Repair05 symbolic evaluator must agree to numerical roundoff on every retained radial case.

### R7-I3 — C7A scalar composite identity

At every native accepted trace state, the frozen v0.19 dictionary requires

`chi = Q (a theta_A/k^2 + alpha_A)`,

hence

`varphi_native = chi - Q alpha_A = a Q theta_A/k^2`.

Repair07 must construct three diagnostic routes at `a_i`:

1. current componentwise route: `PCHIP(chi) - PCHIP(Q) PCHIP(alpha_A)`;
2. composite-first route: `PCHIP(chi - Q alpha_A)`;
3. theta route: `PCHIP(a Q theta_A/k^2)`.

Routes 2 and 3 are an exact algebraic identity evaluated through the same frozen accepted-time sampling. Their numerical agreement is an implementation identity, not a new physical fit.

The official C7A NPZ remains read-only. Repair07 may not write or substitute a repaired state file.

### R7-I4 — Fourier 0i momentum identity

Using the repository Fourier/sign convention and only the sectors explicitly represented in the certified C7A state, define

`G_0i(k) = -2 k^2 [H Psi + Phi_prime/a]`,

`M_rep(k) = a [varrho_b theta_b + Q K_Q theta_A]`.

The represented-sector residual is

`R_rep(k) = G_0i(k) + M_rep(k)`.

Repair07 must also report the residual momentum density required to close the total metric 0i equation,

`Pi_unrepresented(k) = 2 k^2 [H Psi + Phi_prime/a]/a - [varrho_b theta_b + Q K_Q theta_A]`.

This quantity is diagnostic only. It must not be fitted or inserted into the radial constraint. Repair07 does not identify it with a specific standard species unless an independent species-resolved trace is available.

## Frozen numerical audit

Repair07 retains all three scales and both `Nr=256` and `Nr=512` radial grids for radial diagnostics. No scale or radial interval may be selected after inspection.

For each scale/grid, report:

- official-state reproduction error;
- current-vs-composite-first `phi` relative L2 difference;
- composite-first-vs-theta `phi` relative L2 difference;
- current-vs-composite-first K-sector relative L2 difference;
- Repair05 GR-vs-closed-form relative L2 difference;
- global radial linear-momentum residual ratio `||sum_i M_i||_2 / sum_i ||M_i||_2` for the current route;
- the same global ratio when only the diagnostic scalar representation used to evaluate the K contribution is formed by the composite-first route;
- the original pointwise normalized `epsilon_M1` diagnostics for both routes.

The composite-first radial calculation is a diagnostic recomputation of one exact algebraic representation. It is not a state replacement and cannot be used to claim B4 constraint PASS.

For the Fourier identity, report the pointwise symmetric residual

`epsilon_0i(k)=|R_rep|/(|G_0i|+|M_rep|+floor)`

with the same type of fixed numerical floor used elsewhere, plus target-profile-weighted L2 diagnostics for all three frozen scales.

## Gates

### R7-G1 — provenance and immutability

All frozen artifact digests and source blobs must match. The official C7A NPZ must reproduce exactly as in B4 (`<=1e-12` relative L2 for every nonzero stored state array). Repair05 and B4 evaluators are read-only.

### R7-G2 — exact covariant identities

R7-I1 must simplify exactly symbolically. The GR closed form in R7-I2 must agree with the frozen Repair05 analytic GR first variation with relative L2 error `<=1e-10` on every radial case. This `1e-10` gate is an implementation identity tolerance, not a physical constraint threshold.

### R7-G3 — exact native scalar composite

At native accepted trace states, `chi-Q alpha_A` and `a Q theta_A/k^2` must agree to relative L2 error `<=1e-10`. Their two PCHIP-at-`a_i` composite routes must also agree to `<=1e-10`. This is an algebraic implementation-identity gate.

### R7-G4 — inherited C7A Fourier-interface envelope

The represented-sector Fourier 0i identity must remain inside the already frozen C7A interpolation-control scale: `max epsilon_0i <= 2e-2` over the 128 retained k modes. The `2e-2` value is inherited from C7A A6/A7 and is not a replacement for the B4 raw-constraint gate.

### R7-G5 — no post-result repair

Repair07 must not:

- modify or overwrite the official C7A NPZ;
- fit any coefficient, sign, scale factor, radial correction, or standard-sector source;
- alter `K(Q)`, `J(Y)`, the dust source, the homogeneous background, the k grid, the radial domain, or any historical threshold;
- remove tail/zero-crossing radial points from the original pointwise B4 diagnostic;
- execute nonlinear evolution;
- execute finite eta.

The original B4 `1e-7` raw-constraint threshold and Repair05/06 `1e-5` linear-interface threshold remain unchanged and are not re-evaluated as PASS criteria in Repair07.

## Preregistered classifications

### `NL1C7B4_REPAIR07_COVARIANT_FOURIER_BRIDGE_DIAGNOSTIC_PASS`

Use only if R7-G1 through R7-G5 pass. This means the covariant K/GR first variations and the C7A Fourier growing-mode momentum bridge are mutually consistent within inherited numerical controls. It does **not** mean the frozen radial B4 constraint has passed.

The result must still report, without a new pass threshold, how much the current componentwise scalar route differs from the exact composite-first route and how the radial global residual changes under that diagnostic representation.

### `NL1C7B4_REPAIR07_COVARIANT_FOURIER_INTERFACE_MISMATCH`

Use if provenance and exact implementation identities pass but the represented-sector Fourier 0i residual exceeds the inherited `2e-2` envelope. No corrective source may be fitted.

### `NL1C7B4_REPAIR07_IMPLEMENTATION_FAIL`

Use if provenance, state reproduction, exact K/GR identity, native composite identity, finiteness, or immutability checks fail.

## Claim boundary and allowed continuation

Repair07 is an identification audit only. It cannot freeze a new physical initial state and cannot license nonlinear evolution.

If Repair07 gives `COVARIANT_FOURIER_BRIDGE_DIAGNOSTIC_PASS` and the composite-first diagnostic materially changes the radial residual, the next allowed step is a **separately preregistered numerical-representation repair** of the C7A-to-B4 scalar bridge. That repair must create and certify a new identity-preserving state artifact while retaining the historical C7A artifact unchanged. Only after that new state has been independently certified may the original B4 radial constraints be re-tested under their unchanged gates.
