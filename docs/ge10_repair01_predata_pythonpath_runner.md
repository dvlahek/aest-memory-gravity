# GE10 Repair01 predata — repository-root Python import path

## Status

Runner-only repair preregistration after

`GE10_PRE_SCIENCE_IMPORT_IMPLEMENTATION_FAIL`.

No GE10 diagnostic result exists yet.

## Frozen cause

The locked GE10 script imports the frozen GE09 driver as a repository module.

Direct path execution did not include repository root in Python's import path.

## Licensed runner change

Run the unchanged frozen GE10 script with

`PYTHONPATH="$PWD"`.

No Python source file may change.

## Frozen science/diagnostic content

Unchanged:

- GE09 parent artifact ID and digest;
- GE09 historical FAIL;
- stride ladder `{4,2,1}`;
- historical primary maximum;
- fitted-order floor;
- PCHIP/linear descriptive comparisons;
- all diagnostic gates;
- terminal classifications and claim boundary.

## Execution rule

After a runner-only implementation lock, update only the GE10 workflow command to provide repository-root PYTHONPATH.

The first run passing that lock is the first science-eligible GE10 diagnostic execution.
