# GE09 Repair01b predata — native CLASS root canonicalization

## Status

Predata implementation-only repair after the frozen classification

`GE09_REPAIR01A_PRE_SCIENCE_OUTPUT_ROOT_IMPLEMENTATION_FAIL`.

No GE09 local-jet science result exists yet.

## Frozen cause

The locked Repair01a driver supplies the native CLASS root

`.../results/ge09_cli_`.

Pinned CLASS `input_set_root()` appends its own underscore to an explicit root, so the runtime root becomes

`.../results/ge09_cli__`.

The driver then looks for the canonical single-underscore files

`.../results/ge09_cli_perturbations_k*_s.dat`

and fails before science evaluation.

## Licensed implementation change

Change exactly one source line in

`ge09/repair01_dense_accepted_step_local_jet_bridge.py`:

from

`prefix=ROOT/"results"/"ge09_cli_"`

to

`prefix=ROOT/"results"/"ge09_cli"`.

No other source line may change.

## Frozen native CLASS behavior

The repair relies on pinned CLASS commit

`e85808324f51fc694d12e3ed7439552a3c3f9540`

where:

1. reading `k_output_values` sets
   `ppt->store_perturbations = TRUE`
   and
   `pop->write_perturbations = TRUE`;
2. `input_set_root()` appends one underscore to the supplied explicit root;
3. `output_perturbations()` writes
   `<root>perturbations_kN_s.dat`.

Thus a supplied root ending in `ge09_cli` yields exactly

`ge09_cli_perturbations_kN_s.dat`.

No extra `write perturbations` parameter is introduced.

## Unchanged science contract

Keep unchanged:

- Repair01a standard-library imports;
- pinned CLASS commit;
- native CLASS CLI execution;
- p3 precision file and values;
- six k modes;
- successful-step trace hook;
- official CLASS perturbation-table independent-state control;
- 64-node ln(a) representation;
- CubicHermiteSpline/PCHIP split;
- every-second accepted-step control;
- complete 15-entry GE06 local jet;
- all science thresholds and terminal classifications.

## Required lock and execution

After the one-line root change:

1. create a new implementation lock;
2. update only the Repair01 runner provenance to the new driver and lock;
3. execute that locked driver.

The science classification remains exclusively:

- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_PASS`;
- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.

Even PASS does not close the separately frozen GE08 Repair01 standard-matter incompleteness.
