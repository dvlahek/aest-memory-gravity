# NL1C7B4 Repair07b — result freeze

## Status

The locked local Repair07b execution at branch head `2c4811089045479cbfc9d634468509384420d6f8` is frozen as

`NL1C7B4_REPAIR07B_INITIAL_SLICE_BRIDGE_DIAGNOSTIC_PASS`

with `SCIENCE_RC=0` and `EXIT=0`.

This is a diagnostic PASS only. It is not a B4 initial-constraint PASS and does not license finite eta or nonlinear evolution.

## Locked gates

All preregistered Repair07b gates passed:

- `R7B_G1_provenance_and_immutability = true`.
- `R7B_G2_exact_covariant_identities = true`.
- `R7B_G3_initial_slice_scalar_identity = true`.
- `R7B_G4_inherited_C7A_fourier_interface_envelope = true`.
- `R7B_G5_no_post_result_repair = true`.

The historical Repair07a full-time serialized-trace failure remains preserved and non-gating under Repair07b.

## Exact observed diagnostics

- official C7A state reproduction: `2.8776273478160806e-14` <= `1e-12` — PASS.
- initial-slice identity-preserving scalar comparison: `2.3926238952144846e-14` <= `1e-10` — PASS.
- current componentwise vs identity-preserving scalar transfer at `a_i`: `9.340086572380209e-06` relative L2.
- historical full serialized-trace identity: `1.5898457860349032e-07`; this remains FAIL against the historical Repair07a `1e-10` definition and is not reclassified.
- symbolic K exact shift residual: `0`.
- symbolic K Frechet residual: `0`.
- GR Repair05 vs closed-form control: PASS for all retained scales and both radial resolutions, with observed relative L2 from approximately `4.68e-14` to `1.33e-11`.
- represented-sector Fourier 0i maximum symmetric residual: `0.007477020863006294` <= inherited `0.02` envelope — PASS.
- represented-sector Fourier 0i median residual: `3.938998171668772e-05`.

Weighted represented-sector Fourier residuals over the target profiles were:

- scale 5: `8.154300351963885e-06`;
- scale 10: `2.3338517580845122e-05`;
- scale 20: `6.876744562294871e-05`.

No unrepresented source was fitted or inserted.

## Radial representation diagnostic

Changing only the scalar representation in memory from the historical componentwise route to the identity-preserving composite route changed the global linear-momentum residual as follows:

- scale 5, Nr 256: `0.0023884424883889714` -> `8.697877243471949e-06`;
- scale 5, Nr 512: `0.0023851363277469935` -> `8.69207752338775e-06`;
- scale 10, Nr 256: `0.0015824163513875108` -> `2.850771864355484e-05`;
- scale 10, Nr 512: `0.0015796251517141578` -> `2.8447280806758092e-05`;
- scale 20, Nr 256: `0.001872255448969544` -> `6.664093244755302e-05`;
- scale 20, Nr 512: `0.0018653797386362259` -> `6.661086799212653e-05`.

The improvement is stable under the retained radial refinement. Pointwise maxima in tiny-denominator/tail regions remain reported and are not removed, clipped, or reinterpreted.

## Interpretation boundary

Repair07b establishes only that, at the B4 initial slice, the retained growing-mode trace is internally consistent with the exact scalar identity

`chi - Q alpha_A = a Q theta_A / k^2`

and with the represented Fourier 0i bridge at the inherited C7A tolerance.

It does not establish observational detection, B4 constraint certification, nonlinear evolution stability, or finite-eta behavior.

The historical certified C7A NPZ remains immutable. The only licensed continuation is a separately preregistered identity-preserving scalar-representation repair that writes a new artifact and re-certifies the C7A bridge before any B4 retest under the unchanged historical thresholds.
