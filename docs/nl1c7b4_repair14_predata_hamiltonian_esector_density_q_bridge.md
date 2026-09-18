# NL1C7B4 Repair14 — analytic Hamiltonian E-sector density-Q bridge audit

## Status

Locked before implementation and before any Repair14 execution.

Repair14 is licensed only by the frozen Repair13a source-localization PASS at commit
`cb6440383eac99001369e976fae035d74adf30fc`.

Repair14 does not change the AeST action, coefficients, signs, official Repair08 state, or historical B4 gate. It tests if the certified first-order Hamiltonian E-sector residual is the consequence of an incomplete **effective-density -> scalar-Q bridge**.

## Frozen parent result

Exact Repair13a local JSON:

- SHA-256:
  `cad6cb2b49b3b20a0b6346390f8536fb90da8d5000ceed82ac0de86b912679b3`;
- classification:
  `NL1C7B4_REPAIR13A_ROUNDOFF_STABLE_SOURCE_LOCALIZATION_PASS`;
- E2 dominant first-order Hamiltonian source in 54/54 cases;
- E2 first-order-like in 54/54;
- EX first-order-like in 54/54;
- X2 second-order-like in 54/54.

Historical B4 remains FAIL.

## Frozen action definitions

Use exactly

`Q = cosh(u) sigma + sinh(u) phi_r/L`

`X = sinh(u) sigma + cosh(u) phi_r/L`

`E = cosh(u)[(u_t-bu_r)/N + N_r/(NL)] + sinh(u)[k_L+u_r/L]`

`k_L=(L_t-bL_r-Lb_r)/(NL)`

with

`L_E2 = N L R^2 K_B E^2`

`L_EX = 2 N L R^2 C E X`

`L_K = 2 N L R^2 K(Q)`

and frozen constants

`K_B=0.0665`, `C=2-K_B`.

The Hamiltonian/lapse Euler-Lagrange source is

`C_H = partial L/partial N - d_r(partial L/partial N_r)`.

## Exact gauge identities

At `N=1,b=0,N_r=0,b_r=0`:

`partial E/partial N = -cosh(u) u_t - sinh(u) L_t/L`

`partial E/partial N_r = cosh(u)/L`

`partial X/partial N = -sinh(u) phi_t`

`partial X/partial N_r = 0`.

Repair14 must prove these identities symbolically.

## B3 first variation

On the homogeneous B3 background

- `L=a`;
- `R=ar`;
- `L_t=aH`;
- `R_t=aHr`;
- `u=0`;
- `u_t=0`;
- `phi_r=0`;
- `phi_t=Q`;
- `E_bg=X_bg=0`.

Introduce formal perturbation amplitude `epsilon`.

Define

`E_1 = u_dot_1 + H u_1`

`X_1 = Q u_1 + phi_{1,r}/a`.

The preregistered first-order Hamiltonian identities are

`[epsilon^1] C_H^{E2} = -2 K_B a^2 d_r(r^2 E_1)`

`[epsilon^1] C_H^{EX} = -2 C a^2 d_r(r^2 X_1)`.

The direct `partial L/partial N` pieces of E2 and EX must have zero first-order coefficient; the nonzero first-order contribution must come entirely from
`-d_r(partial L/partial N_r)`.

For the K sector, with

`rho_A = Q K_Q-K`,

the intrinsic density part of the first variation must be

`[epsilon^1] C_H^K|intrinsic = -2 a^3 r^2 Q K_QQ delta Q`

in addition to the background-density volume-factor variation.

Therefore the full first-order AeST intrinsic density represented by the frozen spherical action is preregistered as

`delta rho_A = Q K_QQ delta Q + [1/(a r^2)] d_r{r^2[K_B E_1 + C X_1]}`.

Using the certified C7A identities

`E_1 = (d_r E_A)/a`

and

`X_1 = (d_r chi)/a`,

this becomes

`delta rho_A = Q K_QQ delta Q + a^-2 Laplacian[K_B E_A + C chi]`.

For a Fourier mode,

`delta rho_A(k) = Q K_QQ delta Q(k) - (k^2/a^2)[K_B E_A(k)+C chi(k)]`.

## Frozen current bridge semantics

Repair14 must statically certify all of the following from the frozen repository:

1. C7A preregistration states the current bridge
   `deltaQ = rho_A delta_A/(Q K_QQ)`.
2. The frozen B4 reconstruction implements
   `dq=inv(k,(rho/(Q*KQQ))*F['delta_A'],r)`.
3. The frozen v0.19 CLASS patch inserts the AeST effective component into total perturbed density as
   `delta_rho += rho_dark*delta_A`
   using the reused CDM slot.
4. In that same stress-energy patch, the combination
   `K_B E_A + C chi`
   enters `Pi_aest` / pressure, but there is no corresponding explicit E/chi gradient contribution added to `delta_rho`.

This is a code-interface audit only. Repair14 does not alter the CLASS patch.

## Consequence to test

If CLASS `delta_A` is the total effective-fluid density perturbation, the action-level identity implies

`rho_A delta_A = Q K_QQ delta Q + delta rho_E`

with

`delta rho_E = [1/(a r^2)] d_r{r^2[K_B E_1+C X_1]}`.

