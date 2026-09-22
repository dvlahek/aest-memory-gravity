# GE19 Repair25 first-order bath boundary dictionary audit — implementation lock

## Status

Implementation locked after the dedicated Repair25 prelock audit completed successfully.

Dedicated prelock run:

- workflow run: `35714888171`;
- conclusion: `success`;
- head commit: `c63f3bd8ddf6da3619e8a955e38aa1da970a4efd`.

Repair25 remains diagnostic only. It does not rerun q20, modify a frozen threshold, adopt a fitted normalization, or license H4/Z21.

## Frozen parent

Repair24 remains the historical science FAIL

`GE19_REPAIR24_Q20_CONSTRUCTION_FAIL`

with exactly one failed frozen gate:

`H1_X10_initial_match_abs_or_rel_le_1e10`.

Repair24 result-freeze commit:

`82f1f56912f92e628797997d82ffd64de2a4a926`.

Repair24 result-freeze blob:

`3edde5ac2b751ce78bc42de5a6843934804f9b68`.

No Repair24 result is relabelled.

## Preregistration

Commit:

`d02245e5f23ece8fda49c10ede70caf453fd9976`.

File:

`ge19/repair25_predata_first_order_bath_boundary_dictionary_audit.json`.

Frozen blob:

`1e7f25eba5a4c8b297b563edfe6f9c4f276ec6c9`.

The preregistration freezes the exact a=0.4 comparison, the common overlap window, all thresholds, routing rules, and the rule that fitted factors are diagnostic only.

## Implementation

Commit:

`99d5ab968020d59de72ca588711946edf1d82975`.

File:

`ge19/repair25_first_order_bath_boundary_dictionary_audit.py`.

Frozen blob:

`d685dbbb0f7a64f5f80c43559bf19c55b64ca7b1`.

The implementation compares:

1. frozen v0.77 transported `chi/a`;
2. GE15 cancellation-free `chi/a = Q*(a*theta/k^2+alpha)/a`;
3. Repair22/GE19 on-shell `X10 = Q_action*u10 + (i k/a)*varphi10`.

It reports per-mode amplitudes/ratios/phases, Q closure, global and per-mode multiplicative fits, temporal-shape cosines, k-scaling, and preregistered candidate factors.

## Dedicated prelock

Workflow:

`.github/workflows/ge19-repair25-prelock-audit.yml`.

Frozen blob:

`90449e4e157415e56fd3b42375e9ef4d6b3ce4df`.

The prelock verifies the preregistration and implementation blobs, compiles the diagnostic, checks the exact GE09-to-GE19 algebraic identity synthetically, verifies all routing labels, and confirms that q20 construction code is absent.

Successful run:

`35714888171`.

## Frozen implementation dependencies

- `ge19/repair07_window_retarded_reduced_h3_z20_particular.py`:
  `e34d28a2062c748f48bc82fa928844b02631de25`;
- `ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py`:
  `dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7`;
- `ge19/repair13_self_consistent_reduced_background_h1_reclosure.py`:
  `362d63d03d7b850fceae393f535353ded79aeea7`;
- `ge09/repair01_dense_accepted_step_local_jet_bridge.py`:
  `509fa9d7bb323034bbf77b26792f35e1cc2ff7c7`;
- `nl1c4/expanding_memory_source_trajectory.py`:
  `7a9ffab9fa903ca61e88627052e2aa589b4bf459`.

## Frozen local science inputs

The execution must consume the already frozen local artifacts without regenerating them:

- Repair24 JSON SHA-256:
  `71f463524b47f72d2c5082667fe99141d2286ebc2938c4eed6b89a1583339f2a`;
- Repair22 JSON SHA-256:
  `7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374`;
- Repair22 NPZ SHA-256:
  `3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16`;
- Repair13 JSON SHA-256:
  `ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7`;
- Repair13 NPZ SHA-256:
  `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`;
- GE15 certified JSON SHA-256:
  `5975774bf7af0f3af9acf16c8de2dbac0ca032894dc5c6879346a3e11efe84c1`;
- frozen v0.77 trace SHA-256:
  `98c8468e8ccdf902cad8d6e65f3852e863c6fd19df62ece61353ab725ac5a43e`;
- frozen v0.77 trace bytes:
  `2657188`.

The GE15 JSON remains the binding source for the exact R1 dense-trace hash.

## Execution rule

The first valid Repair25 science audit must use this exact locked implementation and the frozen local inputs above.

No q20 rerun is permitted in Repair25.

No post-result rescaling is permitted.

No candidate normalization may be adopted from Repair25 alone.

The next step after the audit is determined only by the frozen routing result.
