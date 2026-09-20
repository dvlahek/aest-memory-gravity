# GE07 Repair01 — runner log-directory implementation lock

## Status

Runner-only repair locked before repaired execution.

## Parent science implementation

GE07 science implementation is unchanged:

- file `ge07/pressureless_matter_directional_source_generator.py`;
- frozen blob `cde8da77a80799cef00fc7c09c3633310fc9e3d4`.

## Repair preregistration

Commit:

`0e73c1fb2c0d6bc9365130e47f3443e7199ef5ba`.

File:

`docs/ge07_repair01_predata_runner_log_directory.md`.

Frozen blob:

`26b57b27af8b63784259a4c69bdb5b151df99f46`.

## Allowed runner change

Before invoking the locked Python process through `tee`, create the log directory with

`mkdir -p results`.

No other runner or science setting may change.

## Reproduction requirement

The repaired run must:

- reach the same locked GE07 generator;
- classify as `GE07_PRESSURELESS_MATTER_DIRECTIONAL_SOURCE_GENERATOR_PASS`;
- retain all science gates true.

