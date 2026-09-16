# NL1C7A Repair01 dense-time implementation lock

Status: **LOCKED BEFORE OFFICIAL REPAIR01 EXECUTION**

Parent preregistration commit:

`d5ad768ff91abd789a1ff24fa7b19dfff8905489`

Historical A6 failure freeze:

`ccf2ac18dd3187f67bafcba4eeeb2b1c0dc524ae`

Frozen Repair01 implementation blobs:

- `nl1c7a/trace_dense_time_repair01.py`: `59afc0ca82217110e8a6e6b2d1d397a62e0452a2`
- `nl1c7a/evaluate_dense_time_repair01.py`: `aa84b4892586a59455ec93b6dfdc0057adc20d38`

Frozen reused science implementations:

- `nl1c7a/a5_denominator_audit.py`: `47b486ca2defbd1db029df003b37909a9d4d170d`
- `nl1c7a/a6_a10_spherical_reconstruction.py`: `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`
- `nl1c7a/apply_trace_extension.py`: `21147e873e6cdee8b55260189eafb8c0e612f02b`

Repair01 changes only `perturbations_sampling_stepsize` from the pinned CLASS default `0.1` to runtime value `0.025`. It does not override `perturbations_integration_stepsize` or `tol_perturbations_integration`.

The exact 128-mode k grid, batch size 24, eta=0 physics, scale ladder, interpolation methods and all A5-A10 thresholds remain unchanged.

If the full Repair01 classification passes, the evaluator additionally stores the exact primary PCHIP spherical state arrays for all three scales in an NPZ artifact. This serialization does not enter any gate.
