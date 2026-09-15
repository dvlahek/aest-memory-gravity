# Stable AeST DESI DR1 R9b2 — pre-result repair01

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Scope

This repair is declared before any R9b2 DESI science result.

The direct-velocity R9b2 implementation is already frozen in commit

`c10d18549ff1ab2ca6f948f7786dfdbc5225ab73`.

That implementation uses the validated primary mapping

`v_newtonian_x = -theta_x / Hconf`

and

`P_tt = P_cb * (v_cb / delta_cb)^2`,

with

`f_direct = sigma8(P_tt) / sigma8(P_dd)`.

The historical R9b proxy `effective_f_sigma8/sigma8` is retained only as a diagnostic comparison. In the initial R9b2 implementation, this diagnostic call was still unguarded. Therefore an exception raised by the obsolete proxy could incorrectly abort a direct-velocity science run even though the proxy no longer enters `df`, the tangent, nuisance projection, likelihood, or classification.

## Repair

Replace only the diagnostic block by a protected `try/except`:

- on success, record `old_proxy` and its relative difference from `f_direct`;
- on failure, record `old_proxy = NaN` and `old_proxy_rel_to_direct = NaN`;
- never use either value in a gate or science quantity.

No other source line is changed by this repair.

## Frozen invariants

This repair does not change:

- the validated CLASS-to-CAMB velocity normalization;
- the direct velocity/density spectra;
- DESI data or covariance;
- `tau H0 = {10,5,2.5,1.25}`;
- `eta = {0, +/-0.025, +/-0.05}`;
- G4 thresholds `E <= 0.05` and `C >= 0.995`;
- nuisance model;
- matched-filter / GLS gates;
- claim discipline.

R9b remains historically classified as

`STABLE_AEST_DESI_DR1_R9B_CENTRAL_DERIVATIVE_FAIL`.
