# GE13 initial execution — dynamic-range implementation-fail freeze

## Status

First locked GE13 execution did not reach a science classification.

Workflow run:

`35501444901`.

Execution HEAD:

`1b98a1804632c40f17a4d500947f3106ed50c1ec`.

Artifact:

- ID: `10602237890`;
- digest:
  `sha256:2f3b15b71528ab517e62114183ce0a5520b403ce937e43673a223213a4b52d69`.

Classification:

`GE13_PRE_SCIENCE_DYNAMIC_RANGE_IMPLEMENTATION_FAIL`.

This is not a GE13 physical or diagnostic FAIL.

## Successful pre-science gates

The run passed:

- lock audit;
- both frozen parent artifact metadata checks;
- both parent artifact downloads;
- preregistration and implementation audit.

It then entered the frozen GE13 diagnostic code.

## Failure

The code constructed the pointwise alpha ratio only where

`|alpha_R1| > max(max|alpha_R1| * 1e-15, 1e-300)`.

Because alpha spans a very large dynamic range between the earliest accepted
radiation-era state and the late-time state, the global late-time amplitude
made this floor too large for some perfectly finite early-time values.

For the third frozen k mode the first equal-ln(a) bin then contained no points
marked valid and the code raised

`RuntimeError: k=0.053865971126789286: empty valid history bin 0`.

No GE13 JSON/NPZ science result was written.

## Diagnosis

The preregistered observable is the ratio

`alpha_R2/alpha_R1`

on the frozen common history.

The implementation error is not a zero crossing or a nonfinite alpha value.
It is the use of a **global amplitude-relative validity floor** for a field with
many orders of magnitude of physical time evolution.

The early alpha values are finite and nonzero in the retained traces.

## Licensed Repair01

A single implementation-only repair is licensed.

It may change only the denominator-validity rule from the global relative floor
to an exact nonzero/finite denominator test:

`valid = isfinite(alpha_R1) & isfinite(alpha_R2) & (abs(alpha_R1) > 1e-300)`.

The preregistered ratio, onset thresholds, 4096-point history grid, 16 bins,
late-window scale fits, parent artifacts, IC audit and all diagnostic gates
remain unchanged.

No new CLASS run, precision level, k mode, threshold or physical interpretation
is licensed.

## Project boundary

Historical GE11 and GE12 classifications remain unchanged.

This failure does not license R3, Z20, IC modification or a physical-instability claim.
