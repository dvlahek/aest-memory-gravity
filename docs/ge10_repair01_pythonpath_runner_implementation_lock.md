# GE10 Repair01 repository-root Python path — implementation lock

## Status

Runner-only repair locked before repaired execution.

Historical parent remains:

`GE10_PRE_SCIENCE_IMPORT_IMPLEMENTATION_FAIL`.

## Repair preregistration

Commit:

`eaaef4fbd924e7f11190d545e183552a5e5f1c54`.

File:

`docs/ge10_repair01_predata_pythonpath_runner.md`.

Frozen blob:

`3a7b6bc526483ce34214f8d81a8ae1e6d04940cc`.

## Frozen GE10 source

`ge10/ge09_source_interpolation_localization.py`

blob:

`6762e53b80c21dbb907abc6f01080dd38cfa634c`.

No Python source change is permitted.

## Allowed runner change

Prefix the existing GE10 Python execution with

`PYTHONPATH="$PWD"`.

No other workflow or diagnostic setting may change.

## Terminal diagnostic classes

- `GE10_GE09_SOURCE_INTERPOLATION_LIMIT_CONFIRMED`;
- `GE10_GE09_SOURCE_INTERPOLATION_DIAGNOSTIC_FAIL`.

GE09 remains frozen FAIL under either outcome.
