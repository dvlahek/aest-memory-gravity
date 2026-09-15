# Stable AeST DESI DR1 R9b2e repair01 — ordered raw-history mapping

## Status before repair

The first R9b2e execution terminated before any diagnostic/science gates were evaluated with

`STABLE_AEST_DESI_DR1_R9B2E_RUN_FAIL`

because the implementation required every scalar dictionary returned by `get_perturbations()` to contain an explicit k field. In the corrected CLASS build used here, the returned scalar histories contain the requested perturbation variables and time coordinates but do not contain a per-history k column.

The failed JSON has `diagnostic_complete=false` and `science_evaluated=false`; therefore this is a technical pre-result repair, not a reclassification of a science result.

## Existing repository convention

`nl1c6d2a/baryon_matter_sector_audit.py` already established and used the mapping convention for this same CLASS interface:

1. pass an ordered `k_output_values` request;
2. require `len(histories) == len(requested_k)`;
3. interpret returned scalar history `i` as the history for requested mode `i`.

That audit does not require a k field inside each raw history dictionary.

## Frozen repair

R9b2e repair01 changes only raw-history mode labeling:

- require exactly 24 returned scalar histories;
- preserve the returned order;
- assign history `i` the frozen requested `K_H[i]` value;
- report raw mode-assignment mismatch as exactly zero by construction of the ordered request/response mapping.

No sorting, nearest-neighbor reassignment, filtering, or data-dependent mode choice is allowed.

The following remain exactly unchanged from the R9b2e preregistration `756eb268bdc4d0c3ba8dc6bfa94ba74eb11bdab1`:

- the 24 requested k modes;
- six theory redshifts;
- eta=0 and tau_H0=10;
- default CLASS k sampling;
- CLASS source/build;
- output fields;
- cubic and PCHIP interpolation;
- continuity definition;
- raw-to-transfer closure definitions;
- all thresholds and all E1–E7 gates;
- all classifications.

No DESI data vector, covariance, or likelihood is loaded.

## Audit rule

The original failed R9b2e execution remains recorded as a technical RUN_FAIL. Repair01 is a rerun of the same preregistered diagnostic after fixing only the invalid assumption that each raw history carries an explicit k column.