Hence the scalar-Q perturbation consistent with the full frozen action is

`delta Q_full = delta Q_current - delta rho_E/(Q K_QQ)`.

Equivalently in Fourier space,

`delta Q_full(k)=delta Q_current(k) + k^2[K_B E_A(k)+C chi(k)]/(a^2 Q K_QQ)`.

This correction is a **diagnostic derived quantity only**. It may not be written as an official state in Repair14.

## Numerical audit

Use the exact frozen Repair08 state and Repair12 11-source evaluator.

Retain all:

- scales `5,10,20 h^-1 Mpc`;
- grids `Nr=256,512`;
- Y families `Simple,Exponential,Sharp`;
- beta `1.0,0.5,0.1`;
- all non-center points;
- eta=0.

### A. Analytic E-sector profile

For each scale/grid pair compute from the frozen state

`E_1=u_dot+H u`

`X_1=Q u+phi_r/a`

and

`A_E = -2 a^2 d_r{r^2[K_B E_1+C X_1]}`.

Also report E2 and EX pieces separately.

### B. Derived K-density correction

Define

`delta rho_E = d_r{r^2[K_B E_1+C X_1]}/(a r^2)`

on non-center points and diagnostic

`Delta deltaQ = -delta rho_E/(Q K_QQ)`.

The induced first-order K-source correction is

`A_Kcorr = -2 a^3 r^2 Q K_QQ Delta deltaQ`.

Require

`A_Kcorr + A_E = 0`

to normalized L2 error `<=1e-12` on every scale/grid pair.

No center value is used in this gate.

### C. Diagnostic corrected-density path

Create in memory only a diagnostic copy of each frozen Repair08 state with

`phidot_minus_Q -> phidot_minus_Q + Delta deltaQ`

at unit perturbation amplitude, with a finite center placeholder that is excluded from all gates.

Use the **same Repair12 virtual lambda path** and exact 11-source evaluator.

At positive amplitudes

`lambda={1,1/2,1/4,1/8}`

compute baseline-subtracted full Hamiltonian numerator norms.

Use the same asymptotic slope gates already frozen in Repair12:

- `1/2 -> 1/4`;
- `1/4 -> 1/8`;
- accepted interval `[1.8,2.2]`.

All 54 corrected diagnostic cases must satisfy the second-order Hamiltonian slope gate.

The original unmodified state and historical Repair12 first-order slopes remain reported and unchanged.

### D. Momentum non-interference

Because the diagnostic `deltaQ` correction changes K_Q only at first order while the K momentum source is proportional to `phi_r K_Q`, its effect on radial momentum begins at second order.

Repair14 must verify on the corrected diagnostic path that the full momentum residual remains asymptotically second-order under the same `[1.8,2.2]` gates.

## Gates

### R14_G1 — frozen provenance

Require exact Repair08, Repair10, Repair11, Repair12, Repair13, and Repair13a hashes/classes, Repair13a result-freeze ancestry, exact dense coverage, and frozen code blobs.

### R14_G2 — exact Hamiltonian E/X gauge identities

All preregistered `partial_N` and `partial_Nr` identities must simplify exactly.

### R14_G3 — exact B3 first variations

The symbolic first-order E2, EX, K intrinsic-density, and combined density identities must simplify exactly to the preregistered formulas.

### R14_G4 — frozen current-bridge semantics

All four static repository statements above must be found exactly in the frozen C7A/B4/v0.19 code or preregistration.

### R14_G5 — analytic E-sector / K-correction cancellation

For all six scale/grid pairs,

`||A_Kcorr+A_E||_2 / max(||A_E||_2,||A_Kcorr||_2) <= 1e-12`.

### R14_G6 — corrected diagnostic Hamiltonian becomes second order

All 54 corrected diagnostic cases must have both gated Hamiltonian L2 slopes in `[1.8,2.2]`.

### R14_G7 — corrected diagnostic momentum remains second order

All 54 corrected diagnostic cases must have both gated momentum L2 slopes in `[1.8,2.2]`.

### R14_G8 — no historical relabel / no state mutation

Require:

- official Repair08 state not written or modified;
- historical B4 FAIL preserved;
- historical Repair12 first-order Hamiltonian result preserved;
- historical Repair13 implementation failure preserved;
- Repair13a PASS preserved;
- no coefficient/sign/source/threshold change;
- no point, scale, Y, or beta selection;
- no nonlinear evolution;
- no finite eta;
- no observational-detection claim.

## Terminal classifications

Allowed:

- `NL1C7B4_REPAIR14_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED`;
- `NL1C7B4_REPAIR14_HAMILTONIAN_ESECTOR_INTERFACE_MISMATCH`;
- `NL1C7B4_REPAIR14_IMPLEMENTATION_FAIL`.

The omission classification requires all eight gates.

It means only that the frozen C7A effective-density to scalar-Q map omits the finite-gradient E-sector term required by the already frozen spherical action and CLASS effective-density semantics, and that inserting the analytically derived term in a diagnostic copy removes the first-order Hamiltonian residual.

It does not modify the official state and does not make historical B4 pass.

Any actual Repair08/C7A state correction requires a new separately preregistered representation repair after Repair14 is frozen.
