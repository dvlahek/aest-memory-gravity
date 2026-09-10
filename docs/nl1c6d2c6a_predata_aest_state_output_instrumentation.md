# NL1C6D2C6A pre-data AeST state-output instrumentation

This declaration is locked before any D2C6A rerun using the new output columns.

## Purpose

Resolve the documented D2C6A INCOMPLETE caused solely by `Class.get_perturbations()` not exposing the already-evolved AeST perturbation states `alpha_aest` and `E_aest`.

## Frozen instrumentation change

Modify only the scalar perturbation-output table used for `k_output_values`:

1. When `aest_enabled == true`, append scalar output titles
   - `alpha_aest`
   - `E_aest`.
2. In the corresponding scalar output row, store the existing perturbation-vector values
   - `y[index_pt_alpha_aest]`
   - `y[index_pt_E_aest]`.

No interpolation, differentiation, reconstruction, rescaling, smoothing, or fitted parameter is permitted in this instrumentation layer.

## Non-changes

The following remain exactly frozen from the existing D2C6A preregistration:

- corrected Exp normalization and all AeST/cosmological parameters,
- action-derived D2C5 equations,
- CLASS perturbation RHS and background RHS,
- memory disabled and eta=0,
- six frozen k modes,
- physical interval z=6 to z=0.2,
- RK4,
- primary grid Nx=128, Nt=4096,
- time control Nt=8192,
- spatial control Nx=256,
- linear j=0 control,
- all I1--I8 thresholds and classifications.

## Instrumentation gate before trajectory interpretation

The rerun is allowed to enter D2C6A physics gates only if all six scalar histories returned by `get_perturbations()` contain finite arrays `alpha_aest` and `E_aest` with the same length and tau grid as the standard perturbation fields.

If the columns are absent, malformed, or nonfinite, classify the run INCOMPLETE. Do not reinterpret it as a physics failure.

No outcome-dependent change to D2C6A gates is permitted after observing the instrumented trajectory.
