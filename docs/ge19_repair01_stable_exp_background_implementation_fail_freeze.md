# GE19 Repair01 stable-Exp execution — implementation-failure freeze

## Status

The first locked GE19 Repair01 local execution terminates before any Stage-A science classification with

`GE19_REPAIR01_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`.

This classification is immutable.

No reduced-H1 state and no Z20 state were constructed.

## Execution provenance

Locked Repair01 runner commit:

`0ddf3164f59ea616f38a638e38155519f4d9f254`.

The local runner reports:

- `GE19_REPAIR01_LOCK_PASS`;
- `GE19_REPAIR01_LOCAL_INPUTS_PRESENT`.

Uploaded files:

- full log:
  - bytes: `131961`;
  - SHA-256:
    `a42b88e4f2f3dc803211b955f1a90ccbbd5adc5b64d31a57a8d995b171fd0ca3`;
- runner log:
  - bytes: `132189`;
  - SHA-256:
    `73183eefe0e22e63fc78e3c676a7c4650cb1dcf6aa1edba6b8e2127224cf9b68`.

## Failure

The terminal exception is

`SyntaxError('cannot assign to literal', ...)`

raised by SymPy `lambdify` while building the stable GE06 coefficient functions.

The generated Python signature contains a large numerical array as an argument, proving that at least one entry in the constructed `direction_args` tuple was no longer a SymPy symbol.

This happens before:

- stable benign GE06 equivalence evaluation;
- physical stable-Exp background evaluation;
- reduced-H1 Stage A;
- H3 source construction;
- Z20 construction.

Therefore this execution contains no H1/H3 science result.

## Root cause

The frozen GE06 module creates the correct symbolic tuple

`direction_args`

when the module is defined.

Later, the module-level audit code executes

`T,X,dt,dx,a,adot,qb,direction=deterministic_grid()`.

This overwrites at least the global name `adot`, which originally denoted the SymPy background symbol, with a numerical array.

GE19 Repair01 reconstructed its stable lambdify signature from individual module attributes such as

`mod6.aa`, `mod6.adot`, ...

instead of using the frozen `mod6.direction_args` tuple.

Thus the new signature accidentally included a numerical array.

## Licensed Repair02

Repair02 may change only the stable re-lambdification symbol capture.

It must use the already frozen GE06 `direction_args` tuple, whose elements were captured when they were still SymPy symbols.

Construct the stable signature as

`(direction_args[0], direction_args[1], Zb, *direction_args[3:])`.

The symbolic expansion must likewise use symbols recovered from frozen symbolic structures, not mutable module-global audit names.

All stable-Exp reconstruction, native-I0 rules, GE06 benign-equivalence gates, Stage-A gates, Stage-B gates, modes, phases, beta0 values, C values, grid controls, gauge and boundary conventions remain unchanged.

## Historical integrity

Neither the original GE19 implementation failure nor GE19 Repair01 is relabelled.

## Claim boundary

Repair01 produced no valid reduced-H1 or Z20 state and carries no physical conclusion.
