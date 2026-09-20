# GE09 Repair01 native CLASS CLI precision execution — implementation lock

## Status

Repair01 is locked before its first execution.

Parent execution is frozen separately as:

`GE09_PRE_SCIENCE_IMPLEMENTATION_FAIL`.

No GE09 science gate was evaluated in that parent run.

## Repair01 preregistration

Commit:

`d5b849c8d8d6dc657815740871bcd977d8cc6316`.

File:

`docs/ge09_repair01_predata_native_cli_precision_execution.md`.

Frozen blob:

`53076ce1e6b0a8446f0adedc6c9d73f75650898c`.

## Diagnostic trace patch

Unchanged from GE09:

`ge09/apply_dense_accepted_step_trace_patch.py`.

Frozen blob:

`23b0cd22ebab499aee0ce03e6b3b678fe727ef55`.

## Repair01 driver

Final pre-lock implementation commit:

`4bccfea123e8c1b227db05269130c5ce65fe6303`.

File:

`ge09/repair01_dense_accepted_step_local_jet_bridge.py`.

Frozen blob:

`27627e9163894174708dec82dfa4951e7f8ecb42`.

## Execution surface

Use the official CLASS executable, not `classy.Class.set()`.

The driver writes a deterministic GE09 ini file and executes

`class ge09_repair01_cli.ini v019p/pre/p3.pre`.

Therefore the already frozen p3 values enter through the native CLASS precision
parser:

- `tol_perturb_integration = 5e-8`;
- `perturb_sampling_stepsize = 0.0025`.

## Independent CLASS-state control

The same native CLI execution generates official scalar perturbation tables

`ge09_cli_perturbations_k0_s.dat ... ge09_cli_perturbations_k5_s.dat`.

The GE09 dense diagnostic trace is compared against their

- tau;
- a;
- phi;
- psi;
- delta_cdm;
- theta_cdm

columns.

The frozen abs-or-rel limit remains `1e-12`.

## Science representation unchanged

All parent GE09 science choices remain unchanged:

- successful NDF15 step endpoints with fresh physical RHS;
- six frozen k modes;
- `0.2<=z<=1.5`;
- 64 common uniform ln(a) nodes;
- derivative-aware CubicHermiteSpline;
- algebraic/background PCHIP;
- deterministic every-second endpoint control;
- same 15-entry GE06 local jet;
- analytic Fourier spatial derivatives;
- source-grid validation <= `1e-4`;
- primary/control global relative L2 <= `5e-4`;
- pointwise abs-or-rel <= `2e-3`;
- scalar pt identity <= `1e-12`.

## Classification

A completed science execution is classified only as

- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_PASS`;
- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.

## Project boundary

Even PASS leaves the separately frozen GE08 Repair01 matter incompleteness
active and does not by itself license Z20.
