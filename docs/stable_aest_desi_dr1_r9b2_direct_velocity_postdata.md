# Stable AeST DESI DR1 R9b2 direct-velocity post-data lock

Status: historical post-data record. This result is never reclassified.

## Frozen result

The completed R9b2 direct-velocity ShapeFit run returned
`STABLE_AEST_DESI_DR1_R9B2_CENTRAL_DERIVATIVE_FAIL`.
All 20 preregistered `(tau_H0, eta)` theory workers completed with finite output.
Gates G1--G3 passed and G4 failed; G5--G6 were therefore not evaluated as science gates.

Frozen central-derivative metrics:

| tau_H0 | E | C | ||T_primary|| |
|---:|---:|---:|---:|
| 10.0 | 0.8397265648803398 | 1.0 | 8.635056576442666e60 |
| 5.0 | 0.8373532081798006 | 1.0 | 8.507510702391644e60 |
| 2.5 | 0.8325560188357494 | 1.0 | 8.260548606631327e60 |
| 1.25 | 0.8229355735214521 | 1.0 | 7.804621436260084e60 |

No DESI likelihood/projection result was licensed because G4 failed. `tau_likelihood` is empty.
The historical R9b proxy result also remains unchanged.

## Uploaded artifact hashes

These hashes identify the completed local result inspected after the run:

- JSON: `b0afd658758eb63708f837884f9e236f945879a97b56daef571abb9342ab4697`
- science log: `082497b66070a4bc6eff4b3c618a2ef7cea2b9e1d7c120820899e60211b09620`
- full runner log: `c3470b854b1c3a44497fef1485eae4c85fad886f79069cab97ad98480259f995`
- NPZ: `84717a0e23a6e0ca83bafbe9e7fc6aa51c25d26aeac68251c0ba7eac077cfcb2`
- bundle ZIP: `66877d7a067819df4c945d1aea83760fe0f6266e8fcd1f42c58186731181aaaf`

## Post-data forensic observation

Inspection of the worker bundle showed that the new external direct-spectrum extraction is pathological already for `eta=0` at selected DESI redshifts, despite normal legacy integrated growth diagnostics. Examples from the frozen `tau_H0=10, eta=0` worker include external `sigma8(Pdd)` values of order `8.1e4` and `7.2e12` in two low-redshift bins, and direct velocity-growth values ranging from about `4e-5` to `2.7e58`, while the legacy integrated growth proxy remains order unity and smooth. Other bins remain normal.

This is not used to alter the historical R9b2 classification. It motivates a new, separate theory-only extraction-invariance audit before any further DESI science evaluation.

A key provenance fact is that the R9b2 workers report bit pattern `4592669915990485346`. Existing pre-R9b2 ULP-forensics code identifies this exact bit as the first member of the certified adjacent-ULP pair at canonical `k_h=0.165`. R5b deliberately inherits that canonical diagnostic output coordinate through `k_output_values`. A broadband integral must therefore first demonstrate invariance to this diagnostic output request before the direct-spectrum extraction can be treated as a physical continuous-`k` observable.

## Claim discipline

- This historical R9b2 result is a failed extraction/gating test, not a DESI detection or exclusion.
- It does not license a statement that the AeST memory response is physically nonlinear.
- No threshold, nuisance model, eta interval, or DESI datum is changed after seeing this result.
- Any repair must be preregistered and validated theory-only before another DESI likelihood/projection run.
