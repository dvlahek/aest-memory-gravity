# NL1C7B4 Repair11 — analytic/covariant E-sector momentum audit

## Status

Locked before implementation and before any Repair11 execution.

Repair11 is licensed only by the frozen Repair10 diagnostic PASS at commit `de03f563ee3e8700b3159be5a46b73633c85db8d`.

Repair11 does not repair the state or alter the theory. It tests if the `AeST_E2` and `AeST_EX` terms that dominate the exact Repair10 radial-momentum hotspot contain a first-order momentum source on the homogeneous B3 background, or instead begin at quadratic perturbative order.

## Frozen definitions

Use exactly the frozen spherical definitions

`k_L = (L_t - b L_r - L b_r)/(N L)`

`sigma = (phi_t - b phi_r)/N`

`X = sinh(u) sigma + cosh(u) phi_r/L`

`E = cosh(u)[(u_t-bu_r)/N + N_r/(NL)] + sinh(u)[k_L+u_r/L]`

and action-density terms

`L_E2 = N L R^2 K_B E^2`

`L_EX = 2 N L R^2 C E X`

with the frozen constants `K_B=0.0665` and `C=2-K_B`.

The radial momentum Euler-Lagrange contribution is

`C_M = partial L/partial b - d_r(partial L/partial b_r)`.

No coefficient or sign may be changed.

## Exact gauge identities to audit

At the frozen evaluation gauge

`N=1, b=0, N_r=0, b_r=0`,

Repair11 preregisters the following analytic identities:

`E = cosh(u) u_t + sinh(u)(L_t/L + u_r/L)`

`X = sinh(u) phi_t + cosh(u) phi_r/L`

`partial_b E = -cosh(u) u_r - sinh(u) L_r/L`

`partial_br E = -sinh(u)`

`partial_b X = -sinh(u) phi_r`

`partial_br X = 0`.

Therefore

`partial_b L_E2 = 2 K_B L R^2 E partial_b E`

`partial_br L_E2 = -2 K_B L R^2 E sinh(u)`

and

`partial_b L_EX = 2 C L R^2[(partial_b E)X - E sinh(u) phi_r]`

`partial_br L_EX = -2 C L R^2 sinh(u) X`.

These identities must be proved symbolically from the frozen definitions, not fitted numerically.

## Homogeneous B3 first variation

On the B3 homogeneous background

- `L=a`;
- `R=ar`;
- `L_t=aH`;
- `u=0`;
- `u_t=0`;
- `phi_r=0`;
- `phi_t=Q`;
- `L_r=0`;
- `N_r=0`;

we have

`E_bg=0`

and

`X_bg=0`.

Introduce a formal perturbation amplitude `epsilon`. The preregistered analytic claim is

`[epsilon^1] C_M^{E2} = 0`

and

`[epsilon^1] C_M^{EX} = 0`.

Thus the E2 and EX sectors must not appear as independent first-order source terms in the linear Fourier 0i momentum identity used by the C7A/Repair07 bridge.

With the frozen zero-`N_r` initial gauge, define

`E_1 = u_dot_1 + H u_1`

`X_1 = Q u_1 + phi_{1,r}/a`.

The preregistered quadratic coefficients are

`[epsilon^2] C_M^{E2} = 2 K_B a^3 u_1 d_r(r^2 E_1)`

and

`[epsilon^2] C_M^{EX} = 2 C a^3 u_1 d_r(r^2 X_1)`.

Repair11 must prove these expressions symbolically.

## Frozen numerical inputs

- Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`;
- Repair08 JSON SHA-256: `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`;
- Repair10 JSON SHA-256: `f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d`;
- Repair10 classification: `NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS`;
- Repair10 result-freeze commit: `de03f563ee3e8700b3159be5a46b73633c85db8d`;
- same dense trace/coverage used by Repair08-10;
- scales `5,10,20 h^-1 Mpc`;
- `Nr=256,512`;
- `eta=0`.

The official Repair08 state is read only.

## Numerical audit

For each of the six scale/grid pairs:

1. construct the same frozen Repair08 state used by Repair09/10;
2. evaluate the exact `AeST_E2` and `AeST_EX` momentum arrays using the frozen `build_nonK()` implementation;
3. independently evaluate the same arrays from the preregistered closed-form gauge derivatives above;
4. compare the full non-center arrays;
5. compare values at every Repair10 M-hotspot against the signed `AeST_E2` and `AeST_EX` values stored in the frozen Repair10 JSON.

The implementation-equivalence normalized error limit is `1e-10`. Repair10 hotspot reproduction uses absolute-or-relative tolerance `1e-12`.

## Virtual perturbation-order audit

No official state is modified.

For diagnostic copies only, scale every perturbation away from the same homogeneous B3 background by

`lambda in {1, 1/2, 1/4, 1/8}`.

For example

`L(lambda)=a+lambda(L-a)`,

`R(lambda)=ar+lambda(R-ar)`,

`u(lambda)=lambda u`,

`u_t(lambda)=lambda u_t`,

`phi(lambda)=lambda phi`,

`phi_t(lambda)=Q+lambda(phi_t-Q)`,

with analogous scaling for `L_t-aH` and `R_t-aHr`.

For each scale/grid pair and each of E2 and EX, compute the non-center L2 norm of the exact momentum contribution and adjacent log2 slopes

`p = log(norm(lambda_i)/norm(lambda_{i+1}))/log(2)`.

The preregistered quadratic-order gate is

`1.8 <= p <= 2.2`

for every finite adjacent slope.

This is a diagnostic perturbative-order test, not a replacement B4 constraint threshold.

## Gates

### R11_G1 — frozen provenance

Require the exact Repair08 and Repair10 hashes/classifications, Repair10 result-freeze ancestry, exact dense coverage, and frozen imported-code blobs.

### R11_G2 — exact gauge shift identities

All preregistered derivatives of E, X, `L_E2`, and `L_EX` must simplify symbolically to zero difference.

### R11_G3 — first-order vanishing

The formal `epsilon^1` coefficients of both radial-momentum EL contributions must simplify exactly to zero.

### R11_G4 — quadratic coefficients

The formal `epsilon^2` coefficients must simplify exactly to the preregistered closed forms.

### R11_G5 — frozen implementation equivalence

For all six scale/grid pairs, frozen `build_nonK()` E2/EX momentum arrays and the independent closed-form implementation must agree to normalized error `<=1e-10` on all non-center points.

### R11_G6 — Repair10 hotspot reproduction

All 54 Repair10 case records must reproduce their stored E2/EX M-hotspot signed contributions to absolute-or-relative tolerance `1e-12`.

### R11_G7 — quadratic amplitude scaling

Every finite adjacent slope in the virtual lambda audit must lie in `[1.8,2.2]`.

### R11_G8 — linear Fourier consistency and claim boundary

Record explicitly that E2/EX first-order momentum source is zero and hence their absence from the frozen linear Fourier represented source

`a[varrho_b theta_b + Q K_Q theta_A]`

is analytically consistent.

Require no state write/projection, coefficient fit, source insertion, sign change, threshold change, point removal, Y/beta/scale selection, nonlinear evolution, finite eta, B4-PASS claim, or observational-detection claim.

## Terminal classifications

Allowed:

- `NL1C7B4_REPAIR11_ESECTOR_ANALYTIC_COVARIANT_AUDIT_PASS`;
- `NL1C7B4_REPAIR11_ESECTOR_INTERFACE_MISMATCH`;
- `NL1C7B4_REPAIR11_IMPLEMENTATION_FAIL`.

If G1-G4 pass but G5 or G6 fails, classify as E-sector interface mismatch.

A PASS means only that the dominant Repair10 E-sector residual is consistent with a contribution that begins at quadratic perturbative order and with the frozen exact spherical implementation. It does not make B4 pass.

Any later reinterpretation of B4, nonlinear initial-data correction, or change to the model requires a separate preregistration.
