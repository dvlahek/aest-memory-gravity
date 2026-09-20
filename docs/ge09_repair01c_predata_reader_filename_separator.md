# GE09 Repair01c predata — canonical perturbation filename separator

## Status

Predata implementation-only repair after the frozen classification

`GE09_REPAIR01B_PRE_SCIENCE_READER_PATH_IMPLEMENTATION_FAIL`.

No GE09 local-jet science result exists yet.

## Frozen cause

Repair01b correctly supplies the native CLASS root

`.../results/ge09_cli`.

Pinned CLASS writes the six official tables as

`ge09_cli_perturbations_kN_s.dat`.

The Python driver still constructs two paths without the canonical separator:

`str(prefix)+f"perturbations_k{i}_s.dat"`.

This yields the nonexistent

`ge09_cliperturbations_kN_s.dat`.

## Licensed implementation change

Change exactly two source occurrences in

`ge09/repair01_dense_accepted_step_local_jet_bridge.py`

from

`str(prefix)+f"perturbations_k{i}_s.dat"`

to

`str(prefix)+f"_perturbations_k{i}_s.dat"`.

The two occurrences are:

1. stale-file cleanup before the native CLASS execution;
2. perturbation-table reader after the native CLASS execution.

No other source line may change.

## Frozen evidence

Repair01b artifact ID:

`10599643436`.

All six official perturbation tables already exist with the canonical names

`ge09_cli_perturbations_k0_s.dat ... ge09_cli_perturbations_k5_s.dat`.

Therefore Repair01c changes only Python filename resolution.

## Unchanged science contract

Keep unchanged:

- Repair01a imports;
- Repair01b root canonicalization;
- pinned CLASS commit;
- native CLASS CLI execution;
- p3 precision values;
- six k modes;
- successful-step dense trace;
- source-state trace;
- official CLASS perturbation-table independent-state control;
- common ln(a) representation;
- Hermite/PCHIP split;
- decimated control;
- complete GE06 local jet;
- all thresholds and terminal science classifications.

## Required lock and execution

After the two filename changes:

1. create a new implementation lock;
2. update only Repair01 workflow provenance;
3. execute the locked driver.

The completed science classification remains exclusively:

- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_PASS`;
- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.

Even PASS leaves the GE08 Repair01 matter incompleteness active.
