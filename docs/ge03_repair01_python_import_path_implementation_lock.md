# GE03 Repair01 — Python import-path implementation lock

## Status

Repair01 implementation locked before repaired GE03 execution.

Parent implementation-fail freeze:

`docs/ge03_initial_implementation_fail_result_freeze.md`

Parent freeze commit:

`1d04c93bf8f0c93455038499a5fcd55c7714a968`.

## Repair preregistration

Commit:

`20401683cca5e30f910b58e6844e654ba041be45`.

File:

`docs/ge03_repair01_predata_python_import_path.md`.

Frozen blob:

`ac255ae3f2cb932fd55f697df9e8054d57f1e1e1`.

## Repaired implementation

Commit:

`765840b1eb6ab84e158e22afd08e1c49b396a9c8`.

File:

`ge03/weakly_nonlinear_y_memory_cross_source.py`.

Frozen blob:

`9f8836668d83c6874ca58fd8dc2c7f2de187c1d7`.

## Exact repair

The only implementation change from the original locked GE03 science code is:

- import `sys`;
- compute the repository root as
  `Path(__file__).resolve().parents[1]`;
- insert that path into `sys.path` before importing the existing `nl1c4` module.

No GE03 equation, input, grid, lambda, beta0, finite-difference step, numerical gate or claim boundary changed.

## Science lock inherited unchanged

The original GE03 science lock remains authoritative for:

- exact retained v0.77 artifact;
- `lambda={10,5,2.5,1.25}`;
- `beta0={1,0.5,0.1}`;
- six signal-band modes and frozen phases;
- native `0.2<=z<=1.5` window;
- `Nx={256,512}`;
- 2/3 dealiasing;
- finite-difference direction steps `1e-4` and `3e-5`;
- all GE03 gates.

## Execution rule

The repaired run is the first run eligible to produce a GE03 science classification.

If the process reaches the locked science evaluation, classify it only by the original GE03 PASS/FAIL rule.

No further repair is licensed without freezing the repaired outcome first.
