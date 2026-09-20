# GE08 full first-order state bridge — implementation lock

## Status

Implementation locked before first GE08 execution.

GE08 is a diagnostic/state-dictionary bridge. It does not modify the AeST/CLASS evolution equations.

## Preregistration

Commit:

`e1b64e3c5e6a3141fde4f746d32bbc7743c4888c`.

File:

`ge08/predata_full_first_order_state_bridge.json`.

Frozen blob:

`250499e1df0a6442a53f4142d236a43ac5e5a113`.

## Diagnostic trace patch

Commit:

`105cbdda9b8cbd3ba456e855bc3bb3cd5de4ae95`.

File:

`ge08/apply_full_state_trace_patch.py`.

Frozen blob:

`20a3afe24a73b3512c5b5ea639466b8ca9bc3b8c`.

The patch adds only an accepted-source-grid diagnostic trace after the existing
`perturbations_einstein()` call.

It does not alter y, dy, pvecmetric, source tables, solver tolerances or any physical equation.

## Audit implementation

Commit:

`8578a61c59a824b3fa490c2b257d7af2ef13d370`.

File:

`ge08/full_first_order_state_bridge.py`.

Frozen blob:

`75ba7446053b257fc8b3ab28faea7a1d2756b8cc`.

## Pinned physics/runtime

- CLASS commit:
  `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- `KB=0.0665`;
- `eta=0`;
- historical `tau H0=10` baseline;
- Newtonian gauge;
- same v0.19/v0.23/v0.72 validated AeST patch chain;
- six signal-band k values:
  `{0.03,0.05,0.08,0.10,0.15,0.20} h/Mpc`;
- audit window:
  `0.2<=z<=1.5`.

## Frozen exact dictionary

Newtonian metric:

`ds^2=-(1+2 psi)dt^2+a^2(1-2 phi)delta_ij dx^i dx^j`.

Therefore the longitudinal 3+1 first-order metric mapping is

- `delta N=psi`;
- `delta L/a=-phi`;
- `delta R/a=-phi`;
- `delta b=0`.

AeST mapping:

- `u_A=a theta_dark/k^2`;
- `varphi=Q u_A`;
- `chi=varphi+Q alpha=Q(a theta_dark/k^2+alpha)`.

Aether rapidity:

At linear order the published `A_i=partial_i alpha` and the 3+1 coframe give

`A_x=a r=partial_x alpha`.

Thus the Fourier longitudinal rapidity-gradient amplitude is `(k/a)alpha` with the fixed Fourier derivative phase retained when reconstructing the real-space field.

Frozen E identity:

`alpha_prime=a(E_aest-psi)`.

## Frozen bridge gates

Require:

- legacy v0.23 and GE08 full traces have identical row counts;
- their k/tau grids agree to `1e-12` abs-or-rel;
- reconstructed chi agrees with the legacy chi trace to `1e-12` abs-or-rel;
- `alpha_prime=a(E-psi)` to `1e-12` abs-or-rel;
- `dy(phi)=phi_prime` to `1e-12` abs-or-rel;
- traced native `delta_m` agrees with CLASS `get_sources()['delta_m']` to `1e-12` abs-or-rel;
- requested k miss <= `1e-12`;
- native tau mismatch <= `1e-12`;
- at least eight native times in the frozen z window;
- all traced/derived values finite.

## Matter-completeness rule

Subtract the exact AeST effective-dark contribution from the CLASS total scalar stress.

Define standard-sector residuals

- `delta_rho_std`;
- `momentum_std`;
- `delta_p_std`;
- `shear_std`.

The full CLASS reference is exactly representable by the already certified single pressureless GE07 matter action only if

`||delta_p_std||/||delta_rho_std|| <=1e-12`

and

`||shear_std||/||delta_rho_std|| <=1e-12`.

This is an exact-closure readiness test, not a claim that standard cosmological matter is physically pressureless to arbitrary precision.

## Terminal classifications

Bridge and exact pressureless matter closure both pass:

`GE08_FULL_FIRST_ORDER_STATE_BRIDGE_H3_READY`.

Bridge passes but full standard matter is not exactly pressureless:

`GE08_FULL_FIRST_ORDER_STATE_BRIDGE_PASS_MATTER_INCOMPLETE`.

Any state/dictionary gate fails:

`GE08_FULL_FIRST_ORDER_STATE_BRIDGE_FAIL`.

## Claim boundary

GE08 does not solve `Z20` or `Z21`, introduce finite eta, or certify nonlinear collapse or observations.
