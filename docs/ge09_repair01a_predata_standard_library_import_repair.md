# GE09 Repair01a predata — standard-library import repair

## Status

Predata implementation-only repair after the frozen classification

`GE09_REPAIR01_PRE_SCIENCE_IMPORT_IMPLEMENTATION_FAIL`.

No GE09 local-jet science result exists yet.

## Frozen cause

The already locked Repair01 native-CLI driver uses

- `re.search/re.findall`;
- `subprocess.run`;

but omitted the corresponding Python standard-library imports.

## Licensed implementation change

Add exactly these two lines to
`ge09/repair01_dense_accepted_step_local_jet_bridge.py`:

`import re`

`import subprocess`

No other source line may change.

## Unchanged science contract

Keep unchanged:

- pinned CLASS commit;
- p3 precision file and values;
- six k modes;
- GE09 successful-step trace hook;
- official CLASS CLI perturbation-table control;
- 64-node ln(a) representation;
- CubicHermiteSpline/PCHIP split;
- every-second accepted-step control;
- complete 15-entry GE06 local jet;
- all science thresholds and terminal classifications.

## Required lock and execution

After the two import lines are added, create a new implementation lock with the corrected driver blob.

Only that locked implementation may be executed.

The science classification remains exclusively:

- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_PASS`;
- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.
