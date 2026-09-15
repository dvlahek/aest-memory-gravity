# Stable AeST DESI DR1 R9b2 direct-velocity launcher repair02

## Status

Pre-result technical repair. No R9b2 science model evaluation occurred before this repair: the repair01 wrapper terminated with shell exit code 127 before invoking the Python science driver because the host exposes `python3` but not a generic `python` executable.

## Frozen history

This repair does not alter or reinterpret any prior result. In particular:

- historical R9b remains `STABLE_AEST_DESI_DR1_R9B_CENTRAL_DERIVATIVE_FAIL`;
- the R9b2 velocity-adapter validation remains `STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_VALIDATED`;
- the R9b2 science preregistration, eta/tau grid, direct-velocity ShapeFit mapping, nuisance model, G4/G5/G6 thresholds, physical eta interval, and claim discipline are unchanged;
- repair01 remains limited to making the legacy `effective_f_sigma8/sigma8` quantity non-gating.

## Failure mode

`run_local_stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection_repair01.sh` invoked the small source-patching helper and `py_compile` through the literal command `python`. On the local WSL environment this command is absent, producing `python: command not found` and `EXIT=127` before the base science runner was reached.

The base R9b2 science runner already resolves the interpreter safely with `command -v python3 || command -v python` and activates the existing `.local/fullj_weyl_bridge_venv` before scientific execution.

## Repair

The repair01 wrapper is changed only to resolve a patch-time Python interpreter as:

1. `.local/fullj_weyl_bridge_venv/bin/python` if it already exists and is executable;
2. otherwise `python3`;
3. otherwise `python`;
4. otherwise fail before any science execution.

The resolved interpreter is used only for the deterministic repair01 text patch and its `py_compile` check. The wrapper then launches the unchanged base R9b2 science runner, which performs its own pinned-environment setup exactly as preregistered.

## Scientific invariance

No theory formula, transfer-function mapping, DESI datum, covariance, fiducial, nuisance column, derivative step, threshold, eta/tau value, likelihood expression, or classification rule is changed by repair02.
