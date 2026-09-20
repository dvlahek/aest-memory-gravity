# GE09 Repair01a standard-library import repair — implementation lock

## Status

Implementation locked before the first science-eligible Repair01a execution.

Historical parent classifications remain unchanged:

- `GE09_PRE_SCIENCE_IMPLEMENTATION_FAIL`;
- `GE09_REPAIR01_PREDATA_RUNNER_FAIL`;
- `GE09_REPAIR01_PRE_SCIENCE_IMPORT_IMPLEMENTATION_FAIL`.

No GE09 local-jet science classification exists yet.

## Repair01a preregistration

Commit:

`35e1e7f59bcda1170d731fbb54f5aa28e95a6b08`.

File:

`docs/ge09_repair01a_predata_standard_library_import_repair.md`.

Frozen blob:

`3ddff2e0044f126b0bda9d6ccdd38daa0e0266fa`.

## Repair01a implementation

Commit:

`4cedb7c755f22272886d4d0bb43ed26a750c806c`.

File:

`ge09/repair01_dense_accepted_step_local_jet_bridge.py`.

Frozen blob:

`06c012763add5f28fa72bbcc77296f101e0a816f`.

Relative to the previously locked Repair01 driver, the only source change is:

`import re`

and

`import subprocess`.

No other source line changed.

## Frozen parent science contract

Unchanged:

- pinned CLASS commit
  `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- official native CLASS CLI execution;
- precision file `v019p/pre/p3.pre`;
- `tol_perturb_integration=5e-8`;
- `perturb_sampling_stepsize=0.0025`;
- six frozen k modes;
- successful NDF15 step-endpoint trace with fresh physical RHS;
- official CLASS scalar perturbation tables as independent-state control;
- 64 common uniform ln(a) nodes;
- derivative-aware CubicHermiteSpline;
- algebraic/background PCHIP;
- every-second accepted-step control;
- complete 15-entry GE06 local jet;
- analytic Fourier spatial derivatives;
- source-grid state validation <= `1e-4`;
- primary/control global relative L2 <= `5e-4`;
- pointwise abs-or-rel <= `2e-3`;
- scalar pt identity <= `1e-12`.

## Workflow auto-trigger note

The implementation commit triggered the pre-existing GE09 workflows before this Repair01a lock existed.

Those runs are not science-eligible because their lock audits still reference the older Repair01 driver blob.

They do not constitute GE09 science results.

## Terminal science classifications

The first execution using this locked Repair01a implementation and an updated lock-aware runner may classify only as:

- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_PASS`;
- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.

## Project boundary

Even a GE09 PASS certifies only the complete first-order local jet.

The frozen GE08 Repair01 standard-matter incompleteness remains active.

GE09 alone does not license `Z20`, `Z21`, finite eta, collapse or observational claims.
