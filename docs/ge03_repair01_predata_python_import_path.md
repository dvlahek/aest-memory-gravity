# GE03 Repair01 — predata Python import-path repair

## Status

Predata / pre-implementation repair preregistration.

Parent frozen result:

`GE03 initial execution — IMPLEMENTATION_FAIL_BEFORE_SCIENCE`.

Parent result-freeze commit:

`1d04c93bf8f0c93455038499a5fcd55c7714a968`.

Parent workflow run:

`35471469893`.

## Failure being repaired

The locked GE03 Python process terminated before science at

`import nl1c4.expanding_memory_source_trajectory as c4`

with

`ModuleNotFoundError: No module named 'nl1c4'`.

No scientific operator evaluation occurred.

## Licensed code change

Exactly one implementation change is allowed.

Before importing `nl1c4`:

1. import `sys`;
2. define
   `ROOT=Path(__file__).resolve().parents[1]`;
3. insert
   `str(ROOT)`
   at the front of `sys.path`.

No other source line may be changed.

## Frozen science content

Unchanged:

- retained v0.77 artifact;
- lambda set `{10,5,2.5,1.25}`;
- `beta0={1,0.5,0.1}`;
- six signal-band modes;
- frozen phases;
- native redshift window;
- `Nx={256,512}`;
- 2/3 dealiasing;
- finite-difference steps `1e-4` and `3e-5`;
- all numerical gates;
- exact NL1B2 `DY2` identity;
- claim boundary.

## Classification boundary

If the repaired process reaches the locked GE03 science calculation, the original GE03 PASS/FAIL rule applies unchanged.

If the repair does not restore execution, classify the repaired run as another implementation failure.

No second repair sequence is licensed without freezing that outcome first.
