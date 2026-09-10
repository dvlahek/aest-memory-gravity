# NL1C6D2C6A result: AeST state export unavailable

## Classification

`NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_INCOMPLETE`

This is an instrumentation/data-exposure limitation, not a numerical or physical failure of the D2C6A equations.

## Run

GitHub Actions run `34442308738` on branch `v053-exp-normalization-corrected` reached the D2C6A executable after the isolated corrected CLASS build passed.

The run stopped before any physical-time trajectory step because `Class.get_perturbations()` did not expose the internal AeST perturbation states required by the preregistered linear-control and initial-state construction:

- `alpha_aest`
- `E_aest`

The returned dense perturbation histories contained the standard `a`, `phi`, `psi`, density and velocity fields, including `delta_cdm` and `theta_cdm`, but not the two AeST state variables.

No I1--I8 physics gate was evaluated. No nonlinear trajectory output was produced. Therefore this run cannot be classified as a D2C6A physics FAIL.

## Allowed remediation

Before any further D2C6A trajectory output, add instrumentation-only export of the already-existing AeST perturbation-vector entries into CLASS scalar perturbation output for `k_output_values`:

- title `alpha_aest` storing `y[index_pt_alpha_aest]`,
- title `E_aest` storing `y[index_pt_E_aest]`.

The export must be conditional on `aest_enabled` and must not modify:

- background equations,
- perturbation equations,
- initial conditions,
- cosmological or AeST parameters,
- RK4 scheme,
- D2C6A spatial/time resolution,
- any preregistered I1--I8 gate.

After instrumentation is added, rerun the unchanged D2C6A preregistered campaign. Historical INCOMPLETE remains INCOMPLETE.
