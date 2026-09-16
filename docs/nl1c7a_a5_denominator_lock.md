# NL1C7A A5 denominator audit lock

Status: **PRE-DATA / LOCKED BEFORE OFFICIAL A5 RESULT**

Parent certified A4:
- run `35104087182`
- head `0762723606536b58b7db39d41608fcaefe8eebd4`
- artifact `10450205501`
- artifact SHA256 `9b1a4f998af55ce594cbdd6db78b9b99944cd25a3f690c68bab49ffef290ffc6`
- classification `NL1C7A_NATIVE_TRACE_COVERAGE_PASS`

Frozen A5 implementation blob:
- `nl1c7a/a5_denominator_audit.py`
- blob SHA `47b486ca2defbd1db029df003b37909a9d4d170d`

Frozen A5 settings are those in `docs/nl1c7a_predata_growing_mode_bridge.md`:
- `a_i=0.02`
- scales `[5,10,20] h^-1 Mpc`
- quadrature supports `256/512`
- target-weight activity cut `1e-10` of peak
- forbidden relevant denominator floor `|T_delta_b| < 1e-12 max|T_delta_b|`
- primary time interpolation PCHIP in ln(a)
- primary k interpolation PCHIP in ln(k)
- no clipping, node deletion, extrapolation, interpolation-based node replacement, or post-result scale selection.

The A5 official workflow may only read the frozen Repair05 artifact and run the frozen A5 implementation. It does not re-run CLASS and does not license A6-A10 or nonlinear evolution.
