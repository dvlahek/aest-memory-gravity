# ACT DR6 exploratory lensing R8 — Limber-switch localization diagnostic

Date: 2026-09-11

Status: frozen after R7 GR pipeline control and before any R8 output.

## Historical status preserved

R7 established that the CLASS -> C_L^{kappa kappa} -> ACT DR6 lens-only pipeline is numerically consistent in GR, with a normal 10-bin ACT chi-square. R6 therefore remains non-interpretable as an observational AeST result because the AeST eta=0 lensing spectrum shows an abrupt anomaly beginning at L=11.

The abrupt onset coincides with the CLASS default CMB-lensing full-Limber switch, l_switch_limber=10, for which the full-Limber branch is used when L>10.

## Purpose

R8 is a pure numerical localization test. It does not fit ACT data and does not claim a physical constraint.

Question: does the abrupt AeST lensing anomaly move when the CLASS full-Limber transition is moved?

## Frozen theory

- same pinned CLASS SHA and AeST patch chain as R5-R7;
- same fixed cosmology as R5-R7;
- aest_enabled=yes;
- model Exp;
- K_B=0.0665;
- tau H0=1;
- memory order 39;
- eta=0;
- linear theory only;
- l_max_scalars=4000;
- output=tCl,pCl,lCl;
- lensing=yes;
- precision file v019p/pre/p3.pre apart from the explicitly varied Limber settings below.

## Frozen diagnostic cases

Run exactly four cases:

1. `switch10`: `want_lcmb_full_limber=yes`, `l_switch_limber=10`;
2. `switch40`: `want_lcmb_full_limber=yes`, `l_switch_limber=40`;
3. `switch100`: `want_lcmb_full_limber=yes`, `l_switch_limber=100`;
4. `full_limber_off`: `want_lcmb_full_limber=no`.

No other theory, precision, cosmology, memory, source, or output setting may be changed.

## Diagnostics

For every case:

- require finite and nonzero C_L^{kappa kappa} for L=2..2999;
- save the full spectrum and raw CLASS `_cl.dat`;
- record C_L^{kappa kappa} around the relevant transition region;
- for switch cases record the local adjacent ratio
  `J_s = C_{s+1}^{kappa kappa} / C_s^{kappa kappa}`;
- also record a smooth-background ratio using the immediately preceding pair
  `B_s = C_s^{kappa kappa} / C_{s-1}^{kappa kappa}`;
- record `J_s/B_s` as a simple switch-jump diagnostic.

For the full-Limber-off case record the same local ratios at L=10/11, 40/41 and 100/101 for direct comparison.

## Interpretation frozen before data

The following are diagnostic expectations, not pass/fail gates:

- if the anomaly is caused by the full-Limber branch/interface, a sharp local feature should track the chosen switch: near L=11 for switch10, near L=41 for switch40, and near L=101 for switch100;
- if the anomaly is physical and independent of the numerical branch, its location should not move with l_switch_limber;
- if disabling full-Limber removes the abrupt feature, that further supports a branch/interface origin.

No threshold for jump size is preregistered. No post-data retuning of switch values is allowed inside R8.

## Technical completion gate

R8 COMPLETE requires only:

1. provenance confirms this preregistration and R7 ancestry;
2. all four frozen cases execute successfully;
3. all four spectra are finite and nonzero for L=2..2999;
4. all preregistered diagnostic ratios are finite;
5. all raw outputs and summary arrays are saved.

Successful execution label:

`ACT_DR6_LENSING_EXPLORATORY_R8_LIMBER_SWITCH_LOCALIZATION_COMPLETE`

Otherwise:

`ACT_DR6_LENSING_EXPLORATORY_R8_LIMBER_SWITCH_LOCALIZATION_INCOMPLETE`

Always:

`OBSERVATIONAL_CLAIM_LICENSED=False`.
