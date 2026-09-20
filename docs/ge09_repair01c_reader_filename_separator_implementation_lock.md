# GE09 Repair01c canonical perturbation filename separator — implementation lock

## Status

Implementation locked before the first Repair01c execution.

No GE09 local-jet science classification exists yet.

## Parent frozen implementation failures

Historical outcomes remain unchanged:

- GE09_PRE_SCIENCE_IMPLEMENTATION_FAIL
- GE09_REPAIR01_PREDATA_RUNNER_FAIL
- GE09_REPAIR01_PRE_SCIENCE_IMPORT_IMPLEMENTATION_FAIL
- GE09_REPAIR01A_PRE_SCIENCE_OUTPUT_ROOT_IMPLEMENTATION_FAIL
- GE09_REPAIR01B_PRE_SCIENCE_READER_PATH_IMPLEMENTATION_FAIL

## Repair01c preregistration

Commit:

`5e754fcab222ed73e18b43f797d0ac34ff7696e7`.

File:

`docs/ge09_repair01c_predata_reader_filename_separator.md`.

Frozen blob:

`9407b9cc5d53365af4a8c9ca59c17d4becf6c6bc`.

## Repair01c implementation

Commit:

`9571668d6707a9a7ea09bb1fd3480742b66a1227`.

File:

`ge09/repair01_dense_accepted_step_local_jet_bridge.py`.

Frozen blob:

`509fa9d7bb323034bbf77b26792f35e1cc2ff7c7`.

Relative to Repair01b exactly two filename-construction lines changed:

- stale-file cleanup;
- official CLASS perturbation-table reader.

Both now resolve

`ge09_cli_perturbations_kN_s.dat`.

No other source line changed.

## Frozen science contract

Unchanged:

- pinned CLASS commit;
- native CLASS CLI;
- p3 precision values;
- six k modes;
- dense successful-step trace with fresh physical RHS;
- official CLASS perturbation tables as independent-state control;
- 64 common ln(a) nodes;
- CubicHermiteSpline/PCHIP representation;
- every-second accepted-step control;
- complete 15-entry GE06 local jet;
- source-grid validation <= 1e-4;
- primary/control global relative L2 <= 5e-4;
- pointwise abs-or-rel <= 2e-3;
- scalar pt identity <= 1e-12.

## Terminal science classifications

The first lock-aware Repair01c execution may classify only as:

- GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_PASS
- GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL

## Project boundary

Even PASS certifies only the complete GE06 local first-order jet.

GE08 Repair01 standard-matter incompleteness remains active.

GE09 alone does not license Z20, Z21, finite eta, collapse or observational claims.
