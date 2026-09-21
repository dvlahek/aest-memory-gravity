# GE19 Repair16 canonical-zero initial-state audit result freeze

## Status

Frozen first locked Repair16 local diagnostic execution.

Terminal classification:

`GE19_REPAIR16_CANONICAL_ZERO_INITIAL_STATE_AUDIT_COMPLETE`.

Frozen routing:

`QUADRATIC_SOURCE_NOETHER_INCOMPATIBILITY_REMAINS`.

Repair14 remains historical H3/Z20 FAIL. Repair15 and Repair16 are diagnostic only.

## Frozen local outputs

Science JSON:

- bytes: `1366591`;
- SHA-256: `768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68`.

Inner FULL log:

- bytes: `1366591`;
- SHA-256: `768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68`.

Outer local runner log:

- bytes: `1371121`;
- SHA-256: `bd22d8eead36929cabdf34172e0c32353e8aab7d97f4ce9a951bbc71d9700c2e`.

The JSON and inner FULL log are byte-identical.

Terminal marker:

`GE19_REPAIR16_DIAGNOSTIC_COMPLETE`.

## Provenance

Repair13 JSON/NPZ, Repair14 JSON and Repair15 JSON hashes match the frozen preregistered parents exactly.

Repair16 does not recompute H1 or the Repair14 Z20 trajectory.

## Global diagnostic result

- initial source norm max: `91405511.46291333`;
- material cases: `714` / `720`;
- algebraic relative residual max: `7.465407808870082e-16`;
- independent lapse backward error max: `1.0`;
- independent shift backward error max: `1.0`;
- anisotropy backward error max: `6.394777335818628e-16`;
- determined qdot L2 max: `1.6277578323698383e-4`;
- local algebraic scaled condition number max: `3.1343173893632996`;
- all material outputs finite: true.

Frozen thresholds were:

- algebraic <= `1e-8`;
- lapse <= `1e-6`;
- shift <= `1e-6`.

Thus canonical y0=0 decisively fails the independent lapse and shift constraints while the eliminated algebraic system and anisotropy close to machine precision.

## Representative material case

Primary, C_min, beta0=1, m=2:

- source norm `3450614.1792420684`;
- algebraic residual `1.7979958682378425e-16`;
- lapse metric `1.0`, target abs `72285.15937577699`, lhs abs `7.019204541351992e-14`;
- shift metric `1.0`, source abs `6.297479197581789e-9`, lhs abs `6.462348535570529e-27`;
- anisotropy metric `1.1873883861820054e-16`;
- local condition number `2.6193609643053004`.

The same pattern repeats across material modes: eliminated rows close, while lapse and shift remain source-dominated.

## Interpretation boundary

Repair16 falsifies the hypothesis that the Repair14 failure is explained solely by using q=0,qdot=0 instead of the natural canonical y=(q,p)=0 boundary.

It does **not yet prove** that the underlying GE06+GE07+Lambda quadratic physics violates the nonlinear Noether/Bianchi identity.

The next permitted diagnostic must decompose the frozen Repair14 quadratic source sector-by-sector and test the source against the exact linear Noether/Bianchi compatibility relation. It must also verify component ordering/signs between the quadratic source bundle and the canonical source vector.

A source-component wiring/sign error remains distinct from a physical source-identity failure.

## Stop rule

No Repair14 rerun, no q20, no H4/Z21 and no threshold relaxation are licensed.

A new H3 trajectory is forbidden until the quadratic source compatibility issue is localized and repaired under a separate preregistration.

## Claim boundary

Repair16 certifies only that canonical-zero initialization does not restore the independent lapse/shift constraints for the frozen Repair14 source.
