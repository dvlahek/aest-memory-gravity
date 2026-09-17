# NL1C7A Repair01 evaluator-interface fix lock

Status: **LOCKED BEFORE RE-EVALUATION OF THE DENSE TRACE**

Historical dense-time run `35149865129` produced a valid denser exact-k trace but the Repair01 evaluator stopped before A5 because the frozen A5 script expects the historical metadata field `repair05.interpolation_used`, while the dense coverage file records the same diagnostic fact under `repair01.interpolation_used`.

This is an evaluator metadata-interface mismatch only. It is not a transfer-zero result and no A5-A10 science gate was evaluated in that run.

Frozen parent artifact:

- run: `35149865129`
- head: `4a275f4777a7e487004f4783bc2a929a93ac8188`
- artifact: `10469031693`
- artifact SHA256: `193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`
- dense trace: 128/128 exact requested k modes, no interpolation or nearest-neighbour substitution
- native times: 179 (historical trace: 46)
- window around `a_i=0.02`: 9 native accepted times below and 16 above

The repair is restricted to creating a compatibility copy of the dense coverage JSON with

`repair05.interpolation_used = repair01.interpolation_used`

while preserving every existing dense-coverage field and value. The dense trace bytes are not modified. The compatibility copy must also retain `repair01` unchanged.

The original frozen A5 script `nl1c7a/a5_denominator_audit.py` and original frozen A6-A10 script `nl1c7a/a6_a10_spherical_reconstruction.py` must be executed unchanged on the exact retained dense trace. Their thresholds, interpolation methods, scale ladder, k grid, quadrature, and zero-norm rule remain unchanged.

No CLASS rerun, solver change, tolerance change, threshold change, k/time interpolation change, profile change, or physics change is allowed in this evaluator-interface repair.

The historical `NL1C7A_TIME_INTERPOLATION_CONTROL_FAIL` remains frozen and is not overwritten. The misleading `NL1C7A_REPAIR01_TRANSFER_ZERO_FAIL` label from run `35149865129` is retained as a historical technical evaluator result and must not be interpreted as an A5 science result because A5 terminated before computation.
