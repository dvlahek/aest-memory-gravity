# GE03 Repair02 — predata retained-artifact directory resolution

## Status

Predata / pre-implementation repair preregistration.

Immediate parent outcome:

GE03 Repair01 execution reached the locked workflow science step but terminated before any GE03 operator evaluation because the retained v0.77 artifact was downloaded into an additional artifact-name subdirectory.

Representative failed run:

`35471582050`.

The failure was:

`FileNotFoundError: frozen_v077/v076_v077_base_trace.dat`.

The downloaded file exists under a nested directory created by `actions/download-artifact@v4`.

No GE03 science JSON was produced.

## Failure class

Implementation / runner path-resolution failure before science.

This is not a GE03 scientific PASS/FAIL.

The original GE03 science lock remains unchanged.

## Licensed repair

Exactly one new helper may be added outside the locked GE03 science implementation.

The helper must:

1. search below the workflow download root for exactly one file named
   `v076_v077_base_trace.dat`;
2. take its parent directory as the retained-artifact science directory;
3. verify that the same directory contains all eight required tangent traces for
   `lambda={10,5,2.5,1.25}`;
4. print only the resolved directory path on success;
5. fail if the base trace is missing, ambiguous, or any required trace is absent.

The locked GE03 Python implementation receives that directory through its already frozen
`--artifact-dir` argument.

## Prohibited changes

Do not change:

- `ge03/weakly_nonlinear_y_memory_cross_source.py`;
- the retained artifact ID or digest;
- lambda values;
- beta values;
- modes or phases;
- redshift window;
- spatial resolutions;
- dealiasing;
- finite-difference steps;
- numerical gates;
- classification rule;
- claim boundary.

## Execution rule

After preregistration:

1. add the deterministic path-resolution helper;
2. freeze its blob in a Repair02 implementation lock;
3. only then modify the workflow runner to call the helper;
4. the first run after that runner change is eligible to reach the unchanged GE03 science calculation.

If the helper cannot deterministically identify one complete retained-artifact directory, freeze another implementation failure.

No science threshold or operator repair is licensed by Repair02.
