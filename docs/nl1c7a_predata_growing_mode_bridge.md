# NL1C7A pre-data preregistration — eta=0 cosmological growing-mode to spherical initial-data bridge

Status: **PRE-DATA / LOCKED BEFORE ANY C7A CLASS TRACE OR SPHERICAL TRAJECTORY**

## Parent state

- NL1C6 closure: `NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_PASS`.
- Certified NL1C6 G11 run: `35089436959`, head `0f868057e788423b588cda5bc654287c784ebee7`, artifact `10442933686`, SHA256 `12b83f6f67f473937514005f6a87764646407e3b2141b4451d47bd92b62c6ddc`.
- NL1C7 initial-data audit: `NL1C7_INITIAL_DATA_CLOSURE_INCOMPLETE`.
- Certified NL1C7 audit run: `35091301474`, head `c4351a752eccc99a86cf458acb4c52a509f63f6e`, artifact `10444427175`, SHA256 `f1f5327bc6c19fb379723ad5f6b03816453d21bc7bfce33a564d217fee01b91a`.
- Frozen NL1C7 profile/evolution preregistration commit: `8e55b2db18a3bf463e392bc6bcba85bcaf056fb9`.

## Purpose

C7A supplies only the missing physical mode selection identified by NL1C7. It maps the already validated eta=0 adiabatic cosmological growing solution into the NL1C6 spherical variables `(L,R,u,phi)` and their initial velocities, together with the conserved dust variables. It does not evolve the nonlinear spherical system and does not enable finite memory coupling.

The bridge must select the regular adiabatic growing mode only. No homogeneous/free scalar-aether wave may be added or fitted.

## Frozen theory/model state

- physical memory coupling: `eta=0`; memory forcing OFF.
- AeST model: Exp.
- `KB=0.0665`, `Q0=1e-4 Mpc^-1`, `K2=9500`, `Z0=1e-17 Mpc^-1`.
- CLASS commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Newtonian-gauge AeST linear variables use the already validated v0.19/v0.19i definitions
  `chi = varphi + Q alpha`, `E = alpha_dot + Psi`, with leading adiabatic mode fixed by the existing v0.19i IC construction.
- The C6 conserved dust sector is identified with the ordinary baryonic dust sector of the CLASS bridge. The CLASS `cdm` slot is the AeST effective scalar dark component and is not re-labelled as the C6 conserved dust.

## Frozen physical size mapping of the existing C7 profile

The dimensionless C7 profile shape, amplitude and initial epoch remain unchanged:

`delta_b(x) = 1e-3 * (1 - x^2/3) * exp(-x^2/2)`, `a_i=0.02`, `x in [0,8]`.

C7A fixes the previously unspecified comoving mapping `r = R_sigma x` on a co-primary scale ladder

`R_sigma = [5, 10, 20] h^-1 Mpc`.

`10 h^-1 Mpc` is the nominal reporting scale only. **All three scales are required for C7A certification; no scale may be selected after the result.**

With Fourier convention `delta(r)=int d^3k/(2pi)^3 delta_tilde(k) exp(i k.r)`, the exact target dust transform is

`delta_b_tilde(k) = delta0 (2pi)^(3/2) R_sigma^3 * [(k R_sigma)^2/3] * exp[-(k R_sigma)^2/2]`.

The common CLASS trace band is frozen to

`k in [0.0015, 1.2] h Mpc^-1`,

with 128 logarithmically spaced requested modes. This covers the relevant support of all three frozen profile scales without nonlinear corrections.

## Frozen gauge bridge

Start from Newtonian gauge

`ds^2 = -(1+2 Psi) dt^2 + a^2(1-2 Phi)(dr^2+r^2 dOmega^2)`.

Use a scalar coordinate generator `xi^mu=(T, d_r S,0,0)` and the convention already frozen in v0.19i, so `Psi -> Psi - Tdot`, `alpha -> alpha + T`, `varphi -> varphi - Q T`.

The target is the C6 proper-time/zero-shift gauge `N=1,b=0`. The gauge conditions are

`Tdot = Psi`, `a^2 Sdot = T`.

Residual coordinate freedom is fixed **only as a gauge convention** by initial-slice alignment

`T(a_i,r)=0`, `S(a_i,r)=0`.

Therefore, on the initial slice,

- `L = a (1-Phi)`;
- `R = a r (1-Phi)`;
- `Ldot = a H (1-Phi-Psi) - a Phidot`;
- `Rdot = a H r (1-Phi-Psi) - a r Phidot`;
- `alpha_PT = alpha_N`;
- `u = (d_r alpha_PT)/a`;
- `udot = (d_r E)/a - H u`;
- `varphi_PT = chi - Q alpha_PT`;
- by scalar shift symmetry the homogeneous value of `phi` is set to zero and the spherical perturbation is `phi=varphi_PT`;
- at `T=0`, the scalar `Q=A^mu grad_mu phi` perturbation is unchanged between the two slicings, and `phidot = Q + deltaQ` with `deltaQ = rho_A delta_A/(Q K_QQ)` for `rho_A=Q K_Q-K`.

