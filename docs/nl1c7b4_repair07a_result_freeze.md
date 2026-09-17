# NL1C7B4 Repair07a — result freeze

## Status

Historical local Repair07a execution is frozen as

`NL1C7B4_REPAIR07A_IMPLEMENTATION_FAIL`

with `SCIENCE_RC=2`.

This is not a B4 physics failure. Repair07a reached all requested diagnostics, but the preregistered G3 gate failed because the full serialized native dense trace did not satisfy the cancellation-sensitive relative-L2 identity at the locked `1e-10` algebra threshold.

## Observed locked result

- state reproduction: `2.8776273478160806e-14` <= `1e-12` — PASS.
- symbolic K exact shift residual: `0` — PASS.
- symbolic K Frechet residual: `0` — PASS.
- GR Repair05 vs closed form: PASS at both radial resolutions for all three scales; representative values range from about `4.68e-14` to `1.33e-11`, below `1e-10`.
- Fourier represented-sector 0i maximum symmetric residual: `0.007477020863006294` <= inherited `0.02` envelope — PASS.
- Fourier median residual: `3.938998171668772e-05`.
- initial-slice composite-first vs theta identity: `2.3926238952144846e-14` — well below `1e-10`.
- current componentwise vs composite-first scalar bridge at `a_i`: `9.340086572380209e-06` relative L2.
- full serialized native-trace identity: `1.5898457860349032e-07` — FAIL against the preregistered `1e-10` G3 threshold.
- cancellation condition across the serialized trace: minimum `1.5239701080886348`, median `573.6227954632575`, maximum `9432.352502865602`.

## Radial diagnostic consequence

The composite-first diagnostic route changes only the scalar representation and does not write a new state. The global radial linear-momentum residual changes as follows:

- scale 5, Nr 256: `0.0023884424883889714` -> `8.697877243471949e-06`.
- scale 5, Nr 512: `0.0023851363277469935` -> `8.69207752338775e-06`.
- scale 10, Nr 256: `0.0015824163513875108` -> `2.850771864355484e-05`.
- scale 10, Nr 512: `0.0015796251517141578` -> `2.8447280806758092e-05`.
- scale 20, Nr 256: `0.001872255448969544` -> `6.664093244755302e-05`.
- scale 20, Nr 512: `0.0018653797386362259` -> `6.661086799212653e-05`.

Pointwise epsilon maxima remain non-negligible and are not removed or reinterpreted. No B4 PASS is claimed.

## Interpretation boundary

Repair07a cannot be relabeled as PASS. The failed G3 definition is preserved exactly as preregistered.

The result nevertheless separates the observed issue:

1. exact K and GR first-variation identities are consistent;
2. the represented Fourier 0i bridge is inside the inherited C7A envelope;
3. the initial-slice composite identity itself is accurate at about `2.4e-14`;
4. the only failing Repair07a implementation gate is the full-time serialized-trace relative-L2 identity, a quantity outside the actual B4 initial-slice test and strongly exposed to cancellation in the stored trace;
5. the frozen current C7A NPZ remains immutable and the historical Repair06 mismatch remains unchanged.

A new preregistration is required before changing the G3 diagnostic domain or metric.
