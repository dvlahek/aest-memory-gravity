# Stable AeST DESI DR1 R9b2b provenance repair01

## Status

This is a pre-science technical repair. The first R9b2b invocation exited with code 3 before Python science execution because the runner compared the locally generated R9b2a JSON against a hard-coded SHA-256.

No CLASS model run, R9b2b source-state extraction, DESI data evaluation, or R9b2b gate result occurred before this repair.

## Problem

The R9b2a JSON is a local generated result and was never committed as a canonical repository artifact. Only its post-result interpretation was committed at

`00d06aa140fc8e9097be3df62ecd6013f0c8b312`.

Therefore an exact byte-level SHA lock on the local R9b2a JSON is not a valid repository provenance requirement. It can reject a semantically identical regenerated result because of byte-level differences that are not part of the frozen science state.

The R9b2 velocity-adapter JSON is different: it is committed in the repository and retains its exact SHA lock.

## Frozen repair

Replace the R9b2a JSON SHA gate with semantic validation against the already locked R9b2a post-result state.

Required R9b2a fields after repair:

- `classification == STABLE_AEST_DESI_DR1_R9B2A_SERIALIZATION_FREE_EXTRACTION_UNRESOLVED`
- `diagnostic_complete == true`
- `science_evaluated == false`
- gate pattern exactly:
  - `R9B2A_A1_provenance_and_historical_fail_lock == true`
  - `R9B2A_A2_internal_output_request_invariance == true`
  - `R9B2A_A3_serialization_free_density_consistency == false`
  - `R9B2A_A4_serialization_free_direct_velocity_sanity == false`
  - `R9B2A_A5_eta0_tau_invariance == true`
  - `R9B2A_A6_material_diagnostic_output_contamination == false`

The runner may print the observed local R9b2a SHA for audit purposes, but it must not gate on that SHA.

No threshold, source-state formula, redshift, tau, eta, GR benchmark, AeST closure test, or R9b2b classification rule is changed.

## Historical results

R9b2 and R9b2a historical classifications remain unchanged. This repair does not reclassify or reinterpret either result.
