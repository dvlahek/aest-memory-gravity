# R9b pre-result methodological repair 01 — global, not per-bin, ShapeFit nuisance deprojection

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

Initial R9b preregistration: `f19f7ddb85ee37d86a516ebdf41d73b96aef311e`.

No R9b DESI likelihood result, eta estimate, chi-square improvement, or memory preference has been computed or inspected at the time of this repair.

## Problem found during implementation audit

The initial preregistration proposed one independent nuisance direction for `df` and one independent nuisance direction for `dm` in every ShapeFit redshift bin.

That design is over-complete for the intended test. The stable-AeST memory tangent in the ShapeFit compression enters primarily through the same `df` and `dm` components. Independent per-bin `df`/`dm` nuisance columns would therefore span almost the entire intended memory tangent by construction and could force the deprojected Fisher information toward zero independently of the data.

This is a methodological identifiability error, not a science outcome.

## Frozen repair

Replace the per-bin nuisance design with exactly two global nuisance columns across the concatenated six-bin ShapeFit vector:

1. `N_df`: nonzero only on all `df` entries, with values equal to the eta=0 theory `df` values in those entries. This profiles one common multiplicative growth-amplitude rescaling across all DESI ShapeFit bins.
2. `N_dm`: nonzero only on all `dm` entries, with value one in each `dm` entry. This profiles one common broadband-slope offset across all DESI ShapeFit bins.

No AP component (`qpar`, `qper`, `qiso`, `qap`) is nuisance-deprojected.

The covariance-metric projector remains

`P_perp = C^-1 - C^-1 N (N^T C^-1 N)^-1 N^T C^-1`,

where `N = [N_df, N_dm]` after dropping a column only if the corresponding parameter does not occur anywhere in the six-bin data vector.

The memory tangent is therefore tested through redshift-dependent and cross-observable departures that cannot be absorbed by one common growth normalization plus one common broadband slope shift.

## Unchanged items

Everything else in the initial R9b preregistration remains frozen and unchanged:

- official DESI repository and commit;
- v1.0 data URL;
- six non-Lyman-alpha bins;
- official ShapeFit observable;
- stable-AeST parent and source topology;
- tau grid `{10,5,2.5,1.25}`;
- eta central/control steps;
- ShapeFit construction and explicit `effective_f_sigma8/sigma8` velocity proxy disclosure;
- central-derivative, projection-algebra and matched-filter/GLS gates;
- physical eta interval `[0,0.05]`;
- no preregistered detection threshold;
- claim discipline requiring R9c full EFT/reptvelocileptors confirmation for any interesting preference.

Historical initial preregistration `f19f7ddb85ee37d86a516ebdf41d73b96aef311e` is not modified or reclassified.
