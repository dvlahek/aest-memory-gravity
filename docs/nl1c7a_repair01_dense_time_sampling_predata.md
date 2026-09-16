# NL1C7A Repair01 pre-data — dense accepted source-time sampling

Status: **PRE-DATA / LOCKED BEFORE REPAIR01 TRACE EXECUTION**

## Parent result

Historical C7A A6-A10 result remains frozen and is not replaced:

- classification: `NL1C7A_TIME_INTERPOLATION_CONTROL_FAIL`
- official run: `35106735707`
- workflow head: `8b02243fc0b1ea58f00466868d58170c73dbc4e4`
- artifact: `10450343358`
- artifact SHA256: `99b795389566a21b0438977af55bae21f92b428d52ad50ba2c9855bafda28fb5`
- post-data freeze commit: `ccf2ac18dd3187f67bafcba4eeeb2b1c0dc524ae`

The failure was localized to A6 for the aether rapidity `u`: PCHIP-ln(a) versus linear-ln(a) spherical reconstruction differed by about `0.03627` on all three frozen scales, above the frozen `0.02` limit. A7, A8, A9 and A10 passed, and `udot` remained below the A6 limit.

## Purpose

Repair01 tests only if the A6 failure is caused by insufficient accepted source-time sampling around the already frozen initial epoch `a_i=0.02`.

No science threshold is changed. No preferred interpolator is selected after the historical result. No physical or perturbation equation is changed.

## Single permitted numerical-interface change

Pinned CLASS commit remains

`e85808324f51fc694d12e3ed7439552a3c3f9540`.

The pinned CLASS precision parameter `perturbations_sampling_stepsize` has default value `0.1`. Repair01 sets only

`perturbations_sampling_stepsize = 0.025`.

This is a 4x refinement of source-function sampling. It is not a change to `perturbations_integration_stepsize`, perturbation tolerances, AeST equations, background equations, initial conditions, physical parameters, k grid, memory coupling, or spherical reconstruction rules.

## Frozen state retained exactly

- `eta=0`.
- Exp AeST model and all frozen parameters unchanged.
- `a_i=0.02`.
- `R_sigma=[5,10,20] h^-1 Mpc` co-primary.
- exact requested k grid: 128 logarithmic modes over `[0.0015,1.2] h Mpc^-1`.
- diagnostic batching only: batch size 24, six CLASS instances.
- no k interpolation in the trace-generation stage and no nearest-neighbour substitution.
- output-only trace fields unchanged.
- PCHIP-ln(a) remains the primary time interpolation and linear-ln(a) remains the independent control.
- PCHIP-ln(k) remains primary and linear-ln(k) remains the independent k control.
- quadratures remain 256/512 nodes.
- A5 denominator floor remains `1e-12`.
- A6/A7 relative limit remains `0.02`.
- A8 limit remains `1e-4`.
- A9 limit remains `1e-6`.
- A10 free-mode prohibition unchanged.

## Repair gates

### R1 — provenance

The historical A6 failure run/head/artifact digest and its post-data freeze commit must match exactly. The original C7A preregistration remains the governing science preregistration.

### R2 — source-sampling-only change

The implementation must verify from the pinned CLASS source that the default `perturbations_sampling_stepsize` is `0.1`, then set it to exactly `0.025` at runtime. `perturbations_integration_stepsize` and perturbation tolerances must not be overridden by Repair01. The previously certified output-only trace source-boundary audit must remain valid.

### R3 — denser exact native trace

All original 128 requested k modes must again be present with relative k mismatch `<=1e-12` and share a common native time grid. No interpolation or nearest-neighbour substitution is allowed in trace generation.

The Repair01 trace must contain strictly more than the historical 46 native times and must provide at least 8 accepted native times below and 8 above `a_i=0.02` within `0.015 <= a <= 0.03`. Failure to obtain this density is a repair-interface failure before A6 interpretation.

### R4 — A5 denominator recheck

A5 is rerun on the Repair01 trace with the original thresholds and scale ladder. It must remain `NL1C7A_A5_FINITE_GROWING_MODE_DENOMINATOR_PASS` with no clipping or node deletion.

### R5 — unchanged A6 time-interpolation control

The complete spherical initial state is reconstructed exactly as in the frozen C7A implementation. Every active field must satisfy the original PCHIP-ln(a) versus linear-ln(a) L2 relative threshold `<=0.02` on all three scales. No field-specific exception may be introduced for `u`.

### R6 — unchanged A7-A10 controls

A7 k interpolation, A8 target-profile reconstruction, A9 bridge identities and A10 no-free-mode injection must all pass under their original thresholds.

## Classification

Full Repair01 PASS:

`NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED`

Allowed non-PASS classifications include:

- `NL1C7A_REPAIR01_PROVENANCE_FAIL`
- `NL1C7A_REPAIR01_SOURCE_SAMPLING_BOUNDARY_FAIL`
- `NL1C7A_REPAIR01_NATIVE_DENSITY_FAIL`
- `NL1C7A_REPAIR01_TRANSFER_ZERO_FAIL`
- `NL1C7A_REPAIR01_TIME_INTERPOLATION_CONTROL_FAIL`
- the corresponding unchanged A7/A8/A9/A10 failures.

A Repair01 PASS licenses construction of the unique eta=0 C7 spherical initial state only. It does not certify nonlinear spherical evolution, finite eta, turnaround, collapse, splashback or an observable.
