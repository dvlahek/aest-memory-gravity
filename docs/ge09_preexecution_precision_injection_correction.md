# GE09 pre-execution correction — explicit p3 precision injection

## Status

No GE09 execution has occurred under the first implementation lock.

During the final runner audit, the implementation was found to rely on
`v063.class_params()`, which does not explicitly include the two p3
perturbation precision values already frozen by the GE09 preregistration:

- `tol_perturb_integration = 5e-8`;
- `perturb_sampling_stepsize = 0.0025`.

The first GE09 lock is therefore **not executed**.

This is a pre-execution implementation/provenance correction, not a
result-informed repair.

## Licensed implementation change

In the GE09 Python driver, add exactly

`pars["tol_perturb_integration"] = 5e-8`

and

`pars["perturb_sampling_stepsize"] = 0.0025`

before `Class.set(pars)`.

No other code, model parameter, common-time grid, interpolation method,
decimation rule, threshold, Fourier representative or claim boundary may
change.

## Required revised lock

After this correction, create a new GE09 implementation lock with the corrected
driver blob.

The original GE09 implementation lock remains historical but unexecuted.
