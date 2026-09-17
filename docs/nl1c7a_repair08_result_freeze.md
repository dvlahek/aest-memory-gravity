# NL1C7A Repair08 — result freeze

## Status

The locked local Repair08 execution is frozen as

`NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED`

with `SCIENCE_RC=0`.

This certifies a new eta=0 identity-preserving C7A initial-state representation only. It is not a B4 initial-constraint PASS, does not license finite eta or nonlinear evolution, and is not an observational detection claim.

## Exact local artifacts

The retained uploaded outputs from the locked local execution have the following SHA-256 digests:

- result JSON: `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`, size `33016` bytes;
- evaluator log: `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`, size `33016` bytes;
- local runner log: `89f392f80d9ada9c9c4b49f0348f71ecd12048a39aebbf03821b03d682aed897`, size `39815` bytes;
- certified Repair08 state NPZ: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`, size `103024` bytes.

The NPZ contains 52 arrays/metadata entries, including 128 native k modes, `a_i=0.02`, scales `[5,10,20] h^-1 Mpc`, and `h=0.6733246390848661`.

## Locked certification result

All ten Repair08 gates passed:

- `R8_G1_provenance_and_retained_inputs = true`;
- `R8_G2_A5_denominator_recheck = true`;
- `R8_G3_identity_preserving_scalar_construction = true`;
- `R8_G4_A6_time_interpolation_control = true`;
- `R8_G5_A7_k_interpolation_control = true`;
- `R8_G6_A8_target_profile_reconstruction = true`;
- `R8_G7_A9_bridge_identities = true`;
- `R8_G8_A10_no_free_mode_injection = true`;
- `R8_G9_unchanged_state_regression = true`;
- `R8_G10_claim_boundary = true`.

Observed maxima were:

- A6 time-interpolation control: `0.002656978791225328 <= 0.02`;
- A7 k-interpolation control: `0.0016264270315724991 <= 0.02`;
- A8 target-profile reconstruction: `6.299255876536103e-07 <= 1e-4`;
- A9 bridge identity: `5.13783497070517e-07 <= 1e-6`;
- unchanged-state regression: `2.1477900069165766e-16 <= 1e-12`.

## Scalar identity result

The canonical Repair08 scalar route

`PCHIP(log(a), a Q theta_A / k^2)`

formed after constructing the composite on each native time grid agrees with the independent

`PCHIP(log(a), chi - Q alpha_A)`

route at `a_i` to relative L2

`2.3926238952144846e-14`.

The historical componentwise route differs from the canonical route at `a_i` by

`9.340086572234657e-06` relative L2.

The cancellation condition is substantial: median `573.6227954632575`, maximum `9432.352502865602`.

## Isolation of the repair

Only the preregistered scalar quantities changed materially:

- `phi`: relative L2 vs historical C7A = `7.750034623845909e-04`, `9.698081569231137e-04`, `4.8341602189623577e-04` for scales 5, 10, 20;
- `X_from_state`: relative L2 vs historical C7A = `4.0090122665534695e-07`, `3.1909640106950637e-07`, `3.5943559648341304e-07`.

Every other reconstructed state quantity agrees with the historical certified C7A NPZ to at most `2.1477900069165766e-16` relative L2.

No coefficient was changed or fitted, no source was inserted, no clipping or radial-point removal was used, no historical threshold was changed, and the historical C7A NPZ was not overwritten.

## Licensed continuation

The only licensed continuation is a separately preregistered B4 initial-constraint retest that consumes this certified Repair08 NPZ under the unchanged historical B4 definitions and thresholds. The historical B4/R05/R06 failures remain preserved and must not be reclassified.
