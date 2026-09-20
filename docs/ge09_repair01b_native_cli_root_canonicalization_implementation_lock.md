# GE09 Repair01b native CLASS root canonicalization — implementation lock

## Status

Implementation locked before the first Repair01b execution.

No GE09 local-jet science classification exists yet.

## Parent frozen implementation failures

The following historical outcomes remain unchanged:

- `GE09_PRE_SCIENCE_IMPLEMENTATION_FAIL`;
- `GE09_REPAIR01_PREDATA_RUNNER_FAIL`;
- `GE09_REPAIR01_PRE_SCIENCE_IMPORT_IMPLEMENTATION_FAIL`;
- `GE09_REPAIR01A_PRE_SCIENCE_OUTPUT_ROOT_IMPLEMENTATION_FAIL`.

## Repair01b preregistration

Commit:

`1424d9254b71b35eff68a9626d1165a437ed6593`.

File:

`docs/ge09_repair01b_predata_native_cli_root_canonicalization.md`.

Frozen blob:

`8ba32af0d1ac44193dfa63cbfc6c657592ee6269`.

## Repair01b implementation

Commit:

`d21f651b2d314db34c7375f60fa0fbc873839efa`.

File:

`ge09/repair01_dense_accepted_step_local_jet_bridge.py`.

Frozen blob:

`03e4d82e83f620155bba2ee9ff51dac017ea7912`.

The only source change relative to Repair01a is:

`prefix=ROOT/"results"/"ge09_cli_"`

to

`prefix=ROOT/"results"/"ge09_cli"`.

No other source line changed.

## Frozen pinned CLASS naming identity

Pinned CLASS commit:

`e85808324f51fc694d12e3ed7439552a3c3f9540`.

The runtime semantics are:

- `k_output_values` enables perturbation storage/writing;
- an explicit root receives exactly one trailing underscore in `input_set_root()`;
- scalar perturbation files are written as
  `<root>perturbations_kN_s.dat`.

Therefore the Repair01b supplied root `ge09_cli` must resolve to the expected canonical files

`ge09_cli_perturbations_kN_s.dat`.

No additional output parameter is introduced.

## Frozen science contract

Unchanged:

- native CLASS CLI;
- p3 precision values;
- six k modes;
- successful NDF15 step-endpoint trace with fresh physical RHS;
- official CLASS perturbation tables as independent-state control;
- 64 common uniform ln(a) nodes;
- derivative-aware CubicHermiteSpline;
- algebraic/background PCHIP;
- every-second accepted-step control;
- 15-entry GE06 local jet;
- source-grid validation <= `1e-4`;
- primary/control global relative L2 <= `5e-4`;
- pointwise abs-or-rel <= `2e-3`;
- scalar pt identity <= `1e-12`.

## Terminal science classifications

The first lock-aware Repair01b execution may classify only as:

- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_PASS`;
- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.

## Project boundary

Even PASS certifies only the complete GE06 first-order local jet.

The frozen GE08 Repair01 standard-matter incompleteness remains active.

GE09 alone does not license `Z20`, `Z21`, finite eta, collapse or observational claims.
