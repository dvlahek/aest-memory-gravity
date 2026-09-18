# NL1C7B4 Repair15 — pre-data density-Q-completed eta=0 state representation

## Status

Pre-data / pre-run preregistration.

Repair14a locally certified:

`NL1C7B4_REPAIR14A_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED`

at result-freeze commit

`be1ad5287a22feb81e9fceef0483eefb17b1a800`.

Repair15 constructs a new state artifact. It does not relabel the historical Repair08 artifact and it does not itself certify B4.

## Problem

The certified Repair08 state uses the frozen historical relation

`deltaQ_current(k)=rho_A delta_A(k)/(Q K_QQ)`.

Repair14a identified that the Hamiltonian first variation requires

`delta rho_A(k)
 = Q K_QQ deltaQ(k)
 - k^2/a^2 [K_B E_A(k)+(2-K_B) chi(k)]`.

For the frozen CLASS effective-density input

`delta rho_A(k)=rho_A delta_A(k)`

the first-order-consistent state variable is therefore

`deltaQ_full(k)
 = rho_A delta_A(k)/(Q K_QQ)
 + k^2/[a^2 Q K_QQ] [K_B E_A(k)+(2-K_B) chi(k)]`.

This is a representation/interface completion. No action coefficient or source is changed.

## Frozen parents

Repair08:

- JSON SHA-256:
  `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`
- NPZ SHA-256:
  `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`
- result-freeze commit:
  `6a8812f9b8d9f4fa373212376b6c01b4649076aa`

Repair14a:

- local JSON SHA-256:
  `d60398e2804222df70e8cd3acda5fb397e9cfdd2068415b9256af4d65a5c64ca`
- result-freeze commit:
  `be1ad5287a22feb81e9fceef0483eefb17b1a800`

Dense trace remains the frozen Repair01 dense trace with exact 128 native k modes and 179 native times.

## Canonical construction

For each scale `s in {5,10,20} h^-1 Mpc`:

1. load the certified Repair08 primary `Nr=256` state directly from its NPZ;
2. retain every state field unchanged except `phidot_minus_Q`;
3. reconstruct the same frozen target profile on the same `NQ=256` logarithmic quadrature grid;
4. interpolate the retained CLASS transfer ratios `E_A/delta_b` and `chi/delta_b` in log-k with the same frozen PCHIP convention;
5. use the frozen background values at `a_i=0.02`:
   - `Q_bg` from the stable inversion of the frozen `K_Q` background;
   - `K_QQ_bg` from the retained dense trace;
6. form

`F_corr(k)
 = k^2/[a_i^2 Q_bg K_QQ_bg]
   [K_B F_EA(k)+(2-K_B)F_chi(k)]`;

7. inverse-transform `F_corr` with the frozen spherical reconstruction;
8. set only

`phidot_minus_Q_new(r)
 = phidot_minus_Q_Repair08(r)+deltaQ_corr(r)`.

No other official state array may change.

## Transfer-level identity gate

On the exact quadrature representation, require

`Q_bg K_QQ_bg F_corr
 - k^2/a_i^2 [K_B F_EA+(2-K_B)F_chi] = 0`

with symmetric relative-L2 error

`<= 1e-12`

for all three scales.

## Real-space density-Q identity gate

Construct independently on the same quadrature grid

`F_density_E
 = -k^2/a_i^2 [K_B F_EA+(2-K_B)F_chi]`

and

`F_rho_delta = rho_A F_delta_A`.

After spherical inverse transforms require

`Q_bg K_QQ_bg deltaQ_full
 + delta_rho_E
 - rho_A delta_A = 0`

with symmetric relative-L2 error

`<= 1e-12`

on all radial points for all three scales.

This is a representation identity check, not a B4 constraint gate.

## State-regression gate

For every Repair08 primary state field other than `phidot_minus_Q`, require relative-L2 reproduction

`<= 1e-12`.

The new `phidot_minus_Q` is allowed to differ and its relative and absolute changes are reported without a fitted bound.

All arrays and background quantities must be finite.

## Metadata gate

The new NPZ must retain:

- `a_i=0.02`;
- scales `[5,10,20]`;
- the exact 128-mode native k grid;
- the frozen `h`;
- all Repair08 state fields;
- a new metadata marker identifying the density-Q completion.

The new NPZ is written only if every Repair15 gate passes.

## Claim boundary

Repair15 forbids:

- overwriting or modifying the historical Repair08 NPZ;
- changing `K_B`, `2-K_B`, any sign, or any action/source term;
- constraint projection;
- solving for a correction from B4 residuals;
- fitting a coefficient or amplitude;
- clipping;
- radial-point removal;
- scale/Y/beta selection;
- threshold change;
- nonlinear evolution;
- finite eta;
- B4 PASS relabeling;
- observational claims.

Repair15 may use only the analytic bridge completion certified by Repair14a.

## Gates

- R15_G1 frozen Repair08 + Repair14a provenance
- R15_G2 exact Fourier density-Q completion identity
- R15_G3 real-space density-Q identity
- R15_G4 unchanged Repair08 state-field regression
- R15_G5 metadata/output integrity
- R15_G6 claim boundary

## Terminal classifications

PASS:

`NL1C7B4_REPAIR15_DENSITY_Q_COMPLETED_STATE_CERTIFIED`

FAIL:

`NL1C7B4_REPAIR15_IMPLEMENTATION_FAIL`

A PASS licenses only a separately preregistered exact nonlinear B4 retest under the original raw constraint limit `1e-7`.

Historical Repair08, Repair09/B4, Repair12, Repair13, Repair14 attempt01, and Repair14a classifications remain unchanged.
