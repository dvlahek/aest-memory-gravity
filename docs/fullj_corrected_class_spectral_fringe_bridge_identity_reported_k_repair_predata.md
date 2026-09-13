# Full-J bridge-identity reported-k repair

Date: 2026-09-13

## Historical incomplete run

The first bridge-identity audit stopped before evaluating any BI science gate because `classy.get_perturbations()` returned scalar history dictionaries with no explicit physical-k field. The available keys were the perturbation variables and time/scale-factor coordinates only. Therefore the preregistered reported-k selector could not be evaluated. This historical run remains `FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_INCOMPLETE`; it is not a physics result and does not alter R3 or the completed extractor-equivalence classification.

## Repair principle

Replace only the unavailable reported-k identification layer with an empirical single-k fingerprint mapping. No physical equation, cosmological/AeST parameter, frozen k value, redshift, science tolerance, prior array, or classification priority is changed.

For each frozen anchor `k/h`, and separately for the R3/direct parameter family and historical bridge parameter family:

1. run an isolated CLASS calculation with `k_output_values` containing only the target k;
2. evaluate the resulting unique `phi+psi` history at the frozen redshifts to obtain a target fingerprint;
3. run the preregistered historical 6/7-k bridge list;
4. evaluate every returned history at the same redshifts;
5. identify the returned history whose full redshift fingerprint has minimum relative L2 distance to the isolated target fingerprint.

This does not assume that `get_perturbations()` preserves request order and does not require a k field inside the returned dictionary.

## Fingerprint gate

For each target and parameter family, the best matching history must satisfy relative L2 <= `2e-5`. The best match must also be unique: the second-best distance must exceed the best distance by at least the larger of `1e-8` absolute or a factor `5`. If the target cannot be uniquely fingerprinted, the repaired audit is incomplete.

The historical positional index is then compared with the fingerprint-matched index. Equality is the repaired BI-G4 history-order identity. Inequality certifies `FULLJ_CLASS_FRINGE_BRIDGE_HISTORY_MAPPING_DEFECT`.

## Existing gates retained

BI-G1, BI-G2, BI-G3, BI-G5, BI-G6, their global/per-anchor tolerances, and classification priority remain exactly as preregistered in `fullj_corrected_class_spectral_fringe_bridge_identity_predata.md`. B1/B2 use the fingerprint-matched target histories. B3 uses the historical positional history. BI-G4 passes only if positional and fingerprint indices agree for every anchor and B3 reproduces B2 within the original tolerances.

## Scope

The repair addresses only an unavailable API metadata field. The previous failed execution is preserved as technical INCOMPLETE. A `FULLJ_CLASS_FRINGE_BRIDGE_TECHNICAL_CAUSE_NOT_FOUND` result remains the only outcome licensing equation-level mode/dispersion follow-up, and still does not itself establish new physics.