Two independent first-order bridge identities must hold:

`X_C6 = (d_r chi)/a`,

and

`E_C6 = (d_r E_CLASS)/a`,

where `X_C6` and `E_C6` are the linearizations of the NL1C6 spherical invariants.

## Frozen growing-mode normalization

For each k and each frozen scale, the target baryonic profile fixes the unique adiabatic growing-mode amplitude by

`A(k) = delta_b_target_tilde(k) / T_delta_b(k,a_i)`.

Every other initial Fourier field is obtained from the same CLASS eta=0 adiabatic solution as

`F_tilde(k) = T_F(k,a_i) A(k)`.

No independent rescaling of metric, AeST scalar, aether or velocity variables is allowed. If the baryon transfer has an unresolved zero on the required support, the bridge fails before reconstruction.

## Required native CLASS trace fields

The accepted source-sampling trace must contain, at minimum:

`k, tau, a, H, Q, rho_A, KQ, KQQ, delta_b, theta_b, delta_A, theta_A, alpha_A, E_A, Phi, Phi_prime, Psi`.

The trace extension is output-only. It may not alter any background, perturbation or memory equation.

## Frozen numerical extraction

- no nonlinear CLASS correction;
- OMP threads = 1;
- accepted source-sampling states only; rejected/adaptive RK stages are forbidden;
- exact target epoch `a_i=0.02` is reconstructed from bracketing native accepted times;
- primary time interpolation: PCHIP in `ln a`;
- independent time control: linear interpolation in `ln a`;
- no extrapolation;
- primary k interpolation of transfer ratios: PCHIP in `ln k`;
- independent k control: linear in `ln k`;
- radial reconstruction uses spherical Bessel transforms on fixed logarithmic quadrature; primary/control quadratures are 256/512 nodes over the frozen k band.

## Gates

### A1 — provenance
All parent run/head/artifact hashes and the frozen C7 preregistration must match exactly.

### A2 — exact gauge/variable dictionary
A symbolic Lie-derivative audit must reproduce the stated lapse, shift, radial-metric and areal-radius transformations and the initial-slice formulas above. The linearized NL1C6 invariants must reduce exactly to `X=chi_r/a` and `E=E_CLASS,r/a`.

### A3 — output-only trace extension
The CLASS trace patch must change only diagnostic output plumbing. It must pass source-code checks that the eta=0 physical evolution equations are byte-identical before and after the trace extension apart from the trace helper/call.

### A4 — native coverage
All 128 frozen k modes must be present with relative k mismatch `<=1e-12`. At least three common native accepted times below and three above `a_i=0.02` within `0.015 <= a <= 0.03` must exist for every requested mode.

### A5 — finite growing-mode denominator
On every quadrature support used after the analytic target-profile weighting, `T_delta_b` must be finite. Nodes with target-profile weight greater than `1e-10` of the peak may not have `|T_delta_b| < 1e-12 * max|T_delta_b|`. No clipping or node deletion is allowed.

### A6 — time-interpolation control
For every frozen scale, reconstruct the complete spherical initial state with both PCHIP-ln(a) and linear-ln(a). For each nonzero reconstructed field among `L-a`, `R-ar`, `Ldot-aH`, `Rdot-aHr`, `u`, `udot`, `phi`, `phidot-Q`, `delta_b`, and dust radial velocity, the scheme-to-scheme L2 relative difference must be `<=2e-2`. Fields whose primary norm is `<=1e-14` are reported and excluded only from the relative quotient, not from the state.

### A7 — k-interpolation control
Holding the primary time interpolation fixed, PCHIP-ln(k) and linear-ln(k) reconstructions must satisfy the same `<=2e-2` L2 relative control for the nonzero spherical fields on every frozen scale.

### A8 — target-profile reconstruction
The direct 256/512 spherical-Bessel reconstruction of the analytic compensated Gaussian target must agree at L2 relative error `<=1e-4` on `x in [0,8]` for every scale, and the 256/512 target reconstruction mismatch must be `<=1e-4`.

### A9 — bridge identities
On the real-space grid, `X_C6` reconstructed from `(u,phi_r)` and independently from `chi_r/a` must agree at L2 relative error `<=1e-6`. `E_C6` reconstructed from `(udot,H u)` and independently from `E_CLASS,r/a` must agree at L2 relative error `<=1e-6`.

### A10 — no free-mode injection
The implementation must contain no independent amplitude, phase or homogeneous scalar/aether-wave parameter beyond the one per-k normalization `A(k)` fixed by the target baryon profile. A static source audit must verify this.

## Classification

PASS:

`NL1C7A_ETA0_GROWING_MODE_SPHERICAL_BRIDGE_CERTIFIED`

Allowed non-PASS classifications include provenance, gauge-dictionary, trace-interface, native-coverage, transfer-zero, time-interpolation, k-interpolation, reconstruction, bridge-identity, and free-mode-injection failures.

A PASS licenses only construction of unique eta=0 C7 initial data on the three frozen scale mappings. It does not itself certify nonlinear evolution, turnaround, collapse, shell crossing, splashback, finite eta or an observable.
