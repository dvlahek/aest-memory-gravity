# C3 R5B sparse-k environment repair preregistration

## Status
Technical repair only. Historical R5/R5A runs remain immutable `C3_R5_REFERENCE_INCOMPLETE` diagnostics. No physics result from them is reclassified.

## Observed technical failure
The R5 sparse-k CLASS helper is present and passes its source audit, but the fresh signed-lambda subprocess does not set `AEST_TANGENT_ALLOW_K_MISS=1`. CLASS therefore exits with code 94 when it evaluates unrelated internal transfer-grid k values that are intentionally absent from the six-mode forcing table.

## Frozen repair
Only `nl1c6d2c6c_r5/build_zero_safe_reference.py::run_signed_case` may change. The subprocess environment will set `AEST_TANGENT_ALLOW_K_MISS=1` in addition to the existing `OMP_NUM_THREADS=1`.

No equations, bath data, tauH0, order, six target k modes, force values, interpolation, lambda, CLASS commit, zero-coupling construction, C3 metric, C3 threshold, or classification rule may change.

Unmatched internal transfer-grid k values receive zero external tangent forcing, exactly as already implemented and used in the R4 sparse-k helper. Exact target-mode matching tolerance remains unchanged.

## Evaluation
The same workflow must first reproduce `C3_CLASS_ETA0_ZERO_COUPLING_PASS`, then build the signed-lambda reference, then evaluate the unchanged original C3 gate. Finite positive eta remains unlicensed regardless of outcome.
