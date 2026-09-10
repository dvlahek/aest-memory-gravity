# NL1C6D2C6A pre-result implementation clarification: exact endpoint background evaluation

Status: **LOCKED BEFORE ANY D2C6A TRAJECTORY STEP OR I1-I8 RESULT**.

## Observed implementation failure

After the preregistered AeST state-output instrumentation succeeded, D2C6A entered the physical integrator but stopped at the exact start time corresponding to `z=6` before the first RK4 step.

The failure was

`FloatingPointError: nonfinite/invalid background interpolation`.

This is an endpoint-domain mismatch in the implementation, not an evaluated D2C6A physics/numerical gate. The R1 background reconstruction retains native CLASS background samples satisfying `0 <= z <= 6`. The earliest retained native sample need not lie exactly at `z=6`. Building `PchipInterpolator(..., extrapolate=False)` from those samples can therefore leave the exact D2C6A start value `a=1/7` infinitesimally or finitely outside the interpolation support.

No physical trajectory step was taken and I1-I8 were not evaluated.

## Frozen correction

Do **not** clip `a`, extrapolate the R1 background spline, move the start redshift, change the time grid, or introduce a tolerance.

Instead evaluate the background quantities at the exact physical conformal time using identities already frozen in the D2C6A preregistration:

1. Obtain `a(tau)` from the corrected CLASS dense scalar history already used to define physical time.
2. Obtain the physical Hubble rate directly from the derivative of that same CLASS spline,

   `H = (da/dtau)/a^2`.

3. Use the already certified corrected Exp shift-charge calibration `I0` from the R1 background audit and reconstruct the charge pointwise from

   `K_Q a^3 = I0`.

   With the corrected Exp normalization,

   `x = K_Q/(2 K2 Z0)`, followed by the already audited positive-branch inverse and `exp_eval` routines to obtain `Q`, `K_Q`, `K_QQ`, and `Z`.

4. Compute

   `Qdot = -3 H K_Q/K_QQ`.

This is the same physical background prescribed in the original preregistration. It removes only an avoidable interpolation-domain dependency at the exact endpoint.

## What remains unchanged

The following remain exactly as preregistered:

- `z=6 -> 0.2` physical interval;
- corrected CLASS model and parameters;
- `sigma=0`, Simple, `beta0=1`;
- `Nx=128/256`, `Nstep=4096/8192`;
- RK4 and pseudospectral/dealiasing implementation;
- exact chain-rule initial derivative clarification;
- all I1-I8 thresholds and classifications;
- no memory, eta, refit, static solver, homotopy, pseudo-time, or branch continuation.

No D2C6A PASS/FAIL conclusion is licensed until the unchanged preregistered I1-I8 gates are actually evaluated.
