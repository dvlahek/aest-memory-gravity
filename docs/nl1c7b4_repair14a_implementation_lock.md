# NL1C7B4 Repair14a — implementation lock

## Status

Locked after Repair14a implementation and before any Repair14a execution.

## Historical Repair14 attempt01

- freeze commit: `381bc30d6266b12c3590b9138c9f1a7bc07de9cc`
- freeze blob: `8e19263ac71597a006509d43b5b0606fab349e7e`
- JSON SHA-256:
  `ea4f1d28330b22d6d3d64f5f6f6d27b3646a889fbee9cffc37c4e789282f0966`
- terminal class:
  `NL1C7B4_REPAIR14_IMPLEMENTATION_FAIL`

Exact historical gate pattern:

`T,T,T,F,T,T,T,T` for R14 G1..G8.

## Repair14a preregistration

- commit: `f8eed7308018bc8f7e626128d9a375c6fc90b374`
- file: `docs/nl1c7b4_repair14a_predata_decoded_static_semantics_parser.md`
- blob: `870fc95eef7335049e4d0785c4acc8a14509864a`

## Repair14a implementation

- commit: `c73ebe709b41cfe8d8d346efb24a92f3eda25cad`
- file: `nl1c7b/initial_constraint_certification_repair14a.py`
- blob: `1bf9ea6b9ed813574a7ed20ce723228347e9f737`

Frozen Repair14 evaluator imported unchanged:

- file: `nl1c7b/initial_constraint_certification_repair14.py`
- blob: `c67aa9f8c64ba2dcb499216feb405a7a339b7b06`

## Sole implementation change

Repair14a monkeypatches only the Repair14 `static_semantics()` function during the inherited evaluator execution.

The corrected parser:

- parses `v019/apply_patch_v019.py` with `ast.parse`;
- finds exactly one assignment to `new_stress`;
- obtains its literal string value via `ast.literal_eval`;
- scans the decoded C lines, not physical Python source lines;
- requires the exact active AeST density line;
- requires no decoded `ppw->delta_rho +=` C line to contain `E_aest` or `chi_aest`.

No Repair14 physics or numerical function is copied or modified.

## Inherited frozen science

The following remain exactly inherited from the frozen Repair14 evaluator:

- symbolic E/X gauge identities;
- exact B3 first variations;
- density-Q identity;
- Repair08 state construction;
- source matrices;
- diagnostic `Delta deltaQ`;
- scales/grids/Y/beta sets;
- lambda ladder;
- radial subset;
- `1e-12` cancellation limit;
- `[1.8,2.2]` H/M slope interval;
- eta=0;
- claim boundary.

An exact science-payload equality check against historical attempt01 is reported diagnostically but is not a new gate.

## Terminal classes

PASS:

`NL1C7B4_REPAIR14A_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED`

FAIL:

`NL1C7B4_REPAIR14A_IMPLEMENTATION_FAIL`

Historical Repair14 attempt01 and historical B4 remain unchanged.
