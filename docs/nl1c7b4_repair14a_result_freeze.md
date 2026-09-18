# NL1C7B4 Repair14a — local result freeze

## Status

Frozen local WSL PASS result from the first locked Repair14a execution.

Terminal classification:

`NL1C7B4_REPAIR14A_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED`

Science return code:

`SCIENCE_RC=0`

Local execution HEAD:

`47ba56b8a85b4f159772a27eef5fe9e1058e93cf`

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- JSON SHA-256:
  `d60398e2804222df70e8cd3acda5fb397e9cfdd2068415b9256af4d65a5c64ca`
- evaluator log SHA-256:
  `9d1efba41465136b31d33518043e87e07efed6c0ce5505b32ea7060b6d9fb5e3`
- local runner log SHA-256:
  `2c079510cb10c3fe76acb1e3a401aec40fe249222a609abf3117dc926bd99128`

## Gate result

All Repair14a gates PASS:

- R14A_G1 historical attempt01 hash and gate pattern: PASS
- R14A_G2 decoded static-semantics parser: PASS
- R14A_G3 inherited Repair14 all gates: PASS
- R14A_G4 claim boundary: PASS

All inherited Repair14 gates G1..G8 are true.

The decoded v0.19 active effective-density line is exactly

`ppw->delta_rho += rho_dark*y[ppw->pv->index_pt_delta_cdm];`

and no decoded `ppw->delta_rho +=` line contains `E_aest` or `chi_aest`.

The repaired parser reproduces the complete Repair14 attempt01 science payload exactly.

## Certified numerical result

Number of analytic scale/grid profile pairs:

`6`

Number of corrected diagnostic cases:

`54`

Worst analytic cancellation residual:

`max ||A_Kcorr+A_E||_2 / max(||A_Kcorr||_2,||A_E||_2)
 = 1.507283138497687e-14`

against the frozen limit

`1e-12`.

Corrected Hamiltonian gated slope interval observed:

`1.975869030883205 .. 2.0453928575447495`

Corrected momentum gated slope interval observed:

`2.005505202700859 .. 2.0397779030678223`

All values are inside the preregistered `[1.8,2.2]` interval.

## Scientific interpretation licensed by Repair14a

The frozen current C7A/B4 density-to-Q relation

`deltaQ_current = rho_A delta_A/(Q K_QQ)`

omits the finite-gradient E/X contribution required by the first-order Hamiltonian identity

`delta rho_A(k)
 = Q K_QQ deltaQ(k)
 - k^2/a^2 [K_B E_A(k) + (2-K_B) chi(k)]`.

Therefore the first-order-consistent scalar relation is

`deltaQ_full(k)
 = deltaQ_current(k)
 + k^2/[a^2 Q K_QQ] [K_B E_A(k) + (2-K_B) chi(k)]`.

This identifies an interface/representation omission. It does not identify an error in the AeST `K_B E^2` coefficient or sign.

## Preserved historical boundaries

- historical Repair14 attempt01 remains `IMPLEMENTATION_FAIL`;
- historical Repair09/B4 remains raw-constraint FAIL;
- Repair08 official NPZ remains unchanged;
- no coefficient, sign, source, threshold, radial subset, Y family, beta, or scale was changed;
- no nonlinear evolution was run;
- eta remains zero;
- no observational claim is made.

## Continuation

A separately preregistered Repair15 may construct a new certified eta=0 state representation whose only physical-state change relative to Repair08 is the first-order density-Q bridge completion in `phidot_minus_Q`.

Repair15 must then be consumed by a separate exact nonlinear B4 retest under the original `1e-7` raw-constraint threshold.
